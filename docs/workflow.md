# Internal Workflow

This document defines the internal workflow the skill must follow for every request.

---

## Step 1: Classify the request

Choose exactly one primary mode:

1. Generate mobile screen concept
2. Design mobile user flow
3. Create platform-aware UI spec
4. Review screen for usability/accessibility
5. Create typography and spacing system
6. Prepare design rationale / handoff

### Classification intent cues

#### Generate mobile screen concept
Use when the user wants:
- a new screen idea
- first-pass structure
- content hierarchy
- layout/component recommendations

#### Design mobile user flow
Use when the user wants:
- ordered steps
- navigation logic
- path design
- recovery and branching

#### Create platform-aware UI spec
Use when the user wants:
- implementation-ready structure
- section-by-section component breakdown
- explicit states and behavior
- detailed design handoff

#### Review screen for usability/accessibility
Use when the user wants:
- critique
- issue finding
- usability review
- accessibility review
- prioritization of problems

#### Create typography and spacing system
Use when the user wants:
- type roles
- hierarchy
- line-height guidance
- spacing scale
- density rules

#### Prepare design rationale / handoff
Use when the user wants:
- explanation of decisions
- handoff notes
- justification
- design summary for cross-functional use

---

### If the request matches no mode

Do not round it to the nearest template. Paywall and pricing architecture, notification strategy, whole-app information architecture, activation strategy, competitive teardown, design-system governance and multi-brand theming are real mobile design work that none of the six modes covers.

Open with `Mode: outside the standard six — [what this actually is]`, name the closest mode and what it would lose, then answer with the reasoning steps below and no template. Keep the header lines and `Next actions`; the rest of the output contract is advisory here.

---

## Step 2: Identify context

Extract or infer:

- product/domain
- user goal
- platform
- screen or flow scope
- constraints
- density or complexity level
- accessibility sensitivity
- whether the user needs exploration, critique, or handoff structure

### Useful context prompts internally
- What is the user trying to accomplish?
- Is this phone-first or broader adaptive/mobile? Resolve device class (phone / tablet / foldable / adaptive) as a second axis alongside platform scope, and load `docs/adaptive-layout.md` when it is anything but phone.
- Is the product consumer, enterprise, high-trust, regulated, or utility-focused?
- Does this require platform divergence?
- Is readability or density a major concern?
- Is the user asking for concept generation, critique, or structured documentation?

### Apply context-aware defaults

Once the context is classified, consult `docs/context-defaults.md` for the defaults tuned to that context (audience × domain × platform × use-context). Apply those defaults as starting points for typography, touch, density, confirmation, motion, and related decisions.

Conflict resolution order (when signals disagree):

1. Safety and accessibility constraints
2. Regulated domain constraints (finance, health, government)
3. Use-context constraints (driving, outdoor, emergency)
4. Audience constraints
5. Platform defaults

When multiple contexts apply, state the resolution in `Assumptions` so the user can correct a misclassification.

---

## Step 3: Check information sufficiency

Determine whether the request includes enough information for the chosen mode.

Use `docs/clarification-policy.md` to decide whether to ask questions or proceed with assumptions.

### If sufficient
Proceed directly.

### If partially sufficient
Continue with minimal labeled assumptions.

### If clarification is required
Ask at most three clarifying questions when a missing answer would materially change the recommendation.

The response should include:

- best inferred mode
- platform scope
- assumptions
- `Clarifying questions`
- `Why this blocks`
- optional `Fast path`
- `Next actions`

Do not ask non-blocking questions before producing useful work.

### If severely underspecified
Still provide a useful structure, but:
- limit specificity
- state missing inputs clearly
- avoid invented certainty

---

## Step 4: Select source priority

Use the source hierarchy in this order:

1. Official platform guidance and standards
2. Accessibility and usability standards
3. Public-sector and enterprise-grade design systems
4. Established research and case-study sources
5. Workflow and tooling references

