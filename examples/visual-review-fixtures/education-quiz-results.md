# Visual Review Fixture: Education Quiz / Results

## Review setup

- Synthetic fixture only. No screenshots, real brands, or copied UI.
- Review evidence type: D2, text description only.
- Platform scope: Cross-platform mobile education app.
- User task: understand quiz performance, learn from mistakes, and choose the next study action.

## Screen description

A quiz results screen appears after a 12-question practice quiz. It shows score, pass/fail status, question list, and recommended next lesson. Product wants the screen to feel motivating but compact.

## Frame specs

- Frame: 390 x 844 px mobile portrait.
- Header: "Quiz complete" with close button.
- Score summary block: 78%, pass/fail label, and time spent.
- Question review list: 12 rows.
- Sticky footer: "Continue" primary CTA and "Retry quiz" secondary text button.

## Visible hierarchy

1. Score percentage.
2. Pass/fail label.
3. Motivational message.
4. Missed question count.
5. Question review list.
6. Recommended lesson card.
7. Continue / Retry actions.

## Components

- Score summary block.
- Pass/fail badge.
- Motivational message.
- Question review rows with correct/incorrect indicators.
- Expandable explanation panels.
- Recommended lesson card.
- Sticky footer actions.

## Typography

- Score percentage: 44 px bold.
- Pass/fail label: 14 px uppercase.
- Motivational message: 16 px regular.
- Question row title: 15 px medium.
- Explanation text: 13 px regular.
- Footer CTA: 16 px semibold.

## Color and state notes

- Correct answers use green check icon.
- Incorrect answers use red x icon.
- Pass/fail status uses color and label.
- Explanations are collapsed by default.
- "Continue" is primary even when the user failed.
- Low-confidence or guessed answers are not represented.

## Interaction states

- Default completed state described.
- Expanding a question reveals the correct answer and explanation.
- Retry starts a new quiz immediately.
- Continue opens the next lesson.
- Loading state after submit is not described.
- Error state if result submission fails is not described.
- Offline state is not described.

## Known constraints

- The screen should support learning, not just scoring.
- Some learners may use screen readers or color filters.
- Failure copy should avoid shame and preserve motivation.
- Educators may need traceability between missed questions and lesson objectives.
- The fixture does not provide psychometric validation or assessment policy.

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform mobile
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- This is a phone-first results screen, 390 x 844 px, after a 12-question practice quiz.
- Correct/incorrect are conveyed by icon plus color (green check, red x), as stated.
- The motivational copy is described in role only; exact wording is unknown.

## Quick summary
The results screen displays performance clearly, but learning recovery is weaker than the score display: explanations are collapsed by default, the primary action is "Continue" even after a failure, missed questions are not grouped or mapped to objectives, and there is no recovery if result submission fails. The structure is solid and the two leading bands project to 4, but the brand voice is named without ever being stated, so the artifact stays at 3/5; visual balance and exact tone cannot be judged from text, and the indicators are not color-only because icons are described.

## Strengths
- Shows a clear score, pass/fail status, and time spent in a prominent summary.
- Provides a per-question review list with expandable explanations and a retry path.
- Recommends a next lesson, giving the learner a forward action.

## Findings

### F1 — No recovery if result submission fails
- Lens: Usability
- Observation: Loading after submit, result-submission error, and offline states are not described.
- Violated principle: Nielsen #1 Visibility of system status; Nielsen #9 Help users recognize, diagnose, and recover from errors.
- User consequence: If submission fails or the learner is offline, results may be lost with no feedback or retry, discarding completed work.
- Change: Add submit loading, an error/offline state with retry, and preserve the learner's submitted answers until the result is confirmed saved.
- Predicted effect: Should reduce lost results on submission failure; confidence M (D2 text-only — structural inference, not measured).
- Severity: 3 (major) — occasional but high impact (lost work), persistent until states exist.
- Moves: Production readiness 2→3; lifts cap: missing submission recovery.

