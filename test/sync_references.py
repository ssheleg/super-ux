#!/usr/bin/env python3
"""Sync shared contracts into every skill that links them.

`plugins/super-ux/skills/references/` is the SOURCE OF TRUTH. The skills CLI ships
only a skill's own directory, so each skill must carry its own copy of the
contracts it links (plus everything those contracts link, transitively) — otherwise
the contracts arrive dangling on Cursor/Codex/OpenClaw/etc.

Run after editing anything in `skills/references/`; `test/validate.py` fails if a
copy has drifted.
"""
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "plugins/super-ux/skills")
SRC = os.path.join(SKILLS, "references")

LINK_RE = re.compile(r"\]\(([a-z0-9-]+\.md)\)")
SKILL_LINK_RE = re.compile(r"\]\(references/([a-z0-9-]+\.md)\)")


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
    print(f"sync complete ({changed} file(s) written/removed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
