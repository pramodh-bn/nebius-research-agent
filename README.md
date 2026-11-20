# Research Courtroom

> ODSC × Nebius Hackathon submission · Challenge: *Build a research agent that brings its sources*

**One-line pitch:** Contested research questions, argued by a prosecution and defense from cited web evidence and ruled on by an impartial judge, for anyone who needs a verifiable answer rather than a one-sided summary.

- **Demo video (3 min):** [YouTube (1080p)](https://youtu.be/Ie_6eDqACPk) · `https://youtu.be/Ie_6eDqACPk`
- **Team:** All Vibes · Pramodh Nanjayya ([@pramodh-bn](https://github.com/pramodh-bn))

## The problem
Researchers and curious users facing disputed questions. A single synthesized answer hides the opposing case. Research Courtroom surfaces both sides, grounds every claim in an evidence ledger, checks whether the cited excerpt really supports the claim, and lets the user challenge the verdict. It can answer "inconclusive" and says why.

## How it works
```
question → 2 Tavily searches → evidence ledger → prosecution → defense → cross-examination → judge → verdict
                                    ↑                  (each output: citation check → claim verification)
                                    └── challenge a claim / submit a URL → follow-up retrieval → re-judge → traceable revision
```
- **Query planning:** two fixed queries (supporting / counterarguments) per case, one follow-up per challenge. Model calls are capped (8 per case, 6 per challenge, hard limit 16, one retry each).
- **Evidence handling:** every source has a stable ID, URL, title, exact excerpt, query, retrieval time and provider metadata. Duplicates are removed by normalized URL and content hash. Unknown citation IDs are stripped; a separate verifier pass labels each claim `supported`, `partially_supported`, `contradicted`, `unsupported` or `insufficient_evidence`. That label is an LLM assessment, not proof. If nothing in the verdict is verified, the decision is forced to *Inconclusive*.
- **Safety:** retrieved text, user URLs and user challenges are untrusted data, fenced in delimiters and never treated as instructions; injection-like excerpts are flagged. User URLs are fetched with SSRF protections (public hosts only, http(s), size/time limits, redirect re-checks) or clearly labeled as unverified search hints. Fetched pages are verified like any other source.
- **Trade-offs:** about 8 model calls per case (latency and cost) for stronger citation integrity; only the first 2400 characters of each source are kept.

More detail: `docs/ARCHITECTURE.md`, `docs/BASELINE.md`, `docs/TEST_REPORT.md`.

## Required services
| Requirement | How we use it |
|---|---|
| Nebius Token Factory (inference) | Model: `Qwen/Qwen3-235B-A22B-Instruct-2507` (configurable via `NEBIUS_MODEL`; the catalog changes, so check `GET /v1/models`) — arguments, cross-examination, judge and claim verifier, via the OpenAI-compatible endpoint |
| Tavily (real-time web search) | Retrieves the evidence ledger; each result's URL and excerpt are stored and shown as clickable links in the UI and in verdict citations |

## Setup
```bash
git clone <repo-url>
cd <repo>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # add your keys — never commit them
python run_app.py                                    # Full stack: React Web UI (:3000) + FastAPI (:8000)
streamlit run app.py                                 # Lightweight Streamlit UI (:8501)
python src/agent.py "Your research question here"    # original starter CLI
python -m pytest -q                                  # mocked tests (no keys needed)
RUN_LIVE=1 python -m pytest -q tests/test_live.py    # optional live smoke test (needs both keys)
```

## Example
Real run (2026-11-19, Nebius `Qwen/Qwen3-235B-A22B-Instruct-2507` + Tavily; 8 model calls, 8 sources):

**Question:** Does intermittent fasting improve long-term weight loss compared with calorie restriction?
**Verdict:** "Intermittent fasting does not consistently improve long-term weight loss compared to calorie restriction; the majority of evidence shows comparable outcomes." Every verdict claim cited ledger IDs and was assessed `supported` or `partially_supported` by the verifier (an LLM opinion, not proof). The judge kept the 4:3 fasting result (E3) as *contested* and listed three unresolved questions (protocol-specific benefits, adherence beyond one year, whether metabolic gains become durable weight loss).
**Sources (excerpt):** E3 news.cuanschutz.edu · E4 hsph.harvard.edu · E5 nature.com · E7 pmc.ncbi.nlm.nih.gov · see all 8 in the UI ledger.
**Challenge:** "Is there newer evidence from trials longer than 12 months?" → 4 new sources (E9–E12) added; verdict unchanged. Note: in this run the model's own explanation claimed no new evidence was added; the app now prefixes the revision reason with the factual count of new sources.

## Failure / insufficient-evidence case
Verified in mocked tests (`docs/TEST_REPORT.md`); to be shown live in the demo:
- Search returns nothing: the case is refused with "No retrievable evidence".
- A claim cites an ID not in the ledger: the ID is removed and the claim shows as unsupported / not verified.
- Verifier fails or no verdict claim is verified: verdict reads "Inconclusive (insufficient verified evidence)".
- Submitted URL is private or fails to load: blocked, or results labeled as unverified search hints. Live check: `http://169.254.169.254/latest/` was blocked ("not a public internet address") and neither fetched nor searched.
- Note: Tavily returns *something* even for nonsense queries, so live "no results" is rare; a nonsense query is not a reliable live failure demo. Use the blocked-URL case instead.

## Judging criteria map
| Criterion | Weight | Where to look |
|---|---|---|
| Sourced and verifiable answers | 30% | Evidence ledger, VERIFIED badges and source links in the UI; demo 0:15–1:30 |
| Works end to end | 25% | Setup, demo, mocked end-to-end tests |
| Usefulness | 20% | The problem |
| Agent design | 15% | How it works, `docs/ARCHITECTURE.md` |
| Use of Token Factory and Tavily | 10% | Required services |

## License
MIT
