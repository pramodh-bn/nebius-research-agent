# RESEARCH COURTROOM — GAMMA APP SLIDE DECK PROMPT & SCRIPT
> **How to use in Gamma App (gamma.app):**
> 1. In Gamma, click **"New with AI"** → select **"Paste in text"** (or **"Import"**).
> 2. Select **"Presentation"** (16:9 widescreen).
> 3. Choose **"Card by Card / Keep text exactly as provided"** or **"Summarize with AI"**.
> 4. Pick or describe theme: *"Dark Mode Executive / Legal Tech: Deep Obsidian (#0B0F19), Slate Navy (#0F172A), and Polished Gold (#F59E0B) with luminous cyan badges and glassmorphism cards."*
> 5. Paste the entire slide content below.

---

# Slide 1: Research Courtroom
### Two Sides Argue. Evidence Decides.
*ODSC × Nebius Hackathon · Track: Research Agents · Team All Vibes*  
*Sole Creator & Engineer: Pramodh Nanjayya*

- **Core Mission:** Putting contested scientific and medical questions on trial using adversarial jurisprudence.
- **Inference Engine:** Nebius Token Factory (Qwen-2.5 32B Reasoner)
- **Real-Time Discovery:** Tavily Live Search & Cryptographic Excerpt Hashing
- **Production Stack:** Python FastAPI + React 19 / Vite / Tailwind CSS

> **Speaker Script:**
> "Welcome. I am Pramodh Nanjayya from Team All Vibes, presenting Research Courtroom for the ODSC Nebius Hackathon. We built an AI research agent based on a simple realization: when science is contested, truth is not a polite consensus. Truth is discovered when opposing sides cross-examine real evidence under strict judicial scrutiny."

---

# Slide 2: The Crisis of Polite Consensus
### Why Conventional AI Research Summaries are Dangerous in High-Stakes Domains

- **The Illusion of Agreement:** Standard single-agent LLMs blend opposing medical studies into a smooth, synthetic compromise that satisfies neither reality.
- **The Asymmetry of Trials:**
  - *Study A:* 40 patients over 8 weeks claiming breakthrough results.
  - *Study B:* 500 patients over 18 months showing zero long-term superiority.
  - *Chatbot Answer:* "Intermittent fasting is promising but results vary." (Dangerous false certainty).
- **Compliance Bias:** When challenged by a user, standard LLMs routinely flip their stance without any new evidence.

> **Speaker Script:**
> "Why does this project exist? When you ask standard AI a clinical research question, it gives you a polite, false agreement. Study A used 40 patients for 8 weeks and claimed success. Study B used 500 patients for 18 months and showed the opposite. Standard chatbots blur them together into dangerous false certainty. In medicine and science, that false certainty costs lives."

---

# Slide 3: The Paradigm Shift: From Search to Trial
### Don't Treat Scientific Research Like a Search Query—Treat it Like a Courtroom

```
[ Contested Clinical Question ]
              │
      ┌───────▼───────┐
      │  Tavily Search │ ➔ Hashes & Admits Raw Excerpts into Evidence Ledger
      └───────┬───────┘
              │
     ┌────────┴────────┐
     ▼                 ▼
[ Prosecution ]   [ Defense ]
Affirmative Case  Skeptical Case
     │                 │
     └────────┬────────┘
              │
    [ Cross-Examination ] ➔ Direct Veracity Challenges
              │
    [ Independent Audit ] ➔ Nebius Qwen 2.5 Verifier (Claims vs. Excerpts)
              │
    [ Judicial Ruling ]   ➔ Bound by the Inconclusive Invariant
```

- **Two Dedicated Advocates:** Prosecution builds the affirmative case; Defense exposes confounding variables and limits.
- **Separation of Powers:** Counsel never verifies their own claims; an independent judicial auditor verifies each assertion.

> **Speaker Script:**
> "Instead of treating deep research like an open-ended autocomplete query, Research Courtroom structures inquiry into an adversarial trial. Two opposing AI agents battle over admitted evidence, audited by an independent Nebius reasoner before the Judge delivers a binding verdict."

---

# Slide 4: Tripartite Jurisprudence
### Three Autonomous Roles Powered by Nebius Token Factory

### 1. Prosecution Counsel
- **Mandate:** Build the strongest empirical affirmative argument.
- **Grounding Rule:** Every single claim must cite verified ledger IDs `[E1]`.
- **Constraint:** Zero unverified assertions allowed past the gate.

