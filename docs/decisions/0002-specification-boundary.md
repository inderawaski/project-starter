# ADR-0002: Specification and implementation are independent

- Status: Accepted
- Date: 2026-10-14

## Context
Discovery may happen inside a repository or via an independent Hermes agent, while implementation may happen in Codex.

## Options considered
One integrated orchestrator; independent specification and coding processes sharing approved issues/docs.

## Decision
Use an independent global specification skill and Linear/documents as the preferred requirements source. Implementation consumes approved specifications without requiring an agent-to-agent pipeline.

## Consequences
The specification skill can run in different agent environments. Each runtime needs its own skills installation and Linear connection.

## Revisit when
A repeated handoff failure requires stronger integration.
