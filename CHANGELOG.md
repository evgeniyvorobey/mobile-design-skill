# Changelog

All notable changes to this project will be documented in this file.

## [1.16.0] - 2026-05-29

### Added
- Mode D review: a causal **Findings** block (observation → violated principle → user consequence → change → predicted effect → Nielsen 0–4 severity → dimension moved), replacing the split issue/fix sections.
- Mode D review: a **current → projected** design-quality score (conditional, capped at 4/5, doubly-provisional for text-only D2/D3) with a per-dimension before/after table.
- Mode D review: an optional **Bold move** block for product-contradicting recommendations, gated by trigger and required fields (deviation, JTBD job, upside, risk, validation path, score impact, conviction).
- Distinctiveness levers and the "inert-screen test" in `docs/design-quality.md`, with a matching rubric cap so a competent-but-forgettable screen scores 3/5 with an upside note rather than a quiet 4/5.
- Heuristics: Cognitive Load Theory (Sweller), form-design principles (Wroblewski), and the Nielsen 0–4 severity scale in `docs/heuristics.md`.
- Inspiration: a derivation layer (production-reasoning sources, editorial/craft schools, and point-of-view products beyond Apple/Google), a generative direction method (JTBD → How-Might-We → Crazy Eights → de Bono → SCAMPER → translate-to-mechanism), and a reference→mechanism discipline in `docs/inspiration-sources.md`.
- Anti-pattern 8 (bold move vs aesthetic laundering); creative-range references and ideation-method links in `docs/sources.md`; NN/g benchmark citations in `docs/visual-benchmark-playbooks.md`.
- Proposal record at `docs/proposals/review-mode-upgrade.md`.

### Changed
- Mode D output contract updated across `skill/templates.md`, `skill/skill.md`, `skill/modes.md`, `docs/design-quality-rubric.md`, `docs/self-review.md`, `docs/evals.md`, `docs/workflow.md`, and `scripts/validate_repo.py`.
- Guardrail #4 carve-out: a product-contradicting recommendation is not aesthetic laundering when justified by a named usability/accessibility/hierarchy mechanism and surfaced in the Bold move block with its tradeoff and validation path.
- Regenerated Mode D calibration to the new format: `examples/review-screen.md`, `examples/golden/settings.md`, all `examples/visual-review-fixtures/`, and `examples/case-studies/social-privacy-settings.md`.

### Fixed (post senior-review hardening)
- Projected score is now a **flat median of the assessable dimensions**, not an inflated "up to N/5"; any higher post-visual-pass figure is confined to a `Ceiling note`. Corrected the arithmetic in all nine Mode D examples (five drop honestly from 4/5 to 3/5). A `must_not_contain` validator guard blocks the "up to" phrasing from returning.
- Reconciled the **Bold move trigger** with its examples: it requires current ≥3/5 AND no unresolved severity-3/4 finding. `examples/review-screen.md` (2/5) now correctly omits the Bold move; `examples/golden/settings.md` was made internally consistent (confirmed delete) so its Bold move is legitimately gated.
- Closed the **D2 visual-overclaim backdoor**: visual dimensions stay `n/v` and are never projected upward from a text-only review (fixed `settings.md` Color/state and the `review-screen.md` Composition row).
- Added a **severity crosswalk** (Nielsen 0–4 ↔ High/Med/Low ↔ P0–P3 ↔ quality-score caps) to `docs/heuristics.md`.
- Fixed stale Mode D references in `docs/evals.md` (accessibility section, projected-line label) and converted the Anti-pattern 4 "Good" fragment to the Findings format. Added a compressed-finding example and an inert-screen-test finding to `examples/golden/settings.md`.

## [1.15.0] - 2026-04-25

### Added
- Synthetic case-study calibration pack at `docs/synthetic-case-studies.md` and `examples/case-studies/`, covering 12 bad-to-good mobile design response cases without real products or screenshots.
- Text-only visual review fixture pack at `docs/visual-review-fixtures.md` and `examples/visual-review-fixtures/`, covering six Figma-like review scenarios with expected critique and prohibited overclaims.
- Benchmark report format at `docs/benchmark-report-format.md` plus `examples/benchmark-report.md` for turning 3-5 references into borrow / do-not-copy / token-component-state guidance.
- Domain packs under `docs/domain-packs/` for fintech, health, SaaS, marketplace, social, and education.
- Optional rendered-output QA workflow at `docs/rendered-output-qa.md` with report schema and sample report under `examples/rendered-output-qa/`.
- Machine-readable metadata for synthetic case studies, domain packs, visual review fixtures, benchmark reports, and rendered-output QA.

