#!/usr/bin/env python3
"""CTX-03.03 — coverage and the handoff receipt (sherlock audit, closing
leaf of CTX-03, on the graph of 03.01 and the fixture of 03.02).

The contract under test, as behaviour against test/flow_graph.py:

* coverage says walked / NOT_RUN / declared absent — an un-walked scenario
  is NOT_RUN, never a pass;
* a dead control (clicked, moved nothing) fails the smoke BY NAME, and so
  does a declared transition the smoke never reached;
* the receipt pins the artifact's sha256, keeps the two gates separate, and
  refuses a status field — a preview upgrades nothing;
* a screenshot-only run is NOT_RUN, not a functional PASS;
* the case corpus states goals WITHOUT UI hints, and its oracles agree with
  the fixture's embedded graph.

Standard library only.
"""
import hashlib
import importlib.util
import json
import os
import re
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
MOD = os.path.join(ROOT, "test", "flow_graph.py")
FIXTURE = os.path.join(ROOT, "test", "fixtures", "interactive-flow", "index.html")
CASES = os.path.join(ROOT, "test", "interactive_flow_cases.json")
WALKDOC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references",
                       "prototype-walkthrough.md")

_spec = importlib.util.spec_from_file_location("flow_graph", MOD)
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


def graph():
    m = re.search(r'<script type="application/json" id="flow-graph">\s*(\{.*?\})\s*</script>',
                  open(FIXTURE, encoding="utf-8").read(), re.S)
    return json.loads(m.group(1))


def walk(*tids):
    g = graph()
    trans = {t["id"]: t for t in g["transitions"]}
    out, state = [], g["entry"]
    for tid in tids:
        t = trans[tid]
        out.append({"transition": tid, "from": state, "to": t["result"]})
        state = t["result"]
    return out


def full_walk():
    return (walk("TR-01", "TR-02", "TR-07")
            + [{"transition": "TR-03", "from": "SCR-02", "to": "SCR-03"},
               {"transition": "TR-04", "from": "SCR-03", "to": "SCR-02"},
               {"transition": "TR-05", "from": "SCR-02", "to": "SCR-01"},
               {"transition": "TR-06", "from": "SCR-01", "to": "SCR-04"}])


def t_unwalked_is_not_run_never_pass():
    cov = G.coverage(graph(), walk("TR-01", "TR-02", "TR-07"))
    assert cov["scenarios"]["SCN-001"] == "walked"
    assert cov["scenarios"]["SCN-002"] == "NOT_RUN", \
        "an un-walked scenario was not NOT_RUN — silence read as coverage"
    assert cov["kinds"]["returning"] == "declared absent"
    assert cov["transitions"]["TR-03"] == "NOT_RUN"


def t_dead_control_fails_smoke_by_name():
    walked = full_walk()
    walked[1] = {"transition": "TR-02", "from": "SCR-02", "to": "SCR-02"}  # dead
    problems = G.smoke(graph(), walked)
    assert any("TR-02" in p and "DEAD" in p for p in problems), \
        f"a dead control passed the smoke: {problems[:2]}"
    problems2 = G.smoke(graph(), walk("TR-01"))
    assert any("TR-06" in p and "never walked" in p for p in problems2), \
        "a skipped declared transition did not fail the smoke"
    assert G.smoke(graph(), full_walk()) == [], "a full walk failed its smoke"


def t_receipt_pins_bytes_and_refuses_status():
    body = open(FIXTURE, "rb").read()
    r = G.receipt(graph(), full_walk(), body)
    assert r["artifact_sha256"] == hashlib.sha256(body).hexdigest()
    assert "production" in r["gates"] and "art_direction" in r["gates"]
    assert r["gates"]["production"] != r["gates"]["art_direction"], \
        "the two gates merged"
    g = graph()
    g["status"] = "implemented"
    try:
        G.receipt(g, full_walk(), body)
        raise AssertionError("a status field reached the receipt — the preview "
                             "upgraded evidence")
    except ValueError as e:
        assert "raises no status" in str(e)


def t_screenshot_only_is_not_functional():
    r = G.receipt(graph(), [], open(FIXTURE, "rb").read())
    assert r["functional"].startswith("NOT_RUN"), \
        f"screenshots alone passed as functional: {r['functional']!r}"


def t_cases_carry_goals_without_ui_hints():
    m = json.load(open(CASES, encoding="utf-8"))
    g = graph()
    labels = {t["action"].lower() for t in g["transitions"]}
    tids = {t["id"] for t in g["transitions"]}
    ids = [c["id"] for c in m["cases"]]
    assert len(ids) == len(set(ids)) and len(ids) >= 5
    for c in m["cases"]:
        goal = c["goal"].lower()
        # The reading-test smell is naming the CONTROL: a multi-word label
        # quoted whole, an instruction verb aimed at one, or a transition id.
        # A one-word verb like "pay" is the user's own language and stays.
        for label in labels:
            if " " in label:
                assert label not in goal, \
                    f"{c['id']}: the goal quotes the control {label!r} — a reading test"
        for verb in ("click", "press", "tap", "нажми", "кликни"):
            assert verb not in goal, \
                f"{c['id']}: the goal instructs {verb!r} — a reading test"
        for tid in tids:
            assert tid.lower() not in goal, f"{c['id']}: the goal names {tid}"
    shot = next(c for c in m["cases"] if "screenshot" in c["id"])
    assert shot["oracle"]["functional"].startswith("NOT_RUN")
    ext = next(c for c in m["cases"] if "external" in c["id"])
    assert ext["oracle"]["external_mock"] == "explicit"
    for sc in ("SCN-001", "SCN-002", "SCN-003"):
        assert any(c["oracle"].get("scenario") == sc for c in m["cases"]), \
            f"no case walks {sc}"


def t_doctrine_states_the_rules():
    flat = " ".join(open(WALKDOC, encoding="utf-8").read().split())
    for needle in ("no second flow store",
                   "stated without UI hints",
                   "NOT_RUN is not a pass",
                   "dead control and fails the smoke by name",
                   "screenshots alone are not a functional pass",
                   "carries no status field",
                   "a green walkthrough satisfies neither"):
        assert needle in flat, f"the doctrine no longer states {needle!r}"


def main():
    case("an un-walked scenario is NOT_RUN, never a pass",
         t_unwalked_is_not_run_never_pass)
    case("a dead control fails the smoke by name", t_dead_control_fails_smoke_by_name)
    case("the receipt pins the bytes, splits the gates and refuses a status",
         t_receipt_pins_bytes_and_refuses_status)
    case("a screenshot-only run is not a functional pass",
         t_screenshot_only_is_not_functional)
    case("the case corpus states goals without UI hints and matches the graph",
         t_cases_carry_goals_without_ui_hints)
    case("the doctrine states the rules", t_doctrine_states_the_rules)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
