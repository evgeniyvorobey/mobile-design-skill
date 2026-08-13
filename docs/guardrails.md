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

Carve-out for bold moves: a recommendation that contradicts the current product or direction is not aesthetic-only when it is justified by a named usability, accessibility, or hierarchy mechanism AND surfaced in the Mode D `Bold move` block with its tradeoff and validation path. Aesthetic-only contradictions ("make it premium", "feels dated") remain a failure.

---

## 5. Do not treat inspiration sources as evidence

Inspiration sources such as Mobbin, Page Flows, UI Sources, Pttrns, Screenlane, Apple Design Awards, Awwwards, Behance, Dribbble, Pinterest, and Figma Community can help with visual range and comparable examples.

They must not be used as proof of:
- usability
- accessibility
- platform correctness
- compliance
- user preference
- business effectiveness

Bad:
- “This is the right checkout pattern because it appears on Dribbble.”
- “This layout is accessible because similar work appears on Behance.”
- “Awwwards sites use this motion, so it is safe for onboarding.”

Better:
- “The pattern is justified by task structure, platform conventions, and accessibility requirements. Use Mobbin/Page Flows for comparable production examples and Behance/Dribbble for visual exploration.”

---

## 6. Do not use visual polish to hide weak product design

Visual craft matters, but it must make the design clearer, not merely more impressive.

Do not use:
- brand expression to hide unclear hierarchy
- animation to distract from missing feedback states
- illustration to replace useful empty-state guidance
- gradients or surface styling to compensate for poor grouping
- "premium" or "modern" language without concrete design mechanisms

Better:
- "Use a stronger title/body contrast and 24dp section spacing so the primary account status is readable before secondary actions."
- "Use a restrained brand accent for the primary action only; keep error and warning colors semantic and paired with icons/text."

---

## 7. Do not ignore typography, spacing, navigation, or touch behavior

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

## 8. Do not blur iOS and Android when conventions differ

If a platform difference matters:
- split the guidance
- note why it differs
- keep the shared structure first when useful

Do not create fake unification when platform behavior is materially different.

---

## 9. Do not invent components, flows, or states without labeling assumptions

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

## 10. Do not overcomplicate when the user needs a design artifact

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

## 11. Always separate fact from recommendation

Useful phrasing:
- `Known from input:`
- `Assumption:`
- `Recommendation:`
- `Cannot verify from provided information:`

This keeps outputs honest and reusable.

---

## 12. Always include practical next actions

End every output with practical next steps such as:
- refine missing states
- verify with platform-specific QA
- run usability testing
- convert to tokens
- align with engineering constraints
- validate with accessibility settings and assistive technology

Do not end with empty inspiration.

---

## 13. Do not return template-complete but decision-empty output

A response can satisfy the visible section structure and still fail the user.

Watch for:
- sections filled with generic placeholders
- recommendations that name components but do not choose between alternatives
- rationale that repeats the user's request instead of explaining a decision
- mode output that has no concrete state, behavior, typography, spacing, or validation implication

Better:
- name the chosen option
- name the rejected alternative where the decision matters
- tie the reason to user task, platform, accessibility, context, or implementation
- if the input is too thin, narrow the artifact and state what cannot be decided yet

Use `docs/weaknesses.md` as the failure-mode map for this guardrail.

---

## 14. Do not let scores hide design risk

The 1-5 rubric in `docs/design-quality-rubric.md` is a quality tool, not a laundering mechanism.

Do not:
- average a serious accessibility, state, platform, or evidence flaw into an acceptable-looking score
- give a 4/5 or 5/5 score to a design with unresolved P0/P1 weakness
- expose a precise visual quality score from text-only input without labeling evidence limits
- use the score instead of explaining the concrete mechanism

Better:
- apply caps from the rubric
- score the weak dimension explicitly
- revise a generated artifact when a dimension's failed boundary question can be answered with the context at hand, then re-derive
- for reviews, attach the score to a short evidence-based reason

---

## 15. Do not ask unnecessary questions

Clarifying questions are useful only when the answer changes the recommendation.

Do not:
- ask a discovery questionnaire before producing a simple artifact
- ask brand/style questions before task, platform, safety, accessibility, or implementation blockers
- ask more than three questions at once
- block a provisional draft when a safe assumption would work

Better:
- apply `docs/clarification-policy.md`
- proceed with the smallest labeled assumption when the gap is not blocking
- ask one to three high-impact questions when the gap changes the design decision
- offer a fast path when the user can accept a provisional draft

---

## 16. Do not describe a source you cannot open, or state a version-bound default as timeless

Two failure modes with the same root: asserting something as current fact when it was never observed.

**Auth-walled references.** Mobbin, Page Flows, UI Sources and Pttrns sit behind sign-in or paid subscriptions. A skill run has no session for them, so their contents have not been seen.

Do not:
- describe what a product's screen looks like "on Mobbin"
- attribute a pattern to "current examples on Page Flows"
- imply a gallery was consulted when it was not

Better:
- name the source as a lookup for the user to perform
- reason from the platform guidance, pattern matrices, and quality bars that the skill does hold
- treat a screenshot or description the user pastes as real evidence, reviewable as normal

**Version-bound defaults.** Platform rows such as Material version, predictive back, themed icons, and OS-gated behaviour are current as of this skill's last review, not permanent facts.

Do not:
- state an OS-gated behaviour as universally available
- present a design-system version as the only correct one

Better:
- name the version or OS level the default assumes
- say the default is current as of the skill's last review when it materially affects the recommendation
