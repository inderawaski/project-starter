# Extending the starter

## Add an optional pack

1. Describe the project signal that justifies the pack (frontend, backend, database, AI).
2. Add actionable recommendations to `catalog/<pack>.yaml`.
3. Prefer upstream references over copies. Review licenses, maintenance, compatibility, and security.
4. If a skill is genuinely needed, install it into the project's supported skills directory.
5. Add project-specific constraints to `AGENTS.md` only when they apply persistently.
6. Record a consequential policy decision in an ADR.

## Adopt a third-party skill

- **Reference:** catalog source, skill name, and tested revision; install from upstream.
- **Wrapper:** create an original skill with your additional contract; link to the upstream skill and specify any dependency.
- **Fork:** copy only when necessary; verify license, preserve notices, include `UPSTREAM.md` with source, commit, and changes.

Do not confuse popularity with quality. Test a skill against real tasks before making it a mandatory recommendation.

## Update defaults

Favor additive, backward-compatible changes. Never silently overwrite files in existing projects. A new starter version applies to new projects; existing projects should opt into updates.
