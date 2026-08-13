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

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform mobile
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- This is a phone-first operational queue, 393 x 852 px, used in short sessions between desktop work.
- Density is intended and appropriate; the goal is scannability, not consumer-style spacing.
- "Close" is the only potentially irreversible bulk action described.

## Quick summary
The card-from-table conversion is a reasonable operational pattern and the density fits power-user work, but safety and traceability need stronger production detail: bulk "Close" can act on many records (and across mixed permissions) without confirmation, conflict and partial-permission states are undefined, status meaning rides on color alone, and empty/error copy is thin. The structure is workable and the leading bands project to 4, but the queue carries no owned asset, so the artifact stays at 3/5 after the fixes, and visual readability cannot be judged from text.

## Strengths
- Converts the desktop table into mobile cards without abandoning record traceability.
- Provides filters (Status, Owner, SLA, Region), skeleton loading, and a selection-driven bulk-action bar that fit enterprise workflows.
- Leads the list with the SLA-breach card, surfacing the riskiest item first.

## Findings

### F1 — Bulk "Close" can act irreversibly without confirmation
- Lens: Usability
- Observation: The bulk-action bar offers Close with no described confirmation or preview, and some users can view but not close records (mixed permissions).
- Violated principle: Nielsen #5 Error prevention; Nielsen #3 User control and freedom.
- User consequence: A user can close many records in one tap — possibly including records they should not act on — with no chance to review, an irreversible operational mistake.
- Change: Require a confirmation that previews the selected count and record names before Close; exclude or clearly flag records the user lacks permission to close.
- Predicted effect: Should reduce accidental and unauthorized bulk closures; confidence M (D2 text-only — structural inference, not measured).
- Severity: 4 (catastrophe) — occasional but irreversible and broad (many records at once), persistent until guarded.
- Moves: Production readiness 2→4; lifts cap: irreversible bulk action without confirmation.

### F2 — Missing conflict state for concurrent edits
- Lens: Usability
- Observation: Records may change while the user reviews the queue, but no conflict state is defined for when another user changes a record mid-session.
- Violated principle: Nielsen #1 Visibility of system status; Nielsen #5 Error prevention.
- User consequence: A user may act on a stale record and overwrite or duplicate another operator's change, corrupting the queue.
- Change: Add a conflict state that detects server-side changes and offers refresh/merge before the action is applied.
- Predicted effect: Should reduce stale-record actions and overwrites; confidence M (D2 text-only).
- Severity: 3 (major) — occasional but high impact, persistent until handled.
- Moves: Production readiness 2→3; lifts cap: missing conflict handling.

### F3 — Partial-permission state undefined
- Lens: Usability
- Observation: Some users can view but not close records, but no partial-permission state is described for actions they cannot perform.
- Violated principle: Nielsen #5 Error prevention; Nielsen #1 Visibility of system status.
- User consequence: Users may attempt actions they are not allowed to take and hit opaque failures, or worse, act on records inconsistently.
- Change: Disable unauthorized actions with a visible reason and reflect permission scope in the selection/bulk bar.
- Predicted effect: Should reduce unauthorized-action attempts and opaque failures; confidence M (D2 text-only).
- Severity: 3 (major) — frequent for limited-permission roles, moderate-to-high impact, persistent.
- Moves: Production readiness 2→3; lifts cap: permission ambiguity.

### F4 — Status meaning carried by color alone
- Lens: Accessibility
- Observation: SLA breach is red, warning is orange, normal is blue, and stale-data cards show a clock icon with no text label.
- Violated principle: WCAG use-of-color (1.4.1) — color must not be the only means of conveying information.
- User consequence: Users with color-vision differences or in glare may misread record status or miss that data is stale, leading to wrong prioritization.
- Change: Add a text label (and/or icon) to each status chip and a text label to the stale indicator; do not rely on hue alone.
- Predicted effect: Should reduce status misreads under color-vision or glare conditions; confidence M (cannot verify rendering from text).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Production readiness 2→3.

### F5 — Traceability at risk from over-truncation
- Lens: Hierarchy & readability
- Observation: Cards carry ID (12 px monospace), customer, status, owner, SLA, and last-updated in a 112 px card; metadata labels are 11 px and the queue is dense.
- Violated principle: Cognitive load (extraneous); legibility under density and text scaling.
- User consequence: If identifying fields truncate or shrink too far, operators lose the ability to trace and trust which record they are acting on.
- Change: Protect the identifying fields (ID, customer, SLA, owner, last-updated) from truncation, allow controlled wrapping, and verify at large text — without abandoning intended density.
- Predicted effect: Should preserve record traceability while keeping density; confidence L (exact readability not verifiable from text).
- Severity: 2 (minor) — frequent, moderate impact, persistent; keep qualified (no screenshot).
- Moves: Density & rhythm 3→4 — the fix supplies the crowded-end rule the repeat unit and 112 px interval currently lack; whether it actually reads at that interval still needs a screenshot.

