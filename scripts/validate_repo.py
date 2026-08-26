#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "SKILL.md",
    ".github/workflows/validate.yml",
    ".github/workflows/release-validate.yml",
    ".claude/skills/mobile-design-skill/SKILL.md",
    ".claude/agents/mobile-design-judge.md",
    "agents/openai.yaml",
    "skill/metadata.yaml",
    "skill/modes.md",
    "skill/templates.md",
    "skill/usage.md",
    "docs/clarification-policy.md",
    "docs/context-defaults.md",
    "docs/adaptive-layout.md",
    "docs/benchmark-report-format.md",
    "docs/design-quality.md",
    "docs/design-quality-rubric.md",
    "docs/domain-packs/index.md",
    "docs/domain-packs/fintech.md",
    "docs/domain-packs/health.md",
    "docs/domain-packs/saas.md",
    "docs/domain-packs/marketplace.md",
    "docs/domain-packs/social.md",
    "docs/domain-packs/education.md",
    "docs/evals.md",
    "docs/golden-examples.md",
    "docs/guardrails.md",
    "docs/github-publishing.md",
    "docs/heuristics.md",
    "docs/inspiration-sources.md",
    "docs/judged-mode.md",
    "docs/llm-judge-runner.md",
    "docs/patterns-catalog.md",
    "docs/principles.md",
    "docs/motion-system.md",
    "docs/quality-bars.md",
    "docs/rendered-output-qa.md",
    "docs/self-review.md",
    "docs/sources.md",
    "docs/synthetic-case-studies.md",
    "docs/versioning.md",
    "docs/visual-benchmark-playbooks.md",
    "docs/visual-review-fixtures.md",
    "docs/weaknesses.md",
    "docs/workflow.md",
    "examples/design-flow.md",
    "examples/clarification-policy.md",
    "examples/generate-screen.md",
    "examples/rationale-handoff.md",
    "examples/review-screen.md",
    "examples/rubric-before-after.md",
    "examples/typography-spacing.md",
    "examples/ui-spec.md",
    "examples/anti-patterns.md",
    "examples/benchmark-report.md",
    "examples/case-studies/fintech-account-overview.md",
    "examples/case-studies/health-medication-refill.md",
    "examples/case-studies/saas-approval-queue.md",
    "examples/case-studies/marketplace-checkout-substitution.md",
    "examples/case-studies/social-privacy-settings.md",
    "examples/case-studies/education-lesson-progress.md",
    "examples/case-studies/onboarding-permissions.md",
    "examples/case-studies/settings-consent-destructive-action.md",
    "examples/case-studies/search-results-filtering.md",
    "examples/case-studies/empty-error-state-recovery.md",
    "examples/case-studies/typography-spacing-system.md",
    "examples/case-studies/rationale-handoff.md",
    "examples/golden/premium-ui.md",
    "examples/golden/enterprise-saas.md",
    "examples/golden/fintech.md",
    "examples/golden/health.md",
    "examples/golden/onboarding.md",
    "examples/golden/settings.md",
    "examples/golden/checkout.md",
    "examples/evals/rubric-score-1.json",
    "examples/evals/rubric-score-2.json",
    "examples/evals/rubric-score-3.json",
    "examples/evals/rubric-score-4.json",
    "examples/evals/rubric-score-5.json",
    "examples/rendered-output-qa/report-schema.json",
    "examples/rendered-output-qa/sample-report.json",
    "examples/visual-review-fixtures/fintech-dashboard-dense-summary.md",
    "examples/visual-review-fixtures/health-appointment-booking.md",
    "examples/visual-review-fixtures/enterprise-saas-mobile-table-card-list.md",
    "examples/visual-review-fixtures/marketplace-product-detail-checkout-edge.md",
    "examples/visual-review-fixtures/social-profile-privacy-control.md",
    "examples/visual-review-fixtures/education-quiz-results.md",
    "scripts/bump_version.py",
    "scripts/install.sh",
    "scripts/rubric_judge_oracle_agent.py",
    "scripts/run_rubric_judge.py",
    "scripts/run_generation_eval.py",
    "scripts/run_diversity_eval.py",
    "scripts/generation_oracle_agent.py",
    "examples/evals/generation-prompts.json",
    "examples/evals/diversity-fixtures.json",
    "scripts/validate_release.py",
    "assets/logo-light.svg",
    "assets/logo-dark.svg",
]

MARKDOWN_GLOBS = [
    "README.md",
    "SKILL.md",
    ".claude/skills/*/SKILL.md",
    ".claude/agents/*.md",
    "docs/*.md",
    "docs/**/*.md",
    "CHANGELOG.md",
    "skill/*.md",
    "examples/*.md",
    "examples/**/*.md",
]

DUPLICATE_HEADING_ALLOWED_FILES = {
    "CHANGELOG.md",
    "docs/evals.md",
    "docs/visual-benchmark-playbooks.md",
    "skill/modes.md",
    "examples/anti-patterns.md",
    "examples/clarification-policy.md",
}

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(
    r"^---\n(?P<body>.*?)\n---\n",
    re.DOTALL,
)
EXAMPLE_OUTPUT_RE = re.compile(
    r"## Example output\s*\n\s*```md\n(?P<body>.*?)\n```",
    re.DOTALL,
)

EXAMPLE_RESPONSE_FILES = [
    "examples/generate-screen.md",
    "examples/design-flow.md",
    "examples/ui-spec.md",
    "examples/review-screen.md",
    "examples/typography-spacing.md",
    "examples/rationale-handoff.md",
]

RUBRIC_EVAL_FIXTURES = [
    "examples/evals/rubric-score-1.json",
    "examples/evals/rubric-score-2.json",
    "examples/evals/rubric-score-3.json",
    "examples/evals/rubric-score-4.json",
    "examples/evals/rubric-score-5.json",
    "examples/evals/rubric-score-2-adversarial.json",
    "examples/evals/rubric-score-3-visual-rules-state-gap.json",
    "examples/evals/rubric-score-3-contradicted-value.json",
]

RUBRIC_DIMENSIONS = {
    "attention_path_and_hierarchy",
    "composition_and_spacing",
    "typography_craft",
    "color_state_and_contrast",
    "density_and_rhythm",
    "interaction_polish_and_motion",
    "context_and_brand_fit",
    "production_readiness",
    "distinctiveness_and_owned_assets",
}

RUBRIC_FIXTURE_REQUIRED_FIELDS = {
    "id",
    "rubric_version",
    "mode",
    "prompt",
    "response_excerpt",
    "expected_score",
    "expected_verdict",
    "expected_cap",
    "hard_limits",
    "dimension_scores",
    "expected_failed_dimensions",
    "expected_rationale",
    "improvement_suggestions",
}

# `Signature move:` must be followed by at least 8 words, so the slot cannot be
# satisfied by the label alone or by a single adjective.
SIGNATURE_MOVE_SHAPE = r"Signature move:\s*(?:\S+\s+){7,}\S+"
# `Quality target:` must name what blocks the next level, not just print a number.
# The alternation is score-conditional on purpose: requiring `blocked from ... until`
# unconditionally made 5/5 unreachable in Modes A and C by test suite, since a top-band
# read has no blocker to name and inventing one to fill the slot is the defect this
# shape exists to prevent. Below the top band the blocker is still mandatory.
QUALITY_TARGET_SHAPE = (
    r"Quality target:\s*\**"
    r"(?:5/5[^\n]*\bnothing blocks 5/5\b"
    r"|[1-4]/5[^\n]*\bblocked from\b[^\n]*\buntil\b)"
)
# The score must be traceable to named dimensions, or "derived" is unfalsifiable.
DIMENSION_READ_SHAPE = r"Dimension read:[^\n]*[1-5][^\n]*[1-5]"
# Labelling only the rejects leaves the third candidate slot unverifiable.
COMMITTED_DIRECTION_SHAPE = r"Direction:[^\n]*\(from:[^)\n]+\)"

MODE_REQUIREMENTS = {
    "Generate mobile screen concept": {
        "sections": [
            "Screen goal",
            "Primary user task",
            "Information hierarchy",
            "Recommended layout structure",
            "Suggested components",
            "Interaction notes",
            "Empty / loading / error states",
            "Platform-specific notes",
            "Accessibility considerations",
            "Design quality calibration",
            "Rationale for major choices",
            "Alternatives considered",
            "Next actions",
        ],
        "accessibility_sections": ["Accessibility considerations"],
        "bullet_shapes": [
            (
                "Alternatives considered",
                {
                    # A direction-level alternative names token consequences, which are
                    # inherently numeric or named. Shape, not phrasing.
                    "pattern": r"\d|`[^`]+`",
                    "min_bullets": 2,
                    "tail_after": r"because",
                    "tail_label": "because",
                    "min_tail_words": 6,
                },
            ),
        ],
        "label_word_counts": [
            ("Design quality calibration", "Attention path:", 12),
            ("Design quality calibration", "Signature move:", 12),
        ],
        "must_contain": [
            ("Design quality calibration", r"Attention path:"),
            ("Design quality calibration", r"Composition and spacing:"),
            ("Design quality calibration", r"Production checks:"),
            ("Design quality calibration", r"\b[1-5]/5\b"),
            # `Signature move:` must carry a real statement, not a label. Shape, not vocabulary.
            ("Design quality calibration", SIGNATURE_MOVE_SHAPE),
            # The quality target names the blocking dimension instead of printing a bare number.
            ("Design quality calibration", QUALITY_TARGET_SHAPE),
            ("Design quality calibration", DIMENSION_READ_SHAPE),
            ("Design quality calibration", COMMITTED_DIRECTION_SHAPE),
        ],
    },
    "Design mobile user flow": {
        "sections": [
            "Flow goal",
            "Entry points",
            "Ordered steps / screens",
            "Decision points",
            "Back-navigation logic",
            "Failure and recovery paths",
            "Platform behavior notes",
            "Accessibility and usability risks",
            "Simplification opportunities",
            "Next actions",
        ],
        "accessibility_sections": ["Accessibility and usability risks"],
    },
    "Create platform-aware UI spec": {
        "sections": [
            "Screen or flow scope",
            "Structural zones",
            "Components by section",
            "State definitions",
            "Behavior rules",
            "Content guidance",
            "Spacing and layout notes",
            "Typography rules",
            "Accessibility requirements",
            "Design quality requirements",
            "Platform-specific implementation notes",
            "Key decision tradeoffs",
            "Next actions",
        ],
        "accessibility_sections": ["Accessibility requirements"],
        "label_word_counts": [
            ("Design quality requirements", "Attention path:", 12),
            ("Design quality requirements", "Signature move:", 12),
        ],
        "must_contain": [
            ("Spacing and layout notes", r"\b\d+\s?(dp|pt|sp|px)\b|space-\d+"),
            ("Typography rules", r"\b\d+\s?(sp|pt|px)\b|body|title|label|caption"),
            ("Design quality requirements", r"Attention path:"),
            ("Design quality requirements", r"Production checks:"),
            ("Design quality requirements", r"\b[1-5]/5\b"),
            ("Design quality requirements", SIGNATURE_MOVE_SHAPE),
            ("Design quality requirements", QUALITY_TARGET_SHAPE),
            ("Design quality requirements", DIMENSION_READ_SHAPE),
            ("Design quality requirements", COMMITTED_DIRECTION_SHAPE),
        ],
    },
    "Review screen for usability/accessibility": {
        "sections": [
            "Quick summary",
            "Strengths",
            "Findings",
            "Design quality score (current → projected)",
            "Severity index",
            "Platform-convention mismatches",
            "Unresolved assumptions",
            "Next actions",
        ],
        "accessibility_sections": ["Findings"],
        "requires_sub_case": True,
        "must_contain": [
            ("Design quality score (current → projected)", r"Current:\s*\b[1-5]/5\b"),
            (
                "Design quality score (current → projected)",
                r"Projected:\s*\b[1-5]/5\b",
            ),
        ],
        "must_not_contain": [
            # The projected score must be a flat median, never an inflated "up to N/5".
            ("Design quality score (current → projected)", r"Projected:\s*up to"),
        ],
    },
    "Create typography and spacing system": {
        "sections": [
            "Type roles",
            "Size hierarchy",
            "Weight usage",
            "Line-height guidance",
            "Spacing scale",
            "Density rules",
            "Visual rhythm rules",
            "Touch-target implications",
            "Accessibility considerations",
            "Usage examples",
            "Next actions",
        ],
        "accessibility_sections": ["Accessibility considerations"],
        "must_contain": [
            ("Size hierarchy", r"\b\d+\s?(sp|pt|px)\b"),
            ("Line-height guidance", r"\b1\.[0-9]\b|\b\d+\s?(sp|pt|px)\b"),
            ("Touch-target implications", r"44\s?pt.*48\s?dp|48\s?dp.*44\s?pt"),
            ("Visual rhythm rules", r"\b(4|8|12|16|24|32|40)\b"),
            ("Visual rhythm rules", r"\b[1-5]/5\b"),
        ],
    },
    "Prepare design rationale / handoff": {
        "bullet_shapes": [
            (
                "Pattern choices and why",
                {
                    "pattern": r"^.+\s+over\s+.+\s+because\s+.+$",
                    "min_bullets": 3,
                    "tail_after": r"\bbecause\b",
                    "tail_label": "because",
                    "min_tail_words": 8,
                },
            ),
            (
                "Key design decisions",
                {
                    "pattern": r"alternative considered:",
                    "min_bullets": 2,
                    "tail_after": r"alternative considered:",
                    "tail_label": "alternative considered:",
                    "min_tail_words": 10,
                },
            ),
        ],
        "sections": [
            "Design objective",
            "Target users and context",
            "Key design decisions",
            "Pattern choices and why",
            "Design quality rationale",
            "Platform alignment",
            "Accessibility and usability considerations",
            "States and edge cases",
            "Implementation notes",
            "Open questions",
            "Validation plan / recommended testing focus",
            "Next actions",
        ],
        "accessibility_sections": ["Accessibility and usability considerations"],
        "must_contain": [
            ("Key design decisions", r"alternative considered:"),
            ("Design quality rationale", r"mechanism:"),
            ("Design quality rationale", r"\b[1-5]/5\b"),
            ("Design quality rationale", SIGNATURE_MOVE_SHAPE),
            ("Design quality rationale", QUALITY_TARGET_SHAPE),
            ("Design quality rationale", DIMENSION_READ_SHAPE),
            ("Design quality rationale", COMMITTED_DIRECTION_SHAPE),
        ],
    },
}

