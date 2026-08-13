# Visual Review Fixture: Social Profile Privacy / Control

## Review setup

- Synthetic fixture only. No screenshots, real brands, or copied UI.
- Review evidence type: D2, text description only.
- Platform scope: Cross-platform mobile social app.
- User task: understand how the profile appears to others and control visibility, contact discovery, and blocked-user settings.

## Screen description

A profile settings screen combines public profile preview, audience controls, contact sync, blocked users, and account visibility in one page. Product wants fewer screens and a friendly tone.

## Frame specs

- Frame: 390 x 844 px mobile portrait.
- Header: "Profile settings" with back button.
- Content: vertically scrollable list of grouped settings.
- Profile preview card: avatar, display name, bio, and public badge.
- Settings rows: Account visibility, Show activity status, Contact discovery, Sync contacts, Blocked users, Muted words.
- Footer: "Deactivate account" link.

## Visible hierarchy

1. Profile preview card.
2. Account visibility row.
3. Contact discovery row.
4. Sync contacts toggle.
5. Show activity status toggle.
6. Blocked users row.
7. Muted words row.
8. Deactivate account link.

## Components

- Profile preview card.
- Setting rows with labels, helper copy, and chevrons.
- Toggle switches.
- Audience selector row.
- Destructive footer link.
- Confirmation sheet for deactivation.
- No inline "view as public" mode is described.

## Typography

- Screen title: 20 px semibold.
- Setting labels: 16 px regular.
- Helper copy: 12 px regular.
- Preview name: 18 px semibold.
- Preview bio: 13 px regular.
- Destructive link: 14 px regular.

## Color and state notes

- Public badge is blue.
- Private state uses a lock icon and gray text.
- Contact sync toggle is on by default for new users.
- Destructive link uses red text.
- Disabled states are not described.
- The preview card does not change live when toggles change.

## Interaction states

- Default state described.
- Toggle on/off states exist.
- Deactivation confirmation sheet exists.
- Unsaved-change state is not described.
- Permission-denied state for contacts is not described.
- Contact sync failure state is not described.
- Blocked-user empty state is not described.

## Known constraints

- Privacy language must be understandable to non-technical users.
- Users need to distinguish who can see profile content, activity status, and contact discovery.
- Contact sync may require OS permission.
- Some users may be minors or in sensitive situations, but the fixture does not provide age or safety policy.
- The review must not claim legal compliance.

## Example output

