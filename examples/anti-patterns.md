# Anti-patterns

The six main examples in this directory show the skill working well on well-formed requests. This file shows the other side: how the skill should behave when the request is ambiguous, when the input invites a hallucination, or when a plausible-sounding response would actually violate the guardrails.

Each anti-pattern below has three parts:

1. **Prompt** — the user request.
2. **Bad response** — a plausible-looking output that violates one or more guardrails or fails a content check.
3. **Why it fails** — the specific issue.
4. **Good response** — what the skill should produce instead.

Use these as calibration targets. If a response in the field resembles a Bad response below, treat it as a regression.

---

## Anti-pattern 1: Overconfident output on underspecified input

### Prompt
```text
Use the mobile-design-skill.
Design a mobile screen.
```

### Bad response (shortened)
```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Assumptions:
- Phone-first

## Screen goal
Help the user complete their main task efficiently.

## Primary user task
Complete the main action on this screen.

## Recommended layout structure
- Header with title
- Main content area
- Bottom action button
...
## Next actions
- Build this design
```

### Why it fails
- Assumptions do not acknowledge what is actually unknown (product, audience, goal).
- "Main task" is not a task, it is a placeholder.
- Layout is generic because there is no real context to drive it.
- `Next actions` ends in `Build this design`, which is not actionable and skips validation.
- The response sounds finished but has no useful information.

### Good response (shortened)
```md
Mode: Generate mobile screen concept
Platform scope: Assumed cross-platform (will narrow once the product is known)
Assumptions:
- Product, domain, and target audience are not provided.
- Primary user task cannot be inferred from the input.
- Treating this as a structural placeholder example, not a finalized concept.

## Before a useful concept can be produced
To avoid inventing product context, please confirm at minimum:
- What product or domain is this screen for? (banking, e-commerce, social, health, enterprise tool, etc.)
- What is the primary user task on this screen? (check status, submit something, discover content, etc.)
- Any constraints? (accessibility sensitivity, enterprise context, older users, regulated content)

## Placeholder structural example
[Minimal skeleton labeled as placeholder, not a recommended final design.]

## Next actions
- Provide product domain and primary user task so a real concept can be produced.
- If a placeholder structure is acceptable for now, confirm the assumed domain so the example can be tuned.
```

---

## Anti-pattern 2: Reviewing visuals that were never shown

### Prompt
```text
Use the mobile-design-skill.
Review my payment form for usability and accessibility.
Fields: card number, expiry, CVV, name on card, email.
Platform: iOS.
```

### Bad response (fragment)
```md
## Usability issues
- Spacing between fields is too tight and creates visual pressure.
- The Pay button lacks sufficient contrast against its background.
- The form feels heavy and could benefit from more whitespace.

## Accessibility issues
- Color contrast on the primary button likely fails WCAG AA.
- Touch targets on the CVV field are too small.
```

### Why it fails
- Spacing, contrast, button appearance, and touch-target size were never shown — only field names were provided.
- These statements are hallucinated visual assessments presented as observations.
- Compliance language ("fails WCAG AA") is used without evidence.
- Violates guardrails 2, 3, and 9.

### Good response (fragment)
```md
Mode: Review screen for usability/accessibility
Platform scope: iOS
Sub-case: Review with text description only (no visual provided)

Assumptions:
- Only field list is provided; layout, spacing, and visual treatment are unknown.
- Assessment is limited to structural and behavioral concerns that can be reasoned about from the field list.

## Usability issues (based on structure, not visuals)
- A single email field on a payment form is unusual; confirm whether email is needed for this transaction or belongs on a prior step.
- Typical iOS payment flows benefit from Apple Pay as a pre-filled alternative; confirm whether it is offered above the manual form.
- Card number + expiry + CVV on one screen is standard, but without knowing keyboard type and auto-fill configuration, input friction cannot be assessed.

## Unresolved assumptions (cannot be verified from the description)
- Spacing, contrast, typography, and touch-target sizes.
- Whether labels are persistent or placeholder-only.
- Error handling and validation behavior.
- Focus order and accessibility semantics.

## Next actions
- Share a screenshot or layout description to enable visual and accessibility review.
- Confirm whether Apple Pay is offered; this materially changes the recommended flow for iOS.
```