### Decision rules
- Use Apple HIG for iOS-specific interaction, layout, and typography interpretation.
- Use `docs/clarification-policy.md` when missing input could materially change platform, task, accessibility, safety, compliance, or implementation guidance.
- Use Material Design 3 and Android Navigation for Android and cross-platform mobile structure where Android behavior matters.
- Use WCAG 2.2 and W3C mobile guidance for accessibility framing.
- Use ISO usability and HCD framing when decisions need justification through context of use and lifecycle reasoning.
- Use GOV.UK and NHS when clarity, service design, task completion, readability, and high-trust patterns matter.
- Use Fluent 2 and related guidance when cross-platform type hierarchy needs coherence.
- Use Figma Variables guidance when outputs need token-friendly structure.
- Use `docs/design-quality.md` when the output proposes, critiques, specifies, or rationalizes a design artifact's hierarchy, composition, density, typography craft, color semantics, interaction polish, brand expression, or production readiness.
- Use `docs/design-quality-rubric.md` when the output needs a 1-5 quality target or review score. Generated/specification outputs derive the score from the assessable dimensions; Mode D reviews expose both a current and a projected score.
- Use `docs/domain-packs/index.md` and the closest pack in `docs/domain-packs/` when fintech, health, SaaS, marketplace, social, or education materially changes trust, safety, hierarchy, state coverage, or handoff requirements.
- Use `docs/synthetic-case-studies.md` and `examples/case-studies/` during maintenance or quality-sensitive calibration to compare weak vs strong response shapes. Do not treat synthetic cases as real-world validation.
- Use `docs/inspiration-sources.md` only when the user asks for visual inspiration, moodboards, benchmarks, or "best-in-class" examples. Treat it as a non-authoritative layer for visual range and production references, not as evidence for usability, accessibility, platform behavior, or compliance.
- Use `docs/benchmark-report-format.md` when a request asks to compare 3-5 references or turn benchmark inspiration into tokens, components, states, and QA checks.
- Use `docs/visual-review-fixtures.md` as maintenance calibration for Mode D text-description reviews and apply the same evidence limits in live reviews.
- Use `docs/rendered-output-qa.md` only after a rendered artifact exists or when the user asks for post-implementation QA. It is optional and must not block normal design generation.
- Use `docs/weaknesses.md` as an internal preflight when the task could invite generic output, unsupported claims, first-idea bias, platform flattening, happy-path-only flow design, or weak handoff.

---

## Step 4.5: Set the design direction (Modes A, C, E)

Before drafting a generated artifact, build three candidate directions internally, then commit to one. The step sits between grounding and building so divergence happens *before* the evidence gauntlet, not instead of it.

**Two of the three come from a catalog, not from instinct.** D1 is the conventional baseline implied by `patterns-catalog.md` and the domain pack; D2 is a named compositional school and D3 a named point-of-view product, both from `inspiration-sources.md`. Discard entries their `Do NOT use for` line disqualifies, then from the survivors take the one whose token consequences differ *most* from D1 — not the first that fits. Every direction carries `from:` its source into the output. A free-generated candidate set is unimodal; that is why this is a retrieval step and not a brainstorm.

Each direction is a thesis line plus token consequences:

| Field | What it fixes |
|-------|---------------|
| Base unit and scale ratio | spacing base (4 or 8) and type ratio — makes density differ measurably |
| Type role split | which roles carry character; which stay on the readable system face |
| Colour-construction rule | how neutral anchor, accent, and semantic roles are derived and held apart |
| One composition move | the single structural gesture the screen is built around |
| Motion signature | one recurring transition, duration from `quality-bars.md`, curve named from `motion-system.md` (M3 token, `cubic-bezier`, SwiftUI spring preset, or Compose damping/stiffness), reduced-motion fallback |

Then:

1. Rank the three against user goal, task, context defaults, platform conventions, and accessibility.
2. Commit to one.
3. Move the two rejects into `Alternatives considered` (Mode A) or `Key decision tradeoffs` (Mode C), each with the mechanism that killed it.

Rules:

- Directions must differ in at least two token fields; three variants of one structure is one direction.
- The step is internal — the response commits to one direction and never presents a menu.
- Divergence is perceptual and compositional. Functional patterns stay convergent (see Step 7, "Choose from known patterns, do not invent").
- Token values are directional defaults, not invented brand facts. Work inside a supplied design system when there is one; say so when there is not.
- Mode F names the direction the delivered design already embodies; it does not generate new ones or invent rejected alternatives the user never described.
- When the input supports only one direction, state that under `Assumptions` rather than inventing two throwaway rejects.

Vocabulary and the long form of this step live in `docs/inspiration-sources.md`.

---

## Step 5: Build the response by mode

