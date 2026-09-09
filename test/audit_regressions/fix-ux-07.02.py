#!/usr/bin/env python3
"""FIX-UX-07.02 — the linter matches required IDs, not literal heading language,
and a duplicate ID FAILs (sherlock audit, UX-07, second leaf).

The fix under test (scripts/ux_lint.py):
* section identity is the NUMBER (from 07.01) — changing a title's language
  does not change identity;
* a DUPLICATE section id (two `## N.` headings) FAILs with U034, rather than
  the parser silently resolving to the first;
* old English-only headings still resolve by number (explicit migration is
  just renaming the title, never the number).

Standard library only.
"""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LINT = os.path.join(ROOT, "plugins", "super-ux", "scripts", "ux_lint.py")

_spec = importlib.util.spec_from_file_location("ux_lint", LINT)
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def vh(n):
    return f"{n}. {M.VISION_SECTION_TITLES[n]}"


def full_vision(overrides=None):
    overrides = overrides or {}
    lines = ["# P — Vision", "", "**Status:** approved", "**Last reviewed:** 2026-09-09", ""]
    for n in M.VISION_SECTION_IDS:
        lines.append(f"## {overrides.get(n, vh(n))}")
        lines.append("body")
    return "\n".join(lines) + "\n"


def run(vision):
    codes = []
    oe, ow = M.err, M.warn
    M.err = lambda m: codes.append(m)
    M.warn = lambda m: codes.append(m)
    try:
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, "docs", "ux"))
        with open(os.path.join(d, "CLAUDE.md"), "w") as fh:
            fh.write(getattr(M, "VISION_RULE_TEXT", M.VISION_RULE_HEADING))
        M.check_vision(Path(d) / "docs" / "ux", vision)
    finally:
        M.err, M.warn = oe, ow
    return [c.split("]")[0] + "]" for c in codes if c.startswith("[")]


def t_title_language_does_not_change_identity():
    ru = full_vision({6: "6. Анти-видение", 1: "1. Суть"})
    codes = run(ru)
    assert "[U030]" not in codes, f"a localized title broke section identity: {codes}"


def t_duplicate_id_fails():
    # inject a second `## 6.` heading
    dup = full_vision().replace("## 6. Anti-vision\nbody",
                                "## 6. Anti-vision\nbody\n## 6. Another Anti-vision\nmore")
    codes = run(dup)
    assert "[U034]" in codes, f"a duplicate section id did not FAIL: {codes}"


def t_no_false_duplicate_on_clean():
    codes = run(full_vision())
    assert "[U034]" not in codes, "a clean vision reported a false duplicate"
    assert "[U030]" not in codes


def t_old_english_headings_still_resolve():
    codes = run(full_vision())   # the seed-default English titles
    assert "[U030]" not in codes, "the old English headings stopped resolving"


def main():
    case("changing a title's language does not change identity",
         t_title_language_does_not_change_identity)
    case("a duplicate section id FAILs (U034)", t_duplicate_id_fails)
    case("a clean vision reports no false duplicate", t_no_false_duplicate_on_clean)
    case("old English headings still resolve by number", t_old_english_headings_still_resolve)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