BANNED_RESPONSE_PATTERNS = [
    r"\bWCAG-compliant\b",
    r"\bpasses accessibility\b",
    r"\bfully accessible\b",
    r"\baccessibility compliant\b",
]
WEAKNESS_REFERENCE_FILES = [
    "SKILL.md",
    ".claude/skills/mobile-design-skill/SKILL.md",
    "README.md",
    "skill/metadata.yaml",
    "skill/modes.md",
    "skill/templates.md",
    "skill/usage.md",
    "docs/evals.md",
    "docs/guardrails.md",
    "docs/self-review.md",
    "docs/sources.md",
    "docs/workflow.md",
]

WEAKNESS_REQUIRED_PATTERNS = [
    "generic artifact",
    "template completion",
    "first-idea bias",
    "aesthetic laundering",
    "evidence overreach",
    "platform flattening",
    "happy-path-only design",
    "weak handoff",
]

DESIGN_QUALITY_RUBRIC_REFERENCE_FILES = [
    "SKILL.md",
    ".claude/skills/mobile-design-skill/SKILL.md",
    "README.md",
    "skill/metadata.yaml",
    "skill/modes.md",
    "skill/templates.md",
    "skill/usage.md",
    "docs/design-quality.md",
    "docs/evals.md",
    "docs/guardrails.md",
    "docs/self-review.md",
    "docs/sources.md",
    "docs/workflow.md",
]

DESIGN_QUALITY_RUBRIC_REQUIRED_PATTERNS = [
    "1/5",
    "2/5",
    "3/5",
    "4/5",
    "5/5",
    "Attention path",
    "Production readiness",
    "Distinctiveness and owned assets",
    "Improvement ladder",
    # The inert cap and its ladder rung must keep naming the same exit condition.
    "3 → 4 (inert cap)",
    "n/v",
]

RUBRIC_EVAL_REFERENCE_FILES = [
    "README.md",
    "docs/design-quality-rubric.md",
    "docs/evals.md",
    "docs/llm-judge-runner.md",
    "skill/metadata.yaml",
]

GOLDEN_EXAMPLE_FILES = [
    "examples/golden/premium-ui.md",
    "examples/golden/enterprise-saas.md",
    "examples/golden/fintech.md",
    "examples/golden/health.md",
    "examples/golden/onboarding.md",
    "examples/golden/settings.md",
    "examples/golden/checkout.md",
    "examples/golden/tablet-list-detail.md",
]

LLM_JUDGE_RUNNER_REFERENCE_FILES = [
    "README.md",
    ".github/workflows/validate.yml",
    "docs/evals.md",
    "docs/llm-judge-runner.md",
    "skill/metadata.yaml",
]

CLARIFICATION_POLICY_REFERENCE_FILES = [
    "SKILL.md",
    ".claude/skills/mobile-design-skill/SKILL.md",
    "README.md",
    "skill/metadata.yaml",
    "skill/modes.md",
    "skill/templates.md",
    "skill/usage.md",
    "docs/evals.md",
    "docs/guardrails.md",
    "docs/self-review.md",
    "docs/sources.md",
    "docs/workflow.md",
]

JUDGED_MODE_REFERENCE_FILES = [
    "SKILL.md",
    ".claude/skills/mobile-design-skill/SKILL.md",
    ".claude/agents/mobile-design-judge.md",
    "README.md",
    "skill/metadata.yaml",
    "skill/usage.md",
    "docs/commands.md",
    "docs/evals.md",
]

JUDGED_MODE_REQUIRED_PATTERNS = [
    "--judge",
    "Judge summary",
    "independent judge",
    "mobile-design-judge",
    "Single-agent fallback",
]

VISUAL_BENCHMARK_REFERENCE_FILES = [
    "SKILL.md",
    "README.md",
    "skill/metadata.yaml",
    "skill/usage.md",
    "docs/inspiration-sources.md",
]

VISUAL_BENCHMARK_REQUIRED_PATTERNS = [
    "Mobbin",
    "Page Flows",
    "Apple Design Awards",
    "Awwwards",
    "Do not use benchmarks as evidence",
    "Translate references into implementable mechanisms",
]

GOLDEN_EXAMPLE_REFERENCE_FILES = [
    "SKILL.md",
    ".claude/skills/mobile-design-skill/SKILL.md",
    "README.md",
    "skill/metadata.yaml",
    "skill/usage.md",
    "docs/design-quality-rubric.md",
    "docs/evals.md",
]

GOLDEN_EXAMPLE_AREAS = {
    "Premium UI": "examples/golden/premium-ui.md",
    "Enterprise SaaS": "examples/golden/enterprise-saas.md",
    "Fintech": "examples/golden/fintech.md",
    "Health": "examples/golden/health.md",
    "Onboarding": "examples/golden/onboarding.md",
    "Settings": "examples/golden/settings.md",
    "Checkout": "examples/golden/checkout.md",
    "Tablet list-detail": "examples/golden/tablet-list-detail.md",
}

RELEASE_AUTOMATION_REFERENCE_FILES = [
    "README.md",
    "docs/release-automation.md",
    "docs/versioning.md",
    "skill/metadata.yaml",
]

RELEASE_AUTOMATION_REQUIRED_PATTERNS = [
    "validate_repo.py",
    "run_rubric_judge.py",
    "rubric_judge_oracle_agent.py",
    "version/tag sanity",
    "validate_release.py",
]

SYNTHETIC_CASE_STUDY_FILES = [
    "examples/case-studies/fintech-account-overview.md",
    "examples/case-studies/health-medication-refill.md",
    "examples/case-studies/saas-approval-queue.md",
    "examples/case-studies/marketplace-checkout-substitution.md",
    "examples/case-studies/social-privacy-settings.md",
    "examples/case-studies/education-lesson-progress.md",
    "examples/case-studies/onboarding-permissions.md",
    "examples/case-studies/settings-consent-destructive-action.md",
    "examples/case-studies/search-results-filtering.md",
    "examples/case-studies/empty-error-state-recovery.md",
    "examples/case-studies/typography-spacing-system.md",
    "examples/case-studies/rationale-handoff.md",
]

SYNTHETIC_CASE_STUDY_SECTIONS = [
    "## Prompt",
    "## Weak response",
    "## Why this is weak",
    "## Strong response",
    "## Why this is stronger",
    "## Regression checks",
]

DOMAIN_PACK_FILES = [
    "docs/domain-packs/fintech.md",
    "docs/domain-packs/health.md",
    "docs/domain-packs/saas.md",
    "docs/domain-packs/marketplace.md",
    "docs/domain-packs/social.md",
    "docs/domain-packs/education.md",
]

DOMAIN_PACK_SECTIONS = [
    "## When To Use",
    "## Primary User Jobs",
    "## Trust And Safety Risks",
    "## Common Mobile Surfaces",
    "## Hierarchy Guidance",
    "## State And Recovery Requirements",
    "## Accessibility Notes",
    "## Platform Notes",
    "## Evidence And Compliance Boundaries",
    "## Design-Quality Traps",
    "## Handoff Checks",
]

VISUAL_REVIEW_FIXTURE_FILES = [
    "examples/visual-review-fixtures/fintech-dashboard-dense-summary.md",
    "examples/visual-review-fixtures/health-appointment-booking.md",
    "examples/visual-review-fixtures/enterprise-saas-mobile-table-card-list.md",
    "examples/visual-review-fixtures/marketplace-product-detail-checkout-edge.md",
    "examples/visual-review-fixtures/social-profile-privacy-control.md",
    "examples/visual-review-fixtures/education-quiz-results.md",
    "examples/visual-review-fixtures/ipad-team-inbox-stretched-phone.md",
]

VISUAL_REVIEW_FIXTURE_SECTIONS = [
    "## Review setup",
    "## Screen description",
    "## Frame specs",
    "## Visible hierarchy",
    "## Components",
    "## Typography",
    "## Color and state notes",
    "## Interaction states",
    "## Known constraints",
    "## Expected critique",
    "## Prohibited critique",
    "## Severity expectations",
    "## Rubric score expectation",
]

BENCHMARK_REPORT_REQUIRED_PATTERNS = [
    "3-5 references",
    "Reference Input Schema",
    "Final Report Template",
    "Borrow",
    "Do not copy",
    "Translate to tokens/components/states",
    "Evidence boundaries",
    "Red Flags",
]

RENDERED_OUTPUT_QA_REQUIRED_PATTERNS = [
    "optional workflow",
    "mobile viewport",
    "overlap",
    "clipping",
    "text overflow",
    "tap target",
    "contrast risk",
    "reduced-motion",
    "rendered-output-qa/v1",
]

CLARIFICATION_POLICY_REQUIRED_PATTERNS = [
    "Ask only when",
    "at most **three**",
    "Clarifying questions",
    "Why this blocks",
    "Fast path",
    "Proceed-with-assumptions",
]


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def validate_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    if missing:
        fail(f"Missing required files: {', '.join(missing)}")


def validate_skill_frontmatter() -> None:
    skill_path = ROOT / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(content)
    if not match:
        fail("SKILL.md must begin with YAML frontmatter")

    frontmatter = match.group("body")
    if "name:" not in frontmatter or "description:" not in frontmatter:
        fail("SKILL.md frontmatter must contain both name and description")


def validate_weakness_layer() -> None:
    weakness_doc = (ROOT / "docs/weaknesses.md").read_text(encoding="utf-8").lower()
    missing_patterns = [
        pattern for pattern in WEAKNESS_REQUIRED_PATTERNS if pattern not in weakness_doc
    ]
    if missing_patterns:
        fail(
            "docs/weaknesses.md is missing required weakness patterns: "
            + ", ".join(missing_patterns)
        )

    missing_references = []
    for relative_path in WEAKNESS_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "weaknesses.md" not in text and "weakness_prevention" not in text:
            missing_references.append(relative_path)

    if missing_references:
        fail(
            "Weakness layer is not referenced by required files: "
            + ", ".join(missing_references)
        )


def validate_design_quality_rubric_layer() -> None:
    rubric_doc = (ROOT / "docs/design-quality-rubric.md").read_text(encoding="utf-8")
    missing_patterns = [
        pattern
        for pattern in DESIGN_QUALITY_RUBRIC_REQUIRED_PATTERNS
        if pattern not in rubric_doc
    ]
    if missing_patterns:
        fail(
            "docs/design-quality-rubric.md is missing required rubric patterns: "
            + ", ".join(missing_patterns)
        )

    missing_references = []
    for relative_path in DESIGN_QUALITY_RUBRIC_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if (
            "design-quality-rubric.md" not in text
            and "design_quality_rubric" not in text
        ):
            missing_references.append(relative_path)

    if missing_references:
        fail(
            "Design-quality rubric layer is not referenced by required files: "
            + ", ".join(missing_references)
        )

    errors = dimension_table_shape_errors(rubric_doc)
    errors.extend(band_five_closure_errors(rubric_doc))
    if errors:
        fail("Dimension table shape validation failed:\n" + "\n".join(errors))


# Every surface that assigns a band, not just the one that defines them. The drafting side
# and the judge both award band 5, and a gate present in one and absent in the other is the
# file-scoped guard this repository keeps rebuilding.
BAND_SCORING_SURFACES = (
    "docs/design-quality-rubric.md",
    "docs/self-review.md",
    "docs/judged-mode.md",
    ".claude/agents/mobile-design-judge.md",
)
CLOSURE_TEST_MARKERS = ("closure test", "the band is 4")
# The four shapes measured to fail the test. Kept as diagnoses; a list of shapes that PASS
# would be a template to satisfy, which is the rule-1 failure this repository has shipped
# twice. If the list is ever inverted, that is the thing to catch.
CLOSURE_FAILURE_SHAPES = (
    "no anchor",
    "no behaviour",
    "no output",
    "no threshold",
)


