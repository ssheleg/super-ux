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
    python3 brand_lint.py [path] --strict  # warnings block too

Exit codes: 0 clean or warnings only, 1 warnings under `--strict`, 2 any error.

One pack, one policy: `ux_lint.py` has always blocked on errors and needed
`--strict` before a warning could fail a build, and this file returned 1 for
warnings alone -- so 13 of the 37 codes turned `npm test` red while printing
`0 error(s), 1 warning(s)`. A gate whose two halves disagree about what a
warning means gets the noisier half switched off, and the half switched off
here is the one that guards public figures.
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

# The one enum this file matches on, kept as a module literal so
# `validate_status_enums_match_contract` can read it out of the source and
# compare it against `brand-contract.md`'s declaration -- the mechanism the UX
# linter has carried since SU-02, applied to the layer that was left out of it.
#
# The defect it closes was live in this repository's own pack and worked by
# accident: `brand-contract.md` declares `draft | validated`, `docs/brand/voice.md`
# said `Status: approved`, and nothing caught it because every read here asked
# `== "draft"` or `!= "draft"`. So `approved` behaved like `validated` today and
# would have read as NOT validated the first time any check tested for the value
# instead of against `draft`. Same class as the screens enum SU-02 closed: an
# out-of-enum value that is neither refused nor accepted, and invisible.
VOICE_STATUSES = ("draft", "validated")

# Whether the humanization pass runs at all, which is a different question from
# `Humanization pass:`, which names WHICH implementation runs. `on` is the
# pack's default and it is a default rather than a preference: an unswept draft
# carries the markers `ai-tells.md` grades, and a reader registers them before
# they can name why. Turning it off is a legitimate decision and it IS a
# decision, so it leaves its reason in the file instead of a silence that reads
# identically to never having been asked.
HUMANIZATION_MODES = ("on", "off")

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


def unfilled(value: str) -> bool:
    """A template placeholder, not data.

    Templates ship worked examples so the shape is unambiguous, and a project
    mid-fill has some rows done and some not. `<...>` means "nobody has filled
    this in yet" -- reporting it as a defect would make every freshly seeded
    project fail on its own scaffolding, which teaches people to ignore the
    linter on day one.
    """
    value = value.strip()
    return not value or (value.startswith("<") and value.endswith(">"))


def read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def content_date(path: Path) -> str | None:
    """The date this file's content last changed, as `YYYY-MM-DD`.

    Git first, mtime only as a fallback. A fresh clone stamps every file with
    the checkout time, so an mtime-based answer says "changed today" about a
    file nobody has touched in months -- which made `B005` fire on every CI
    run the moment this project put its own linter in CI, and would have
    trained a reader to ignore the one gate it was added to enforce.
    """
    try:
        import subprocess

        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", path.name],
            cwd=path.parent, capture_output=True, text=True, timeout=10,
        )
        stamp = out.stdout.strip()
        if out.returncode == 0 and re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
            return stamp
    except Exception:
        pass
    try:
        import datetime

        return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()
    except OSError:
        return None


# A trailing comment, aligned away from the value the way the seeded templates
# write one. Two spaces or more, because one space is prose: a `Humanization
# declined:` reason may legitimately say "per ticket #431", and truncating it
# would read as no reason at all. Found by standing instruction #3 on the first
# enum field the templates seeded with a literal value beside a comment.
HEADER_COMMENT_RE = re.compile(r"[ \t]{2,}#.*$")


def header_field(text: str, key: str) -> str | None:
    """A `Key: value` line from a file's header block, comment stripped."""
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.M)
    if not match:
        return None
    return HEADER_COMMENT_RE.sub("", match.group(1)).strip() or None


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
        # A markdown cell escapes a literal pipe as `\|`. Splitting on a raw
        # pipe therefore tore `Select [e.g. 1,3 | all | q]:` into three cells
        # and pointed a registry row at a file called "all". A string registry
        # that cannot hold a string containing a pipe cannot describe a CLI.
        parts = re.split(r"(?<!\\)\|", line.strip("|"))
        cells = [c.strip().replace("\\|", "|") for c in parts]
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
    # B034 -- an out-of-enum `Status` is refused rather than read as no status.
    if status is not None and not unfilled(status) \
            and status not in VOICE_STATUSES:
        findings.append(Finding(
            "B034", SEVERITY_ERROR, "voice.md", 1,
            f"`Status: {status}` is not one of "
            f"{' | '.join(VOICE_STATUSES)} -- every read in this file asks "
            f"whether the status is `draft`, so an unrecognised value behaves "
            f"like `validated` today and reads as not-validated the moment a "
            f"check tests for the value instead of against `draft`",
        ))

    # B064 -- the humanization pass: does it run, and was that decided.
    # Three branches, one code, and each is reachable only in the state the
    # others are not: absent, present-and-illegal, present-legal-and-off. A
    # fixture for one therefore cannot be satisfied by another firing.
    humanization = header_field(voice, "Humanization")
    if humanization is None:
        findings.append(Finding(
            "B064", SEVERITY_WARN, "voice.md", 1,
            f"no `Humanization:` field, so the pack default `on` applies and "
            f"nobody has recorded whether that was chosen -- write "
            f"`Humanization: on` to make the state readable, here and in every "
            f"status this pack prints",
        ))
    elif not unfilled(humanization):
        if humanization not in HUMANIZATION_MODES:
            findings.append(Finding(
                "B064", SEVERITY_ERROR, "voice.md", 1,
                f"`Humanization: {humanization}` is not one of "
                f"{' | '.join(HUMANIZATION_MODES)} -- an unrecognised value "
                f"leaves the pass in neither state, and the copy modes read "
                f"this field to decide whether to run",
            ))
        elif humanization == "off" and not header_field(voice, "Humanization declined"):
            findings.append(Finding(
                "B064", SEVERITY_ERROR, "voice.md", 1,
                f"`Humanization: off` with no `Humanization declined:` line -- "
                f"switching the pass off is a decision and it outlives whoever "
                f"made it, so it carries the reason and the date rather than "
                f"reading, later, as an oversight nobody can safely reverse",
            ))

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
    if derived and derived != "inferred" and not unfilled(derived):
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
                changed = content_date(brand_dir.parent / "ux" / "foundation.md")
                if changed and changed > calibrated:
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

    # B007 -- a voice defined only by what it is drifts toward the average of
    # everything. Naming one brand you admire and one you refuse gives the
    # writer two fixed points, and the refused one does most of the work: it
    # is the only field that can be checked against a draft out loud.
    # A `draft` voice has not been calibrated yet and the references are part
    # of calibrating it, so firing here would put a warning on every freshly
    # seeded project -- which is how a linter teaches people to ignore it on
    # day one. The check begins the moment someone claims the voice is done.
    if voice and status and status != "draft":
        section = re.search(
            r"^##\s+Voice references\s*$(.*?)(?=^##\s|\Z)",
            voice, re.MULTILINE | re.DOTALL,
        )
        body = section.group(1) if section else ""
        admired = re.search(r"\*\*Admired:\*\*\s*(\S.*)", body)
        refused = re.search(r"\*\*Refused:\*\*\s*(\S.*)", body)
        missing = [
            name for name, m in (("Admired", admired), ("Refused", refused))
            if not m or unfilled(m.group(1))
        ]
        if missing:
            findings.append(Finding(
                "B007", SEVERITY_WARN, "voice.md", 1,
                f"`## Voice references` is missing {', '.join(missing)} -- "
                f"a voice with no brand it refuses to sound like has no edge "
                f"to be checked against",
            ))

    return findings


