# Codex Start Prompt

Copy the prompt below into the first Codex conversation opened at the project root.

---

Please first read all of the following files:

- `AGENTS.md`
- `README.md`
- `docs/PRODUCT_SPEC.md`
- `docs/ARCHITECTURE.md`
- `docs/TECH_DECISIONS.md`
- `docs/DATA_MODEL.md`
- `docs/ROADMAP.md`
- `docs/ORIGINAL_PROJECT_ANALYSIS.md`

Do not immediately implement the entire application.

First complete these tasks:

1. Summarise your understanding of:
   - the product goal;
   - the target user;
   - the core user journey;
   - the MVP boundary;
   - the intended final architecture;
   - the explicitly excluded features.

2. Identify any contradictions, missing decisions, ambiguous requirements, legal risks, privacy risks, security risks, or technically unrealistic assumptions in the documents.

3. Propose an initial repository structure that preserves the required boundaries between:
   - browser extension;
   - FastAPI API layer;
   - application services;
   - DeepSeek provider;
   - repository/database layer.

4. Recommend the smallest practical initial toolchain for the extension. Do not select a large frontend framework unless you can explain why the Side Panel requires it.

5. Break Phase 1 into independently verifiable tasks. Each task must include:
   - goal;
   - files involved;
   - implementation notes;
   - acceptance criteria;
   - test or manual verification procedure;
   - dependencies.

6. Do not add:
   - a copied problem bank;
   - an online judge;
   - code execution;
   - automatic LeetCode scraping;
   - unrestricted webpage permissions;
   - authentication;
   - payments;
   - a Web App;
   - PostgreSQL;
   - DeepSeek integration;
   unless the current milestone explicitly requires them.

7. Do not modify files yet.

8. Wait for confirmation after presenting your analysis and Phase 1 task breakdown.

Be critical and specific. Do not agree with every design decision automatically.
