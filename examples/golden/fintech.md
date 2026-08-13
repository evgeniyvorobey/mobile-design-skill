# Golden Example: Fintech

## Prompt

```text
Use the mobile-design-skill.

Design a mobile screen concept for a personal investing portfolio risk summary.

Inputs:
- Platform: cross-platform
- User goal: understand whether their portfolio is overexposed before making changes
- Audience: retail investors with mixed financial literacy
- Constraints: trust-sensitive, moderate data density, avoid investment advice claims, accessible charts
```

## Golden output

```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- The screen summarizes existing holdings; it does not recommend trades.
- Risk metrics are computed by the product and have approved definitions.
- Users can drill into educational detail but should not need it to understand the top-level state.

## Screen goal
Explain current portfolio risk in plain language while preserving enough detail for users to verify where the risk comes from.

## Information hierarchy
1. Overall risk level and last-updated timestamp
2. Top contributors to risk or concentration
3. Allocation/risk breakdown with accessible labels
4. Scenario or volatility explanation
5. Educational and support links

## Recommended layout structure
- Header with Portfolio risk and timestamp.
- Summary block with risk level, plain-language interpretation, and confidence/coverage caveat if data is incomplete.
- Concentration section showing top sectors/assets and percentages.
- Chart section using labels, values, and table fallback rather than color-only wedges.
- "What this means" section with neutral education, not advice.
- Secondary actions: view holdings, learn about risk, export/share if supported.

## Behavior and states
- Show stale or partial-data warnings before the risk summary if calculations are not current.
- Let users switch between allocation by asset class, sector, and region without changing the meaning of the summary.
- Keep exact values available near charts; do not make users estimate from visuals.
- Empty state should explain that risk summary requires funded or connected holdings.
- Error state preserves last known summary if available and labels it clearly.

## Design quality calibration
- Dimension read: attention path 4, composition 3, typography 3, colour/state 3, density 3, interaction 2, context & brand fit 3, production readiness 3, distinctiveness 4. Median of the assessable = 3.
- Quality target: 3/5 - acceptable baseline concept; blocked from 4/5 by Interaction polish and motion (2), which lists feedback once for the screen rather than deciding it per action, until each action carries its own feedback and the spacing, type, and colour decisions carry stated values.
- Signature move: `type.numeral-tabular` - tabular lining numerals on every monetary and risk value. Repeated in the summary figure, the chart axis labels, and the holdings rows, so digits align vertically across all three and column scanning works without gridlines.
- Fintech trust comes from clarity, traceability, and restrained emphasis, not from dramatic red/green scoring.
- Overall risk gets the strongest hierarchy; charts are supporting evidence, not decoration.
- Use semantic color carefully and always pair it with text labels, icons, and numeric values.
- Keep educational copy short enough for mobile, with deeper explanations one tap away.
- Avoid language that tells users what to buy, sell, or change unless the product is explicitly authorized for advice.

## Accessibility and production checks
- Verify chart comprehension without color, screen reader summaries for chart data, large text, long asset names, dark mode, and stale-data messaging.
```

## Design-quality notes

- Reward answers that separate financial education from investment advice.
- Penalize overconfident claims, unlabeled charts, red/green-only risk language, or buried data freshness.
- Strong calibration includes exact values near visualizations and graceful partial-data states.
