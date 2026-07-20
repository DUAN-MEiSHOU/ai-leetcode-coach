# Original Project Analysis

Reference repository:

```text
https://github.com/viviannnl/leetcode-coach
```

This document describes the conceptual reference. It does not grant permission to copy code. Check the repository's licence before reusing implementation.

---

## 1. Original Product Position

The original project is best understood as an AI-powered daily practice planner and review scheduler.

It is not:

- an online judge;
- a complete LeetCode clone;
- a live code editor;
- a full interactive coding tutor.

Its main loop is:

```text
Choose roadmap
→ Generate daily plan
→ Solve problems externally
→ Submit natural-language feedback
→ Update attempt history
→ Schedule review
→ Generate the next plan
```

---

## 2. Original User Commands

Conceptually, the original CLI includes actions similar to:

```text
init
plan <available time>
done <natural-language feedback>
progress
```

The user selects a roadmap, asks for a plan, reports results, and views progress.

---

## 3. Original Module Structure

The repository contains a small Python package with modules conceptually responsible for:

- CLI interaction;
- coaching orchestration;
- roadmap loading;
- local JSON state;
- spaced-review logic;
- LLM calls.

A simplified conceptual structure:

```text
CLI
 ↓
Coach
 ├── Roadmap
 ├── Store
 ├── Review Rules
 └── LLM
 ↓
Local JSON State
```

---

## 4. Strong Design Ideas Worth Reimplementing

### 4.1 Small Product Scope

The original project focuses on one valuable question:

```text
What should I practise today?
```

This is a strong MVP decision.

### 4.2 Complete Learning Loop

The product connects:

- planning;
- practice;
- feedback;
- persistence;
- review.

Even with little code, it creates a coherent loop.

### 4.3 LLM and Deterministic Code Separation

The LLM handles:

- plan reasoning;
- natural-language feedback parsing;
- explanatory text.

Traditional code handles:

- state;
- validation;
- roadmap data;
- review intervals;
- persistence.

This separation should be preserved.

### 4.4 Structured Output

The model is expected to return structured data rather than uncontrolled prose.

Our version should retain this principle with Pydantic validation and retry handling.

---

## 5. Original Limitations

The original project does not provide:

- browser integration;
- Web App;
- code selection;
- line-level explanation;
- library-function explanation;
- live progressive hints;
- code execution;
- database server;
- multi-user accounts;
- production monitoring;
- complex testing infrastructure.

It appears designed as a lightweight local demo.

---

## 6. How Our Project Differs

| Original Project | Our Project |
|---|---|
| CLI | Browser Side Panel |
| Local JSON | PostgreSQL |
| Claude-oriented | DeepSeek initially |
| Planning and feedback | Planning, hints, code explanation, review |
| Local single-user | Evolvable toward multi-user |
| No webpage integration | User-initiated selection and paste |
| No backend service | FastAPI backend |
| No Web App | Later management Web App |

---

## 7. Reimplementation Principle

The goal is not to copy the repository line by line.

The goal is to reimplement the useful concepts:

- daily planning;
- roadmap awareness;
- natural-language feedback;
- structured data;
- spaced review;
- progress tracking.

These concepts should be integrated into a new architecture that matches the browser-side coaching product.

---

## 8. First Feature to Reuse Conceptually

The first original feature to reintroduce after the extension and backend work is stable should be:

```text
available time
→ user history
→ due reviews
→ daily plan
```

Before that, build the new product foundation:

- extension;
- Side Panel;
- selection input;
- FastAPI;
- DeepSeek;
- coaching modes;
- persistence.