### F6 — Weak empty and error copy
- Lens: Usability
- Observation: Empty state is "No exceptions" and the error is "Could not refresh," with no context, retry, or last-known-data behavior.
- Violated principle: Nielsen #9 Help users recognize, diagnose, and recover from errors; Nielsen #1 Visibility of system status.
- User consequence: Operators cannot tell whether the queue is genuinely clear or failed to load, and a refresh failure offers no recovery or fallback to last-known data.
- Change: Give empty/error states context and a retry, and preserve last-known records with a staleness note when refresh fails; define offline behavior.
- Predicted effect: Should improve recovery and trust during refresh failures; confidence M (D2 text-only).
- Severity: 2 (minor) — occasional, moderate impact, persistent until defined.
- Moves: Interaction polish & motion 2→3.

### F7 — Priority ordering is unexplained
- Lens: Hierarchy & readability
- Observation: The SLA-breach card leads, but the rest is ordered by last-updated time with no explanation of the priority logic.
- Violated principle: Nielsen #1 Visibility of system status; recognition over recall.
- User consequence: Operators may not understand why items are ordered as they are and could miss high-risk items further down.
- Change: Make the sort explicit (and ideally selectable), and expose the SLA-breach reason on the card.
- Predicted effect: Should improve trust in ordering and risk-spotting; confidence M (D2 text-only).
- Severity: 1 (cosmetic) — frequent, low-to-moderate impact, persistent.
- Moves: Attention path & hierarchy 2→3.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {1, 1, 2, 2, 3, 3}; pinned by an unguarded irreversible bulk action (F1) and missing conflict/permission states (F2, F3).
- Projected: 3/5 — median of the assessable projected bands {1, 3, 3, 4, 4, 4} once F1+F2+F3 land (plus F4/F5/F6); held there by the inert Distinctiveness band no finding lifts.
- Ceiling note: with a visual pass confirming readability at the intended density the leading bands hold at 4, but the inert-screen cap holds the artifact at 3/5 until the queue carries one owned asset (large-text legibility at density, offline, and color-vision rendering are still unverified from the description).
- Primary lever(s): F1 (guarding the irreversible bulk Close is the single change that most unblocks the score).

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Production readiness | 2 | 4 | F1/F2/F3 lift safety caps | provisional |
| Attention path & hierarchy | 3 | 4 | F7 ordering (rung 3→4) | provisional |
| Interaction polish & motion | 2 | 3 | F6 states (rung 2→3) | provisional |
| Color, state & contrast | 1 | 3 | status rides on hue alone, so the second-cue test fails (F4); 3→4 needs stated pairs and their dark-theme values | provisional |
| Density & rhythm | 3 | 4 | repeat unit and 112 px interval are already stated; F5 supplies the crowded-end rule (rung 3→4) | provisional |
| Distinctiveness & owned assets | 1 | 1 | inert — a generic card queue once the logo is removed, and no finding adds an owned asset | provisional |
- Projected overall = median of the assessable projected dimensions {4, 4, 3, 3, 4, 1} = 3 (even count, lower middle). Not the sum of per-dimension gains; colour stops at 3 because a description cannot state a pair, and whether the 112 px interval actually reads is still a screenshot question.

## Severity index
- 4 (catastrophe): F1
- 3 (major): F2, F3
- 2 (minor): F4, F5, F6
- 1 (cosmetic): F7

## Platform-convention mismatches
- Cross-platform caution: the bottom bulk-action bar, pull-to-refresh, and overflow menus should follow each platform's idioms rather than a single forced pattern.
- Destructive confirmation should respect platform conventions for irreversible actions (dialog vs. action sheet) rather than acting like a web table.

## Unresolved assumptions
- Cannot verify readability, contrast, or perceived clutter at the intended density from text.
- Cannot verify tap-target sizes for checkboxes, chips, or overflow menus.
- Cannot verify offline behavior because it is not described.
- Cannot verify whether truncation actually hides identifying fields without a screenshot.

## Next actions
- Guard bulk "Close" with a count-and-names confirmation and permission-aware action availability before any visual polish.
- Define conflict and partial-permission states, add non-color status labels, and strengthen empty/error/offline copy.
- Run a visual pass at the intended density with large text and color-vision simulation to confirm the projected score.
```

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

Severity uses the Nielsen 0-4 scale (High maps to 3, or 4 if irreversible/catastrophic; Medium to 2; Low to 1).

- 4 (catastrophe): irreversible or broad bulk action (Close) without confirmation, because it can affect many records at once and cannot be undone.
- 3 (major): missing conflict state, permission ambiguity.
- 2 (minor): color-only status semantics, traceability/truncation risk, weak error recovery.
- 1 (cosmetic): exact card spacing, perceived clutter, and visual balance should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected score: current 2/5 → projected 3/5 (flat median of the assessable dimensions, conditional, provisional D2).
- Reason for current: the core operational structure is workable and density is already decided, but colour-only status, conflict handling, and bulk-action safety pull the median to 2.
- Reason for projected: guarding the irreversible bulk Close, adding conflict/permission states, and supplying the crowded-end rule lift production readiness, attention path and density to 4 — but the screen owns no asset, so the inert-screen cap holds the artifact at 3/5, and readability at the intended density still cannot be raised from a text-only description.
- No Bold move is expected: the screen is at 2/5 with an unresolved severity-4 finding (unguarded bulk Close), so the Bold move trigger (competent, with no unresolved severity-3/4 finding) is not met.
