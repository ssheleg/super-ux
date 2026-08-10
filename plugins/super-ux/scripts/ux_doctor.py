#!/usr/bin/env python3
"""Diagnose a project's UX chain against the current contract (stdlib only).

`ux_lint.py` checks a chain against itself -- ids, links, orphans. It cannot
tell you that the whole base is written to a contract three versions old,
because from the inside everything is consistent. That is the drift this
finds: between the project and the contract it was written to.

Read-only by default. `--fix` applies only the changes that cannot be wrong:
renaming a file the contract owns and stamping a marker onto an artifact whose
shape already matches. Everything else is reported for a human to decide.

    python3 ux_doctor.py [path]           # report
    python3 ux_doctor.py [path] --fix     # apply the safe subset
    python3 ux_doctor.py [path] --brief   # one line, for sweeping many projects
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CURRENT = 4

# What each contract version introduced, so a report can say what is missing
# rather than only that something is old.
HISTORY = {
    2: "`Traces:` on every scenario + traceability rules; `foundation.md` (personas, JTBD, journeys, stories)",
    3: "scenarios become use cases (`user action -> system response`), `Alt paths`, `Traces` includes `FLW-NN`; `flows.md`; `plans/`",
    4: "`screens.md` — one `SCR-NN` entry per screen with per-state Figma frames; flows reference screens by id instead of respecifying them",
}

# Additive since v4 — absence is not a version problem, but it is worth naming.
ADDITIVE = [
    ("foundation.md", "## Product mechanics", "Product mechanics section (personalization, engagement, a11y regime) — 0.26.1"),
    ("scenarios.md", "**Telemetry:**", "`Telemetry` on scenarios — the bridge to analytics practices, 0.28.0"),
    ("foundation.md", "**Kill criteria:**", "`Kill criteria` on stories — gives `dropped` a definition, 0.28.0"),
]

ARTIFACTS = ["vision.md", "foundation.md", "flows.md", "screens.md", "scenarios.md"]

# Names the contract owns, and the near-misses seen in the wild.
RENAMES = {
    "ux-scenarios.md": "scenarios.md",
    "ux-flows.md": "flows.md",
    "ux-foundation.md": "foundation.md",
    "ux-screens.md": "screens.md",
}


def find_ux_dir(arg: str | None) -> Path | None:
    base = Path(arg) if arg else Path.cwd()
    for cand in (base, base / "docs" / "ux", base.parent if base.name else base):
        if any((cand / a).exists() for a in ARTIFACTS) or (cand / "ux-scenarios.md").exists():
            return cand
    return None


def marker(path: Path) -> int | None:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    except OSError:
        return None
    m = re.search(r"ux-contract v(\d+)", head)
    return int(m.group(1)) if m else None


def diagnose(ux: Path) -> dict:
    present = {a: (ux / a).exists() for a in ARTIFACTS}
    markers = {a: marker(ux / a) for a in ARTIFACTS if present[a]}
    known = [v for v in markers.values() if v is not None]

    misnamed = {
        wrong: right
        for wrong, right in RENAMES.items()
        if (ux / wrong).exists() and not (ux / right).exists()
    }
    # Audit reports loose in docs/ux instead of docs/ux/audits/
    loose = sorted(
        p.name for p in ux.glob("*.md")
        if re.search(r"audit", p.name, re.I) and p.name not in ARTIFACTS
    )
    audits = sorted(p.name for p in (ux / "audits").glob("*.md")) if (ux / "audits").is_dir() else []

    missing_additive = []
    for fname, needle, label in ADDITIVE:
        f = ux / fname
        if f.exists() and needle not in f.read_text(encoding="utf-8", errors="ignore"):
            missing_additive.append(label)

    return {
        "present": present,
        "markers": markers,
        "effective": min(known) if known else None,
        "mixed": len(set(known)) > 1,
        "misnamed": misnamed,
        "loose_audits": loose,
        "audits": audits,
        "missing_additive": missing_additive,
    }


def report(ux: Path, d: dict) -> int:
    problems = 0
    print(f"docs/ux: {ux}")

    eff, markers = d["effective"], d["markers"]
    unmarked = [a for a, v in markers.items() if v is None]

    if d["mixed"]:
        problems += 1
        detail = ", ".join(f"{a} v{v}" for a, v in sorted(markers.items()) if v)
        print(f"  MIXED CONTRACT: {detail}")
        print("    Each artifact was last touched by a different version and nothing reconciled them.")
    elif eff is None:
        problems += 1
        print("  NO CONTRACT MARKER on any artifact — the chain is unmanaged.")
    elif eff < CURRENT:
        problems += 1
        print(f"  BEHIND: contract v{eff}, current v{CURRENT}")

    if unmarked and not d["mixed"]:
        problems += 1
        print(f"  UNMARKED: {', '.join(sorted(unmarked))}")

    lowest = eff if eff is not None else 1
    for v in range(lowest + 1, CURRENT + 1):
        if v in HISTORY:
            print(f"    v{v} added — {HISTORY[v]}")

    for wrong, right in d["misnamed"].items():
        problems += 1
        print(f"  MISNAMED: {wrong} -> {right}  (the tooling looks for the contract name and finds nothing)")

    missing_core = [a for a, ok in d["present"].items() if not ok]
    if missing_core:
        print(f"  ABSENT: {', '.join(missing_core)}")

    if d["loose_audits"]:
        problems += 1
        print(f"  AUDITS OUTSIDE audits/: {', '.join(d['loose_audits'])}")

    if d["audits"] and not d["present"].get("scenarios.md"):
        problems += 1
        print(f"  {len(d['audits'])} audit report(s) but no scenarios.md — audited against a base that is not there")

    for label in d["missing_additive"]:
        print(f"  optional, absent: {label}")

    print("  OK — on the current contract" if problems == 0 else f"  {problems} problem(s)")
    return problems


def fix(ux: Path, d: dict) -> list[str]:
    """Only the changes that cannot be wrong."""
    done = []
    for wrong, right in d["misnamed"].items():
        (ux / wrong).rename(ux / right)
        done.append(f"renamed {wrong} -> {right}")
    if d["loose_audits"]:
        (ux / "audits").mkdir(exist_ok=True)
        for name in d["loose_audits"]:
            (ux / name).rename(ux / "audits" / name)
            done.append(f"moved {name} -> audits/")
    return done


def brand_contract_state(root: Path) -> list[str]:
    """The brand pack's contract version, or why there is nothing to report.

    Same blind spot as the chain's: a pack written to an old contract is
    internally consistent, so `brand_lint.py` stays quiet about it. Only a
    marker comparison notices, which is why the doctor reads it too.
    """
    brand = root / "docs" / "brand"
    if not brand.is_dir():
        return []
    versions: dict[str, str] = {}
    unmarked: list[str] = []
    for path in sorted(brand.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        found = re.search(r"^Contract:\s*brand-contract\s*(v\d+)\s*$", text, re.M)
        rel = path.relative_to(brand).as_posix()
        if found:
            versions[rel] = found.group(1)
        else:
            unmarked.append(rel)
    out = []
    distinct = set(versions.values())
    if len(distinct) > 1:
        out.append(
            "docs/brand: mixed contract versions -- "
            + ", ".join(f"{k} {v}" for k, v in sorted(versions.items()))
        )
    elif distinct and distinct != {"v1"}:
        out.append(
            f"docs/brand: written to brand-contract {distinct.pop()}, current is v1"
        )
    if unmarked:
        out.append(
            "docs/brand: no contract marker on " + ", ".join(unmarked[:4])
        )
    return out


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ux = find_ux_dir(args[0] if args else None)
    if ux is None:
        print("no UX docs found (docs/ux/). Run /ux to set one up.")
        return 0

    d = diagnose(ux)
    if "--brief" in sys.argv:
        eff = d["effective"]
        state = "mixed" if d["mixed"] else (f"v{eff}" if eff else "unmarked")
        flags = []
        if d["misnamed"]:
            flags.append("misnamed")
        if d["loose_audits"]:
            flags.append("loose-audits")
        if d["audits"] and not d["present"].get("scenarios.md"):
            flags.append("audits-without-base")
        print(f"{ux}  {state}{'  ' + ','.join(flags) if flags else ''}")
        return 0

    problems = report(ux, d)

    brand = brand_contract_state(ux.parent.parent)
    if brand:
        print("\nBrand pack:")
        for line in brand:
            print(f"  {line}")
        problems = True

    if "--fix" in sys.argv:
        applied = fix(ux, d)
        print("\nApplied:" if applied else "\nNothing to apply automatically.")
        for line in applied:
            print(f"  {line}")
        if applied:
            print("  Re-run without --fix to see what is left for a human.")
    elif problems:
        print("\n  --fix applies the mechanical subset (renames, moving audit reports).")
        print("  Contract upgrades are content decisions: run /ux-update for those.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
