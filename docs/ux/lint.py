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
            err(f"[U001] {label}: duplicate id {i} ({n} entries)")
    nums = sorted(int(i.split("-")[1]) for i in seen)
    if nums:
        missing = [n for n in range(1, max(nums) + 1) if n not in nums]
        if missing:
            warn(f"[U002] {label}: id gaps (retired entries should stay): {missing}")


def figma_enabled(foundation: str) -> bool | None:
    """True/False from foundation Design tooling; None if unstated (default-on)."""
    m = re.search(r"\*\*Figma:\*\*\s*(enabled|disabled)", foundation, re.IGNORECASE)
    if not m:
        return None
    return m.group(1).lower() == "enabled"


def entry_blocks(text: str, prefix: str) -> dict[str, str]:
    """Map PREFIX-id -> its section body (from its header to the next ### / ##)."""
    out: dict[str, str] = {}
    parts = re.split(rf"^###\s+({prefix}-\d+):", text, flags=re.MULTILINE)
    # parts = [pre, id1, body1, id2, body2, ...]
    for i in range(1, len(parts), 2):
        sid = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ""
        body = re.split(r"^##\s", body, maxsplit=1, flags=re.MULTILINE)[0]
        out[sid] = body
    return out


# A cited path, deliberately narrow: it must carry a slash AND an extension, so
# `src/routes/x.tsx:12` matches and prose like "partial — client/server split"
# or "the route is built" does not. Widening this to any slash-bearing token was
# tried and flagged three correct prose entries, which is the false positive that
# gets a rule switched off.
CITED_PATH = re.compile(r"\b([\w.-]+(?:/[\w.-]+)+\.[A-Za-z][\w]{0,4}(?::\d+)?)")


def screen_blocks(text: str) -> dict[str, str]:
    """Map SCR-id -> its section body."""
    return entry_blocks(text, "SCR")


def coverage_claim(cov: str, root: Path) -> tuple[bool, list[str]]:
    """A `Coverage:` value read as the claim about code that it is.

    Returns `(names_no_file, cited_paths_that_do_not_exist)`. One owner for two
    layers: `screens.md` and the requirement layer above it ask the same two
    questions of the same field, and an answer that differed between them would
    be a second contract wearing one field's name.
    """
    cited = CITED_PATH.findall(cov)
    missing = [rel for rel in cited if not (root / rel.split(":", 1)[0]).exists()]
    return (not cited, missing)


# --- The observable a requirement is unfinished without --------------------
#
# `Expected result` on a scenario and `Acceptance criteria` on a story are the
# contract's names for the same thing: the thing a reader can watch happen and
# disagree about. Until this block existed, no rule in this file opened a
# scenario or a story body at all -- the contract asked for an observable and
# nothing read for one, so a scenario could reach `implemented` having never
# said what would be true if it worked.
#
# Field spelling is read tolerantly on purpose. `Expected:` and `Acceptance:`
# are the short forms in live use (this pack's own chain writes both), and the
# question these codes ask is whether an observable EXISTS. A rule that failed a
# scenario for spelling its field the short way would be a different rule
# wearing this one's number, and it would be the false positive that gets the
# whole family switched off.
SCENARIO_OBSERVABLE = re.compile(r"\*\*Expected(?:\s+result)?:\*\*[ \t]*(.*)")
STORY_OBSERVABLE = re.compile(r"\*\*Acceptance(?:\s+criteria)?:\*\*[ \t]*(.*)")
FIELD_START = re.compile(r"^\s*(?:[-*]\s+)?\*\*[^*]+:\*\*")
PLACEHOLDER = re.compile(r"^(?:[-—–]+|<[^>]*>|tbd|todo|n/?a|\?+)$", re.IGNORECASE)

# A scenario or story that declares itself unfinished is not a finding: it has
# already said what these codes would say. `retired` and `dropped` are gone, and
# `draft`/`proposed` are the states in which the observable is still being
# written. Every other value -- including an unstated one -- is a claim to be
# finished, and that claim is what gets checked.
SCENARIO_UNFINISHED = ("draft", "retired")
STORY_UNFINISHED = ("proposed", "dropped")


