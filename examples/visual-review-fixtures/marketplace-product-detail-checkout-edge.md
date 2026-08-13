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

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform mobile
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- This is a phone-first product detail page, 390 x 844 px, with a sticky "Buy now" that can skip cart.
- Substitution preference is enabled by default, as stated.
- Stock is limited ("Only 2 left"); whether that figure is accurate is not stated and is not assumed.

## Quick summary
The buying path is clear and media-first, but it carries several trust and recovery risks before a fast purchase: total cost is delayed until checkout, substitution is opted in by default, there is no recovery if stock changes mid-checkout, return terms are buried, and payment errors are toast-only. None of this is called deceptive — but the combination undermines confidence before a one-tap buy. The structure can support a fast path once transparency improves; visual properties cannot be judged from text.

## Strengths
- Leads with media-first product exploration via the image carousel.
- Surfaces a stock signal, a seller module (rating, response time), and return terms on the page.
- Provides a checkout sheet that can support a fast path if transparency is improved.

## Findings

### F1 — Total cost is delayed until checkout
- Lens: Usability
- Observation: The base price is prominent (24 px), but it excludes shipping and taxes; the total appears only after address loads in the checkout sheet.
- Violated principle: Nielsen #1 Visibility of system status; match between system and the real world (true cost expectations).
- User consequence: A user can commit toward "Buy now" anchored on a base price and only discover the real total deep in checkout, a trust and abandonment risk.
- Change: Show an estimated total or total range (and the shipping/tax dependency) before the CTA, and update it as soon as address is known.
- Predicted effect: Should reduce surprise at the final total; confidence M (D2 text-only — structural inference, not measured). No conversion claim is made.
- Severity: 3 (major) — frequent (every purchase), high impact (trust, cost), persistent.
- Moves: Production readiness 2→3; lifts cap: delayed total-cost transparency.

### F2 — Substitution is opted in by default
- Lens: Usability
- Observation: The substitution preference is enabled by default in the checkout sheet.
- Violated principle: Nielsen #3 User control and freedom; Nielsen #5 Error prevention (avoid default opt-ins for consequential choices).
- User consequence: Users may unknowingly accept substitutions they did not want, receiving a different item — a trust violation if not clearly chosen.
- Change: Make substitution an explicit choice (off by default, or a clear inline decision) with a plain explanation of what substitution means.
- Predicted effect: Should reduce unwanted substitutions; confidence M (D2 text-only).
- Severity: 3 (major) — frequent, high impact (wrong item, trust), persistent until changed.
- Moves: Production readiness 2→3; lifts cap: default opt-in risk.

### F3 — No recovery if stock changes mid-checkout
- Lens: Usability
- Observation: Stock is limited ("Only 2 left") and inventory can change during checkout, but no stock-change state is described.
- Violated principle: Nielsen #1 Visibility of system status; Nielsen #9 Help users recognize, diagnose, and recover.
- User consequence: A user can complete checkout for an item that sold out, hitting a late failure with no graceful recovery.
- Change: Add a stock-change dialog that detects sell-out before payment and offers options (wait-list, substitute with consent, or cancel).
- Predicted effect: Should reduce dead-end checkouts on stock change; confidence M (D2 text-only).
- Severity: 3 (major) — occasional but high impact, persistent until handled.
- Moves: Production readiness 2→3; lifts cap: missing stock-change recovery.

### F4 — Payment errors are toast-only
- Lens: Usability
- Observation: Payment failure uses a toast only; whether the checkout form is preserved is not described.
- Violated principle: Nielsen #9 Help users recognize, diagnose, and recover from errors; Nielsen #1 Visibility of system status.
- User consequence: A transient toast is easy to miss and may not preserve checkout context, forcing re-entry or an unclear failure.
- Change: Show a persistent, specific payment-error state that preserves the checkout form and offers retry.
- Predicted effect: Should reduce missed payment errors and re-entry; confidence M (D2 text-only).
- Severity: 3 (major) — occasional but high impact (failed purchase), persistent until changed.
- Moves: Interaction polish & motion 2→3; lifts cap: toast-only error recovery.

### F5 — Return terms are de-emphasized before purchase
- Lens: Hierarchy & readability
- Observation: Return terms are a collapsed disclosure in small gray text, sixth in the hierarchy, before a final purchase action.
- Violated principle: Nielsen #1 Visibility of system status; recognition over recall.
- User consequence: Important, seller-variable return terms are easy to miss before buying, which can cause post-purchase disputes.
- Change: Summarize key return terms near the CTA (not only in a collapsed block) so they are visible before purchase.
- Predicted effect: Should improve awareness of return terms before buying; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path & hierarchy 2→3.

