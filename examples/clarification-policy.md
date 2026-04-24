# Clarification Policy Examples

These examples show when the skill should ask questions and when it should proceed with assumptions.

---

## Example 1: Blocking visual review

### Prompt

```text
Use the mobile-design-skill.
Review this mobile screen for color contrast, spacing, and hierarchy.
```

### Expected behavior

```md
Mode: Review screen for usability/accessibility
Platform scope: Unspecified
Assumptions:
- No screenshot, Figma link, or detailed visual description was provided.
- Visual contrast, exact spacing, and visual hierarchy cannot be assessed reliably from the prompt alone.

## Clarifying questions
1. Can you share a screenshot, Figma link, or detailed visual description of the screen?
2. Should the review target iOS, Android, or cross-platform behavior?

## Why this blocks
- Color contrast and spacing are visual claims; without visual evidence, the review would risk inventing observations.
- Platform conventions affect hierarchy, navigation, and control treatment.

## Fast path
- I can proceed with a structure-only review if you describe the screen layout, content, controls, and known issues.

## Next actions
- Share the visual artifact, or confirm that a structure-only review is acceptable.
```

---

## Example 2: Non-blocking concept request

### Prompt

```text
Use the mobile-design-skill.
Design a profile edit screen.
```

### Expected behavior

The skill should not stop for a long questionnaire. It should proceed with a limited concept:

```md
Mode: Generate mobile screen concept
Platform scope: Assumed cross-platform phone-first
Assumptions:
- Product domain and audience are not provided, so the concept stays neutral and structural.
- Authentication is already complete before this screen.

[Mode A artifact continues...]

## Next actions
- Confirm product/domain and audience so field grouping, density, and trust level can be tuned.
- Confirm whether native iOS/Android divergence is required before detailed handoff.
```

---

## Example 3: Policy-sensitive spec

### Prompt

```text
Use the mobile-design-skill.
Create a production-ready UI spec for medication refill.
```

### Expected behavior

The skill can begin, but must not invent medical policy:

```md
Mode: Create platform-aware UI spec
Platform scope: Assumed cross-platform phone-first
Assumptions:
- Medication eligibility, pharmacy rules, and clinical safety copy are not provided.
- The spec can define safe UI structure, but cannot invent clinical, legal, or pharmacy rules.

## Clarifying questions
1. Is refill eligibility determined before this screen, or must the screen explain eligibility/rejection?
2. Does the flow support pickup, delivery, or both?
3. Are there required safety states such as doctor approval, interaction warning, or too-early refill?

## Why this blocks
- These answers change the state model, error handling, and safety hierarchy.

## Fast path
- I can draft a conservative base spec with explicit placeholder states for eligibility, pharmacy choice, and safety warnings.

## Next actions
- Answer the three questions above, or confirm the conservative base-spec assumption.
```
