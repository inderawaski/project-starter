# Extending the starter

## Optional skill packs

Optional packs are selected at initialization with one or more `--pack` flags. Keep them relevant to a real project surface; the initializer does not install every pack. The machine-readable catalog at `catalog/skills.json` records the use case, required dependencies, project configuration, limitations, source URL, revision, and license check for each skill.

To add or change a pack:

1. State the project signal that makes it useful and when it should not be installed.
2. Verify the actual skill name, path, instructions, dependencies, installer compatibility, and license at a specific upstream release or commit.
3. Prefer a well-maintained upstream skill that fits. Use original project guidance only when there is no suitable upstream option; keep any additions small and focused.
4. Pin an immutable tag, full commit, or raw file URL. Do not use a moving branch as a reproducibility claim.
5. Add the entry to `catalog/skills.json`. Update `THIRD_PARTY_NOTICES.md`, this guide, and the changelog.
6. Extend `scripts/validate.py` and `tests/` so the catalog and installation behavior stay consistent.

The catalog currently offers:

- `frontend`: Addy Osmani's `frontend-ui-engineering` for user-facing UI work. Configure the actual framework, design system, accessibility baseline, supported browsers, and UI checks in `AGENTS.md`.
- `backend`: Addy Osmani's `api-and-interface-design` for owned service contracts. Add the project's API compatibility, authentication, error, and integration-test conventions to `AGENTS.md`.
- `database`: Neon `postgres-best-practices` for PostgreSQL only. Record the server version, migration tool, transaction practices, and recovery commands. Do not install it for a different database engine.
- `ai`: the local provider-agnostic `ai-product-practices` skill for product behavior that depends on models, prompts, retrieval, or model-triggered actions. It guides evaluation, trust boundaries, and operational decisions without requiring a particular vendor.
- `vercel-ai-sdk`: Vercel's `ai-sdk` skill for projects using Vercel AI SDK. Install any JavaScript package dependencies independently; this skill does not install dependencies or provide general model evaluation coverage.

## Adopt an upstream skill

- **Unmodified upstream:** Keep the original skill external and install it from the pinned source in the catalog.
- **Thin wrapper:** Keep our additional instructions in a separate original skill and identify its upstream dependency. Do not edit upstream contents.
- **Modified fork:** Copy only when a real gap requires changes. Verify the license, preserve notices, record the upstream commit and exact changes in `UPSTREAM.md`, and update `THIRD_PARTY_NOTICES.md`.

Do not claim a revision is tested just because it is pinned. Record the actual source review and which CLI/runtime checks were performed. Skills CLI's own lock metadata can track installation activity but is not treated here as a reproducibility lock; `catalog/skills.json` pins upstream inputs and `starter-skills.lock.json` records the selections made for a project.

## Update defaults

Review upstream changes before changing pins. Check changed skill content, paths, dependencies, license, supported runtimes, and workflow implications. A new starter version applies to new projects; do not rewrite existing projects' lockfiles or installed files silently. Existing projects can compare their `starter-skills.lock.json` to a reviewed newer catalog and opt into the update.
