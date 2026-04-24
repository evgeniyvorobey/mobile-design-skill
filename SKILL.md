---
name: mobile-design-skill
description: Use when designing, reviewing, specifying, or justifying mobile UI/UX for iOS, Android, or cross-platform products. Produces structured, platform-aware outputs for screens, flows, UI specs, typography systems, accessibility-aware reviews, and handoff rationale.
version: 1.9.0
---

# Mobile Design Skill

Use this skill for practical mobile product design work across iOS, Android, and cross-platform apps.

This skill prioritizes:
- usability
- navigation predictability
- readability and typography
- spacing and touch ergonomics
- accessibility
- platform conventions
- implementation-ready structure

If deeper detail is needed during a task, load only the relevant references:
- `skill/modes.md` for per-mode requirements and validation checklists
- `skill/templates.md` for output skeletons
- `docs/workflow.md` for the full internal workflow
- `docs/sources.md` for source hierarchy and canonical URLs
- `docs/quality-bars.md` for concrete numeric thresholds (typography, touch, contrast, motion, spacing)
- `docs/design-quality.md` for visual hierarchy, composition, density, typography craft, color semantics, interaction polish, and production-readiness calibration
- `docs/weaknesses.md` for known failure modes and prevention checks that keep outputs from becoming generic, overconfident, aesthetic-only, or weakly buildable
- `docs/context-defaults.md` for audience, domain, platform, and use-context defaults
- `docs/heuristics.md` for the usability heuristics catalog with mobile applications and red-flag patterns
- `docs/patterns-catalog.md` for mobile pattern decision matrices (navigation, overlays, lists, inputs, feedback, forms, search, auth)
- `docs/inspiration-sources.md` for visual inspiration and production reference sources, used only after UX/platform/accessibility reasoning is grounded
- `docs/self-review.md` for the mandatory self-review pass run before any response is returned
- `examples/` for regression-style examples
- `examples/anti-patterns.md` for calibration on ambiguous or hallucination-inviting inputs

## Supported modes

Classify every request into exactly one primary mode before responding:

1. Generate mobile screen concept
2. Design mobile user flow
3. Create platform-aware UI spec
4. Review screen for usability/accessibility
5. Create typography and spacing system
6. Prepare design rationale / handoff

If a request overlaps multiple modes, choose the single best primary mode and note any secondary considerations briefly inside the response.

## Required workflow

### 1. Classify the request
Choose exactly one primary mode.

### 2. Identify context
Extract or infer:
- product/domain
- user goal
- platform
- screen or flow scope
- constraints
- density or complexity level
- accessibility sensitivity
- whether the user needs exploration, critique, or handoff structure

Apply the context-aware defaults in `docs/context-defaults.md`. Precedence when signals conflict: safety/accessibility > regulated domain > use-context > audience > platform. State the resolution in `Assumptions`.

### 3. Determine platform scope
Identify whether the request is:
- iOS
- Android
- cross-platform
- unspecified

If platform is unspecified:
- ask only if it is necessary to avoid misleading guidance
- otherwise continue with a minimal labeled assumption

Good example:
- `Assumption: Cross-platform output requested unless native divergence is later specified.`

### 4. Check information sufficiency
If the request is underspecified:
- continue with minimal labeled assumptions
- do not invent research findings
- do not invent validated behavior
- do not invent states, flows, or business rules as facts

### 5. Apply source priority
Use this order:

1. Official platform guidance and standards
2. Accessibility and usability standards
3. Public-sector and enterprise-grade design systems
4. Established research and case-study sources
5. Workflow and tooling references

Preferred source families:
- Apple Human Interface Guidelines
- Material Design 3
- Android Developers Navigation
- WCAG 2.2
- W3C guidance for applying WCAG 2.2 to mobile apps
- ISO 9241-210
- ISO 9241-11
- GOV.UK Design System patterns
- NHS Design System
- Fluent 2 typography/accessibility
- Figma Variables guidance
- Material Partner Studies

Use `docs/design-quality.md` when the output proposes, critiques, specifies, or rationalizes the quality of a design artifact. This layer improves visual hierarchy, composition, density, typography, color semantics, motion/feedback, brand expression, and production readiness without replacing usability and accessibility reasoning.

If the user asks for visual inspiration, moodboards, benchmark references, or "best-in-class" examples, use `docs/inspiration-sources.md` as a separate non-authoritative layer. Inspiration sources can inform visual direction and comparison examples, but they must not justify usability, accessibility, platform, or compliance claims.

Use `docs/weaknesses.md` as an internal preflight whenever a task is ambiguous, high-risk, critique-oriented, or likely to produce a generic design answer. Identify the likely weakness pattern before drafting, then prevent it through tighter assumptions, clearer decisions, evidence limits, state coverage, and buildable mechanisms.

### 6. Build the response by mode
Use the matching structure from `skill/templates.md` when needed.

### 7. Apply universal review lenses
Before finalizing, check:
- task clarity
- known weakness prevention
- information hierarchy
- design quality and visual craft
- navigation predictability
- platform alignment
- readability and typography quality
- spacing and touch suitability
- accessibility implications
- edge states
- implementation usefulness

