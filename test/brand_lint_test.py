#!/usr/bin/env python3
"""Fixture-per-code tests for brand_lint.py (stdlib only).

One case per check code: it fires on the violation and stays silent on the
clean variant. A check that has never been watched fail against a planted
defect is not evidence, so every code here gets both halves.

Run: python3 test/brand_lint_test.py
"""

from __future__ import annotations

import datetime
import os
import shutil
import subprocess
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

import brand_lint  # noqa: E402

checks = 0
failures: list[str] = []

MARKER = "Contract: brand-contract v1"

TODAY = datetime.date.today().isoformat()

MINIMAL = {
    "README.md": MARKER + "\n\nSources:\n  ui: docs/brand/strings.md\n",
    "voice.md": (
        MARKER + "\n"
        "Voice pack: operator-brief\n"
        "Locales: en (primary)\n"
        "Locale parity threshold: 80%\n"
        "Derived-from: inferred\n"
        "Status: validated\n"
        "Humanization: on\n"
        # B005 compares foundation.md's MTIME against this date, and a
        # fixture's files are always written now. A hardcoded date here is a
        # time bomb: this suite was green on 2026-08-05 and red on 2026-08-06
        # with no code change. Calibrate "today" so the baseline cannot expire.
        f"Last calibrated: {TODAY}\n"
        "\n## Voice references\n"
        "- **Admired:** Stripe docs — every claim has a runnable example\n"
        "- **Refused:** an outage page that is cheerful about it\n"
    ),
    "terminology.md": MARKER + "\n",
    "facts.md": MARKER + "\n",
    "channels.md": MARKER + "\n",
    "strings.md": MARKER + "\n",
}


# The four states of the humanization field, each derived from the well-formed
# pack above so that nothing but the field itself differs. A fixture that built
# its own voice.md would drift from MINIMAL and start proving something else.
_VOICE = MINIMAL["voice.md"]
voice_no_humanization = _VOICE.replace("Humanization: on\n", "")
voice_humanization_bad = _VOICE.replace("Humanization: on", "Humanization: sometimes")
voice_humanization_off = _VOICE.replace("Humanization: on", "Humanization: off")
voice_humanization_declined = _VOICE.replace(
    "Humanization: on",
    "Humanization: off\n"
    "Humanization declined: 2026-08-30, every string on this surface is fixed "
    "by counsel and may not be reworded",
)


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
        # Fixtures that declare TypeScript sources need an actual source. The
        # empty-source error has separate negative fixtures; avoid testing it
        # incidentally in every unrelated brand-code case.
        (root / "src").mkdir()
        (root / "src/fixture.ts").write_text("// fixture source\n")
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


