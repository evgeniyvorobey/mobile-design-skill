# Visual Review Fixture: Fintech Dashboard Dense Summary

## Review setup

- Synthetic fixture only. No screenshots, real brands, or copied UI.
- Review evidence type: D2, text description only.
- Platform scope: Cross-platform mobile, with native navigation differences unresolved.
- User task: quickly understand current money position and choose a safe next action.

## Screen description

A personal finance dashboard summarizes checking, savings, credit card balance, monthly spending, upcoming bills, and investment movement on one home screen. The product owner wants a "premium dense summary" that fits everything above the fold.

## Frame specs

- Frame: 390 x 844 px mobile portrait.
- Top safe area assumed but not specified.
- Header height: 56 px.
- Bottom navigation: 64 px, 5 items.
- Main content scrolls vertically, but the first viewport contains 9 separate information groups.
- Primary CTA "Move money" is sticky above bottom navigation.

## Visible hierarchy

1. Total net worth card with large amount and small "as of 7:10 AM" label.
2. Three account summary cards in a horizontal carousel.
3. Monthly spending ring chart.
4. Upcoming bills list with three rows.
5. Investment movement mini chart.
6. Credit card balance warning chip.
7. Sticky "Move money" CTA.
8. Bottom navigation.

## Components

- Net worth card with amount, percentage movement, and timestamp.
- Account cards for checking, savings, credit card.
- Spending ring chart with categories.
- Bills list rows with merchant, due date, and amount.
- Investment sparkline.
- Red/green movement chips.
- Sticky primary CTA.
- Bottom navigation icons with labels.

## Typography

- Net worth amount: 32 px semibold.
- Account balances: 20 px semibold.
- Chart labels: 11 px regular.
- Bills merchant names: 14 px medium.
- Due dates and timestamps: 11 px regular.
- Bottom navigation labels: 10 px regular.
- Several rows use truncation after 16 characters.

## Color and state notes

- Positive movement is green, negative movement is red.
- Upcoming bill due today is red text only.
- Credit card warning chip uses red background with white text.
- Spending chart categories are differentiated by hue only.
- Privacy masking is available from account settings, not from this screen.
- Dark mode is planned but not described.

## Interaction states

- Default state described.
- Loading state is "show spinners in every card".
- Error state is a generic toast: "Something went wrong".
- Offline state is not described.
- Stale data state uses only the timestamp in the net worth card.
- Tapping "Move money" opens a transfer flow.
- Tapping an account card opens account detail.

## Known constraints

- Sensitive financial data can be visible in public settings.
- Users may have missing accounts, delayed bank sync, or stale investment data.
- Product wants density, but the screen must still support large text.
- The dashboard should avoid implying financial advice.

## Expected critique

- The review should identify density and hierarchy risk: 9 information groups compete before the user confirms current financial position.
- The review should flag financial clarity risk: net worth, account balances, and credit card debt need stronger semantic separation.
- The review should flag color-only semantics for positive/negative movement, due-today bills, and chart categories.
- The review should flag weak stale-data handling: timestamp alone may not be enough when bank sync or investment data is delayed.
- The review should flag sensitive-data exposure: privacy masking should be reachable from the dashboard or fast gesture/control.
- The review should flag loading/error weakness: card-level spinners and generic toast do not preserve trust or explain which data is unavailable.
- The review should recommend concrete fixes: group accounts and liabilities, expose sync freshness per group, add text/icon labels to movement, create a compact privacy toggle, define offline/stale/error cards, reduce first-viewport groups.
- The review should note at least one strength: useful high-level financial summary, direct account access, and a clear primary transfer action.

## Prohibited critique

- Do not claim exact contrast failure unless contrast values are provided.
- Do not claim regulatory compliance or non-compliance.
- Do not say the dashboard gives financial advice unless the copy explicitly does that.
- Do not claim the chart is unreadable based only on text; say the hue-only encoding creates a risk.
- Do not assert exact tap-target failure unless component dimensions are provided.
- Do not infer a specific bank, brand, or copied pattern.

## Severity expectations

- High: sensitive data exposure, stale financial data ambiguity, color-only risk for financial status, weak error recovery for account sync.
- Medium: overcrowded hierarchy, overuse of small labels, carousel hiding account comparison.
- Low: bottom navigation label size and visual polish should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected current design-quality score: 2/5.
- Reason: the screen has a useful structure, but trust, hierarchy, state handling, and color semantics are weak enough to create material financial understanding risk.
