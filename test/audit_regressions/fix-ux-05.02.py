#!/usr/bin/env python3
"""FIX-UX-05.02 — observable copy corpus: surface count, actual text changes
and semantic invariants (sherlock audit, UX-05).

The finding: EV-04 promises one status line PER SURFACE, but its expect held a
single "Humanization:" — one line for a two-surface batch passed. And nothing
asserted that adaptation preserves the claim's facts, or that already-good
text survives a pass unchanged.

The fix under test:
* cases.json — EV-04 carries expect_count {"Humanization:": 2} and an
  invariant; EV-05 is the no-op case (already-good text, invariants verbatim);
* run.py classify() enforces expect_count and invariants;
* both audit mock substitutions FAIL (one line for two surfaces; altered
  invariant), and two valid surface outputs PASS.

Runs the real run.py with a fake `claude`. Standard library only.
"""
import json
import os
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RUN = os.path.join(ROOT, "test", "evals", "run.py")
CASES = os.path.join(ROOT, "test", "evals", "cases.json")

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


def fake_claude(stdout_lines):
    d = tempfile.mkdtemp()
    body = "\n".join(f'echo "{l}"' for l in stdout_lines) + "\nexit 0\n"
    path = os.path.join(d, "claude")
    with open(path, "w") as fh:
        fh.write("#!/bin/sh\n" + body)
    os.chmod(path, 0o755)
    return d

def run_case(bindir, case_id):
    mf = tempfile.mkstemp(suffix=".json")[1]
    env = dict(os.environ, PATH=bindir + os.pathsep + os.environ.get("PATH", ""))
    r = subprocess.run([sys.executable, RUN, "--case", case_id, "--timeout", "30",
                        "--manifest", mf], capture_output=True, text=True,
                       timeout=120, env=env)
    return r, json.loads(open(mf).read())


def t_cases_carry_the_structure():
    d = json.loads(open(CASES, encoding="utf-8").read())
    ev04 = next(c for c in d["cases"] if c["id"] == "EV-04")
    assert ev04.get("expect_count", {}).get("Humanization:") == 2, \
        "EV-04 does not demand one status line per surface"
    assert ev04.get("invariants"), "EV-04 protects no semantic invariant"
    ev05 = next(c for c in d["cases"] if c["id"] == "EV-05")
    assert ev05.get("invariants") and "no-op" in ev05["measures"].lower(), \
        "the already-good no-op case is missing"


def t_one_line_for_two_surfaces_fails():
    r, man = run_case(fake_claude(
        ["Humanization: on — 3 markers, 2 addressed",
         "hero copy here … before the call ends"]), "EV-04")
    assert r.returncode == 1, "one status line satisfied a two-surface promise — the finding"
    assert man[0]["state"] == "FAIL"
    assert "x2 (found 1)" in r.stdout, f"the count shortfall is not named:\n{r.stdout[-400:]}"


def t_altered_invariant_fails():
    r, man = run_case(fake_claude(
        ["Humanization: on", "Humanization: on",
         "notes become follow-ups after the call ends"]), "EV-04")   # fact altered
    assert r.returncode == 1, "an adaptation that altered the claim's fact passed"
    assert "invariant altered or lost" in r.stdout


def t_two_valid_surface_outputs_pass():
    r, man = run_case(fake_claude(
        ["hero: Meeting notes become follow-up emails before the call ends.",
         "Humanization: on — hero, 2 markers addressed",
         "post: Notes into follow-ups, before the call ends.",
         "Humanization: on — post, clean"]), "EV-04")
    assert r.returncode == 0, f"two valid surface outputs failed:\n{r.stdout[-500:]}"
    assert man[0]["state"] == "PASS"


def t_noop_case_guards_good_text():
    good = ["Humanization: on — nothing to change",
            "We store your notes on your device. Deleting the app deletes them. "
            "Nothing is uploaded unless you press Share."]
    r, man = run_case(fake_claude(good), "EV-05")
    assert r.returncode == 0, f"the untouched no-op failed:\n{r.stdout[-400:]}"
    rewritten = ["Humanization: on — polished it up",
                 "Your notes live safely on-device; removal wipes them. "
                 "Uploads happen only via Share."]
    r2, _ = run_case(fake_claude(rewritten), "EV-05")
    assert r2.returncode == 1, "a pass that rewrote already-good text was scored PASS"


def main():
    case("cases.json carries expect_count/invariants and the no-op case",
         t_cases_carry_the_structure)
    case("one status line for two surfaces FAILS (audit mock #1)",
         t_one_line_for_two_surfaces_fails)
    case("an altered semantic invariant FAILS (audit mock #2)", t_altered_invariant_fails)
    case("two valid surface outputs PASS", t_two_valid_surface_outputs_pass)
    case("the no-op case: untouched good text passes, a rewrite fails",
         t_noop_case_guards_good_text)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
