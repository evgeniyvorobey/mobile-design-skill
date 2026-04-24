# Rubric Before / After

This example shows how the 1-5 rubric upgrades a weak response into a stronger, shippable design recommendation.

---

## Prompt

```text
Use the mobile-design-skill.

Create a cross-platform UI spec for a subscription settings screen.
Users need to see current plan, renewal date, payment method, invoices, and cancel option.
```

---

## Weak response

```md
Mode: Create platform-aware UI spec
Platform scope: Cross-platform
Assumptions:
- Subscription is active.
- Users can update payment and cancel.

## Structural zones
- Header with title
- Plan card
- Payment card
- Invoices card
- Cancel button

## State definitions
- Default
- Loading
- Error

## Behavior rules
- Show the current plan.
- Let the user update payment.
- Let the user cancel.

## Design quality requirements
- Quality target: 2/5 — visible structure exists, but the spec is not buildable enough.
- Attention path: user sees plan first.
- Composition and spacing: use clean spacing.
- Typography: make headings clear.
- Color and state: use error color when needed.
- Interaction polish: show loading.
- Production checks: test before launch.
```

### Why it scores 2/5

- It is template-complete but decision-empty.
- It does not define cancellation, payment failure, restore/reactivate, invoice empty state, or platform billing differences.
- It uses vague mechanisms: "clean spacing", "clear headings", "test before launch".
- It gives engineering almost no behavior rules.

---

## Improved response

```md
Mode: Create platform-aware UI spec
Platform scope: Cross-platform
Assumptions:
- Subscription management happens inside the app, but platform billing policy still needs product/legal confirmation.
- The user is authenticated and has at least one active or expired subscription record.

## Screen or flow scope
Subscription settings screen covering plan summary, renewal/payment maintenance, invoices, cancellation, and recovery states.

## Structural zones
- Summary zone: current plan name, price, renewal date, and status badge in one grouped block.
- Payment zone: masked payment method, payment status, and Update action.
- Records zone: invoices/receipts list with empty state for no invoice history.
- Support zone: terms, billing support, and restore/reactivate where applicable.
- Destructive zone: Cancel subscription as a secondary/destructive action separated from routine maintenance.

## State definitions
- Default: active plan with renewal date and payment method.
- Payment issue: warning banner above payment zone; Update payment becomes recommended action.
- Cancel pending: show access end date and reactivation action if product policy allows.
- Expired: plan summary switches to expired status with renewal/reactivation entry point.
- Loading: skeleton for summary and payment rows; hide cancellation until subscription status is known.
- Empty invoices: explain that receipts appear after completed billing cycles.
- Error: keep last known subscription state visible and provide retry.

## Behavior rules
- If payment status is failed, place the warning before invoices because recovery is time-sensitive.
- If cancellation is tapped, open a confirmation flow that explains access end date before final confirmation.
- If platform billing owns the subscription, route to the platform-managed subscription screen instead of showing unsupported in-app controls.
- Preserve last known subscription data during refresh so the screen does not collapse into a blank state.

## Design quality requirements
- Quality target: 4/5 — shippable structure once billing ownership and cancellation policy are confirmed.
- Attention path: first glance answers "what plan am I on and when does it renew?"; second glance handles payment health; cancellation stays visible but not visually dominant.
- Composition and spacing: use 16dp/pt screen padding, 12dp/pt row rhythm inside groups, and 24dp/pt separation before destructive actions.
- Typography: plan name uses title role, renewal/payment metadata uses body role, legal/support links use label/body-small only when noncritical.
- Color and state: failed payment uses warning/error semantic role with icon + text; cancellation is destructive by label and placement, not color alone.
- Interaction polish: update payment, restore, retry, and cancel confirmation need pressed, loading, success, and error states.
- Production checks: QA large text, dark mode, platform billing redirect, empty invoices, payment failure, cancel pending, and restore/reactivate.

## Key decision tradeoffs
- Summary-first structure chosen over action-first structure because users need billing confidence before maintenance actions.
- Secondary cancellation placement chosen over bottom primary destructive CTA because cancellation is important but not the routine entry task.
```

### Why it scores 4/5

- The primary attention path is explicit.
- States and recovery paths are concrete.
- Visual quality is translated into spacing, type, state, and interaction mechanisms.
- Platform billing uncertainty is exposed instead of invented.
- Engineering can begin implementation without guessing the whole behavior model.

### What would make it 5/5

- Confirm exact billing ownership rules for iOS and Android.
- Add localization and long-currency formatting behavior.
- Add analytics events and acceptance criteria for each state transition.
- Validate cancellation copy and refund policy with product/legal.
