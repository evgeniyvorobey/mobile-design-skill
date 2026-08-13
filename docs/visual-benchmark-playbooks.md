# Visual Benchmark Playbooks

This document defines how to use visual benchmark sources without weakening the skill's evidence hierarchy.

Visual benchmarks are useful for range, calibration, and concrete examples. They are not proof. A reference can show how another product solved, expressed, or framed something, but it cannot validate that the same choice is usable, accessible, platform-correct, compliant, or appropriate for the current product.

Use this document with [`inspiration-sources.md`](inspiration-sources.md). Inspiration sources widen exploration. The normal source hierarchy still decides what is right.

---

## Evidence floor: the skill cannot open these sources

Mobbin, Page Flows, UI Sources and Pttrns require sign-in or a paid subscription; a skill run has no session for them, and a fetch returns a landing page rather than the screens. Apple Design Award and Awwwards pages are public but have not been browsed either.

So these playbooks are **checklists for a benchmark the user runs**, not a description of what those sources currently contain. Extract a principle from a reference the user supplies; never narrate a reference nobody in the conversation has seen. If the user pastes screenshots or notes, that is real evidence and the playbook applies to it directly.

---

## Core rule

Separate visual inspiration and benchmark observations from evidence.

Use benchmarks for:

- visual range
- comparable screen structures
- flow examples
- interaction pacing
- state coverage prompts
- craft calibration
- implementation translation ideas

Do not use benchmarks as evidence for:

- usability
- accessibility
- platform correctness
- legal, privacy, health, finance, or compliance requirements
- user preference
- business performance
- claims that a pattern is "best practice"

Bad:
- "This is accessible because an award-winning app uses it."
- "This checkout flow is correct because it appears on Page Flows."
- "Awwwards proves this motion pattern is appropriate for onboarding."

Better:
- "The flow is grounded in the user's task, platform conventions, and accessibility requirements. Page Flows can provide comparable sequencing examples."
- "The visual direction can be benchmarked against Apple Design Award winners, but text scaling, touch targets, contrast, and navigation behavior still need separate verification."

---

## Benchmark workflow

1. Ground the recommendation first.
   Use official platform guidance, accessibility standards, usability heuristics, domain constraints, implementation constraints, and the user's context before opening benchmark sources.

2. Benchmark visual and flow examples second.
   Use Mobbin, Page Flows, Apple Design Awards, and Awwwards to compare screen structure, hierarchy, visual tone, motion, content density, and sequencing.

3. Translate references into implementable mechanisms.
   Convert observations into tokens, components, states, spacing, typography, interaction rules, motion timings, and QA checks. Do not copy a reference's surface without naming the mechanism it suggests.

4. Label what is evidence and what is inspiration.
   Keep benchmark notes in an `Inspiration references`, `Benchmark observations`, or `Visual direction` section. Keep platform, accessibility, usability, and compliance rationale in separate sections.

5. Re-check the result against the skill's quality bars.
   Confirm contrast, text scaling, touch target size, navigation recovery, content hierarchy, state coverage, and platform fit before presenting the benchmark-backed recommendation.

Sourced discipline: NN/g "Competitive Usability Evaluations" distinguishes competitive *reviews* (expert) from competitive *testing* (users) and warns "you want to beat the competition, not copy them." NN/g "7 Steps to Benchmark Your Product's UX" frames a benchmark as a metric to measure against, never a design to replicate.

---

## Mobbin

Use Mobbin for production UI screen references and product-pattern benchmarking.

### When to use

Use Mobbin when the user asks for:

- mobile app screen examples
- product UI references
- category benchmarking
- onboarding, search, home, detail, paywall, settings, or account screen patterns
- visual density comparison across real products
- practical examples that feel closer to shipped UI than portfolio shots

### What to extract as inspiration

Extract:

- screen composition and information hierarchy
- common component groupings
- density and spacing patterns
- navigation placement and tab structure examples
- empty, loading, paywall, upgrade, and account-state prompts when available
- use of imagery, icons, product cards, lists, and summaries
- differences between consumer, marketplace, finance, health, productivity, and media surfaces

Translate into:

