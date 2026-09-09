#!/usr/bin/env python3
"""XD-10.01 — the stress matrix is linked to the UX contract as a receipt
(sherlock audit, XD-10).

The fix under test (references/scenario-format.md):
* an optional `Pressure:` receipt per scenario id — never a second scenario
  table;
* evidence classes planned/simulated/observed plus inherited approved
  assumptions, separated; migration invents no observed status;
* risk-based subset for a small change, declared full coverage for a large
  flow;
* interactive evidence matches the same states/viewports as visual compare;
* the migration and scope rules run as behaviour.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "scenario-format.md")

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


def t_receipt_not_second_table():
    d = flat()
    assert "`Pressure:` — the optional state-stress receipt (never a second table)" in d
    assert "state-stress-matrix.md" in d
    assert "the steps, states and expected results live once, in the scenario" in d


def t_evidence_classes_and_migration():
    d = flat()
    for cls in ("`planned`", "`simulated`", "`observed`", "`inherited`"):
        assert cls in d, f"evidence class {cls} missing"
    assert "Migration invents nothing" in d
    assert "never as `observed`" in d


def t_scope_follows_risk():
    d = flat()
    assert "risk-based SUBSET" in d
    assert "coverage: full" in d
    assert "Demanding all product states for a one-line polish is how receipts stop being written." in d


def t_interactive_matches_visual():
    d = flat()
    assert "Interactive evidence matches visual evidence." in d
    assert "SAME state and viewport" in d
    assert "two half-receipts" in d


# ---- behaviour


def migrate(rows):
    """Old scenario rows → receipt rows; nothing becomes observed."""
    out = []
    for r in rows:
        cls = r.get("evidence")
        if cls not in ("simulated", "observed"):
            cls = "inherited" if r.get("approved_assumption") else "planned"
        if cls == "observed" and not r.get("render_seen"):
            cls = "planned"                       # an unproven observed is refused
        out.append({"state": r["state"], "evidence": cls})
    return out


def required_states(change, taxonomy):
    if change["size"] == "small":
        return sorted(change["affected"])          # risk-based subset
    return sorted(taxonomy)                        # full coverage


def t_migration_fixture():
    rows = migrate([
        {"state": "empty-first-use"},                                   # unmarked
        {"state": "loading", "approved_assumption": True},              # inherited
        {"state": "error", "evidence": "observed"},                     # claimed, unproven
        {"state": "success", "evidence": "observed", "render_seen": True},
    ])
    by = {r["state"]: r["evidence"] for r in rows}
    assert by["empty-first-use"] == "planned"
    assert by["loading"] == "inherited"
    assert by["error"] == "planned", "an invented observed survived migration"
    assert by["success"] == "observed"


def t_scope_fixture():
    taxonomy = ["first-use", "cleared", "no-results", "error-empty",
                "loading", "drafts", "retry", "cancel", "concurrent"]
    small = required_states({"size": "small", "affected": ["loading", "first-use"]},
                            taxonomy)
    assert small == ["first-use", "loading"], \
        "a visual polish was billed for every product state"
    big = required_states({"size": "large-flow", "affected": []}, taxonomy)
    assert big == sorted(taxonomy), "a large flow escaped full coverage"


def t_viewport_fixture():
    def receipt_whole(visual, trace):
        return visual["state"] == trace["state"] and visual["viewport"] == trace["viewport"]
    assert not receipt_whole({"state": "error", "viewport": "mobile"},
                             {"state": "error", "viewport": "desktop"}), \
        "a cross-viewport pair counted as one receipt"
    assert receipt_whole({"state": "error", "viewport": "mobile"},
                         {"state": "error", "viewport": "mobile"})


def main():
    case("the receipt is not a second table", t_receipt_not_second_table)
    case("evidence classes separated; migration invents nothing",
         t_evidence_classes_and_migration)
    case("scope follows risk", t_scope_follows_risk)
    case("interactive evidence matches visual", t_interactive_matches_visual)
    case("fixture: migration produces no invented observed", t_migration_fixture)
    case("fixture: subset for polish, full for a flow", t_scope_fixture)
    case("fixture: a cross-viewport pair is two half-receipts", t_viewport_fixture)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
