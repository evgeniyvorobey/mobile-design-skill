# Synthetic Case Study: Rationale And Handoff

## Prompt

```text
Use the mobile-design-skill.

Prepare a design rationale and engineering handoff for a weekly fitness summary screen.

Inputs:
- Platform: cross-platform
- User goal: understand weekly activity and choose what to do next
- Audience: casual fitness users
- Constraints: metrics may be incomplete, avoid medical claims, needs implementation-ready states
```

## Weak response

```md
Mode: Prepare design rationale / handoff
Platform scope: Cross-platform
Assumptions:
- Users track weekly activity.
- The screen should motivate progress.

The design uses a clean summary card with weekly stats, a chart, and a CTA to start the next workout. This helps users see progress and stay motivated. Use a friendly tone, colorful visuals, and clear icons. Engineers should build cards, charts, and buttons with loading and error states.

Accessibility and usability considerations: make charts accessible and text readable.
Next actions: build the screen and test with users.
```

## Why this is weak

- Rationale restates the concept instead of explaining decisions and tradeoffs.
- "Motivate progress" can become pressure or misleading health interpretation.
- Missing incomplete-data, no-workout, offline, and chart fallback states.
- Engineering handoff lacks component responsibilities, state rules, and QA checks.
- Validation plan is generic.

## Strong response

```md
Mode: Prepare design rationale / handoff
Platform scope: Cross-platform
Assumptions:
- Activity metrics are wellness/fitness summaries, not medical interpretation.
- Weekly data may be incomplete because of denied permissions, offline sync, or skipped tracking.
- The product has no provided coaching algorithm, so recommendations must stay neutral.

## Design objective
Show the user's weekly activity in a way that is understandable, honest about missing data, and actionable without making health claims.

## Target users and context
Casual users may check the screen once or twice a week. They need quick orientation, not a dense analytics dashboard.

## Key design decisions
- Summary first: one plain-language weekly status plus the top metric.
- Completeness visible: data coverage appears near the summary, not hidden in settings.
- Trend over judgment: charts show change and consistency, not "good/bad" medical interpretation.
- Next action is contextual: start workout, review missing data, connect permissions, or rest if product policy supports it.

## Pattern choices and why
- Use a summary module plus metric list rather than chart-only view because mixed-literacy users need text and numbers together.
- Use a compact bar or line chart with table fallback for weekly values.
- Use inline data-quality banner for incomplete metrics, not a blocking modal.
- Keep primary CTA below the summary so users read status before acting.

## Design quality rationale
- Attention path: weekly status, top metric, data completeness, trend, next action.
- Composition: one summary module followed by repeated metric rows; avoid nested cards for each metric.
- Typography: metric hero for the main value, body text for explanation, labels for units and date range.
- Color/state: semantic status is paired with text; no red/green-only activity judgment.
- Interaction polish: chart points expose exact values on tap and via accessible list.

## Platform alignment
- iOS: preserve navigation hierarchy from dashboard to weekly detail; use native share/export only if implemented.
- Android: system back returns to dashboard with selected week preserved; chart detail bottom sheet should not trap back navigation.

## States and edge cases
- Complete week: show summary, chart, metric rows, and next action.
- Partial week: show coverage percentage or missing-days count if product supplies it.
- No workouts: show first useful action and explain what will appear after tracking.
- Permission denied: explain which metric is unavailable and provide settings recovery.
- Offline/stale: show last synced timestamp and avoid implying current status.
- Loading: skeleton summary and metric rows; no fake placeholder values.
- Error: preserve last known weekly summary with timestamp if safe.

## Implementation notes
- Model metric value, unit, source, freshness, and completeness separately.
- Chart component needs accessible text/table fallback.
- CTA selection should come from state rules, not hardcoded copy.
- Analytics, if used, should distinguish viewing summary from starting a workout; no health outcome claim.

## Open questions
- What metric is the primary weekly value: active minutes, workouts, distance, or product-defined score?
- Which missing-data reasons can be exposed to users?
- Are rest/recovery suggestions allowed by product policy?

## Validation plan or recommended testing focus
- Test whether users can identify the weekly status, data completeness, and next action within one minute.
- QA no data, partial data, stale data, denied permission, chart table fallback, long units, large text, and dark mode.

## Next actions
- Confirm primary metric, data completeness model, and allowed next-action rules.
- Create engineering states for complete, partial, empty, denied, stale, loading, and error.
```

## Why this is stronger

- Quality target: 4/5 - strong once analytics events, backend constraints, and experiment scope are confirmed.
- Turns rationale into decision logic and implementation guidance.
- Avoids medical or coaching overclaim.
- Makes incomplete data visible and state-driven.
- Provides a concrete validation focus.
- Gives engineering model implications rather than only visual suggestions.

## Regression checks

- Does the handoff distinguish value, unit, source, freshness, and completeness?
- Does it avoid health outcome claims?
- Does it include chart alternatives for accessibility?
- Does it define CTA behavior by state?
- Does it include concrete validation criteria?
