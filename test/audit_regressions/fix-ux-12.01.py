#!/usr/bin/env python3
"""FIX-UX-12.01 — a static PASS cannot promote a scenario to implemented
(sherlock audit, UX-12).

The finding: the audit loop checked "the expected result observably occurs"
against the CODE and flipped validated→implemented on a PASS — but a file:line
proves the implementation's TEXT, not that a user reaches the branch (an
overlay, auth, a network gate, CSS can hide it), and the live browser pass is
off by default.

The fix under test (ux-audit SKILL.md):
* three evidence tiers named (static conformance / executable verification /
  production observation); each step-3 criterion tagged STATIC or RUNTIME;
* a RUNTIME criterion PASSes only with a test / browser / runtime receipt,
  else BLOCKED (unverified), never invented when no browser exists;
* implemented is set only when every dependent RUNTIME criterion has runtime
  proof; a pure-static scenario may reach implemented with the proof type
  named; delivery-vs-Product separation kept;
* the promotion rule run as behaviour (the overlay-intercept fixture).

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-audit", "SKILL.md")

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


def t_three_tiers_named():
    d = flat()
    assert "Three evidence tiers" in d
    for tier in ("Static conformance", "executable verification", "production observation"):
        assert tier in d, f"the {tier} tier is missing"
    assert "a `file:line` proves the TEXT of an implementation, not that a user reaches it" in d


def t_criteria_tagged_and_runtime_needs_proof():
    d = flat()
    assert "is reachable BY A USER (RUNTIME" in d
    assert "handler that\n actually FIRES on the user's click (RUNTIME".replace("\n ", " ") in d \
        or "handler that actually FIRES on the user's click (RUNTIME" in d
    assert "the expected result observably occurs (RUNTIME)" in d
    assert "PASSes only with a test, a browser check, or a\n verified runtime receipt".replace("\n ", " ") in d \
        or "PASSes only with a test, a browser check, or a verified runtime receipt" in d
    assert "never invented when no browser is available" in d


def t_implemented_requires_runtime_proof():
    d = flat()
    assert "flip\n `validated` → `implemented` ONLY where every RUNTIME criterion".replace("\n ", " ") in d \
        or "flip `validated` → `implemented` ONLY where every RUNTIME criterion" in d
    assert "stays `validated` with those criteria BLOCKED" in d
    assert "all STATIC may reach `implemented`" in d
    # delivery-vs-Product separation kept
    assert "The audit never writes `Product:`." in d


# ---------------- the promotion rule, run as behaviour


def audit_scenario(criteria):
    """criteria: list of {tier, static_ok, runtime_proof}. Returns
    (verdict-per-criterion, may_promote)."""
    verdicts = {}
    for c in criteria:
        if c["tier"] == "static":
            verdicts[c["id"]] = "PASS" if c.get("static_ok") else "FAIL"
        else:  # runtime
            if c.get("runtime_proof"):
                verdicts[c["id"]] = "PASS"
            else:
                verdicts[c["id"]] = "BLOCKED"     # never PASS off code alone
    promote = all(v == "PASS" for v in verdicts.values())
    return verdicts, promote


def t_overlay_intercept_does_not_promote():
    # button + handler present (static), but an overlay eats the click (runtime,
    # no proof) → static-conformant, live would FAIL, implemented not set
    v, promote = audit_scenario([
        {"id": "element-exists", "tier": "static", "static_ok": True},
        {"id": "click-fires", "tier": "runtime", "runtime_proof": False},
    ])
    assert v["element-exists"] == "PASS"
    assert v["click-fires"] == "BLOCKED", "an overlay-intercepted click passed off file:line"
    assert promote is False, "implemented was set despite an unverified runtime criterion"


def t_pure_static_may_promote():
    v, promote = audit_scenario([
        {"id": "copy-present", "tier": "static", "static_ok": True},
    ])
    assert promote is True, "a pure-static scenario could not reach implemented"


def t_runtime_with_receipt_promotes():
    v, promote = audit_scenario([
        {"id": "element-exists", "tier": "static", "static_ok": True},
        {"id": "click-fires", "tier": "runtime", "runtime_proof": True},
    ])
    assert promote is True, "a runtime criterion with a receipt did not promote"


def main():
    case("the three evidence tiers are named", t_three_tiers_named)
    case("criteria are tagged; runtime needs test/browser/receipt, never invented",
         t_criteria_tagged_and_runtime_needs_proof)
    case("implemented requires runtime proof; static-only may promote; Product kept separate",
         t_implemented_requires_runtime_proof)
    case("an overlay-intercept fixture stays static-conformant, not implemented",
         t_overlay_intercept_does_not_promote)
    case("a pure-static scenario may promote", t_pure_static_may_promote)
    case("a runtime criterion with a receipt promotes", t_runtime_with_receipt_promotes)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
