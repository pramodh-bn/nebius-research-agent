#!/usr/bin/env python3
"""Gamma App Presentation Deck Generator & Speaker Script Assistant.

Use this script to inspect, export, or generate slide prompts tailored for Gamma App (https://gamma.app).

Usage:
    python scripts/generate_gamma_deck.py --export gamma_deck.md
    python scripts/generate_gamma_deck.py --speakers
    python scripts/generate_gamma_deck.py --summary
"""

import argparse
from pathlib import Path
import sys

DECK_FILE = Path(__file__).resolve().parent.parent / "docs" / "GAMMA_SLIDES_PROMPT.md"

SLIDES_DATA = [
    {
        "num": 1,
        "title": "Research Courtroom: Two Sides Argue. Evidence Decides.",
        "duration_sec": 18,
        "key_points": [
            "ODSC × Nebius Hackathon presentation",
            "Sole Engineer: Pramodh Nanjayya · Team All Vibes",
            "Nebius Token Factory (Qwen-2.5) + Tavily Live Search",
        ],
        "script": "Welcome. I am Pramodh Nanjayya from Team All Vibes, presenting Research Courtroom for the ODSC Nebius Hackathon. We built an AI research agent based on a simple realization: when science is contested, truth is not a polite consensus. Truth is discovered when opposing sides cross-examine real evidence under strict judicial scrutiny."
    },
    {
        "num": 2,
        "title": "The Crisis of Polite Consensus (The Cost of False Certainty)",
        "duration_sec": 24,
        "key_points": [
            "Why conventional AI research summaries mislead in clinical science",
            "Study A (40 pts, 8 wks) vs. Study B (500 pts, 18 mos)",
            "Standard chatbots hallucinate polite compromise instead of rigorous truth",
        ],
        "script": "Why does this project exist? When you ask standard AI a clinical research question, it gives you a polite, false agreement. Study A used 40 patients for 8 weeks and claimed success. Study B used 500 patients for 18 months and showed the opposite. Standard chatbots blur them together into dangerous false certainty. In medicine and science, that false certainty costs lives."
    },
    {
        "num": 3,
        "title": "The Paradigm Shift: From Search Query to Courtroom Trial",
        "duration_sec": 20,
        "key_points": [
            "Search to Courtroom pipeline diagram",
            "Two dedicated advocates (Prosecution vs. Defense)",
            "Independent auditor & Judicial Bench on Nebius",
        ],
        "script": "Instead of treating deep research like an open-ended autocomplete query, Research Courtroom structures inquiry into an adversarial trial. Two opposing AI agents battle over admitted evidence, audited by an independent Nebius reasoner before the Judge delivers a binding verdict."
    },
    {
        "num": 4,
        "title": "Tripartite Jurisprudence (Autonomous Role Specialization)",
        "duration_sec": 22,
        "key_points": [
            "Prosecution: Affirmative grounding with mandatory [E1] citations",
            "Defense: Methodological limits, confounders, and contraindications",
            "Judicial Bench: Courage to rule Inconclusive",
        ],
        "script": "Our architecture enforces tripartite separation: Prosecution argues for the claim; Defense argues against it; and the Judicial Bench evaluates both sides against strict evidentiary standards. The Judge holds the courage to rule Inconclusive whenever evidence fails to meet the burden of proof."
    },
    {
        "num": 5,
        "title": "Defensive Invariants & Engineering Rigor",
        "duration_sec": 20,
        "key_points": [
            "Zero hallucinated citation IDs permitted",
            "Hardened SSRF firewall against cloud metadata theft",
            "56 automated passing backend tests",
        ],
        "script": "We engineered strict defensive invariants. If an agent tries to hallucinate a citation like 'E99', the system prunes it automatically. If a user tries to inject a cloud metadata address during cross-examination, our SSRF defense refuses the connection cold. Fifty-six automated tests ensure these guarantees hold."
    },
    {
        "num": 6,
        "title": "The Live Courtroom Experience (Transparency & Auditability)",
        "duration_sec": 18,
        "key_points": [
            "Real-time Server-Sent Events (SSE) deliberation stream",
            "Interactive citation drawer with exact cryptographic excerpts",
            "Instant ruling announcement modal with verified claim counts",
        ],
        "script": "When a case is filed, the user watches the courtroom in real time. Counsel drafts live before your eyes, citations link directly to cryptographic excerpt receipts, and the full judicial deliberation unfolds with complete auditability."
    },
    {
        "num": 7,
        "title": "Validation & Empirical Results on Contested Inquiries",
        "duration_sec": 20,
        "key_points": [
            "Intermittent fasting vs. calorie restriction evaluated",
            "No compromise bias: Inconclusive verdict accurately rendered",
            "100% citation excerpt grounding",
        ],
        "script": "Here are the empirical results across contested trials. In every case, the courtroom refused to generate synthetic consensus. When clinical trials showed equal weight loss at 12 months, the court ruled Inconclusive, citing exact evidence receipts."
    },
    {
        "num": 8,
        "title": "Grand Finale & Call To Action",
        "duration_sec": 18,
        "key_points": [
            "Punchline: 'Truth is not a compromise. Put the science on trial.'",
            "github.com/pramodh-bn/nebius-research-agent",
            "ODSC × Nebius Hackathon 2026",
        ],
        "script": "The future of AI research isn't about asking an LLM to hallucinate a polite compromise. It is about building systems that can prove the work is right. Truth is not a compromise. Put the science on trial. Thank you."
    },
]

