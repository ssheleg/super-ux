#!/usr/bin/env python3
"""FIX-UX-07.01 — locale-independent section IDs (sherlock audit, UX-07).

The finding: the vision contract and the linter regex required nine literal
ENGLISH headings, so a Russian vision with semantically-equivalent sections
got U030.

The fix under test (ux_lint.py + scenario-format.md + vision/SKILL.md):
* a section's machine identity is its NUMBER; the title is localizable;
* a Russian vision with all nine numbered sections keeps all nine ids;
* a vision missing a section (e.g. anti-vision) still FAILs U030 whatever the
  language;
* the docs declare the convention and tell the author to read it.

Standard library only.
"""
import importlib.util
import io
import os
import sys
import contextlib

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LINT = os.path.join(ROOT, "plugins", "super-ux", "scripts", "ux_lint.py")
FMT = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "scenario-format.md")
VISION = os.path.join(ROOT, "plugins", "super-ux", "skills", "vision", "SKILL.md")

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


RU_FULL = """# Продукт — Видение

**Status:** approved
**Last reviewed:** 2026-09-09

## 1. Суть
essence text
## 2. Ключевая идея
idea
## 3. Что делает система
does
## 4. Роль пользователя
role
## 5. Принципы
principles
## 6. Анти-видение
what it will never be
## 7. Горизонт
horizon
## 8. Одно предложение
one sentence
## 9. Тест на согласованность
the test
"""


def run_check(vision_text):
    """Capture the U-codes check_vision emits for a vision string."""
    codes = []
    orig_err = M.err
    orig_warn = M.warn
    M.err = lambda msg: codes.append(("err", msg))
    M.warn = lambda msg: codes.append(("warn", msg))
    try:
        from pathlib import Path
        # check_vision(ux, vision); ux only used for the instruction-file path,
        # which emits U032 — give it a temp dir with a CLAUDE.md carrying the rule
        import tempfile
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, "docs", "ux"))
        os.makedirs(os.path.join(d, ".claude"))
        with open(os.path.join(d, "CLAUDE.md"), "w") as fh:
            fh.write(M.VISION_RULE_TEXT if hasattr(M, "VISION_RULE_TEXT") else
                     M.VISION_RULE_HEADING)
        M.check_vision(Path(d) / "docs" / "ux", vision_text)
    finally:
        M.err = orig_err
        M.warn = orig_warn
    return [m for _, m in codes]


def t_section_id_is_number():
    assert M.VISION_SECTION_IDS == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert callable(M._VSEC)


def t_russian_vision_keeps_all_nine():
    msgs = run_check(RU_FULL)
    u030 = [m for m in msgs if "[U030]" in m]
    assert u030 == [], f"a full Russian vision reported missing sections: {u030}"


def t_missing_anti_vision_fails_in_russian():
    # drop section 6
    partial = "\n".join(l for l in RU_FULL.splitlines()
                        if not l.startswith("## 6.") and l != "what it will never be")
    msgs = run_check(partial)
    assert any("[U030]" in m and "6." in m for m in msgs), \
        "a Russian vision missing anti-vision did not FAIL U030"


def t_docs_declare_the_convention():
    with open(FMT, encoding="utf-8") as fh:
        d = " ".join(fh.read().split())
    assert "the NUMBER is the section's machine\nidentity".replace("\n", " ") in d \
        or "the NUMBER is the section's machine identity" in d
    assert "Do not demand English prose for the parser's sake." in d
    assert "Анти-видение" in d
    with open(VISION, encoding="utf-8") as fh:
        v = " ".join(fh.read().split())
    assert "identified by their NUMBER, not their English\ntitle".replace("\n", " ") in v \
        or "identified by their NUMBER, not their English title" in v
    assert "read it before writing the vision" in v


def main():
    case("a section's identity is its number", t_section_id_is_number)
    case("a full Russian vision keeps all nine section ids",
         t_russian_vision_keeps_all_nine)
    case("a Russian vision missing anti-vision FAILs U030",
         t_missing_anti_vision_fails_in_russian)
    case("the docs declare the numeric-id convention and tell the author to read it",
         t_docs_declare_the_convention)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