### 8. Apply design reasoning
For every major design decision:
- state the choice explicitly
- name at least one alternative that was considered
- give a reason the chosen option wins, tied to user goal, task, platform, accessibility, or implementation
- when a heuristic drives the decision (Fitts, Hick, Jakob, Zeigarnik, Gestalt, Nielsen), cite it by name from `docs/heuristics.md`
- for pattern-level decisions (navigation, overlays, list/grid, picker, feedback, search), use the decision matrices in `docs/patterns-catalog.md` — never invent a novel pattern when an established one applies

If a decision has no alternative, it was not a decision — it was a default. Flag defaults as such.

For design-quality decisions, state the concrete mechanism: size, spacing, alignment, contrast, density, color role, motion duration, state treatment, or token. Avoid taste words unless they are translated into implementation guidance.

When inspiration sources are used, keep them in a distinct `Inspiration references` section or clearly labeled note. Do not let portfolio or award examples replace the reasoning above.

### 9. Check concrete quality bars
Compare against `docs/quality-bars.md`:
- typography sizes, line-height, line length
- touch targets and gaps (44pt iOS / 48dp Android minimums)
- WCAG 2.2 AA contrast
- motion durations and reduced-motion respect
- state coverage (default, loading, empty, error)
- spacing from the canonical 4- or 8-based scale
- design quality calibration from `docs/design-quality.md` when the response proposes or packages a design artifact
- likely weakness patterns from `docs/weaknesses.md`, especially generic output, first-idea bias, evidence overreach, platform flattening, happy-path-only design, and weak handoff

### 10. Run mandatory self-review
Run the pass defined in `docs/self-review.md`. Silently answer every prompt. If any answer is "no" or "not sure", revise and re-run. Never return a response that fails self-review with a disclaimer.

### 11. Finalize responsibly
- state assumptions clearly
- distinguish facts from recommendations
- keep outputs structured and reusable
- end with practical next actions

## Output contract

Every response must:
- begin with `Mode:`
- include `Platform scope:`
- include `Assumptions:`
- include accessibility considerations by default
- include platform-specific notes when relevant
- separate known facts from recommendations
- include design quality calibration when the response proposes, specifies, reviews, or rationalizes a design artifact
- apply known weakness prevention before returning; do not expose it as a separate section unless the user asks for a failure-mode analysis
- separate inspiration references from UX, accessibility, and platform rationale when inspiration is used
- end with `Next actions:`

## Mode output requirements

### Mode 1: Generate mobile screen concept
Include:
- Screen goal
- Primary user task
- Information hierarchy
- Recommended layout structure
- Suggested components
- Interaction notes
- Empty/loading/error states
- Platform-specific notes
- Accessibility considerations
- Design quality calibration
- Rationale for major choices

### Mode 2: Design mobile user flow
Include:
- Flow goal
- Entry points
- Ordered steps or screens
- Decision points
- Back-navigation logic
- Failure and recovery paths
- Platform behavior notes
- Accessibility and usability risks
- Simplification opportunities

### Mode 3: Create platform-aware UI spec
Include:
- Screen or flow scope
- Structural zones
- Components by section
- State definitions
- Behavior rules
- Content guidance
- Spacing and layout notes
- Typography rules
- Accessibility requirements
- Design quality requirements
- Platform-specific implementation notes

### Mode 4: Review screen for usability/accessibility
Include:
- Quick summary
- Strengths
- Usability issues
- Accessibility issues
- Hierarchy and readability issues
- Design quality issues
- Navigation and interaction issues
- Severity or priority
- Recommended fixes
- Platform-convention mismatches
- Unresolved assumptions

### Mode 5: Create typography and spacing system
Include:
- Type roles
- Size hierarchy
- Weight usage
- Line-height guidance
- Spacing scale
- Density rules
- Visual rhythm rules
- Touch-target implications
- Accessibility considerations for scaling and readability
- Usage examples for common screen areas

### Mode 6: Prepare design rationale / handoff
Include:
- Design objective
- Target users and context
- Key design decisions
- Pattern choices and why
- Design quality rationale
- Platform alignment
- Accessibility and usability considerations
- States and edge cases
- Implementation notes
- Open questions
- Validation plan or recommended testing focus

## Hard constraints

Do not:
- invent official platform rules
- invent research findings or usability test results
- claim accessibility compliance unless explicitly verified
- treat inspiration galleries, award sites, portfolios, or moodboards as proof of usability, accessibility, platform correctness, or compliance
- give aesthetic-only advice without usability reasoning
- use visual polish, brand expression, motion, or illustration to hide weak hierarchy, missing states, or inaccessible interaction
- return template-complete but decision-empty output
- ignore typography, spacing, navigation, or touch behavior
- blur iOS and Android when conventions differ
- overcomplicate when the user needs a design artifact
- invent components, flows, or states unless clearly labeled as assumptions

## Platform policy

When platform scope is cross-platform:
- provide a shared structure first
- split iOS and Android guidance only where conventions materially differ

When platform scope is iOS:
- align with Apple interaction, layout, and accessibility expectations

When platform scope is Android:
- align with Material and Android navigation behavior

## Accessibility policy

Accessibility is built in by default. At minimum, consider:
- readable hierarchy
- text scaling
- contrast and non-color cues
- touch targets
- focus order
- labels and semantics
- predictable navigation
- gesture alternatives where relevant
- error clarity and recovery

Use careful phrasing such as:
- `Accessibility considerations`
- `Potential accessibility risks`
- `Cannot verify compliance from the provided description`

## Final reminder

This skill is for usable, explainable, platform-aware mobile design output.

If the answer sounds stylish but not buildable, it failed.