def registry(brand_dir: Path) -> list[dict]:
    """`strings.md` data rows as dicts, header dropped."""
    rows = []
    for cells in table_rows(read(brand_dir / "strings.md") or ""):
        if len(cells) < 5 or cells[0].strip().lower() == "key":
            continue
        if unfilled(cells[0]) or unfilled(cells[1]) or unfilled(cells[2]):
            continue
        rows.append({
            "key": cells[0], "text": cells[1], "location": cells[2],
            "scenario": cells[3], "status": cells[4],
        })
    return rows


def dictionary(brand_dir: Path) -> tuple[list, list, list]:
    """(banned, product terms, entity names) from `terminology.md`."""
    text = read(brand_dir / "terminology.md") or ""
    sections: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.*?)\s*$", line)
        if heading:
            current = heading.group(1)
            sections[current] = []
        elif current:
            sections[current].append(line)

    def rows(fragment: str, header: str) -> list[list[str]]:
        for title, lines in sections.items():
            if fragment.lower() in title.lower():
                return [
                    r for r in table_rows("\n".join(lines))
                    if r and r[0].strip().lower() != header
                ]
        return []

    banned = [r[0] for r in rows("Banned", "word or phrase") if r[0]]
    terms = [
        (r[0], r[1]) for r in rows("Product terms", "our term") if len(r) > 1
    ]
    entities = [
        (r[0], r[1]) for r in rows("Entity and tier", "name") if len(r) > 1
    ]
    return banned, terms, entities


def _alternatives(cell: str) -> list[str]:
    """A comma-separated cell as a list, placeholders dropped."""
    out = []
    for part in cell.split(","):
        part = part.strip()
        if part and not part.startswith("<"):
            out.append(part)
    return out


def _mentions(needle: str, haystack: str) -> bool:
    return bool(re.search(rf"(?<!\w){re.escape(needle)}(?!\w)", haystack, re.I))


def check_terminology(brand_dir: Path) -> list[Finding]:
    """B010-B012 -- the dictionary is law, in the interface and in copy."""
    findings: list[Finding] = []
    banned, terms, entities = dictionary(brand_dir)
    for row in registry(brand_dir):
        text = row["text"]
        for word in banned:
            if _mentions(word, text):
                findings.append(Finding(
                    "B010", SEVERITY_ERROR, row["location"], 0,
                    f"`{row['key']}` uses the banned word `{word}`: "
                    f"\"{text}\"",
                ))
        for ours, generic_cell in terms:
            for generic in _alternatives(generic_cell):
                if _mentions(generic, text):
                    findings.append(Finding(
                        "B011", SEVERITY_ERROR, row["location"], 0,
                        f"`{row['key']}` says `{generic}` where the product "
                        f"term is `{ours}`: \"{text}\"",
                    ))
        for name, wrong_cell in entities:
            for wrong in _alternatives(wrong_cell):
                if wrong and wrong in text:
                    findings.append(Finding(
                        "B012", SEVERITY_ERROR, row["location"], 0,
                        f"`{row['key']}` spells the entity `{name}` as "
                        f"`{wrong}`: \"{text}\"",
                    ))
    return findings


# `I'm`, `I'll`, `I've`, `I'd`, with either apostrophe. Nothing else: `We're`
# and `They'd` mid-sentence really are miscased, and only the first person has a
# capital that is grammar rather than a choice.
CONTRACTED_I = re.compile(r"^I['\u2019](m|ll|ve|d)$")

WEAK_LABELS = {
    "ok", "yes", "no", "submit", "done", "go", "click here",
    "learn more", "get started", "continue",
}

LITERAL_RE = re.compile(r"""(["'`])((?:(?!\1)[^\n]){3,200})\1""")

# A `'` or `"` literal cannot cross a newline in JS or TS, so `[^\n]` above is
# right for those. A TEMPLATE literal can, and `usage()` in this pack's own
# installer is twenty lines of exactly one -- the most-read UI surface the pack
# has, invisible to the registry since B022 existed. `strings.md` recorded it as
# needing "a per-language extractor"; it needed a second pattern.
#
# A multi-line template is split into PARAGRAPHS, not lines and not left whole.
# Whole is useless: one 1800-character blob is a document, and nobody agrees or
# retires a document. Per line is worse than it looks -- it was tried first, and
# it turned wrapped prose into six findings no registry row could sensibly hold
# ("docs/ux skeleton, the docs/brand pack, and all three linters" is half a
# sentence). A blank-line-separated block is the unit a reader actually sees: a
# title, a usage list, an explanation. The 4000-char ceiling guards against an
# unbalanced backtick swallowing a file; it is not a claim about copy.
TEMPLATE_RE = re.compile(r"`((?:[^`\\]|\\.){3,4000})`", re.DOTALL)


def code_literals(text: str) -> list[str]:
    """Every string literal in source, one entry per unit a reader would see.

    Comments must already be stripped by the caller -- `_strip_comments` leaves
    literals untouched, which is what makes both patterns below safe to run.
    """
    out: list[str] = [lit for _quote, lit in LITERAL_RE.findall(text)]
    for block in TEMPLATE_RE.findall(text):
        if "\n" not in block:
            continue          # single-line backticks are already in `out`
        for para in re.split(r"\n\s*\n", block):
            joined = " ".join(
                line.strip() for line in para.splitlines() if line.strip()
            )
            if len(joined) >= 3:
                out.append(joined)
    return out

# A template literal's interpolations split it into pieces, and the pieces are
# not strings: `${a} : ${b}` yielded a literal " : ". Running this check over
# super-ux's own installer produced 598 such fragments and buried the four real
# findings under them. A check whose output nobody reads is not a check.
CODE_FRAGMENT_RE = re.compile(
    r"""
      ^\s*(?:\|\||&&|\?|:|\}|\{|\))   # opens with an operator or a brace
    | (?:\|\||&&|===|!==|=>)\s*$        # ends with one
    | \$\{                              # carries an interpolation opener
    | ^\s*[:?]\s*$                      # is only a ternary arm separator
    """,
    re.VERBOSE,
)


# Where a build puts the page a reader actually gets. Checked in this order and
# the first one that exists wins; a project with none of them is checked against
# its source, exactly as before.
RENDER_DIRS = ("dist", "build", "out", "_site")

_ENTITIES = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"',
             "&#39;": "'", "&apos;": "'", "&nbsp;": " ", "&#8217;": "\u2019",
             "&#8216;": "\u2018", "&#8212;": "\u2014", "&#8211;": "\u2013"}

_rendered_cache: dict = {}


def normalise(text: str) -> str:
    """Collapse whitespace so an 80-column wrap and a rendered line agree.

    Punctuation spacing is normalised too, and that is not cosmetic tidying.
    Stripping `<strong>people</strong>,` leaves `people ,` once the tag becomes
    a space, so an inline span inside a sentence would fail the comparison over
    a space no reader can see. Applied to both sides, so the check still
    compares wording and no longer compares markup.
    """
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?%)\]}\u00bb\u201d\u2019])", r"\1", text)
    return re.sub(r"([(\[{\u00ab\u201c])\s+", r"\1", text)


