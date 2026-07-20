# System Architecture

## 1. High-Level Architecture

```text
┌───────────────────────────────────────────────┐
│                LeetCode Website               │
│ Problem | Editor | Run | Submit | Test Result │
└───────────────────────────────────────────────┘
                    │ user action
                    ▼
┌───────────────────────────────────────────────┐
│        Chrome / Edge Browser Extension        │
│ Floating Entry | Side Panel | Context Menu    │
└───────────────────────────────────────────────┘
                    │ HTTPS / local HTTP
                    ▼
┌───────────────────────────────────────────────┐
│                 FastAPI Backend               │
│ API | Coach Services | Validation | Logging   │
└───────────────────────────────────────────────┘
             │                         │
             ▼                         ▼
┌─────────────────────┐      ┌──────────────────┐
│    DeepSeek API     │      │    PostgreSQL    │
│ Explanation / Plan │      │ Learning Records │
└─────────────────────┘      └──────────────────┘
```

A later Web App will connect to the same backend.

---

## 2. Responsibilities

### 2.1 LeetCode

Responsible for:

- official problem display;
- code editor;
- code execution;
- testing;
- submission;
- result validation.

Our product must not duplicate these responsibilities in the MVP.

### 2.2 Browser Extension

Responsible for:

- opening the Side Panel;
- collecting user-initiated text;
- sending selected text through a context menu;
- displaying coach responses;
- storing lightweight local settings;
- communicating with the backend;
- displaying current-session state.

It should not:

- contain secret API keys;
- access the database directly;
- implement review rules;
- call DeepSeek with a developer-owned key directly;
- automatically scrape complete pages in the MVP.

### 2.3 FastAPI Backend

Responsible for:

- API contracts;
- request validation;
- authentication later;
- coaching workflows;
- DeepSeek provider calls;
- prompt management;
- structured-output validation;
- persistence;
- review scheduling;
- rate limiting later;
- error handling and logging.

### 2.4 DeepSeek Provider

Responsible for:

- natural-language explanation;
- progressive hint generation;
- complete solution generation;
- feedback parsing;
- study-plan generation;
- input classification where useful.

DeepSeek should not control persisted state directly.

### 2.5 PostgreSQL

Responsible for:

- users;
- settings;
- problem references;
- study sessions;
- attempts;
- hint events;
- conversations;
- messages;
- review schedules;
- API usage metadata.

---

## 3. Proposed Repository Structure

```text
ai-leetcode-coach/
├── AGENTS.md
├── README.md
├── CODEX_START_PROMPT.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── docs/
│   ├── PRODUCT_SPEC.md
│   ├── ARCHITECTURE.md
│   ├── TECH_DECISIONS.md
│   ├── DATA_MODEL.md
│   ├── ROADMAP.md
│   └── ORIGINAL_PROJECT_ANALYSIS.md
├── extension/
│   ├── manifest.json
│   ├── src/
│   │   ├── background/
│   │   ├── sidepanel/
│   │   ├── content/
│   │   ├── shared/
│   │   └── options/
│   └── tests/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── llm/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   └── pyproject.toml
└── tests/
```

Codex may refine this structure, but architectural boundaries must remain clear.

---

## 4. Browser Extension Architecture

### 4.1 Main Components

- `manifest.json`
- background service worker
- Side Panel page
- context menu registration
- message-passing utilities
- local settings storage
- later optional content script

### 4.2 First Permissions

Recommended initial permissions:

```json
{
  "permissions": [
    "sidePanel",
    "storage",
    "contextMenus",
    "activeTab"
  ]
}
```

Avoid `<all_urls>` in the first version.

A later LeetCode-specific integration may request:

```json
{
  "permissions": ["scripting"],
  "host_permissions": [
    "https://leetcode.com/*",
    "https://leetcode.cn/*"
  ]
}
```

Only add these when implementing a clearly user-approved feature.

### 4.3 Selection Flow

```text
User selects webpage text
→ User opens context menu
→ Clicks "Send to AI LeetCode Coach"
→ Background worker receives selectionText
→ Background worker opens Side Panel
→ Message is sent to Side Panel
→ Side Panel displays the selected content
```

---

## 5. Backend Architecture

### 5.1 API Layer

Example endpoints:

```text
GET  /health
POST /api/v1/coach/explain
POST /api/v1/coach/hint
POST /api/v1/coach/solve
POST /api/v1/coach/analyse-error
POST /api/v1/attempts
GET  /api/v1/reviews/due
POST /api/v1/plans
```

The exact API should be introduced gradually.

### 5.2 Service Layer

Possible services:

- `ExplanationService`
- `HintService`
- `SolutionService`
- `FeedbackService`
- `StudyPlanService`
- `ReviewService`
- `ConversationService`

### 5.3 LLM Layer

Components:

- provider interface;
- DeepSeek implementation;
- prompt templates;
- output schemas;
- retry and parsing logic;
- model configuration;
- optional usage tracking.

Example provider abstraction:

```python
class LLMProvider(Protocol):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        ...
```

Business services should depend on the interface, not directly on the DeepSeek SDK.

### 5.4 Persistence Layer

Use:

- SQLAlchemy ORM;
- Alembic migrations;
- repositories;
- transaction boundaries.

No raw database access from API routes.

---

## 6. Request Model

A common coaching request can be normalised:

```json
{
  "mode": "explain_code",
  "source": "manual_paste",
  "content_type": "code",
  "language": "python",
  "content": "counts[num] = counts.get(num, 0) + 1",
  "surrounding_context": "...",
  "problem_metadata": {
    "platform": "leetcode",
    "title": "Two Sum",
    "url": "https://leetcode.com/problems/two-sum/"
  },
  "preferences": {
    "answer_depth": "detailed",
    "allow_full_solution": true
  }
}
```

Possible modes:

- `explain_problem`
- `hint`
- `pseudocode`
- `complete_solution`
- `explain_code`
- `explain_line`
- `explain_syntax`
- `explain_library`
- `analyse_error`
- `summarise_attempt`

---

## 7. Security Architecture

### Secrets

- Developer DeepSeek key lives only in backend environment variables.
- `.env` must never be committed.
- Extension code contains only backend URL configuration.

### Data

- Do not log full API keys.
- Avoid logging complete user code in production by default.
- Add deletion and retention controls later.
- Mark whether content is ephemeral or persisted.

### Abuse

Later add:

- authentication;
- per-user limits;
- rate limiting;
- request-size limits;
- timeout controls;
- cost tracking.

---

## 8. Deployment Evolution

### Local Development

```text
Extension
→ http://localhost:8000
→ FastAPI
→ DeepSeek API
→ PostgreSQL in Docker
```

### Early Hosted Version

```text
Extension
→ HTTPS backend
→ Managed PostgreSQL
→ DeepSeek API
```

### Later Product

```text
Extension + Web App
→ Shared API
→ Auth + Billing + Usage Control
→ PostgreSQL
→ Multiple LLM providers
```
