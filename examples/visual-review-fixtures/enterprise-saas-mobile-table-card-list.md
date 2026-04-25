# Visual Review Fixture: Enterprise SaaS Mobile Table/Card List

## Review setup

- Synthetic fixture only. No screenshots, real brands, or copied UI.
- Review evidence type: D2, text description only.
- Platform scope: Cross-platform mobile, operational enterprise SaaS.
- User task: scan a queue, find risky items, and take safe action on selected records.

## Screen description

A mobile enterprise app shows a queue of operational exceptions. The desktop product uses a table, but mobile converts each row into a card. Product wants power-user density and bulk actions without losing record traceability.

## Frame specs

- Frame: 393 x 852 px mobile portrait.
- Header: title "Exceptions", search icon, filter icon.
- Filter chips row: Status, Owner, SLA, Region.
- Card list: 8 cards visible across the first two viewports.
- Each card height: 112 px.
- Bottom bulk-action bar appears after one card is selected.

## Visible hierarchy

1. Queue title and total count.
2. Filter chips.
3. SLA breach card with red status chip.
4. Other exception cards ordered by last updated time.
5. Bottom bulk-action bar after selection.

## Components

- Header with search and filter controls.
- Horizontal filter chips.
- Record cards with ID, customer, status chip, owner initials, SLA time, last updated, and checkbox.
- Inline overflow menu per card.
- Bottom bulk-action bar: Assign, Snooze, Close.
- Pull-to-refresh behavior.

## Typography

- Screen title: 22 px semibold.
- Record ID: 12 px monospace.
- Customer name: 15 px medium.
- Status chip: 11 px uppercase.
- Metadata labels: 11 px regular.
- SLA timer: 13 px semibold.
- Bulk-action labels: 12 px medium.

## Color and state notes

- SLA breach uses red chip and red timer.
- Warning status uses orange chip.
- Normal status uses blue chip.
- Selected card uses light blue background.
- Cards with stale data show a small clock icon, but no text label.
- Offline mode is not described.

## Interaction states

- Default list state described.
- Loading state uses skeleton cards.
- Empty state says "No exceptions".
- Error state says "Could not refresh".
- Selection state shows bottom bulk-action bar.
- Partial permission state is not described.
- Conflict state after another user changes a record is not described.

## Known constraints

- Enterprise users need dense scanning, not marketing-style spacing.
- Records may change while the user is reviewing the queue.
- Some users can view records but cannot close them.
- Bulk actions can affect many records and should prevent irreversible mistakes.
- Mobile may be used in short sessions between desktop workflows.

## Expected critique

- The review should recognize that density is appropriate for operational work, but must be made scannable through stronger ordering and labels.
- The review should flag color-only status semantics: status chips and stale indicators need text/icons beyond hue.
- The review should flag traceability risk: record ID, customer, SLA, owner, and last updated must remain readable and not over-truncated.
- The review should flag bulk-action risk: Close should require confirmation or preview of selected records, especially when permissions differ.
- The review should flag missing conflict and partial-permission states.
- The review should flag weak empty/error copy: "No exceptions" and "Could not refresh" need context, retry, and last-known-data behavior.
- The review should recommend concrete fixes: add a priority sort explanation, expose SLA breach reason, use status labels with icons, add conflict resolution, disable unauthorized bulk actions with reason, show selected-record count and names before destructive actions.
- The review should note strengths: card conversion from desktop table, filters, skeleton loading, and selection bar fit enterprise workflows.

## Prohibited critique

- Do not claim mobile cards are always worse than tables.
- Do not demand sparse consumer-style cards when the task requires dense scanning.
- Do not claim exact readability or contrast failure without visual evidence.
- Do not invent enterprise compliance requirements.
- Do not assume all bulk actions are destructive; only "Close" is potentially final from the fixture.
- Do not claim the queue ordering is wrong without acknowledging the stated last-updated ordering.

## Severity expectations

- High: irreversible or broad bulk action without confirmation, missing conflict state, permission ambiguity.
- Medium: color-only status semantics, traceability/truncation risk, weak error recovery.
- Low: exact card spacing, perceived clutter, and visual balance should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected current design-quality score: 3/5.
- Reason: the core operational structure is workable, but status semantics, conflict handling, and bulk-action safety need stronger production detail.
