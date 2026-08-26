#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

METADATA_PATH = ROOT / "skill" / "metadata.yaml"
SKILL_PATH = ROOT / "SKILL.md"
CLAUDE_WRAPPER_PATH = ROOT / ".claude" / "skills" / "mobile-design-skill" / "SKILL.md"
README_PATH = ROOT / "README.md"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"

SEMVER_PATTERN = (
    r"(?:0|[1-9]\d*)\."
    r"(?:0|[1-9]\d*)\."
    r"(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z](?:[0-9A-Za-z.-]*[0-9A-Za-z])?)?"
    r"(?:\+[0-9A-Za-z](?:[0-9A-Za-z.-]*[0-9A-Za-z])?)?"
)
SEMVER_RE = re.compile(rf"^{SEMVER_PATTERN}$")
METADATA_VERSION_RE = re.compile(
    rf"^version:\s*[\"']?({SEMVER_PATTERN})[\"']?\s*$",
    re.MULTILINE,
)
FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
FRONTMATTER_VERSION_RE = re.compile(
    rf"^version:\s*[\"']?({SEMVER_PATTERN})[\"']?\s*$",
    re.MULTILINE,
)
README_MARKDOWN_BADGE_RE = re.compile(
    rf"!\[version\]\("
    rf"https://img\.shields\.io/badge/version-({SEMVER_PATTERN})-[A-Za-z0-9_-]+"
    rf"(?:\?[^)]*)?\)"
)
README_HTML_BADGE_RE = re.compile(
    rf"<img\b(?=[^>]*\balt=[\"']version[\"'])[^>]*"
    rf"\bsrc=[\"']"
    rf"https://img\.shields\.io/badge/version-({SEMVER_PATTERN})-[A-Za-z0-9_-]+"
    rf"(?:\?[^\"']*)?[\"'][^>]*>",
    re.IGNORECASE,
)
README_CURRENT_VERSION_RE = re.compile(
    rf"Current version:\s*\*\*({SEMVER_PATTERN})\*\*"
)
CHANGELOG_ENTRY_RE = re.compile(
    r"^## \[(?P<label>[^\]]+)\](?:\s*-\s*(?P<date>\d{4}-\d{2}-\d{2}))?",
    re.MULTILINE,
)


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    if not path.exists():
        fail(f"Missing required release validation file: {relative(path)}")
    return path.read_text(encoding="utf-8")


def extract_single_version(pattern: re.Pattern[str], text: str, label: str) -> str:
    matches = pattern.findall(text)
    if len(matches) != 1:
        fail(f"Expected exactly one version in {label}; found {len(matches)}")
    version = matches[0]
    if not SEMVER_RE.match(version):
        fail(f"{label} contains invalid semver `{version}`")
    return version


def read_frontmatter_version(path: Path) -> str:
    text = read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(f"{relative(path)} must begin with YAML frontmatter")
    return extract_single_version(
        FRONTMATTER_VERSION_RE,
        match.group("body"),
        f"{relative(path)} frontmatter",
    )


def read_readme_versions() -> tuple[list[str], str]:
    text = read_text(README_PATH)
    badge_versions = [
        *README_MARKDOWN_BADGE_RE.findall(text),
        *README_HTML_BADGE_RE.findall(text),
    ]
    if not badge_versions:
        fail("README.md must contain a version badge")

    for version in badge_versions:
        if not SEMVER_RE.match(version):
            fail(f"README.md version badge contains invalid semver `{version}`")

    current_version = extract_single_version(
        README_CURRENT_VERSION_RE,
        text,
        "README.md current version line",
    )
    return badge_versions, current_version


def changelog_entry_body(text: str, match: re.Match[str]) -> str:
    """Everything between one `## [x.y.z]` heading and the next one, or the end of file."""
    following = CHANGELOG_ENTRY_RE.search(text, match.end())
    return text[match.end():following.start() if following else len(text)]


def changelog_body_is_empty(body: str) -> bool:
    """True when the entry carries no prose: only `### Section` headings and bare bullets.

    `bump_version.py` writes exactly that shape as a placeholder. A placeholder is
    indistinguishable from a described release to every other check in this file,
    so a release with zero lines of description would otherwise pass the gate.
    """
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if re.fullmatch(r"[-*+]\s*", stripped):
            continue
        return False
    return True


def read_changelog_top_version() -> str:
    text = read_text(CHANGELOG_PATH)
    matches = list(CHANGELOG_ENTRY_RE.finditer(text))
    if not matches:
        fail("CHANGELOG.md must contain a top release entry like `## [1.2.3] - YYYY-MM-DD`")

    match = matches[0]
    label = match.group("label").strip()
    if not SEMVER_RE.match(label):
        if label.lower() == "unreleased":
            fail(
                "CHANGELOG.md still opens with the `## [Unreleased]` placeholder that "
                "`bump_version.py` wrote. Write the entry, then rename the heading to "
                "`## [x.y.z] - YYYY-MM-DD` -- a release is not describable until it is"
            )
        fail(f"CHANGELOG.md top release entry is not a semver version: `{label}`")

    # Two ways a release ships with no readable history, both observed on this repo:
    # a placeholder left unfilled, and a placeholder left in place above the real entry.
    if changelog_body_is_empty(changelog_entry_body(text, match)):
        fail(
            f"CHANGELOG.md entry `## [{label}]` has an empty body -- section headings and "
            "bare bullets only. Fill in the placeholder that `bump_version.py` wrote, or "
            "delete it if the real entry is written elsewhere in the file"
        )

    counts: dict[str, int] = {}
    for entry in matches:
        entry_label = entry.group("label").strip()
        counts[entry_label] = counts.get(entry_label, 0) + 1
    duplicates = sorted(version for version, count in counts.items() if count > 1)
    if duplicates:
        fail(
            "CHANGELOG.md repeats these version headings: "
            + ", ".join(f"`## [{version}]`" for version in duplicates)
            + " -- a duplicate heading means an unfilled placeholder was left above the "
            "real entry, and the release history reads as two entries for one release"
        )

    return label


