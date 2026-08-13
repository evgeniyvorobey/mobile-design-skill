# LLM-as-Judge Runner

This document defines the runner for semantic evaluation of the design-quality rubric fixtures.

The structural validator checks that examples and fixtures are well formed. The judge runner checks whether an LLM judge can assign the expected rubric score and explain the failure or quality level using the same dimensions as `docs/design-quality-rubric.md`.

---

## Runner script

Use:

```bash
python3 scripts/run_rubric_judge.py --dry-run
```

This loads every fixture under `examples/evals/` and confirms score coverage.

Export provider-agnostic JSONL judge requests:

```bash
python3 scripts/run_rubric_judge.py --export-jsonl tmp/rubric-judge-requests.jsonl
```

Validate JSONL judge outputs:

```bash
python3 scripts/run_rubric_judge.py --judge-output tmp/rubric-judge-results.jsonl
```

Run semantic calibration through an external judge agent command:

```bash
python3 scripts/run_rubric_judge.py \
  --judge-command "./scripts/local_judge_agent.sh" \
  --judge-command-output tmp/rubric-judge-results.jsonl
```

Self-test the parser and comparison logic without calling an LLM:

```bash
python3 scripts/run_rubric_judge.py \
  --export-expected-output tmp/rubric-judge-expected.jsonl \
  --judge-output tmp/rubric-judge-expected.jsonl
```

Self-test the external command adapter without calling an LLM:

```bash
python3 scripts/run_rubric_judge.py \
  --judge-command "python3 scripts/rubric_judge_oracle_agent.py"
```

The runner intentionally does not call a specific LLM provider. It emits a stable JSONL contract that can be used with Codex, Claude Code, OpenAI, Anthropic, local models, or any internal evaluation harness.

For public open-source use, prefer `--judge-command` over provider-specific adapters. The repository never needs API keys. The external command owns model selection, credentials, rate limits, and logging.

---

## LLM-agnostic contract

The external judge command must work regardless of which LLM the user prefers.

The runner only depends on process IO:

- stdin: request JSONL
- stdout: judge-output JSONL
- stderr: optional logs
- exit code: non-zero means failure

The command may call any backend: Codex, Claude Code, OpenAI, Anthropic, local models, a company gateway, or a human-in-the-loop script. The command is responsible for translating the generic `messages` array into whatever prompt shape that backend expects.

The request schema is versioned so adapters can stay stable:

```json
{
  "schema_version": "rubric-judge-request/v1",
  "id": "rubric-score-4-strong-leave-request",
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "expected": {
    "score": 4,
    "verdict": "strong and shippable"
  }
}
```

Adapters must not rely on a specific model family, token format, SDK, API key name, or hosted provider. If a backend cannot consume `system` / `user` messages natively, the adapter should flatten them into that backend's preferred prompt format.

---

## External judge command protocol

`--judge-command` runs a separate executable agent process.

The runner sends provider-agnostic judge request JSONL to the command's stdin. Each line has:

- `schema_version`
- `id`
- `messages`
- `expected`

The command must write judge-output JSONL to stdout using the same contract as `--judge-output`.

The command may write logs to stderr. Stdout must remain machine-readable JSONL.

For commands with pipes, shell-specific setup, or secrets, put the logic in a wrapper script and pass the script path:

```bash
python3 scripts/run_rubric_judge.py \
  --judge-command "./scripts/local_judge_agent.sh"
```

Save the raw stdout before validation when debugging:

```bash
python3 scripts/run_rubric_judge.py \
  --judge-command "./scripts/local_judge_agent.sh" \
  --judge-command-output tmp/rubric-judge-results.jsonl
```

Bound long-running judge agents:

```bash
python3 scripts/run_rubric_judge.py \
  --judge-command "./scripts/local_judge_agent.sh" \
  --judge-command-timeout 600
```

`scripts/rubric_judge_oracle_agent.py` is intentionally not a real judge. It echoes the expected fixture outcomes from stdin and exists only to prove that the external command protocol works in CI.

---

## Judge output contract

Each judge output line must include the fixture id and a JSON object with this shape:

```json
{
  "id": "rubric-score-3-acceptable-baseline-delivery-status",
  "judge": {
    "score": 3,
    "verdict": "acceptable baseline",
    "cap": "No cap",
    "hard_limits": [],
    "dimension_scores": {
      "attention_path_and_hierarchy": 4,
      "composition_and_spacing": 3,
      "typography_craft": 3,
      "color_state_and_contrast": 3,
      "density_and_rhythm": 3,
      "interaction_polish_and_motion": 3,
      "context_and_brand_fit": 3,
      "production_readiness": 3,
      "distinctiveness_and_owned_assets": 2
    },
    "failed_dimensions": [
      "production readiness",
      "color/state specificity",
      "typography craft"
    ],
    "rationale": "The response covers the task but lacks concrete production mechanisms.",
    "improvement_suggestions": [
      "Add semantic status treatment with non-color cues.",
      "Add token-ready spacing and typography values."
    ]
  }
}
```

The runner also accepts records where the judge JSON appears under `output`, `response`, or `result`, as long as a JSON object can be extracted.

---

## Pass criteria

For every fixture:

- score must match `expected_score`
- verdict must include the expected verdict phrase
- dimension scores must include all rubric dimensions as integers from 1 to 5
- expected hard limits must appear in the judge result when the fixture defines them
- expected failed dimensions must appear in the judge result or rationale
- improvement suggestions must contain at least two concrete items

Extra output ids fail the run. Missing fixture ids fail the run.

---

## What this runner does not do

It does not replace human design judgment. It checks calibration: whether the judge applies the same rubric consistently across known examples.

It also does not make a weak generated response stronger by itself. It tells the skill maintainers when the scoring model drifts from the rubric.

It does not store or require provider API keys. Authentication belongs to the external agent command or the environment that runs it.

---

## Maintenance

When adding a new rubric fixture:

1. Add a JSON fixture under `examples/evals/`.
2. Include every required field used by `scripts/validate_repo.py`.
3. Include all nine dimension scores — the set in `RUBRIC_DIMENSIONS` in `scripts/validate_repo.py`, which the rubric's dimension table matches row for row.
4. Add at least two improvement suggestions.
5. Run `python3 scripts/validate_repo.py`.
6. Run `python3 scripts/run_rubric_judge.py --dry-run`.
7. Run `python3 scripts/run_rubric_judge.py --judge-command "python3 scripts/rubric_judge_oracle_agent.py"`.
8. If you use a live judge agent, run `python3 scripts/run_rubric_judge.py --judge-command "<your-agent-command>"`.

---

## What the CI self-tests do and do not prove

`scripts/rubric_judge_oracle_agent.py` echoes each fixture's expected values back on stdout. The CI steps that use it prove the JSONL contract — request shape, parser, stdin/stdout adapter — and nothing about design quality. No model runs in CI, and no generated response is scored there. A change to `SKILL.md` that degrades live output cannot fail these steps.

Real semantic calibration requires the external-agent command path with an actual model behind it, run during maintenance. Reading a green CI badge as evidence of output quality is the mistake these step names now guard against.
