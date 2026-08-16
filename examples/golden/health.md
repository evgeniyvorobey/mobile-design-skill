# Golden Example: Health

## Prompt

```text
Use the mobile-design-skill.

Prepare a design rationale and handoff for a mobile lab result detail screen.

Inputs:
- Platform: iOS and Android
- Product: patient health app
- User goal: understand a new lab result and know whether follow-up is needed
- Audience: patients, including anxious users and older adults
- Constraints: high trust, regulated content, no diagnosis, clinician-reviewed copy, accessible data display
```

## Golden output

```md
Mode: Prepare design rationale / handoff
Platform scope: Cross-platform with iOS and Android notes
Assumptions:
- The result has already been released to the patient.
- Reference ranges and clinician comments may be available per result.
- The app must not diagnose or replace professional medical guidance.

## Design objective
Help patients identify what the result is, whether it is in or out of range, what context is available, and what safe next step exists.

## Key design decisions
- Result summary first: test name, value, unit, range status, and collection date sit above explanatory content.
- Context before interpretation: show reference range, prior result if available, and clinician note before generic education.
- Calm escalation: out-of-range states use clear language and next-step guidance without alarmist visual treatment.
- Support path visible: contact care team or view message thread appears near the clinician note, not buried at the bottom.

## Screen structure
- Header: Lab result detail, back navigation.
- Summary section: test name, value, unit, range status, date/time.
- Range visualization: labeled range with exact numeric boundaries and current value marker.
- Clinician note: shown prominently when present.
- Trend section: prior values with accessible table fallback.
- Education section: short approved explanation of the test.
- Next steps: message care team, schedule follow-up, or wait for clinician review depending on result state.

## Design quality calibration
- Quality target: 2/5 - derived, not claimed. The clinical judgement is the strong part: Context and brand fit at 4, and the value/unit/range triad is a genuine owned asset at 4. Everything else is value-empty - Typography craft sits at band 1, failing its 1 -> 2 question because no type role is named at all, Interaction polish at 1, and a network-fetched clinical value carries no loading or error state, which is also a cap. Naming the type roles and defining the fetch states is the first work; two independent scorings of this block both land it at 2.
- Signature move: `layout.value-unit-range` - a fixed value/unit/range triad that keeps the three readings together at every text size instead of reflowing them apart. Repeated on the result card, the trend row, and the history list, so a number is never seen without the range that gives it meaning.
- Trust comes from precise hierarchy, source clarity, and restrained status treatment.
- Avoid making out-of-range results look like emergencies unless clinical policy says so.
- Numeric values, units, range labels, and timestamps must remain visible together so users do not misread context.
- Use color as a secondary cue only; pair every status with text and iconography.
- The design should reduce uncertainty without pretending to interpret the result beyond approved content.

## Platform and accessibility notes
- iOS: keep navigation predictable and avoid hiding clinical support actions behind gestures.
- Android: preserve back behavior to the result list or notification origin without losing read state.
- Support large text by allowing range visuals and tables to stack vertically.
- Screen reader order should read result name, value, unit, status, date, then clinician note before education.

## Production checks
- QA normal, abnormal, critical-policy, pending-clinician-note, no-prior-result, long test name, large text, and screen reader states.
```

## Design-quality notes

- Reward answers that are careful about medical interpretation and source of truth.
- Penalize diagnosis-like wording, alarmist styling, vague "consult a doctor" placement, or chart-only communication.
- Strong health examples make clinician notes, timestamps, units, and reference ranges inseparable.
- The `2/5` is derived from the nine bands, not from the quality of the clinical reasoning, which is the strongest thing here. Two independent scorings agreed. A domain-correct artifact with no type role named and no fetch states is exactly the shape this corpus exists to make visible: judgement is not craft, and the rubric scores both.
