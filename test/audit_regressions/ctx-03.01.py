#!/usr/bin/env python3
"""CTX-03.01 — the bounded scenario graph (sherlock audit, parent CTX-03).

The contract under test, as behaviour against test/flow_graph.py: every
declared transition carries origin/action/result; origins and results
resolve; a dangling state is detected; the seven kinds are covered or
declared absent; an external destination is an explicit mock; and a graph
that smuggles a status field is refused — a preview raises no status.

Standard library only.
"""
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MODULE = os.path.join(ROOT, "test", "flow_graph.py")
REF = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                   "interactive-flow-prototypes.md")

_spec = importlib.util.spec_from_file_location("flow_graph", MODULE)
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

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


def good_graph():
    return json.loads(json.dumps({
        "flow": "FL-checkout", "entry": "SCR-01",
        "screens": [{"id": "SCR-01", "title": "Cart"},
                    {"id": "SCR-02", "title": "Address"},
                    {"id": "SCR-03", "title": "Error"},
                    {"id": "SCR-04", "title": "Done"}],
        "external": [{"id": "external:stripe-checkout", "mock": "explicit"}],
        "terminals": ["SCR-04"],
        "transitions": [
            {"id": "TR-01", "origin": "SCR-01", "action": "Continue",
             "result": "SCR-02", "kind": "happy"},
            {"id": "TR-02", "origin": "SCR-02", "action": "Pay",
             "result": "external:stripe-checkout", "kind": "external"},
            {"id": "TR-03", "origin": "SCR-02", "action": "Invalid zip",
             "result": "SCR-03", "kind": "error"},
            {"id": "TR-04", "origin": "SCR-03", "action": "Fix and retry",
             "result": "SCR-02", "kind": "recovery"},
            {"id": "TR-05", "origin": "SCR-02", "action": "Back",
             "result": "SCR-01", "kind": "back"},
            {"id": "TR-06", "origin": "SCR-01", "action": "Cancel",
             "result": "SCR-04", "kind": "cancel"},
        ],
        "scenarios": [{"id": "SCN-001", "kind": "happy", "path": ["TR-01", "TR-02"]}],
        "absent": ["returning"],
    }))


def t_sound_graph_passes():
    problems = G.validate_graph(good_graph())
    assert problems == [], f"a sound graph was refused: {problems[:3]}"


def t_transition_needs_all_three():
    g = good_graph()
    del g["transitions"][2]["action"]
    problems = G.validate_graph(g)
    assert any("IFP-01" in p and "action" in p for p in problems), \
        f"an edge without an action passed: {problems[:2]}"
    g2 = good_graph()
    g2["transitions"][0]["result"] = "SCR-99"
    problems2 = G.validate_graph(g2)
    assert any("IFP-02" in p and "SCR-99" in p for p in problems2), \
        "a transition into an undeclared screen passed"


def t_dangling_state_detected():
    g = good_graph()
    g["screens"].append({"id": "SCR-05", "title": "Orphan"})
    problems = G.validate_graph(g)
    assert any("IFP-03" in p and "SCR-05" in p and "unreachable" in p
               for p in problems), f"an unreachable screen passed: {problems[:2]}"
    g2 = good_graph()
    g2["terminals"] = []
    problems2 = G.validate_graph(g2)
    assert any("IFP-03" in p and "SCR-04" in p and "no way out" in p
               for p in problems2), "an undeclared dead end passed"


def t_kinds_covered_or_declared_absent():
    g = good_graph()
    g["absent"] = []
    problems = G.validate_graph(g)
    assert any("IFP-04" in p and "returning" in p for p in problems), \
        "a silently missing kind passed"
    g2 = good_graph()
    g2["transitions"][1]["kind"] = "magic"
    assert any("IFP-04" in p for p in G.validate_graph(g2)), \
        "an invented kind passed"


def t_external_must_be_explicit_mock():
    g = good_graph()
    g["external"][0].pop("mock")
    problems = G.validate_graph(g)
    assert any("IFP-05" in p and "explicit" in p for p in problems), \
        "an undeclared stand-in passed as a working integration"


def t_preview_raises_no_status():
    for site in ("graph", "screen", "transition", "scenario"):
        g = good_graph()
        target = {"graph": g, "screen": g["screens"][0],
                  "transition": g["transitions"][0],
                  "scenario": g["scenarios"][0]}[site]
        target["status"] = "implemented"
        problems = G.validate_graph(g)
        assert any("IFP-06" in p for p in problems), \
            f"a smuggled status on the {site} passed — the preview raised a status"


def t_reference_and_module_agree():
    flat = " ".join(open(REF, encoding="utf-8").read().split())
    for needle in ("origin/action/result, all three", "no dangling state",
                   "mock", "a preview raises no status", "test/flow_graph.py"):
        assert needle.lower() in flat.lower(), \
            f"the reference no longer states {needle!r}"
    for rule in ("IFP-01", "IFP-02", "IFP-03", "IFP-04", "IFP-05", "IFP-06"):
        assert rule in flat, f"the reference lost {rule}"


def main():
    case("a sound multi-branch graph passes", t_sound_graph_passes)
    case("a transition needs origin/action/result and a resolving target",
         t_transition_needs_all_three)
    case("a dangling state is detected — unreachable and no-way-out",
         t_dangling_state_detected)
    case("the seven kinds are covered or declared absent",
         t_kinds_covered_or_declared_absent)
    case("an external destination is an explicit mock",
         t_external_must_be_explicit_mock)
    case("a preview raises no status, at every site", t_preview_raises_no_status)
    case("the reference and the module agree", t_reference_and_module_agree)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
