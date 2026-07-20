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

## Development Principle

Do not ask an AI coding agent to build the whole product at once.

Use the sequence in `docs/ROADMAP.md`, validate every milestone, and keep the project runnable after each step.
