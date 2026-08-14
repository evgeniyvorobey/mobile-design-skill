# Visual Review Fixture: iPad Team Inbox Stretched Phone

## Review setup

- Synthetic fixture only. No screenshots, real brands, or copied UI.
- Review evidence type: D2, text description only.
- Platform scope: iPadOS, tablet device class (regular width primary, compact width reachable at runtime).
- User task: triage a shared team inbox — scan threads, open one, reply or assign it, and move on.

## Screen description

A team inbox app ships one layout for iPhone and iPad. On a 12.9-inch iPad in landscape the iPhone layout is rendered unchanged and centred. The product team believes the app "supports iPad" because it runs, rotates, and does not crash in Split View.

## Frame specs

- Frame: 1366 x 1024 pt, iPad landscape.
- Content column: 390 pt wide, horizontally centred, with 488 pt of empty background on each side.
- Bottom tab bar: spans the full 1366 pt; five tabs (Inbox, Assigned, Mentions, Search, Settings) centred as a group in the middle of the bar; bar height 83 pt.
- Thread row height: 84 pt, 8 rows visible in the first viewport.
- Thread detail: pushed full-screen over the whole 1366 pt width.
- Compose: full-screen modal over the whole 1366 pt width, with a single 1366 pt-wide text area.
- Reply field in the thread detail: 1366 pt wide, 44 pt tall.

## Visible hierarchy

1. "Inbox" title, 34 pt bold, at the top of the 390 pt column.
2. Filter chips: Unread, Assigned to me, Urgent.
3. Thread rows ordered by most recent message.
4. Bottom tab bar.
5. A 56 pt floating compose button, bottom right of the 390 pt column.

## Components

- Header with title and a search icon.
- Horizontal filter chips.
- Thread row: 40 pt avatar, sender names, subject (1 line), message preview (1 line), timestamp, unread dot.
- Thread detail: message list, quoted-text collapse control, reply field, "Assign" button in the top-right nav bar.
- Long-press on a thread row opens a context menu: Assign, Snooze, Archive, Delete.
- Pull-to-refresh on the thread list.
- Compose modal with To, Subject, and body fields.

## Typography

- Screen title: 34 pt bold.
- Thread subject: 15 pt semibold.
- Sender names: 15 pt regular.
- Message preview: 13 pt regular, one line, truncated.
- Timestamp: 11 pt regular.
- Message body in the thread detail: 15 pt regular, line length unbounded across the full 1366 pt width.
- Tab labels: 10 pt.

## Color and state notes

- Unread threads are marked by a blue dot and by a slightly darker row background; the subject is not weighted differently.
- "Urgent" threads show a red timestamp.
- Assigned threads show the assignee's avatar tinted green.
- The selected tab is tinted blue; unselected tabs are grey.
- Dark mode is supported.
- Increased-contrast behaviour is not described.

## Interaction states

- Default list state described.
- Loading uses a spinner centred in the 390 pt column.
- Empty state shows an illustration and "You're all caught up".
- Error state shows "Couldn't refresh" with a Retry button.
- Sending failure in compose is not described.
- Split View: the same 390 pt column is used, now filling the narrower window.
- Stage Manager and external display behaviour are not described.
- Hardware keyboard support is not described; many users have a keyboard case.
- No drag-and-drop is described.

## Known constraints

- One codebase ships to iPhone and iPad; the team does not want two designs.
- Threads arrive continuously; the list changes while the user reads.
- Some users may view a thread but not assign it.
- The team ships to iPad because customers asked for it, and considers the current state "supported".
- Deleting a thread removes it for the whole team.

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: iPadOS
Device class: Tablet — regular width, and compact width whenever Split View or Slide Over narrows the window
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- The 390 pt column and the 1366 x 1024 pt frame are as described; I have not seen the screen.
- "Supports iPad" is a product claim about running, not about a regular-width layout.
- Deleting affects the whole team, so it is treated as irreversible and shared.

