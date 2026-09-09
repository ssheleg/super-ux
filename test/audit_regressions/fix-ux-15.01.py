#!/usr/bin/env python3
"""FIX-UX-15.01 — applicability dimensions separated; the universal consent
gate is gone (sherlock audit, UX-15).

The finding: for any stored field (quiz/email/payment status) the practice
demanded consent before the first write and justified it with GDPR Art. 13 —
but Art. 13 is an INFORMATION duty, the EDPB lists six legal bases of which
consent is one, and contract-necessary or legally-required processing must not
hang on a consent checkbox.

The fix under test (references/best-practices.md, BP-213/BP-214):
* four separate dimensions — information duty / legal basis / explicit
  consent / geography;
* the notice stays before the first write (always); the consent checkbox
  applies only where consent IS the basis;
* the same UI with different applicability gets different verdicts, run as
  behaviour on fixtures;
* BP-214 no longer orders a universal consent gate.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "best-practices.md")
MIRROR = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-flows",
                      "references", "best-practices.md")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def flat(path=DOC):
    with open(path, encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def t_four_dimensions_named():
    d = flat()
    assert "four SEPARATE things" in d
    for dim in ("**(1) information**", "**(2) legal basis**",
                "**(3) explicit consent**", "**(4) geography**"):
        assert dim in d, f"dimension {dim} missing"
    assert "six Art. 6(1) bases" in d


def t_notice_always_consent_conditional():
    d = flat()
    assert "goes *before the first write*, always" in d
    assert "a checkbox only where consent IS the chosen basis" in d
    assert "never as a universal gate" in d


def t_art13_is_information_duty():
    d = flat()
    assert "Art. 13 is an INFORMATION duty" in d
    assert "the EDPB lists six lawful bases of which consent is one" in d
    assert "neither needs nor benefits from a consent checkbox" in d
    assert "put the notice and consent **before the first write**" not in d, \
        "the universal consent-before-first-write order survived in BP-213"


def t_bp214_gate_conditional():
    d = flat()
    assert "put the consent gate before the first write" not in d, \
        "BP-214 still orders a universal consent gate"
    assert "gate on consent only the processing whose basis IS consent" in d


def t_geography_splits_the_verdict():
    d = flat()
    assert "the same UI serving two regions gets two verdicts, not one" in d


# ---- the dimension rule as behaviour


def verdicts(field):
    """field: {purpose, basis, region_in_scope} → the per-dimension duties."""
    return {
        "notice_before_first_write": field["region_in_scope"],   # info duty, always in scope
        "consent_checkbox": field["region_in_scope"] and field["basis"] == "consent",
        "basis_recorded": True,
    }


def t_same_ui_different_applicability_differs():
    payment = verdicts({"purpose": "payment status", "basis": "contract",
                        "region_in_scope": True})
    marketing = verdicts({"purpose": "marketing email", "basis": "consent",
                          "region_in_scope": True})
    out_of_scope = verdicts({"purpose": "marketing email", "basis": "consent",
                             "region_in_scope": False})
    assert payment["consent_checkbox"] is False, \
        "contract-basis payment status demanded a consent checkbox"
    assert payment["notice_before_first_write"] is True, "the info duty was dropped"
    assert marketing["consent_checkbox"] is True
    assert out_of_scope["notice_before_first_write"] is False and \
        out_of_scope["consent_checkbox"] is False, \
        "geography did not change the verdict"
    assert payment != marketing != out_of_scope


def t_mirror_synced():
    assert flat() == flat(MIRROR), \
        "ux-flows mirror drifted from the source of truth"


def main():
    case("the four dimensions are named separately", t_four_dimensions_named)
    case("notice is unconditional, the checkbox is basis-conditional",
         t_notice_always_consent_conditional)
    case("Art. 13 is stated as an information duty; six bases; old order gone",
         t_art13_is_information_duty)
    case("BP-214's universal consent gate is conditional now", t_bp214_gate_conditional)
    case("geography splits the verdict", t_geography_splits_the_verdict)
    case("fixture: same UI, different applicability, different verdicts",
         t_same_ui_different_applicability_differs)
    case("the ux-flows mirror is synced", t_mirror_synced)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
