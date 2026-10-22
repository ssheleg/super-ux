#!/usr/bin/env python3
"""family_gate.py: two checks every sshlg-skills member runs in its own gate.

Canonical copy: ssheleg/sshlg-skills `member-gate/family_gate.py`. Every member carries it
byte for byte as `test/family_gate.py`; the hub checks the copies by hash. Do not edit a
member's copy: change the canonical file and copy it out.

    python3 test/family_gate.py              check this repository (the current directory)
    python3 test/family_gate.py --self-test  plant each defect in a scratch copy, watch it fail

1. The board parses (hub B-108). Every row of every table in `docs/evidence/backlog.md` has
   as many cells as its own header (a bare `|` inside a cell shifts the row), and no row id
   appears twice. A repository without a board says so and passes.
2. The release workflow refuses an unreachable tag (hub B-109). `.github/workflows/release.yml`
   checks out full history (`fetch-depth: 0`) and asks `git merge-base --is-ancestor` before it
   publishes. A repository without the workflow says so and passes.

Exit 0 green, 1 a defect, 2 a self-test whose plant was not caught. Standard library only.
"""
import os
import re
import shutil
import sys
import tempfile

BOARD = os.path.join("docs", "evidence", "backlog.md")
RELEASE = os.path.join(".github", "workflows", "release.yml")
ROW_ID = re.compile(r"^\**([A-Z][A-Z0-9]*-\d+[a-z]?)\**$")


def cells(line):
    """Cells of a table row; an escaped `\\|` stays inside its cell."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return re.split(r"(?<!\\)\|", body)


def board_problems(root):
    path = os.path.join(root, BOARD)
    if not os.path.exists(path):
        return [], "no %s; nothing to parse" % BOARD
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    out, seen, width, in_fence = [], {}, None, False
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if in_fence or not line.lstrip().startswith("|"):
            width = None
            continue
        c = cells(line)
        if width is None:
            width = len(c)          # the header row of this table
            continue
        if all(re.fullmatch(r"\s*:?-{3,}:?\s*", x) for x in c):
            continue                # the separator row
        if len(c) != width:
            out.append("%s:%d: a row has %d cells against the %d its header declares"
                       % (BOARD, n, len(c), width))
        m = ROW_ID.match(c[0].strip()) if c else None
        if m:
            rid = m.group(1)
            if rid in seen:
                out.append("%s:%d: row id %s appears twice (first at line %d)" % (BOARD, n, rid, seen[rid]))
            else:
                seen[rid] = n
    return out, "%d row ids read" % len(seen)


def release_problems(root):
    path = os.path.join(root, RELEASE)
    if not os.path.exists(path):
        return [], "no %s; nothing to check" % RELEASE
    with open(path, encoding="utf-8") as fh:
        text = "\n".join(l for l in fh.read().split("\n") if not l.lstrip().startswith("#"))
    out = []
    if not re.search(r"fetch-depth:\s*0\b", text):
        out.append("%s: no `fetch-depth: 0`, so the tag's ancestry cannot be read" % RELEASE)
    if "merge-base --is-ancestor" not in text:
        out.append("%s: no `git merge-base --is-ancestor` check before publishing" % RELEASE)
    return out, "ancestry guard present" if not out else ""


def check(root):
    problems, notes = [], []
    for fn in (board_problems, release_problems):
        p, note = fn(root)
        problems += p
        if note:
            notes.append(note)
    return problems, notes


def self_test(root):
    caught = 0
    plants = [
        ("a bare pipe shifts a row", BOARD,
         "\n| id | Row | Status |\n|---|---|---|\n| PLANT-1 | a | b | open |\n"),
        ("an id appears twice", BOARD,
         "\n| id | Row | Status |\n|---|---|---|\n| PLANT-2 | a | open |\n| PLANT-2 | b | open |\n"),
        ("the ancestry check is gone", RELEASE, None),
    ]
    for name, rel, text in plants:
        with tempfile.TemporaryDirectory() as tmp:
            for sub in (BOARD, RELEASE):
                src = os.path.join(root, sub)
                if os.path.exists(src):
                    os.makedirs(os.path.dirname(os.path.join(tmp, sub)), exist_ok=True)
                    shutil.copy(src, os.path.join(tmp, sub))
            target = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if text is not None:
                with open(target, "a", encoding="utf-8") as fh:
                    fh.write(text)
            else:
                with open(target, "w", encoding="utf-8") as fh:
                    fh.write("on: push\njobs:\n  release:\n    steps:\n      - uses: actions/checkout@v4\n")
            problems, _ = check(tmp)
            if problems:
                caught += 1
                print("  caught  %s: %s" % (name, problems[-1]))
            else:
                print("  MISSED  %s" % name)
    print("family_gate self-test: %d of %d plants caught" % (caught, len(plants)))
    return 0 if caught == len(plants) else 2


def main(argv):
    root = os.getcwd()
    if "--self-test" in argv:
        return self_test(root)
    problems, notes = check(root)
    for p in problems:
        print("FAIL  " + p)
    print("family_gate: %s (%s)" % ("FAIL" if problems else "OK", "; ".join(notes)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
