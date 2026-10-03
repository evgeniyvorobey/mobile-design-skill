#!/usr/bin/env bash
#
# Install mobile-design-skill for Claude Code.
#
# --method link (default) keeps the skill live: the install is a small directory
# holding a generated wrapper SKILL.md whose references are ABSOLUTE paths into
# this clone, so `git pull` updates the content without reinstalling. It is not a
# symlink to the repo's wrapper: Claude Code hands the skill its unresolved
# directory and the Read tool resolves `..` lexically, so a symlinked wrapper's
# `../../../` references point outside the repository and nothing loads.
# --method copy builds a self-contained copy with paths rewritten to stay inside
# the installed directory.
# It also installs the companion mobile-design-judge agent used by
# /mobile-design-skill --judge when the host supports custom agents.
#
# Usage:
#   ./scripts/install.sh                          # global install (default)
#   ./scripts/install.sh --scope project --project-path /abs/path/to/project
#   (or run the script from inside the target project: /path/to/clone/scripts/install.sh --scope project)
#   ./scripts/install.sh --method copy            # self-contained copy instead of a live install
#   ./scripts/install.sh --uninstall              # remove a previous install
#   ./scripts/install.sh --status                 # show where the skill is installed
#   ./scripts/install.sh --help
#
# After install, invoke the skill in Claude Code with:
#   /mobile-design-skill
# Re-run the install after a `git pull` that changes .claude/skills/mobile-design-skill/SKILL.md
# or the judge agent, or after moving the clone.
#
# Requirements:
#   - bash 3.2+ (macOS default works)
#   - ln -s support for the judge agent symlink in --method link
#     Use --method copy on filesystems or OSes where symlinks are not available.
#
# Exit codes:
#   0 on success
#   1 on usage error, missing prerequisites, or a refused target
#   2 when removing an install that does not exist

set -euo pipefail

SKILL_NAME="mobile-design-skill"
AGENT_NAME="mobile-design-judge"
INSTALL_MARKER=".mobile-design-skill-install"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_REAL="$(cd "$REPO_ROOT" && pwd -P)"
SOURCE_WRAPPER="$REPO_ROOT/.claude/skills/$SKILL_NAME"
SOURCE_SKILL_MD="$SOURCE_WRAPPER/SKILL.md"
SOURCE_AGENT="$REPO_ROOT/.claude/agents/$AGENT_NAME.md"

SCOPE="global"
METHOD="link"
PROJECT_PATH="$(pwd)"
ACTION="install"

print_help() {
    sed -n '2,36p' "$0" | sed -e 's/^#//' -e 's/^ //'
}

describe_install() {
    local target="$1"
    if [[ -L "$target" ]]; then
        echo "  status:         legacy symlink -> $(readlink "$target") (re-run install.sh to replace it)"
    elif [[ -d "$target" && -f "$target/$INSTALL_MARKER" ]]; then
        local method source
        method="$(sed -n '1p' "$target/$INSTALL_MARKER")"
        source="$(sed -n '2p' "$target/$INSTALL_MARKER")"
        echo "  status:         $method install from $source"
    elif [[ -d "$target" && -f "$target/SKILL.md.canonical" ]]; then
        echo "  status:         directory (copy install)"
    elif [[ -e "$target" ]]; then
        echo "  status:         present, but not created by install.sh"
    else
        echo "  status:         not installed"
    fi
}

describe_agent() {
    local target="$1"
    if [[ -L "$target" ]]; then
        echo "  status:         symlink -> $(readlink "$target")"
    elif [[ -f "$target" ]]; then
        echo "  status:         file (copy install)"
    else
        echo "  status:         not installed"
    fi
}

print_status() {
    echo "Repo root:        $REPO_ROOT"
    echo "Source wrapper:   $SOURCE_WRAPPER"
    echo ""
    echo "Global install:   $HOME/.claude/skills/$SKILL_NAME"
    describe_install "$HOME/.claude/skills/$SKILL_NAME"
    echo ""
    echo "Project install:  $PROJECT_PATH/.claude/skills/$SKILL_NAME"
    describe_install "$PROJECT_PATH/.claude/skills/$SKILL_NAME"
    echo ""
    echo "Global agent:     $HOME/.claude/agents/$AGENT_NAME.md"
    describe_agent "$HOME/.claude/agents/$AGENT_NAME.md"
    echo ""
    echo "Project agent:    $PROJECT_PATH/.claude/agents/$AGENT_NAME.md"
    describe_agent "$PROJECT_PATH/.claude/agents/$AGENT_NAME.md"
}

fail() {
    echo "Error: $*" >&2
    exit 1
}

# Physical path of a location that may not exist yet: resolve the nearest existing
# ancestor and append the rest. Never follows the final component, so a symlink at the
# target is judged as a symlink, not as whatever it points at.
physical_path() {
    local path="$1" suffix=""
    while [[ ! -d "$path" ]]; do
        suffix="/$(basename "$path")$suffix"
        path="$(dirname "$path")"
    done
    echo "$(cd "$path" && pwd -P)$suffix"
}

