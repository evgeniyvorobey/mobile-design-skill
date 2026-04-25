# Synthetic Case Study: SaaS Approval Queue

## Prompt

```text
Use the mobile-design-skill.

Design a mobile user flow for an enterprise SaaS approval queue.

Inputs:
- Platform: cross-platform
- User goal: review and approve or reject access requests while away from desktop
- Audience: managers and admins
- Constraints: role permissions, auditability, high volume, mistake prevention, useful on phone
```

## Weak response

```md
Mode: Design mobile user flow
Platform scope: Cross-platform
Assumptions:
- Users have requests to approve.
- Managers need a simple queue.

The app opens to a list of approval cards. Each card has requester name, request type, approve, and reject buttons. Users can filter by pending or approved. Add a bulk approve button for speed. Confirmation toast appears after action.

Accessibility and usability risks: make buttons large and text readable.
Next actions: test with admins and refine filters.
```

## Why this is weak

- Optimizes speed before risk and auditability.
- Bulk approval is introduced without permission, risk, or review constraints.
- Request details are too thin for accountable decisions.
- Back navigation, undo/confirmation, offline, and stale data are missing.
- Accessibility does not address dense lists, focus order, or destructive choices.

## Strong response

```md
Mode: Design mobile user flow
Platform scope: Cross-platform
Assumptions:
- The mobile app is for time-sensitive approvals, not full admin configuration.
- Some requests may require elevated permission or desktop-only review.
- Audit records are required for approve/reject decisions.

## Flow goal
Let managers clear safe, well-understood approvals on mobile while preventing high-risk or under-informed actions.

## Entry points
- Push notification for a high-priority request
- Queue tab from the enterprise app
- Deep link from email or chat

## Ordered steps/screens
1. Queue summary: pending count, stale-data timestamp, filters for priority, requester, system, and age.
2. Request list: compact rows with requester, system, requested role, age, risk signal, and due state.
3. Request detail: full reason, requested scope, requester history, owner, policy notes, and related access.
4. Decision screen: approve/reject with optional required comment and visible audit consequence.
5. Result state: action recorded, request removed or moved to completed, next request offered.

## Decision points
- If request risk is high, require detail view before approving.
- If role permission is insufficient, show why and provide escalation route.
- If request data is stale, require refresh before decision.
- If batch action is available, restrict to homogeneous low-risk requests and show count plus shared criteria.

## Back-navigation logic
- Back from detail returns to queue with filters and scroll position preserved.
- Back from decision returns to detail with comment preserved.
- Back after success returns to the updated queue, not the stale notification origin.

## Failure and recovery paths
- Offline: queue can show cached read-only requests; decisions are disabled unless the product supports queued approvals.
- Network failure after submit: show pending confirmation state and prevent duplicate action.
- Permission denied: explain current role and route to desktop or admin contact.
- Conflict: if another approver acted first, show final state and audit trail.

## Platform behavior notes
- iOS: avoid putting approve/reject only in swipe actions; provide visible buttons on detail.
- Android: system back must not discard comments silently; predictive back should preview return to detail or queue.

## Accessibility and usability risks
- Dense rows need clear heading order: requester, system, role, risk, due time.
- Approve and reject must be visually and semantically distinct.
- Risk color must be paired with text and icon.
- Batch selection needs count announcements and clear deselection.

## Simplification opportunities
- Default queue can show only "needs your action"; completed and delegated items stay behind filters.
- Use progressive disclosure: row summary first, full policy details only in detail.

## Next actions
- Confirm risk taxonomy, permissions, and which requests are mobile-approvable.
- QA stale data, permission denied, concurrent approval, batch selection, and screen reader flow.
```

## Why this is stronger

- Quality target: 4/5 - strong once approval policy, permission roles, and audit requirements are confirmed.
- Makes mobile approval intentionally narrower than desktop admin work.
- Adds risk gates, stale-data checks, and audit consequences.
- Defines back behavior and conflict recovery.
- Treats density as useful for trained users while protecting decisions.
- Gives concrete rules for batch actions instead of a generic speed feature.

## Regression checks

- Does the flow prevent approval from stale or insufficient data?
- Does it explain audit consequences before final action?
- Does it preserve filters, scroll, and comments across back navigation?
- Does it restrict batch actions with explicit criteria?
- Does it avoid gesture-only approve/reject controls?
