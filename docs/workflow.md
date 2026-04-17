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
- Is this phone-first or broader adaptive/mobile?
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

### If sufficient
Proceed directly.

### If partially sufficient
Continue with minimal labeled assumptions.

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
- Use Material Design 3 and Android Navigation for Android and cross-platform mobile structure where Android behavior matters.
- Use WCAG 2.2 and W3C mobile guidance for accessibility framing.
- Use ISO usability and HCD framing when decisions need justification through context of use and lifecycle reasoning.
- Use GOV.UK and NHS when clarity, service design, task completion, readability, and high-trust patterns matter.
- Use Fluent 2 and related guidance when cross-platform type hierarchy needs coherence.
- Use Figma Variables guidance when outputs need token-friendly structure.

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

### Information hierarchy
- Is priority ordered by user need and decision timing?

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

When the mode does not produce concrete values (Mode B flow, Mode F rationale), this check is lighter — confirm that the output does not contradict any bar.

---

## Step 9: Self-review against the quality bar

Run the self-review pass defined in `docs/self-review.md`.

- Silently answer every prompt in the universal section.
- Silently answer every prompt in the mode-specific section.
- If any answer is "no" or "not sure", revise and re-run.
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
