# Visual Review Fixture: Health Appointment Booking

## Review setup

- Synthetic fixture only. No screenshots, real brands, or copied UI.
- Review evidence type: D2, text description only.
- Platform scope: Cross-platform mobile.
- User task: book an appointment safely without missing urgency, location, or preparation requirements.

## Screen description

A health app booking screen lets the user choose a clinician, appointment type, date, and time. The product team wants the screen to feel "calm and simple" while still handling urgent-care warnings and insurance constraints.

## Frame specs

- Frame: 375 x 812 px mobile portrait.
- Header: back button, title "Book visit", and help icon.
- Content area: vertically scrollable.
- Sticky footer: total estimate and "Book appointment" button.
- The date selector uses a 7-day horizontal strip.
- Time slots are shown in a two-column grid.

## Visible hierarchy

1. Clinician card with name, specialty, rating, and next available date.
2. Appointment type segmented control: Video, Clinic, Phone.
3. Date strip.
4. Time-slot grid.
5. Insurance estimate module.
6. Small urgent symptoms notice.
7. Sticky booking footer.

## Components

- Clinician summary card.
- Appointment type segmented control.
- Horizontal date selector.
- Time-slot buttons.
- Insurance estimate disclosure.
- Urgent symptoms notice.
- Sticky footer with estimated cost and primary CTA.
- Help icon in the header.

## Typography

- Screen title: 20 px semibold.
- Clinician name: 18 px semibold.
- Specialty and location: 13 px regular.
- Time-slot labels: 14 px medium.
- Insurance estimate: 13 px regular.
- Urgent symptoms notice: 11 px regular.
- Footer CTA: 16 px semibold.

## Color and state notes

- Available time slots use white background and blue border.
- Selected time slot uses filled blue.
- Disabled time slots are gray with no explanation.
- Urgent symptoms notice is gray text with a small warning icon.
- Insurance estimate uses neutral gray copy: "Estimate may vary".
- Error states are not visible in the default description.

## Interaction states

- Default state described.
- Disabled state exists for unavailable time slots, but reason is not shown.
- Loading state for time slots is a full-screen spinner.
- Error state says "Could not load availability".
- Time zone handling is not described.
- Appointment confirmation state is not described.
- Cancellation or reschedule entry point is not described.

## Known constraints

- Some symptoms may require urgent or emergency care.
- Appointment availability can change while the user is booking.
- Insurance estimate may be unavailable or incomplete.
- Location, video requirements, and preparation instructions may differ by appointment type.
- The design must not diagnose, triage, or claim medical safety from UI alone.

## Expected critique

- The review should flag urgency visibility: urgent symptom guidance is too low in hierarchy and too small for a safety-critical boundary.
- The review should flag disabled time-slot ambiguity: unavailable slots need explanation or filtering, not unexplained gray buttons.
- The review should flag booking confidence gaps: time zone, location/video requirements, preparation notes, and confirmation details are unresolved.
- The review should flag weak loading and error states: full-screen spinner and generic error block the task without preserving chosen clinician/type/date.
- The review should flag sticky footer risk: estimated cost and booking CTA should not imply final insurance certainty.
- The review should recommend concrete fixes: move urgent guidance near appointment type, use clear emergency escalation copy, show disabled reasons, preserve selections during availability refresh, add conflict/slot-taken recovery, clarify estimate language, add confirmation summary before final booking.
- The review should note strengths: clinician context, appointment-type control, date/time selection, and sticky CTA support a focused booking task.

## Prohibited critique

- Do not claim the app is medically safe or unsafe as a whole.
- Do not claim HIPAA, GDPR, WCAG, or clinical compliance.
- Do not invent symptom-specific medical advice.
- Do not assert that the rating is unethical or inaccurate without source context.
- Do not claim exact contrast failure from gray text unless values are provided.
- Do not say the booking flow prevents missed urgent care; only the described warning can be reviewed.

## Severity expectations

- High: urgent-care notice too de-emphasized, unavailable slot ambiguity, final booking without confirmation of time/location/type.
- Medium: full-screen loading, generic availability error, insurance-estimate ambiguity.
- Low: calm visual tone and exact spacing should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected current design-quality score: 2/5.
- Reason: the structure supports booking, but safety escalation, state clarity, and appointment confidence are too weak for a health context.