### Changed
- `SKILL.md`, the Claude Code wrapper, `skill/skill.md`, `skill/usage.md`, README, `docs/workflow.md`, `docs/evals.md`, and `docs/design-quality-rubric.md` now surface the synthetic calibration and optional QA layers.
- `scripts/validate_repo.py` now validates the new synthetic case studies, domain packs, visual review fixtures, benchmark report format, rendered-output QA schema/sample, and required references.

## [1.14.0] - 2026-04-25

### Added
- External judge command adapter in `scripts/run_rubric_judge.py` via `--judge-command`, allowing a separate agent process to receive judge requests on stdin and return judge-output JSONL on stdout.
- Interactive judged mode via `/mobile-design-skill --judge`, allowing the skill to draft, run an independent rubric judge pass in the same session when available, revise if needed, and return a compact `Judge summary`.
- Companion Claude Code custom agent at `.claude/agents/mobile-design-judge.md` for independent judged-mode scoring.
- Judged mode reference at `docs/judged-mode.md`, covering orchestration, judge prompt contract, fallback behavior, and final response shape.
- `--judge-command-output` and `--judge-command-timeout` options for saving agent output and bounding live semantic judge runs without adding provider keys to the repository.
- Deterministic oracle agent at `scripts/rubric_judge_oracle_agent.py` for CI-safe external command adapter self-tests.
- Versioned request schema marker `rubric-judge-request/v1` so external judge agents can stay stable across any LLM backend.
- Visual benchmark playbooks at `docs/visual-benchmark-playbooks.md` for Mobbin, Page Flows, Apple Design Awards, and Awwwards, with explicit inspiration-vs-evidence boundaries.
- Golden example calibration pack under `examples/golden/` for premium UI, enterprise SaaS, fintech, health, onboarding, settings, and checkout.
- Golden example index at `docs/golden-examples.md` for taste calibration and review expectations.
- Release validation command at `scripts/validate_release.py`, covering version/tag sanity, repository validation, judge dry-run, parser self-test, and external oracle self-test.
- Manual GitHub Actions release gate at `.github/workflows/release-validate.yml`.
- Release automation reference at `docs/release-automation.md`.

### Changed
- `docs/llm-judge-runner.md`, `docs/evals.md`, README, and metadata now document the LLM-agnostic external-agent judge workflow as the preferred open-source path.
- `SKILL.md`, the Claude Code wrapper, `skill/skill.md`, `skill/usage.md`, `docs/commands.md`, and `docs/evals.md` now surface `/mobile-design-skill --judge`.
- `SKILL.md`, the Claude Code wrapper, `skill/skill.md`, `skill/usage.md`, README, and metadata now surface visual benchmark playbooks and golden examples as quality calibration resources.
- `scripts/install.sh` now installs, reports, and uninstalls the companion `mobile-design-judge` agent alongside the skill.
- `scripts/validate_repo.py` now validates the external judge command contract, visual benchmark playbooks, golden examples, and release automation alongside JSONL export and output validation.
- GitHub Actions now self-tests the external judge command adapter without requiring model credentials.

## [1.13.1] - 2026-04-25

### Added
- Documentation hygiene validation for Markdown trailing whitespace and unexpected duplicate headings in `scripts/validate_repo.py`.

### Changed
- Canonical URL appendices in `docs/sources.md`, `docs/design-quality.md`, and `docs/inspiration-sources.md` now use normal Markdown links instead of hard-break URL formatting.
- Reference-pack documentation in `README.md`, `SKILL.md`, the Claude Code wrapper, and `skill/usage.md` now surfaces the full supporting docs set consistently.
- `docs/github-publishing.md` is now part of the required repository structure validation.

## [1.13.0] - 2026-04-25

### Added
- Clarification policy at `docs/clarification-policy.md`, defining when the skill should ask blocking questions vs proceed with labeled assumptions.
- Clarification examples at `examples/clarification-policy.md`, covering blocking visual review, non-blocking concept generation, and policy-sensitive healthcare specs.
- Machine-readable `clarification_policy` metadata and response contract fields for max questions, blocking criteria, fast path, and assumptions.

