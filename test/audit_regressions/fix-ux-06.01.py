#!/usr/bin/env python3
"""FIX-UX-06.01 — the alignment rule lands in the file the active host reads
(sherlock audit, UX-06).

The finding: step 4 listed files by agent, then created CLAUDE.md when all were
absent; the linter was satisfied by ANY of the three files carrying the rule
and never checked whether the current host reads it. So a Codex project (reads
AGENTS.md) could pass with the rule only in CLAUDE.md.

The fix under test (vision SKILL.md + scripts/ux_lint.py):
* host capability decides the default target (Codex→AGENTS.md,
  Claude→CLAUDE.md, Gemini→GEMINI.md), detected by marker dir; an explicit
  project target takes priority;
* the linter checks the rule against the ACTIVE host's file, not any file;
* empty Codex/Claude/Gemini fixtures resolve to AGENTS/CLAUDE/GEMINI;
* a repeat is idempotent; mixed-host gets each target.

Standard library only.
"""
import importlib.util
import os
import sys
import tempfile

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LINT = os.path.join(ROOT, "plugins", "super-ux", "scripts", "ux_lint.py")
VISION = os.path.join(ROOT, "plugins", "super-ux", "skills", "vision", "SKILL.md")

_spec = importlib.util.spec_from_file_location("ux_lint", LINT)
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

failures = []


def case(name, fn):
    try:
        fn()
        print(f"  ok  {name}")
    except AssertionError as e:
        failures.append(f"{name}: {e}")
        print(f"FAIL  {name}: {e}")


from pathlib import Path


def t_host_target_map():
    assert M.HOST_TARGET == {"claude": "CLAUDE.md", "codex": "AGENTS.md",
                             "gemini": "GEMINI.md"}


def t_active_host_by_marker():
    for host, marker in (("codex", ".codex"), ("gemini", ".gemini"),
                         ("claude", ".claude")):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, marker))
        assert M.active_hosts(Path(d)) == [host], f"{marker} did not resolve to {host}"


def t_default_is_claude_when_undetectable():
    d = tempfile.mkdtemp()
    assert M.active_hosts(Path(d)) == ["claude"]


def t_empty_fixtures_resolve_targets():
    # the expected-result mapping: empty Codex/Claude/Gemini → AGENTS/CLAUDE/GEMINI
    for marker, target in ((".codex", "AGENTS.md"), (".claude", "CLAUDE.md"),
                           (".gemini", "GEMINI.md")):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, marker))
        host = M.active_hosts(Path(d))[0]
        assert M.HOST_TARGET[host] == target


def t_mixed_host_lists_all():
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, ".codex"))
    os.makedirs(os.path.join(d, ".claude"))
    hosts = set(M.active_hosts(Path(d)))
    assert hosts == {"codex", "claude"}, f"mixed host not both: {hosts}"


def t_vision_doc_is_host_first():
    with open(VISION, encoding="utf-8") as fh:
        d = " ".join(fh.read().split())
    assert "the file the running HOST actually reads" in d
    assert "decide the target by host capability FIRST" in d
    assert "Never hardcode `CLAUDE.md`" in d
    assert "mixed-host" in d


def t_lint_checks_active_host_not_any():
    with open(LINT, encoding="utf-8") as fh:
        s = fh.read()
    assert "ACTIVE HOST reads" in s, "the lint does not scope to the active host"
    assert "active_hosts(root)" in s
    # U032 (no file for the active host) and U033 (file present, no rule) stay distinct
    assert "the active host has no instruction file" in s
    assert "nothing the running host reads ever sees the vision" in s


def main():
    case("HOST_TARGET maps each host to its file", t_host_target_map)
    case("the active host is detected by its marker dir", t_active_host_by_marker)
    case("the default is claude when undetectable", t_default_is_claude_when_undetectable)
    case("empty codex/claude/gemini fixtures resolve AGENTS/CLAUDE/GEMINI",
         t_empty_fixtures_resolve_targets)
    case("a mixed-host project lists all active hosts", t_mixed_host_lists_all)
    case("vision step 4 is host-first, never hardcoded CLAUDE.md",
         t_vision_doc_is_host_first)
    case("the linter checks the active host's file, not any file",
         t_lint_checks_active_host_not_any)
    if failures:
        print(f"\n{len(failures)} failure(s)")
        return 1
    print("\nall green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
