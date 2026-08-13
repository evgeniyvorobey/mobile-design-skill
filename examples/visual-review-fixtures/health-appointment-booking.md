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

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform mobile
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- This is a phone-first booking screen, 375 x 812 px.
- The urgent-symptoms notice is the only safety boundary present on this screen.
- Confirmation, time zone, and reschedule flows are out of scope because they are not described.

## Quick summary
The screen supports a focused booking task — clinician, type, date, time, estimate — but it under-weights the parts that matter most in a health context: the urgent-symptoms boundary sits low and tiny, unavailable slots are unexplained, and the user lacks confirmation of time zone, location/video requirements, and what they are actually booking. Loading and error states block the task without preserving selections. Current quality is low for a safety-relevant flow. Structure-and-behavior fixes have a clear path to a stronger score; visual tone cannot be judged from text.

## Strengths
- Provides clinician context (name, specialty, rating, next available) to support an informed choice.
- Offers a clear appointment-type control (Video / Clinic / Phone) up front.
- Combines date and time selection with a sticky estimate and primary CTA for a focused task.

## Findings

### F1 — Urgent-symptoms guidance is de-emphasized
- Lens: Usability
- Observation: The urgent-symptoms notice is sixth in the hierarchy, sits low on the screen, and is described as small text with a small icon.
- Violated principle: Nielsen #5 Error prevention; Nielsen #1 Visibility of system status (safety-critical boundary).
- User consequence: A user with urgent symptoms may not see the guidance in time and could book a routine slot instead of seeking emergency care.
- Change: Move urgent guidance near the appointment-type choice (before slot selection) and give it clear escalation copy and prominence appropriate to a safety boundary.
- Predicted effect: Should raise the chance the urgent path is seen before booking; confidence M (D2 text-only — structural inference, not measured). This reviews only the described warning; it does not claim the flow prevents missed urgent care.
- Severity: 3 (major) — occasional but high impact (safety), persistent until repositioned.
- Moves: Attention path & hierarchy 2→3; lifts cap: safety-boundary visibility.

### F2 — Unavailable time slots are unexplained
- Lens: Usability
- Observation: Disabled time slots are gray with no reason shown; the disabled state exists but does not explain why.
- Violated principle: Nielsen #1 Visibility of system status; Nielsen #9 Help users recognize, diagnose, and recover.
- User consequence: Users cannot tell whether a slot is taken, outside hours, or unavailable for their appointment type, causing confusion and repeated taps.
- Change: Show a reason for disabled slots (or filter them out) and distinguish "taken" from "unavailable for this type."
- Predicted effect: Should reduce confusion and dead-end taps on the slot grid; confidence M (D2 text-only).
- Severity: 3 (major) — frequent, moderate-to-high impact, persistent.
- Moves: Production readiness 2→3; lifts cap: unexplained disabled state.

### F3 — Final booking lacks a confirmation summary
- Lens: Usability
- Observation: There is no confirmation state; time zone is undescribed, and location/video requirements and preparation notes are not surfaced before the user taps "Book appointment."
- Violated principle: Nielsen #5 Error prevention; Nielsen #1 Visibility of system status.
- User consequence: Users may book the wrong time (time-zone mismatch) or arrive unprepared for the wrong modality, which is costly to correct in a health context.
- Change: Add a confirmation summary before final booking that states time (with time zone), modality, location/video requirements, and any preparation notes.
- Predicted effect: Should reduce wrong-time and wrong-modality bookings; confidence M (D2 text-only).
- Severity: 3 (major) — occasional but high impact, persistent until a summary exists.
- Moves: Production readiness 2→3; lifts cap: missing confirmation.

### F4 — Loading and error states discard task context
- Lens: Usability
- Observation: Loading availability is a full-screen spinner; the error is generic ("Could not load availability"); neither preserves the chosen clinician/type/date.
- Violated principle: Nielsen #1 Visibility of system status; Nielsen #9 Error recovery.
- User consequence: A full-screen spinner and generic error block the task and can lose the user's selections, forcing re-entry.
- Change: Scope loading to the slot region, give the error a cause and retry, and preserve clinician/type/date across refreshes; add slot-taken/conflict recovery.
- Predicted effect: Should reduce lost selections and dead-end errors; confidence M (D2 text-only).
- Severity: 2 (minor) — occasional, moderate impact, persistent until states improve.
- Moves: Interaction polish & motion 2→3.

