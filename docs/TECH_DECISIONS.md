# Technical Decisions

This file records decisions already made. Do not reverse them casually.

---

## TD-001: Do Not Build a Complete Problem Bank

**Decision:** The project will not create or publish a copied LeetCode problem bank.

**Reasoning:**

- copyright and platform-term risks;
- high content-maintenance cost;
- the project value is coaching, not content replication;
- LeetCode already provides problem presentation and judging.

**Implementation consequence:**

Problem input should come from user-initiated actions:

- manual paste;
- selected text;
- later screenshots;
- later user-approved metadata extraction.

The database may store problem metadata and private learning records, but should not become a public copy of complete problem statements.

---

## TD-002: LeetCode Remains the Coding and Validation Environment

**Decision:** Users write, run, test, and submit code in LeetCode.

**Reasoning:**

- avoids building an editor and judge too early;
- avoids arbitrary-code-execution security risk;
- reduces scope;
- creates a focused product position.

**Consequence:** The coach integrates beside LeetCode rather than replacing it.

---

## TD-003: Primary Interface Is a Browser Side Panel

**Decision:** Use a small floating entry button plus a browser Side Panel.

**Reasoning:**

- lower page-switching cost;
- Side Panel supports longer explanations better than a small overlay;
- floating button provides a lightweight entry;
- the user can keep LeetCode visible.

**Consequence:** A draggable overlay may be considered later, but it is not the primary interface.

---

## TD-004: Support Both Manual Paste and User-Selected Text

**Decision:** The first useful version should support:

1. manual text paste;
2. selected webpage text sent through a context menu.

**Reasoning:**

- manual paste is simple and reliable;
- selection input reduces friction;
- both normalise to the same backend request model;
- user intent is explicit.

---

## TD-005: Use Minimal Browser Permissions

**Decision:** Start with:

- `sidePanel`
- `storage`
- `contextMenus`
- `activeTab`

**Reasoning:**

- privacy;
- lower installation friction;
- less maintenance;
- no need for unrestricted page access.

**Consequence:** Do not request `<all_urls>` in the initial version.

---

## TD-006: Use FastAPI Backend

**Decision:** The browser extension communicates with a FastAPI backend.

**Reasoning:**

- keeps API keys out of extension code;
- centralises prompts and business rules;
- enables validation, persistence, limits, and future accounts;
- aligns with the user's Python experience and career goals.

---

## TD-007: DeepSeek Is the Initial Model Provider

**Decision:** Use the user's DeepSeek API access initially.

**Reasoning:**

- available to the developer;
- sufficient for explanation and structured workflows;
- supports an OpenAI-compatible integration pattern.

**Consequence:**

- API key stored in backend `.env`;
- model and base URL configured through settings;
- provider interface should allow future replacement;
- validate all structured output.

---

## TD-008: Backend Versus BYOK

**Decision:** During development, use the developer's DeepSeek key through the local backend.

**Long-term direction:** Support either:

- platform-provided usage;
- user-provided API key.

**Reasoning:**

- development remains simple;
- key stays out of extension source;
- architecture remains compatible with future commercial or BYOK modes.

No billing system is included in the MVP.

---

## TD-009: PostgreSQL Is the Intended Database

**Decision:** Use PostgreSQL for the intended application architecture.

**Reasoning:**

- suitable for multi-user relational data;
- common in FastAPI and SaaS systems;
- supports transactions, indexing, JSON fields, migrations, and managed hosting;
- useful for the developer's engineering learning goals.

**Fallback:** SQLite may be used temporarily if PostgreSQL setup blocks the first prototype.

**Constraint:** Use SQLAlchemy and Alembic so database choice does not leak into business logic.

---

## TD-010: LLM and Deterministic Logic Must Be Separated

**Decision:** LLMs handle interpretation and teaching. Traditional code handles persistent state and rules.

**LLM responsibilities:**

- explanations;
- hints;
- solution generation;
- feedback parsing;
- plan reasoning.

**Traditional-code responsibilities:**

- schema validation;
- persistence;
- review intervals;
- authentication;
- limits;
- state transitions;
- data integrity.

---

## TD-011: Progressive Hints Are a Core Product Feature

**Decision:** Do not reduce the product to a normal chat box.

Assistance levels should include:

1. restatement;
2. first hint;
3. algorithm/data-structure hint;
4. pseudocode;
5. implementation guidance;
6. complete solution.

The user must be allowed to request a complete answer.

---

## TD-012: Python Is the First-Class Language

**Decision:** Implement and test the richest explanation experience for Python first.

**Later priority:**

- Java;
- C++;
- JavaScript;
- Go.

**Reasoning:** Supporting every language from the beginning would create shallow and unreliable behaviour.

---

## TD-013: No Online Code Execution in the MVP

**Decision:** Do not execute arbitrary user code.

**Reasoning:**

- security;
- container isolation;
- time and memory limits;
- multi-language environment maintenance;
- judge-data requirements.

LeetCode already provides execution and submission.

---

## TD-014: Build Incrementally

**Decision:** Each milestone must be independently runnable and testable.

Do not ask Codex to generate the entire product at once.

Preferred progression:

1. extension shell;
2. selection input;
3. FastAPI health endpoint;
4. extension/backend connection;
5. DeepSeek integration;
6. coaching modes;
7. persistence;
8. planning and review.
