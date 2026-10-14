# Getting started

## Requirements

- Python 3 for the scripts.
- Node.js and `npx` for the pinned Vercel Skills CLI (`skills@1.7.2`).
- Network access to the exact GitHub tags or commits listed in `catalog/skills.json` on the first install.

The catalog is the source of truth for core skills, upstream pins, pack recommendations, license checks, and the installer version. Skills CLI's own update metadata is not treated as a lockfile; each source URL here pins a tag, commit, or exact raw file revision.

## Initialize a project

Preview the base Codex setup and an optional frontend pack:

```bash
python3 scripts/init.py ../my-project --runtime codex --pack frontend --dry-run
```

Create it:

```bash
python3 scripts/init.py ../my-project --runtime codex
```

The initializer copies `starter/AGENTS.md` and `.agents/references/architecture-principles.md`, installs the maintained local `project-structure` and `testing-strategy` skills, and installs the three pinned upstream core skills. It writes `starter-skills.lock.json` with the chosen revisions. Project files are never overwritten; repeat initialization merges newly requested skill pins into the generated lock while preserving existing pins. A failed or unverifiable upstream install is printed to stderr and causes a nonzero exit code.

Choose only the packs the project needs:

```bash
python3 scripts/init.py ../my-project --runtime codex --pack backend --pack database
```

Packs are not installed by default. `database` is specifically for PostgreSQL. `ai` provides provider-agnostic practices; add `vercel-ai-sdk` only for projects using that SDK. It does not add an `ai` package dependency. See [Extending the starter](extending.md) for each pack's signals, prerequisites, and limits.

### Codex

The initializer targets the project-local `.agents/skills/` directory, which Codex discovers ([Skills CLI v1.7.2 runtime paths](https://github.com/vercel-labs/skills/blob/v1.7.2/README.md#supported-agents)). Start a Codex session in the project after initialization. The project-level `AGENTS.md` contains short persistent instructions; specialized procedures stay in skills.

### Hermes

Run the same initializer with `--runtime hermes`. The pinned Skills CLI targets Hermes' native project skills directory, `.hermes/skills/` ([CLI mapping](https://github.com/vercel-labs/skills/blob/v1.7.2/README.md#supported-agents), [Hermes project-skill documentation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md)). Hermes uses the nearest `.git` directory as the project root and requires explicit trust before it loads repo-owned skills. After creating or initializing the Git repository, run:

```bash
hermes skills trust /path/to/my-project
```

The initializer does not grant trust. These runtime-specific paths match the pinned Skills CLI's Codex and Hermes targets. Hermes installation/trust is documented, but should be exercised in a working Hermes installation before relying on it.

## Global product specification

Specification generation is intentionally separate from project initialization. Install its global entry point and pinned `interview-me` dependency for the runtime you use:

```bash
python3 scripts/install_specification.py --runtime codex
# or
python3 scripts/install_specification.py --runtime hermes
```

For Codex this installs to `~/.agents/skills/`; for Hermes it installs to `~/.hermes/skills/`. The script uses the same pinned Skills CLI for the upstream skill and copies the repository's original product-specification skill and its references. Existing global files are preserved. Use `--dry-run` to preview. The install takes effect in new sessions; restart or open a new session if a skill is not listed.

`product-specification` remains the single entry point for the product workflow and uses the upstream `interview-me` interviewing method when skill composition is available. It includes a concise fallback for hosts that cannot load another skill. Ask it to interview about a rough idea, present the behavioral summary, and wait for explicit approval before authoring detailed tickets or documents.

Configure Linear separately in the runtime if you want it to create issues or documents there. Do not commit access tokens. Markdown remains available when Linear is not configured.

## Maintenance and boundaries

- Root `AGENTS.md` and `skills/starter-maintenance` maintain this starter repository.
- `skills/product-specification` and upstream `interview-me` provide the global specification workflow.
- Initializer output provides project-level implementation instructions and core skills.
- Selected optional packs add project-specific skills only where relevant.

Discussion-only requests do not authorize code changes. Small direct coding requests remain supported without a Linear issue. No stage sequence, orchestrator, or dedicated reviewer agent is required.

## Verification

After initialization, inspect `starter-skills.lock.json`, the installed `SKILL.md` files, and command output. For a Hermes project, check `hermes skills list` after trust and start a new session. The starter repository's own checks are:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```
