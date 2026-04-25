# Benchmark Report Format

Use this format when the skill needs visual range from 3-5 references without copying screens, layouts, brands, or proprietary UI.

Benchmark reports turn references into design constraints and reusable mechanisms. They do not validate that a pattern is usable, accessible, compliant, or correct for the current product.

## When To Request References

Ask the user for 3-5 references when the request depends on taste, visual direction, or category calibration and the prompt does not already provide enough signal.

Strong triggers:

- The user asks for "premium", "modern", "best-in-class", "high-end", "inspired by", or "like leading apps".
- The task is about visual direction, art direction, brand feel, onboarding tone, paywall feel, dashboard density, checkout confidence, or category benchmarking.
- The product category has strong visual conventions that affect trust, such as fintech, health, enterprise SaaS, marketplace, education, social, or wellness.
- The user asks to improve design quality but provides only functional requirements.
- The skill must choose between multiple plausible visual directions and the cost of guessing is high.

If references are useful but not required, proceed with stated assumptions and include a short `Reference request` note for a stronger next iteration.

## When References Are Optional

The skill can work without references when the request is mostly structural, behavioral, or corrective.

Proceed without asking for references when:

- The user asks for a screen spec, user flow, accessibility review, typography scale, state model, or handoff.
- Platform conventions, accessibility, domain constraints, and implementation details are enough to make a useful recommendation.
- The user needs a first draft quickly and the visual direction can be expressed as neutral defaults.
- The request is compliance-sensitive; references may still inspire presentation, but they cannot decide the rule.
- The user already provided a clear brand system, design system, screenshots, Figma context, or product constraints.

Do not block a useful answer only because benchmarks are absent. Use references to improve calibration, not to replace design reasoning.

## Reference Input Schema

Ask for references in this compact structure:

```md
## References

| Source | Name | Link | Why relevant | Known limitations |
| --- | --- | --- | --- | --- |
| Production UI / flow / portfolio / award / internal product | Short label | URL or unavailable | What this should help calibrate | What it cannot prove or what may not transfer |
```

Field rules:

- `Source`: category of reference, not a credibility claim. Examples: production UI, flow capture, portfolio concept, award page, internal product, design system.
- `Name`: short human label. Avoid implying endorsement.
- `Link`: optional. If the user cannot provide links, accept a concise written description.
- `Why relevant`: name the specific thing to learn: density, hierarchy, tone, motion, component grouping, sequencing, trust pattern, or state coverage.
- `Known limitations`: state why the reference may not transfer: different platform, different audience, unknown accessibility, concept-only, marketing surface, missing states, regulated-domain mismatch.

Use 3 references for a narrow surface, 4 for a flow or multi-screen feature, and 5 for a broad product direction. More than 5 usually creates noise unless the task is explicitly research-heavy.

## Final Report Template

Use this template when returning a benchmark report:

```md
## Context
- Product/task:
- Platform:
- Audience:
- Design goal:
- Constraints:
- What references are allowed to influence:
- What references cannot decide:

## References table
| # | Source | Name | Link | Why relevant | Known limitations |
| --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |

## Borrow
- Mechanism to borrow:
- Why it fits this product:
- How to adapt it:

## Do not copy
- Surface detail to avoid:
- Reason:
- Safer alternative:

## Translate to tokens/components/states
- Tokens:
- Components:
- States:
- Motion/interaction:
- Content rules:
- QA checks:

## Evidence boundaries
- Inspiration only:
- Evidence needed elsewhere:
- Platform/accessibility checks:
- Compliance or domain checks:

## Risks
- Design risk:
- Product risk:
- Accessibility risk:
- Implementation risk:
- Research gap:

## Next actions
- Immediate design decision:
- Prototype or spec task:
- Validation task:
- Open question:
```

For shorter answers, keep the same section order and reduce each section to one or two bullets.

## Scoring And Quality Rules

References inform visual range, not proof. A benchmark-backed answer should only score higher when the skill translates references into concrete design decisions and keeps the evidence boundary intact.

Quality rules:

- Score up when references become tokens, components, states, sequencing rules, interaction behavior, or QA checks.
- Score up when the report names what should not be copied and why.
- Score up when platform, accessibility, and domain constraints are checked independently from references.
- Score down when the answer copies a screenshot, brand treatment, component surface, or layout without adaptation.
- Score down when references are used as proof of usability, accessibility, compliance, conversion, retention, or business impact.
- Score down when the report cherry-picks only visually attractive references and ignores the user's actual task or risk profile.

Reference quality does not automatically raise design quality. A weak translation from strong references is still weak design work.

## Red Flags

- Cherry-picking one polished reference and treating it as category truth.
- Copying a screenshot, component surface, brand expression, illustration style, or motion sequence.
- Ignoring platform conventions, accessibility requirements, large text, contrast, touch targets, or screen reader behavior.
- Treating awards, gallery presence, or portfolio polish as validation.
- Using web-first references as mobile interaction proof.
- Borrowing consumer-app patterns for regulated, high-trust, or enterprise workflows without adjusting risk and density.
- Forgetting hidden states: empty, loading, error, offline, permission denied, long content, localization, and destructive actions.

## Self-Review Checklist

Before returning a benchmark report, confirm:

- Did I ask for references only when they materially improve the answer?
- Did I accept written descriptions when links or screenshots are unavailable?
- Did I separate inspiration from evidence?
- Did I translate references into tokens, components, states, behavior, or QA checks?
- Did I name what must not be copied?
- Did I check platform and accessibility independently?
- Did I keep the recommendation useful if every reference disappeared?
