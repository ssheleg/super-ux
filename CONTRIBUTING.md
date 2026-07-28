# Contributing to super-ux

Thanks for looking. This repo is a **content repo**: almost everything an
agent reads is markdown, and the only executable parts are a zero-dependency
installer CLI, a stdlib linter that ships into your projects, and a stdlib
validator that keeps the whole thing honest.

## Repo layout

```
plugins/super-ux/
  skills/<skill>/SKILL.md        the four agent skills
  skills/<skill>/references/     each skill's OWN copy of the contracts it links
  skills/references/             the SOURCE OF TRUTH for those contracts
  commands/*.md                  the /ux slash commands
  scripts/ux_lint.py             the linter seeded into target projects
cursor/rules/*.mdc               the same methodology for Cursor
templates/                       what gets seeded into a project's docs/ux/
bin/super-ux.js                  the npx installer (zero dependencies)
install.sh                       POSIX fallback for the Cursor channel
test/validate.py                 the test suite (stdlib only)
test/sync_references.py          regenerates the per-skill contract copies
```

**Why the contracts are duplicated:** the skills CLI ships only a skill's own
directory, so a sibling `skills/references/` arrives dangling on every
non-Claude agent. `skills/references/` is the source of truth; the per-skill
copies are generated and must stay byte-identical. Never edit a copy by hand.

## The loop

```sh
# 1. edit
# 2. if you touched plugins/super-ux/skills/references/:
python3 test/sync_references.py
# 3. always:
python3 test/validate.py
```

`validate.py` is the gate CI runs on every push and PR. It checks manifests
and the four-way version sync, skill/command/rule front-matter and the
description canon, template presence, the shipped contract copies, that every
asset the installer copies is covered by `package.json` `files[]`, that the
hard rule embedded in `/ux-rule` matches `templates/claude-rule.md`, that
`CHANGELOG.md` has no duplicate release headings, and that every relative
markdown link resolves.

If you add a rule to the methodology, add the check that fails when someone
breaks it. A prose rule nobody can verify is a suggestion.

## Conventions

- **English** for everything agent-facing. Skill descriptions follow the
  canon: they open with `Use when`, pair each Russian trigger beside its
  English equivalent, and keep front-matter under 1024 characters.
- **One owner per fact.** A field, a rule, or a path is defined in exactly one
  file and referenced everywhere else. Two definitions is drift with a delay
  fuse — several past bugs were exactly this.
- **Line width ~78** in markdown, so diffs stay readable.
- **Stable IDs, never reused** (`SCN-NNN`, `FLW-NN`, `SCR-NN`, `ST-NNN`,
  `BP-NNN`, `PRN-NN`). Retired entries stay with a reason.
- Adding a practice to `best-practices.md`: next free `BP-NNN`, one practice
  per entry, `Do` / `Why` / `Apply when` / `Tags` / `Source`, tags from the
  taxonomy at the top of the file, under ~6 lines. Then wire it into
  `practice-selection.md` so it actually gets pulled by something.

## Testing a change end-to-end

The repo is not the artifact — test what a user actually installs:

```sh
# npm channel, from a packed tarball in a temp dir (never the working tree)
npm pack && mkdir -p /tmp/t && tar xzf super-ux-*.tgz -C /tmp/t
mkdir /tmp/t/proj && node /tmp/t/package/bin/super-ux.js --cursor /tmp/t/proj

# the seeded project must lint clean from the first second
cd /tmp/t/proj && python3 docs/ux/lint.py
```

## Releasing (maintainer)

1. Bump the version in **four** places — `package.json`,
   `.claude-plugin/marketplace.json`, `plugins/super-ux/.claude-plugin/plugin.json`,
   and a new `## x.y.z — YYYY-MM-DD` section in `CHANGELOG.md`. The validator
   fails if they disagree.
2. `python3 test/validate.py` green, commit, push.
3. Tag `vX.Y.Z` and push the tag. The release workflow (armed by the
   `RELEASE_ENABLED` repo variable) validates, checks the tag against the
   manifests, creates the GitHub release from that CHANGELOG section, and
   smoke-tests `npx` from a clean cwd.
4. `npm publish` — a deliberate human step (2FA).
5. Refresh local installs: the two commands in the README's
   "Keeping installs current".

## Reporting problems

Open an issue with the agent and channel you used (Claude Code plugin, Cursor
rules, skills CLI, npx), the version (`npm view super-ux version` or
`plugin.json`), and what the agent did versus what the contract says it should
have done. A quote from the file it got wrong is worth more than a
description.