def rendered_text(root: Path) -> str | None:
    """All built HTML as one normalised string, or None if nothing is built.

    B021 asks whether the registry's string is what a reader sees, and used to
    look for it in the component source. Two things make that unanswerable
    there: an interpolated value never appears literally -- `{years} years,
    installable.` cannot contain `13 years, installable.` -- and an inline
    `<strong>` or `<a>` splits a sentence the registry stores whole. On one site
    that was five errors nobody could fix, and both honest repairs were bad:
    hardcode the number and lose the guarantee that it is derived, or delete the
    rows and lose the check.

    The text a reader gets exists, just not in `src/`. Tags come out, entities
    come back, whitespace collapses, and the same comparison then answers the
    question it was always asking.
    """
    if root in _rendered_cache:
        return _rendered_cache[root]
    out = None
    for name in RENDER_DIRS:
        built = root / name
        if not built.is_dir():
            continue
        chunks = []
        for page in sorted(built.rglob("*.html")):
            html = read(page) or ""
            html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.S | re.I)
            html = re.sub(r"<[^>]+>", " ", html)
            for ent, ch in _ENTITIES.items():
                html = html.replace(ent, ch)
            html = re.sub(r"&#(\d+);", lambda m: chr(int(m.group(1))), html)
            chunks.append(html)
        if chunks:
            out = normalise(" ".join(chunks))
            break
    _rendered_cache[root] = out
    return out


def _looks_like_copy(literal: str) -> bool:
    """A quoted literal that could plausibly be user-visible text."""
    if not literal or literal[0].islower() and " " not in literal:
        return False
    if CODE_FRAGMENT_RE.search(literal):
        return False
    # Prose has at least two word characters in a row somewhere, and at least
    # one letter. "} ${selected.has(i) ? " has neither once operators are gone.
    if not re.search(r"[A-Za-z]{2,}", literal):
        return False
    # A lone ALL-CAPS token is an identifier -- ENOENT, README. A lone
    # capitalised one is a button label -- Publish, Archive -- and excluding
    # those would silently switch B022 off for exactly the strings it exists
    # to catch.
    if " " not in literal and literal.isupper():
        return False
    # A lone token opening with `-` or `.` is a flag or a file extension:
    # `--force`, `.mdc`, `.cursor`. Nobody reads them as sentences.
    if " " not in literal and literal[0] in "-.":
        return False
    if literal.strip() in DIRECTIVES:
        return False
    return True


# Language directives that are quoted strings and never reach a user.
DIRECTIVES = {"use strict", "use client", "use server"}


LABEL_KEY_RE = re.compile(
    r"^(button|cta|label|title|heading|header|menu|tab|nav|placeholder"
    r"|action|link|toggle|chip|badge)\b", re.IGNORECASE
)


def check_consistency(brand_dir: Path, sources: dict) -> list[Finding]:
    """B020-B025 -- the registry, the code and the casing agree."""
    findings: list[Finding] = []
    root = brand_dir.parent.parent
    rows = registry(brand_dir)
    _, _, entities = dictionary(brand_dir)
    entity_words = {name for name, _ in entities}

    swept: set[str] = set()   # one unregistered-literal sweep per file
    by_key: dict[str, set] = {}
    for row in rows:
        by_key.setdefault(row["key"], set()).add(row["text"])
    for key, texts in sorted(by_key.items()):
        if len(texts) > 1:
            listed = " / ".join(f'"{t}"' for t in sorted(texts))
            findings.append(Finding(
                "B020", SEVERITY_ERROR, "strings.md", 0,
                f"one action, two names -- `{key}` is {listed}. An action "
                f"keeps one name across the whole flow",
            ))

    # B026 -- a label is a name, not a statement, so it ends with nothing.
    # Scoped by key prefix rather than by guessing at the text: a message may
    # be a sentence and should be, while a button that ends in a full stop is
    # the single most common tell that prose leaked into a control.
    for row in rows:
        if not LABEL_KEY_RE.match(row["key"]):
            continue
        text = row["text"].rstrip()
        if not text.endswith(".") or text.endswith("..") or text.endswith("…"):
            continue
        if ". " in text:      # genuinely several sentences -- a different defect
            continue
        findings.append(Finding(
            "B026", SEVERITY_WARN, "strings.md", 0,
            f"`{row['key']}` ends in a full stop: \"{text}\". A label, button, "
            f"menu item or title is a name and takes no terminal punctuation",
        ))

    for row in rows:
        location = row["location"]
        file_part = location.split(":")[0]
        target = root / file_part
        if not target.is_file():
            findings.append(Finding(
                "B023", SEVERITY_ERROR, location, 0,
                f"`{row['key']}` points at {file_part}, which does not exist",
            ))
            continue

        body = read(target) or ""
        literals = [
            lit for lit in code_literals(_strip_comments(body, target.suffix))
            if _looks_like_copy(lit)
        ]
        if literals:
            # The registry records what a reader sees, so the built page is the
            # authority whenever there is one. Source is the fallback and stays
            # byte-exact for projects that do not build.
            built = rendered_text(root)
            if built is not None:
                if normalise(row["text"]) not in built:
                    findings.append(Finding(
                        "B021", SEVERITY_ERROR, location, 0,
                        f"`{row['key']}` is \"{row['text']}\" in the registry, "
                        f"but that text is not on the rendered page",
                    ))
            # Byte-exact first, and that stays the invariant `strings.md`
            # documents: escape sequences included, so a row holding `\n---`
            # is compared as the three characters the source carries.
            #
            # The wrap-tolerant form is a FALLBACK, not a loosening, and it
            # exists because without it a wrapped block is unregisterable by
            # construction -- B022 would demand a row for `usage()` that B021
            # would then refuse, which is a check with no passing answer. It
            # compares the same wording across a newline the reader never sees,
            # which is exactly what the rendered-page branch above already does.
            elif row["text"] not in body \
                    and row["text"].strip() not in body \
                    and normalise(row["text"]) not in normalise(body):
                findings.append(Finding(
                    "B021", SEVERITY_ERROR, location, 0,
                    f"`{row['key']}` is \"{row['text']}\" in the registry, "
                    f"but that text is not in {file_part} (no build found; "
                    f"checked the source)",
                ))
            if file_part not in swept:
                swept.add(file_part)
                known = {r["text"] for r in rows}
                trimmed = {t.strip() for t in known}
                for lit in dict.fromkeys(literals):   # one report per literal
                    if lit not in known and lit.strip() not in trimmed:
                        findings.append(Finding(
                            "B022", SEVERITY_WARN, f"{file_part}", 0,
                            f"\"{lit}\" is in the code with no registry row -- "
                            f"agree it or retire it",
                        ))

    proper: set[str] = set()
    for name in entity_words:
        proper.update(name.split())
    for row in rows:
        # Escape sequences are not words: "\\n--- Skills for ..." begins with a
        # token whose only letter is the n of \\n.
        readable = re.sub(r"\\[nrt]|\\x[0-9a-fA-F]{2}\[[0-9;]*[A-Za-z]", " ",
                          row["text"])
        words = readable.split()
        first = next(
            (i for i, w in enumerate(words) if re.search(r"[A-Za-z]", w)), 0
        )
        for index, word in enumerate(words[first + 1:], start=first + 1):
            stripped = word.strip(".,:;!?()[]\"'")
            if stripped in proper or (stripped.isupper() and len(stripped) > 1):
                continue        # a declared entity, or an acronym like AI / CLI
            # A capital after a full stop is a sentence, not Title Case. The
            # check read "…development. Select what to install:" as miscased
            # until super-ux ran it over its own menu.
            if words[index - 1].rstrip('"\')').endswith((".", "!", "?", ":")):
                continue
            bare = word.strip(".,:;!?()")
            if not bare or bare in entity_words:
                continue
            if bare.isupper() and len(bare) <= 4:
                continue
            # A contraction of "I" is not Title Case, and flagging it fought a
            # threshold this pack sets on purpose: formats.md asks for 4-8
            # contractions per 1000 words and the first-person ones are the
            # loudest available. Three registry rows on sshlg.me tripped this on
            # 2026-08-15 and none of them was miscased; the writer's only repair
            # was to delete the contraction the pack had asked for.
            if CONTRACTED_I.match(bare):
                continue
            if bare[0].isupper():
                findings.append(Finding(
                    "B024", SEVERITY_ERROR, row["location"], 0,
                    f"`{row['key']}` is not sentence case: \"{row['text']}\"",
                ))
                break
        if row["key"].startswith("button.") and \
                row["text"].strip().lower() in WEAK_LABELS:
            findings.append(Finding(
                "B025", SEVERITY_WARN, row["location"], 0,
                f"`{row['key']}` is \"{row['text']}\" -- a button says what "
                f"happens, not that something happens",
            ))

    return findings


FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
# A figure is a claim. An identifier, a standard's designation and a year are
# not, and B030 read all three as unsourced claims until this project ran the
# linter over its own README: `BP-079`, `NIST SP 800-63B` and `Apple HIG 2025`
# each produced an error nobody could act on. The check had the right shape
# and the wrong meaning, and only a pack pointed at real prose could tell.
NUMBER_RE = re.compile(
    r"""
      \d+\s?%                        # 40%, 40 %
    | [$€£]\s?\d[\d,.]*              # $3.10, €1,200
    | (?<![A-Za-z]-)                  # not the tail of BP-079, SCN-001, PRN-24
      (?<!\.\.)                       # not the far end of a range: BP-079..090
      (?<!\d-)                        # not the tail of 800-63B
      \b\d{3,}\b
      (?![-\d])                       # not the head of 800-63B
    """,
    re.VERBOSE,
)

# A bare four-digit year dates a claim; it is not the claim.
YEAR_RE = re.compile(r"^(?:19|20)\d{2}$")
SUPERLATIVES = (
    "the best", "best-in-class", "leading", "fastest", "most trusted",
    "#1", "number one", "world-class", "unmatched",
)


def _front_matter(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    fields = {}
    for line in match.group(1).splitlines():
        pair = re.match(r"^([\w-]+):\s*(.*)$", line)
        if pair:
            fields[pair.group(1)] = pair.group(2).strip()
    return fields, text[match.end():]


# A source file is not prose, and the prose rules were reading all of it. On
# sshlg.me that produced 20 rhetorical-dash errors inside `//` comments and 7
# keyword-stuffing errors on `const`, `string` and `name` -- 27 standing errors
# that no edit to the copy could clear, in a report meant to be read. A report
# nobody can act on is a report nobody reads, which is the same failure as a
# rule that contradicts a threshold.
#
# For a code file the body is its copy: the string literals `_looks_like_copy`
# accepts, which is the definition `B022` already sweeps with. A comment is
# addressed to a maintainer and an identifier is not a word; a brand pack has no
# opinion about either.
CODE_SUFFIXES = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".py", ".go", ".rb", ".rs", ".java", ".kt", ".swift", ".php",
}

# `${...}` in a template literal is a value, not a word.
#
# Replaced by a space rather than dropped, so `founder of ${n} products` does not
# collapse into one word. Substituted rather than left in place, because
# `CODE_FRAGMENT_RE` rejects any literal carrying an interpolation -- so without
# this line every interpolated string would fail `_looks_like_copy` and
# interpolated copy would lose its coverage entirely. That would be a worse bug
# than the one this fixes: on sshlg.me the whole biography is interpolated.
INTERPOLATION_RE = re.compile(r"\$\{[^{}]*\}")


# Languages whose line comment is `#` rather than `//`.
HASH_COMMENT_SUFFIXES = {".py", ".rb"}


