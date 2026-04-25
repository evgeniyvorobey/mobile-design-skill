# Golden Example: Settings

## Prompt

```text
Use the mobile-design-skill.

Review this mobile settings screen for usability and accessibility.

Screen description:
- account section with profile, email, password
- notifications section with five toggles
- privacy section with location, analytics, ad personalization
- support section with help center and contact
- destructive delete account button at bottom
- many rows use vague labels like "Improve experience"

Constraints:
- cross-platform consumer app
- privacy-sensitive
- users may come here to quickly disable tracking or change notifications
```

## Golden output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- Visual spacing, contrast, and exact touch-target sizing cannot be verified from the description.
- The settings list is phone-first and uses standard row/toggle patterns.
- Some privacy settings may have legal copy requirements not provided here.

## Quick summary
The screen has the right major categories, but the privacy and notification controls need clearer labels, state explanation, and stronger separation from routine account maintenance. The largest risk is users not understanding what each setting changes.

## Usability issues
- Vague labels such as "Improve experience" are not decision-ready for privacy-sensitive settings.
- Five notification toggles may be scannable, but only if labels describe the notification type and outcome.
- Delete account at the bottom is appropriately separated, but it still needs confirmation, consequence preview, and recovery policy.
- Users trying to disable tracking need a direct privacy path rather than hunting through ambiguous rows.

## Accessibility issues
- Toggle rows need accessible names that include the setting meaning and current state.
- Labels should not depend on supporting fine print that may be skipped by assistive technology.
- Destructive actions need clear text, confirmation, and focus management after cancellation or completion.
- Exact visual contrast and touch targets cannot be assessed without a screenshot or spec.

## Recommended fixes
- Rename vague privacy rows with explicit outcomes, such as "Share analytics data" or "Personalized ads".
- Add one-line helper text only where the setting has non-obvious consequences.
- Group tracking-related controls together and place them before support if privacy is a common task.
- Keep destructive account deletion in its own final section with a danger-labeled row and confirmation flow.
- Provide search or anchors only if the settings list grows beyond what categories can handle.

## Design quality calibration
- Current design quality score: 3/5 from description - structurally recognizable, but label clarity and privacy decision support are not yet shippable.
- Settings quality is mostly information architecture and wording, not visual novelty.
- Good rows are self-contained: label, current state, and consequence are understandable without opening every detail screen.
- Use standard platform controls for toggles and navigation rows; custom controls add risk with little benefit here.
- Delete account should be discoverable but visually and spatially distinct from routine settings.

## Next actions
- Rewrite privacy and notification labels before visual polish.
- Define delete-account confirmation, data retention copy, and recovery behavior.
- Review with a screen reader once exact rows and controls are implemented.
```

## Design-quality notes

- Reward answers that treat settings as task routing and consent clarity.
- Penalize visual-only critique on text-only input, generic "make it cleaner" advice, or hidden destructive-action behavior.
- Strong settings calibration distinguishes toggle rows, navigation rows, helper copy, and destructive flows.