def band_five_closure_errors(rubric_doc: str) -> list[str]:
    """Band 5 is awarded on a test that gets run, not on how the statement reads.

    Measured: 63 statements from live output, three blind readers each, situations written
    from band-stripped copies so probe difficulty could not track the arm. Band-5 statements
    settled their unlisted case 11/28; band-4 statements 9/25; Fisher one-sided p = 0.52, and
    the sign inverts once dimension is adjusted for. The boundary did not separate them, so
    it cannot be operated by inspection.
    """
    errors: list[str] = []
    if "### The band-5 closure test" not in rubric_doc:
        errors.append(
            "docs/design-quality-rubric.md: missing `### The band-5 closure test` — awarding "
            "band 5 on how a statement reads was measured not to separate it from band 4"
        )
    missing_shapes = [shape for shape in CLOSURE_FAILURE_SHAPES if shape not in rubric_doc]
    if missing_shapes:
        errors.append(
            "docs/design-quality-rubric.md: the closure test lost failure shape(s) "
            + ", ".join(f"`{shape}`" for shape in missing_shapes)
            + " — these are the four that account for the measured failures"
        )

    for relative_path in BAND_SCORING_SURFACES:
        text = (ROOT / relative_path).read_text(encoding="utf-8").lower()
        if not any(marker in text for marker in CLOSURE_TEST_MARKERS):
            errors.append(
                f"{relative_path}: assigns design-quality bands but does not carry the "
                "band-5 closure test; a gate on one scoring surface and not the other is "
                "how a guard gets scoped to a file instead of to the class"
            )

    return errors


BOUNDARY_HEADER = "| Dimension | 1 → 2 | 2 → 3 | 3 → 4 | 4 → 5 |"
RUBRIC_DIMENSION_ROW_LABELS = (
    "Attention path and hierarchy",
    "Composition and spacing",
    "Typography craft",
    "Color, state, and contrast",
    "Density and rhythm",
    "Interaction polish and motion",
    "Context and brand fit",
    "Production readiness",
    "Distinctiveness and owned assets",
)


def dimension_table_shape_errors(rubric_doc: str) -> list[str]:
    """Four boundaries define five bands; three descriptions defined three.

    The table this replaced had columns `1-2 signals | 3 signals | 4-5 signals`, so 2 and 5
    had no anchor of their own and a model could pick a column but not a number. Boundaries
    are also what keeps rule 1 satisfiable: a cell phrased as a question cannot be pasted
    into an output as an answer, and every cell in the old table could be.
    """
    errors: list[str] = []
    if BOUNDARY_HEADER not in rubric_doc:
        return [
            f"docs/design-quality-rubric.md: missing the boundary header `{BOUNDARY_HEADER}`; "
            "five bands need four boundaries, and a table of descriptions cannot supply them"
        ]

    rows = {}
    for line in rubric_doc.splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[0] in RUBRIC_DIMENSION_ROW_LABELS:
            rows[cells[0]] = cells[1:]

    for label, cells in rows.items():
        top = cells[3]
        # The `4 -> 5` cell has to ask what the rule RETURNS. One cell used to ask what shape
        # the statement took -- "is that appearance behaviour expressed as one transform" --
        # and the closure test structurally could not be run on it: three blind readers
        # unanimously judged a correct transform underdetermined because the cell never asked
        # for an output. A question mark alone does not catch this; form-grading vocabulary does.
        form_graded = re.search(r"\b(expressed|phrased|written|framed|stated)\s+as\b", top, re.IGNORECASE)
        if form_graded:
            errors.append(
                f"docs/design-quality-rubric.md: `{label}` 4 → 5 grades the form of a statement "
                f"(`{form_graded.group(0)}`) instead of what it returns; the closure test cannot "
                "be run on a cell that never asks for an output"
            )
        if not re.search(r"\b(return|returns|decide|decides|produce|produces|assign|assigns|settle|settles|say|says|joins?)\b", top, re.IGNORECASE):
            errors.append(
                f"docs/design-quality-rubric.md: `{label}` 4 → 5 names no returning verb, so "
                "there is nothing for the closure test to write down as the answer"
            )

    for label in RUBRIC_DIMENSION_ROW_LABELS:
        if label not in rows:
            errors.append(f"docs/design-quality-rubric.md: dimension `{label}` has no boundary row")
            continue
        for index, cell in enumerate(rows[label]):
            boundary = f"{index + 1} → {index + 2}"
            if not cell.endswith("?"):
                errors.append(
                    f"docs/design-quality-rubric.md: `{label}` {boundary} is not a question — "
                    "a cell stating the answer gets copied into an output as one"
                )
            if re.search(r"\b[1-5]\s*/\s*5\b", cell):
                errors.append(
                    f"docs/design-quality-rubric.md: `{label}` {boundary} names a score; a "
                    "boundary asks about the artifact, it does not print a level"
                )

    return errors


def validate_rubric_eval_pack() -> None:
    seen_scores: set[int] = set()
    spreads: dict[str, int] = {}
    vectors: dict[str, dict[str, int]] = {}
    errors: list[str] = []

    for relative_path in RUBRIC_EVAL_FIXTURES:
        fixture_path = ROOT / relative_path
        try:
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{relative_path}: invalid JSON ({exc})")
            continue

        missing_fields = RUBRIC_FIXTURE_REQUIRED_FIELDS - fixture.keys()
        if missing_fields:
            errors.append(
                f"{relative_path}: missing fields {', '.join(sorted(missing_fields))}"
            )
            continue

        score = fixture["expected_score"]
        if not isinstance(score, int) or score < 1 or score > 5:
            errors.append(f"{relative_path}: expected_score must be an integer 1..5")
        else:
            seen_scores.add(score)
            expected_filename_marker = f"score-{score}"
            if expected_filename_marker not in fixture_path.name:
                errors.append(
                    f"{relative_path}: filename must contain `{expected_filename_marker}`"
                )

        dimensions = fixture["dimension_scores"]
        if not isinstance(dimensions, dict):
            errors.append(f"{relative_path}: dimension_scores must be an object")
        else:
            missing_dimensions = RUBRIC_DIMENSIONS - dimensions.keys()
            extra_dimensions = dimensions.keys() - RUBRIC_DIMENSIONS
            if missing_dimensions:
                errors.append(
                    f"{relative_path}: missing dimension scores {', '.join(sorted(missing_dimensions))}"
                )
            if extra_dimensions:
                errors.append(
                    f"{relative_path}: unknown dimension scores {', '.join(sorted(extra_dimensions))}"
                )
            for dimension, value in dimensions.items():
                if not isinstance(value, int) or value < 1 or value > 5:
                    errors.append(
                        f"{relative_path}: dimension `{dimension}` must be an integer 1..5"
                    )

            values = [v for v in dimensions.values() if isinstance(v, int)]
            if values and isinstance(score, int):
                median = statistics.median(sorted(values))
                floor_median = int(median)
                spreads[relative_path] = max(values) - min(values)
                vectors[relative_path] = {
                    name: band for name, band in dimensions.items() if isinstance(band, int)
                }
                capped = not str(fixture["expected_cap"]).strip().lower().startswith("no ")
                if score > floor_median:
                    errors.append(
                        f"{relative_path}: expected_score {score} is above the median of "
                        f"the dimension scores ({floor_median}); the final score is the "
                        "median lowered by caps, never raised above it"
                    )
                elif score < floor_median and not capped:
                    errors.append(
                        f"{relative_path}: expected_score {score} is below the median "
                        f"({floor_median}) with no cap recorded in expected_cap"
                    )

        if not isinstance(fixture["hard_limits"], list):
            errors.append(f"{relative_path}: hard_limits must be a list")
        if not isinstance(fixture["expected_failed_dimensions"], list):
            errors.append(f"{relative_path}: expected_failed_dimensions must be a list")
        if not isinstance(fixture["improvement_suggestions"], list) or len(fixture["improvement_suggestions"]) < 2:
            errors.append(
                f"{relative_path}: improvement_suggestions must contain at least 2 items"
            )
        if not re.search(r"\S", fixture["expected_rationale"]):
            errors.append(f"{relative_path}: expected_rationale must not be empty")

    expected_scores = {1, 2, 3, 4, 5}
    if not expected_scores.issubset(seen_scores):
        errors.append(
            "Rubric eval fixtures must cover scores 1..5; missing "
            + ", ".join(str(score) for score in sorted(expected_scores - seen_scores))
        )

    # Before this check the fixtures had dimension spreads of 0,1,1,0,0 -- a judge
    # that ignored the median rule and the caps passed the entire pack.
    wide = [f for f, spread in spreads.items() if spread >= 2]
    if len(wide) < 2:
        errors.append(
            "At least 2 rubric fixtures must have a dimension spread of 2 or more, so "
            f"the median rule is actually exercised; found {len(wide)}"
        )

    # Four of the six vectors were constant (all 1s, all 4s, all 5s, near-all 2s). When a
    # vector is constant, `median(vector) == expected_score` holds trivially, so a judge
    # that computes the median and a judge that reads `expected_score` and back-fills the
    # vector are indistinguishable -- a pack that replays a known-good answer.
    flat = sorted(path for path, spread in spreads.items() if spread == 0)
    if flat:
        errors.append(
            "flat dimension vector in " + ", ".join(flat) + " -- every dimension identical, "
            "so the pack cannot separate a judge that derives the median from one that "
            "back-fills it from the expected score"
        )

    if vectors and not any(
        min(vector.values()) <= 2 and max(vector.values()) >= 5 for vector in vectors.values()
    ):
        errors.append(
            "examples/evals/: no fixture vector spans a band <=2 and a band >=5, so the pack "
            "never shows the judge a design excellent on one axis and broken on another -- the "
            "case `Do not average away a serious flaw` describes, and the one that separates a "
            "judge applying the critical-dimension step from one that stops at the median"
        )

    for dimension in sorted(RUBRIC_DIMENSIONS):
        seen = {vector[dimension] for vector in vectors.values() if dimension in vector}
        if vectors and len(seen) < MIN_DISTINCT_BANDS_IN_FIXTURE_PACK:
            errors.append(
                f"examples/evals/: dimension `{dimension}` takes only {sorted(seen)} across the "
                f"fixture pack; fewer than {MIN_DISTINCT_BANDS_IN_FIXTURE_PACK} distinct bands "
                "means the judge is never shown what the other levels look like for it"
            )

    before_after = (ROOT / "examples/rubric-before-after.md").read_text(encoding="utf-8")
    for pattern in [
        "## Weak response",
        "## Improved response",
        "2/5",
        "4/5",
        "What would make it 5/5",
    ]:
        if pattern not in before_after:
            errors.append(f"examples/rubric-before-after.md: missing `{pattern}`")

    for relative_path in RUBRIC_EVAL_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "examples/evals" not in text and "rubric-before-after.md" not in text:
            errors.append(f"{relative_path}: missing rubric eval pack reference")

    if errors:
        fail("Rubric eval pack validation failed:\n" + "\n".join(errors))


def validate_llm_judge_runner_contract() -> None:
    runner = (ROOT / "scripts/run_rubric_judge.py").read_text(encoding="utf-8")
    errors: list[str] = []
    for pattern in [
        "--dry-run",
        "--export-jsonl",
        "--export-expected-output",
        "--judge-output",
        "--judge-command",
        "--judge-command-output",
        "rubric-judge-request/v1",
        "dimension_scores",
        "improvement_suggestions",
    ]:
        if pattern not in runner:
            errors.append(f"scripts/run_rubric_judge.py: missing `{pattern}`")

    docs = (ROOT / "docs/llm-judge-runner.md").read_text(encoding="utf-8")
    for pattern in [
        "python3 scripts/run_rubric_judge.py --dry-run",
        "--judge-command",
        "LLM-agnostic contract",
        "schema_version",
        "stdin",
        "stdout",
        "rubric_judge_oracle_agent.py",
        "Judge output contract",
        "Pass criteria",
    ]:
        if pattern not in docs:
            errors.append(f"docs/llm-judge-runner.md: missing `{pattern}`")

    for relative_path in LLM_JUDGE_RUNNER_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "run_rubric_judge.py" not in text and "llm_judge_runner" not in text:
            errors.append(f"{relative_path}: missing LLM judge runner reference")

    if errors:
        fail("LLM judge runner contract validation failed:\n" + "\n".join(errors))


def validate_clarification_policy_layer() -> None:
    policy = (ROOT / "docs/clarification-policy.md").read_text(encoding="utf-8")
    errors: list[str] = []
    for pattern in CLARIFICATION_POLICY_REQUIRED_PATTERNS:
        if pattern not in policy:
            errors.append(f"docs/clarification-policy.md: missing `{pattern}`")

    example = (ROOT / "examples/clarification-policy.md").read_text(encoding="utf-8")
    for pattern in [
        "## Example 1: Blocking visual review",
        "## Example 2: Non-blocking concept request",
        "## Example 3: Policy-sensitive spec",
        "## Clarifying questions",
        "## Fast path",
    ]:
        if pattern not in example:
            errors.append(f"examples/clarification-policy.md: missing `{pattern}`")

    for relative_path in CLARIFICATION_POLICY_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "clarification-policy.md" not in text and "clarification_policy" not in text:
            errors.append(f"{relative_path}: missing clarification policy reference")

    if errors:
        fail("Clarification policy validation failed:\n" + "\n".join(errors))


