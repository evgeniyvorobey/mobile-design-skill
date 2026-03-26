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
Assumptions:
- The booking is already successfully completed before this screen appears.
- Secondary actions include reschedule, add to calendar, and contact clinic.
- Existing component library supports alert, summary, and action-row patterns.

## Design objective
Help patients leave the booking flow with clear confidence about what they booked, what they need to prepare, and what they can do next.

## Target users and context
This screen serves patients immediately after booking an appointment. Many users may be stressed, distracted, or reading quickly on a phone. Some users may also have larger text settings or reduced confidence with digital healthcare flows.

## Key design decisions
- Elevated the appointment summary above secondary actions
- Grouped preparation instructions into a dedicated section
- Reduced visual competition around non-essential controls
- Kept next-step guidance explicit instead of relying on users to infer what happens after booking

## Pattern choices and why
- Summary-first layout because users need confirmation before optional follow-up actions
- Sectioned content because healthcare details are easier to parse when grouped by meaning
- Secondary actions placed lower because reschedule/contact/calendar are important but not equal to the confirmation task
- Clear instructional text because confirmation screens in high-trust contexts must reduce uncertainty, not merely announce success

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
