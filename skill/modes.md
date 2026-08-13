# Mode Definitions

This document defines the six supported modes for `mobile-design-skill`.

Each mode includes:

- required input
- optional input
- output structure
- validation checklist
- fallback behavior

All modes also use `docs/weaknesses.md` as a failure-mode preflight. The goal is to prevent outputs that are structurally complete but generic, overconfident, aesthetic-only, platform-flattened, or weakly buildable.

Modes that propose, specify, review, or rationalize a design artifact also use `docs/design-quality-rubric.md`. Generated/specification outputs derive the score from the assessable dimensions rather than aiming at a number; reviews expose both a current and a projected (conditional) score with evidence limits.

All modes use `docs/clarification-policy.md` before drafting. Ask clarifying questions only when missing information would materially change the recommendation; otherwise proceed with minimal labeled assumptions.

---

## Mode A: Generate mobile screen concept

### Purpose
Create a first-pass concept for a mobile screen that is usable, structured, and platform-aware.

### Required input
At least one of:
- app idea
- feature description
- user goal
- screen type

### Optional input
- platform
- target audience
- brand or tone
- current design system
- accessibility sensitivity
- enterprise context
- content density
- wireframe notes
- constraints and deadlines

### Output structure
- Mode
- Platform scope
- Device class
- Assumptions
- Screen goal
- Primary user task
- Information hierarchy
- Recommended layout structure
- Suggested components
- Interaction notes
- Empty / loading / error states
- Platform-specific notes
- Accessibility considerations
- Adaptive behavior — include only when device class is not phone; omit entirely for phone-only work
- Design quality calibration
- Rationale for major choices
- Alternatives considered — the two rejected directions from step 5.5. Each entry carries its `from:` provenance (the catalog entry it was derived from, or `baseline`), at least two of that direction's token consequences (base unit and ratio, type role split, colour-construction rule, composition move, motion signature), and the mechanism that kills it. A layout described in layout words is not a direction, and two variants of one structure are not two alternatives.
- Next actions

### Validation checklist
- Is the primary task obvious?
- Is the hierarchy sequenced by user need rather than decoration?
- Are recommended components plausible for the task?
- Are empty/loading/error states included?
- Are touch and readability implications addressed?
- Are visual hierarchy, composition, density, and production checks calibrated?
- Does the `Quality target` line name the dimension blocking the next level, rather than printing a bare number?
- Does `Signature move` name an owned asset as a token with repeat locations, or honestly record the screen as inert?
- Are the two alternatives structurally different from the chosen layout, and is the mechanism that kills each one named?
- Are platform differences called out if relevant?
- If device class is not phone, does the concept give the layout at compact and regular width, name a canonical layout, and change navigation with width?
- Is accessibility included by default?
- Are invented details labeled as assumptions?

### Fallback behavior
If the request is underspecified:
- infer only the minimum viable context
- label assumptions clearly
- keep the concept structural rather than visually over-specified

---

## Mode B: Design mobile user flow

### Purpose
Define a usable, predictable, recoverable mobile task flow.

### Required input
At least one of:
- user goal
- flow description
- feature description
- journey start and end states

### Optional input
- platform
- authentication context
- target audience
- failure scenarios
- enterprise or regulated context
- current navigation model
- content density
- accessibility sensitivity

### Output structure
- Mode
- Platform scope
- Device class
- Assumptions
- Flow goal
- Entry points
- Ordered steps/screens
- Decision points
- Back-navigation logic
- Failure and recovery paths
- Platform behavior notes
- Accessibility and usability risks
- Simplification opportunities
- Next actions

### Validation checklist
- Is the success path clear?
- Are decision points explicit?
- Is back-navigation logic predictable?
- Are error and recovery paths present?
- Are steps scoped to mobile realities, not desktop fantasies?
- Are platform navigation differences included where relevant?
- Are usability and accessibility risks included?
- Are unnecessary steps flagged for simplification?

### Fallback behavior
If the request is incomplete:
- define a lean “happy path” plus minimum recovery paths
- note where business rules or product policy details are missing

---

## Mode C: Create platform-aware UI spec

### Purpose
Translate a screen or flow into implementation-friendly UI structure and behavior.

### Required input
At least one of:
- screen description
- wireframe description
- feature description
- flow scope

### Optional input
- platform
- current design system
- content model
- states
- interaction constraints
- handoff depth
- brand constraints
- accessibility sensitivity
- engineering context

### Output structure
- Mode
- Platform scope
- Device class
- Assumptions
- Screen or flow scope
- Structural zones
- Components by section
- State definitions
- Behavior rules
- Content guidance
- Spacing and layout notes
- Typography rules
- Accessibility requirements
- Adaptive behavior — include only when device class is not phone; omit entirely for phone-only work
- Design quality requirements
- Platform-specific implementation notes — split into iOS-specific and Android-specific subsections when conventions materially differ
- Key decision tradeoffs — for each contested choice, what was given up and why that cost is acceptable here
- Next actions