```md
Mode: Review screen for usability/accessibility
Platform scope: Cross-platform mobile
Sub-case: D2 description only (text description provided, no visual asset)
Assumptions:
- This is a phone-first profile settings screen, 390 x 844 px.
- Contact sync is on by default for new users, as stated.
- No "view as public" mode is present; the preview does not update live with toggle changes.

## Quick summary
The screen gathers the right privacy controls in one place, but it under-delivers on the two things this surface exists to do: help users understand who can see what, and let them change it with confidence. Related controls (visibility, discovery, sync, activity) are not separated by audience or data type, contact sync is on by default without a clear consent step, the preview does not reflect changes, and deactivation is a low-context footer link. The inventory is useful, so the ceiling is decent, but visual properties cannot be judged from text.

## Strengths
- Collects the relevant privacy controls (visibility, discovery, sync, activity, blocked, muted) in one place.
- Provides helper copy under settings and a lock icon for the private state.
- Includes a confirmation sheet for the destructive deactivation action.

## Findings

### F1 — Contact sync is on by default without clear consent
- Lens: Usability
- Observation: The contact-sync toggle is on by default for new users, and no explicit consent step is described; contact sync may also require OS permission.
- Violated principle: Nielsen #5 Error prevention; Nielsen #3 User control and freedom (consent should be a deliberate choice).
- User consequence: New users may upload their contacts without realizing it, a privacy decision made for them rather than by them — high risk in sensitive situations.
- Change: Make contact sync an explicit opt-in with a plain-language explanation of what is shared and why; never default it on.
- Predicted effect: Should reduce unintended contact uploads; confidence M (D2 text-only — structural inference, not measured). Framed as risk; no compliance claim is made.
- Severity: 3 (major) — frequent (every new user), high impact (privacy), persistent until changed.
- Moves: Production readiness 2→3; lifts cap: default-on consent risk.

### F2 — Privacy model is ambiguous across related controls
- Lens: Usability
- Observation: Account visibility, Contact discovery, Sync contacts, and Show activity status are related but presented as a flat list, not separated by audience or data type.
- Violated principle: Nielsen #6 Recognition over recall; Cognitive load (extraneous); Gestalt common region.
- User consequence: Users cannot easily reason about who can see their content vs. how people find them vs. what data is shared, so they may set the wrong control.
- Change: Group into "Who can see me," "How people find me," and "Account controls," with clear audience/data framing per group.
- Predicted effect: Should improve privacy comprehension and reduce mis-set controls; confidence M (D2 text-only).
- Severity: 3 (major) — frequent, high impact (privacy comprehension), persistent.
- Moves: Attention path & hierarchy 2→3; lifts cap: privacy-model ambiguity.

### F3 — Deactivation is a low-context destructive link
- Lens: Usability
- Observation: "Deactivate account" is a footer link; a confirmation sheet exists, but there is no consequence summary or cooling-off context described.
- Violated principle: Nielsen #5 Error prevention; Nielsen #3 User control and freedom.
- User consequence: Users may trigger a high-stakes account action without understanding its consequences, and a bare confirmation may not be enough to prevent regret.
- Change: Give deactivation a consequence summary (what is lost, what is recoverable) and cooling-off/undo framing in the confirmation, and place it with appropriate context rather than as a bare footer link.
- Predicted effect: Should reduce regretted deactivations; confidence M (D2 text-only).
- Severity: 3 (major) — occasional but high impact (account loss), persistent until contextualized.
- Moves: Production readiness 2→3; lifts cap: destructive-action safeguard.

### F4 — Preview does not reflect setting changes
- Lens: Usability
- Observation: The profile preview card does not change live when toggles change, and no "view as public" mode is described.
- Violated principle: Nielsen #1 Visibility of system status; recognition over recall.
- User consequence: Users cannot see what changes when they adjust visibility, so they cannot confirm the effect of a privacy decision.
- Change: Make the preview update with settings, or add an explicit "View as public" mode that reflects current choices.
- Predicted effect: Should improve confidence that privacy changes took effect; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Interaction polish & motion 2→3.

### F5 — Missing permission, failure, and empty states
- Lens: Usability
- Observation: No permission-denied state for contacts, no contact-sync failure state, and no blocked-user empty state are described; unsaved-change state is also undefined.
- Violated principle: Nielsen #1 Visibility of system status; Nielsen #9 Help users recognize, diagnose, and recover.
- User consequence: When OS permission is denied or sync fails, users get no recovery path, and an empty blocked-users list gives no orientation.
- Change: Add an OS-permission-denied path, a contact-sync failure/retry state, and a blocked-users empty state; clarify unsaved-change handling.
- Predicted effect: Should reduce dead ends around permissions and sync; confidence M (D2 text-only).
- Severity: 2 (minor) — occasional, moderate impact, persistent until defined.
- Moves: Production readiness 2→3.

## Design quality score (current → projected)
- Current: 2/5 — median of the assessable Now bands {1, 2, 2, 2, 3, 3}; pinned by default-on contact sync (F1), privacy-model ambiguity (F2), and a low-context destructive action (F3).
- Projected: 3/5 — median of the assessable projected bands {1, 3, 3, 3, 3, 4} once F1+F2+F3 land (plus F4/F5); held there by the colour, typography and distinctiveness bands no finding touches.
- Ceiling note: with a visual pass confirming tone, contrast, and control sizing the leading band reaches 4, but the inert-screen cap holds the artifact at 3/5 until the screen carries one owned asset (large-text, contrast of gray/red text, and dark mode are still unverified from the description).
- Primary lever(s): F2 (separating controls by audience/data type is what most unlocks privacy comprehension), closely tied with F1.

| Dimension | Now | Projected | Gated by | Confidence |
|-----------|-----|-----------|----------|------------|
| Attention path & hierarchy | 2 | 3 | F2 grouping (rung 2→3) | provisional |
| Production readiness | 2 | 4 | F1/F3/F5 lift consent/safety caps | provisional |
| Interaction polish & motion | 2 | 3 | F4 live preview (rung 2→3) | provisional |
| Color, state & contrast | 3 | 3 | roles are decided and the private state pairs gray with a lock icon; 3→4 needs stated pairs, which a description does not carry | provisional |
| Typography craft | 3 | 3 | six roles carry stated sizes and weights; 3→4 needs the behaviour named when text scales up, which no finding supplies | provisional |
| Distinctiveness & owned assets | 1 | 1 | inert — preview card and rows are interchangeable once the logo is removed, and no finding adds an owned asset | provisional |
- Projected overall = median of the assessable projected dimensions {3, 4, 3, 3, 3, 1} = 3. Not the sum of per-dimension gains; colour and typography do not move because no finding states a pair or a text-scaling behaviour, and neither rung is projected upward from text.

## Severity index
- 4 (catastrophe): none
- 3 (major): F1, F2, F3
- 2 (minor): F4, F5
- 1 (cosmetic): none

## Platform-convention mismatches
- Cross-platform caution: contact-permission requests and denied-permission paths must follow each OS's permission model rather than inventing platform copy.
- Toggles, confirmation sheets, and destructive actions should follow platform-idiomatic patterns per OS.

## Unresolved assumptions
- Cannot verify contrast of red destructive text or gray private-state text from text.
- Cannot verify toggle or tap-target sizes from the description.
- Cannot verify whether the friendly tone reads clearly without a screenshot.
- Cannot make any legal/compliance claim; sensitive-situation concerns are framed as risk, not fact.

## Next actions
- Make contact sync explicit opt-in and regroup controls into audience/data-type sections before any visual polish.
- Add a deactivation consequence summary, live/"view as public" preview, and the missing permission/failure/empty states.
- Run a visual pass with large text and the permission/failure scenarios to confirm the projected score.
```

