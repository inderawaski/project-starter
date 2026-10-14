---
name: starter-maintenance
description: Maintain this project-starter library through conversational changes, focused interviews, decision records, and validation.
---

# Starter maintenance

Use when a user asks to add/change a starter rule, skill, catalog entry, initializer behavior, or philosophy.

1. Inspect root `AGENTS.md`, affected files, and relevant ADRs.
2. Determine intent: what failed, what should change, and which projects benefit.
3. For significant tradeoffs, interview **one question at a time** and challenge speculative complexity.
4. Present a short proposed change and its consequences before implementing material policy changes.
5. After approval, edit only relevant files; preserve upstream ownership and attribution.
6. Write a new ADR for consequential decisions; supersede rather than erase old decisions.
7. Update the changelog and usage docs where appropriate.
8. Run validation/tests and report what passed, what did not, and any outstanding risks.

Do not require an interview for trivial edits. Do not create mandatory multi-agent processes merely because they sound more rigorous.
