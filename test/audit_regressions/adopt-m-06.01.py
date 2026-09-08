#!/usr/bin/env python3
"""ADOPT-M-06.01 — research synthesis keeps provenance (sherlock audit).

The adoption: a research-evidence ledger contract in the foundation layer —
observation / citation / inference / hypothesis as separate classes,
contradictory participants preserved and linked, every number bound to
entity + unit + population + date, and no-data topics staying hypotheses
(no quota of invented evidence).

This file checks the doctrine ships (source of truth + the synced copy the
skills CLI actually delivers + the SKILL.md load condition), then drives the
documented row contract as behaviour: a checker implementing exactly the rules
the reference states, run over acceptance fixtures both ways — the valid ledger
passes, and each corruption the contract exists to catch is caught.

Standard library only.
"""
import os
import sys

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "plugins", "super-ux", "skills", "references", "research-evidence.md")
SHIPPED = os.path.join(ROOT, "plugins", "super-ux", "skills", "ux-foundation",
                       "references", "research-evidence.md")
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


def t_doctrine_ships_everywhere():
    assert os.path.isfile(SRC), "the source-of-truth contract is missing"
    assert os.path.isfile(SHIPPED), "ux-foundation does not ship its copy (run test/sync_references.py)"
    with open(SRC, "rb") as a, open(SHIPPED, "rb") as b:
        assert a.read() == b.read(), "the shipped copy drifted from skills/references/"
    text = open(SRC, encoding="utf-8").read()
    for needle in ("observation", "citation", "inference", "hypothesis",
                   "contradicts", "single-source", "population", "confirm-by",
                   "no quota of evidence", "append-only",
                   "together or not at all"):
        assert needle in text, f"the contract no longer states {needle!r}"
    skill = open(SKILL, encoding="utf-8").read()
    assert "research-evidence.md" in skill, "SKILL.md never links the contract"
    assert "Every finding lands with its provenance" in skill, \
        "SKILL.md link lost its load condition"


# ---------------------------- the documented row contract, run as behaviour


CLASSES = {"observation", "citation", "inference", "hypothesis"}
NUMBER_ANCHORS = ("unit", "entity", "population", "date")


def violations(rows):
    """The rules exactly as references/research-evidence.md states them."""
    out = []
    by_id = {r["id"]: r for r in rows}
    for r in rows:
        if r.get("class") not in CLASSES:
            out.append(f"{r['id']}: unknown class {r.get('class')!r}")
        # a number travels with its anchors — together or not at all
        anchored = [k for k in NUMBER_ANCHORS if r.get(k)]
        if r.get("number") and len(anchored) != len(NUMBER_ANCHORS):
            missing = [k for k in NUMBER_ANCHORS if not r.get(k)]
            out.append(f"{r['id']}: number without {'/'.join(missing)} — rejected, not padded")
        # contradictions are linked both ways, and the contradicted row stays
        for other in r.get("contradicts", []):
            if other not in by_id:
                out.append(f"{r['id']}: contradicts {other}, which is not in the ledger")
            elif r["id"] not in by_id[other].get("contradicts", []):
                out.append(f"{r['id']}: contradiction with {other} is linked one way only")
        if r.get("class") == "inference":
            inputs = r.get("derived_from", [])
            if not inputs:
                out.append(f"{r['id']}: an inference that names no inputs cannot be re-derived")
            for src in inputs:
                if src not in by_id:
                    out.append(f"{r['id']}: derived from {src}, which does not exist — invented evidence")
            if len(inputs) == 1 and not r.get("single_source"):
                out.append(f"{r['id']}: rests on one input and does not carry single-source")
        if r.get("class") == "hypothesis" and not r.get("confirm_by"):
            out.append(f"{r['id']}: a hypothesis must name what would confirm it")
    return out


def row(id_, class_, **kw):
    d = {"id": id_, "class": class_}
    d.update(kw)
    return d


def t_contradictory_participants_stay_linked():
    ledger = [
        row("RE-0001", "observation", source="P07, session 2026-08-14",
            contradicts=["RE-0002"]),
        row("RE-0002", "observation", source="P11, session 2026-08-15",
            contradicts=["RE-0001"]),
        row("RE-0003", "inference", derived_from=["RE-0001", "RE-0002"],
            source="derived"),
    ]
    assert violations(ledger) == [], f"a valid contradiction pair was rejected: {violations(ledger)}"
    one_way = [
        row("RE-0001", "observation", contradicts=["RE-0002"]),
        row("RE-0002", "observation"),
    ]
    v = violations(one_way)
    assert any("one way only" in x for x in v), f"a one-way contradiction link passed: {v}"


def t_number_binds_its_anchors():
    good = [row("RE-0005", "observation", number="12%", unit="of sessions",
                entity="checkout currency step", population="DE cohort, n=41",
                date="2026-08")]
    assert violations(good) == []
    for dropped in NUMBER_ANCHORS:
        bad_row = dict(good[0])
        bad_row.pop(dropped)
        v = violations([bad_row])
        assert any("number without" in x and dropped in x for x in v), \
            f"a number missing {dropped} passed: {v}"


def t_single_source_is_flagged():
    unflagged = [
        row("RE-0001", "citation", source="https://x (read 2026-08-14)"),
        row("RE-0002", "inference", derived_from=["RE-0001"]),
    ]
    v = violations(unflagged)
    assert any("single-source" in x for x in v), f"a single-source inference passed unflagged: {v}"
    flagged = [
        row("RE-0001", "citation", source="https://x (read 2026-08-14)"),
        row("RE-0002", "inference", derived_from=["RE-0001"], single_source=True),
    ]
    assert violations(flagged) == []


def t_no_data_stays_hypothesis():
    honest = [row("RE-0009", "hypothesis",
                  confirm_by="five sessions on the pricing page")]
    assert violations(honest) == []
    quota_filling = [
        row("RE-0009", "inference", derived_from=["RE-9999"]),  # cites a row that never existed
    ]
    v = violations(quota_filling)
    assert any("invented evidence" in x for x in v), f"invented evidence passed: {v}"
    bare = [row("RE-0010", "hypothesis")]
    v2 = violations(bare)
    assert any("confirm" in x for x in v2), f"a hypothesis with no confirm-by passed: {v2}"


def t_checker_reads_only_documented_fields():
    """Every field the checker reads is a field the contract documents — the test
    cannot drift into rules the doctrine never stated."""
    text = open(SRC, encoding="utf-8").read()
    for field in ("class", "source", "contradicts", "single-source", "number",
                  "unit", "entity", "population", "date", "confirm-by", "derived-from"):
        assert field in text, f"the checker reads {field!r} and the contract never names it"


def main():
    case("the contract ships in both channels with its load condition", t_doctrine_ships_everywhere)
    case("two contradictory participants remain, linked both ways", t_contradictory_participants_stay_linked)
    case("a number binds entity+unit+population+date", t_number_binds_its_anchors)
    case("a single-source inference is flagged", t_single_source_is_flagged)
    case("no data stays a hypothesis; invented evidence is caught", t_no_data_stays_hypothesis)
    case("the checker reads only documented fields", t_checker_reads_only_documented_fields)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
