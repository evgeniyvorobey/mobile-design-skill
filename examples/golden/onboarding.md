# Golden Example: Onboarding

## Prompt

```text
Use the mobile-design-skill.

Design the onboarding flow for a mobile habit coaching app.

Inputs:
- Platform: cross-platform
- User goal: set one realistic habit and receive the first reminder
- Audience: first-time users with low patience
- Constraints: avoid over-personalization, deliver value fast, notification permission required eventually, accessible and calm
```

## Golden output

```md
Mode: Design mobile user flow
Platform scope: Cross-platform
Assumptions:
- Account creation can be deferred until after the first habit is configured.
- The product sends reminders, but notification permission should be requested after the user sees why it matters.
- The first session should focus on one habit, not a complete life plan.

## Flow goal
Move from first launch to one configured habit and a meaningful reminder with minimal setup burden.

## Ordered steps / screens
1. Welcome with concrete value proposition and Get started.
2. Choose one habit category from a short list.
3. Pick a starter habit or write a simple custom habit.
4. Choose reminder timing with sensible defaults.
5. Explain notification permission in context, then request system permission.
6. Confirmation screen showing the habit, next reminder, and first tiny action.
7. Optional account creation or sync prompt after confirmation.

## Decision points
- User selects suggested habit vs custom habit.
- User accepts suggested reminder vs edits time/frequency.
- Notification permission granted vs denied vs skipped.
- User creates account now vs later.

## Failure and recovery paths
- Permission denied: keep the habit saved, show in-app reminder fallback, and offer a later enable path.
- User abandons custom text: preserve draft and offer starter suggestions.
- Reminder time invalid or too soon: inline correction with clear reason.
- Account creation skipped: continue without blocking first value if product policy permits.

## Design quality calibration
- Quality target: 4/5 - strong onboarding flow once permission copy, account policy, and habit taxonomy are confirmed.
- Good onboarding earns each question; it should not ask for goals, motivation, demographics, and preferences before one useful habit exists.
- Use calm, task-sized screens with one primary decision each.
- The notification permission request should be preceded by a concrete reminder preview, not a generic permission pitch.
- Confirmation should make the first success feel real: habit name, reminder time, and immediate next action.
- Accessibility quality depends on simple language, large tap targets, and progress that does not rely on tiny step indicators.

## Next actions
- Confirm whether account creation can be deferred.
- Test whether users understand the permission request after seeing the reminder preview.
- Validate that denied permission still leaves the product usable.
```

## Design-quality notes

- Reward answers that deliver first value before heavy personalization.
- Penalize flows that front-load quizzes, require account creation without justification, or request notifications before context.
- Strong onboarding calibration includes skip/deny paths that preserve progress.
