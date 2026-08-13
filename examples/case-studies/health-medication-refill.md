# Synthetic Case Study: Health Medication Refill

## Prompt

```text
Use the mobile-design-skill.

Create a platform-aware UI spec for a medication refill request screen.

Inputs:
- Platform: iOS and Android
- Product: patient health app
- User goal: request a refill before running out of medication
- Audience: patients, including older adults
- Constraints: high trust, no medical advice, prescription eligibility may vary, pharmacy pickup or delivery
```

## Weak response

```md
Mode: Create platform-aware UI spec
Platform scope: Cross-platform
Assumptions:
- The patient has medications.
- The app supports refill requests.

Show a medication card with name, dosage, remaining pills, and a large "Refill now" button. Let the user choose pickup or delivery, then confirm. Add push notifications when the refill is ready. Use a clean design with calming colors and large buttons.

Accessibility requirements: large text, high contrast, and screen reader labels.
Next actions: test with patients and check pharmacy integration.
```

## Why this is weak

- Treats every medication as refillable and every refill as a simple order.
- Does not address eligibility, prescriber approval, pharmacy availability, insurance, or expired prescriptions.
- Risks medical overclaim by presenting "remaining pills" as definitive without source and timestamp.
- Recovery states are missing for rejected, delayed, partial, or out-of-stock requests.
- Accessibility is generic and not tied to medication safety.

## Strong response

```md
Mode: Create platform-aware UI spec
Platform scope: Cross-platform with iOS and Android notes
Assumptions:
- Refill eligibility is determined by backend clinical/pharmacy rules.
- The UI can display medication details already approved for patient view.
- The app does not advise dose changes or replacement medications.

## Screen or flow scope
Single medication refill request from medication detail to request submitted.

## Structural zones
- Medication identity: name, strength, form, prescribed directions summary, prescribing clinician if available.
- Refill status: eligible now, too early, expired, needs clinician approval, processing, ready, unavailable.
- Fulfillment choice: current pharmacy, change pharmacy, pickup/delivery if supported.
- Review and submit: medication, quantity if provided by source system, fulfillment, estimated next step, contact path.

## Components by section
- Status banner with text and icon, not color alone.
- Detail rows for medication name, strength, last filled date, refills remaining when known, pharmacy.
- Primary CTA changes by status: "Request refill", "Message care team", "View pharmacy options", or disabled with reason.
- Inline help for "why not refillable" using approved copy.

## State definitions
- Default eligible: show request CTA and fulfillment options.
- Too early: explain earliest request date if supplied; do not imply clinical judgment.
- Expired/no refills: route to message care team or renewal request if supported.
- Loading: show medication identity only if cached and label status as checking.
- Error: preserve medication detail, show "Refill status unavailable", retry, and pharmacy/care-team contact.
- Submitted: confirmation with request ID/time, expected next status, and notification controls.

## Behavior rules
- If status is unknown, disable submit until eligibility resolves or show a safe contact alternative.
- If the user changes pharmacy, re-check availability before final submit.
- Do not silently replace medication, strength, or pharmacy.
- Preserve user choices if a network retry is needed.

## Spacing and layout notes
- Use a single-column form with 16-20 pt/dp horizontal padding.
- Keep medication identity and status above the fold.
- Older-adult default: larger body text, generous row height, and clear touch gaps.

## Typography rules
- Medication name uses title role; strength/form uses body-emphasis role.
- Status explanation uses body text, not small caption text.
- Critical dates and pharmacy name must not truncate without a detail view.

## Accessibility requirements
- Screen reader order: medication identity, refill status, reason, action.
- Touch targets should meet or exceed platform minimums; older-adult context should use roomier targets.
- Every status pairs text, icon, and semantic label.
- Date, dose, and units must remain visible together.

## Key decision tradeoffs
- Chosen: status-first flow. It prevents users from filling a request that cannot be submitted.
- Rejected: always showing "Refill now". It creates false confidence and weak recovery.

## Platform-specific implementation notes
- iOS: use native confirmation sheet or form screen for review; avoid gesture-only dismissal when choices are unsaved.
- Android: system back from review returns to choices with values preserved; Material dialogs only for final confirmation or blocking errors.

## Next actions
- Confirm refill status taxonomy and approved copy for each status.
- QA eligible, too early, expired, needs approval, pharmacy unavailable, large text, and screen reader order.
```

## Why this is stronger

- Quality target: 5/5 - resilient: unknown, expired, unavailable and submitted states all have safe recovery, density and touch behavior adapt for older adults, and engineers get behavior rules plus QA cases. Refill taxonomy and pharmacy integration are product inputs, not design gaps.
- Starts with clinical/pharmacy eligibility rather than a generic CTA.
- Avoids medical advice and clearly labels backend-driven status.
- Defines safe recovery for unknown, expired, unavailable, and submitted states.
- Gives engineers behavior rules and QA cases.
- Adjusts density and touch behavior for older adults.

## Regression checks

- Does the response avoid changing medication or dose semantics?
- Does it define what happens when refill eligibility is unknown?
- Does it include status-specific CTAs instead of one universal CTA?
- Does it preserve user choices through retry?
- Does it keep medical units, dates, and medication identity inseparable?
