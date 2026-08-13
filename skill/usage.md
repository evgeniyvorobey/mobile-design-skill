# Usage Guide

This guide explains how to invoke `mobile-design-skill` in Claude Code or Codex.

---

## Quick start

Load `SKILL.md` as the active instruction set, then provide a design task.

If you want the expanded reference pack available during use, keep these files nearby:

- `skill/modes.md`
- `skill/templates.md`
- `docs/sources.md`
- `docs/workflow.md`
- `docs/clarification-policy.md`
- `docs/judged-mode.md`
- `docs/principles.md`
- `docs/guardrails.md`
- `docs/quality-bars.md`
- `docs/context-defaults.md`
- `docs/heuristics.md`
- `docs/patterns-catalog.md`
- `docs/design-quality.md`
- `docs/design-quality-rubric.md`
- `docs/golden-examples.md`
- `docs/synthetic-case-studies.md`
- `docs/domain-packs/index.md`
- `docs/weaknesses.md`
- `docs/inspiration-sources.md`
- `docs/visual-benchmark-playbooks.md`
- `docs/benchmark-report-format.md`
- `docs/visual-review-fixtures.md`
- `docs/rendered-output-qa.md`
- `docs/self-review.md`

The skill will:

1. classify the request into one mode
2. determine platform scope
3. identify missing information
4. apply clarification policy: ask only blocking questions, otherwise proceed with assumptions
5. apply judged mode when invoked with `--judge`
6. make only minimal labeled assumptions
7. return a structured mode-specific output
8. include accessibility and usability by default
9. include design-quality calibration for visual hierarchy, rhythm, craft, and production readiness when producing design artifacts
10. apply a 1-5 design-quality rubric, deriving the score from a visible dimension read for generated artifacts and exposing both a current and a projected score in reviews
11. use `examples/evals/`, `examples/rubric-before-after.md`, `examples/golden/`, and `examples/case-studies/` as calibration references when tuning quality and taste
12. use domain packs for fintech, health, SaaS, marketplace, social, and education when the product category materially changes risk, hierarchy, state coverage, or trust language
13. use visual benchmark playbooks and benchmark report format to keep references separate from evidence claims
14. use visual-review fixtures to calibrate text-only review discipline and avoid unsupported visual overclaims
15. use rendered-output QA only after a rendered artifact exists; do not block normal design generation waiting for screenshots or builds
16. use `scripts/run_rubric_judge.py` for provider-agnostic LLM-as-judge calibration, including external-agent command runs
17. run known-weakness preflight to avoid generic output, first-idea bias, evidence overreach, platform flattening, happy-path-only design, and weak handoff
18. keep inspiration references separate from UX, accessibility, and platform rationale when inspiration is requested

---

## Minimal prompt pattern

```text
Use the mobile-design-skill.

Task: [describe the request]
Platform: [iOS / Android / cross-platform / unknown]
User goal: [goal]
Context: [audience, product, constraints]
```

---

## Recommended prompt pattern

```text
Use the mobile-design-skill.

Task:
Create a platform-aware UI spec for a recurring invoice detail screen.

Inputs:
- Product: small business invoicing app
- User goal: review invoice status and send a reminder
- Platform: cross-platform
- Audience: busy owners with moderate financial literacy
- Screen type: detail screen
- Constraints: dense content, touch-friendly, accessibility-sensitive, existing token system
- Current wireframe: header with status, totals, line items, timeline, CTA row
```

---

## Choosing the right mode intentionally

You can let the skill classify automatically, or specify intent more directly.

### Generate mobile screen concept
Use for:
- new screens
- early structure
- component and layout direction

Example:
```text
Design a first-pass mobile screen concept for a medication refill screen.
```

### Design mobile user flow
Use for:
- onboarding
- checkout
- booking
- verification
- multi-step tasks

Example:
```text
Map the mobile user flow from install to first success.
```

### Create platform-aware UI spec
Use for:
- turning wireframes into structured specs
- implementation-ready handoff
- platform-specific component and behavior notes

Example:
```text
Turn this wireframe into a platform-aware UI spec.
```

### Review screen for usability/accessibility
Use for:
- critiquing existing designs
- identifying hierarchy, navigation, readability, or accessibility issues
- prioritizing fixes

Example:
```text
Review this Android settings screen for usability and accessibility.
```

### Create typography and spacing system
Use for:
- defining type roles
- density guidance
- spacing scales
- readable mobile systems

Example:
```text
Create a typography and spacing system for a finance app used by older adults.
```

### Prepare design rationale / handoff
Use for:
- documenting decisions
- preparing design review notes
- helping engineering handoff
- summarizing why a solution was chosen

Example:
```text
Prepare a design rationale and handoff for this onboarding redesign.
```

---

## Input quality tips

The skill works best when the prompt includes:

- product or domain
- user goal
- platform
- screen or flow scope
- constraints
- audience
- current screen or wireframe summary if available

But because humans adore missing context, the skill will still proceed with minimal labeled assumptions when necessary.

---

## Good example prompts

### Example 1
```text
Use the mobile-design-skill.

Create a mobile screen concept for a ride-booking pickup confirmation screen.
Platform: iOS
Audience: commuters in a hurry
Constraints: one-handed use, high time pressure, location uncertainty
```

### Example 2
```text
Use the mobile-design-skill.

Design the flow for resetting a forgotten password in an enterprise Android app.
Constraints: regulated environment, MFA required, older employee base
```

### Example 3
```text
Use the mobile-design-skill.

Review a cross-platform profile edit screen.
Screen description:
- avatar at top
- long stacked form
- save button at very bottom
- optional fields mixed with required
- weak error messaging
Constraints: accessibility-sensitive
```

### Example 4
```text
Use the mobile-design-skill.

Generate a mobile screen concept for a premium habit tracker and include inspiration references.
Platform: iOS
Audience: general consumer
Constraints: calm visual direction, accessibility-sensitive, no gamification overload
```

---

## What the skill will not do

The skill will not:

- invent official platform guidance
- invent validated research findings
- claim verified accessibility compliance without sufficient evidence
- block useful output with nonessential questions
- provide aesthetic-only advice detached from task clarity or usability
- return a section-complete response with no real decisions, tradeoffs, or buildable mechanisms
- ignore typography, spacing, navigation, touch behavior, or states

---

## Interpreting the output

Every response starts with:

- `Mode:`
- `Platform scope:`
- `Assumptions:`

Every response ends with:

- `Next actions:`

This makes outputs easy to reuse in product docs, design reviews, tickets, or handoff notes.

---

## Best practices for teams

For team use:

1. keep prompts tied to a user task, not just a screen name
2. include constraints early
3. state platform clearly if native behavior matters
4. use the review mode before final handoff
5. use the rationale mode after major design changes
6. use the typography/spacing mode before components start drifting into chaos, as they always do when nobody is watching
