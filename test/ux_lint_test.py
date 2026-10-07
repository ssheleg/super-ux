#!/usr/bin/env python3
"""Fixture-per-code tests for ux_lint.py (stdlib only).

One case per code `U001..U054`: it fires on the violation and stays silent on
the clean variant. A check that has never been watched fail against a planted
defect is not evidence, so every code gets both halves.

`validate_ux_lint_coverage` in test/validate.py asks for each emitted code by
name here and in the contract, which is what stops this file falling behind the
linter the way it did between v0.16.0 and v0.33.0.

Run: python3 test/ux_lint_test.py
"""

from __future__ import annotations

import io
import re
import sys
import tempfile
from pathlib import Path

# A planted defect is this project's unit of evidence, and CPython's bytecode
# cache can defeat it. Invalidation compares (mtime, size), so a plant that
# swaps bytes without changing length -- `"B064"` for `"B999"` -- and is
# reverted inside the same second leaves a `.pyc` the interpreter considers
# current. The revert then runs the plant, and the transcript reports a defect
# that is no longer in the file. Measured on 2026-08-30, on exactly that pair.
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plugins/super-ux/scripts"))

import ux_lint  # noqa: E402

checks = 0
failures: list[str] = []

CODE_RE = re.compile(r"\[(U\d{3})\]")

RULE = "## Vision alignment — hard rule (super-ux)"

# The smallest tree the linter accepts as a project: `find_ux_dir` needs one of
# scenarios/foundation/vision, and every other file may be empty. `screens.md`
# carries the web-surface declaration so U050 does not fire in every case.
MINIMAL = {
    "scenarios.md": "# Scenarios\n",
    "foundation.md": "# Foundation\n",
    "flows.md": "# Flows\n",
    "screens.md": "# UI Screen Registry\n\n## Web surfaces\n\n- **Web surfaces:** no\n",
}

FULL_BLOCK = (
    "- **Web surface:**\n"
    "  - **Route:** /pricing\n"
    "  - **Answers:** what does it cost and what is in each tier\n"
    "  - **Indexable:** yes\n"
    "  - **Without JS:** the tier table and prices render in plain HTML\n"
    "  - **Entity:** schema.org/Product with Offer per tier\n"
)

# FIX-UX-07.01 — a section heading is `## <n>. <title>`; the id is the number.
def _vh(n):
    return f"{n}. {ux_lint.VISION_SECTION_TITLES[n]}"

VISION_OK = "\n".join(
    f"## {_vh(n)}\n\nwritten\n" for n in ux_lint.VISION_SECTION_IDS
)

# The shipped seed's exact shape: eight sections with nothing under them, and
# the ninth carrying the three `<question>` placeholders `templates/vision.md`
# actually ships. Anything that counts a placeholder as content goes silent
# here, which is how `U076` first failed to fire on the document it exists for.
VISION_SEEDED = "\n".join(
    f"## {_vh(n)}\n\n" for n in ux_lint.VISION_SECTION_IDS[:-1]
) + f"## {_vh(ux_lint.VISION_SECTION_IDS[-1])}\n\n1. <question>\n2. <question>\n"

VISION_ALL_PLACEHOLDER = "\n".join(
    f"## {_vh(n)}\n\n<to be written>\n" for n in ux_lint.VISION_SECTION_IDS
)


def screens(*entries: str, declaration: str | None = "no", index: bool = True,
            fmt: int = 1) -> str:
    out = ["# UI Screen Registry", ""]
    if fmt >= 2:
        out = ["<!-- screens-format: 2 -->"] + out
    if index:
        out += ["## Index", "",
                "| ID | Screen | Used by | Figma | Status | Coverage |",
                "|----|--------|---------|-------|--------|----------|"]
        for i, _ in enumerate(entries, start=1):
            out.append(f"| SCR-{i:02d} | Screen {i} | — | — | designed | none yet |")
        out.append("")
    if declaration is not None:
        out += ["## Web surfaces", "", f"- **Web surfaces:** {declaration}", ""]
    out += ["## Screens", ""]
    for i, body in enumerate(entries, start=1):
        out += [f"### SCR-{i:02d}: Screen {i}", body, ""]
    return "\n".join(out) + "\n"


def case(name: str, files: dict, *, errors: set = frozenset(),
         warns: set = frozenset(), root_files: dict | None = None) -> None:
    """Run the linter over a temp tree and compare the codes it emitted.

    Matching is by code, never by wording: a message reworded for clarity must
    not turn a real gate red, and a code that silently stops firing must.
    """
    global checks
    checks += 1
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ux = base / "docs" / "ux"
        ux.mkdir(parents=True)
        for rel, body in {**MINIMAL, **files}.items():
            path = ux / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        for rel, body in (root_files or {}).items():
            path = base / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")

        ux_lint.ERRORS.clear()
        ux_lint.WARNS.clear()
        argv, stdout = sys.argv, sys.stdout
        sys.argv = ["ux_lint.py", str(ux)]
        sys.stdout = io.StringIO()
        try:
            ux_lint.main()
        finally:
            sys.argv, sys.stdout = argv, stdout
        got_e = {c for m in ux_lint.ERRORS for c in CODE_RE.findall(m)}
        got_w = {c for m in ux_lint.WARNS for c in CODE_RE.findall(m)}

    if not errors <= got_e:
        failures.append(f"{name}: expected error(s) {sorted(errors - got_e)}, got {sorted(got_e)}")
    if not warns <= got_w:
        failures.append(f"{name}: expected warning(s) {sorted(warns - got_w)}, got {sorted(got_w)}")
    # Silence is asserted by `silent()`, which names the codes it forbids. A
    # case that named nothing would assert nothing, so it is a usage error.
    if not errors and not warns:
        failures.append(f"{name}: case() with no expected code — use silent()")


def silent(name: str, files: dict, codes: set, root_files: dict | None = None) -> None:
    """The clean twin: these codes must NOT fire on this tree."""
    global checks
    checks += 1
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ux = base / "docs" / "ux"
        ux.mkdir(parents=True)
        for rel, body in {**MINIMAL, **files}.items():
            path = ux / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        for rel, body in (root_files or {}).items():
            path = base / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        ux_lint.ERRORS.clear()
        ux_lint.WARNS.clear()
        argv, stdout = sys.argv, sys.stdout
        sys.argv = ["ux_lint.py", str(ux)]
        sys.stdout = io.StringIO()
        try:
            ux_lint.main()
        finally:
            sys.argv, sys.stdout = argv, stdout
        got = {c for m in ux_lint.ERRORS + ux_lint.WARNS for c in CODE_RE.findall(m)}
    fired = got & codes
    if fired:
        failures.append(f"{name}: expected silence on {sorted(fired)}, they fired")


# --- U001 / U002: id integrity -------------------------------------------

case("U001 duplicate scenario id",
     {"scenarios.md": "# S\n\n### SCN-001: a\nx\n\n### SCN-001: b\ny\n"},
     errors={"U001"})
silent("U001 clean on unique ids",
       {"scenarios.md": "# S\n\n### SCN-001: a\nx\n\n### SCN-002: b\ny\n"}, {"U001"})

case("U002 a gap in the id sequence",
     {"scenarios.md": "# S\n\n### SCN-001: a\nx\n\n### SCN-003: b\ny\n"},
     warns={"U002"})
silent("U002 clean on a contiguous sequence",
       {"scenarios.md": "# S\n\n### SCN-001: a\nx\n\n### SCN-002: b\ny\n"}, {"U002"})

# --- U003 / U004: index <-> entries ---------------------------------------

INDEXED = ("# S\n\n| ID | Name |\n|---|---|\n| SCN-001 | a |\n\n"
           "### SCN-001: a\nx\n")

case("U003 an entry with no index row",
     {"scenarios.md": "# S\n\n| ID | Name |\n|---|---|\n| SCN-001 | a |\n\n"
                      "### SCN-001: a\nx\n\n### SCN-002: b\ny\n"},
     warns={"U003"})