## Quick summary
The app runs on iPad but has no regular-width layout: the phone screen is centred in 1366 pt, roughly two-thirds of the window is empty background, and the one place the width *is* used — the thread body — uses it to make lines nobody can comfortably read. Bottom tabs at expanded width put primary navigation as far from the eye as the layout allows. Underneath that, the row content model and the state coverage are reasonable and mostly survive the fix. The width-blindness is the whole finding set; almost everything else follows from it.

## Strengths
- The thread row carries the fields triage actually needs — sender, subject, preview, timestamp, unread — and the row height leaves room for them at larger text.
- Loading, empty, and error states all exist and the error state offers a retry.
- Filter chips (Unread, Assigned to me, Urgent) match the triage task rather than mirroring a desktop menu.

## Findings

### F1 — No regular-width layout: the phone screen is centred in 1366 pt
- Lens: Hierarchy & readability
- Observation: A 390 pt column sits centred with 488 pt of empty background on each side; the thread list and the thread detail are two full-screen states rather than two panes.
- Violated principle: Jakob's Law and platform convention (HIG split views; the canonical list-detail layout); Gestalt common region — the window's regions carry no content.
- User consequence: Every thread costs a push and a back, the user loses the list while reading, and the comparison the triage task depends on is impossible — on a screen with room for both.
- Change: Adopt list-detail at regular width — list pane 320–400 pt, detail pane taking the rest — and keep the current single-pane layout for compact width, with the selection surviving the collapse in both directions.
- Predicted effect: Should remove one navigation round-trip per thread and keep the queue visible while reading; confidence M (structural inference from the description, not measured).
- Severity: 3 (major) — frequent (every thread), high impact on the core task, persistent.
- Moves: Composition and spacing 1→3; Attention path and hierarchy 2→3.

### F2 — Bottom tab bar at expanded width
- Lens: Navigation & interaction
- Observation: Five tabs sit in a bar spanning 1366 pt, centred as a group, 10 pt labels, at the bottom edge of a 1024 pt-tall window.
- Violated principle: Fitts's Law; platform convention for regular width (sidebar or navigation rail, not a bottom bar).
- User consequence: Primary navigation sits at the far edge from where the user is reading, the tab targets are small relative to the window, and the horizontal space the bar occupies does nothing.
- Change: Navigation rail (80 dp, leading edge) at medium width and a permanently visible sidebar (240–360 pt) at expanded width, carrying the same five destinations; keep the bottom bar at compact width.
- Predicted effect: Should shorten the travel to a destination and free the bottom edge; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path and hierarchy 2→3.

### F3 — Message body has no reading measure at 1366 pt
- Lens: Hierarchy & readability
- Observation: The thread detail sets 15 pt body text across the full 1366 pt width with line length unbounded; the compose body is a single 1366 pt-wide field.
- Violated principle: the 45–75 character reading measure; the rule that extra width becomes columns or margins, never longer lines.
- User consequence: Lines run far past the measure, so the eye loses the line return and long threads become hard to read exactly where the app is asking for attention.
- Change: Cap the body column at 640–720 pt and give the remaining width to margins; the same cap applies to the compose body.
- Predicted effect: Should improve sustained reading in long threads; confidence M (cannot confirm rendered line counts from text).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Typography craft 2→3.

### F4 — The detail pane's states are undefined once the layout is two-pane
- Lens: Usability
- Observation: The description defines list states (loading, empty, error) but the detail is only ever a pushed screen, so there is no state for "nothing selected", and back behaviour is defined only for the pushed case.
- Violated principle: state coverage; Nielsen #1 visibility of system status.
- User consequence: After F1 lands, the user meets a blank half-window at launch and back becomes ambiguous — in a two-pane layout there is no screen to pop.
- Change: Define the detail pane's empty state (the mailbox name, its unread count, and a compose action) and define back in both states: at compact, back returns to the list; at expanded, back is not a navigation action.
- Predicted effect: Should remove the blank-pane launch state and keep back predictable across a resize; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent at launch, moderate impact, persistent.
- Moves: Production readiness 2→3.

