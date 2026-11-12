# mobile-design-skill

A mobile UI/UX design skill for Claude Code, Codex and the Claude API. What the model reads at runtime is `SKILL.md`, `skill/platform.md` and the `docs/` files `SKILL.md` names; the rest is tooling, calibration material and record.

## Layout

- `SKILL.md`: canonical entrypoint, the whole default behaviour. Section 5 lists the docs read only on request.
- `skill/`: `platform.md` (dated platform facts) and `metadata.yaml`.
- `.claude/skills/mobile-design-skill/SKILL.md`: thin wrapper that reaches the canonical files through `${CLAUDE_SKILL_DIR}/../../../`, so every runtime file keeps its repository-relative path.
- `.claude/agents/mobile-design-judge.md`: the independent judge for `/mobile-design-skill --judge`.
- `.claude/skills/mobile-logo-system/`, `.claude/vendor/`: a gitignored local install of the sibling skill, owned by `~/Documents/mobile-logo-system`. Edit it there.
- `docs/`: references and instruments; `docs/evals.md` says which instrument answers which question.
- `examples/evals/`: rubric fixtures and gate brief sets. Held-out sets stay sealed until a gate run opens them.
- `scripts/`: validators, installer, version bumper, eval runners.

## Changing the skill

1. Edit, then run what CI runs (`.github/workflows/validate.yml`): `python3 scripts/validate_repo.py`, `python3 scripts/verify_install.py`, `python3 scripts/run_rubric_judge.py --dry-run`. Done is all green.
2. A new `docs/` file goes into `REQUIRED_FILES` in `scripts/validate_repo.py`, and either into `SKILL.md` section 5 or into `SKILL_ENTRYPOINT_DOC_EXCLUSIONS` with the reason.
3. The validators check structure, never quality. When runtime text changed (`SKILL.md`, `skill/`, a doc `SKILL.md` points to), run the release gate `scripts/run_baseline_gate.py` (procedure in `docs/paired-comparison.md`) or `scripts/run_paired_eval.py`, and record the result, pass or fail, in the CHANGELOG entry. A release without the gate says so there.
4. Bump with `python3 scripts/bump_version.py major|minor|patch` (it syncs every version reference; policy in `docs/versioning.md`), and run `python3 scripts/validate_release.py` before a tag.

## Source of truth and copies

This repo is the source of truth. After a change, report which copies need a sync and leave the sync to the owner.

- `~/.claude/skills/mobile-design-skill/`: link install. Its generated wrapper holds absolute paths into the main checkout `~/Documents/mobile-design-skill`, so content follows that checkout once it is pulled. Re-run `./scripts/install.sh` when the wrapper or the judge agent changed.
- `~/Documents/thera_tales/.claude/skills/mobile-design-skill/`: a full copy with its own wrapper `SKILL.md`; its `SKILL.md.canonical` mirrors this repo's `SKILL.md`.
