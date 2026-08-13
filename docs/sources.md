# Source Hierarchy

This skill uses a deliberate source hierarchy.

The goal is to keep outputs grounded in durable, practical guidance rather than transient trend material.

This file now serves two purposes:

1. it defines the source-priority logic used by the skill
2. it preserves a GitHub-readable appendix of canonical public URLs

The URL appendix was consolidated during repository preparation from an external curation document titled `Curated Learning Map for Mobile UI/UX Design Using US and European Sources` (`Design thinking.pdf`).

---

## Priority order

### 1. Official platform guidance and standards
Use first when platform behavior, component choice, layout norms, navigation, or accessibility expectations are at stake.

Primary references:
- Apple Human Interface Guidelines
- Material Design 3
- Android Developers Navigation
- Apple accessibility guidance
- Apple typography guidance
- Material accessibility and typography guidance

Use these for:
- native interaction expectations
- platform component and layout decisions
- platform-specific navigation behavior
- typography and scaling expectations
- accessibility behavior tied to platform conventions

---

### 2. Accessibility and usability standards
Use when evaluating whether design decisions support inclusive, effective, efficient interaction.

Primary references:
- WCAG 2.2
- W3C guidance for applying WCAG 2.2 to mobile apps
- ISO 9241-210
- ISO 9241-11
- ETSI EN 301 549 when EU/public-sector context matters

Use these for:
- usability framing
- accessibility interpretation
- context-of-use reasoning
- lifecycle and human-centered process framing
- mobile-specific application of accessibility criteria

---

### 3. Public-sector and enterprise-grade design systems
Use when you need practical, maintained, low-drama patterns for real services and high-trust or dense workflows.

Primary references:
- GOV.UK Design System patterns
- NHS Design System
- NHS App Design System
- NHS typography guidance
- Fluent 2 typography/accessibility
- SAP Fiori mobile guidance for enterprise cases
- USWDS typography/accessibility as supporting practical system references

Use these for:
- forms
- task flows
- high-trust services
- readability calibration
- system thinking for typography and accessibility
- enterprise mobile patterns

---

### 4. Established research and case-study sources
Use when official guidance does not fully answer design tradeoffs or when learning from production examples.

Primary references:
- Nielsen Norman Group mobile UX guidance (incl. severity ratings and "Making Usability Findings Actionable")
- Baymard mobile UX research
- Luke Wroblewski, *Web Form Design* (form and input patterns)
- Jon Yablonski, *Laws of UX* (umbrella for Fitts, Hick, Doherty, Jakob, Aesthetic-Usability)
- Material Partner Studies
- Apple design videos and resources
- Android adaptive app stories
- selected first-party design-system case studies

Use these for:
- usability pitfalls
- common failure modes
- practical examples of adoption
- case-based reasoning
- validation and learning patterns

Do not turn these into fake statistics or fabricated findings.

---

### 5. Workflow and tooling references
Use last, after interaction and usability decisions are already grounded.

Primary references:
- Figma components, libraries, and variables guidance
- Apple design resources
- Framer components workflow
- Sketch libraries
- accessibility testing tooling references

Use these for:
- tokenization
- component organization
- shared library structure
- handoff practicality
- prototyping and workflow support

Tooling should support design quality, not substitute for it.

---

## Design quality calibration layer

Design quality calibration is defined separately in [`design-quality.md`](design-quality.md).

Use it when an output proposes, critiques, specifies, or rationalizes:

- visual hierarchy
- composition and spacing
- typography craft
- color semantics
- density and rhythm
- interaction polish and motion
- brand expression
- production readiness

This layer interprets the source hierarchy above into practical quality checks. It does not supersede platform guidance, accessibility standards, or quality bars.

---

## Clarification policy layer

Clarification behavior is defined separately in [`clarification-policy.md`](clarification-policy.md).

Use it when task inputs are underspecified, risky, or precision-sensitive. This layer decides whether to:

- proceed with minimal labeled assumptions
- ask one to three blocking questions
- offer a provisional fast path
- move uncertainty to `Unresolved assumptions`, `Open questions`, or `Next actions`

The policy protects both speed and accuracy. It prevents the skill from blocking useful output with nonessential questions, and it prevents overconfident recommendations when missing context would materially change the design.

---

## Design quality rubric layer

The 1-5 design-quality scoring rubric is defined separately in [`design-quality-rubric.md`](design-quality-rubric.md).

Use it to:

- derive the quality score from the assessable dimensions before returning generated design artifacts, rather than aiming at a number
- expose current quality score in design reviews
- prevent serious weaknesses from being averaged away by visual polish
- define the improvement ladder from baseline to strong and resilient

The rubric is a synthesis tool. It does not create evidence by itself and must still defer to platform guidance, accessibility standards, quality bars, and known weakness prevention.

---

## Known weaknesses prevention layer

Known weakness patterns are defined separately in [`weaknesses.md`](weaknesses.md).

