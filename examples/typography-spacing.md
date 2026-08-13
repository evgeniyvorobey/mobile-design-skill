# Example: Create typography and spacing system

## Example prompt

```text
Use the mobile-design-skill.

Create a typography and spacing system for a cross-platform mobile banking app.

Inputs:
- Audience: broad consumer base, including older adults
- Constraints: high trust, readability-first, moderate data density, existing brand font may be applied later
- Platform: cross-platform
```

## Example output

```md
Mode: Create typography and spacing system
Platform scope: Cross-platform
Device class: Phone (compact width only; a regular-width layout can be added on request)
Assumptions:
- The product will use a neutral system-compatible font stack until brand typography is finalized.
- The primary surfaces are phone screens, with possible later adaptation to tablet.
- Financial summaries and forms are the dominant screen types.

## Type roles
- Display:
  - reserved for rare marketing or onboarding moments, not transactional screens
- Screen title:
  - primary page-level orientation
- Section title:
  - distinguishes account groups, cards, or content sections
- Body:
  - default readable text for transactional content
- Secondary body:
  - supporting context such as timestamps or descriptions
- Label:
  - field labels, tab labels, compact metadata
- Caption / helper:
  - hints, helper text, validation support
- Button / action label:
  - CTAs and secondary action text

## Size hierarchy
- Display → 28-32pt iOS / 28-32sp Android; use sparingly and only where the task is not dense
- Screen title → 24-28pt / 22-24sp; one clear level above section titles
- Section title → 17-20pt / 16-18sp; distinct from body, but not oversized
- Body → 17pt iOS / 16sp Android for readable transactional content
- Secondary body → 15pt / 14sp; one step below body, but still comfortably readable
- Label / helper → 13-14pt / 12-14sp; compact without becoming fragile at scale settings

## Weight usage
- Regular weight for most body reading
- Medium emphasis for section titles, key actions, and critical status lines
- Avoid overusing bold for routine metadata
- Reserve stronger emphasis for true priority signals such as balance totals or error headings

## Line-height guidance
- Keep body copy at 1.45-1.6 line-height for scanability on small screens.
- Use 1.25-1.35 line-height for short labels and 1.4-1.55 for paragraphs, helper text, and explanatory content.
- Do not compress line height to make dense content “fit” if it reduces comprehension.

## Spacing scale
- 4: micro spacing inside compact control groupings
- 8: close relationship between label and field, or icon and text
- 12: small group spacing inside cards and form clusters
- 16: default internal padding and common vertical rhythm
- 24: section separation
- 32: major screen-level separation
- 40: rare large separation for summary blocks or onboarding moments

## Density rules
- Use moderate default density for lists and forms.
- Increase spacing between sections more than between items inside a section.
- Dense financial content should be grouped and chunked, not merely compressed.
- When in doubt, reduce concurrent information before shrinking typography.

## Visual rhythm rules
- Quality target: 4/5 — token-ready rhythm that remains usable at larger text sizes and across dense finance screens.
- Use a 4/8-based rhythm: 8 between label and value pairs, 16 inside cards or form groups, 24 between sections, and 32 for major screen transitions.
- Keep transaction rows visually repeatable: merchant, metadata, and amount should align consistently across every row.
- Use spacing before borders: add containers only when proximity and alignment are not enough to show grouping.
- Limit a routine transactional screen to 3-4 visible type styles so hierarchy stays stable across large-text settings.

## Touch-target implications
- Action rows and tap areas should remain at least 44pt on iOS / 48dp on Android even when text scales.
- Tight vertical spacing must not collapse interactive row height below platform minimums.
- Compact labels should not create tiny control areas around segmented actions or inline links.

## Accessibility considerations
- Support text scaling without breaking hierarchy or clipping critical financial values.
- Do not rely on small caption text for essential information.
- Ensure contrast and emphasis do not depend solely on weight changes.
- Keep field labels persistent and readable, especially in forms.
- Test tabular or summary layouts with larger text before freezing component sizes.

## Usage examples
- App bar:
  - screen title + one supporting action only where necessary
- Account summary card:
  - section title, prominent balance, secondary metadata below
- Transaction list row:
  - primary merchant/body line, secondary date/category line, amount aligned consistently
- Form:
  - persistent label, input, helper/error text with clear spacing steps
- Bottom action area:
  - strong action label, generous vertical padding, clear separation from scroll content

## Next actions
- Convert roles and spacing steps into design tokens before component production starts.
- Validate the system on dense screens such as transaction detail, transfer form, and account summary.
- Test with larger text settings and error-heavy form scenarios.
```
