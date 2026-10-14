---
name: project-structure
description: Apply pragmatic domain and responsibility separation when designing or modifying project structure.
---

# Project structure

Use when introducing a domain, moving code, defining module boundaries, or when existing structure complicates a change. Read `.agents/references/architecture-principles.md` first.

1. Inspect current conventions and identify the business domain affected.
2. Distinguish domain behavior, presentation, persistence, and integrations.
3. Keep feature-specific code together; extract common code only for demonstrated reuse.
4. Prefer a small change that fits the existing repository over wholesale reorganization.
5. Evaluate import direction, ownership, coupling, discoverability, and testability.
6. Explain exceptions when strict domain grouping would worsen clarity.

Do not impose a universal directory tree or add layers without a concrete reason.
