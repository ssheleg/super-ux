#!/usr/bin/env python3
"""Consistency validator for the super-ux repo (stdlib only).

Checks (spec docs/superpowers/specs/2026-07-19-super-ux-design.md, section 9):
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
    expected = {"ux.md", "ux-init.md", "ux-update.md", "ux-audit.md", "ux-rule.md", "ux-foundation.md", "ux-flows.md", "ux-lint.md"}
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
    for name in ("scenarios.md", "audit-report.md", "claude-rule.md", "foundation.md", "flows.md", "screens.md", "README.md"):
        path = ROOT / "templates" / name
        text = read(path)
        check(bool(text and text.strip()), f"templates/{name}: missing or empty")


def validate_hard_rule_copies() -> None:
    """The hard rule lives in two Claude-facing places — they must be one text.

    `templates/claude-rule.md` seeds new projects; `/ux-rule` appends its own
    embedded copy to an existing CLAUDE.md. Two copies of a rule is exactly the
    drift this plugin exists to prevent, and neither file looks wrong alone.
    """
    template = (read(ROOT / "templates/claude-rule.md") or "").strip()
    command = read(ROOT / "plugins/super-ux/commands/ux-rule.md") or ""
    match = re.search(r"```markdown\n(.*?)\n   ```", command, re.DOTALL)
    if not check(bool(match) and bool(template), "ux-rule.md: no embedded ```markdown rule block"):
        return
    embedded = "\n".join(
        line[3:] if line.startswith("   ") else line
        for line in match.group(1).splitlines()
    ).strip()
    check(
        embedded == template,
        "ux-rule.md's embedded rule block differs from templates/claude-rule.md "
        "(one rule, one text — re-copy the template into the command)",
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
    validate_shipped_references()
    validate_catalog()
    validate_brand_contract()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} failure(s) out of {checks} checks")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
