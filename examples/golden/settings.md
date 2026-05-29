# Golden Example: Settings

This is a compact, high-quality Mode D review used for taste and structure calibration. It shows the causal Finding format, a current→projected score, and a correctly-gated Bold move on an already-competent (3/5) screen.

## Prompt

```text
Use the mobile-design-skill.

Review this iOS settings screen for usability and accessibility.

Screen description:
- grouped list: Account, Notifications, Privacy, Display, About
- each row has a label and a chevron
- some rows have current-value subtitles, some don't
- toggles for some notification options
- destructive "Delete account" at the very bottom in red
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
Solid, conventional iOS settings structure that users will navigate without friction. Main risks are an unconfirmed destructive action and inconsistent row subtitles — both fixable without restructuring. Competent today, with a clear path to strong.

## Strengths
- Grouped categorization matches iOS conventions (Jakob's Law).
- Chevrons correctly signal drill-in navigation.
- Destructive action is visually distinct.

## Findings

### F1 — Delete account likely has no confirmation
- Lens: Navigation & interaction
- Observation: "Delete account" sits at the bottom in red; no confirmation step is described.
- Violated principle: Nielsen #5 Error prevention; Nielsen #3 User control and freedom.
- User consequence: A single tap could trigger irreversible account loss with no chance to recover.
- Change: Add a confirmation sheet stating the consequence explicitly before deletion; require deliberate confirmation.
- Predicted effect: Should prevent accidental irreversible deletion; confidence M (behavior unverifiable from text).
- Severity: 4 (catastrophe) — rare action, but maximal, irreversible impact.
- Moves: Production readiness 3→4; lifts cap: P1 (destructive action without recovery).

### F2 — Destructive cue relies on color alone
- Lens: Accessibility
- Observation: The destructive action is signaled by red text only.
- Violated principle: WCAG use-of-color (color is not the only cue).
- User consequence: Color-blind users may not perceive the row as destructive.
- Change: Reinforce with an icon or an explicit "irreversible" label alongside the red.
- Predicted effect: Should make the destructive nature perceivable without relying on color; confidence M.
- Severity: 2 (minor) — affects a subset, moderate impact, persistent.
- Moves: Color/state 3→4.

### F3 — Inconsistent current-value subtitles
- Lens: Hierarchy & readability
- Observation: Some rows show a current-value subtitle, some don't.
- Violated principle: Nielsen #4 Consistency and standards; Nielsen #6 Recognition over recall.
- User consequence: Users must drill into rows just to check state, adding avoidable navigation.
- Change: Standardize current-value subtitles across all rows where a value exists.
- Predicted effect: Should reduce drill-in just to read state; confidence M.
- Severity: 2 (minor) — frequent, low-moderate impact, persistent.
- Moves: Attention path 3→4.

## Design quality score (current → projected)
- Current: 3/5 — provisional (D2 text-only). Conventional structure is sound; held below 4 by the unconfirmed destructive action and inconsistent subtitles.
- Projected after High+Medium findings: up to 4/5 — conditional: requires F1+F2+F3 to land AND a visual pass to confirm contrast. Provisional (D2): visual dimensions not raised from text.
- Ceiling note: capped at 4/5 — large-text and VoiceOver resilience unverified from the description.
- Largest single lever: F1 (lifts the destructive-action cap holding structure at 3).

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path & hierarchy | 3 | 4 | rung 3→4 (F3) | provisional |
| Color, state & contrast | 3 | 4 | rung 3→4 (F2) | not-from-text |
| Production readiness | 3 | 4 | F1 lifts P1 cap | provisional |
| Context & brand fit | 4 | 4 | iOS-conventional | provisional |
- Overall = median of projected column, lowered if a critical task dimension stays weak. Not the sum of per-dimension gains.

## Severity index
- 4 (catastrophe): F1
- 3 (major): none
- 2 (minor): F2, F3
- 1 (cosmetic): none

## Bold move (optional)
- The move: Surface the one or two most-changed settings (e.g. Notifications, Privacy) as a pinned "Frequently used" group at the top, above the standard groups.
- Deviates from: the conventional static iOS settings ordering.
- Job served (JTBD): "When I open settings, I want to reach the control I came for fast, so I can get back to the task." Outcome: minimize taps-to-reach for the most-used controls.
- UX upside: Cuts navigation cost for the common case (Hick's Law) without removing the familiar full list below.
- Risk / cost: Breaks a learned, stable location (Jakob's Law); a personalized top group can reduce spatial predictability.
- De-risk / validate: Instrument which settings are opened most; A/B the pinned group on taps-to-reach; keep the full standard list intact below; ship only if reach improves without confusion.
- Score impact: safe fixes → 4/5; this targets 5/5 on task-fit but does NOT raise the score until validated.
- Conviction: Speculative.

## Platform-convention mismatches
- None significant; structure aligns with iOS settings conventions.

## Unresolved assumptions
- Cannot verify confirmation behavior from the description.
- Cannot verify VoiceOver announcements for toggles.

## Next actions
- Add destructive confirmation, standardize subtitles, and reinforce the destructive cue beyond color.
- Verify assistive-tech labels for toggles, then confirm the projected score with a visual pass.
```

## Design-quality notes

- Reward reviews that chain each finding observation → violated principle → user consequence → change → predicted effect, instead of listing problems and fixes separately.
- Reward an honest current→projected score: the projection is conditional ("up to 4/5 IF F1+F2+F3 land"), capped at 4/5, and labeled provisional because the input is text-only.
- Reward a correctly-gated Bold move: the screen is already 3/5 with no unresolved severity-3 finding (its one severity-4 has a concrete fix), so a speculative, clearly-separated bold move is allowed — and it states what it breaks (Jakob's Law), the job it serves, and its validation path.
- Penalize visual-only critique on text-only input, generic "make it cleaner" advice, a flat fix list with no predicted effect, hidden destructive-action behavior, or a projected score asserted without conditions.