### F5 — Sticky estimate may imply false cost certainty
- Lens: Usability
- Observation: The sticky footer pairs a total estimate with the booking CTA; insurance estimate copy is neutral gray ("Estimate may vary") and may be unavailable or incomplete.
- Violated principle: Nielsen #1 Visibility of system status; match between system and the real world (cost expectations).
- User consequence: A prominent footer total next to "Book appointment" can read as a final price, surprising users when insurance differs.
- Change: Make the estimate's provisional nature explicit at the CTA (clearly an estimate, not a final charge) and state when an estimate is unavailable.
- Predicted effect: Should reduce false certainty about final cost; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Production readiness 2→3.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {1, 1, 2, 2, 2, 3}; pinned by the de-emphasized urgent boundary (F1), unexplained disabled slots (F2), and missing confirmation (F3).
- Projected: 3/5 — median of the assessable projected bands {1, 3, 3, 3, 3, 4} once F1+F2+F3 land (plus F4/F5); held there by the typography and distinctiveness bands no finding touches.
- Ceiling note: with a visual pass confirming tone, contrast, and large-text behavior the leading band reaches 4, but the inert-screen cap holds the artifact at 3/5 until the screen carries one owned asset (contrast of gray notices and dark mode are still unverified from the description).
- Primary lever(s): F1 + F3 (safety visibility and pre-booking confirmation, the two that most pin a health flow at 2).

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path & hierarchy | 2 | 3 | F1 reposition (rung 2→3) | provisional |
| Production readiness | 2 | 4 | F2/F3/F5 lift task-safety caps | provisional |
| Interaction polish & motion | 2 | 3 | F4 states (rung 2→3) | provisional |
| Color, state & contrast | 1 | 3 | unavailable is gray with no other cue, so the second-cue test fails (F2); 3→4 needs stated pairs and their increased-contrast values | provisional |
| Typography craft | 3 | 3 | seven roles carry stated sizes and weights; 3→4 needs the behaviour named when text scales up, which no finding supplies | provisional |
| Distinctiveness & owned assets | 1 | 1 | inert — "calm and simple" is an adjective, not an owned asset, and no finding adds one | provisional |
- Projected overall = median of the assessable projected dimensions {3, 4, 3, 3, 3, 1} = 3. Not the sum of per-dimension gains; colour stops at 3 because a description states no pair, and that rung is never projected upward from text.

## Severity index
- 4 (catastrophe): none
- 3 (major): F1, F2, F3
- 2 (minor): F4, F5
- 1 (cosmetic): none

## Platform-convention mismatches
- Cross-platform caution: the sticky footer and back behavior should respect each platform's safe-area and navigation conventions.
- The segmented appointment-type control and date strip should follow platform-idiomatic selection patterns rather than a single forced style.

## Unresolved assumptions
- Cannot verify contrast of the gray urgent notice or estimate copy from text.
- Cannot verify the "calm and simple" visual tone without a screenshot.
- Cannot verify tap-target sizes for time slots from the description.
- Cannot verify time-zone handling, confirmation, or reschedule flows because they are not described.

## Next actions
- Reposition and strengthen the urgent-symptoms guidance and add a pre-booking confirmation summary (time zone, modality, location/video, prep).
- Explain or filter unavailable slots and preserve selections across availability refresh and errors.
- Run a visual pass with large text and the safety/error scenarios to confirm the projected score.
```

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

Severity uses the Nielsen 0-4 scale (High maps to 3, or 4 if irreversible/catastrophic; Medium to 2; Low to 1).

- 3 (major): urgent-care notice too de-emphasized, unavailable slot ambiguity, final booking without confirmation of time/location/type.
- 2 (minor): full-screen loading, generic availability error, insurance-estimate ambiguity.
- 1 (cosmetic): calm visual tone and exact spacing should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected score: current 2/5 → projected 3/5 (flat median of the assessable dimensions, conditional, provisional D2).
- Reason for current: the structure supports booking and the type roles are decided, but safety escalation, state clarity, unexplained gray disabled slots, and appointment confidence are too weak for a health context.
- Reason for projected: repositioning the urgent boundary, explaining disabled slots, and adding a pre-booking confirmation lift production readiness to 4 — but typography stays at 3 because no finding names the text-scaling behaviour, the screen owns no asset, and visual tone and contrast of gray notices cannot be raised from a text-only description.
- No Bold move is expected: the screen has unresolved severity-3 findings, so the Bold move trigger is not met.
