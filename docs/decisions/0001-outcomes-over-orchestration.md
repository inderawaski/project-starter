# ADR-0001: Outcomes over orchestration

- Status: Accepted
- Date: 2026-10-14

## Context
A mandatory orchestrator, state machine, and specialized agent sequence added substantial design effort before repeated development failures demonstrated the need.

## Options considered
Rigid multi-agent pipeline; single autonomous coding agent with guidance and checks; no shared guidance.

## Decision
Start with a coding agent, concise AGENTS.md, relevant skills, and verification. Agent delegation is optional, not a prerequisite.

## Consequences
Less setup and process overhead. Different agents may take different paths; executable checks and acceptance criteria remain important.

## Revisit when
Documented recurring failures persist despite adequate specs, tests, and guidance.