- component inventory
- layout zones
- type roles
- spacing rhythm
- surface and elevation rules
- state checklist prompts
- comparable visual directions, not copied screens

### What NOT to treat as evidence

Do not treat Mobbin as evidence for:

- whether a pattern is usable in the user's context
- whether a screen meets accessibility requirements
- whether the pattern follows current iOS or Android guidance
- whether a conversion, retention, or onboarding choice works
- whether a regulated-domain pattern is compliant
- whether hidden states, error handling, or assistive technology behavior are handled well

### Checklist

Before using Mobbin in output, confirm:

- Is the selected reference from a comparable product category, task, or density level?
- Is the benchmark used after the flow and platform logic are already grounded?
- Are visual observations separated from UX and accessibility rationale?
- Have you translated the reference into concrete mechanisms instead of aesthetic adjectives?
- Have you considered missing states that screenshots may not show?
- Have you checked platform fit for iOS, Android, or cross-platform implementation?

### Red flags

- Copying a layout because it looks polished without matching the user's task.
- Treating a single screenshot as proof of a whole flow.
- Ignoring error, empty, loading, permission, offline, and edge states.
- Using a consumer app reference for a high-trust, regulated, or enterprise workflow without adjusting density and confirmation.
- Assuming a production screenshot is accessible or current.

---

## Page Flows

Use Page Flows for end-to-end journey references and sequencing benchmarks.

### When to use

Use Page Flows when the user asks for:

- onboarding, checkout, subscription, upgrade, search, booking, or account flows
- comparison of step order and branching
- examples of progressive disclosure
- permission, paywall, cancellation, or recovery patterns
- flow audits or redesigns where sequencing matters more than static visuals

### What to extract as inspiration

Extract:

- step sequence and task progression
- entry and exit points
- decision points and branching
- where products ask for permissions, payment, or account creation
- how errors, confirmations, cancellations, or upgrades appear in the journey
- copy placement and timing for trust-building moments
- friction distribution across the flow

Translate into:

- flow maps
- screen-by-screen state requirements
- decision tables
- recovery paths
- navigation rules
- handoff notes for routing and analytics events

### What NOT to treat as evidence

Do not treat Page Flows as evidence for:

- whether the flow has been usability-tested
- whether the step count is optimal
- whether a dark pattern, paywall, or retention tactic is ethical or appropriate
- whether accessibility behavior is correct
- whether a permission sequence follows platform guidance
- whether a legal or subscription disclosure is compliant

### Checklist

Before using Page Flows in output, confirm:

- Is the compared flow solving the same user job?
- Are required platform and domain constraints already identified?
- Are happy path, error path, cancellation, back behavior, and recovery considered?
- Are benchmark observations labeled as examples rather than proof?
- Are friction points translated into explicit design decisions?
- Are compliance-sensitive moments reviewed against authoritative sources, not the benchmark?

### Red flags

- Treating a competitor's retention or paywall flow as acceptable without ethical and platform review.
- Copying account creation timing without considering user trust and value exchange.
- Using a captured flow as if it represents all states or all user segments.
- Ignoring back navigation, cancellation, offline, timeout, or failed payment behavior.
- Measuring quality only by fewer steps instead of task clarity, control, and recovery.

---

## Apple Design Awards

Use Apple Design Awards for high-craft platform inspiration and calibration of polished iOS experiences.

### When to use

Use Apple Design Awards when the user asks for:

- iOS craft references
- platform-native polish
- interaction quality examples
- accessibility or inclusivity inspiration
- high-end consumer experience direction
- refined motion, haptics, typography, content presentation, or delight

### What to extract as inspiration

Extract:

- clarity of hierarchy and focus
- use of system conventions with expressive brand moments
- content-first composition
- tasteful motion and feedback patterns
- onboarding tone and progressive learning
- accessibility-conscious product thinking when explicitly visible or discussed
- ways exceptional apps balance personality with usability

Translate into:

- platform-aware interaction principles
- motion intent and reduced-motion requirements
- typography and content hierarchy mechanisms
- native component usage notes
- polish criteria for feedback, transitions, empty states, and success states

### What NOT to treat as evidence

Do not treat Apple Design Awards as evidence for:

