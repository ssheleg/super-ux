#!/usr/bin/env python3
"""Consistency validator for the super-ux repo (stdlib only).

Checks (spec docs/evidence/specs/2026-07-19-super-ux-design.md, section 9):
  0. Every asset bin/super-ux.js copies is shipped by package.json files[].
  1. Manifests parse, required fields present, versions in sync with CHANGELOG.
  2. Every skill has front-matter: name (matching its directory), description.
  3. Every command has front-matter: description.
  4. Every cursor rule (.mdc) has front-matter: alwaysApply, and description
     unless alwaysApply is true.
  5. Templates shipped by the plugin exist and are non-empty.
  6. Relative markdown links inside the repo resolve.

Exit code 0 with "OK (<n> checks)" when clean; 1 with FAIL: lines otherwise.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

failures: list[str] = []
checks = 0


def check(ok: bool, msg: str) -> bool:
    global checks
    checks += 1
    if not ok:
        failures.append(msg)
    return ok


def read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None



def check_description_canon(rel, path, name: str, desc: str) -> None:
    """The canon rules every skill description must satisfy, and its budgets.

    The budgets were measured against the wrong thing until 2026-08-20: the
    check measured the whole front-matter block -- delimiters, `name`,
    `description` and any other key -- and compared its length to 1024. The
    Agent Skills standard budgets the two FIELDS: `name` at 64 characters and
    `description` at 1024. So a 40-character name pushed a legal 1000-character
    description over an imaginary line, while a `description` of 1024 with a
    short name passed a limit it was exactly at rather than under. No skill here
    was over either real budget, which is why nothing ever said so -- a check
    measuring the wrong quantity looks identical to a check that holds.
    """
    check(
        desc.startswith("Use when"),
        f"{rel}/SKILL.md: description must start with 'Use when' (canon)",
    )
    check(
        bool(re.search(r"[а-яё]", desc, re.I)),
        f"{rel}/SKILL.md: description must carry Russian trigger aliases beside the English ones (canon)",
    )
    check(
        len(name) <= 64,
        f"{rel}/SKILL.md: front-matter `name` is {len(name)} chars, the Agent "
        f"Skills limit is 64",
    )
    check(
        len(desc) <= 1024,
        f"{rel}/SKILL.md: front-matter `description` is {len(desc)} chars, the "
        f"Agent Skills limit is 1024",
    )


def raw_front_matter(path: Path) -> str:
    """The front-matter block verbatim -- the bytes an agent host actually loads.

    `front_matter()` below is a line-by-line reader and that is the point of
    having both: it answers what THIS repository believes, and this answers
    what a YAML parser sees. `B-033` is the gap between them.
    """
    text = read(path) or ""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return "" if end == -1 else text[4:end]


def front_matter(path: Path) -> dict | None:
    """Parse a leading ----delimited front-matter block into a flat dict."""
    text = read(path)
    if text is None or not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    data: dict = {}
    for line in text[3:end].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip().strip("\"").strip("'")
        if value.lower() in ("true", "false"):
            data[key.strip()] = value.lower() == "true"
        else:
            data[key.strip()] = value
    return data


def load_json(rel: str, required: list[str]) -> dict | None:
    path = ROOT / rel
    text = read(path)
    if not check(text is not None, f"{rel}: missing"):
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        check(False, f"{rel}: invalid JSON ({exc})")
        return None
    for field in required:
        check(field in data, f"{rel}: missing required field '{field}'")
    return data


def changelog_version() -> str | None:
    text = read(ROOT / "CHANGELOG.md")
    if not check(text is not None, "CHANGELOG.md: missing"):
        return None
    headings = re.findall(r"^## \[?(\d+\.\d+\.\d+)\]?", text or "", re.MULTILINE)
    check(bool(headings), "CHANGELOG.md: no '## [x.y.z]' release heading")
    # A version documented twice silently truncates the release notes: the
    # release workflow extracts the FIRST matching section and stops there.
    duplicates = sorted({v for v in headings if headings.count(v) > 1})
    check(not duplicates, f"CHANGELOG.md: duplicate release heading(s) {duplicates}")
    return headings[0] if headings else None


def validate_manifests() -> None:
    marketplace = load_json(
        ".claude-plugin/marketplace.json",
        ["name", "owner", "description", "plugins"],
    )
    plugin = load_json(
        "plugins/super-ux/.claude-plugin/plugin.json",
        ["name", "description", "version", "license"],
    )
    package = load_json("package.json", ["name", "version", "bin", "files", "license"])
    if package:
        check(package.get("name") == "super-ux", "package.json: name != super-ux")
        bin_rel = (package.get("bin") or {}).get("super-ux", "")
        bin_path = ROOT / bin_rel
        if check(bin_path.is_file(), f"package.json: bin '{bin_rel}' missing"):
            first_line = (read(bin_path) or "").splitlines()[:1]
            check(
                first_line == ["#!/usr/bin/env node"],
                f"{bin_rel}: missing '#!/usr/bin/env node' shebang",
            )
        for entry in ("bin", "cursor", "templates"):
            check(
                entry in package.get("files", []),
                f"package.json: files[] must include '{entry}'",
            )
    changelog = changelog_version()
    if marketplace:
        entries = marketplace.get("plugins", [])
        check(len(entries) == 1, "marketplace.json: expected exactly one plugin entry")
        if entries:
            entry = entries[0]
            check(entry.get("name") == "super-ux", "marketplace.json: plugin name != super-ux")
            source = entry.get("source", "")
            check(
                (ROOT / source).is_dir(),
                f"marketplace.json: plugin source '{source}' is not a directory",
            )
            if plugin:
                # The ecosystem requires the description in both manifests; the
                # duplication is structural, so it gets a check instead of trust.
                check(
                    entry.get("description") == plugin.get("description"),
                    "marketplace.json plugin description differs from plugin.json's "
                    "(same text in both, or the listing and the installed plugin disagree)",
                )
            if plugin and package and changelog:
                versions = {
                    entry.get("version"),
                    plugin.get("version"),
                    package.get("version"),
                    changelog,
                }
                check(
                    len(versions) == 1,
                    "version mismatch: marketplace=%s plugin=%s package=%s changelog=%s"
                    % (
                        entry.get("version"),
                        plugin.get("version"),
                        package.get("version"),
                        changelog,
                    ),
                )


def validate_npm_payload() -> None:
    """Everything the installer CLI copies must be inside the npm tarball.

    `npm publish` ships only package.json `files[]`. A path the CLI reads that
    is not covered there exists in the repo, passes every local test, and then
    dies with ENOENT for every `npx super-ux` user — so the coverage is checked
    from the CLI source itself, not from a hand-kept list.
    """
    package = load_json("package.json", [])
    if not package:
        return
    patterns = [p.strip("/") for p in package.get("files", [])]

    def covered(rel: str) -> bool:
        return any(rel == pat or rel.startswith(pat + "/") for pat in patterns)

    source = read(ROOT / "bin/super-ux.js") or ""
    reads: set[str] = set()
    for call in re.findall(r"path\.join\(\s*ROOT\s*,([^)]*)\)", source):
        segments: list[str] = []
        for part in call.split(","):
            literal = re.fullmatch(r"\s*'([^']*)'\s*", part)
            if not literal:  # template literal / variable — stop at the last static segment
                break
            segments.append(literal.group(1))
        if segments:
            reads.add("/".join(segments))
    check(bool(reads), "bin/super-ux.js: no ROOT-relative asset paths found (parser out of date?)")
    for rel in sorted(reads):
        if not check((ROOT / rel).exists(), f"bin/super-ux.js reads '{rel}' which does not exist"):
            continue
        check(
            covered(rel),
            f"package.json: files[] does not ship '{rel}', which bin/super-ux.js copies "
            f"(npx super-ux would fail with ENOENT)",
        )


def validate_skills() -> None:
    skills_dir = ROOT / "plugins/super-ux/skills"
    skill_dirs = [
        p for p in sorted(skills_dir.iterdir()) if p.is_dir() and p.name != "references"
    ] if skills_dir.is_dir() else []
    check(bool(skill_dirs), "plugins/super-ux/skills: no skill directories found")
    for skill in skill_dirs:
        rel = skill.relative_to(ROOT)
        fm = front_matter(skill / "SKILL.md")
        if not check(fm is not None, f"{rel}/SKILL.md: missing or has no front-matter"):
            continue
        check(fm.get("name") == skill.name, f"{rel}/SKILL.md: front-matter name != '{skill.name}'")
        check(bool(fm.get("description")), f"{rel}/SKILL.md: missing description")
        check_description_canon(rel, skill / "SKILL.md",
                                fm.get("name") or "", fm.get("description") or "")
    for ref in ("scenario-format.md", "best-practices.md", "ux-design-principles.md", "practice-selection.md", "figma-integration.md", "figma-structure.md", "component-guidelines.md", "system-map.md", "visual-identity.md"):
        check(
            (skills_dir / "references" / ref).is_file(),
            f"plugins/super-ux/skills/references/{ref}: missing",
        )


def validate_commands() -> None:
    commands_dir = ROOT / "plugins/super-ux/commands"
    expected = {
        "ux.md", "ux-init.md", "ux-update.md", "ux-audit.md", "ux-rule.md",
        "ux-foundation.md", "ux-flows.md", "ux-lint.md", "ux-doctor.md",
        "vision.md", "brand.md", "brand-init.md", "brand-update.md",
        "brand-lint.md", "copy.md",
    }
    found = {p.name for p in commands_dir.glob("*.md")} if commands_dir.is_dir() else set()
    check(expected <= found, f"commands: missing {sorted(expected - found)}")
    for name in sorted(found):
        fm = front_matter(commands_dir / name)
        ok = check(fm is not None, f"commands/{name}: missing front-matter")
        if ok:
            check(bool(fm.get("description")), f"commands/{name}: missing description")


def validate_cursor_rules() -> None:
    rules_dir = ROOT / "cursor/rules"
    rules = sorted(rules_dir.glob("*.mdc")) if rules_dir.is_dir() else []
    check(bool(rules), "cursor/rules: no .mdc rules found")
    for rule in rules:
        rel = rule.relative_to(ROOT)
        fm = front_matter(rule)
        if not check(fm is not None, f"{rel}: missing front-matter"):
            continue
        check("alwaysApply" in fm, f"{rel}: missing alwaysApply")
        if not fm.get("alwaysApply"):
            check(bool(fm.get("description")), f"{rel}: agent-requested rule needs a description")


def validate_templates() -> None:
    for name in ("scenarios.md", "audit-report.md", "claude-rule.md", "vision-rule.md", "vision.md", "foundation.md", "flows.md", "screens.md", "README.md"):
        path = ROOT / "templates" / name
        text = read(path)
        check(bool(text and text.strip()), f"templates/{name}: missing or empty")


def _dedent_block(block: str) -> str:
    """Strip the uniform list indent a rule block may carry inside a command."""
    lines = block.splitlines()
    body = [l for l in lines if l.strip()]
    pad = min((len(l) - len(l.lstrip(" ")) for l in body), default=0)
    return "\n".join(l[pad:] if len(l) >= pad else l for l in lines).strip()


HARD_RULES = [
    ("templates/claude-rule.md", "plugins/super-ux/commands/ux-rule.md",
     "## UX scenarios — hard rule (super-ux)"),
    ("templates/vision-rule.md", "plugins/super-ux/skills/vision/SKILL.md",
     "## Vision alignment — hard rule (super-ux)"),
]


def validate_hard_rule_copies() -> None:
    """Every hard rule lives in two places at once — they must be one text.

    A template seeds new projects; a command or skill carries its own embedded
    copy to append to an existing instruction file. Two copies of a rule is
    exactly the drift this plugin exists to prevent, and neither file looks
    wrong alone.

    Found by audit: the vision rule shipped in 0.31.0 with no template and no
    gate, in the same repo whose validator already called that the main enemy.
    So the pair list is data, and adding a rule without adding its row here
    fails on the missing template rather than passing silently.
    """
    for template_path, carrier_path, heading in HARD_RULES:
        template = (read(ROOT / template_path) or "").strip()
        carrier = read(ROOT / carrier_path) or ""
        if not check(bool(template), f"{template_path}: missing or empty — a hard rule needs one source"):
            continue
        blocks = [
            _dedent_block(b) for b in re.findall(r"```markdown\n(.*?)\n\s*```", carrier, re.DOTALL)
        ]
        matching = [b for b in blocks if b.startswith(heading)]
        if not check(
            len(matching) == 1,
            f"{carrier_path}: expected exactly one embedded ```markdown block "
            f"starting '{heading}', found {len(matching)}",
        ):
            continue
        check(
            matching[0] == template,
            f"{carrier_path}'s embedded rule block differs from {template_path} "
            f"(one rule, one text — re-copy the template into the carrier)",
        )


def validate_linter() -> None:
    import py_compile

    path = ROOT / "plugins/super-ux/scripts/ux_lint.py"
    if not check(path.is_file(), "plugins/super-ux/scripts/ux_lint.py: missing"):
        return
    try:
        py_compile.compile(str(path), doraise=True)
        check(True, "ux_lint.py compiles")
    except py_compile.PyCompileError as exc:
        check(False, f"ux_lint.py: does not compile ({exc})")


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")


def validate_links() -> None:
    for path in sorted(ROOT.rglob("*.md")) + sorted(ROOT.rglob("*.mdc")):
        if ".git" in path.parts or "node_modules" in path.parts:
            continue
        text = read(path)
        if text is None:
            continue
        for target in LINK_RE.findall(text):
            if target.startswith(SKIP_PREFIXES):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            check(
                resolved.exists(),
                f"{path.relative_to(ROOT)}: broken relative link -> {target}",
            )


def validate_reference_contents() -> None:
    """Every `## Contents` anchor in a reference resolves to a heading in that file.

    Past 100 lines a reference carries a Contents list, which makes it the one
    part of the shelf that goes stale by someone else's edit: rename a heading
    and the entry above it still looks right. Nothing pointed at it, so nothing
    would have said so — standing instruction #4 on the oldest hand-kept set here.

    The slug rule is GitHub's, and the difference matters: punctuation is dropped
    and every remaining space becomes one hyphen, never collapsed. A heading
    written `## FR-01 — Collect the funnels` therefore anchors as
    `#fr-01--collect-the-funnels`, with TWO hyphens, and a checker that collapses
    them reports 22 false failures across a shelf that is in fact clean. That
    happened while this check was being written, which is why it is written down.
    """
    def slug(heading: str) -> str:
        s = re.sub(r"[^\w \-]", "", heading.strip().lower())
        return s.replace(" ", "-")

    src = ROOT / "plugins/super-ux/skills/references"
    for path in sorted(src.glob("*.md")):
        text = read(path) or ""
        block = re.search(r"^## Contents\n(.*?)(?=^## )", text, re.M | re.S)
        if not block:
            continue
        headings = {slug(h) for h in re.findall(r"^#{2,4} (.+)$", text, re.M)}
        for anchor in re.findall(r"\]\(#([a-z0-9_-]+)\)", block.group(1)):
            check(
                anchor in headings,
                f"{path.relative_to(ROOT)}: Contents links #{anchor}, no heading slugs to it",
            )


def validate_shipped_references() -> None:
    """Every skill must carry its OWN copy of the contracts it links.

    The skills CLI ships only a skill's own directory, so a sibling
    `skills/references/` reaches Claude Code plugins but arrives BROKEN on every
    other agent. Each `skills/<skill>/references/*.md` must therefore exist and be
    byte-identical to the source of truth in `skills/references/`.
    """
    root = ROOT / "plugins/super-ux/skills"
    src = root / "references"
    for skill_dir in sorted(p for p in root.iterdir() if p.is_dir() and p.name != "references"):
        skill_md = skill_dir / "SKILL.md"
        text = read(skill_md) or ""
        check(
            "../references/" not in text,
            f"{skill_dir.name}/SKILL.md links ../references/ — contracts must live INSIDE the skill dir "
            f"(a sibling dir is not shipped by the skills CLI)",
        )
        linked = sorted(set(re.findall(r"\]\(references/([a-z0-9-]+\.md)\)", text)))
        for name in linked:
            local = skill_dir / "references" / name
            if not check(local.is_file(), f"{skill_dir.name}: missing shipped contract references/{name}"):
                continue
            origin = src / name
            if origin.is_file():
                check(
                    local.read_bytes() == origin.read_bytes(),
                    f"{skill_dir.name}/references/{name} has drifted from skills/references/{name} "
                    f"(re-sync: python3 test/sync_references.py)",
                )
        # contracts referenced by the copies themselves must resolve locally too
        refdir = skill_dir / "references"
        if refdir.is_dir():
            for f in sorted(refdir.glob("*.md")):
                for target in re.findall(r"\]\(([^)\s]+)\)", f.read_text(encoding="utf-8")):
                    if target.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    check(
                        (refdir / target.split("#")[0]).exists(),
                        f"{skill_dir.name}/references/{f.name}: dangling link {target}",
                    )


def validate_shipped_templates() -> None:
    """Every template a shipped text seeds from travels WITH what ships.

    SUX-01, family audit 2026-08-29: six shipped texts said "the plugin's
    `templates/`" while the marketplace source is `./plugins/super-ux` and
    `templates/` lived at the repo root — absent from all 13 cached installed
    versions, so every init workflow dead-ended. Each text looked right alone,
    because the path resolved in the one place users never run from: this
    repository's own checkout.

    The repo root stays the source of truth (`HARD_RULES` and the installer
    CLI read it); `sync_references.py` mirrors the full tree into
    `plugins/super-ux/templates/` and the named seeds into each skill that
    names one, and this check refuses drift and strays the same way
    `validate_shipped_references` does for contracts.
    """
    src = ROOT / "templates"
    dst = ROOT / "plugins/super-ux/templates"
    src_files = {p.relative_to(src).as_posix() for p in src.rglob("*") if p.is_file()}
    check(bool(src_files), "templates/: no files to ship")
    if not check(dst.is_dir(), "plugins/super-ux/templates: missing — the plugin ships no "
                               "templates and every seeding text dead-ends "
                               "(re-sync: python3 test/sync_references.py)"):
        return
    dst_files = {p.relative_to(dst).as_posix() for p in dst.rglob("*") if p.is_file()}
    for rel in sorted(src_files):
        if not check(rel in dst_files,
                     f"plugins/super-ux/templates/{rel}: missing from the shipped plugin "
                     f"(re-sync: python3 test/sync_references.py)"):
            continue
        check((src / rel).read_bytes() == (dst / rel).read_bytes(),
              f"plugins/super-ux/templates/{rel} has drifted from templates/{rel} "
              f"(re-sync: python3 test/sync_references.py)")
    for rel in sorted(dst_files - src_files):
        check(False, f"plugins/super-ux/templates/{rel}: no source at templates/{rel} — "
                     f"a copy with no source is a fork "
                     f"(re-sync: python3 test/sync_references.py)")
    for skill_dir in sorted(p for p in (ROOT / "plugins/super-ux/skills").iterdir() if p.is_dir()):
        tdir = skill_dir / "templates"
        if not tdir.is_dir():
            continue
        for f in sorted(p for p in tdir.rglob("*") if p.is_file()):
            rel = f.relative_to(tdir).as_posix()
            origin = src / rel
            if not check(origin.is_file(),
                         f"{skill_dir.name}/templates/{rel}: no source at templates/{rel} — "
                         f"a copy with no source is a fork "
                         f"(re-sync: python3 test/sync_references.py)"):
                continue
            check(f.read_bytes() == origin.read_bytes(),
                  f"{skill_dir.name}/templates/{rel} has drifted from templates/{rel} "
                  f"(re-sync: python3 test/sync_references.py)")


SHIPPED_ASSET_RE = re.compile(r"`((?:templates|scripts)(?:/[A-Za-z0-9._-]+)*/?)`")


def validate_shipped_paths() -> None:
    """Every plugin-asset path a shipped text names resolves inside what ships.

    The CLASS behind SUX-01, not just its instance. A skill installed by the
    skills CLI is its own directory and nothing else — the rule
    `validate_shipped_references` already enforces for contracts — and the
    Claude Code plugin is `plugins/super-ux/` and nothing above it. So a
    backticked `templates/…` or `scripts/…` token in a command must resolve
    under the plugin root, and one in a skill file must resolve under that
    skill's own directory. A token that resolves only at this repository's
    root is exactly how six texts pointed at a dead path in every installed
    channel for months while every gate stayed green.
    """
    plugin = ROOT / "plugins/super-ux"
    for path in sorted(plugin.rglob("*.md")):
        rel = path.relative_to(ROOT)
        parts = path.relative_to(plugin).parts
        if parts[0] == "skills":
            if len(parts) < 3 or parts[1] == "references":
                # The master contracts are gated as the per-skill copies they
                # become — every copy below skills/<skill>/ is scanned here.
                continue
            base = plugin / "skills" / parts[1]
            where = f"skill '{parts[1]}' ships its own directory and nothing else"
        else:
            base = plugin
            where = "the plugin ships plugins/super-ux/ and nothing above it"
        text = read(path) or ""
        for token in SHIPPED_ASSET_RE.findall(text):
            check((base / token.rstrip("/")).exists(),
                  f"{rel}: names `{token}`, which does not resolve inside what ships — "
                  f"{where} (ship it: python3 test/sync_references.py, or repoint the text)")


NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}

# Prose lives in these; the per-skill `references/` copies are byte-identical
# to their source and would multiply every finding by seven. `CHANGELOG.md` and
# `docs/evidence/` are history: a number that was right at v0.30.0 must stay
# written as it was.
def _prose_files() -> list[Path]:
    out = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "SECURITY.md"]
    for pattern in ("templates/**/*.md", "cursor/rules/*.mdc",
                    "plugins/super-ux/commands/*.md",
                    "plugins/super-ux/skills/*/SKILL.md",
                    "plugins/super-ux/skills/references/*.md"):
        out.extend(sorted(ROOT.glob(pattern)))
    return [p for p in out if p.is_file()]


def _skill_names() -> list[str]:
    d = ROOT / "plugins/super-ux/skills"
    return sorted(p.name for p in d.iterdir() if p.is_dir() and p.name != "references") if d.is_dir() else []


def validate_stated_numbers() -> None:
    """Every count written in prose, against the artifact it counts.

    Found by audit, three at once: the README advertised 181 practices against
    a catalog of 206, "31 deterministic checks" against a linter emitting 33,
    and four different PRN ranges (..10, ..16, ..21, ..24) across six files.
    Every one of them passed 3427 checks, because the suite verified shape and
    never once verified a number. A figure nobody can recompute is a claim.
    """
    catalog = read(ROOT / "plugins/super-ux/skills/references/best-practices.md") or ""
    bp_count = len(re.findall(r"^#### BP-\d+:", catalog, re.M))
    lint = read(ROOT / "plugins/super-ux/scripts/brand_lint.py") or ""
    brand_codes = len(set(re.findall(r'"(B\d{3})"', lint)))
    principles = read(ROOT / "plugins/super-ux/skills/references/ux-design-principles.md") or ""
    prn_nums = [int(n) for n in re.findall(r"PRN-(\d+)", principles)]
    prn_max = max(prn_nums) if prn_nums else 0
    funnel = read(ROOT / "plugins/super-ux/skills/references/funnel-research.md") or ""
    fr_nums = [int(n) for n in re.findall(r"FR-(\d+)", funnel)]
    fr_max = max(fr_nums) if fr_nums else 0
    skills = _skill_names()

    check(bp_count > 0, "best-practices.md: no `#### BP-NNN:` entries to count")
    check(brand_codes > 0, "brand_lint.py: no check codes to count")
    check(prn_max > 0, "ux-design-principles.md: no PRN ids to count")
    check(fr_max > 0, "funnel-research.md: no FR ids to count")

    for path in _prose_files():
        rel = path.relative_to(ROOT)
        text = read(path) or ""

        for stated in re.findall(r"catalog of (\d+) proven practices", text):
            check(int(stated) == bp_count,
                  f"{rel}: says {stated} proven practices, best-practices.md holds {bp_count}")
        for stated in re.findall(r"(\d+) deterministic checks", text):
            check(int(stated) == brand_codes,
                  f"{rel}: says {stated} deterministic checks, brand_lint.py emits {brand_codes}")
        # `PRN-01..NN` claims to span the catalog. A genuine sub-range must be
        # written another way (`PRN-01 – PRN-10`), so this form is unambiguous.
        for stated in re.findall(r"PRN-01\.\.(?:PRN-)?(\d+)", text):
            check(int(stated) == prn_max,
                  f"{rel}: claims the heuristic catalog spans PRN-01..{stated}, "
                  f"ux-design-principles.md ends at PRN-{prn_max}")
        # Same form, same reason: `FR-01..NN` claims to span the funnel-research
        # method. A genuine sub-range is written `FR-03 – FR-05`, so this one is
        # unambiguous and a step added without updating the carriers goes red.
        for stated in re.findall(r"FR-01\.\.(?:FR-)?(\d+)", text):
            check(int(stated) == fr_max,
                  f"{rel}: claims the funnel-research method spans FR-01..{stated}, "
                  f"funnel-research.md ends at FR-{fr_max}")
        for word in re.findall(r"\b(one|two|three|four|five|six|seven|eight|nine|ten) skills\b", text):
            check(NUMBER_WORDS[word] == len(skills),
                  f"{rel}: says '{word} skills', the plugin ships {len(skills)} "
                  f"({', '.join(skills)})")

    rules = sorted((ROOT / "cursor/rules").glob("*.mdc"))
    requested = [r for r in rules if not (front_matter(r) or {}).get("alwaysApply")]
    readme = read(ROOT / "README.md") or ""
    for word in re.findall(r"\b(one|two|three|four|five|six|seven|eight|nine|ten) agent-requested rules\b", readme):
        check(NUMBER_WORDS[word] == len(requested),
              f"README.md: says '{word} agent-requested rules', cursor/rules has {len(requested)}")


def validate_skill_parity() -> None:
    """A skill exists in seven places or it does not exist.

    Found by audit: `brand-voice` and `copywriting` shipped in 0.30.0 and
    reached neither manifest description nor the `/ux` router; `vision` shipped
    in 0.31.0 and reached neither the system map nor a Cursor rule. Each was
    invisible in a different place, and no single file looked wrong. Absence
    has one side, so it has to be asked for by name.
    """
    skills = _skill_names()
    check(bool(skills), "no skill directories to check parity against")

    router = read(ROOT / "plugins/super-ux/commands/ux.md") or ""
    smap = read(ROOT / "plugins/super-ux/skills/references/system-map.md") or ""
    smap_skills = smap.split("## Skills & the one entry point", 1)[-1].split("\n## ", 1)[0]
    plugin = load_json("plugins/super-ux/.claude-plugin/plugin.json", []) or {}
    market = load_json(".claude-plugin/marketplace.json", []) or {}
    market_desc = (market.get("plugins") or [{}])[0].get("description", "")
    rule_names = {p.stem for p in (ROOT / "cursor/rules").glob("*.mdc")}

    for name in skills:
        check(name in router,
              f"{name} is not named in commands/ux.md — /ux calls itself the only "
              f"command a user needs, so a skill it cannot route to is a skill nobody runs")
        check(name in smap_skills,
              f"{name} is missing from system-map.md's 'Skills & the one entry point' section")
        check(name in plugin.get("description", ""),
              f"{name} is missing from plugins/super-ux/.claude-plugin/plugin.json description")
        check(name in market_desc,
              f"{name} is missing from .claude-plugin/marketplace.json description")
        check(name in rule_names,
              f"cursor/rules/{name}.mdc is missing — the Cursor channel would ship "
              f"{len(rule_names) - 1} of {len(skills)} domains")

    for cmd in ("/ux-doctor", "/vision", "/brand-lint", "/copy"):
        check(cmd in smap, f"system-map.md does not list the {cmd} command")

    # B-014: existence was checked and reachability was not. `cursor/rules/
    # <name>.mdc` counted as one of the five places above, which is why
    # `vision.mdc` existed -- and nothing asked whether the always-on umbrella
    # rule names it. Measured 2026-08-20: `cursor/rules/super-ux.mdc:39` named
    # four workflows against eight `.mdc` files shipped, and `grep -c` returned
    # 0 for `vision`, `brand-voice` and `copywriting`. A Cursor user got three
    # rule files nothing routed to and a chain missing its top layer, for three
    # releases, on the one channel where a rule that is never named is a rule
    # that is never loaded.
    umbrella_rel = "cursor/rules/super-ux.mdc"
    umbrella = read(ROOT / umbrella_rel) or ""
    if check(bool(umbrella), f"{umbrella_rel}: missing — the always-on rule the "
                             f"Cursor channel routes from"):
        check(bool((front_matter(ROOT / umbrella_rel) or {}).get("alwaysApply")),
              f"{umbrella_rel}: not alwaysApply — an umbrella nobody loads routes "
              f"to nothing")
        for name in skills:
            check(name in umbrella,
                  f"{umbrella_rel} does not name `{name}` — the Cursor channel "
                  f"ships {name}.mdc and the always-on rule never routes to it, "
                  f"so the file is present and unreachable")
        for rule in sorted(rule_names - {"super-ux"} - set(skills)):
            check(rule in umbrella,
                  f"{umbrella_rel} does not name `{rule}`, a rule this repo ships "
                  f"— every .mdc is reachable from the umbrella or from nothing")


SEEDED_SCRIPTS = [
    ("docs/ux/lint.py", "ux_lint.py"),
    ("docs/ux/doctor.py", "ux_doctor.py"),
    ("docs/brand/lint.py", "brand_lint.py"),
]


def validate_seeded_scripts() -> None:
    """Every script an instruction tells a reader to run is put there by a command.

    Found by audit: `/ux-rule` installed a rule saying "run
    `python3 docs/brand/lint.py`" and seeded only `docs/ux/lint.py`; `/ux` told
    the reader to run `docs/ux/doctor.py` after a repair step that never copied
    it; `/ux-doctor` claimed `/ux-rule` "seeds both scripts". Three files, one
    missing seam, and nothing that reads a single file can see it.
    """
    commands = sorted((ROOT / "plugins/super-ux/commands").glob("*.md"))
    texts = {p.name: (read(p) or "") for p in commands}
    for dest, source in SEEDED_SCRIPTS:
        seeders = [n for n, txt in texts.items() if source in txt and dest in txt]
        # A seeded copy that has fallen behind its source is worse than a
        # missing one: it runs, it reports, and it reports the previous
        # release's rules. `docs/brand/lint.py` sat 227 lines behind
        # `brand_lint.py` through this repo's own dogfood, so the pack was
        # linted twice and neither pass used the checks that had just been
        # added. Byte equality, because these are copies and not renderings.
        src_path, dst_path = ROOT / "plugins/super-ux/scripts" / source, ROOT / dest
        src_text, dst_text = read(src_path), read(dst_path)
        if check(src_text is not None, f"{source}: source script missing") and \
           check(dst_text is not None, f"{dest}: seeded copy missing"):
            check(
                src_text == dst_text,
                f"{dest} has drifted from {source} — re-seed it (`cp` in the "
                f"same change), because a stale copy runs the previous "
                f"release's rules and says nothing about it",
            )
        check(
            bool(seeders),
            f"no command copies {source} to {dest}, yet something instructs the "
            f"reader to run it — a rule pointing at a file nobody installed",
        )


def validate_catalog() -> None:
    """The catalog's shape is an invariant nothing enforced until now.

    All 146 entries at the time of writing carried the same five fields, ids ran
    unbroken, and every tag came from the taxonomy -- by hand, every time. A
    practice that quietly loses `Source` reads as authoritative while resting on
    nothing, and one missing from `practice-selection.md` is unreachable: the
    catalog holds it and no skill ever routes to it. Both fail silently, which is
    exactly the kind of thing a validator is for.
    """
    src = ROOT / "plugins/super-ux/skills/references"
    catalog = read(src / "best-practices.md")
    routing = read(src / "practice-selection.md")
    if not check(catalog is not None, "best-practices.md is missing"):
        return
    if not check(routing is not None, "practice-selection.md is missing"):
        return

    taxonomy_block = catalog.split("## Tag taxonomy", 1)[-1].split("## Practices", 1)[0]
    taxonomy = set(re.findall(r"`([a-z0-9-]+)`", taxonomy_block))
    check(bool(taxonomy), "best-practices.md: tag taxonomy is empty or unparseable")

    entries = re.findall(r"^#### (BP-\d+):.*?(?=^#### BP-|\Z)", catalog, re.M | re.S)
    bodies = re.split(r"^#### BP-\d+:", catalog, flags=re.M)[1:]
    if not check(bool(entries), "best-practices.md: no BP entries found"):
        return

    for entry_id, body in zip(entries, bodies):
        body = body.split("\n#### ", 1)[0]
        for field in ("**Do:**", "**Why:**", "**Apply when:**", "**Tags:**", "**Source:**"):
            check(field in body, f"best-practices.md {entry_id}: missing {field.strip('*:')} field")
        tags_line = re.search(r"^- \*\*Tags:\*\*(.+)$", body, re.M)
        if tags_line:
            for tag in (t.strip() for t in tags_line.group(1).split(",")):
                if tag:
                    check(
                        tag in taxonomy,
                        f"best-practices.md {entry_id}: tag `{tag}` is not in the taxonomy "
                        f"(add it there deliberately, or use an existing one)",
                    )

    numbers = [int(e.split("-")[1]) for e in entries]
    check(len(numbers) == len(set(numbers)), "best-practices.md: duplicate BP ids")
    expected = list(range(1, len(numbers) + 1))
    check(
        sorted(numbers) == expected,
        f"best-practices.md: ids must run BP-001..BP-{len(numbers):03d} without gaps "
        f"(found {len(numbers)} entries, max BP-{max(numbers):03d})",
    )

    # The header paragraph is a table of contents, not routing: it spans the whole
    # catalog by construction, so counting it would make every entry look reachable.
    # Only the selection tables below the first heading actually route anything.
    tables = routing.split("\n## ", 1)[-1]
    routed: set[int] = set()
    for lo, hi in re.findall(r"BP-(\d+)\.\.(\d+)", tables):
        routed.update(range(int(lo), int(hi) + 1))
    routed.update(int(n) for n in re.findall(r"BP-(\d+)", tables))

    span = re.search(r"BP-(\d+)\.\.(\d+)", routing)
    if check(span is not None, "practice-selection.md: no BP-A..B catalog span in the header"):
        check(
            int(span.group(2)) == max(numbers),
            f"practice-selection.md: header span ends at BP-{int(span.group(2)):03d} but the "
            f"catalog ends at BP-{max(numbers):03d} (re-read the header when adding entries)",
        )

    # The index is generated; a stale one is worse than none, because it is
    # trusted the same way and silently omits whatever was added last.
    index = read(src / "best-practices-index.md")
    if check(index is not None, "best-practices-index.md is missing (run bp_index.py)"):
        indexed = {int(n) for n in re.findall(r"BP-(\d+)", index)}
        missing = sorted(set(numbers) - indexed)
        check(
            not missing,
            "best-practices-index.md is stale, missing "
            + ", ".join(f"BP-{n:03d}" for n in missing[:6])
            + " -- regenerate: python3 plugins/super-ux/scripts/bp_index.py",
        )

    unreachable = sorted(set(numbers) - routed)
    check(
        not unreachable,
        "practice-selection.md: "
        + ", ".join(f"BP-{n:03d}" for n in unreachable[:8])
        + (" and more" if len(unreachable) > 8 else "")
        + " are in the catalog but not routed -- no skill can reach them",
    )

    # `B-021` asked for the arrow above and it was already here, closed and
    # never struck off the board. The arrow that was genuinely missing runs the
    # other way: a row routing at a practice the catalog no longer defines
    # sends a profile at nothing, and it survives every check in this function
    # because each of them starts from the catalog. Found by planting `BP-999`
    # into a routing row and watching nothing say so.
    ghosts = sorted(routed - set(numbers))
    check(
        not ghosts,
        "practice-selection.md routes to "
        + ", ".join(f"BP-{n:03d}" for n in ghosts[:8])
        + (" and more" if len(ghosts) > 8 else "")
        + ", which the catalog does not define -- the row sends a profile at "
          "nothing, and every other check here starts from the catalog so none "
          "of them can see it",
    )


def validate_brand_contract() -> None:
    """`docs/brand/` has one contract, and it lives in exactly one file.

    Every brand skill, template and the linter key off these names. A name
    defined twice is drift with a delay fuse, so the contract is the only
    place any of them is written down -- this check is what keeps that true.
    """
    src = ROOT / "plugins/super-ux/skills/references"
    text = read(src / "brand-contract.md")
    if not check(text is not None, "brand-contract.md is missing"):
        return
    for token in (
        "Contract: brand-contract v1", "voice.md", "terminology.md",
        "facts.md", "channels.md", "strings.md", "locales/<code>.md",
        "Locale parity threshold", "Derived-from", "Last calibrated",
        "Confidence", "Register", "Distance", "Humor", "Density",
        "Hero", "Enemy", "Product role", "Promise",
        "agreed", "proposed", "drifted", "orphan",
        "Length coefficient", "Sources:",
    ):
        check(token in text, f"brand-contract.md: missing `{token}`")


PACKS = (
    "operator-brief", "calm-expert", "peer-builder",
    "editorial-premium", "plain-service", "playful-consumer",
)
PACK_FIELDS = (
    "Use for", "Not for", "Axes", "Narrative template", "Lexicon",
    "Pack bans", "Register deltas", "Ready lines", "Failure mode",
)


def validate_voice_packs() -> None:
    """Six packs, and every one of them admits how it degrades.

    `Failure mode` is the field that makes an archetype library safe to ship:
    without it a pack is an instruction to overshoot, and the audit has no
    way to call the overshoot anything but taste.
    """
    src = ROOT / "plugins/super-ux/skills/references"
    text = read(src / "voice-packs.md")
    if not check(text is not None, "voice-packs.md is missing"):
        return
    for section in text.split("\n## ")[1:]:
        name = section.split("\n", 1)[0].strip()
        if name not in PACKS:
            continue
        for field in PACK_FIELDS:
            check(field in section, f"voice-packs.md: {name} missing `{field}`")
    for pack in PACKS:
        check(f"\n## {pack}\n" in text, f"voice-packs.md: pack `{pack}` missing")


BRAND_TEMPLATES = (
    "README.md", "voice.md", "terminology.md", "facts.md",
    "channels.md", "strings.md", "locale.md",
)


def validate_brand_templates() -> None:
    """Every seeded brand file announces which contract it was written to.

    Without the marker on the artifact itself, a base three contract versions
    old is indistinguishable from a current one -- it is internally
    consistent either way, which is exactly why the linter cannot see it and
    the doctor can.
    """
    tdir = ROOT / "templates/brand"
    for name in BRAND_TEMPLATES:
        text = read(tdir / name)
        if not check(text is not None, f"templates/brand/{name} is missing"):
            continue
        lines = text.splitlines()
        first = lines[0].strip() if lines else ""
        check(
            first == "Contract: brand-contract v1",
            f"templates/brand/{name}: first line must be the contract marker",
        )
    readme = read(tdir / "README.md") or ""
    check(
        "Sources:" in readme,
        "templates/brand/README.md: no `Sources:` block -- the linter would "
        "have nothing to scan (B006)",
    )


BRAND_FIRST_BP = 182


def validate_brand_practices() -> None:
    """The brand cluster carries a sixth field, and nothing reuses `voice`.

    `Checked:` starts at BP-182 deliberately: backfilling it onto BP-001..181
    would put a date on a verification nobody performed, which is the exact
    failure the field exists to prevent.
    """
    src = ROOT / "plugins/super-ux/skills/references"
    text = read(src / "best-practices.md") or ""
    ids = sorted(int(n) for n in re.findall(r"^#### BP-(\d{3}):", text, re.M))
    if not check(bool(ids), "best-practices.md: no practices parsed"):
        return
    check(
        max(ids) >= 205,
        f"brand practices: catalog ends at BP-{max(ids):03d}, need BP-205 "
        f"or higher (six clusters of at least four)",
    )
    for num in range(BRAND_FIRST_BP, max(ids) + 1):
        body = re.search(
            rf"^#### BP-{num:03d}:.*?(?=^#### |\Z)", text, re.M | re.S
        )
        if not check(body is not None, f"BP-{num:03d} is missing"):
            continue
        for field in ("- **Do:**", "- **Why:**", "- **Apply when:**",
                      "- **Tags:**", "- **Source:**", "- **Checked:**"):
            check(field in body.group(0),
                  f"BP-{num:03d}: missing {field}")
    # `.` spans newlines under re.S, so the tag group must exclude them --
    # otherwise every entry's "tags" run to the end of the file and the first
    # practice appears to carry every tag in the catalog.
    # Scoped to the brand range on purpose: BP-060..065 are voice-interface
    # practices and `voice` is their correct Domain tag. The collision is only
    # a problem for new entries, where `voice` would mean the brand's.
    for num, tags in re.findall(
        r"^#### BP-(\d{3}):.*?- \*\*Tags:\*\* ([^\n]+)", text, re.M | re.S
    ):
        if int(num) < BRAND_FIRST_BP:
            continue
        check(
            not re.search(r"(?:^|[ ,`])voice(?:[ ,`]|$)", tags),
            f"BP-{num}: uses the tag `voice`, which in this catalog means a "
            f"voice interface -- the brand tag is `brand-voice`",
        )


def validate_brand_field_ownership() -> None:
    """Every field the linter reads is one the contract still defines.

    `validate_brand_contract` catches a field disappearing from the contract.
    It cannot catch the other half: `header_field(voice, "X")` on a field the
    contract renamed returns None, the check that depended on it stops firing,
    and nothing anywhere goes red. A check that silently stops checking is
    worse than one that was never written, because the green is still printed.

    This is the "what breaks if this moves" question, made mechanical for the
    one place it actually bites.
    """
    src = ROOT / "plugins/super-ux/skills/references"
    contract = read(src / "brand-contract.md") or ""
    linter = read(ROOT / "plugins/super-ux/scripts/brand_lint.py") or ""
    fields = sorted(set(re.findall(r'header_field\([^,]+,\s*"([^"]+)"\)', linter)))
    check(bool(fields), "brand_lint.py: no header_field reads found to verify")
    for field in fields:
        check(
            field in contract,
            f"brand_lint.py reads the field `{field}`, which brand-contract.md "
            f"no longer defines -- the read returns nothing and its check stops "
            f"firing silently",
        )


def validate_brand_lint_coverage() -> None:
    """Every code the linter can emit has a fixture, and the contract names it.

    Found by audit, not by the suite: four codes shipped with no fixture while
    the count looked right, and eighteen were documented only in the linter's
    own source -- in a repo whose canon is one owner per fact. A green suite
    cannot report a check it was never asked to run, so this asks.
    """
    lint = read(ROOT / "plugins/super-ux/scripts/brand_lint.py") or ""
    tests = read(ROOT / "test/brand_lint_test.py") or ""
    contract = read(
        ROOT / "plugins/super-ux/skills/references/brand-contract.md"
    ) or ""
    emitted = sorted(set(re.findall(r'"(B\d{3})"', lint)))
    check(bool(emitted), "brand_lint.py: no check codes found")
    for code in emitted:
        check(
            f'"{code}"' in tests,
            f"{code} is emitted by brand_lint.py with no fixture in "
            f"brand_lint_test.py -- a check nobody watched fail is not evidence",
        )
        check(
            code in contract,
            f"{code} is emitted by brand_lint.py but brand-contract.md does "
            f"not name it -- the code's meaning would live only in the source",
        )


BOARD = "docs/evidence/backlog.md"
LEDGER = "docs/evidence/verification.md"


def validate_board_ids() -> None:
    """A register whose ids are not unique cannot be cited.

    B-016, found by stage-0 harvest and unfixable in passing: `B-011`, `B-012`
    and `B-013` each appeared in BOTH the open table and the Closed table with
    different content, so "closed in B-013" resolved to two rows. Three
    collisions accumulated because nothing read the board at all -- it is the
    one document in this repository that records what the repository owes, and
    it had no gate of any kind.

    Ids are read from the first cell of every row in either table, which is the
    only place the board puts one, and every citation of a `B-`/`SU-` id in the
    ledger must resolve to exactly one of them. The ledger citation is the half
    that caught `R-22` filing the `AT-` gap as `B-016` where the board files it
    as `B-017` -- a one-word error inside the register whose id reuse was itself
    the open row above it.
    """
    board = read(ROOT / BOARD) or ""
    if not check(bool(board), f"{BOARD}: missing or empty"):
        return
    ids = re.findall(r"^\|\s*((?:B|SU)-\d+)\s*\|", board, re.M)
    check(bool(ids), f"{BOARD}: no `| B-NNN |` or `| SU-NN |` rows to check")
    for rid in sorted({i for i in ids if ids.count(i) > 1}):
        check(False, f"{BOARD}: {rid} appears {ids.count(rid)} times -- a register "
                     f"whose ids are not unique cannot be cited, because "
                     f"'closed in {rid}' resolves to more than one row")
    known = set(ids)
    ledger = read(ROOT / LEDGER) or ""
    for cited in sorted(set(re.findall(r"\b(B-\d{3})\b", ledger))):
        check(cited in known, f"{LEDGER} cites {cited}, which is not a row on the "
                              f"board -- a ledger row pointing at no task is a "
                              f"claim with nothing behind it")


# Every live copy of a hard rule, and the anchors it is allowed not to carry.
#
# B-015 and B-018: the `UX scenarios` rule has four payload homes and
# `HARD_RULES` pairs two of them byte for byte. Measured 2026-08-20:
# `templates/claude-rule.md` 320 words / 2102 chars, `CLAUDE.md:68` 349 / 2284,
# `cursor/rules/super-ux.mdc:6` 348 / 2204 -- and the `.mdc` named four
# workflows out of the seven skills the pack ships, three releases behind.
#
# Byte equality is the wrong test for the copies that are NOT the carrier: this
# repository's own `CLAUDE.md` diverges by choice and its wording is the better
# one ("approved **for the change at hand**"). So the test is anchor parity --
# every path, command and skill name the template names must be named by every
# live copy -- and an exemption is DATA with a reason beside it, because the
# alternative to naming one is a check nobody can pass and everybody deletes.
HARD_RULE_HOMES = (
    ("UX scenarios — hard rule (super-ux)", "CLAUDE.md", ()),
    ("UX scenarios — hard rule (super-ux)", "cursor/rules/super-ux.mdc",
     # Cursor has no slash commands: this channel routes by rule file, and the
     # rules it must name are asserted by `validate_skill_parity` instead.
     ("/ux",)),
    ("Brand voice — hard rule (super-ux)", "CLAUDE.md", ()),
)


def _rule_section(text: str, heading: str) -> str | None:
    """One hard-rule section, from its heading to the next same-or-higher one."""
    match = re.search(rf"^(#{{1,3}})\s*{re.escape(heading)}\s*$", text, re.M)
    if not match:
        return None
    rest = text[match.end():]
    nxt = re.search(r"^#{1,2} ", rest, re.M)
    return match.group(0) + (rest[:nxt.start()] if nxt else rest)


def validate_hard_rule_anchors() -> None:
    """Every live copy of a hard rule names everything its source names."""
    template = read(ROOT / "templates/claude-rule.md") or ""
    if not check(bool(template), "templates/claude-rule.md: missing"):
        return
    for heading, rel, exempt in HARD_RULE_HOMES:
        source = _rule_section(template, heading)
        if not check(source is not None,
                     f"templates/claude-rule.md has no '{heading}' section -- the "
                     f"anchors every copy is measured against come from it"):
            continue
        # Backticked tokens are the paths, commands and skill names the rule
        # names; a bolded token with no space is a companion skill. Derived, not
        # restated: adding an anchor to the template makes every copy answer for
        # it, which is the only way a copy can fall behind and be noticed.
        anchors = set(re.findall(r"`([^`\n]+)`", source))
        anchors |= {t for t in re.findall(r"\*\*([^*\n]+)\*\*", source) if " " not in t}
        anchors -= set(exempt)
        check(bool(anchors), f"'{heading}': the template section names no anchor")
        copy = _rule_section(read(ROOT / rel) or "", heading)
        if not check(copy is not None,
                     f"{rel}: no '{heading}' section -- a live copy of a hard rule "
                     f"that has lost its heading is a copy nothing can compare"):
            continue
        for anchor in sorted(anchors):
            check(anchor in copy,
                  f"{rel}: its '{heading}' copy does not name `{anchor}`, which "
                  f"templates/claude-rule.md does -- a copy that dropped a "
                  f"requirement reads as a rule with one fewer requirement")


FACTS = "docs/brand/facts.md"

# Set on the nested run below. It skips the RECOMPUTATION and not the `check()`
# calls, so the child performs exactly as many checks as the parent and the
# count it prints is the count the parent would print. That is the whole trick,
# and it is what makes the one self-referential row honest instead of clever:
# the row's Source is `python3 test/validate.py`, so the check runs that command.
FACTS_NESTED = "SUPER_UX_FACTS_RECOMPUTE_CHILD"

# A Source that cannot be recomputed on this machine says so in these words.
# `agents reachable via the skills CLI` is an external registry: there is no
# command here that returns it, and the row that admits it is worth more than a
# row that is quietly skipped by a loop claiming to check everything.
NOT_HERE = "not recomputable here:"


def _disclose(msg: str) -> None:
    """A check that could not run, said out loud rather than counted as a pass."""
    print(f"  unlooked: {msg}")


def validate_facts_recompute() -> None:
    """Every row in `facts.md` is what its own `Source` command returns.

    `facts.md` has said "Every row below names a command that recomputes it"
    since the table existed, and until 2026-08-20 nothing ran one. The file even
    argued the point in its own prose -- "naming the command is not the same as
    running it, and only running it produces a fact" -- three paragraphs above
    seven hand-maintained integers. Recomputed by hand on 2026-08-20: six agreed
    and `repo validator checks` read 3500 against a measured 3539, so the table
    that exists to be the only source of any public figure was itself carrying a
    stale one. The row is `Public: no`, which is why no `B030` ever pointed at
    it: the wrong number was unquotable and therefore uncheckable.

    Two rows are special and both are handled rather than skipped. The validator
    row's Source is this very script, run as a child with `FACTS_NESTED` set. The
    agents row names an external registry and is disclosed, not passed.
    """
    nested = os.environ.get(FACTS_NESTED) == "1"
    text = read(ROOT / FACTS) or ""
    if not check(bool(text), f"{FACTS}: missing or empty"):
        return
    check(
        "names a command that recomputes it" in text,
        f"{FACTS} no longer claims every row names a command that recomputes it "
        f"-- this check exists because that sentence is in the file",
    )
    # `\|` inside a cell is a literal pipe, which every Source command here uses
    # -- splitting naively cut each of them in half and reported six rows as
    # naming no command at all. And the file holds a SECOND six-column table,
    # for proof that is not a number, so the block is scoped by its header the
    # way `brand_lint.facts()` scopes it rather than by column count.
    def cells(line: str) -> list[str]:
        parts = re.split(r"(?<!\\)\|", line.strip().strip("|"))
        return [p.strip().replace(r"\|", "|") for p in parts]

    facts, in_table = [], False
    for line in text.splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            in_table = False
            continue
        row = cells(line)
        if row and row[0].lower() == "fact":
            in_table = True
            continue
        if not in_table or set("".join(row)) <= set("-: "):
            continue
        if len(row) >= 6:
            facts.append(row)
    check(bool(facts), f"{FACTS}: no fact rows found to recompute")

    for row in facts:
        name, value, source = row[0], row[1], row[2]
        if source.startswith(NOT_HERE):
            _disclose(f"{FACTS} `{name}` — {source[len(NOT_HERE):].strip()}")
            continue
        command = re.search(r"`([^`]+)`", source)
        if not check(
            command is not None,
            f"{FACTS}: `{name}` names no runnable command in its Source. Either "
            f"give it one in backticks or mark it `{NOT_HERE} <why>` -- a row "
            f"that is neither is a number nobody recomputes and nobody admits to",
        ):
            continue
        if nested:
            # Counted, not run: the parent is the run that recomputes, and the
            # child exists only to print a total the parent can compare.
            check(True, "")
            continue
        try:
            proc = subprocess.run(
                ["bash", "-c", command.group(1)], cwd=str(ROOT),
                capture_output=True, text=True, timeout=300,
                env={**os.environ, FACTS_NESTED: "1"},
            )
        except (OSError, subprocess.SubprocessError) as exc:
            check(False, f"{FACTS}: `{name}` -- its Source command could not run "
                         f"({exc})")
            continue
        got = proc.stdout.strip()
        check(
            got == value,
            f"{FACTS}: `{name}` records {value!r} and its own Source command "
            f"returns {got!r} -- `{command.group(1)}`"
            + (f" (stderr: {proc.stderr.strip()[:160]})" if proc.returncode else ""),
        )


def validate_ai_tell_coverage() -> None:
    """Every `AT-` id in the table has a section, and every section a row.

    B-017: the marker set was numbered `AT-01..AT-15` precisely so coverage
    would be computable, and nothing computed it. Watched: deleting the whole
    `### AT-15.` section while leaving its table row in place kept
    `python3 test/validate.py` at `OK (3539 checks)`, exit 0 -- the ids were a
    promise, not a mechanism. `validate_brand_lint_coverage` had done exactly
    this for `B0NN` since v0.30.0; this is the same question asked of the only
    other numbered set the pack ships.

    Both directions, because they fail differently. A row with no section is a
    marker an agent is told exists and can read nothing about. A section with no
    row is a marker that is documented and unreachable from the index -- and the
    index is what `ai-tells.md` is consulted through.
    """
    path = ROOT / "plugins/super-ux/skills/references/ai-tells.md"
    text = read(path) or ""
    if not check(bool(text), "references/ai-tells.md: missing or empty"):
        return
    rows = re.findall(r"^\|\s*(AT-\d+)\s*\|", text, re.M)
    sections = re.findall(r"^###\s+(AT-\d+)\.", text, re.M)
    check(bool(rows), "ai-tells.md: no `| AT-NN |` table rows to count")
    check(bool(sections), "ai-tells.md: no `### AT-NN.` sections to count")
    for dup, label in ((rows, "table row"), (sections, "section")):
        seen = {i for i in dup if dup.count(i) > 1}
        check(not seen, f"ai-tells.md: duplicate {label}(s) for {sorted(seen)}")
    for at in sorted(set(rows) - set(sections)):
        check(False, f"ai-tells.md: {at} has a table row and no `### {at}.` section "
                     f"-- a marker an agent is told exists and can read nothing about")
    for at in sorted(set(sections) - set(rows)):
        check(False, f"ai-tells.md: {at} has a section and no table row -- the "
                     f"index is how this file is consulted, so the marker is "
                     f"documented and unreachable")
    nums = sorted(int(i.split("-")[1]) for i in set(rows))
    check(
        nums == list(range(1, len(nums) + 1)),
        f"ai-tells.md: the marker set is {nums} -- `AT-` ids are sequential from "
        f"01, and a gap means a retired marker was deleted rather than kept",
    )

    # `B-031`: an exemption is a promise the code has to keep, and until
    # v0.52.0 one of them had gone unkept for thirteen days while this file
    # said otherwise. `B-017` closed the arrow from a named marker to a check;
    # this closes the arrow from a named exemption to a fixture asserting
    # silence. A positive fixture proves a rule fires; only a negative one
    # proves the exemption survives the next person widening the rule.
    fixtures = read(ROOT / "test/brand_lint_test.py") or ""
    exemptions = sorted(set(re.findall(r"\bAT-\d+-E\d+\b", text)))
    check(bool(exemptions),
          "ai-tells.md declares no `AT-NN-EN` exemption ids -- the grammatical "
          "exemptions are unnumbered again, so nothing can compute coverage "
          "over them")
    for ex in exemptions:
        check(ex in fixtures,
              f"ai-tells.md declares the exemption {ex} and "
              f"test/brand_lint_test.py has no fixture naming it -- an "
              f"exemption with no negative fixture is a promise the next "
              f"widening of the rule will break in silence")
    for ex in sorted(set(re.findall(r"\bAT-\d+-E\d+\b", fixtures)) - set(exemptions)):
        check(False,
              f"test/brand_lint_test.py has a fixture for {ex} and ai-tells.md "
              f"declares no such exemption -- the fixture is asserting silence "
              f"nobody promised")


def check_id_set_coverage(rel: str, prefix: str, noun: str) -> tuple[set[str], str]:
    """A numbered doctrine set proves its own completeness, or it is a promise.

    Standing instruction #4 in `docs/evidence/retro.md` is explicit: an artifact
    added to stop drift needs its own answer to "what would notice if this fell
    behind?", and where the artifact is a set, the members get ids first so
    coverage can be computed at all. `validate_ai_tell_coverage` asked this of
    `AT-`; this asks it of every id set the reference shelf ships, from one
    place, because a fourth hand-written copy of the same comparison is the
    drift it exists to refuse.

    Both directions, because they fail differently. A row with no section is a
    rule an agent is told exists and can read nothing about. A section with no
    row is a rule unreachable from the index the file is consulted through.

    Returns the ids found and the file text, so a caller can add the checks that
    are specific to its own file.
    """
    text = read(ROOT / rel) or ""
    name = rel.rsplit("/", 1)[-1]
    if not check(bool(text), f"{rel}: missing or empty"):
        return set(), ""
    rows = re.findall(rf"^\|\s*({prefix}-\d+)\s*\|", text, re.M)
    sections = re.findall(rf"^###\s+({prefix}-\d+)\.", text, re.M)
    check(bool(rows), f"{name}: no `| {prefix}-NN |` table rows to count")
    check(bool(sections), f"{name}: no `### {prefix}-NN.` sections to count")
    for dup, label in ((rows, "table row"), (sections, "section")):
        seen = {i for i in dup if dup.count(i) > 1}
        check(not seen, f"{name}: duplicate {label}(s) for {sorted(seen)}")
    for i in sorted(set(rows) - set(sections)):
        check(False, f"{name}: {i} has a table row and no `### {i}.` section "
                     f"-- a {noun} an agent is told exists and can read nothing "
                     f"about")
    for i in sorted(set(sections) - set(rows)):
        check(False, f"{name}: {i} has a section and no table row -- the index "
                     f"is how this file is consulted, so the {noun} is "
                     f"documented and unreachable")
    nums = sorted(int(i.split("-")[1]) for i in set(rows))
    check(
        nums == list(range(1, len(nums) + 1)),
        f"{name}: the set is {nums} -- `{prefix}-` ids are sequential from 01, "
        f"and a gap means a {noun} was deleted rather than retired",
    )
    return set(sections), text


def check_reference_is_linked(rel: str, skill: str) -> None:
    """An unlinked reference is not shipped, so it reaches nobody.

    `sync_references.py` copies the transitive closure of a skill's links into
    that skill. A file nobody links sits in `skills/references/` and travels no
    further, which looks identical to a file that shipped.
    """
    name = rel.rsplit("/", 1)[-1]
    text = read(ROOT / f"plugins/super-ux/skills/{skill}/SKILL.md") or ""
    check(
        f"references/{name}" in text,
        f"{skill}/SKILL.md does not link references/{name} -- an unlinked "
        f"reference is not shipped into the skill and reaches nobody",
    )


# A front-matter block that a regex reader accepts and a YAML parser refuses.
# Kept as a permanent self-test rather than as a one-off plant: this gate's whole
# claim is that it sees what `front_matter()` cannot, and a gate that has stopped
# being able to see it would otherwise go green on a clean tree forever.
YAML_SELF_TEST = 'name: x\ndescription: Use when a style pack: dashboards is picked\n'


def validate_front_matter_is_yaml() -> None:
    """Every shipped front-matter block parses with a REAL YAML parser.

    `B-033`. `front_matter()` reads the block line by line and never asks what a
    YAML parser would, so a `: ` inside an unquoted scalar turns the whole block
    into an invalid mapping and ships anyway: every reader here stays green
    while any installer that parses YAML refuses the file outright and the hub
    copy freezes on the previous version. The family shipped exactly that twice
    in twelve days -- `sheleg-design` 1.37.4 and 1.58.0, both
    `mapping values are not allowed here` -- and the remedy is ported from the
    sibling that paid for it rather than reinvented.

    Two guards carry the weight, and both are failures the first version of this
    check would have had. It **fails closed** without PyYAML, because a guard
    that discloses and passes when its tool is absent is not a guard. And it
    refuses an **empty walk**, because four globs that all match nothing is a
    moved directory rather than a clean tree.
    """
    try:
        import yaml
    except ImportError:
        check(False, (
            "PyYAML is not importable, and this guard fails closed without it -- "
            "an unparseable SKILL.md installs from every regex reader here and is "
            "refused by every YAML-parsing one. Remedy: python3 -m pip install pyyaml"
        ))
        return

    # The self-test first: if the parser no longer refuses the shape this gate
    # exists for, nothing below it means anything.
    try:
        yaml.safe_load(YAML_SELF_TEST)
        refused = False
    except yaml.YAMLError:
        refused = True
    check(refused, "the front-matter self-test parsed as valid YAML -- this gate "
                   "claims to see what front_matter() cannot, and on this parser "
                   "it no longer can")

    shipped = sorted({
        *ROOT.glob("plugins/*/skills/*/SKILL.md"),
        *ROOT.glob("plugins/*/commands/*.md"),
        *ROOT.glob("cursor/rules/*.mdc"),
    })
    if not check(bool(shipped),
                 "front-matter YAML guard: no shipped front-matter files found -- "
                 "the walk is empty, which is a moved directory rather than a pass"):
        return

    for path in shipped:
        rel = path.relative_to(ROOT)
        raw = raw_front_matter(path)
        if not check(bool(raw), f"{rel}: no front-matter block to parse"):
            continue
        err, data = None, None
        try:
            data = yaml.safe_load(raw)
        except yaml.YAMLError as exc:
            err = exc
        check(
            err is None,
            f"{rel}: front-matter is not valid YAML "
            f"({str(err).splitlines()[0] if err else ''}). The shipped shape of "
            f"this defect is a `: ` inside an unquoted scalar -- quote the "
            f"scalar, or write the separator as ` - ` the way the siblings do",
        )
        check(
            err is not None or isinstance(data, dict),
            f"{rel}: front-matter parses to "
            f"{type(data).__name__ if err is None else 'nothing'}, not a mapping",
        )
        desc = data.get("description") if isinstance(data, dict) else None
        check(
            not isinstance(data, dict) or "description" not in data
            or isinstance(desc, str),
            f"{rel}: `description` parses to {type(desc).__name__}, not a string "
            f"-- an inner `key: value` nests it into a mapping with no parse "
            f"error at all, and an agent host then loads an empty description",
        )


def validate_ledger_table_shape() -> None:
    r"""A ledger row has the cells its own header declares.

    Found by the family umbrella's validator on this repository's own v0.52.0
    tag, not by this one: `B-029`'s row carried an unescaped `|` inside a
    backticked span -- `` `Kind: copy | layout` `` -- and markdown splits a row
    on the pipe before any inline parsing happens, so the code fence does not
    protect it. Every column after the break shifts by one, and `Status` then
    reads as whatever landed in its place: a `resolved` row that machine-reads
    as something else, in the two files this pipeline treats as its record.

    The escape-awareness is the whole check. A first pass counted `\|` as a
    separator and reported fourteen broken rows in files with one, which is a
    detector that would have been switched off inside a week.

    What the `seen` guard does NOT cover, measured rather than assumed:
    `backlog.md` carries the header twice, so renaming one of them leaves the
    other, rows after it keep being checked, and `seen` stays true while
    thirteen rows silently stop being read. That partial loss is the ratchet's
    job -- the count fell 4488 to 4475 -- and this guard only catches a header
    that vanished entirely. Two mechanisms, one for each shape of the failure.
    """
    ledgers = (
        ("docs/evidence/backlog.md", r"^\| (?:B|SU)-\d+ \|", r"^\| id \| Row \|"),
        ("docs/evidence/verification.md", r"^\| R-\d+ \|", r"^\| REQ \| What ships \|"),
    )
    sep = re.compile(r"(?<!\\)\|")
    for rel, row_pat, hdr_pat in ledgers:
        text = read(ROOT / rel)
        if not check(text is not None, f"{rel}: missing"):
            continue
        row_re, hdr_re = re.compile(row_pat), re.compile(hdr_pat)
        width = None
        seen = False
        for number, line in enumerate((text or "").split("\n"), start=1):
            if hdr_re.match(line):
                width = len(sep.findall(line)) - 1
                continue
            if width is None or not row_re.match(line):
                continue
            seen = True
            cells = len(sep.findall(line)) - 1
            check(
                cells == width,
                f"{rel}:{number}: {line.split('|')[1].strip()} has {cells} cells "
                f"against the {width} its header declares -- an unescaped `|` "
                f"inside a cell splits the row before the backticks are read, "
                f"and every column after it shifts",
            )
        check(seen, f"{rel}: no data rows matched -- the ledger's shape changed "
                    f"and this check passed by looking at nothing")


def validate_graph_claims() -> None:
    """The code graph may not assert a number the repository contradicts.

    `B-022` was about the graph being stale. Refreshing it surfaced the sharper
    problem: a node label is an LLM summary, and two of them assert
    "82 tags, 206 practices" about a catalog that has 241 and an index that
    states no counts at all. Nobody computed that number and nothing checked it.

    A wrong document gets argued with; a wrong graph gets believed, because it
    arrives with the authority of a machine and a reader has no way to tell a
    measured node from an invented one. So the counts it asserts are compared
    against the files they are about. Skipped entirely where no graph exists:
    the graph is recommended and never required.
    """
    graph = ROOT / "graphify-out/graph.json"
    if not graph.is_file():
        return
    text = read(graph) or ""
    catalog = read(ROOT / "plugins/super-ux/skills/references/best-practices.md") or ""
    actual = len(re.findall(r"^#### BP-\d+:", catalog, re.M))
    if not check(actual > 0, "best-practices.md: no practices to count"):
        return
    # Only the label fields, and the narrowing is load-bearing. A node
    # summarising a past defect legitimately quotes an old number -- one of
    # them says "the README advertised 181 practices against a catalog of 206",
    # which is history and true. A label is where the graph speaks in its own
    # voice about what is there now, and that is the only voice this can judge.
    import json as _json

    try:
        data = _json.loads(text)
    except ValueError as exc:
        check(False, f"graphify-out/graph.json does not parse: {exc}")
        return

    claimed: set[int] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in ("label", "norm_label") and isinstance(value, str):
                    claimed.update(
                        int(n) for n in re.findall(r"(\d+)\s+practices\b", value)
                    )
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    for n in sorted(claimed - {actual}):
        check(False, f"graphify-out/graph.json labels a node \"{n} practices\" "
                     f"and the catalog has {actual} -- a label is a summary a "
                     f"model wrote, and a wrong graph gets believed where a "
                     f"wrong document gets argued with")


def validate_eval_cases() -> None:
    """The behaviour evals exist, and every case still points at its instruction.

    `B-032`. What an agent does with an instruction cannot be checked here: it
    costs money and it is not deterministic, so `test/evals/run.py` is run by a
    person and its verdict is read by one. What IS deterministic is the shape of
    the case file, and the failure that would otherwise happen quietly: an
    instruction reworded in the skill while its eval keeps quoting the old
    words, so the case still runs, still passes, and measures nothing.

    So the anchor is the load-bearing field. A case whose anchor no longer
    appears verbatim in the file it names is refused here, which forces the
    person rewording the instruction to look at what was measuring it.
    """
    import json as _json

    path = ROOT / "test/evals/cases.json"
    raw = read(path)
    if not check(raw is not None, "test/evals/cases.json: missing -- `B-032` is "
                                  "closed by a mechanism, and this is it"):
        return
    try:
        data = _json.loads(raw or "")
    except ValueError as exc:
        check(False, f"test/evals/cases.json does not parse: {exc}")
        return
    runner = ROOT / "test/evals/run.py"
    check(runner.is_file(), "test/evals/run.py: missing -- the cases have no runner")

    cases = data.get("cases") or []
    check(bool(cases), "test/evals/cases.json declares no cases")
    ids = [c.get("id", "") for c in cases]
    check(len(ids) == len(set(ids)), f"test/evals/cases.json: duplicate ids in {ids}")
    nums = sorted(int(i.split("-")[1]) for i in ids if re.fullmatch(r"EV-\d+", i))
    check(
        len(nums) == len(ids) and nums == list(range(1, len(nums) + 1)),
        f"test/evals/cases.json: ids are {ids} -- `EV-` ids are sequential from "
        f"01, and a gap means a case was deleted rather than replaced",
    )
    for case in cases:
        cid = case.get("id", "?")
        check(bool(case.get("brief")), f"{cid}: no brief, so there is nothing to run")
        check(bool(case.get("expect")),
              f"{cid}: no `expect`, so the case cannot fail and measures nothing")
        check(bool(case.get("measures")),
              f"{cid}: no `measures` line saying what behaviour it is about")
        inst = case.get("instruction") or {}
        rel, anchor_text = inst.get("file"), inst.get("anchor")
        if not check(bool(rel) and bool(anchor_text),
                     f"{cid}: names no instruction -- an eval that cites nothing "
                     f"cannot go stale visibly, which is the whole point"):
            continue
        body = read(ROOT / rel)
        if not check(body is not None, f"{cid} cites {rel}, which does not exist"):
            continue
        check(anchor_text in (body or ""),
              f"{cid}: the anchor {anchor_text!r} no longer appears in {rel} -- "
              f"the instruction was reworded and its eval still quotes the old "
              f"words, so the case runs, passes, and measures nothing")


def validate_vision_rule_embed() -> None:
    """The linter's copy of the vision rule is the template, byte for byte.

    `B-001` closed by giving the seeded linter the canonical text, which makes
    it a THIRD copy -- and a third copy with no comparator is the drift this
    plugin exists to prevent. So it is compared here, the same way
    `validate_hard_rule_copies` compares the other two.
    """
    template = (read(ROOT / "templates/vision-rule.md") or "").strip()
    lint = read(ROOT / "plugins/super-ux/scripts/ux_lint.py") or ""
    if not check(bool(template), "templates/vision-rule.md: missing or empty"):
        return
    embedded = _module_literals(lint).get("VISION_RULE_TEXT")
    if not check(isinstance(embedded, str) and bool(embedded),
                 "ux_lint.py: VISION_RULE_TEXT is not a readable string literal "
                 "-- U077 compares a project's installed rule against it, so an "
                 "unreadable constant means the check silently stops checking"):
        return
    check(
        embedded.strip() == template,
        "ux_lint.py's VISION_RULE_TEXT differs from templates/vision-rule.md -- "
        "one rule, one text, and this copy is the one every target project "
        "measures itself against",
    )


def validate_audit_scope_enum() -> None:
    """The `/ux-audit` scope enum lives in four homes, and they must agree.

    `B-030`. `SUX-06` found `copy` and `benchmark:<competitor>` legal in the
    skill's body and absent from both places an agent reads first, so the two
    scopes existed and were unreachable. That instance was fixed by hand in
    v0.50.0 and the class was not: a scope added tomorrow goes invisible the
    same way. Same shape as `validate_status_enums_match_contract`, applied to
    the other enum this pack ships in more than one file.

    Two homes are the enum and must be equal: the command's `argument-hint`,
    which is what a user sees, and the skill's step-1 parenthetical, which is
    what the agent reads. Two are subsets and must not stray: the `## <Name>
    scope (`token`)` sections, and the single-pass list. A subset may be
    smaller -- not every scope needs a section -- but a token in one of them
    that no home declares is a scope the body treats as legal and nothing
    offers.
    """
    cmd = read(ROOT / "plugins/super-ux/commands/ux-audit.md") or ""
    skl = read(ROOT / "plugins/super-ux/skills/ux-audit/SKILL.md") or ""
    if not check(bool(cmd) and bool(skl), "ux-audit command or skill is missing"):
        return

    hint = re.search(r'^argument-hint:\s*"\[([^\]]+)\]', cmd, re.M)
    step = re.search(r"Scope is\s*\n?\s*`\$ARGUMENTS` if given \(([^)]+)\)", skl)
    if not check(hint is not None,
                 "ux-audit.md: no `argument-hint: \"[a | b | ...]\"` to read -- the "
                 "enum's user-facing home has moved and this check cannot compare it"):
        return
    if not check(step is not None,
                 "ux-audit/SKILL.md: step 1 no longer says ``$ARGUMENTS` if given "
                 "(...)` -- the enum's agent-facing home has moved"):
        return

    declared = {t.strip() for t in hint.group(1).split("|") if t.strip()}
    stepwise = set(re.findall(r"`([^`]+)`", step.group(1)))
    check(bool(declared), "ux-audit.md: the argument-hint declares no scopes")
    for tok in sorted(declared - stepwise):
        check(False, f"ux-audit: `{tok}` is offered in the command's "
                     f"argument-hint and absent from the skill's step 1 -- the "
                     f"user is offered a scope the agent does not enumerate")
    for tok in sorted(stepwise - declared):
        check(False, f"ux-audit: `{tok}` is enumerated in the skill's step 1 "
                     f"and absent from the command's argument-hint -- the scope "
                     f"is legal and nothing offers it, which is SUX-06 exactly")

    sections = set(re.findall(r"^## .*? scope \(`([^`]+)`\)", skl, re.M))
    for tok in sorted(sections - declared):
        check(False, f"ux-audit/SKILL.md has a `## … scope (`{tok}`)` section "
                     f"for a scope no home declares -- the body treats it as "
                     f"legal and no caller can reach it")
    single = re.search(r"Single-pass\s*\n?\s*scopes \(([^)]+)\)", skl)
    if check(single is not None,
             "ux-audit/SKILL.md no longer names its single-pass scopes -- the "
             "list decides which scopes skip the scenario loop"):
        passes = {t for part in re.findall(r"`([^`]+)`", single.group(1))
                  for t in part.split("/")}
        for tok in sorted(passes - declared):
            check(False, f"ux-audit/SKILL.md lists `{tok}` as a single-pass "
                         f"scope and no home declares it as a scope at all")


def validate_doctrine_set_coverage() -> None:
    """Every numbered set on the reference shelf, and the skill it ships into."""
    sets = (
        ("plugins/super-ux/skills/references/landing-pages.md", "LP", "rule",
         "copywriting"),
        ("plugins/super-ux/skills/references/onboarding.md", "ON", "rule",
         "ux-flows"),
        ("plugins/super-ux/skills/references/internal-screens.md", "IS", "rule",
         "ux-flows"),
        ("plugins/super-ux/skills/references/product-frameworks.md", "PF",
         "framework", "ux-foundation"),
    )
    for rel, prefix, noun, skill in sets:
        sections, text = check_id_set_coverage(rel, prefix, noun)
        check_reference_is_linked(rel, skill)
        if not text:
            continue
        # The runnable part of a file is the only part that can point at
        # nothing. Renumbering the set and not the checks is the exact drift
        # the ids were introduced to make visible.
        tail = text.split("## The readiness check", 1)
        if len(tail) == 2:
            for i in sorted(set(re.findall(rf"\b({prefix}-\d+)\b", tail[1]))
                            - sections):
                check(False, f"{rel.rsplit('/', 1)[-1]}: the readiness check "
                             f"names {i} and no section defines it -- a check "
                             f"pointing at nothing")

    # The rules were extracted from teardowns that live in this repository, and
    # both the playbook and the linter's own comments cite them. A citation
    # that stops resolving is the shape `evidence-docs` exists to refuse: a
    # claim that reads as sourced and is not. Nothing else watches these.
    cited: set[str] = set()
    for src in ("plugins/super-ux/scripts/brand_lint.py",
                "plugins/super-ux/skills/references/landing-pages.md",
                "docs/brand/lint.py"):
        cited |= set(re.findall(r"docs/research/landings/[\w.-]+\.md",
                                read(ROOT / src) or ""))
    check(bool(cited), "nothing cites docs/research/landings/ -- the playbook's "
                       "evidence base is unreferenced, so it is not evidence")
    for ref in sorted(cited):
        check((ROOT / ref).exists(),
              f"{ref} is cited and does not exist -- a claim that reads as "
              f"sourced and is not")


def validate_ux_lint_coverage() -> None:
    """Every code the UX linter can emit has a fixture, and the contract names it.

    The brand linter has had this since v0.30.0 and the older, more central
    linter had neither codes nor fixtures until v0.34.0 -- so the harness could
    fall behind the linter exactly the way the linter had fallen behind the
    contract, and nothing would have said so.
    """
    lint = read(ROOT / "plugins/super-ux/scripts/ux_lint.py") or ""
    tests = read(ROOT / "test/ux_lint_test.py") or ""
    contract = read(
        ROOT / "plugins/super-ux/skills/references/scenario-format.md"
    ) or ""
    emitted = sorted(set(re.findall(r"\[(U\d{3})\]", lint)))
    check(bool(emitted), "ux_lint.py: no check codes found")
    for code in emitted:
        check(
            f'"{code}"' in tests,
            f"{code} is emitted by ux_lint.py with no fixture in "
            f"ux_lint_test.py -- a check nobody watched fail is not evidence",
        )
        check(
            code in contract,
            f"{code} is emitted by ux_lint.py but scenario-format.md does not "
            f"name it -- the code's meaning would live only in the source",
        )


# The contract's one home for every enum the linter matches on. Parsed, not
# restated: a second copy here would be the third copy of a table that had
# already drifted between the first two.
#
# The alternation was `(SCN|ST|SCR)` until 2026-08-20, and that short alphabet
# was the whole defect: NINE live `Status:` values sat on layers this regex could
# not name -- four flows, two personas, three jobs -- so the parity check was
# real, passing, and blind to three quarters of the layers that carry a status.
# A prefix added to the linter's table with no row in the contract now fails
# here, which is what the check was always supposed to mean.
ENUM_DECL_RE = re.compile(
    r"^- `(SCN|ST|SCR|P|JTBD)-N+` \*\*(Status|Product)\*\* — `([^`]+)`",
    re.MULTILINE,
)

# A layer whose state lives on the document, not on an entry: `vision.md` in the
# scenario contract, `voice.md` in the brand contract. Same shape, no id.
DOC_ENUM_DECL_RE = re.compile(
    r"^- `([\w.-]+\.md)` \*\*(\w+)\*\* — `([^`]+)`", re.MULTILINE
)

# The layers the contract declares to have NO status. Read from the contract's
# own sentence rather than restated, so deleting the sentence fails the check
# that depends on it.
STATUSLESS_DECL_RE = re.compile(r"A `Status` on either is `U075`")


def _module_literals(source: str) -> dict:
    """Module-level assignments of literal values, read without importing."""
    out: dict = {}
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return out
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            out[target.id] = ast.literal_eval(node.value)
        except (ValueError, TypeError, SyntaxError):
            continue
    return out


def validate_status_enums_match_contract() -> None:
    """Every enum the linter matches on is the enum the contract declares.

    The defect this exists for was live in this repository and had never been
    reported. `scenario-format.md` declared five screen statuses — `blocked`
    among them, with a rules paragraph of its own — and `ux_lint.py` matched
    four, so a `blocked` screen produced `status = None` and `U021` quietly
    stopped applying to it. An out-of-enum value that reads as *no value* is the
    worst of the three possible outcomes: not refused, not accepted, invisible.

    A contract and a matcher are two copies of one table, and two copies drift.
    This makes them fail together instead. The linter's side is read out of its
    own source with `ast`, so nothing is restated here either.
    """
    lint = read(ROOT / "plugins/super-ux/scripts/ux_lint.py") or ""
    contract = read(
        ROOT / "plugins/super-ux/skills/references/scenario-format.md"
    ) or ""

    declared: dict[tuple[str, str], set[str]] = {}
    for prefix, field, values in ENUM_DECL_RE.findall(contract):
        declared[(prefix, field)] = {v.strip() for v in values.split("|") if v.strip()}
    check(
        bool(declared),
        "scenario-format.md declares no status/product enum in the form "
        "`- `SCN-NNN` **Status** — `a | b`` — the one home of every enum the "
        "linter matches on has moved or been renamed",
    )

    literals = _module_literals(lint)
    matched: dict[tuple[str, str], set[str]] = {
        (prefix, "Status"): set(values)
        for prefix, values in (literals.get("STATUS_ENUMS") or {}).items()
    }
    product = set(literals.get("PRODUCT_STATES") or ())
    check(bool(product), "ux_lint.py: PRODUCT_STATES is not a readable literal")
    product_layers = literals.get("PRODUCT_LAYERS") or ()
    check(bool(product_layers), "ux_lint.py: PRODUCT_LAYERS is not a readable literal")
    for prefix in product_layers:
        matched[(prefix, "Product")] = product

    for key in sorted(set(matched) | set(declared)):
        prefix, field = key
        check(
            matched.get(key) == declared.get(key),
            f"{prefix} {field}: ux_lint.py matches "
            f"{sorted(matched.get(key) or [])} and scenario-format.md declares "
            f"{sorted(declared.get(key) or [])} — one side moved alone, and a "
            f"value only the contract knows about reads as no value at all",
        )

    # --- The document-level layers, and the two declared to have none ---------
    doc_declared = {
        name: {v.strip() for v in values.split("|") if v.strip()}
        for name, field, values in DOC_ENUM_DECL_RE.findall(contract)
        if field == "Status"
    }
    doc_matched = {
        name: set(values)
        for name, values in (literals.get("DOC_STATUS_ENUMS") or {}).items()
    }
    check(bool(doc_matched), "ux_lint.py: DOC_STATUS_ENUMS is not a readable literal")
    for name in sorted(set(doc_matched) | set(doc_declared)):
        check(
            doc_matched.get(name) == doc_declared.get(name),
            f"{name} Status: ux_lint.py matches {sorted(doc_matched.get(name) or [])} "
            f"and scenario-format.md declares {sorted(doc_declared.get(name) or [])}",
        )

    statusless = {p for p, _f, _w in (literals.get("STATUSLESS_LAYERS") or ())}
    check(
        statusless == {"FLW", "JRN"},
        f"ux_lint.py: STATUSLESS_LAYERS is {sorted(statusless)} — the contract's "
        f"declared statusless layers are FLW and JRN",
    )
    check(
        bool(STATUSLESS_DECL_RE.search(contract)),
        "scenario-format.md no longer says that a `Status` on FLW or JRN is "
        "`U075` — a layer declared to have no status only has none while the "
        "contract says so",
    )
    for prefix in sorted(statusless):
        check(
            f"`{prefix}-NN` **Status**" not in contract,
            f"scenario-format.md declares a Status enum for {prefix} while "
            f"ux_lint.py refuses one there (U075) — the two cannot both be right",
        )

    # --- The brand layer, whose enum was outside this mechanism entirely ------
    brand_lint = read(ROOT / "plugins/super-ux/scripts/brand_lint.py") or ""
    brand_contract = read(
        ROOT / "plugins/super-ux/skills/references/brand-contract.md"
    ) or ""
    brand_declared = {
        (name, field): {v.strip() for v in values.split("|") if v.strip()}
        for name, field, values in DOC_ENUM_DECL_RE.findall(brand_contract)
    }
    brand_matched = set(_module_literals(brand_lint).get("VOICE_STATUSES") or ())
    check(
        bool(brand_matched),
        "brand_lint.py: VOICE_STATUSES is not a readable literal",
    )
    check(
        brand_declared.get(("voice.md", "Status")) == brand_matched,
        f"voice.md Status: brand_lint.py matches {sorted(brand_matched)} and "
        f"brand-contract.md declares "
        f"{sorted(brand_declared.get(('voice.md', 'Status')) or [])} "
        f"— the layer whose out-of-enum value shipped for two releases",
    )

    # The second document-level enum on the same file, inside the mechanism
    # from the day it was written rather than after it drifted. `Humanization`
    # is read by every mode that produces text, so a value only one side knows
    # about is a pass that silently does not run.
    kinds = set(_module_literals(brand_lint).get("STRING_KINDS") or ())
    check(bool(kinds), "brand_lint.py: STRING_KINDS is not a readable literal")
    check(
        brand_declared.get(("strings.md", "Kind")) == kinds,
        f"strings.md Kind: brand_lint.py matches {sorted(kinds)} and "
        f"brand-contract.md declares "
        f"{sorted(brand_declared.get(('strings.md', 'Kind')) or [])}",
    )

    modes = set(_module_literals(brand_lint).get("HUMANIZATION_MODES") or ())
    check(bool(modes), "brand_lint.py: HUMANIZATION_MODES is not a readable literal")
    check(
        brand_declared.get(("voice.md", "Humanization")) == modes,
        f"voice.md Humanization: brand_lint.py matches {sorted(modes)} and "
        f"brand-contract.md declares "
        f"{sorted(brand_declared.get(('voice.md', 'Humanization')) or [])}",
    )


# The exact words the two homes of the after-a-run step must carry. An audit
# reads code; the product state is a claim about the world. `U068` refuses the
# two artefacts an audit could hand in as an outcome signal, and this is the
# other half of that guard — the instruction that would produce the attempt.
AUDIT_PRODUCT_GUARD = "never writes `Product:`"

AUDIT_PRODUCT_GUARD_HOMES = (
    "plugins/super-ux/skills/ux-audit/SKILL.md",
    "plugins/super-ux/skills/references/scenario-format.md",
)


def validate_audit_leaves_product_alone() -> None:
    """No shipped instruction lets an audit PASS promote the outcome state.

    Manifesto M-21: a change can be implementation-verified and
    product-unvalidated, and pretending delivery proof is outcome proof is not
    Proof of Done. The audit's after-a-run step used to say only "flip
    `validated` → `implemented` where the audit PASSed", so the chain could
    record that the code does what the scenario said and had no way to record
    whether the scenario was the right thing to build. Both homes of that step
    carry the prohibition now, and both are checked, because the step had
    already been copied once.
    """
    for rel in AUDIT_PRODUCT_GUARD_HOMES:
        text = read(ROOT / rel) or ""
        check(
            AUDIT_PRODUCT_GUARD in text,
            f"{rel}: the after-a-run step does not say the audit "
            f"{AUDIT_PRODUCT_GUARD} — an audit allowed to write the outcome "
            f"state turns delivery proof into outcome proof, which is the whole "
            f"defect the field exists to prevent",
        )


# Paths under docs/ belong to the target project, so an instruction naming one
# is telling a reader to run a file super-ux put there. Repo-internal commands
# (test/validate.py and friends) are addressed to a contributor and are not.
RUN_INSTRUCTION_RE = re.compile(r"python3\s+(docs/[\w./-]+\.py)")

RUN_INSTRUCTION_SURFACES = (
    "plugins/super-ux/commands",
    "plugins/super-ux/skills",
    "templates",
)


def validate_run_instructions() -> None:
    """Every path an instruction says to run is a path some command seeds.

    `validate_seeded_scripts` asks the question one way -- for each known
    destination, does a command copy it? That leaves the other direction open,
    and it is the direction a rename breaks: an instruction pointing at
    `docs/ux/linter.py` while commands seed `docs/ux/lint.py` passes the first
    check and fails the reader.
    """
    seeded = {dest for dest, _ in SEEDED_SCRIPTS}
    named: dict[str, list[str]] = {}
    files = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "CLAUDE.md"]
    for rel in RUN_INSTRUCTION_SURFACES:
        files.extend(sorted((ROOT / rel).rglob("*.md")))
    for path in files:
        for hit in RUN_INSTRUCTION_RE.findall(read(path) or ""):
            named.setdefault(hit, []).append(
                path.relative_to(ROOT).as_posix()
            )
    check(bool(named), "no `python3 docs/....py` instruction found anywhere")
    for path, sources in sorted(named.items()):
        check(
            path in seeded,
            f"instructions tell the reader to run `{path}` "
            f"({sources[0]}{'' if len(sources) == 1 else f' +{len(sources) - 1} more'}) "
            f"but no command seeds that path -- SEEDED_SCRIPTS has "
            f"{', '.join(sorted(seeded))}",
        )



# --------------------------------------------------------------- the ratchet
#
# Ported from sheleg-design, whose retrospective recorded the class: a gate
# whose check count can fall silently cannot detect a deleted requirement --
# there, stripping four required headings dropped the count by one and the
# suite stayed green. This repository had no ratchet at all, so the same
# deletion here was invisible by construction rather than by accident.
FLOORS = ROOT / "test" / "floors.json"


def check_floor(script: str, count: int) -> int:
    """Non-zero when this run checked less than the recorded floor."""
    if not FLOORS.is_file():
        return 0
    try:
        floors = json.loads(FLOORS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL: {FLOORS.name} is not valid JSON ({exc})", file=sys.stderr)
        return 1
    floor = floors.get(script)
    if floor is None:
        return 0
    if count < floor:
        print(
            f"FAIL: {script} ran {count} checks, below its floor of {floor}. "
            f"Checks do not disappear on their own -- something that used to be "
            f"required is not being required any more. If the drop is intended, "
            f"lower the floor in {FLOORS.name} in the same commit, with the reason.",
            file=sys.stderr,
        )
        return 1
    return 0


def _disclose_routing(msg):
    """A check that could not run, said out loud rather than counted as a pass."""
    print(f"  unlooked: {msg}")


def check_routed_triggers_still_advertised():
    """The family's routing hook fires on words this description has to keep.

    B-54, 2026-08-16: `sheleg-design` 1.37.0 shipped green on its own gate having dropped
    a phrase from its description that was a live trigger in the umbrella's
    `lib/triggers.js`. This repository has no way to know that table exists, and it
    releases BEFORE the umbrella re-pins, so the umbrella found out minutes after the tag.
    A hook firing on a promise nobody made is the defect; a patch release was the cost.

    **The table is not copied here.** The umbrella's own checker is asked, reading the
    module the hook itself calls, so there is no duplicate to drift. When no umbrella sits
    above this checkout — the ordinary state of a standalone clone, and of CI — this
    discloses instead of passing, because a check that cannot look must never read as one
    that looked.
    """
    script = os.path.join(str(ROOT), "..", "..", "test", "advertised_check.js")
    if not os.path.isfile(script):
        _disclose_routing("routed triggers — no sshlg-skills umbrella above this checkout")
        return
    try:
        proc = subprocess.run(["node", script, "--member", "super-ux", "--root", str(ROOT)],
                              capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        _disclose_routing(f"routed triggers — could not run the umbrella's checker ({exc})")
        return
    if proc.returncode == 1:
        check(False, (proc.stdout + proc.stderr).strip())
    elif proc.returncode != 0:
        _disclose_routing(f"routed triggers — {(proc.stderr or 'the checker could not look').strip()}")


def main() -> int:
    validate_manifests()
    validate_npm_payload()
    validate_skills()
    validate_commands()
    validate_cursor_rules()
    validate_templates()
    validate_hard_rule_copies()
    validate_linter()
    validate_links()
    validate_reference_contents()
    validate_shipped_references()
    validate_shipped_templates()
    validate_shipped_paths()
    validate_catalog()
    validate_stated_numbers()
    validate_skill_parity()
    validate_seeded_scripts()
    validate_brand_contract()
    validate_voice_packs()
    validate_brand_templates()
    validate_brand_practices()
    validate_brand_field_ownership()
    validate_brand_lint_coverage()
    validate_ux_lint_coverage()
    validate_status_enums_match_contract()
    validate_audit_leaves_product_alone()
    validate_run_instructions()
    validate_ai_tell_coverage()
    validate_front_matter_is_yaml()
    validate_ledger_table_shape()
    validate_graph_claims()
    validate_eval_cases()
    validate_vision_rule_embed()
    validate_audit_scope_enum()
    validate_doctrine_set_coverage()
    validate_board_ids()
    validate_hard_rule_anchors()
    validate_facts_recompute()
    # A release must not publish over a red `validate`.
    #
    # On 2026-08-12 `sheleg-dev` tagged v0.4.1 while its own validate run for that exact
    # tag FAILED, and npm served 0.4.1 four minutes later — two separate workflows with
    # nothing connecting them. Six of the family's nine repositories were in that state.
    # `workflow_call` connects them; these three keep the connection there, because a
    # dependency nobody checks is a dependency somebody removes.
    _wf = ROOT / ".github" / "workflows"
    _val, _rel = _wf / "validate.yml", _wf / "release.yml"
    if _val.is_file() and _rel.is_file():
        _v, _r = _val.read_text(encoding="utf-8"), _rel.read_text(encoding="utf-8")
        check(bool(re.search(r"^\s*workflow_call:\s*$", _v, re.M)),
              ".github/workflows/validate.yml: no `workflow_call:` trigger — the release "
              "workflow cannot run this suite, so a publish goes out over whatever subset "
              "it runs itself")
        check(bool(re.search(r"^\s*uses:\s*\./\.github/workflows/validate\.yml\s*$", _r, re.M)),
              ".github/workflows/release.yml: does not call ./.github/workflows/validate.yml "
              "— a red validate would not stop a publish")
        check(bool(re.search(r"^\s*needs:\s*(?:\[[^\]]*\bvalidate\b[^\]]*\]|validate)\s*$", _r, re.M)),
              ".github/workflows/release.yml: no job declares `needs: validate` — calling the "
              "suite without depending on it lets the release run beside it rather than "
              "after it, which looks gated and is not")

    # `SKILL-CARD.md` is the entry a stranger decides from, and nothing read it.
    #
    # It carries the fields Anthropic's Skills-for-enterprise guidance asks every
    # organisation to keep — "written so somebody who did not build this can decide" —
    # and the version moves in `package.json`, `plugin.json` and `marketplace.json` on
    # every release while the card was in no list. So it could only drift. Measured
    # 2026-09-01 across the family: FOUR of nine cards were behind, this one by four
    # minor releases (0.48.3 against 0.52.3) and `agent-stack` by ten.
    #
    # A card that states no version at all is refused too: one a reader cannot see go
    # stale is worse than one that lags visibly.
    _card = ROOT / "SKILL-CARD.md"
    if _card.is_file():
        _ships = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
        _row = r"\|\s*\*{0,2}Version\*{0,2}\s*\|\s*`?([0-9]+\.[0-9]+\.[0-9]+)`?\s*\|"
        _m = re.search(_row, _card.read_text(encoding="utf-8"))
        check(bool(_m),
              "SKILL-CARD.md: no `Version` row this check can read — the card is the entry "
              "a stranger decides from, and a version it does not state is one that cannot "
              "go stale visibly. Write it as a table row.")
        if _m:
            check(_m.group(1) == _ships,
                  f"SKILL-CARD.md: the registry card says {_m.group(1)} and package.json "
                  f"ships {_ships} — the card is what somebody who did not build this "
                  "decides from, so the one field that dates it may not lag. Bump it in "
                  "the same change as the manifests.")

    check_routed_triggers_still_advertised()

    if failures:
        # `B-019`: a reader counts the lines and the summary reports a number,
        # and when one defect is emitted twice those disagree. Print each
        # distinct message once and say plainly when a message arrived more
        # than once, so a double emission is a visible fact rather than an
        # inflated count nobody can reconcile against the output.
        seen: list[str] = []
        for failure in failures:
            if failure not in seen:
                seen.append(failure)
                print(f"FAIL: {failure}")
        if len(seen) != len(failures):
            print(f"note: {len(failures) - len(seen)} duplicate emission(s); "
                  f"a check is firing twice for one defect")
        print(f"{len(seen)} failure(s) out of {checks} checks")
        return 1
    rc = check_floor("validate.py", checks)
    if rc:
        return rc
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
