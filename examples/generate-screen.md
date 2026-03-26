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
Assumptions:
- The user is already authenticated.
- Manager approval rules are handled after submission, not edited on this screen.
- The primary device is phone-sized, not tablet-first.

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

## Rationale for major choices
- Dates and leave type come first because the system cannot provide meaningful balance or policy feedback until they are chosen.
- Balance and policy impact sit directly below the core inputs because they influence the decision to submit.
- Policy detail is summarized inline and linked out secondarily because the main task is submission, not reading a policy essay on a phone.
- Sticky action treatment is recommended because enterprise forms often become vertically long.

## Next actions
- Confirm whether partial-day requests, attachments, or delegate coverage are in scope.
- Validate whether balance and blackout data are real-time or cached.
- Test readability and error comprehension with text scaling enabled.
```
