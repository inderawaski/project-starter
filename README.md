# Agent Project Starter

A small, public, agent-friendly library for starting software projects with clear instructions, useful skills, and verifiable outcomes—without a mandatory agent orchestration pipeline.

## What lives here

- `starter/`: files copied into a new project.
- `skills/`: original skills maintained in this repository.
- `catalog/`: recommended upstream skills and optional packs, with source and review status.
- `docs/`: decisions, maintenance guidance, and extension recipes.
- `scripts/`: bootstrap and validation utilities.
- `AGENTS.md`: instructions for agents *maintaining this library*.

## Quick start

```bash
git clone <YOUR-REPOSITORY-URL>
cd project-starter
python3 scripts/init.py /path/to/my-project
python3 scripts/init.py /path/to/my-project --pack frontend --dry-run
```

The initializer copies `starter/AGENTS.md` and local project-structure guidance. It **never overwrites** existing files. It prints suggested external skill commands rather than executing remote code. Review and install external skills yourself.

For global specification work, install `skills/product-specification` into your agent's supported global skills directory, and configure Linear independently in each agent runtime. See `docs/getting-started.md`.

## Operating model

1. Discuss or provide a draft brief.
2. Use `product-specification` to interview you and present a short behavioral summary.
3. After explicit approval, write detailed Linear issues or a document.
4. Ask your coding agent to implement an issue, or directly handle a small clear task.
5. Verify the outcome; do not require a fixed multi-agent pipeline.

## Updating this library with an agent

Talk to an agent **inside this repository**. It should read root `AGENTS.md`, use `skills/starter-maintenance`, interview you when a change has significant tradeoffs, implement the agreed changes, validate them, and record meaningful decisions in `docs/decisions/`.

Example: “I want frontend projects to recommend accessibility checks. Interview me if necessary, update the catalog and docs, and record why.”

## Scope and limitations

This repository is a starter, not an orchestrator, product management system, or automatic CI gate. The skill catalog is curated *recommendations*, not an independently tested quality ranking. Third-party skills are linked rather than bundled. Review upstream code, instructions, versions, and licenses before installing.

## License

Original material in this repository: MIT (see `LICENSE`). Third-party skills retain their own licenses. See `THIRD_PARTY_NOTICES.md`.
