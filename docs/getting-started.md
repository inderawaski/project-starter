# Getting started

## New project

```bash
python3 scripts/init.py ../my-project
python3 scripts/init.py ../my-project --pack frontend --dry-run
```

The first command creates a project-level `AGENTS.md`, architecture reference, and project-structure skill without overwriting existing files. The second previews optional recommendations.

Edit placeholders in the generated `AGENTS.md` and configure actual verification commands. Install third-party skills using your agent runtime's supported mechanism after reviewing their upstream source and license.

## Global product specification

Install `skills/product-specification` into the global skill directory recognized by each runtime. The location differs by Codex, Hermes, and configuration. Configure Linear separately for each agent. Do not commit access tokens.

Run: “Use product-specification to interview me about this feature. Present the short behavioral review before writing Linear tickets.”

## Maintenance

Open this repository in an agent and say: “Use starter-maintenance. I want to change X because Y.” The agent should inspect decisions, interview only when useful, update relevant files, validate, and write an ADR for significant policy changes.

## Not automatic

The initializer does not install third-party skills, set up Linear, publish to GitHub, or configure CI. Those actions require separate setup and authorization.
