# Example: Review screen for usability/accessibility

## Example prompt

```text
Use the mobile-design-skill.

Review this cross-platform mobile profile edit screen for usability and accessibility.

Screen description:
- title at top
- profile photo
- name, email, phone, birthday, address, company, job title all in one long form
- save button only at bottom
- placeholders are being used as labels
- required fields are not marked until submit
- errors appear only in red text
- there is a back arrow but unsaved changes behavior is unclear

Constraints:
- enterprise app
- high density
- many users are older
```

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform
Device class: Phone (compact width only; a regular-width layout can be added on request)
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- This is a phone-first screen.
- Email may be read-only in some account states, but that is not shown here.
- No section collapsing is currently implemented.

## Quick summary
The screen is functionally complete but structurally overloaded: weak form clarity, poor error prevention, insufficient labeling, and fragile completion behavior on a long mobile form. It will create avoidable errors and unnecessary scrolling, especially for older users or larger text settings. Current quality is low, but the structural fixes below have a clear, attributable path to a stronger score.

## Strengths
- Common profile fields are present in one place.
- The top title and profile image create basic orientation.
- A single save action reduces ambiguity about how edits are finalized.

## Findings

### F1 — Required fields revealed only at submit
- Lens: Usability
- Observation: Required fields are not marked until the user submits; errors then appear in red text.
- Violated principle: Nielsen #5 Error prevention; Wroblewski form-design (mark required before submit).
- User consequence: Users complete the whole form, hit save, then back-track to fix errors — high-effort recovery on a long form, worse for older users.
- Change: Mark required fields inline before submit; validate on blur with supportive helper text; pair errors with icon + text, not color alone.
- Predicted effect: Should cut submit-time error bounce and re-scrolling; confidence M (D2 text-only — structural inference, not measured).
- Severity: 3 (major) — frequent (every submit), high impact (rework), persistent (repeats each edit).
- Moves: Production readiness 2→3; lifts cap: P1 (late required-field feedback).

### F2 — Placeholder text used as the only label
- Lens: Accessibility
- Observation: Placeholders are used in place of persistent field labels.
- Violated principle: Nielsen #6 Recognition over recall; label semantics for assistive technology.
- User consequence: Labels vanish once typing starts; recall load rises and assistive tech may not announce a stable field name.
- Change: Add persistent visible labels above each field; keep placeholders only for format hints.
- Predicted effect: Should reduce field-identification errors and improve screen-reader clarity; confidence M (semantics unverifiable from text).
- Severity: 3 (major) — frequent, high impact, persistent.
- Moves: Production readiness 2→3; lifts cap: P1 (placeholder-only labeling).

### F3 — Flat, ungrouped long form
- Lens: Hierarchy & readability
- Observation: Seven fields (name, email, phone, birthday, address, company, job title) sit in one undifferentiated block.
- Violated principle: Gestalt proximity / common region; Cognitive load (extraneous).
- User consequence: The form reads as one long list; scanning effort and perceived length rise, especially at large text sizes.
- Change: Group into Personal / Contact / Work / Address with section headers.
- Predicted effect: Should reduce scanning effort and perceived length; confidence M.
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path 2→3, Composition 2→3.

### F4 — Unclear unsaved-changes behavior on back
- Lens: Navigation & interaction
- Observation: A back arrow exists but unsaved-changes behavior is undefined.
- Violated principle: Nielsen #5 Error prevention; Nielsen #3 User control and freedom.
- User consequence: Users risk silently losing edits on a long form, which erodes trust and forces re-entry.
- Change: On back with unsaved edits, prompt to save or discard; preserve entered data.
- Predicted effect: Should prevent accidental data loss; confidence M.
- Severity: 3 (major) — occasional but high impact, persistent across sessions.
- Moves: Interaction polish 2→3.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {1, 1, 2, 2, 2, 2}; provisional (D2 text-only), pinned by late required-field feedback (F1) and placeholder-only labeling (F2).
- Projected: 3/5 — median of the assessable projected bands {1, 3, 3, 3, 3, 3} once F1–F4 land; held there by the inert Distinctiveness band that no finding lifts.
- Ceiling note: with a visual pass confirming contrast, spacing, and large-text behavior the dimension bands reach 4, but the inert-screen cap holds the artifact at 3/5 until this screen carries one owned asset (resilience such as dark mode and AT semantics is still unverified from the description).
- Primary lever(s): F1 + F2 (they lift the P1 caps pinning the score at 2).

| Dimension | Now | Projected | Gated by (cap / ladder rung) | Confidence |
|-----------|-----|-----------|------------------------------|------------|
| Attention path & hierarchy | 2 | 3 | rung 2→3 (F3) | provisional |
| Production readiness | 2 | 3 | F1/F2 lift P1 caps | provisional |
| Interaction polish & motion | 2 | 3 | rung 2→3 (F4) | provisional |
| Composition & spacing | 2 | 3 | seven fields in one undifferentiated block (F3); 3→4 needs stated spacing values | provisional |
| Color, state & contrast | 1 | 3 | errors are red-only, so the second-cue test fails (F1); 3→4 needs stated foreground/background pairs | provisional |
| Distinctiveness & owned assets | 1 | 1 | inert — nothing here survives removing the logo, and no finding adds an owned asset | provisional |
- Projected overall = median of the assessable projected dimensions {3, 3, 3, 3, 3, 1} = 3. Not the sum of per-dimension gains; colour stops at 3 because a description cannot state a pair or its dark-theme value, and that rung is never projected upward from text.

## Severity index
- 4 (catastrophe): none
- 3 (major): F1, F2, F4
- 2 (minor): F3
- 1 (cosmetic): none

## Bold move
- None. The Bold move trigger is not met: the screen is at 2/5 with unresolved severity-3 findings (F1, F2, F4). Fix the foundation first; a bold, product-contradicting move (e.g. splitting the form into a progressive flow) is only worth proposing once the screen is competent and inert.

## Platform-convention mismatches
- Cross-platform caution: back behavior must remain predictable and must not silently discard edits.
- If the same screen is used on iOS and Android, save and exit patterns should respect each platform's navigation expectations rather than acting like a web form dropped into a phone.

## Unresolved assumptions
- Cannot verify field editability rules.
- Cannot verify keyboard handling.
- Cannot verify accessibility semantics or assistive-technology announcements.
- Cannot verify text-scaling resilience from the description alone.

## Next actions
- Restructure the form into grouped sections and add required-field marking before polishing visuals.
- Define unsaved-changes behavior explicitly and preserve entered data.
- Run a review with large text and error scenarios to confirm the projected score.
```
