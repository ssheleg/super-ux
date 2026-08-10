#!/usr/bin/env python3
"""Fixture tests for ux_lint.py (stdlib only).

The brand linter has carried a fixture per check code since v0.30.0; the UX
linter — older, and the one every project actually runs — has carried none.
This file is that harness. It starts at the `Web surface:` block and grows
backwards; `docs/superpowers/backlog.md` → B-010 tracks the backfill for the
checks that predate it.

Each case writes a whole `docs/ux/` tree into a temp dir, runs the linter's
`main()` against it, and compares the errors and warnings it collected. A
check that has never been watched fail against a planted defect is not
evidence, so every case here plants one and every rule gets its clean twin.

Run: python3 test/ux_lint_test.py
"""

from __future__ import annotations

import io
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plugins/super-ux/scripts"))

import ux_lint  # noqa: E402

checks = 0
failures: list[str] = []

# The smallest tree the linter accepts as a project. `find_ux_dir` needs one
# of scenarios/foundation/vision to exist; everything else may be empty.
MINIMAL = {
    "scenarios.md": "# Scenarios\n",
    "foundation.md": "# Foundation\n",
    "flows.md": "# Flows\n",
    "screens.md": "# UI Screen Registry\n",
}

FULL_BLOCK = (
    "- **Web surface:**\n"
    "  - **Route:** /pricing\n"
    "  - **Answers:** what does it cost and what is in each tier\n"
    "  - **Indexable:** yes\n"
    "  - **Without JS:** the tier table and prices render in plain HTML\n"
    "  - **Entity:** schema.org/Product with Offer per tier\n"
)


def screens(declaration: str | None, *entries: str, index: bool = True) -> str:
    """Compose a screens.md with an optional Web surfaces declaration."""
    out = ["# UI Screen Registry", ""]
    if index:
        out += [
            "## Index",
            "",
            "| ID | Screen | Used by | Figma | Status | Coverage |",
            "|----|--------|---------|-------|--------|----------|",
        ]
        for i, _ in enumerate(entries, start=1):
            out.append(f"| SCR-{i:02d} | Screen {i} | — | — | designed | none yet |")
        out.append("")
    if declaration is not None:
        out += ["## Web surfaces", "", f"- **Web surfaces:** {declaration}", ""]
    out += ["## Screens", ""]
    for i, body in enumerate(entries, start=1):
        out += [f"### SCR-{i:02d}: Screen {i}", body, ""]
    return "\n".join(out) + "\n"


def case(name: str, files: dict, *, errors: set = frozenset(), warns: set = frozenset()) -> None:
    """Run the linter over a temp tree and compare the messages it kept.

    Matching is by substring so a fixture pins the defect, not the wording:
    a message reworded for clarity must not turn a real gate red.
    """
    global checks
    checks += 1
    with tempfile.TemporaryDirectory() as tmp:
        ux = Path(tmp) / "docs" / "ux"
        ux.mkdir(parents=True)
        for rel, body in {**MINIMAL, **files}.items():
            path = ux / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")

        ux_lint.ERRORS.clear()
        ux_lint.WARNS.clear()
        argv, stdout = sys.argv, sys.stdout
        sys.argv = ["ux_lint.py", str(ux)]
        sys.stdout = io.StringIO()  # the linter prints its own verdict per run
        try:
            ux_lint.main()
        finally:
            sys.argv, sys.stdout = argv, stdout
        got_e = list(ux_lint.ERRORS)
        got_w = list(ux_lint.WARNS)

    for fragment in errors:
        if not any(fragment in m for m in got_e):
            failures.append(f"{name}: expected an ERROR containing {fragment!r}; got {got_e}")
    for fragment in warns:
        if not any(fragment in m for m in got_w):
            failures.append(f"{name}: expected a WARNING containing {fragment!r}; got {got_w}")
    if not errors and not warns:
        # A clean case must be clean about *this* rule, not about everything —
        # the minimal tree legitimately warns about orphans and missing rules.
        noise = [m for m in got_e + got_w if "web surface" in m.lower()]
        if noise:
            failures.append(f"{name}: expected silence on web surfaces; got {noise}")


# --- the declaration ------------------------------------------------------

case(
    "no declaration at all warns",
    {"screens.md": screens(None, "- **Purpose:** something\n")},
    warns={"no **Web surfaces:** declaration"},
)

case(
    "declaration of no is silence",
    {"screens.md": screens("no", "- **Purpose:** something\n")},
)

case(
    "declaration of yes with no public screen warns",
    {"screens.md": screens("yes", "- **Purpose:** something\n")},
    warns={"declares web surfaces but no screen carries"},
)

case(
    "declaration of yes with a full block is silence",
    {"screens.md": screens("yes", "- **Purpose:** something\n" + FULL_BLOCK)},
)

case(
    "an unreadable declaration value warns",
    {"screens.md": screens("maybe later", "- **Purpose:** something\n")},
    warns={"no **Web surfaces:** declaration"},
)

# --- the block's five fields ---------------------------------------------

for missing in ("Route", "Answers", "Indexable", "Without JS", "Entity"):
    partial = "\n".join(
        line for line in FULL_BLOCK.strip().splitlines() if f"**{missing}:**" not in line
    ) + "\n"
    case(
        f"a block missing {missing} is an error",
        {"screens.md": screens("yes", "- **Purpose:** something\n" + partial)},
        errors={f"web surface block is missing **{missing}:**"},
    )

case(
    "a block under a no declaration contradicts it",
    {"screens.md": screens("no", "- **Purpose:** something\n" + FULL_BLOCK)},
    errors={"declares no web surfaces but SCR-01 carries"},
)

# --- the contradiction the declaration cannot hide ------------------------

case(
    "a URL entry point under a no declaration warns",
    {
        "screens.md": screens("no", "- **Purpose:** something\n"),
        "flows.md": (
            "# Flows\n\n### FLW-01: Buy\n"
            "- **Entry point:** https://example.com/pricing\n"
            "- **Screens traversed:** SCR-01\n"
        ),
    },
    warns={"flows.md: FLW-01 starts at a URL"},
)

case(
    "an in-app entry point under a no declaration is silence",
    {
        "screens.md": screens("no", "- **Purpose:** something\n"),
        "flows.md": (
            "# Flows\n\n### FLW-01: Buy\n"
            "- **Entry point:** the Projects screen, logged in\n"
            "- **Screens traversed:** SCR-01\n"
        ),
    },
)

# --- the template must pass from the first second (standing instruction 3) --

case(
    "the shipped template lints clean",
    {"screens.md": (ROOT / "templates" / "screens.md").read_text(encoding="utf-8")},
)


if failures:
    print(f"FAIL ({len(failures)} of {checks} checks)")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)
print(f"OK ({checks} checks)")
