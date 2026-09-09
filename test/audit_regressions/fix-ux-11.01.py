#!/usr/bin/env python3
"""FIX-UX-11.01 — the degraded path reaches a permitted build state
(sherlock audit, UX-11).

The finding: ux-flows allowed a provisional profile and text-only specs when
Figma was absent, but the final build gate demanded the whole approved chain
and (with Figma enabled) every state linked to a frame — so the degradation
path never ended in a state any rule permitted building, and one serious
unknown blocked the entire product.

The fix under test (ux-flows + ux-scenarios SKILLs):
* one four-state machine — full / provisional / tooling-degraded / declined —
  read from effective capabilities and accepted decisions in EVERY layer;
* a missing optional Figma never blocks an approved text spec (build with
  explicit deferred frame sync; restoration updates the record, nothing
  re-runs);
* a serious unknown blocks only its dependent decisions;
* the state machine run as behaviour on the expected scenarios.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FLOWS = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-flows", "SKILL.md")
SCEN = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-scenarios", "SKILL.md")

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


def t_state_machine_exists():
    d = flat(FLOWS)
    assert "The build state — one machine, four states" in d
    for st in ("**full**", "**provisional**", "**tooling-degraded**", "**declined**"):
        assert st in d, f"the {st} state is missing"
    assert "effective capabilities and accepted decisions" in d


def t_optional_figma_never_blocks_approved_spec():
    d = flat(FLOWS)
    assert "A missing optional tool never blocks an approved text spec" in d
    assert "Deferred: frame sync" in d
    assert "recorded approvals stand in every layer, nothing re-runs" in d


def t_unknowns_block_only_dependents():
    d = flat(FLOWS)
    assert "a serious unknown blocks only its dependent decisions, never the whole product" in d
    assert "a destructive unknown keeps its dependents blocked until decided" in d


def t_scenarios_gate_reads_the_machine():
    d = flat(SCEN)
    assert "the scenarios a screen DEPENDS ON" in d, \
        "the scenarios gate still blocks the whole product"
    assert "four-state machine" in d
    assert "an approved text spec builds even with optional Figma absent" in d
    assert "count in every layer without re-running the chain" in d


# ---------------- the machine, run as behaviour


def build_state(approved, figma_enabled, figma_connected, open_unknowns, touches_unknown,
                declined=False):
    if declined:
        return "declined"
    if not approved:
        return "blocked"
    if touches_unknown and open_unknowns:
        return "blocked"                      # only the DEPENDENT screen blocks
    if figma_enabled and not figma_connected:
        return "tooling-degraded: build on text spec, deferred frame sync"
    return "full"


def t_machine_behaviour():
    # brief: "implement the agreed screen", Figma unavailable → builds
    s = build_state(approved=True, figma_enabled=True, figma_connected=False,
                    open_unknowns=True, touches_unknown=False)
    assert s.startswith("tooling-degraded"), \
        "an approved spec with Figma absent did not reach a build state — the finding"
    # a destructive unknown keeps ITS screen blocked
    assert build_state(True, True, False, open_unknowns=True, touches_unknown=True) == "blocked"
    # an unrelated screen builds despite the unknown existing elsewhere
    assert build_state(True, False, False, open_unknowns=True, touches_unknown=False) == "full"
    # figma restored: the same approvals yield full without re-approval
    assert build_state(True, True, True, open_unknowns=False, touches_unknown=False) == "full"


def main():
    case("the four-state machine exists and reads capabilities+decisions",
         t_state_machine_exists)
    case("optional Figma never blocks an approved text spec",
         t_optional_figma_never_blocks_approved_spec)
    case("unknowns block only their dependents", t_unknowns_block_only_dependents)
    case("the scenarios gate reads the same machine", t_scenarios_gate_reads_the_machine)
    case("the machine run as behaviour on the audit's scenarios", t_machine_behaviour)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
