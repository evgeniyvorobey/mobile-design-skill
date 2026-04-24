# Output Templates

Use these templates as the response skeleton for each mode.

Templates are structure, not quality. Before returning any filled template, run the known-weakness preflight from `docs/weaknesses.md`; do not expose the preflight as a separate output section unless the user explicitly asks for failure-mode analysis.

---

## Template A: Generate mobile screen concept

```md
Mode: Generate mobile screen concept
Platform scope: [iOS / Android / Cross-platform / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Screen goal
[what the screen is for]

## Primary user task
[the main action the user needs to complete]

## Information hierarchy
1. [highest priority content/action]
2. [secondary content/action]
3. [supporting content/action]

## Recommended layout structure
- Header:
- Primary content area:
- Secondary content area:
- Persistent actions / navigation:
- Footer or bottom area if relevant:

## Suggested components
- [component] — [why]
- [component] — [why]

## Interaction notes
- [behavior]
- [behavior]

## Empty / loading / error states
- Empty:
- Loading:
- Error:

## Platform-specific notes
### iOS
- [only if relevant]

### Android
- [only if relevant]

## Accessibility considerations
- [consideration]
- [consideration]
- [consideration]

## Design quality calibration
- Attention path:
- Composition and spacing:
- Typography:
- Color and state:
- Interaction polish:
- Production checks:

## Rationale for major choices
- [decision] because [reason]
- [decision] because [reason]

## Alternatives considered
- [alternative] — rejected because [reason tied to user goal, task, platform, accessibility, or implementation]
- [alternative] — rejected because [reason]

## Next actions
- [action]
- [action]
```

---

## Template B: Design mobile user flow

```md
Mode: Design mobile user flow
Platform scope: [iOS / Android / Cross-platform / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Flow goal
[what the flow needs to accomplish]

## Entry points
- [entry point]
- [entry point]

## Ordered steps / screens
1. [screen/step]
2. [screen/step]
3. [screen/step]

## Decision points
- [condition] → [branch]
- [condition] → [branch]

## Back-navigation logic
- [rule]
- [rule]

## Failure and recovery paths
- [failure case] → [recovery]
- [failure case] → [recovery]

## Platform behavior notes
### iOS
- [note]

### Android
- [note]

## Accessibility and usability risks
- [risk]
- [risk]

## Simplification opportunities
- [opportunity]
- [opportunity]

## Next actions
- [action]
- [action]
```

---

## Template C: Create platform-aware UI spec

```md
Mode: Create platform-aware UI spec
Platform scope: [iOS / Android / Cross-platform / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Screen or flow scope
[scope]

## Structural zones
- Top area:
- Main content area:
- Supporting area:
- Bottom actions / navigation:

## Components by section
### Section 1
- [component]
- [component]

### Section 2
- [component]
- [component]

## State definitions
- Default:
- Focused / active:
- Loading:
- Empty:
- Error:
- Success:
- Disabled if applicable:

## Behavior rules
- [rule]
- [rule]

## Content guidance
- [content principle]
- [content principle]

## Spacing and layout notes
- [note]
- [note]

## Typography rules
- [role] → [usage]
- [role] → [usage]

## Accessibility requirements
- [requirement]
- [requirement]
- [requirement]

## Design quality requirements
- Attention path:
- Composition and spacing:
- Typography:
- Color and state:
- Interaction polish:
- Production checks:

## Platform-specific implementation notes
### iOS
- [note]

### Android
- [note]

## Key decision tradeoffs
- [decision] chosen over [alternative] because [reason]
- [decision] chosen over [alternative] because [reason]

## Next actions
- [action]
- [action]
```

---

## Template D: Review screen for usability/accessibility

```md
Mode: Review screen for usability/accessibility
Platform scope: [iOS / Android / Cross-platform / Assumed]
Sub-case: [D1 visual provided / D2 description only / D3 problem statement / D4 context change]
Assumptions:
- [assumption 1]
- [assumption 2]

## Quick summary
[one-paragraph assessment; for D3, lead with diagnosis hypothesis]

## Strengths
- [strength]
- [strength]

## Usability issues
- [issue]
- [issue]

## Accessibility issues
- [issue]
- [issue]

## Hierarchy and readability issues
- [issue]
- [issue]

## Design quality issues
- [issue]
- [issue]

## Navigation and interaction issues
- [issue]
- [issue]

## Severity / priority
- High:
- Medium:
- Low:

## Recommended fixes
- [fix]
- [fix]

## Platform-convention mismatches
- [mismatch]
- [mismatch]

## Unresolved assumptions
- [unknown]
- [unknown]

## Next actions
- [action]
- [action]
```

---

## Template E: Create typography and spacing system

```md
Mode: Create typography and spacing system
Platform scope: [iOS / Android / Cross-platform / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Type roles
- Display:
- Screen title:
- Section title:
- Body:
- Secondary body:
- Label:
- Caption / helper:
- Button / action label:

## Size hierarchy
- [role] → [size guidance]
- [role] → [size guidance]

## Weight usage
- [weight] for [purpose]
- [weight] for [purpose]

## Line-height guidance
- [guidance]
- [guidance]

## Spacing scale
- 4
- 8
- 12
- 16
- 24
- 32
- 40

## Density rules
- [rule]
- [rule]

## Visual rhythm rules
- [rule]
- [rule]

## Touch-target implications
- [implication]
- [implication]

## Accessibility considerations
- [consideration]
- [consideration]

## Usage examples
- App bar:
- List row:
- Form:
- Detail screen:
- Bottom action area:

## Next actions
- [action]
- [action]
```

---

## Template F: Prepare design rationale / handoff

```md
Mode: Prepare design rationale / handoff
Platform scope: [iOS / Android / Cross-platform / Assumed]
Assumptions:
- [assumption 1]
- [assumption 2]

## Design objective
[objective]

## Target users and context
[users and context]

## Key design decisions
- [decision] — alternative considered: [alternative] — chosen because [reason tied to user goal, task, platform, accessibility, or implementation]
- [decision] — alternative considered: [alternative] — chosen because [reason]

## Pattern choices and why
- [pattern] over [alternative pattern] because [reason]
- [pattern] over [alternative pattern] because [reason]

## Design quality rationale
- [quality decision] — [mechanism: size/spacing/alignment/color/density/motion/token] — [why it fits context]
- [quality decision] — [mechanism] — [why]

## Platform alignment
### iOS
- [alignment note]

### Android
- [alignment note]

## Accessibility and usability considerations
- [consideration]
- [consideration]

## States and edge cases
- [state]
- [state]

## Implementation notes
- [note]
- [note]

## Open questions
- [question]
- [question]

## Validation plan / recommended testing focus
- [test focus]
- [test focus]

## Next actions
- [action]
- [action]
```
