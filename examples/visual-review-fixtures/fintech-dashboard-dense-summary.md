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

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform mobile
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- This is a phone-first home screen, 390 x 844 px.
- Privacy masking exists only in account settings, not on this screen.
- Dark mode is planned but undescribed, so it is out of scope for evidence.

## Quick summary
The dashboard packs a useful financial overview into one screen, but it is structurally overloaded and trust-fragile: nine information groups compete in the first viewport, account assets and credit-card debt are not semantically separated, status meaning rides on color alone, stale-data and error handling are thin, and sensitive balances cannot be masked from here. Current quality is low for a money-status surface. The structural fixes below have a clear path to a stronger score, but visual properties cannot be confirmed from text.

## Strengths
- Provides a genuinely useful high-level financial summary in one place.
- Gives direct access to each account via tappable account cards.
- Offers a clear primary action ("Move money") for the most common next step.

## Findings

### F1 — Sensitive balances cannot be hidden from the dashboard
- Lens: Usability
- Observation: Privacy masking is reachable only from account settings; the dashboard itself exposes net worth and balances with no on-screen control, and the screen may be used in public.
- Violated principle: Nielsen #3 User control and freedom; Nielsen #7 Flexibility and efficiency (fast access to a frequent need).
- User consequence: Users in public settings cannot quickly hide financial data, exposing sensitive amounts to shoulder-surfing and eroding trust in the product.
- Change: Add a compact privacy toggle (or quick gesture) on the dashboard that masks amounts in place and persists per session.
- Predicted effect: Should reduce unwanted exposure of sensitive amounts; confidence M (D2 text-only — structural inference, not measured).
- Severity: 3 (major) — frequent (any public use), high impact (sensitive data), persistent (every visit until masked).
- Moves: Production readiness 2→3; lifts cap: trust gap on sensitive-data exposure.

### F2 — Stale financial data is signaled only by a timestamp
- Lens: Usability
- Observation: Stale data state relies on the single "as of 7:10 AM" timestamp in the net worth card; bank sync or investment data may be delayed without per-group freshness.
- Violated principle: Nielsen #1 Visibility of system status.
- User consequence: Users may act on out-of-date balances (e.g. move money against a stale figure) because freshness is neither per-group nor prominent.
- Change: Expose sync freshness per data group; surface a clear "data may be delayed" state when sync is behind, distinct from normal.
- Predicted effect: Should reduce decisions made on stale balances; confidence M (D2 text-only).
- Severity: 3 (major) — occasional but high impact (financial decisions), persistent across sync delays.
- Moves: Production readiness 2→3; lifts cap: stale-data ambiguity.

### F3 — Status meaning carried by color alone
- Lens: Accessibility
- Observation: Positive/negative movement is green/red, the due-today bill is red text only, and spending-chart categories are differentiated by hue only.
- Violated principle: WCAG use-of-color (1.4.1) — do not use color as the only means of conveying information.
- User consequence: Users with color-vision differences or in low-light/glare may miss gains/losses, an urgent due-today bill, or which spending category is which.
- Change: Pair movement with a sign/arrow + text, label the due-today bill with text/icon, and add labels or patterns to chart categories — do not rely on hue alone.
- Predicted effect: Should reduce misread financial status under color-vision or glare conditions; confidence M (cannot verify rendering from text).
- Severity: 3 (major) — frequent, high impact (financial status), persistent.
- Moves: Production readiness 2→3; lifts cap: color-only status risk.

### F4 — Weak loading and error recovery
- Lens: Usability
- Observation: Loading shows spinners in every card; the error state is a single generic toast ("Something went wrong"); offline is undescribed.
- Violated principle: Nielsen #1 Visibility of system status; Nielsen #9 Help users recognize, diagnose, and recover from errors.
- User consequence: All-card spinners hide which data is actually unavailable, and a generic toast neither explains the failure nor preserves trust in the rest of the screen.
- Change: Use per-group loading/error/offline cards that name which data is unavailable and offer retry; preserve last-known values where safe.
- Predicted effect: Should improve recovery and preserve trust during partial failures; confidence M (D2 text-only).
- Severity: 3 (major) — occasional but high impact, persistent until states are defined.
- Moves: Production readiness 2→3; Interaction polish 2→3.

### F5 — Overcrowded first viewport
- Lens: Hierarchy & readability
- Observation: The first viewport contains nine separate information groups (net worth, three account cards, spending ring, bills, investment chart, credit warning chip, sticky CTA) competing before the user confirms current position.
- Violated principle: Cognitive load (extraneous); Hick's Law (too many competing targets); Gestalt proximity / common region.
- User consequence: The user must scan many competing groups to answer "where do I stand," raising effort and slowing the core task.
- Change: Reduce first-viewport groups; lead with current position, then progressively reveal detail; group accounts (assets) separately from liabilities (credit card debt).
- Predicted effect: Should reduce scanning effort to confirm financial position; confidence M (perceived density not measurable from text).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path & hierarchy 2→3.

