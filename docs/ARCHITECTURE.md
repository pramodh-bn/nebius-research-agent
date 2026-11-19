# Architecture

```
question -> Tavily (2 queries) -> evidence ledger -> prosecution -> defense -> cross-examination -> judge -> verdict
                                       ^                 each output: validate citations -> verify claims
                                       +-- challenge: follow-up retrieval, re-argue, re-judge, record revision
```
- `src/courtroom/core.py`: all logic. `Search` and `Reasoner` are injected protocols (mocked in tests). `app.py`: Streamlit UI.
- **Ledger:** stable per-case IDs, URL + content dedup, retrieval time/query/provider metadata, injection flag. Excerpts are fenced as data.
- **Integrity:** `validate_claims` strips unknown IDs; `verify_claims` (separate model call) labels each cited claim supported / partially_supported / contradicted / unsupported / insufficient_evidence. This is an LLM assessment, not proof. Verifier failure => insufficient_evidence.
- **Judge:** sees ledger, both arguments and the cross-examination. If no verdict claim is verified, the decision is forced to "Inconclusive (insufficient verified evidence)" and the model's own decision is kept as `model_decision`.
- **Bounds:** one retry per model call (`max_attempts=2`), hard cap of 16 calls per operation (`max_calls`). A normal case uses 8 calls (args 2x2, cross-exam 2, judge 2); a challenge uses 6. Cross-exam is capped at 4 exchanges.
- **Reconsideration:** `challenge()` optionally targets one verdict claim, runs follow-up retrieval, and (if a URL is given) `admit_url()` fetches it via `fetch.py`: http(s) only, ports 80/443, no credentials, every resolved IP must be public (checked again on each of at most 3 redirects), text/HTML/plain only, 1 MB cap, 5s connect / 10s read timeouts. A fetched page enters the ledger (`provider=user_url_fetch`) and is verified like any source. Fetch failure falls back to search results labeled `search_hint` (not the submitted page); unsafe URLs are never fetched or searched. Each revision stores before/after decisions, evidence added, verified-claim counts and a reason; a change with no new evidence is flagged.
- **Limits:** DNS is validated before connecting but not pinned (DNS rebinding only partly mitigated); only the first 2400 characters of a fetched page are kept as the excerpt; no PDF support.
