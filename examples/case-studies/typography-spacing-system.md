# Synthetic Case Study: Typography And Spacing System

## Prompt

```text
Use the mobile-design-skill.

Create a typography and spacing system for a mobile fitness tracker.

Inputs:
- Platform: iOS and Android
- Product: consumer fitness tracker
- Screens: workout summary, activity feed, settings, workout setup
- Constraints: glanceable metrics, accessible large text, dark mode, compact but not cramped
```

## Weak response

```md
Mode: Create typography and spacing system
Platform scope: iOS and Android
Assumptions:
- Fitness apps need clear metrics.
- The system should feel modern.

Use 32 for big metrics, 24 for headings, 16 for body, 14 for captions, and 12 for small labels. Use medium weight for important text. Use 8, 16, 24, and 32 spacing. Cards should have 16 padding and rounded corners. Make buttons at least 44/48 high.

Accessibility considerations: support dynamic type and high contrast.
Next actions: apply to screens and test.
```

## Why this is weak

- Provides a size list but not role semantics or usage rules.
- Does not explain metric numerals, units, truncation, large text, or dense screens.
- Spacing tokens are generic and not tied to rhythm or component states.
- Platform differences are only implied by touch target numbers.
- Dark mode and contrast are mentioned without mechanisms.

## Strong response

```md
Mode: Create typography and spacing system
Platform scope: iOS and Android
Assumptions:
- Use platform system fonts unless the product has an approved brand typeface.
- Metrics such as pace, heart rate, distance, and duration are product-provided; this system only defines presentation.
- Screens need both glanceable workout data and denser settings/feed rows.

## Type roles
- Metric hero: primary workout value, one per screen zone.
- Metric unit: unit attached to metric hero, never separated visually or semantically.
- Title: screen and section titles.
- Body: explanatory and row text.
- Label: field labels, metric labels, and compact metadata.
- Caption: timestamps and secondary helper text.

## Size hierarchy
- Metric hero: 40-48 pt/sp, line-height 1.05-1.15, tabular numerals where available.
- Title: 22-28 pt/sp, line-height 1.2-1.3.
- Section title: 17-20 pt/sp, line-height 1.25-1.35.
- Body: 15-17 pt/sp, line-height 1.45-1.55.
- Label: 13-15 pt/sp, line-height 1.3-1.45.
- Caption: 12-13 pt/sp, line-height 1.35-1.5; avoid using for critical health or workout status.

## Weight usage
- Metric hero: semibold or platform equivalent; avoid ultra-bold for long numbers.
- Labels: medium only when paired with values.
- Body: regular; use weight changes sparingly so metrics keep priority.

## Line-height guidance
- Glanceable metric groups use tighter line-height but more external spacing.
- Body/helper text uses looser line-height to remain readable in dark mode and large text.
- Never place multiline helper copy in a metric grid cell without allowing the cell to expand.

## Spacing scale
- Base token scale: 4, 8, 12, 16, 20, 24, 32, 40.
- Screen padding: 16 compact, 20 standard, 24 for high-trust or explanation-heavy settings.
- Metric group internal gap: 4-8 between label, value, unit; 16-24 between groups.
- Section gap: 24 standard; 32 after major summary modules.
- Row height: 48 minimum; 56-64 for settings rows with helper text.

## Density rules
- Workout summary: sparse, hero metric plus 2-4 secondary metrics.
- Activity feed: medium density; repeated rows must align timestamps and values.
- Settings: medium, grouped sections, helper text only where consequence changes.
- Workout setup: roomy controls and clear thumb-zone primary action.

## Visual rhythm rules
- Align metric baselines within a row.
- Units stay adjacent to values and use smaller role, not separate columns.
- Repeat label-value rhythm across workout summary and feed so users can compare quickly.
- Use dividers or spacing, not nested cards, for dense repeated rows.

## Touch-target implications
- iOS controls at least 44 pt; Android controls at least 48 dp.
- Fitness setup and during-workout controls should exceed minimums when used in motion.
- Tap targets can be larger than visible icons.

## Accessibility considerations
- Dynamic Type / font scaling may stack metric grids into a single column.
- Do not encode heart-rate zones by color alone; pair with text and icon/pattern.
- Critical workout status uses body or label roles, not caption-only text.
- Dark mode requires semantic colors and verified contrast during implementation.

## Usage examples for common screen areas
- Workout summary: Metric hero for distance, label for "Distance", body for interpretation, caption for timestamp.
- Activity feed row: title for workout type, label for duration/distance, caption for sync state if not critical.
- Settings row: body label, optional helper text, platform switch or disclosure.

## Next actions
- Map these roles to design tokens and platform text styles.
- QA large text, long units/locales, dark mode, in-motion tapping, and metric grid wrapping.
```

## Why this is stronger

- Quality target: 4/5 - strong once brand typeface, localization, and platform token mappings are confirmed.
- Defines roles and behavior, not just sizes.
- Connects typography to fitness-specific metrics and units.
- Gives token-ready spacing and density rules.
- Covers platform touch targets and in-motion use.
- Handles large text and dark mode with mechanisms.

## Regression checks

- Does the system define type roles before sizes?
- Does it keep metric units attached to values?
- Does it provide density rules per screen type?
- Does it include wrapping behavior for large text?
- Does it avoid caption-only critical status?