def validate_judged_mode_layer() -> None:
    policy = (ROOT / "docs/judged-mode.md").read_text(encoding="utf-8")
    errors: list[str] = []
    for pattern in JUDGED_MODE_REQUIRED_PATTERNS:
        if pattern not in policy:
            errors.append(f"docs/judged-mode.md: missing `{pattern}`")

    for relative_path in JUDGED_MODE_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "judged-mode.md" not in text and "--judge" not in text:
            errors.append(f"{relative_path}: missing judged mode reference")

    if errors:
        fail("Judged mode validation failed:\n" + "\n".join(errors))


def validate_visual_benchmark_playbooks() -> None:
    doc = (ROOT / "docs/visual-benchmark-playbooks.md").read_text(encoding="utf-8")
    errors: list[str] = []

    for pattern in VISUAL_BENCHMARK_REQUIRED_PATTERNS:
        if pattern not in doc:
            errors.append(f"docs/visual-benchmark-playbooks.md: missing `{pattern}`")

    for source in ["Mobbin", "Page Flows", "Apple Design Awards", "Awwwards"]:
        section = extract_section(doc, source)
        if not section:
            errors.append(f"docs/visual-benchmark-playbooks.md: missing `## {source}` section")
            continue
        for pattern in [
            "### When to use",
            "### What to extract as inspiration",
            "### What NOT to treat as evidence",
            "### Checklist",
            "### Red flags",
        ]:
            if pattern not in section:
                errors.append(
                    f"docs/visual-benchmark-playbooks.md: `## {source}` missing `{pattern}`"
                )

    for relative_path in VISUAL_BENCHMARK_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if (
            "visual-benchmark-playbooks.md" not in text
            and "benchmark_playbooks" not in text
        ):
            errors.append(f"{relative_path}: missing visual benchmark playbooks reference")

    if errors:
        fail("Visual benchmark playbooks validation failed:\n" + "\n".join(errors))


def validate_golden_examples() -> None:
    index = (ROOT / "docs/golden-examples.md").read_text(encoding="utf-8")
    errors: list[str] = []

    for area, relative_path in GOLDEN_EXAMPLE_AREAS.items():
        if relative_path not in index:
            errors.append(f"docs/golden-examples.md: missing `{relative_path}`")
        if area not in index:
            errors.append(f"docs/golden-examples.md: missing `{area}`")

    for relative_path in GOLDEN_EXAMPLE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for pattern in [
            "## Prompt",
            "## Golden output",
            "## Design-quality notes",
        ]:
            if pattern not in text:
                errors.append(f"{relative_path}: missing `{pattern}`")
        if (
            "Quality target:" not in text
            and "Current design quality score:" not in text
            and not re.search(r"Current:\s*[1-5]/5", text)
        ):
            errors.append(
                f"{relative_path}: missing `Quality target:`, "
                "`Current design quality score:`, or `Current: n/5`"
            )

    for relative_path in GOLDEN_EXAMPLE_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if (
            "docs/golden-examples.md" not in text
            and "examples/golden" not in text
            and "golden_examples" not in text
        ):
            errors.append(f"{relative_path}: missing golden examples reference")

    if errors:
        fail("Golden examples validation failed:\n" + "\n".join(errors))


def validate_release_automation() -> None:
    script = (ROOT / "scripts/validate_release.py").read_text(encoding="utf-8")
    workflow = (ROOT / ".github/workflows/release-validate.yml").read_text(
        encoding="utf-8"
    )
    errors: list[str] = []

    for pattern in RELEASE_AUTOMATION_REQUIRED_PATTERNS:
        if pattern not in script and pattern not in workflow:
            errors.append(f"release automation missing `{pattern}`")

    for pattern in ["workflow_dispatch", "release_ref", "validate_release.py"]:
        if pattern not in workflow:
            errors.append(f".github/workflows/release-validate.yml: missing `{pattern}`")

    for relative_path in RELEASE_AUTOMATION_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "validate_release.py" not in text and "release_automation" not in text:
            errors.append(f"{relative_path}: missing release automation reference")

    if errors:
        fail("Release automation validation failed:\n" + "\n".join(errors))


def validate_synthetic_case_studies() -> None:
    index = (ROOT / "docs/synthetic-case-studies.md").read_text(encoding="utf-8")
    errors: list[str] = []

    for relative_path in SYNTHETIC_CASE_STUDY_FILES:
        if relative_path not in index:
            errors.append(f"docs/synthetic-case-studies.md: missing `{relative_path}`")

        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for section in SYNTHETIC_CASE_STUDY_SECTIONS:
            if section not in text:
                errors.append(f"{relative_path}: missing `{section}`")

        # Any 1-5 score, not literally 4/5: requiring one score here was itself a
        # monoculture generator -- it made "every case study is 4/5" a CI rule.
        if not re.search(r"\b[1-5]/5\b", text):
            errors.append(f"{relative_path}: missing a `[1-5]/5` quality target marker")
        if "real product" in text.lower() and "not" not in text.lower():
            errors.append(f"{relative_path}: must not imply real-product validation")
        regression_checks = extract_section(text, "Regression checks")
        if bullet_count(regression_checks) < 3:
            errors.append(
                f"{relative_path}: `## Regression checks` must contain at least 3 bullets"
            )

    for relative_path in [
        "SKILL.md",
        "README.md",
        "skill/metadata.yaml",
        "skill/usage.md",
        "docs/design-quality-rubric.md",
        "docs/evals.md",
    ]:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "synthetic-case-studies.md" not in text and "examples/case-studies" not in text:
            errors.append(f"{relative_path}: missing synthetic case studies reference")

    if errors:
        fail("Synthetic case studies validation failed:\n" + "\n".join(errors))


def validate_domain_packs() -> None:
    index = (ROOT / "docs/domain-packs/index.md").read_text(encoding="utf-8")
    errors: list[str] = []

    for relative_path in DOMAIN_PACK_FILES:
        if relative_path.removeprefix("docs/domain-packs/") not in index:
            errors.append(f"docs/domain-packs/index.md: missing `{relative_path}`")

        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for section in DOMAIN_PACK_SECTIONS:
            if section not in text:
                errors.append(f"{relative_path}: missing `{section}`")

        boundaries = extract_section(text, "Evidence And Compliance Boundaries")
        if "proof" not in boundaries.lower() or "compliance" not in boundaries.lower():
            errors.append(
                f"{relative_path}: evidence boundaries must mention proof and compliance"
            )

    for relative_path in [
        "SKILL.md",
        "README.md",
        "skill/metadata.yaml",
        "skill/usage.md",
        "docs/workflow.md",
        "docs/design-quality-rubric.md",
        "docs/evals.md",
    ]:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if (
            "docs/domain-packs" not in text
            and "domain-packs" not in text
            and "domain_packs" not in text
        ):
            errors.append(f"{relative_path}: missing domain packs reference")

    if errors:
        fail("Domain packs validation failed:\n" + "\n".join(errors))


def validate_visual_review_fixtures() -> None:
    index = (ROOT / "docs/visual-review-fixtures.md").read_text(encoding="utf-8")
    errors: list[str] = []

    for relative_path in VISUAL_REVIEW_FIXTURE_FILES:
        if relative_path not in index:
            errors.append(f"docs/visual-review-fixtures.md: missing `{relative_path}`")

        text = (ROOT / relative_path).read_text(encoding="utf-8")
        for section in VISUAL_REVIEW_FIXTURE_SECTIONS:
            if section not in text:
                errors.append(f"{relative_path}: missing `{section}`")
        if "Synthetic fixture only" not in text:
            errors.append(f"{relative_path}: missing synthetic fixture boundary")
        if "Do not claim" not in text:
            errors.append(f"{relative_path}: missing prohibited-claim guardrail")

    for relative_path in [
        "SKILL.md",
        "README.md",
        "skill/metadata.yaml",
        "docs/design-quality-rubric.md",
        "docs/evals.md",
    ]:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "visual-review-fixtures.md" not in text and "visual_review_fixtures" not in text:
            errors.append(f"{relative_path}: missing visual review fixtures reference")

    if errors:
        fail("Visual review fixtures validation failed:\n" + "\n".join(errors))


def validate_benchmark_report_format() -> None:
    doc = (ROOT / "docs/benchmark-report-format.md").read_text(encoding="utf-8")
    example = (ROOT / "examples/benchmark-report.md").read_text(encoding="utf-8")
    errors: list[str] = []

    for pattern in BENCHMARK_REPORT_REQUIRED_PATTERNS:
        if pattern not in doc:
            errors.append(f"docs/benchmark-report-format.md: missing `{pattern}`")
    for pattern in ["## Prompt", "## Report output", "Evidence boundaries", "Do not copy"]:
        if pattern not in example:
            errors.append(f"examples/benchmark-report.md: missing `{pattern}`")

    for relative_path in [
        "SKILL.md",
        "README.md",
        "skill/metadata.yaml",
        "skill/usage.md",
        "docs/evals.md",
        "docs/inspiration-sources.md",
    ]:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "benchmark-report-format.md" not in text and "benchmark_report_format" not in text:
            errors.append(f"{relative_path}: missing benchmark report format reference")

    if errors:
        fail("Benchmark report format validation failed:\n" + "\n".join(errors))


