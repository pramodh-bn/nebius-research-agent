# RESEARCH COURTROOM
## Cinematic Hackathon Presentation Deck
**Team All Vibes · Solo Engineer: Pramodh Nanjayya**  
**ODSC × Nebius Hackathon Submission**

---

### SLIDE 1 — TITLE & MISSION
```
================================================================================
                           RESEARCH COURTROOM
                   Two Sides Argue. Evidence Decides.
================================================================================

              ODSC × Nebius Hackathon · Track: Research Agents
              Team: All Vibes  |  Creator & Sole Engineer: Pramodh Nanjayya
              Inference: Nebius Token Factory (Qwen/Qwen3-235B)
              Search: Tavily Live Web Retrieval
              Stack: Python FastAPI + React 19 / Vite / Tailwind
```

---

### SLIDE 2 — THE PROBLEM: THE CONSENSUS ILLUSION
```
================================================================================
THE PROBLEM: WHY AI RESEARCH SUMMARIES MISLEAD
================================================================================

[ The Status Quo ]
  • Single-agent summarizers flatten genuine scientific controversy into a 
    synthetic, one-sided "consensus".
  • Confident Hallucinations: Models invent plausible-sounding citations that 
    collapse upon verification.
  • Compliance Bias: When challenged by users, standard chatbots flip verdicts 
    without new evidence.

[ The Cost ]
  • In medicine, engineering, and policy, truth is not found in compromise.
  • It is found in adversarial scrutiny and evidence provenance.
```

---

### SLIDE 3 — THE INVENTIVE SOLUTION
```
================================================================================
THE SOLUTION: AN ADVERSARIAL COURTROOM
================================================================================

                      [ CONTESTED QUESTION ]
                                │
                        ┌───────▼───────┐
                        │ TAVILY SEARCH │ (2 targeted queries)
                        └───────┬───────┘
                                │
                     [ EVIDENCE LEDGER ]
               (Stable IDs, Hashed, Deduplicated)
                                │
               ┌────────────────┴────────────────┐
               ▼                                 ▼
      [ PROSECUTION COUNSEL ]          [ DEFENSE COUNSEL ]
      Affirmative Case Grounded        Counterarguments, Limits &
      in Admitted Citations            Adherence Boundaries
               │                                 │
               └────────────────┬────────────────┘
                                │
                      [ CROSS-EXAMINATION ]
                  Direct Examination on Veracity
                                │
                        [ VERIFIER PASS ]
                  Independent Claim Excerpt Audit
                                │
                        [ JUDICIAL RULING ]
               Impartial Verdict · Forced Inconclusive
```

---

### SLIDE 4 — CITATION INTEGRITY & VERIFICATION
```
================================================================================
ENGINEERING INTEGRITY: AGENTS NEVER GRADE THEIR OWN HOMEWORK
================================================================================

1. Citation Validation
   • Hallucinated citation IDs (e.g., citing 'E99' when only E1-E8 exist) are 
     pruned programmatically by code before rendering.

2. The Dedicated Verifier Pass
   • A distinct model call on Nebius Token Factory receives ONLY:
     - The extracted claim sentence
     - The raw excerpt text (max 2,400 chars)
   • Labels: Supported · Partially Supported · Contradicted · Unsupported

3. Invariant: Forced Inconclusiveness
   • If no verdict claim meets verified evidentiary support, the judge's 
     discretion is overridden by code to rule "Inconclusive".
```

---

### SLIDE 5 — LIVE DELIBERATION STREAMING (SSE)
```
================================================================================
LIVING DOCUMENT: REAL-TIME STREAMING ARCHITECTURE
================================================================================

[ Client ] <==== Server-Sent Events (SSE) ==== [ FastAPI Backend ]
  React 19                                        Nebius Reasoner + Tavily

• Phase 1: Live Discovery  --> Ticker streams queries; Ledger counter increments.
• Phase 2: Prosecution     --> Left column auto-populates claims & verification badges.
• Phase 3: Defense         --> Right column auto-populates rebuttals & limitations.
• Phase 4: Cross-Exam      --> Counsel exchange thread expands live.
• Phase 5: Verdict Pop-Up  --> Instant judicial announcement modal fires.
```

