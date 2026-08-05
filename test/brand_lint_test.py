#!/usr/bin/env python3
"""Fixture-per-code tests for brand_lint.py (stdlib only).

One case per check code: it fires on the violation and stays silent on the
clean variant. A check that has never been watched fail against a planted
defect is not evidence, so every code here gets both halves.

Run: python3 test/brand_lint_test.py
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plugins/super-ux/scripts"))

import brand_lint  # noqa: E402

checks = 0
failures: list[str] = []

MARKER = "Contract: brand-contract v1"

MINIMAL = {
    "README.md": MARKER + "\n\nSources:\n  ui: src/**/*.ts\n",
    "voice.md": (
        MARKER + "\n"
        "Voice pack: operator-brief\n"
        "Locales: en (primary)\n"
        "Locale parity threshold: 80%\n"
        "Derived-from: inferred\n"
        "Status: validated\n"
        "Last calibrated: 2026-08-05\n"
    ),
    "terminology.md": MARKER + "\n",
    "facts.md": MARKER + "\n",
    "channels.md": MARKER + "\n",
    "strings.md": MARKER + "\n",
}


def case(name: str, files: dict, expect: set, project: dict | None = None) -> None:
    """Write a temp pack and compare the codes returned.

    `files` land inside the brand directory; `project` lands beside it, at
    the project root, which is where a `Location` column resolves from. A
    fixture that cites `src/a.ts:1` and does not plant it is testing B023
    whether it meant to or not -- so every fixture cites what it plants.
    """
    global checks
    checks += 1
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        brand = root / "docs" / "brand"
        brand.mkdir(parents=True)
        for rel, body in files.items():
            target = brand / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        for rel, body in (project or {}).items():
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        got = {f.code for f in brand_lint.run(brand)}
    if got != expect:
        failures.append(
            f"{name}: expected {sorted(expect)}, got {sorted(got)}"
        )


def main() -> int:
    case("clean minimal base", MINIMAL, set())

    case(
        "no Sources block",
        {**MINIMAL, "README.md": MARKER + "\n"},
        {"B006"},
    )
    case(
        "missing contract marker",
        {**MINIMAL, "voice.md": "Voice pack: operator-brief\n"},
        {"B001"},
    )
    case(
        "mixed contract versions",
        {**MINIMAL, "facts.md": "Contract: brand-contract v2\n"},
        {"B002"},
    )
    case(
        "voice draft while strings are agreed",
        {
            **MINIMAL,
            "voice.md": MINIMAL["voice.md"].replace(
                "Status: validated", "Status: draft"
            ),
            "strings.md": (
                MARKER + "\n"
                "| Key | Text (primary) | Location | Scenario | Status |\n"
                "|---|---|---|---|---|\n"
                "| a.b | Publish | src/a.ts:1 | SCN-001 | agreed |\n"
            ),
        },
        {"B003"}, project={"src/a.ts": "x\n"},
    )

    banned = (
        MARKER + "\n\n## Banned\n"
        "| Word or phrase | Why | Use instead |\n"
        "|---|---|---|\n"
        "| leverage | filler verb | use |\n"
    )
    terms = (
        MARKER + "\n\n## Product terms — always\n"
        "| Our term | Never write | Applies to |\n"
        "|---|---|---|\n"
        "| Run | Execution | what the product performs |\n"
    )
    entities = (
        MARKER + "\n\n## Entity and tier names — exact spelling\n"
        "| Name | Wrong forms seen |\n"
        "|---|---|\n"
        "| Pro | PRO, Pro plan |\n"
    )

    def registry(*rows: str) -> str:
        head = (
            MARKER + "\n"
            "| Key | Text (primary) | Location | Scenario | Status |\n"
            "|---|---|---|---|---|\n"
        )
        return head + "".join(rows)

    case(
        "banned word in an interface string",
        {**MINIMAL, "terminology.md": banned,
         "strings.md": registry(
             "| a.b | Leverage this | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B010"}, project={"src/a.ts": "x\n"},
    )
    case(
        "generic word where a product term exists",
        {**MINIMAL, "terminology.md": terms,
         "strings.md": registry(
             "| a.b | Start execution | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B011"}, project={"src/a.ts": "x\n"},
    )
    case(
        "entity name spelled inconsistently",
        {**MINIMAL, "terminology.md": entities,
         "strings.md": registry(
             "| a.b | Upgrade to Pro plan | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B012"}, project={"src/a.ts": "x\n"},
    )
    case(
        "one action, two names",
        {**MINIMAL, "strings.md": registry(
            "| action.publish | Publish | src/a.ts:1 | SCN-001 | agreed |\n",
            "| action.publish | Submit | src/b.ts:2 | SCN-001 | agreed |\n")},
        {"B020"}, project={"src/a.ts": "x\n", "src/b.ts": "x\n"},
    )
    case(
        "registry entry pointing at a vanished location",
        {**MINIMAL, "strings.md": registry(
            "| a.b | Publish | src/gone.ts:1 | SCN-001 | drifted |\n")},
        {"B023"},
    )
    case(
        "button label is not sentence case",
        {**MINIMAL, "strings.md": registry(
            "| button.save | Save Changes | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B024"}, project={"src/a.ts": "x\n"},
    )
    case(
        "button label is not a verb phrase",
        {**MINIMAL, "strings.md": registry(
            "| button.ok | OK | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B025"}, project={"src/a.ts": "x\n"},
    )

    case(
        "registry text is not the text in the code",
        {**MINIMAL, "strings.md": registry(
            "| a.b | Publish | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B021", "B022"},
        project={"src/a.ts": 'const label = "Submit";\n'},
    )
    case(
        "code string with no registry row",
        {**MINIMAL, "strings.md": registry(
            "| a.b | Publish | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B022"},
        project={"src/a.ts": 'const a = "Publish";\nconst b = "Archive";\n'},
    )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} failure(s) out of {checks} checks")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
