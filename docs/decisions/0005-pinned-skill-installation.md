# ADR-0005: Install reviewed upstream skills at pinned revisions

- Status: Accepted
- Date: 2026-10-14
- Supersedes: [ADR-0004](0004-upstream-skills.md)

## Context

ADR-0004 preferred catalog references over installation. That left the agreed default implementation capabilities unavailable in newly initialized projects and made the starter depend on users manually repairing setup. Upstream sources change over time, so installing a moving branch would make starter behavior hard to reproduce. Codex and Hermes have related but distinct runtime setup, and Hermes requires explicit trust for repository-owned project skills.

## Options considered

1. Keep advisory links and ask users to install skills manually.
2. Copy upstream skill content into this repository.
3. Use an established installer with immutable source revisions, keep upstream content external, and record per-project selections.

## Decision

Use Vercel Skills CLI pinned to `1.7.2` from a JSON catalog. Install the five implementation capabilities by default: local original `project-structure` and risk-based `testing-strategy`, plus upstream `systematic-debugging`, `verification-before-completion`, and `code-review-and-quality`. Keep optional packs opt-in. Pin each source by tag, commit, or immutable raw file URL and generate `starter-skills.lock.json` for the requested skill set and revisions.

Do not vendor upstream skill content in the starter. Preserve existing destination files, verify the installed skill entry point, and report installation failures with a failing exit code. Use the runtime's native skill path: `.agents/skills` for Codex and `.hermes/skills` for Hermes. Do not automatically trust a Hermes project; document its explicit trust step. Install global specification skills through a separate command and their runtime-specific global skill directories. On repeat initialization, merge newly requested skills into the generated lock while preserving existing pinned entries.

## Consequences

- A fresh project obtains the agreed core skills when its user has Node.js, `npx`, and source network access.
- A failed download is visible and retryable; the generated lock describes requested inputs and does not falsely claim every remote install succeeded.
- The source manifest is stable until reviewed pins are intentionally changed.
- Upstream license, attribution, compatibility, and revision review remains part of maintenance.
- Codex and Hermes discovery are documented separately; Hermes trust stays a user-controlled step.

## Revisit when

The Skills CLI stops supporting pinned repository sources, a runtime changes its skill paths, or installation failures make the current external-install strategy impractical.
