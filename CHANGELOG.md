# Changelog

All notable changes to this project will be documented in this file.

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
