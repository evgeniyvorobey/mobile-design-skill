# Example: Prepare design rationale / handoff

## Example prompt

```text
Use the mobile-design-skill.

Prepare a design rationale and handoff for a redesign of a mobile appointment booking confirmation screen.

Inputs:
- Platform: iOS and Android
- Product: healthcare appointment booking app
- User goal: confirm booking details and know what happens next
- Audience: patients, including anxious and older users
- Constraints: high trust, accessibility-sensitive, existing component library, limited engineering time
- Design changes:
  - simplified layout
  - more prominent appointment summary
  - clearer preparation instructions
  - moved secondary actions lower
```

## Example output

```md
Mode: Prepare design rationale / handoff
Platform scope: Cross-platform with iOS and Android notes
Device class: Phone (compact width only; a regular-width layout can be added on request)
Assumptions:
- The booking is already successfully completed before this screen appears.
- Secondary actions include reschedule, add to calendar, and contact clinic.
- Existing component library supports alert, summary, and action-row patterns.

## Design objective
Help patients leave the booking flow with clear confidence about what they booked, what they need to prepare, and what they can do next.

## Target users and context
This screen serves patients immediately after booking an appointment. Many users may be stressed, distracted, or reading quickly on a phone. Some users may also have larger text settings or reduced confidence with digital healthcare flows.

## Key design decisions
- Elevated the appointment summary above secondary actions — alternative considered: action-first confirmation — chosen because patients need to verify time, location, and provider before choosing optional follow-up actions.
- Grouped preparation instructions into a dedicated section — alternative considered: mixing instructions into the summary block — chosen because healthcare preparation details need clear scanning and should not compete with the confirmed appointment facts.
- Reduced visual competition around non-essential controls — alternative considered: equal-weight action row near the top — chosen because anxious and older users benefit from a calmer hierarchy after completing a booking.
- Kept next-step guidance explicit — alternative considered: relying on a generic success message — chosen because the screen must answer what happens next without requiring inference.

## Pattern choices and why
- Summary-first layout over action-first layout because a booked appointment is a fact the patient must verify before any follow-up option is worth evaluating, and an action-first screen forces that verification to happen after the decision.
- Sectioned content over a single stacked paragraph because healthcare details are easier to parse when grouped by meaning.
- Secondary actions lower on the screen over equal-weight top actions because reschedule/contact/calendar are important but not equal to the confirmation task.
- Clear instructional text over icon-led hints because confirmation screens in high-trust contexts must reduce uncertainty, not merely announce success.

## Design quality rationale
- Direction: calm confirmation — restraint carries the trust this screen needs, with the accent doing one job (from: Vignelli, The Vignelli Canon) — committed over an action-first and a celebratory direction
- Dimension read: attention path 4, composition 4, typography 3, colour/state 3, density 4, interaction 3, context & brand fit 4, production readiness 3, distinctiveness 4. Median of the assessable = 4.
- Quality target: 4/5 — strong handoff quality; blocked from 5/5 by Production readiness until token names and the state-to-component mapping are stated for the listed states, so two implementers produce the same screen.
- Signature move: the confirmation accent token is the owned asset — `color.accent-confirm` appears in exactly three places (the confirmation checkmark, the primary next-step button, and the success toast) and nowhere else, so recognition builds through repetition rather than through decoration. Kano check: it sits on a delighter, not on a missing affordance; brand-expression budget: one perceptual move on this screen.
- Confirmation summary prominence — mechanism: larger title/body contrast, top placement, and 24dp/24pt separation from secondary actions — fits the high-trust healthcare context because patients need fast confirmation before exploring options.
- Calm section rhythm — mechanism: repeated section headers, 16dp/16pt internal spacing, and 24dp/24pt section gaps — supports anxious and older users by making the screen predictable.
- Reduced secondary-action weight — mechanism: lower placement and secondary button styling — keeps optional actions available without competing with the completed booking state.
- Restrained brand expression — mechanism: brand accent reserved for confirmation/success and primary next step, not every heading — preserves trust and avoids confusing status semantics.
- Handoff resilience — mechanism: explicit state list and large-text QA checks — helps engineering preserve the visual hierarchy under dynamic content and accessibility settings.

## Platform alignment
### iOS
- Keep the confirmation screen calm and clearly structured without overloading the top area.
- Preserve predictable back and dismissal behavior so users do not fear losing their booking state.

### Android
- Ensure back behavior returns users to the correct prior context without implying the booking failed.
- Keep action hierarchy aligned with Material-style emphasis rather than competing equal-weight buttons.

## Accessibility and usability considerations
- Critical appointment details should not rely on color or iconography alone.
- Preparation instructions must remain readable at larger text sizes.
- Secondary actions should be clearly labeled and comfortably tappable.
- The confirmation state should remain understandable even if assistive technology reads the screen linearly.
- This rationale does not claim verified accessibility compliance; implementation and QA validation are still required.

## States and edge cases
- Default confirmation state
- Booking confirmed but preparation details unavailable
- Calendar integration unavailable
- Clinic contact unavailable
- Follow-up action triggered from confirmation screen
- Delayed sync or temporary network issue after confirmation

## Implementation notes
- Reuse existing summary and alert components where possible to reduce engineering lift.
- Treat preparation instructions as structured content, not a large undifferentiated paragraph.
- Maintain separation between confirmed booking details and optional next actions.
- If sticky actions are not feasible, keep the primary information above the fold and secondary actions below with clear headings.

## Open questions
- Are calendar and reschedule actions both required on this screen?
- Is preparation content dynamic by appointment type?
- Should contact-clinic action appear only for certain appointment categories?
- What is the fallback if instructions fail to load?

## Validation plan / recommended testing focus
- Test whether users can accurately state appointment time, location, and next preparation step after a short glance.
- Test large-text behavior on summary and instruction sections.
- Validate that users understand booking is complete even when they navigate back.
- Review edge cases where preparation content or secondary services are unavailable.

## Next actions
- Confirm secondary action scope and ranking with product and support teams.
- Review large-text and assistive-technology reading order during implementation QA.
- Align final copy with medical-content and service-content standards before release.
```