def validate_rendered_output_qa() -> None:
    doc = (ROOT / "docs/rendered-output-qa.md").read_text(encoding="utf-8")
    errors: list[str] = []

    for pattern in RENDERED_OUTPUT_QA_REQUIRED_PATTERNS:
        if pattern not in doc:
            errors.append(f"docs/rendered-output-qa.md: missing `{pattern}`")

    try:
        schema = json.loads(
            (ROOT / "examples/rendered-output-qa/report-schema.json").read_text(
                encoding="utf-8"
            )
        )
        sample = json.loads(
            (ROOT / "examples/rendered-output-qa/sample-report.json").read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError as exc:
        fail(f"Rendered-output QA JSON validation failed: {exc}")

    required = set(schema.get("required", []))
    missing_sample_keys = required - sample.keys()
    if missing_sample_keys:
        errors.append(
            "examples/rendered-output-qa/sample-report.json: missing required keys "
            + ", ".join(sorted(missing_sample_keys))
        )
    if schema.get("properties", {}).get("schema_version", {}).get("const") != "rendered-output-qa/v1":
        errors.append("report-schema.json: missing rendered-output-qa/v1 schema version")
    if sample.get("schema_version") != "rendered-output-qa/v1":
        errors.append("sample-report.json: missing rendered-output-qa/v1 schema version")

    for relative_path in [
        "SKILL.md",
        "README.md",
        "skill/metadata.yaml",
        "docs/design-quality-rubric.md",
        "docs/evals.md",
    ]:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "rendered-output-qa.md" not in text and "rendered_output_qa" not in text:
            errors.append(f"{relative_path}: missing rendered-output QA reference")

    if errors:
        fail("Rendered-output QA validation failed:\n" + "\n".join(errors))


# Contract elements are emitted by every mode, so they live in the output contract
# rather than in the per-mode lists. Parity compares only the mode-specific fields.
CONTRACT_ELEMENTS = {"mode", "platform scope", "device class", "assumptions", "next actions"}


def normalize_output_field(text: str) -> str:
    """Reduce an output-structure bullet to a comparable field name.

    Detail after an em dash is explanatory prose, not part of the contract, so it is
    dropped. `/` and `or` are used interchangeably across the two files.
    """
    field = re.sub(r"^[-*]\s+", "", text.strip())
    field = re.split(r"\s+—\s+", field, maxsplit=1)[0]
    field = field.replace("/", " or ")
    return re.sub(r"\s+", " ", field).strip().rstrip(".").lower()


def bullet_fields(block: str) -> set[str]:
    fields = {
        normalize_output_field(line)
        for line in block.splitlines()
        if re.match(r"^[-*]\s+\S", line)
    }
    return {field for field in fields if field and field not in CONTRACT_ELEMENTS}


def parse_skill_mode_fields() -> dict[str, set[str]]:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    section = re.search(
        r"^## Mode output requirements\s*$(?P<body>.*?)(?=^## |\Z)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    if not section:
        fail("SKILL.md: missing `## Mode output requirements` section")

    modes: dict[str, set[str]] = {}
    for match in re.finditer(
        r"^### Mode \d+:\s*(?P<title>.+?)\s*$(?P<body>.*?)(?=^### |\Z)",
        section.group("body"),
        re.DOTALL | re.MULTILINE,
    ):
        modes[normalize_output_field(match.group("title"))] = bullet_fields(match.group("body"))
    return modes


def parse_modes_doc_fields() -> dict[str, set[str]]:
    text = (ROOT / "skill/modes.md").read_text(encoding="utf-8")
    modes: dict[str, set[str]] = {}
    for match in re.finditer(
        r"^## Mode [A-Z]:\s*(?P<title>.+?)\s*$(?P<body>.*?)(?=^## |\Z)",
        text,
        re.DOTALL | re.MULTILINE,
    ):
        structure = re.search(
            r"^### Output structure\s*$(?P<body>.*?)(?=^### |\Z)",
            match.group("body"),
            re.DOTALL | re.MULTILINE,
        )
        if not structure:
            fail(f"skill/modes.md: mode `{match.group('title')}` has no `### Output structure`")
        modes[normalize_output_field(match.group("title"))] = bullet_fields(structure.group("body"))
    return modes


def validate_mode_parity() -> None:
    """SKILL.md is always loaded; skill/modes.md is not. Drift between them ships silently.

    This is the check that would have caught the v1.16.0 Mode D contract never reaching
    the entrypoint.
    """
    skill_modes = parse_skill_mode_fields()
    doc_modes = parse_modes_doc_fields()
    errors: list[str] = []

    if not skill_modes:
        errors.append("SKILL.md: no `### Mode <n>:` blocks found under `## Mode output requirements`")
    if not doc_modes:
        errors.append("skill/modes.md: no `## Mode <letter>:` blocks found")

    for title in sorted(set(skill_modes) - set(doc_modes)):
        errors.append(f"mode `{title}` is in SKILL.md but has no counterpart in skill/modes.md")
    for title in sorted(set(doc_modes) - set(skill_modes)):
        errors.append(f"mode `{title}` is in skill/modes.md but has no counterpart in SKILL.md")

    for title in sorted(set(skill_modes) & set(doc_modes)):
        only_skill = sorted(skill_modes[title] - doc_modes[title])
        only_doc = sorted(doc_modes[title] - skill_modes[title])
        if only_skill:
            errors.append(f"mode `{title}`: in SKILL.md but not skill/modes.md: {only_skill}")
        if only_doc:
            errors.append(f"mode `{title}`: in skill/modes.md but not SKILL.md: {only_doc}")

    if errors:
        fail(
            "Mode parity validation failed (SKILL.md and skill/modes.md must list the same "
            "output fields per mode):\n" + "\n".join(errors)
        )


SKILL_ENTRYPOINT_REQUIRED_PATTERNS = [
    # Step 3 resolves two axes, not one.
    "Device class:",
    "docs/adaptive-layout.md",
    # Divergence runs before drafting.
    "5.5",
    # An honest mismatch stays visible instead of being laundered into a template.
    "outside the standard six",
]

AUTH_WALLED_REFERENCE_FILES = [
    "docs/inspiration-sources.md",
    "docs/visual-benchmark-playbooks.md",
]


MAX_SINGLE_SCORE_SHARE = 0.75
MIN_DISTINCT_SCORES = 3

# The dimension vector is a second carrier of the same defect the two constants above
# guard, one level down: a corpus whose `Dimension read:` lines never print a band teaches
# a scale that has no such level. Before these checks the seven committed lines held 63
# values with ZERO 2s, and `attention path` and `composition` were the literal constant 4
# in all seven -- invisible to the share check, which reads only the headline, and to the
# fixture spread check, which reads only JSON.
#
# The numbers below are corpus-composition choices, not measurements. They are the same
# kind of number as `wide < 2` in the fixture pack and MIN_DISTINCT_SCORES above, and are
# recorded as such so nobody later reads them as an empirical bar.
MIN_DISTINCT_BANDS_PER_DIMENSION = 2
MIN_DISTINCT_BANDS_IN_FIXTURE_PACK = 3  # across `examples/evals/rubric-score-*.json`
MIN_WIDE_DIMENSION_READS = 2  # lines whose assessable bands span >= 3 points
MIN_MODE_D_DISTINCT_BANDS = 3  # per column, across all committed review tables

CANONICAL_DIMENSIONS = (
    "attention path",
    "composition",
    "typography",
    "colour/state",
    "density",
    "interaction",
    "context & brand fit",
    "production readiness",
    "distinctiveness",
)

DIMENSION_READ_LINE = re.compile(r"Dimension read:(?P<body>[^\n]*)")
DIMENSION_READ_PAIR = re.compile(r"^(?P<name>.+?)[:\s]\s*(?P<band>[1-5]|n/v)$", re.IGNORECASE)
# `Now | Projected` rows in a Mode D score table.
MODE_D_TABLE_ROW = re.compile(
    r"^\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<now>n/v|[1-5])\s*\|\s*(?P<projected>n/v|[1-5])\s*\|"
)


def parse_dimension_read(line: str) -> list[int | None]:
    """Bands from one `Dimension read:` line; `None` for `n/v`.

    Four shapes in the committed corpus have to survive: the trailing
    `Median of the assessable = N.` restatement on the same line, `colour/state`
    carrying a slash, `context & brand fit` carrying an ampersand and spaces, and
    `n/v` as a value that is excluded from the median rather than counted low.
    """
    match = DIMENSION_READ_LINE.search(line)
    if not match:
        return []
    core = re.split(r"Median of", match.group("body"), maxsplit=1)[0]
    bands: list[int | None] = []
    for chunk in core.split(","):
        # First band token in the chunk, not the whole chunk anchored. A live run appended
        # prose after the last dimension ("... distinctiveness 5. All nine assessable --
        # nothing is `n/v` ...") and an anchored match dropped that dimension silently,
        # which is the failure mode where a parser under-counts instead of erroring.
        pair = re.search(r"\b([1-5]|n/v)\b(?=[.,;]|\s|$)", chunk.strip(), re.IGNORECASE)
        if pair:
            band = pair.group(1).lower()
            bands.append(None if band == "n/v" else int(band))
    return bands


def label_body(section_text: str, label: str) -> str:
    """Text belonging to a `- Label:` bullet: its own line plus indented continuations."""
    lines = section_text.splitlines()
    body: list[str] = []
    for index, line in enumerate(lines):
        if not re.match(rf"^\s*-\s*{re.escape(label)}", line):
            continue
        body.append(re.sub(rf"^\s*-\s*{re.escape(label)}", "", line))
        for follow in lines[index + 1:]:
            if not follow.strip():
                break
            if re.match(r"^\s+", follow) and not re.match(r"^-", follow):
                body.append(re.sub(r"^\s*-\s*", "", follow))
                continue
            break
        break
    return " ".join(body).strip()


def catalog_entry_tokens() -> set[str]:
    """Distinctive names from the two catalogs step 5.5 samples.

    Parsed from docs/inspiration-sources.md rather than hard-coded, so adding a
    school or a point-of-view product automatically widens what provenance is
    accepted — the catalog is the single source of truth for the option set.
    """
    doc = (ROOT / "docs/inspiration-sources.md").read_text(encoding="utf-8")
    names: list[str] = re.findall(r"^#### (?P<name>.+?)\s*$", doc, re.MULTILINE)

    products = re.search(
        r"^### Point-of-view products.*?$(?P<body>.*?)(?=^### |^---|\Z)",
        doc,
        re.DOTALL | re.MULTILINE,
    )
    if products:
        for row in re.findall(r"^\|\s*(?P<cell>[^|]+?)\s*\|", products.group("body"), re.MULTILINE):
            if cell_is_header(row):
                continue
            names.append(row)

    tokens = {"baseline"}
    for name in names:
        cleaned = re.sub(r"[*_`]", "", name)
        for part in re.split(r"[/,;]| and ", cleaned):
            part = part.strip().strip(".").lower()
            if len(part) > 3:
                tokens.add(part)
    return tokens


def cell_is_header(cell: str) -> bool:
    stripped = cell.strip().lower()
    return stripped in {"product", "source", "school", ""} or set(stripped) <= set("-: ")


def validate_direction_provenance() -> None:
    """Two of step 5.5's three directions come from the catalog, and say so.

    Live acceptance for v1.17.0 showed four runs of one prompt generating the same
    candidate pair and committing to the same winner: a free-generated candidate set
    is unimodal. Requiring the provenance makes a bypassed catalog visible in the
    output instead of hidden in the reasoning.
    """
    tokens = catalog_entry_tokens()
    if len(tokens) < 8:
        fail(
            "docs/inspiration-sources.md: could not parse the direction catalog "
            f"(found {len(tokens)} usable entry tokens); step 5.5 has nothing to sample"
        )

    errors: list[str] = []
    for relative_path in ("examples/generate-screen.md", "examples/ui-spec.md"):
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        section = extract_section(text, "Alternatives considered") or extract_section(
            text, "Key decision tradeoffs"
        )
        provenances = re.findall(r"from:\s*(?P<src>[^)\n,;]+)", section, re.IGNORECASE)
        if len(provenances) < 2:
            errors.append(
                f"{relative_path}: rejected directions must carry `from:` provenance "
                f"for the catalog entry they were derived from; found {len(provenances)}"
            )
            continue
        for source in provenances:
            normalized = re.sub(r"[*_`]", "", source).strip().lower()
            if not any(tok in normalized or normalized in tok for tok in tokens):
                errors.append(
                    f"{relative_path}: `from: {source.strip()}` is not an entry in the "
                    "direction catalog in docs/inspiration-sources.md"
                )

    if errors:
        fail("Direction provenance validation failed:\n" + "\n".join(errors))


def validate_calibration_corpus_diversity() -> None:
    """The calibration corpus is loaded exactly when taste is being decided.

    A corpus where almost every exemplar carries the same score teaches the model to
    print that score. Before this check, 21 of 23 `Quality target:` values were 4/5.

    Note on what is NOT checked here: a pairwise n-gram similarity check over the
    calibration bodies was specified and then dropped. Measured against the real
    corpus its median was 0.0 (max 0.043) because the blocks describe different
    domains in different words — it would have passed vacuously forever while the
    structural sameness it was meant to catch went unmeasured. Signature-move
    distinctness below is the instrument that actually bites.
    """
    errors: list[str] = []
    scores: list[str] = []
    signatures: dict[str, str] = {}

    for file_path in sorted((ROOT / "examples").rglob("*.md")):
        relative_path = file_path.relative_to(ROOT).as_posix()
        text = file_path.read_text(encoding="utf-8")
        scores.extend(re.findall(r"Quality target:\s*\[?([1-5])/5", text))
        for match in re.finditer(r"^\s*-?\s*Signature move:\s*(?P<body>\S.*)$", text, re.MULTILINE):
            body = match.group("body")
            if body.lower().lstrip().startswith(("none", "[")):
                continue  # an honest "inert" record, or a template placeholder
            key = re.sub(r"[^a-z0-9 ]", " ", body.lower())
            key = " ".join(key.split()[:12])
            if key in signatures and signatures[key] != relative_path:
                errors.append(
                    f"{relative_path}: `Signature move:` duplicates {signatures[key]} — "
                    "an owned asset shared across two exemplars is not owned"
                )
            signatures.setdefault(key, relative_path)

    if not scores:
        errors.append("examples/: no `Quality target:` values found")
    else:
        counts = Counter(scores)
        top_score, top_count = counts.most_common(1)[0]
        share = top_count / len(scores)
        if share > MAX_SINGLE_SCORE_SHARE:
            errors.append(
                f"examples/: {top_count} of {len(scores)} `Quality target:` values are "
                f"{top_score}/5 ({share:.0%}); a calibration corpus above "
                f"{MAX_SINGLE_SCORE_SHARE:.0%} on one score teaches the model to print it"
            )
        if len(counts) < MIN_DISTINCT_SCORES:
            errors.append(
                f"examples/: only {len(counts)} distinct `Quality target:` score(s); "
                f"the corpus must demonstrate at least {MIN_DISTINCT_SCORES}"
            )

    errors.extend(dimension_band_diversity_errors())

    if errors:
        fail("Calibration corpus diversity validation failed:\n" + "\n".join(errors))


def dimension_band_diversity_errors() -> list[str]:
    """The same defect one level below the headline, and in both of its carriers.

    Scores are printed twice in this corpus: as a `Dimension read:` bullet in the
    generation modes, and as a `| Now | Projected |` table in Mode D. Each was pinned to
    its own two-value band -- generation to {3,4}, review to {2,3} -- and the two regimes
    hid each other, because the union across both carriers covered more ground than either
    did. So these assert per carrier, never on the merged set.
    """
    errors: list[str] = []
    reads: list[tuple[str, list[int | None]]] = []
    now_bands: list[int] = []
    projected_bands: list[int] = []

    for file_path in sorted((ROOT / "examples").rglob("*.md")):
        relative_path = file_path.relative_to(ROOT).as_posix()
        for number, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            if "Dimension read:" in line and "[dimension]" not in line:
                reads.append((f"{relative_path}:{number}", parse_dimension_read(line)))
                continue
            row = MODE_D_TABLE_ROW.match(line)
            if row and "dimension" not in row.group("name").lower():
                for band, sink in ((row.group("now"), now_bands), (row.group("projected"), projected_bands)):
                    if band != "n/v":
                        sink.append(int(band))

    if not reads:
        return ["examples/: no `Dimension read:` lines found"]

    assessable = [[band for band in bands if band is not None] for _, bands in reads]
    values = [band for bands in assessable for band in bands]

    missing = sorted({1, 2, 3, 4, 5} - set(values))
    if missing:
        errors.append(
            f"examples/: no `Dimension read:` band of {missing} anywhere in {len(values)} "
            "values; a corpus that never scores a level teaches a scale that has no such level"
        )

    for index, name in enumerate(CANONICAL_DIMENSIONS):
        seen = {bands[index] for _, bands in reads if len(bands) > index and bands[index] is not None}
        if len(seen) < MIN_DISTINCT_BANDS_PER_DIMENSION:
            errors.append(
                f"examples/: `{name}` is {seen.pop() if seen else 'unread'} in every "
                "`Dimension read:` line; a single-valued dimension is measuring the rubric, "
                "not the artifact"
            )

    if not any(bands and min(bands) <= 2 and max(bands) >= 5 for bands in assessable):
        errors.append(
            "examples/: no `Dimension read:` line carries both a band <=2 and a band >=5; "
            "the corpus never demonstrates a design strong in one place and weak in another, "
            "which is the case `Do not average away a serious flaw` describes"
        )

    wide = sum(1 for bands in assessable if bands and max(bands) - min(bands) >= 3)
    if wide < MIN_WIDE_DIMENSION_READS:
        errors.append(
            f"examples/: only {wide} `Dimension read:` line(s) span 3+ bands; at least "
            f"{MIN_WIDE_DIMENSION_READS} must, or the median rule is never exercised on a real spread"
        )

    for label, bands in (("Now", now_bands), ("Projected", projected_bands)):
        if not bands:
            errors.append(f"examples/: no Mode D `{label}` bands found in any review table")
        elif len(set(bands)) < MIN_MODE_D_DISTINCT_BANDS:
            errors.append(
                f"examples/: Mode D `{label}` column takes only {sorted(set(bands))} across "
                f"{len(bands)} assessable rows; fewer than {MIN_MODE_D_DISTINCT_BANDS} distinct "
                "bands is a review corpus that has stopped reading"
            )

    return errors


PRESCRIBED_SCORE_PATTERNS = [
    r"target\s+\**4/5\**\s+before",
    r"internally target 4/5",
    r"target 4/5 quality",
    # A filled-in illustrative line outweighs a prose instruction to derive: live
    # acceptance showed three of four runs reproducing the doc's example blocker
    # near-verbatim. Reference docs carry the derivation form, never a filled score.
    r"Quality target:\s*[1-5]/5\s*[-—]",
    # A pre-handoff sweep found two survivors the first three patterns could not
    # reach, in files the scope did not cover. Widen both together or neither.
    r"target(?:ing)?\s+(?:at least\s+)?\**4/5",
]
PRESCRIBED_SCORE_SCOPE = ("docs/", "skill/", "SKILL.md")


def validate_score_is_derived_not_prescribed() -> None:
    """A prescribed target is not a score.

    Live acceptance for v1.17.0 produced 4/5 on five of five runs while every
    structural validator passed: the template slot had been un-nailed, but seven
    instruction sites still told the model to aim at 4/5, so it aimed and hit.
    """
    errors: list[str] = []
    for file_path in iter_markdown_files():
        relative_path = file_path.relative_to(ROOT).as_posix()
        if relative_path.startswith("docs/proposals/") or relative_path == "CHANGELOG.md":
            continue  # these record the history of the defect
        if not relative_path.startswith(PRESCRIBED_SCORE_SCOPE):
            continue  # examples are meant to carry real derived scores
        text = file_path.read_text(encoding="utf-8")
        for pattern in PRESCRIBED_SCORE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(
                    f"{relative_path}: /{pattern}/ prescribes the score instead of "
                    "deriving it from the assessable dimensions"
                )

    errors.extend(score_anchor_errors())

    if errors:
        fail("Prescribed-score validation failed:\n" + "\n".join(errors))


# The defect class, stated once: any instruction-carrying text that supplies a PRIOR OVER
# THE VALUE of a derived score, rather than a RULE THE DERIVATION MUST OBEY.
#
# The discriminator, applied per sentence: is this statement's truth value knowable before
# the dimension read exists? "A good draft usually lands at 4/5" is -- anchor. "If the
# derived score is below N, revise" is not -- trigger, and triggers stay.
#
# The patterns above this comment are a synonym list built one defect at a time, and by the
# time this class was written they matched ZERO lines inside their own scope: every live
# anchor had drifted to phrasings without the word "target" ("usually lands at", "4/5-style",
# "At 4/5,", "not a quiet 4/5"). These four are scoped to the class instead.
SCORE_ANCHOR_PATTERNS = [
    (
        "frequency anchor — states where scores usually land, which is knowable before any artifact is read",
        r"\b(usual(?:ly)?|typical(?:ly)?|normal(?:ly)?|generally|commonly|in practice|tends? to|"
        r"most\s+(?:drafts?|designs?|responses?|screens?|specs?|artifacts?))\b[^.\n]{0,80}\b[1-5]\s*/\s*5\b",
    ),
    (
        "frequency anchor — names a score as the expected or default outcome",
        r"\b[1-5]\s*/\s*5\b[^.\n]{0,60}\b(?:is|are|remains?)\s+(?:the\s+)?"
        r"(?:usual|typical|normal|expected|common|default)\b",
    ),
    (
        "exemplar-label anchor — tags a corpus or exemplar with a score level, so imitating it targets that level",
        r"\b[1-5]\s*/\s*5[-\s](?:style|shaped|grade|level|calibre|caliber)\b"
        r"|\ban?\s+(?:\w+\s+){0,2}[1-5]\s*/\s*5\s+"
        r"(?:answer|response|spec|draft|design|example|output|screen|artifact)s?\b",
    ),
    (
        "presupposition anchor — grammar that assumes a score as the current state",
        r"\bquiet\s+[1-5]\s*/\s*5\b"
        r"|\b(?:is|sits|stays|stops?|stopping|remains?|settles?)\s+at\s+[1-5]\s*/\s*5\b"
        r"|\bstopping at the default\b",
    ),
]
# Three exclusions, each for a construction that names a score without supplying a prior.
# They are listed with their false positive so the next reader can tell the difference:
#   - a before/after pair states two derived scores    `the upgrade path from 2/5 to 4/5`
#   - a negated label denies a level rather than setting one
#                                                     `2/5 state handling is not a 4/5 design`
#   - a claim about one named artifact is data         `the screen is at 2/5 with a severity-3`
SCORE_TRANSITION = re.compile(
    r"\b([1-5])\s*/\s*5\b[^\n]{0,60}?(?:→|->|\bto\b|\bbecomes?\b|\binto\b|\bupgrades?\b)"
    r"[^\n]{0,60}?\b([1-5])\s*/\s*5\b"
)
NEGATED_SCORE_LABEL = re.compile(r"\b(?:not|never|rather than|instead of)\s+an?\s+(?:\w+\s+){0,3}[1-5]\s*/\s*5\b", re.IGNORECASE)
SPECIFIC_ARTIFACT_CLAIM = re.compile(
    r"\b(?:the|this)\s+(?:\w+\s+){0,2}(?:screen|draft|design|spec|response|answer|review|artifact|result|read)"
    r"\s+(?:is|sits|stays|remains)\s+at\s+[1-5]\s*/\s*5\b",
    re.IGNORECASE,
)


def anchor_is_excluded(line: str) -> bool:
    transition = SCORE_TRANSITION.search(line)
    if transition and transition.group(1) != transition.group(2):
        return True
    return bool(NEGATED_SCORE_LABEL.search(line) or SPECIFIC_ARTIFACT_CLAIM.search(line))
# A floor on the derivation's INPUTS is the sharpest form of the class: it forbids emitting
# a low band at all. Captured and compared rather than matched literally, so no threshold is
# invented -- the guard only asserts that a stated band range equals the scale.
DIMENSION_FLOOR_PATTERN = (
    r"\b(?:any|each|every|no)\s+dimension\s+(?:that\s+)?(?:scor\w+\s+)?"
    r"(?:below|under|less\s+than|beneath)\s+\**([1-5])\b"
)
DIMENSION_RANGE_PATTERN = (
    r"\bscore\s+(?:each|every|all)\s+(?:relevant\s+)?dimensions?\s+(?:from\s+)?"
    r"\**([1-5])\**\s*(?:or|to|and|[-–—])\s*\**([1-5])\b"
)
# A cap is a downward clamp with a named exit; it is the opposite of a prior and may use
# frequency vocabulary legitimately ("a P1 weakness normally caps the score at 2/5").
# Named here rather than exempted silently, so an anchor cannot be laundered by inserting
# the word "cap".
CAP_VOCABULARY = re.compile(r"\b(caps?|capped|capping|hard limit|Fail|floor|ceiling|until fixed)\b", re.IGNORECASE)
# Derived-score slots in the corpus carry real numbers by design. Excluded by line shape,
# not by directory, so anchors living in prose beside them are still scanned.
SCORE_SLOT_LINE = re.compile(
    r"^\s*[-*>|]?\s*\**(?:Quality target|Dimension read|Current|Projected|Ceiling note|Score|"
    r"Expected score|Quality target after fixes)\**\s*:"
)
ANCHOR_SCAN_EXTRA_FILES = ("skill/metadata.yaml", "agents/openai.yaml")
ANCHOR_SCAN_SKIP = ("docs/proposals/", "CHANGELOG.md")


def score_anchor_errors() -> list[str]:
    errors: list[str] = []
    paths = [p for p in iter_markdown_files()]
    paths += [ROOT / name for name in ANCHOR_SCAN_EXTRA_FILES if (ROOT / name).exists()]

    for file_path in sorted(set(paths)):
        relative_path = file_path.relative_to(ROOT).as_posix()
        if relative_path.startswith(ANCHOR_SCAN_SKIP):
            continue  # these record the history of the defect
        for number, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            if SCORE_SLOT_LINE.match(line) or anchor_is_excluded(line):
                continue
            for label, pattern in SCORE_ANCHOR_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE) and not CAP_VOCABULARY.search(line):
                    errors.append(f"{relative_path}:{number}: {label} — `{line.strip()[:90]}`")
            floor = re.search(DIMENSION_FLOOR_PATTERN, line, re.IGNORECASE)
            if floor and int(floor.group(1)) > 1:
                errors.append(
                    f"{relative_path}:{number}: floor on the derivation's inputs — no dimension "
                    f"may be reported below {floor.group(1)}, which is a prior, not a rule"
                )
            band_range = re.search(DIMENSION_RANGE_PATTERN, line, re.IGNORECASE)
            if band_range and (band_range.group(1), band_range.group(2)) != ("1", "5"):
                errors.append(
                    f"{relative_path}:{number}: dimensions are told to score "
                    f"{band_range.group(1)}-{band_range.group(2)} rather than across the whole scale"
                )

    return errors


def validate_modes_carry_contract_elements() -> None:
    """The authoritative file must not teach a shape the scorers reject.

    `SKILL.md` names `skill/modes.md` the tiebreaker, and its `### Output structure`
    blocks are what a model copies. All six omitted `Device class` while both the
    response validator and the generation eval hard-failed any response without it —
    invisible to mode parity, because contract elements are stripped before comparing.
    """
    doc = (ROOT / "skill/modes.md").read_text(encoding="utf-8")
    blocks = re.findall(
        r"^### Output structure\s*$(?P<body>.*?)(?=^### |\Z)", doc, re.DOTALL | re.MULTILINE
    )
    if len(blocks) != 6:
        fail(f"skill/modes.md: expected 6 `### Output structure` blocks, found {len(blocks)}")

    errors: list[str] = []
    for index, body in enumerate(blocks, start=1):
        listed = {normalize_output_field(line) for line in body.splitlines() if line.startswith("- ")}
        missing = sorted(CONTRACT_ELEMENTS - listed - {"sub-case (d1 or d2 or d3 or d4)"})
        if missing:
            errors.append(
                f"skill/modes.md: output structure #{index} omits contract element(s) "
                + ", ".join(f"`{m}`" for m in missing)
            )

    if errors:
        fail("Mode contract-element validation failed:\n" + "\n".join(errors))


BANNED_MODE_D_HEADERS = ("## Usability issues", "## Accessibility issues", "## Recommended fixes", "## Severity or priority")


def validate_calibration_teaches_current_shape() -> None:
    """A banned shape may appear as a counterexample, never as a model answer.

    examples/anti-patterns.md loads as calibration (SKILL.md), and two of its
    "Good response" fragments still carried the pre-1.16 Mode D bucket shape that
    SKILL.md explicitly bans. The changelog for 1.17.0 documents that a filled-in
    example outweighs a prose instruction three runs in four; this was that failure,
    live, inside the file meant to demonstrate correctness.
    """
    text = (ROOT / "examples/anti-patterns.md").read_text(encoding="utf-8")
    errors: list[str] = []
    good = False
    for number, line in enumerate(text.splitlines(), start=1):
        if re.match(r"^### (Good|Bad) response", line):
            good = line.startswith("### Good")
            continue
        if good and any(line.startswith(h) for h in BANNED_MODE_D_HEADERS):
            errors.append(
                f"examples/anti-patterns.md:{number}: `{line.strip()}` is the pre-1.16 "
                "Mode D shape and must not appear under a `### Good response`"
            )

    if errors:
        fail("Calibration-shape validation failed:\n" + "\n".join(errors))


def validate_single_workflow_source() -> None:
    """Exactly one file may claim to be the workflow.

    Three files each describing the workflow (SKILL.md, skill/skill.md,
    skill/modes.md) is the structural condition that let the v1.16.0 Mode D
    contract ship without reaching the entrypoint. skill/skill.md was retired in
    v1.18.1 after drifting two releases behind — it carried none of step 5.5,
    device class, the no-fit branch, the derived score or direction provenance,
    while still asserting a pre-1.16 review rule. This check stops a third fork
    from quietly reappearing.
    """
    errors: list[str] = []

    owners = {
        "## Mode output requirements": "SKILL.md",
        "## Required workflow": "SKILL.md",
    }
    for marker, owner in owners.items():
        holders = [
            f.relative_to(ROOT).as_posix()
            for f in iter_markdown_files()
            if marker in f.read_text(encoding="utf-8")
        ]
        # The changelog and the proposal quote these headings when describing changes.
        holders = [
            h for h in holders
            if not h.startswith("docs/proposals/") and h != "CHANGELOG.md"
        ]
        if holders != [owner]:
            errors.append(
                f"`{marker}` must appear in {owner} and nowhere else; found in "
                + (", ".join(holders) if holders else "no file")
            )

    if errors:
        fail(
            "Single-workflow-source validation failed (a second file claiming to be "
            "the workflow drifts, and the drift ships):\n" + "\n".join(errors)
        )


def validate_skill_entrypoint_contract() -> None:
    """SKILL.md is the only always-loaded file, so capability lives or dies here.

    Every branch listed below reached the entrypoint in a specific release. This
    check exists because the v1.16.0 Mode D contract did not, and nothing noticed.
    """
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    missing = [p for p in SKILL_ENTRYPOINT_REQUIRED_PATTERNS if p not in skill]
    if missing:
        fail(
            "SKILL.md is missing required entrypoint contract markers "
            "(a capability that never reaches SKILL.md is effectively absent): "
            + ", ".join(missing)
        )


def validate_unreadable_source_honesty() -> None:
    """Auth-walled references must be framed as a lookup, never as something consulted."""
    errors: list[str] = []

    for relative_path in AUTH_WALLED_REFERENCE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if "cannot" not in text.lower() or "sign-in" not in text.lower():
            errors.append(
                f"{relative_path}: must state plainly that Mobbin / Page Flows / "
                "UI Sources / Pttrns cannot be opened by a skill run"
            )

    review = (ROOT / "docs/self-review.md").read_text(encoding="utf-8")
    if re.search(r"Did I use production references", review):
        errors.append(
            "docs/self-review.md: the prompt asking whether production references were "
            "*used* invites describing screens the skill has never seen; ask whether the "
            "reference was framed as a lookup instead"
        )

    if errors:
        fail("Unreadable-source honesty validation failed:\n" + "\n".join(errors))


def validate_inspiration_gate_parity() -> None:
    """The inspiration gate in SKILL.md must not be narrower than the layer it guards.

    Before this check, SKILL.md listed 4 trigger signals while
    docs/inspiration-sources.md declared 9 — so requests like "make it feel premium"
    never reached the layer whose own trigger list names that exact phrase, and the
    direction vocabulary behind it stayed unreachable.
    """
    doc = (ROOT / "docs/inspiration-sources.md").read_text(encoding="utf-8")
    section = re.search(
        r"^## When to use inspiration\s*$(?P<body>.*?)(?=^## |\Z)",
        doc,
        re.DOTALL | re.MULTILINE,
    )
    if not section:
        fail("docs/inspiration-sources.md: missing `## When to use inspiration` section")

    signals = re.findall(r'^-\s+"(?P<signal>[^"]+)"', section.group("body"), re.MULTILINE)
    if len(signals) < 5:
        fail(
            "docs/inspiration-sources.md: expected the trigger list to enumerate the "
            f"inspiration signals as quoted bullets; found {len(signals)}"
        )

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    missing = [signal for signal in signals if signal.lower() not in skill.lower()]
    if missing:
        fail(
            "Inspiration gate is narrower than the layer it guards. SKILL.md does not "
            "carry these signals from docs/inspiration-sources.md: "
            + ", ".join(f'"{signal}"' for signal in missing)
        )


def validate_motion_band_consistency() -> None:
    """One authority for motion durations.

    `docs/design-quality.md` used to declare a 200-500ms "personality band" while
    `docs/quality-bars.md` capped full-screen navigation at 400ms, so a motion
    signature had no legal room and the two files disagreed silently.
    """
    errors: list[str] = []

    bars = (ROOT / "docs/quality-bars.md").read_text(encoding="utf-8")
    if not re.search(r"^### Signature transition\s*$", bars, re.MULTILINE):
        errors.append(
            "docs/quality-bars.md: missing `### Signature transition` — the motion "
            "signature needs a band defined where the durations live"
        )

    quality = (ROOT / "docs/design-quality.md").read_text(encoding="utf-8")
    motion = re.search(r"^### Motion-personality tokens.*?(?=^###|\Z)", quality, re.DOTALL | re.MULTILINE)
    if not motion:
        errors.append("docs/design-quality.md: missing `### Motion-personality tokens`")
    elif "quality-bars.md" not in motion.group(0):
        errors.append(
            "docs/design-quality.md: the motion-personality section must defer to "
            "`docs/quality-bars.md` rather than declaring its own duration band"
        )

    motion = (ROOT / "docs/motion-system.md").read_text(encoding="utf-8")
    if "docs/quality-bars.md" not in motion:
        errors.append(
            "docs/motion-system.md: must defer to `docs/quality-bars.md` for durations "
            "rather than declaring its own bands"
        )
    for relative_path in ("SKILL.md", "docs/quality-bars.md", "docs/workflow.md", "docs/design-quality.md"):
        if "motion-system.md" not in (ROOT / relative_path).read_text(encoding="utf-8"):
            errors.append(f"{relative_path}: missing motion system reference")

    for relative_path, text in (
        ("docs/design-quality.md", quality),
        ("docs/quality-bars.md", bars),
        ("docs/motion-system.md", motion),
    ):
        for number, line in enumerate(text.splitlines(), start=1):
            if re.search(r"\b(?:4[1-9]\d|[5-9]\d\d|\d{4,})\s?ms\b", line):
                errors.append(
                    f"{relative_path}:{number}: motion duration above the 400 ms "
                    "signature ceiling"
                )

    if errors:
        fail("Motion band validation failed:\n" + "\n".join(errors))


# The defect class: a surface the workflow routes a design choice to carries no device-class
# layer, so a tablet request is answered out of phone-only material. `docs/patterns-catalog.md`
# was that surface -- fourteen sections of phone patterns and no entry that decides a layout at
# regular width, while SKILL.md step 8 sends every pattern-level decision to it. Enumerating the
# surfaces rather than the file makes the guard fire for the next one that loses the layer.
LARGE_SCREEN_DECISION_SURFACES = [
    "docs/patterns-catalog.md",
    "docs/quality-bars.md",
    "docs/context-defaults.md",
    "docs/adaptive-layout.md",
]

LARGE_SCREEN_REQUIRED_TERMS = [
    "compact",
    "expanded",
    "list-detail",
    "navigation rail",
    "sidebar",
]

# The second half of the class. Once the bars are repeated for lookup at the point of decision,
# the copies drift -- the failure `validate_motion_band_consistency` was written for. A width
# threshold is a comparison operator, a number, and a unit, on a line naming a width class.
WIDTH_CLASS_BREAKPOINTS = {"600", "840", "1200"}
# Anchored to the class name and stopped at the cell boundary, so a pane minimum in the next
# column of the same row is not read as a breakpoint; height classes carry their own numbers.
WIDTH_CLASS_THRESHOLD_RE = re.compile(
    r"\b(?:compact|medium|expanded)\b[^|\n]{0,40}?"
    r"(?:<=|>=|<|>|\u2264|\u2265)\s*~?\s*(\d{3,4})\s*(?:dp|pt)\b",
    re.IGNORECASE,
)


def validate_large_screen_coverage() -> None:
    """Every decision surface carries the device-class layer, and they agree on the numbers."""
    errors: list[str] = []

    for relative_path in LARGE_SCREEN_DECISION_SURFACES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        lowered = text.lower()
        for term in LARGE_SCREEN_REQUIRED_TERMS:
            if term not in lowered:
                errors.append(
                    f"{relative_path}: missing `{term}` -- a decision surface without the "
                    "device-class layer answers a tablet request out of phone-only material"
                )
        for breakpoint in ("600", "840"):
            if breakpoint not in text:
                errors.append(
                    f"{relative_path}: missing the `{breakpoint}` width-class breakpoint"
                )

    for file_path in iter_markdown_files():
        relative_path = file_path.relative_to(ROOT).as_posix()
        if relative_path.startswith("docs/proposals/") or relative_path == "CHANGELOG.md":
            continue  # these record the history, including superseded numbers
        for number, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            if "height" in line.lower():
                continue  # height classes are a different axis with their own numbers
            for value in WIDTH_CLASS_THRESHOLD_RE.findall(line):
                if value not in WIDTH_CLASS_BREAKPOINTS:
                    errors.append(
                        f"{relative_path}:{number}: width-class threshold `{value}` disagrees "
                        "with the breakpoints in docs/quality-bars.md "
                        f"({', '.join(sorted(WIDTH_CLASS_BREAKPOINTS))})"
                    )

    if errors:
        fail("Large-screen coverage validation failed:\n" + "\n".join(errors))


# The defect class: a file ships, every validator passes, and the README never learns about it.
# v1.30.1 repaired three of these at once -- docs/motion-system.md, the tablet golden and the
# stretched-phone fixture were registered in their own indexes and in this script, and none of the
# 32 validators reads the README's enumerations. Scoped to the class rather than to those three.
# v1.35.1 shipped the same class again in a directory the globs did not reach: `SKILL.md`
# sends the reader to `scripts/run_generation_eval.py`, and the README -- the document a
# reader starts from -- names neither it nor `run_diversity_eval.py`. Shipped code is a
# shipped file. The `examples/` globs below were already satisfied when they were added;
# they are here to keep them satisfied, which is what a guard is for.
README_MUST_ENUMERATE = [
    "docs/*.md",
    "docs/domain-packs/*.md",
    "scripts/*.py",
    "scripts/*.sh",
    "examples/*.md",
    "examples/golden/*.md",
    "examples/visual-review-fixtures/*.md",
    "examples/case-studies/*.md",
    "examples/evals/*.json",
    "examples/rendered-output-qa/*.json",
]


def validate_paired_eval_falsifier() -> None:
    """The falsifier cell must still falsify, and the two refusals must still refuse.

    `run_paired_eval.py` is worth having only because it declines to report a
    contrast whose own control failed. Both the ceiling that makes it decline and
    the fixture corpus that proves it declines can be deleted without any other
    check in this repository noticing — the self-test would keep passing on the two
    corpora that remain, and the harness would keep printing win rates it has no
    right to print.

    Asserting that the word "null" appears somewhere would be the shape check
    proposal section 27 warned about. These four are computable properties of the
    thing itself: the falsifier corpus exists, its nulls really do draw agreed
    winners, and neither refusal has been widened into a no-op.
    """
    errors: list[str] = []

    script = (ROOT / "scripts/run_paired_eval.py").read_text(encoding="utf-8")

    ceiling = re.search(r"^NULL_AGREED_WINNER_MAX = (?P<expr>.+)$", script, re.MULTILINE)
    if not ceiling:
        errors.append("scripts/run_paired_eval.py: no `NULL_AGREED_WINNER_MAX` ceiling on the control")
    else:
        try:
            value = eval(ceiling.group("expr"), {"__builtins__": {}})  # noqa: S307 - a literal ratio
        except Exception:
            value = None
        if not isinstance(value, (int, float)) or not 0 < value < 1:
            errors.append(
                f"scripts/run_paired_eval.py: `NULL_AGREED_WINNER_MAX` is {ceiling.group('expr')!r}; "
                "a ceiling at or above 1 never refuses a failed control, which is the "
                "only reason this harness exists"
            )

    minimum = re.search(r"^MIN_NULL_PAIRS = (?P<value>\d+)$", script, re.MULTILINE)
    if not minimum or int(minimum.group("value")) < 1:
        errors.append(
            "scripts/run_paired_eval.py: `MIN_NULL_PAIRS` must require at least one null "
            "pair; a contrast with no control is the failure this guards"
        )

    try:
        pack = json.loads((ROOT / "examples/evals/paired-comparison-fixtures.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("Paired-comparison falsifier validation failed:\n  - missing examples/evals/paired-comparison-fixtures.json")
    except json.JSONDecodeError as exc:
        fail(f"Paired-comparison falsifier validation failed:\n  - fixture pack is not valid JSON ({exc})")

    for corpus in ("separating", "indistinguishable", "broken_control"):
        if corpus not in pack:
            errors.append(f"examples/evals/paired-comparison-fixtures.json: missing the `{corpus}` corpus")

    broken = pack.get("broken_control", {})
    verdicts = broken.get("verdicts", {})
    null_pairs: dict[str, set[str]] = {}
    for pair_id, verdict in verdicts.items():
        if not pair_id.startswith("null-"):
            continue
        null_pairs.setdefault(pair_id.rsplit("-", 1)[0], set()).add(verdict)
    agreed = sum(
        1
        for calls in null_pairs.values()
        if len(calls) == 2 and calls == {"document-1", "document-2"}
    )
    if not null_pairs:
        errors.append(
            "examples/evals/paired-comparison-fixtures.json: the `broken_control` corpus has "
            "no null-pair verdicts, so it cannot falsify anything"
        )
    elif agreed == 0:
        errors.append(
            "examples/evals/paired-comparison-fixtures.json: no null pair in `broken_control` "
            "draws an agreed winner across both orders, so the corpus no longer represents a "
            "failed control and the self-test's refusal assertion is vacuous"
        )

    if errors:
        fail("Paired-comparison falsifier validation failed:\n" + "\n".join(f"  - {e}" for e in errors))


# The mirror of README_MUST_ENUMERATE, for the document the MODEL starts from. Until
# 1.35.2 the asymmetry ran the wrong way: every shipped doc had to be named in the README,
# which a human reads, and nothing had to be named in `SKILL.md`, which is what actually
# gets loaded at runtime. `docs/paired-comparison.md` sat outside the entrypoint that way
# while its siblings `docs/evals.md` and `docs/llm-judge-runner.md` were inside it.
#
# The four exclusions below are process documents about releasing this repository, not
# about designing a screen. They are deliberately outside a runtime reading list; each
# one carries the reason it is excluded, so a fifth cannot be added silently.
SKILL_ENTRYPOINT_DOC_EXCLUSIONS = {
    "docs/commands.md": "invocation reference for the slash command, not runtime design guidance",
    "docs/github-publishing.md": "publishing kit for maintainers of this repository",
    "docs/release-automation.md": "release validation workflow, run by CI and maintainers",
    "docs/versioning.md": "semver policy for this repository",
}


def validate_skill_entrypoint_enumerates_docs() -> None:
    """Every runtime doc is named in the canonical `SKILL.md`, and the wrapper mirrors it.

    Two failures this catches, both of which shipped:

    1. A doc lands under `docs/`, is wired into its neighbours, passes every validator,
       and the entrypoint the model reads never mentions it.
    2. The canonical entrypoint and the Claude Code wrapper drift apart, so the same
       skill loads a different set of documents depending on how it was invoked. Before
       1.35.2 the wrapper was missing five docs the canon named.
    """
    errors: list[str] = []
    canonical = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    wrapper_path = ROOT / ".claude/skills/mobile-design-skill/SKILL.md"
    wrapper = wrapper_path.read_text(encoding="utf-8")

    for path in sorted(ROOT.glob("docs/*.md")):
        relative_path = path.relative_to(ROOT).as_posix()
        if relative_path in SKILL_ENTRYPOINT_DOC_EXCLUSIONS:
            continue
        if path.name not in canonical:
            errors.append(
                f"SKILL.md: never names `{relative_path}` -- a document the model is never "
                "told to read is not shipped guidance. Add it to the reference list, or add "
                "it to SKILL_ENTRYPOINT_DOC_EXCLUSIONS with the reason it is not runtime"
            )

    for name in sorted(set(re.findall(r"`(docs/[A-Za-z0-9_./-]+\.md)`", canonical))):
        if Path(name).name not in wrapper:
            errors.append(
                f".claude/skills/mobile-design-skill/SKILL.md: canonical SKILL.md names "
                f"`{name}` and the wrapper does not -- /mobile-design-skill would load a "
                "different document set than the canonical entrypoint"
            )

    if errors:
        fail("Skill entrypoint enumeration failed:\n" + "\n".join(f"  - {e}" for e in errors))


def validate_readme_enumerates_shipped_files() -> None:
    """Every shipped reference file is named somewhere in README.md."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    errors: list[str] = []

    for pattern in README_MUST_ENUMERATE:
        for path in sorted(ROOT.glob(pattern)):
            if path.name.lower() == "index.md":
                continue
            if path.name not in readme:
                relative_path = path.relative_to(ROOT).as_posix()
                errors.append(
                    f"README.md: never names `{relative_path}` -- a file can ship, pass every "
                    "other validator, and stay invisible to the one document a reader starts from"
                )

    if errors:
        fail("README enumeration validation failed:\n" + "\n".join(errors))


def validate_projected_score_lines() -> None:
    """The projected score is a flat median, never a ceiling and never `up to N/5`."""
    errors: list[str] = []

    for file_path in sorted((ROOT / "examples").rglob("*.md")):
        relative_path = file_path.relative_to(ROOT).as_posix()
        for number, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not re.match(r"^[-*]\s*Projected:", line):
                continue
            if not re.match(r"^[-*]\s*Projected:\s*[1-5]/5\b", line):
                errors.append(
                    f"{relative_path}:{number}: `Projected:` must state a flat [1-5]/5 number"
                )
            lowered = line.lower()
            for phrase in ("up to", "ceiling"):
                if phrase in lowered:
                    errors.append(
                        f"{relative_path}:{number}: `Projected:` line must not contain "
                        f"`{phrase}` — a post-visual-pass figure belongs in `Ceiling note`"
                    )

    if errors:
        fail("Projected-score validation failed:\n" + "\n".join(errors))


def iter_markdown_files() -> list[Path]:
    markdown_files: list[Path] = []
    for pattern in MARKDOWN_GLOBS:
        markdown_files.extend(ROOT.glob(pattern))
    return sorted(set(markdown_files))


def validate_documentation_hygiene() -> None:
    errors: list[str] = []

    for file_path in iter_markdown_files():
        relative_path = file_path.relative_to(ROOT).as_posix()
        text = file_path.read_text(encoding="utf-8")
        in_fence = False
        seen_headings: dict[str, int] = {}

        for lineno, line in enumerate(text.splitlines(), start=1):
            if line.rstrip(" \t") != line:
                errors.append(f"{relative_path}:{lineno}: trailing whitespace")

            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
            if not heading_match:
                continue

            heading = f"{heading_match.group(1)} {heading_match.group(2).strip()}"
            if relative_path in DUPLICATE_HEADING_ALLOWED_FILES:
                continue

            previous_line = seen_headings.get(heading)
            if previous_line:
                errors.append(
                    f"{relative_path}:{lineno}: duplicate heading `{heading}` "
                    f"(first seen on line {previous_line})"
                )
            else:
                seen_headings[heading] = lineno

    if errors:
        fail("Documentation hygiene validation failed:\n" + "\n".join(errors))


def validate_links() -> None:
    missing_links: list[str] = []
    for file_path in iter_markdown_files():
        text = file_path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for match in LINK_RE.finditer(line):
                target = match.group(1).strip()
                if not target or "://" in target or target.startswith("#") or target.startswith("mailto:"):
                    continue
                candidate = (file_path.parent / target).resolve()
                fallback = (ROOT / target).resolve()
                if not candidate.exists() and not fallback.exists():
                    missing_links.append(f"{file_path.relative_to(ROOT)}:{lineno} -> {target}")

    if missing_links:
        fail("Broken relative links found:\n" + "\n".join(missing_links))


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*\n(?P<body>.*?)(?=^## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def bullet_count(text: str) -> int:
    return len(re.findall(r"(?m)^-\s+\S", text))


def check_response(response: str, mode: str, label: str) -> list[str]:
    """The structural contract for one skill response — corpus or freshly generated.

    Split out of validate_example_responses() so scripts/run_generation_eval.py can
    hold live output to exactly the rules the committed examples are held to. Every
    check in this repo used to read markdown a human wrote; this is the seam that
    lets one read what the model actually produced.
    """
    errors: list[str] = []
    requirements = MODE_REQUIREMENTS.get(mode)
    if not requirements:
        return [f"{label}: unknown mode `{mode}`"]

    if not response.startswith(f"Mode: {mode}"):
        errors.append(f"{label}: response must start with exact `Mode: {mode}`")

    if not re.search(r"^Platform scope:\s+\S", response, re.MULTILINE):
        errors.append(f"{label}: missing `Platform scope:` line")

    device_class = re.search(r"^Device class:\s+(?P<value>\S.*)$", response, re.MULTILINE)
    if not device_class:
        errors.append(f"{label}: missing `Device class:` line")
    elif "phone" not in device_class.group("value").lower():
        # Anything wider than a phone must say what the layout does at each width.
        if not re.search(r"^## Adaptive behavior\s*$", response, re.MULTILINE):
            errors.append(
                f"{label}: `Device class: {device_class.group('value')}` "
                "requires an `## Adaptive behavior` section"
            )

    assumptions = extract_assumptions(response)
    if bullet_count(assumptions) < 2:
        errors.append(f"{label}: `Assumptions:` must contain at least 2 bullets")

    for section in requirements["sections"]:
        if not re.search(rf"^## {re.escape(section)}\s*$", response, re.MULTILINE):
            errors.append(f"{label}: missing `## {section}` section")

    for section in requirements["accessibility_sections"]:
        if bullet_count(extract_section(response, section)) < 3:
            errors.append(
                f"{label}: `## {section}` must contain at least 3 bullets"
            )

    next_actions = extract_section(response, "Next actions")
    if bullet_count(next_actions) < 2:
        errors.append(f"{label}: `## Next actions` must contain at least 2 bullets")
    for action in re.findall(r"(?m)^-\s+(.+)$", next_actions):
        # A denylist of five phrases caught "test it" and nothing else. What
        # separates a real next action from a stock one is that it names an
        # object: "validate" is one word, "Validate whether balance and blackout
        # data are real-time or cached" is eleven. Word count is the shape test;
        # requiring a digit or proper noun was tried and rejected, because it
        # fails specific, well-written actions and rewards inserting a number.
        if len(action.split()) < 6:
            errors.append(
                f"{label}: next action `{action.strip()}` is too short to "
                "name an object; say what is tested, defined, or confirmed"
            )

    if requirements.get("requires_sub_case") and not re.search(
        r"^Sub-case:\s+\S", response, re.MULTILINE
    ):
        errors.append(f"{label}: missing `Sub-case:` line")

    for section, field, min_words in requirements.get("label_word_counts", []):
        words = len(label_body(extract_section(response, section), field).split())
        if words < min_words:
            errors.append(
                f"{label}: `## {section}` gives only {words} words after "
                f"`{field}` (minimum {min_words}) — a label is not a statement"
            )

    for section, spec in requirements.get("bullet_shapes", []):
        body = extract_section(response, section)
        bullets = re.findall(r"(?m)^-\s+(.+)$", body)
        matching = [b for b in bullets if re.search(spec["pattern"], b, re.IGNORECASE)]
        if len(matching) < spec["min_bullets"]:
            errors.append(
                f"{label}: `## {section}` needs at least "
                f"{spec['min_bullets']} bullets matching /{spec['pattern']}/; "
                f"found {len(matching)}"
            )
        for bullet in matching:
            tail = re.split(spec["tail_after"], bullet, maxsplit=1, flags=re.IGNORECASE)
            words = len(tail[-1].split()) if len(tail) > 1 else 0
            if words < spec["min_tail_words"]:
                errors.append(
                    f"{label}: `## {section}` bullet gives only {words} "
                    f"words after `{spec['tail_label']}` "
                    f"(minimum {spec['min_tail_words']}): {bullet[:70]}"
                )

    for section, pattern in requirements.get("must_contain", []):
        body = extract_section(response, section)
        if not re.search(pattern, body, re.IGNORECASE):
            errors.append(
                f"{label}: `## {section}` must match /{pattern}/"
            )

    for section, pattern in requirements.get("must_not_contain", []):
        body = extract_section(response, section)
        if re.search(pattern, body, re.IGNORECASE):
            errors.append(
                f"{label}: `## {section}` must NOT match /{pattern}/"
            )

    for pattern in BANNED_RESPONSE_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            errors.append(f"{label}: banned response phrase /{pattern}/")

    return errors


def validate_example_responses() -> None:
    errors: list[str] = []

    for relative_path in EXAMPLE_RESPONSE_FILES:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        output_match = EXAMPLE_OUTPUT_RE.search(text)
        if not output_match:
            errors.append(f"{relative_path}: missing fenced `## Example output` block")
            continue

        response = output_match.group("body").strip()
        mode_match = re.match(r"^Mode:\s*(.+)$", response, re.MULTILINE)
        if not mode_match:
            errors.append(f"{relative_path}: missing `Mode:` line")
            continue

        errors.extend(check_response(response, mode_match.group(1).strip(), relative_path))

    if errors:
        fail("Example response validation failed:\n" + "\n".join(errors))


def extract_assumptions(text: str) -> str:
    pattern = re.compile(
        r"^Assumptions:\s*\n(?P<body>.*?)(?=^## |\Z)",
        re.DOTALL | re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def main() -> None:
    validate_required_files()
    validate_skill_frontmatter()
    validate_weakness_layer()
    validate_design_quality_rubric_layer()
    validate_rubric_eval_pack()
    validate_llm_judge_runner_contract()
    validate_clarification_policy_layer()
    validate_judged_mode_layer()
    validate_visual_benchmark_playbooks()
    validate_golden_examples()
    validate_release_automation()
    validate_synthetic_case_studies()
    validate_domain_packs()
    validate_visual_review_fixtures()
    validate_benchmark_report_format()
    validate_rendered_output_qa()
    validate_mode_parity()
    validate_direction_provenance()
    validate_calibration_corpus_diversity()
    validate_score_is_derived_not_prescribed()
    validate_modes_carry_contract_elements()
    validate_calibration_teaches_current_shape()
    validate_single_workflow_source()
    validate_skill_entrypoint_contract()
    validate_unreadable_source_honesty()
    validate_inspiration_gate_parity()
    validate_motion_band_consistency()
    validate_large_screen_coverage()
    validate_paired_eval_falsifier()
    validate_readme_enumerates_shipped_files()
    validate_skill_entrypoint_enumerates_docs()
    validate_projected_score_lines()
    validate_documentation_hygiene()
    validate_links()
    validate_example_responses()
    print(
        "[OK] Repository structure, documentation hygiene, relative links, "
        "and example responses are valid."
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        fail(f"Unexpected validation error: {exc}")
