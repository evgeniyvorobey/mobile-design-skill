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

- High: missing result-submission recovery, primary action mismatch after failure if pass/fail changes the next best task.
- Medium: explanations hidden by default for missed questions, weak objective mapping, accessibility labels for correct/incorrect indicators.
- Low: exact motivational tone, visual balance of score block, and footer spacing should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected current design-quality score: 3/5.
- Reason: the screen has a solid results structure and review path, but recovery, learning guidance, and state handling need more production-ready detail.