### F6 — Assets and liabilities not semantically separated
- Lens: Hierarchy & readability
- Observation: Net worth, account balances, and credit-card debt share the same card treatment without strong separation between what the user owns and what the user owes.
- Violated principle: Gestalt common region; Cognitive load (extraneous).
- User consequence: Users may misread their true position when assets and debt are visually interchangeable, weakening financial clarity.
- Change: Visually and structurally separate assets from liabilities (distinct grouping/section), and make the credit-card balance read as a liability, not another account.
- Predicted effect: Should reduce misreading of net position; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path & hierarchy 2→3.

### F7 — Small labels and over-truncation
- Lens: Hierarchy & readability
- Observation: Several roles sit at 10-11 px (chart labels, due dates/timestamps, bottom-nav labels) and some rows truncate after 16 characters; the screen must still support large text.
- Violated principle: Cognitive load (extraneous); legibility/readability under text scaling.
- User consequence: Small labels and aggressive truncation can hide merchant names and metadata, especially at larger text sizes, harming scanning.
- Change: Raise minimum label sizes, allow wrapping or progressive disclosure instead of hard truncation, and verify behavior at large text settings.
- Predicted effect: Should improve label legibility and reduce truncation loss at large text; confidence L (exact sizes/contrast not verifiable from text).
- Severity: 1 (cosmetic) — frequent, low-to-moderate impact, persistent; keep qualified (no screenshot).
- Moves: Typography craft 3→4 — the fix names the behaviour when text scales up, which the six stated roles currently lack; rendered legibility at those sizes still needs a screenshot.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {1, 1, 2, 2, 2, 3}; pinned by sensitive-data exposure (F1), stale-data ambiguity (F2), and color-only status (F3).
- Projected: 3/5 — median of the assessable projected bands {1, 3, 3, 3, 4, 4} once F1+F2+F3+F4 land (plus F5/F6/F7); held there by the inert Distinctiveness band no finding lifts.
- Ceiling note: with a visual pass confirming contrast, spacing, and large-text behavior the leading bands hold at 4, but the inert-screen cap holds the artifact at 3/5 until the dashboard carries one owned asset (dark mode and color-vision rendering are still unverified from the description).
- Primary lever(s): F1 + F2 + F3 (the trust trio that pins a money-status surface at 2).

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path & hierarchy | 2 | 3 | F5/F6 grouping (rung 2→3) | provisional |
| Production readiness | 2 | 4 | F1/F2/F3/F4 lift trust caps | provisional |
| Interaction polish & motion | 2 | 3 | F4 states (rung 2→3) | provisional |
| Color, state & contrast | 1 | 3 | movement, due-today and chart categories ride on hue alone (F3); 3→4 needs stated pairs and the dark theme the fixture leaves undescribed | provisional |
| Typography craft | 3 | 4 | six roles carry stated sizes; F7 supplies the large-text behaviour they lack (rung 3→4) | provisional |
| Distinctiveness & owned assets | 1 | 1 | inert — "premium dense summary" is an adjective, not an owned asset, and no finding adds one | provisional |
- Projected overall = median of the assessable projected dimensions {3, 4, 3, 3, 4, 1} = 3. Not the sum of per-dimension gains; colour stops at 3 because a description states no pair and dark mode is undescribed, and that rung is never projected upward from text.

## Severity index
- 4 (catastrophe): none
- 3 (major): F1, F2, F3, F4
- 2 (minor): F5, F6
- 1 (cosmetic): F7

## Platform-convention mismatches
- Cross-platform caution: the sticky "Move money" CTA and bottom navigation must respect each platform's safe-area and navigation conventions rather than behaving like a web layout dropped into a phone.
- Privacy masking and quick controls should follow platform-idiomatic patterns (e.g. gesture vs. control) per OS rather than a single forced pattern.

## Unresolved assumptions
- Cannot verify contrast ratios, exact spacing, or visual weight from text.
- Cannot verify chart readability; the hue-only encoding is a stated risk, not a measured failure.
- Cannot verify tap-target sizes from the description.
- Cannot verify large-text or dark-mode resilience from text alone.

## Next actions
- Add an on-dashboard privacy toggle and per-group sync-freshness state before polishing visuals.
- Separate assets from liabilities, reduce first-viewport groups, and add non-color status cues.
- Run a visual pass with large text, color-vision simulation, and partial-failure scenarios to confirm the projected score.
```

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

Severity uses the Nielsen 0-4 scale (High maps to 3, or 4 if irreversible/catastrophic; Medium to 2; Low to 1).

- 3 (major): sensitive data exposure, stale financial data ambiguity, color-only risk for financial status, weak error recovery for account sync.
- 2 (minor): overcrowded hierarchy, assets/liabilities not separated, carousel hiding account comparison.
- 1 (cosmetic): bottom-navigation label size, small labels, and visual polish should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected score: current 2/5 → projected 3/5 (flat median of the assessable dimensions, conditional, provisional D2).
- Reason for current: the screen has a useful structure and decided type roles, but trust, hierarchy, state handling, and hue-only color semantics are weak enough to create material financial understanding risk.
- Reason for projected: landing the major findings (privacy toggle, per-group freshness, non-color status, per-group error states) plus the grouping and text-scaling fixes lift production readiness and typography to 4 — but the dashboard owns no asset, so the inert-screen cap holds the artifact at 3/5, and contrast, spacing, and large-text rendering cannot be raised from a text-only description.
- No Bold move is expected: the screen has unresolved severity-3 findings, so the Bold move trigger is not met.
