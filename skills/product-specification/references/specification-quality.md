# Detailed specification quality

A detailed spec should allow a coding agent to implement observable behavior without inventing product rules.

Include when relevant:
- Goal and user value
- Scope, non-goals, constraints
- Entry conditions and user journeys
- Functional requirements and state transitions
- Business rules, validation, permissions
- Empty, loading, partial, error, retry, duplicate, cancellation behavior
- Data retention and privacy decisions
- Testable acceptance criteria (Given / When / Then or equivalent)
- Dependencies and cross-ticket contracts
- Open decisions explicitly labeled, with impact

Do not introduce major behavior not covered by discovery and approved behavioral review. Technical implementation details may remain flexible unless they affect product behavior.
