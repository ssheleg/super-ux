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


WEAK_LABELS = {
    "ok", "yes", "no", "submit", "done", "go", "click here",
    "learn more", "get started", "continue",
}

LITERAL_RE = re.compile(r"""(["'`])((?:(?!\1)[^\n]){3,200})\1""")

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
            lit for _q, lit in LITERAL_RE.findall(body) if _looks_like_copy(lit)
        ]
        if literals:
            if row["text"] not in body and row["text"].strip() not in body:
                findings.append(Finding(
                    "B021", SEVERITY_ERROR, location, 0,
                    f"`{row['key']}` is \"{row['text']}\" in the registry, "
                    f"but that text is not in {file_part}",
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


def documents(brand_dir: Path, sources: dict, key: str) -> list[tuple]:
    """(relative path, front matter, body) for one declared source key."""
    root = brand_dir.parent.parent
    out = []
    for pattern in sources.get(key, []):
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            fields, body = _front_matter(read(path) or "")
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


def facts(brand_dir: Path) -> list[dict]:
    rows = []
    for cells in table_rows(read(brand_dir / "facts.md") or ""):
        if len(cells) < 6 or cells[0].strip().lower() == "fact":
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


def check_facts(brand_dir: Path, sources: dict) -> list[Finding]:
    """B030-B032 -- every figure traces to a row, every row to a source."""
    findings: list[Finding] = []
    rows = facts(brand_dir)
    known = " ".join(r["value"] for r in rows if r["public"].lower() != "no")

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
            if compact not in known.replace(" ", ""):
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
    for path, fields, body in documents(brand_dir, sources, "marketing"):
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
    """B060-B061 -- machine-drafting markers, and the one absolute ban."""
    findings: list[Finding] = []

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
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