silent("U003 clean when every entry is indexed", {"scenarios.md": INDEXED}, {"U003"})

case("U004 an index row with no entry",
     {"scenarios.md": "# S\n\n| ID | Name |\n|---|---|\n| SCN-001 | a |\n| SCN-002 | ghost |\n\n"
                      "### SCN-001: a\nx\n"},
     errors={"U004"})
silent("U004 clean when the index has no ghost", {"scenarios.md": INDEXED}, {"U004"})

# --- U010 / U011: flows <-> screens ---------------------------------------

case("U010 a flow referencing a screen that does not exist",
     {"flows.md": "# F\n\n### FLW-01: a\n- **Screens traversed:** SCR-09\n",
      "screens.md": screens("- **Purpose:** p\n- **Status:** designed\n")},
     errors={"U010"})
silent("U010 clean when the referenced screen exists",
       {"flows.md": "# F\n\n### FLW-01: a\n- **Screens traversed:** SCR-01\n",
        "screens.md": screens("- **Purpose:** p\n- **Status:** designed\n")}, {"U010"})

case("U011 a screen no flow uses",
     {"flows.md": "# F\n\n### FLW-01: a\n- **Screens traversed:** SCR-01\n",
      "screens.md": screens("- **Purpose:** p\n- **Status:** designed\n",
                            "- **Purpose:** q\n- **Status:** designed\n")},
     warns={"U011"})

# --- U012 / U013 / U014: traceability -------------------------------------

case("U012 a scenario tracing to a story that is not in the foundation",
     {"scenarios.md": "# S\n\n### SCN-001: a\n- **Traces:** ST-009\n",
      "foundation.md": "# F\n\n### ST-001: a\n- **Priority:** could\n"},
     warns={"U012"})
silent("U012 clean when the story exists",
       {"scenarios.md": "# S\n\n### SCN-001: a\n- **Traces:** ST-001\n",
        "foundation.md": "# F\n\n### ST-001: a\n- **Priority:** could\n"}, {"U012"})

case("U013 a scenario tracing to a flow that does not exist",
     {"scenarios.md": "# S\n\n### SCN-001: a\n- **Traces:** FLW-09\n",
      "flows.md": "# F\n\n### FLW-01: a\n- **Screens traversed:** none\n"},
     warns={"U013"})

case("U014 a must story with no scenario tracing to it",
     {"scenarios.md": "# S\n\n### SCN-001: a\n- **Traces:** none\n",
      "foundation.md": "# F\n\n### ST-001: a\n- **Priority:** must\n"},
     warns={"U014"})
silent("U014 clean when the must story is traced",
       {"scenarios.md": "# S\n\n### SCN-001: a\n- **Traces:** ST-001\n",
        "foundation.md": "# F\n\n### ST-001: a\n- **Priority:** must\n"}, {"U014"})

# --- U020 / U021: screen states and coverage ------------------------------

STATES_EMPTY = ("- **Purpose:** p\n- **States:**\n"
                "  | State | Trigger | Figma frame | Behavior |\n"
                "  |---|---|---|---|\n"
                "  | error | fail | <frame deep-link> | message |\n"
                "- **Status:** designed\n")
STATES_LINKED = STATES_EMPTY.replace("<frame deep-link>", "https://figma.com/file/x?node-id=1")

case("U020 a state with no Figma frame while Figma is on",
     {"screens.md": screens(STATES_EMPTY)},
     errors={"U020"})
silent("U020 clean when the state carries a frame link",
       {"screens.md": screens(STATES_LINKED)}, {"U020"})
silent("U020 silent when Figma is disabled",
       {"screens.md": screens(STATES_EMPTY),
        "foundation.md": "# F\n\n**Figma:** disabled\n"}, {"U020"})

# U020 used to read only the four rows it had a name for (loading / empty /
# error / success), so a `keyboard-up` or `offline` row with an empty frame cell
# passed a project whose hard rule says every state has a frame. The column is
# found by its header now, not by its position after the state name.
def screens2(*entries: str, **kw) -> str:
    """A registry that opted into format 2: the matrix codes are errors here."""
    return screens(*entries, fmt=2, **kw)


STATES_NEW_NAME = STATES_EMPTY.replace("| error |", "| keyboard-up |")
case("U020 a state outside the old four still needs its frame",
     {"screens.md": screens2(STATES_NEW_NAME)},
     errors={"U020"})
silent("U020 clean when the new-name state carries its frame",
       {"screens.md": screens(STATES_NEW_NAME.replace(
           "<frame deep-link>", "https://figma.com/file/x?node-id=2"))}, {"U020"})

# --- U079 / U080 / U081: states and axes, the rows and columns of review ----
#
# The contact sheet a human approves has screen states for rows and render axes
# for columns, and both come from here. A screen with no state list gives the
# sheet no rows; one with no axes gives it no columns, and a reviewer then sees
# the happy path at one width in one theme and calls it the screen.

AXES_LINE = "- **Axes:** viewport: 375, 1280; theme: light, dark; text: default, 200%; locale: en, ar\n"
STATE_ROW_FIG = ("- **States:**\n"
                 "  | State | Trigger | Figma frame | Behavior |\n"
                 "  |---|---|---|---|\n"
                 "  | default | open | https://figma.com/file/x?node-id=1 | list |\n")
FIG_OFF = {"foundation.md": "# F\n\n**Figma:** disabled\n"}

case("U079 a screen with no state list",
     {"screens.md": screens2("- **Purpose:** p\n" + AXES_LINE + "- **Status:** designed\n")},
     errors={"U079"})
case("U079 still fires with Figma off: the list is required either way",
     {"screens.md": screens2("- **Purpose:** p\n" + AXES_LINE + "- **Status:** designed\n"),
      **FIG_OFF},
     errors={"U079"})
silent("U079 clean on a States table",
       {"screens.md": screens("- **Purpose:** p\n" + STATE_ROW_FIG + AXES_LINE
                              + "- **Status:** designed\n")}, {"U079"})
silent("U079 clean on an inline state list with Figma off",
       {"screens.md": screens("- **Purpose:** p\n- **States:** default, loading, error\n"
                              + AXES_LINE + "- **Status:** designed\n"), **FIG_OFF},
       {"U079", "U020"})
silent("U079 silent on a retired screen",
       {"screens.md": screens("- **Purpose:** p\n- **Status:** retired\n")}, {"U079", "U080"})

case("U080 a screen with no axes and no project default",
     {"screens.md": screens2("- **Purpose:** p\n" + STATE_ROW_FIG + "- **Status:** designed\n")},
     errors={"U080"})
case("U080 an axes line that omits one of the four",
     {"screens.md": screens2("- **Purpose:** p\n" + STATE_ROW_FIG
                            + "- **Axes:** viewport: 375; theme: light, dark; text: default\n"
                            + "- **Status:** designed\n")},
     errors={"U080"})
case("U080 a placeholder is not a value",
     {"screens.md": screens2("- **Purpose:** p\n" + STATE_ROW_FIG
                            + "- **Axes:** viewport: <widths>; theme: light; text: default; locale: en\n"
                            + "- **Status:** designed\n")},
     errors={"U080"})
silent("U080 clean when the screen declares all four",
       {"screens.md": screens("- **Purpose:** p\n" + STATE_ROW_FIG + AXES_LINE
                              + "- **Status:** designed\n")}, {"U080"})
silent("U080 reads a declaration wrapped over several lines",
       {"screens.md": screens("- **Purpose:** p\n" + STATE_ROW_FIG
                              + "- **Axes:** viewport: 375, 1280; theme: light, dark;\n"
                              + "  text: default, 200%; locale: en\n"
                              + "- **Status:** designed\n")}, {"U080"})
silent("U080 clean when the Design system sets the project default",
       {"screens.md": screens("- **Purpose:** p\n" + STATE_ROW_FIG + "- **Status:** designed\n")
        .replace("## Web surfaces", "## Design system\n\n" + AXES_LINE + "\n## Web surfaces")},
       {"U080"})

