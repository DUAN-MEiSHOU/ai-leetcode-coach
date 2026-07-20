# AGENTS.md

## 1. Project Mission

Build an AI-powered LeetCode learning coach that works alongside existing coding platforms rather than replacing them.

The system should help users:

- decide what to practice today;
- understand problem statements;
- receive progressive hints;
- understand complete solutions;
- explain arbitrary code blocks or single lines;
- identify and explain syntax and library functions;
- analyse errors and failed attempts;
- record learning outcomes;
- schedule future reviews.

The user continues to use LeetCode for:

- viewing the original problem;
- editing code;
- compiling and running code;
- submitting and validating solutions.

This project must not become a replacement LeetCode platform.

---

## 2. Product Form

The intended product form is:

1. A Chrome/Edge browser extension using Manifest V3.
2. A lightweight floating entry button on supported pages.
3. A browser Side Panel as the main coaching interface.
4. A FastAPI backend.
5. DeepSeek API as the initial LLM provider.
6. PostgreSQL as the intended production database.
7. A later Web App for planning, review, progress, history, and account management.

During early development, the backend and database may run locally.

---

## 3. Core Product Boundaries

### Included

- Manual paste input.
- Send selected webpage text to the coach.
- AI chat in the Side Panel.
- Progressive hints.
- Complete-answer mode.
- Whole-code explanation.
- Single-line explanation.
- Syntax explanation.
- Standard-library and library-function explanation.
- Error-message analysis.
- Study planning.
- Attempt recording.
- Spaced review scheduling.
- Learning history and progress tracking.

### Excluded from the MVP

- A full copied LeetCode problem bank.
- Automatic bulk crawling or scraping of LeetCode.
- A proprietary online judge.
- A self-hosted multi-language code execution sandbox.
- Automatic unrestricted reading of all webpage content.
- Automatic reading of the LeetCode editor in the first version.
- Payments, subscriptions, or commercial quota systems.
- Mobile apps.
- Support for every programming language.
- Multi-agent frameworks unless clearly justified.

Do not add excluded features without an explicit product decision.

---

## 4. Legal and Privacy Constraints

- Do not copy or store a public database of complete LeetCode problem statements.
- Do not scrape LeetCode pages in bulk.
- Problem content should come from user-initiated actions such as:
  - manual paste;
  - user-selected text;
  - user-uploaded screenshots in a later version.
- Store only the minimum necessary metadata and user-owned learning data.
- Do not place any API key in extension source code.
- Do not commit `.env` files.
- Do not request broad browser permissions when narrower permissions are sufficient.
- Prefer user-triggered access through `activeTab` and context-menu selection.
- Clearly separate public problem metadata from private user learning records.

---

## 5. Initial Technical Stack

### Browser Extension

- Chrome/Edge Manifest V3
- Side Panel API
- Context Menu API
- Extension Storage API
- `activeTab`
- Plain HTML/CSS/TypeScript or a minimal frontend setup
- Avoid a large frontend framework unless complexity justifies it

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- DeepSeek API through an OpenAI-compatible client
- Structured JSON responses where appropriate
- Explicit timeout, retry, and error handling

### Database

- PostgreSQL for the intended multi-user architecture
- SQLite may be used temporarily only if database setup blocks early development
- Database access must be abstracted through SQLAlchemy and repository/service layers

### Development Infrastructure

- Docker Compose for local PostgreSQL
- `.env` for secrets
- `.env.example` for documented configuration
- Git and GitHub
- Automated tests where practical

---

## 6. Architecture Rules

Use clear separation of concerns:

```text
Browser Extension
    ↓
FastAPI API Layer
    ↓
Application / Coach Services
    ↓
LLM Provider + Repository Layer
    ↓
PostgreSQL
```

Recommended backend layers:

- `api`: HTTP routes and request/response schemas
- `services`: use-case orchestration and coach logic
- `llm`: prompts, provider clients, structured parsing
- `models`: ORM entities
- `schemas`: Pydantic schemas
- `repositories`: database access
- `core`: settings, logging, errors, security
- `tests`: unit and integration tests

Do not put LLM calls directly inside API route functions.

Do not put raw SQL or database logic inside extension code.

Do not couple business logic directly to DeepSeek-specific response objects.

---

## 7. LLM Rules

- The initial provider is DeepSeek.
- Provider code must be replaceable later.
- API key must be loaded from backend environment variables.
- Model name and base URL must be configuration values.
- Validate model outputs.
- Never assume returned JSON is correct.
- Implement bounded retries for malformed or empty structured output.
- Preserve the distinction between:
  - deterministic business rules;
  - LLM interpretation and explanation.

The LLM may:

- explain;
- classify;
- generate hints;
- parse natural-language feedback;
- generate structured study plans.

Traditional code must control:

- persistence;
- authorization;
- validation;
- review intervals;
- limits;
- state transitions;
- problem identity checks.

---

## 8. Coaching Behaviour

The product is a coach, not merely a chat wrapper.

For problem solving, support progressive disclosure:

1. Restate the problem.
2. Clarify inputs, outputs, and constraints.
3. Give a directional hint.
4. Suggest a data structure or algorithm.
5. Provide pseudocode.
6. Explain the key implementation idea.
7. Provide a complete solution only when requested.

The user must always be able to explicitly request a full answer.

For code explanation, distinguish:

- overall code explanation;
- selected-block explanation;
- single-line explanation;
- syntax explanation;
- library-function explanation;
- complexity analysis;
- bug analysis.

---

## 9. Development Process

Work in small, independently testable tasks.

For each task:

1. State the files to be changed.
2. Implement only the requested scope.
3. Add or update tests where practical.
4. Run available checks.
5. Update documentation when behaviour changes.
6. Report:
   - files changed;
   - behaviour implemented;
   - commands run;
   - test results;
   - known limitations;
   - next recommended task.

Do not generate the entire application in one step.

Do not create fake implementations that only return hard-coded success messages unless explicitly building a UI stub.

---

## 10. Code Quality

- Prefer readable code over clever code.
- Use type hints in Python.
- Use Pydantic models for API contracts.
- Use clear error messages.
- Keep functions focused.
- Avoid hidden global state.
- Avoid duplicated prompt strings.
- Keep secrets out of logs.
- Add comments for non-obvious decisions, not for every line.
- Use migrations for schema changes.
- Design APIs consistently.

---

## 11. Testing Expectations

At minimum, add tests for:

- request validation;
- LLM response parsing;
- review scheduling;
- database repository operations;
- API error handling;
- extension message handling where practical.

Mock external DeepSeek calls in automated tests.

Do not require paid API calls for the normal test suite.

---

## 12. Current Development Priority

The first implementation milestone is a minimal browser extension:

- loadable in Chrome/Edge developer mode;
- toolbar action;
- Side Panel;
- manual text input;
- send button;
- no backend connection yet;
- no page scraping;
- no database;
- no DeepSeek call.

After that:

1. selected-text context menu;
2. extension message flow;
3. FastAPI health endpoint;
4. extension-to-backend connection;
5. DeepSeek integration;
6. structured coaching modes;
7. persistence;
8. planning and review.

Always consult `docs/PRODUCT_SPEC.md`, `docs/ARCHITECTURE.md`,
`docs/TECH_DECISIONS.md`, `docs/DATA_MODEL.md`, and `docs/ROADMAP.md`
before making architectural changes.
