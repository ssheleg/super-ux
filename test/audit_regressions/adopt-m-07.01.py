#!/usr/bin/env python3
"""ADOPT-M-07.01 — the research ledger wired in, without a new research route
(sherlock audit; depends on ADOPT-M-06.01's research-evidence contract).

The adoption: the foundation layer uses a LOCAL ledger
(`docs/ux/research-ledger.md`, per references/research-evidence.md) and the
evidence ids and unknowns TRAVEL into the scenarios — provenance rides the
trace chain. A transcript already on disk is a complete input: no Notion, no
Dovetail, no browser, no API key.

Acceptance, run as behaviour over a local fixture: the fixture needs no
plugins or keys (stdlib only, no network), scenarios retain evidence ids and
unknowns, and the two drop defects — a dangling RE- citation and a hypothesis
silently dropped on the way to a scenario — are caught.

Standard library only.
"""
import os
import re
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SKILL = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-foundation", "SKILL.md")

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


# ------------------------------------------------------------------ the doctrine


def t_doctrine_wires_the_ledger_without_a_route():
    flat = " ".join(open(SKILL, encoding="utf-8").read().split())
    for needle in ("The ledger is local, and it is not a new route",
                   "docs/ux/research-ledger.md",
                   "a step INSIDE foundation work, never a separate pipeline",
                   "no Notion, no Dovetail, no browser and no API key",
                   "Evidence ids and unknowns travel into the scenarios",
                   "scenarios built on top RETAIN those ids",
                   "rides along as an explicit unknown"):
        assert needle in flat, f"the doctrine no longer states {needle!r}"


# ------------------------- the carry-through, run over a local fixture


LEDGER = """# Research ledger

- id: RE-0001
  class: observation
  statement: "P07 abandoned checkout at the currency step"
  source: P07, transcript 2026-08-14 (local file)
- id: RE-0002
  class: hypothesis
  statement: "DE users expect EUR by default"
  confirm-by: five sessions with DE cohort
"""

FOUNDATION = """# Foundation
## Personas
- PER-01 freelancer — cites: RE-0001
## Journeys
- J-01 checkout — pain at currency step (RE-0001); open: RE-0002
"""

SCENARIO_GOOD = """# Scenarios
- SC-01 (traces: J-01) pay in local currency
  evidence: RE-0001
  unknown: RE-0002 — DE users expect EUR by default (unconfirmed)
"""

SCENARIO_DROPS_UNKNOWN = """# Scenarios
- SC-01 (traces: J-01) pay in local currency
  evidence: RE-0001
"""

SCENARIO_DANGLING = """# Scenarios
- SC-01 (traces: J-01) pay in local currency
  evidence: RE-0999
  unknown: RE-0002 — DE users expect EUR by default (unconfirmed)
"""


def ledger_ids(text):
    return set(re.findall(r"\bid: (RE-\d{4})", text))


def hypotheses(text):
    out = set()
    for block in text.split("- id: ")[1:]:
        m = re.match(r"(RE-\d{4})", block)
        if m and "class: hypothesis" in block:
            out.add(m.group(1))
    return out


def carry_violations(ledger, foundation, scenarios):
    """The documented rules: every cited id resolves; every hypothesis a
    foundation row carries reaches the scenarios as an explicit unknown."""
    known = ledger_ids(ledger)
    out = []
    for rid in set(re.findall(r"\bRE-\d{4}\b", foundation + scenarios)):
        if rid not in known:
            out.append(f"{rid}: cited but not in the ledger — provenance broke")
    for hyp in hypotheses(ledger):
        if hyp in foundation and not re.search(rf"unknown: {hyp}\b", scenarios):
            out.append(f"{hyp}: a hypothesis shaped the foundation and was dropped "
                       "on the way to the scenarios — a guess in a fact's clothes")
    return out


def with_fixture(scenario_text):
    d = tempfile.mkdtemp(prefix="adopt-m-0701-")
    try:
        ux = os.path.join(d, "docs", "ux")
        os.makedirs(ux)
        for name, text in (("research-ledger.md", LEDGER),
                           ("foundation.md", FOUNDATION),
                           ("scenarios.md", scenario_text)):
            with open(os.path.join(ux, name), "w") as fh:
                fh.write(text)
        with open(os.path.join(ux, "research-ledger.md")) as a, \
                open(os.path.join(ux, "foundation.md")) as b, \
                open(os.path.join(ux, "scenarios.md")) as c:
            return carry_violations(a.read(), b.read(), c.read())
    finally:
        shutil.rmtree(d)


def t_local_fixture_needs_no_plugins_or_keys():
    """The whole flow runs from files on disk: this test imports nothing beyond
    the stdlib, opens no socket, and reads no environment key."""
    assert with_fixture(SCENARIO_GOOD) == [], \
        f"a complete local fixture was rejected: {with_fixture(SCENARIO_GOOD)}"
    for mod in ("requests", "notion_client", "dovetail"):
        assert mod not in sys.modules, f"{mod} was imported — the local flow phoned home"


def t_scenarios_retain_ids_and_unknowns():
    assert re.search(r"evidence: RE-0001", SCENARIO_GOOD)
    assert re.search(r"unknown: RE-0002", SCENARIO_GOOD)
    assert with_fixture(SCENARIO_GOOD) == []


def t_dropped_unknown_is_caught():
    v = with_fixture(SCENARIO_DROPS_UNKNOWN)
    assert any("dropped" in x for x in v), f"a dropped hypothesis passed: {v}"


def t_dangling_citation_is_caught():
    v = with_fixture(SCENARIO_DANGLING)
    assert any("RE-0999" in x and "not in the ledger" in x for x in v), \
        f"a dangling evidence id passed: {v}"


def main():
    case("the doctrine wires the local ledger without a new route",
         t_doctrine_wires_the_ledger_without_a_route)
    case("a local transcript fixture needs no plugins or keys",
         t_local_fixture_needs_no_plugins_or_keys)
    case("scenarios retain evidence ids and unknowns", t_scenarios_retain_ids_and_unknowns)
    case("a hypothesis dropped en route is caught", t_dropped_unknown_is_caught)
    case("a dangling evidence citation is caught", t_dangling_citation_is_caught)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