def field_body(body: str, pattern: re.Pattern) -> str | None:
    """A `**Field:**` value: the rest of its line plus the lines beneath it.

    `None` when the field is absent, `""` when it carries nothing. Reading the
    lines beneath is what makes `Acceptance criteria` legible at all -- the
    contract puts its Given/When/Then bullets under the label, not after it.
    """
    m = pattern.search(body)
    if m is None:
        return None
    out = [m.group(1).strip()]
    for line in body[m.end():].splitlines():
        if not line.strip():
            continue
        if FIELD_START.match(line) or line.lstrip().startswith("#"):
            break
        out.append(line.strip())
    return "\n".join(part for part in out if part).strip()


def stated(value: str | None) -> bool:
    """Does this field say anything? A placeholder is not an answer."""
    if value is None:
        return False
    for line in value.splitlines():
        line = line.strip().lstrip("-*").strip()
        if line and not PLACEHOLDER.match(line):
            return True
    return False


def declared_status(body: str) -> str | None:
    m = re.search(r"\*\*Status:\*\*\s*([A-Za-z-]+)", body)
    return m.group(1).lower() if m else None


def check_observables(scenarios: str, foundation: str, root: Path) -> None:
    """A requirement with no observable is unfinished, and says so or is told.

    The reason this is a gate and not advice: an observable added after the
    implementation is read is not a test of the requirement, it is a
    description of the code. By then the only honest thing left to measure is
    whether the code does what the code does. So the observable is required at
    the layer that DEFINES the requirement, where it is still cheap, and the
    citation that connects it to code is required the moment the requirement
    claims to be implemented.
    """
    for sid, body in sorted(entry_blocks(scenarios, "SCN").items()):
        status = declared_status(body)
        if status in SCENARIO_UNFINISHED:
            continue
        if not stated(field_body(body, SCENARIO_OBSERVABLE)):
            err(f"[U060] scenarios.md: {sid} states no observable result — add "
                f"**Expected result:**. A requirement with no observable cannot be "
                f"connected to evidence later without inventing the test after "
                f"reading the implementation")
        cov_m = re.search(r"\*\*Coverage:\*\*\s*(.+)", body)
        cov = cov_m.group(1).strip() if cov_m else ""
        if status == "implemented" and (not cov or cov.lower().startswith("none")):
            warn(f"[U063] scenarios.md: {sid} is 'implemented' and names no code — "
                 f"the status claims an audit passed and nothing says against what")
        if cov and not cov.lower().startswith("none"):
            unfalsifiable, missing = coverage_claim(cov, root)
            if unfalsifiable:
                warn(f"[U064] scenarios.md: {sid} claims Coverage '{cov}' and names no file")
            for rel in missing:
                err(f"[U065] scenarios.md: {sid} cites '{rel}', which does not exist")

    for sid, body in sorted(entry_blocks(foundation, "ST").items()):
        status = declared_status(body)
        if status in STORY_UNFINISHED:
            continue
        # `or ""` so the second question is never asked of None: the linter's
        # promise is that malformed markdown is reported, not raised, and the
        # only way to watch the first branch fail is to disable it.
        criteria = field_body(body, STORY_OBSERVABLE) or ""
        if not stated(criteria):
            err(f"[U061] foundation.md: {sid} states no acceptance criteria — a story "
                f"whose delivery nobody can witness is unfinished, whatever its status")
        elif not re.search(r"\bthen\b", criteria, re.IGNORECASE):
            warn(f"[U062] foundation.md: {sid} acceptance criteria name no outcome "
                 f"(no 'then') — the contract's shape is Given/When/Then, and the "
                 f"'then' is the only half an audit can check")


