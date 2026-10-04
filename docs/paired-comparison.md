# Paired comparison

Every other instrument in this repository scores one artifact against a written standard, and every one of them asks whether something is **stated**. This one asks a different question, of two artifacts at once: **which of these is the better design?**

It exists because that question could not previously be answered here, and the gap was measured rather than assumed.

## What was measured

Six real skill outputs were each given a twin that is a worse design while changing no value, deleting no statement and contradicting no bar — degraded only along ordering, emphasis allocation among conforming values, and coherence, the three axes no bar reaches. Corpus purity was verified by a checker, not asserted.

| instrument, same twelve pairs | separation |
|---|---|
| the nine rubric boundary questions | **0 of 12**, p = 1.000 |
| forced-choice paired comparison, no rubric | **12 of 12** judgements, **6 of 6** pairs, two-sided sign test p = 0.031 |

The rubric is not a rubber stamp: the same read reproduces only **10/12 = 83%** on unchanged text. It moves. It moves zero times out of twelve between a design and a worse version of it.

The comparison was also right for the right reason — all six signal pairs came back naming the exact injected degradation, unprompted — and it declined all six null-pair judgements. Full record: proposal sections 33-35.

## How to run it

```
python3 scripts/run_paired_eval.py --self-test
python3 scripts/run_paired_eval.py --arm-a A.jsonl --arm-b B.jsonl --nulls N.jsonl --export-requests pairs.jsonl
python3 scripts/run_paired_eval.py --arm-a A.jsonl --arm-b B.jsonl --nulls N.jsonl --verdicts v.jsonl
```

Arm files carry one `{"id", "response"}` object per line. The null file carries a **cosmetic rewrite** of each of a subset of arm-A responses.

## The two refusals, and why they are in the tool

**A contrast without null pairs is not reported.** A judge handed two documents will find a winner. The only way to see that happening is to hand it two documents describing the same design in different words. At least three null pairs are required, and at least one for every three signal pairs, so the control can carry the contrast it guards.

**A contrast whose control failed is reported as unreadable, and exits non-zero.** If the judge names an agreed winner on more than a third of null pairs, no win rate from that run means anything. Every prior release in this series had to notice that kind of failure by hand, and three of them did not.

**The judge never sees which pair is a null, or the presentation order.** Each request carries an opaque id; the internal id (`null-p3-ab`) stays inside the harness, because a judge that could read it could pass the control and pick an arm without reading either document. A failed control prints the control and nothing else: no win rate or p-value reaches stdout.

**The unit of inference is the pair.** Both presentation orders of one pair judge the same two documents, so the p-value is a two-sided exact sign test over pairs (a pair goes to the arm that won more of its two judgements; ties are dropped), not a binomial over judgements.

## Building the null pairs

A null must be a **cosmetic rewrite, not identical text**, and it must **not be length-matched to its original**. Identical text is a trivial null that any judge passes. A same-design/different-prose twin tests whether the judge reads the design or reads the document — and it is what bounds the shared-model-family confound, since the rewrite is written by the same kind of agent as everything else in the run. In the validation, judges declined all six cosmetic nulls at high confidence, so the instrument is not merely detecting that an agent edited a file.

**Vary the length of the rewrite, deliberately, by the same order the contrast varies it.** A null written to hold length constant is blind to a length effect, and length is the correlate this instrument most needs cleared: in the 18-pair run of proposal section 42 the longer document won 27 of 36 signal judgements (p = 0.004), and the six nulls of that run — written to a "within 5% of the original" instruction, so differing by a median 2.3% against the contrast's 13.7% — could not say whether that was bias or substance. Rebuilt as five nulls varying by -15% to +40%, with every numeric value, backticked token and heading verified to survive as an exact multiset, the judge returned `no-meaningful-difference` on **10 of 10** judgements at maximum confidence, including on a document 40% longer than its twin. That is what clears the confound; a matched control never could.

Hold the rewrite to: every `## ` heading identical and in order, the numeric-token multiset identical, the length deliberately varied as above (never matched), and no decision, order, pattern, role assignment or state behaviour changed. The harness refuses a null whose text is identical to its original.

## The release gate: skill versus no skill

Every comparison above sets the skill against itself. The first comparison with the same model and **no skill**, on 2026-10-01, went to the baseline on 8 briefs of 8 (two-sided sign test over briefs, p = 0.0078), with three cosmetic nulls and two format nulls holding. `scripts/run_baseline_gate.py` makes that comparison repeatable and reads a rule off it. All three parts are required:

1. **The null control is readable.** If it is not, the run is unreadable (exit 2): neither a pass nor a fail.
2. **Skill share is at least 0.5**, where share = (pairs won + half the pairs tied) / pairs. A draw passes, because the claim under test is "not worse than no skill".
3. **The skill arm carries no more medium-or-high errors than the baseline arm**, in a blind error audit of both.

