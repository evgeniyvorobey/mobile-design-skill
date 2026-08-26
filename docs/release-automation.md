# Release Automation

Release validation is handled by [`release-validate.yml`](../.github/workflows/release-validate.yml) and [`validate_release.py`](../scripts/validate_release.py). The workflow runs automatically on every pushed `v*` tag, and can also be dispatched by hand against any ref.

## Validation Checks

The release validator is deterministic and does not require network access, model credentials, or API keys. It runs:

- Repository validation through [`scripts/validate_repo.py`](../scripts/validate_repo.py).
- Install verification through [`scripts/verify_install.py`](../scripts/verify_install.py): both install methods are performed into a throwaway directory and every path either wrapper names is resolved against what was actually installed.
- Diversity metric self-test through [`scripts/run_diversity_eval.py`](../scripts/run_diversity_eval.py).
- Generation eval prompt pack and oracle replay through [`scripts/run_generation_eval.py`](../scripts/run_generation_eval.py) and [`scripts/generation_oracle_agent.py`](../scripts/generation_oracle_agent.py).
- Paired comparison self-test and judge adapter through [`scripts/run_paired_eval.py`](../scripts/run_paired_eval.py) and [`scripts/paired_eval_oracle_agent.py`](../scripts/paired_eval_oracle_agent.py).
- Rubric judge fixture dry-run through [`scripts/run_rubric_judge.py`](../scripts/run_rubric_judge.py).
- Judge parser self-test by exporting expected oracle output and validating it back through the parser.
- External command oracle self-test through [`scripts/rubric_judge_oracle_agent.py`](../scripts/rubric_judge_oracle_agent.py).
- Version and tag sanity across [`skill/metadata.yaml`](../skill/metadata.yaml), [`SKILL.md`](../SKILL.md), the README badge/current version line, the Claude Code wrapper, and the top [`CHANGELOG.md`](../CHANGELOG.md) entry.
- CHANGELOG shape: the top entry must be a semver heading, must carry a non-empty body, and no version may head two entries. An unfilled `## [Unreleased]` placeholder, an empty entry, and a placeholder left above the real entry are each rejected.

Every check above runs in CI on a pushed `v*` tag. Nothing in this file is manual-only.

## Local Command

Run the full release validation before tagging:

```sh
python3 scripts/validate_release.py
```

To validate against a planned release tag:

```sh
python3 scripts/validate_release.py --tag-or-ref v1.14.0
```

The supplied tag/ref must match `v<version>` from `skill/metadata.yaml`. Both `v1.14.0` and `refs/tags/v1.14.0` are accepted forms.

## GitHub Action

**Release Validate** runs automatically on every pushed tag matching `v*`. The tag is passed to the validator as `--tag-or-ref`, so a tag whose name does not match `v<version>` from `skill/metadata.yaml` fails the run.

The workflow can also be dispatched by hand. The optional `release_ref` input checks out the supplied tag/ref and verifies that it matches the canonical version; leave it empty to validate the branch selected in the workflow UI.