### F6 — Stock urgency relies on color alone
- Lens: Accessibility
- Observation: Stock urgency is conveyed by orange text only.
- Violated principle: WCAG use-of-color (1.4.1) — color must not be the only means of conveying information.
- User consequence: Users with color-vision differences or in glare may not register the urgency signal, missing a relevant stock cue.
- Change: Pair the stock signal with an icon and/or explicit text (e.g. "Only 2 left in stock") rather than color alone.
- Predicted effect: Should make the stock signal perceivable beyond color; confidence M (cannot verify rendering from text).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Production readiness 2→3.

### F7 — No final review before a one-tap purchase
- Lens: Usability
- Observation: "Buy now" can skip cart and there is no described final review row before payment is committed.
- Violated principle: Nielsen #5 Error prevention; Nielsen #3 User control and freedom.
- User consequence: A fast path without a final review can let users commit to a purchase before confirming item, total, and substitution choice.
- Change: Add a concise final review row (item, total, substitution choice, return summary) before the purchase is committed.
- Predicted effect: Should reduce accidental or under-informed purchases; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Production readiness 2→3.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {1, 1, 2, 2, 2, 3}; pinned by delayed total cost (F1), default substitution (F2), no stock-change recovery (F3), and toast-only payment errors (F4).
- Projected: 3/5 — median of the assessable projected bands {1, 3, 3, 3, 3, 4} once F1+F2+F3+F4 land (plus F5/F6/F7); held there by the typography and distinctiveness bands no finding touches.
- Ceiling note: with a visual pass confirming media quality, contrast, and spacing the leading band reaches 4, but the inert-screen cap holds the artifact at 3/5 until the page carries one owned asset (large-text, contrast of small gray/orange text, and dark mode are still unverified from the description).
- Primary lever(s): F1 + F2 (cost transparency and explicit substitution, the trust pair that most pins a checkout edge at 2).

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Production readiness | 2 | 4 | F1/F2/F3/F7 lift trust caps | provisional |
| Attention path & hierarchy | 2 | 3 | F5 return terms (rung 2→3) | provisional |
| Interaction polish & motion | 2 | 3 | F4 error state (rung 2→3) | provisional |
| Color, state & contrast | 1 | 3 | stock urgency is orange-only, so the second-cue test fails (F6); 3→4 needs stated pairs and their dark-theme values | provisional |
| Typography craft | 3 | 3 | eight roles carry stated sizes and weights; 3→4 needs the behaviour named when text scales up, which no finding supplies | provisional |
| Distinctiveness & owned assets | 1 | 1 | inert — a canonical product-detail page once the logo is removed, and no finding adds an owned asset | provisional |
- Projected overall = median of the assessable projected dimensions {4, 3, 3, 3, 3, 1} = 3. Not the sum of per-dimension gains; colour stops at 3 because a description states no pair, and that rung is never projected upward from text.

## Severity index
- 4 (catastrophe): none
- 3 (major): F1, F2, F3, F4
- 2 (minor): F5, F6, F7
- 1 (cosmetic): none

## Platform-convention mismatches
- Cross-platform caution: the sticky CTA, checkout sheet, and toast/dialog behavior should follow each platform's idioms rather than a single forced pattern.
- Payment-error and stock-change prompts should use platform-idiomatic dialogs rather than a transient web-style toast.

## Unresolved assumptions
- Cannot verify image quality, carousel cropping, or product-photo trust from text.
- Cannot verify contrast of the orange stock text or small gray return terms from text.
- Cannot verify tap-target sizes from the description.
- Cannot call the urgency false or the flow legally deceptive; limited stock is stated, accuracy is not, and no conversion claim is made.

## Next actions
- Show an estimated total before the CTA, make substitution explicit opt-in, and add a stock-change recovery path before any visual polish.
- Replace the payment toast with a persistent error state that preserves the form, summarize return terms near the CTA, and add a final review row.
- Run a visual pass with large text and color-vision simulation to confirm the projected score.
```

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

Severity uses the Nielsen 0-4 scale (High maps to 3, or 4 if irreversible/catastrophic; Medium to 2; Low to 1).

- 3 (major): delayed total cost, default substitution, no stock-change recovery, payment error toast only.
- 2 (minor): return terms de-emphasized, color-only stock urgency, seller-unavailable gap.
- 1 (cosmetic): media carousel quality and visual polish should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected score: current 2/5 → projected 3/5 (flat median of the assessable dimensions, conditional, provisional D2).
- Reason for current: the buying path is clear and the type roles are decided, but fee transparency, inventory volatility, default opt-in, orange-only urgency, and recovery states create trust and checkout-risk gaps.
- Reason for projected: showing total cost before the CTA, making substitution explicit opt-in, and adding stock-change and payment-error recovery lift production readiness to 4 — but typography stays at 3 because no finding names the text-scaling behaviour, the page owns no asset, and media quality, contrast, and spacing cannot be raised from a text-only description.
- No Bold move is expected: the screen has unresolved severity-3 findings, so the Bold move trigger is not met.