---

### SLIDE 6 — INTERACTIVE RECONSIDERATION & SSRF HARDENING
```
================================================================================
CROSS-EXAMINING THE COURT: RESILIENT ADMISSION
================================================================================

[ User URL & Challenge Submission ]
  ├── 1. SSRF Safety Gate (src/courtroom/fetch.py)
  │      • HTTP/HTTPS only; Ports 80 & 443 only
  │      • Every resolved IP verified against private / loopback / cloud metadata
  │      • BLOCKED: http://169.254.169.254/latest/
  │      • Re-verified on up to 3 redirects; 1 MB size cap; 5s timeout
  │
  ├── 2. Delta Revision Tracking
  │      • Before vs. After decision comparison
  │      • Verified claim count delta
  │      • Explicit reason: "4 new sources added" vs "No new evidence added"
  │
  └── 3. Intellectual Honesty
         • The court REFUSES to flip its verdict under user pressure unless 
           new evidence genuinely justifies reconsideration.
```

---

### SLIDE 7 — THE VERDICT ANNOUNCEMENT POP-UP
```
================================================================================
THE VERDICT POP-UP: INSTANT RULING CONVERGENCE
================================================================================

┌──────────────────────────────────────────────────────────────────────────────┐
│  ⚖️ JUDICIAL RULING ANNOUNCED                                                │
│  The Verdict Has Been Reached                                    [RC-4821]   │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │ COURT RULING: INCONCLUSIVE                                             │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  Reasoning Excerpt:                                                          │
│  "Randomized trials demonstrate equivalent weight loss between intermittent  │
│  fasting and calorie restriction over 12 months. Superiority beyond one year  │
│  remains unresolved."                                                        │
│                                                                              │
│  [ 8 Evidence Sources ]   [ 6 Verified Claims ]   [ 3 Unresolved Questions ]  │
│                                                                              │
│                         [ Dismiss ]  [ Review Full Verdict ]                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### SLIDE 8 — EMPIRICAL VERIFICATION & TEST SUITE
```
================================================================================
TEST RIGOR: 56 AUTOMATED TESTS PASSING IN < 1 SECOND
================================================================================

Test Suite                  Tests    Passing    Coverage Area
─────────────────────────────────────────────────────────────────────────────
tests/test_core.py            16       100%     Dual-counsel, judge, bounds
tests/test_evidence.py        16       100%     Citation integrity, dedup
tests/test_engine.py          20       100%     Cross-exam, call budgets
tests/test_reconsideration.py 52       100%     SSRF gate, delta tracking
tests/test_api.py             56       100%     FastAPI SSE & sync endpoints
─────────────────────────────────────────────────────────────────────────────
Total Automated Tests:        56       100%     Runtime: 0.56 seconds
```

---

### SLIDE 9 — HARDWARE & COMPONENT BUDGET
```
================================================================================
EXECUTION BUDGET: HARD-CAPPED PREDICTABILITY
================================================================================

Operation           Model Calls    Token Budget    Search Calls    Latency
─────────────────────────────────────────────────────────────────────────────
Initial Trial       8 calls        ~12k tokens     2 queries       ~25s
User Challenge      6 calls        ~8k tokens      1 query         ~18s
Hard Limit          16 max calls   Strict cap      3 max queries   Guaranteed

• Model Injected: Qwen/Qwen3-235B-A22B-Instruct-2507 on Nebius Token Factory
• Zero recursive runaway loops. Deterministic call budget.
```

---

### SLIDE 10 — CONCLUSION: ONE ENGINEER, ONE VISION
```
================================================================================
ALL VIBES · RESEARCH COURTROOM
================================================================================

"The future of AI research is not about synthetic consensus.
 It is about verifiable truth."

• Built by a solo engineer: Pramodh Nanjayya
• Tested. Verified. Hardened.
• Live UI: http://localhost:3000
• API Docs: http://localhost:8000/docs
• Repository: nebius-research-agent
```
