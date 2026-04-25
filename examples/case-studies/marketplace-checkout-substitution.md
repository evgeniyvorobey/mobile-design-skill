# Synthetic Case Study: Marketplace Checkout Substitution

## Prompt

```text
Use the mobile-design-skill.

Create a mobile screen concept for grocery marketplace checkout with substitution preferences.

Inputs:
- Platform: cross-platform
- User goal: finish checkout while controlling what happens if items are unavailable
- Audience: busy shoppers
- Constraints: inventory can change, totals may change, substitutions require consent, pickup or delivery
```

## Weak response

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- Some items may be substituted.
- Users want a fast checkout.

Add a checkout page with order summary, payment, delivery address, and a substitution checkbox. If items are out of stock, let the shopper approve replacements later. Show a final total and a place order button. Use cards and a progress indicator.

Accessibility considerations: make the checkbox accessible and use clear labels.
Next actions: test checkout and validate substitutions.
```

## Why this is weak

- A single substitution checkbox hides item-level decisions and price sensitivity.
- Does not explain total volatility, replacement price limits, or "do not replace" choices.
- Pushes consent to later, when the user may miss the prompt.
- Missing recovery for item unavailable before payment, after payment, or during fulfillment.
- Treats checkout as generic instead of trust-sensitive commerce.

## Strong response

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- The marketplace can provide item availability and substitution candidates, but inventory may change after checkout.
- Substitution consent must be explicit per item or per clearly scoped group.
- Final charges may differ within product-approved limits.

## Screen goal
Let shoppers place an order while understanding which items can change, how much totals can change, and how to recover if availability shifts.

## Primary user task
Review order risk and set substitution preferences before final payment confirmation.

## Information hierarchy
1. Delivery/pickup slot and inventory freshness
2. Items requiring substitution decisions
3. Total estimate with possible adjustment rules
4. Payment and final confirmation
5. Secondary policies: refund, contact, shopper notes

## Recommended layout structure
- Status strip: selected store, slot, and inventory timestamp.
- Substitution review module above final total when any item is volatile.
- Item rows: original item, quantity, price, availability state, and preference.
- Preference controls: "Best similar item", "Only this brand/size", "Contact me", "Do not replace".
- Total module: current subtotal, estimated substitution range if supported, fees, taxes, and authorization note.
- Final CTA: "Place order" with concise consent copy near the button.

## Empty / loading / error states
- Loading: hold payment CTA until inventory and substitution rules resolve.
- No substitution needed: collapse module but leave "Substitution preferences" reachable from item rows.
- Item unavailable before checkout: require decision before final CTA.
- Inventory changes after submit: notification opens to an item-specific decision screen with deadline and default behavior.
- Payment error: preserve cart, slot, and substitution choices.

## Alternatives considered
- Rejected: one global substitution checkbox. It is fast but hides important item-level consent.
- Rejected: delaying all substitution choices until shopper fulfillment. It reduces checkout friction but increases missed decisions and unwanted replacements.

## Platform-specific notes
- iOS: use a review screen or sheet for item preference editing; avoid nested sheets for payment plus substitution.
- Android: system back from preference editing returns to checkout with choices preserved; Material chips can represent preference state if labels remain visible.

## Accessibility considerations
- Preference controls must be explicit radio choices, not color-only tags.
- Total changes should be announced as estimate/range, not final charge.
- Long product names and quantity/unit labels must remain readable with large text.
- Shopper-contact deadlines need text and time, not only countdown color.

## Design quality calibration
- Quality target: 4/5 - shippable after legal/payment language and substitution defaults are confirmed.
- Trust comes from item-level consent, total transparency, and preserving choices through checkout errors.

## Next actions
- Confirm substitution preference taxonomy, payment authorization copy, and default behavior when the shopper does not respond.
- QA out-of-stock before checkout, after submit, payment failure, expired slot, large text, and screen reader order.
```

## Why this is stronger

- Moves substitution decisions before final commitment where they affect trust.
- Handles volatile inventory and total changes without inventing business metrics.
- Provides item-level mechanisms and recovery paths.
- Makes consent auditable and accessible.
- Names the tradeoff between friction and unwanted replacements.

## Regression checks

- Does the response avoid one vague global substitution control?
- Does it explain total estimate versus final charge risk?
- Does it define what happens when inventory changes after submit?
- Does it preserve cart, slot, payment, and substitution choices after errors?
- Does it provide explicit "do not replace" behavior?