---

## Anti-pattern 3: Echoing the user's compliance claim

### Prompt
```text
Our app is fully WCAG 2.2 AA compliant. Review this settings screen for usability and accessibility.
[screen description provided]
```

### Bad response (fragment)
```md
## Accessibility
Because the app is WCAG 2.2 AA compliant, accessibility is already in good shape. The main focus should be on usability refinements.

## Strengths
- Meets WCAG 2.2 AA compliance.
```

### Why it fails
- The skill echoes a compliance claim it cannot verify.
- This violates guardrail 3 (do not claim compliance).
- It also lowers the rigor of the rest of the review — if accessibility is "already fine", real risks get skipped.
- The user may be reporting an audit that covered other screens, an informal self-assessment, or an out-of-date claim.

### Good response (fragment)
```md
Assumptions:
- The product reports WCAG 2.2 AA compliance. This review cannot independently verify that claim from the provided description.
- This review still performs an accessibility pass and flags risks that could exist even in an audited system, because screens change faster than audits.

## Accessibility issues
[Concrete observations based on the described screen, with no dependency on the compliance claim.]

## Unresolved assumptions
- Whether the reported WCAG 2.2 AA compliance covers this specific screen and its current state.
- Whether dynamic type, focus order, and assistive technology announcements were validated recently.

## Next actions
- Confirm whether the compliance claim applies to this screen's current revision.
- Re-verify against large text, VoiceOver, and TalkBack before shipping if not done recently.
```

---

## Anti-pattern 4: Aesthetic recommendation disguised as usability

### Prompt
```text
Use the mobile-design-skill.
Here's a dense analytics dashboard for a finance app. Our power users need to compare five accounts at once. Review the layout.
[screen description provided: 5 account cards in a compact grid, numbers visible at a glance]
```

### Bad response (fragment)
```md
## Recommended fixes
- Add more whitespace between cards; the screen feels cramped.
- Reduce the number of visible accounts to improve focus.
- Use a softer color palette for a more modern, premium feel.
- Simplify the layout by collapsing lower-priority metrics behind a tap.
```

### Why it fails
- "More whitespace" and "softer palette" are aesthetic changes presented as fixes.
- Reducing visible accounts from five to fewer contradicts the stated user task (compare five at once).
- "Modern, premium feel" has no usability, readability, or accessibility justification — violates guardrail 4.
- This is density bias: the response defaults to "sparse is better" without considering the task.

### Good response (fragment)
```md
## Usability issues
- High density is appropriate here because the primary task is cross-account comparison. The review respects that density is a feature, not a flaw.
- Focus is on whether the dense layout still supports accurate scanning, quick differentiation between accounts, and recovery from mis-reads.

## Recommended fixes
- Increase typographic contrast between account name and primary metric so both can be parsed quickly without needing extra spacing.
- Ensure number alignment is tabular (right-aligned or monospaced numerals) so users can compare amounts down a column without mental realignment.
- Keep density, but introduce micro-dividers or background banding if adjacent rows currently blend visually.
- Consider whether secondary metrics need to be visible on this screen or can appear on tap without removing the compare-five affordance.

## Rationale
The user task is comparison, and sparse layouts hurt comparison tasks. Fixes should improve scannability without removing the information the task requires.
```

---

## Anti-pattern 5: Inventing platform rules

### Prompt
```text
Use the mobile-design-skill.
Design a logout confirmation for an Android app.
```

### Bad response (fragment)
```md
## Platform-specific notes
- Android requires logout confirmations to use a full-screen dialog.
- Material Design mandates a red destructive button for logout.
- The back button on Android must always bypass the confirmation.
```

