# Demo script (2-3 minutes)

Record only after a live run with real keys. Use the real output; do not stage results.

| Time | Show | Say |
|---|---|---|
| 0:00-0:15 | Streamlit app, empty | "Research Courtroom: a contested question gets a prosecution, a defense, and a judge who reads the evidence, not the arguments." |
| 0:15-0:45 | File a case (a genuinely contested question) | Both sides' claims with VERIFIED / NOT VERIFIED badges and clickable sources. |
| 0:45-1:10 | Open two source links; show the ledger entry (query, retrieval time) | "Every claim cites a ledger ID; unknown IDs are stripped, and a second model pass assesses whether the excerpt supports the claim. That assessment is an opinion, not proof." |
| 1:10-1:30 | Cross-examination + verdict | Point out unresolved items and any "Inconclusive" outcome. |
| 1:30-2:15 | Challenge one claim, submit a URL | Show fetch status, new evidence in the diff, and the reason the verdict changed or did not. "It never changes the verdict just because I push." |
| 2:15-2:40 | Failure case: nonsense question or blocked URL (`http://169.254.169.254/`) | Show the insufficient-evidence message / "blocked by safety checks". |
| 2:40-3:00 | README and tests | "Mocked test suite, opt-in live tests, Nebius Token Factory for inference, Tavily for search." |
