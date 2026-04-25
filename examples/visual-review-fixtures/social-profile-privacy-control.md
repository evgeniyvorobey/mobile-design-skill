# Visual Review Fixture: Social Profile Privacy / Control

## Review setup

- Synthetic fixture only. No screenshots, real brands, or copied UI.
- Review evidence type: D2, text description only.
- Platform scope: Cross-platform mobile social app.
- User task: understand how the profile appears to others and control visibility, contact discovery, and blocked-user settings.

## Screen description

A profile settings screen combines public profile preview, audience controls, contact sync, blocked users, and account visibility in one page. Product wants fewer screens and a friendly tone.

## Frame specs

- Frame: 390 x 844 px mobile portrait.
- Header: "Profile settings" with back button.
- Content: vertically scrollable list of grouped settings.
- Profile preview card: avatar, display name, bio, and public badge.
- Settings rows: Account visibility, Show activity status, Contact discovery, Sync contacts, Blocked users, Muted words.
- Footer: "Deactivate account" link.

## Visible hierarchy

1. Profile preview card.
2. Account visibility row.
3. Contact discovery row.
4. Sync contacts toggle.
5. Show activity status toggle.
6. Blocked users row.
7. Muted words row.
8. Deactivate account link.

## Components

- Profile preview card.
- Setting rows with labels, helper copy, and chevrons.
- Toggle switches.
- Audience selector row.
- Destructive footer link.
- Confirmation sheet for deactivation.
- No inline "view as public" mode is described.

## Typography

- Screen title: 20 px semibold.
- Setting labels: 16 px regular.
- Helper copy: 12 px regular.
- Preview name: 18 px semibold.
- Preview bio: 13 px regular.
- Destructive link: 14 px regular.

## Color and state notes

- Public badge is blue.
- Private state uses a lock icon and gray text.
- Contact sync toggle is on by default for new users.
- Destructive link uses red text.
- Disabled states are not described.
- The preview card does not change live when toggles change.

## Interaction states

- Default state described.
- Toggle on/off states exist.
- Deactivation confirmation sheet exists.
- Unsaved-change state is not described.
- Permission-denied state for contacts is not described.
- Contact sync failure state is not described.
- Blocked-user empty state is not described.

## Known constraints

- Privacy language must be understandable to non-technical users.
- Users need to distinguish who can see profile content, activity status, and contact discovery.
- Contact sync may require OS permission.
- Some users may be minors or in sensitive situations, but the fixture does not provide age or safety policy.
- The review must not claim legal compliance.

## Expected critique

- The review should flag privacy model ambiguity: Account visibility, Contact discovery, Sync contacts, and Activity status are related but not clearly separated by audience and data type.
- The review should flag default-on contact sync as high risk unless the product has a clearly explained consent step.
- The review should flag missing public preview behavior: users need to see what changes when visibility settings change.
- The review should flag destructive action placement: Deactivate account should not be a low-context footer link without account consequence summary.
- The review should flag missing permission and failure states for contact sync.
- The review should recommend concrete fixes: split settings into "Who can see me", "How people find me", and "Account controls"; add live preview or "View as public"; make contact sync explicit opt-in; add OS permission denied path; add consequence summary and cooling-off copy for deactivation.
- The review should note strengths: grouped settings, helper copy, lock icon, and confirmation sheet are useful foundations.

## Prohibited critique

- Do not claim GDPR, COPPA, DSA, or privacy-law compliance or non-compliance.
- Do not claim the design is unsafe for minors without policy context.
- Do not infer abusive-use scenarios as facts; frame sensitive-situation concerns as risk.
- Do not claim exact visual contrast failure for red/gray text without values.
- Do not assert that toggles are too small unless dimensions are provided.
- Do not invent platform permission copy.

## Severity expectations

- High: default-on contact sync without explicit consent context, privacy model ambiguity, destructive account action with weak consequence summary.
- Medium: preview not updating, missing contact permission/failure states, blocked-user empty state missing.
- Low: exact tone, spacing, and red-link visual weight should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected current design-quality score: 2/5.
- Reason: the screen has a useful settings inventory, but privacy comprehension, consent clarity, and destructive-action safeguards are not strong enough.
