"""FastAPI backend for Research Courtroom web UI.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from courtroom.core import Case, Courtroom, Evidence, NebiusReasoner, TavilySearch, CourtroomError

load_dotenv()

app = FastAPI(title="Research Courtroom API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_courtroom() -> Courtroom:
    nebius = os.getenv("NEBIUS_API_KEY")
    tavily = os.getenv("TAVILY_API_KEY")
    if not nebius or not tavily:
        raise HTTPException(status_code=500, detail="NEBIUS_API_KEY and TAVILY_API_KEY must be set in .env")
    return Courtroom(
        TavilySearch(tavily),
        NebiusReasoner(
            nebius,
            os.getenv("NEBIUS_MODEL", "Qwen/Qwen3-235B-A22B-Instruct-2507"),
            os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1"),
        ),
    )


def format_evidence(e: Evidence) -> dict[str, Any]:
    domain = ""
    try:
        domain = urlsplit(e.url).netloc.replace("www.", "")
    except Exception:
        domain = e.url
    origin = e.metadata.get("origin", "search")
    if e.provider == "user_url_fetch":
        origin = "user_url_fetch"
    return {
        "id": e.id,
        "title": e.title,
        "url": e.url,
        "domain": domain,
        "excerpt": e.excerpt,
        "query": e.query,
        "retrievedAt": e.retrieved_at,
        "origin": origin,
        "kind": "User submitted" if origin == "user_url_fetch" else "Live search",
        "untrusted": e.suspicious,
        "admitted": True,
        "metadata": e.metadata,
    }


def format_claims(raw_claims: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    claims = []
    for i, c in enumerate(raw_claims, 1):
        v = c.get("verification", {})
        status = c.get("status", "unsupported")
        claims.append({
            "id": f"{prefix}{i}",
            "text": c.get("text", ""),
            "status": status,
            "evidenceIds": c.get("sources", []),
            "verification": {
                "assessment": v.get("status", status),
                "verified": bool(c.get("verified", False)),
                "method": "llm",
                "note": v.get("explanation", "Verified against evidence ledger excerpts"),
            },
        })
    return claims


def format_revisions(raw_revs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    revs = []
    for i, r in enumerate(raw_revs, 1):
        added = [e["id"] if isinstance(e, dict) else str(e) for e in r.get("evidence_added", [])]
        revs.append({
            "id": i,
            "timestamp": "",
            "challenge": r.get("challenge", ""),
            "target": r.get("target_claim", "Whole verdict") or "Whole verdict",
            "beforeDecision": str(r.get("before_decision", "")),
            "afterDecision": str(r.get("after_decision", "")),
            "beforeVerified": r.get("verified_claims_before", 0),
            "afterVerified": r.get("verified_claims_after", 0),
            "evidenceAdded": added,
            "explanation": r.get("reason", ""),
            "status": "admitted" if r.get("decision_changed") else "sample",
            "urlStatus": r.get("url_status", "none"),
            "sourceUrl": r.get("source_url", ""),
        })
    return revs


def serialize_case_for_ui(case: Case) -> dict[str, Any]:
    prosecution_claims = format_claims(case.prosecution.get("claims", []), "P")
    defense_claims = format_claims(case.defense.get("claims", []), "D")
    verdict_claims = format_claims(case.verdict.get("claims", []), "V")
    evidence_list = [format_evidence(e) for e in case.evidence]

    # Raw dump for state persistence across challenges
    raw_dict = {
        "question": case.question,
        "evidence": [
            {
                "id": e.id,
                "title": e.title,
                "url": e.url,
                "excerpt": e.excerpt,
                "query": e.query,
                "retrieved_at": e.retrieved_at,
                "provider": e.provider,
                "content_hash": e.content_hash,
                "suspicious": e.suspicious,
                "metadata": e.metadata,
            }
            for e in case.evidence
        ],
        "prosecution": case.prosecution,
        "defense": case.defense,
        "verdict": case.verdict,
        "revisions": case.revisions,
        "warnings": case.warnings,
        "cross_exam": case.cross_exam,
        "calls_used": case.calls_used,
    }

    exchanges = []
    for x in case.cross_exam.get("exchanges", []):
        asker = x.get("asker", "prosecution").capitalize()
        exchanges.append({
            "side": asker,
            "question": x.get("question", ""),
            "answer": x.get("answer", ""),
            "ids": x.get("sources", []),
            "verified": x.get("verified", False),
        })

    return {
        "id": "RC-" + str(abs(hash(case.question)) % 10000).zfill(4),
        "question": case.question,
        "mode": "live",
        "decision": case.verdict.get("decision", "Inconclusive"),
        "verdict": case.verdict.get("reasoning", ""),
        "prosecution": prosecution_claims,
        "defense": defense_claims,
        "verdictClaims": verdict_claims,
        "prosecutionSummary": case.prosecution.get("summary", ""),
        "defenseSummary": case.defense.get("summary", ""),
        "prosecutionLimitations": case.prosecution.get("limitations", []),
        "defenseLimitations": case.defense.get("limitations", []),
        "unresolved": case.verdict.get("unresolved", []),
        "exchanges": exchanges,
        "evidence": evidence_list,
        "revisions": format_revisions(case.revisions),
        "warnings": case.warnings,
        "evidenceWarning": case.verdict.get("evidence_warning", ""),
        "callsUsed": case.calls_used,
        "_raw": raw_dict,
    }


def deserialize_case(raw: dict[str, Any]) -> Case:
    evidence = [
        Evidence(
            id=e["id"],
            title=e["title"],
            url=e["url"],
            excerpt=e["excerpt"],
            query=e["query"],
            retrieved_at=e.get("retrieved_at", ""),
            provider=e.get("provider", "tavily"),
            content_hash=e.get("content_hash", ""),
            suspicious=e.get("suspicious", False),
            metadata=e.get("metadata", {}),
        )
        for e in raw.get("evidence", [])
    ]
    return Case(
        question=raw.get("question", ""),
        evidence=evidence,
        prosecution=raw.get("prosecution", {}),
        defense=raw.get("defense", {}),
        verdict=raw.get("verdict", {}),
        revisions=raw.get("revisions", []),
        warnings=raw.get("warnings", []),
        cross_exam=raw.get("cross_exam", {}),
        calls_used=raw.get("calls_used", 0),
    )


class FileCaseRequest(BaseModel):
    question: str


class ChallengeRequest(BaseModel):
    case_raw: dict[str, Any]
    challenge: str
    source_url: str = ""
    target_claim: str = ""


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model": os.getenv("NEBIUS_MODEL", "Qwen/Qwen3-235B-A22B-Instruct-2507"),
        "base_url": os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1"),
    }


@app.post("/api/case")
def api_file_case(req: FileCaseRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Research question cannot be empty")
    court = get_courtroom()
    try:
        case = court.file_case(req.question.strip())
        return serialize_case_for_ui(case)
    except CourtroomError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}")


@app.post("/api/challenge")
def api_challenge(req: ChallengeRequest):
    if not req.challenge.strip() and not req.source_url.strip():
        raise HTTPException(status_code=400, detail="Challenge text or source URL required")
    court = get_courtroom()
    try:
        case = deserialize_case(req.case_raw)
        updated_case = court.challenge(
            case,
            question=req.challenge,
            source_url=req.source_url,
            target_claim=req.target_claim,
        )
        return serialize_case_for_ui(updated_case)
    except CourtroomError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {exc}")
