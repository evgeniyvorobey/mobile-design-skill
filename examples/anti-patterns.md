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

## Findings
- **F1 — Usability.** Observation: the form asks for an email address alongside card details. Violated principle: Nielsen #8, aesthetic and minimalist design — every field on a payment screen competes with the one that completes the purchase. User consequence: an extra field at the moment of payment measurably raises abandonment, and if the email is already known the ask reads as a data grab. Change: remove the field, or move it to the step where the account is identified. Predicted effect: fewer fields between intent and completion; directional, low confidence without funnel data. Severity: 2 (minor — frequent, low impact per occurrence). Moves: Attention path 3 → 4.
- **F2 — Usability.** Observation: no platform payment method is described above the manual form. Violated principle: Jakob's Law — iOS users expect Apple Pay first on a payment sheet. User consequence: users who could have paid in one authentication retype a card instead. Change: offer Apple Pay above the manual form, with the manual path intact below. Predicted effect: shorter path for the majority case; directional. Severity: 3 (major — affects the primary task on every visit). Moves: Attention path 3 → 4. **Unverified:** whether Apple Pay is offered is not stated in the description; confirm before acting.

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

## Findings
- **F1 — Accessibility.** Observation: [concrete structural observation from the described screen]. Violated principle: [named WCAG criterion or platform requirement]. User consequence: [who is blocked and from what]. Change: [the specific fix]. Predicted effect: [outcome, directional]. Severity: [0–4]. Moves: [dimension, band → band]. Stated independently of the compliance claim, which this review cannot verify.

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

### Good response (fragment, new Findings format)
```md
## Quick summary
High density is appropriate here: the primary task is cross-account comparison, and sparse layouts hurt comparison. The review keeps density and focuses on whether the dense layout still supports accurate scanning and recovery from mis-reads.

## Findings

### F1 — Account name and primary metric compete for attention
- Lens: Hierarchy & readability
- Observation: Each card shows account name and primary metric at similar visual weight.
- Violated principle: Von Restorff effect; attention path.
- User consequence: The eye cannot lock onto the comparison value quickly, slowing cross-account scanning — the exact task.
- Change: Increase typographic contrast between account name and primary metric (weight/size), no extra spacing.
- Predicted effect: Should speed value scanning without reducing how many accounts fit; confidence M (D2 text-only).
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Attention path & hierarchy 3→4.

### F2 — Amounts are not aligned for down-column comparison
- Lens: Hierarchy & readability
- Observation: Numbers appear without stated tabular alignment.
- Violated principle: Gestalt continuity; comparison-task ergonomics.
- User consequence: Users mentally re-align digits to compare amounts across accounts, adding effort to the core task.
- Change: Use tabular (right-aligned or monospaced) numerals so amounts compare down a column.
- Predicted effect: Should cut mental realignment when comparing accounts; confidence M.
- Severity: 2 (minor) — frequent, moderate impact, persistent.
- Moves: Composition & spacing 3→4.

(Note: do NOT recommend "more whitespace", "softer palette", or "reduce visible accounts" — those are aesthetic changes or contradict the stated compare-five task.)
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

## Anti-pattern 7: Template-complete but decision-empty output

### Prompt
```text
Use the mobile-design-skill.
Create a UI spec for a cross-platform subscription settings screen.
Users need to see current plan, renewal date, payment method, and cancel option.
```

### Bad response (fragment)
```md
## Structural zones
- Top area: plan information
- Main content area: subscription details
- Bottom area: actions

## Behavior rules
- Show the current plan.
- Let the user update payment.
- Let the user cancel.

## Key decision tradeoffs
- Use a clear layout because it is better for users.
```

### Why it fails
- The visible sections are present, but no real design decisions were made.
- "Clear layout" is not a tradeoff and has no rejected alternative.
- The spec omits state and risk details: renewal failed, payment expired, cancellation confirmation, refund policy unknown, restore purchase, and platform billing differences.
- An engineer cannot implement the behavior without guessing.

### Good response (fragment)
```md
## Structural zones
- Summary zone: current plan name, price, renewal date, and status badge in one grouped block so the user's first glance answers "what am I paying for?"
- Payment zone: payment method row with masked details, status, and "Update" action; keep it separate from cancellation to avoid accidental destructive intent.
- Support zone: invoices, terms, and contact support as secondary rows.
- Bottom action zone: cancel subscription as a secondary/destructive text action, not the primary CTA.

## State definitions
- Default: active subscription with renewal date.
- Payment issue: warning banner above payment zone, "Update payment" becomes the recommended action.
- Cancel pending: show end-of-access date and restore/reactivate option if allowed.
- Loading: skeleton for plan summary and payment row; do not show cancellation action until status is known.
- Error: keep last known subscription state visible and provide retry.

