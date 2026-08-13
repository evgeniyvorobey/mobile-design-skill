---
name: mobile-design-skill
description: Use when designing, reviewing, specifying, or justifying mobile UI/UX for iOS, Android, or cross-platform products. Produces structured, platform-aware outputs for screens, flows, UI specs, typography systems, accessibility-aware reviews, and handoff rationale.
version: 1.16.0
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
- `docs/clarification-policy.md` for deciding when to ask questions vs proceed with assumptions
- `docs/judged-mode.md` for `/mobile-design-skill --judge` orchestration with an independent judge pass
- `docs/principles.md` for durable mobile design principles
- `docs/guardrails.md` for hard safety, evidence, accessibility, and platform constraints
- `docs/sources.md` for source hierarchy and canonical URLs
- `docs/quality-bars.md` for concrete numeric thresholds (typography, touch, contrast, motion, spacing)
- `docs/design-quality.md` for visual hierarchy, composition, density, typography craft, color semantics, interaction polish, and production-readiness calibration
- `docs/design-quality-rubric.md` for 1-5 quality scoring, target levels, caps, and improvement ladder
- `docs/golden-examples.md` and `examples/golden/` for taste and domain calibration across premium UI, enterprise SaaS, fintech, health, onboarding, settings, and checkout
- `docs/synthetic-case-studies.md` and `examples/case-studies/` for synthetic bad-to-good calibration cases when tuning output quality
- `docs/domain-packs/index.md` and `docs/domain-packs/` for domain-specific mobile playbooks covering fintech, health, SaaS, marketplace, social, and education
- `docs/weaknesses.md` for known failure modes and prevention checks that keep outputs from becoming generic, overconfident, aesthetic-only, or weakly buildable
- `docs/evals.md` for structural, content, and fail-condition evaluation criteria
- `docs/llm-judge-runner.md` and `scripts/run_rubric_judge.py` for semantic rubric fixture calibration, including external-agent command runs during maintenance
- `docs/context-defaults.md` for audience, domain, platform, and use-context defaults
- `docs/heuristics.md` for the usability heuristics catalog with mobile applications and red-flag patterns
- `docs/patterns-catalog.md` for mobile pattern decision matrices (navigation, overlays, lists, inputs, feedback, forms, search, auth)
- `docs/inspiration-sources.md` for visual inspiration and production reference sources, used only after UX/platform/accessibility reasoning is grounded
- `docs/visual-benchmark-playbooks.md` for source-specific Mobbin, Page Flows, Apple Design Awards, and Awwwards benchmark checklists
- `docs/benchmark-report-format.md` and `examples/benchmark-report.md` for turning 3-5 references into borrow / do-not-copy / token-component-state guidance
- `docs/visual-review-fixtures.md` and `examples/visual-review-fixtures/` for text-only Figma-like review fixtures and expected critique discipline
- `docs/rendered-output-qa.md` and `examples/rendered-output-qa/` for optional QA after a design exists as HTML, app build, prototype, screenshot, or recording
- `docs/self-review.md` for the mandatory self-review pass run before any response is returned
- `examples/` for regression-style examples
- `examples/evals/` and `examples/rubric-before-after.md` for design-quality rubric score calibration
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

## Invocation flags

If the request begins with `--judge` or explicitly asks for judge mode, strip the flag before classifying the design task and apply `docs/judged-mode.md`.

Judged mode means:
- draft the response privately using the normal workflow
- run an independent judge pass in the same session when the host supports subagents or parallel reviewers
- revise the draft when the judge score is below 4/5 and the issue can be fixed without inventing facts
- append a compact `Judge summary` section to the final response

Do not ask the user to run `scripts/run_rubric_judge.py` manually for interactive judged mode.

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

If the request matches fintech, health, SaaS, marketplace, social, or education, load the closest domain pack from `docs/domain-packs/` before drafting. Domain packs are synthetic calibration material: they can shape hierarchy, trust language, states, and handoff checks, but they do not prove compliance, user preference, safety, or business performance.

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

### 4. Check information sufficiency and clarification need
Apply `docs/clarification-policy.md`.

If the request is underspecified but safe to answer:
- continue with minimal labeled assumptions
- do not invent research findings
- do not invent validated behavior
- do not invent states, flows, or business rules as facts

If missing information would materially change the recommendation:
- ask at most three clarifying questions
- explain why they block reliable output
- offer a fast path with the smallest safe assumption when useful

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

Use `docs/design-quality-rubric.md` to score the design-quality level from 1-5. For generated or specified artifacts, target 4/5 before returning; if a draft scores 3/5 or below and can be improved without inventing facts, revise it. For reviews, expose both a current and a projected score: the projected number is the flat median of the assessable (non-`n/v`) projected dimensions, stated as a plain number and never as "up to". Any higher figure reachable only after a visual pass belongs in a separate `Ceiling note`, never in the projected number.

Use `docs/synthetic-case-studies.md` and `examples/case-studies/` during maintenance, calibration, or quality-sensitive drafting to compare weak vs strong answer shapes. Treat these examples as synthetic fixtures, not real-world validation.

Use `docs/clarification-policy.md` when the request is underspecified, risky, or precision-sensitive. Ask only when the answer would change the design decision; otherwise proceed with assumptions and surface the unknowns in the appropriate section.

