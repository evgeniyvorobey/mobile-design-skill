# Health Mobile Domain Pack

Use this pack for mobile experiences involving fitness, wellness, symptoms, medication, appointments, care plans, health records, vitals, medical devices, or clinical-adjacent support.

This pack provides design recommendations, not medical, clinical, regulatory, or safety certification. Confirm high-risk flows with clinicians, legal, privacy, security, and safety owners.

## When To Use

- Fitness, habit, nutrition, sleep, cycle, mental wellness, or recovery tracking.
- Medication reminders, symptom logs, appointment support, lab results, care plans, or triage-adjacent flows.
- HealthKit, Health Connect, wearable, sensor, or imported health-data experiences.
- Any screen where incorrect interpretation could delay care, increase anxiety, or expose sensitive data.

## Primary User Jobs

- Understand a health state, trend, reminder, or task without panic or false certainty.
- Record data accurately with correct units, timing, context, and source.
- Decide the next safe action: continue, adjust, contact care team, seek urgent help, or wait.
- Manage consent, data sharing, permissions, privacy, and device connections.
- Recover from missed medication, failed sync, incomplete entry, or concerning result.
- Share or export information with the right context and privacy controls.

## Trust And Safety Risks

- Diagnostic or treatment language that exceeds the product's intended use.
- Single data points framed as clinical conclusions without context.
- Hidden units, ranges, timestamps, device source, or measurement confidence.
- Alarmist copy that increases anxiety without a clear next action.
- Overbroad health-data permissions or unclear sharing with providers, insurers, coaches, or family.
- Notification patterns that expose sensitive information on lock screens.
- Accessibility gaps in time-critical or stress-heavy workflows.

## Common Mobile Surfaces

- Today dashboard with tasks, reminders, trends, and safety-relevant alerts.
- Measurement entry for vitals, symptoms, meals, medication, pain, mood, sleep, or activity.
- Trend detail with range, source, timestamp, annotation, and export/share options.
- Medication schedule with dose, timing, missed-dose handling, refill, and interaction disclaimers.
- Appointment or care-plan screen with preparation, instructions, status, and contact paths.
- Device or data-source connection with consent, sync status, conflict handling, and removal.
- Privacy/share center with permissions, recipients, export, deletion, and audit hints.

## Hierarchy Guidance

- Put the user's immediate safe next action ahead of secondary analytics.
- Pair health values with unit, source, timestamp, and context; avoid naked numbers.
- Separate "tracked by user", "imported from device", "provided by clinician", and "estimated".
- Use calm, precise status language; avoid wellness hype for safety-relevant states.
- Make trends understandable in text, not only charts.
- Keep critical actions visible: call, message, book, export, edit, mark taken, pause reminders.
- Place consent and data-sharing explanation before requesting sensitive permissions.

## State And Recovery Requirements

- Empty: no data, no device, no medication, no appointment, no care plan.
- Loading/syncing: show source and whether existing data is stale or incomplete.
- Stale: label last sync and provide a manual refresh or reconnect path.
- Missing: allow "not taken", "unknown", "skipped", or "prefer not to say" where appropriate.
- Conflict: handle duplicate records, device/user mismatches, unit mismatch, or time-zone changes.
- Error: preserve entries; avoid losing symptom or medication logs on network failure.
- Escalation: define urgent, concerning, informational, and routine states with safe copy.
- Privacy recovery: allow disconnect, revoke sharing, delete/export data, and adjust notifications.

## Accessibility Notes

- Support large text, screen readers, high contrast, reduced motion, and clear focus order.
- Do not rely on color alone for severity, adherence, or trend direction.
- Make medication names, dose, units, and times readable at a glance.
- Avoid fast, pulsing, or alarming animations for health warnings.
- Provide captions/transcripts for instructional media.
- Design for users under stress, pain, fatigue, low vision, tremor, or cognitive overload.

## Platform Notes

- On iOS, request HealthKit access only for health/fitness functionality and explain why before permission.
- On Android, use Health Connect permission framing and clear data-source language when applicable.
- Respect system notification privacy; offer discreet reminder modes for sensitive conditions.
- Use platform date, time, measurement, and locale conventions for units and reminders.
- Do not make custom gestures required for core health tasks.

## Evidence And Compliance Boundaries

- Do not make diagnosis, treatment, clinical performance, or emergency-safety claims from design alone.
- Do not imply HealthKit, Health Connect, or wearable integration validates data accuracy.
- Do not infer HIPAA, GDPR, medical-device, clinical, or regional requirements without expert review.
- Benchmarks can inspire structure, but cannot prove safety, accessibility, or clinical appropriateness.
- This pack is not compliance proof; clinical, privacy, and regulatory claims need qualified review.
- If the product provides care recommendations, require a validated clinical and regulatory basis.

## Design-Quality Traps

- Beautiful graphs with no unit, timestamp, source, or plain-language meaning.
- Gamification that pressures unsafe behavior or hides recovery options.
- Anxiety-inducing red alerts without a clear next action.
- Asking for sensitive permissions before explaining user benefit and control.
- Treating missed health tasks as failure rather than recoverable events.
- Mixing coaching, clinical, and marketing language in the same hierarchy.

## Handoff Checks

- Define every health value's unit, source, freshness, range display, and empty/error state.
- Specify consent copy, permission timing, data sharing, export, deletion, and disconnect behavior.
- Include escalation copy owners and review status for safety-sensitive states.
- Provide accessible chart summaries and non-color severity tokens.
- Document medication, reminder, time-zone, and missed-dose edge cases.
- Flag medical, privacy, security, legal, and clinical review requirements.

## Source Anchors

- Apple HealthKit HIG, Android Health Connect, Apple accessibility, Android mobile UI guidance.
- W3C WCAG 2.2, W3C mobile accessibility, NHS digital service manual accessibility design.
- Use these as grounding references; they do not replace clinical or regulatory review.
