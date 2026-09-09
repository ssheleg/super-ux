#!/usr/bin/env python3
"""FIX-UX-03.01 — the humanization contract is advisory (sherlock audit, UX-03).

The finding: SKILL.md says a marker count never gates, but ai-tells.md graded
text "reads as written by a person" / "decisive on its own" and had B060 ERROR
at three S1 markers — a verdict on authorship and a gate. A quote containing
`delve` / `needless to say` / `in conclusion` reproduced the error, and
`Humanization: off` with a reason changed nothing.

This is the DOCTRINE leaf (the code is FIX-UX-03.02). Under test:
* ai-tells.md — B060 WARNS, never errors, never gates; the grade is advisory,
  never a claim of authorship; a quote, a registered term and explicit `off`
  do not force a rewrite; brand bans are a separate user policy;
* copywriting SKILL.md — a number of markers does not prove authorship; the
  pass is advisory; quote/term/off never force a rewrite.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SKILL = os.path.join(ROOT, "plugins", "super-ux", "skills", "copywriting", "SKILL.md")
TELLS = os.path.join(ROOT, "plugins", "super-ux", "skills", "copywriting",
                     "references", "ai-tells.md")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def read(p):
    with open(p, encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def t_b060_is_advisory_not_a_gate():
    d = read(TELLS)
    assert "it WARNS, it never errors and never gates" in d, \
        "B060 still errors/gates in the reference"
    assert "errors at three S1" not in d, "the three-S1 error rule survived"


def t_grade_is_not_a_verdict_on_authorship():
    d = read(TELLS)
    assert "never a claim that a person or a machine wrote it" in d, \
        "the grade is still a verdict on authorship"
    assert "Reads as written by a person" not in d, "the authorship grade language survived"


def t_quote_term_off_do_not_force_rewrite():
    for path, name in ((TELLS, "ai-tells.md"), (SKILL, "SKILL.md")):
        d = read(path)
        assert "do NOT\nforce a rewrite".replace("\n", " ") in d or \
               "never force a rewrite" in d, f"{name}: quote/term/off can still force a rewrite"
        assert "Brand bans are a separate user\npolicy".replace("\n", " ") in d or \
               "Brand bans are a separate user policy" in d, \
            f"{name}: brand bans are not separated from AI-tells"


def t_markers_do_not_prove_authorship():
    for path, name in ((TELLS, "ai-tells.md"), (SKILL, "SKILL.md")):
        d = read(path)
        assert ("does not prove authorship" in d
                or "not a verdict on authorship" in d
                or "no more prove a machine wrote the text" in d), \
            f"{name}: a marker count is still treated as proof of authorship"


def t_off_preserves_text():
    d = read(TELLS)
    assert "`off` (with its\nrecorded reason) preserves the text exactly".replace("\n", " ") in d \
        or "preserves the text exactly" in d, "explicit off does not preserve the text"


def main():
    case("B060 is advisory — warns, never errors or gates", t_b060_is_advisory_not_a_gate)
    case("the naturalness grade is not a verdict on authorship",
         t_grade_is_not_a_verdict_on_authorship)
    case("a quote, a registered term and off never force a rewrite; brand bans separate",
         t_quote_term_off_do_not_force_rewrite)
    case("a number of markers does not prove authorship", t_markers_do_not_prove_authorship)
    case("explicit off preserves the text", t_off_preserves_text)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
