#!/usr/bin/env python3
"""FIX-UX-10.01 — loading fills a real delay; it never stages a computation
(sherlock audit, UX-10).

The finding: funnel-research.md's step table defined Loading as "a calculated
pause that makes the result feel computed for this person", and the SKILL
mandated the loading screen as a step — extending BP-005 (which fills an
EXISTING delay) into a manufactured one that fakes personal analysis.

The fix under test (three docs + the decision run as behaviour):
* the funnel table's Loading row requires REAL asynchronous work, shows the
  actual operation, never delays a ready result, and names a narrative pause
  honestly (no false analysis claim, cost measured);
* BP-005 gains the Don't (never manufacture, never hold back, no false
  claims); the SKILL scopes the loading screen to a real wait;
* instant local result → no timer; slow op → real pending; missing-answer
  branch → honest empty state, no fake personalization.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BASE = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-flows")
FUNNEL = os.path.join(BASE, "references", "funnel-research.md")
BP = os.path.join(BASE, "references", "best-practices.md")
SKILL = os.path.join(BASE, "SKILL.md")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def flat(p):
    with open(p, encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def t_funnel_row_requires_real_work():
    d = flat(FUNNEL)
    assert "A calculated pause that makes the result feel computed" not in d, \
        "the staged-computation row survived — the finding itself"
    assert "REAL asynchronous work exists" in d
    assert "never delay a ready result" in d
    assert "no claim of personal analysis that is not happening" in d
    assert "measures its cost" in d


def t_missing_answer_branch_is_honest():
    d = flat(FUNNEL)
    assert "honest empty state, never a staged personalization over answers nobody gave" in d
    assert "An instant local result renders without a timer" in d


def t_bp005_has_the_dont():
    d = flat(BP)
    assert "manufacture the wait" in d, "BP-005 lost its Don't"
    assert "never holds a ready result back" in d
    assert '"analyzing your answers…" over a lookup table is a false claim' in d
    assert "a real loading/preparation moment exists" in d, \
        "Apply-when no longer requires a real moment"


def t_skill_scopes_the_loading_step():
    d = flat(SKILL)
    assert "where a real wait exists — never a manufactured one" in d, \
        "the SKILL still mandates a loading screen unconditionally"


# ---------------- the decision, run as behaviour


def render(result_ready_ms, real_async, claims_analysis, analysis_happens):
    """The doctrine as a function: what the screen may show."""
    if claims_analysis and not analysis_happens:
        return "REFUSED: false analysis claim"
    if result_ready_ms == 0 and not real_async:
        return "result"                      # instant local result: no timer
    if real_async:
        return "pending(actual operation)"
    return "REFUSED: manufactured delay"


def t_decision_behaviour():
    assert render(0, False, False, False) == "result", "an instant result got a timer"
    assert render(0, True, False, False).startswith("pending"), \
        "a real slow operation shows no pending"
    assert "REFUSED" in render(0, False, True, False), "a false analysis claim passed"
    assert "REFUSED" in render(500, False, False, False) or \
           render(500, False, False, False) == "REFUSED: manufactured delay", \
        "a delay with no async work was staged"
    assert render(0, True, True, True).startswith("pending"), \
        "an honest analysis claim over real analysis was refused"


def main():
    case("the funnel row requires real async work, honest narrative pause",
         t_funnel_row_requires_real_work)
    case("the missing-answer branch is honest; instant results show no timer",
         t_missing_answer_branch_is_honest)
    case("BP-005 carries the Don't", t_bp005_has_the_dont)
    case("the SKILL scopes the loading step to a real wait", t_skill_scopes_the_loading_step)
    case("the decision run as behaviour", t_decision_behaviour)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
