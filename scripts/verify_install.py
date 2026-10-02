#!/usr/bin/env python3
"""
Install the skill the way a user installs it, then read what got installed.

Every other check in this repository reads the repository. None of them has ever
looked at an install. The two are not the same tree: `install.sh --method copy`
inlines a subset of the repo next to a rewritten wrapper, so a reference that is
valid in the working copy can dangle in the thing a user actually loads --
`SKILL.md` named `scripts/run_rubric_judge.py` for four minor versions while the
copy install placed no `scripts/` directory at all.

References are resolved the way the host resolves them. Claude Code hands a skill
its unresolved directory as `${CLAUDE_SKILL_DIR}`, and its Read tool normalises `..`
lexically, without following symlinks. An earlier version of this check called
`Path.resolve()` first, which follows the symlink a link install used to be, so it
passed an install whose every reference pointed outside the repository.

This script performs a real install into a throwaway project directory, in both
methods, and asserts that every path either wrapper names resolves to a file that
is there. It also asserts that install.sh refuses targets that are this clone or
inside it, and refuses to remove a directory it did not create. It runs no model
and says nothing about design quality.

    python3 scripts/verify_install.py
    python3 scripts/verify_install.py --keep    # leave the temp install for inspection
"""
from __future__ import annotations

import argparse
import os
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
INSTALL_MARKER = ".mobile-design-skill-install"

# `${CLAUDE_SKILL_DIR}/<path>` as the wrappers write it.
SKILL_DIR_REF_RE = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/([A-Za-z0-9_./-]+)")
# Absolute paths a link-install wrapper writes into the clone.
ABSOLUTE_REF_RE = re.compile(r"`(/[^`\n]+)`")
# Backticked repo-relative paths in the canonical entrypoint. A trailing slash means
# a directory reference, which must resolve to a directory that is not empty.
CANONICAL_REF_RE = re.compile(r"`((?:docs|skill|examples|scripts)/[A-Za-z0-9_./-]*)`")


