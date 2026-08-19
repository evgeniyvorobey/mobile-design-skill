# Paired comparison

Every other instrument in this repository scores one artifact against a written standard, and every one of them asks whether something is **stated**. This one asks a different question, of two artifacts at once: **which of these is the better design?**

It exists because that question could not previously be answered here, and the gap was measured rather than assumed.

## What was measured

Six real skill outputs were each given a twin that is a worse design while changing no value, deleting no statement and contradicting no bar — degraded only along ordering, emphasis allocation among conforming values, and coherence, the three axes no bar reaches. Corpus purity was verified by a checker, not asserted.

| instrument, same twelve pairs | separation |
|---|---|
| the nine rubric boundary questions | **0 of 12**, p = 1.000 |
| forced-choice paired comparison, no rubric | **12 of 12**, p = 0.00024 |

The rubric is not a rubber stamp: the same read reproduces only **10/12 = 83%** on unchanged text. It moves. It moves zero times out of twelve between a design and a worse version of it.

The comparison was also right for the right reason — all six signal pairs came back naming the exact injected degradation, unprompted — and it declined all six null-pair judgements. Full record: proposal sections 33-35.

## How to run it

```
python3 scripts/run_paired_eval.py --self-test
python3 scripts/run_paired_eval.py --arm-a A.jsonl --arm-b B.jsonl --nulls N.jsonl --export-requests pairs.jsonl
python3 scripts/run_paired_eval.py --arm-a A.jsonl --arm-b B.jsonl --nulls N.jsonl --verdicts v.jsonl
```

Arm files carry one `{"id", "response"}` object per line, the same shape `run_generation_eval.py` consumes. The null file carries a **cosmetic rewrite** of each of a subset of arm-A responses.

## The two refusals, and why they are in the tool

**A contrast without null pairs is not reported.** A judge handed two documents will find a winner. The only way to see that happening is to hand it two documents describing the same design in different words. At least three null pairs are required, and at least one for every three signal pairs, so the control can carry the contrast it guards.

**A contrast whose control failed is reported as unreadable, and exits non-zero.** If the judge names an agreed winner on more than a third of null pairs, no win rate from that run means anything. Every prior release in this series had to notice that kind of failure by hand, and three of them did not.

## Building the null pairs

A null must be a **cosmetic rewrite, not identical text**, and it must **not be length-matched to its original**. Identical text is a trivial null that any judge passes. A same-design/different-prose twin tests whether the judge reads the design or reads the document — and it is what bounds the shared-model-family confound, since the rewrite is written by the same kind of agent as everything else in the run. In the validation, judges declined all six cosmetic nulls at high confidence, so the instrument is not merely detecting that an agent edited a file.

**Vary the length of the rewrite, deliberately, by the same order the contrast varies it.** A null written to hold length constant is blind to a length effect, and length is the correlate this instrument most needs cleared: in the 18-pair run of proposal section 42 the longer document won 27 of 36 signal judgements (p = 0.004), and the six nulls of that run — written to a "within 5% of the original" instruction, so differing by a median 2.3% against the contrast's 13.7% — could not say whether that was bias or substance. Rebuilt as five nulls varying by -15% to +40%, with every numeric value, backticked token and heading verified to survive as an exact multiset, the judge returned `no-meaningful-difference` on **10 of 10** judgements at maximum confidence, including on a document 40% longer than its twin. That is what clears the confound; a matched control never could.

Hold the rewrite to: every `## ` heading identical and in order, the numeric-token multiset identical, length within a few percent, and no decision, order, pattern, role assignment or state behaviour changed.

## What it cannot do

- **It reads a document describing a screen, not a screen.** Nothing here escapes that channel; only a rendered artifact would.
- **Judge, author and null-writer share a model family.** The null pairs bound this confound. They do not remove it.
- **It compares. It does not score.** There is no band, no absolute number, and no way to ask it whether a single artifact is any good — only whether one is better than another. Most modes produce one artifact, so this is an evaluation instrument and not an authoring one.
- **The judge's verdict correlates with length on real contrasts, and that correlation is substance, not bias.** Measured both ways in section 42: 27 of 36 to the longer document on genuinely different designs, and 0 of 10 to the longer document when the design is held identical. Read a length gap between arms as a signal about how much each one decided, not as a defect in the instrument.
- **`confidence` does not track effect size.** In validation, confidence on null pairs (3.00) *exceeded* confidence on signal pairs (2.83), because certainty that two things are the same is still certainty. Do not read confidence as a proxy for how large a difference is.

## Where it belongs

Use it to compare two arms of skill output — before and after an instruction-text change, one prompt pack run twice against two trees. That is the pre/post question sections 13-35 of the proposal could not ask, and every release in that stretch measured a proxy instead: presence of a rule, coverage of a tier, correctness of a decision.

It does not replace `docs/design-quality-rubric.md`. The rubric answers what a single artifact states and where it sits; this answers which of two is better. Section 35 measured them disagreeing completely, and the rubric is still the instrument for everything a comparison cannot reach.
