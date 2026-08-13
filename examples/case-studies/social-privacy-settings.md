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
- Lists problems and fixes loosely with no causal chain, no severity, and no predicted effect.

## Strong response

```md
Mode: Review screen for usability/accessibility
Platform scope: Assumed cross-platform because platform is unspecified
Sub-case: D2 description only
Assumptions:
- This is a description-only review, so visual spacing, contrast, and exact tap sizes cannot be verified.
- The settings affect other users' ability to see or contact the account owner.
- Delete account is destructive and should not sit among reversible privacy toggles.

## Quick summary
The current structure is likely understandable at the row level but weak at privacy comprehension: users cannot verify "who sees what," and an irreversible delete sits inside the same toggle pattern as reversible choices. Current quality is low for a privacy surface, but the structural fixes below have a clear path to a stronger score.

## Strengths
- The described settings cover important privacy controls.
- Toggle rows can be efficient for reversible binary settings when labels and consequences are clear.

## Findings

### F1 — No audience preview for visibility settings
- Lens: Usability
- Observation: There is no preview of who can see what; visibility settings are bare toggles.
- Violated principle: Nielsen #1 Visibility of system status; Nielsen #2 Match between system and the real world.
- User consequence: Users change visibility blind and cannot confirm the outcome, so they either over-share by mistake or avoid the settings entirely.
- Change: Add an audience preview ("View as…": public / followers / mutuals / nobody, or product-approved equivalents) tied to each visibility setting.
- Predicted effect: Should raise confidence that a setting did what the user intended; confidence M (D2 text-only — structural inference).
- Severity: 3 (major) — frequent, high impact (privacy mistakes), persistent.
- Moves: Attention path 2→3; lifts cap: privacy-comprehension gap.

### F2 — Destructive delete sits among reversible toggles
- Lens: Navigation & interaction
- Observation: "Delete account" appears in the same long toggle list as reversible privacy settings.
- Violated principle: Nielsen #5 Error prevention; Nielsen #3 User control and freedom.
- User consequence: An irreversible action is one mistap away and is visually equivalent to reversible settings, risking accidental account loss.
- Change: Move delete account into a separate "Account actions" section with a dedicated destructive flow, confirmation, and clear irreversibility/recovery boundaries.
- Predicted effect: Should reduce accidental destructive actions; confidence M (behavior unverifiable from text).
- Severity: 3 (major) — rare action, maximal impact, persistent risk.
- Moves: Production readiness 2→3; lifts cap: P1 (destructive action among reversible controls).

### F3 — Unrelated settings in one ungrouped list
- Lens: Hierarchy & readability
- Observation: Public profile, activity status, read receipts, discoverability, and blocked users appear as equivalent toggles in one list, though they have different mental models.
- Violated principle: Gestalt proximity / common region; Cognitive load (extraneous).
- User consequence: Users must infer which setting affects visibility vs. interaction vs. findability vs. safety, slowing decisions and reducing confidence.
- Change: Group into Profile visibility, Interaction signals, Findability, Safety, and Account actions; place blocked users under Safety.
- Predicted effect: Should reduce scanning effort and mis-set privacy choices; confidence M.
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path 2→3, Composition 2→3.

### F4 — Toggle labels lack state and consequence
- Lens: Accessibility
- Observation: Toggles are named by setting only; there is no described state or consequence text, and warnings are not described beyond toggles.
- Violated principle: Nielsen #6 Recognition over recall; label semantics for assistive technology; WCAG use-of-color (do not rely on color alone).
- User consequence: Screen-reader users may hear only the setting name without its state or effect, and any color-only privacy warning is missed by some users.
- Change: Give each toggle an accessible name that includes current state and effect; ensure screen-reader order reads group → setting → state → effect; never signal a privacy warning by color alone.
- Predicted effect: Should improve comprehension for assistive-tech users; confidence M (semantics unverifiable from text).
- Severity: 2 (minor) — affects a subset, moderate impact, persistent.
- Moves: Production readiness 2→3.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {1, 2, 2, 2}; pinned by no audience preview (F1) and the destructive action sitting among reversible toggles (F2).
- Projected: 3/5 — median of the assessable projected bands {1, 3, 3, 4} once F1+F2+F3+F4 land and the audience taxonomy and retention/recovery policy are confirmed.
- Ceiling note: with a visual pass confirming large-text, screen-reader, and preview-accuracy resilience the dimension bands reach 4, but the inert-screen cap holds the artifact at 3/5 until the screen carries one owned asset.
- Primary lever(s): F1 + F2 (privacy comprehension and destructive-action separation pin the score at 2).

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path & hierarchy | 2 | 3 | F1/F3 grouping (rung 2→3) | provisional |
| Production readiness | 2 | 4 | F2/F4 lift caps | provisional |
| Color, state & contrast | 2 | 3 | toggle state is not colour-only, but the description decides no colour role; F2/F4 decide destructive and warning, and 3→4 needs stated pairs | provisional |
| Distinctiveness & owned assets | 1 | 1 | inert — a bare toggle list, and no finding adds an owned asset | provisional |
- Projected overall = median of the assessable projected dimensions {3, 4, 3, 1} = 3. Not the sum of per-dimension gains; colour stops at 3 because a description cannot state a pair or its dark-theme value, and that rung is never projected upward from text.

## Severity index
- 4 (catastrophe): none
- 3 (major): F1, F2
- 2 (minor): F3, F4
- 1 (cosmetic): none

## Unresolved assumptions
- Exact visual density, contrast, tap target size, and platform component choice require a screenshot or design file.
- Legal retention and account recovery policy are not provided.

## Next actions
- Define the audience model for each setting and map every toggle to a visible consequence.
- QA screen-reader labels, large text, privacy-preview accuracy, blocked-users navigation, and delete-account confirmation.
```

## Why this is stronger

- Quality target after fixes: projected 3/5 (flat median of the assessable dimensions, conditional); the bands reach 4 once a visual pass plus the audience taxonomy, retention policy, and moderation routes are confirmed, but the inert-screen cap holds the artifact at 3/5 until it carries an owned asset.
- Qualifies visual uncertainty from text-only input and keeps the rendered properties — stated contrast pairs, dark-theme values — out of the upward projection.
- Each finding is one causal chain (observation → violated principle → user consequence → change → predicted effect) with Nielsen 0–4 severity.
- Separates reversible settings from destructive account actions.
- Exposes both a current and a conditional projected score; no Bold move is offered because unresolved severity-3 findings remain.
- Avoids claiming legal or accessibility compliance.

## Regression checks

- Does the review classify evidence limits for description-only input?
- Does it include at least one real strength?
- Is each finding a single causal chain with a named violated principle and a predicted effect?
- Does it separate audience visibility from safety and account actions?
- Does it avoid visual overclaim about spacing or contrast, and keep the rendered properties (stated contrast pairs, dark-theme values) out of the projection?
- Does it expose a current and a conditional projected score, and correctly omit the Bold move while severity-3 findings are unresolved?
