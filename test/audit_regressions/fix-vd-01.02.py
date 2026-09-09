#!/usr/bin/env python3
"""FIX-VD-01.02 — the provisional pack path (sherlock audit, VD-01).

The finding: the full 13-heading pack contract applied from the first sketch,
so an exploration that should hold two candidate identities collapsed into
one declared identity immediately.

The fix under test (super-ux references/visual-identity.md + sheleg-design
DESIGN_SYNC_BRIDGE.md):
* before a direction is chosen, sketches run on PROVISIONAL semantic tokens
  (roles + working values); two candidate identities are two provisional sets;
* the full 13-heading contract is a consolidation/publication gate — a first
  sketch is never blocked by it, a reusable pack still passes it;
* nothing provisional syncs across the bridge;
* the gate rule run as behaviour.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VI = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                  "visual-identity.md")
BRIDGE = os.path.expanduser(
    "~/DATA/sheleg-design-skill/plugins/sheleg-design/skills/sheleg-design/DESIGN_SYNC_BRIDGE.md")

failures = []
not_run = []


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


def t_provisional_path_exists():
    d = flat(VI)
    assert "**provisional semantic tokens**" in d
    assert "two candidate identities are two provisional token sets, not a contract violation" in d


def t_full_contract_at_consolidation():
    d = flat(VI)
    assert "applies when a direction is CHOSEN" in d
    assert "a first sketch is never blocked by thirteen headings" in d
    assert "a reusable pack still passes every one of them" in d
    assert "Free-styling one screen at a time remains the thing neither path allows." in d


def t_bridge_gate_is_publication_not_sketch():
    if not os.path.isfile(BRIDGE):
        not_run.append("sheleg-design checkout absent — bridge check NOT_RUN")
        return
    d = flat(BRIDGE)
    assert "publication gate, not a sketch gate" in d
    assert "nothing provisional syncs" in d
    assert "owed at the moment of consolidation" in d


# ---- behaviour


def gate(artifact):
    """artifact: {stage, headings, provisional}. Returns (allowed, blocked_by)."""
    if artifact["stage"] == "sketch":
        return (True, None) if artifact.get("provisional") else (True, None)
    if artifact["stage"] == "publish":
        if artifact.get("provisional"):
            return (False, "nothing provisional syncs")
        if artifact.get("headings", 0) < 13:
            return (False, "the full pack contract")
        return (True, None)
    return (False, "unknown stage")


def t_first_sketch_not_blocked():
    ok, why = gate({"stage": "sketch", "provisional": True, "headings": 0})
    assert ok, f"a first sketch was blocked: {why}"


def t_reusable_pack_still_gated():
    ok, why = gate({"stage": "publish", "provisional": False, "headings": 11})
    assert not ok and why == "the full pack contract", \
        "an 11-heading pack published"
    ok2, _ = gate({"stage": "publish", "provisional": False, "headings": 13})
    assert ok2, "a full pack was refused"
    ok3, why3 = gate({"stage": "publish", "provisional": True, "headings": 13})
    assert not ok3 and "provisional" in why3, "a provisional set synced"


def main():
    case("the provisional path exists with two-candidate wording",
         t_provisional_path_exists)
    case("the full contract lands at consolidation, sketches free",
         t_full_contract_at_consolidation)
    case("the bridge names publication-not-sketch and blocks provisional sync",
         t_bridge_gate_is_publication_not_sketch)
    case("fixture: a first sketch is not blocked", t_first_sketch_not_blocked)
    case("fixture: a reusable pack is still gated; provisional never syncs",
         t_reusable_pack_still_gated)
    for n in not_run:
        print(f"  NOT_RUN  {n}")
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
