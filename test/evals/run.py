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

    python3 test/evals/run.py              # every case
    python3 test/evals/run.py --case EV-02
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = Path(__file__).with_name("cases.json")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", help="run one case by id")
    ap.add_argument("--timeout", type=int, default=300)
    args = ap.parse_args()

    data = json.loads(CASES.read_text(encoding="utf-8"))
    cases = [c for c in data["cases"] if not args.case or c["id"] == args.case]
    if not cases:
        print(f"no case matching {args.case!r}", file=sys.stderr)
        return 2

    binary = shutil.which("claude")
    if not binary:
        print("the `claude` CLI is not on PATH -- these cases run a brief "
              "through an agent, so there is nothing to run them with. This is "
              "not a pass.", file=sys.stderr)
        return 2

    failed = 0
    for case in cases:
        print(f"\n=== {case['id']}: {case['measures']} ===")
        try:
            out = subprocess.run(
                [binary, "-p", case["brief"]],
                cwd=ROOT, capture_output=True, text=True, timeout=args.timeout,
            )
        except subprocess.TimeoutExpired:
            print(f"  TIMEOUT after {args.timeout}s")
            failed += 1
            continue
        text = out.stdout
        missing = [e for e in case["expect"] if e.lower() not in text.lower()]
        present = [f for f in case.get("forbid", []) if f.lower() in text.lower()]
        if missing:
            print(f"  MISSING  {missing}")
        if present:
            print(f"  FORBIDDEN {present}")
        if missing or present:
            failed += 1
            print(f"  --- output ---\n{text[:1200]}")
        else:
            print("  PASS")

    print(f"\n{len(cases) - failed}/{len(cases)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