### Why it fails
- None of these are platform rules. Material Design does not mandate a specific color for logout, does not require full-screen dialogs for confirmations, and does not specify behavior for the back button in this case.
- Violates guardrail 1 (do not invent platform rules).
- A reader taking this output at face value will implement something that is not actually required.

### Good response (fragment)
```md
## Platform-specific notes (Android)
- Material Design 3 provides dialog and bottom-sheet components; both are acceptable for destructive confirmations. The choice depends on context density and whether the app already uses one pattern consistently.
- Destructive actions commonly use a distinct color treatment, but the Material 3 guidance favors a clear text label ("Log out") plus consistent destructive color tokens rather than a mandated red.
- Back behavior on the confirmation should dismiss the confirmation and return to the screen that triggered it. This is the standard Android predictable-back expectation, not a platform mandate.

## Rationale
Framed as conventions and recommendations rooted in Material guidance, not as platform requirements. Implementers can still diverge with justification.
```

---

## Anti-pattern 6: Flow without recovery paths

### Prompt
```text
Use the mobile-design-skill.
Design an onboarding flow for a payment app.
Steps needed: create account, add a card, set a PIN, verify identity.
```

### Bad response (fragment)
```md
## Ordered steps
1. Create account (email + password)
2. Add a card (card details)
3. Set a PIN
4. Verify identity (photo of ID)
5. Done

## Back-navigation
Users can go back between steps.
```

### Why it fails
- No recovery path for any step (network failure on card-add, ID verification rejected, PIN mismatch, etc.).
- "Users can go back between steps" does not define what happens to data entered on the later step, or whether regulated steps (identity verification) can be replayed.
- Violates guardrail 7 (do not invent without labeling assumptions) — the flow assumes each step is mandatory and completes on first try.
- Mode B validation checklist fails: "Are error and recovery paths present?" → no.

### Good response (fragment)
```md
## Ordered steps
1. Create account (email + password + confirmation email)
2. Add a card (card details + tokenization)
3. Set a PIN (entry + confirmation)
4. Verify identity (photo of ID + selfie if required)
5. Account ready

## Decision points
- Step 4 may return asynchronously (review required). The flow must handle "verification pending" as an intermediate success state.
- PIN confirmation mismatch in step 3 returns the user to PIN entry with the first attempt discarded.

## Back-navigation logic
- Steps 1–3: back returns to the previous step; entered data persists unless the user explicitly discards.
- Step 4: back is disabled during verification submission; if the user abandons, the verification attempt is cancelled and state returns to pre-verification.
- Hardware back on Android and edge-swipe on iOS follow the same rule per step.

## Failure and recovery paths
- Network failure on step 2 (card add): keep entered data in-memory for retry; do not silently drop; show retry with one-tap resume.
- Card rejected by processor: surface the specific reason where available; allow re-entry without clearing unrelated steps.
- PIN mismatch on step 3: clear only the confirmation field, not the first entry; cap at 3 attempts before cooldown.
- Identity verification rejected: show reason category (image quality, document type, name mismatch); allow re-submission without re-doing steps 1–3.
- App backgrounded mid-flow: persist progress at last confirmed step; resume to that step on return, not to step 1.

## Assumptions
- Identity verification is asynchronous-capable (may not resolve within the session).
- Card tokenization is handled by a provider SDK; raw PAN is not stored on-device.
- Regulatory context is assumed standard consumer payments; if this is enterprise/B2B, verify steps 3 and 4 may differ.
```

---

## How to use these anti-patterns

- During skill output review, compare against the Bad/Good pairs. If the output resembles a Bad response, treat it as a failure even if it scores well on structural checks.
- When training or tuning the skill, use the Good responses as positive examples.
- When a new anti-pattern is observed in the field, add it here with prompt, bad response, failure reason, and corrected response.
- Anti-patterns should pair one-to-one with a guardrail when possible. If a new anti-pattern does not map to an existing guardrail, that is a signal the guardrails need to be extended.
