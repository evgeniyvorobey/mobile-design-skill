# SaaS Mobile Domain Pack

Use this pack for enterprise, B2B, admin, workflow, operations, analytics, support, field-service, incident, CRM, HR, finance-ops, or internal productivity mobile experiences.

This pack provides recommendations, not proof of business value, compliance, security, or organizational fit. Confirm workflow and permission requirements with product, operations, security, and customer-facing teams.

## When To Use

- Dense mobile tools that support work, approvals, monitoring, triage, collaboration, or task completion.
- Companion mobile apps for desktop SaaS products.
- Operational dashboards, queues, alerts, field workflows, support consoles, and admin actions.
- Any workflow where permissions, audit trail, data freshness, or irreversible changes matter.

## Primary User Jobs

- Triage what changed, what is urgent, and what requires action.
- Complete a narrow job quickly away from the desk.
- Approve, reject, assign, comment, escalate, or pause work with confidence.
- Inspect records with enough context to avoid opening a desktop app.
- Recover from offline, stale data, permission mismatch, or conflicting updates.
- Understand what the system did, who changed it, and what happens next.

## Trust And Safety Risks

- Dense screens that hide severity, owner, deadline, or blocked state.
- Stale dashboards presented as live operational truth.
- Permissions that expose restricted records or allow accidental admin changes.
- Bulk actions without preview, undo, or audit visibility.
- Notification pressure that trains users to ignore critical alerts.
- Mobile parity assumptions that overload small screens with desktop complexity.
- Ambiguous object identity in lists with similar accounts, tickets, projects, or people.

## Common Mobile Surfaces

- Work queue/inbox with priority, status, owner, SLA, and filters.
- Record detail with summary, timeline, metadata, attachments, comments, and actions.
- Approval/review screen with decision context, policy hints, impact, and audit note.
- Dashboard with top signals, drill-down, freshness, and thresholds.
- Incident/on-call surface with severity, affected users, timeline, runbook, and escalation.
- Search/filter surface with saved views, chips, scope, and recent records.
- Settings/admin companion with role, workspace, team, notifications, and security controls.

## Hierarchy Guidance

- Lead with the user's next work decision, not a generic dashboard.
- Make object identity unmistakable: name, account/workspace, status, and key metadata.
- Show severity, deadline, owner, and blocker above secondary analytics.
- Use progressive disclosure for dense fields; mobile should reveal context in layers.
- Keep primary actions stable and visible; avoid burying approve/reject/escalate behind menus.
- Separate read-only insight from action-taking surfaces.
- Preserve audit clarity: who did what, when, and from which state.

## State And Recovery Requirements

- Empty: no assigned work, no matching filters, no access, no workspace, no alerts.
- Loading: avoid layout jump in queues; keep filters visible.
- Stale: show last updated time and refresh behavior for dashboards and records.
- Conflict: detect record updated elsewhere before destructive or approval actions.
- Offline: support draft notes, queued actions, or read-only cache only when safe and labeled.
- Permission denied: explain missing role or workspace and provide request/escalation path.
- Error: preserve comments, forms, filters, and selected records after failure.
- Recovery: undo, cancel, retry, reassign, reopen, and audit note where appropriate.

## Accessibility Notes

- Support keyboard/screen-reader flows for dense lists, tables, and action sheets.
- Do not rely only on color for severity, status, ownership, or SLA breach.
- Keep row labels explicit; repeated records must be distinguishable by screen reader.
- Use clear focus order in filters, bulk-selection, and approval sheets.
- Avoid tiny metadata clusters that collapse under large text.
- Provide accessible names for icon-only workspace, sort, filter, and overflow controls.

## Platform Notes

- Respect native navigation expectations: predictable back behavior, deep links, and recoverable modals.
- On Android, design for predictive back, resizable windows, and edge-to-edge layouts where relevant.
- On iOS, use familiar navigation stacks, contextual menus, and confirmation patterns for consequential actions.
- Use system share sheets, file pickers, notification settings, and authentication where possible.
- Consider tablet and foldable breakpoints without assuming full desktop parity.

## Evidence And Compliance Boundaries

- Do not claim a mobile workflow is operationally safe without customer/process validation.
- Do not infer enterprise compliance controls from UI affordances alone.
- Audit logs, permissions, data retention, and approval policy need backend and security confirmation.
- Benchmarks can inspire queue/list/detail structure but cannot prove correctness for a customer's process.
- This pack is not compliance proof; security, privacy, procurement, and retention claims need qualified review.
- Treat role, workspace, tenant, and data-residency assumptions as open questions unless specified.

## Design-Quality Traps

- Dashboard-first mobile apps that avoid the actual job-to-be-done.
- Desktop table shrinkage instead of mobile triage hierarchy.
- Hiding data freshness and permission scope.
- Over-polished empty states that obscure access problems.
- Bulk actions without preview, confirmation, undo, or audit intent.
- Notification settings that mix critical operational alerts with marketing or low-priority updates.

## Handoff Checks

- Define roles, permissions, workspace/tenant boundaries, and hidden-field behavior.
- Specify list sorting, filtering, saved views, pagination/infinite scroll, and stale-data states.
- Map every record status, action availability rule, and conflict outcome.
- Include audit trail requirements, confirmation copy, undo windows, and failure recovery.
- Provide responsive layouts for compact phones, large phones, tablets, and foldables if in scope.
- Flag security, compliance, customer-success, and operations review items.

## Source Anchors

- Apple HIG, Android mobile UI guidance, W3C WCAG 2.2, W3C mobile accessibility.
- GOV.UK Service Manual patterns are useful for forms, errors, and service recovery.
- Use these as grounding references; customer workflow evidence still needs discovery.
