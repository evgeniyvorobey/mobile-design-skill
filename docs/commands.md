# Command Reference

This skill supports two invocation styles, depending on the host:

- in Claude Code: invoke it directly with `/mobile-design-skill`
- in Codex: use the installed skill normally via `Use the mobile-design-skill...` or `$mobile-design-skill`, depending on your Codex surface

The six operating modes below behave like reusable commands once the skill is active.

---

## How to invoke the skill

### Claude Code

As of March 26, 2026, Claude Code officially supports direct skill invocation with `/skill-name` and documents that a skill at `.claude/skills/<skill-name>/SKILL.md` can be invoked with `/skill-name`.

For this repository, the direct command is:

```text
/mobile-design-skill
```

With inline arguments:

```text
/mobile-design-skill create a platform-aware UI spec for a package tracking screen
```

With judged mode:

```text
/mobile-design-skill --judge create a platform-aware UI spec for a fitness tracker app
```

`--judge` asks the skill to draft privately, run an independent rubric judge pass in the same session when the host supports subagents, revise if needed, and return the final answer with a compact `Judge summary`. It should not require the user to run a separate script manually.

This repository includes the Claude Code wrapper at:

- [`.claude/skills/mobile-design-skill/SKILL.md`](../.claude/skills/mobile-design-skill/SKILL.md)

### Codex-style invocation

```text
Use the mobile-design-skill.

Task: [what you need]
Platform: [iOS / Android / cross-platform / unknown]
User goal: [goal]
Context: [product, audience, constraints]
```

### Codex short explicit invocation

```text
Use the mobile-design-skill.

Review this Android settings screen for usability and accessibility.
```

### Codex skill mention

```text
Use $mobile-design-skill to create a platform-aware UI spec for a package tracking screen.
```

### Important compatibility note

As of March 26, 2026:

- I verified official Anthropic documentation that Claude Code supports direct `/skill-name` invocation for custom skills.
- I found official OpenAI documentation confirming that skills are supported in Codex, but I did not find an official OpenAI source documenting `/skill-name` as the standard custom-skill invocation pattern for Codex.

So this repository is packaged to support both products, but the invocation UX is not identical:

- Claude Code: `/mobile-design-skill`
- Codex: standard skill usage or explicit skill mention

---

## Important note

The skill classifies every request into exactly one primary mode.

That means you can use it in two ways:

1. ask explicitly for the mode you want
2. describe the task and let the skill classify it automatically

For public documentation, it is usually better to show explicit mode phrasing because it is easier for first-time users to understand.

Use `--judge` for higher-confidence outputs when the extra latency of an independent judge pass is acceptable.

---

## 1. Generate mobile screen concept

Use this when you need a first-pass screen concept for a mobile interface.

Best for:
- new screens
- layout direction
- hierarchy planning
- component recommendations

Example:

```text
Use the mobile-design-skill.

Generate a mobile screen concept for a medication refill screen.
Platform: iOS
Audience: older adults
Constraints: accessibility-sensitive, high trust, dense medical content
```

What the skill returns:
- screen goal
- primary user task
- information hierarchy
- recommended layout structure
- suggested components
- interaction notes
- empty/loading/error states
- accessibility considerations
- rationale and next actions

---

## 2. Design mobile user flow

Use this when you need a multi-step task flow rather than a single screen.

Best for:
- onboarding
- booking
- checkout
- account recovery
- verification flows

Example:

```text
Use the mobile-design-skill.

Design a mobile user flow for resetting a forgotten password.
Platform: Android
Audience: enterprise employees
Constraints: MFA required, older user base, regulated environment
```

What the skill returns:
- flow goal
- entry points
- ordered steps or screens
- decision points
- back-navigation logic
- failure and recovery paths
- accessibility and usability risks
- simplification opportunities

---

## 3. Create platform-aware UI spec

Use this when you already know the screen or flow and want an implementation-friendly spec.

Best for:
- turning wireframes into specs
- preparing design handoff
- making states and behavior explicit
- documenting platform-specific behavior

Example:

```text
Use the mobile-design-skill.

Create a platform-aware UI spec for a package tracking detail screen.
Platform: Android
User goal: check delivery progress and contact support if needed
Current screen: top app bar, progress steps, package details, address, support actions
```

What the skill returns:
- structural zones
- components by section
- state definitions
- behavior rules
- content guidance
- spacing and typography notes
- accessibility requirements
- iOS or Android implementation notes

---

## 4. Review screen for usability/accessibility

Use this when you already have a screen description, wireframe, or UI summary and want critique.

Best for:
- design review
- accessibility-aware critique
- finding usability problems
- prioritizing fixes

Example:

```text
Use the mobile-design-skill.

Review this cross-platform profile edit screen for usability and accessibility.
Screen description:
- long stacked form
- save button only at bottom
- placeholders used as labels
- errors appear only in red text
Constraints: enterprise app, high density, many older users
```

What the skill returns:
- quick summary
- strengths
- usability issues
- accessibility issues
- hierarchy and readability issues
- navigation and interaction issues
- severity or priority
- recommended fixes

---

## 5. Create typography and spacing system

Use this when you need a mobile-friendly type and spacing foundation rather than a single screen.

Best for:
- defining type roles
- spacing scales
- readability systems
- token preparation
- density guidance

Example:

```text
Use the mobile-design-skill.

Create a typography and spacing system for a cross-platform mobile banking app.
Audience: broad consumer base, including older adults
Constraints: readability-first, moderate data density, brand font may be applied later
```

What the skill returns:
- type roles
- size hierarchy
- weight usage
- line-height guidance
- spacing scale
- density rules
- touch-target implications
- accessibility considerations
- usage examples

---

## 6. Prepare design rationale / handoff

Use this when the design direction already exists and you need to explain or package it for a team.

Best for:
- handoff notes
- design rationale
- cross-functional review
- documenting why a solution was chosen

Example:

```text
Use the mobile-design-skill.

Prepare a design rationale and handoff for a redesign of a mobile appointment booking confirmation screen.
Platform: iOS and Android
Audience: older and anxious users
Constraints: high trust, accessibility-sensitive, limited engineering time
Design changes:
- simplified layout
- clearer summary
- more explicit preparation instructions
```

What the skill returns:
- design objective
- target users and context
- key decisions
- pattern choices and why
- platform alignment
- accessibility and usability considerations
- states and edge cases
- implementation notes
- open questions
- validation plan

---

## How to write better prompts

The skill works best when your prompt includes:

- product or domain
- user goal
- platform
- screen or flow scope
- audience
- constraints
- existing wireframe or screen summary if available

If some of that is missing, the skill will proceed with minimal labeled assumptions.

If the missing information would materially change the recommendation, the skill follows `docs/clarification-policy.md`: it asks at most three blocking clarifying questions, explains why they matter, and offers a fast path when a provisional draft is still useful.

---

## What not to expect

This skill is not meant for:

- pure visual inspiration
- aesthetic-only feedback
- fabricated UX research claims
- fake accessibility compliance statements
- generic “make it more modern” advice

It is designed for structured, explainable, implementation-friendly mobile design output.
