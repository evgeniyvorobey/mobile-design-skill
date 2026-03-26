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
- Display → use sparingly and only where the task is not dense
- Screen title → one clear level above section titles
- Section title → distinct from body, but not oversized
- Body → stable default reading size across lists, forms, and details
- Secondary body → one step below body, but still comfortably readable
- Label / helper → compact without becoming fragile at scale settings

## Weight usage
- Regular weight for most body reading
- Medium emphasis for section titles, key actions, and critical status lines
- Avoid overusing bold for routine metadata
- Reserve stronger emphasis for true priority signals such as balance totals or error headings

## Line-height guidance
- Keep body copy comfortably open enough for scanability on small screens.
- Use slightly tighter line height for short labels and slightly more generous line height for paragraphs, helper text, and explanatory content.
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

## Touch-target implications
- Action rows and tap areas should remain comfortable even when text scales.
- Tight vertical spacing must not collapse interactive row height.
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
