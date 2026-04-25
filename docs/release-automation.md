# Release Automation

Manual release validation is handled by [`release-validate.yml`](../.github/workflows/release-validate.yml) and [`validate_release.py`](../scripts/validate_release.py).

## Validation Checks

The release validator is deterministic and does not require network access, model credentials, or API keys. It runs:

- Repository validation through [`scripts/validate_repo.py`](../scripts/validate_repo.py).
- Rubric judge fixture dry-run through [`scripts/run_rubric_judge.py`](../scripts/run_rubric_judge.py).
- Judge parser self-test by exporting expected oracle output and validating it back through the parser.
- External command oracle self-test through [`scripts/rubric_judge_oracle_agent.py`](../scripts/rubric_judge_oracle_agent.py).
- Version and tag sanity across [`skill/metadata.yaml`](../skill/metadata.yaml), [`SKILL.md`](../SKILL.md), the README badge/current version line, the Claude Code wrapper, and the top [`CHANGELOG.md`](../CHANGELOG.md) entry.

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

Use the **Release Validate** workflow from GitHub Actions. The optional `release_ref` input checks out the supplied tag/ref and verifies that it matches the canonical version.

Leave `release_ref` empty to validate the branch selected in the workflow UI. Set it to the release tag when validating an existing tag before publishing release notes.
