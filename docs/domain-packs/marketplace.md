# Marketplace Mobile Domain Pack

Use this pack for mobile experiences involving buying, selling, booking, delivery, resale, services, creator commerce, local commerce, rentals, or two-sided marketplace interactions.

This pack provides recommendations, not proof of conversion, trust, marketplace liquidity, seller quality, legal compliance, or payment safety.

## When To Use

- Browsing, search, listing, cart, checkout, booking, negotiation, messaging, delivery, or returns.
- Seller onboarding, listing creation, inventory, order management, payouts, or disputes.
- Service marketplaces with availability, location, quote, appointment, or cancellation complexity.
- Any flow where trust depends on availability, price, fees, identity, reviews, timing, or recourse.

## Primary User Jobs

- Find a suitable item/service quickly with relevant filters and trustworthy comparison.
- Understand total cost, availability, delivery/booking timing, condition, and cancellation terms.
- Decide whether the seller/provider, listing, or offer is trustworthy enough.
- Complete checkout or booking with confidence and recover from inventory/payment changes.
- Communicate safely before and after purchase without losing platform protection.
- Resolve issues: delay, cancellation, substitution, refund, return, dispute, or no-show.

## Trust And Safety Risks

- Hidden fees, tax, service charges, deposit, delivery, or cancellation penalties.
- Stale inventory, unavailable appointment slots, or changed prices after selection.
- Misleading ratings, sparse reviews, fake scarcity, or seller-quality overclaim.
- Unsafe off-platform messaging or payment nudges.
- Ambiguous refund, return, dispute, guarantee, or platform-protection language.
- Location/privacy exposure for buyers, sellers, couriers, hosts, or service providers.
- Review pressure that hides negative outcomes or creates retaliation fear.

## Common Mobile Surfaces

- Discovery feed/search with filters, sort, map/list switch, saved searches, and recent views.
- Listing/detail with media, title, price, fees, condition, availability, seller, reviews, and policies.
- Compare/shortlist surface with key differences and saved items.
- Cart/booking composer with quantity, options, delivery/slot, substitutions, and total cost.
- Checkout with payment, address/location, fees, protection, cancellation, and confirmation.
- Order/trip/booking tracking with status, ETA, messages, receipt, and support.
- Seller/provider dashboard with listing status, availability, tasks, payouts, and dispute states.

## Hierarchy Guidance

- Put decision-critical listing facts above promotional or discovery modules.
- Show total price early and repeat it before final commitment.
- Keep availability, condition, seller identity, location radius, and policy terms close to the CTA.
- Separate platform guarantees from seller claims and user reviews.
- Use filters that map to real user constraints: price, distance, date, size, condition, rating, availability.
- Make status timelines concrete: requested, confirmed, preparing, shipped, delivered, completed, disputed.
- Keep messaging and support reachable from order context, not only global help.

## State And Recovery Requirements

- Empty: no results, no saved items, no cart, no orders, no seller listings.
- Loading: preserve filters and prevent phantom availability.
- Stale: revalidate price, inventory, delivery, and slots before commitment.
- Conflict: item sold, slot unavailable, price changed, seller cancelled, payment failed.
- Partial success: order placed but message failed, payment authorized but confirmation pending.
- Offline: avoid committing purchases/bookings while unable to verify availability.
- Recovery: edit options, choose substitute, retry payment safely, cancel, refund, dispute, contact support.
- Post-purchase: clear next step, receipt, policy, and expected update timing.

## Accessibility Notes

- Provide text equivalents for listing media, condition badges, map pins, and delivery status.
- Do not rely on color alone for availability, deal, seller status, or warning labels.
- Ensure filters, sort controls, quantity steppers, calendars, maps, and bottom sheets are accessible.
- Support large text in listing cards without hiding price, fees, or CTA.
- Avoid countdown scarcity that cannot be paused or understood by assistive tech.
- Make chat, support, dispute, and cancellation actions reachable by screen reader.

## Platform Notes

- Use native permissions for location, camera, photos, contacts, notifications, and payments.
- Explain why location, camera, or media access is needed before requesting permission.
- Respect platform payment policies and system payment affordances where applicable.
- On Android, account for predictive back in checkout, booking, and filter sheets.
- On iOS, avoid trapping users in full-screen flows without clear cancel/review paths.

## Evidence And Compliance Boundaries

- Do not claim a listing, seller, payment, review, or guarantee is safe without product evidence.
- Do not infer consumer protection, marketplace liability, tax, insurance, or regional booking rules.
- Do not use benchmark marketplaces as proof that fee hiding, urgency, or review patterns are acceptable.
- This pack is not compliance proof; consumer, payment, tax, and safety claims need qualified review.
- Payment, refunds, disputes, fraud, identity, and off-platform communication need policy review.
- Ratings and reviews need abuse, moderation, and authenticity considerations.

## Design-Quality Traps

- Beautiful listing cards that omit total cost, availability, condition, or seller trust context.
- Checkout that introduces fees late.
- Fake urgency and scarcity replacing useful decision support.
- Treating reviews as pure trust without showing recency, volume, relevance, or moderation boundaries.
- Messaging flows that encourage off-platform risk.
- Support hidden after payment, cancellation, or failed delivery.

## Handoff Checks

- Define listing status, price/fee calculation, availability freshness, and final revalidation rules.
- Specify filter behavior, empty results, saved searches, and map/list parity.
- Map checkout, booking, payment, cancellation, refund, return, and dispute states.
- Include permission rationale, privacy treatment for location/contact/media, and notification categories.
- Document seller/provider states, policy surfaces, and moderation/escalation routes.
- Flag legal, tax, payment, consumer protection, and trust/safety review items.

## Source Anchors

- Apple HIG, Android mobile UI guidance, W3C WCAG 2.2.
- Apple App Store Review Guidelines and Google Play policies for payment, UGC, safety, and privacy context.
- Use these as grounding references; marketplace policy and legal obligations remain product-specific.
