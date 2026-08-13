# Golden Example: Settings

This is a compact, high-quality Mode D review used for taste and structure calibration. It shows the causal Finding format (including a compressed cosmetic finding), an honest current→projected score that does NOT inflate, the inert-screen test producing a finding, and a correctly-gated Bold move on a competent-but-inert (3/5) screen with no unresolved severity-3/4.

## Prompt

```text
Use the mobile-design-skill.

Review this iOS settings screen for usability and accessibility.

Screen description:
- grouped list: Account, Notifications, Privacy, Display, About
- each row has a label and a chevron
- some rows have current-value subtitles, some don't
- toggles for some notification options
- destructive "Delete account" at the very bottom in red, opening a confirmation sheet that states the consequence
```

## Golden output

```md
Mode: Review screen for usability/accessibility
Platform scope: iOS
Sub-case: D2 description only
Assumptions:
- Standard iOS grouped table view.
- No search field in settings.

## Quick summary
A sound, conventional iOS settings screen: the structure is correct and the destructive action is already confirmed, so there is no major risk here. The real ceiling is that it is competent but inert — indistinguishable from any other settings screen. The fixes below are minor; the larger opportunity is a deliberate point of view, captured as a Bold move.

## Strengths
- Grouped categorization matches iOS conventions (Jakob's Law).
- Chevrons correctly signal drill-in navigation.
- The destructive action already opens a confirmation sheet — error prevention is handled.

## Findings

### F1 — Destructive cue relies on color alone
- Lens: Accessibility
- Observation: The Delete account row is signaled by red text only (the confirmation sheet aside).
- Violated principle: WCAG use-of-color (color is not the only cue).
- User consequence: Color-blind users may not perceive the row as destructive before tapping into the sheet.
- Change: Reinforce with an icon or an explicit "irreversible" label alongside the red.
- Predicted effect: Should make the destructive nature perceivable without relying on color; confidence M (rendering unverifiable from text).
- Severity: 2 (minor) — affects a subset, moderate impact, persistent.
- Moves: Color, state & contrast 1→3 — the fix supplies the missing second cue; the stated pair and its dark-theme value stay out of reach of a description, so the band stops at 3.

### F2 — Inconsistent current-value subtitles
- Lens: Hierarchy & readability
- Observation: Some rows show a current-value subtitle, some don't.
- Violated principle: Nielsen #4 Consistency and standards; Nielsen #6 Recognition over recall.
- User consequence: Users must drill into rows just to check state, adding avoidable navigation.
- Change: Standardize current-value subtitles across all rows where a value exists.
- Predicted effect: Should reduce drill-in just to read state; confidence M.
- Severity: 2 (minor) — frequent, low-moderate impact, persistent.
- Moves: Attention path & hierarchy 3→4.

### F3 — Screen is competent but inert (compressed)
- Observation: Strip the wordmark and brand color and this is indistinguishable from any iOS settings screen — zero owned distinctive assets (inert-screen test).
- Change: Give the screen one ownable, low-risk distinctive moment — see Bold move; do not add decoration to functional rows.
- Severity: 1 (cosmetic) — costs a quality point (Context & brand fit caps at 3), not a task failure.

## Design quality score (current → projected)
- Current: 3/5 — median of the assessable Now bands {1, 1, 3, 3, 3}; conventional and correct, but inert and reliant on colour alone for the one destructive row.
- Projected: 3/5 — median of the assessable projected bands {1, 3, 3, 3, 4} after F1+F2 land; the minor fixes remove friction without adding a point of view, so the overall does not move.
- Ceiling note: with a visual pass confirming contrast and large-text behavior the dimension bands reach 4, but the inert-screen cap holds the artifact at 3/5 until the screen carries one owned asset — the Bold move, once validated, is that asset.
- Primary lever(s): F2 lifts hierarchy; the score is otherwise gated by inertness (F3), which the safe fixes do not address.

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path & hierarchy | 3 | 4 | rung 3→4 (F2) | provisional |
| Production readiness | 3 | 3 | confirmation already present; no open cap | provisional |
| Context & brand fit | 3 | 3 | inert (F3); not lifted by safe fixes | provisional |
| Color, state & contrast | 1 | 3 | destructive row is red-only, so the second-cue test fails (F1); 3→4 needs stated pairs and their dark-theme values | provisional |
| Distinctiveness & owned assets | 1 | 1 | inert (F3); the Bold move is the only candidate asset and it is not banked until validated | provisional |
- Projected overall = median of the assessable projected dimensions {4, 3, 3, 3, 1} = 3. Not the sum of per-dimension gains; colour stops at 3 because a description cannot state a pair or its dark-theme value, and that rung is never projected upward from text.

## Severity index
- 4 (catastrophe): none
- 3 (major): none
- 2 (minor): F1, F2
- 1 (cosmetic): F3

## Bold move (optional)
- The move: Surface the one or two most-changed settings (e.g. Notifications, Privacy) as a pinned "Frequently used" group at the top, above the standard groups.
- Deviates from: the conventional static iOS settings ordering.
- Job served (JTBD): "When I open settings, I want to reach the control I came for fast, so I can get back to the task." Outcome: minimize taps-to-reach for the most-used controls.
- UX upside: Cuts navigation cost for the common case (Hick's Law) without removing the familiar full list below; gives the screen a reason to exist beyond the default.
- Risk / cost: Breaks a learned, stable location (Jakob's Law); a personalized top group can reduce spatial predictability.
- De-risk / validate: Instrument which settings are opened most; A/B the pinned group on taps-to-reach; keep the full standard list intact below; ship only if reach improves without confusion.
- Score impact: safe fixes leave it at 3/5; this targets a distinctive 4/5 on Context & brand fit but does NOT raise the score until validated.
- Conviction: Speculative.

## Platform-convention mismatches
- None significant; structure aligns with iOS settings conventions.

## Unresolved assumptions
- Cannot verify the confirmation sheet's copy or VoiceOver announcements from the description.
- Cannot verify contrast or large-text rendering.

## Next actions
- Standardize subtitles and reinforce the destructive cue beyond color.
- Validate the "Frequently used" group against taps-to-reach before committing; confirm the 4/5 ceiling with a visual pass.
```

## Design-quality notes

- Reward reviews that chain each finding observation → violated principle → user consequence → change → predicted effect, and that use the compressed form (Observation → Change → Severity) for a cosmetic finding (F3) instead of padding it to eight fields.
- Reward an honest current→projected score that does NOT inflate: here the projection stays 3/5 because the minor fixes don't add a point of view, with the 4/5 ceiling confined to a `Ceiling note`. A projection that equals the current score is correct when the fixes are minor — the value lives in the ceiling and the Bold move.
- Reward the inert-screen test producing a real finding (F3) and gating `Context & brand fit`, then motivating the Bold move — the distinctiveness lever doing actual work in Mode D.
- Reward a correctly-gated Bold move: the screen is competent (3/5) with NO unresolved severity-3/4 finding (the destructive action is already confirmed), so a speculative, clearly-separated bold move is allowed — it names what it breaks (Jakob's Law), the job it serves, and a validation path, and it does not bank the score.
- Penalize visual-only critique on text-only input, numerically projecting a rendered property upward from text (Color/state may reach band 3 on decided roles, but never band 4, because a description states no foreground/background pair and no dark-theme value), a flat fix list with no predicted effect, an inflated "up to 4/5" projection, or a Bold move offered over an unresolved catastrophe.