# True when $1 is $2 or lies inside it.
is_within() {
    [[ "$1" == "$2" || "$1" == "$2/"* ]]
}

# A directory this script created: it carries the marker, or it is a pre-marker copy install.
is_our_install_dir() {
    [[ -f "$1/$INSTALL_MARKER" || -f "$1/SKILL.md.canonical" ]]
}

is_our_agent_file() {
    [[ -L "$1" ]] || grep -q "^name: $AGENT_NAME\$" "$1" 2>/dev/null
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --scope)
            [[ $# -ge 2 ]] || fail "--scope requires a value (global|project)"
            SCOPE="$2"
            shift 2
            ;;
        --method)
            [[ $# -ge 2 ]] || fail "--method requires a value (link|copy)"
            METHOD="$2"
            shift 2
            ;;
        --project-path)
            [[ $# -ge 2 ]] || fail "--project-path requires an absolute path"
            PROJECT_PATH="$2"
            shift 2
            ;;
        --uninstall)
            ACTION="uninstall"
            shift
            ;;
        --status)
            ACTION="status"
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            fail "Unknown argument: $1 (try --help)"
            ;;
    esac
done

case "$SCOPE" in
    global|project) ;;
    *) fail "--scope must be global or project (got: $SCOPE)" ;;
esac

case "$METHOD" in
    link|copy) ;;
    *) fail "--method must be link or copy (got: $METHOD)" ;;
esac

if [[ "$ACTION" == "status" ]]; then
    print_status
    exit 0
fi

[[ -f "$SOURCE_SKILL_MD" ]] || fail "Source wrapper not found at $SOURCE_SKILL_MD. Run from a cloned repo."
[[ -f "$SOURCE_AGENT" ]] || fail "Source judge agent not found at $SOURCE_AGENT. Run from a cloned repo."