## Expected critique

- The review should flag privacy model ambiguity: Account visibility, Contact discovery, Sync contacts, and Activity status are related but not clearly separated by audience and data type.
- The review should flag default-on contact sync as high risk unless the product has a clearly explained consent step.
- The review should flag missing public preview behavior: users need to see what changes when visibility settings change.
- The review should flag destructive action placement: Deactivate account should not be a low-context footer link without account consequence summary.
- The review should flag missing permission and failure states for contact sync.
- The review should recommend concrete fixes: split settings into "Who can see me", "How people find me", and "Account controls"; add live preview or "View as public"; make contact sync explicit opt-in; add OS permission denied path; add consequence summary and cooling-off copy for deactivation.
- The review should note strengths: grouped settings, helper copy, lock icon, and confirmation sheet are useful foundations.

## Prohibited critique

- Do not claim GDPR, COPPA, DSA, or privacy-law compliance or non-compliance.
- Do not claim the design is unsafe for minors without policy context.
- Do not infer abusive-use scenarios as facts; frame sensitive-situation concerns as risk.
- Do not claim exact visual contrast failure for red/gray text without values.
- Do not assert that toggles are too small unless dimensions are provided.
- Do not invent platform permission copy.

## Severity expectations

Severity uses the Nielsen 0-4 scale (High maps to 3, or 4 if irreversible/catastrophic; Medium to 2; Low to 1).

- 3 (major): default-on contact sync without explicit consent context, privacy model ambiguity, destructive account action with weak consequence summary.
- 2 (minor): preview not updating, missing contact permission/failure states, blocked-user empty state missing.
- 1 (cosmetic): exact tone, spacing, and red-link visual weight should remain qualified because no screenshot is provided.

## Rubric score expectation

- Expected score: current 2/5 → projected 3/5 (flat median of the assessable dimensions, conditional, provisional D2).
- Reason for current: the screen has a useful settings inventory and already decides its colour and type roles, but privacy comprehension, consent clarity, and destructive-action safeguards are not strong enough.
- Reason for projected: making contact sync explicit opt-in, regrouping controls by audience/data type, and adding deactivation safeguards lift production readiness to 4 — but colour and typography stay at 3 because no finding states a pair or a text-scaling behaviour, the screen owns no asset, and tone, contrast, and control sizing cannot be raised from a text-only description.
- No Bold move is expected: the screen has unresolved severity-3 findings, so the Bold move trigger is not met.
