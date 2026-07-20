# Product Specification

## 1. Product Name

Working name: **AI LeetCode Coach**

The name may change later.

---

## 2. Product Vision

Create an AI learning coach that stays beside the user while they solve algorithm problems.

The product should reduce the need to switch between LeetCode, general-purpose chatbots, documentation pages, personal notes, and separate study-planning tools.

The product is not intended to replace LeetCode.

---

## 3. Target Users

Primary users:

- beginner and intermediate algorithm learners;
- students preparing for coding interviews;
- users who can write some code but struggle to understand solutions deeply;
- users who need structured review and study planning;
- users who often rely on AI but want more guided and educational support.

Initial development may target a single user, but the architecture should be able to evolve toward multiple users.

---

## 4. Main User Problem

Algorithm learners often face four recurring questions:

1. What should I practise today?
2. How should I think about this problem?
3. What does this code actually do?
4. When should I review this problem again?

Existing platforms provide problems and judging, while general AI chat tools provide answers. Few tools connect planning, in-problem coaching, code understanding, and review history into one learning loop.

---

## 5. Core User Journey

```text
Open LeetCode
→ Open AI Coach Side Panel
→ See or choose today's task
→ Paste or select problem context
→ Ask for explanation or progressive hints
→ Write and test code in LeetCode
→ Select code or error output for analysis
→ Submit in LeetCode
→ Record outcome
→ Schedule future review
```

---

## 6. Core Functional Areas

### 6.1 Study Planning

The coach should eventually:

- accept the user's available study time;
- consider learning history;
- balance new problems and review problems;
- recommend a manageable daily plan;
- explain why each problem was selected.

### 6.2 Progressive Problem-Solving Support

The coach should provide levels of assistance:

1. problem restatement;
2. input/output clarification;
3. first directional hint;
4. data-structure or algorithm hint;
5. pseudocode;
6. implementation guidance;
7. complete answer.

The user may explicitly request the complete answer at any time.

### 6.3 Code Explanation

The coach should support:

- full-program explanation;
- selected-block explanation;
- single-line explanation;
- variable-state explanation;
- function-call explanation;
- control-flow explanation;
- time and space complexity;
- alternative implementations;
- possible bugs and edge cases.

### 6.4 Syntax and Library Explanation

The coach should identify and explain:

- programming language syntax;
- standard-library modules;
- standard-library functions;
- common third-party functions;
- parameters and return values;
- complexity where relevant;
- equivalent code;
- current-context purpose.

Initial language priority:

1. Python
2. Java
3. C++
4. JavaScript and Go later

### 6.5 Error Analysis

Users should be able to provide:

- compiler errors;
- runtime errors;
- wrong-answer examples;
- failed test cases;
- selected suspicious code.

The coach should:

- classify the error;
- identify likely causes;
- provide hints before rewriting everything;
- explain the correction.

### 6.6 Learning Records

The system should eventually record:

- problem identifier or metadata;
- date;
- language;
- duration;
- outcome;
- hint level used;
- whether the full solution was viewed;
- notes;
- next review date.

### 6.7 Spaced Review

The product should schedule review using deterministic business rules.

A simple early sequence may be:

```text
1 → 3 → 7 → 16 → 35 → 90 days
```

Difficulty and hint usage may shorten or reset the interval.

---

## 7. Product Interface

### 7.1 Browser Extension

The primary in-problem interface.

Components:

- small floating entry button;
- Side Panel;
- manual paste input;
- right-click action for selected text;
- coaching-mode selector;
- chat history for the current task;
- completion-record form.

### 7.2 Web App

A later management interface for:

- today's plan;
- roadmap;
- learning history;
- review calendar;
- progress statistics;
- saved explanations;
- account and API settings.

The Web App is not the initial coding environment.

---

## 8. Input Sources

Initial supported sources:

- manually pasted problem text;
- manually pasted code;
- manually pasted errors;
- user-selected webpage text sent through the context menu.

Later possible sources:

- screenshots;
- user-approved extraction of current problem metadata;
- user-approved extraction of editor code;
- imported user history.

The system should not automatically crawl or ingest complete problem banks.

---

## 9. Data Storage Principles

The database should store:

- user-owned learning data;
- platform name;
- problem title;
- problem URL;
- difficulty;
- topic tags;
- attempt and review metadata;
- conversation metadata;
- optional user code snapshots.

The system should avoid storing complete copyrighted problem statements as a public shared dataset.

Full problem text may be handled temporarily as user-provided session context and may be discarded unless the user explicitly chooses to save it.

---

## 10. MVP Scope

### MVP 1: Extension Shell

- Manifest V3 extension;
- toolbar action;
- Side Panel;
- manual paste area;
- send button;
- local UI only.

### MVP 2: Selection Input

- right-click selected webpage text;
- send selection to Side Panel;
- preserve line breaks;
- classify input manually or automatically.

### MVP 3: AI Explanation

- FastAPI backend;
- DeepSeek integration;
- whole-code explanation;
- single-line explanation;
- syntax explanation;
- library-function explanation;
- progressive hints;
- complete-answer mode.

### MVP 4: Learning Record

- attempts;
- duration;
- outcomes;
- hint usage;
- review scheduling;
- progress view.

---

## 11. Non-Goals for Early Versions

- reproducing LeetCode's complete content;
- building a full coding platform;
- running arbitrary untrusted code;
- replacing LeetCode's judge;
- social features;
- rankings;
- paid subscriptions;
- enterprise administration;
- every programming language;
- model fine-tuning;
- complex multi-agent orchestration.

---

## 12. Success Criteria

The first useful product should allow a learner to:

1. open the Side Panel while solving a problem;
2. paste or send selected text;
3. request a specific coaching action;
4. receive a clear response from DeepSeek;
5. record the outcome;
6. see the problem scheduled for future review.

The experience should require less page switching than using a general chatbot.
