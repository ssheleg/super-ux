Contract: brand-contract v1

# Interface strings

A **decision registry**, not a message catalog. It holds no translations and
does not replace i18n keys. It records which strings have been reconciled
with the voice, which scenario each serves, and where each one lives.

This is what makes "one action, two names" (`B020`) checkable at all. Without
it, that defect is only findable by reading the entire interface — which is
why it survives in every product that has not written one down.

super-ux's whole interface is `bin/super-ux.js`. The `Text` column holds the
literal **exactly as it appears in the source**, escape sequences included —
that is what makes `B021` (registry says one thing, code says another) a
check rather than a guess. A literal pipe is written `\|`, as markdown
requires.

| Key | Text (primary) | Location | Scenario | Status |
|---|---|---|---|---|
| menu.item.skills | Skills for any AI agent (Claude Code, Codex, Cursor, 70+ — opens agent picker) | bin/super-ux.js:22 | SCN-001 | agreed |
| menu.item.cursor | Cursor rules + docs/ux skeleton + docs/brand pack + linters, into a project | bin/super-ux.js:23 | SCN-001 | agreed |
| menu.item.claude | Claude Code plugin (skills + /ux commands, user-global) | bin/super-ux.js:24 | SCN-001 | agreed |
| help.usage.claude.install | claude plugin install | bin/super-ux.js:45 | SCN-014 | agreed |
| handoff.skills | \n--- Skills for any agent: delegating to the skills CLI picker --- | bin/super-ux.js:156 | SCN-001 | agreed |
| handoff.claude | \n--- Claude Code plugin --- | bin/super-ux.js:162 | SCN-013 | agreed |
| claude.marketplace.exists | (marketplace may already be added — continuing) | bin/super-ux.js:171 | SCN-013 | agreed |
| claude.installed | Claude Code plugin installed (scope: user). Restart sessions to pick it up; then run /ux in any project. | bin/super-ux.js:174 | SCN-013 | agreed |
| warning.plugin.install | warning: claude plugin install failed — see output above | bin/super-ux.js:176 | SCN-013 | agreed |
| menu.hint.keys | \x1b[2K  ↑/↓ move · space/number toggle · a all · enter confirm · q quit\n | bin/super-ux.js:252 | SCN-001 | agreed |
| menu.select.prompt | Select [e.g. 1,3 \| all \| q]:  | bin/super-ux.js:302 | SCN-004 | agreed |
| menu.intro | super-ux — scenario-driven UI development. Select what to install:\n | bin/super-ux.js:309 | SCN-001 | agreed |
| menu.nothing | Nothing selected. | bin/super-ux.js:325 | SCN-003 | agreed |
| prompt.cursor.dir | Cursor rules — project directory [.]:  | bin/super-ux.js:336 | SCN-006 | agreed |
| routers.offer.1 | \nTo have these skills apply by default in every project, add the\n | bin/super-ux.js:368 | SCN-012 | agreed |
| routers.offer.2 | family's routing block to your agent's global instructions:\n\n | bin/super-ux.js:369 | SCN-012 | agreed |
| routers.offer.command |   npx --yes sshlg-skills routers --member super-ux\n | bin/super-ux.js:370 | SCN-012 | agreed |

## Columns

- **Key** — dot-separated, stable, names the action rather than the screen.
  Two rows sharing a `Key` with different `Text` is `B020`.
- **Text (primary)** — the string in the primary locale, verbatim. Other
  locales live in the project's own i18n files; parity is computed against
  this column.
- **Location** — `file:line`. A location that no longer resolves is `B023`.
- **Scenario** — the `SCN-NNN` this string serves. A string serving no
  scenario is a question for `ux-scenarios`, not a copy problem.
- **Status** — `agreed` · `proposed` · `drifted` · `orphan`.

## The word prefix is the vocabulary

`install:` · `skip:` · `keep:` · `seed:` · `sync:` · `warning:` · `error:`.
One fate per file, one word per fate, and the word never changes meaning
between two lines of the same run. If a run ever reports `keep:` for
something it overwrote, this registry is what proves the string lied.

## Not registered, and why

- **Interpolated messages** — `install: ${dst}`, `error: unknown mode
  '${args[0]}'`, the `done:` summary. Their invariant half is the word
  prefix above; the rest is a path or an argument the user just typed. A row
  holding `error: unknown mode '…'` would never match the source and would
  turn `B021` into permanent noise.
- **The usage block** — a multi-line template literal in `usage()`. Its
  wording is governed by SCN-014, which states what it must contain.
- **ANSI control sequences and the selection glyphs** `◉` `◯` `❯` — they
  carry state, not language, and are specified in `docs/ux/screens.md` →
  Design system, where changing them is a UI decision rather than a copy
  decision.
