# Golden Example: Premium UI

## Prompt

```text
Use the mobile-design-skill.

Generate a mobile screen concept for a premium hotel suite detail screen.

Inputs:
- Platform: iOS
- User goal: decide whether a suite is worth booking for a special trip
- Audience: high-intent travelers comparing a few expensive options
- Constraints: premium visual feel, rich imagery, price transparency, accessibility-sensitive, no marketing fluff
```

## Golden output

```md
Mode: Generate mobile screen concept
Platform scope: iOS
Assumptions:
- The user arrived from search results with dates and guests already selected.
- Real photography and verified amenity data are available.
- Booking is not completed on this screen; the next step is review/reserve.

## Screen goal
Help the traveler judge value quickly: what the suite looks like, what makes it different, what it costs, and what happens if they reserve.

## Primary attention path
1. Suite image and name
2. Nightly price, total estimate, and cancellation status
3. Distinctive amenities and room facts
4. Availability and Reserve action
5. Policies, reviews, and secondary detail

## Recommended layout structure
- Full-width image gallery at the top with visible count and accessible labels.
- Suite identity block with name, property context, rating/review summary, and one-line value cue.
- Price transparency row with nightly price, estimated total, taxes/fees disclosure, and cancellation label.
- Room facts grid with sleep capacity, bed type, size, view, and accessibility-relevant facts.
- Short amenity highlights before long descriptions.
- Sticky bottom action area with price summary and Reserve CTA.

## Interaction and state notes
- Tapping price details opens a fee breakdown, not a vague tooltip.
- Image gallery supports swipe, thumbnail preview, and descriptive alt text for key images.
- If dates change availability, update price and cancellation state in place.
- Sticky CTA must not cover policy text or safe-area controls.

## Design quality calibration
- Dimension read: attention path 4, composition 3, typography 3, colour/state 3, density 3, interaction 3, context & brand fit 5, production readiness 3, distinctiveness 4. Median of the assessable = 3.
- Quality target: 3/5 - a concept whose structure is decided but whose values are not stated; blocked from 4/5 by Interaction polish and motion (3) until the bleed-to-condense header and the in-place price update carry duration, curve and a reduced-motion fallback, and the availability update carries the loading and error states whose absence also caps this at 3/5. Composition, typography, density and production readiness sit at 3 on the same boundary and have to follow.
- Signature move: `layout.hero-bleed` - the hero image bleeds under the status bar and condenses into a 96pt sticky header on scroll. Repeated at the hero, the gallery viewer, and the reservation confirmation, so the same bleed-to-condense gesture identifies the product across all three.
- Premium feel comes from restraint, hierarchy, material quality, and photography, not decorative gradients or oversized type everywhere.
- Use generous top imagery, then compact factual sections so the screen remains useful for a high-cost decision.
- Keep typography elegant but readable: one strong title, body-sized facts, and smaller metadata only for noncritical support.
- Use brand accent sparingly for the CTA and selected gallery state; do not color every premium cue.
- Price, cancellation, and taxes must be visible before the Reserve action earns trust.

## Accessibility and production checks
- Verify image gallery labels, large text wrapping, sticky CTA safe-area spacing, dark mode image overlays, and VoiceOver reading order.
- Do not claim luxury through low-contrast text, tiny captions, or hidden fees.
```

## Design-quality notes

- Reward answers that define premium as trust, restraint, image quality, and decision clarity.
- Penalize answers that suggest vague polish such as "more elegant spacing" without explaining hierarchy, imagery, price disclosure, or states.
- Treat hidden fees, low-contrast luxury styling, and purely atmospheric imagery as regressions.