**When it runs.** Before tagging a release that changes what the model reads at runtime: `SKILL.md`, `skill/`, `docs/` outside `docs/proposals/`, or the committed examples. The result goes in that release's CHANGELOG entry either way. While the gate is red, a release ships only if it does not lower the share on the same brief set, and says the gate is red; red is a state the repository is in, not one to hide. The gate needs a model, so it is a maintainer step. CI runs `--self-test`, which proves the rule passes, fails and refuses as specified.

**Brief sets** (`examples/evals/baseline-gate-briefs.json`):

- `core` is the eight briefs of the 2026-10-01 run. It is the working set: those briefs have been read while fixing the skill, so a win on them is not held-out evidence.
- `extended` is core plus the ten prompts of `generation-prompts.json`, for a core result that sits inside the noise. Two draws of unchanged text differ by one or two pairs, so a change expected to move that much needs sixteen briefs or more, not eight.
- `held-out` is sixteen briefs, S01 to S16, written by an independent agent that read only the existing briefs, checked by a second, and committed in `examples/evals/baseline-gate-heldout.json` with their sha-256 pinned in the brief pack. Do not read a sealed set while tuning. Open it for a release decision that claims the skill beats no skill, and once a held-out run has informed a change, write a new sealed set. The committed set was written on 2026-10-04 and opened the same day by the run that released 2.1.0, so it is a working set now, and the next held-out claim needs a new one. The eight briefs opened on 2026-10-03 (H1 to H8) are in `baseline-gate-heldout-2026-10-03.json`; the pack names that file under `opened_held_out_files`, and its briefs are usable as an open set. Have the set written and checked by agents that do not read `SKILL.md`, `skill/`, `docs/` or any run record, and keep the brief text out of everything the maintainer reads until the score.

**Procedure.**

```
python3 scripts/run_baseline_gate.py --set core --export-requests requests.jsonl
python3 scripts/run_baseline_gate.py --arm-skill S.jsonl --arm-baseline B.jsonl \
    --export-audit-requests audit.jsonl
python3 scripts/run_baseline_gate.py --arm-skill S.jsonl --arm-baseline B.jsonl --nulls N.jsonl \
    --export-judge-requests judge.jsonl
python3 scripts/run_baseline_gate.py --arm-skill S.jsonl --arm-baseline B.jsonl --nulls N.jsonl \
    --verdicts verdicts.jsonl --errors errors.jsonl
```

- Freeze the tree the skill arm reads — a `git worktree` at the candidate commit — and write the predictions and the decision rule down before any generator starts.
- One generator per request. Both arms get the same framing and differ in one instruction: load the skill, or answer as you normally would. The baseline arm reads no file.
- Generate both arms in one batch and at one effort level, and write the effort level into the pre-registration. Do not reuse a baseline arm from another day: on 2026-10-03 the same model with no skill answered the same briefs at 0.36 to 0.44 of the length it wrote on 2026-10-01, and two runs that had reused the older arm reported a length and a time ratio that a same-batch run did not reproduce. Subagents inherit the session's effort level, and a result at one level does not carry to another: the same skill tied a one-sentence request at `max` and led it at `xhigh`, on two different days.
- Nulls are cosmetic rewrites of skill-arm responses, built as the section above says: at least three, at least one for every three briefs, lengths varied.
- One judge per judge request and one auditor per small group of audit requests. Both see opaque ids and neutral file names; a judge request carries the brief, and the audit mixes the two arms.
- Record the cost beside the verdict: minutes and tokens per skill generation, and output-limit hits. A skill that draws while taking three times as long has not earned its place.

**What it does not show.** A run is 8 to 18 briefs, one draw per cell. Judges, generators, rewriters and auditors share a model family. Documents are judged, not screens. And a same-model baseline says nothing about a weaker model, where a skill may be worth more.

## What it cannot do

- **It reads a document describing a screen, not a screen.** Nothing here escapes that channel; only a rendered artifact would.
- **Judge, author and null-writer share a model family.** The null pairs bound this confound. They do not remove it.
- **It compares. It does not score.** There is no band, no absolute number, and no way to ask it whether a single artifact is any good — only whether one is better than another. Most modes produce one artifact, so this is an evaluation instrument and not an authoring one.
- **The judge's verdict correlates with length on real contrasts, and that correlation is substance, not bias.** Measured both ways in section 42: 27 of 36 to the longer document on genuinely different designs, and 0 of 10 to the longer document when the design is held identical. Read a length gap between arms as a signal about how much each one decided, not as a defect in the instrument.
- **`confidence` does not track effect size.** In validation, confidence on null pairs (3.00) *exceeded* confidence on signal pairs (2.83), because certainty that two things are the same is still certainty. Do not read confidence as a proxy for how large a difference is.

## Where it belongs

Use it to compare two arms of skill output — before and after an instruction-text change, one prompt pack run twice against two trees. That is the pre/post question sections 13-35 of the proposal could not ask, and every release in that stretch measured a proxy instead: presence of a rule, coverage of a tier, correctness of a decision.

It does not replace `docs/design-quality-rubric.md`. The rubric answers what a single artifact states and where it sits; this answers which of two is better. Section 35 measured them disagreeing completely, and the rubric is still the instrument for everything a comparison cannot reach.
