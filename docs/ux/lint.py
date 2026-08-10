#!/usr/bin/env python3
"""super-ux linter — checks a target project's docs/ux/ for integrity and drift.

Deterministic enforcement of the ux-contract: run it after any UX change and
before calling the work done, and wire it into the project's CI/pre-commit.
It turns the prose rules (same-change, no lost Figma, no orphans, no drift)
into a check that fails.

Usage:
  python3 docs/ux/lint.py            # lint ./docs/ux
  python3 docs/ux/lint.py <dir>      # lint <dir> (a docs/ux directory or its parent)
  python3 docs/ux/lint.py --strict   # warnings also fail (exit 1)

Exit codes: 0 clean (warnings allowed unless --strict), 1 problems found,
2 no UX docs at all (run /ux first). Stdlib only; tolerant parsing — reports
what it can and never crashes on malformed markdown.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ERRORS: list[str] = []
WARNS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def warn(msg: str) -> None:
    WARNS.append(msg)


def read(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    # Strip HTML comments so template examples (shipped commented-out) and
    # notes are never parsed as real entries.
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def find_ux_dir(arg: str | None) -> Path | None:
    base = Path(arg) if arg else Path.cwd()
    for cand in (base, base / "docs" / "ux", base.parent if base.name else base):
        if any((cand / n).exists() for n in ("scenarios.md", "foundation.md", "vision.md")):
            return cand
    return None


def ids(text: str, prefix: str) -> list[str]:
    """All '### PREFIX-NN:' entry ids, in order."""
    return re.findall(rf"^###\s+({prefix}-\d+):", text, re.MULTILINE)


def index_ids(text: str, prefix: str) -> set[str]:
    """Ids appearing in a leading '| PREFIX-NN |' index-table cell."""
    return set(re.findall(rf"^\|\s*({prefix}-\d+)\s*\|", text, re.MULTILINE))


def refs(text: str, prefix: str) -> set[str]:
    """Every PREFIX-NN token mentioned anywhere."""
    return set(re.findall(rf"\b({prefix}-\d+)\b", text))


def check_unique_and_gaps(entry_ids: list[str], label: str) -> None:
    seen: dict[str, int] = {}
    for i in entry_ids:
        seen[i] = seen.get(i, 0) + 1
    for i, n in seen.items():
        if n > 1:
            err(f"{label}: duplicate id {i} ({n} entries)")
    nums = sorted(int(i.split("-")[1]) for i in seen)
    if nums:
        missing = [n for n in range(1, max(nums) + 1) if n not in nums]
        if missing:
            warn(f"{label}: id gaps (retired entries should stay): {missing}")


def figma_enabled(foundation: str) -> bool | None:
    """True/False from foundation Design tooling; None if unstated (default-on)."""
    m = re.search(r"\*\*Figma:\*\*\s*(enabled|disabled)", foundation, re.IGNORECASE)
    if not m:
        return None
    return m.group(1).lower() == "enabled"


def screen_blocks(text: str) -> dict[str, str]:
    """Map SCR-id -> its section body (from its header to the next ### / ##)."""
    out: dict[str, str] = {}
    parts = re.split(r"^###\s+(SCR-\d+):", text, flags=re.MULTILINE)
    # parts = [pre, id1, body1, id2, body2, ...]
    for i in range(1, len(parts), 2):
        sid = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        body = re.split(r"^##\s", body, maxsplit=1, flags=re.MULTILINE)[0]
        out[sid] = body
    return out


VISION_SECTIONS = [
    "1. Essence",
    "2. Core idea",
    "3. What the system does",
    "4. The user's role",
    "5. Principles",
    "6. Anti-vision",
    "7. Horizon",
    "8. The one sentence",
    "9. The alignment test",
]

VISION_RULE_HEADING = "## Vision alignment — hard rule (super-ux)"
INSTRUCTION_FILES = ("CLAUDE.md", "AGENTS.md", "GEMINI.md")


def check_vision(ux: Path, vision: str) -> None:
    """The vision layer: all nine sections, and the rule that makes it read.

    A vision with no alignment rule in the project's instruction file is a
    document, not a constraint — and its absence looks exactly like
    compliance, which is why it is checked rather than trusted.
    """
    if not vision.strip():
        return
    for section in VISION_SECTIONS:
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", vision, re.MULTILINE):
            err(f"vision.md: missing section '## {section}'")
    # Emptiness is a defect only once the document claims to be finished.
    # A freshly seeded template is all headings and no content by design, and
    # a linter that fails on its own seed teaches people to skip the linter.
    approved = bool(re.search(r"\*\*Status:\*\*\s*approved", vision, re.IGNORECASE))
    if approved:
        for section in ("6. Anti-vision", "9. The alignment test"):
            body = re.split(rf"^##\s+{re.escape(section)}\s*$", vision, maxsplit=1,
                            flags=re.MULTILINE)
            if len(body) == 2:
                tail = re.split(r"^##\s", body[1], maxsplit=1, flags=re.MULTILINE)[0]
                if not tail.strip():
                    err(f"vision.md: approved but '## {section}' is empty — "
                        f"the section that settles arguments cannot be blank")

    root = ux.parent.parent if ux.name == "ux" else ux.parent
    present = [root / n for n in INSTRUCTION_FILES if (root / n).is_file()]
    if not present:
        warn("vision.md exists but the project has no CLAUDE.md / AGENTS.md / "
             "GEMINI.md — the alignment rule has nowhere to live")
        return
    if not any(VISION_RULE_HEADING in read(p) for p in present):
        warn(f"vision.md exists but no '{VISION_RULE_HEADING}' block in "
             f"{', '.join(p.name for p in present)} — nothing ever reads the vision "
             f"(run the `vision` skill's step 4)")


def check_links(ux: Path) -> None:
    link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    for md in sorted(ux.rglob("*.md")):
        text = read(md)
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            resolved = (md.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                warn(f"{md.name}: broken link -> {target}")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    strict = "--strict" in sys.argv[1:]
    ux = find_ux_dir(args[0] if args else None)
    if ux is None:
        print("no UX docs found (docs/ux/scenarios.md). Run /ux to set up.")
        return 2

    vision = read(ux / "vision.md")
    foundation = read(ux / "foundation.md")
    flows = read(ux / "flows.md")
    screens = read(ux / "screens.md")
    scenarios = read(ux / "scenarios.md")

    has_flows = bool(ids(flows, "FLW"))
    has_screens = bool(ids(screens, "SCR"))
    has_stories = bool(ids(foundation, "ST"))

    # --- ID integrity ---
    for text, pref, label in [
        (scenarios, "SCN", "scenarios.md"),
        (flows, "FLW", "flows.md"),
        (screens, "SCR", "screens.md"),
        (foundation, "ST", "foundation.md/stories"),
        (foundation, "JTBD", "foundation.md/jobs"),
    ]:
        entry_ids = ids(text, pref)
        if entry_ids:
            check_unique_and_gaps(entry_ids, label)

    # --- Index <-> entries sync (scenarios, screens) ---
    for text, pref, name in [(scenarios, "SCN", "scenarios.md"), (screens, "SCR", "screens.md")]:
        entries = set(ids(text, pref))
        if not entries:
            continue
        idx = index_ids(text, pref)
        for missing in sorted(entries - idx):
            warn(f"{name}: {missing} has no index row")
        for ghost in sorted(idx - entries):
            err(f"{name}: index lists {ghost} but no entry exists")

    # --- Flows reference existing screens ---
    if has_flows and has_screens:
        screen_ids = set(ids(screens, "SCR"))
        used = refs(flows, "SCR")
        for miss in sorted(used - screen_ids):
            err(f"flows.md references {miss} but screens.md has no such screen")
        for orphan in sorted(screen_ids - used):
            warn(f"screens.md: {orphan} is used by no flow (orphan)")

    # --- Scenario traces resolve ---
    if ids(scenarios, "SCN"):
        story_ids = set(ids(foundation, "ST"))
        flow_ids = set(ids(flows, "FLW"))
        traced_st = refs(scenarios, "ST")
        traced_flw = refs(scenarios, "FLW")
        if has_stories:
            for miss in sorted(traced_st - story_ids):
                warn(f"scenarios.md: traces to {miss} which is not in foundation.md")
        if has_flows:
            for miss in sorted(traced_flw - flow_ids):
                warn(f"scenarios.md: traces to {miss} which is not in flows.md")

    # --- must/should stories have a scenario ---
    if has_stories and ids(scenarios, "SCN"):
        traced = refs(scenarios, "ST")
        for m in re.finditer(r"^###\s+(ST-\d+):", foundation, re.MULTILINE):
            sid = m.group(1)
            # Only this story's own body: stop at the next heading, so a
            # neighbor's Priority line is never read as this story's.
            tail = re.split(r"^#{2,3}\s", foundation[m.end():], maxsplit=1, flags=re.MULTILINE)[0]
            if re.search(r"\*\*Priority:\*\*\s*(must|should)", tail, re.IGNORECASE):
                if sid not in traced:
                    warn(f"foundation.md: {sid} (must/should) has no scenario tracing to it")

    # --- Screen-level: Figma frames, coverage, drift status ---
    if has_screens:
        fig = figma_enabled(foundation)
        for sid, body in screen_blocks(screens).items():
            status_m = re.search(r"\*\*Status:\*\*\s*(designed|built|drifted|retired)", body)
            status = status_m.group(1) if status_m else None
            if status == "retired":
                continue
            # every state row present in the States table
            state_rows = re.findall(r"^\s*\|\s*(loading|empty|error|success)\s*\|(.*)\|\s*$",
                                    body, re.MULTILINE | re.IGNORECASE)
            if fig is not False:  # enabled or default-on
                for state, rest in state_rows:
                    cells = [c.strip() for c in rest.split("|")]
                    frame = cells[1] if len(cells) >= 2 else ""
                    if not frame or frame in ("-", "—", "<frame deep-link>", "<frame link>"):
                        err(f"screens.md: {sid} state '{state}' has no Figma frame link")
            cov_m = re.search(r"\*\*Coverage:\*\*\s*(.+)", body)
            cov = cov_m.group(1).strip() if cov_m else ""
            if status == "built" and (not cov or cov.lower().startswith("none")):
                warn(f"screens.md: {sid} is 'built' but has no Coverage")

    check_vision(ux, vision)
    check_links(ux)

    # --- Report ---
    for e in ERRORS:
        print(f"ERROR: {e}")
    for w in WARNS:
        print(f"warn:  {w}")
    total = len(ERRORS) + len(WARNS)
    if not total:
        print(f"OK — docs/ux is consistent ({ux})")
        return 0
    print(f"\n{len(ERRORS)} error(s), {len(WARNS)} warning(s)")
    if ERRORS or (strict and WARNS):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
