#!/usr/bin/env python3
"""ADOPT-M-08.01 — comparing behavioural concepts (sherlock audit).

The adoption, in ux-flows' diverge-before-converging rule: criteria and hard
constraints are fixed BEFORE the options exist; the options must differ in
behaviour a user could tell apart; only OPEN choices are compared (an accepted
structure is not re-opened by a fresh fork); a rejected option keeps why /
locator / revisit-condition; and the record is the whole ceremony — no
mandatory extra approval for having compared.

The comparison contract also runs as behaviour over fixtures both ways.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SKILL = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-flows", "SKILL.md")

checks = 0
failures = []


def case(name, fn):
    global checks
    try:
        fn()
        checks += 1
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def t_doctrine_states_the_comparison_rules():
    flat = " ".join(open(SKILL, encoding="utf-8").read().split())
    for needle in ("Criteria and hard constraints are written BEFORE the options exist",
                   "or the winner writes the rubric",
                   "behaviour a user could tell apart",
                   "not two wordings of one flow",
                   "an accepted structure is not re-opened",
                   "**why** it lost", "a locator: file, frame or commit",
                   "the revisit condition",
                   "no extra approval step is added for having compared"):
        assert needle in flat, f"the doctrine no longer states {needle!r}"


# --------------------- the comparison contract, run as behaviour


def compare(options, criteria_fixed, structure_accepted=False):
    """The documented rules. Returns violations; an empty list means the
    comparison may proceed and its record is complete."""
    out = []
    if not criteria_fixed:
        out.append("criteria written after the options — the winner wrote the rubric")
    if structure_accepted:
        out.append("the structure is accepted — a fresh fork does not reopen it")
    if len(options) >= 2 and all(o.get("behavior") == options[0].get("behavior")
                                 for o in options):
        out.append("the options share one behaviour — two wordings of one flow")
    for o in options:
        if o.get("rejected"):
            for field in ("why", "locator", "revisit"):
                if not o.get(field):
                    out.append(f"rejected option lost its {field}")
    return out


def t_discriminating_behavior_required():
    same = [{"behavior": "wizard"}, {"behavior": "wizard"}]
    v = compare(same, criteria_fixed=True)
    assert any("one behaviour" in x for x in v), f"two skins of one flow passed: {v}"
    different = [{"behavior": "wizard"}, {"behavior": "single-page-with-inline-recovery"}]
    assert compare(different, criteria_fixed=True) == []


def t_rejected_option_keeps_its_three_fields():
    full = [{"behavior": "a"},
            {"behavior": "b", "rejected": True, "why": "worse recovery path",
             "locator": "figma frame F-12", "revisit": "if support tickets on step 3 exceed 5%"}]
    assert compare(full, criteria_fixed=True) == []
    for dropped in ("why", "locator", "revisit"):
        opts = [{"behavior": "a"},
                {"behavior": "b", "rejected": True, "why": "x", "locator": "y", "revisit": "z"}]
        del opts[1][dropped]
        v = compare(opts, criteria_fixed=True)
        assert any(dropped in x for x in v), f"a rejected option without {dropped} passed: {v}"


def t_criteria_first_and_no_reopening():
    v = compare([{"behavior": "a"}, {"behavior": "b"}], criteria_fixed=False)
    assert any("rubric" in x for x in v), f"post-hoc criteria passed: {v}"
    v2 = compare([{"behavior": "a"}, {"behavior": "b"}], criteria_fixed=True,
                 structure_accepted=True)
    assert any("does not reopen" in x for x in v2), f"an accepted structure was reopened: {v2}"


def t_no_extra_approval_mandated():
    flat = " ".join(open(SKILL, encoding="utf-8").read().split())
    assert "no extra approval step is added" in flat
    # and the contract itself adds none: a clean comparison returns [] — proceed
    assert compare([{"behavior": "a"}, {"behavior": "b"}], criteria_fixed=True) == []


def main():
    case("the doctrine states the comparison rules", t_doctrine_states_the_comparison_rules)
    case("options must have discriminating behaviour", t_discriminating_behavior_required)
    case("a rejected option keeps why/locator/revisit", t_rejected_option_keeps_its_three_fields)
    case("criteria come first; accepted structures stay closed", t_criteria_first_and_no_reopening)
    case("no mandatory extra approval", t_no_extra_approval_mandated)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