# --- Delivery proof is not outcome proof -----------------------------------
#
# `Status` is the DELIVERY state: does the code do what the scenario said. An
# audit PASS moves it, and that is the whole of what an audit can know.
# `Product` is the OUTCOME state: did shipping it change anything for a user.
# Only a signal from the world moves it.
#
# Until this block existed the pack had one state and the word `unobserved`
# appeared in it nowhere, so a shipped scenario silently counted as a validated
# one: `implemented` was read as "we were right about this", which is a claim
# nothing in the chain could support. Manifesto M-21 names the state that was
# missing rather than the check -- *some outcome evidence cannot exist until
# after release, so `unobserved` is a legitimate product state; pretending
# delivery proof is outcome proof is not.*
#
# So this field has NO FLOOR AND NO TARGET. Its absence means `unobserved` and
# is never a finding; a scenario may hold `unobserved` for its whole life and
# nothing here will fail. `contradicted` is not a failing gate either -- it is
# the information the field exists to make recordable, and what to do about it is
# a product decision no linter makes. Two things are refused, and both are
# claims rather than states: an outcome claim that names no observation (U067),
# and delivery proof handed in wearing an outcome label (U068). The two artefacts
# an audit produces are a `file:line` and a verdict, and U068 refuses both AS A
# SIGNAL -- which is what makes an audit PASS unable to promote this field in
# code as well as in doctrine.
PRODUCT_STATES = ("unobserved", "observed", "contradicted")
# The two layers that carry a hypothesis: a scenario is the unit that ships and
# a story is the unit that bets. A screen has a delivery state and no bet of its
# own, so it carries no product state, and this tuple is what
# `validate_status_enums_match_contract` reads rather than guessing from
# `STATUS_ENUMS`.
PRODUCT_LAYERS = ("SCN", "ST")
PRODUCT_EVIDENCED = ("observed", "contradicted")
PRODUCT_FIELD = re.compile(r"\*\*Product:\*\*[ \t]*(.*)")
# What an audit hands back, in the two forms the contract gives it. The verdict
# tokens are upper case and nothing else in these documents is, so they are safe
# to key on: `PASS` is a verdict, `passed` is prose, and that sentence is the
# negative fixture. The second is the audit report's own home, which the contract
# fixes at `docs/ux/audits/` — a path into it is the audit speaking, whatever
# prose is wrapped around it, and prose around a citation is how the first form
# would otherwise be smuggled past. Kept as a tuple so deleting one pattern turns
# exactly one fixture red.
AUDIT_EVIDENCE = (
    re.compile(r"\b(?:PASS|FAIL|PARTIAL)\b"),
    re.compile(r"\bdocs/ux/audits/[\w.-]+"),
)

# A code citation as this layer actually writes one, RANGES INCLUDED. `CITED_PATH`
# stops at the first line number on purpose -- it resolves a path, and the range
# is B-004's open work -- so subtracting only what it matches left `-296` behind
# and read it as prose. The plant caught that: `observed — bin/super-ux.js:235-296`
# went clean on the first attempt, and the range form is exactly what this pack's
# own chain writes. Used for the residue test below and nothing else.
CITED_SPAN = re.compile(
    r"`?\b[\w.-]+(?:/[\w.-]+)+\.[A-Za-z][\w]{0,4}(?::\d+(?:-\d+)?)?`?"
)

# Every enum this file matches on, in one table, because the drift it closes was
# exactly a table kept twice. `scenario-format.md` has declared `blocked` for a
# screen since the value was introduced -- with a paragraph of rules of its own
# -- and the matcher here listed four of the five values, so a `blocked` screen
# produced `status = None` and `U021` quietly stopped applying to it. An
# out-of-enum value must be an error, because the alternative is that it means
# nothing and nothing says so. `validate_status_enums_match_contract` compares
# this table against the contract's declaration and fails when either side moves
# alone.
STATUS_ENUMS = {
    "SCN": ("draft", "validated", "implemented", "retired"),
    "ST": ("proposed", "validated", "delivered", "dropped"),
    "SCR": ("designed", "blocked", "built", "drifted", "retired"),
}

# The canonical spelling of a field, and the short form in live use beside it.
# `U060`/`U061` read both on purpose -- their question is whether an observable
# EXISTS -- which left the vocabulary itself ungated: a project could spell a
# required field any way it liked and no code said so. The long spelling is
# canonical because it is what the contract declares and what both shipped
# templates seed, so a fresh install already writes it and the migration cost
# falls on nobody who followed the template. A warning, not an error: the
# observable is present and unambiguous, and failing a project over a synonym is
# the false positive that gets a whole family switched off.
FIELD_ALIASES = (
    ("SCN", "scenarios.md", "**Expected:**", "**Expected result:**"),
    ("ST", "foundation.md", "**Acceptance:**", "**Acceptance criteria:**"),
)


