# Example: Generate mobile screen concept

## Example prompt

```text
Use the mobile-design-skill.

Design a mobile screen concept for a “Request time off” screen in an enterprise HR app.

Inputs:
- User goal: submit vacation request quickly without missing policy rules
- Platform: cross-platform
- Audience: employees who use the app occasionally
- Constraints: dense policy content, must work for accessibility-sensitive users, company design system exists but is generic
```

## Example output

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Device class: Phone (compact width only; a regular-width layout can be added on request)
Assumptions:
- The user is already authenticated.
- Manager approval rules are handled after submission, not edited on this screen.
- Compact width (phone) only; a regular-width layout can be added on request.

## Screen goal
Help employees submit a time-off request with enough context to avoid preventable errors and policy confusion.

## Primary user task
Choose dates, review request impact, and submit with confidence.

## Information hierarchy
1. Request dates and leave type
2. Balance and policy impact
3. Optional note or supporting detail
4. Submission action
5. Secondary policy details and help

## Recommended layout structure
- Header:
  - Screen title: Request time off
  - Optional back action
- Primary form area:
  - Leave type selector
  - Start date
  - End date
  - Partial-day option if supported
- Context block:
  - Remaining balance
  - Policy warnings or blackout dates
  - Approval expectation summary
- Optional note area:
  - Free-text note
- Primary action area:
  - Submit request button
- Secondary support:
  - Link to full policy
  - Contact HR / help link if needed

## Suggested components
- Segmented control or selection list for leave type — keeps the choice explicit and easy to scan
- Date pickers — reduce input ambiguity
- Inline summary card for balance and policy status — keeps critical constraints near the task
- Inline validation messages — avoids delayed failure after submit
- Sticky bottom CTA on longer screens — protects completion on smaller devices

## Interaction notes
- Recalculate balance and warnings immediately after date selection.
- Keep policy warnings inline, not hidden behind a modal.
- Disable submit only when the form is materially incomplete, and explain why.
- If blackout dates exist, show them before final submit rather than after.

## Empty / loading / error states
- Empty:
  - Default blank state with short helper text under leave type and dates
- Loading:
  - Skeleton or lightweight loading state for balance and policy data
- Error:
  - Inline error if balance service fails, with retry and fallback note that submission cannot be validated yet

## Platform-specific notes
### iOS
- Keep the top area clean and avoid crowding it with too many utility actions.
- Use platform-consistent date input behavior and avoid forcing custom gesture-heavy interaction.

### Android
- Ensure back behavior is predictable if the user entered data but has not submitted.
- Keep supporting actions visually secondary to the main submit path.

## Accessibility considerations
- Use clear field labels, not placeholder-only inputs.
- Keep policy warnings readable and not color-dependent.
- Support text scaling without collapsing the form or hiding validation.
- Preserve logical focus order from leave type to dates to summary to submit.
- Ensure touch targets remain comfortable around date selection and toggles.

## Design quality calibration
- Direction: policy-adjacent baseline — the balance block sits directly under the inputs it depends on (from: baseline) — committed over the calm and dense-modular directions in `Alternatives considered`
- Dimension read: attention path 4, composition 4, typography 3, colour/state 3, density 4, interaction 3, context & brand fit 3, production readiness 2, distinctiveness 1. Median of the assessable = 3.
- Quality target: 3/5 — blocked from 4/5 by Production readiness, stalled at its 2→3 boundary until leave type is decided as one control rather than offered as segmented control or selection list. Typography, colour/state, interaction and context & brand fit each stop at their 3→4 boundary — no value on the title role, no foreground/background pair, no duration or curve, no departure budget — so the median holds at 3 even once the inert cap lifts.
- Attention path:
  - First glance: date range and leave type; second glance: balance/policy impact; final action: Submit request.
- Composition and spacing:
  - Use 16pt/16dp screen padding, 12-16pt/12-16dp between related form fields, and 24pt/24dp before the balance/policy impact block.
- Typography:
  - Use a clear screen title, 16-17pt/16sp body text for form values, and 13-14pt/14sp labels so policy details do not become fragile at larger text sizes.
- Color and state:
  - Reserve semantic color for warnings and errors; pair every warning with text and an icon, not color alone.
- Interaction polish:
  - Recalculate balance with inline feedback rather than a blocking spinner so the form remains stable.
- Signature move:
  - None. With the logo removed this screen is interchangeable with any HR leave form, so it is inert and the artifact caps at 3/5. No brand palette, type, or motion token was supplied, and inventing one here would be fabrication. Exit: supply the design-system accent and one repeatable treatment — for example a `balance-impact` band reused on the request row, the confirmation sheet, and the approval notification — and the inert cap lifts.
- Production checks:
  - Verify Dynamic Type/font-scale, sticky CTA safe-area spacing, offline balance failure, and unsaved-change back behavior.

## Rationale for major choices
- Dates and leave type come first because the system cannot provide meaningful balance or policy feedback until they are chosen.
- Balance and policy impact sit directly below the core inputs because they influence the decision to submit.
- Policy detail is summarized inline and linked out secondarily because the main task is submission, not reading a policy essay on a phone.
- Sticky action treatment is recommended because enterprise forms often become vertically long.

## Alternatives considered
- Policy-first layout — rejected because employees need to enter dates before the policy guidance can become specific and actionable.
- Full multi-step wizard — rejected because this is an occasional enterprise task, but the field count is still small enough to keep visible in one structured screen.
- Hiding balance and policy impact behind a details link — rejected because those details directly affect whether the request can be submitted.
- Direction rejected — calm and generous (from: Headspace / Calm): base unit 8, ratio 1.2, section gap 32, one focal element per screen, motion signature at the slow end of its band — rejected because the policy block needs three values visible simultaneously for comparison, and the larger rhythm pushes the balance summary below the fold on a 4.7-inch device.
- Direction rejected — dense modular (from: Müller-Brockmann, Grid Systems): base unit 4, ratio 1.333, two-column metadata rows, near-monochrome with one signal colour reserved for policy state, 150 ms cross-fade only — rejected because this is an occasional task for non-expert users, where scanning speed matters less than error avoidance, and tighter rows raise mis-tap risk around date selection.

## Next actions
- Confirm whether partial-day requests, attachments, or delegate coverage are in scope.
- Validate whether balance and blackout data are real-time or cached.
- Test readability and error comprehension with text scaling enabled.
```