### Validation checklist
- Can an engineer or designer build from this?
- Are states explicit?
- Are behaviors described instead of implied?
- Are spacing and typography included?
- Are content constraints included?
- Are platform notes split where conventions differ?
- If device class is not phone, does `Adaptive behavior` name the breakpoint, canonical layout, collapse rule, detail-pane empty state, and what survives a multitasking resize?
- Are accessibility requirements concrete?
- Are visual hierarchy, spacing, typography, color/state, and production quality requirements concrete?
- Does the `Quality target` line name the dimension blocking the next level, rather than printing a bare number?
- Does `Key decision tradeoffs` state what was given up for each contested choice, not only what was chosen?
- Are unknown details labeled as assumptions?

### Fallback behavior
If the request lacks detail:
- create a base spec with explicit assumptions
- avoid pretending to know hidden business rules
- keep state definitions conservative and reusable

---

## Mode D: Review screen for usability/accessibility

### Purpose
Run an expert review of a screen or screen description through usability, accessibility, hierarchy, design-quality, and platform lenses. Mode D borrows critique's reasoning structure (objective → decision → why it is or isn't effective) but, as an expert review rather than a facilitated critique, it also prescribes fixes: each finding is one causal chain — observation → violated principle → user consequence → change → predicted effect — not a list of problems split from a separate list of remedies.

### Sub-cases

Mode D behaves differently depending on what the user provides. Classify the request into exactly one sub-case at the start of the response, and adjust scope accordingly.

#### D1: Review with visual design provided
The user shares a screenshot, Figma link, or detailed visual description that includes layout, spacing, typography treatment, and color.

- Full assessment is possible across visual hierarchy, spacing, typography, colors, and contrast.
- Accessibility checks can address visual properties (contrast, focus appearance, touch-target visibility) as well as structural ones.
- Use this sub-case label at the top of the response.

#### D2: Review with text description only
The user describes layout structure (fields, sections, actions, content) but no visual treatment.

- Assess structure, logic, information order, state coverage, and interaction behavior.
- Do not assert visual properties (contrast, spacing in pixels, visual weight) without qualifiers. Flag them under `Unresolved assumptions`.
- Accessibility assessment is limited to properties that can be reasoned from structure: label strategy, state semantics, input affordances. Mark visual accessibility (contrast, focus visibility) as unverifiable.
- Use this sub-case label at the top of the response.

#### D3: Review with problem statement
The user reports a symptom without a clear root cause ("users complain", "analytics show drop-off at step 3", "something feels off").

- Lead with diagnosis: what likely causes the reported symptom, based on the described context.
- Differentiate diagnosis from assessment. Diagnosis is a hypothesis; assessment reports observable problems.
- Suggest targeted investigation steps (specific events to check, specific user actions to observe), not a full redesign.
- Use this sub-case label at the top of the response.

#### D4: Review with context change
The user asks whether an existing design still holds under a changed context (new audience, new regulatory framing, new platform, new accessibility requirement).

- Re-evaluate the existing design through the new lens; do not re-review from scratch.
- Call out which prior-acceptable choices now fail under the new context, and which remain fine.
- If the context change invalidates assumptions baked into the original design, state that the design likely needs re-structuring, not just adjustment.
- Use this sub-case label at the top of the response.

### Required input
At least one of:
- screen description
- wireframe description
- UI spec
- screenshot description
- current layout summary

### Optional input
- platform
- target audience
- product context
- known complaints
- current constraints
- business priority
- accessibility sensitivity
- severity preference

### Output structure
- Mode
- Platform scope
- Device class
- Sub-case (D1 / D2 / D3 / D4)
- Assumptions
- Quick summary
- Strengths
- Findings — each finding is one causal chain with: Lens (Usability / Accessibility / Hierarchy & readability / Design quality / Navigation & interaction), Observation, Violated principle (named), User consequence, Change, Predicted effect (directional + confidence), Severity (Nielsen 0–4 = frequency × impact × persistence), Moves (which design-quality dimension it shifts, band→band)
- Design quality score (current → projected) — current and projected scores plus a per-dimension table carrying all nine rubric dimensions; both numbers are flat medians of the assessable bands in their column, the current over the bands as found and the projected over the bands once the fixes land (visual dimensions are never projected upward from a text-only review); a higher number reachable only after a visual pass goes in a separate Ceiling note
- Severity index — findings rolled up by Nielsen 0–4 level
- Bold move (optional) — include only when the trigger is met (see below)
- Platform-convention mismatches
- Unresolved assumptions
- Next actions

