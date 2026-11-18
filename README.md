# Research Courtroom — Research Agent

> ODSC × Nebius Hackathon submission · Challenge: *Build a research agent that brings its sources*

**One-line pitch:** Contested research questions, argued by a prosecution and defense from cited web evidence and ruled on by an impartial judge, for anyone who needs a verifiable answer rather than a one-sided summary. (Status: MVP, see `docs/BASELINE.md`.)

- **Demo video (2–3 min):** <link>
- **Team:** <names / GitHub handles>

## The problem
Researchers and curious users facing disputed questions. A single synthesized answer hides the opposing case; Research Courtroom surfaces both sides, grounds them in an evidence ledger, and lets the user challenge the verdict.

## How it works
```
question → plan queries → Tavily search → select & dedupe evidence → Nebius Token Factory synthesis → answer with citations
```
- **Query planning:** <how the agent decides what to search and when to stop>
- **Evidence handling:** <how sources are filtered, deduplicated, checked>
- **Safety:** <how web content is kept separate from trusted instructions>
- **Trade-offs:** <latency, cost, reliability>

## Required services
| Requirement | How we use it |
|---|---|
| Nebius Token Factory (inference) | Model: `<model name>` — <role in the agent> |
| Tavily (real-time web search) | <how results feed the model and how links survive into answers> |

## Setup
```bash
git clone <repo-url>
cd <repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your keys — never commit them
python src/agent.py "Your research question here"   # starter CLI\nstreamlit run app.py                                 # Research Courtroom UI\npython -m pytest -q                                  # tests
```

## Example
**Question:** <example question>
**Answer (excerpt):** <answer with [1], [2] citations>
**Sources:** [1] <url> · [2] <url>

## Failure / insufficient-evidence case
<Show what the agent does when search returns nothing useful or a tool fails.>

## Judging criteria map
| Criterion | Weight | Where to look |
|---|---|---|
| Sourced and verifiable answers | 30% | Example above, demo 0:00–… |
| Works end to end | 25% | Setup, demo |
| Usefulness | 20% | The problem |
| Agent design | 15% | How it works |
| Use of Token Factory and Tavily | 10% | Required services |

## License
MIT

