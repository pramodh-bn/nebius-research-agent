# Test report

Environment: Windows, Python 3.15, pytest 8.

## Automated (mocked, deterministic)
Command: `python -m pytest -q` -> **52 passed** (live tests skipped without keys).

Covered: empty question; empty search results; search failure; duplicate sources (URL and content); stable IDs; fabricated citation IDs; malformed claim structure; unsupported / contradicted / insufficient claims downgraded; partial support labeling; verifier failure never yields "verified"; malformed model JSON with retry, and persistent failure; model call budget; cross-examination with fabricated IDs and invalid askers; forced "Inconclusive"; prompt-injection flagging and delimiter neutralization; SSRF blocking (schemes, localhost, private/link-local/IPv6/mapped addresses, credentials, ports, internal names, hostnames resolving to private IPs, redirects to private hosts, redirect loops); size, content-type, status and timeout limits; changed verdict, unchanged verdict, change-without-evidence flag; fetched, duplicate, blocked and search-hint URL paths; non-HTTP URL and empty challenge rejection.

## Live checks (2026-11-19, real keys)
- `RUN_LIVE=1 python -m pytest -q tests/test_live.py` -> 1 passed (~38 s): full case with Tavily + Nebius `Qwen/Qwen3-235B-A22B-Instruct-2507` at `https://api.tokenfactory.nebius.com/v1`; all citations resolve; 8 model calls.
- Live challenge run: 6 calls, 4 new sources, verdict unchanged. Private-URL submission blocked.
- Found: `meta-llama/Llama-3.3-70B-Instruct` (starter default) is no longer in the account's model catalog and returns HTTP 403 on chat. The starter CLI `src/agent.py` was **not** live-tested and will fail unless `NEBIUS_MODEL` is set to an available model.
- Found: a live case showed the judge's `change_explanation` can misstate whether new evidence was added; fixed by computing the new-source count in code.
- A nonsense query still returned Tavily results, so the "no results" path was not triggered live.

## Other checks
- Starter CLI `src/agent.py`: imports and exposes `research` with dummy keys (no network call made).
- Secret scan of tracked files: no keys found; `.env` is untracked and git-ignored.
- Fresh-clone test: `git clone -b dev` of the local repo (commit 62042ea) into a temp directory, then `python -m pytest -q` -> 52 passed, 1 skipped. Dependencies were already installed in the environment, so `pip install -r requirements.txt` was not re-run in a clean virtualenv.

## Not verified
- **Streamlit UI not run interactively**; a headless `AppTest` hung in this environment, so UI code is only syntax-checked.
- Starter CLI against live services.

## Known limitations
- Claim verification is an LLM assessment, not proof; it can be wrong.
- Only the first 2400 characters of any source are kept and verified.
- DNS rebinding is only partly mitigated; no PDF fetching.
- Tavily search is the only retrieval path for non-URL evidence; 2 initial queries and 1 follow-up per challenge.