def git_date_beats_mtime() -> None:
    """B005 dates a file by its commit, not by when it landed on this disk.

    A fresh clone stamps every file's mtime with the checkout time, so an
    mtime answer says "changed today" about a file nobody has touched. That
    is not hypothetical: it turned this project's own CI red the first run
    after `docs/brand/lint.py` was added to the workflow, on a pack that was
    clean locally and clean in fact.

    The fixture commits `foundation.md` with a back-dated commit and a
    deliberately fresh mtime. Under git, no finding. Under mtime, `B005`.
    """
    global checks
    checks += 1
    git = shutil.which("git")
    if not git:
        return
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        brand = root / "docs" / "brand"
        brand.mkdir(parents=True)
        files = {**MINIMAL, "voice.md": MINIMAL["voice.md"]
                 .replace("Derived-from: inferred", "Derived-from: P-01")
                 .replace(f"Last calibrated: {TODAY}", "Last calibrated: 2020-06-01")}
        for rel, body in files.items():
            (brand / rel).write_text(body, encoding="utf-8")
        ux = root / "docs" / "ux"
        ux.mkdir(parents=True)
        (ux / "foundation.md").write_text("### P-01: the operator\n", encoding="utf-8")

        env = {
            **os.environ,
            "GIT_AUTHOR_DATE": "2020-01-01T00:00:00",
            "GIT_COMMITTER_DATE": "2020-01-01T00:00:00",
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
        }
        run = lambda *a: subprocess.run(
            [git, *a], cwd=root, env=env, capture_output=True, text=True)
        run("init", "-q")
        run("add", "-A")
        result = run("commit", "-q", "-m", "seed")
        if result.returncode != 0:
            failures.append(f"git fixture: commit failed -- {result.stderr.strip()[:120]}")
            return

        # The mtime says now; the commit says 2020-01-01, before the voice was
        # calibrated on 2020-06-01. Only one of those answers is right.
        (ux / "foundation.md").touch()
        got = {f.code for f in brand_lint.run(brand)}
    if got:
        failures.append(
            f"git date: expected no finding from a 2020-01-01 commit against a "
            f"2020-06-01 calibration, got {sorted(got)}"
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


SOCIAL_SOURCES = MARKER + (
    "\n\nSources:\n  ui: src/**/*.ts\n  marketing: content/**/*.md\n"
)

SHORT_VIDEO = (
    MARKER + "\n\n### short video\n\n```\n"
    "Register:   distance -1\n"
    "Format:     hook, body, one ask; spoken line and on-screen text written apart\n"
    "Limits:     none\n"
    "Forbidden:  physics: none | brand: none\n"
    "CTA:        one\n"
    "Proof:      one sourced figure\n"
    "Locales:    none\n"
    "```\n"
)

INSTAGRAM = (
    MARKER + "\n\n### Instagram\n\n```\n"
    "Register:   distance -1\n"
    "Format:     a caption; the first line is what the feed shows\n"
    "Limits:     body 2200\n"
    "Forbidden:  physics: link in body, max 5 hashtags, fold 125, one ask"
    " | brand: none\n"
    "CTA:        one\n"
    "Proof:      none\n"
    "Locales:    none\n"
    "```\n"
)

# The hook figure is public copy like any other, so the fixtures that use it
# carry its row. Without the row the hook is a B030, which one case asserts.
HOOK_FACTS = (
    MARKER + "\n\n"
    "| Fact | Value | Source | Checked | Review by | Public |\n"
    "|---|---|---|---|---|---|\n"
    f"| forgotten subscription spend | $400 | billing export | {TODAY} "
    "| 2099-01-01 | yes |\n"
)

STRONG_HOOK = "You lose $400 a month to one subscription you forgot."


def reel(fields: dict, body: str = "Open the bank app and sort by date.") -> dict:
    head = "".join(f"{k}: {v}\n" for k, v in {"surface": "short video",
                                             "title": "Reel", **fields}.items())
    return {"content/r.md": f"---\n{head}---\n\n{body}\n"}


def short_video_cases() -> None:
    """B044 -- the hook filter. A filter, never a predictor (hooks.md).

    Every dealbreaker fixture is built on a hook that otherwise scores above
    the WEAK line, so the end-to-end code can only have come from the
    dealbreaker branch; the unit checks below then assert WHICH branch fired,
    because a set of codes proves the code arrived and not why (retro #5).
    """
    global checks
    pack = {**MINIMAL, "README.md": SOCIAL_SOURCES, "channels.md": SHORT_VIDEO,
            "facts.md": HOOK_FACTS}

    case("B044 silent on a hook that passes the filter",
         pack, set(), project=reel({"hook": STRONG_HOOK,
                                    "on-screen": "$400 A MONTH, GONE"}))
    case("B044 fires on a hook the five checks call WEAK",
         pack, {"B044"},
         project=reel({"hook": "So today I wanted to talk about some things"}))
    case("B044 reads every numbered hook variant, not only the first",
         pack, {"B044"},
         project=reel({"hook": STRONG_HOOK,
                       "hook-2": "So today I wanted to talk about some things"}))
    case("B044 fires on on-screen text longer than ten words",
         pack, {"B044"},
         project=reel({"hook": STRONG_HOOK,
                       "on-screen": "this is a very long line of on screen "
                                    "text that nobody will read"}))
    dealbreakers = {
        "stop-scrolling": "Stop scrolling: you lose $400 a month to one subscription.",
        "preamble": "You lose $400 a month, and I'll show you how to stop it.",
        "greeting": "Hey, you lose $400 a month to one subscription.",
        "hashtag": "You lose $400 a month to one subscription #money",
        "emoji": "You lose $400 a month to one subscription \U0001F4B8",
    }
    for flag, hook in dealbreakers.items():
        case(f"B044 dealbreaker `{flag}` fires on its own",
             pack, {"B044"}, project=reel({"hook": hook}))
        checks += 1
        got = brand_lint.hook_score(hook)
        if flag not in got["flags"] or got["verdict"] == "WEAK":
            failures.append(
                f"hook_score: `{flag}` should be the only reason this hook is "
                f"filtered, got verdict {got['verdict']} flags {got['flags']}")

    checks += 1
    strong = brand_lint.hook_score(STRONG_HOOK)
    if strong["verdict"] != "STRONG" or strong["flags"]:
        failures.append(f"hook_score: the strong hook scored {strong}")
    checks += 1
    weak = brand_lint.hook_score("So today I wanted to talk about some things")
    if weak["verdict"] != "WEAK" or weak["flags"]:
        failures.append(f"hook_score: the weak hook scored {weak}")
    checks += 1
    # The arithmetic the reference states: 0.6 * mean + 0.4 * min - 15 per flag.
    parts = list(strong["checks"].values())
    expected = round(0.6 * sum(parts) / len(parts) + 0.4 * min(parts), 1)
    if round(strong["score"], 1) != expected:
        failures.append(f"hook_score: {strong['score']} is not 0.6*mean+0.4*min "
                        f"({expected}) over {strong['checks']}")

    # The vocabulary is English, so a hook in another script is not scored;
    # the two script-independent dealbreakers still apply.
    russian = "Ты теряешь деньги на подписке, о которой давно забыл."
    case("B044 does not score a Cyrillic hook against English vocabulary",
         pack, set(), project=reel({"hook": russian}))
    checks += 1
    if brand_lint.hook_score(russian)["verdict"] is not None:
        failures.append("hook_score: a Cyrillic hook was scored against "
                        "English word lists")
    case("B044 still applies the hashtag dealbreaker to a Cyrillic hook",
         pack, {"B044"}, project=reel({"hook": russian + " #деньги"}))

    case("B030 reads the spoken hook: its figure needs a facts.md row",
         {**pack, "facts.md": MARKER + "\n"}, {"B030"},
         project=reel({"hook": STRONG_HOOK}))

    # The script itself (video-script.md): hook, on-screen text, beats, one
    # ask. Fixture for C2 -- a script written to the reference lints clean.
    script = (
        "## Beats\n\n"
        "0:00 Hook. Open on the bank app, scrolled to the charge.\n\n"
        "0:02 Stakes. Every month it renews, and nobody opens it.\n\n"
        "0:07 Body. Sort the statement by merchant. Circle anything you have "
        "not opened in thirty days. Cancel from the store, not the app.\n\n"
        "0:24 Payoff. The charge is gone from next month.\n\n"
        "0:27 Ask. Send this to the friend who still pays for that gym.\n"
    )
    case("a short-video script written to the reference lints clean",
         pack, set(),
         project=reel({"hook": STRONG_HOOK, "on-screen": "$400 A MONTH, GONE"},
                      body=script))


def instagram_caption_cases() -> None:
    """B045 (the feed window), B046 (one ask), and the existing B042/B043
    mechanics declared for Instagram's physics."""
    pack = {**MINIMAL, "README.md": SOCIAL_SOURCES, "channels.md": INSTAGRAM}

    def caption(body: str) -> dict:
        return {"content/c.md":
                f"---\nsurface: Instagram\ntitle: Caption\n---\n\n{body}\n"}

    tail = ("\n\nSort the statement by merchant and circle every charge you "
            "have not opened in a month. Cancel from the store, not the app, "
            "or it renews anyway.")
    clean = ("Your bank app hides the charge you forgot." + tail
             + "\n\nComment CANCEL and I will send the checklist."
             + "\n\n#budgeting #subscriptions")
    case("an Instagram caption written to the playbook lints clean",
         pack, set(), project=caption(clean))
    case("B045 fires when the first line runs past the feed window",
         pack, {"B045"},
         project=caption("Your bank app hides the charge you forgot, and it "
                         "keeps renewing every single month because nobody "
                         "opens the app it belongs to anymore at all" + tail
                         + "\n\nComment CANCEL and I will send the checklist."))
    # The tag is mid-line on purpose: a caption OPENING with `#` is answered
    # by the opener branch, and that fixture stayed green with this branch
    # deleted (planted 2026-10-07).
    case("B045 fires on a hashtag inside the feed window",
         pack, {"B045"},
         project=caption("Your bank app hides the #budgeting charge you forgot."
                         + tail
                         + "\n\nComment CANCEL and I will send the checklist."))
    case("B045 fires on a caption that opens with a mention",
         pack, {"B045"},
         project=caption("@bank your app hides the charge I forgot." + tail
                         + "\n\nComment CANCEL and I will send the checklist."))
    case("B046 fires on a caption with no ask",
         pack, {"B046"},
         project=caption("Your bank app hides the charge you forgot." + tail))
    case("B046 fires on a caption with two asks",
         pack, {"B046"},
         project=caption("Your bank app hides the charge you forgot." + tail
                         + "\n\nComment CANCEL for the checklist, and save this "
                           "for the first of the month."))
    case("B046 counts a Russian ask as one ask",
         pack, set(),
         project=caption("Банк прячет подписку, о которой ты забыл."
                         "\n\nОтсортируй выписку по магазину и отметь всё, что "
                         "ты не открывал месяц. Отменяй в сторе, а не в самом "
                         "приложении, иначе оно продлится."
                         "\n\nНапиши в комментариях ОТМЕНА, и я пришлю чеклист."))
    case("B046 counts two Russian asks as two",
         pack, {"B046"},
         project=caption("Банк прячет подписку, о которой ты забыл."
                         "\n\nОтсортируй выписку по магазину и отметь всё, что "
                         "ты не открывал месяц. Отменяй в сторе, а не в самом "
                         "приложении, иначе оно продлится."
                         "\n\nНапиши в комментариях ОТМЕНА. Сохрани пост, "
                         "чтобы не потерять."))
    case("B042 applies to an Instagram caption: links there do not click",
         pack, {"B042"},
         project=caption(clean.replace("I will send the checklist.",
                                       "I will send https://example.com/list")))
    case("B043 applies Instagram's five-hashtag cap",
         pack, {"B043"},
         project=caption(clean.replace("#budgeting #subscriptions",
                                       "#a1 #b2 #c3 #d4 #e5 #f6")))


def invisible_character_cases() -> None:
    """B066 -- AT-16, invisible and look-alike-space characters.

    One fixture per class the reference names (raw source: the eighteen
    classes the humanizer in `Jakeschincariol/instagram-agent-skill` strips),
    one for the catch-all, and one per numbered exemption. The dash and the
    quotation marks are never this check's business, in any language.
    """
    global checks
    pack = {**MINIMAL, "README.md": SOCIAL_SOURCES, "channels.md": SHORT_VIDEO}

    def doc(body: str) -> dict:
        return {"content/a.md":
                f"---\nsurface: short video\ntitle: Ship\n---\n\n{body}\n"}

    classes = {
        "​": "ZERO WIDTH SPACE", "‌": "ZERO WIDTH NON-JOINER",
        "‍": "ZERO WIDTH JOINER", "⁠": "WORD JOINER",
        "﻿": "ZERO WIDTH NO-BREAK SPACE", "­": "SOFT HYPHEN",
        "᠎": "MONGOLIAN VOWEL SEPARATOR", "؜": "ARABIC LETTER MARK",
        "‎": "LEFT-TO-RIGHT MARK", "‏": "RIGHT-TO-LEFT MARK",
        "⁣": "INVISIBLE SEPARATOR", "\U000E0041": "TAG LATIN CAPITAL LETTER A",
        " ": "NO-BREAK SPACE", " ": "NARROW NO-BREAK SPACE",
        " ": "THIN SPACE", " ": "FIGURE SPACE",
        " ": "EM SPACE", " ": "EN SPACE",
    }
    for char, name in classes.items():
        case(f"B066 finds U+{ord(char):04X} {name}",
             pack, {"B066"}, project=doc(f"Ship your{char}first release today."))
        checks += 1
        hits = brand_lint.invisible_chars(f"Ship your{char}first release today.")
        if [h[1] for h in hits] != [ord(char)]:
            failures.append(f"invisible_chars: U+{ord(char):04X} reported as {hits}")
    case("B066 catch-all: any other format character (U+202E override)",
         pack, {"B066"}, project=doc("Ship your‮first release today."))
    case("B066 reports an embedding override even inside right-to-left text",
         pack, {"B066"}, project=doc("שלום ‮world, ship today."))

    # Exemptions. Each id is declared in ai-tells.md and named here, and
    # `validate_ai_tell_coverage` refuses either side without the other.
    case("AT-16-E1: a joiner inside an emoji sequence is the emoji",
         pack, set(),
         project=doc("The family plan \U0001F468‍\U0001F469‍\U0001F467 ships today."))
    case("AT-16-E2: a joiner inside a script that needs it is spelling",
         pack, set(), project=doc("Ship today: می‌خواهم."))
    case("AT-16-E3: a direction mark inside right-to-left text is layout",
         pack, set(), project=doc("שלום‏ world, ship today."))
    case("AT-16-E4: tag characters inside a flag sequence are the flag",
         pack, set(),
         project=doc("Made in England \U0001F3F4\U000E0067\U000E0062\U000E0065"
                     "\U000E006E\U000E0067\U000E007F and shipped today."))
    case("AT-16-E5: a no-break space in Russian typography is normative",
         pack, set(), project=doc("Релиз выходит в пятницу, в полдень."))
    checks += 1
    if brand_lint.invisible_chars("Prix : douze euros", locale="fr"):
        failures.append("invisible_chars: AT-16-E5 did not honour locale fr")
    checks += 1
    if not brand_lint.invisible_chars("Price : twelve euros", locale="en"):
        failures.append("invisible_chars: a narrow space in English went unreported")
    case("AT-16-E6: the dash and the quotation marks are never this check's business",
         pack, set(),
         project=doc("Москва — столица России. Сезон 2020–2024 закрыт. "
                     "Он сказал «готово» и ушёл."))
    case("AT-16-E7: a byte-order mark opening a file is its encoding signature",
         pack, set(),
         project={"content/a.md": "﻿---\nsurface: short video\ntitle: Ship\n"
                                  "---\n\nShip your first release today.\n"})


def main() -> int:
    case("clean minimal base", MINIMAL, set())
    case("B009 refuses an empty declared source glob",
         {**MINIMAL, "README.md": MARKER + "\nSources:\n  marketing: absent/**/*.html\n"},
         {"B009"})

    case(
        "no Sources block",
        {**MINIMAL, "README.md": MARKER + "\n"},
        {"B006"},
    )
    case(
        "missing contract marker",
        # The references section stays, and so does `Humanization`, or this
        # fixture would test two codes at once and pass for the wrong reason.
        {**MINIMAL, "voice.md": "Voice pack: operator-brief\n"
         "Humanization: on\n"
         "\n## Voice references\n- **Admired:** Stripe docs\n"
         "- **Refused:** a cheerful outage page\n"},
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
    # B034 -- an out-of-enum `Status`. This pack's own `voice.md` said
    # `Status: approved` for two releases while `brand-contract.md` declared
    # `draft | validated`, and it worked by accident: every read here asks
    # `== "draft"` or `!= "draft"`, so `approved` behaved like `validated` and
    # would have read as NOT validated the first time a check tested for the
    # value. Same class as the screens enum SU-02 closed -- an out-of-enum value
    # that is neither refused nor accepted, and invisible.
    case(
        "a voice status the contract does not declare",
        {**MINIMAL, "voice.md": MINIMAL["voice.md"].replace(
            "Status: validated", "Status: approved")},
        {"B034"},
    )
    case(
        "a plausible-looking third state is still not one",
        {**MINIMAL, "voice.md": MINIMAL["voice.md"].replace(
            "Status: validated", "Status: agreed")},
        {"B034"},
    )
    case(
        "`draft` is in the enum, and B003 is a different question",
        {**MINIMAL, "voice.md": MINIMAL["voice.md"].replace(
            "Status: validated", "Status: draft")},
        set(),
    )

    # B022 reads a multi-line template literal as PARAGRAPHS since 2026-08-20 --
    # `LITERAL_RE` used `[^\n]`, so `usage()` in this pack's own installer, the
    # most-read UI surface it has, was invisible to the registry for as long as
    # the code existed. A paragraph the source wraps cannot be a byte-exact
    # registry row, so B021 falls back to the wrap-tolerant comparison the
    # rendered-page branch already used; without it B022 would demand a row that
    # B021 refuses, which is a check with no passing answer.
    wrapped_src = (
        "function usage() {\n"
        "  console.log(`the tool that writes things down\n"
        "\n"
        "Every run prints one line per file it wrote\n"
        "and one summary line at the end.\n"
        "`);\n"
        "}\n"
    )
    case(
        "a string inside a multi-line template literal is swept",
        {**MINIMAL, "README.md": MARKER + "\n\nSources:\n  ui: src/*.js\n",
         "strings.md": MARKER + "\n"
         "| Key | Text (primary) | Location | Scenario | Status |\n"
         "|---|---|---|---|---|\n"
         "| help.title | the tool that writes things down | src/a.js:2 | SCN-001 | agreed |\n"},
        {"B022"},
        project={"src/a.js": wrapped_src},
    )
    case(
        "a wrapped paragraph registered in its collapsed form is not a divergence",
        {**MINIMAL, "README.md": MARKER + "\n\nSources:\n  ui: src/*.js\n",
         "strings.md": MARKER + "\n"
         "| Key | Text (primary) | Location | Scenario | Status |\n"
         "|---|---|---|---|---|\n"
         "| help.title | the tool that writes things down | src/a.js:2 | SCN-001 | agreed |\n"
         "| help.body | Every run prints one line per file it wrote and one "
         "summary line at the end. | src/a.js:4 | SCN-001 | agreed |\n"},
        set(),
        project={"src/a.js": wrapped_src},
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

    # `B-029`. `Kind: layout` registers a string whose shape carries the
    # meaning and stops the language rules judging typesetting. The pair below
    # is the isolation: the same row, the same banned word, differing only in
    # the column under test, so a fixture cannot pass because some other guard
    # happened to hold.
    case(
        "a layout row is registered and not judged as language",
        {**MINIMAL, "terminology.md": banned,
         "strings.md": registry(
             "| a.b | Leverage this | src/a.ts:1 | SCN-001 | agreed | layout |\n")},
        set(), project={"src/a.ts": "x\n"},
    )
    case(
        "the same row as copy is judged, which is what makes the pair a control",
        {**MINIMAL, "terminology.md": banned,
         "strings.md": registry(
             "| a.b | Leverage this | src/a.ts:1 | SCN-001 | agreed | copy |\n")},
        {"B010"}, project={"src/a.ts": "x\n"},
    )
    case(
        "a Kind the contract does not declare",
        {**MINIMAL, "terminology.md": banned,
         "strings.md": registry(
             "| a.b | Publish | src/a.ts:1 | SCN-001 | agreed | furniture |\n")},
        {"B065"}, project={"src/a.ts": "x\n"},
    )
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
        "a contraction of I inside a sentence is not Title Case",
        {**MINIMAL, "strings.md": registry(
            "| section.a.lede | Tell me what you want and by when. "
            "Where it does not fit I'm going to say so. "
            "| src/a.ts:1 | SCN-001 | agreed |\n")},
        set(), project={"src/a.ts": "x\n"},
    )
    case(
        "a contraction of any other pronoun still is",
        {**MINIMAL, "strings.md": registry(
            "| section.b.lede | Tell me what you want and by when. "
            "Where it does not fit We're going to say so. "
            "| src/a.ts:1 | SCN-001 | agreed |\n")},
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
    # B030 read identifiers, standards and years as unsourced claims until this
    # linter was pointed at super-ux's own README, where `BP-079..090`,
    # `NIST SP 800-63B` and `Apple HIG 2025` produced nine errors nobody could
    # act on. A check that cries wolf is uninstalled, so each shape gets a
    # fixture: the regression would otherwise look exactly like working.
    case(
        "catalog ids and ranges are not figures",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project={"content/a.md": page(
            "landing hero", "Craft floors",
            "BP-079..090 and BP-130..135 are craft floors; PRN-24 always holds.")},
    )
    case(
        "a standard's designation is not a figure",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project={"content/a.md": page(
            "landing hero", "Auth",
            "Password rules follow NIST SP 800-63B rev 4.")},
    )
    case(
        "a year dates a claim, it is not the claim",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project={"content/a.md": page(
            "landing hero", "Guidance",
            "Guidance from Apple HIG 2025 and Material 3 Expressive.")},
    )
    case(
        "a real unsourced figure still blocks",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B030"},
        project={"content/a.md": page(
            "landing hero", "Reach", "Used by 4200 teams.")},
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
    # B030 compared a figure against every value joined into ONE string and
    # asked `compact not in known.replace(" ", "")`, so the corpus was a single
    # character sequence and every substring of it counted as sourced. Against
    # this pack's own seven public rows the corpus was `7158215243770+`, which
    # sourced the invented `1582` in "super-ux ... ships 1582 checks": the
    # linter printed `brand pack is clean` and exited 0. An invented public
    # number passing the check whose only purpose is to refuse one is the worst
    # failure this file can have, because it is indistinguishable from working.
    two_facts = (
        MARKER + "\n\n"
        "| Fact | Value | Source | Checked | Review by | Public |\n"
        "|---|---|---|---|---|---|\n"
        "| skills shipped | 7 | `ls skills \\| wc -l` | 2026-08-01 | 2099-01-01 | yes |\n"
        "| practices | 215 | `grep -c BP- x.md` | 2026-08-01 | 2099-01-01 | yes |\n"
    )
    case(
        "a figure that is only a SUBSTRING of the joined values is not sourced",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": two_facts},
        {"B030"},
        project={"content/a.md": page("landing hero", "Reach", "Ships 1582 checks.")},
    )
    case(
        "a figure spanning two adjacent values is not sourced either",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": two_facts},
        {"B030"},
        project={"content/a.md": page("landing hero", "Reach", "Used by 7215 teams.")},
    )
    case(
        "each value is still sourced on its own",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": two_facts},
        set(),
        project={"content/a.md": page(
            "landing hero", "Catalog", "A catalog of 215 practices.")},
    )
    case(
        "a bound marker in the value sources the figure a sentence writes",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": MARKER + "\n\n"
         "| Fact | Value | Source | Checked | Review by | Public |\n"
         "|---|---|---|---|---|---|\n"
         "| agents | 500+ | registry | 2026-08-01 | 2099-01-01 | yes |\n"},
        set(),
        project={"content/a.md": page("landing hero", "Reach", "Reaches 500+ agents.")},
    )
    # B033 -- two rows under one `Fact` name. Watched: a second
    # `| skills shipped | 99 | ... |` row left the pack clean AND put `99` into
    # the sourced set, so the duplicate did not merely go unreported, it
    # licensed a figure nobody had agreed.
    case(
        "two rows under one fact name",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": two_facts + "| skills shipped | 99 | `ls` | 2026-08-01 "
                     "| 2099-01-01 | yes |\n"},
        {"B033"},
        project={"content/a.md": page("landing hero", "Hello", "Hello.")},
    )
    case(
        "the same name spelled with different case is still one key",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": two_facts + "| Skills Shipped | 99 | `ls` | 2026-08-01 "
                     "| 2099-01-01 | yes |\n"},
        {"B033"},
        project={"content/a.md": page("landing hero", "Hello", "Hello.")},
    )
    case(
        "distinct fact names are not a duplicate",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero,
         "facts.md": two_facts},
        set(),
        project={"content/a.md": page("landing hero", "Hello", "Hello.")},
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

    # The four codes an audit found emitting with no fixture behind them. The
    # DoD said one per code and the count looked right; four had slipped, which
    # is what an audit is for and what a passing suite cannot tell you.
    case(
        "foundation changed after the voice was last calibrated",
        {**MINIMAL, "voice.md": MINIMAL["voice.md"]
            .replace("Derived-from: inferred", "Derived-from: P-01")
            .replace(f"Last calibrated: {TODAY}", "Last calibrated: 2020-01-01")},
        {"B005"},
        project={"docs/ux/foundation.md": "### P-01: the operator\n"},
    )
    git_date_beats_mtime()
    case(
        "the title promises more than the body delivers",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B054"},
        project={"content/a.md":
                 "---\nsurface: landing hero\ntitle: 7 ways to ship\n---\n\n"
                 "- one\n- two\n"},
    )
    case(
        "machine-drafting markers above the S1 threshold",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B060"},
        project={"content/a.md":
                 "---\nsurface: landing hero\ntitle: Ship\n---\n\n"
                 "It is important to note that teams delve into this. "
                 "In conclusion, it is worth noting the result.\n"},
    )
    # AT-06 -- B062. The rule is a distinction, so the negative cases carry
    # as much weight as the positive ones: a check that cannot tell the
    # Russian copula from the rhetorical reflex would ban correct grammar,
    # and the first project it did that to would switch it off.
    def page(body: str, title: str = "Ship") -> dict:
        return {"content/a.md":
                f"---\nsurface: landing hero\ntitle: {title}\n---\n\n{body}\n"}

    # These two are written in Russian on purpose. In English the strict rule
    # fires on any bare dash, so an English fixture stays green when the
    # conjunction rule is deleted -- the same code arrives from a different
    # branch and a set comparison cannot tell them apart. Planting that
    # deletion is how the hole was found. In Russian the strict rule is off,
    # so only the branch under test can produce the code.
    case(
        "a dash introduces a conjunction, where strict is off",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B062"},
        project=page("Это работает — и работает быстро."),
    )
    case(
        "a pair of dashes brackets an aside, where strict is off",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B062"},
        project=page("Результат — которого никто не ждал — пришёл вовремя."),
    )
    case(
        "a lone dash where the locale has no grammatical dash",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B062"},
        project=page("One thing matters — speed."),
    )
    case(
        "AT-06-E1: the Russian copula is grammar, not a tell",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project=page("Москва — столица России."),
    )
    case(
        "AT-06-E3: Russian direct speech is a convention, not a tell",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project=page("— Привет, — сказал он."),
    )
    case(
        "AT-06-E2: a numeric range is arithmetic, not a tell",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project=page("The window runs 2020—2024 without a gap."),
    )
    # B064 -- three branches, one code, and each fixture is written in the
    # only state where its own branch can fire: absent, present-and-illegal,
    # present-legal-and-off. Standing instruction #5: a fixture that asserts a
    # set of codes proves the code arrived, not which branch produced it.
    case(
        "no Humanization field, so the default applies unrecorded",
        {**MINIMAL, "voice.md": voice_no_humanization},
        {"B064"},
    )
    case(
        "an out-of-enum Humanization value leaves the pass in neither state",
        {**MINIMAL, "voice.md": voice_humanization_bad},
        {"B064"},
    )
    case(
        "Humanization off with no recorded reason",
        {**MINIMAL, "voice.md": voice_humanization_off},
        {"B064"},
    )
    case(
        "an aligned trailing comment is not part of the value",
        {**MINIMAL, "voice.md": _VOICE.replace(
            "Humanization: on",
            "Humanization: on          # on | off; on is the default")},
        set(),
    )
    case(
        "a reason citing a ticket number keeps the hash",
        {**MINIMAL, "voice.md": _VOICE.replace(
            "Humanization: on",
            "Humanization: off\nHumanization declined: per ticket #431")},
        set(),
    )
    case(
        "Humanization off with a recorded reason is a decision, not a defect",
        {**MINIMAL, "voice.md": voice_humanization_declined},
        set(),
    )
    # The mark has more than one spelling, and the tell is the role rather
    # than the codepoint. Each of the three below is written where the
    # branch under test is the ONLY thing that can produce the code:
    # neither carries an em dash, so deleting the normaliser leaves no dash
    # for any branch to find and the fixture goes red -- which is the miss
    # standing instruction #5 was written about. Measured on trycomp.ai,
    # 2026-08-30: twenty rhetorical dashes, zero em dashes.
    case(
        "a hyphen with a space each side is the same mark",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B062"},
        project=page("One thing matters - speed."),
    )
    case(
        "an en dash is the same mark",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B062"},
        project=page("One thing matters \u2013 speed."),
    )
    # Russian, so the strict branch is off and only the conjunction rule can
    # fire: this proves the normalised spelling reaches that branch too,
    # rather than being caught by strict on its way past.
    case(
        "a spaced hyphen introduces a conjunction, where strict is off",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B062"},
        project=page("\u042d\u0442\u043e \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442 - \u0438 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442 \u0431\u044b\u0441\u0442\u0440\u043e."),
    )
    # The allowance AT-06 has always promised and nothing implemented. In a
    # strict locale every bare dash is an error, so the cell dash was one
    # too; delete the table-cell rule and this fixture goes red.
    case(
        "AT-06-E4: a dash alone in a table cell is an empty string, not punctuation",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project=page("| Surface | Owner |\n|---|---|\n| landing | - |\n"),
    )
    # The lone backtick inside the fence is load-bearing. Without it the
    # inline-code stripper happens to pair the fence markers around the dash
    # and removes it anyway, so deleting the fence stripper leaves the suite
    # green -- watched, on a planted deletion. With it, the inline pass
    # leaves the dash standing and only the fence pass can clear it.
    case(
        "a dash inside a fenced block is code, not prose",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project=page("Run it.\n\n```\nusage: `ship — fast\n```\n"),
    )

    # AT-07 -- B063, the same rule B026 applies to the registry, applied to
    # documents. Split by artifact rather than by rule, so that neither can
    # be satisfied by fixing the other.
    case(
        "a document title ends in a full stop",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B063"},
        project=page("A body with nothing wrong in it.", title="Ship faster."),
    )
    case(
        "a heading ends in a full stop",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        {"B063"},
        project=page("## Why it matters.\n\nA body with nothing wrong in it."),
    )
    case(
        "a heading that asks, and one that abbreviates, are both names",
        {**MINIMAL, "README.md": marketing_sources, "channels.md": hero},
        set(),
        project=page("## Why does it matter?\n\n## Built on Node.js\n\n"
                     "## Logs, metrics, traces, etc.\n\nA clean body."),
    )

    case(
        "a locale row left identical to the primary",
        {**MINIMAL,
         "voice.md": MINIMAL["voice.md"].replace(
             "Locales: en (primary)", "Locales: en (primary), de"),
         "locales/de.md": MARKER + "\nLocale: de\nPrimary: no\n\n"
         "| Primary | Replacement | Job |\n|---|---|---|\n"
         "| ship it | ship it | permission to stop |\n"},
        {"B072"},
    )

    # --- B007: the voice names what it admires and what it refuses ---
    no_refs = MINIMAL["voice.md"].split("\n## Voice references")[0] + "\n"
    case(
        "B007 voice.md with no Voice references section",
        {**MINIMAL, "voice.md": no_refs},
        {"B007"},
    )
    case(
        "B007 fires when only one half is named",
        {**MINIMAL, "voice.md": no_refs + "\n## Voice references\n"
         "- **Admired:** Stripe docs — every claim has a runnable example\n"},
        {"B007"},
    )
    case(
        "B007 fires when the half is a template placeholder",
        {**MINIMAL, "voice.md": no_refs + "\n## Voice references\n"
         "- **Admired:** Stripe docs\n- **Refused:** <brand you refuse to sound like>\n"},
        {"B007"},
    )

    case(
        "B007 silent on a draft voice, which has not been calibrated yet",
        {**MINIMAL, "voice.md": no_refs.replace("Status: validated", "Status: draft")},
        set(),
    )

    # --- B026: a label is not a sentence, so it takes no full stop ---
    case(
        "B026 a menu label ending in a period",
        {**MINIMAL, "strings.md": registry("| menu.item.install | Install the plugin. | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B026"}, project={"src/a.ts": "Install the plugin.\n"},
    )
    case(
        "B026 silent on the same label without one",
        {**MINIMAL, "strings.md": registry("| menu.item.install | Install the plugin | src/a.ts:1 | SCN-001 | agreed |\n")},
        set(), project={"src/a.ts": "Install the plugin\n"},
    )
    case(
        "B026 silent on a prose key, which is allowed sentences",
        {**MINIMAL, "strings.md": registry("| error.disk.full | The disk is full. | src/a.ts:1 | SCN-001 | agreed |\n")},
        set(), project={"src/a.ts": "The disk is full.\n"},
    )
    case(
        "B026 silent on an ellipsis, which is progress and not a full stop",
        {**MINIMAL, "strings.md": registry("| button.save | Saving… | src/a.ts:1 | SCN-001 | agreed |\n")},
        set(), project={"src/a.ts": "Saving…\n"},
    )
    case(
        "B026 catches a multi-sentence label too",
        {**MINIMAL, "strings.md": registry("| title.welcome | Welcome. Let us begin. | src/a.ts:1 | SCN-001 | agreed |\n")},
        {"B026"}, project={"src/a.ts": "Welcome. Let us begin.\n"},
    )

    # A source file is not prose: comments and identifiers are addressed to a
    # maintainer, and the prose rules were reading both. The three cases below
    # are the fix and its two boundaries -- what stops being read, what keeps
    # being read, and the interpolated case that would have been lost silently.
    marketing = {**MINIMAL,
                 "README.md": MARKER + "\n\nSources:\n  ui: src/**/*.ts\n"
                                       "  marketing: src/**/*.ts\n"}

    case(
        "a rhetorical dash inside a code comment is not copy",
        marketing, set(),
        project={"src/a.ts": "// this clause — and that one\nconst x = 1;\n"},
    )
    case(
        "a rhetorical dash inside a rendered string still is",
        marketing, {"B062"},
        project={"src/a.ts":
                 'export const t = "this clause — and the one after it";\n'},
    )
    case(
        "an interpolated template literal keeps its coverage",
        marketing, {"B062"},
        project={"src/a.ts":
                 "export const t = `we shipped ${n} of them — and it held`;\n"},
    )
    case(
        "an identifier repeated fifty times is not keyword stuffing",
        marketing, set(),
        project={"src/a.ts": "const value = 1;\n" * 50},
    )
    case(
        "a URL is not a comment, and its literal survives the scanner",
        marketing, set(),
        project={"src/a.ts":
                 'const u = "https://example.com/docs"; // a note — with a dash\n'},
    )

    # facts.md is a document, not only a facts table: it also carries product
    # ledgers, and one of them has six columns whose meanings are nothing like
    # a fact row's. Scoping by header rather than by column count is what keeps
    # a sale year out of the Review column.
    ledger_facts = (
        MARKER + "\n\n"
        "| Fact | Value | Source | Checked | Review | Public |\n"
        "|---|---|---|---|---|---|\n"
        "| Name | Acme | owner-stated | 2026-01-01 | 2099-01-01 | yes |\n"
        "\n## Sold\n\n"
        "| Product | App Store name | id | Released | Sold | Publisher today |\n"
        "|---|---|---|---|---|---|\n"
        "| Thing | Thing App | 1449023197 | 2019-04-05 | 2022 | Someone Ltd |\n"
    )
    case(
        "a product ledger in facts.md is not read as six fact fields",
        {**MINIMAL, "facts.md": ledger_facts}, set(),
    )

    # Density is a property of the document a reader meets. A word can be 6% of
    # one small data file and under 1% of the page that file is a tenth of, and
    # only the second number is about the reader. Literals stay under the 200
    # characters LITERAL_RE allows, which is why the fixtures are built from many
    # short strings rather than one long one.
    dense = (
        'export const a0 = "cofounder cofounder cofounder alpha1 alpha2 alpha3";\n'
        + "".join(f'export const a{i} = "delta{i} echo{i} foxtrot{i} golf{i} '
                  f'hotel{i}";\n' for i in range(1, 10))
    )
    sparse = "".join(
        f'export const b{i} = "india{i} juliett{i} kilo{i} lima{i} mike{i}";\n'
        for i in range(60)
    )
    case(
        "density is measured over the pooled copy, not per source file",
        marketing, set(), project={"src/a.ts": dense, "src/b.ts": sparse},
    )
    case(
        "a word dense across the whole pool still fires",
        marketing, {"B051"},
        project={"src/a.ts": dense,
                 "src/c.ts": dense.replace("a0", "c0").replace("const a", "const c")},
    )

    # The scanner is the load-bearing half of that fix, so it is tested directly
    # as well: the end-to-end cases above would pass with a regex that happened
    # to be wrong in a way no fixture reached.
    global checks
    for name, src, suffix, present, absent in (
        ("a // inside a URL is not a comment",
         'const u = "https://x.dev/a";  // note', ".ts", "https://x.dev/a", "note"),
        ("a quoted phrase inside a comment goes with it",
         '// "AI integrations" named nothing', ".ts", "", '"AI integrations"'),
        ("a block comment goes, the literal stays",
         '/* "dropped" */ const a = "kept here";', ".ts", "kept here", '"dropped"'),
        ("a hash comment is a comment in Python only",
         'x = "kept"  # "dropped"', ".py", "kept", '"dropped"'),
        ("an escaped quote does not end the string",
         'const s = "he said \\"hi\\" then left";', ".ts", "then left", None),
    ):
        checks += 1
        got = brand_lint._strip_comments(src, suffix)
        if present and present not in got:
            failures.append(f"strip_comments: {name}: lost {present!r}")
        if absent and absent in got:
            failures.append(f"strip_comments: {name}: kept {absent!r}")

    short_video_cases()
    instagram_caption_cases()
    invisible_character_cases()

    fix_idempotent()

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} failure(s) out of {checks} checks")
        return 1
    # See the note in ux_lint_test.py: this script's floor was recorded and
    # never read, so a deleted fixture dropped the count in silence.
    sys.path.insert(0, str(ROOT / "test"))
    from validate import check_floor

    rc = check_floor("brand_lint_test.py", checks)
    if rc:
        return rc
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
