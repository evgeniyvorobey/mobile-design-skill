# Evaluation Criteria

This document defines concrete evaluation criteria for the `mobile-design-skill` output by mode. It enables automated and human-judged quality checks, regression testing, and consistent feedback across iterations.

Use this document when:

- reviewing a skill response before shipping
- building evals for LLM-as-judge scoring
- regression-testing prompt or skill changes
- assessing whether a mode output meets the contract

Every mode is evaluated across three layers:

1. **Structural validation** — mechanical checks that can be automated via regex, parsing, or validators.
2. **Content validation** — semantic checks that require a human or LLM-as-judge.
3. **Fail conditions** — hard stops that invalidate the response regardless of other scores.

---

## Shared structural validation (all modes)

Every response must satisfy the following, regardless of mode:

- [ ] Starts with `Mode: [exact mode name]`
- [ ] Contains `Platform scope: [iOS | Android | Cross-platform | Assumed: <description>]`
- [ ] Contains `Assumptions:` section with at least 2 items
- [ ] Contains the mode-specific accessibility section with at least 3 concrete items:
  - Mode A / E: `## Accessibility considerations`
  - Mode B: `## Accessibility and usability risks`
  - Mode C: `## Accessibility requirements`
  - Mode D: `## Accessibility issues`
  - Mode F: `## Accessibility and usability considerations`
- [ ] Contains a `## Next actions` section with at least 2 specific, testable items
- [ ] Does not contain the compliance-claim tokens: `compliant`, `WCAG-compliant`, `passes accessibility` unless the user provided verified evidence
- [ ] Does not contain fabricated quantitative research claims (regex: `\d+%`, `users completed`, `testing proved`, `research shows`) unless sourced

## Shared fail conditions (all modes)

Any of the following invalidates the response:

- Missing the mode-specific accessibility section
- `Next actions` are generic (examples: "test it", "validate", "iterate", "improve")
- Hallucinated platform rule (example: "iOS requires X" without source or "recommendation" framing)
- Blended iOS and Android guidance where conventions materially differ
- Aesthetic-only recommendation without usability, readability, accessibility, or implementation justification
- Visual polish, brand expression, motion, or illustration used to hide weak hierarchy, missing states, or inaccessible interaction
- Compliance claim echoed from user input without "cannot independently verify" qualifier
- Inspiration source used as evidence for usability, accessibility, platform correctness, compliance, or user preference
- Template-complete but decision-empty output: required sections exist, but recommendations have no choices, rejected alternatives, context-specific reasons, or buildable mechanisms

## Known weakness validation

Use [`weaknesses.md`](weaknesses.md) as the regression map for content review.

For every evaluated response:

- [ ] The likely weakness pattern is prevented by the response, not merely absent from wording.
- [ ] The output is specific to the user's product, task, audience, platform, or constraints.
- [ ] Major decisions include a chosen option, a rejected alternative where relevant, and a concrete reason.
- [ ] Evidence boundaries are clear: facts, assumptions, recommendations, and unverifiable items are separated where risk exists.
- [ ] The response is buildable enough for the requested mode: states, behaviors, values, tokens, QA checks, or validation focus are present as appropriate.
- [ ] The 1-5 design-quality rubric from [`design-quality-rubric.md`](design-quality-rubric.md) is applied when the response proposes, specifies, reviews, or rationalizes a design artifact.

Hard-fail the response if it matches a P0 or P1 weakness in `docs/weaknesses.md`.

---

## Mode A: Generate mobile screen concept

### Structural validation
- [ ] Response begins with `Mode: Generate mobile screen concept`
- [ ] Contains sections: `Screen goal`, `Primary user task`, `Information hierarchy`, `Recommended layout structure`, `Suggested components`, `Empty / loading / error states`, `Design quality calibration`
- [ ] Contains `Alternatives considered` with at least one rejected alternative and reason
- [ ] Information hierarchy is ordered (numbered or bulleted with priority)
- [ ] All three edge states (empty, loading, error) are explicitly addressed
- [ ] If platform-specific notes are included, they are split per platform (not merged)

### Content validation
- [ ] Primary user task is singular and explicit (not a list of three tasks)
- [ ] Hierarchy is task-driven (by user need), not visual-first (by prominence)
- [ ] Suggested components are buildable on the named platform (native or common UI kit)
- [ ] Rationale connects each major choice to user goal, accessibility, or implementation
- [ ] Design quality calibration defines attention path, composition/spacing, typography, color/state, interaction polish, and production checks where relevant
- [ ] Accessibility considerations are specific to the screen (not generic "use labels")
- [ ] No invented research findings; no quantitative claims without source

### Fail conditions
- Primary user task is ambiguous or absent
- Empty/loading/error states missing
- Hallucinated component (named pattern that does not exist on the target platform)
- Generic accessibility section copied across responses