STATES_STORY = ("- **States:**\n"
                "  | State | Trigger | Figma frame | Story | Behavior |\n"
                "  |---|---|---|---|---|\n"
                "  | default | open | https://figma.com/file/x?node-id=1 | src/List.stories.tsx | list |\n"
                "  | empty | none | https://figma.com/file/x?node-id=2 | — | prompt |\n")
case("U081 a built screen's state with no story in its Story column",
     {"screens.md": screens2("- **Purpose:** p\n" + STATES_STORY + AXES_LINE
                            + "- **Coverage:** none yet\n- **Status:** built\n")},
     errors={"U081"})
silent("U081 clean when every state names its story",
       {"screens.md": screens("- **Purpose:** p\n"
                              + STATES_STORY.replace("| — |", "| src/List.stories.tsx#Empty |")
                              + AXES_LINE + "- **Coverage:** none yet\n- **Status:** built\n")},
       {"U081"})
silent("U081 silent before the build: a designed screen has no story yet",
       {"screens.md": screens("- **Purpose:** p\n" + STATES_STORY + AXES_LINE
                              + "- **Status:** designed\n")}, {"U081"})
silent("U081 reads a header as a word: `History` is not a Story column",
       {"screens.md": screens("- **Purpose:** p\n"
                              + STATES_STORY.replace("| Story |", "| History |")
                              + AXES_LINE + "- **Coverage:** none yet\n- **Status:** built\n")},
       {"U081"})
silent("U081 silent without a Story column: Figma-off projects keep the list only",
       {"screens.md": screens("- **Purpose:** p\n- **States:** default, empty\n" + AXES_LINE
                              + "- **Coverage:** none yet\n- **Status:** built\n"), **FIG_OFF},
       {"U081", "U020", "U079"})

# --- The migration: format 1 warns, format 2 fails --------------------------
#
# U079-U081 and the widened U020 arrived in 0.58.0 as errors on every registry,
# and 71 of the 80 passing `screens.md` files on the maintainer's machine went
# red on upgrade. A registry now opts in with `<!-- screens-format: 2 -->`, which the
# seed writes, so a new project is strict from its first line and an old one is
# told what to add without its CI breaking. These cases read the EXIT CODE as
# well as the codes, because "a warning" that still exits 1 is the same break.

def lint_tree(files: dict, root_files: dict | None = None) -> tuple[set, set, int]:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        ux = base / "docs" / "ux"
        ux.mkdir(parents=True)
        for rel, body in {**MINIMAL, **files}.items():
            (ux / rel).write_text(body, encoding="utf-8")
        for rel, body in (root_files or {}).items():
            path = base / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        ux_lint.ERRORS.clear()
        ux_lint.WARNS.clear()
        argv, stdout = sys.argv, sys.stdout
        sys.argv = ["ux_lint.py", str(ux)]
        sys.stdout = io.StringIO()
        try:
            rc = ux_lint.main()
        finally:
            sys.argv, sys.stdout = argv, stdout
        return ({c for m in ux_lint.ERRORS for c in CODE_RE.findall(m)},
                {c for m in ux_lint.WARNS for c in CODE_RE.findall(m)}, rc)


def migration(name: str, files: dict, *, warns: set = frozenset(),
              errors: set = frozenset(), not_errors: set = frozenset(),
              rc: int | None = None) -> None:
    global checks
    checks += 1
    got_e, got_w, got_rc = lint_tree(files)
    if not warns <= got_w:
        failures.append(f"{name}: expected warning(s) {sorted(warns - got_w)}, got {sorted(got_w)}")
    if not errors <= got_e:
        failures.append(f"{name}: expected error(s) {sorted(errors - got_e)}, got {sorted(got_e)}")
    if got_e & not_errors:
        failures.append(f"{name}: {sorted(got_e & not_errors)} fired as ERROR on a format-1 registry")
    if rc is not None and got_rc != rc:
        failures.append(f"{name}: exit {got_rc}, expected {rc} (errors {sorted(got_e)})")


LEGACY_STATES = ("- **Purpose:** p\n- **States:**\n"
                 "  | State | Trigger | Figma frame | Behavior |\n"
                 "  |---|---|---|---|\n"
                 "  | success | default | https://figma.com/file/x?node-id=1 | list |\n"
                 "  | error | fail | https://figma.com/file/x?node-id=2 | retry |\n"
                 "- **Status:** designed\n")
MATRIX = {"U079", "U080", "U081"}

migration("format 1: an old registry with no axes warns U080 and exits 0",
          {"screens.md": screens(LEGACY_STATES)},
          warns={"U080"}, not_errors=MATRIX | {"U020"}, rc=0)
migration("format 1: a screen with no state list warns U079 and exits 0",
          {"screens.md": screens("- **Purpose:** p\n- **Status:** designed\n")},
          warns={"U079", "U080"}, not_errors=MATRIX, rc=0)
migration("format 1: a frameless state the old rule never read warns, exits 0",
          {"screens.md": screens(STATES_NEW_NAME.replace("- **Status:**", AXES_LINE + "- **Status:**"))},
          warns={"U020"}, not_errors={"U020"}, rc=0)
migration("format 1: a built state with an empty Story cell warns U081, exits 0",
          {"screens.md": screens("- **Purpose:** p\n" + STATES_STORY + AXES_LINE
                                 + "- **Coverage:** none yet\n- **Status:** built\n")},
          warns={"U081"}, not_errors=MATRIX, rc=0)
migration("format 1: the old U020 — one of the four rows with no frame — still fails",
          {"screens.md": screens(STATES_EMPTY + AXES_LINE)},
          errors={"U020"}, rc=1)
migration("format 2: a marked registry missing axes fails U080",
          {"screens.md": screens2(LEGACY_STATES)},
          errors={"U080"}, rc=1)
migration("format 2: a marked registry with no state list fails U079",
          {"screens.md": screens2("- **Purpose:** p\n" + AXES_LINE + "- **Status:** designed\n")},
          errors={"U079"}, rc=1)

checks += 1
for seed in (ROOT / "templates" / "screens.md",
             ROOT / "plugins" / "super-ux" / "templates" / "screens.md"):
    if ux_lint.screens_format(seed) != 2:
        failures.append(f"the seed {seed.relative_to(ROOT)} does not carry "
                        f"`<!-- screens-format: 2 -->` — a new project would start lenient")
checks += 1
if ux_lint.screens_format(ROOT / "docs" / "ux" / "screens.md") != 2:
    failures.append("this repository's own screens.md is not on format 2 — the migration "
                    "the pack asks of others has not been done here")
# The migration is offered by the doctor -- the pack's existing "this chain is
# behind the contract" tool -- so a format-1 project is told what to add.
import ux_doctor  # noqa: E402


