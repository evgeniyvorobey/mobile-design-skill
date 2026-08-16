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
- Dimension read: attention path 3, composition 3, typography 1, colour/state 3, density 3, interaction 3, context & brand fit 3, production readiness 2, distinctiveness 5. Median of the assessable = 3.
- Quality target: 3/5 - a decided flow carrying one owned motion signature; blocked from 4/5 by Typography (1), which names no type role at all, and by the six dimensions that stop at the same 3 -> 4 boundary until the flow puts values on its decisions - type roles, spacing, contrast pairs, and the curve for `motion.commit`. Production readiness sits at 2 for a reason worth naming rather than leaving implicit: the four recovery paths cover permission, abandonment and validation but not a failed network call at the account or sync step, and no step defines a loading treatment for the first write or the initial sync. Both are gaps, kept here deliberately so the corpus carries a band-2 production read.
- Signature move: `motion.commit` - one 300ms shared-element transition carries the habit name from the entry field into the confirmation card. Replayed at first completion and at each streak milestone, so the same gesture always means "this counted". Reduced-motion fallback: cross-fade, no translation.
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
