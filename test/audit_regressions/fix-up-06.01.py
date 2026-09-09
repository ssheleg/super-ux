#!/usr/bin/env python3
"""FIX-UP-06.01 — the installer result is typed and the exit code is computed
from it (sherlock audit, UP-06).

The finding: the super-menu-failure fixture picked item 3 (Claude plugin) with
every child operation mocked to status 1 — the output said "plugin install
failed" and the process exited 0: installClaudePlugin returned nothing, and
the menu tracked only the skills-picker refusal.

The fix under test (bin/super-ux.js, run as a real process against throwaway
HOMEs and a fake PATH — POSIX only, skipped honestly elsewhere):
* results are typed installed/unchanged/refused/unsupported/failed with the
  backend's exit/signal/command preserved in the output;
* a selected FAILURE exits 1; a refusal exits 3; an absent backend
  (unsupported) exits the documented 4; success stays 0;
* failure outranks refusal outranks unsupported.

Standard library only.
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
not_run = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def make_env(claude_exit=None, npx_exit=0):
    """A throwaway HOME and a PATH holding only node + our fakes."""
    home = tempfile.mkdtemp(prefix="up0601-")
    fakebin = os.path.join(home, "fakebin")
    os.makedirs(fakebin)
    # node ONLY — the real npm global bin dir sits beside node and carries the
    # real `claude`, which the absent-backend case must not find (and no case
    # may reach the network through a real CLI).
    node_only = os.path.join(home, "nodebin")
    os.makedirs(node_only)
    os.symlink(shutil.which("node"), os.path.join(node_only, "node"))
    node_dir = node_only
    if claude_exit is not None:
        with open(os.path.join(fakebin, "claude"), "w") as fh:
            fh.write(f"#!/bin/sh\nexit {claude_exit}\n")
        os.chmod(os.path.join(fakebin, "claude"), 0o755)
    with open(os.path.join(fakebin, "npx"), "w") as fh:
        fh.write(f"#!/bin/sh\nexit {npx_exit}\n")
    os.chmod(os.path.join(fakebin, "npx"), 0o755)
    env = dict(os.environ, HOME=home,
               PATH=f"{fakebin}:{node_dir}:/usr/bin:/bin")
    return home, env


def run_menu(selection, env):
    r = subprocess.run(["node", CLI], input=selection, text=True,
                       capture_output=True, env=env, timeout=120)
    return r


def t_selected_failure_exits_1():
    home, env = make_env(claude_exit=1)
    try:
        r = run_menu("3\n", env)
        assert r.returncode == 1, \
            f"exit {r.returncode}, expected 1\n{r.stdout}\n{r.stderr}"
        assert "The plugin did not install" in r.stderr, "the failure is not stated"
        assert "claude plugin install super-ux@super-ux" in r.stderr, \
            "the backend command is not preserved in the output"
        assert "exited 1" in r.stderr, "the backend exit code is not preserved"
    finally:
        shutil.rmtree(home, ignore_errors=True)


def t_unsupported_exits_4():
    home, env = make_env(claude_exit=None)      # no claude on PATH
    try:
        r = run_menu("3\n", env)
        assert r.returncode == 4, \
            f"exit {r.returncode}, expected 4\n{r.stdout}\n{r.stderr}"
        assert "claude CLI not found" in r.stdout
    finally:
        shutil.rmtree(home, ignore_errors=True)


def t_refusal_still_exits_3():
    home, env = make_env(claude_exit=0)
    try:
        plug = os.path.join(home, ".claude", "plugins")
        os.makedirs(plug)
        with open(os.path.join(plug, "installed_plugins.json"), "w") as fh:
            fh.write('{"plugins": {"super-ux@super-ux": [{"installPath": "/x"}]}}')
        r = run_menu("1\n", env)
        assert r.returncode == 3, \
            f"exit {r.returncode}, expected 3\n{r.stdout}\n{r.stderr}"
    finally:
        shutil.rmtree(home, ignore_errors=True)


def t_success_exits_0():
    home, env = make_env(claude_exit=0)
    try:
        r = run_menu("3\n", env)
        assert r.returncode == 0, \
            f"exit {r.returncode}, expected 0\n{r.stdout}\n{r.stderr}"
    finally:
        shutil.rmtree(home, ignore_errors=True)


def t_exit_contract_documented():
    with open(CLI, encoding="utf-8") as fh:
        s = fh.read()
    assert "EXIT_FAILED = 1" in s and "EXIT_UNSUPPORTED = 4" in s
    assert "Failure outranks refusal outranks unsupported" in s


def main():
    if os.name != "posix":
        print("skip: POSIX only — the fakes are shell scripts")
        return 0
    case("a selected failure exits 1 with the backend command+exit preserved",
         t_selected_failure_exits_1)
    case("an absent backend exits the documented 4", t_unsupported_exits_4)
    case("the plugin-present refusal still exits 3", t_refusal_still_exits_3)
    case("a clean install still exits 0", t_success_exits_0)
    case("the exit contract is documented in the header", t_exit_contract_documented)
    for n in not_run:
        print(f"  NOT_RUN  {n}")
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
