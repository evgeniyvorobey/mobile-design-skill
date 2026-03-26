# Changelog

All notable changes to this project will be documented in this file.

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
