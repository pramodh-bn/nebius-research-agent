# Test report

Environment: Windows, Python 3.15, pytest 8.

## Automated (mocked, deterministic)
Command: `python -m pytest -q` -> **52 passed** (live tests skipped without keys).

Covered: empty question; empty search results; search failure; duplicate sources (URL and content); stable IDs; fabricated citation IDs; malformed claim structure; unsupported / contradicted / insufficient claims downgraded; partial support labeling; verifier failure never yields "verified"; malformed model JSON with retry, and persistent failure; model call budget; cross-examination with fabricated IDs and invalid askers; forced "Inconclusive"; prompt-injection flagging and delimiter neutralization; SSRF blocking (schemes, localhost, private/link-local/IPv6/mapped addresses, credentials, ports, internal names, hostnames resolving to private IPs, redirects to private hosts, redirect loops); size, content-type, status and timeout limits; changed verdict, unchanged verdict, change-without-evidence flag; fetched, duplicate, blocked and search-hint URL paths; non-HTTP URL and empty challenge rejection.

## Other checks
- Starter CLI `src/agent.py`: imports and exposes `research` with dummy keys (no network call made).
- Secret scan of tracked files: no keys found; `.env` is untracked and git-ignored.
- Fresh-clone test: see the final run recorded in the git history message of the submission branch / below.

## Not verified
- **Live Nebius and Tavily calls: not run** (no API keys were available). Opt-in test: `tests/test_live.py` (`RUN_LIVE=1` plus both keys).
- **Streamlit UI not run interactively**; a headless `AppTest` hung in this environment, so UI code is only syntax-checked.
- Starter CLI answer quality against live services.

## Known limitations
- Claim verification is an LLM assessment, not proof; it can be wrong.
- Only the first 2400 characters of any source are kept and verified.
- DNS rebinding is only partly mitigated; no PDF fetching.
- Tavily search is the only retrieval path for non-URL evidence; 2 initial queries and 1 follow-up per challenge.