---

## Mode B: Design mobile user flow

### Structural validation
- [ ] Response begins with `Mode: Design mobile user flow`
- [ ] Contains sections: `Flow goal`, `Entry points`, `Ordered steps/screens`, `Decision points`, `Back-navigation logic`, `Failure and recovery paths`
- [ ] Ordered steps are numbered or sequenced
- [ ] Decision points are explicit (not implied in step descriptions)
- [ ] At least one failure path is defined

### Content validation
- [ ] Success path is end-to-end (entry → success state)
- [ ] Back-navigation behavior is defined for every step, not just the last one
- [ ] Recovery paths cover at least one of: network failure, user abandonment, input validation error
- [ ] No desktop-specific assumptions (example: no hover states, no keyboard-first flows unless explicit)
- [ ] Each step scopes what the user sees, what they can do, and what happens next
- [ ] Simplification opportunities are flagged separately from the flow

### Fail conditions
- Back-navigation logic missing or vague ("user goes back")
- No recovery path defined for the primary failure mode
- Flow assumes desktop conventions (hover-to-reveal, right-click, long-form keyboard entry)
- Invented business rules not flagged as assumptions

---

## Mode C: Create platform-aware UI spec

### Structural validation
- [ ] Response begins with `Mode: Create platform-aware UI spec`
- [ ] Contains sections: `Structural zones`, `Components by section`, `State definitions`, `Behavior rules`, `Spacing and layout notes`, `Typography rules`, `Accessibility requirements`, `Design quality requirements`, `Key decision tradeoffs`
- [ ] For cross-platform specs: contains `iOS-specific implementation notes` AND `Android-specific implementation notes` OR an explicit statement that conventions align
- [ ] State definitions cover at minimum: default, loading, empty, error
- [ ] Spacing values are concrete (example: "16 dp" or "space-4 token"), not relative ("more spacing")

### Content validation
- [ ] An engineer can begin implementation from this spec without asking for missing structural information
- [ ] Component names match the named design system or a reasonable default (Material, iOS native, custom)
- [ ] Behaviors are described as rules ("If X, then Y"), not narrative
- [ ] Typography rules specify role-to-size mapping (not just a list of sizes)
- [ ] Accessibility requirements include specific targets: touch size, label behavior, focus order, contrast
- [ ] Design quality requirements include concrete attention path, composition/spacing, typography, color/state, interaction polish, and production checks
- [ ] Platform-specific notes reflect actual platform behavior, not stereotypes

### Fail conditions
- States missing or only "default" defined
- Spacing/typography vague ("appropriate", "modern", "comfortable")
- Cross-platform spec collapses iOS and Android into one without stating conventions align
- Invented component names not tied to any design system or explicit assumption

---

## Mode D: Review screen for usability/accessibility

### Structural validation
- [ ] Response begins with `Mode: Review screen for usability/accessibility`
- [ ] Contains sections: `Quick summary`, `Strengths`, `Usability issues`, `Accessibility issues`, `Hierarchy and readability issues`, `Design quality issues`, `Navigation and interaction issues`, `Severity or priority`, `Recommended fixes`, `Unresolved assumptions`
- [ ] Sub-case is classified in the opening (visual / description-only / problem-statement / context-change)
- [ ] Severity uses consistent tiers (High/Medium/Low or equivalent)
- [ ] At least one strength is identified (not only negatives)

### Content validation
- [ ] Issues are concrete, not aesthetic opinions ("form is too long without grouping" vs "feels cluttered")
- [ ] Every severity-High issue has a recommended fix
- [ ] Unresolved assumptions list what cannot be verified from the provided material
- [ ] For description-only reviews: visual/aesthetic claims are qualified ("cannot verify from description")
- [ ] Design quality issues do not assert color, spacing, balance, contrast, or visual weight from text-only input without qualifier
- [ ] For problem-statement reviews: diagnosis is differentiated from assessment
- [ ] Compliance language avoided (see shared fail conditions)

### Fail conditions
- Review asserts visual properties (color, contrast, spacing) from text-only input without qualifier
- No strengths section or "no strengths found"
- Severity tiers inconsistent within the response
- Recommended fixes repeat the issue without actionable change
- Compliance claim without verified evidence

---

## Mode E: Create typography and spacing system

### Structural validation
- [ ] Response begins with `Mode: Create typography and spacing system`
- [ ] Contains sections: `Type roles`, `Size hierarchy`, `Weight usage`, `Line-height guidance`, `Spacing scale`, `Density rules`, `Visual rhythm rules`, `Touch-target implications`
- [ ] Type roles are named (not just sizes): Display, Title, Body, Caption, Label, etc.
- [ ] Size hierarchy includes concrete sizes (`pt` / `sp` / token-equivalent)
- [ ] Line-height guidance includes concrete ratios or values
- [ ] Spacing scale is systematic (powers of 2, 4-based, or named token scale)
- [ ] Touch-target minimum is stated (44 pt iOS / 48 dp Android or equivalent)

