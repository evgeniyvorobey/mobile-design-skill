# Visual Review Fixture: Marketplace Product Detail / Checkout Edge

## Review setup

- Synthetic fixture only. No screenshots, real brands, or copied UI.
- Review evidence type: D2, text description only.
- Platform scope: Cross-platform mobile marketplace.
- User task: decide whether to buy an item and understand price, availability, delivery, return, and seller risk before checkout.

## Screen description

A marketplace product detail page includes a sticky "Buy now" action that can skip cart and open checkout. The item has limited stock, variable shipping fee, seller-provided return terms, and optional substitution if the item sells out before payment.

## Frame specs

- Frame: 390 x 844 px mobile portrait.
- Product media carousel at top: 320 px height.
- Product title, rating, price, delivery estimate, seller module, and return terms follow.
- Sticky bottom CTA: "Buy now".
- Checkout sheet can slide up over the product page.

## Visible hierarchy

1. Product media carousel.
2. Product title and price.
3. "Only 2 left" stock message.
4. Delivery estimate.
5. Seller rating.
6. Return terms disclosure.
7. Related items carousel.
8. Sticky "Buy now" CTA.

## Components

- Product image carousel indicator.
- Price row with base price.
- Stock urgency label.
- Delivery estimate row.
- Seller card with rating and response time.
- Return terms collapsed disclosure.
- Substitution preference checkbox in checkout sheet.
- Sticky CTA.
- Checkout sheet with address, shipping fee, taxes, total, and payment method.

## Typography

- Product title: 19 px semibold.
- Base price: 24 px semibold.
- Stock label: 13 px medium.
- Delivery estimate: 14 px regular.
- Seller metadata: 12 px regular.
- Return terms summary: 12 px regular.
- Checkout total: 18 px semibold.
- Sticky CTA label: 16 px semibold.

## Color and state notes

- Stock urgency uses orange text only.
- Price in product detail excludes shipping and taxes.
- Checkout sheet shows total only after address loads.
- Substitution preference is enabled by default.
- Return terms disclosure uses small gray text.
- Payment error state is a toast.

## Interaction states

- Default product detail described.
- Image loading state not described.
- Price recalculation after address entry is described but not visually specified.
- Stock change while user is in checkout is not described.
- Payment failure uses toast only.
- Substitution opt-out state exists.
- Seller unavailable state is not described.

## Known constraints

- Marketplace inventory can change while the user is checking out.
- Shipping and tax depend on address.
- Seller return terms can vary by item.
- Substitution affects trust and should be explicit.
- The screen must avoid dark patterns around urgency, hidden fees, and default opt-ins.

## Expected critique

- The review should flag price transparency risk: base price is prominent, but total cost is delayed until checkout.
- The review should flag stock volatility: "Only 2 left" and checkout need a recovery path if stock changes.
- The review should flag default substitution risk: opt-in by default can undermine trust if not clearly explained.
- The review should flag return-term discoverability: important terms are collapsed and small before a final purchase action.
- The review should flag payment failure weakness: toast-only errors are easy to miss and do not preserve checkout context.
- The review should flag color-only urgency: orange text alone should not be the only stock signal.
- The review should recommend concrete fixes: show estimated total range before CTA, expose shipping/tax dependency, make substitution opt-in explicit, summarize return terms near CTA, add stock-change dialog, preserve payment form after failure, show final review row before purchase.
- The review should note strengths: clear media-first product exploration, visible stock signal, seller module, and checkout sheet can support a fast path if transparency is improved.

## Prohibited critique

- Do not claim the flow is legally deceptive without legal review.
- Do not claim conversion impact from hiding fees.
- Do not assert image quality, carousel cropping, or product-photo trust from text-only evidence.
- Do not claim exact contrast or tap-target failures without measurements.
- Do not call urgency fake; the fixture states limited stock but not whether it is false.
- Do not infer a real marketplace brand.

## Severity expectations

- High: delayed total cost, default substitution, no stock-change recovery, payment error toast only.
- Medium: return terms de-emphasized, color-only stock urgency, seller-unavailable gap.
- Low: media carousel quality and visual polish should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected current design-quality score: 2/5.
- Reason: the buying path is clear, but fee transparency, inventory volatility, default opt-in, and recovery states create trust and checkout-risk gaps.