def fail(message: str) -> None:
    print(f"[FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def run_install(project: Path, method: str, install_sh: Path = INSTALL_SH, extra: list[str] | None = None,
                env: dict[str, str] | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    args = ["bash", str(install_sh), "--method", method, "--scope", "project", "--project-path", str(project)]
    return subprocess.run(args + (extra or []), capture_output=True, text=True, env=env, cwd=cwd)


def lexical(base: Path | str, reference: str) -> Path:
    """Resolve the way the host's Read tool does: join, then normalise `..` textually."""
    return Path(os.path.normpath(os.path.join(str(base), reference)))


def check_target(target: Path, reference: str, source: str, errors: list[str]) -> None:
    if reference.endswith("/"):
        if not target.is_dir():
            errors.append(f"{source}: `{reference}` is not a directory in the install ({target})")
        elif not any(target.iterdir()):
            errors.append(f"{source}: `{reference}` is an empty directory in the install")
        return
    if not target.is_file():
        errors.append(f"{source}: `{reference}` does not exist in the install ({target})")


def check_reference(base: Path, reference: str, source: str, errors: list[str]) -> None:
    check_target(lexical(base, reference), reference, source, errors)


def verify_copy_install(project: Path) -> list[str]:
    errors: list[str] = []
    installed = project / ".claude" / "skills" / SKILL_NAME
    wrapper = installed / "SKILL.md"
    canonical = installed / "SKILL.md.canonical"

    if not wrapper.is_file():
        return [f"copy install: no wrapper at {wrapper}"]
    if not canonical.is_file():
        errors.append(f"copy install: no inlined canonical entrypoint at {canonical}")
    if not (installed / INSTALL_MARKER).is_file():
        errors.append(f"copy install: no {INSTALL_MARKER} marker, so --uninstall would refuse it")

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
    if installed.is_symlink():
        errors.append(
            f"link install: {installed} is a symlink. The host does not resolve it before "
            "joining `..`, so a symlinked wrapper's relative references escape the repository"
        )
    if not (installed / INSTALL_MARKER).is_file():
        errors.append(f"link install: no {INSTALL_MARKER} marker, so --uninstall would refuse it")
    wrapper = installed / "SKILL.md"
    if not wrapper.is_file():
        return errors + [f"link install: no wrapper at {wrapper}"]

    wrapper_text = wrapper.read_text(encoding="utf-8")
    if "../" in wrapper_text:
        errors.append("link install: the wrapper still contains `../` references")
    # `${CLAUDE_SKILL_DIR}` is the unresolved install directory, exactly as the host passes it.
    for reference in sorted(set(SKILL_DIR_REF_RE.findall(wrapper_text))):
        check_reference(installed, reference, "link install wrapper", errors)
    # Absolute references into the clone. Other backticked absolute strings in the
    # wrapper (the `/mobile-design-skill` command itself) are not paths.
    clone_root = str(ROOT.resolve()) + "/"
    absolute = sorted({ref for ref in ABSOLUTE_REF_RE.findall(wrapper_text) if ref.startswith(clone_root)})
    if not absolute:
        errors.append(f"link install: the wrapper names no absolute paths into the clone at {clone_root}")
    for reference in absolute:
        check_target(lexical("/", reference), reference, "link install wrapper", errors)

    agent = project / ".claude" / "agents" / f"{AGENT_NAME}.md"
    if not (agent.is_file() or agent.is_symlink()):
        errors.append(f"link install: judge agent missing at {agent}")

    return errors


def minimal_clone(destination: Path) -> Path:
    """The files install.sh needs, so refusal tests never run against the real clone."""
    for relative in ("scripts/install.sh", f".claude/skills/{SKILL_NAME}/SKILL.md", f".claude/agents/{AGENT_NAME}.md"):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    return destination


def verify_refusals(workdir: Path) -> list[str]:
    errors: list[str] = []
    wrapper_rel = Path(".claude") / "skills" / SKILL_NAME / "SKILL.md"
    agent_rel = Path(".claude") / "agents" / f"{AGENT_NAME}.md"

    # 1. Project scope pointed at the clone itself: the README's old instruction.
    clone = minimal_clone(workdir / "self-target" / "clone")
    for action in ([], ["--uninstall"]):
        result = run_install(clone, "link", install_sh=clone / "scripts" / "install.sh", extra=action, cwd=clone)
        label = "uninstall" if action else "install"
        if result.returncode == 0:
            errors.append(f"refusal: project-scope {label} into the clone itself exited 0")
        if not (clone / wrapper_rel).is_file() or not (clone / agent_rel).is_file():
            errors.append(f"refusal: project-scope {label} into the clone deleted the shipped wrapper or agent")

    # 1b. A project directory inside the clone. Nothing exists there yet, so only the
    # within-the-clone guard can refuse it; without that guard the install litters the clone.
    inner = clone / "some-project"
    inner.mkdir(parents=True, exist_ok=True)
    result = run_install(inner, "link", install_sh=clone / "scripts" / "install.sh")
    if result.returncode == 0 or (inner / ".claude").exists():
        errors.append("refusal: project-scope install into a directory inside the clone was not refused")

    # 2. A clone placed where the global install goes, then the default global install.
    home = workdir / "self-target" / "home"
    placed = minimal_clone(home / ".claude" / "skills" / SKILL_NAME)
    env = dict(os.environ, HOME=str(home))
    result = subprocess.run(["bash", str(placed / "scripts" / "install.sh")], capture_output=True, text=True, env=env)
    if result.returncode == 0:
        errors.append("refusal: global install from a clone at ~/.claude/skills exited 0")
    if not (placed / wrapper_rel).is_file():
        errors.append("refusal: global install deleted a clone placed at ~/.claude/skills")

    # 3. Uninstall must not remove a directory install.sh did not create.
    foreign = workdir / "self-target" / "foreign-project"
    stray = foreign / ".claude" / "skills" / SKILL_NAME / "notes.txt"
    stray.parent.mkdir(parents=True, exist_ok=True)
    stray.write_text("not ours\n", encoding="utf-8")
    result = run_install(foreign, "link", extra=["--uninstall"])
    if result.returncode == 0 or not stray.is_file():
        errors.append("refusal: --uninstall removed a directory install.sh did not create")

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
            result = run_install(project, method)
            if result.returncode != 0:
                fail(f"install.sh --method {method} exited {result.returncode}\n{result.stdout}\n{result.stderr}")
            method_errors = verify(project)
            if method_errors:
                errors.extend(method_errors)
                print(f"[FAIL] {method} install: {len(method_errors)} problem(s)")
            else:
                print(f"[OK] {method} install: every referenced path resolves as the host resolves it")

        print("\n== install.sh refusals ==", flush=True)
        refusal_errors = verify_refusals(workdir)
        if refusal_errors:
            errors.extend(refusal_errors)
            print(f"[FAIL] refusals: {len(refusal_errors)} problem(s)")
        else:
            print("[OK] refusals: never installs into or deletes the clone, never removes a foreign directory")
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
