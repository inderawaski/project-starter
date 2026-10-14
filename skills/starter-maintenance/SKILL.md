---
name: starter-maintenance
description: Maintain this project-starter library through conversational changes, focused interviews, decision records, and validation.
---

# Starter maintenance

Use when a user asks to add/change a starter rule, skill, catalog entry, initializer behavior, or philosophy.

1. Inspect root `AGENTS.md`, affected files, and relevant ADRs.
2. Understand the user's motivation, what failed, what should change, and which projects benefit. Preserve stated reasons alongside the requested outcome.
3. Use the user's existing decisions first. For consequential unresolved choices, interview conversationally, **one question at a time**, and challenge speculative complexity.
4. When a material policy choice still needs agreement, present a concise proposal with its consequences before editing. Do not repeat questions already answered in the request or accepted ADRs.
5. Edit only relevant files; preserve upstream ownership and attribution.
6. Write a new ADR for consequential decisions; supersede rather than erase old decisions.
7. Update the changelog and usage docs where appropriate.
8. Run validation/tests and report what passed, what did not, and any outstanding risks.

Do not require an interview for trivial edits. Do not create mandatory multi-agent processes merely because they sound more rigorous.
