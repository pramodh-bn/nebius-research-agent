# Baseline (Stage 0)

Date: 2026-11-18. Branch flow: `feature/*` → `dev` → `main` (main only when all work is done).

## What exists
- **Starter CLI** (`src/agent.py`): Tavily search → Nebius (OpenAI-compatible) synthesis with `[n]` citations. Unchanged. Reads `NEBIUS_API_KEY`/`TAVILY_API_KEY` at import time (fails with `KeyError` if missing).
- **Overlay** (merged in `dev`): `app.py` (Streamlit UI), `src/courtroom/core.py` (`Evidence`, `Case`, `Search`/`Reasoner` protocols, `TavilySearch`, `NebiusReasoner`, `validate_claims`, `Courtroom`), `tests/test_core.py`.
- `requirements.txt` = starter deps + streamlit, requests, pydantic, pytest.

## Verified
- `python -m pip install -r requirements.txt` succeeded (Python 3.15).
- `python -m pytest -q` → 3 passed.

## Not verified
- Streamlit app not launched; starter CLI not run.
- No live Nebius or Tavily calls (no keys used).

## Known limitations / discrepancies
- Claim checking validates citation IDs only, not semantic support.
- User URLs are search hints only; no bounded fetch or SSRF protection.
- No source dedup, retrieval timestamps/query metadata, or prompt-injection boundaries beyond the starter prompt wording.
- Default model differs: starter/.env.example use `meta-llama/Llama-3.3-70B-Instruct`; `app.py` falls back to `meta-llama/Meta-Llama-3.1-70B-Instruct`. Starter hardcodes base URL; overlay reads `NEBIUS_BASE_URL`.
- Only 3 tests; none cover malformed JSON, timeouts, empty results, or injection.
- README and SUBMISSION_CHECKLIST still hold official placeholders.
