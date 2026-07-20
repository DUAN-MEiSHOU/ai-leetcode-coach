# Data Model

This is a proposed model for the future PostgreSQL database. It may be refined during implementation.

---

## 1. Design Principles

- Store user-owned learning records.
- Store problem references and metadata, not a public copied problem bank.
- Keep complete pasted problem content ephemeral by default.
- Separate conversations from attempts.
- Record hint usage because it affects learning quality and review scheduling.
- Support future multi-user architecture.
- Use UUIDs or database-generated identifiers consistently.
- Include `created_at` and `updated_at` where appropriate.

---

## 2. Entity Overview

```text
User
 ├── UserSetting
 ├── StudyPlan
 ├── StudySession
 ├── Attempt
 ├── Conversation
 └── ReviewSchedule

ProblemReference
 ├── Attempt
 ├── StudyPlanItem
 ├── Conversation
 └── ReviewSchedule

Conversation
 └── Message

Attempt
 └── HintEvent
```

---

## 3. Proposed Tables

### 3.1 users

Purpose: future account identity.

Fields:

- `id`
- `email`
- `display_name`
- `created_at`
- `updated_at`
- `is_active`

For the local single-user prototype, one seeded local user may be used.

---

### 3.2 user_settings

Purpose: preferences and model configuration metadata.

Fields:

- `id`
- `user_id`
- `preferred_language`
- `preferred_programming_language`
- `explanation_depth`
- `default_hint_mode`
- `save_code_snapshots`
- `created_at`
- `updated_at`

Do not store raw developer API keys here in the early version.

---

### 3.3 problem_references

Purpose: identify an external problem without copying a full problem bank.

Fields:

- `id`
- `platform`
- `external_problem_id`
- `slug`
- `title`
- `url`
- `difficulty`
- `topics_json`
- `created_at`
- `updated_at`

Unique constraint candidate:

```text
(platform, external_problem_id)
```

or:

```text
(platform, url)
```

Fields such as title and difficulty may come from user input or later user-approved extraction.

---

### 3.4 study_plans

Purpose: a generated daily or session plan.

Fields:

- `id`
- `user_id`
- `plan_date`
- `available_minutes`
- `focus`
- `status`
- `created_at`
- `updated_at`

Suggested status values:

- `draft`
- `active`
- `completed`
- `cancelled`

---

### 3.5 study_plan_items

Purpose: items inside a plan.

Fields:

- `id`
- `study_plan_id`
- `problem_reference_id`
- `item_type`
- `estimated_minutes`
- `reason`
- `position`
- `status`
- `created_at`

Suggested `item_type` values:

- `new`
- `review`

Suggested status values:

- `pending`
- `started`
- `completed`
- `skipped`

---

### 3.6 study_sessions

Purpose: a timed learning session.

Fields:

- `id`
- `user_id`
- `problem_reference_id`
- `started_at`
- `ended_at`
- `duration_minutes`
- `programming_language`
- `source`
- `created_at`

Suggested source values:

- `manual_paste`
- `page_selection`
- `future_page_context`
- `future_screenshot`

---

### 3.7 attempts

Purpose: the outcome of one problem-solving attempt.

Fields:

- `id`
- `user_id`
- `problem_reference_id`
- `study_session_id`
- `attempted_at`
- `duration_minutes`
- `outcome`
- `max_hint_level_used`
- `used_hint`
- `viewed_full_solution`
- `viewed_external_solution`
- `language`
- `notes`
- `created_at`
- `updated_at`

Suggested outcome values:

- `solved_independently`
- `solved_with_hints`
- `viewed_solution`
- `gave_up`
- `reviewed_easily`
- `struggled`

---

### 3.8 hint_events

Purpose: record coaching assistance used during an attempt.

Fields:

- `id`
- `attempt_id`
- `hint_level`
- `hint_type`
- `created_at`

Suggested hint types:

- `problem_restatement`
- `direction`
- `data_structure`
- `algorithm`
- `pseudocode`
- `implementation`
- `complete_solution`

This table enables analysis of how much support the user needed.

---

### 3.9 review_schedules

Purpose: deterministic spaced review state for each user/problem pair.

Fields:

- `id`
- `user_id`
- `problem_reference_id`
- `next_review_at`
- `interval_days`
- `review_streak`
- `last_outcome`
- `last_attempt_id`
- `created_at`
- `updated_at`

Unique constraint:

```text
(user_id, problem_reference_id)
```

---

### 3.10 conversations

Purpose: group AI coaching messages.

Fields:

- `id`
- `user_id`
- `problem_reference_id`
- `study_session_id`
- `mode`
- `title`
- `created_at`
- `updated_at`

Modes may include:

- `problem_help`
- `code_explanation`
- `error_analysis`
- `review`
- `general`

---

### 3.11 messages

Purpose: store messages in a conversation.

Fields:

- `id`
- `conversation_id`
- `role`
- `content`
- `content_type`
- `model`
- `prompt_version`
- `token_input`
- `token_output`
- `created_at`

Roles:

- `user`
- `assistant`
- `system`

Privacy note: production storage of full user code should be configurable.

---

### 3.12 code_snapshots

Purpose: optional saved user code.

Fields:

- `id`
- `user_id`
- `problem_reference_id`
- `attempt_id`
- `language`
- `content`
- `source`
- `created_at`

This table should be optional and controlled by a user setting.

---

### 3.13 api_usage

Purpose: future cost and limit tracking.

Fields:

- `id`
- `user_id`
- `provider`
- `model`
- `operation`
- `input_tokens`
- `output_tokens`
- `estimated_cost`
- `request_id`
- `created_at`

Not required for the earliest local prototype.

---

## 4. Temporary Session Context

Complete pasted problem statements, screenshots, and page selections may be represented in request objects but should not automatically become permanent database records.

Example temporary context:

```json
{
  "source": "page_selection",
  "content_type": "problem_text",
  "content": "...",
  "persist": false
}
```

---

## 5. Review Algorithm

Initial deterministic interval sequence:

```text
1, 3, 7, 16, 35, 90 days
```

Possible rule:

- independent success or easy review:
  - increment streak;
  - advance interval;
- solved with hints:
  - retain or shorten interval;
- viewed full solution, gave up, or struggled:
  - reset streak;
  - review soon.

The exact algorithm should be isolated in a `ReviewService` and tested independently.

---

## 6. Migration Strategy

Use Alembic.

Rules:

- every schema change receives a migration;
- avoid manually editing production schemas;
- seed data must be separate from migrations;
- tests should create isolated databases;
- local development may use Docker PostgreSQL.

---

## 7. Initial Minimal Schema

Do not create every table on day one.

Recommended first persistent milestone:

- `users`
- `problem_references`
- `attempts`
- `review_schedules`

Add conversations and usage tracking only when the related feature exists.