### Changed
- `SKILL.md`, `skill/skill.md`, `docs/workflow.md`, `docs/self-review.md`, `docs/guardrails.md`, `docs/evals.md`, `docs/sources.md`, `skill/modes.md`, `skill/templates.md`, and `skill/usage.md` now apply the ask-vs-assume policy.
- `scripts/validate_repo.py` now requires and validates the clarification policy layer, examples, and required references.
- `README.md`, the Claude Code wrapper, and `docs/commands.md` now surface the clarification behavior and examples.

## [1.12.0] - 2026-04-25

### Added
- Provider-agnostic LLM-as-judge runner at `scripts/run_rubric_judge.py` for exporting rubric judge JSONL requests and validating JSONL judge outputs against expected fixture scores.
- Runner documentation at `docs/llm-judge-runner.md`, including judge output contract, pass criteria, dry-run usage, JSONL export, and self-test flow.
- Machine-readable `llm_judge_runner` metadata and `llm_as_judge_runner` quality flag in `skill/metadata.yaml`.

### Changed
- `docs/evals.md` and `docs/design-quality-rubric.md` now document semantic judge calibration using `scripts/run_rubric_judge.py`.
- `scripts/validate_repo.py` now requires the runner and documentation, verifies the runner contract, and checks that CI/docs/metadata reference it.
- GitHub Actions now runs the judge runner dry-run and oracle-output parser self-test in addition to repository validation.
- `README.md`, `SKILL.md`, and `skill/usage.md` now surface the LLM-as-judge runner as a maintenance and calibration tool.

## [1.11.0] - 2026-04-25

### Added
- Rubric eval fixture pack under `examples/evals/`, covering expected design-quality scores from `1/5` through `5/5` with prompts, response excerpts, dimension scores, caps/hard limits, failed dimensions, rationales, and improvement suggestions.
- Before/after calibration example at `examples/rubric-before-after.md`, showing how a template-complete `2/5` UI spec is upgraded into a buildable `4/5` spec.
- Machine-readable rubric eval pack references under `design_quality_rubric.eval_pack` and `design_quality_rubric_eval_pack` in `skill/metadata.yaml`.

### Changed
- `docs/design-quality-rubric.md` and `docs/evals.md` now reference the fixture pack and explain how to use it for human review or future LLM-as-judge scoring.
- `scripts/validate_repo.py` now validates rubric fixtures as JSON, checks full score coverage `1..5`, verifies dimension-score keys, requires improvement suggestions, and validates the before/after example.
- `README.md`, `SKILL.md`, and `skill/usage.md` now surface the rubric eval pack as a calibration resource.

## [1.10.0] - 2026-04-25

### Added
- 1-5 design-quality scoring layer at `docs/design-quality-rubric.md`, with score levels, dimension scoring, caps/hard limits, final scoring method, improvement ladder, and self-review prompts.
- Machine-readable `design_quality_rubric` metadata and `design_quality_rubric_1_to_5` quality flag in `skill/metadata.yaml`.
- Score/target fields in relevant templates and examples: generated artifacts target 4/5; reviews expose current score with evidence limits.

### Changed
- `SKILL.md`, `skill/skill.md`, `docs/workflow.md`, `docs/design-quality.md`, `docs/sources.md`, `docs/self-review.md`, `docs/evals.md`, `docs/guardrails.md`, `skill/modes.md`, and `skill/templates.md` now apply the rubric when proposing, specifying, reviewing, or rationalizing design artifacts.
- `scripts/validate_repo.py` now requires `docs/design-quality-rubric.md`, verifies the layer is referenced by required surfaces, and checks committed examples for `1-5/5` quality score or target markers.
- `README.md`, the Claude Code wrapper, and `skill/usage.md` now reference `docs/design-quality-rubric.md`; version synchronized to `1.10.0`.

## [1.9.0] - 2026-04-25

### Added
- Known weaknesses and failure-mode prevention layer at `docs/weaknesses.md`, covering generic artifacts, template-complete but decision-empty output, first-idea bias, aesthetic laundering, evidence overreach, platform flattening, context blindness, happy-path-only design, visual overclaim, weak handoff, and overlong process theater.
- Machine-readable `weakness_prevention` metadata and `known_weakness_preflight` quality flag in `skill/metadata.yaml`.
- Anti-pattern calibration for template-complete but decision-empty UI specs in `examples/anti-patterns.md`.

