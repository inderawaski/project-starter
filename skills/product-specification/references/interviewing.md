# Interview fallback

Use this short fallback only when the runtime cannot load the upstream `interview-me` skill. When that dependency is available, use it as the interview method and follow the product-specific contract in `../SKILL.md`.

Ask one focused question at a time. Resolve actual product decisions, not template fields.

Explore selectively:
- User/problem: who, why, expected outcome
- Trigger and entry: when the behavior starts
- Happy path and state transitions
- Eligibility, permissions, and validation
- Partial success, retries, duplicate actions, failures, cancellation
- Data handling, privacy, persistence, and ownership
- Explicit non-goals and backward compatibility
- Acceptance examples: given context, when action, then observable result

Prefer: “I recommend X because Y; would you rather X or Z?” over a generic open-ended questionnaire.

Keep a private/working decision ledger:
- Confirmed
- Proposed default
- Unresolved
- Excluded

Do not confuse a recommendation with an approved decision. Stop interviewing when remaining ambiguity is low impact or can safely be documented as a default.
