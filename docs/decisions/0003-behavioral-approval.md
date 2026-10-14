# ADR-0003: Approve behavior, not a lengthy PRD

- Status: Accepted
- Date: 2026-10-14

## Context
Long detailed spec reviews are burdensome, yet ambiguity must be resolved before implementation.

## Options considered
Approve a full detailed PRD; skip approval; interview deeply then approve a short behavioral summary.

## Decision
Interview about important edge cases and acceptance criteria first. Present only a concise behavioral/flow summary for explicit approval. After approval, generate detailed Linear issues or documents.

## Consequences
Review stays short. The agent must avoid inventing significant new decisions during detailed authoring and must return for clarification if it discovers one.

## Revisit when
Repeated misunderstandings survive behavioral approval.
