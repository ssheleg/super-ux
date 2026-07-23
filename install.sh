#!/bin/sh
# super-ux installer: Cursor rules + docs/ux skeleton for a target project.
# Claude Code needs no installer — see usage below.
set -eu

SRC="$(cd "$(dirname "$0")" && pwd)"

usage() {
  cat <<'EOF'
super-ux installer

Usage:
  ./install.sh --cursor <project-dir> [--force]

Copies cursor/rules/*.mdc into <project-dir>/.cursor/rules/ and seeds
docs/ux/scenarios.md from templates/ if absent. An existing scenario base is
NEVER overwritten. Existing rule files are skipped unless --force is given.

Claude Code (no installer needed):
  /plugin marketplace add ssheleg/super-ux
  /plugin install super-ux@super-ux
EOF
}

[ $# -ge 1 ] || { usage; exit 0; }
[ "$1" = "--cursor" ] || { echo "error: unknown mode '$1'" >&2; usage; exit 1; }
[ $# -ge 2 ] || { echo "error: --cursor requires <project-dir>" >&2; exit 1; }

TARGET="$2"
FORCE=0
[ "${3:-}" = "--force" ] && FORCE=1

[ -d "$TARGET" ] || { echo "error: '$TARGET' is not a directory" >&2; exit 1; }

RULES_DIR="$TARGET/.cursor/rules"
mkdir -p "$RULES_DIR"

installed=0
skipped=0
for rule in "$SRC"/cursor/rules/*.mdc; do
  name="$(basename "$rule")"
  if [ -f "$RULES_DIR/$name" ] && [ "$FORCE" -ne 1 ]; then
    echo "skip:    $RULES_DIR/$name exists (use --force to overwrite)"
    skipped=$((skipped + 1))
  else
    cp "$rule" "$RULES_DIR/$name"
    echo "install: $RULES_DIR/$name"
    installed=$((installed + 1))
  fi
done

mkdir -p "$TARGET/docs/ux/audits"
for tpl in scenarios foundation flows screens; do
  if [ -f "$TARGET/docs/ux/$tpl.md" ]; then
    echo "keep:    $TARGET/docs/ux/$tpl.md exists (never overwritten)"
  else
    cp "$SRC/templates/$tpl.md" "$TARGET/docs/ux/$tpl.md"
    echo "seed:    $TARGET/docs/ux/$tpl.md"
  fi
done

echo "done: $installed installed, $skipped skipped"
