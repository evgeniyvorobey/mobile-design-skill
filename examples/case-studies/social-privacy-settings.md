# Synthetic Case Study: Social Privacy Settings

## Prompt

```text
Use the mobile-design-skill.

Review and improve a social app privacy settings screen from this description:
- The screen is a long list of toggles.
- Toggles include public profile, activity status, read receipts, discoverability, blocked users, and delete account.
- There is no preview of who can see what.
- Platform is unspecified.
```

## Weak response

```md
Mode: Review screen for usability/accessibility
Platform scope: Assumed cross-platform
Assumptions:
- This is a mobile social app.
- Users want control over privacy.

The screen should be cleaner and less cluttered. Group toggles into cards, use icons, and make the delete account button red at the bottom. Add a short description under each toggle and maybe a profile preview. Make sure the colors have contrast and the toggles are accessible.

Next actions: redesign the screen and test privacy understanding.
```

## Why this is weak

- Makes visual claims from a text-only description without qualifying uncertainty.
- Does not distinguish privacy visibility, interaction signals, discoverability, safety, and destructive actions.
- Treats delete account as just a red button placement problem.
- "Maybe a profile preview" is not specified as a mechanism.
- Accessibility and severity are generic.

## Strong response

```md
Mode: Review screen for usability/accessibility
Platform scope: Assumed cross-platform because platform is unspecified
Assumptions:
- This is a description-only review, so visual spacing, contrast, and exact tap sizes cannot be verified.
- The settings affect other users' ability to see or contact the account owner.
- Delete account is destructive and should not sit among reversible privacy toggles.

## Quick summary
The current structure is likely understandable at the row level but weak at privacy comprehension. Users need grouped mental models, audience previews, and stronger separation between reversible privacy choices and destructive account actions.

## Strengths
- The described settings cover important privacy controls.
- Toggle rows can be efficient for reversible binary settings if labels and consequences are clear.

## Usability issues
- High: unrelated toggles in one long list force users to infer consequences.
- High: no audience preview means users cannot verify "who sees what" before changing settings.
- Medium: discoverability, activity, and read receipts have different mental models but appear as equivalent toggles.

## Accessibility issues
- Toggle labels must include current state and consequence, not only setting name.
- Screen reader order should read group name, setting, state, and effect.
- Privacy warnings cannot rely on color alone.

## Hierarchy and readability issues
- Group settings into: Profile visibility, Interaction signals, Findability, Safety, Account actions.
- Put blocked users under Safety, not near public-profile controls.
- Keep Delete account in a separate Account actions section with destructive treatment and explanation.

## Design quality issues
- Description-only evidence limits visual scoring; structural quality is currently around 2/5.
- A stronger design would expose consequences before change, not after error or confusion.

## Navigation and interaction issues
- Use detail rows for complex settings such as discoverability instead of a single toggle if multiple channels are affected.
- Provide a "View as..." or audience preview for profile visibility.
- For delete account, require a dedicated flow with data export/recovery information if product policy supports it.

## Severity or priority
- High: no audience preview for visibility settings.
- High: destructive delete action appears in the same control pattern as reversible toggles.
- Medium: long ungrouped list reduces scanning and confidence.

## Recommended fixes
- Add grouped sections with plain-language descriptions.
- Replace ambiguous toggles with detail screens where the consequence has multiple parts.
- Add preview states: public, followers, mutuals, nobody, or product-approved equivalents.
- Separate Delete account into a destructive flow with confirmation and clear irreversibility/recovery boundaries.

## Unresolved assumptions
- Exact visual density, contrast, tap target size, and platform component choice require screenshot or design file.
- Legal retention and account recovery policy are not provided.

## Next actions
- Define the audience model for each setting and map every toggle to a visible consequence.
- QA screen reader labels, large text, privacy preview accuracy, blocked-users navigation, and delete-account confirmation.
```

## Why this is stronger

- Quality target: 4/5 - strong once audience taxonomy, retention policy, and moderation routes are confirmed.
- Qualifies visual uncertainty from text-only input.
- Moves from "cleaner list" to privacy comprehension mechanisms.
- Separates reversible settings from destructive account actions.
- Includes severity, actual strengths, and actionable fixes.
- Avoids claiming legal or accessibility compliance.

## Regression checks

- Does the review classify evidence limits for description-only input?
- Does it include at least one real strength?
- Does it separate audience visibility from safety and account actions?
- Does it avoid visual overclaim about spacing or contrast?
- Does it define concrete privacy preview behavior?