Use the response structure defined in `skill/templates.md`.

### Mandatory response header
Every response begins with:
- Mode
- Platform scope
- Assumptions

### Mandatory response footer
Every response ends with:
- Next actions

---

## Step 6: Apply universal review lenses

Before finalizing, check the draft against these lenses:

### Task clarity
- Can the user’s main task be identified immediately?

### Clarification need
- Would any missing answer materially change the recommendation?
- If yes, did the response ask no more than three high-impact clarifying questions?
- If no, did the response proceed with minimal labeled assumptions?

### Known weakness prevention
- Which weakness pattern from `docs/weaknesses.md` is most likely for this task?
- Has the draft actively prevented that weakness rather than only avoiding banned words?
- Would the response still be useful if a designer or engineer removed all generic design language?

### Information hierarchy
- Is priority ordered by user need and decision timing?

### Design quality and visual craft
- Does the proposal define the intended attention path?
- Are composition, spacing, typography, color, and density translated into concrete mechanisms rather than taste words?
- Does visual expression support the task and platform instead of hiding weak structure?
- What is the design-quality target or score from `docs/design-quality-rubric.md`, and what prevents it from reaching the next level?

### Navigation predictability
- Can the user understand where they are, where they can go, and how to recover?

### Platform alignment
- Does the answer respect iOS/Android conventions where relevant?

### Readability and typography
- Are type roles and reading structure appropriate?
- Is density manageable?
- Do the numbers match `docs/quality-bars.md` (body size, line-height, line length)?

### Spacing and touch suitability
- Are interaction zones separated clearly?
- Is touch behavior plausible?
- Do touch targets meet the platform minimums in `docs/quality-bars.md` (44pt iOS / 48dp Android)?

### Accessibility implications
- Does the output address scaling, semantics, focus, labels, and predictable interaction?
- Does contrast meet WCAG 2.2 AA as defined in `docs/quality-bars.md`?

### Edge states
- Are empty, loading, error, and recovery states included where relevant?

### Implementation usefulness
- Can design and engineering teams act on this without reverse-engineering vague prose?

---

## Step 7: Apply design reasoning

Every major design decision in the response must have:

- an explicit choice (not "use a button" but "use a filled primary button at the bottom edge")
- at least one alternative that was considered
- a reason the chosen option wins over the alternative, tied to user goal, task, platform, accessibility, or implementation

If a decision has no alternative, it was not a decision — it was a default, and defaults should be flagged as such.

This step exists to prevent first-idea-wins output, which is the most common failure mode in LLM-generated design.

For design-quality decisions, state the mechanism that makes the quality happen: size, spacing, alignment, contrast, density, color role, motion duration, state treatment, or token. Avoid saying "premium", "clean", "modern", "delightful", or "polished" unless the response translates the word into concrete UI decisions.

### Applies to

- Mode A: layout choice, component choice, hierarchy order
- Mode B: step ordering, recovery strategy, decision-point design
- Mode C: structural zone choice, state definition granularity, platform divergence choices
- Mode D: fix recommendations (why this fix, not another)
- Mode E: role scale ratio, weight strategy, density preset
- Mode F: every "Key design decision" must pair with an alternative and a reason

### How to surface

- In Mode A, C, and F: populate the `Alternatives considered` block in the template.
- In other modes: fold the alternative inline into the rationale, not as a separate section.

### Ground reasoning in established heuristics

