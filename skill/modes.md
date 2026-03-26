# Mode Definitions

This document defines the six supported modes for `mobile-design-skill`.

Each mode includes:

- required input
- optional input
- output structure
- validation checklist
- fallback behavior

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
- Rationale for major choices
- Next actions

### Validation checklist
- Is the primary task obvious?
- Is the hierarchy sequenced by user need rather than decoration?
- Are recommended components plausible for the task?
- Are empty/loading/error states included?
- Are touch and readability implications addressed?
- Are platform differences called out if relevant?
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
- iOS-specific and/or Android-specific implementation notes
- Next actions

### Validation checklist
- Can an engineer or designer build from this?
- Are states explicit?
- Are behaviors described instead of implied?
- Are spacing and typography included?
- Are content constraints included?
- Are platform notes split where conventions differ?
- Are accessibility requirements concrete?
- Are unknown details labeled as assumptions?

### Fallback behavior
If the request lacks detail:
- create a base spec with explicit assumptions
- avoid pretending to know hidden business rules
- keep state definitions conservative and reusable

---

## Mode D: Review screen for usability/accessibility

### Purpose
Critique a screen or screen description through usability, accessibility, hierarchy, and platform lenses.

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
- Assumptions
- Quick summary
- Strengths
- Usability issues
- Accessibility issues
- Hierarchy and readability issues
- Navigation and interaction issues
- Severity or priority
- Recommended fixes
- Platform-convention mismatches
- Unresolved assumptions
- Next actions

### Validation checklist
- Does the review distinguish strengths from problems?
- Are issues concrete rather than aesthetic opinions?
- Are severity levels useful?
- Are fixes practical?
- Are platform mismatches called out?
- Are typography and spacing reviewed, not ignored?
- Is compliance language avoided unless verified?
- Are unresolved assumptions stated?

### Fallback behavior
If evidence is limited:
- frame findings as probable issues, not proven defects
- state what cannot be verified from the provided material

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
- Assumptions
- Type roles
- Size hierarchy
- Weight usage
- Line-height guidance
- Spacing scale
- Density rules
- Touch-target implications
- Accessibility considerations for scaling and readability
- Usage examples for common screen areas
- Next actions

### Validation checklist
- Does the system define roles instead of random sizes?
- Does it address scaling and readability?
- Does it cover spacing as a system?
- Does it relate density to content and task needs?
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
- Assumptions
- Design objective
- Target users and context
- Key design decisions
- Pattern choices and why
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
- Does it cover edge states and implementation concerns?
- Does it avoid invented evidence?
- Does it separate known facts from recommendations?
- Is it usable in design/dev handoff?
- Does it end with a realistic validation plan?

### Fallback behavior
If research evidence is missing:
- do not fabricate validation
- explicitly recommend what should be tested or confirmed next
