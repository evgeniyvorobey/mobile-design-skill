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
- Quality target: 4/5 - health-safe handoff once medical copy, release timing, and escalation rules are confirmed.
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
