---
name: Bug report
about: The agent did something the contract says it shouldn't, or a command/linter broke
labels: bug
---

**What happened**

<!-- What the agent (or the CLI / linter) actually did. -->

**What should have happened**

<!-- Quote the file that says so — SKILL.md, a reference, a Cursor rule, the
contract. A quote beats a description. -->

**How to reproduce**

<!-- The command or prompt, and the state of docs/ux/ when it ran. -->

**Environment**

- Agent / channel: <!-- Claude Code plugin, Cursor rules, skills CLI, npx installer -->
- super-ux version: <!-- npm view super-ux version, or plugin.json -->
- OS / Python: <!-- python3 --version, if the linter or validator is involved -->

**Linter output** (if relevant)

```
python3 docs/ux/lint.py
```
