#!/usr/bin/env python3
"""Consistency validator for the super-ux repo (stdlib only).

Checks (spec docs/superpowers/specs/2026-07-19-super-ux-design.md, section 9):
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
    match = re.search(r"^## \[?(\d+\.\d+\.\d+)\]?", text, re.MULTILINE)
    check(match is not None, "CHANGELOG.md: no '## [x.y.z]' release heading")
    return match.group(1) if match else None


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
    check(
        (skills_dir / "references/scenario-format.md").is_file(),
        "plugins/super-ux/skills/references/scenario-format.md: missing",
    )


def validate_commands() -> None:
    commands_dir = ROOT / "plugins/super-ux/commands"
    expected = {"ux.md", "ux-init.md", "ux-update.md", "ux-audit.md", "ux-rule.md", "ux-foundation.md"}
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
    for name in ("scenarios.md", "audit-report.md", "claude-rule.md", "foundation.md"):
        path = ROOT / "templates" / name
        text = read(path)
        check(bool(text and text.strip()), f"templates/{name}: missing or empty")


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


def main() -> int:
    validate_manifests()
    validate_skills()
    validate_commands()
    validate_cursor_rules()
    validate_templates()
    validate_links()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} failure(s) out of {checks} checks")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