def product_state(body: str) -> tuple[str | None, str]:
    """The `Product:` value read as `(state, signal)`.

    `(None, "")` when the field is absent, and absence is not a finding: it
    means `unobserved`, the honest default. A field that is PRESENT and says
    nothing is a different thing and is reported -- the same distinction
    `field_body` draws between `None` and `""`.
    """
    m = PRODUCT_FIELD.search(body)
    if m is None:
        return (None, "")
    m2 = re.match(r"\s*([A-Za-z][\w-]*)\s*[—–:-]?\s*(.*)$", m.group(1).strip(),
                  re.DOTALL)
    if m2 is None:
        return ("", "")
    return (m2.group(1).lower(), m2.group(2).strip())


def check_product_state(scenarios: str, foundation: str) -> None:
    """The outcome state, which nothing an audit can produce is allowed to move."""
    layers = {"SCN": (scenarios, "scenarios.md"), "ST": (foundation, "foundation.md")}
    for prefix in PRODUCT_LAYERS:
        text, name = layers[prefix]
        for sid, body in sorted(entry_blocks(text, prefix).items()):
            state, signal = product_state(body)
            if state is None:
                continue  # absent == `unobserved`; no floor asks for the field
            if state not in PRODUCT_STATES:
                err(f"[U066] {name}: {sid} declares Product "
                    f"'{state or '(nothing)'}', which is not one of "
                    f"{' | '.join(PRODUCT_STATES)} — an unrecognised value reads "
                    f"as no product state at all, which is how a shipped scenario "
                    f"silently counts as a validated one")
                continue
            if state not in PRODUCT_EVIDENCED:
                continue
            # Three disjoint guards rather than an elif chain: each fixture must
            # be able to fire ONE of them, so that disabling one turns exactly
            # its own case red (standing instruction #5).
            if not stated(signal):
                err(f"[U067] {name}: {sid} claims Product '{state}' and names no "
                    f"signal — an outcome state is a claim about the world, and it "
                    f"has to say which observation supports it")
            # Punctuation is dropped before the residue is judged: `stated()`
            # reads a lone comma as content, so two citations separated by one
            # went clean until the plant said otherwise.
            residue = re.sub(r"[^\w]+", " ", CITED_SPAN.sub(" ", signal))
            if stated(signal) and not stated(residue):
                err(f"[U068] {name}: {sid} offers '{signal}' as an outcome signal, "
                    f"and that is a code citation — delivery proof, which "
                    f"`Status` and `Coverage` already carry. Pretending delivery "
                    f"proof is outcome proof is the one thing this field exists "
                    f"to prevent")
            if stated(signal) and any(p.search(signal) for p in AUDIT_EVIDENCE):
                err(f"[U068] {name}: {sid} offers an audit's own output as an "
                    f"outcome signal — an audit reads code and cannot know whether "
                    f"shipping this changed anything for a user")


def check_field_vocabulary(scenarios: str, foundation: str) -> None:
    """A required field is spelled the way the contract names it."""
    layers = {"SCN": scenarios, "ST": foundation}
    for prefix, name, alias, canonical in FIELD_ALIASES:
        for sid, body in sorted(entry_blocks(layers[prefix], prefix).items()):
            if alias in body:
                warn(f"[U069] {name}: {sid} spells the field '{alias}'; the "
                     f"contract's name is '{canonical}'. The observable is read "
                     f"either way — this is the vocabulary, so a required field "
                     f"cannot be spelled any way a project likes with nothing "
                     f"saying so")


def check_status_enums(scenarios: str, foundation: str, screens: str) -> None:
    """A status outside its layer's enum is refused, not read as no status."""
    for text, prefix, name in ((scenarios, "SCN", "scenarios.md"),
                               (foundation, "ST", "foundation.md"),
                               (screens, "SCR", "screens.md")):
        allowed = STATUS_ENUMS[prefix]
        for sid, body in sorted(entry_blocks(text, prefix).items()):
            status = declared_status(body)
            if status is None or status in allowed:
                continue
            err(f"[U070] {name}: {sid} declares Status '{status}', which is not "
                f"one of {' | '.join(allowed)} — an unrecognised status reads as "
                f"no status, and every rule keyed on one silently stops applying")


