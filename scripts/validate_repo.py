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
    "docs/guardrails.md",
    "docs/principles.md",
    "docs/sources.md",
    "docs/workflow.md",
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


def main() -> None:
    validate_required_files()
    validate_skill_frontmatter()
    validate_links()
    print("[OK] Repository structure and relative links are valid.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        fail(f"Unexpected validation error: {exc}")