### Content validation
- [ ] Roles map to use cases, not just to components
- [ ] Line-height values are specified per role, not one-size-fits-all
- [ ] Density rules explain when to use tighter vs looser spacing based on task
- [ ] Visual rhythm rules explain how spacing, type roles, and grouping should repeat across screens
- [ ] Accessibility considerations include dynamic type / large-text scaling behavior
- [ ] If multilingual support was requested, script-specific adjustments (CJK, Arabic, Devanagari) are called out
- [ ] Examples show roles applied to common screen areas (header, body, form, list)

### Fail conditions
- Type roles are absent, only a size list
- Touch-target minimum missing
- Dynamic type / scaling behavior not addressed
- Multilingual requested but no script-specific notes

---

## Mode F: Prepare design rationale / handoff

### Structural validation
- [ ] Response begins with `Mode: Prepare design rationale / handoff`
- [ ] Contains sections: `Design objective`, `Target users and context`, `Key design decisions`, `Pattern choices and why`, `Design quality rationale`, `Platform alignment`, `States and edge cases`, `Implementation notes`, `Open questions`, `Validation plan or recommended testing focus`
- [ ] Each key decision is separated from its justification
- [ ] Open questions list at least one genuinely open item (not filler)

### Content validation
- [ ] Rationale connects decisions to user goals, context, or constraints, not to aesthetic preference
- [ ] Pattern choices reference official guidance or established convention
- [ ] Design quality rationale connects visual hierarchy, composition, density, brand expression, or motion to the product context with concrete mechanisms
- [ ] Platform alignment is substantive, not "follows platform best practices"
- [ ] Validation plan specifies WHAT to test and HOW (method, metric, or acceptance criterion)
- [ ] Implementation notes address at least one concern engineering actually faces (state management, accessibility semantics, analytics, performance)

### Fail conditions
- Rationale is reverse-engineered from the task with no actual design shown or referenced
- Validation plan is "test with users" without specifics
- Open questions list is empty or synthetic
- Fabricated research findings used as justification

---

## Scoring rubric

For evals, score each response across three dimensions:

| Dimension | Weight | Scoring |
|-----------|--------|---------|
| Structural validation | 30% | Pass rate across the mode's structural checks |
| Content validation | 50% | Count of content checks passing / total |
| Hallucination & safety | 20% | Binary pass/fail on shared fail conditions + mode fail conditions |

A response that fails any hard fail condition receives an overall score of **Fail** regardless of the weighted score.

## Design quality rubric

Use [`design-quality-rubric.md`](design-quality-rubric.md) for the design-quality score.

Structural/content evals answer "does the response satisfy the skill contract?" The design-quality rubric answers "how strong is the design artifact itself?"

For generated concepts, UI specs, typography systems, and handoff:

- [ ] Internal target is 4/5 or higher.
- [ ] Any dimension below 4/5 is either revised or clearly blocked by missing input.
- [ ] The output does not average away a serious flaw such as missing states, weak accessibility behavior, or platform flattening.

For reviews:

- [ ] `Design quality issues` includes a current score such as `Current design quality score: 2/5 — ...`.
- [ ] Text-only reviews label the score as structural/provisional when visual evidence is missing.
- [ ] Score rationale references concrete dimensions: hierarchy, spacing, typography, color/state, interaction polish, brand/context fit, or production readiness.

---

## How to run evals

### Automated structural checks

Run:

```bash
python3 scripts/validate_repo.py
```

The repository validator checks required files, relative links, root skill frontmatter, and the committed example outputs in `examples/`. It extracts each `## Example output` fenced block and verifies the mode-specific structural contract, including assumptions, required sections, accessibility sections, concrete numeric values where required, decision tradeoffs, and non-generic next actions.

These checks are intentionally structural. They catch contract drift and missing sections, but they do not replace human or LLM-as-judge content review.

### Human or LLM-as-judge content checks

For content validation:

1. Provide the response alongside the mode-specific criteria from this file.
2. Score each content check as pass / partial / fail.
3. Record the rationale for any non-pass, so the pattern is visible across runs.

### Regression testing with examples

The files in `examples/` are treated as regression targets. When the skill, `modes.md`, or `templates.md` changes:

1. Re-generate each example with the updated skill.
2. Score the regenerated response against this file.
3. Compare to the committed example; any content regression should block the change.

---

## Maintenance

- When a new mode or section is added to `modes.md` or `templates.md`, add corresponding checks here.
- When a new guardrail is added to `guardrails.md`, add a matching shared fail condition here.
- Keep structural checks automatable; resist ambiguous criteria in that layer.
- Content checks should describe behavior, not enforce style.
