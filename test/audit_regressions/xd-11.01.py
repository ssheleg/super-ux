#!/usr/bin/env python3
"""XD-11.01 — the copy state contract, without a new copy workflow (sherlock
audit, XD-11).

The fix under test (references/ui-copy.md):
* the state-message tuple — fact / preservation / action / consequence /
  forbidden claims;
* wording carries observed/hypothesis provenance; localization translates
  complete messages, never concatenated slots;
* the internal exception never reaches the UI; a legal/payment polish never
  changes meaning;
* copy never mints a state the scenario lacks;
* the tuple run as behaviour: an error may not promise retry/saved the
  scenario does not prove.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references", "ui-copy.md")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def flat():
    with open(DOC, encoding="utf-8") as fh:
        return " ".join(fh.read().split())


def t_tuple_slots():
    d = flat()
    assert "The state-message tuple" in d
    for slot in ("**fact**", "**preservation**", "**action**", "**consequence**",
                 "**forbidden claims**"):
        assert slot in d, f"slot {slot} missing"


def t_forbidden_claims_examples():
    d = flat()
    assert '"Try again" is a forbidden claim where the scenario has no retry path' in d
    assert "may not promise retry or safety the flow does not deliver" in d


def t_provenance_and_localization():
    d = flat()
    assert "**observed** in the running product, or **hypothesis** from the scenario" in d
    assert "localization translates the COMPLETE message" in d
    assert "which no grammar survives" in d


def t_exception_and_legal():
    d = flat()
    assert "never surface the internal exception itself" in d
    assert "may not change what the condition MEANS" in d


def t_copy_never_mints_states():
    d = flat()
    assert "Copy polishes states; it never mints them." in d
    assert "a new state is a scenario change first" in d


# ---- the tuple as behaviour


def lint_message(message, scenario):
    """Which forbidden claims the message makes against THIS scenario."""
    violations = []
    if "try again" in message.lower() and not scenario.get("retry_path"):
        violations.append("promises retry the scenario does not prove")
    if "saved" in message.lower() and not scenario.get("autosave"):
        violations.append("promises preservation the scenario does not prove")
    return violations


def t_error_cannot_promise_unproven():
    scenario = {"retry_path": False, "autosave": False}
    v = lint_message("We could not publish. Your changes are saved. Try again.",
                     scenario)
    assert len(v) == 2, f"unproven promises passed: {v}"
    proven = {"retry_path": True, "autosave": True}
    assert lint_message("We could not publish. Your changes are saved. Try again.",
                        proven) == []


def t_copy_edit_cannot_add_state():
    def copy_edit_allowed(scenario_states, edited_states):
        return set(edited_states) <= set(scenario_states)
    assert not copy_edit_allowed(["error", "empty"], ["error", "empty", "success"]), \
        "a copy edit minted a success state"
    assert copy_edit_allowed(["error", "empty"], ["error"])


def main():
    case("the five tuple slots are named", t_tuple_slots)
    case("forbidden claims carry the retry/saved examples", t_forbidden_claims_examples)
    case("provenance + complete-message localization", t_provenance_and_localization)
    case("no internal exception in UI; legal meaning untouched", t_exception_and_legal)
    case("copy never mints a state", t_copy_never_mints_states)
    case("fixture: an error cannot promise retry/saved unproven",
         t_error_cannot_promise_unproven)
    case("fixture: a copy edit cannot add a state", t_copy_edit_cannot_add_state)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
