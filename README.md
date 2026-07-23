# AI LeetCode Coach

An AI-powered learning companion that works alongside LeetCode.

The user continues to use LeetCode for problem viewing, coding, execution, and submission. This project provides a coaching layer for:

- daily study planning;
- progressive hints;
- complete solution explanations;
- code-block and single-line explanations;
- syntax and library-function explanations;
- error analysis;
- attempt recording;
- spaced review scheduling.

## Product Direction

The intended product consists of:

- a Chrome/Edge browser extension;
- a lightweight floating entry button;
- a browser Side Panel;
- a FastAPI backend;
- DeepSeek API integration;
- PostgreSQL persistence;
- a later Web App for planning, history, and review.

The MVP will not include:

- a copied LeetCode problem bank;
- a proprietary code editor or online judge;
- automatic bulk scraping;
- unrestricted automatic page reading;
- multi-language sandbox execution.

## Repository Documents

Read these before development:

- `AGENTS.md`
- `docs/PRODUCT_SPEC.md`
- `docs/ARCHITECTURE.md`
- `docs/TECH_DECISIONS.md`
- `docs/DATA_MODEL.md`
- `docs/ROADMAP.md`
- `docs/ORIGINAL_PROJECT_ANALYSIS.md`
- `CODEX_START_PROMPT.md`

## Planned Repository Structure

```text
ai-leetcode-coach/
├── AGENTS.md
├── README.md
├── CODEX_START_PROMPT.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docs/
├── extension/
├── backend/
└── tests/
```

The implementation folders may initially be empty. Codex should create them one milestone at a time.

## Current Status

- Phase 1: loadable Manifest V3 extension shell.
- Phase 2: selected webpage text can be sent to the Side Panel through a context menu.
- Phase 3: minimal FastAPI backend with `/health` and `/api/v1/coach/echo`.
- Phase 4: DeepSeek provider abstraction, local configuration, and Side Panel explanation flow.
- Phase 5: structured coaching modes and safe Markdown response rendering.
- Phase 6: Python-first static context for imports, calls, and selected lines.
- Phase 7 foundation: PostgreSQL models, migration, repositories, and learning-record API.
- Phase 8: deterministic review scheduling and persisted study-plan generation.
- Phase 9: LeetCode-specific floating Side Panel entry with restricted host access.

Not yet included:

- real DeepSeek calls until a local `.env` key is configured;
- authentication;
- payments;
- Web App;
- code execution;
- automatic LeetCode scraping.

## Local Backend

From the `backend` directory:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Verify:

```text
http://127.0.0.1:8000/health
```

Run backend tests:

```bash
python -m unittest discover -s tests
```

To validate a locally configured DeepSeek key, see the smoke-check instructions
in `backend/README.md`. The live check is opt-in and sends one small request.

## Development Principle

Do not ask an AI coding agent to build the whole product at once.

Use the sequence in `docs/ROADMAP.md`, validate every milestone, and keep the project runnable after each step.