### 2. Defense Counsel
- **Mandate:** Identify methodological flaws, sample bias, and protocol limits.
- **Adversarial Check:** Tests whether claimed benefits hold across long-term durations (>12 months).
- **Scope:** Ensures contraindications are surfaced, not buried.

### 3. The Judicial Bench (Nebius Qwen 2.5)
- **Mandate:** Independent impartiality.
- **The Inconclusive Invariant:** If the affirmative fails to prove superiority beyond doubt, the judge is compelled to rule **Inconclusive**.
- **No Hallucinations:** Prunes claims whose citations fail exact excerpt matching.

> **Speaker Script:**
> "Our architecture enforces tripartite separation: Prosecution argues for the claim; Defense argues against it; and the Judicial Bench evaluates both sides against strict evidentiary standards. The Judge holds the courage to rule Inconclusive whenever evidence fails to meet the burden of proof."

---

# Slide 5: Defensive Security & Architectural Invariants
### Zero Hallucinations · SSRF Firewall · Cryptographic Ledger

- **Strict Excerpt Hashing:** Evidence items are preserved as immutable SHA-256 excerpts with verified URIs and retrieval timestamps.
- **Hardened SSRF Firewall:** Cross-examination and source ingestion screen all URLs against RFC-1918 private subnets and cloud metadata endpoints (`169.254.169.254`). Sockets are dropped before network dispatch.
- **Independent Auditor Pass:** Claims are audited in isolated single-sentence contexts directly against raw source text (max 2,400 chars).
- **56 Automated Passing Tests:** Comprehensive backend test suite verifying citation integrity, SSRF rejection, and streaming resilience.

> **Speaker Script:**
> "We engineered strict defensive invariants. If an agent tries to hallucinate a citation like 'E99', the system prunes it automatically. If a user tries to inject a cloud metadata address during cross-examination, our SSRF defense refuses the connection cold. Fifty-six automated tests ensure these guarantees hold."

---

# Slide 6: The Live Courtroom Experience
### Real-Time Transparency Through Server-Sent Events (SSE)

- **Live Deliberation Stream:** Streaming SSE ticker visualizes real-time evidence ingestion, claim formulation, and cross-examination.
- **Interactive Provenance Drawer:** Clicking any citation badge (`[E1]`, `[E3]`) opens the exact verified excerpt modal with source domain and timestamp.
- **Instant Verdict Announcement:** Modal announcement surfaces the ruling, verified claim counts, and full judicial reasoning.
- **Real-Time Cross-Examination:** Users can challenge the court with follow-up counterarguments and new sources, triggering dynamic trial reconsiderations.

> **Speaker Script:**
> "When a case is filed, the user watches the courtroom in real time. Counsel drafts live before your eyes, citations link directly to cryptographic excerpt receipts, and the full judicial deliberation unfolds with complete auditability."

---

# Slide 7: Validation & Empirical Results
### Tested on Contested Real-World Inquiries

| Research Question | Opposing Evidence Conflict | Judicial Ruling |
|---|---|---|
| **Intermittent Fasting vs. Calorie Restriction** | Short-term 8-wk fat loss vs. 12-mo equivalent weight loss | **INCONCLUSIVE** (Equivalent when isocaloric) |
| **Remote Work vs. Office Productivity** | Self-reported output gains vs. collaborative innovation decline | **INCONCLUSIVE** (Role & tenure dependent) |
| **AI vs. Junior Developer Code Quality** | Speed of completion vs. security vulnerability rate | **CONTESTED** (High defect rate without senior review) |

- **Zero Consensus Bias:** The court resisted defaulting to artificial certainty in all trials.
- **100% Citation Grounding:** No phantom citations survived verification.

> **Speaker Script:**
> "Here are the empirical results across contested trials. In every case, the courtroom refused to generate synthetic consensus. When clinical trials showed equal weight loss at 12 months, the court ruled Inconclusive, citing exact evidence receipts."

---

# Slide 8: The Conclusion & Call To Action
### Truth is Not a Compromise. Put the Science on Trial.

- **Open Source:** Production-ready codebase with full test suite, Docker support, and live frontend.
- **GitHub Repository:** `https://github.com/pramodh-bn/nebius-research-agent`
- **Team:** All Vibes
- **Sole Creator & Engineer:** Pramodh Nanjayya
- **Hackathon:** ODSC × Nebius Hackathon 2026

> **Speaker Script:**
> "The future of AI research isn't about asking an LLM to hallucinate a polite compromise. It is about building systems that can prove the work is right. Truth is not a compromise. Put the science on trial. Thank you."