- official HIG rules
- automatic accessibility compliance
- permission to copy a distinctive interaction or visual identity
- suitability for Android or cross-platform behavior
- suitability for dense enterprise, regulated, or low-bandwidth contexts
- proof that a visually ambitious pattern is appropriate for the user's task

Use Apple Human Interface Guidelines, Apple accessibility guidance, and relevant standards for evidence. Use award winners for inspiration and craft calibration.

### Checklist

Before using Apple Design Awards in output, confirm:

- Is the benchmark being used for craft calibration rather than policy?
- Are HIG and accessibility requirements checked separately?
- Is the reference relevant to the user's app type and interaction model?
- Are expressive details translated into native mechanisms, states, and constraints?
- Are platform-specific assumptions labeled if the user's product is not iOS-only?
- Are motion and visual effects paired with reduced-motion and contrast considerations?

### Red flags

- Saying a choice is "Apple-approved" because an award winner uses something similar.
- Importing a game, media, or creative-app interaction into a utility workflow without task justification.
- Treating delight as more important than clarity, speed, or control.
- Copying distinctive art direction or interaction identity instead of extracting a principle.
- Forgetting that award pages are curated storytelling, not a full implementation audit.

---

## Awwwards

Use Awwwards for web craft, expressive visual direction, typography, layout, and motion inspiration.

### When to use

Use Awwwards when the user asks for:

- visual exploration
- high-impact landing, editorial, campaign, or brand surfaces
- motion and interaction inspiration
- typography and layout range
- premium visual direction
- web-to-mobile adaptation ideas for expressive products

Use it carefully for mobile app work. Awwwards is often web-first, campaign-heavy, and optimized for visual impact rather than repeated mobile task completion.

### What to extract as inspiration

Extract:

- typography mood and scale relationships
- image treatment and art direction
- transition ideas and motion intent
- editorial pacing
- brand expression
- visual rhythm across sections
- ways to create memorable first impressions

Translate into:

- restrained mobile visual language
- token-ready type, color, spacing, and motion rules
- hero or onboarding art direction
- interaction polish for low-risk moments
- implementation-safe animation and performance requirements

### What NOT to treat as evidence

Do not treat Awwwards as evidence for:

- mobile usability
- native app platform behavior
- accessibility compliance
- performance suitability
- checkout, forms, authentication, healthcare, finance, or government-service UX
- whether an experimental motion pattern is safe for repeated use
- whether contrast, reduced motion, keyboard navigation, or screen reader behavior is acceptable

### Checklist

Before using Awwwards in output, confirm:

- Is the task suited to expressive visual inspiration?
- Is the reference being adapted to mobile constraints rather than copied?
- Have accessibility, motion sensitivity, contrast, and performance risks been called out?
- Is the visual idea translated into components, tokens, and fallback states?
- Is the expressive moment kept away from high-risk tasks unless justified?
- Are platform and usability decisions grounded elsewhere?

### Red flags

- Using scroll effects, parallax, or complex motion in task-critical mobile flows.
- Treating a desktop editorial layout as a mobile app layout.
- Letting visual spectacle reduce readability, touch clarity, or state legibility.
- Recommending low-contrast type because it looks premium in a showcase.
- Ignoring performance and battery cost for animation-heavy directions.

---

## Output pattern

When benchmark sources are used, keep the response structured like this:

```md
## Evidence basis
- Platform/accessibility/usability sources used for decisions:
- Constraints from the user's context:
- Compliance or domain assumptions:

## Benchmark observations
- Source:
- Comparable surface or flow:
- Useful inspiration:
- Limits of the reference:

## Implementable translation
- Components:
- Type/spacing/color tokens:
- States:
- Motion/feedback:
- QA checks:
```

Do not merge `Evidence basis` and `Benchmark observations`. The separation is what keeps the recommendation honest.

---

## Maintenance

- Keep these playbooks focused on how to use benchmark sources, not on source marketing.
- Revisit the source list when `docs/inspiration-sources.md` changes.
- Remove or demote a source if it becomes low-signal, inaccessible, or mostly irrelevant to mobile product work.
- Add new playbooks only when they change how outputs should be produced.
