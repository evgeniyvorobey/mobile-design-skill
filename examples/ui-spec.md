# Example: Create platform-aware UI spec

## Example prompt

```text
Use the mobile-design-skill.

Create a platform-aware UI spec for a package tracking detail screen.

Inputs:
- Platform: Android
- Product: delivery app
- User goal: check delivery progress and contact support if something looks wrong
- Constraints: high status clarity, must work well with large text, frequent repeat use
- Current screen description:
  - top app bar with tracking number
  - progress steps
  - package details
  - delivery address
  - support actions
```

## Example output

```md
Mode: Create platform-aware UI spec
Platform scope: Android
Device class: Phone (compact width only; a regular-width layout can be added on request)
Assumptions:
- This screen is reached from a shipment list or push notification.
- Shipment status updates are near real-time.
- Users are authenticated and permitted to view address details.

## Screen or flow scope
Single detail screen for one tracked package, optimized for status comprehension and support escalation.

## Structural zones
- Top area:
  - top app bar with back navigation and concise title
- Status summary zone:
  - current delivery state
  - ETA or delivery window
  - visual step progression
- Detail zone:
  - package metadata
  - address block
- Action zone:
  - support and issue-reporting actions
- Supporting zone:
  - event timeline if space allows below primary details

## Components by section
### Top app bar
- Back navigation
- Title: Tracking details
- Optional overflow for secondary actions such as share only if supported

### Status summary
- Status headline
- Supporting ETA text
- Progress tracker with labeled steps
- Alert container if delay or exception exists

### Package details
- Tracking number
- Carrier or courier name
- Package type if relevant

### Address block
- Delivery address
- Delivery instructions summary if available

### Action zone
- Primary secondary-style action: Contact support
- Optional action: Report an issue
- Optional action: Refresh status if manual refresh exists

### Event timeline
- Reverse chronological tracking events
- Timestamp + short description

## State definitions
- Default:
  - current status, ETA, visible details, available support action
- Loading:
  - skeleton for status and timeline
- Empty:
  - no timeline events yet, but package exists
- Error:
  - status unavailable, show last known update and retry action
- Exception:
  - delayed, failed attempt, or address issue highlighted above the detail zone
- Delivered:
  - final state with proof-of-delivery content if supported

## Behavior rules
- Keep the current shipment status visible without requiring scroll.
- If a delivery exception exists, surface it above standard progress information.
- Do not hide contact support inside overflow if the shipment is delayed or failed.
- Preserve the last known delivery state when live refresh fails.
- Timeline items should be readable individually without requiring expansion for basic status meaning.

## Color and state rules
- Four status roles, each a container/on-container pair rather than a single hue: in-transit uses the neutral surface with default on-surface text; delivered uses the success container with on-success text; delayed uses the warning container with on-warning text; failed and address-issue use the error container with on-error text.
- Every pair carries a text label and a step icon, so removing colour loses emphasis and never loses meaning. Delayed and failed must remain distinguishable without hue, since both sit in the same alert container position.
- Contrast floor: 4.5:1 for status text on its container, 3:1 for the progress tracker's step fills and the container edge against the screen background.
- Dark theme is one transform, not a second palette: containers drop to the low-emphasis tonal step and the on-container roles take the light text token, with the same four pairings and the same floors. Increased contrast raises each container one tonal step and keeps the on-container role fixed.
- The alert container keeps its own pair when it moves above the detail zone; it does not inherit the surface it lands on.

## Content guidance
- Use plain status language before internal logistics terminology.
- Make timestamp formatting concise and consistent.
- Separate factual shipment updates from support instructions.
- Avoid showing raw operational codes.

## Spacing and layout notes
- Use 16dp horizontal screen padding on phone layouts.
- Use 24dp between the status zone and the detail zone; use 12-16dp between related rows inside a zone.
- Keep support actions at a minimum 48dp touch height with 8dp minimum separation between independent targets.
- Allow enough vertical space for large-text expansion in the progress tracker and address block; avoid fixed-height containers for status text.
- Avoid multi-column compression on phone layouts.

## Typography rules
- Status headline: 22-24sp, 28-32sp line height, strongest emphasis on screen
- ETA/supporting time: 16sp body style with 24sp line height
- Section labels: 14sp medium label style, clearly distinct from body text
- Event rows: 16sp body for event text, 12-14sp lower-emphasis timestamp
- Action labels: 16sp medium emphasis with short phrasing

## Accessibility requirements
- Status changes must not rely on color alone.
- Progress steps need text labels, not just icons or dots.
- Address and support actions must remain accessible at larger text sizes.
- Focus order should move from screen title to status summary to details to actions to timeline.
- Interactive controls need comfortable touch targets and clear labels.

## Design quality requirements
- Direction: structured-neutral — status colour held apart from brand colour so a wrong status read is never a branding accident (from: baseline) — committed over the editorial and perceived-speed directions in `Key decision tradeoffs`
- Dimension read: attention path 4, composition 4, typography 4, colour/state 5, density 4, interaction 4, context & brand fit 3, production readiness 3, distinctiveness 4. Median of the assessable = 4.
- Quality target: 4/5 — shippable Android detail screen, blocked from 5/5 by Context & brand fit and Production readiness, both at band 3, until the spec states a departure budget for what brand may override and gives the remaining values token names with their state-to-component mapping.
- Attention path:
  - First glance must land on current status and ETA; second glance moves to exception/support actions; timeline is tertiary.
- Composition and spacing:
  - Use a status summary block with 24dp separation from detail rows and 12dp row rhythm inside metadata groups.
- Typography:
  - Keep the status headline at 22-24sp and timeline body at 16sp so the status does not compete with historical events.
- Color and state:
  - Four status roles as container/on-container pairs with stated contrast floors, and dark and increased-contrast derived as one transform over those roles rather than a second palette, so a new status role inherits its appearance behaviour without a hand-made variant.
- Interaction polish:
  - Refresh and support actions need pressed, loading, success, and error states; background refresh should preserve the last known status.
- Signature move:
  - One owned motion token, `motion.status-advance` (240ms, standard-decelerate), plays wherever tracking state moves forward: the timeline row entering, the status headline swapping, and the refresh success confirmation. It is a motion signature rather than an invented brand color, so it needs no brand input, and repeating it in exactly three named places is what makes it an owned asset instead of decoration. Reduced-motion fallback: cross-fade, no translation.
- Production checks:
  - QA large text at 200%, dark theme, delayed-status exception, offline retry, and TalkBack focus order.

## Platform-specific implementation notes
### Android
- Respect predictable system back behavior from detail screen to shipment list or originating context.
- Keep the top app bar behavior stable during scroll; avoid hiding key orientation information too aggressively.
- Use Material-aligned status and action hierarchy rather than a custom ornamental tracker.

## Key decision tradeoffs
- Status-first structure chosen over timeline-first structure because users check current delivery progress before reading historical events.
- Inline support actions chosen over overflow-only support because exception states require quick recovery and should not hide help behind a secondary menu.
- Labeled progress tracker chosen over icon-only steps because delivery states must remain understandable without relying on color or icon interpretation.
- Direction rejected — perceived speed first (from: Superhuman): base unit 8, ratio 1.2, optimistic status rendering with skeletons at the 200 ms threshold, signature transition pushed to the fastest band — rejected because carrier data arrives on the carrier's schedule, not the app's, and optimistic rendering of a status the app cannot yet confirm is the one failure mode a tracking screen must not have.
- Direction chosen — structured-neutral (from: baseline): base unit 8, ratio 1.25, one accent held apart from the semantic status colours, status band as the composition move, `motion.status-advance` as the signature). Gave up expressive range in exchange for status colour that never competes with brand colour — the right trade when a wrong status read costs the user a missed delivery.
- Direction rejected — editorial (from: Brutalist / editorial web craft): base unit 4, ratio 1.333, display face on the status headline, one grid-breaking full-bleed block, abrupt 150 ms motion — rejected because a delivery screen is checked in seconds under interruption, and an irregular vertical rhythm slows the status read; the cost of the rejection is a less memorable screen, accepted deliberately.

## Next actions
- Confirm whether proof-of-delivery, map preview, or courier contact are in scope.
- Define exact exception states and corresponding support actions.
- Test the progress tracker and timeline with large text and delayed-status scenarios.
```
