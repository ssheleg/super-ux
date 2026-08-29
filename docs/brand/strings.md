Contract: brand-contract v1

# Interface strings

A **decision registry**, not a message catalog. It holds no translations and
does not replace i18n keys. It records which strings have been reconciled
with the voice, which scenario each serves, and where each one lives.

This is what makes "one action, two names" (`B020`) checkable at all. Without
it, that defect is only findable by reading the entire interface, which is
why it survives in every product that has not written one down.

super-ux's whole interface is `bin/super-ux.js`. The `Text` column holds the
literal **exactly as it appears in the source**, escape sequences included,
that is what makes `B021` (registry says one thing, code says another) a
check rather than a guess. A literal pipe is written `\|`, as markdown
requires.

| Key | Text (primary) | Location | Scenario | Status |
|---|---|---|---|---|
| help.title | super-ux installer | bin/super-ux.js:72 | SCN-014 | agreed |
| menu.item.skills | Skills for any AI agent (Claude Code, Codex, Cursor, 70+; opens agent picker) | bin/super-ux.js:66 | SCN-001 | agreed |
| menu.item.cursor | Cursor rules + docs/ux skeleton + docs/brand pack + linters, into a project | bin/super-ux.js:67 | SCN-001 | agreed |
| menu.item.claude | Claude Code plugin (skills + /ux commands, user-global) | bin/super-ux.js:68 | SCN-001 | agreed |
| help.usage.claude.install | claude plugin install | bin/super-ux.js:96 | SCN-014 | agreed |
| handoff.skills | \n--- Skills for any agent: delegating to the skills CLI picker --- | bin/super-ux.js:247 | SCN-001 | agreed |
| handoff.claude | \n--- Claude Code plugin --- | bin/super-ux.js:265 | SCN-013 | agreed |
| claude.marketplace.exists | (marketplace may already be added, continuing) | bin/super-ux.js:274 | SCN-013 | agreed |
| claude.installed | Claude Code plugin installed (scope: user). Restart sessions to pick it up; then run /ux in any project. | bin/super-ux.js:277 | SCN-013 | agreed |
| warning.plugin.install | warning: claude plugin install failed, see output above | bin/super-ux.js:279 | SCN-013 | agreed |
| menu.hint.keys | \x1b[2K  ↑/↓ move · space/number toggle · a all · enter confirm · q quit\n | bin/super-ux.js:355 | SCN-001 | agreed |
| menu.select.prompt | Select [e.g. 1,3 \| all \| q]:  | bin/super-ux.js:405 | SCN-004 | agreed |
| menu.intro | super-ux: scenario-driven UI development. Select what to install:\n | bin/super-ux.js:412 | SCN-001 | agreed |
| menu.nothing | Nothing selected | bin/super-ux.js:428 | SCN-003 | agreed |
| prompt.cursor.dir | Cursor rules, project directory [.]:  | bin/super-ux.js:439 | SCN-006 | agreed |
| routers.offer.1 | \nTo have these skills apply by default in every project, add the\n | bin/super-ux.js:481 | SCN-012 | agreed |
| routers.offer.2 | family's routing block to your agent's global instructions:\n\n | bin/super-ux.js:482 | SCN-012 | agreed |
| routers.offer.command |   npx --yes sshlg-skills routers --member super-ux\n | bin/super-ux.js:483 | SCN-012 | agreed |
| help.exit.refused |   3 refused: the super-ux PLUGIN is installed in this home, and the skills | bin/super-ux.js:81 | SCN-014 | agreed |
| refuse.shadow | refused: super-ux is already ${found}.\n | bin/super-ux.js:230 | SCN-016 | agreed |
| refuse.shadow.found.json |          (declared in ~/.claude/plugins/installed_plugins.json) | bin/super-ux.js:227 | SCN-016 | agreed |
| refuse.shadow.reason |          The skills CLI auto-detects Claude Code and would write a plain copy\n | bin/super-ux.js:231 | SCN-016 | agreed |
| refuse.shadow.reason.2 |          to ~/.claude/skills/super-ux, which shadows the plugin and serves the\n | bin/super-ux.js:232 | SCN-016 | agreed |
| refuse.shadow.reason.3 |          version it was copied from forever. Update the plugin channel instead:\n | bin/super-ux.js:233 | SCN-016 | agreed |
| refuse.shadow.remedy.marketplace |            claude plugin marketplace update super-ux\n | bin/super-ux.js:234 | SCN-016 | agreed |
| refuse.shadow.remedy.launcher.label |          Family launcher (updates every member, prunes shadow copies):\n | bin/super-ux.js:236 | SCN-016 | agreed |
| refuse.shadow.remedy.launcher |            npx --yes sshlg-skills@latest update\n | bin/super-ux.js:237 | SCN-016 | agreed |
| refuse.shadow.override |          Pass --force (npx super-ux --force) to run the picker anyway: a\n | bin/super-ux.js:238 | SCN-016 | agreed |
| refuse.shadow.override.2 |          deliberate choice to run two channels, where the stale one wins. | bin/super-ux.js:239 | SCN-016 | agreed |
| updates.how | \nUpdates: rerun npx super-ux@latest (--cursor <dir> --force refreshes a\n | bin/super-ux.js:257 | SCN-017 | agreed |
| updates.how.2 | project's rules and linters), or refresh the whole family with\n | bin/super-ux.js:258 | SCN-017 | agreed |
| updates.launcher | npx --yes sshlg-skills@latest update (every channel, and it prunes plain\n | bin/super-ux.js:259 | SCN-017 | agreed |
| updates.launcher.2 | copies that would shadow a plugin). | bin/super-ux.js:260 | SCN-017 | agreed |

## Columns

- **Key.** Dot-separated, stable, names the action rather than the screen.
  Two rows sharing a `Key` with different `Text` is `B020`.
- **Text (primary).** The string in the primary locale, verbatim. Other
  locales live in the project's own i18n files; parity is computed against
  this column.
- **Location.** `file:line`. A location that no longer resolves is `B023`.
- **Scenario.** The `SCN-NNN` this string serves. A string serving no
  scenario is a question for `ux-scenarios`, not a copy problem.
- **Status.** `agreed` · `proposed` · `drifted` · `orphan`.

## The word prefix is the vocabulary

`install:` · `skip:` · `keep:` · `seed:` · `sync:` · `warning:` · `error:` ·
`refused:`. One fate per file, one word per fate, and the word never changes
meaning between two lines of the same run. If a run ever reports `keep:` for
something it overwrote, this registry is what proves the string lied.
`refused:` is the loud one on purpose: it means a requested channel was not
installed, why, and what to run instead — a refusal that exits 0 reads as
success to every script above it.

## Not registered, and why

- **Interpolated messages,** `install: ${dst}`, `error: unknown mode
  '${args[0]}'`, the `done:` summary. Their invariant half is the word
  prefix above; the rest is a path or an argument the user just typed. A row
  holding `error: unknown mode '…'` would never match the source and would
  turn `B021` into permanent noise.
- **The usage block's option table,** the four `Usage:` lines in `usage()`.
  Until 2026-08-20 the whole block was unregistered for a reason that was not
  a decision: the literal extractor could not cross a newline, so a multi-line
  template literal was invisible to `B022` and nothing here had to be argued.
  It is visible now — the block's title line is registered above — and the
  option table deliberately is not. A column-aligned table of flags is layout,
  not language: its `Text` cell would carry a 34-space run and a registry of
  layouts is a registry nobody reads. `B022` warns about it on every run, and
  that standing warning is the honest state of a help screen nobody has agreed
  — it is the finding, not noise. Its contents stay governed by SCN-014. The
  exit-codes table added for the refusal (SCN-016) is the same case: its one
  sentence of language is registered above as `help.exit.refused`, the aligned
  columns are not.
- **ANSI control sequences and the selection glyphs** `◉` `◯` `❯`, which
  carry state, not language, and are specified in `docs/ux/screens.md` →
  Design system, where changing them is a UI decision rather than a copy
  decision.