The Bold move trigger: offer one only when ALL hold — the screen is already competent (current ≥3/5) but inert (loses no major points yet has no point of view); there is no unresolved severity-3 or severity-4 finding (fix those first); and there is a concrete UX upside. Allowed in D1/D3; in D2 it may address structure/flow only; in D4 only if the new context unlocks it. It is not a fix and not required to ship; if the trigger is not met, omit the section. A recommendation that contradicts the stated product/task is a failure only when its justification is aesthetic — a contradiction justified by a named usability/accessibility/hierarchy mechanism and surfaced in the Bold move block with its tradeoff and validation path is encouraged, not penalized.

### Validation checklist
- Is the sub-case (D1 / D2 / D3 / D4) classified explicitly?
- Does the review distinguish strengths from problems, with at least one genuine strength?
- Is each finding a single causal chain (observation → violated principle → user consequence → change → predicted effect), not an issue split from its fix?
- Does every finding name the violated principle (heuristic/law), instead of "this feels off"?
- Does every predicted effect name a user outcome, stated directionally with a confidence level and no fabricated percentages?
- Is severity rated on the Nielsen 0–4 scale and justified as frequency × impact × persistence?
- For D2: are visual claims qualified as unverifiable, or restricted to structure?
- For D3: is diagnosis separated from assessment?
- For D4: is the review framed as a delta against the changed context, not a full re-review?
- Are both a current and a projected design-quality score exposed, each the median of the assessable bands in its own column of the nine-dimension table (a flat number, not "up to"), with any higher post-visual-pass figure confined to a Ceiling note?
- For D2/D3: is the projected score labeled provisional, and are visual dimensions kept at n/v (never projected upward)?
- Is every `n/v` there because the evidence channel cannot carry the question, rather than because the input was thin? Thin evidence inside the right channel is a low band; marking it n/v removes the weakest dimension from the median.
- If a Bold move is offered: is the trigger met, does it carry all required fields (deviation, JTBD job, upside, risk, validation path, score impact, conviction), and is it kept separate from the required fixes?
- Was any UX-strengthening recommendation withheld only because it contradicts the current product? If so, is it moved to Bold move with its tradeoff?
- Are platform mismatches called out, and typography/spacing reviewed where verifiable?
- Are design-quality claims limited to what can be verified from the provided visual or description?
- Is compliance language avoided unless verified, and are unresolved assumptions stated?

### Fallback behavior
If evidence is limited:
- frame findings as probable issues, not proven defects
- state what cannot be verified from the provided material
- for D2 in particular, never assert visual properties without a qualifier; move them to `Unresolved assumptions`

---

## Mode E: Create typography and spacing system

### Purpose
Create a mobile-friendly type and spacing system grounded in readability, scaling, and touch ergonomics.

### Required input
At least one of:
- product type
- target audience
- platform
- density preference
- current design direction

### Optional input
- current brand typography
- accessibility sensitivity
- enterprise context
- multilingual support
- content heaviness
- handoff depth
- existing token system

### Output structure
- Mode
- Platform scope
- Device class
- Assumptions
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
- Next actions

### Validation checklist
- Does the system define roles instead of random sizes?
- Does it address scaling and readability?
- Does it cover spacing as a system?
- Does it relate density to content and task needs?
- Does it define visual rhythm and role limits so the system can be applied consistently?
- Is the score derived from a visible dimension read rather than aimed at, and does rhythm, density, scaling, and production-ready value coverage support it?
- Does it note touch implications?
- Does it remain plausible across platforms?
- Are accessibility constraints included?
- Are examples practical?

### Fallback behavior
If brand rules are unknown:
- define a neutral, platform-safe structure
- separate role definitions from font-family decisions
- mark unresolved brand-level decisions clearly

---

## Mode F: Prepare design rationale / handoff

### Purpose
Explain and package design decisions for product, design, and engineering handoff.

### Required input
At least one of:
- design description
- redesign summary
- screen or flow concept
- decision summary

### Optional input
- platform
- audience
- project context
- constraints
- known tradeoffs
- implementation stage
- research notes
- accessibility sensitivity

### Output structure
- Mode
- Platform scope
- Device class
- Assumptions
- Design objective
- Target users and context
- Key design decisions — each carries the alternative considered and why it lost; a decision with no rejected alternative is a default and must be labeled as one
- Pattern choices and why
- Design quality rationale
- Platform alignment
- Accessibility and usability considerations
- States and edge cases
- Implementation notes
- Open questions
- Validation plan or recommended testing focus
- Next actions

### Validation checklist
- Does it explain why decisions were made?
- Does it connect choices to user goals and context?
- Does it show platform alignment?
- Does it explain how visual hierarchy, composition, density, and brand expression support the design objective?
- Does the rationale state the quality target or current score using the 1-5 rubric?
- Does it cover edge states and implementation concerns?
- Does it avoid invented evidence?
- Does it separate known facts from recommendations?
- Is it usable in design/dev handoff?
- Does it end with a realistic validation plan?

### Fallback behavior
If research evidence is missing:
- do not fabricate validation
- explicitly recommend what should be tested or confirmed next
