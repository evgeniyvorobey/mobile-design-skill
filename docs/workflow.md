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

### Spacing and touch suitability
- Are interaction zones separated clearly?
- Is touch behavior plausible?

### Accessibility implications
- Does the output address scaling, semantics, focus, labels, and predictable interaction?

### Edge states
- Are empty, loading, error, and recovery states included where relevant?

### Implementation usefulness
- Can design and engineering teams act on this without reverse-engineering vague prose?

---

## Step 7: Finalize responsibly

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