### Changed
- `SKILL.md`, `skill/skill.md`, `docs/workflow.md`, `docs/sources.md`, `docs/self-review.md`, `docs/evals.md`, `docs/guardrails.md`, `skill/modes.md`, and `skill/templates.md` now use the weakness layer as an internal preflight before returning design output.
- `scripts/validate_repo.py` now requires `docs/weaknesses.md`, checks that required weakness patterns are present, and verifies the layer is referenced by the skill, docs, metadata, usage, and README surfaces.
- `README.md`, the Claude Code wrapper, and `skill/usage.md` now reference `docs/weaknesses.md`; version synchronized to `1.9.0`.

## [1.8.0] - 2026-04-25

### Added
- Design-quality calibration layer at `docs/design-quality.md`, grounded in Apple HIG, Material/Android, Fluent, GOV.UK, Baymard, and NN/g visual-design principles.
- New mode sections for design craft and production readiness: `Design quality calibration`, `Design quality requirements`, `Design quality issues`, `Visual rhythm rules`, and `Design quality rationale`.
- Metadata flag `design_quality_calibration` plus machine-readable design-quality dimensions in `skill/metadata.yaml`.

### Changed
- `SKILL.md`, `skill/skill.md`, `docs/workflow.md`, `docs/sources.md`, `docs/self-review.md`, and `docs/guardrails.md` now require visual hierarchy, composition, density, typography craft, color semantics, interaction polish, brand expression, and production-readiness reasoning when a response proposes or packages a design artifact.
- `skill/templates.md`, `skill/modes.md`, `docs/evals.md`, and `scripts/validate_repo.py` now enforce the design-quality sections for relevant modes.
- Golden examples for screen concept, UI spec, review, typography/spacing, and handoff now include concrete design-quality calibration rather than generic visual polish advice.
- `README.md`, the Claude Code wrapper, and `skill/usage.md` now reference `docs/design-quality.md`.

## [1.7.0] - 2026-04-25

### Added
- Inspiration/reference layer at `docs/inspiration-sources.md`, separating production UI references (Mobbin, Page Flows, UI Sources, Pttrns, Screenlane), platform/award references (Apple Design Awards, Material Design blog/case studies, Awwwards), and visual portfolio/moodboard references (Behance, Dribbble, Pinterest, Figma Community).
- Metadata support for non-authoritative inspiration sources via `inspiration_sources` and `inspiration_sources_separated_from_evidence`.
- Self-review prompts that check inspiration sources are separated from UX rationale, platform guidance, accessibility requirements, and compliance language.
- Automated example-response validation in `scripts/validate_repo.py`. The validator now extracts committed `## Example output` blocks and checks mode-specific structural contracts, accessibility sections, concrete values, decision tradeoffs, and non-generic next actions.

### Changed
- `SKILL.md`, `skill/skill.md`, and `docs/workflow.md` now instruct the skill to use inspiration sources only when requested or materially useful, and never as evidence for usability, accessibility, platform correctness, or compliance.
- `docs/sources.md`, `docs/guardrails.md`, and `docs/evals.md` now explicitly classify inspiration as a non-authoritative layer and treat misuse of inspiration as a fail condition.
- `README.md`, the Claude Code wrapper, and `scripts/validate_repo.py` now reference and require `docs/inspiration-sources.md`.
- `examples/generate-screen.md`, `examples/ui-spec.md`, `examples/review-screen.md`, `examples/typography-spacing.md`, and `examples/rationale-handoff.md` were updated to match the current templates and quality bars.
- GitHub Actions and README validation wording now reflect structure, link, and example-output validation.

## [1.6.1] - 2026-04-18

### Added
- Project logo at `assets/logo.svg` (horizontal lockup: mark + wordmark). Logo also mirrored at `.claude/skills/mobile-design-skill/logo.svg` for the Claude Code skill wrapper.
- Centered hero block in `README.md` displays the logo above the version / license badges.

### Changed
- `README.md` repository tree now lists `assets/` and the logo file in the wrapper directory.
- `scripts/bump_version.py` now recognizes the HTML `<img>` form of the version badge and the `Current version: **X.Y.Z**` line, in addition to the markdown-image badge. Previously only the markdown badge was updated; the HTML hero layout introduced in this release would have drifted.
- `scripts/validate_repo.py` requires `assets/logo.svg`.

## [1.6.0] - 2026-04-18

