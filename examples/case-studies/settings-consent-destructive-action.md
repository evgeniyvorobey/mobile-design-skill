# Synthetic Case Study: Settings Consent And Destructive Action

## Prompt

```text
Use the mobile-design-skill.

Create a platform-aware UI spec for an app settings screen that includes marketing consent, analytics consent, data export, and delete account.

Inputs:
- Platform: cross-platform
- Product: subscription app
- User goal: manage consent and account data without confusion
- Constraints: consent must be explicit, delete account is destructive, legal retention rules are unknown
```

## Weak response

```md
Mode: Create platform-aware UI spec
Platform scope: Cross-platform
Assumptions:
- The app has consent settings.
- Users can delete their account.

Create a settings list with toggles for marketing emails and analytics. Add a data export row and a red Delete account button at the bottom. Add confirmation before deletion. Use simple copy and clear icons.

Accessibility requirements: label toggles and make destructive actions obvious.
Next actions: review with legal and test the flow.
```

## Why this is weak

- Puts consent and account deletion into a generic settings list without auditability or consequence clarity.
- Treats analytics consent as a simple toggle without explaining collection scope or effect.
- Does not handle unknown legal retention rules responsibly.
- Delete account confirmation is underspecified and may hide export/recovery options.
- State coverage is missing for export processing, consent saving, and deletion failure.

## Strong response

```md
Mode: Create platform-aware UI spec
Platform scope: Cross-platform
Assumptions:
- Legal retention, deletion timing, and consent record requirements are not provided and must be confirmed.
- Marketing consent and analytics consent are separate decisions with separate consequences.
- Data export may be asynchronous.

## Screen or flow scope
Settings section for privacy, consent, data export, and account deletion.

## Structural zones
- Privacy overview: short explanation and last updated date for consent settings if available.
- Communication consent: marketing email/push choices with channel-specific labels.
- Product analytics consent: data collection explanation, current state, and effect of turning off.
- Data portability: export request/status/download.
- Account deletion: separate destructive zone leading to a dedicated flow.

## Components by section
- Consent rows use switch controls only for reversible, immediate settings.
- Complex consent opens a detail screen with purpose, current state, and save action.
- Data export row shows idle, requested, processing, ready, expired, and failed states.
- Delete account row is separated from toggles and uses destructive styling plus explanation.

## State definitions
- Consent saving: disable changed control briefly, show saving state, preserve previous value until confirmed.
- Consent save failed: revert or show unresolved pending state based on product rules; never silently flip.
- Export processing: show requested timestamp and expected delivery channel if provided.
- Delete blocked: explain active subscription, unpaid balance, or legal hold only if supplied by backend.
- Delete failure: preserve account, show retry/support, and do not imply deletion occurred.

## Behavior rules
- If legal retention is unknown, say "Deletion request" rather than promising immediate deletion.
- Turning off marketing must not be bundled with account or service-critical notifications.
- Analytics consent copy must not claim privacy guarantees beyond provided policy.
- Delete account requires a dedicated review screen with consequences, export option, and final confirmation.

## Spacing and layout notes
- Keep reversible toggles in grouped rows; destructive action gets its own section after data export.
- Use enough vertical separation so delete is not accidentally tapped while scrolling consent settings.

## Typography rules
- Consequences use body text, not tiny captions.
- Legal/policy links are secondary but visible near the setting they explain.

## Accessibility requirements
- Switch labels include setting name, current state, and immediate effect.
- Delete flow must be keyboard/screen-reader operable without relying on color.
- Error messages announce near the failed control.
- Touch targets meet platform minimums with extra spacing around destructive action.

## Key decision tradeoffs
- Chosen: detail screens for complex consent. They add one tap but reduce misunderstanding.
- Rejected: one "Privacy preferences" master toggle. It hides separate consent purposes.

## Platform-specific implementation notes
- iOS: use native list grouping and a destructive confirmation flow; avoid swipe actions for deletion.
- Android: system back from deletion review returns to settings with no account changes; Material dialog can confirm final irreversible step after review.

## Next actions
- Confirm retention, deletion timing, export delivery, and consent audit requirements with policy/legal.
- QA consent save failure, export processing, export expired, delete blocked, delete failure, large text, and screen reader labels.
```

## Why this is stronger

- Quality target: 4/5 - strong once consent audit, deletion timing, export, and retention rules are confirmed.
- Separates consent semantics from destructive account action.
- Does not overpromise deletion behavior without legal rules.
- Adds state handling for saving, export, and deletion failures.
- Provides a clear implementation contract.
- Preserves user trust through labels, grouping, and recovery.

## Regression checks

- Does the response avoid promising immediate deletion without policy?
- Does it separate marketing, analytics, export, and delete?
- Does it define save failure and export states?
- Does it keep destructive actions away from reversible toggles?
- Does it include final confirmation plus consequences for deletion?
