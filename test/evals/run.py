#!/usr/bin/env python3
"""Run the behaviour evals. Not part of CI, and that is deliberate.

`B-032`: every other gate in this repository verifies an artifact, and an
artifact is downstream of behaviour nobody measures. These cases run a brief
through an agent and read what comes back, which costs money and is not
deterministic -- two properties that make a required CI check something people
learn to re-run until it passes.

`validate.py` gates the SHAPE of `cases.json`: ids, anchors that still resolve,
a brief and an expectation per case. That much is deterministic. What the agent
does with the brief is what this script is for, and a human reads the verdict.

Outcome states are SEPARATE (FIX-UX-05.01) -- a process that died is not a
process whose output failed a substring check, and neither is a pass:

    PASS         exit 0 and every expectation met
    FAIL         exit 0, output read, expectations not met
    EXIT_ERROR   nonzero exit -- NEVER a pass, whatever stdout happens to say
    TIMEOUT      the agent never came back
    REFUSAL      exit 0 but the agent declined the brief
    SETUP_ERROR  nothing to run with (no CLI) -- not a pass either

Each case runs in an ISOLATED working directory, never the repository: an agent
told to write files must not leave them in this checkout. A manifest recording
command / exit / state / artifacts per case is written and its path printed.

    python3 test/evals/run.py              # every case
    python3 test/evals/run.py --case EV-02
    python3 test/evals/run.py --manifest out.json
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = Path(__file__).with_name("cases.json")

REFUSAL_MARKERS = ("i can't help", "i cannot help", "i won't", "i must decline",
                   "не могу помочь", "отказываюсь")


def classify(returncode: int, text: str, case: dict) -> tuple[str, list, list]:
    """One state per run, exit code FIRST: substring luck on a dead process is
    the defect this function exists to close."""
    if returncode != 0:
        return "EXIT_ERROR", [], []
    lowered = text.lower()
    if any(m in lowered for m in REFUSAL_MARKERS):
        return "REFUSAL", [], []
    missing = [e for e in case["expect"] if e.lower() not in lowered]
    present = [f for f in case.get("forbid", []) if f.lower() in lowered]
    if missing or present:
        return "FAIL", missing, present
    return "PASS", [], []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", help="run one case by id")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--manifest", help="where to write the run manifest "
                                       "(default: a temp file, path printed)")
    args = ap.parse_args()

    data = json.loads(CASES.read_text(encoding="utf-8"))
    cases = [c for c in data["cases"] if not args.case or c["id"] == args.case]
    if not cases:
        print(f"no case matching {args.case!r}", file=sys.stderr)
        return 2

    manifest_path = Path(args.manifest) if args.manifest else \
        Path(tempfile.mkstemp(prefix="evals-manifest-", suffix=".json")[1])
    manifest: list[dict] = []

    binary = shutil.which("claude")
    if not binary:
        print("the `claude` CLI is not on PATH -- these cases run a brief "
              "through an agent, so there is nothing to run them with. "
              "SETUP_ERROR, and this is not a pass.", file=sys.stderr)
        manifest.append({"state": "SETUP_ERROR", "command": ["claude"], "exit": None})
        manifest_path.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
        print(f"manifest: {manifest_path}", file=sys.stderr)
        return 2

    failed = 0
    for case in cases:
        print(f"\n=== {case['id']}: {case['measures']} ===")
        # ISOLATED: the agent works in a scratch directory, never this checkout.
        # Whatever files the brief makes it write stay here and are removed;
        # the repository is byte-identical before and after the run.
        workdir = Path(tempfile.mkdtemp(prefix=f"eval-{case['id']}-"))
        command = [binary, "-p", case["brief"]]
        started = time.time()
        try:
            out = subprocess.run(command, cwd=workdir, capture_output=True,
                                 text=True, timeout=args.timeout)
            state, missing, present = classify(out.returncode, out.stdout, case)
            exit_code: int | None = out.returncode
            text = out.stdout
        except subprocess.TimeoutExpired:
            state, missing, present, exit_code, text = "TIMEOUT", [], [], None, ""
        artifacts = sorted(str(p.relative_to(workdir))
                           for p in workdir.rglob("*") if p.is_file())
        manifest.append({
            "id": case["id"], "state": state, "command": command,
            "exit": exit_code, "artifacts": artifacts,
            "seconds": round(time.time() - started, 1),
        })
        shutil.rmtree(workdir, ignore_errors=True)

        if state == "PASS":
            print("  PASS")
        else:
            failed += 1
            print(f"  {state}")
            if missing:
                print(f"  MISSING  {missing}")
            if present:
                print(f"  FORBIDDEN {present}")
            if state in ("FAIL", "REFUSAL"):
                print(f"  --- output ---\n{text[:1200]}")

    manifest_path.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print(f"\n{len(cases) - failed}/{len(cases)} passed")
    print(f"manifest: {manifest_path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