## Key decision tradeoffs
- Group plan summary above payment details, chosen over a flat list because subscription confidence depends on seeing plan + renewal before payment maintenance.
- Keep cancellation visually secondary, chosen over bottom primary destructive CTA because cancel is important but not the routine task on settings entry.
```

---

## Anti-pattern 8: Bold move as aesthetic laundering

### Prompt
```text
Use the mobile-design-skill.
Review this finance dashboard. It is competent but feels generic.
[D1: screenshot provided; no unresolved severity-3/4 issues, screen is ~3/5 but inert]
```

### Bad response (fragment)
```md
## Bold move
- Make the dashboard feel more premium with a bolder hero and a richer color story.
```

### Why it fails
- No mechanism, no named product contradiction, no job, no validation path — it is "make it premium" with a new label.
- A Bold move is held to a *higher* evidence bar than a normal fix, not a lower one. This is aesthetic laundering (guardrail 4).

### Good response (fragment)
```md
## Bold move (optional)
- The move: Replace the five-tab bottom nav with three tabs plus a context-aware action bar.
- Deviates from: the product's "everything one tap away" principle and the Material bottom-nav convention (Jakob's Law).
- Job served (JTBD): "When I open the app, I want to act on what matters now, so I can finish fast." Outcome: minimize taps-to-primary-action per screen.
- UX upside: cuts choice load (Hick's Law) and frees the thumb zone for the one primary task (Fitts).
- Risk / cost: two destinations move one level deeper; power users lose a shortcut.
- De-risk / validate: tree-test findability of the demoted destinations; ship the action bar with a first-use coach mark; kill if findability drops.
- Score impact: safe fixes → 4/5; this targets 5/5 on focus and distinctiveness, gated on the findability test.
- Conviction: worth a spike.
```

### Why it is stronger
- It names what it breaks, the job it serves, the upside (with heuristics), the risk, and a concrete validation path with a kill criterion.
- It stays in the `Bold move` block, separate from required fixes, and does not raise the score until validated.

---

## Anti-pattern 9: Rounding a request to the nearest mode

### Prompt
```text
Use the mobile-design-skill.
Help me design our paywall pricing architecture — how many tiers, what gates which feature,
where the upgrade prompts live across the app, and how we handle downgrade.
```

### Bad response (fragment)
```md
Mode: Generate mobile screen concept
Platform scope: Cross-platform
Device class: Phone

## Screen goal
Help users understand pricing tiers and choose a plan.

## Information hierarchy
1. Plan cards
2. Feature comparison
3. Upgrade CTA
```

### Why it fails
- The request is pricing and gating **architecture across an app**; the answer is one paywall screen. The mode header claims a screen concept was asked for, which is false.
- Everything the user actually asked — tier count, which feature sits behind which gate, where prompts appear across the app, downgrade handling — is absent, and the template's completeness hides that.
- The user gets a plausible artifact for a question they did not ask, and no signal that the fit was poor.

### Good response (fragment)
```md
Mode: outside the standard six — monetization and gating architecture across the app
Platform scope: Cross-platform
Device class: Phone (compact width only; a regular-width layout can be added on request)
Assumptions:
- Subscription model with at least one free tier; no enterprise/seat licensing in scope.
- Store billing rules (Apple/Google) apply and constrain what can be offered in-app.

Closest mode: Design mobile user flow (Mode 2), which would cover the upgrade path itself.
What it would lose: tier structure, the feature-to-gate mapping, prompt placement across
surfaces, and downgrade/regret handling — which is most of the question.

## Gating map
- Gate on value delivered, not on effort saved: gate the outcome the free tier already taught
  the user to want, so the upgrade reads as continuation rather than a wall.
- One gate per job. Two gates on the same job read as nickel-and-diming.
...

## Prompt placement across surfaces
- At the moment of blocked intent, inline — not on launch. A launch interstitial is measured on
  impressions, not on activation, which is why it survives review despite hurting retention.
...

## Downgrade and regret
- Downgrade must be as reachable as upgrade, or the store's own cancellation flow becomes the
  user's first support experience.
...

## Next actions
- Confirm the free-tier feature list and which store the launch targets.
- Once the tier structure is settled, run Mode 2 on the upgrade flow and Mode 1 on the paywall screen.
```

### Why it is stronger
- The mode header is honest, so the user immediately sees the request sat outside the six.
- It names the closest mode and exactly what that mode would have dropped.
- It answers the actual question with reasoning, and points at the modes that *do* fit the sub-tasks once the architecture is settled.

---

## How to use these anti-patterns

- During skill output review, compare against the Bad/Good pairs. If the output resembles a Bad response, treat it as a failure even if it scores well on structural checks.
- When training or tuning the skill, use the Good responses as positive examples.
- Use `docs/weaknesses.md` to decide whether a new field failure deserves a new anti-pattern.
- When a new anti-pattern is observed in the field, add it here with prompt, bad response, failure reason, and corrected response.
- Anti-patterns should pair one-to-one with a guardrail when possible. If a new anti-pattern does not map to an existing guardrail, that is a signal the guardrails need to be extended.
