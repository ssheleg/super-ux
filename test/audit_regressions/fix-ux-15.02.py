#!/usr/bin/env python3
"""FIX-UX-15.02 — scenarios reference the policy decision; the frontend never
invents it (sherlock audit, UX-15, second leaf).

The fix under test (references/best-practices.md, BP-213):
* the UX scenario names the decided basis and regime; screens are checked
  against THAT decision;
* an undecided jurisdiction/basis is marked decision-needed and blocks the
  legal verdict — never guessed from the UI's shape;
* an informational acknowledgement ("Got it", dismissing a notice) is never
  recorded as consent;
* the rule run as behaviour on fixtures.

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


def t_policy_referenced_not_invented():
    d = flat()
    assert "The scenario REFERENCES the policy decision; the frontend implements it, never invents it" in d
    assert "checked against THAT decision" in d


def t_unknown_jurisdiction_is_decision_needed():
    d = flat()
    assert "marked **decision-needed**" in d
    assert "blocks that screen's legal verdict" in d
    assert "never guessed from the UI's shape" in d


def t_acknowledgement_is_not_consent():
    d = flat()
    assert "informational acknowledgement is not consent" in d
    assert "fabricated the one artifact an audit would ask for" in d


# ---- behaviour fixtures


def check_screen(scenario, ui_events):
    """scenario: {basis_decided, regime_decided}; ui_events: list of events.
    Returns the verdict the audit would give."""
    if not (scenario.get("basis_decided") and scenario.get("regime_decided")):
        return {"verdict": "decision-needed", "consent_recorded": False}
    consent = any(e == "affirmative-consent" for e in ui_events)
    return {"verdict": "checkable", "consent_recorded": consent}


def t_unknown_jurisdiction_fixture():
    v = check_screen({"basis_decided": "consent", "regime_decided": None},
                     ["affirmative-consent"])
    assert v["verdict"] == "decision-needed", \
        "an undecided regime still got a legal verdict"
    assert v["consent_recorded"] is False, \
        "consent was recorded under an undecided policy"


def t_acknowledgement_fixture():
    v = check_screen({"basis_decided": "consent", "regime_decided": "GDPR"},
                     ["notice-dismissed", "got-it-click"])
    assert v["consent_recorded"] is False, \
        "an informational acknowledgement was passed off as consent"
    v2 = check_screen({"basis_decided": "consent", "regime_decided": "GDPR"},
                      ["affirmative-consent"])
    assert v2["consent_recorded"] is True


def t_mirror_synced():
    assert flat() == flat(MIRROR), "ux-flows mirror drifted"


def main():
    case("the policy is referenced, never invented", t_policy_referenced_not_invented)
    case("an unknown jurisdiction is decision-needed", t_unknown_jurisdiction_is_decision_needed)
    case("an acknowledgement is not consent", t_acknowledgement_is_not_consent)
    case("fixture: undecided regime → decision-needed, no consent recorded",
         t_unknown_jurisdiction_fixture)
    case("fixture: 'Got it' is not recorded as consent; the affirmative act is",
         t_acknowledgement_fixture)
    case("the ux-flows mirror is synced", t_mirror_synced)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