### Added
- Terminal install script at `scripts/install.sh` supporting global and project-scope installation, symlink (default) and self-contained copy methods, uninstall, and status inspection. After cloning the repo, a one-liner `./scripts/install.sh` installs the skill into `~/.claude/skills/mobile-design-skill`.
- Install-script awareness in `scripts/validate_repo.py` (`scripts/install.sh` now in `REQUIRED_FILES`).

### Changed
- `README.md` rewritten end-to-end with a terminal-first installation flow. New sections: Quickstart, What this skill does, Install (Claude Code via script / Claude Code manual / Codex / Claude API Python / Claude API TypeScript / Cursor and other IDEs), Usage, Supported modes, Architecture, Updating, Uninstalling, Customization, Versioning, Contributing. Each integration path has copy-pasteable commands.
- Repository architecture tree in README updated to include all v1.2.0–v1.5.0 additions (self-review, quality-bars, context-defaults, heuristics, patterns-catalog, evals, versioning, bump_version.py, install.sh, anti-patterns).

## [1.5.0] - 2026-04-18

### Added
- Patterns catalog at `docs/patterns-catalog.md` with decision matrices (Use-when / Avoid-when / Trade-offs / Red-flag) for: primary navigation (bottom nav vs drawer vs top tabs), back behavior, presentation overlays (modal vs sheet vs full-screen, bottom sheet variants, popover, action sheet), content display (list vs grid, card vs row, pagination strategies, accordion, carousel), actions (primary action placement, destructive confirmation vs undo, bulk actions, swipe actions), input (inline vs dedicated edit, picker variants, segmented vs dropdown vs tabs, search UX, form field grouping), feedback (toast vs snackbar vs banner vs alert, loading indicators, optimistic UI, error communication), states (empty, skeleton, error), forms (single-screen vs multi-step, validation timing, save strategy, required-field marking), onboarding (walkthrough vs coach marks vs just-in-time), search, notifications, authentication, accessibility, and platform divergence
- Self-review prompt block `Pattern selection` in `docs/self-review.md` — checks that patterns were chosen via matrix, losing alternative cited, and red flags inspected in Mode D reviews
- Metadata flag `pattern_catalog_grounded` on `skill/metadata.yaml`