When a decision is driven by a known usability heuristic, cite the heuristic by name (Fitts' Law, Hick's Law, Jakob's Law, Zeigarnik Effect, etc.). This anchors the reasoning in established practice rather than preference.

See `docs/heuristics.md` for the catalog with mobile applications and red-flag patterns. Use the red flags during Mode D reviews as a concrete violation checklist.

When two heuristics point to different solutions:

- Name both.
- Pick one based on the active context (see `docs/context-defaults.md`).
- Explain the tradeoff in the output, do not hide it.

### Choose from known patterns, do not invent

For every pattern-level decision (navigation, presentation overlay, list vs grid, primary action placement, picker variant, feedback surface, search scope, etc.), consult the decision matrices in `docs/patterns-catalog.md` first.

- Use the matching Use-when / Avoid-when criteria to pick a pattern, not aesthetic preference.
- Cite the pattern choice in the `Pattern choices and why` block.
- The losing pattern goes into `Alternatives considered` with the reason it lost.
- During Mode D reviews, use the pattern entries' red flags as a violation check.

Never invent a novel pattern when an established one covers the case. Novelty breaks Jakob's Law. Invent only when no established pattern applies, and document the deviation with reasons.

### Calibrate design quality

When the mode proposes or packages a design artifact, consult `docs/design-quality.md` and include the relevant calibration:

- Attention path: what the user sees first, second, and then acts on
- Composition and spacing: how grouping, alignment, and rhythm reveal relationships
- Typography: concrete role, size, weight, line-height, and scaling rules
- Color and state: semantic roles, contrast, dark/increased-contrast implications, non-color cues
- Interaction polish: feedback, motion, loading/saving/success/error behavior
- Production checks: token, component, state, and QA implications

Keep this calibration concise. It should make the design more buildable, not turn the answer into a visual-design essay.

### Score design quality

Use `docs/design-quality-rubric.md` after calibration:

- For generated concepts, UI specs, typography systems, and handoff: derive the score as the median of the assessable dimensions, then apply caps. Do not aim at a number; report what the dimensions give.
- If the draft scores 3/5 or below and context is sufficient, revise the weak dimension before returning.
- If the derivation lands below 4/5 and the context cannot lift it, report the derived score and state the missing input under `Assumptions`, `Unresolved assumptions`, or `Open questions`. Do not round up to 4/5.
- For Mode D reviews: expose both a current and a projected score inside `Design quality score (current → projected)`. The exact contract — flat median of the assessable dimensions, `n/v` handling, `Ceiling note`, and the Bold move trigger — lives in the Mode D section of `skill/modes.md`. Follow it there rather than a summary here.
- Do not let a high visual score hide P0/P1 weaknesses, missing states, accessibility risks, or unsupported claims.

### Keep inspiration separate from rationale

When the response uses inspiration sources:

- keep them in an `Inspiration references` section or clearly labeled note
- separate production references (Mobbin, Page Flows, UI Sources, Pttrns, Screenlane) from portfolio or moodboard references (Behance, Dribbble, Pinterest)
- never use inspiration as the reason a UX pattern is correct
- return to the normal decision criteria before choosing: task clarity, platform conventions, accessibility, quality bars, pattern matrices, and implementation constraints

---

## Step 8: Check concrete quality bars

Compare the draft against the numeric thresholds in `docs/quality-bars.md`.

At minimum, confirm:

- Typography roles cover the needed hierarchy and every role has a size and line-height within the stated ranges.
- Touch targets meet platform minimums and have sufficient gaps.
- Contrast recommendations meet WCAG 2.2 AA.
- Motion durations fall within the recommended ranges and respect reduced-motion settings.
- States include at minimum default, loading, empty, error.
- Spacing values come from the canonical scale, not ad-hoc numbers.
- Design-quality calibration does not contradict task clarity, accessibility, quality bars, or platform conventions.
- The design-quality rubric is applied when relevant, and the score printed is the median of the dimension read written above it; a dimension whose failed boundary question the input can answer is lifted and the score re-derived.
- Known weakness patterns from `docs/weaknesses.md` are addressed before self-review.

When the mode does not produce concrete values (Mode B flow, Mode F rationale), this check is lighter — confirm that the output does not contradict any bar.

---

## Step 9: Self-review against the quality bar

Run the self-review pass defined in `docs/self-review.md`.

- Silently answer every prompt in the universal section.
- Silently answer every prompt in the mode-specific section.
- A "yes" on any of the four blocking-gate questions blocks the return until it is fixed; re-run the gate after the fix.
- A "no" on an improvement prompt is the next edit, not a reason to withhold the response.
- Never return a response that fails self-review with a disclaimer. Fix it or narrow the scope.

Self-review is not optional. It is the single highest-impact quality mechanism in this skill.

---

## Step 10: Finalize responsibly

Make sure the final answer:

- states assumptions clearly
- distinguishes facts from recommendations
- remains structured and reusable
- avoids unsupported claims
- ends with concrete next actions

---

## Quality bar

A good output from this skill should feel:

- immediately usable in a design or product workflow
- grounded in platform and accessibility realities
- concise without being thin
- specific without pretending certainty
- helpful to both design and implementation

If the output sounds stylish but not buildable, it failed.
