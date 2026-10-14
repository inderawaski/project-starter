# Instructions for agents maintaining this repository

This repository is an **agent-friendly project starter library**, not an application being built from it. Do not confuse this file with `starter/AGENTS.md`, which is copied into downstream projects.

## Mission and invariants

- Prefer minimal, composable guidance over mandatory orchestrated agent pipelines.
- Keep specification discovery separate from coding implementation.
- Favor observable outcomes and executable checks over prescribed sequences of agent roles.
- Preserve users' intent and their reasons for decisions.
- Never silently introduce a mandatory tool, framework, role, or workflow.
- Keep upstream skills external by default; do not copy them into this repository without checking their license and documenting provenance.

## Request modes

- **Discussion:** Explore, inspect, and recommend. Do not change files unless explicitly asked.
- **Maintenance:** Make requested edits to the starter, skills, catalog, scripts, or docs. Preserve the user's reason for the change as well as the requested outcome.
- **New policy/architecture:** Discuss material tradeoffs first; use `skills/starter-maintenance/SKILL.md`.
- **Bug fix:** Investigate and fix focused defects; verify affected behavior.

If a consequential choice remains unclear, ask focused questions one at a time and propose a concise change before implementation when policy agreement is still needed. Use decisions already stated in the request or accepted ADRs; do not ask users to repeat them. For low-impact details, make a reasonable assumption and state it. Trivial maintenance does not need an interview or ADR.

## Before changing anything

1. Read the affected files and any relevant ADRs.
2. Determine whether the change affects global specification work, per-project starter behavior, or both.
3. Check compatibility with existing conventions and CLI behavior.
4. Explain major alternatives when a decision is non-obvious; request approval before material policy reversals.
5. Keep edits focused. Do not refactor unrelated content.

## Decision records

Use `docs/decisions/TEMPLATE.md` for meaningful changes to philosophy, architecture, default skills, installer behavior, or maintenance policy. Small wording fixes do not need an ADR. Never rewrite an accepted ADR to conceal history: supersede it with a new one and cross-link.

Update `CHANGELOG.md` for user-visible changes. Update `docs/extending.md` or catalog entries when adding recommendations. Do not invent adoption or review statistics.

## Third-party material

For links: record upstream URL and license-check status. For modified copies: verify license, preserve required notices, record upstream commit and changes in `UPSTREAM.md`, and update `THIRD_PARTY_NOTICES.md`. Do not present a wrapper as an unmodified upstream skill.

## Verification

Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v` after changes. For initializer changes, exercise `--dry-run` and a temporary destination. Report checks actually run and any gaps.

## Skills

- `skills/starter-maintenance/SKILL.md` — significant changes to this repository.
- `skills/product-specification/SKILL.md` — upstream product discovery, review, and Linear authoring.
- `skills/project-structure/SKILL.md` — generic architecture guidance for downstream projects.
- `skills/testing-strategy/SKILL.md` — choose focused, proportionate tests for repository code changes.

Never treat discussion as permission to edit, publish, push, or create external tickets.
