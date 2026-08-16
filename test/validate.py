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



def raw_front_matter(path) -> str:
    """The front-matter block verbatim -- what an agent host actually loads."""
    text = read(path) or ""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return "" if end == -1 else text[4:end]


def check_description_canon(rel, path, desc: str) -> None:
    """The three canon rules every skill description must satisfy."""
    check(
        desc.startswith("Use when"),
        f"{rel}/SKILL.md: description must start with 'Use when' (canon)",
    )
    check(
        bool(re.search(r"[а-яё]", desc, re.I)),
        f"{rel}/SKILL.md: description must carry Russian trigger aliases beside the English ones (canon)",
    )
    raw = raw_front_matter(path)
    check(
        len(raw) <= 1024,
        f"{rel}/SKILL.md: front-matter is {len(raw)} chars, must be under 1024 (canon)",
    )


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
        check_description_canon(rel, skill / "SKILL.md", fm.get("description") or "")
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
    validate_run_instructions()
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

    check_routed_triggers_still_advertised()

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} failure(s) out of {checks} checks")
        return 1
    rc = check_floor("validate.py", checks)
    if rc:
        return rc
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
