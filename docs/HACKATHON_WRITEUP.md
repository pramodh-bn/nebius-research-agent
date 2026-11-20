# RESEARCH COURTROOM: Adversarial Multi-Agent Scientific Jurisprudence
### Official Hackathon Submission & Technical Whitepaper
**ODSC × Nebius Hackathon · Track: Research Agents**  
**Team:** All Vibes  
**Creator & Sole Engineer:** Pramodh Nanjayya  
**Repository:** [github.com/allvibes/nebius-research-agent](https://github.com/allvibes/nebius-research-agent)  
**Live Stack:** FastAPI (SSE Deliberation Engine) + React 19 / Vite UI + Nebius Token Factory (Qwen-2.5 Reasoner) + Tavily Web Search

---

## 1. Executive Summary

When ordinary AI systems are asked a contested, multi-faceted scientific question—such as whether intermittent fasting is superior to continuous calorie restriction, or whether ultra-processed foods cause depression independently of caloric intake—they almost invariably produce a **"consensus illusion."** They flatten deep clinical trial contradictions into a polite, homogenized, and often hallucinated compromise. Worse, when challenged by a user, standard conversational agents exhibit compliance bias, reversing their conclusions arbitrarily without evidentiary support.

**Research Courtroom** reimagines automated research through the lens of **adversarial jurisprudence**. Instead of a single LLM attempting to synthesize truth in a vacuum, Research Courtroom constructs an impartial judicial trial:
1. **The Prosecution Counsel** presents the affirmative case grounded strictly in admitted evidence.
2. **The Defense Counsel** challenges study duration, sample bias, protocol heterogeneity, and adverse effects.
3. **An Independent Reasoner (Nebius Qwen-2.5)** audits every extracted claim against the raw source excerpts before any verdict is rendered.
4. **The Impartial Judge** synthesizes a formal judicial ruling. If no claim survives evidentiary verification, the system is **forced by code invariant** to rule *Inconclusive*.
5. **Interactive Cross-Examination:** Users can challenge the court with new evidence or alternative theories. Hardened Server-Side Request Forgery (SSRF) protections ensure security against cloud metadata theft (`169.254.169.254`) and private network probing.

---

## 2. The Core Problem: The Consensus Illusion

Modern conversational AI suffers from four fundamental failure modes when deployed for scientific research:

| Failure Mode | How Standard AI Behaves | How Research Courtroom Solves It |
| :--- | :--- | :--- |
| **Consensus Illusion** | Collapses conflicting clinical trial outcomes into a bland, false compromise. | Pits two specialized adversarial agents (Prosecution & Defense) against each other with opposing evidentiary burdens. |
| **Hallucinated Citations** | Synthesizes plausible-looking PubMed IDs, journal citations, and author names that do not exist. | Cryptographic evidence ledger hashes and seals Tavily search excerpts; hallucinated citations are pruned programmatically by code. |
| **Self-Grading Homework** | The same model generating the summary verifies its own output, hiding its biases. | Multi-agent separation: The verifier is a distinct, zero-shot model invocation evaluating only claim-versus-excerpt truth value. |
| **Compliance Flipped Verdicts** | Flips its answer when a user pushes back, regardless of whether new evidence is supplied. | Structured Bayesian trial reconsideration: Verdicts require verified evidentiary updates; user challenges with malicious URLs are rejected by hardened SSRF filters. |

---

## 3. System Architecture & Technical Implementation

```
                                  [ USER CONTESTED QUESTION ]
                                               │
                                     ┌─────────▼─────────┐
                                     │   TAVILY SEARCH   │ (Targeted Pro & Con Queries)
                                     └─────────┬─────────┘
                                               │
                                   [ EVIDENCE LEDGER (E1..En) ]
                                (Hashed, Deduplicated, Sanitized)
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
            [ PROSECUTION COUNSEL ]                         [ DEFENSE COUNSEL ]
          Affirmative Case Grounded                       Methodological Limits,
           in Admitted Citations                        Confounders & Discrepancies
                       │                                               │
                       └───────────────────────┬───────────────────────┘
                                               │
                                    [ CROSS-EXAMINATION ]
                               Rebuttal on Veracity & Study Scope
                                               │
                                     [ INDEPENDENT AUDIT ]
                           (Nebius Qwen Reasoner Verifies Each Claim)
                                               │
                                    [ JUDICIAL VERDICT ]
                          Formal Matrix Ruling or Forced Inconclusive
                                               │
                                 [ SERVER-SENT EVENTS (SSE) ]
                          Live Deliberation Stream pushed to React UI
```

### 3.1 Nebius Token Factory Integration
Research Courtroom leverages the **Nebius AI Studio** inference infrastructure utilizing **Qwen/Qwen2.5-Coder-32B-Instruct** and **Qwen/Qwen3-235B**:
- **Prompt Engineering with Structured Schema Enforcers:** Model outputs are strictly constrained to typed Pydantic data contracts.
- **Latency Optimization:** Real-time token generation streams deliberation events over SSE directly into the user interface.
- **Dedicated Auditor Role:** A distinct model call on Nebius receives only the extracted claim sentence and raw source text (capped at 2,400 characters), returning categorical labels: `Supported`, `Partially Supported`, `Contradicted`, or `Unsupported`.

### 3.2 Live Deliberation Streaming Engine (FastAPI SSE)
Rather than making users wait for an entire trial to complete behind a loading spinner, Research Courtroom provides a **live document deliberation stream** (`/api/case/stream` and `/api/challenge/stream`):
- Pushes granular status events: `search_started`, `evidence_admitted`, `prosecution_drafting`, `defense_drafting`, `cross_exam_deliberating`, `verdict_reached`.
- Streams claims live into the React document view as counsel drafts them.
- Emits an instant **Judicial Ruling Pop-Up Dialog** the moment the judge closes the trial, allowing researchers to immediately review findings and unresolved questions.

### 3.3 Security & Hardening: Defeating SSRF
When an interactive system allows users to provide reference URLs for reconsideration, it creates a high-risk attack vector for **Server-Side Request Forgery (SSRF)**. Research Courtroom incorporates defense-in-depth:
1. **Cloud Metadata IP Blocking:** Rejects `169.254.169.254` (AWS/GCP/Azure instance metadata), `127.0.0.1`, `::1`, and RFC 1918 private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).
2. **DNS Rebinding Prevention:** Resolves domain names to IP addresses prior to socket binding and inspects the resolved address before initiating outbound HTTP requests.
3. **Protocol Sanitization:** Restricts requests exclusively to `http://` and `https://` schemas, forbidding `file://`, `gopher://`, or unix domain sockets.

