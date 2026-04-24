#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "SKILL.md",
    ".claude/skills/mobile-design-skill/SKILL.md",
    "agents/openai.yaml",
    "skill/skill.md",
    "skill/metadata.yaml",
    "skill/modes.md",
    "skill/templates.md",
    "skill/usage.md",
    "docs/context-defaults.md",
    "docs/design-quality.md",
    "docs/design-quality-rubric.md",
    "docs/evals.md",
    "docs/guardrails.md",
    "docs/heuristics.md",
    "docs/inspiration-sources.md",
    "docs/patterns-catalog.md",
    "docs/principles.md",
    "docs/quality-bars.md",
    "docs/self-review.md",
    "docs/sources.md",
    "docs/versioning.md",
    "docs/weaknesses.md",
    "docs/workflow.md",
    "examples/design-flow.md",
    "examples/generate-screen.md",
    "examples/rationale-handoff.md",
    "examples/review-screen.md",
    "examples/typography-spacing.md",
    "examples/ui-spec.md",
    "examples/anti-patterns.md",
    "scripts/bump_version.py",
    "scripts/install.sh",
    "assets/logo-light.svg",
    "assets/logo-dark.svg",
]

MARKDOWN_GLOBS = [
    "README.md",
    "SKILL.md",
    ".claude/skills/*/SKILL.md",
    "docs/*.md",
    "skill/*.md",
    "examples/*.md",
]

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
        "must_contain": [
            ("Design quality calibration", r"Attention path:"),
            ("Design quality calibration", r"Composition and spacing:"),
            ("Design quality calibration", r"Production checks:"),
            ("Design quality calibration", r"\b[1-5]/5\b"),
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
        "must_contain": [
            ("Spacing and layout notes", r"\b\d+\s?(dp|pt|sp|px)\b|space-\d+"),
            ("Typography rules", r"\b\d+\s?(sp|pt|px)\b|body|title|label|caption"),
            ("Design quality requirements", r"Attention path:"),
            ("Design quality requirements", r"Production checks:"),
            ("Design quality requirements", r"\b[1-5]/5\b"),
        ],
    },
    "Review screen for usability/accessibility": {
        "sections": [
            "Quick summary",
            "Strengths",
            "Usability issues",
            "Accessibility issues",
            "Hierarchy and readability issues",
            "Design quality issues",
            "Navigation and interaction issues",
            "Severity / priority",
            "Recommended fixes",
            "Platform-convention mismatches",
            "Unresolved assumptions",
            "Next actions",
        ],
        "accessibility_sections": ["Accessibility issues"],
        "requires_sub_case": True,
        "must_contain": [
            ("Design quality issues", r"Current design quality score:.*\b[1-5]/5\b"),
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
            ("Pattern choices and why", r"\bover\b"),
            ("Design quality rationale", r"mechanism:"),
            ("Design quality rationale", r"\b[1-5]/5\b"),
        ],
    },
}

BANNED_RESPONSE_PATTERNS = [
    r"\bWCAG-compliant\b",
    r"\bpasses accessibility\b",
    r"\bfully accessible\b",
    r"\baccessibility compliant\b",
]
GENERIC_NEXT_ACTIONS = {
    "test it",
    "validate",
    "iterate",
    "improve",
    "build this design",
}

WEAKNESS_REFERENCE_FILES = [
    "SKILL.md",
    ".claude/skills/mobile-design-skill/SKILL.md",
    "README.md",
    "skill/skill.md",
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
    "skill/skill.md",
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
    "Improvement ladder",
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


def validate_links() -> None:
    markdown_files: list[Path] = []
    for pattern in MARKDOWN_GLOBS:
        markdown_files.extend(ROOT.glob(pattern))

    missing_links: list[str] = []
    for file_path in sorted(set(markdown_files)):
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


def validate_example_responses() -> None:
    errors: list[str] = []

    for relative_path in EXAMPLE_RESPONSE_FILES:
        file_path = ROOT / relative_path
        text = file_path.read_text(encoding="utf-8")
        output_match = EXAMPLE_OUTPUT_RE.search(text)
        if not output_match:
            errors.append(f"{relative_path}: missing fenced `## Example output` block")
            continue

        response = output_match.group("body").strip()
        mode_match = re.match(r"^Mode:\s*(.+)$", response, re.MULTILINE)
        if not mode_match:
            errors.append(f"{relative_path}: missing `Mode:` line")
            continue

        mode = mode_match.group(1).strip()
        requirements = MODE_REQUIREMENTS.get(mode)
        if not requirements:
            errors.append(f"{relative_path}: unknown mode `{mode}`")
            continue

        if not response.startswith(f"Mode: {mode}"):
            errors.append(f"{relative_path}: response must start with exact `Mode: {mode}`")

        if not re.search(r"^Platform scope:\s+\S", response, re.MULTILINE):
            errors.append(f"{relative_path}: missing `Platform scope:` line")

        assumptions = extract_assumptions(response)
        if bullet_count(assumptions) < 2:
            errors.append(f"{relative_path}: `Assumptions:` must contain at least 2 bullets")

        for section in requirements["sections"]:
            if not re.search(rf"^## {re.escape(section)}\s*$", response, re.MULTILINE):
                errors.append(f"{relative_path}: missing `## {section}` section")

        for section in requirements["accessibility_sections"]:
            if bullet_count(extract_section(response, section)) < 3:
                errors.append(
                    f"{relative_path}: `## {section}` must contain at least 3 bullets"
                )

        next_actions = extract_section(response, "Next actions")
        if bullet_count(next_actions) < 2:
            errors.append(f"{relative_path}: `## Next actions` must contain at least 2 bullets")
        for action in re.findall(r"(?m)^-\s+(.+)$", next_actions):
            normalized = action.strip().rstrip(".").lower()
            if normalized in GENERIC_NEXT_ACTIONS:
                errors.append(f"{relative_path}: generic next action `{action}`")

        if requirements.get("requires_sub_case") and not re.search(
            r"^Sub-case:\s+\S", response, re.MULTILINE
        ):
            errors.append(f"{relative_path}: missing `Sub-case:` line")

        for section, pattern in requirements.get("must_contain", []):
            body = extract_section(response, section)
            if not re.search(pattern, body, re.IGNORECASE):
                errors.append(
                    f"{relative_path}: `## {section}` must match /{pattern}/"
                )

        for pattern in BANNED_RESPONSE_PATTERNS:
            if re.search(pattern, response, re.IGNORECASE):
                errors.append(f"{relative_path}: banned response phrase /{pattern}/")

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
    validate_links()
    validate_example_responses()
    print("[OK] Repository structure, relative links, and example responses are valid.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        fail(f"Unexpected validation error: {exc}")
