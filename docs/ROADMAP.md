# Development Roadmap

The project must be built in small, verifiable milestones.

---

## Phase 0: Repository and Context

### Goal

Create the repository, add project documents, initialise Git, and verify that Codex understands the project.

### Deliverables

- context documents;
- `.gitignore`;
- `.env.example`;
- initial README;
- agreed directory structure.

### Acceptance Criteria

- Codex can accurately summarise the product and exclusions;
- no product code is required yet;
- all secrets are excluded from Git.

---

## Phase 1: Minimal Browser Extension

### Goal

Create a loadable Chrome/Edge Manifest V3 extension.

### Features

- toolbar action;
- Side Panel;
- project title;
- multi-line text input;
- send button;
- local placeholder output;
- no backend;
- no DeepSeek;
- no database.

### Acceptance Criteria

- extension loads in developer mode;
- clicking the toolbar icon opens the Side Panel;
- text can be entered;
- clicking send shows a local placeholder response;
- installation steps are documented.

---

## Phase 2: Selected-Text Input

### Goal

Allow users to send selected webpage text to the Side Panel.

### Features

- context-menu item;
- `selectionText` capture;
- background worker;
- Side Panel opening;
- message passing;
- preserve line breaks;
- classify source as `page_selection`.

### Acceptance Criteria

- select text on a webpage;
- right-click and choose the extension action;
- Side Panel opens;
- selected text appears in the input area;
- no complete-page scraping occurs.

---

## Phase 3: FastAPI Foundation

### Goal

Create a small backend.

### Features

- FastAPI app;
- configuration;
- `/health`;
- CORS for local extension development;
- Pydantic request/response models;
- structured errors;
- tests.

### Acceptance Criteria

- backend starts locally;
- `/health` returns success;
- tests pass;
- extension can call a simple echo endpoint.

---

## Phase 4: DeepSeek Integration

### Goal

Connect the backend to DeepSeek securely.

### Features

- environment configuration;
- OpenAI-compatible client;
- provider abstraction;
- timeout;
- limited retries;
- empty-response handling;
- mocked tests;
- one generic explanation endpoint.

### Acceptance Criteria

- key is read only from backend environment;
- extension never receives the key;
- a pasted code block can receive a model explanation;
- invalid provider responses are handled safely;
- tests do not require paid calls.

---

## Phase 5: Structured Coaching Modes

### Goal

Make the Side Panel more than a generic chatbot.

### Modes

- explain problem;
- progressive hint;
- pseudocode;
- complete solution;
- explain code block;
- explain selected line;
- explain syntax;
- explain library function;
- analyse error.

### Acceptance Criteria

- each mode has a clear request schema;
- prompts are versioned or centrally stored;
- responses use consistent sections;
- the UI makes the active mode visible.

---

## Phase 6: Python-First Code Understanding

### Goal

Improve reliability for Python.

### Features

- language selection;
- Python syntax identification;
- import detection;
- function-call extraction;
- standard-library explanation;
- surrounding-context support;
- line-number handling.

Possible tools:

- Python `ast`;
- lightweight parsing;
- later Tree-sitter.

### Acceptance Criteria

- selected-line explanations use surrounding code;
- standard-library calls are correctly identified in common cases;
- explanations distinguish syntax from current-context purpose.

---

## Phase 7: PostgreSQL Persistence

### Goal

Add learning records.

### Features

- Docker Compose PostgreSQL;
- SQLAlchemy;
- Alembic;
- initial models;
- repositories;
- attempt API;
- review schedule API.

Initial tables:

- users;
- problem references;
- attempts;
- review schedules.

### Acceptance Criteria

- database starts locally;
- migrations run;
- attempt records persist;
- due reviews can be queried;
- repository tests pass.

---

## Phase 8: Study Planning and Review

### Goal

Recreate and extend the original project's learning loop.

### Features

- available-time input;
- daily plan;
- new-versus-review balance;
- deterministic review intervals;
- feedback parsing;
- attempt completion;
- next-review calculation.

### Acceptance Criteria

- user can generate a plan;
- complete a problem;
- record the result;
- see an updated review date;
- deterministic scheduling is covered by tests.

---

## Phase 9: Floating Entry Button

### Goal

Add a low-friction page entry point.

### Features

- small floating button on supported pages;
- opens Side Panel;
- does not obstruct LeetCode;
- limited host permissions;
- resilient styling.

This phase may be moved earlier if the Side Panel-only experience feels inconvenient.

---

## Phase 10: Web App

### Goal

Add a management dashboard.

### Features

- login later;
- today's plan;
- learning history;
- review calendar;
- progress statistics;
- saved conversations;
- settings.

The Web App does not become a coding judge.

---

## Phase 11: Advanced Integrations

Possible later features:

- user-approved current-problem metadata extraction;
- user-approved editor-code extraction;
- screenshot input;
- official-document retrieval;
- Java and C++ parsing;
- platform-provided quota;
- BYOK;
- model-provider switching;
- improved recommendation models.

---

## Out-of-Scope Backlog

Do not implement without a new decision:

- copied full problem bank;
- automatic bulk scraping;
- online judge;
- arbitrary code sandbox;
- social network;
- leaderboard;
- payment system;
- mobile application;
- model training;
- multi-agent orchestration for its own sake.
