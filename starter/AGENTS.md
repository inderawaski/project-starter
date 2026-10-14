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
- See `.agents/references/architecture-principles.md` and `.agents/skills/project-structure/SKILL.md`.

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
- Use relevant skills for architecture, debugging, testing, verification, and review.
- Run relevant tests, lint, type checks, and build commands where available; do not claim unrun checks passed.
- Review significant changes for correctness, regressions, and security.
- Report changed behavior, checks run, limitations, and unresolved issues.

## Project-specific rules
[Add only constraints that matter. Add optional skill packs as the project demands.]