Use this layer as internal preflight and regression memory when a task is likely to trigger:

- generic output on underspecified input
- template completion without real decisions
- first-idea bias
- aesthetic laundering
- evidence overreach
- platform flattening
- context blindness
- happy-path-only design
- visual overclaim in reviews
- weak handoff and buildability

This layer does not add new evidence. It protects the source hierarchy by forcing the response to stay specific, honest, context-aware, and buildable.

---

## Non-authoritative inspiration layer

The inspiration layer is defined separately in [`inspiration-sources.md`](inspiration-sources.md).

Use it only when the user asks for visual inspiration, moodboards, competitive references, production examples, or "best-in-class" examples.

Inspiration sources are not part of the evidence hierarchy above. They can help with:

- visual range
- comparable production surfaces
- moodboard direction
- interaction examples
- pattern benchmarking

They must not be used for:

- official platform behavior
- accessibility claims
- compliance claims
- usability proof
- fabricated trend or popularity claims

### Distinctiveness and creative-range references

These inform visual range and the distinctiveness levers in [`design-quality.md`](design-quality.md). They are NOT evidence for usability, accessibility, platform correctness, or compliance.

- Marty Neumeier, *Zag* / *The Brand Gap* (radical differentiation, the Onlyness test)
- Byron Sharp & Jenni Romaniuk, *Building Distinctive Brand Assets* (fame × uniqueness)
- Noriaki Kano, the Kano model (must-be / performance / attractive quality)
- Don Norman, *Emotional Design* (visceral / behavioral / reflective)
- Aarron Walter, *Designing for Emotion*; Stephen Anderson, *Seductive Interaction Design*
- Alla Kholmatova, *Design Systems* (functional vs. perceptual patterns)
- Val Head, *Designing Interface Animation*; Disney's twelve principles of animation
- Ellen Lupton, *Thinking with Type* (typographic personality)

---

## Core 15 reference set

The skill is anchored to the following core set:

1. Apple Human Interface Guidelines
2. Material Design 3
3. Android Developers Navigation
4. Nielsen Norman Group mobile UX guidance
5. Baymard mobile UX research
6. WCAG 2.2
7. W3C guidance for applying WCAG 2.2 to mobile apps
8. ETSI EN 301 549 overview
9. ISO 9241-210
10. ISO 9241-11
11. GOV.UK Design System patterns
12. NHS Design System
13. Fluent 2 typography/accessibility
14. Figma Variables guidance
15. Material Partner Studies

---

## Source application rules

### Use official guidance first
If Apple, Material, or Android navigation directly address the issue, prefer those references over secondary commentary.

### Use standards to frame quality, not to fake certainty
Standards help structure reasoning. They do not authorize unsupported compliance claims.

### Use public-sector systems as practical calibration
GOV.UK and NHS are useful when the design needs:
- clarity
- trust
- lower cognitive load
- better readability
- more predictable task completion

### Use case studies to understand adaptation, not to copy surfaces
The point is to learn:
- what changed
- why it worked
- how system constraints were preserved

### Use tooling references only after interaction decisions are clear
Figma variables are for scaling decisions that already make sense, not for laundering bad structure into official-looking tokens.

---

## Source-to-task mapping

### Best sources for navigation and flow
- Apple HIG
- Material Design 3
- Android Navigation guidance
- GOV.UK patterns

### Best sources for accessibility
- WCAG 2.2
- W3C mobile WCAG guidance
- Apple accessibility guidance
- Material accessibility guidance
- NHS accessibility guidance

### Best sources for typography and spacing
- Apple typography
- Material typography
- Fluent 2 typography
- GOV.UK type scale
- NHS typography
- Google Fonts line-height guidance

### Best sources for human-centered process
- ISO 9241-210
- ISO 9241-11
- UK Government Design Principles
- Double Diamond
- inclusive user research guidance

### Best sources for scalable systems and handoff
- Figma variables guidance
- public design systems
- case studies showing token/system adoption

---

## Practical interpretation for this skill

When generating outputs:

- prefer the most authoritative relevant source family
- distinguish facts from recommendations
- avoid unsupported absolutes
- keep outputs operational
- include platform-specific splits only where they materially matter

---

## Canonical URL appendix

These are the normalized public links maintainers can cite, verify, or review when updating the skill.

### Foundations