---

## 4. Verification & Automated Test Suite

Research Courtroom was developed following strict Test-Driven Development (TDD) discipline.

- **Total Automated Tests:** 56 passing tests across 5 test suites.
- **Execution Speed:** Full test suite executes in under 25 seconds.
- **Test Categories:**
  - `test_courtroom_flow.py`: Full end-to-end trial lifecycle, citation integrity, and verifier pass.
  - `test_reconsideration.py`: Challenge submission, evidence revision tracking, and verdict stability.
  - `test_ssrf_security.py`: Malicious IP rejection, loopback blocking, and DNS rebinding defenses.
  - `test_evidence_hashing.py`: SHA-256 deduplication and citation formatting guarantees.
  - `test_live_stream.py`: SSE protocol compliance, event sequence, and payload serialization.

```bash
$ python -m pytest -q
........................s................................                [100%]
56 passed, 1 skipped in 24.64s
```

---

## 5. Hackathon Evaluation Criteria Alignment

| Criteria | Hackathon Expectation | Research Courtroom Delivery |
| :--- | :--- | :--- |
| **Technical Novelty** | Innovative agent architecture beyond basic RAG | Adversarial Tripartite Jurisprudence (Prosecution vs. Defense + Independent Verifier + Inconclusive Invariant). |
| **Nebius Platform Usage** | Meaningful integration with Nebius infrastructure | Powers multi-agent deliberation, cross-examination rebuttals, and high-precision verification audits via Nebius Token Factory. |
| **Completeness & Polish** | End-to-end working software with UI | Full-stack implementation: FastAPI SSE backend + React 19 / Tailwind / Vite UI + dark-mode courtroom design + live stream feed + verdict pop-up dialog. |
| **Reliability & Security** | Defenses against hallucinations and vulnerabilities | 56 passing automated tests, cryptographic evidence hashing, anti-hallucination citation pruning, and RFC 1918 / Cloud Metadata SSRF protections. |
| **Presentation & Story** | Compelling demonstration and clear vision | 1080p cinematic presentation film, interactive HTML keynote slides, authentic screen recording, and creator-narrated title reveal. |

---

## 6. Credits & Team

- **Team:** All Vibes
- **Creator & Sole Engineer:** Pramodh Nanjayya
- **Submission Date:** November 20, 2026
- **License:** MIT
