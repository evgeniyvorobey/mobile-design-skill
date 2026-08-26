#!/usr/bin/env python3
"""
Bump the skill version across all files that track it.

Usage:
    python3 scripts/bump_version.py major
    python3 scripts/bump_version.py minor
    python3 scripts/bump_version.py patch
    python3 scripts/bump_version.py 1.4.0
    python3 scripts/bump_version.py --show

Semver policy for this skill is defined in `docs/versioning.md`.

The single source of truth is `skill/metadata.yaml`. This script:

1. Reads the current version.
2. Computes the new version.
3. Updates every file that carries the version string.
4. Inserts an `## [Unreleased]` placeholder at the top of CHANGELOG.md.
5. Prints next steps (edit the CHANGELOG entry, commit, tag, push).
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

METADATA_PATH = ROOT / "skill" / "metadata.yaml"
SKILL_MD_PATH = ROOT / "SKILL.md"
CLAUDE_SKILL_MD_PATH = ROOT / ".claude" / "skills" / "mobile-design-skill" / "SKILL.md"
README_PATH = ROOT / "README.md"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
METADATA_VERSION_RE = re.compile(r"^version:\s*(\d+\.\d+\.\d+)\s*$", re.MULTILINE)
FRONTMATTER_VERSION_RE = re.compile(r"^version:\s*(\d+\.\d+\.\d+)\s*$", re.MULTILINE)
README_BADGE_RE = re.compile(
    r"(!\[version\]\(https://img\.shields\.io/badge/version-)(\d+\.\d+\.\d+)(-[a-zA-Z]+\))"
)
# Also match the HTML <img> form so the script stays in sync when the README
# uses HTML for layout (centered hero block).
README_HTML_BADGE_RE = re.compile(
    r'(<img\s+alt="version"\s+src="https://img\.shields\.io/badge/version-)(\d+\.\d+\.\d+)(-[a-zA-Z]+">)'
)
README_CURRENT_VERSION_RE = re.compile(
    r"(Current version:\s*\*\*)(\d+\.\d+\.\d+)(\*\*)"
)


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def read_metadata_version() -> str:
    text = METADATA_PATH.read_text(encoding="utf-8")
    match = METADATA_VERSION_RE.search(text)
    if not match:
        fail(f"Could not find `version:` in {METADATA_PATH.relative_to(ROOT)}")
    return match.group(1)


def parse_semver(value: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(value)
    if not match:
        fail(f"Not a valid semver: {value}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def compute_next_version(current: str, argument: str) -> str:
    if SEMVER_RE.match(argument):
        return argument

    major, minor, patch = parse_semver(current)
    if argument == "major":
        return f"{major + 1}.0.0"
    if argument == "minor":
        return f"{major}.{minor + 1}.0"
    if argument == "patch":
        return f"{major}.{minor}.{patch + 1}"
    fail(f"Unknown bump type: {argument}. Use major | minor | patch | X.Y.Z.")
    return ""  # unreachable, silences type checker


def update_metadata(new_version: str) -> None:
    text = METADATA_PATH.read_text(encoding="utf-8")
    text, count = METADATA_VERSION_RE.subn(f"version: {new_version}", text, count=1)
    if count != 1:
        fail(f"Failed to update version in {METADATA_PATH.relative_to(ROOT)}")
    METADATA_PATH.write_text(text, encoding="utf-8")


def update_frontmatter_version(path: Path, new_version: str) -> bool:
    """Set `version:` in the YAML frontmatter if the frontmatter exists. Returns True if written."""
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter_match:
        return False
    frontmatter = frontmatter_match.group(1)
    if FRONTMATTER_VERSION_RE.search(frontmatter):
        new_frontmatter = FRONTMATTER_VERSION_RE.sub(
            f"version: {new_version}", frontmatter, count=1
        )
    else:
        new_frontmatter = frontmatter.rstrip() + f"\nversion: {new_version}"
    updated = text.replace(frontmatter, new_frontmatter, 1)
    path.write_text(updated, encoding="utf-8")
    return True


def update_readme_badge(new_version: str) -> bool:
    """Update every version reference in the README: markdown badge, HTML badge, and the
    'Current version: **X.Y.Z**' line. Returns True if at least one reference was updated."""
    if not README_PATH.exists():
        return False
    text = README_PATH.read_text(encoding="utf-8")
    total = 0
    for pattern in (README_BADGE_RE, README_HTML_BADGE_RE, README_CURRENT_VERSION_RE):
        text, count = pattern.subn(rf"\g<1>{new_version}\g<3>", text, count=1)
        total += count
    if total == 0:
        return False
    README_PATH.write_text(text, encoding="utf-8")
    return True


def insert_changelog_placeholder(new_version: str) -> bool:
    """Insert an `## [Unreleased]` placeholder at the top of the CHANGELOG.

    The placeholder is deliberately NOT labelled with the new version. A placeholder
    that already carries the version number is structurally indistinguishable from a
    finished release entry: releases 1.33.5 through 1.35.1 each shipped with the
    placeholder left in place and the real entry appended underneath, producing two
    `## [x.y.z]` headings for one release, and `validate_release.py` accepted every
    one of them. `## [Unreleased]` cannot be mistaken for a release -- the release
    gate rejects a non-semver top heading, so the entry has to be written and
    renamed before the version can be tagged.
    """
    text = CHANGELOG_PATH.read_text(encoding="utf-8")
    if re.search(rf"^## \[{re.escape(new_version)}\]", text, re.MULTILINE):
        return False
    if re.search(r"^## \[Unreleased\]", text, re.MULTILINE):
        return False

    placeholder = (
        "## [Unreleased]\n\n"
        "### Added\n"
        "- \n\n"
        "### Changed\n"
        "- \n\n"
    )

    pattern = re.compile(r"^(# Changelog.*?\n\n)(## \[)", re.DOTALL | re.MULTILINE)
    match = pattern.search(text)
    if not match:
        fail(
            "Could not find a previous `## [x.y.z]` entry in CHANGELOG.md to anchor the insertion"
        )

    updated = pattern.sub(rf"\g<1>{placeholder}\g<2>", text, count=1)
    CHANGELOG_PATH.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    if len(sys.argv) < 2:
        fail("Usage: bump_version.py <major|minor|patch|X.Y.Z|--show>")

    argument = sys.argv[1]

    current = read_metadata_version()

    if argument == "--show":
        print(current)
        return

    new_version = compute_next_version(current, argument)

    if new_version == current:
        fail(f"New version equals current ({current}). Nothing to do.")

    update_metadata(new_version)
    frontmatter_root = update_frontmatter_version(SKILL_MD_PATH, new_version)
    frontmatter_claude = update_frontmatter_version(CLAUDE_SKILL_MD_PATH, new_version)
    readme_updated = update_readme_badge(new_version)
    changelog_inserted = insert_changelog_placeholder(new_version)

    print(f"[OK] Version bumped: {current} -> {new_version}")
    print("")
    print("Updated files:")
    print(f"  - {METADATA_PATH.relative_to(ROOT)}")
    if frontmatter_root:
        print(f"  - {SKILL_MD_PATH.relative_to(ROOT)} (frontmatter)")
    if frontmatter_claude:
        print(f"  - {CLAUDE_SKILL_MD_PATH.relative_to(ROOT)} (frontmatter)")
    if readme_updated:
        print(f"  - {README_PATH.relative_to(ROOT)} (badge)")
    if changelog_inserted:
        print(f"  - {CHANGELOG_PATH.relative_to(ROOT)} (`## [Unreleased]` placeholder)")
    print("")
    print("Next steps:")
    print(f"  1. Write the CHANGELOG.md entry, then rename `## [Unreleased]` to "
          f"`## [{new_version}] - {date.today().isoformat()}`")
    print("  2. Run: python3 scripts/validate_repo.py")
    print("  3. Commit the changes")
    print(f"  4. Tag: git tag v{new_version}")
    print("  5. Push: git push && git push --tags")


if __name__ == "__main__":
    main()
