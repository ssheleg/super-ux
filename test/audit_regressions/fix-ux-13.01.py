#!/usr/bin/env python3
"""FIX-UX-13.01 — preconditions per scope, not one blanket scenarios stop
(sherlock audit, UX-13).

The finding: an unconditional stop ("no scenarios → stop") routed a standalone
brand/copy project into scenario creation; benchmark demanded file:line for
external observations.

The fix under test (ux-audit/SKILL.md):
* preconditions computed AFTER the scope — scenario needs scenarios.md, copy
  needs the brand pack, benchmark needs observed URLs + capture receipts;
* /ux-audit copy on a brand-only project runs the copy pass only; /ux-audit
  all without base runs what it can and states the limitation;
* evidence kind by claim — file:line for code, URL+timestamp+capture for
  external data; a benchmark never invents a local file:line;
* the routing rule run as behaviour.

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


def t_preconditions_per_scope():
    d = flat()
    assert "Preconditions are computed AFTER the scope, one per pass — never a blanket\nstop.".replace("\n", " ") in d \
        or "computed AFTER the scope, one per pass — never a blanket stop" in d
    assert "**copy scope** needs only the brand pack" in d
    assert "not routed into creating scenarios it has no use for" in d
    assert "**benchmark scope** needs the observed competitor URLs and their capture\n  receipts".replace("\n  ", " ") in d \
        or "benchmark scope** needs the observed competitor URLs and their capture receipts" in d


def t_all_without_base_states_limit():
    d = flat()
    assert "runs the passes whose inputs exist and STATES\nthe scenario limitation".replace("\n", " ") in d \
        or "runs the passes whose inputs exist and STATES the scenario limitation" in d


def t_evidence_kind_by_claim():
    d = flat()
    assert "A claim about\nTHIS codebase cites **`file:line`**".replace("\n", " ") in d \
        or "A claim about THIS codebase cites **`file:line`**" in d
    assert "URL + timestamp + capture" in d
    assert "a benchmark never invents a local\n`file:line`".replace("\n", " ") in d \
        or "a benchmark never invents a local `file:line`" in d
    assert "Every verdict must cite `file:line` evidence." not in d, \
        "the blanket file:line rule survived"


# ---- the routing rule as behaviour


def passes_for(scope, have):
    """scope: 'scenario'|'copy'|'benchmark'|'all'; have: set of inputs.
    Returns (passes_run, limitations)."""
    need = {"scenario": "scenarios", "copy": "brand", "benchmark": "urls"}
    run, limits = [], []
    scopes = ["scenario", "copy", "benchmark"] if scope == "all" else [scope]
    for s in scopes:
        if need[s] in have:
            run.append(s)
        else:
            limits.append(f"{s}: needs {need[s]}")
    return run, limits


def t_copy_only_on_brand_project():
    run, limits = passes_for("copy", have={"brand"})
    assert run == ["copy"] and not limits, \
        f"a brand-only copy audit did not run copy-only: {run} {limits}"
    # crucially, no scenario creation demanded
    assert "scenario" not in run


def t_all_without_scenarios_runs_rest():
    run, limits = passes_for("all", have={"brand", "urls"})
    assert "copy" in run and "benchmark" in run
    assert "scenario" not in run and any("scenario" in l for l in limits), \
        "the missing scenario base was not stated as a limitation"


def main():
    case("preconditions are per-scope, not a blanket stop", t_preconditions_per_scope)
    case("ux-audit all without base runs what it can and states the limit",
         t_all_without_base_states_limit)
    case("evidence kind is by claim; benchmark never invents file:line",
         t_evidence_kind_by_claim)
    case("fixture: copy on a brand-only project runs copy only",
         t_copy_only_on_brand_project)
    case("fixture: all without scenarios runs the rest, states the limit",
         t_all_without_scenarios_runs_rest)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