### F2 — Primary action does not adapt to outcome
- Lens: Usability
- Observation: "Continue" is primary even when the learner failed, opening the next lesson regardless of result.
- Violated principle: Nielsen #7 Flexibility and efficiency of use; match between system and the real world (the best next step depends on outcome).
- User consequence: After a failure, advancing to the next lesson may not be the best next step; the screen nudges the learner past unaddressed gaps.
- Change: Adapt the primary action by outcome (e.g. "Review mistakes" or "Retry" on failure), or clearly explain why continuing is recommended.
- Predicted effect: Should better match the next action to the learner's result; confidence M (D2 text-only). Reviewed as a structural mismatch, not a measured learning outcome.
- Severity: 3 (major) — frequent on failures, moderate-to-high impact, persistent.
- Moves: Attention path & hierarchy 2→3; lifts cap: outcome-action mismatch.

### F3 — Explanations collapsed and mistakes not surfaced first
- Lens: Usability
- Observation: Explanations are collapsed by default and missed questions are interleaved in a 12-row list rather than grouped or prioritized.
- Violated principle: Cognitive load (extraneous); recognition over recall.
- User consequence: Learners must hunt for the questions they got wrong and expand each one, raising the effort to learn from mistakes — the core job of the screen.
- Change: Group incorrect answers first, add a "Review mistakes" action, and make each missed question's explanation easy to reach.
- Predicted effect: Should reduce effort to learn from mistakes; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path & hierarchy 2→3.

### F4 — Missed questions not mapped to objectives/lessons
- Lens: Usability
- Observation: There is no described linkage between missed questions and lesson objectives, though educators may need that traceability.
- Violated principle: Match between system and the real world; recognition over recall.
- User consequence: Learners (and educators) cannot tell which concept a mistake maps to or where to study next, weakening the learning loop.
- Change: Map each missed question to its objective and a linked lesson the learner can open.
- Predicted effect: Should improve targeted study after a quiz; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Production readiness 2→3.

### F5 — Accessible labels for correct/incorrect not confirmed
- Lens: Accessibility
- Observation: Correct/incorrect use a green check and red x (icon plus color), but screen-reader text labels for the indicators are not described.
- Violated principle: Name/role/value for assistive technology (status must be programmatically available).
- User consequence: Screen-reader users may not hear whether an answer was correct or incorrect if the icons lack text alternatives.
- Change: Add explicit text labels ("Correct"/"Incorrect") for each indicator for assistive technology; keep icon plus color for sighted users.
- Predicted effect: Should improve screen-reader clarity of results; confidence M (semantics unverifiable from text). Note: the indicators are not color-only, since icons are described — the requirement is accessible labels, not removing color reliance.
- Severity: 2 (minor) — frequent for AT users, moderate impact, persistent.
- Moves: Production readiness 2→3.

### F6 — Possible shame risk in failure copy
- Lens: Design quality
- Observation: A motivational message is present and "Continue" stays primary after failure; failure copy should avoid shame, but exact wording is not provided.
- Violated principle: Match between system and the real world (tone appropriate to a learner who failed); cognitive/emotional load.
- User consequence: If the motivational copy reads as negative after a failure, it can discourage the learner and undermine motivation.
- Change: Ensure failure copy is supportive and outcome-aware; pair it with a constructive next step rather than a generic "Continue."
- Predicted effect: Should reduce discouragement after failure; confidence L (cannot evaluate unseen copy). Does not invent or assert the exact wording.
- Severity: 1 (cosmetic) — occasional, low-to-moderate impact, persistent; keep qualified.
- Moves: Context & brand fit 2→2, Distinctiveness & owned assets 2→2 — the fix asks for supportive, outcome-aware copy but names no convention, no departure and no stated treatment, so neither band moves; the copy itself stays unseen.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {2, 2, 2, 3, 3, 3}; held down by missing submission recovery (F1), an outcome-blind primary action (F2), and a brand voice that is named but never stated.
- Projected: 3/5 — median of the assessable projected bands {2, 2, 3, 3, 4, 4} once F1+F2 land (plus F3/F4/F5); held there by the context and distinctiveness bands no finding states a treatment for.
- Ceiling note: with a visual pass confirming balance and tone the leading bands hold at 4, but the artifact stays at 3/5 until the motivational moment becomes a stated treatment (large-text, color-filter rendering, and screen-reader behavior are still unverified from the description).
- Primary lever(s): F2 (adapting the primary action to outcome turns a scoring screen into a learning screen), with F1 protecting completed work.

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path & hierarchy | 3 | 4 | F2/F3 (rung 3→4) | provisional |
| Production readiness | 2 | 4 | F1/F4/F5 lift recovery/AT caps | provisional |
| Color, state & contrast | 3 | 3 | check/x icons and the pass/fail label are second cues and the roles are decided; 3→4 needs stated pairs, which a description does not carry | provisional |
| Context & brand fit | 2 | 2 | no convention is named and no departure carries a reason; F6 asks for supportive copy without naming either | provisional |
| Typography craft | 3 | 3 | six roles carry stated sizes and weights; 3→4 needs the behaviour named when text scales up, which no finding supplies | provisional |
| Distinctiveness & owned assets | 2 | 2 | the motivational message is a named asset whose treatment is never stated (F6) — an adjective, not a token | provisional |
- Projected overall = median of the assessable projected dimensions {4, 4, 3, 2, 3, 2} = 3. Not the sum of per-dimension gains; colour stops at 3 because a description states no pair, and that rung is never projected upward from text.

