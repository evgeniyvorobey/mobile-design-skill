# Golden Example: Enterprise SaaS

## Prompt

```text
Use the mobile-design-skill.

Create a platform-aware UI spec for a mobile incident triage queue in an enterprise SaaS admin app.

Inputs:
- Platform: Android
- User goal: review urgent incidents and assign the next owner while away from desk
- Audience: operations managers and on-call leads
- Constraints: dense information, repeat use, high consequence mistakes, existing design system, must support large text
```

## Golden output

```md
Mode: Create platform-aware UI spec
Platform scope: Android
Assumptions:
- This is a companion workflow for quick triage, not a replacement for the full desktop console.
- Incident severity, service, age, assignee, and SLA status are available.
- Bulk editing may exist on desktop, but mobile should optimize safe single-incident action.

## Screen scope
Incident queue with filtering, scannable status, and quick assignment for one incident at a time.

## Structural zones
- Top app bar: title, refresh state, optional search.
- Filter row: severity, team/service, assignment, SLA risk.
- Queue list: incident rows optimized for comparison.
- Selected incident preview: bottom sheet or detail screen for assignment and next action.
- Offline or stale-data banner when live status cannot be trusted.

## Row content model
- Severity and SLA risk as text + icon + color, not color alone.
- Incident title or service name as the primary line.
- Age, affected service, current owner, and customer impact as secondary metadata.
- One clearly labeled action entry: Assign, Reassign, or Acknowledge depending on state.

## Behavior rules
- Keep filters sticky while scrolling long queues.
- Preserve the list position after assignment or refresh.
- Confirm destructive or high-impact changes, such as reassigning away from an active owner.
- If incident data is stale, allow reading but block assignment until refreshed or clearly mark the risk.
- Do not hide SLA-risk filters in overflow; this is core triage, not a utility setting.

## Design quality calibration
- Quality target: 3/5 - derived, not claimed: the queue's structure, its risk-over-action weighting and its filtered-empty recovery are decided, and the severity rail is a real owned asset (Attention path 4, Distinctiveness 4). Blocked from 4/5 by Production readiness at 2, which fails its 2 -> 3 question - the spec offers "bottom sheet or detail screen" instead of choosing one, and a queue whose whole point is live data defines neither a loading nor an error state. Choosing the surface and defining those two states is the work; two independent scorings of this block both land it at 3.
- Signature move: `layout.severity-rail` - a 4dp leading rail carrying severity on every incident row. Repeated in the list, the detail header, and the filtered-empty state, so severity is legible from the edge of the screen before any text is read, and never depends on color alone.
- Enterprise quality means dense but organized: alignment, repeatable row rhythm, clear status semantics, and low ornament.
- Use 16dp horizontal padding, 8-12dp row internals, and strong vertical alignment for metadata comparison.
- Use tabular or consistently aligned numerals for age, counts, and SLA time remaining.
- Primary visual weight belongs to severity/SLA plus incident identity; assignment actions are available but not louder than risk.
- Empty and filtered-empty states must help users recover by adjusting filters, not display generic emptiness.

## Android-specific notes
- Respect system back from detail/preview to the same filtered queue state.
- Use Material-style top app bar, chips, list rows, and bottom sheet patterns where the existing system allows.
- Ensure touch targets remain at least 48dp even when rows are visually dense.

## Production checks
- Test with 100+ incidents, large text, stale-data state, permission-denied assignment, dark theme, and TalkBack focus order.
```

## Design-quality notes

- Reward density that supports the stated enterprise task instead of reflexively simplifying the queue.
- Penalize decorative cards, marketing-style empty states, or recommendations that move critical filters behind overflow.
- A strong answer names data freshness, permissions, and mistake prevention as first-class design constraints.
- The `3/5` is derived from the nine bands, not from how finished the block reads. Two independent scorings agreed on it and on the blocker. A reader who thinks this deserves more should re-derive rather than adopt the number — and if they reach 4, the thing that moved is Production readiness answering its own question.
