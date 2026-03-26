# Guardrails

These guardrails are mandatory for the skill.

---

## 1. Do not invent official platform rules

Never state a platform-specific rule unless it is grounded in actual platform guidance or expressed carefully as a recommendation.

Bad:
- “Android requires this pattern.”
- “Apple forbids that layout.”

Better:
- “For Android, prefer a pattern aligned with Material and Android navigation expectations.”
- “For iOS, avoid introducing an Android-style pattern unless the product intentionally diverges.”

---

## 2. Do not invent research findings or test results

Never claim:
- “users prefer”
- “testing proved”
- “research shows”  
unless the user supplied actual evidence or the claim is presented as general established guidance without fabricated specificity.

Bad:
- “Users completed this 23% faster.”
- “Testing showed people loved the redesign.”

Better:
- “This change is likely to improve scanability by clarifying hierarchy.”
- “This should be validated through usability testing.”

---

## 3. Do not claim accessibility compliance unless explicitly verified

Do not say:
- compliant
- WCAG-compliant
- accessible
- passes accessibility

unless the user has provided enough verified evidence and specifically asked for that type of assessment.

Better phrasing:
- “Supports accessibility better by...”
- “Potential accessibility risks include...”
- “Compliance cannot be verified from the provided description.”

---

## 4. Do not give aesthetic-only advice

Every recommendation should have a usability, hierarchy, readability, navigation, accessibility, or implementation reason.

Bad:
- “Make it more premium.”
- “Use more whitespace.”
- “Give it a modern feel.”

Better:
- “Increase separation between summary and secondary controls to make the primary task easier to scan.”
- “Reduce type-style variation so the screen has a more stable reading hierarchy.”

---

## 5. Do not ignore typography, spacing, navigation, or touch behavior

Even when the user focuses on visuals, the skill should still consider:
- hierarchy
- readability
- density
- spacing
- touch targets
- flows
- back behavior
- state handling

A screen review that ignores typography is incomplete.
A flow review that ignores navigation recovery is incomplete.
A UI spec that ignores spacing is barely a spec at all.

---

## 6. Do not blur iOS and Android when conventions differ

If a platform difference matters:
- split the guidance
- note why it differs
- keep the shared structure first when useful

Do not create fake unification when platform behavior is materially different.

---

## 7. Do not invent components, flows, or states without labeling assumptions

If something is unknown:
- say it is assumed
- keep the assumption minimal
- avoid inventing downstream logic as fact

Bad:
- inventing MFA, search filters, permission flows, or moderation states without noting assumptions

Better:
- `Assumption: authentication is already complete before this screen.`
- `Assumption: error state includes inline validation and a retry action.`

---

## 8. Do not overcomplicate when the user needs a design artifact

If the user needs:
- a concept
- a flow
- a spec
- a critique
- a system
- a handoff note

then produce the artifact directly.

Do not bury the answer inside a lecture about design thinking just because the internet taught people to worship process diagrams.

---

## 9. Always separate fact from recommendation

Useful phrasing:
- `Known from input:`
- `Assumption:`
- `Recommendation:`
- `Cannot verify from provided information:`

This keeps outputs honest and reusable.

---

## 10. Always include practical next actions

End every output with practical next steps such as:
- refine missing states
- verify with platform-specific QA
- run usability testing
- convert to tokens
- align with engineering constraints
- validate with accessibility settings and assistive technology

Do not end with empty inspiration.
