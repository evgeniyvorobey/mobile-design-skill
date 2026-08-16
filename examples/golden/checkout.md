# Golden Example: Checkout

## Prompt

```text
Use the mobile-design-skill.

Create a platform-aware UI spec for a grocery delivery checkout screen.

Inputs:
- Platform: cross-platform
- User goal: review order, choose delivery slot, confirm payment, and place order
- Audience: busy repeat shoppers
- Constraints: substitutions matter, fees must be clear, address/payment saved, high error recovery, large text support
```

## Golden output

```md
Mode: Create platform-aware UI spec
Platform scope: Cross-platform
Assumptions:
- User is signed in and has at least one saved address and payment method.
- Cart review happened earlier, but checkout still needs an order summary and substitution confidence.
- Delivery slots, fees, and item availability can change during checkout.

## Screen or flow scope
Single checkout review screen with editable sections for address, delivery slot, substitutions, payment, fees, and final order placement.

## Structural zones
- Delivery section: address, delivery notes, selected slot, and edit actions.
- Substitution section: per-order default plus link to item-level exceptions.
- Payment section: saved method, promo/credit, and payment issue state.
- Order summary: item count, subtotal, delivery fee, service fee, taxes, discounts, tip if applicable, and total.
- Final action area: sticky Place order CTA with total and slot reminder.

## Behavior rules
- If a delivery slot expires or changes price, block final placement and show a specific recovery path.
- If item availability changes, surface it above payment and explain substitution impact.
- Fees must be expandable into clear line items before the final CTA.
- Editing address, slot, payment, or substitutions returns the user to the same checkout state.
- Payment failure should keep the order intact and focus recovery on the payment section.

## State definitions
- Default: saved address, valid slot, valid payment, clear total.
- Slot unavailable: show replacement slots and preserve cart.
- Payment issue: highlight payment section and keep Place order disabled with explanation.
- Item changed: show availability/substitution alert before final total.
- Loading: keep section skeletons stable; do not make the CTA jump.
- Empty: every item became unavailable, so the order cannot be placed — keep the address and slot chosen, replace the summary with the substitution and re-shop paths, and disable Place order with the reason attached.
- Error: preserve last known checkout data and offer retry.

## Design quality calibration
- Dimension read: attention path 5, composition 3, typography 2, colour/state 3, density 3, interaction 3, context & brand fit 4, production readiness 3, distinctiveness 4. Median of the assessable = 3.
- Quality target: 3/5 - the checkout structure and its volatile states are decided but never given values, so it reads as a strong concept under a UI-spec label. Blocked from 4/5 by Typography (2), which assigns no type role to totals against fee labels, and by the five dimensions at 3 whose 3-to-4 boundary asks for the spacing, contrast, interval, motion and token values this spec states nowhere.
- Signature move: `layout.total-anchor` - the running total occupies the same bottom-anchored position at cart, slot selection, and place-order. Its position never moves across the flow, so under time pressure the user's eye never has to search for the number that decides the purchase.
- Checkout quality is confidence under time pressure: users must see where the order goes, when it arrives, what happens if items are missing, and what they will pay.
- The total and Place order action can be sticky, but they must not hide fee disclosure or editable sections.
- Use compact sections with clear edit affordances; avoid turning every section into a visually heavy card if row grouping is enough.
- Reserve urgent color for blocking issues such as expired slot or payment failure; substitution preferences are important but not always errors.
- Large text should stack rows gracefully and keep totals legible without truncating fee labels.

## Production checks
- QA slot expiry during checkout, item availability changes, promo failure, payment decline, address edit return, large text, screen reader order, and dark mode.
```

## Design-quality notes

- Reward answers that anticipate volatile checkout data instead of treating checkout as a static form.
- Penalize hidden fees, weak substitution handling, generic loading states, or CTAs that remain enabled through blocking issues.
- Strong checkout calibration keeps trust, recoverability, and final-price clarity in the same hierarchy.