def _strip_comments(text: str, suffix: str) -> str:
    """Remove comments, leaving string literals untouched.

    A regex cannot do this and the first version of this fix tried: `"https://x"`
    contains `//`, and a comment can quote a phrase, which is how
    `// "AI integrations" named nothing checkable -- and "AI" is the medium` came
    back as a rhetorical-dash error in copy on the first run of the very change
    that was supposed to stop reading comments.

    The scanner is small because it only has to know one thing at a time:
    whether it is currently inside a quote.
    """
    hashed = suffix in HASH_COMMENT_SUFFIXES
    out: list[str] = []
    quote = None
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < n:      # an escaped quote is not the end
                out.append(text[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "\"'`":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if hashed and ch == "#":
            while i < n and text[i] != "\n":
                i += 1
            continue
        if not hashed and text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
            continue
        if not hashed and text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = n if end == -1 else end + 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _copy_in_code(text: str, suffix: str = ".ts") -> str:
    """The user-visible strings in a source file, joined as prose."""
    out = []
    for literal in code_literals(_strip_comments(text, suffix)):
        candidate = re.sub(r"\s{2,}", " ", INTERPOLATION_RE.sub(" ", literal)).strip()
        # A literal with no space is an import path, an identifier or a one-word
        # label. None of them can carry a rhetorical dash or stuff a keyword, and
        # `"@/data/site"` counted as copy would put `data` into the density
        # figures. B022 still sees them; these checks do not need to.
        if " " not in candidate:
            continue
        if _looks_like_copy(candidate):
            out.append(candidate)
    return "\n\n".join(out)


def documents(brand_dir: Path, sources: dict, key: str) -> list[tuple]:
    """(relative path, front matter, body) for one declared source key."""
    root = brand_dir.parent.parent
    out = []
    for pattern in sources.get(key, []):
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            fields, body = _front_matter(read(path) or "")
            if path.suffix in CODE_SUFFIXES:
                body = _copy_in_code(body, path.suffix)
            out.append((path.relative_to(root).as_posix(), fields, body))
    return out


def surfaces(brand_dir: Path) -> dict[str, dict]:
    """`channels.md` records: surface name -> field dict."""
    text = read(brand_dir / "channels.md") or ""
    out: dict[str, dict] = {}
    for match in re.finditer(r"^### (.+?)$\s*```(.*?)```", text, re.M | re.S):
        record = {}
        for line in match.group(2).splitlines():
            pair = re.match(r"^([A-Za-z][A-Za-z ]*?):\s*(.*)$", line)
            if pair:
                record[pair.group(1).strip()] = pair.group(2).strip()
        out[match.group(1).strip()] = record
    return out


def tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """The same rows, but grouped per table as (header, data rows).

    `table_rows` flattens every table in a file into one list, which is right
    for a caller that wants every row and wrong for one that wants the rows of
    a particular table. `facts()` was the second kind and used the first: it
    took any six-column row anywhere in facts.md, so the App Store table --
    `Product | App Store name | id | Released | Sold | Publisher today` -- was
    read as six fact fields. Its **Sold** year landed in `Review`, which
    produced three "was due for review on 2022" warnings about sales that
    completed on schedule, and its own header row became a fact called
    `Product`. Four phantom rows in a registry of 43.

    What it did **not** do, checked before this comment was written: the App
    Store ids were already registered properly, by the `Sold-app store ids` row,
    so the B030 corpus was never widened by the bug. Only the product names
    entered it, and B030 only reads numbers.

    A table is identified by its header, because that is the only thing in a
    markdown table that says what its columns mean.
    """
    blocks, current = [], []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            current.append(line)
        elif current:
            rows = table_rows("\n".join(current))
            if rows:
                blocks.append((rows[0], rows[1:]))
            current = []
    if current:
        rows = table_rows("\n".join(current))
        if rows:
            blocks.append((rows[0], rows[1:]))
    return blocks


def facts(brand_dir: Path) -> list[dict]:
    rows = []
    for header, body in tables(read(brand_dir / "facts.md") or ""):
        # Scoped by header rather than by column count -- see tables(). Any
        # six-column table in this file used to qualify, and one of them is a
        # product ledger whose columns mean something else entirely.
        if len(header) < 6 or header[0].strip().lower() != "fact":
            continue
        for cells in body:
            if len(cells) < 6:
                continue
            if unfilled(cells[0]) or unfilled(cells[1]):
                continue
            rows.append({
                "fact": cells[0], "value": cells[1], "source": cells[2],
                "checked": cells[3], "review": cells[4], "public": cells[5],
            })
    return rows


def _today() -> str:
    import datetime

    return datetime.date.today().isoformat()


def _fact_figures(value: str) -> set[str]:
    """Every figure ONE fact's `Value` sources, normalised the way copy is read.

    B030 compares a figure in public copy against this set exactly. Until
    2026-08-20 it compared against every value joined into a single string and
    asked `compact not in known.replace(" ", "")` -- so the corpus was one
    character sequence and every SUBSTRING of it counted as sourced. With this
    pack's own seven public rows the corpus was `7158215243770+`, which sourced
    the invented `1582` in "super-ux ... ships 1582 checks": the linter printed
    `brand pack is clean` and exited 0. An invented public number passing the
    check whose entire purpose is to refuse one is the worst failure this file
    can have, because it is indistinguishable from working.

    Three forms are accepted, and each is the same claim written differently:
    the value with its whitespace removed; the same with a bound marker stripped,
    so a row of `500+` sources the `500` a sentence writes; and whatever the
    figure regex reads INSIDE the value, so `$3.10` and a thousands separator are
    matched in the form copy uses. Nothing else -- a figure not written in the
    table is not in the table.
    """
    compact = re.sub(r"\s+", "", value)
    figures = {compact, compact.strip("+~><≈").strip()}
    figures.update(m.replace(" ", "") for m in NUMBER_RE.findall(value))
    return {f for f in figures if f}


def check_facts(brand_dir: Path, sources: dict) -> list[Finding]:
    """B030-B033 -- every figure traces to a row, every row to a source."""
    findings: list[Finding] = []
    rows = facts(brand_dir)
    known: set[str] = set()
    for row in rows:
        if row["public"].lower() != "no":
            known |= _fact_figures(row["value"])

    # B033 -- `Fact` is the key a figure is cited by, and a table with two rows
    # under one key has no answer to "what is that number". Watched: a second
    # `| skills shipped | 99 |` row left the pack clean AND put `99` into the
    # sourced corpus, so the duplicate did not merely go unreported -- it
    # licensed a wrong figure in public copy. An error, not a warning: the two
    # rows disagree by construction and no reader can tell which one is meant.
    by_key: dict[str, int] = {}
    for row in rows:
        key = normalise(row["fact"]).lower()
        by_key[key] = by_key.get(key, 0) + 1
    for key, count in sorted(by_key.items()):
        if count > 1:
            findings.append(Finding(
                "B033", SEVERITY_ERROR, "facts.md", 0,
                f"`{key}` has {count} rows -- a fact is cited by its name, and "
                f"two rows under one name make every figure quoting it "
                f"ambiguous. Retire one or rename both",
            ))

    for row in rows:
        if unfilled(row["source"]):
            findings.append(Finding(
                "B031", SEVERITY_WARN, "facts.md", 0,
                f"`{row['fact']}` has no source -- an unsourced fact is an "
                f"opinion with a number on it",
            ))
        elif row["review"] and not row["review"].startswith("<") \
                and row["review"] < _today():
            findings.append(Finding(
                "B031", SEVERITY_WARN, "facts.md", 0,
                f"`{row['fact']}` was due for review on {row['review']}",
            ))

    for path, _fields, body in documents(brand_dir, sources, "marketing"):
        for number in NUMBER_RE.findall(body):
            compact = number.replace(" ", "")
            if YEAR_RE.match(compact):
                continue
            if compact not in known:
                findings.append(Finding(
                    "B030", SEVERITY_ERROR, path, 0,
                    f"`{number}` appears in public copy with no row in "
                    f"facts.md -- a number nobody can check is a claim "
                    f"nobody should make",
                ))
        for paragraph in re.split(r"\n\s*\n", body):
            lowered = paragraph.lower()
            for superlative in SUPERLATIVES:
                if superlative in lowered and not re.search(r"\d", paragraph):
                    findings.append(Finding(
                        "B032", SEVERITY_ERROR, path, 0,
                        f"`{superlative}` with nothing beside it to back it",
                    ))
                    break
    return findings


def _limits(record: dict) -> dict[str, int]:
    out: dict[str, int] = {}
    for part in record.get("Limits", "").split(","):
        pair = re.match(r"^\s*([\w ]+?)\s+(\d+)\s*$", part)
        if pair:
            out[pair.group(1).strip().lower()] = int(pair.group(2))
    return out


def _coefficient(brand_dir: Path, locale: str | None) -> float:
    if not locale:
        return 1.0
    text = read(brand_dir / "locales" / f"{locale}.md") or ""
    value = header_field(text, "Length coefficient")
    try:
        return float(value) if value else 1.0
    except ValueError:
        return 1.0


def check_channels(brand_dir: Path, sources: dict) -> list[Finding]:
    """B040-B043 -- platform physics, applied with the locale's coefficient."""
    findings: list[Finding] = []
    records = surfaces(brand_dir)

    for key in ("marketing", "store"):
        for path, fields, body in documents(brand_dir, sources, key):
            record = records.get(fields.get("surface", ""))
            if not record:
                continue
            locale = fields.get("locale")
            factor = _coefficient(brand_dir, locale)
            for name, limit in _limits(record).items():
                value = body if name == "body" else fields.get(name, "")
                allowed = int(limit * factor)
                if value and len(value.strip()) > allowed:
                    # Same overflow, two codes on purpose: B040 is the
                    # primary-locale case, B073 the one the coefficient
                    # created. They are fixed differently -- one shortens the
                    # string, the other questions the original design.
                    code = "B073" if locale else "B040"
                    findings.append(Finding(
                        code, SEVERITY_ERROR, path, 0,
                        f"{name} is {len(value.strip())} characters, over the "
                        f"{allowed} this surface allows"
                        + (f" for `{locale}` (coefficient {factor})"
                           if locale else ""),
                    ))

            physics = record.get("Forbidden", "").split("|")[0].lower()
            if "link in body" in physics and re.search(r"https?://", body):
                findings.append(Finding(
                    "B042", SEVERITY_ERROR, path, 0,
                    "link in the post body -- this surface suppresses reach "
                    "for it; the convention is the first reply",
                ))
            cap = re.search(r"max (\d+) hashtags", physics)
            if cap:
                used = re.findall(r"(?<!\w)#\w+", body)
                if len(used) > int(cap.group(1)):
                    findings.append(Finding(
                        "B043", SEVERITY_WARN, path, 0,
                        f"{len(used)} hashtags, over the {cap.group(1)} this "
                        f"surface tolerates",
                    ))

            keywords = fields.get("keywords")
            if keywords is not None:
                findings.extend(_ios_keywords(path, fields, keywords))
    return findings


def _ios_keywords(path: str, fields: dict, raw: str) -> list[Finding]:
    """B041 -- the four rules that recover a third of the 100-character field."""
    findings = []
    if ", " in raw:
        findings.append(Finding(
            "B041", SEVERITY_ERROR, path, 0,
            "space after a comma in the keyword field -- each one is a "
            "character bought for nothing",
        ))
    terms = [t.strip() for t in raw.split(",") if t.strip()]
    singulars = {t[:-1] for t in terms if t.endswith("s")}
    for term in terms:
        if term in singulars:
            findings.append(Finding(
                "B041", SEVERITY_ERROR, path, 0,
                f"`{term}` and its plural are both listed -- the store "
                f"matches both forms from the singular",
            ))
    title = fields.get("title", "").lower()
    for term in terms:
        if term.lower() in title.split():
            findings.append(Finding(
                "B041", SEVERITY_ERROR, path, 0,
                f"`{term}` is already in the title, which is indexed at "
                f"higher weight -- the field spends it twice",
            ))
    return findings


AI_AGENTS = ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended")

FILLER_OPENERS = (
    "in today's digital landscape", "in the ever-evolving world",
    "in today's fast-paced", "in an increasingly", "in the modern era",
)

# S1 markers only -- the ones decisive on their own. The full catalogue,
# with S2 and S3, is in references/ai-tells.md.
S1_MARKERS = (
    "delve", "it is important to note", "it's important to note",
    "it is worth noting", "in conclusion", "needless to say",
    "landscape of", "leverage the", "robust and", "seamless integration",
    "crucial to", "navigate the complexities",
)

STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "your", "you",
    "are", "was", "were", "have", "has", "had", "not", "but", "all",
    "can", "will", "into", "than", "then", "them", "they", "our", "its",
    "some", "other", "here", "more", "most", "when", "what", "which",
}

SENSITIVE_PREFIXES = ("error.", "destructive.", "billing.", "paywall.")
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF☀-➿️]"
)

