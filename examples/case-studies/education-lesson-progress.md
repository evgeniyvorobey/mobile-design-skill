# Synthetic Case Study: Education Lesson Progress

## Prompt

```text
Use the mobile-design-skill.

Design a mobile screen concept for lesson progress in a learning app.

Inputs:
- Platform: cross-platform
- User goal: know what to continue, what is complete, and what needs review
- Audience: adult learners with intermittent sessions
- Constraints: offline mode, motivational but not childish, accessibility-sensitive progress indicators
```

## Weak response

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- Learners have lessons and progress.
- Progress should feel motivating.

Use a progress ring at the top showing percent complete, then cards for lessons with badges and a big Continue button. Completed lessons get checkmarks and locked lessons use a lock icon. Add streaks for motivation and a friendly empty state.

Accessibility considerations: label progress and make buttons tappable.
Next actions: test motivation and polish icons.
```

## Why this is weak

- Reduces learning progress to a percent and decorative rewards.
- Does not distinguish completed, in progress, needs review, locked, downloaded, or sync-pending lessons.
- Streaks may create pressure without being tied to the user's goal.
- Offline behavior is mentioned in the prompt but absent in the response.
- Accessibility for progress indicators is too shallow.

## Strong response

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- Lessons can be started, completed, queued for review, locked, downloaded, or sync-pending.
- The product tracks progress but has not supplied mastery or grading definitions.
- Offline mode should preserve local progress and explain sync status.

## Screen goal
Help learners resume the right lesson and understand progress without turning learning into a noisy reward board.

## Primary user task
Choose the next useful learning action: continue, review, download, or resolve sync.

## Information hierarchy
1. Recommended next lesson or review item
2. Overall module progress with plain-language label
3. Lesson list grouped by status
4. Offline/sync state
5. Optional achievement or streak content

## Recommended layout structure
- Header: course/module name and sync status.
- Next action panel: lesson title, estimated time if known, current status, primary CTA.
- Progress summary: "6 of 10 lessons complete" plus progress bar; percent is secondary.
- Lesson list: rows with title, status, duration, downloaded state, and review-needed marker.
- Offline banner: visible when local progress has not synced.

## Empty / loading / error states
- Loading: show course title if cached and skeleton lesson rows.
- No lessons: explain that content is not assigned or not downloaded, with refresh/contact action.
- Offline: allow downloaded lessons, queue progress locally, show sync-pending state.
- Sync conflict: show last saved local progress and server progress; ask user to choose or provide product-defined merge behavior.

## Alternatives considered
- Rejected: progress-ring-first layout. It is visually simple but does not tell the learner what to do next.
- Rejected: streak as primary motivation. Intermittent learners need continuity, not pressure.

## Platform-specific notes
- iOS: use clear navigation title and native list behavior; avoid hiding download actions behind swipe only.
- Android: system back returns to course list with scroll position preserved; downloadable lessons can use Material list controls.

## Accessibility considerations
- Progress uses text and numeric counts, not only ring fill.
- Lesson status is exposed as text: complete, in progress, review needed, locked, downloaded, sync pending.
- Large text should stack metadata under lesson titles without truncating titles.
- Motion for progress updates should respect reduced-motion settings.

## Design quality calibration
- Quality target: 4/5 - strong once product definitions for mastery, lock rules, and sync conflict handling are confirmed.
- The screen's craft comes from decision clarity and calm progress semantics, not from badges.

## Next actions
- Confirm status taxonomy, offline write rules, and whether review-needed is algorithmic or instructor-defined.
- QA offline start, offline completion, sync pending, conflict, locked lesson, large text, and screen reader order.
```

## Why this is stronger

- Makes the next learning action more important than decorative completion.
- Adds offline and sync states central to the prompt.
- Uses progress semantics that are accessible without relying on a ring.
- Avoids invented mastery claims.
- Provides platform and QA specifics.

## Regression checks

- Does the concept make next action obvious?
- Does it avoid percent-only progress?
- Does it define offline and sync-pending behavior?
- Does it distinguish complete, in progress, review needed, locked, and downloaded?
- Does it keep motivation supportive rather than pressuring?
