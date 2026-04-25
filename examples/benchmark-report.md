# Benchmark Report Example

This example is synthetic. It uses placeholder references and generic descriptions only; it does not copy real brands, screenshots, layouts, or proprietary product UI.

## Prompt

```text
Use the mobile-design-skill.

Create a benchmark report for a cross-platform mobile fitness tracker home screen.

Product context:
- Audience: busy adults who track workouts, sleep, and daily recovery
- Goal: make the home screen feel premium, calm, and actionable
- Constraints: avoid medical claims, support large text, include empty and stale-data states

References:
1. Source: Production UI placeholder
   Name: Calm activity dashboard
   Link: unavailable - synthetic written reference
   Why relevant: good hierarchy between today's status, trend cards, and primary action
   Known limitations: unknown accessibility and no error states shown

2. Source: Flow reference placeholder
   Name: First-week fitness onboarding
   Link: unavailable - synthetic written reference
   Why relevant: shows progressive setup and how connected-device prompts are timed
   Known limitations: onboarding only; does not prove dashboard density or long-term retention

3. Source: Portfolio concept placeholder
   Name: Premium recovery visual system
   Link: unavailable - synthetic written reference
   Why relevant: useful for restrained color, soft data visualization, and calm tone
   Known limitations: concept-only; may ignore platform behavior, real data, and accessibility
```

## Report output

```md
## Context
- Product/task: Cross-platform fitness tracker home screen for workout, sleep, and recovery tracking.
- Platform: iOS and Android.
- Audience: Busy adults who need a quick read and one clear next action.
- Design goal: Premium, calm, actionable, and trustworthy without medical positioning.
- Constraints: Avoid medical claims, support large text, show empty and stale-data states.
- What references are allowed to influence: hierarchy, visual density, card rhythm, tone, and setup timing.
- What references cannot decide: health accuracy, accessibility compliance, platform behavior, or whether the flow improves retention.

## References table
| # | Source | Name | Link | Why relevant | Known limitations |
| --- | --- | --- | --- | --- | --- |
| 1 | Production UI placeholder | Calm activity dashboard | Unavailable - synthetic written reference | Calibrates hierarchy between today's status, trend cards, and primary action | Unknown accessibility and no error states shown |
| 2 | Flow reference placeholder | First-week fitness onboarding | Unavailable - synthetic written reference | Calibrates progressive setup and connected-device prompt timing | Onboarding only; not evidence for dashboard density or retention |
| 3 | Portfolio concept placeholder | Premium recovery visual system | Unavailable - synthetic written reference | Calibrates restrained color, soft data visualization, and calm tone | Concept-only; may ignore platform behavior, real data, and accessibility |

## Borrow
- Use a single top status summary that answers "How am I doing today?" before showing detailed cards.
- Use calm trend cards with short labels, exact values, and one-line interpretation.
- Time connected-device prompts after the user sees value; make setup a secondary card unless data is required.
- Use restrained color as emphasis for state, not decoration.

## Do not copy
- Do not copy the exact dashboard composition from the production placeholder; adapt to this product's three data types: workout, sleep, and recovery.
- Do not copy portfolio-style low-contrast charts; premium cannot come at the cost of readability.
- Do not copy onboarding prompt timing if the user has no connected device or has already dismissed setup.
- Do not use medical-sounding recovery language such as "diagnosis", "risk", or "normal range".

## Translate to tokens/components/states
- Tokens: neutral background, one primary accent, semantic status colors paired with text, 8-point spacing rhythm, type roles for status, metric, label, and caption.
- Components: Today summary, primary action button, metric trend card, setup prompt card, stale-data banner, compact weekly trend, device connection row.
- States: no data, partial data, stale wearable sync, permission denied, device disconnected, loading, error with last known values, large-text layout.
- Motion/interaction: short value-change transitions only after data refresh; no decorative looping motion on the home screen.
- Content rules: phrase recovery as educational wellness feedback, not medical advice; keep all status labels explainable in one tap.
- QA checks: large text, dark mode, chart comprehension without color, tap targets, stale timestamp visibility, long localized labels.

## Evidence boundaries
- Inspiration only: visual calmness, density range, card grouping, setup timing ideas.
- Evidence needed elsewhere: user comprehension, retention effect, health copy approval, and wearable-sync reliability.
- Platform/accessibility checks: native navigation, dynamic type/font scaling, minimum touch targets, contrast, screen reader order.
- Compliance or domain checks: avoid medical claims and clarify that scores are wellness estimates based on available data.

## Risks
- Design risk: Premium styling may become too quiet, hiding the primary action.
- Product risk: Users may over-trust recovery score if uncertainty and data freshness are not visible.
- Accessibility risk: Soft charts and low contrast can fail readability.
- Implementation risk: Combining wearable sync, permissions, and stale data creates many edge states.
- Research gap: Need to validate whether users understand the relationship between workouts, sleep, and recovery.

## Next actions
- Immediate design decision: Choose one top-level daily status model and define its copy boundaries.
- Prototype or spec task: Create the home screen with Today summary, three trend cards, stale-data banner, and setup prompt variants.
- Validation task: Run comprehension review on recovery wording and chart labels.
- Open question: Should the primary action be "Start workout", "Log activity", or context-aware based on the user's latest state?
```