# AT-06, the rhetorical dash. The rule is a distinction, not a ban: a dash
# standing in for a full stop, a comma or a colon is the machine-drafting
# marker, and a dash the language requires is grammar. Stripping both
# produces ungrammatical Russian, so the checks below are ordered by what
# can actually be established without parsing the sentence.
DASH = "—"

# Every spelling of the same mark. The tell is the ROLE the dash plays, not
# the codepoint it is written with: swapping "—" for "–", or for a hyphen
# with a space each side, leaves the habit exactly where it was, and a check
# bound to one codepoint cannot see that it happened. Measured on
# trycomp.ai, 2026-08-30: twenty rhetorical dashes, zero em dashes, every
# one of them written " - ". See `docs/research/landings/trycomp.md`.
DASH_ALIASES = "–‒―"

# A dash alone in a table cell stands for "no value": a glyph doing the job
# of an empty string, not punctuation joining two clauses. AT-06 has said so
# since it was written, and until the spellings were normalised nothing
# implemented it, so a bare cell dash was reported in every strict locale.
TABLE_CELL_DASH_RE = re.compile(rf"(?<=\|)([ \t]*)[{DASH}{DASH_ALIASES}-]([ \t]*)(?=\|)")

# A hyphen with whitespace on both sides, mid-line. The lookbehind is what
# keeps a markdown bullet out of it: a list item's hyphen opens its line, so
# nothing non-space precedes the indent in front of it.
DASH_HYPHEN_RE = re.compile(r"(?<=\S)([ \t]+)-([ \t]+)(?=\S)")
DASH_ALIAS_RE = re.compile(rf"[{DASH_ALIASES}]")

# Never a finding. A range is arithmetic and direct speech is a convention.
DASH_RANGE_RE = re.compile(rf"\d\s*{DASH}\s*\d")
DASH_SPEECH_RE = re.compile(rf"^\s*{DASH}\s")

# Rhetorical in every language: a dash cannot introduce a coordinating
# conjunction, because that is a comma's job. The copula dash is never
# followed by one, which is what makes this safe to run on Russian.
DASH_CONJ_RE = re.compile(
    rf"{DASH}\s+(?:и|а|но|или|да|and|but|or|so|yet|nor)\s",
    re.I,
)

# Locales whose orthography requires a dash between subject and predicate
# when the verb is absent (<<Москва — столица>>). Deliberately short: a
# language belongs here only when the construction is a rule of its
# orthography rather than a stylistic option, and a wrong entry silently
# switches the strict check off for a whole language.
COPULA_LOCALES = ("ru", "uk", "be")
CYRILLIC_RE = re.compile("[Ѐ-ӿ]")

# A title is a name. `.` ends a statement, so it does not belong; `?` and
# `…` do, because a title may genuinely ask or genuinely trail off.
ABBREVIATION_RE = re.compile(r"(?:\b[A-Za-z]\.[A-Za-z]\.|\b(?:etc|vs|Inc|Ltd|Co|jr|sr|no)\.|\.[a-z]{2,4})$", re.I)


