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
- **Not yet implemented:** direct URL fetch with SSRF protection and the before/after evidence diff (Stage 3).