def doctor_says(screens_text: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        ux = Path(tmp) / "docs" / "ux"
        ux.mkdir(parents=True)
        (ux / "screens.md").write_text(screens_text, encoding="utf-8")
        out, stdout = io.StringIO(), sys.stdout
        sys.stdout = out
        try:
            ux_doctor.report(ux, ux_doctor.diagnose(ux))
        finally:
            sys.stdout = stdout
        return out.getvalue()


checks += 1
said = doctor_says(screens(LEGACY_STATES))
if "screens-format: 2" not in said or "Axes" not in said:
    failures.append("doctor: a format-1 screens.md is not offered the migration "
                    f"(Axes line, state lists, then the marker); it said: {said!r}")
checks += 1
said = doctor_says(screens2(LEGACY_STATES))
if "format 1" in said:
    failures.append("doctor: offers the format-2 migration to a registry already on it")

# --- U082 / U083 / U084: the onboarding budget (design-award R2) ----------------
#
# At most one onboarding screen stands between the entry and the first value.
# More is allowed only when the director record says why, and the linter can
# check that the record exists and talks about onboarding; it cannot judge the
# reason, which is the human's.

def flow(body: str, name: str = "Get started") -> str:
    return f"# Flows\n\n### FLW-01: {name}\n- **Goal:** g\n{body}"

case("U082 two onboarding screens and no budget record",
     {"flows.md": flow("- **Onboarding:** SCR-01, SCR-02\n- **First value:** SCR-03\n")},
     errors={"U082"})
case("U082 a budget record that does not exist",
     {"flows.md": flow("- **Onboarding:** SCR-01, SCR-02\n- **First value:** SCR-03\n"
                       "- **Onboarding budget:** docs/design/app/director-record.md\n")},
     errors={"U082"})
case("U082 a budget record that never mentions onboarding",
     {"flows.md": flow("- **Onboarding:** SCR-01, SCR-02\n- **First value:** SCR-03\n"
                       "- **Onboarding budget:** docs/design/app/director-record.md\n")},
     errors={"U082"},
     root_files={"docs/design/app/director-record.md": "# Record\n\n## Brief\n\ncalm\n"})
silent("U082 clean on one onboarding screen",
       {"flows.md": flow("- **Onboarding:** SCR-01\n- **First value:** SCR-02\n")}, {"U082"})
silent("U082 clean on two screens the director record justifies",
       {"flows.md": flow("- **Onboarding:** SCR-01, SCR-02\n- **First value:** SCR-03\n"
                         "- **Onboarding budget:** docs/design/app/director-record.md\n")},
       {"U082"},
       root_files={"docs/design/app/director-record.md":
                   "# Record\n\n## Open\n\nTwo onboarding screens: consent is a legal step.\n"})

case("U083 a flow named onboarding that declares no budget field",
     {"flows.md": flow("", name="First-run onboarding")},
     warns={"U083"})
silent("U083 clean once the flow declares its onboarding screens",
       {"flows.md": flow("- **Onboarding:** none\n- **First value:** SCR-01\n",
                         name="First-run onboarding")}, {"U083"})
silent("U083 silent on a flow that is not onboarding",
       {"flows.md": flow("", name="Export a report")}, {"U083"})

case("U084 an onboarding count with no first value to count against",
     {"flows.md": flow("- **Onboarding:** SCR-01\n")},
     warns={"U084"})
silent("U084 clean when the first value is named",
       {"flows.md": flow("- **Onboarding:** SCR-01\n- **First value:** SCR-02\n")}, {"U084"})

# --- U085: art direction is approved on a critique, and says which ----------

case("U085 art direction approved with no critique cited",
     {"flows.md": flow("- **Art direction:** approved 2026-10-07 by the owner\n")},
     errors={"U085"})
case("U085 a cited critique that does not resolve",
     {"flows.md": flow("- **Art direction:** approved 2026-10-07 — critique: "
                       "docs/design/app/director-record.md#critique\n")},
     errors={"U085"})
silent("U085 clean when the approval cites a critique that exists",
       {"flows.md": flow("- **Art direction:** approved 2026-10-07 — critique: "
                         "docs/design/app/director-record.md#critique\n")},
       {"U085"},
       root_files={"docs/design/app/director-record.md": "# R\n\n## Critique\n\nx\n"})
silent("U085 clean when the critique is a link the reader can open",
       {"flows.md": flow("- **Art direction:** approved — critique: "
                         "https://figma.com/file/x?node-id=9\n")}, {"U085"})
silent("U085 silent while art direction is pending",
       {"flows.md": flow("- **Art direction:** pending — two directions on the 2-up sheet\n")},
       {"U085"})

case("U021 a built screen with no coverage",
     {"screens.md": screens("- **Purpose:** p\n- **Coverage:** none yet\n"
                            "- **Status:** built\n")},
     warns={"U021"})
silent("U021 clean when a built screen names its code",
       {"screens.md": screens("- **Purpose:** p\n- **Coverage:** src/a.tsx:1\n"
                              "- **Status:** built\n")}, {"U021"})

# --- U055/U056: a Coverage claim is a claim about code ---------------------
#
# Both directions, per the standard: the defect each must catch, and the shapes
# each must NOT flag. The counter-cases are the expensive half here — a widened
# path pattern flagged three correct prose entries before it was narrowed.

case("U055 a partial claim that names no file",
     {"screens.md": screens("- **Purpose:** p\n- **Coverage:** partial — the route is built\n"
                            "- **Status:** built\n")},
     warns={"U055"})
silent("U055 clean when the claim cites a file",
       {"screens.md": screens("- **Purpose:** p\n- **Coverage:** partial — src/a.tsx\n"
                              "- **Status:** built\n")},
       {"U055"}, root_files={"src/a.tsx": "x\n"})
silent("U055 silent on `none`, which claims nothing about code",
       {"screens.md": screens("- **Purpose:** p\n- **Coverage:** none — not built yet\n"
                              "- **Status:** designed\n")}, {"U055"})
silent("U055 silent on a screen with no Coverage line at all",
       {"screens.md": screens("- **Purpose:** p\n- **Status:** designed\n")}, {"U055"})
silent("U055 silent on prose carrying a slash but no file",
       {"screens.md": screens("- **Purpose:** p\n"
                              "- **Coverage:** partial — client/server split, see src/a.tsx\n"
                              "- **Status:** built\n")},
       {"U055"}, root_files={"src/a.tsx": "x\n"})

case("U056 a cited file that does not exist",
     {"screens.md": screens("- **Purpose:** p\n- **Coverage:** full — src/gone.tsx\n"
                            "- **Status:** built\n")},
     errors={"U056"})
silent("U056 clean when the cited file exists",
       {"screens.md": screens("- **Purpose:** p\n- **Coverage:** full — src/a.tsx\n"
                              "- **Status:** built\n")},
       {"U056"}, root_files={"src/a.tsx": "x\n"})
# --- U057: a flow's verdict must be measurable, not inherited --------------

case("U057 a flow whose screens name no implementing file",
     {"flows.md": "# F\n\n### FLW-01: a\n- **Screens traversed:** SCR-01\n",
      "screens.md": screens("- **Used by:** FLW-01 (step 1)\n"
                            "- **Coverage:** partial — the route is built\n"
                            "- **Status:** built\n")},
     warns={"U057"})
silent("U057 clean when one of the flow's screens cites a file",
       {"flows.md": "# F\n\n### FLW-01: a\n- **Screens traversed:** SCR-01\n",
        "screens.md": screens("- **Used by:** FLW-01 (step 1)\n"
                              "- **Coverage:** full — src/a.tsx\n"
                              "- **Status:** built\n")},
       {"U057"}, root_files={"src/a.tsx": "x\n"})
silent("U057 silent on a flow that names no screen — that is U010's subject",
       {"flows.md": "# F\n\n### FLW-02: b\n- **Screens traversed:** SCR-01\n",
        "screens.md": screens("- **Used by:** FLW-02 (step 1)\n"
                              "- **Coverage:** full — src/a.tsx\n"
                              "- **Status:** built\n")},
       {"U057"}, root_files={"src/a.tsx": "x\n"})

silent("U056 tolerates a line suffix on the citation",
       {"screens.md": screens("- **Purpose:** p\n- **Coverage:** full — src/a.tsx:42\n"
                              "- **Status:** built\n")},
       {"U056"}, root_files={"src/a.tsx": "x\n"})

# --- U030..U033: the vision layer -----------------------------------------

case("U030 a vision missing one of the nine sections",
     # FIX-UX-07.01: renaming a title no longer removes a section (the NUMBER is
     # the id), so a truly missing section deletes `## 6.` and its body.
     {"vision.md": VISION_OK.replace("## 6. Anti-vision\n\nwritten\n", "")},
     errors={"U030"}, root_files={"CLAUDE.md": RULE + "\n"})
silent("U030 a section keeps its id when the title is localized",
       {"vision.md": VISION_OK.replace("## 6. Anti-vision", "## 6. Анти-видение")},
       {"U030"}, root_files={"CLAUDE.md": RULE + "\n"})
silent("U030 clean on all nine sections",
       {"vision.md": VISION_OK}, {"U030"}, root_files={"CLAUDE.md": RULE + "\n"})

# `B-005`: a seeded vision is nine headings over comments, and `read()` strips
# comments, so it passed every check until somebody self-declared `approved`.
# The placeholder pass matters as much as the emptiness one: section 9 ships
# three `<question>` lines, and counting those as content kept this check
# silent on the exact document it was written for.
# `B-028`: a range proves its bounds and nothing else. Both fixtures cite the
# same file with the same span; only the named subject differs, so the pair
# isolates the subject resolver from the bounds check that was already there.
case("U078 a citation naming a subject that is not in the span",
     {"screens.md": screens("- **Purpose:** p\n"
                            "- **Coverage:** `src/a.js:1-2 target`\n"
                            "- **Status:** built\n")},
     warns={"U078"}, root_files={"src/a.js": "const a = 1;\nconst b = 2;\nfunction target() {\n  return 3;\n}\n"})
silent("U078 silent when the subject is inside the span",
       {"screens.md": screens("- **Purpose:** p\n"
                              "- **Coverage:** `src/a.js:1-4 target`\n"
                              "- **Status:** built\n")},
       {"U078"}, root_files={"src/a.js": "const a = 1;\nconst b = 2;\nfunction target() {\n  return 3;\n}\n"})
silent("U078 silent when no subject is named, which is the old form",
       {"screens.md": screens("- **Purpose:** p\n"
                              "- **Coverage:** `src/a.js:1-2`\n"
                              "- **Status:** built\n")},
       {"U078"}, root_files={"src/a.js": "const a = 1;\nconst b = 2;\nfunction target() {\n  return 3;\n}\n"})

# `B-001`: the rule lives in a third place -- a target project's instruction
# file -- and until `U077` nothing there compared it to anything. The pair is
# the isolation: the same tree, the same rule, one word changed.
case("U077 an installed vision rule softened by hand",
     {"vision.md": VISION_OK},
     warns={"U077"},
     root_files={"CLAUDE.md": ux_lint.VISION_RULE_TEXT.replace(
         "Do not pick one silently.", "Use your judgement.") + "\n"})
silent("U077 silent on a faithful copy",
       {"vision.md": VISION_OK}, {"U077"},
       root_files={"CLAUDE.md": ux_lint.VISION_RULE_TEXT + "\n"})

case("U076 a vision that is still the seeded template",
     {"vision.md": VISION_SEEDED},
     warns={"U076"}, root_files={"CLAUDE.md": RULE + "\n"})
case("U076 a vision where every section is a placeholder",
     {"vision.md": VISION_ALL_PLACEHOLDER},
     warns={"U076"}, root_files={"CLAUDE.md": RULE + "\n"})
silent("U076 silent once one section is written",
       {"vision.md": VISION_SEEDED.replace(
           "## 1. Essence\n", "## 1. Essence\n\nA design chain.\n", 1)},
       {"U076"}, root_files={"CLAUDE.md": RULE + "\n"})
silent("U076 silent on a fully written vision",
       {"vision.md": VISION_OK}, {"U076"}, root_files={"CLAUDE.md": RULE + "\n"})

case("U034 a vision with a duplicate section id",
     {"vision.md": VISION_OK.replace(
         "## 6. Anti-vision\n\nwritten\n",
         "## 6. Anti-vision\n\nwritten\n## 6. Second Six\n\ndup\n")},
     errors={"U034"}, root_files={"CLAUDE.md": RULE + "\n"})
silent("U034 clean when every section id is unique",
       {"vision.md": VISION_OK}, {"U034"}, root_files={"CLAUDE.md": RULE + "\n"})
case("U031 an approved vision with an empty anti-vision",
     {"vision.md": VISION_OK.replace("## 6. Anti-vision\n\nwritten\n", "## 6. Anti-vision\n\n")
      + "\n**Status:** approved\n"},
     errors={"U031"}, root_files={"CLAUDE.md": RULE + "\n"})
silent("U031 silent while the vision is not approved",
       {"vision.md": VISION_OK.replace("## 6. Anti-vision\n\nwritten\n", "## 6. Anti-vision\n\n")},
       {"U031"}, root_files={"CLAUDE.md": RULE + "\n"})

case("U032 a vision with no instruction file to live in",
     {"vision.md": VISION_OK},
     warns={"U032"})

case("U033 an instruction file with no alignment rule",
     {"vision.md": VISION_OK},
     warns={"U033"}, root_files={"CLAUDE.md": "# Project\n"})
silent("U033 clean when the rule is installed",
       {"vision.md": VISION_OK}, {"U033"}, root_files={"CLAUDE.md": RULE + "\n"})

# --- U040: links -----------------------------------------------------------

case("U040 a link to a file that does not exist",
     {"scenarios.md": "# S\n\nsee [the flow](flows-gone.md)\n"},
     warns={"U040"})
silent("U040 clean when the link resolves",
       {"scenarios.md": "# S\n\nsee [the flow](flows.md)\n"}, {"U040"})

# --- U050..U054: the web surface ------------------------------------------

case("U050 no Web surfaces declaration",
     {"screens.md": screens("- **Purpose:** p\n- **Status:** designed\n", declaration=None)},
     warns={"U050"})
silent("U050 clean once the question is answered",
       {"screens.md": screens("- **Purpose:** p\n- **Status:** designed\n")}, {"U050"})

case("U051 a block under a declaration of no",
     {"screens.md": screens("- **Purpose:** p\n- **Status:** designed\n" + FULL_BLOCK)},
     errors={"U051"})

case("U052 a declaration of yes with no block anywhere",
     {"screens.md": screens("- **Purpose:** p\n- **Status:** designed\n", declaration="yes")},
     warns={"U052"})

for missing in ux_lint.WEB_SURFACE_FIELDS:
    partial = "\n".join(
        line for line in FULL_BLOCK.strip().splitlines() if f"**{missing}:**" not in line
    ) + "\n"
    case(f"U053 a block missing {missing}",
         {"screens.md": screens("- **Purpose:** p\n- **Status:** designed\n" + partial,
                                declaration="yes")},
         errors={"U053"})
silent("U053 clean on the complete block",
       {"screens.md": screens("- **Purpose:** p\n- **Status:** designed\n" + FULL_BLOCK,
                              declaration="yes")}, {"U053"})

case("U054 a flow starting at a URL under a declaration of no",
     {"flows.md": "# F\n\n### FLW-01: buy\n- **Entry point:** https://example.com/pricing\n"
                  "- **Screens traversed:** SCR-01\n",
      "screens.md": screens("- **Purpose:** p\n- **Status:** designed\n")},
     warns={"U054"})
silent("U054 clean on an in-app entry point",
       {"flows.md": "# F\n\n### FLW-01: buy\n- **Entry point:** the Projects screen\n"
                    "- **Screens traversed:** SCR-01\n",
        "screens.md": screens("- **Purpose:** p\n- **Status:** designed\n")}, {"U054"})

# --- U060..U065: a requirement with no observable is unfinished -------------
#
# The rule the requirement layer stated in prose and had no mechanism for: a
# scenario or a story that names no observable cannot be connected to evidence
# afterwards without inventing the test after reading the implementation. The
# screens layer below it got exactly this check (U055/U056); the layer that
# DEFINES the requirement did not, so `ux_lint.py` never opened a scenario body
# at all -- measured by grep: no rule read `Expected result`, `Acceptance
# criteria` or `Coverage` above the screens layer.
#
# Field spelling is deliberately tolerant (`Expected result` / `Expected`,
# `Acceptance criteria` / `Acceptance`): the question these codes ask is whether
# an observable EXISTS, and a rule that answered "the field is spelled the long
# way" would be a different rule wearing this one's number.


def scn(body: str, sid: str = "SCN-001") -> str:
    """A scenarios.md with one indexed entry -- the smallest shape U060 reads."""
    return (f"# Scenarios\n\n| ID | Title |\n|---|---|\n| {sid} | a |\n\n"
            f"### {sid}: a\n{body}")


def story(body: str, sid: str = "ST-001") -> str:
    """A foundation.md with one user story."""
    return f"# Foundation\n\n### {sid}: a\n{body}"


STEPS = "- **Steps:**\n  1. user acts -> system responds\n"

case("U060 an implemented scenario that states no observable",
     {"scenarios.md": scn(STEPS + "- **Status:** implemented\n"
                          "- **Coverage:** src/a.tsx\n")},
     errors={"U060"}, root_files={"src/a.tsx": "x\n"})
silent("U060 clean when the scenario states its expected result",
       {"scenarios.md": scn(STEPS + "- **Expected result:** the project appears in the sidebar\n"
                            "- **Status:** implemented\n- **Coverage:** src/a.tsx\n")},
       {"U060"}, root_files={"src/a.tsx": "x\n"})
silent("U060 accepts the short `Expected:` spelling this pack's own chain uses",
       {"scenarios.md": scn(STEPS + "- **Expected:** the project appears in the sidebar\n"
                            "- **Status:** implemented\n- **Coverage:** src/a.tsx\n")},
       {"U060"}, root_files={"src/a.tsx": "x\n"})
silent("U060 silent while the scenario is still a draft, which declares itself unfinished",
       {"scenarios.md": scn(STEPS + "- **Status:** draft\n")}, {"U060"})
silent("U060 silent on a retired scenario",
       {"scenarios.md": scn(STEPS + "- **Status:** retired\n")}, {"U060"})
case("U060 a placeholder standing in for an observable",
     {"scenarios.md": scn("- **Expected result:** <what the user observes on success>\n"
                          "- **Status:** validated\n")},
     errors={"U060"})

case("U061 a story that states no acceptance criteria",
     {"foundation.md": story("- **Story:** As P-01, I want x, so that y.\n"
                             "- **Priority:** could\n- **Status:** delivered\n")},
     errors={"U061"})
silent("U061 clean when the story carries Given/When/Then criteria",
       {"foundation.md": story("- **Story:** As P-01, I want x, so that y.\n"
                               "- **Acceptance criteria:**\n"
                               "  - Given a TTY, when I run it, then a list appears.\n"
                               "- **Priority:** could\n- **Status:** delivered\n")},
       {"U061", "U062"})
silent("U061 silent while the story is only proposed",
       {"foundation.md": story("- **Story:** As P-01, I want x, so that y.\n"
                               "- **Priority:** could\n- **Status:** proposed\n")},
       {"U061"})
case("U061 an acceptance field with nothing under it",
     {"foundation.md": story("- **Acceptance criteria:**\n"
                             "- **Priority:** could\n- **Status:** delivered\n")},
     errors={"U061"})

case("U062 acceptance criteria that state no observable outcome",
     {"foundation.md": story("- **Acceptance criteria:**\n"
                             "  - The installer is fast and the menu is legible.\n"
                             "- **Status:** delivered\n")},
     warns={"U062"})
silent("U062 accepts a criterion compressed to Given/then, the shape this pack writes",
       {"foundation.md": story("- **Acceptance:**\n"
                               "  - Given an existing rule file, then the line reads `skip:`.\n"
                               "- **Status:** delivered\n")},
       {"U062"})

IMPLEMENTED = "- **Expected result:** the project appears\n- **Status:** implemented\n"

case("U063 an implemented scenario naming no code",
     {"scenarios.md": scn(IMPLEMENTED)},
     warns={"U063"})
silent("U063 clean when the implemented scenario cites its code",
       {"scenarios.md": scn(IMPLEMENTED + "- **Coverage:** src/a.tsx:12\n")},
       {"U063"}, root_files={"src/a.tsx": "x\n"})
silent("U063 silent on a scenario that does not claim to be implemented",
       {"scenarios.md": scn("- **Expected result:** the project appears\n"
                            "- **Status:** validated\n")}, {"U063"})

case("U064 a scenario Coverage claim that names no file",
     {"scenarios.md": scn(IMPLEMENTED + "- **Coverage:** partial — the route is built\n")},
     warns={"U064"})
silent("U064 clean when the scenario claim cites a file",
       {"scenarios.md": scn(IMPLEMENTED + "- **Coverage:** partial — src/a.tsx\n")},
       {"U064"}, root_files={"src/a.tsx": "x\n"})
silent("U064 silent on `none`, which claims nothing about code",
       {"scenarios.md": scn("- **Expected result:** the project appears\n"
                            "- **Status:** draft\n- **Coverage:** none yet\n")}, {"U064"})

case("U065 a scenario citing a file that does not exist",
     {"scenarios.md": scn(IMPLEMENTED + "- **Coverage:** src/gone.tsx\n")},
     errors={"U065"})
silent("U065 clean when the cited file exists",
       {"scenarios.md": scn(IMPLEMENTED + "- **Coverage:** src/a.tsx:42\n")},
       {"U065"}, root_files={"src/a.tsx": "x\n"})


# --- U066..U070: the outcome state, and the enums that keep it readable ------
#
# Manifesto M-21: a change can be implementation-verified and product-
# unvalidated, and pretending delivery proof is outcome proof is not Proof of
# Done. Before this block the word `unobserved` appeared nowhere in the pack:
# `Status: implemented` was the only state a scenario had, and an audit PASS
# wrote it -- so a shipped scenario silently counted as a validated one and
# nothing could record whether the scenario was the right thing to build.
#
# `Product` has no floor and no target. Its absence is `unobserved`, which is
# the honest default, and every fixture below that leaves the field out asserts
# exactly that: silence. What is refused is a claim to hold outcome evidence
# that names none (U067), and delivery proof handed in wearing an outcome label
# (U068) -- a `file:line`, or an audit verdict. Those are the two artefacts an
# audit can produce, and neither of them is a user.

SCN_DONE = ("- **Expected result:** the project appears\n"
            "- **Status:** implemented\n- **Coverage:** src/a.tsx\n")
STORY_DONE = ("- **Acceptance criteria:**\n"
              "  - Given a TTY, when I run it, then a list appears.\n"
              "- **Status:** delivered\n")
SRC = {"src/a.tsx": "x\n"}

# --- U066: an out-of-enum product value is an error, never "no state" -------

case("U066 a product state outside its enum",
     {"scenarios.md": scn(SCN_DONE + "- **Product:** verified\n")},
     errors={"U066"}, root_files=SRC)
case("U066 a declared-but-empty product field, which names no evidence state",
     {"scenarios.md": scn(SCN_DONE + "- **Product:**\n")},
     errors={"U066"}, root_files=SRC)
case("U066 a story borrowing a word the product enum does not contain",
     {"foundation.md": story(STORY_DONE + "- **Product:** shipped\n")},
     errors={"U066"})
silent("U066 clean on `unobserved`, the honest default",
       {"scenarios.md": scn(SCN_DONE + "- **Product:** unobserved\n")},
       {"U066", "U067", "U068"}, root_files=SRC)
silent("U066 clean on `observed` carrying a signal from the world",
       {"scenarios.md": scn(SCN_DONE + "- **Product:** observed — 41% of installs "
                            "picked more than one channel (telemetry, 2026-09)\n")},
       {"U066", "U067", "U068"}, root_files=SRC)
silent("U066 clean on `contradicted`, which is information and not a failing gate",
       {"scenarios.md": scn(SCN_DONE + "- **Product:** contradicted — installs fell "
                            "9% against the previous release (telemetry, 2026-09)\n")},
       {"U066", "U067", "U068"}, root_files=SRC)
silent("U066 silent when the field is absent — absence IS unobserved, and no floor asks",
       {"scenarios.md": scn(SCN_DONE)},
       {"U066", "U067", "U068"}, root_files=SRC)
silent("U066 clean on a story carrying the field",
       {"foundation.md": story(STORY_DONE + "- **Product:** unobserved\n")},
       {"U066", "U067", "U068"})

# --- U067: an outcome claim that names no observation -----------------------
#
# Standing instruction #5: the fixture is written where only this branch can
# fire. `observed` with an empty signal cannot reach either U068 branch, because
# both are guarded on the signal being stated.

case("U067 an `observed` product state naming no signal",
     {"scenarios.md": scn(SCN_DONE + "- **Product:** observed\n")},
     errors={"U067"}, root_files=SRC)
case("U067 a `contradicted` product state naming no signal",
     {"scenarios.md": scn(SCN_DONE + "- **Product:** contradicted\n")},
     errors={"U067"}, root_files=SRC)
silent("U067 silent on `unobserved`, which claims no observation to name",
       {"scenarios.md": scn(SCN_DONE + "- **Product:** unobserved\n")},
       {"U067"}, root_files=SRC)
silent("U067 silent on a note beside `unobserved` — the state may carry prose",
       {"scenarios.md": scn(SCN_DONE + "- **Product:** unobserved — no telemetry "
                            "exists until the release ships\n")},
       {"U067"}, root_files=SRC)

# --- U068: delivery proof handed in wearing an outcome label -----------------
#
# The row's whole point, and the reason an audit PASS cannot promote this field:
# the two things an audit produces are a `file:line` and a verdict, and U068
# refuses both AS A SIGNAL. Each fixture is written so only its own branch can
# fire -- the citation case leaves nothing but paths, the verdict case leaves
# prose, so the path branch's guard is false there.

case("U068 a code citation offered as an outcome signal",
     {"scenarios.md": scn(SCN_DONE + "- **Product:** observed — src/a.tsx:12\n")},
     errors={"U068"}, root_files=SRC)
case("U068 a code citation with a line RANGE, the form this pack's own chain writes",
     {"scenarios.md": scn(SCN_DONE + "- **Product:** observed — "
                          "`src/a.tsx:235-296`\n")},
     errors={"U068"}, root_files=SRC)
case("U068 two citations and nothing else",
     {"scenarios.md": scn(SCN_DONE + "- **Product:** observed — "
                          "`src/a.tsx:12`, `src/b.tsx:1-9`\n")},
     errors={"U068"}, root_files=SRC)
case("U068 an audit verdict offered as an outcome signal",
     {"scenarios.md": scn(SCN_DONE + "- **Product:** observed — the audit of "
                          "2026-08-19 came back PASS on every step\n")},
     errors={"U068"}, root_files=SRC)
case("U068 a story promoting itself on a code citation",
     {"foundation.md": story(STORY_DONE + "- **Product:** contradicted — "
                             "src/a.tsx\n")},
     errors={"U068"}, root_files=SRC)
case("U068 the audit report itself, linked with prose around it",
     {"scenarios.md": scn(SCN_DONE + "- **Product:** observed — every step held, "
                          "see docs/ux/audits/2026-08-19.md\n")},
     errors={"U068"}, root_files=SRC)
silent("U068 clean when the signal is an observation and cites code beside it",
       {"scenarios.md": scn(SCN_DONE + "- **Product:** observed — 41% of installs "
                            "picked more than one channel, measured off the counter "
                            "in src/a.tsx\n")},
       {"U068"}, root_files=SRC)
silent("U068 silent on prose that merely passed, not a `PASS` verdict",
       {"scenarios.md": scn(SCN_DONE + "- **Product:** observed — every user in the "
                            "five-person test passed the step unaided\n")},
       {"U068"}, root_files=SRC)

# --- U069: the field vocabulary SU-01 left to be decided --------------------
#
# The long spelling is canonical: it is what the contract declares and what both
# shipped templates seed, so a fresh install writes it. The short forms stay
# READ (U060/U061 ask whether an observable exists, not how it is spelled) and
# become a warning, because an error here would fail every project already
# writing them -- the false positive that gets a family switched off.

case("U069 the short `Expected:` spelling, which the contract does not declare",
     {"scenarios.md": scn("- **Expected:** the project appears\n"
                          "- **Status:** validated\n")},
     warns={"U069"})
case("U069 the short `Acceptance:` spelling on a story",
     {"foundation.md": story("- **Acceptance:**\n"
                             "  - Given a TTY, when I run it, then a list appears.\n"
                             "- **Status:** delivered\n")},
     warns={"U069"})
silent("U069 clean on the canonical `Expected result:`",
       {"scenarios.md": scn("- **Expected result:** the project appears\n"
                            "- **Status:** validated\n")}, {"U069"})
silent("U069 clean on the canonical `Acceptance criteria:`",
       {"foundation.md": story(STORY_DONE)}, {"U069"})

# --- U070: a status outside its layer's enum ---------------------------------
#
# The drift was live in this file and had never been reported: the contract has
# declared five screen statuses since `blocked` was introduced -- with a rules
# paragraph of its own -- and the matcher listed four, so a `blocked` screen read
# as having NO status and U021 quietly stopped applying to it.

case("U070 a scenario status outside its enum",
     {"scenarios.md": scn("- **Expected result:** the project appears\n"
                          "- **Status:** shipped\n")},
     errors={"U070"})
case("U070 a story carrying the scenario layer's `implemented`",
     {"foundation.md": story("- **Acceptance criteria:**\n"
                             "  - Given a TTY, when I run it, then a list appears.\n"
                             "- **Status:** implemented\n")},
     errors={"U070"})
case("U070 a screen status outside its enum",
     {"screens.md": screens("- **Purpose:** p\n- **Status:** shipped\n")},
     errors={"U070"})
silent("U070 clean on `blocked`, the fifth screen status the matcher used to drop",
       {"screens.md": screens("- **Purpose:** p\n- **Status:** blocked — the "
                              "retention policy decides the copy; owner: founder\n")},
       {"U070"})
silent("U070 clean on each scenario status the enum declares",
       {"scenarios.md": (scn("- **Expected result:** a\n- **Status:** draft\n", "SCN-001")
                         + "\n### SCN-002: b\n- **Expected result:** b\n"
                           "- **Status:** validated\n"
                           "- **Coverage:** src/a.tsx\n"
                         + "\n### SCN-003: c\n- **Expected result:** c\n"
                           "- **Status:** implemented\n- **Coverage:** src/a.tsx\n"
                         + "\n### SCN-004: d\n- **Expected result:** d\n"
                           "- **Status:** retired\n")},
       {"U070"}, root_files=SRC)
silent("U070 silent when a status is not declared at all — a different rule's question",
       {"scenarios.md": scn("- **Expected result:** the project appears\n")},
       {"U070"})


# --- U071 / U072: a Coverage range resolved, not just its path ---------------
#
# B-004, open since 2026-08-10, and the plant that closed it: a citation was
# split on `:` and only the path was resolved, so the line numbers were
# decoration. `bin/super-ux.js:99000-99999` passed against a 396-line file and
# `python3 docs/ux/lint.py` printed `OK`, exit 0. Underneath it, seven live
# citations in this pack's own `screens.md` were pre-shift ranges — `SCR-01`
# pointed at 223-284 while `selectInteractive` had moved to 235-296, and
# `scenarios.md` had the same function right, so the two layers disagreed in
# writing and nothing compared them.

TEN_LINES = {"src/a.tsx": "".join(f"line {i}\n" for i in range(1, 11))}

case("U071 a screen cites a range past the end of the file",
     {"screens.md": screens("- **Purpose:** p\n- **Status:** built\n"
                            "- **Coverage:** `src/a.tsx:900-999`\n")},
     errors={"U071"}, root_files=TEN_LINES)
case("U071 a screen cites a single line the file does not have",
     {"screens.md": screens("- **Purpose:** p\n- **Status:** built\n"
                            "- **Coverage:** `src/a.tsx:11`\n")},
     errors={"U071"}, root_files=TEN_LINES)
case("U071 a range that ends before it starts is not a range",
     {"screens.md": screens("- **Purpose:** p\n- **Status:** built\n"
                            "- **Coverage:** `src/a.tsx:8-3`\n")},
     errors={"U071"}, root_files=TEN_LINES)
silent("U071 clean on a range the file has",
       {"screens.md": screens("- **Purpose:** p\n- **Status:** built\n"
                              "- **Coverage:** `src/a.tsx:3-7`\n")},
       {"U071"}, root_files=TEN_LINES)
silent("U071 clean on a citation with no line at all — U055's question, not this one",
       {"screens.md": screens("- **Purpose:** p\n- **Status:** built\n"
                              "- **Coverage:** `src/a.tsx`\n")},
       {"U071"}, root_files=TEN_LINES)
case("U072 a scenario cites a range past the end of the file",
     {"scenarios.md": scn("- **Expected result:** a\n- **Status:** implemented\n"
                          "- **Coverage:** `src/a.tsx:200-300`\n")},
     errors={"U072"}, root_files=TEN_LINES)
silent("U072 clean on a range the file has",
       {"scenarios.md": scn("- **Expected result:** a\n- **Status:** implemented\n"
                            "- **Coverage:** `src/a.tsx:1-10`\n")},
       {"U072"}, root_files=TEN_LINES)

# --- U073 / U074: the job layer, invisible until 2026-08-20 ------------------
#
# SU-03, and two defects that hid each other. `ids()` and `entry_blocks()`
# required `### PREFIX-NN:`; this pack's own three jobs are `### JTBD-01` with no
# name, so the matcher returned zero entries and NOT ONE rule in the linter
# applied to the layer — not id uniqueness, not the gap warning, not a required
# field. Watched: two identical `### JTBD-01` headers passed the whole gate,
# exit 0. Because the layer could not be seen, the missing `Success metric` on
# all three could not be reported either.

JOB_OK = ("- **Statement:** When x, I want y, so I can z.\n"
          "- **Personas:** P-01\n"
          "- **Type:** functional\n"
          "- **Forces:** push: a; pull: b; anxiety: c; habit: d\n"
          "- **Success metric:** the user stops doing x by hand\n")


def jobs(body: str, sid: str = "JTBD-01", named: bool = True) -> str:
    head = f"### {sid}: a job" if named else f"### {sid}"
    return f"# Foundation\n\n## Jobs to Be Done\n\n{head}\n{body}"


case("U073 a job header with the id alone", {"foundation.md": jobs(JOB_OK, named=False)},
     errors={"U073"})
case("U073 a persona header with the id alone",
     {"foundation.md": "# Foundation\n\n### P-01\nwho they are\n"}, errors={"U073"})
case("U073 a story header with the id alone",
     {"foundation.md": "# Foundation\n\n### ST-001\n" + STORY_DONE}, errors={"U073"})
case("U073 a scenario header with the id alone",
     {"scenarios.md": "# Scenarios\n\n| ID | Title |\n|---|---|\n| SCN-001 | a |\n\n### SCN-001\n- **Expected result:** a\n"}, errors={"U073"})
case("U073 a screen header with the id alone",
     {"screens.md": "# UI Screen Registry\n\n## Web surfaces\n\n- **Web surfaces:** no\n\n## Screens\n\n### SCR-01\n- **Purpose:** p\n"}, errors={"U073"})
case("U073 a flow header with the id alone",
     {"flows.md": "# Flows\n\n### FLW-01\n**Traces:** ST-001\n"}, errors={"U073"})
silent("U073 clean on the contract's named header",
       {"foundation.md": jobs(JOB_OK)}, {"U073"})
case("U074 a job with no Success metric",
     {"foundation.md": jobs(JOB_OK.replace(
         "- **Success metric:** the user stops doing x by hand\n", ""))},
     errors={"U074"})
case("U074 a job that is only a statement",
     {"foundation.md": jobs("- **Statement:** When x, I want y, so I can z.\n")},
     errors={"U074"})
silent("U074 clean on a job carrying all five fields",
       {"foundation.md": jobs(JOB_OK)}, {"U074"})
silent("U074 silent on a retired job — a retired record is not an unfinished one",
       {"foundation.md": jobs("- **Statement:** When x, I want y, so I can z.\n"
                              "- **Status:** retired\n")}, {"U074"})
case("U001 sees the job layer now: two entries under one id",
     {"foundation.md": (jobs(JOB_OK) + "\n### JTBD-01: another job\n" + JOB_OK)},
     errors={"U001"})

# --- U075: a Status on a layer the contract gives none ----------------------
#
# Nine live values sat outside every enum: `confirmed` on four flows and on two
# personas and three jobs, while the parity check's own regex accepted `SCN`,
# `ST` and `SCR` only. The personas and jobs got an enum; the flows did not,
# because a flow's coverage is measured through its screens (U057) and a status
# declared on it is exactly the inherited verdict that rule refuses.

case("U075 a flow declaring a status",
     {"flows.md": "# Flows\n\n### FLW-01: install\n**Status:** confirmed\n"},
     errors={"U075"})
case("U075 a journey declaring a status",
     {"foundation.md": "# Foundation\n\n### JRN-01: first install\n"
                       "**Status:** confirmed\n"},
     errors={"U075"})
silent("U075 clean on a flow that declares no status",
       {"flows.md": "# Flows\n\n### FLW-01: install\n**Traces:** ST-001\n"},
       {"U075"})
case("U070 reaches the persona layer it could not see before",
     {"foundation.md": "# Foundation\n\n### P-01: the operator\n"
                       "who they are. **Status:** shipped\n"},
     errors={"U070"})
case("U070 reaches the job layer too",
     {"foundation.md": jobs(JOB_OK + "- **Status:** shipped\n")}, errors={"U070"})
silent("U070 clean on `confirmed`, the value both foundation layers were using",
       {"foundation.md": "# Foundation\n\n### P-01: the operator\n"
                         "who they are. **Status:** confirmed\n"},
       {"U070"})
case("U070 a vision status outside `draft | approved`",
     {"vision.md": "# P — Vision\n\n**Status:** shipped\n\n" + VISION_OK},
     errors={"U070"}, root_files={"CLAUDE.md": RULE})
silent("U070 clean on an approved vision",
       {"vision.md": "# P — Vision\n\n**Status:** approved\n\n" + VISION_OK},
       {"U070"}, root_files={"CLAUDE.md": RULE})


# --- the shipped template must pass from the first second ------------------

silent("the shipped screens template lints clean",
       {"screens.md": (ROOT / "templates" / "screens.md").read_text(encoding="utf-8")},
       {f"U{n:03d}" for n in range(1, 100)})

# Standing instruction #3: a new check runs against the seeded template before
# it runs against anything else. The requirement layer's two templates are all
# HTML comments by design, and `read()` strips those -- so a check that read the
# raw text would fail on every fresh install, which is the one habit this
# product cannot survive.
silent("the shipped scenarios template lints clean",
       {"scenarios.md": (ROOT / "templates" / "scenarios.md").read_text(encoding="utf-8")},
       {f"U{n:03d}" for n in range(1, 100)})
silent("the shipped foundation template lints clean",
       {"foundation.md": (ROOT / "templates" / "foundation.md").read_text(encoding="utf-8")},
       {f"U{n:03d}" for n in range(1, 100)})


if failures:
    print(f"FAIL ({len(failures)} of {checks} checks)")
    for f in failures:
        print("  -", f)
    raise SystemExit(1)

# The ratchet, applied to the file that carries it. `test/floors.json` has held a
# floor for this script since v0.36.1 and nothing read it: `check_floor` was
# called for `validate.py` alone, so two of the three recorded floors were
# decorative and a deleted fixture would have dropped the count in silence —
# which is the exact failure the floors file exists to make impossible.
sys.path.insert(0, str(ROOT / "test"))
from validate import check_floor  # noqa: E402

rc = check_floor("ux_lint_test.py", checks)
if rc:
    raise SystemExit(rc)
print(f"OK ({checks} checks)")
