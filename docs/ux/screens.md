# UI Screen Registry

<!-- Managed with super-ux (ux-contract v4). The UI map. -->

The UI map for super-ux's own installer. A "screen" here is one coherent
terminal view — a rendered list, a prompt, or a block of output.

Figma is **disabled** for this project (`foundation.md` → Design tooling):
the whole surface is a terminal.

## Index

| ID | Screen | Used by | Figma | Status | Coverage |
|----|--------|---------|-------|--------|----------|
| SCR-01 | Interactive multi-select list | FLW-01 | n/a | built | `bin/super-ux.js:338-399` |
| SCR-02 | Non-TTY numbered list + prompt | FLW-02 | n/a | built | `bin/super-ux.js:401-409` |
| SCR-03 | Project directory prompt | FLW-01, FLW-02 | n/a | built | `bin/super-ux.js:436-440` |
| SCR-04 | Install log | FLW-01, FLW-02, FLW-03 | n/a | built | `bin/super-ux.js:105-198` |
| SCR-05 | Skills CLI handoff | FLW-01, FLW-02 | n/a | built | `bin/super-ux.js:219-251` |
| SCR-06 | Claude plugin install output | FLW-01, FLW-02, FLW-03 | n/a | built | `bin/super-ux.js:264-281` |
| SCR-07 | Usage / help | FLW-04 | n/a | built | `bin/super-ux.js:71-98` |

## Design system

- **Style pack:** none — no visual layer. This project's interface is ANSI
  text, and inventing a palette for it would be exactly the drift the rule
  in `CLAUDE.md` forbids.
- **State vocabulary:** every file line begins with one of `install:`,
  `skip:`, `keep:`, `seed:`, `sync:`, `warning:`, `error:`, `refused:`. The
  word carries the meaning; colour never does.
- **Selection glyphs:** `◉` selected, `◯` not, `❯` cursor.

## Web surfaces

- **Web surfaces:** no

super-ux ships a terminal installer and a plugin. Its only public text lives in
the GitHub README, which is a *copy* surface (`docs/brand/channels.md` → landing
hero) and not a web surface this project routes: there is no path we choose, no
canonical we set and no markup we emit. The day a hosted page exists — docs, a
landing, pricing — this line flips to `yes` and every public screen takes its
five-field `Web surface:` block.

## Screens

### SCR-01: Interactive multi-select list
**Status:** built
**Used by:** FLW-01
**Coverage:** `bin/super-ux.js:338-399`

Three items, nothing preselected. Redraw moves the cursor up by
`items.length + 1` and clears each line, so the list updates in place.

| State | Shown | Frame |
|---|---|---|
| loading | not applicable — renders on first keypress registration | n/a |
| empty | not applicable — the item list is a constant | n/a |
| error | not applicable — no input can fail here; unknown keys are ignored | n/a |
| success | three rows plus the key hint line | n/a |

**Elements:** one row per item (`❯`/space, `◉`/`◯`, index, label); a hint
line reading `↑/↓ move · space/number toggle · a all · enter confirm · q quit`.
**Keys:** up/`k`, down/`j`, space, `1`–`9`, `a`, enter, `q`/esc/ctrl+c.
**Exit:** raw mode is restored and the keypress listener removed on every
exit path, including quit — a terminal left in raw mode is the worst thing a
CLI can leave behind.

### SCR-02: Non-TTY numbered list + prompt
**Status:** built
**Used by:** FLW-02
**Coverage:** `bin/super-ux.js:401-409`

| State | Shown | Frame |
|---|---|---|
| loading | not applicable | n/a |
| empty | empty input is a valid answer meaning "nothing" | n/a |
| error | `error: invalid selection '<input>'`, exit 1, nothing written | n/a |
| success | numbered list, then `Select [e.g. 1,3 \| all \| q]:` | n/a |

**Accepts:** `1,3` or `1 3`, `a`/`all`/`*`, empty/`q`/`quit`.
**Rejects:** anything non-integer or out of range — as a failure, never as a
silently narrowed selection.

### SCR-03: Project directory prompt
**Status:** built
**Used by:** FLW-01, FLW-02
**Coverage:** `bin/super-ux.js:436-440`

| State | Shown | Frame |
|---|---|---|
| loading | not applicable | n/a |
| empty | empty input means `.` — the default is in the prompt | n/a |
| error | an invalid path is reported by SCR-04, not here | n/a |
| success | `Cursor rules — project directory [.]: ` | n/a |

Asked **before** any install runs, so this prompt never interleaves with the
external skills-CLI picker's own output.

### SCR-04: Install log
**Status:** built
**Used by:** FLW-01, FLW-02, FLW-03
**Coverage:** `bin/super-ux.js:105-198`

One line per file. This screen is the whole answer to JTBD-02.

| State | Shown | Frame |
|---|---|---|
| loading | not applicable — output is synchronous and streamed | n/a |
| empty | `Nothing selected.` when the selection is empty | n/a |
| error | `error: '<path>' is not a directory`, exit 1, nothing written | n/a |
| success | per-file lines, then the `done:` summary | n/a |

**Degraded state:** a linter missing from the package payload prints a
`warning:` naming the file and the URL to get it, and the install continues.
Dying on an ENOENT after the rules are already on disk would leave a
half-installed project with a stack trace as its only record.

### SCR-05: Skills CLI handoff
**Status:** built
**Used by:** FLW-01, FLW-02
**Coverage:** `bin/super-ux.js:219-251`

| State | Shown | Frame |
|---|---|---|
| loading | the external picker owns the terminal until it exits | n/a |
| empty | not applicable | n/a |
| error | `warning: 'npx skills add …' missing\|failed` — never fatal | n/a |
| refused | `refused:` naming the installed plugin (spec from `installed_plugins.json`, or the marketplaces dir as fallback), the two `claude plugin` update commands, the family launcher, and `--force` as the override; exit 3, picker never launched, nothing written | n/a |
| success | a banner line, then the external picker's own output | n/a |

**Refused state, in full (SCN-016):** the handoff consults the target home's
`~/.claude/plugins/installed_plugins.json` before delegating, because the
skills CLI auto-detects Claude Code and writes the plain
`~/.claude/skills/super-ux` copy that shadows the installed plugin. A missing
or corrupt JSON reads as "no plugin" and the handoff proceeds — fail open,
never crash. Only this channel is gated: `--cursor` installs are untouched.

### SCR-06: Claude plugin install output
**Status:** built
**Used by:** FLW-01, FLW-02, FLW-03
**Coverage:** `bin/super-ux.js:264-281`

| State | Shown | Frame |
|---|---|---|
| loading | the `claude` CLI owns the terminal while it runs | n/a |
| empty | not applicable | n/a |
| error | install failure prints a `warning:` and the run continues | n/a |
| success | confirmation naming the scope, the restart, and `/ux` | n/a |

**Degraded state:** no `claude` binary → the two `/plugin` commands are
printed for the user to paste inside Claude Code. An already-added
marketplace is not an error and says so.

### SCR-07: Usage / help
**Status:** built
**Used by:** FLW-04
**Coverage:** `bin/super-ux.js:71-98`

| State | Shown | Frame |
|---|---|---|
| loading | not applicable | n/a |
| empty | not applicable | n/a |
| error | printed after `error: unknown mode '<arg>'`, then exit 1 | n/a |
| success | usage, the three menu items, and what each one writes | n/a |

What this screen claims item 2 writes must match what SCR-04 actually
writes. It drifted once and the audit of 2026-08-10 caught it.
