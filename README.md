# Agent Project Starter

A small, public, agent-friendly library for starting software projects with clear instructions, useful skills, and verifiable outcomes—without a mandatory agent orchestration pipeline.

## What lives here

- `starter/`: project instructions and architecture reference copied into a new repository.
- `skills/`: original project-structure, testing-strategy, AI product-practices, product-specification, and starter-maintenance skills.
- `catalog/skills.json`: pinned upstream skill sources, runtime installer version, and optional packs.
- `docs/`: getting started, extension guidance, and decision history.
- `scripts/`: project initializer, global specification installer, shared Skills CLI adapter, and validation.
- `AGENTS.md`: instructions for agents maintaining this library.

## Quick start

Requirements: Python 3, Node.js with `npx`, and network access to the pinned GitHub sources on first installation.

```bash
git clone <YOUR-REPOSITORY-URL>
cd project-starter
python3 scripts/init.py ../my-project --runtime codex
```

The initializer installs five implementation skills: the local `project-structure` and `testing-strategy` skills, plus pinned upstream `systematic-debugging`, `verification-before-completion`, and `code-review-and-quality`. It records requested skills and source revisions in `starter-skills.lock.json`; repeat runs merge newly requested skills and keep existing pins. Project files are never overwritten. Failed or unverifiable upstream installs produce a nonzero exit status and a visible error.

Preview before writing:

```bash
python3 scripts/init.py ../my-project --runtime codex --pack frontend --dry-run
```

Optional packs are installed only when selected. Available packs are `frontend`, `backend`, `database` (PostgreSQL only), `ai` (provider-agnostic product practices), and `vercel-ai-sdk` (Vercel AI SDK implementation guidance). See `docs/getting-started.md` for runtime setup and project-specific caveats.

For Hermes, use `--runtime hermes`. Codex skills go under `.agents/skills`; Hermes skills go under its native `.hermes/skills` path. Hermes requires a Git repository to be trusted before it loads project skills; initialize Git and then run `hermes skills trust /path/to/my-project`. Trust is an explicit Hermes security step and is not performed by the initializer.

## Global specification workflow

The product-specification workflow is global and separate from per-project implementation skills. After cloning, run:

```bash
python3 scripts/install_specification.py --runtime codex
# or
python3 scripts/install_specification.py --runtime hermes
```

This installs the original `product-specification` entry point and pinned upstream `interview-me` into the runtime's global skills directory. The local skill has a short fallback for runtimes that do not compose one skill from another. Linear access must be configured in the chosen runtime; Markdown remains supported when Linear is unavailable.

## Operating model

1. Bring a rough idea or draft to `product-specification` for conversational discovery.
2. Review and explicitly approve a concise behavioral summary.
3. After approval, create detailed Linear issues or a document.
4. Implement an approved issue or a small, clear direct request; discussion-only requests do not modify code.
5. Use relevant skills and verify the outcome without requiring a fixed multi-agent pipeline.

## Maintaining this library

Talk to an agent **inside this repository**. It should use root `AGENTS.md` and `skills/starter-maintenance`, understand the reason for the proposed change, inspect relevant decisions, interview only where consequential choices remain, and update documentation, ADRs, and validation as appropriate.

Example: “Our testing guidance produces too many low-value tests. Review the current policy, ask me about the problem where needed, and implement an agreed adjustment.”

## Scope and attribution

This repository is a starter library, not an orchestrator, project management system, or automatic CI gate. Upstream skill content is installed from its original source at recorded revisions; third-party skill files are not bundled here. Optional packs remain opt-in. See `THIRD_PARTY_NOTICES.md` for source and license checks and `docs/decisions/` for the reasons behind material choices.

## License

Original material in this repository: MIT (see `LICENSE`). Third-party skills retain their own licenses.