def prose_only(text: str) -> str:
    """Fenced blocks and inline code are not prose and never carry a tell."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def normalise_dash_spelling(text: str) -> str:
    """Reduce every spelling of the rhetorical mark to the canonical dash.

    Length-preserving by construction -- every substitution swaps a single
    character for a single character -- so a finding can quote the author's
    own characters while the branches below judge the normalised ones. A
    quote showing a dash the author never typed sends them grepping for it.
    """
    text = TABLE_CELL_DASH_RE.sub(r"\1 \2", text)
    text = DASH_HYPHEN_RE.sub(rf"\1{DASH}\2", text)
    return DASH_ALIAS_RE.sub(DASH, text)


def sentences(text: str) -> list[str]:
    """Crude split, sufficient to count dashes inside one sentence."""
    return [p for p in re.split(r"(?<=[.!?])\s+|\n\s*\n", text) if p.strip()]


def grammatical_dash_language(text: str, primary: str | None) -> bool:
    """Does a grammatical dash exist in the language this text is written in?

    Two signals, and either is enough, because the consequence of guessing
    wrong in one direction is a linter that calls correct Russian an error.
    A missed rhetorical dash is a style note; a false error on grammar is
    how a check gets switched off.
    """
    if primary and primary.split("-")[0].lower() in COPULA_LOCALES:
        return True
    return bool(CYRILLIC_RE.search(text))


def _around(sentence: str, original: str | None = None, width: int = 34) -> str:
    """The dash with enough either side to find it and decide the fix.

    `sentence` is normalised and `original` is what the author wrote. The
    position comes from the first and the characters from the second, which
    is why the substitutions above are length-preserving: a quote is only
    useful if it can be found in the file it came from.
    """
    source = sentence if original is None else original
    at = sentence.find(DASH)
    if at < 0:
        return " ".join(source.split())[:width * 2]
    start, end = max(0, at - width), min(len(source), at + width)
    return (("…" if start else "")
            + " ".join(source[start:end].split())
            + ("…" if end < len(source) else ""))


def dash_findings(code: str, path: str, text: str, strict: bool) -> list[Finding]:
    """AT-06 over one body of prose. `strict` bans every non-range dash.

    Every finding quotes the dash in context and carries the line it sits on.
    Thirty-seven findings reading "a dash stands in for a full stop" is a
    report nobody can act on, and a check nobody can act on gets switched
    off rather than obeyed.
    """
    findings: list[Finding] = []
    raw = prose_only(text)
    body = normalise_dash_spelling(raw)
    if DASH not in body:
        return findings

    # Line numbers come from the stripped body, so a dash inside a fenced
    # block cannot shift the number of one in the prose after it.
    offsets = {}
    cursor = 0
    for number, line in enumerate(body.splitlines(keepends=True), start=1):
        offsets[cursor] = number
        cursor += len(line)

    def line_of(fragment: str) -> int:
        at = body.find(fragment[:40])
        if at < 0:
            return 0
        best = 0
        for start, number in offsets.items():
            if start <= at:
                best = number
            else:
                break
        return best

    # `raw` and `body` are the same length and split at the same points --
    # normalisation touches neither terminal punctuation nor newlines -- so
    # the two sentence lists stay aligned and the quote comes from the raw.
    for sentence, original in zip(sentences(body), sentences(raw)):
        if DASH not in sentence:
            continue
        if DASH_SPEECH_RE.match(sentence):
            continue

        line = line_of(sentence)
        quoted = _around(sentence, original)

        conj = DASH_CONJ_RE.search(sentence)
        if conj:
            findings.append(Finding(
                code, SEVERITY_ERROR, path, line,
                f'a dash introduces "{conj.group(0).strip()}", which is a '
                f"comma's job; no language puts a grammatical dash before a "
                f'conjunction: "{quoted}"',
            ))
            continue

        bare = sentence.count(DASH) - len(DASH_RANGE_RE.findall(sentence))
        if bare >= 2:
            findings.append(Finding(
                code, SEVERITY_ERROR, path, line,
                f"{bare} dashes bracket an aside in one sentence, which is "
                f'the parenthetical reflex; use commas or brackets: "{quoted}"',
            ))
            continue

        if strict and bare > 0:
            findings.append(Finding(
                code, SEVERITY_ERROR, path, line,
                f"a dash stands in for a full stop, a comma or a colon, and "
                f"this locale has no grammatical dash; pick the mark that "
                f'states the real relationship: "{quoted}"',
            ))
    return findings


def title_full_stop(title: str) -> bool:
    """AT-07. True when a title ends in a full stop that is a full stop."""
    text = title.strip()
    if not text.endswith("."):
        return False
    if text.endswith("..") or text.endswith("…"):
        return False
    if ". " in text:            # several sentences -- a different defect
        return False
    return not ABBREVIATION_RE.search(text)


def check_bot_safety(brand_dir: Path, sources: dict) -> list[Finding]:
    """B050-B054 -- do not write text that looks like gaming a crawler."""
    findings: list[Finding] = []
    channels = read(brand_dir / "channels.md") or ""
    targets_ai = "AI search: target" in channels

    if targets_ai and "robots" in sources:
        for path, _fields, _body in [
            (p, {}, "") for p in sources["robots"]
        ]:
            robots = read(brand_dir.parent.parent / path) or ""
            blocks = []
            agent = None
            for line in robots.splitlines():
                head = re.match(r"^User-agent:\s*(.+?)\s*$", line, re.I)
                if head:
                    agent = head.group(1).strip()
                elif re.match(r"^Disallow:\s*/\s*$", line, re.I) and agent:
                    if agent in AI_AGENTS:
                        blocks.append(agent)
            if blocks:
                findings.append(Finding(
                    "B050", SEVERITY_ERROR, path, 0,
                    f"channels.md declares AI search a target while "
                    f"{', '.join(blocks)} is blocked here -- content quality "
                    f"is irrelevant to a crawler that never arrives",
                ))

    records = surfaces(brand_dir)
    marketing = documents(brand_dir, sources, "marketing")

    # Density is a property of the DOCUMENT a reader meets, and a code file is
    # not one. A project that keeps its copy in `src/data/*.ts` splits one page
    # across seven files, and measuring each file separately measures the split:
    # on sshlg.me that produced six errors -- `co-founder` at 2.0% of
    # `track-record.ts`, `account` at 1.2% of `site.ts` -- while the rendered
    # page carried nothing above 1% and those two words sat at 0.07% and 0.04%.
    #
    # So the code files are pooled into one document and the markdown ones are
    # not, because there one file really is one page. The pooled finding names
    # the set rather than a file, since no single file is the defect.
    pooled = [d for d in marketing if Path(d[0]).suffix in CODE_SUFFIXES]
    per_file = [d for d in marketing if Path(d[0]).suffix not in CODE_SUFFIXES]
    if pooled:
        label = (f"{len(pooled)} source file(s) pooled"
                 if len(pooled) > 1 else pooled[0][0])
        per_file.append((label, {}, "\n\n".join(d[2] for d in pooled)))

    for path, fields, body in per_file:
        words = [w.lower().strip(".,:;!?()\"'") for w in body.split()]
        real = [w for w in words if len(w) > 3 and w not in STOPWORDS]
        if len(real) >= 40:
            counts: dict[str, int] = {}
            for word in real:
                counts[word] = counts.get(word, 0) + 1
            for word, count in sorted(counts.items()):
                if count / len(words) > 0.01:
                    findings.append(Finding(
                        "B051", SEVERITY_ERROR, path, 0,
                        f"`{word}` is {count / len(words):.1%} of the "
                        f"document -- above 1% reads as stuffing, which "
                        f"lowers citation likelihood rather than raising it",
                    ))
                    break

    for path, fields, body in marketing:

        opening = body.strip().lower()[:120]
        for filler in FILLER_OPENERS:
            if opening.startswith(filler) or f"\n{filler}" in opening:
                findings.append(Finding(
                    "B052", SEVERITY_ERROR, path, 0,
                    f"filler opener \"{filler}…\" -- it delays the answer "
                    f"past the point where extraction happens",
                ))
                break

        record = records.get(fields.get("surface", ""))
        if record and "author" in record.get("Proof", "").lower():
            if not fields.get("author"):
                findings.append(Finding(
                    "B053", SEVERITY_WARN, path, 0,
                    "no named author, and this surface makes claims that "
                    "need one",
                ))

        title = fields.get("title", "")
        promised = re.match(r"^\s*(\d+)\b", title)
        if promised:
            items = len(re.findall(r"^\s*(?:[-*]|\d+\.)\s+", body, re.M))
            headings = len(re.findall(r"^#{2,}\s+", body, re.M))
            if max(items, headings) < int(promised.group(1)):
                findings.append(Finding(
                    "B054", SEVERITY_WARN, path, 0,
                    f"the title promises {promised.group(1)} and the body "
                    f"delivers {max(items, headings)}",
                ))
    return findings


def check_ai_tells(brand_dir: Path, sources: dict) -> list[Finding]:
    """B060-B063 -- machine-drafting markers, and the one absolute ban.

    B060 counts vocabulary markers, B061 bans levity where the user is
    losing something, B062 is AT-06 (the rhetorical dash) and B063 is AT-07
    (a title that ends in a full stop) outside the string registry, which
    B026 already covers. The grades and the reasoning are in
    `references/ai-tells.md`; this file carries only the provable subset.
    """
    findings: list[Finding] = []
    primary, _others = declared_locales(brand_dir)

    for path, _fields, body in documents(brand_dir, sources, "marketing"):
        lowered = body.lower()
        hits = [m for m in S1_MARKERS if m in lowered]
        if not hits:
            continue
        grade = "B" if len(hits) < 3 else "C"
        severity = SEVERITY_ERROR if len(hits) >= 3 else SEVERITY_WARN
        findings.append(Finding(
            "B060", severity, path, 0,
            f"{len(hits)} S1 marker(s) -- {', '.join(sorted(hits))}. "
            f"Naturalness grade {grade}",
        ))

    # B062 -- the rhetorical dash, in every surface that ships prose.
    for key in ("marketing", "store"):
        for path, fields, body in documents(brand_dir, sources, key):
            text = f"{fields.get('title', '')}\n{body}"
            strict = not grammatical_dash_language(text, primary)
            findings.extend(dash_findings("B062", path, body, strict))

    for row in registry(brand_dir):
        strict = not grammatical_dash_language(row["text"], primary)
        findings.extend(dash_findings("B062", row["location"], row["text"], strict))

    # B063 -- AT-07 outside the registry: document titles and the headings
    # inside them. B026 owns the same rule for `strings.md`, and the two are
    # split by artifact rather than by rule so that neither can be satisfied
    # by fixing the other.
    for key in ("marketing", "store"):
        for path, fields, body in documents(brand_dir, sources, key):
            title = fields.get("title", "")
            if title and title_full_stop(title):
                findings.append(Finding(
                    "B063", SEVERITY_WARN, path, 0,
                    f'the title ends in a full stop: "{title.strip()}". '
                    f"A title is a name, not a statement",
                ))
            for heading in re.findall(r"^#{1,6}\s+(.+?)\s*$", prose_only(body), re.M):
                if title_full_stop(heading):
                    findings.append(Finding(
                        "B063", SEVERITY_WARN, path, 0,
                        f'a heading ends in a full stop: "{heading.strip()}". '
                        f"A heading is a name, not a statement",
                    ))

    for row in registry(brand_dir):
        if not row["key"].startswith(SENSITIVE_PREFIXES):
            continue
        text = row["text"]
        reason = None
        if "!" in text:
            reason = "an exclamation mark"
        elif EMOJI_RE.search(text):
            reason = "an emoji"
        if reason:
            findings.append(Finding(
                "B061", SEVERITY_ERROR, row["location"], 0,
                f"`{row['key']}` carries {reason}. The user is losing data, "
                f"access or money on this surface; levity reads as mockery "
                f"of a loss the product caused",
            ))
    return findings


def declared_locales(brand_dir: Path) -> tuple[str | None, list[str]]:
    """(primary, others) from voice.md's `Locales:` line."""
    text = read(brand_dir / "voice.md") or ""
    raw = header_field(text, "Locales") or ""
    primary, others = None, []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        code = part.split()[0]
        if "(primary)" in part:
            primary = code
        else:
            others.append(code)
    return primary, others