WEB_SURFACE_FIELDS = ("Route", "Answers", "Indexable", "Without JS", "Entity")


def web_surfaces_declared(screens: str) -> bool | None:
    """True/False from the project-level declaration; None if unstated."""
    m = re.search(r"\*\*Web surfaces:\*\*\s*(yes|no)\b", screens, re.IGNORECASE)
    if not m:
        return None
    return m.group(1).lower() == "yes"


def check_web_surface(screens: str, flows: str) -> None:
    """A screen a crawler will read is designed as one, or declared not to be.

    The rule this enforces is decided at design time and cannot be recovered
    by an audit: by the time a landing is live, its URL is in other people's
    links and its structure is what an answer engine already quoted. So the
    chain records the five things a later audit checks -- and a project with
    no public page says so once, because a declared absence is countable and
    an unanswered question is not.
    """
    declared = web_surfaces_declared(screens)
    blocks = {
        sid: body for sid, body in screen_blocks(screens).items()
        if "**Web surface:**" in body
    }

    if declared is None:
        warn(
            "[U050] screens.md: no **Web surfaces:** declaration — answer yes or no once "
            "(a public page a search or answer engine reads?). An unanswered "
            "question reads as no, and this one cannot be fixed after launch"
        )
    elif declared is False and blocks:
        for sid in sorted(blocks):
            err(
                f"[U051] screens.md: declares no web surfaces but {sid} carries a "
                f"**Web surface:** block — one of the two is wrong"
            )
    elif declared is True and not blocks:
        warn(
            "[U052] screens.md: declares web surfaces but no screen carries a "
            "**Web surface:** block"
        )

    for sid, body in sorted(blocks.items()):
        for field in WEB_SURFACE_FIELDS:
            if f"**{field}:**" not in body:
                err(f"[U053] screens.md: {sid} web surface block is missing **{field}:**")

    # A declaration of "no" is silence, so it must not be able to hide a flow
    # that plainly starts on the web. This is the one contradiction the
    # declaration cannot absorb.
    if declared is False:
        for fid, body in sorted(entry_blocks(flows, "FLW").items()):
            m = re.search(r"\*\*Entry point:\*\*\s*(.+)", body)
            if not m:
                continue
            entry = m.group(1).strip()
            if re.match(r"https?://|/\S", entry):
                warn(
                    f"[U054] flows.md: {fid} starts at a URL ({entry.split()[0]}) while "
                    f"screens.md declares no web surfaces — one of the two is wrong"
                )


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
            err(f"[U030] vision.md: missing section '## {section}'")
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
                    err(f"[U031] vision.md: approved but '## {section}' is empty — "
                        f"the section that settles arguments cannot be blank")

    root = ux.parent.parent if ux.name == "ux" else ux.parent
    present = [root / n for n in INSTRUCTION_FILES if (root / n).is_file()]
    if not present:
        warn("[U032] vision.md exists but the project has no CLAUDE.md / AGENTS.md / "
             "GEMINI.md — the alignment rule has nowhere to live")
        return
    if not any(VISION_RULE_HEADING in read(p) for p in present):
        warn(f"[U033] vision.md exists but no '{VISION_RULE_HEADING}' block in "
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
                warn(f"[U040] {md.name}: broken link -> {target}")


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

    # Cited paths are project-relative, so they resolve against the tree the
    # ux directory sits in — the same derivation `check_links` already uses.
    project_root = ux.parent.parent if ux.name == "ux" else ux.parent

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
            warn(f"[U003] {name}: {missing} has no index row")
        for ghost in sorted(idx - entries):
            err(f"[U004] {name}: index lists {ghost} but no entry exists")

    # --- Flows reference existing screens ---
    if has_flows and has_screens:
        screen_ids = set(ids(screens, "SCR"))
        used = refs(flows, "SCR")
        for miss in sorted(used - screen_ids):
            err(f"[U010] flows.md references {miss} but screens.md has no such screen")
        for orphan in sorted(screen_ids - used):
            warn(f"[U011] screens.md: {orphan} is used by no flow (orphan)")

        # --- A flow's verdict must be measurable, not inherited -------------
        #
        # The layer order is foundation → flows → screens → scenarios, and audits
        # in practice attach to the two ENDS. Flows sit between and are the only
        # layer with no artefact of their own to measure: a flow is a path across
        # screens, so the cheap thing is to derive its verdict from theirs — and a
        # derived verdict presented as a measured one is what let one project's
        # `flows.md` carry no code verdict for 42 flows across three weeks, its
        # header delegating to an audit that had itself derived them.
        #
        # This does not verdict a flow. It reports the flows for which no verdict
        # can be measured at all, which is the state that was invisible.
        for fid, fbody in sorted(entry_blocks(flows, "FLW").items()):
            mine = [b for b in screen_blocks(screens).values()
                    if re.search(r"\*\*Used by:\*\*[^\n]*\b" + re.escape(fid) + r"\b", b)]
            if not mine:
                continue  # a flow naming no screen is U010's subject, not this one
            cited_anywhere = False
            for b in mine:
                m = re.search(r"\*\*Coverage:\*\*\s*(.+)", b)
                if m and CITED_PATH.search(m.group(1)):
                    cited_anywhere = True
                    break
            if not cited_anywhere:
                warn(f"[U057] flows.md: {fid} has no screen naming an implementing "
                     f"file, so its coverage cannot be measured — only inherited")

    # --- Scenario traces resolve ---
    if ids(scenarios, "SCN"):
        story_ids = set(ids(foundation, "ST"))
        flow_ids = set(ids(flows, "FLW"))
        traced_st = refs(scenarios, "ST")
        traced_flw = refs(scenarios, "FLW")
        if has_stories:
            for miss in sorted(traced_st - story_ids):
                warn(f"[U012] scenarios.md: traces to {miss} which is not in foundation.md")
        if has_flows:
            for miss in sorted(traced_flw - flow_ids):
                warn(f"[U013] scenarios.md: traces to {miss} which is not in flows.md")

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
                    warn(f"[U014] foundation.md: {sid} (must/should) has no scenario tracing to it")

    # --- Screen-level: Figma frames, coverage, drift status ---
    if has_screens:
        fig = figma_enabled(foundation)
        screens_root = project_root
        for sid, body in screen_blocks(screens).items():
            # Read by value, not matched against a copy of the enum: the copy
            # was one value short of the contract for as long as `blocked`
            # existed, and an unmatched status silently became no status.
            # `check_status_enums` owns the enum for all three layers now.
            status = declared_status(body)
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
                        err(f"[U020] screens.md: {sid} state '{state}' has no Figma frame link")
            cov_m = re.search(r"\*\*Coverage:\*\*\s*(.+)", body)
            cov = cov_m.group(1).strip() if cov_m else ""
            if status == "built" and (not cov or cov.lower().startswith("none")):
                warn(f"[U021] screens.md: {sid} is 'built' but has no Coverage")
            # A Coverage value other than `none` is a CLAIM ABOUT CODE, and a claim
            # about code that names no code is unfalsifiable — not by a script and
            # not by a reader, who has nowhere to go to disagree. Measured in a real
            # project: five screens carried `partial` in the index while their
            # entries named no file, and one of them said `none — no route exists`
            # about a route a task had built the day before. Two fields of one
            # record contradicting each other, neither checked against the other.
            if cov and not cov.lower().startswith("none"):
                # The line suffix is part of a citation, not of the path --
                # `coverage_claim` owns that, for this layer and the one above.
                unfalsifiable, missing = coverage_claim(cov, screens_root)
                if unfalsifiable:
                    warn(f"[U055] screens.md: {sid} claims Coverage '{cov}' and names no file")
                for rel in missing:
                    err(f"[U056] screens.md: {sid} cites '{rel}', which does not exist")

    check_observables(scenarios, foundation, project_root)
    check_product_state(scenarios, foundation)
    check_field_vocabulary(scenarios, foundation)
    check_status_enums(scenarios, foundation, screens)
    check_vision(ux, vision)
    check_web_surface(screens, flows)
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
