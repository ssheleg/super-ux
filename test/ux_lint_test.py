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

VISION_OK = "\n".join(
    f"## {s}\n\nwritten\n" for s in ux_lint.VISION_SECTIONS
)


def screens(*entries: str, declaration: str | None = "no", index: bool = True) -> str:
    out = ["# UI Screen Registry", ""]
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
     {"vision.md": VISION_OK.replace("## 6. Anti-vision", "## 6. Antivision")},
     errors={"U030"}, root_files={"CLAUDE.md": RULE + "\n"})
silent("U030 clean on all nine sections",
       {"vision.md": VISION_OK}, {"U030"}, root_files={"CLAUDE.md": RULE + "\n"})

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


# --- the shipped template must pass from the first second ------------------

silent("the shipped screens template lints clean",
       {"screens.md": (ROOT / "templates" / "screens.md").read_text(encoding="utf-8")},
       {f"U{n:03d}" for n in range(1, 70)})

# Standing instruction #3: a new check runs against the seeded template before
# it runs against anything else. The requirement layer's two templates are all
# HTML comments by design, and `read()` strips those -- so a check that read the
# raw text would fail on every fresh install, which is the one habit this
# product cannot survive.
silent("the shipped scenarios template lints clean",
       {"scenarios.md": (ROOT / "templates" / "scenarios.md").read_text(encoding="utf-8")},
       {f"U{n:03d}" for n in range(1, 70)})
silent("the shipped foundation template lints clean",
       {"foundation.md": (ROOT / "templates" / "foundation.md").read_text(encoding="utf-8")},
       {f"U{n:03d}" for n in range(1, 70)})


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
