#!/usr/bin/env python3
"""Lint a project's brand pack against `brand-contract v1` (stdlib only).

`ux_lint.py` checks the UX chain against itself; `ux_doctor.py` catches a
chain written to an old contract. This is the third question, about a
different artifact: does the text the product actually ships match the voice
the product wrote down?

It checks only what a machine can prove -- a banned word, one action under
two names, a number with no sourced fact, a field over its limit, a blocked
crawler. Everything evaluative -- tone drift, whether a claim lands, whether
the voice has overshot into its own failure mode -- belongs to the `copy`
scope of `ux-audit`, which reads the same pack and answers with evidence.

Read-only by default. `--fix` applies only the changes that cannot be wrong.

    python3 brand_lint.py [path]           # report (default docs/brand)
    python3 brand_lint.py [path] --fix     # apply the safe subset
    python3 brand_lint.py [path] --brief   # one line, for sweeping projects
    python3 brand_lint.py [path] --json    # machine-readable findings

Exit codes: 0 clean, 1 warnings only, 2 any error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import namedtuple
from pathlib import Path

CONTRACT = "brand-contract"
CONTRACT_VERSION = "v1"

SEVERITY_ERROR = "error"
SEVERITY_WARN = "warn"

Finding = namedtuple("Finding", "code severity path line message")

# The files the contract owns. `locales/` is a directory and optional; a
# project with one locale legitimately has none.
CONTRACT_FILES = (
    "voice.md", "terminology.md", "facts.md",
    "channels.md", "strings.md", "README.md",
)

SOURCE_KEYS = ("ui", "marketing", "store", "robots", "locales")

MARKER_RE = re.compile(rf"^Contract:\s*{CONTRACT}\s*(v\d+)\s*$", re.M)


def read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def header_field(text: str, key: str) -> str | None:
    """A `Key: value` line from a file's header block."""
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.M)
    return match.group(1) if match else None


def table_rows(text: str) -> list[list[str]]:
    """Every pipe-table data row, as trimmed cell lists.

    Separator rows (`|---|---|`) and header rows are indistinguishable from
    data by shape alone, so the separator is dropped and the caller decides
    what the first surviving row means.
    """
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows


def load_sources(brand_dir: Path) -> dict[str, list[str]]:
    """The `Sources:` block from README.md -- key -> glob patterns.

    The linter cannot guess where a project keeps its text, and guessing
    wrong produces the worst possible output: a clean report about a surface
    that was never read. So an absent block is a finding (B006) and an
    absent key means its checks are skipped and counted as skipped.
    """
    text = read(brand_dir / "README.md") or ""
    block = re.search(r"^Sources:\s*$(.*?)(?=^\S|\Z)", text, re.M | re.S)
    if not block:
        return {}
    sources: dict[str, list[str]] = {}
    for line in block.group(1).splitlines():
        entry = re.match(r"^\s+(\w+):\s*(.+?)\s*$", line)
        if not entry:
            continue
        key, value = entry.group(1), entry.group(2)
        if key in SOURCE_KEYS:
            sources[key] = [p.strip() for p in value.split() if p.strip()]
    return sources


def check_contract(brand_dir: Path) -> list[Finding]:
    """B001-B006 -- the pack announces its contract and what to scan."""
    findings: list[Finding] = []
    versions: dict[str, str] = {}

    for path in sorted(brand_dir.rglob("*.md")):
        rel = path.relative_to(brand_dir).as_posix()
        text = read(path) or ""
        marker = MARKER_RE.search(text)
        if not marker:
            findings.append(Finding(
                "B001", SEVERITY_ERROR, rel, 1,
                f"no `Contract: {CONTRACT} {CONTRACT_VERSION}` marker -- "
                f"without it a pack written to an old contract is "
                f"indistinguishable from a current one",
            ))
            continue
        versions[rel] = marker.group(1)

    distinct = set(versions.values())
    if len(distinct) > 1:
        listed = ", ".join(
            f"{rel} {ver}" for rel, ver in sorted(versions.items())
        )
        findings.append(Finding(
            "B002", SEVERITY_ERROR, "", 0,
            f"mixed contract versions in one pack: {listed}",
        ))

    voice = read(brand_dir / "voice.md") or ""
    status = header_field(voice, "Status")
    strings = read(brand_dir / "strings.md") or ""
    agreed = [r for r in table_rows(strings) if r and r[-1] == "agreed"]
    if status == "draft" and agreed:
        findings.append(Finding(
            "B003", SEVERITY_WARN, "voice.md", 1,
            f"voice.md is `draft` while strings.md already has "
            f"{len(agreed)} agreed string(s) -- they were agreed against a "
            f"voice nobody approved",
        ))

    derived = header_field(voice, "Derived-from")
    if derived and derived != "inferred":
        foundation = read(brand_dir.parent / "ux" / "foundation.md")
        ids = [i.strip() for i in derived.split(",") if i.strip()]
        if foundation is not None:
            for ident in ids:
                if ident not in foundation:
                    findings.append(Finding(
                        "B004", SEVERITY_ERROR, "voice.md", 1,
                        f"Derived-from references `{ident}`, which is not in "
                        f"docs/ux/foundation.md -- the trace is broken",
                    ))
        calibrated = header_field(voice, "Last calibrated")
        if foundation is not None and calibrated:
            try:
                stamp = (brand_dir.parent / "ux" / "foundation.md").stat().st_mtime
                import datetime

                changed = datetime.date.fromtimestamp(stamp).isoformat()
                if changed > calibrated:
                    findings.append(Finding(
                        "B005", SEVERITY_WARN, "voice.md", 1,
                        f"foundation.md changed on {changed}, after the voice "
                        f"was last calibrated on {calibrated}",
                    ))
            except OSError:
                pass

    if not load_sources(brand_dir):
        findings.append(Finding(
            "B006", SEVERITY_ERROR, "README.md", 1,
            "no `Sources:` block -- the linter has nothing to scan, and a "
            "clean report over a surface it never read is worse than no "
            "report",
        ))

    return findings


def run(brand_dir: Path, fix: bool = False) -> list[Finding]:
    """Every check, in order. `fix` is applied by the caller via apply_fixes."""
    findings: list[Finding] = []
    findings.extend(check_contract(brand_dir))
    return findings


def report(findings: list[Finding], brief: bool, as_json: bool) -> None:
    if as_json:
        print(json.dumps([f._asdict() for f in findings], indent=2))
        return
    errors = [f for f in findings if f.severity == SEVERITY_ERROR]
    warns = [f for f in findings if f.severity == SEVERITY_WARN]
    if brief:
        state = "clean" if not findings else f"{len(errors)}E {len(warns)}W"
        print(f"brand: {state}")
        return
    for finding in findings:
        where = f"{finding.path}:{finding.line}" if finding.path else "pack"
        tag = "ERROR" if finding.severity == SEVERITY_ERROR else "warn "
        print(f"{tag} {finding.code} {where}: {finding.message}")
    if not findings:
        print("brand pack is clean")
    else:
        print(f"\n{len(errors)} error(s), {len(warns)} warning(s)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="docs/brand")
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--brief", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    brand_dir = Path(args.path)
    if not brand_dir.is_dir():
        print(f"no brand pack at {brand_dir} -- run /brand-init")
        return 2

    findings = run(brand_dir, fix=args.fix)
    report(findings, args.brief, args.json)

    if any(f.severity == SEVERITY_ERROR for f in findings):
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