def check_locales(brand_dir: Path, sources: dict) -> list[Finding]:
    """B070-B072 -- a locale may lag, but it may not hide that it lags."""
    findings: list[Finding] = []
    primary, others = declared_locales(brand_dir)
    root = brand_dir.parent.parent

    for code in others:
        if not (brand_dir / "locales" / f"{code}.md").is_file():
            findings.append(Finding(
                "B070", SEVERITY_ERROR, "voice.md", 0,
                f"`{code}` is declared but has no locales/{code}.md -- "
                f"nothing records its address form, humor level or "
                f"length coefficient",
            ))

    threshold = header_field(read(brand_dir / "voice.md") or "",
                             "Locale parity threshold")
    limit = 0.0
    if threshold:
        try:
            limit = float(threshold.rstrip("%")) / 100
        except ValueError:
            limit = 0.0

    if primary and limit and "locales" in sources:
        catalogues: dict[str, set] = {}
        for pattern in sources["locales"]:
            for path in sorted(root.glob(pattern)):
                try:
                    data = json.loads(read(path) or "{}")
                except json.JSONDecodeError:
                    continue
                if isinstance(data, dict):
                    catalogues[path.stem] = set(data)
        base = catalogues.get(primary, set())
        for code in others:
            keys = catalogues.get(code)
            if base and keys is not None:
                parity = len(keys & base) / len(base)
                if parity < limit:
                    findings.append(Finding(
                        "B071", SEVERITY_WARN, f"locales/{code}.md", 0,
                        f"{code} covers {parity:.0%} of {primary}, under the "
                        f"declared {limit:.0%} -- {len(base - keys)} string(s) "
                        f"behind",
                    ))

    for code in others:
        text = read(brand_dir / "locales" / f"{code}.md") or ""
        for cells in table_rows(text):
            if len(cells) < 2 or cells[0].startswith("<"):
                continue
            if cells[0].strip().lower() in ("primary", "term"):
                continue
            if cells[0] and cells[0] == cells[1]:
                findings.append(Finding(
                    "B072", SEVERITY_WARN, f"locales/{code}.md", 0,
                    f"`{cells[0]}` is unchanged from the primary -- a "
                    f"word-for-word rendering translates the words and not "
                    f"the job the string does",
                ))
    return findings


FIXABLE = ("B024", "B041", "B023")


def apply_fixes(brand_dir: Path, findings: list[Finding]) -> int:
    """The subset that cannot be wrong. Everything else needs a human.

    B024 normalises casing, B041 tightens the iOS keyword field, and B023
    re-points a registry row when the string is unchanged and matches
    exactly one new location. Anything requiring a judgement about meaning
    is reported, never rewritten.
    """
    rewritten = 0
    root = brand_dir.parent.parent
    strings_path = brand_dir / "strings.md"
    text = read(strings_path)
    if text is None:
        return 0
    original = text

    _, _, entities = dictionary(brand_dir)
    entity_words = {name for name, _ in entities}
    for finding in findings:
        if finding.code != "B024":
            continue
        for row in registry(brand_dir):
            words = row["text"].split()
            fixed = [words[0]] + [
                w if (w.strip(".,:;!?()") in entity_words
                      or (w.isupper() and len(w) <= 4))
                else w[0].lower() + w[1:]
                for w in words[1:]
            ]
            replacement = " ".join(fixed)
            if replacement != row["text"]:
                text = text.replace(
                    f"| {row['text']} |", f"| {replacement} |"
                )

    for finding in findings:
        if finding.code != "B023":
            continue
        row_key = finding.message.split("`")[1]
        for row in registry(brand_dir):
            if row["key"] != row_key:
                continue
            matches = [
                p for p in root.rglob("*")
                if p.is_file() and p.suffix in (".ts", ".tsx", ".js", ".jsx")
                and row["text"] in (read(p) or "")
            ]
            if len(matches) == 1:
                new = matches[0].relative_to(root).as_posix()
                text = text.replace(row["location"], f"{new}:1")

    if text != original:
        strings_path.write_text(text, encoding="utf-8")
        rewritten += 1

    for path, fields, _body in documents(brand_dir, load_sources(brand_dir),
                                         "store"):
        raw = fields.get("keywords")
        if not raw or ", " not in raw:
            continue
        target = root / path
        body = read(target) or ""
        tightened = raw.replace(", ", ",")
        target.write_text(
            body.replace(f"keywords: {raw}", f"keywords: {tightened}"),
            encoding="utf-8",
        )
        rewritten += 1

    return rewritten


def run(brand_dir: Path, fix: bool = False) -> list[Finding]:
    """Every check, in order. `fix` is applied by the caller via apply_fixes."""
    sources = load_sources(brand_dir)
    findings: list[Finding] = []
    findings.extend(check_contract(brand_dir))
    findings.extend(check_terminology(brand_dir))
    findings.extend(check_consistency(brand_dir, sources))
    findings.extend(check_facts(brand_dir, sources))
    findings.extend(check_channels(brand_dir, sources))
    findings.extend(check_bot_safety(brand_dir, sources))
    findings.extend(check_ai_tells(brand_dir, sources))
    findings.extend(check_locales(brand_dir, sources))
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
    parser.add_argument(
        "--strict", action="store_true",
        help="let warnings fail the run too (same meaning as ux_lint.py --strict)",
    )
    args = parser.parse_args(argv)

    brand_dir = Path(args.path)
    if not brand_dir.is_dir():
        print(f"no brand pack at {brand_dir} -- run /brand-init")
        return 2

    findings = run(brand_dir, fix=args.fix)
    if args.fix:
        rewritten = apply_fixes(brand_dir, findings)
        print(f"--fix rewrote {rewritten} file(s)")
        findings = run(brand_dir)
    report(findings, args.brief, args.json)

    if any(f.severity == SEVERITY_ERROR for f in findings):
        return 2
    # A warning is advice about a judgement a person still has to make -- an
    # unregistered string, a fact past review, a label naming no outcome. It
    # blocks only when the caller asks, which is what `--strict` is for.
    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
