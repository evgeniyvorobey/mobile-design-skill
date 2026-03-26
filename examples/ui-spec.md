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

## Content guidance
- Use plain status language before internal logistics terminology.
- Make timestamp formatting concise and consistent.
- Separate factual shipment updates from support instructions.
- Avoid showing raw operational codes.

## Spacing and layout notes
- Use stronger separation between the status zone and the detail zone than between items within a zone.
- Keep the action zone visually distinct from informational rows.
- Allow enough vertical space for large-text expansion in the progress tracker and address block.
- Avoid multi-column compression on phone layouts.

## Typography rules
- Status headline: strongest emphasis on screen
- ETA/supporting time: secondary emphasis
- Section labels: compact but clearly distinct
- Event rows: readable body style with lower-emphasis timestamp
- Action labels: medium emphasis and short phrasing

## Accessibility requirements
- Status changes must not rely on color alone.
- Progress steps need text labels, not just icons or dots.
- Address and support actions must remain accessible at larger text sizes.
- Focus order should move from screen title to status summary to details to actions to timeline.
- Interactive controls need comfortable touch targets and clear labels.

## Platform-specific implementation notes
### Android
- Respect predictable system back behavior from detail screen to shipment list or originating context.
- Keep the top app bar behavior stable during scroll; avoid hiding key orientation information too aggressively.
- Use Material-aligned status and action hierarchy rather than a custom ornamental tracker.

## Next actions
- Confirm whether proof-of-delivery, map preview, or courier contact are in scope.
- Define exact exception states and corresponding support actions.
- Test the progress tracker and timeline with large text and delayed-status scenarios.
```
