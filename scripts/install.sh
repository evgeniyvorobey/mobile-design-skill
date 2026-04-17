#!/usr/bin/env bash
#
# Install mobile-design-skill for Claude Code.
#
# The script creates a symlink from the Claude Code skills directory
# (global or project scope) to this repository's wrapper at
# .claude/skills/mobile-design-skill. The wrapper then resolves the
# canonical SKILL.md and supporting files via relative paths inside the repo.
#
# Usage:
#   ./scripts/install.sh                          # global install (default)
#   ./scripts/install.sh --scope project          # install into current project's .claude/
#   ./scripts/install.sh --scope project --project-path /abs/path
#   ./scripts/install.sh --method copy            # copy instead of symlink (self-contained)
#   ./scripts/install.sh --uninstall              # remove a previous install
#   ./scripts/install.sh --status                 # show where the skill is installed
#   ./scripts/install.sh --help
#
# After install, invoke the skill in Claude Code with:
#   /mobile-design-skill
#
# Requirements:
#   - bash 4+ (macOS default bash 3 works)
#   - ln -s support (symlinks) for --method link (default)
#     Use --method copy on filesystems or OSes where symlinks are not available.
#
# Exit codes:
#   0 on success
#   1 on usage error or missing prerequisites
#   2 when removing an install that does not exist

set -euo pipefail

SKILL_NAME="mobile-design-skill"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SOURCE_WRAPPER="$REPO_ROOT/.claude/skills/$SKILL_NAME"
SOURCE_SKILL_MD="$SOURCE_WRAPPER/SKILL.md"

SCOPE="global"
METHOD="link"
PROJECT_PATH="$(pwd)"
ACTION="install"

print_help() {
    sed -n '2,30p' "$0" | sed -e 's/^#//' -e 's/^ //'
}

print_status() {
    local global_target="$HOME/.claude/skills/$SKILL_NAME"
    local project_target="$PROJECT_PATH/.claude/skills/$SKILL_NAME"

    echo "Repo root:        $REPO_ROOT"
    echo "Source wrapper:   $SOURCE_WRAPPER"
    echo ""
    echo "Global install:   $global_target"
    if [[ -L "$global_target" ]]; then
        local target
        target="$(readlink "$global_target")"
        echo "  status:         symlink -> $target"
    elif [[ -d "$global_target" ]]; then
        echo "  status:         directory (copy install)"
    else
        echo "  status:         not installed"
    fi

    echo ""
    echo "Project install:  $project_target"
    if [[ -L "$project_target" ]]; then
        local target
        target="$(readlink "$project_target")"
        echo "  status:         symlink -> $target"
    elif [[ -d "$project_target" ]]; then
        echo "  status:         directory (copy install)"
    else
        echo "  status:         not installed"
    fi
}

fail() {
    echo "Error: $*" >&2
    exit 1
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

case "$SCOPE" in
    global)
        TARGET_PARENT="$HOME/.claude/skills"
        ;;
    project)
        [[ "$PROJECT_PATH" = /* ]] || PROJECT_PATH="$(cd "$PROJECT_PATH" && pwd)"
        TARGET_PARENT="$PROJECT_PATH/.claude/skills"
        ;;
esac

TARGET_DIR="$TARGET_PARENT/$SKILL_NAME"

if [[ "$ACTION" == "uninstall" ]]; then
    if [[ -L "$TARGET_DIR" || -d "$TARGET_DIR" ]]; then
        rm -rf "$TARGET_DIR"
        echo "[OK] Removed $TARGET_DIR"
        exit 0
    else
        echo "Nothing to remove at $TARGET_DIR"
        exit 2
    fi
fi

mkdir -p "$TARGET_PARENT"

if [[ -L "$TARGET_DIR" || -e "$TARGET_DIR" ]]; then
    echo "Existing install at $TARGET_DIR — replacing"
    rm -rf "$TARGET_DIR"
fi

case "$METHOD" in
    link)
        ln -s "$SOURCE_WRAPPER" "$TARGET_DIR"
        echo "[OK] Symlinked $TARGET_DIR"
        echo "     -> $SOURCE_WRAPPER"
        ;;
    copy)
        # For a self-contained copy install, inline the canonical SKILL.md and
        # supporting files into the wrapper so the ../../../ references in the
        # wrapper do not break.
        mkdir -p "$TARGET_DIR/skill" "$TARGET_DIR/docs"
        cp "$REPO_ROOT/SKILL.md" "$TARGET_DIR/SKILL.md.canonical"
        cp -R "$REPO_ROOT/skill/." "$TARGET_DIR/skill/"
        cp -R "$REPO_ROOT/docs/." "$TARGET_DIR/docs/"
        # Replace the wrapper SKILL.md with one whose paths point to the inlined files.
        sed -e 's|${CLAUDE_SKILL_DIR}/../../../SKILL.md|${CLAUDE_SKILL_DIR}/SKILL.md.canonical|g' \
            -e 's|${CLAUDE_SKILL_DIR}/../../../skill/|${CLAUDE_SKILL_DIR}/skill/|g' \
            -e 's|${CLAUDE_SKILL_DIR}/../../../docs/|${CLAUDE_SKILL_DIR}/docs/|g' \
            "$SOURCE_SKILL_MD" > "$TARGET_DIR/SKILL.md"
        echo "[OK] Copied self-contained skill to $TARGET_DIR"
        ;;
esac

echo ""
echo "Next steps:"
echo "  1. Open Claude Code in any project."
echo "  2. Run: /$SKILL_NAME"
echo "  3. Or pass a task inline: /$SKILL_NAME review this Android settings screen"
echo ""
echo "To update later:   cd $REPO_ROOT && git pull"
echo "To uninstall:      $SCRIPT_DIR/install.sh --uninstall --scope $SCOPE"
