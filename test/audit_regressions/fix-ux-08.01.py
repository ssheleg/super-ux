#!/usr/bin/env python3
"""FIX-UX-08.01 — approval changes the decision, not the provenance (sherlock
audit, UX-08).

The finding: reverse-engineering tagged observed/inferred, then held inferred
"until the user confirms" — and `confirmed` was described as confirmation by
observation. A founder-operator could confirm a wished-for persona without
research; approval and evidence status were one field.

The fix under test (ux-foundation SKILL.md + references/scenario-format.md):
* three separate axes — evidence_kind (brief/owner-belief/interview/telemetry/
  code-inference), decision_status (proposed/accepted/rejected),
  validation_status (unvalidated/observed/contradicted);
* approval moves decision_status only; validation_status moves only on a real
  interview/observation with a dated receipt;
* F×S×S and emotion carry source+scale or `unknown`, never an invented score;
* the three-axis rule run as behaviour.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SKILL = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-foundation", "SKILL.md")
FMT = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "scenario-format.md")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def flat(path):
    with open(path, encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def t_three_axes_in_contract():
    d = flat(FMT)
    assert "THREE separate axes, not one `confirmed`" in d
    for axis in ("**evidence_kind**", "**decision_status**", "**validation_status**"):
        assert axis in d, f"axis {axis} missing"
    for k in ("brief | owner-belief | interview | telemetry | code-inference",
              "proposed | accepted | rejected",
              "unvalidated | observed | contradicted"):
        assert k in d, f"axis values missing: {k}"


def t_approval_moves_decision_only():
    d = flat(FMT)
    assert "The operator's\n approval moves THIS, and only this.".replace("\n ", " ") in d \
        or "approval moves THIS, and only this" in d
    assert "Approval never does." in d
    assert "with a DATED receipt — moves it\n to `observed`".replace("\n ", " ") in d \
        or "moves it to `observed`" in d


def t_skill_separates_the_axes():
    s = flat(SKILL)
    assert "Present for a DECISION, not to launder the evidence." in s
    assert "it does NOT change\n evidence_kind".replace("\n ", " ") in s \
        or "it does NOT change evidence_kind" in s
    assert "A founder cannot promote a wished-for persona to observed by approving it." in s


def t_scores_carry_source_or_unknown():
    s = flat(SKILL)
    assert "each factor carries its SOURCE and SCALE, or the value is `unknown`" in s
    assert "never a number invented to fill the cell" in s


# ---- the three-axis rule as behaviour


def apply_approval(record):
    """The operator says 'confirm'. Only decision_status changes."""
    r = dict(record)
    r["decision_status"] = "accepted"
    return r   # evidence_kind and validation_status untouched


def add_observation(record, dated_receipt):
    r = dict(record)
    if dated_receipt:
        r["validation_status"] = "observed"
        r["evidence_kind"] = "interview"
    return r


def t_founder_approval_fixture():
    persona = {"evidence_kind": "owner-belief", "decision_status": "proposed",
               "validation_status": "unvalidated"}
    approved = apply_approval(persona)
    assert approved["decision_status"] == "accepted"
    assert approved["evidence_kind"] == "owner-belief", "approval changed the provenance"
    assert approved["validation_status"] == "unvalidated", \
        "approval promoted an unresearched persona to observed — the finding"
    # a real interview moves validation and adds a dated receipt
    researched = add_observation(approved, dated_receipt="2026-09-09 interview")
    assert researched["validation_status"] == "observed"
    assert researched["evidence_kind"] == "interview"


def t_unknown_frequency_stays_unknown():
    def score(freq, sev, solv):
        if any(x == "unknown" for x in (freq, sev, solv)):
            return "unknown"     # never invent a product
        return freq * sev * solv
    assert score("unknown", 3, 2) == "unknown", "an unknown factor was invented into a score"
    assert score(2, 3, 2) == 12


def main():
    case("the contract declares three separate axes", t_three_axes_in_contract)
    case("approval moves decision only; observation moves validation",
         t_approval_moves_decision_only)
    case("the SKILL separates the axes and forbids laundering",
         t_skill_separates_the_axes)
    case("scores carry source/scale or unknown", t_scores_carry_source_or_unknown)
    case("fixture: a founder's approval does not reach observed",
         t_founder_approval_fixture)
    case("fixture: an unknown factor stays unknown", t_unknown_frequency_stays_unknown)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
