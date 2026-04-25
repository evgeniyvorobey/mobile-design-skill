# Rendered Output QA

Rendered-output QA is an optional workflow for checking a design after it exists as a visible artifact: HTML, local app build, running prototype, or screenshot. It is not required for normal skill usage and does not add mandatory dependencies.

Use it when the user asks to validate an implemented mobile screen, when a design has been translated into code, or when a screenshot/prototype reveals visual behavior that a text-only spec cannot verify.

## Purpose

The workflow catches implementation and visual-regression issues that are hard to prove from a written design spec:

- mobile viewport fit
- overlap, clipping, and text overflow
- tap target risk
- contrast risk
- responsive behavior
- loading, empty, and error states
- keyboard and focus behavior
- reduced-motion behavior

It complements `docs/design-quality-rubric.md`. A strong written design can still fail rendered QA if it clips text, hides the primary action behind the keyboard, or breaks at common mobile widths.

## When to use

Use rendered-output QA only when at least one concrete artifact is available:

- running local web app or HTML page
- native app build, simulator, emulator, or preview
- interactive prototype
- screenshot supplied by the user
- recorded screen flow

Do not block normal design generation waiting for screenshots or a local build. If no rendered artifact exists, produce the design/spec normally and list rendered QA as a recommended next action.

## Inputs

Minimum useful inputs:

- product or screen name
- platform scope: iOS, Android, cross-platform, mobile web
- artifact type: local URL, app build, prototype, screenshot, or recording
- primary task to validate
- target states if known: default, loading, empty, error, success

Optional inputs:

- design tokens or design-system constraints
- expected breakpoints or supported devices
- known accessibility requirements
- expected motion behavior
- locale, text scaling, dark mode, or high-contrast requirements

## Workflow

### 1. Establish evidence

Classify the artifact and state what can be verified.

- Running app/HTML: layout, interaction, focus, keyboard, responsive behavior, and state transitions may be checked.
- Screenshot: static layout, visible clipping, hierarchy, approximate tap-target risk, and contrast risk may be checked.
- Recording: timing, transition continuity, loading behavior, and interaction feedback may be checked, but DOM/focus details remain unverified.
- Text-only description: do not run rendered-output QA; use normal screen review and label visual claims as unverified.

### 2. Exercise mobile viewports

Check at least:

- narrow phone viewport around 320-360 px wide
- common phone viewport around 390-430 px wide
- tall phone viewport
- landscape only if the product supports it
- tablet only if the product claims tablet support

For native apps, map these to the nearest simulator/emulator devices. For mobile web, use browser device emulation or project-owned responsive test tooling if already available.

### 3. Inspect layout integrity

Look for:

- overlapping text, controls, icons, badges, sheets, or sticky bars
- clipped labels, counters, prices, dates, names, or CTAs
- text overflow caused by localization, long content, or dynamic type
- unsafe-area problems around notches, home indicators, and sticky CTAs
- content hidden behind keyboard, bottom navigation, or modal sheets
- containers that resize unexpectedly when loading text or errors appear

### 4. Check interaction ergonomics

Look for:

- tap targets that appear below 44 pt on iOS or 48 dp on Android
- controls placed too close together for repeated use
- destructive actions too close to primary actions
- swipe, drag, or gesture interactions without visible alternatives
- disabled controls without explanation
- pressed, loading, success, and error feedback

Treat tap target measurements as hints unless the implementation exposes exact dimensions.

### 5. Check state coverage

Verify the artifact includes or can simulate:

- default state
- loading state
- empty state
- error state
- success or completion state where relevant
- offline or retry state where relevant
- permission-denied state where relevant

If a state is not available in the artifact, report it as "not verified" instead of inventing a pass/fail result.

### 6. Check accessibility behavior

Check what the artifact allows:

- readable text at expected mobile sizes
- visible focus indication for keyboard or switch-control style navigation
- logical focus order when a browser, simulator, or accessibility tooling exposes it
- keyboard avoiding critical fields and actions
- reduced-motion behavior for transitions, loaders, and animated feedback
- dark mode, increased contrast, or large text only if the artifact supports toggling them

Do not claim WCAG compliance from visual inspection alone. Use "contrast risk" or "contrast appears acceptable from available evidence" unless measured values are available.

### 7. Report and revise

Create a compact report with:

- artifact and viewport coverage
- passed checks
- unresolved checks
- findings with severity and evidence
- recommended fixes
- whether a design-quality score should be capped by rendered issues

Use `examples/rendered-output-qa/report-schema.json` as the report contract and `examples/rendered-output-qa/sample-report.json` as a concrete example.

The report schema version is `rendered-output-qa/v1`.

## Check catalog

### Mobile viewports

Goal: prove the screen remains usable across expected phone sizes.

Pass signals:

- primary task is visible without awkward horizontal scrolling
- sticky navigation and CTAs respect safe areas
- hierarchy remains recognizable on narrow and common viewports
- important content does not disappear at width changes

Common failures:

- CTA falls below bottom safe area
- horizontal scroll appears on a phone viewport
- two-column desktop pattern survives into mobile
- modal sheet leaves too little usable content area

### Overlap, clipping, and text overflow

Goal: catch visual integrity failures.

Pass signals:

- no visible text/control overlap
- long names, prices, labels, and dates wrap, truncate, or resize intentionally
- error messages do not push controls into unusable positions
- loading placeholders reserve stable dimensions

Common failures:

- badge overlaps title
- price truncates in checkout summary
- error text hides submit button
- skeleton loading shifts layout after content loads

