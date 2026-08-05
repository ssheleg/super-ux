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


def fix_idempotent() -> None:
    """`--fix` clears what it claims to, and the second run has nothing left.

    A fixer that keeps finding work on an unchanged tree is either not
    fixing or not detecting, and both look identical from the outside.
    """
    global checks
    checks += 1
    files = {
        **MINIMAL,
        "strings.md": (
            MARKER + "\n"
            "| Key | Text (primary) | Location | Scenario | Status |\n"
            "|---|---|---|---|---|\n"
            "| button.save | Save Changes | src/a.ts:1 | SCN-001 | agreed |\n"
        ),
    }
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        brand = root / "docs" / "brand"
        brand.mkdir(parents=True)
        for rel, body in files.items():
            (brand / rel).write_text(body, encoding="utf-8")
        (root / "src").mkdir()
        (root / "src" / "a.ts").write_text("x\n", encoding="utf-8")

        before = {f.code for f in brand_lint.run(brand)}
        if before != {"B024"}:
            failures.append(f"fix: expected B024 before, got {sorted(before)}")
            return
        first = brand_lint.apply_fixes(brand, brand_lint.run(brand))
        after = {f.code for f in brand_lint.run(brand)}
        second = brand_lint.apply_fixes(brand, brand_lint.run(brand))
        if after:
            failures.append(f"fix: B024 survived --fix, got {sorted(after)}")
        if first < 1:
            failures.append("fix: first pass rewrote nothing")
        if second != 0:
            failures.append(f"fix: second pass rewrote {second} file(s)")


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

    marketing_sources = MARKER + (
        "\n\nSources:\n  ui: src/**/*.ts\n  marketing: content/**/*.md\n"
    )
    hero = (
        MARKER + "\n\n### landing hero\n\n```\n"
        "Register:   confidence +1\n"
        "Format:     one headline\n"
        "Limits:     title 60\n"
        "Forbidden:  physics: none | brand: none\n"
        "CTA:        one\n"
        "Proof:      one number, sourced\n"
        "Locales:    none\n"
        "```\n"
    )
    x_surface = (
        MARKER + "\n\n### X\n\n```\n"
        "Register:   density +1\n"
        "Format:     one idea\n"
        "Limits:     body 280\n"
        "Forbidden:  physics: link in body suppresses reach; max 2 hashtags"
        " | brand: none\n"
        "CTA:        first reply\n"
        "Proof:      none\n"
        "Locales:    none\n"
        "```\n"
    )
    sourced = (
        MARKER + "\n\n"
        "| Fact | Value | Source | Checked | Review by | Public |\n"
        "|---|---|---|---|---|---|\n"
        "| speed gain | 42% | bench/2026-08.md | 2026-08-01 | 2099-01-01 | yes |\n"
    )

    def page(surface: str, title: str, body: str) -> str:
        return f"---\nsurface: {surface}\ntitle: {title}\n---\n\n{body}\n"

    case(
        "number in public copy with no sourced fact",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B030"},
        project={"content/a.md": page("landing hero", "Faster", "We are 42% faster.")},
    )
    case(
        "the same number, sourced",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": sourced},
        set(),
        project={"content/a.md": page("landing hero", "Faster", "We are 42% faster.")},
    )
    case(
        "fact with no source",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": MARKER + "\n\n"
         "| Fact | Value | Source | Checked | Review by | Public |\n"
         "|---|---|---|---|---|---|\n"
         "| speed gain | 42% |  | 2026-08-01 | 2099-01-01 | yes |\n"},
        {"B031"},
        project={"content/a.md": page("landing hero", "Faster", "Hello.")},
    )
    case(
        "superlative with nothing to back it",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B032"},
        project={"content/a.md": page("landing hero", "Best", "The best platform for teams.")},
    )
    case(
        "title over the surface limit",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B040"},
        project={"content/a.md": page(
            "landing hero",
            "A headline that keeps going well past the sixty character limit set here",
            "Hello.")},
    )
    case(
        "link in the post body where physics forbids it",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": x_surface},
        {"B042"},
        project={"content/p.md": page("X", "Post", "Read https://example.com now.")},
    )
    case(
        "more hashtags than the surface allows",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": x_surface},
        {"B043"},
        project={"content/p.md": page("X", "Post", "Shipped #build #ship #now")},
    )

    store_sources = MARKER + (
        "\n\nSources:\n  ui: src/**/*.ts\n  store: store/**/*.md\n"
    )
    app_store = (
        MARKER + "\n\n### App Store\n\n```\n"
        "Register:   density +2\n"
        "Format:     title, subtitle, keyword field\n"
        "Limits:     title 30\n"
        "Forbidden:  physics: none | brand: none\n"
        "CTA:        none\n"
        "Proof:      rating\n"
        "Locales:    none\n"
        "```\n"
    )
    case(
        "iOS keyword field wastes the three ways it can",
        {**MINIMAL, "README.md": store_sources, "channels.md": app_store},
        {"B041"},
        project={"store/ios.md":
                 "---\nsurface: App Store\ntitle: MyTasks todo\n"
                 "keywords: task, tasks, todo\n---\n\nBody.\n"},
    )
    case(
        "the same field, written tight",
        {**MINIMAL, "README.md": store_sources, "channels.md": app_store},
        set(),
        project={"store/ios.md":
                 "---\nsurface: App Store\ntitle: MyTasks todo\n"
                 "keywords: task,checklist,reminder\n---\n\nBody.\n"},
    )

    ai_sources = MARKER + (
        "\n\nSources:\n  ui: src/**/*.ts\n  marketing: content/**/*.md\n"
        "  robots: public/robots.txt\n"
    )
    blog = (
        MARKER + "\nAI search: target\n\n### blog\n\n```\n"
        "Register:   distance -1\n"
        "Format:     long form\n"
        "Limits:     none\n"
        "Forbidden:  physics: none | brand: none\n"
        "CTA:        none\n"
        "Proof:      named author required\n"
        "Locales:    none\n"
        "```\n"
    )

    case(
        "AI search declared a target while the crawlers are blocked",
        {**MINIMAL, "README.md": ai_sources, "channels.md": blog},
        {"B050"},
        project={
            "public/robots.txt": "User-agent: GPTBot\nDisallow: /\n",
            "content/a.md": "---\nsurface: blog\nauthor: R. Iyer\n"
            "title: Post\n---\n\nA short post.\n",
        },
    )
    case(
        "keyword repeated past one percent of the document",
        {**MINIMAL, "README.md": ai_sources, "channels.md": blog},
        {"B051"},
        project={
            "public/robots.txt": "User-agent: *\nAllow: /\n",
            "content/a.md": "---\nsurface: blog\nauthor: R. Iyer\n"
            "title: Widgets\n---\n\n"
            + ("widgets " * 4 + "plus assorted filler content lines ") * 8,
        },
    )
    case(
        "filler opener",
        {**MINIMAL, "README.md": ai_sources, "channels.md": blog},
        {"B052"},
        project={
            "public/robots.txt": "User-agent: *\nAllow: /\n",
            "content/a.md": "---\nsurface: blog\nauthor: R. Iyer\ntitle: X\n"
            "---\n\nIn today's digital landscape, teams need clarity.\n",
        },
    )
    case(
        "claims with no named author where the surface requires one",
        {**MINIMAL, "README.md": ai_sources, "channels.md": blog},
        {"B053"},
        project={
            "public/robots.txt": "User-agent: *\nAllow: /\n",
            "content/a.md": "---\nsurface: blog\ntitle: X\n---\n\nA short post.\n",
        },
    )
    case(
        "humor on an error string",
        {**MINIMAL, "strings.md": registry(
            "| error.upload | Oops! that did not work 🙃 | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B061"},
        project={"src/a.ts": "x\n"},
    )

    multi = MINIMAL["voice.md"].replace(
        "Locales: en (primary)", "Locales: en (primary), de"
    )
    locale_sources = MARKER + (
        "\n\nSources:\n  ui: src/**/*.ts\n  locales: i18n/*.json\n"
    )
    de = (
        MARKER + "\nLocale: de\nPrimary: no\nAddress form: Sie\n"
        "Length coefficient: 1.30\n"
    )

    case(
        "declared locale with no locale file",
        {**MINIMAL, "voice.md": multi},
        {"B070"},
    )
    case(
        "locale parity below the declared threshold",
        {**MINIMAL, "voice.md": multi, "README.md": locale_sources,
         "locales/de.md": de},
        {"B071"},
        project={
            "i18n/en.json": '{"a":"1","b":"2","c":"3","d":"4"}',
            "i18n/de.json": '{"a":"1"}',
        },
    )
    case(
        "field overflows once the locale coefficient is applied",
        {**MINIMAL, "voice.md": multi, "channels.md": hero,
         "README.md": marketing_sources, "locales/de.md": de},
        {"B073"},
        project={"content/de.md":
                 "---\nsurface: landing hero\nlocale: de\n"
                 "title: " + "x" * 82 + "\n---\n\nHallo.\n"},
    )

    # B004 traces the voice back to the foundation, so the two contracts have
    # to agree on how a persona is numbered. They did not: the UX contract
    # writes P-NN and the brand template said PER-NN, which made a project
    # following our own template fail a blocking check while being correct.
    traced = MINIMAL["voice.md"].replace(
        "Derived-from: inferred", "Derived-from: P-01, JTBD-02"
    )
    foundation = "## Personas\n\n### P-01: the operator\n\n## Jobs\n\n### JTBD-02: ship\n"
    case(
        "Derived-from resolves against the foundation's own id scheme",
        {**MINIMAL, "voice.md": traced},
        set(),
        project={"docs/ux/foundation.md": foundation},
    )
    case(
        "Derived-from cites a persona the foundation does not have",
        {**MINIMAL, "voice.md": MINIMAL["voice.md"].replace(
            "Derived-from: inferred", "Derived-from: P-09")},
        {"B004"},
        project={"docs/ux/foundation.md": foundation},
    )

    fix_idempotent()

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} failure(s) out of {checks} checks")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
