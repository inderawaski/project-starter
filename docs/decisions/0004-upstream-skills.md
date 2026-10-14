# ADR-0004: Reference upstream skills by default

- Status: Accepted
- Date: 2026-10-14

## Context
Copying skills into a starter creates maintenance and attribution burdens.

## Options considered
Vendor all skills; use upstream references; fork only where necessary.

## Decision
Maintain a catalog of upstream references. Use original wrappers for additional behavior and forks only for substantial modifications, with provenance and license notices.

## Consequences
Installation needs network/runtime setup; upstream changes must be reviewed and versions recorded when adopting skills.

## Revisit when
Reproducibility or upstream instability warrants vendoring a specific skill.
