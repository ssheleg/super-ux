#!/usr/bin/env python3
"""Sync shared contracts and templates into everything that ships them.

`plugins/super-ux/skills/references/` is the SOURCE OF TRUTH for contracts. The
skills CLI ships only a skill's own directory, so each skill must carry its own
copy of the contracts it links (plus everything those contracts link,
transitively) — otherwise the contracts arrive dangling on
Cursor/Codex/OpenClaw/etc.

`templates/` at the repo root is the SOURCE OF TRUTH for seeds, and it travels
the same way (SUX-01, 2026-08-29: six shipped texts named "the plugin's
`templates/`" while the marketplace ships `./plugins/super-ux` — the directory
was absent from every installed channel and every init workflow dead-ended).
The full tree is mirrored into `plugins/super-ux/templates/` for the plugin
channel, and each skill whose SKILL.md names a backticked `templates/…` path
gets its own copy of exactly those files, because a skill installed by the
skills CLI has no plugin root to reach up to.

Run after editing anything in `skills/references/` or `templates/`;
`test/validate.py` fails if a copy has drifted.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "plugins/super-ux/skills")
SRC = os.path.join(SKILLS, "references")
TEMPLATES = os.path.join(ROOT, "templates")
PLUGIN_TEMPLATES = os.path.join(ROOT, "plugins/super-ux/templates")

LINK_RE = re.compile(r"\]\(([a-z0-9-]+\.md)\)")
SKILL_LINK_RE = re.compile(r"\]\(references/([a-z0-9-]+\.md)\)")
TEMPLATE_TOKEN_RE = re.compile(r"`templates/([A-Za-z0-9._/-]*)`")


def closure(seed, available):
    """Every contract reachable from `seed` by following links between contracts."""
    seen, stack = set(), list(seed)
    while stack:
        name = stack.pop()
        if name in seen or name not in available:
            continue
        seen.add(name)
        text = open(os.path.join(SRC, name), encoding="utf-8").read()
        stack.extend(n for n in LINK_RE.findall(text) if n in available and n not in seen)
    return seen


def _files_under(root):
    """Every file below `root`, as a path relative to it. Empty when absent."""
    out = set()
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            out.add(os.path.relpath(os.path.join(dirpath, name), root))
    return out


def template_closure(text):
    """Template files (relative to templates/) a text names in backticks.

    A token naming a file ships that file; a token naming a directory (with or
    without the trailing slash) ships everything under it. A token that names
    nothing ships nothing — `validate_shipped_paths` in test/validate.py is the
    gate that refuses it, so the failure is loud rather than silently skipped.
    """
    available = _files_under(TEMPLATES)
    needed = set()
    for token in TEMPLATE_TOKEN_RE.findall(text):
        token = token.rstrip("/")
        if token in available:
            needed.add(token)
        elif token == "":
            needed |= available
        else:
            needed |= {rel for rel in available if rel.startswith(token + "/")}
    return needed


def mirror_templates(needed, dest):
    """Make `dest` hold exactly `needed` (relative paths), byte-identical to
    templates/. Strays are removed, emptied directories pruned."""
    changed = 0
    for rel in sorted(needed):
        s, d = os.path.join(TEMPLATES, rel), os.path.join(dest, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if not os.path.exists(d) or open(s, "rb").read() != open(d, "rb").read():
            shutil.copyfile(s, d)
            changed += 1
    for rel in sorted(_files_under(dest) - needed):
        os.remove(os.path.join(dest, rel))
        changed += 1
    for dirpath, dirnames, filenames in os.walk(dest, topdown=False):
        if not dirnames and not filenames:
            os.rmdir(dirpath)
    return changed


def main():
    available = {f for f in os.listdir(SRC) if f.endswith(".md")}
    changed = 0
    for skill in sorted(os.listdir(SKILLS)):
        skill_dir = os.path.join(SKILLS, skill)
        if not os.path.isdir(skill_dir) or skill == "references":
            continue
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        text = open(skill_md, encoding="utf-8").read()
        seeds = template_closure(text)
        if seeds or os.path.isdir(os.path.join(skill_dir, "templates")):
            changed += mirror_templates(seeds, os.path.join(skill_dir, "templates"))
            if seeds:
                print(f"{skill}: {len(seeds)} template(s) shipped")
        needed = closure(set(SKILL_LINK_RE.findall(text)), available)
        if not needed:
            continue
        dest = os.path.join(skill_dir, "references")
        os.makedirs(dest, exist_ok=True)
        for name in sorted(needed):
            s, d = os.path.join(SRC, name), os.path.join(dest, name)
            if not os.path.exists(d) or open(s, "rb").read() != open(d, "rb").read():
                shutil.copyfile(s, d)
                changed += 1
        # drop copies no longer linked
        for stale in sorted(set(os.listdir(dest)) - needed):
            os.remove(os.path.join(dest, stale))
            changed += 1
        print(f"{skill}: {len(needed)} contract(s) shipped")
    changed += mirror_templates(_files_under(TEMPLATES), PLUGIN_TEMPLATES)
    print(f"plugin: full templates/ tree shipped ({len(_files_under(PLUGIN_TEMPLATES))} file(s))")
    print(f"sync complete ({changed} file(s) written/removed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
