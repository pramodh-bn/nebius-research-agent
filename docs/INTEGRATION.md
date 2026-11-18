# Research Courtroom v2 — official starter overlay

Use the official cloned repository as the destination. This archive is an overlay, NOT a replacement repository.

1. Create a branch: `git switch -c feature/research-courtroom`.
2. Extract this ZIP into the repository root, preserving the original `src/agent.py`, `README.md`, `LICENSE`, and `SUBMISSION_CHECKLIST.md`.
3. The overlay contains `app.py`, `src/courtroom/`, `tests/`, merged `requirements.txt`, and `.env.example`.
4. Compare existing requirements and environment files before replacing them; retain any extra dependencies/configuration added since cloning.
5. Create `.env` from `.env.example` and populate keys. Do not commit `.env`.
6. Run `python -m pip install -r requirements.txt`, `python -m pytest -q`, and `streamlit run app.py`.
7. Update the original README to describe Research Courtroom and preserve all official submission fields.

Limitations: MVP claim checking validates citation IDs, not semantic support; user URLs are search hints, not directly fetched/verified; live API integrations have not been verified. See MASTER_PROMPT_V2.md for next implementation tasks.
