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


def validate_rubric_eval_pack() -> None:
    seen_scores: set[int] = set()
    spreads: dict[str, int] = {}
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

    if errors:
        fail("Calibration corpus diversity validation failed:\n" + "\n".join(errors))


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

    if errors:
        fail("Prescribed-score validation failed:\n" + "\n".join(errors))


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

    for relative_path, text in (
        ("docs/design-quality.md", quality),
        ("docs/quality-bars.md", bars),
    ):
        for number, line in enumerate(text.splitlines(), start=1):
            if re.search(r"\b(?:4[1-9]\d|[5-9]\d\d|\d{4,})\s?ms\b", line):
                errors.append(
                    f"{relative_path}:{number}: motion duration above the 400 ms "
                    "signature ceiling"
                )

    if errors:
        fail("Motion band validation failed:\n" + "\n".join(errors))


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