def main():
    parser = argparse.ArgumentParser(description="Gamma App Presentation Deck Assistant")
    parser.add_argument("--export", type=str, help="Export prompt file to custom destination")
    parser.add_argument("--speakers", action="store_true", help="Print slide-by-slide speaker script with timings")
    parser.add_argument("--summary", action="store_true", help="Print slide titles and key points summary")
    args = parser.parse_args()

    if args.export:
        out_p = Path(args.export)
        out_p.write_text(DECK_FILE.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"✅ Exported Gamma App deck prompt to {out_p.resolve()}")
        return

    if args.speakers:
        total_time = sum(s["duration_sec"] for s in SLIDES_DATA)
        print("\n🎙️ SLIDE-BY-SLIDE SPEAKER SCRIPT & PACING GUIDE")
        print(f"Total Slides: {len(SLIDES_DATA)} | Estimated Runtime: {total_time}s (~{total_time // 60}m {total_time % 60}s)\n" + "=" * 70)
        for s in SLIDES_DATA:
            print(f"\n[Slide {s['num']}] {s['title']} ({s['duration_sec']}s)")
            print(f'"{s["script"]}"')
        print("\n" + "=" * 70)
        return

    if args.summary:
        print("\n📋 RESEARCH COURTROOM — 8-SLIDE DECK OVERVIEW")
        for s in SLIDES_DATA:
            print(f"\nSlide {s['num']}: {s['title']}")
            for p in s["key_points"]:
                print(f"  • {p}")
        return

    # Default action: print instructions and file location
    print(f"""
================================================================================
🚀 GAMMA APP (gamma.app) PRESENTATION GENERATOR PROMPT READY!
================================================================================

Prompt File Location:
  {DECK_FILE}

How to generate in Gamma App:
  1. Open https://gamma.app in your browser.
  2. Click 'New with AI' -> Choose 'Paste in text' (or 'Import').
  3. Select 'Presentation' (16:9 widescreen).
  4. Theme suggestion:
     'Dark Mode Executive / Legal Tech: Deep Obsidian (#0B0F19), Slate Navy (#0F172A),
      and Polished Gold (#F59E0B) with luminous cyan badges and glassmorphism cards.'
  5. Copy and paste the contents of docs/GAMMA_SLIDES_PROMPT.md.

CLI Options:
  python scripts/generate_gamma_deck.py --speakers  (Print speaker script & timings)
  python scripts/generate_gamma_deck.py --summary   (Print slide-by-slide summary)
  python scripts/generate_gamma_deck.py --export <path> (Export to file)
================================================================================
""")

if __name__ == "__main__":
    main()