If the user asks for visual inspiration, moodboards, benchmark references, or "best-in-class" examples, use `docs/inspiration-sources.md` as a separate non-authoritative layer. Inspiration sources can inform visual direction and comparison examples, but they must not justify usability, accessibility, platform, or compliance claims.

Use `docs/visual-benchmark-playbooks.md` when the user asks for Mobbin, Page Flows, Apple Design Awards, Awwwards, or source-specific benchmark guidance. Extract visual and flow inspiration, then translate it into implementable mechanisms. Never treat benchmark sources as evidence for usability, accessibility, platform correctness, compliance, user preference, or business performance.

Use `docs/benchmark-report-format.md` when the user asks to compare 3-5 references, benchmark a category, or turn inspiration into design direction. Ask for references only when they materially improve the answer; otherwise proceed with labeled assumptions and keep the output useful.

Use `docs/visual-review-fixtures.md` only as calibration/evaluation material for Mode D text-description reviews. In live reviews, apply the same discipline: qualify visual claims when no screenshot or Figma evidence is provided.

Use `docs/rendered-output-qa.md` only when a rendered artifact exists or the user asks for post-implementation QA. Do not block normal design generation waiting for screenshots, builds, or Playwright. When no artifact exists, list rendered QA as a next action.

Use `docs/weaknesses.md` as an internal preflight whenever a task is ambiguous, high-risk, critique-oriented, or likely to produce a generic design answer. Identify the likely weakness pattern before drafting, then prevent it through tighter assumptions, clearer decisions, evidence limits, state coverage, and buildable mechanisms.

### 6. Build the response by mode
Load the classified mode's section in `skill/modes.md` and follow both its `### Output structure` and its `### Validation checklist`. Use the matching skeleton from `skill/templates.md`.

The mode lists in `## Mode output requirements` below are the same set of sections as `skill/modes.md`, and a parity check keeps them identical. Where the two ever disagree, `skill/modes.md` is authoritative — it carries the per-field detail this file compresses.

### 7. Apply universal review lenses
Before finalizing, check:
- task clarity
- clarification need
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
- design quality score or target from `docs/design-quality-rubric.md` when the response reviews, proposes, specifies, or rationalizes a design artifact
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
- ask clarifying questions only when missing information would materially change the recommendation; otherwise proceed with labeled assumptions
- include design quality calibration when the response proposes, specifies, reviews, or rationalizes a design artifact
- apply the 1-5 design-quality rubric internally; expose the score in reviews and expose the target only when useful for generated artifacts
- apply known weakness prevention before returning; do not expose it as a separate section unless the user asks for a failure-mode analysis
- separate inspiration references from UX, accessibility, and platform rationale when inspiration is used
- end with `Next actions:`

### Sections are a maximum, not a minimum

`Mode:`, `Platform scope:`, `Assumptions:` and `Next actions:` are always on. Every other section listed under `## Mode output requirements` is included only when it carries a decision the input actually supports.

Omit — never stub — a section you would otherwise fill with a placeholder, a restatement of the request, or a generic caution, and name the omission in one line under `Assumptions` so the reader knows it was a choice rather than an oversight. A short request deserves a short answer: a filled-in section with nothing decided in it is worse than an absent one, because it reads as coverage.

This does not license dropping accessibility, states, or platform notes when they are relevant. Those are omitted only when the input genuinely puts them out of scope, and the omission is stated.

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
- Alternatives considered — name two structurally different layout approaches, commit to one, and state the mechanism that kills the other. Two variants of the same structure is not an alternative.

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
- Key decision tradeoffs — for each contested choice, what was given up and why that cost is acceptable here

### Mode 4: Review screen for usability/accessibility
Include:
- Sub-case (D1 / D2 / D3 / D4) — D1 visual evidence, D2 description only, D3 problem statement, D4 context change. Classify explicitly at the top; it sets what may be claimed.
- Quick summary
- Strengths — at least one genuine strength; a review with only negatives is biased, not thorough.
- Findings — one causal chain per finding, never an issue split from its fix: Lens (Usability / Accessibility / Hierarchy & readability / Design quality / Navigation & interaction), Observation, Violated principle (named), User consequence, Change, Predicted effect (directional + confidence), Severity (Nielsen 0–4 = frequency × impact × persistence), Moves (which design-quality dimension it shifts, band→band).
- Design quality score (current → projected) — current and projected scores plus a per-dimension table. The projected number is the flat median of the assessable (non-`n/v`) projected dimensions, not the sum of per-dimension gains; visual dimensions are never projected upward from a text-only review. Any higher number reachable only after a visual pass goes in a separate `Ceiling note`.
- Severity index — findings rolled up by Nielsen 0–4 level.
- Bold move (optional) — include only when all hold: current ≥3/5 but inert, no unresolved severity-3 or severity-4 finding, and a concrete UX upside. Omit the section entirely when the trigger is not met.
- Platform-convention mismatches
- Unresolved assumptions

Do not use the pre-1.16 bucket shape (`Usability issues` / `Accessibility issues` / `Recommended fixes` / `Severity or priority`). Findings carry the lens, the severity, and the fix inside one chain.

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
- Key design decisions — each one carries the alternative that was considered and why it lost; a decision with no rejected alternative is a default, and must be labeled as one
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
- block useful output with nonessential questions

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