## Severity index
- 4 (catastrophe): none
- 3 (major): F1, F2
- 2 (minor): F3, F4, F5
- 1 (cosmetic): F6

## Platform-convention mismatches
- Cross-platform caution: the sticky footer actions and close button should follow each platform's navigation and dismissal conventions.
- Expand/collapse and result announcements should use platform-idiomatic patterns and assistive-technology APIs rather than a single forced style.

## Unresolved assumptions
- Cannot verify whether the 44 px score block is visually overwhelming without a screenshot.
- Cannot verify contrast of the check/x icons or labels from text.
- Cannot evaluate the motivational copy because exact wording is not provided.
- Cannot claim any learning-improvement or assessment-validity outcome.

## Next actions
- Add submission loading/error/offline recovery that preserves submitted answers, and adapt the primary action to outcome.
- Group mistakes first, map missed questions to objectives/lessons, and add accessible labels for correct/incorrect.
- Run a visual pass with large text, a color filter, and a screen reader to confirm the projected score.
```

## Expected critique

- The review should identify that the score is clear, but learning recovery is weaker than performance display.
- The review should flag "Continue" as primary even after failure; the primary action should adapt to outcome or show why continuing is recommended.
- The review should flag collapsed explanations: missed questions need easier access to explanation and lesson linkage.
- The review should flag color-only risk only if the icon/label combination is insufficient for the described indicator; since red x and green check are described, the critique should focus on ensuring labels and screen-reader text, not claiming pure color-only status.
- The review should flag missing result-submission error/offline state.
- The review should flag possible shame risk in copy if the motivational message is negative, but should not invent exact copy.
- The review should recommend concrete fixes: group incorrect answers first, add "Review mistakes" action, map each missed question to objective and lesson, preserve submitted answers on error, add screen-reader labels for correct/incorrect, adapt primary CTA by outcome.
- The review should note strengths: clear score, question review, expandable explanations, retry path, and recommended lesson create a useful baseline.

## Prohibited critique

- Do not claim the assessment is valid or invalid without educational measurement context.
- Do not invent exact motivational copy.
- Do not say the indicators are color-only when icons are explicitly described; instead require accessible labels.
- Do not claim score typography is visually overwhelming without qualifying that no screenshot is provided.
- Do not claim completion or learning improvement metrics.
- Do not infer age group, school policy, or grading consequences.

## Severity expectations

Severity uses the Nielsen 0-4 scale (High maps to 3, or 4 if irreversible/catastrophic; Medium to 2; Low to 1).

- 3 (major): missing result-submission recovery, primary action mismatch after failure if pass/fail changes the next best task.
- 2 (minor): explanations hidden by default for missed questions, weak objective mapping, accessibility labels for correct/incorrect indicators.
- 1 (cosmetic): exact motivational tone, visual balance of score block, and footer spacing should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected score: current 2/5 → projected 3/5 (flat median of the assessable dimensions, conditional, provisional D2).
- Reason for current: the screen has a solid results structure, decided colour and type roles, and a working review path, but recovery, learning guidance, and state handling need more production-ready detail, and the motivational voice is named without being stated.
- Reason for projected: adding submission recovery and an outcome-aware primary action, plus surfacing mistakes and objective mapping, lift attention path and production readiness to 4 — but context and distinctiveness stay at 2 until the motivational moment becomes a stated treatment, and visual balance, tone, and rendering cannot be raised from a text-only description.
- No Bold move is expected: the screen is at 2/5 with an unresolved severity-3 finding (missing result-submission recovery), so the Bold move trigger (competent, with no unresolved severity-3/4 finding) is not met.