### F5 — Unread and assignment ride on colour
- Lens: Accessibility
- Observation: Unread is a blue dot plus a slightly darker row; the subject is not weighted. Urgent is a red timestamp. Assigned is a green-tinted avatar.
- Violated principle: WCAG 1.4.1 use of colour — colour must not be the only means of conveying information.
- User consequence: Users with colour-vision differences, or reading in glare, can miss which threads are unread, urgent, or already taken, and duplicate someone else's work.
- Change: Weight the subject for unread, give Urgent a text or icon label beside the timestamp, and label the assignee rather than tinting the avatar. Row background alone is not a second cue.
- Predicted effect: Should reduce misreads of triage state; confidence M (cannot verify rendered contrast from text).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Color, state, and contrast 1→3.

### F6 — Multitasking and keyboard behaviour unstated
- Lens: Usability
- Observation: Split View reuses the same column; Stage Manager, external display, and hardware-keyboard behaviour are not described, and many users have a keyboard case.
- Violated principle: platform convention — a tablet layout is never guaranteed the full screen, and resize must not lose state.
- User consequence: A resize mid-triage may lose scroll position, selection, or an in-progress reply, and keyboard users have no stated way to move the selection or send.
- Change: State that selection, scroll position, and in-progress compose text survive every width change; add `↑ ↓` selection, `Return` to open, and a send shortcut with visible focus.
- Predicted effect: Should prevent state loss on resize and speed up keyboard triage; confidence L (behaviour is unstated rather than described as broken).
- Severity: 1 (cosmetic) — occasional, moderate impact, currently unverifiable.
- Moves: Production readiness 2→3.

### F7 — Team-wide Delete sits in a long-press menu with no confirmation
- Lens: Usability
- Observation: Long-press offers Assign, Snooze, Archive, Delete; deletion removes the thread for the whole team and no confirmation or undo is described.
- Violated principle: Nielsen #5 error prevention; Nielsen #3 user control and freedom.
- User consequence: One mis-press destroys a thread for every teammate with no stated recovery.
- Change: Separate Delete from the frequent actions, confirm it with the scope stated ("Deletes for everyone"), and offer an undo window.
- Predicted effect: Should reduce irreversible shared deletions; confidence M (D2 text-only).
- Severity: 3 (major) — occasional, irreversible and shared, persistent until guarded.
- Moves: Production readiness 2→3.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {1, 1, 2, 2, 2, 2, 3}; the layout is contradicted by its own width and colour carries meaning alone.
- Projected: 3/5 — median of the assessable projected bands {3, 3, 3, 3, 3, 3, 3} once F1–F5 and F7 land. The fixes decide the default case at each width; they do not state the values (spacing, pairs, intervals, durations) the 3→4 boundary asks for, and a text-only review cannot supply them.
- Ceiling note: with a visual pass and stated values, the leading bands could reach 4; nothing here supports projecting a visual dimension upward from a description.
- Primary lever(s): F1 — the width-blind layout is the parent of F2, F3, and F4, and fixing it is what makes the rest worth doing.

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path and hierarchy | 2 | 3 | F1/F2 decide what leads at regular width | provisional |
| Composition and spacing | 1 | 3 | F1 — the window's regions currently carry nothing; values still unstated | provisional |
| Typography craft | 2 | 3 | F3 caps the measure; role values still unstated | provisional |
| Color, state, and contrast | 1 | 3 | F5 adds the second cue; pairs and dark values unstated | provisional |
| Density and rhythm | 3 | 3 | the 84 pt row is a stated repeat unit; the crowded end is undescribed | provisional |
| Interaction polish and motion | 2 | 3 | states exist per screen, not per action; no durations described | provisional |
| Production readiness | 2 | 3 | F4/F6/F7 close state, resize, and destructive-action gaps | provisional |
| Distinctiveness and owned assets | 1 | 1 | inert — a generic inbox once the logo is removed, and no finding adds an owned asset | provisional |
| Context and brand fit | n/v | n/v | no brand or domain conventions stated in the fixture | — |
- Projected overall = median of the assessable projected dimensions {3, 3, 3, 3, 3, 3, 3, 1} = 3 (even count, lower middle).

