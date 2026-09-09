#!/usr/bin/env python3
"""FIX-UP-06.02 — selection aggregation (sherlock audit, UP-06, second leaf).

The fix under test (bin/super-ux.js, run as a real process):
* the exit code aggregates ONLY the selected install operations, each labelled
  by channel; the optional router offer never changes the result;
* a MIXED selection where a required op fails reports PARTIAL naming what
  installed and what failed, and there is no overall success;
* a router-offer failure is caught and does not flip the exit code.

POSIX only; skipped honestly elsewhere. Standard library only.
"""
import os
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CLI = os.path.join(ROOT, "bin", "super-ux.js")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def make_env(claude_exit=0, npx_exit=0):
    home = tempfile.mkdtemp(prefix="up0602-")
    fakebin = os.path.join(home, "fakebin")
    os.makedirs(fakebin)
    node_only = os.path.join(home, "nodebin")
    os.makedirs(node_only)
    os.symlink(shutil.which("node"), os.path.join(node_only, "node"))
    with open(os.path.join(fakebin, "claude"), "w") as fh:
        fh.write(f"#!/bin/sh\nexit {claude_exit}\n")
    os.chmod(os.path.join(fakebin, "claude"), 0o755)
    with open(os.path.join(fakebin, "npx"), "w") as fh:
        fh.write(f"#!/bin/sh\nexit {npx_exit}\n")
    os.chmod(os.path.join(fakebin, "npx"), 0o755)
    env = dict(os.environ, HOME=home,
               PATH=f"{fakebin}:{node_only}:/usr/bin:/bin")
    return home, env


def run_menu(selection, env):
    return subprocess.run(["node", CLI], input=selection, text=True,
                          capture_output=True, env=env, timeout=120)


def t_mixed_selection_reports_partial():
    # cursor (always installs) + claude (fails) → PARTIAL, exit 1
    home, env = make_env(claude_exit=1)
    try:
        r = run_menu("2,3\n", env)
        assert r.returncode == 1, \
            f"exit {r.returncode}, expected 1\n{r.stdout}\n{r.stderr}"
        assert "partial:" in r.stderr, "a mixed selection did not report PARTIAL"
        assert "installed cursor" in r.stderr, "the succeeded channel is not named"
        assert "FAILED claude" in r.stderr, "the failed channel is not named"
    finally:
        shutil.rmtree(home, ignore_errors=True)


def t_all_selected_fail_is_not_partial():
    home, env = make_env(claude_exit=1)
    try:
        r = run_menu("3\n", env)
        assert r.returncode == 1
        assert "failed: claude" in r.stderr and "partial:" not in r.stderr, \
            "a single failed op should read 'failed', not 'partial'"
    finally:
        shutil.rmtree(home, ignore_errors=True)


def t_router_offer_does_not_change_result():
    # cursor installs fine (exit 0) even though the router offer's npx 'fails'
    home, env = make_env(claude_exit=0, npx_exit=7)
    try:
        r = run_menu("2\n", env)
        assert r.returncode == 0, \
            f"the optional router offer flipped the exit code: {r.returncode}\n{r.stderr}"
    finally:
        shutil.rmtree(home, ignore_errors=True)


def t_aggregation_is_selected_only():
    with open(CLI, encoding="utf-8") as fh:
        s = fh.read()
    body = s[s.index("const results = [];"):s.index("function offerRouters")] \
        if "function offerRouters" in s[s.index("const results = [];"):] \
        else s[s.index("const results = [];"):]
    assert "channel: 'cursor'" in s and "channel: 'claude'" in s and "channel: 'skills'" in s, \
        "results are not labelled by channel"
    assert "optional enrichment and is\n  // deliberately NOT in this list".replace("\n  // ", " ") in \
        " ".join(s.split()) or "deliberately NOT in this list" in s, \
        "the router offer is not documented as outside the result set"
    assert "try { offerRouters(); }" in s, "the router offer is not guarded"


def main():
    if os.name != "posix":
        print("skip: POSIX only — the fakes are shell scripts")
        return 0
    case("a mixed selection with a failed required op reports PARTIAL",
         t_mixed_selection_reports_partial)
    case("a single failed op reads failed, not partial",
         t_all_selected_fail_is_not_partial)
    case("the optional router offer never changes the install result",
         t_router_offer_does_not_change_result)
    case("the aggregation is over selected ops only, router offer excluded+guarded",
         t_aggregation_is_selected_only)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
