# Screenplay: Research Courtroom (Team All Vibes)

**Runtime:** 2:32 (152.5 s) · **Resolution:** 1920x1080 25 fps · **Audio:** Neural Christopher + Authentic Voice Sample (`Pramodh Nanjayya`) + Hollywood Orchestral Score (*The Epic 2* by Rafael Krux) with dynamic sidechain ducking.

**Pronunciation:** Pramodh Nanjayya = `/pɹəmˈoʊd nɑːnˈdʒaɪjə/`

---

## Act I: The Problem & The Mission (0:00 to 0:40)

| Time | Scene | Narration | Visual | Audio & SFX |
|---|---|---|---|---|
| **0:00** | **Slide 1: Title & Attribution** | *"All Vibes presents: Research Courtroom. Created and engineered by... [Pramodh Nanjayya] ...for the Nebius Hackathon. We put contested science on trial."* | Dark-mode keynote slide, glowing Scale of Justice emblem, sole engineer badge, authentic user voice attribution. | Orchestral string swell, brass rise. |
| **0:15** | **Slide 2: The Purpose / Why** | *"Why does this exist? When you ask an AI about clinical research, it gives you a polite, false agreement. Study A used forty patients for eight weeks and claimed success. Study B used five hundred patients for eighteen months and showed the opposite. Standard AI blurs them together into dangerous false certainty. Research Courtroom dismantles that illusion."* | Side-by-side card comparison: Fragile Agreement vs. Adversarial Jurisprudence. Highlighting the cost of false certainty in medicine. | Driving trailer percussion, low brass pulse. |

---

## Act II: Architecture & Invariants (0:40 to 1:16)

| Time | Scene | Narration | Visual | Audio & SFX |
|---|---|---|---|---|
| **0:41** | **Slide 3: Tripartite Architecture** | *"Its purpose is simple: don't treat scientific research like a search query—treat it like a trial. A Prosecution and Defense battle over evidence, audited by an independent Nebius Qwen reasoner before the Judge rules."* | Glassmorphism cards showing Prosecution (Affirmative), Defense (Skeptical), and Judge (Nebius Qwen 2.5 32B Reasoner). | Rhythmic string arpeggios, building momentum. |
| **0:58** | **Slide 4: Verification Invariants** | *"Zero hallucinated citations. Hardened against cloud metadata theft. And the courage to rule inconclusive when evidence fails to prove the case. Fifty-six automated tests."* | 4 invariant pillars: Citation Grounding, SSRF Defense, Inconclusive Invariant, 56/56 Verified Tests. | Heavy brass accent, sub-bass pulse. |
| **1:12** | **Slide 5: Live Transition** | *"And now, let us step into the live courtroom."* | Transition card highlighting the live case question. | Orchestral swell before the cut. |

---

## Act III: The Live Courtroom Trial (1:16 to 2:15)

| Time | Scene | Narration | Visual | Camera & Focus |
|---|---|---|---|---|
| **1:16** | **Filing & Real-Time Stream** | *"We file a contested clinical case. Watch the live deliberation stream. Tavily searches real-time sources, hashes each excerpt, and counsel drafts live into the document."* | Live application. Typing question into search input. Real-time SSE deliberation feed ticker. | **Zoom 1.5x** to search bar, then **Zoom 1.4x** to deliberation stream (`⚡ Real-Time SSE Deliberation Stream`). |
| **1:33** | **Opening Arguments & Provenance** | *"Every citation binds directly to a verified excerpt. If citations are hallucinated, they are stripped immediately. Counsel then cross-examine each other directly on veracity."* | Split-screen Prosecution vs. Defense. Citation badges `[E1]`, `[E3]`, `[E5]`. Clicking citation triggers full excerpt modal. | **Zoom 1.3x** to opposing arguments (`🏛️ Opposing Counsel`), HUD: `📖 Provenance Ledger · Excerpt Audit`. |
| **1:47** | **The Judicial Ruling** | *"The verdict has been reached. An instant ruling announcement confirms the finding: inconclusive for long-term superiority. We review the full judicial reasoning."* | Instant Verdict Announcement Dialog pops up. Displays `INCONCLUSIVE`, verified claims, and judicial reasoning. Click `Review Full Verdict`. | Reset zoom (`⚖️ Judicial Verdict · Inconclusive Invariant`), smooth scroll to judicial verdict breakdown. |
| **2:01** | **Cross-Examination & Security Block** | *"Finally, we cross-examine the court with a blocked cloud metadata address. Hardened security refuses the socket cold. Fifty-six tests passing."* | User inputs `http://169.254.169.254/latest/meta-data/` into cross-examination box. Immediate red SSRF safety check refusal. | **Zoom 1.45x** to challenge form (`🛡️ Hardened SSRF Defense · Metadata Block`). |

---

## Act IV: Grand Finale & Resolution (2:15 to 2:32)

| Time | Scene | Narration | Visual | Audio & SFX |
|---|---|---|---|---|
| **2:15** | **Slide 6: Closing Card & Call to Action** | *"Truth is not a compromise. Don't search for consensus—put the science on trial. Explore the codebase and run Research Courtroom today at github.com/pramodh-bn/nebius-research-agent."* | Grand Hero Closing Card: Glowing Scales of Justice emblem, Punchline (*"Truth is not a compromise. Put the science on trial."*), glowing GitHub CTA box, attribution (*"Created & Engineered by Pramodh Nanjayya · Team All Vibes"*). | Climax of *The Epic 2*, heroic brass cadence, orchestral reverb tail fading to black. |

---

## Submission Checklist

- [x] Runtime under 3 minutes (152.5 seconds).
- [x] Authentic voice integration on Slide 1 for Pramodh Nanjayya.
- [x] Hollywood trailer score with sidechain ducking.
- [x] Dynamic camera pan & zoom on active UI sections with HUD label pills.
- [x] Punchline and GitHub CTA displayed cleanly on Slide 6 closing card.
- [x] Synchronized `.srt` subtitles file generated (`demo_out/research-courtroom.srt`).
- [x] 56/56 passing backend automated tests.
