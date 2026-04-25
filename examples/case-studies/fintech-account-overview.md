# Synthetic Case Study: Fintech Account Overview

## Prompt

```text
Use the mobile-design-skill.

Design a mobile screen concept for a personal finance account overview.

Inputs:
- Platform: cross-platform
- User goal: quickly understand current cash position and recent account activity
- Audience: general consumers with mixed financial literacy
- Constraints: trust-sensitive, privacy-sensitive, avoid financial advice, include pending transactions
```

## Weak response

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- The app has accounts and transactions.
- Users want a modern dashboard.

Use a clean dashboard with a large balance card at the top, colorful spending chart, and recent transactions below. Add quick actions for transfer, pay, and deposit. Use green for positive amounts and red for negative amounts. Add a pull-to-refresh pattern and an empty state if there are no transactions.

Accessibility considerations: use readable fonts, labels, and enough contrast.
Next actions: validate with users and polish the UI.
```

## Why this is weak

- Treats finance trust as visual polish instead of clarity, freshness, and traceability.
- Does not explain pending versus posted balances, stale data, hidden amounts, or privacy mode.
- Uses red/green as a primary semantic channel without non-color cues.
- Quick actions appear before risk-sensitive context or confirmation rules.
- States are generic and not tied to financial failure modes.

## Strong response

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- The overview shows read-only account status first; money movement starts from secondary actions.
- Balance data can be current, stale, partially synced, or unavailable.
- Pending transactions may affect available balance but are not final posted activity.

## Screen goal
Help users understand available cash, recent changes, and whether the displayed data is current before they act.

## Primary user task
Check "Can I safely spend or move money right now?" without interpreting a chart.

## Information hierarchy
1. Available balance, account name, and last-updated timestamp
2. Posted balance and pending impact, visually separated from available balance
3. Recent activity grouped by pending and posted
4. Secondary insights, such as spending category summary
5. Money movement actions after status clarity

## Recommended layout structure
- Header: account selector, masked account identifier, privacy toggle for hiding amounts.
- Balance summary: available balance as the focal value; posted balance and pending delta as supporting values.
- Data status row: "Updated 2 min ago", "Refreshing", "Some institutions unavailable", or "Last known balance".
- Activity list: pending group first, posted group second, each row with merchant, date, amount, status, and dispute/support affordance where relevant.
- Quick actions: transfer, pay, deposit, and statements below the account status zone.

## Empty / loading / error states
- Loading: skeleton for balance and list; do not show old amounts as if current.
- Partial sync: keep last known values but label unavailable accounts and exclude them from totals.
- Empty activity: explain whether the account is new, filtered, or has no posted activity.
- Error: show last successful timestamp, retry, and support path; avoid silent background failure.

## Alternatives considered
- Rejected: chart-first dashboard. It can support exploration later, but it weakens the primary cash-position task.
- Rejected: hiding pending transactions in a separate tab. Pending impact must be visible near available balance.

## Platform-specific notes
- iOS: account details can use a native list with large title at account level; destructive or sensitive actions use system confirmation patterns.
- Android: system back returns to the account list while preserving scroll and privacy state; Material pull-to-refresh should not replace explicit stale-data messaging.

## Accessibility considerations
- Amounts need text labels, signs, and grouping; do not depend on red/green only.
- Rows expose merchant, amount, date, and status in screen reader order.
- Privacy mode must hide values consistently in cards, charts, widgets, and recents.
- Large text should stack balance metadata under the amount instead of truncating.

## Design quality calibration
- Quality target: 4/5 - strong once institution data rules and terminology are confirmed.
- Trust comes from hierarchy, timestamps, pending-state clarity, and restrained color, not from decorative finance charts.

## Next actions
- Confirm exact definitions for available balance, posted balance, pending amount, and stale data.
- QA privacy mode, partial-sync, no-activity, long merchant names, large text, dark mode, and screen reader row order.
```

## Why this is stronger

- Converts a generic dashboard into a task-specific cash-position screen.
- Separates facts, assumptions, and recommendations without financial advice.
- Handles stale, partial, pending, and privacy states.
- Provides concrete platform and accessibility behavior.
- Names rejected alternatives and why they are weaker for this task.

## Regression checks

- Does the response put data freshness near the balance?
- Does it distinguish pending from posted activity?
- Does it avoid advice-like language?
- Does it provide non-color cues for positive, negative, pending, and failed states?
- Does it include privacy mode and partial-data behavior?
