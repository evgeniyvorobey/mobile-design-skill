# Usage Guide

This guide explains how to invoke `mobile-design-skill` in Claude Code or Codex.

---

## Quick start

Load `SKILL.md` as the active instruction set, then provide a design task.

If you want the expanded reference pack available during use, keep these files nearby:

- `skill/skill.md`
- `skill/modes.md`
- `skill/templates.md`
- `docs/sources.md`
- `docs/workflow.md`
- `docs/design-quality.md`
- `docs/design-quality-rubric.md`
- `docs/weaknesses.md`

The skill will:

1. classify the request into one mode
2. determine platform scope
3. identify missing information
4. make only minimal labeled assumptions
5. return a structured mode-specific output
6. include accessibility and usability by default
7. include design-quality calibration for visual hierarchy, rhythm, craft, and production readiness when producing design artifacts
8. apply a 1-5 design-quality rubric, targeting 4/5 for generated artifacts and exposing current score in reviews
9. use `examples/evals/` and `examples/rubric-before-after.md` as calibration references when tuning rubric scoring
10. run known-weakness preflight to avoid generic output, first-idea bias, evidence overreach, platform flattening, happy-path-only design, and weak handoff
11. keep inspiration references separate from UX, accessibility, and platform rationale when inspiration is requested

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
