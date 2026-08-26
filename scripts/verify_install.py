#!/usr/bin/env python3
"""
Install the skill the way a user installs it, then read what got installed.

Every other check in this repository reads the repository. None of them has ever
looked at an install. The two are not the same tree: `install.sh --method copy`
inlines a subset of the repo next to a rewritten wrapper, so a reference that is
valid in the working copy can dangle in the thing a user actually loads --
`SKILL.md` named `scripts/run_rubric_judge.py` for four minor versions while the
copy install placed no `scripts/` directory at all.

This script performs a real install into a throwaway project directory, in both
methods, and asserts that every path either wrapper names resolves to a file that
is there. It runs no model and says nothing about design quality.

    python3 scripts/verify_install.py
    python3 scripts/verify_install.py --keep    # leave the temp install for inspection
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL_SH = ROOT / "scripts" / "install.sh"
SKILL_NAME = "mobile-design-skill"
AGENT_NAME = "mobile-design-judge"

# `${CLAUDE_SKILL_DIR}/<path>` as the wrappers write it.
SKILL_DIR_REF_RE = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/([A-Za-z0-9_./-]+)")
# Backticked repo-relative paths in the canonical entrypoint. A trailing slash means
# a directory reference, which must resolve to a directory that is not empty.
CANONICAL_REF_RE = re.compile(r"`((?:docs|skill|examples|scripts)/[A-Za-z0-9_./-]*)`")


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def run_install(project: Path, method: str) -> None:
    result = subprocess.run(
        [
            "bash",
            str(INSTALL_SH),
            "--method",
            method,
            "--scope",
            "project",
            "--project-path",
            str(project),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail(
            f"install.sh --method {method} exited {result.returncode}\n"
            f"{result.stdout}\n{result.stderr}"
        )


def check_reference(base: Path, reference: str, source: str, errors: list[str]) -> None:
    target = (base / reference).resolve()
    if reference.endswith("/"):
        if not target.is_dir():
            errors.append(f"{source}: `{reference}` is not a directory in the install ({target})")
        elif not any(target.iterdir()):
            errors.append(f"{source}: `{reference}` is an empty directory in the install")
        return
    if not target.is_file():
        errors.append(f"{source}: `{reference}` does not exist in the install ({target})")


def verify_copy_install(project: Path) -> list[str]:
    errors: list[str] = []
    installed = project / ".claude" / "skills" / SKILL_NAME
    wrapper = installed / "SKILL.md"
    canonical = installed / "SKILL.md.canonical"

    if not wrapper.is_file():
        return [f"copy install: no wrapper at {wrapper}"]
    if not canonical.is_file():
        errors.append(f"copy install: no inlined canonical entrypoint at {canonical}")

    wrapper_text = wrapper.read_text(encoding="utf-8")
    if "../../../" in wrapper_text:
        errors.append(
            "copy install: the wrapper still contains `../../../` references. A copy install "
            "has no repository above it, so every one of those resolves outside the skill"
        )
    for reference in sorted(set(SKILL_DIR_REF_RE.findall(wrapper_text))):
        check_reference(installed, reference, "copy install wrapper", errors)

    if canonical.is_file():
        for reference in sorted(set(CANONICAL_REF_RE.findall(canonical.read_text(encoding="utf-8")))):
            check_reference(installed, reference, "copy install SKILL.md.canonical", errors)

    agent = project / ".claude" / "agents" / f"{AGENT_NAME}.md"
    if not agent.is_file():
        errors.append(f"copy install: judge agent missing at {agent}")

    return errors


def verify_link_install(project: Path) -> list[str]:
    errors: list[str] = []
    installed = project / ".claude" / "skills" / SKILL_NAME
    if not installed.is_symlink():
        errors.append(f"link install: {installed} is not a symlink")
    wrapper = installed / "SKILL.md"
    if not wrapper.is_file():
        return errors + [f"link install: no wrapper at {wrapper}"]

    # `${CLAUDE_SKILL_DIR}` is the directory the wrapper lives in, which for a symlink
    # install is the repository's own wrapper directory.
    base = installed.resolve()
    for reference in sorted(set(SKILL_DIR_REF_RE.findall(wrapper.read_text(encoding="utf-8")))):
        check_reference(base, reference, "link install wrapper", errors)

    agent = project / ".claude" / "agents" / f"{AGENT_NAME}.md"
    if not (agent.is_file() or agent.is_symlink()):
        errors.append(f"link install: judge agent missing at {agent}")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", action="store_true", help="do not delete the temporary install")
    args = parser.parse_args()

    workdir = Path(tempfile.mkdtemp(prefix="mobile-design-skill-install-"))
    errors: list[str] = []
    try:
        for method, verify in (("copy", verify_copy_install), ("link", verify_link_install)):
            project = workdir / method
            project.mkdir(parents=True, exist_ok=True)
            print(f"\n== {method} install into {project} ==", flush=True)
            run_install(project, method)
            method_errors = verify(project)
            if method_errors:
                errors.extend(method_errors)
                print(f"[FAIL] {method} install: {len(method_errors)} broken reference(s)")
            else:
                print(f"[OK] {method} install: every referenced path resolves")
    finally:
        if args.keep:
            print(f"\nTemporary install left at {workdir}")
        else:
            shutil.rmtree(workdir, ignore_errors=True)

    if errors:
        fail("Install verification failed:\n" + "\n".join(f"  - {e}" for e in errors))

    print("\n[OK] Both install methods produce a skill whose every reference resolves.")


if __name__ == "__main__":
    main()