case "$SCOPE" in
    global)
        TARGET_PARENT="$HOME/.claude/skills"
        AGENT_TARGET_PARENT="$HOME/.claude/agents"
        ;;
    project)
        [[ -d "$PROJECT_PATH" ]] || fail "--project-path does not exist: $PROJECT_PATH"
        [[ "$PROJECT_PATH" = /* ]] || PROJECT_PATH="$(cd "$PROJECT_PATH" && pwd)"
        TARGET_PARENT="$PROJECT_PATH/.claude/skills"
        AGENT_TARGET_PARENT="$PROJECT_PATH/.claude/agents"
        ;;
esac

TARGET_DIR="$TARGET_PARENT/$SKILL_NAME"
AGENT_TARGET="$AGENT_TARGET_PARENT/$AGENT_NAME.md"

# Refuse any target that is, contains, or sits inside this clone. Without this,
# `--scope project` run from the clone's root (where PROJECT_PATH defaults to) resolves
# the target to the repository's own wrapper and deletes it, and a clone placed at
# ~/.claude/skills/mobile-design-skill is deleted by the default global install.
TARGET_REAL="$(physical_path "$TARGET_PARENT")/$SKILL_NAME"
AGENT_REAL="$(physical_path "$AGENT_TARGET_PARENT")/$AGENT_NAME.md"
if is_within "$TARGET_REAL" "$REPO_REAL" || is_within "$REPO_REAL" "$TARGET_REAL" \
    || is_within "$AGENT_REAL" "$REPO_REAL"; then
    fail "Refusing to $ACTION at $TARGET_DIR: that is this clone ($REPO_REAL) or inside it.
To target a project, run the script from that project's directory, or pass
--project-path /absolute/path/to/project."
fi

if [[ "$ACTION" == "uninstall" ]]; then
    removed=0
    if [[ -L "$TARGET_DIR" ]]; then
        rm -f "$TARGET_DIR"
        echo "[OK] Removed $TARGET_DIR"
        removed=1
    elif [[ -d "$TARGET_DIR" ]]; then
        is_our_install_dir "$TARGET_DIR" \
            || fail "$TARGET_DIR was not created by install.sh (no $INSTALL_MARKER); not removing it."
        rm -rf "$TARGET_DIR"
        echo "[OK] Removed $TARGET_DIR"
        removed=1
    fi
    if [[ -L "$AGENT_TARGET" || -f "$AGENT_TARGET" ]]; then
        is_our_agent_file "$AGENT_TARGET" \
            || fail "$AGENT_TARGET is not the $AGENT_NAME agent; not removing it."
        rm -f "$AGENT_TARGET"
        echo "[OK] Removed $AGENT_TARGET"
        removed=1
    fi
    if [[ "$removed" == "1" ]]; then
        exit 0
    else
        echo "Nothing to remove at $TARGET_DIR or $AGENT_TARGET"
        exit 2
    fi
fi

mkdir -p "$TARGET_PARENT"
mkdir -p "$AGENT_TARGET_PARENT"

if [[ -L "$TARGET_DIR" ]]; then
    echo "Existing install at $TARGET_DIR — replacing"
    rm -f "$TARGET_DIR"
elif [[ -e "$TARGET_DIR" ]]; then
    is_our_install_dir "$TARGET_DIR" \
        || fail "$TARGET_DIR exists and was not created by install.sh; move it away first."
    echo "Existing install at $TARGET_DIR — replacing"
    rm -rf "$TARGET_DIR"
fi

if [[ -L "$AGENT_TARGET" || -e "$AGENT_TARGET" ]]; then
    is_our_agent_file "$AGENT_TARGET" \
        || fail "$AGENT_TARGET exists and is not the $AGENT_NAME agent; move it away first."
    echo "Existing judge agent at $AGENT_TARGET — replacing"
    rm -f "$AGENT_TARGET"
fi

# The wrapper's references are `${CLAUDE_SKILL_DIR}/../../../<path>`.
WRAPPER_PARENT_REF='${CLAUDE_SKILL_DIR}/\.\./\.\./\.\./'

case "$METHOD" in
    link)
        # Absolute paths into the clone: they resolve the same way whether the host
        # normalises `..` lexically or follows symlinks, and they stay live on `git pull`.
        repo_ref="$(printf '%s/' "$REPO_REAL" | sed -e 's/[\\|&]/\\&/g')"
        mkdir -p "$TARGET_DIR"
        sed -e "s|$WRAPPER_PARENT_REF|$repo_ref|g" "$SOURCE_SKILL_MD" > "$TARGET_DIR/SKILL.md"
        if [[ -f "$SOURCE_WRAPPER/logo.svg" ]]; then
            cp "$SOURCE_WRAPPER/logo.svg" "$TARGET_DIR/logo.svg"
        fi
        printf 'link\n%s\n' "$REPO_REAL" > "$TARGET_DIR/$INSTALL_MARKER"
        ln -s "$SOURCE_AGENT" "$AGENT_TARGET"
        echo "[OK] Installed $TARGET_DIR"
        echo "     wrapper references point into $REPO_REAL"
        echo "[OK] Symlinked $AGENT_TARGET"
        echo "     -> $SOURCE_AGENT"
        ;;
    copy)
        # For a self-contained copy install, inline the canonical SKILL.md and
        # supporting files into the wrapper so the ../../../ references in the
        # wrapper do not break.
        mkdir -p "$TARGET_DIR/skill" "$TARGET_DIR/docs" "$TARGET_DIR/examples" "$TARGET_DIR/scripts"
        cp "$REPO_ROOT/SKILL.md" "$TARGET_DIR/SKILL.md.canonical"
        cp -R "$REPO_ROOT/skill/." "$TARGET_DIR/skill/"
        cp -R "$REPO_ROOT/docs/." "$TARGET_DIR/docs/"
        # docs/ references examples/ throughout (rubric fixtures, calibration material);
        # without this the copy install degrades silently instead of failing.
        cp -R "$REPO_ROOT/examples/." "$TARGET_DIR/examples/"
        # docs/ names run_rubric_judge.py, run_paired_eval.py and run_baseline_gate.py.
        # Without scripts/ those references dangle in every copy install, and the
        # calibration harnesses cannot be run from an installed skill at all.
        cp -R "$REPO_ROOT/scripts/." "$TARGET_DIR/scripts/"
        if [[ -f "$SOURCE_WRAPPER/logo.svg" ]]; then
            cp "$SOURCE_WRAPPER/logo.svg" "$TARGET_DIR/logo.svg"
        fi
        # Replace the wrapper SKILL.md with one whose paths point to the inlined files.
        sed -e 's|${CLAUDE_SKILL_DIR}/../../../SKILL.md|${CLAUDE_SKILL_DIR}/SKILL.md.canonical|g' \
            -e 's|${CLAUDE_SKILL_DIR}/../../../skill/|${CLAUDE_SKILL_DIR}/skill/|g' \
            -e 's|${CLAUDE_SKILL_DIR}/../../../docs/|${CLAUDE_SKILL_DIR}/docs/|g' \
            -e 's|${CLAUDE_SKILL_DIR}/../../../examples/|${CLAUDE_SKILL_DIR}/examples/|g' \
            -e 's|${CLAUDE_SKILL_DIR}/../../../scripts/|${CLAUDE_SKILL_DIR}/scripts/|g' \
            "$SOURCE_SKILL_MD" > "$TARGET_DIR/SKILL.md"
        printf 'copy\n%s\n' "$REPO_REAL" > "$TARGET_DIR/$INSTALL_MARKER"
        cp "$SOURCE_AGENT" "$AGENT_TARGET"
        echo "[OK] Copied self-contained skill to $TARGET_DIR"
        echo "[OK] Copied judge agent to $AGENT_TARGET"
        ;;
esac

echo ""
echo "Next steps:"
echo "  1. Open Claude Code in any project."
echo "  2. Run: /$SKILL_NAME"
echo "  3. Or pass a task inline: /$SKILL_NAME review this Android settings screen"
echo "  4. For judged mode: /$SKILL_NAME --judge create a fitness tracker dashboard"
echo ""
echo "To update later:   cd $REPO_ROOT && git pull   (re-run this script if the wrapper or judge agent changed)"
echo "To uninstall:      $SCRIPT_DIR/install.sh --uninstall --scope $SCOPE"
