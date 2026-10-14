---
name: product-specification
description: Interview a user about a rough product idea, confirm a concise behavioral summary, then write detailed implementation-ready specs to Linear or documents.
---

# Product specification

Use when the user brings a rough idea, draft spec, feature request, or wants requirements clarified. This skill is independent of the code repository, but may inspect repository context if available and relevant.

## Interviewing dependency

Use Addy Osmani's upstream `interview-me` skill as the interviewing foundation when it is installed in the same runtime. It provides focused, conversational, one-question-at-a-time discovery. This skill owns the product-specific scope, sufficient-discovery threshold, approval boundary, and authoring contract below. Do not substitute a different upstream end-to-end specification workflow.

Some runtimes do not reliably load one skill from another. In that case, use the concise fallback in `references/interviewing.md`; it captures only the interview behaviors needed here and does not attempt to reproduce the upstream skill. Install instructions and the pinned source are in `catalog/skills.json` and `docs/getting-started.md`.

## Contract

**Never publish detailed Linear tickets or documents before explicit approval of the concise behavioral review.** Interview about edge cases and acceptance criteria *before* approval, but do not dump their exhaustive detail in the review.

## Phase 1 — Understand and interview

- Read the brief and any available relevant prior documents or repository context.
- Interview conversationally, **one consequential question at a time**.
- State a hypothesis or recommendation when it makes decisions easier.
- Explore goals, scope, user journeys, permissions, business rules, alternatives, failure and partial states, edge cases, and acceptance criteria.
- Challenge vague words such as “simple”, “automatic”, and “fast”.
- Distinguish confirmed decisions, recommendations, assumptions, and unresolved questions.
- Prioritize material ambiguity. Avoid exhaustive hypothetical interrogation.
- If the user provides a complete draft, interview only about meaningful gaps.

See `references/interviewing.md`.

## Phase 2 — Short behavioral review

Produce a short, scannable account of:
- Goal and in/out of scope
- Main user flow
- Significant alternate/failure flows
- Key decisions and exclusions
- Any remaining material assumptions

Target a 1–3 minute review for an ordinary feature. **Do not present the full edge-case matrix or detailed acceptance criteria.** Ask: “Is this the intended behavior and scope?” Revise until explicitly approved.

See `references/behavioral-review.md`.

## Phase 3 — Author detailed specifications

After approval:
- Expand *previously discussed* behavior into actionable, testable requirements.
- Include scope, flows, rules, states, edge cases, acceptance criteria, dependencies, and non-goals as applicable.
- Choose one issue for a small coherent change; use parent/child issues for independently implementable work.
- Keep a parent-level behavioral contract if splitting.
- Do not silently invent significant product behavior. Reopen discovery for material gaps.
- Prefer Linear when available and authorized; otherwise draft a document for user review or export.
- Before external writes, confirm the target team/project if not already known. Never infer destructive operations.

See `references/specification-quality.md` and `references/linear-authoring.md`.

## Separation of responsibilities

This skill authors specifications. It does not implement, deploy, or orchestrate coding agents. Any implementation handoff is a link to approved issues/docs, not a mandatory pipeline.