### Tap target hints

Goal: identify likely touch ergonomics issues.

Pass signals:

- common controls visually meet 44 pt iOS / 48 dp Android target guidance or have enough hit-area padding
- adjacent controls have adequate spacing
- destructive and primary actions are not easily mis-tapped

Common failures:

- icon-only controls are visually tiny with no apparent hit area
- list-row trailing actions are crowded
- close button sits too close to drag handle or system edge

### Contrast hints

Goal: identify likely readability and state-recognition issues.

Pass signals:

- primary text and key controls appear readable in the tested theme
- disabled and secondary states remain distinguishable without relying on color alone
- error/success/warning states include non-color cues where relevant

Common failures:

- placeholder text is too close to background
- disabled CTA looks enabled or primary CTA looks disabled
- chart or status color is the only signal

### Responsive behavior

Goal: confirm layout adapts intentionally, not accidentally.

Pass signals:

- components reflow predictably at narrow/common phone widths
- fixed-position elements do not cover content
- dynamic content does not change the screen's basic rhythm
- optional tablet/landscape layouts have explicit behavior

Common failures:

- card grids squeeze instead of stacking
- sticky CTA covers final form fields
- bottom sheet consumes almost the whole viewport

### Loading, empty, and error states

Goal: ensure users can understand and recover from non-happy paths.

Pass signals:

- loading state preserves context and avoids layout jump
- empty state explains the condition and next useful action
- error state states what happened and how to recover
- retry or offline behavior does not trap the user

Common failures:

- spinner-only loading on a high-stakes or slow operation
- empty state is decorative but gives no action
- error message appears far from the failing field

### Keyboard and focus

Goal: validate input-heavy screens and accessibility navigation.

Pass signals:

- focused field remains visible above the keyboard
- primary action remains reachable or has a clear alternative
- focus order follows visual/task order
- modals trap focus while open and restore it when closed where the platform supports this behavior

Common failures:

- keyboard hides password or payment fields
- fixed footer covers validation errors
- focus jumps from header to footer before form fields

### Reduced motion

Goal: prevent animation from becoming a usability or accessibility problem.

Pass signals:

- reduced-motion mode removes or shortens non-essential motion
- loading and success feedback remain understandable without motion
- parallax, large transitions, and repeated loops have calmer alternatives

Common failures:

- screen transition depends on motion to explain navigation
- animated success state has no static confirmation
- repeated shimmer or loop cannot be reduced

## Browser or Playwright Workflow

This repository does not require Playwright or browser automation for every user. Use the tooling already present in the target project.

Conceptual browser workflow:

1. Open the local build, prototype, or supplied HTML.
2. Set target mobile viewport(s).
3. Capture observations manually or with existing screenshot tooling.
4. Exercise relevant states and input behavior.
5. Record findings using the rendered-output QA report format.

Conceptual Playwright-style workflow, only when the project already has it:

1. Launch the local URL with mobile viewport presets.
2. Navigate to the target screen.
3. Capture screenshots or traces for evidence.
4. Inspect element bounding boxes for overlap, clipping, and tap-target hints.
5. Toggle state fixtures, query params, mocks, or storybook states if available.
6. Emulate reduced motion, dark mode, locale, or text scaling where the project supports it.
7. Emit a JSON report that follows `examples/rendered-output-qa/report-schema.json`.

The skill should never tell a user that Playwright is required just to design or review a mobile screen. Rendered-output QA is a higher-confidence add-on after a visible artifact exists.

## Report format

Use JSON when the report may be consumed by automation. Use markdown when the user only needs a human review, but preserve the same concepts:

- `artifact`
- `coverage`
- `summary`
- `checks`
- `findings`
- `unverified`
- `recommendations`

Machine-readable examples live in:

- `examples/rendered-output-qa/report-schema.json`
- `examples/rendered-output-qa/sample-report.json`

## Severity scale

- `blocker`: prevents completing the primary task or creates serious accessibility/usability risk
- `high`: likely to cause user failure, hidden information, or repeated mistakes
- `medium`: degrades clarity, efficiency, or trust but has a workable path
- `low`: polish or resilience issue that should be fixed before final release
- `info`: observation, coverage note, or non-blocking recommendation

If a rendered issue blocks the primary task, cap the design-quality score at 2/5 until fixed. If the artifact is usable but has visible clipping, missing state coverage, or uncertain contrast, cap at 3/5 unless there is strong mitigating evidence.

## Evidence boundaries

Rendered-output QA must separate observed facts from inferred risks.

Use:

- "Observed" for direct evidence from the artifact.
- "Likely" for visual/touch/contrast risk without exact measurement.
- "Not verified" when the artifact does not expose the state or behavior.
- "Requires instrumentation" when a result needs DOM bounds, native accessibility tree, contrast values, or analytics.

Do not invent:

- accessibility compliance
- exact contrast ratios without measurement
- business impact
- device support beyond tested viewports
- state behavior that was not reachable

## Integration with the skill

When rendered-output QA is requested, the skill should:

1. Classify the normal mobile-design mode first.
2. State the artifact type and what can be verified.
3. Run the rendered-output checklist only for available evidence.
4. Produce findings with severity, evidence, and fix guidance.
5. Keep unverified items explicit.
6. Recommend the smallest design or implementation change that removes the risk.

Rendered-output QA is strongest after a generated design has been implemented. It should raise the confidence of the design-quality rubric, not replace the design reasoning that created the screen.
