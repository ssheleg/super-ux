#!/usr/bin/env python3
"""FIX-UX-05.01 — runner outcome states: a dead process is never a PASS
(sherlock audit, UX-05).

The finding, reproduced live: test/evals/run.py never checked
subprocess.returncode and scored by substring — a stub that exits 1 while
printing the expected words got PASS/exit 0. And cases ran with cwd=ROOT, so an
agent told to write files polluted the repository fixture.

The fix under test, driving the REAL run.py with a fake `claude` on PATH:
* an exit-1 process whose stdout contains every expectation is EXIT_ERROR,
  never PASS (the runner exits 1);
* a refusal at exit 0 is REFUSAL, not FAIL-by-substring;
* PASS still works for exit 0 + expectations met;
* the repository is byte-identical before and after a run whose agent writes
  files (isolation), and those files appear in the manifest;
* the manifest records command / exit / state / artifacts per case.

Standard library only.
"""
import hashlib
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


def first_case_id_and_expect():
    data = json.loads(open(CASES, encoding="utf-8").read())
    c = data["cases"][0]
    return c["id"], c["expect"]


def fake_claude(behaviour, expects):
    """A fake `claude` CLI on PATH. behaviour: exit1-with-expected / pass /
    refuse / write-file."""
    d = tempfile.mkdtemp()
    lines = "\n".join(f'echo "{e}"' for e in expects)
    if behaviour == "exit1-with-expected":
        body = f"{lines}\nexit 1\n"
    elif behaviour == "pass":
        body = f"{lines}\nexit 0\n"
    elif behaviour == "refuse":
        body = 'echo "I cannot help with that."\nexit 0\n'
    elif behaviour == "write-file":
        body = f'echo "polluting" > agent-artifact.txt\n{lines}\nexit 0\n'
    path = os.path.join(d, "claude")
    with open(path, "w") as fh:
        fh.write("#!/bin/sh\n" + body)
    os.chmod(path, 0o755)
    return d


def run_runner(bindir, case_id, manifest):
    env = dict(os.environ, PATH=bindir + os.pathsep + os.environ.get("PATH", ""))
    return subprocess.run([sys.executable, RUN, "--case", case_id,
                           "--timeout", "30", "--manifest", manifest],
                          capture_output=True, text=True, timeout=120, env=env)


def t_exit1_with_expected_stdout_is_exit_error():
    cid, expects = first_case_id_and_expect()
    mf = tempfile.mkstemp(suffix=".json")[1]
    r = run_runner(fake_claude("exit1-with-expected", expects), cid, mf)
    assert r.returncode == 1, \
        f"an exit-1 process with lucky stdout passed the runner (exit {r.returncode}) — the finding"
    assert "EXIT_ERROR" in r.stdout, f"the state is not EXIT_ERROR:\n{r.stdout[-400:]}"
    man = json.loads(open(mf).read())
    assert man[0]["state"] == "EXIT_ERROR" and man[0]["exit"] == 1


def t_pass_still_passes():
    cid, expects = first_case_id_and_expect()
    mf = tempfile.mkstemp(suffix=".json")[1]
    r = run_runner(fake_claude("pass", expects), cid, mf)
    assert r.returncode == 0, f"a genuine pass failed:\n{r.stdout[-400:]}\n{r.stderr[-200:]}"
    man = json.loads(open(mf).read())
    assert man[0]["state"] == "PASS" and man[0]["exit"] == 0


def t_refusal_is_its_own_state():
    cid, _ = first_case_id_and_expect()
    mf = tempfile.mkstemp(suffix=".json")[1]
    r = run_runner(fake_claude("refuse", []), cid, mf)
    assert r.returncode == 1
    man = json.loads(open(mf).read())
    assert man[0]["state"] == "REFUSAL", f"a refusal was scored {man[0]['state']}"


def repo_digest():
    h = hashlib.sha256()
    out = subprocess.run(["git", "-C", ROOT, "status", "--porcelain"],
                         capture_output=True, text=True)
    h.update(out.stdout.encode())
    return h.hexdigest()


def t_repo_not_polluted_and_artifacts_in_manifest():
    cid, expects = first_case_id_and_expect()
    before = repo_digest()
    mf = tempfile.mkstemp(suffix=".json")[1]
    run_runner(fake_claude("write-file", expects), cid, mf)
    assert repo_digest() == before, "the run polluted the repository fixture"
    man = json.loads(open(mf).read())
    assert "agent-artifact.txt" in man[0]["artifacts"], \
        "the artifact the agent wrote is not in the manifest"
    assert man[0]["command"][0].endswith("claude"), "the manifest records no command"


def main():
    case("an exit-1 process with expected stdout is EXIT_ERROR, never PASS",
         t_exit1_with_expected_stdout_is_exit_error)
    case("a genuine pass still passes", t_pass_still_passes)
    case("a refusal is its own state", t_refusal_is_its_own_state)
    case("the repo is not polluted; artifacts land in the manifest",
         t_repo_not_polluted_and_artifacts_in_manifest)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