def normalize_tag_or_ref(value: str) -> str:
    normalized = value.strip()
    if normalized.startswith("refs/tags/"):
        return normalized.removeprefix("refs/tags/")
    if normalized.startswith("tags/"):
        return normalized.removeprefix("tags/")
    return normalized


def validate_version_sanity(tag_or_ref: str | None) -> None:
    print("\n== Version/tag sanity check ==", flush=True)

    metadata_version = extract_single_version(
        METADATA_VERSION_RE,
        read_text(METADATA_PATH),
        relative(METADATA_PATH),
    )

    versions: list[tuple[str, str]] = [
        (relative(SKILL_PATH), read_frontmatter_version(SKILL_PATH)),
        (relative(CLAUDE_WRAPPER_PATH), read_frontmatter_version(CLAUDE_WRAPPER_PATH)),
    ]

    readme_badge_versions, readme_current_version = read_readme_versions()
    versions.extend(
        (f"README.md version badge #{index}", version)
        for index, version in enumerate(readme_badge_versions, start=1)
    )
    versions.append(("README.md current version", readme_current_version))
    versions.append(("CHANGELOG.md top entry", read_changelog_top_version()))

    errors = [
        f"{label}: expected {metadata_version}, got {version}"
        for label, version in versions
        if version != metadata_version
    ]

    if tag_or_ref:
        expected_tag = f"v{metadata_version}"
        actual_tag = normalize_tag_or_ref(tag_or_ref)
        if actual_tag != expected_tag:
            errors.append(
                f"release tag/ref: expected `{expected_tag}` or `refs/tags/{expected_tag}`, "
                f"got `{tag_or_ref}`"
            )

    if errors:
        fail("Release version sanity failed:\n" + "\n".join(errors))

    print(f"[OK] Release version references are synchronized at {metadata_version}.")
    if tag_or_ref:
        print(f"[OK] Release tag/ref matches v{metadata_version}.")


def run_step(name: str, command: list[str]) -> None:
    print(f"\n== {name} ==", flush=True)
    print("$ " + " ".join(shlex.quote(part) for part in command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, check=False)
    if completed.returncode != 0:
        fail(f"{name} failed with exit code {completed.returncode}")


def release_tmp_dir() -> Path:
    base = Path(os.environ.get("RUNNER_TEMP", "/tmp"))
    return base / "mobile-design-skill-release-validation"


def run_release_checks() -> None:
    run_step("Repository validation", [sys.executable, "scripts/validate_repo.py"])
    run_step(
        "Install verification (both methods, every reference resolves)",
        [sys.executable, "scripts/verify_install.py"],
    )
    run_step(
        "Diversity metric self-test",
        [sys.executable, "scripts/run_diversity_eval.py", "--self-test"],
    )
    run_step(
        "Generation eval prompt pack",
        [sys.executable, "scripts/run_generation_eval.py", "--dry-run"],
    )
    run_step(
        "Generation eval oracle replay",
        [
            sys.executable,
            "scripts/run_generation_eval.py",
            "--replayable-only",
            "--generate-command",
            f"{sys.executable} scripts/generation_oracle_agent.py",
        ],
    )
    run_step(
        "Paired comparison self-test",
        [sys.executable, "scripts/run_paired_eval.py", "--self-test"],
    )
    run_step(
        "Paired comparison judge adapter",
        [
            sys.executable,
            "scripts/run_paired_eval.py",
            "--fixture-arms",
            "separating",
            "--judge-command",
            f"{sys.executable} scripts/paired_eval_oracle_agent.py",
        ],
    )
    run_step(
        "Rubric judge dry-run",
        [sys.executable, "scripts/run_rubric_judge.py", "--dry-run"],
    )

    tmp_dir = release_tmp_dir()
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    try:
        expected_output = tmp_dir / "rubric-judge-expected.jsonl"
        run_step(
            "Rubric judge parser self-test",
            [
                sys.executable,
                "scripts/run_rubric_judge.py",
                "--export-expected-output",
                str(expected_output),
                "--judge-output",
                str(expected_output),
            ],
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    oracle_command = f"{shlex.quote(sys.executable)} scripts/rubric_judge_oracle_agent.py"
    run_step(
        "External command oracle self-test",
        [
            sys.executable,
            "scripts/run_rubric_judge.py",
            "--judge-command",
            oracle_command,
        ],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run deterministic release validation: repository checks, rubric judge "
            "self-tests, external command oracle self-test, and version/tag sanity."
        )
    )
    parser.add_argument(
        "--tag-or-ref",
        help=(
            "Optional release tag/ref to validate. Accepted release forms are "
            "`v<version>` and `refs/tags/v<version>`."
        ),
    )
    parser.add_argument(
        "--version-only",
        action="store_true",
        help="Run only the version/tag sanity check.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tag_or_ref = args.tag_or_ref or os.environ.get("RELEASE_REF")

    validate_version_sanity(tag_or_ref)
    if not args.version_only:
        run_release_checks()

    print("\n[OK] Release validation passed.")


if __name__ == "__main__":
    main()
