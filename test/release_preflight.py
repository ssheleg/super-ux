#!/usr/bin/env python3
"""Refuse to tag a release from a tree the remote has already moved past.

Written after a real incident: a v0.27.0 tag was pushed from a base that
predated four released versions. `git push --follow-tags` is not atomic -- the
branch ref was rejected as non-fast-forward while the tag went through anyway,
so CI built a public release from a tree missing 0.26.2..0.26.5. Nothing about
that state looks wrong locally: the working tree is clean, the validator is
green, and the version numbers agree with each other.

Run before `git tag`. Exit 0 means the tag would carry everything the remote
has. Requires network for the fetch; that is the point.

    python3 test/release_preflight.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args: str) -> tuple[int, str]:
    p = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def main() -> int:
    problems: list[str] = []

    code, out = git("status", "--porcelain")
    if code == 0 and out:
        problems.append(f"working tree is not clean:\n{out}")

    code, out = git("fetch", "--quiet", "origin")
    if code != 0:
        problems.append(f"could not fetch origin -- run again with network: {out}")
    else:
        # The check the incident needed: does HEAD contain everything origin/main has?
        code, _ = git("merge-base", "--is-ancestor", "origin/main", "HEAD")
        if code != 0:
            _, behind = git("log", "--oneline", "HEAD..origin/main")
            problems.append(
                "HEAD does not contain origin/main -- tagging now would publish a tree "
                "missing work that is already released:\n" + behind
            )

    versions = {
        "package.json": json.loads((ROOT / "package.json").read_text())["version"],
        "plugin.json": json.loads(
            (ROOT / "plugins/super-ux/.claude-plugin/plugin.json").read_text()
        )["version"],
        "marketplace.json": json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text()
        )["plugins"][0]["version"],
    }
    changelog = re.search(r"^## (\d+\.\d+\.\d+)", (ROOT / "CHANGELOG.md").read_text(), re.M)
    versions["CHANGELOG.md"] = changelog.group(1) if changelog else "<none>"
    if len(set(versions.values())) != 1:
        problems.append(
            "version is not in sync across the four manifests: "
            + ", ".join(f"{k}={v}" for k, v in versions.items())
        )

    if problems:
        for p in problems:
            print(f"BLOCKED: {p}")
        print("\nDo not tag. Fix the above, re-run, then tag and push with --atomic.")
        return 1

    version = next(iter(versions.values()))
    print(f"OK -- safe to tag v{version}")
    print("Push branch and tag together: git push --atomic origin main v" + version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
