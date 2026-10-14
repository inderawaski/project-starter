# ADR-0006: Keep testing and review proportional to change risk

- Status: Accepted
- Date: 2026-10-14

## Context

The starter requires testing and review capabilities but does not require a fixed agent sequence. The initially listed Addy Osmani `test-driven-development` skill enforces a strict red-green-refactor workflow, which is stronger than the project's stated testing requirement. Addy's `code-review-and-quality` skill also recommends review for every change; invoking it unconditionally would turn review into a formal stage even for trivial work.

## Options considered

1. Require strict TDD and formal review for every change.
2. Leave testing and review as generic, unresolved advice.
3. Provide a small original risk-based testing skill, make the upstream review skill available, and condition invocation on task size and risk.

## Decision

Choose option 3. `testing-strategy` covers test levels, observable behavior, regression prevention, mocking, deterministic isolation, test value, and effort proportionate to risk. It recommends test-first development when it helps but does not mandate it. Install upstream `code-review-and-quality` by default, and direct the implementation instructions to load it for requested reviews and consequential, broad, or security-sensitive changes. Tiny changes get a proportionate self-check, not a separate reviewer or stage.

## Consequences

- The default setup covers the required testing and review capabilities without prescribing the same process for every task.
- Testing guidance is original and therefore maintained and reviewed in this repository.
- The selected upstream review skill has supplementary repository-level checklists that a single-skill install does not include; the skill's own review axes remain available and this limitation is documented.

## Revisit when

Project evidence shows the risk-based guidance is producing recurring test gaps or unnecessary review burden.