## Severity index
- 3 (major): F1, F7
- 2 (minor): F2, F3, F4, F5
- 1 (cosmetic): F6

## Platform-convention mismatches
- Bottom tab bar at expanded width where iPadOS convention is a sidebar or rail.
- A full-screen push where the platform's canonical layout for a collection-and-item task is a split view.
- Compose as a full-window modal at 1366 pt where a sheet or a pane-scoped composer fits the platform better.
- Split View treated as an afterthought rather than as a width the app is handed at runtime.

## Unresolved assumptions
- Cannot verify rendered contrast for the blue dot, red timestamp, or green avatar tint from text.
- Cannot verify what the layout does at 200 % font scale, since scaling behaviour is not described.
- Cannot verify whether state survives a resize, because resize behaviour is unstated rather than described.
- Cannot judge visual balance or the perceived emptiness of the side margins without a screenshot.

## Next actions
- Introduce list-detail at regular width with the compact layout kept as a first-class state, then move navigation to a rail and sidebar.
- Cap the reading measure, define the detail pane's empty state and back behaviour in both states, and add the second cue to unread, urgent, and assigned.
- Guard the team-wide Delete with a scoped confirmation and an undo window.
```

## Expected critique

- The review should identify that the screen has no regular-width layout at all, and name list-detail as the canonical layout rather than describing a bespoke one.
- The review should flag the bottom tab bar at expanded width and name the navigation rail and sidebar as the width-appropriate replacements.
- The review should flag the unbounded reading measure in the thread body and compose field, and give a numeric cap.
- The review should note that a two-pane layout needs the detail pane's own empty state and a back rule for both the two-pane and the collapsed state.
- The review should flag colour-only unread, urgent, and assignment cues.
- The review should flag the team-wide Delete as irreversible and shared, and require a scoped confirmation or undo.
- The review should treat Split View and Slide Over as widths the app is handed at runtime, and require state to survive resize.
- The review should note real strengths: the row content model, the triage-shaped filters, and the existing loading/empty/error states.
- The review should keep the compact-width layout: the current single column is correct at compact width and only wrong as the *only* layout.

## Prohibited critique

- Do not claim a centred single column is always wrong; with a locked measure and the surrounding width doing work, it is a legitimate reading layout.
- Do not demand a third pane or an inspector; the window is 1366 pt and the task does not need simultaneous secondary controls.
- Do not claim exact contrast, balance, or perceived emptiness from a text description.
- Do not claim the app fails accessibility compliance; name the risk and its standard instead.
- Do not invent engagement, retention, or triage-speed numbers for the proposed fix.
- Do not demand drag-and-drop as a defect; it is an accelerator, and its absence is not a failure.
- Do not treat "supports Split View" as evidence that the adaptive behaviour is designed.

## Severity expectations

Severity uses the Nielsen 0-4 scale (High maps to 3, or 4 if irreversible/catastrophic; Medium to 2; Low to 1).

- 3 (major): no regular-width layout, because it costs a round-trip on every thread in the core task; team-wide Delete without confirmation, because it is irreversible and shared.
- 2 (minor): bottom tabs at expanded width, unbounded measure, undefined detail-pane state, colour-only status cues.
- 1 (cosmetic): unstated multitasking and keyboard behaviour, which is missing information rather than an observed defect.
- Not a finding: the compact-width layout itself, the row content model, and the presence of the existing states.

## Rubric score expectation

- Expected score: current 2/5 → projected 3/5 (flat median of the assessable dimensions, conditional, provisional D2).
- Reason for current: the layout is contradicted by the width it runs at and colour carries meaning alone, so composition and colour sit at 1 and the median lands at 2.
- Reason for projected: adopting list-detail, moving navigation by width, capping the measure, adding second cues, and guarding the destructive action decide the default case at each width — but none of them state the spacing, pairs, intervals, or durations the 3→4 boundary asks for, and distinctiveness stays inert because no finding adds an owned asset.
- No Bold move is expected: the screen is at 2/5 with an unresolved severity-3 finding, so the Bold move trigger is not met.
