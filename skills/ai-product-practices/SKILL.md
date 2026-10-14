---
name: ai-product-practices
description: Make AI-backed product behavior measurable, bounded, and safe to change across providers and frameworks.
---

# AI product practices

Use when a product feature depends on model output, retrieval, prompts, or model-triggered actions. Keep recommendations specific to the product's actual risk and stack; this skill does not prescribe a model vendor or application framework.

## Define observable behavior

- Identify what a user can observe, what a wrong answer or action would cost, and how the feature should behave when the model, provider, retrieval source, or tool fails.
- Separate invariants the application can enforce deterministically from quality goals that require human or model-assisted evaluation.
- Make the failure behavior clear: safe refusal, retry, fallback, human review, or a user-visible error, depending on the product.

## Evaluate changes

- Keep a small, versioned set of representative examples for important user journeys, failure cases, and likely abuse cases. Include regressions from prior incidents when appropriate.
- Test deterministic properties with ordinary code tests: schema validity, authorization, tool allowlists, persistence rules, and safe handling of failures.
- Evaluate variable model behavior with suitable measures and reviewed examples. Compare against a baseline when changing prompts, models, retrieval, or output handling; do not treat one successful sample as evidence of quality.
- Use held-out examples or varied inputs where memorization is a concern. Keep thresholds tied to user and business impact rather than choosing a metric for its convenience.

## Keep trust boundaries explicit

- Treat user input, retrieved content, and tool output as untrusted data. Delimit data from instructions and do not let retrieved text expand the agent's authority.
- Enforce identity, permissions, and consequential-action rules in application code, outside model-generated text.
- Parse and validate structured outputs before use. Handle malformed, incomplete, or out-of-policy values as failures.
- Give tools only the permissions and data they need. Require confirmation or a human decision for actions the product classifies as high impact.

## Operate the feature responsibly

- Track the model/provider version, prompt or policy version, and relevant retrieval or tool configuration needed to interpret a result.
- Set project-appropriate latency and cost budgets; define fallback behavior for limits, provider errors, and unavailable dependencies.
- Keep logs useful for debugging without recording secrets or unnecessary sensitive user content. Follow the product's retention and privacy rules.

Do not add an evaluation harness, model judge, telemetry service, or approval flow just because this skill mentions it. Choose the smallest practical checks for the feature's risk.