### Changed
- `docs/workflow.md` Step 7 (design reasoning) now requires consulting `docs/patterns-catalog.md` for pattern-level decisions and forbids inventing novel patterns where established ones apply (Jakob's Law)
- `SKILL.md` and `skill/skill.md` updated to require pattern-catalog grounding in Step 8 / design reasoning
- `README.md` file index and repository tree reference `docs/patterns-catalog.md`
- `scripts/validate_repo.py` requires the new file

## [1.4.0] - 2026-04-18

### Added
- Context-aware defaults catalog at `docs/context-defaults.md` covering audience (older adults, children, power users, general consumer), domain (finance, health, social, e-commerce, enterprise, government, productivity, entertainment), platform (iOS, Android, cross-platform, tablet), and use-context (one-handed, outdoor, in-vehicle, emergency, at-desk), with explicit precedence for resolving conflicts across dimensions
- Heuristics catalog at `docs/heuristics.md` with mobile applications and red-flag violation patterns for Fitts, Hick, Miller, Jakob, Doherty, Tesler, Postel, Zeigarnik, Peak-End, Goal-Gradient, Serial-Position, Choice Overload, Recognition-over-Recall, Aesthetic-Usability, Von Restorff, Nielsen's 10, Gestalt principles, thumb zone, interruption-resilience, and one-screen-at-a-time
- Self-review prompts for context fit and heuristic grounding in `docs/self-review.md`
- Metadata flags `context_aware_defaults` and `heuristic_grounded_reasoning` on `skill/metadata.yaml`

### Changed
- `docs/workflow.md` Step 2 now applies context-aware defaults with documented precedence; Step 7 (design reasoning) now requires citing heuristics by name where they drive decisions
- `SKILL.md` and `skill/skill.md` updated with context-defaults precedence and heuristic-grounded reasoning requirement
- `README.md` file index and repository tree updated to reference `docs/context-defaults.md` and `docs/heuristics.md`
- `scripts/validate_repo.py` updated to require the new files

## [1.3.0] - 2026-04-18

### Added
- Semantic versioning policy at `docs/versioning.md` with bump rules and single-source-of-truth model
- Version bump automation at `scripts/bump_version.py` that synchronizes `skill/metadata.yaml`, both `SKILL.md` frontmatters, the README badge, and inserts a CHANGELOG placeholder
- `version:` field in the root `SKILL.md` frontmatter and `.claude/skills/mobile-design-skill/SKILL.md` frontmatter
- Version badge in `README.md`
- Mandatory self-review pass at `docs/self-review.md`, defining universal and mode-specific prompts the skill runs silently before returning any response
- Concrete numeric quality thresholds at `docs/quality-bars.md` covering typography (sizes, line-height, line length, scaling), touch targets (44pt iOS / 48dp Android minimums and gaps), color and contrast (WCAG 2.2 AA), motion (durations, easing, reduced-motion), spacing (canonical scale), forms, states (loading thresholds), navigation, accessibility specifics, and platform-specific anchors (iOS nav/tab bar, Android app bar / FAB)
- New workflow steps: Step 7 (apply design reasoning with explicit alternatives), Step 8 (check concrete quality bars), Step 9 (mandatory self-review); existing finalize step moved to Step 10
- `Alternatives considered` block in Mode A template
- `Key decision tradeoffs` block in Mode C template
- Alternative/reason pairing required in Mode F `Key design decisions` and `Pattern choices and why` blocks
- Metadata flags `mandatory_self_review`, `concrete_numeric_thresholds`, `design_reasoning_with_alternatives` on `skill/metadata.yaml`

### Changed
- `SKILL.md` and `skill/skill.md` updated with the new workflow steps (Apply design reasoning, Check concrete quality bars, Run mandatory self-review) and references to the new documents
- `docs/workflow.md` Step 6 (review lenses) now cross-references specific numeric bars in `docs/quality-bars.md`
- `README.md` file index and repository tree updated to reference `docs/quality-bars.md` and `docs/self-review.md`
- `scripts/validate_repo.py` updated to require the new files

## [1.2.0] - 2026-04-18

### Added
- Evaluation criteria document at `docs/evals.md` with structural, content, and hard-fail checks for each of the six modes
- Anti-pattern calibration set at `examples/anti-patterns.md` with six worked Bad / Good response pairs for underspecified input, description-only review, compliance echo, aesthetic-only advice, platform hallucination, and flows without recovery paths
- Mode D sub-case classification (D1 visual / D2 description only / D3 problem statement / D4 context change) in `skill/modes.md` with scope rules, validation checks, and fallback behavior per sub-case
- `Sub-case:` field in the Mode D output template (`skill/templates.md`)

### Changed
- `README.md` updated to reference the new `docs/evals.md` and `examples/anti-patterns.md` entries in the file index and repository structure
- `.gitignore` now excludes `.claude/vendor/` to prevent machine-specific absolute-path symlinks from being committed

### Fixed
- Removed duplicated `skill/` and `docs/` trees inside `.claude/skills/mobile-design-skill/` that contained a second level of nested duplicates; the Claude Code wrapper correctly resolves to the root `skill/` and `docs/` via relative paths

## [1.1.0] - 2026-03-26

### Added
- Canonical root `SKILL.md` with Codex-compatible frontmatter
- Claude Code project skill wrapper at `.claude/skills/mobile-design-skill/SKILL.md` for direct `/mobile-design-skill` invocation
- `agents/openai.yaml` UI metadata for Codex skill discovery
- GitHub Actions validation workflow in `.github/workflows/validate.yml`
- Repository validation script in `scripts/validate_repo.py`
- Canonical public URL appendix in `docs/sources.md`, consolidated from the external source curation document used during repo preparation
- GitHub publishing kit in `docs/github-publishing.md`
- Command reference in `docs/commands.md`

### Changed
- Updated `README.md` for GitHub-first publishing, Codex entrypoint guidance, and screenshot-free example-based presentation
- Refined maintenance guidance to keep `SKILL.md`, `skill/skill.md`, and `agents/openai.yaml` aligned

## [1.0.0] - 2026-03-26

### Added
- Initial production-ready release of `mobile-design-skill`
- Six supported modes:
  - Generate mobile screen concept
  - Design mobile user flow
  - Create platform-aware UI spec
  - Review screen for usability/accessibility
  - Create typography and spacing system
  - Prepare design rationale / handoff
- Main skill prompt in `skill/skill.md`
- Metadata file in `skill/metadata.yaml`
- Mode-by-mode requirements in `skill/modes.md`
- Output templates in `skill/templates.md`
- Usage guide in `skill/usage.md`
- Documentation set:
  - design principles
  - source hierarchy
  - guardrails
  - workflow
- Six complete worked examples
- GitHub-ready repository scaffolding
