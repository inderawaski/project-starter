# Project agent instructions

> Replace bracketed placeholders when initializing this project. Keep this file short; detailed procedures belong in skills and references.

## Project context
- Product: [what it does]
- Users: [who benefits]
- Stage: [prototype / MVP / production]
- Stack: [languages, frameworks, package manager]
- Important commands: [install / test / lint / typecheck / build]

## Engineering priorities
- Correct behavior, simplicity, maintainability, and clear boundaries.
- Follow existing patterns unless they cause a concrete problem.
- Organize primarily by business domain, with responsibility separation within each domain.
- Avoid speculative abstractions and unrelated refactoring.
- See `.agents/references/architecture-principles.md` and the installed `project-structure` skill (`.agents/skills/` in Codex or `.hermes/skills/` in Hermes).

## Request modes
- **Discussion:** Answer and inspect as needed; do not edit code unless asked.
- **Implement issue:** Read the issue and linked context; inspect the repository; implement the agreed behavior; verify.
- **Direct change:** Proceed on small, clear tasks. Ask focused questions or suggest specification discovery if behavior or scope is materially unclear.

## Decision boundaries
- Make routine technical choices autonomously.
- Ask before consequential changes to user-visible behavior, data, security, APIs, architecture, or scope.
- If the approved spec conflicts with the codebase or constraints, surface the conflict; don't silently rewrite requirements.
- Do not perform destructive actions, deploy, publish, or change external tickets without explicit authorization.

## Quality and completion
- The starter provides skills for architecture, debugging, testing, verification, and review. Use each when the task calls for it; availability does not mean every skill must be invoked on every change.
- For failures, use systematic debugging to find the cause before changing code. Choose tests by observable behavior and risk; test-first work is useful when it clarifies behavior or guards a regression, but is not mandatory.
- Run relevant tests, lint, type checks, and build commands where available; do not claim unrun checks passed.
- Use the code-review skill when a review is requested or a change is consequential, broad, or security-sensitive. Tiny changes need a proportionate self-check, not a separate review stage or reviewer agent.
- Report changed behavior, checks run, limitations, and unresolved issues.

## Project-specific rules
[Add only constraints that matter. Add optional skill packs as the project demands.]