- [ISO 9241-210: Human-centred design for interactive systems](https://www.iso.org/standard/77520.html)
- [ISO 9241-11: Usability definitions and concepts](https://www.iso.org/standard/63500.html)
- [Design Council Double Diamond](https://www.designcouncil.org.uk/our-resources/the-double-diamond/)
- [UK Government Design Principles](https://www.gov.uk/guidance/government-design-principles)

### Adaptive layout and large screens

- [Apple HIG: Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Apple HIG: Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking)
- [Apple HIG: Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)
- [Material 3: Applying layout / window size classes](https://m3.material.io/foundations/layout/applying-layout/window-size-classes)
- [Material 3: Canonical layouts](https://m3.material.io/foundations/layout/canonical-layouts/overview)
- [Android: Use window size classes](https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes)
- [Android: Large screen app quality](https://developer.android.com/docs/quality-guidelines/large-screen-app-quality)

### Platform and pattern guidance

- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Apple layout guidance](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Material Design 3](https://m3.material.io/)
- [Android Developers Navigation](https://developer.android.com/guide/navigation)
- [SAP Fiori for iOS](https://www.sap.com/design-system/fiori-design-ios/fiori-design-ios)
- [SAP Fiori for Android](https://www.sap.com/design-system/fiori-design-android/)
- [GOV.UK Design System patterns](https://design-system.service.gov.uk/patterns/)
- [NHS Design System](https://service-manual.nhs.uk/design-system)
- [NHS App Design System](https://design-system.nhsapp.service.nhs.uk/)
- [Android large-screen/adaptive stories](https://developer.android.com/large-screens/stories)

### Research and usability

- [Nielsen Norman Group mobile UX study guide](https://www.nngroup.com/articles/mobile-ux-study-guide/)
- [Nielsen Norman Group touch target size](https://www.nngroup.com/articles/touch-target-size/)
- [Nielsen Norman Group mobile usability testing](https://www.nngroup.com/articles/mobile-usability-testing/)
- [Nielsen Norman Group usability testing 101](https://www.nngroup.com/articles/usability-testing-101/)
- [Baymard mobile app research](https://baymard.com/research/mobile-app)
- [Baymard checkout UX research](https://baymard.com/blog/current-state-of-checkout-ux)
- [GOV.UK Service Manual user research](https://www.gov.uk/service-manual/user-research)
- [NHS accessibility guidance for user research](https://service-manual.nhs.uk/accessibility/user-research)

### Typography

- [Apple typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography)
- [Apple fonts and SF](https://developer.apple.com/fonts/)
- [Material Design 3 typography](https://m3.material.io/styles/typography/applying-type)
- [Fluent 2 typography](https://fluent2.microsoft.design/typography)
- [Google Fonts Knowledge: suitable line height](https://fonts.google.com/knowledge/using_type/choosing_a_suitable_line_height)
- [GOV.UK type scale](https://design-system.service.gov.uk/styles/type-scale/)
- [U.S. Web Design System typography](https://designsystem.digital.gov/components/typography/)
- [NHS typography](https://service-manual.nhs.uk/design-system/styles/typography)

### Accessibility

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [W3C guidance on applying WCAG 2.2 to mobile apps](https://www.w3.org/TR/wcag2mobile-22/)
- [ETSI EN 301 549 overview](https://www.etsi.org/human-factors-accessibility/en-301-549-v3-the-harmonized-european-standard-for-ict-accessibility)
- [Apple accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [Material accessibility foundations](https://m3.material.io/foundations/overview/principles)
- [Material text resizing guidance](https://m3.material.io/foundations/writing/text-resizing)
- [U.S. Web Design System accessibility](https://designsystem.digital.gov/documentation/accessibility/)

### Design systems, workflow, and tools

- [Adobe Spectrum inclusive design](https://spectrum.adobe.com/page/inclusive-design/)
- [Apple Design](https://developer.apple.com/design/)
- [Apple Design Resources](https://developer.apple.com/design/resources/)
- [Material Partner Studies](https://m3.material.io/blog/material-partner-studies)
- [Uber design system at scale](https://www.uber.com/blog/design-system-at-scale/)
- [Monzo writing system](https://monzo.com/blog/weve-made-our-writing-system-available-to-all)
- [Figma components, styles, and shared libraries](https://www.figma.com/best-practices/components-styles-and-shared-libraries/)
- [Figma Variables guide](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
- [Sketch libraries](https://www.sketch.com/docs/libraries/)
- [Framer components workflow](https://www.framer.com/academy/lessons/framer-fundamentals-components)
- [Deque Axe accessibility tools](https://www.deque.com/axe/)

### Creative methods and exploration

- [IDEO Design Thinking](https://designthinking.ideo.com/)
- [IDEO.org Design Kit](https://www.designkit.org/resources/1.html)
- [Stanford d.school Design Thinking Bootleg](https://dschool.stanford.edu/tools/design-thinking-bootleg)
- [Google Design expressive design research](https://design.google/library/expressive-material-design-google-research)
- [Edward de Bono — Lateral Thinking](https://www.debonogroup.com/services/core-programs/lateral-thinking/)
- [SCAMPER technique](https://en.wikipedia.org/wiki/SCAMPER)
- [Jobs-to-be-Done (Strategyn / Ulwick)](https://strategyn.com/jobs-to-be-done/)
- [Google Design Sprint Kit — Crazy 8s](https://designsprintkit.withgoogle.com/methodology/phase3-sketch/crazy-8s)
