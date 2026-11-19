# Research Courtroom

> ODSC × Nebius Hackathon submission · Challenge: *Build a research agent that brings its sources*

**One-line pitch:** Contested research questions, argued by a prosecution and defense from cited web evidence and ruled on by an impartial judge, for anyone who needs a verifiable answer rather than a one-sided summary.

- **Demo video (2–3 min):** _TODO: add link after recording (script: `docs/DEMO_SCRIPT.md`)_
- **Team:** _TODO: names / GitHub handles_

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
| Nebius Token Factory (inference) | Model: `meta-llama/Llama-3.3-70B-Instruct` (configurable via `NEBIUS_MODEL`) — arguments, cross-examination, judge and claim verifier, via the OpenAI-compatible endpoint |
| Tavily (real-time web search) | Retrieves the evidence ledger; each result's URL and excerpt are stored and shown as clickable links in the UI and in verdict citations |

## Setup
```bash
git clone <repo-url>
cd <repo>
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # add your keys — never commit them
streamlit run app.py                                 # Research Courtroom UI
python src/agent.py "Your research question here"    # original starter CLI
python -m pytest -q                                  # mocked tests (no keys needed)
RUN_LIVE=1 python -m pytest -q tests/test_live.py    # optional live smoke test (needs both keys)
```

## Example
_TODO: paste a real run after a live test with API keys. No example is included yet because live Nebius/Tavily calls have not been run; nothing here is invented._

## Failure / insufficient-evidence case
Verified in mocked tests (`docs/TEST_REPORT.md`); to be shown live in the demo:
- Search returns nothing: the case is refused with "No retrievable evidence".
- A claim cites an ID not in the ledger: the ID is removed and the claim shows as unsupported / not verified.
- Verifier fails or no verdict claim is verified: verdict reads "Inconclusive (insufficient verified evidence)".
- Submitted URL is private or fails to load: blocked, or results labeled as unverified search hints.

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
