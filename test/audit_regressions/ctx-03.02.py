#!/usr/bin/env python3
"""CTX-03.02 — the clickable flow fixture (sherlock audit, parent CTX-03, on
CTX-03.01's bounded scenario graph).

The fixture (test/fixtures/interactive-flow/index.html) is a local page whose
every capability is DECLARED in an embedded graph and interpreted by a
generic runner. Checked here, stdlib only:

* the embedded graph passes test/flow_graph.py — the fixture and the
  contract are one document;
* the controls exist for what is declared: a scenario selector holding every
  scenario, a reset, deep-link handling, and per-transition buttons the
  runner derives from the graph;
* every declared scenario path traverses the graph to a legal state —
  controls traverse intended states by construction;
* the payment step is a LABELLED simulation (data-mock="explicit", the
  SIMULATION banner) and the page calls no live service: no external
  script/src/href, no fetch, no XMLHttpRequest, no SDK.
"""
import importlib.util
import json
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FIXTURE = os.path.join(ROOT, "test", "fixtures", "interactive-flow", "index.html")
GRAPH_MOD = os.path.join(ROOT, "test", "flow_graph.py")

_spec = importlib.util.spec_from_file_location("flow_graph", GRAPH_MOD)
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


def html():
    with open(FIXTURE, encoding="utf-8") as fh:
        return fh.read()


def graph():
    m = re.search(r'<script type="application/json" id="flow-graph">\s*(\{.*?\})\s*</script>',
                  html(), re.S)
    assert m, "the fixture carries no embedded flow-graph block"
    return json.loads(m.group(1))


def t_embedded_graph_is_sound():
    problems = G.validate_graph(graph())
    assert problems == [], f"the embedded graph violates its own contract: {problems[:3]}"


def t_controls_exist_for_what_is_declared():
    doc = html()
    assert 'data-role="scenario-selector"' in doc, "no scenario selector"
    assert 'data-action="reset"' in doc, "no reset control"
    assert "location.hash" in doc, "no deep-link handling"
    assert 'setAttribute("data-transition", t.id)' in doc, \
        "transition buttons are not derived from the graph"
    g = graph()
    assert "G.scenarios.forEach" in doc, \
        "the selector does not enumerate the declared scenarios"
    assert len(g["scenarios"]) >= 3, "fewer scenarios than the acceptance needs"


def t_every_scenario_path_traverses_legally():
    g = graph()
    trans = {t["id"]: t for t in g["transitions"]}
    legal_states = {s["id"] for s in g["screens"]} | {e["id"] for e in g["external"]}
    for sc in g["scenarios"]:
        state = g["entry"]
        for tid in sc["path"]:
            t = trans.get(tid)
            assert t, f"{sc['id']}: path names undeclared transition {tid}"
            assert t["origin"] == state, \
                (f"{sc['id']}: {tid} fires from {t['origin']} but the walk is at "
                 f"{state} — the control cannot traverse the intended state")
            state = t["result"]
            assert state in legal_states, f"{sc['id']}: walked into undeclared {state}"
        assert state in set(g.get("terminals", [])) | {g["entry"]} | legal_states


def t_simulation_is_labelled_and_nothing_is_live():
    doc = html()
    assert 'data-mock", "explicit"' in doc.replace("'", '"') or \
           'data-mock="explicit"' in doc or 'setAttribute("data-mock", "explicit")' in doc, \
        "the external step is not marked as an explicit mock"
    assert "SIMULATION" in doc, "the simulation banner is missing"
    for live in ("fetch(", "XMLHttpRequest", "<script src=", "https://", "http://"):
        assert live not in doc, \
            f"the fixture contains {live!r} — a preview must not reach a live service"
    ext = graph()["external"]
    assert all(e.get("mock") == "explicit" for e in ext), \
        "an external destination is not declared as an explicit mock"


def t_page_is_a_complete_local_document():
    doc = html()
    assert doc.lstrip().lower().startswith("<!doctype html>"), "no doctype"
    assert re.search(r'<meta charset="utf-8">', doc, re.I), \
        "no charset — a file:// page falls back to a legacy encoding"


def main():
    case("the embedded graph passes the bounded-graph contract",
         t_embedded_graph_is_sound)
    case("selector, reset, deep link and derived controls exist",
         t_controls_exist_for_what_is_declared)
    case("every declared scenario path traverses legally",
         t_every_scenario_path_traverses_legally)
    case("the simulation is labelled and nothing is live",
         t_simulation_is_labelled_and_nothing_is_live)
    case("the page is a complete local document", t_page_is_a_complete_local_document)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
