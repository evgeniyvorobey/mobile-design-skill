# Synthetic Case Study: Empty And Error State Recovery

## Prompt

```text
Use the mobile-design-skill.

Prepare a design rationale and handoff for empty and error states in a mobile document sync app.

Inputs:
- Platform: cross-platform
- User goal: understand whether documents are missing, syncing, offline, or failed
- Audience: knowledge workers
- Constraints: preserve user work, support offline, avoid panic, useful for engineering handoff
```

## Weak response

```md
Mode: Prepare design rationale / handoff
Platform scope: Cross-platform
Assumptions:
- Users have documents.
- Sync can fail.

Use friendly empty states with illustrations and clear CTAs. For errors, show "Something went wrong" with a retry button. Show a spinner while syncing and a toast when documents are saved. Keep the tone calm and provide support links.

Accessibility and usability considerations: make messages readable and retry buttons accessible.
Next actions: implement error states and test edge cases.
```

## Why this is weak

- Collapses empty, offline, syncing, failed, and partial data into generic states.
- "Something went wrong" does not tell users whether work is safe.
- Toast-only success/failure can be missed and may not be accessible.
- Does not define persistence, conflict, retry, or last-synced behavior.
- Provides weak handoff for engineering.

## Strong response

```md
Mode: Prepare design rationale / handoff
Platform scope: Cross-platform
Assumptions:
- Documents can exist locally, remotely, or both.
- Offline editing is supported for at least some document types.
- Exact sync conflict rules are product-defined and not assumed here.

## Design objective
Make document state legible so users know whether work is safe, missing, still syncing, or needs action.

## Target users and context
Knowledge workers may open the app while commuting, between meetings, or after editing on another device. They need calm status clarity more than decorative reassurance.

## Key design decisions
- Separate true empty from filtered empty, offline empty, and sync failure.
- Keep last-known documents visible when safe instead of replacing the list with a full-screen error.
- Put sync status near the document list and affected document rows.
- Use explicit recovery actions: retry, view local copy, resolve conflict, clear filters, or contact support.

## Pattern choices and why
- Inline banners for partial sync issues: preserves context and avoids panic.
- Row-level status badges for documents affected individually.
- Full-screen empty state only when there are no local or remote documents for the current scope.
- Dedicated conflict resolution screen when two versions require user choice.

## States and edge cases
- First-use empty: explain how to add or import documents.
- Filtered empty: show active filter and "Clear filters".
- Offline with local docs: show local docs, offline banner, and queued changes.
- Offline with no local docs: explain that documents may appear when connected.
- Syncing: show non-blocking progress and last successful sync.
- Partial failure: show unaffected docs normally and flag failed rows.
- Conflict: show both versions, timestamps, device/source if available, and safe choice.
- Delete failure: keep document visible and explain it was not deleted.

## Implementation notes
- Sync state should be modelled separately from document existence.
- Toasts can supplement but must not be the only carrier of save or failure status.
- Preserve edits locally before network submit when supported.
- Expose status strings for assistive technologies.

## Accessibility and usability considerations
- Status labels must be text, not spinner-only or color-only.
- Screen reader users need updates for sync started, sync failed, and conflict available.
- Retry buttons must identify scope: retry all, retry document, or retry upload.
- Large text should not hide file name, state, and timestamp.

## Validation plan or recommended testing focus
- Test offline with local docs, offline with no local docs, partial sync failure, conflict, failed delete, and filtered empty.
- Acceptance criterion: user can correctly answer "is my work safe?" from each state without support copy.

## Open questions
- What conflict resolution policy is approved?
- Which document types support offline editing?
- How long can a queued local change remain before requiring user action?

## Next actions
- Align product and engineering on the sync state model.
- QA every state with network throttling, airplane mode, large text, and screen reader announcements.
```

## Why this is stronger

- Quality target: 4/5 - strong once source priority, retry behavior, and offline storage rules are confirmed.
- Builds a state taxonomy instead of one generic empty/error template.
- Keeps user trust focused on whether work is safe.
- Gives implementation constraints around sync state and local persistence.
- Defines validation that can be tested.
- Avoids unsupported claims about conflict behavior.

## Regression checks

- Does the rationale distinguish true empty, filtered empty, offline, partial failure, and conflict?
- Does it preserve user work as the primary trust concern?
- Does it avoid toast-only failure handling?
- Does it provide row-level and global recovery actions?
- Does it include engineering-facing state model implications?
