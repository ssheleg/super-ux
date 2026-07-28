# Security

## What this skill does on your machine

`super-ux` is documentation plus one small Python linter and one Node installer.
Nothing here is a service, and nothing runs on its own.

| Component | Runtime behavior |
|---|---|
| `plugins/super-ux/skills/**/SKILL.md`, `references/*.md` | Text. Read by the agent; executes nothing. |
| `plugins/super-ux/scripts/ux_lint.py` | Runs only when you or the agent invokes it. Python **standard library only** — no dependencies, no install step. Reads `docs/ux/` and your source tree, writes nothing. |
| `plugins/super-ux/commands/*.md`, `cursor/rules/*.mdc` | Text read by the host agent. |
| `templates/*.md` | Seed files copied into `docs/ux/` on first init. Never overwrite existing files. |
| `bin/super-ux.js` (npx installer) | Runs only when you invoke it. Copies the skill and rules into `~/.claude/` and/or `.cursor/`. Zero dependencies, no post-install script. |

There is no telemetry, no analytics and no phone-home. Nothing is transmitted
anywhere.

## What it executes

The installer spawns child processes with an explicit argument list — never a
shell string, so nothing in a config file can be interpreted as shell syntax:

- `claude --version` to detect whether Claude Code is present
- `claude plugin …` only when you asked for the plugin channel

`ux_lint.py` spawns nothing and opens no sockets.

## What it writes

Only inside the target you point it at: `docs/ux/` in your project, plus
`~/.claude/skills/`, `~/.claude/commands/` or `.cursor/` depending on the channel
you chose. It creates directories and copies files; it does not delete your work,
and initialization is incremental — existing layers are left untouched.

## What the skill will not do

The audit is **read-only by default**. It reports what the code does and where it
diverges from the scenario base, with `file:line` evidence. It does not rewrite
your source to make an audit pass, and it does not silently change user-facing
behavior to match a document — a mismatch is reported as a finding, and the fix
is your decision.

## Reporting a vulnerability

Do **not** open a public issue. Report privately through
[GitHub Security Advisories](https://github.com/ssheleg/super-ux/security/advisories/new),
or via the contacts on [sshlg.me](https://sshlg.me).

Include the version, your OS and agent, what you observed, and a reproduction if
you have one. Expect a first response within a few days. Fixes ship as a normal
tagged release with the issue described in `CHANGELOG.md`.

## Supported versions

The latest release on `main` is the supported one. There are no long-term support
branches — fixes go into the next tag.

## Verifying for yourself

```bash
git clone https://github.com/ssheleg/super-ux && cd super-ux
```

```bash
python3 test/validate.py
```

```bash
grep -rn "spawnSync\|execSync\|child_process\|urlopen\|fetch(" bin plugins
```

The last command returns the installer's two `claude` calls and nothing else.
