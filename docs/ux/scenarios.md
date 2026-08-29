# UX Scenarios

<!-- Managed with super-ux (ux-contract v4). Update in the same change as any user-facing behavior change. -->

The source of truth for what super-ux's own installer does. Every change to
`bin/super-ux.js` that a user can observe updates this file in the same
change.

## Index

| ID | Title | Feature | Persona | Traces | Status | Last audit |
|----|-------|---------|---------|--------|--------|------------|
| SCN-001 | Pick channels from the interactive list | install | P-01 | ST-001, FLW-01, SCR-01 | implemented | 2026-08-10 |
| SCN-002 | Quit the list without installing anything | install | P-01 | ST-001, FLW-01, SCR-01 | implemented | 2026-08-10 |
| SCN-003 | Confirm with nothing selected | install | P-01 | ST-001, FLW-01, SCR-04 | implemented | 2026-08-10 |
| SCN-004 | Select from piped stdin | install | P-02 | ST-002, FLW-02, SCR-02 | implemented | 2026-08-10 |
| SCN-005 | Reject an out-of-range selection | install | P-02 | ST-002, FLW-02, SCR-02 | implemented | 2026-08-10 |
| SCN-006 | Install into a project non-interactively | install | P-02 | ST-004, FLW-03, SCR-04 | implemented | 2026-08-10 |
| SCN-007 | Refuse a target that is not a directory | install | P-02 | ST-004, FLW-03, SCR-04 | implemented | 2026-08-10 |
| SCN-008 | Never overwrite an existing base | install | P-02 | ST-003, FLW-03, SCR-04 | implemented | 2026-08-10 |
| SCN-009 | Refresh rules and linters with --force | install | P-02 | ST-004, FLW-03, SCR-04 | implemented | 2026-08-10 |
| SCN-010 | Survive a linter missing from the payload | install | P-02 | ST-003, FLW-03, SCR-04 | implemented | 2026-08-10 |
| SCN-011 | Seeded project passes both linters | install | P-01 | ST-005, FLW-03, SCR-04 | implemented | 2026-08-10 |
| SCN-012 | Offer the routing block from either door | routing | P-02 | ST-006, FLW-01, FLW-03 | implemented | 2026-08-10 |
| SCN-013 | Install the Claude Code plugin without the CLI | install | P-01 | ST-001, FLW-01, SCR-06 | implemented | 2026-08-10 |
| SCN-014 | Read the help before running | install | P-02 | ST-007, FLW-04, SCR-07 | implemented | 2026-08-10 |
| SCN-015 | Reject an unknown flag | install | P-02 | ST-007, FLW-04, SCR-07 | implemented | 2026-08-10 |
| SCN-016 | Refuse the shadow the skills handoff would create | install | P-01 | ST-001, ST-003, FLW-01, FLW-02, SCR-05 | implemented | 2026-08-29 |
| SCN-017 | Be told how the next version arrives | install | P-01 | ST-006, FLW-01, FLW-02, FLW-03 | implemented | 2026-08-29 |

## Personas

See `foundation.md`: **P-01** solo builder shipping with an agent, **P-02**
multi-agent operator.

## Scenarios

### SCN-001: Pick channels from the interactive list
**Traces:** ST-001, FLW-01, SCR-01 · **Status:** implemented
**Preconditions:** stdin and stdout are both TTYs.
**Steps:**
1. User runs `npx super-ux` with no arguments → three rows render, all
   `◯`, cursor `❯` on the first, hint line beneath.
2. User presses `↓` → the cursor moves to row 2; nothing is selected.
3. User presses space → row 2 becomes `◉`.
4. User presses `2` → row 2 returns to `◯` (number keys toggle, they do not
   only select).
5. User presses `a` → all three become `◉`; pressing `a` again clears all.
6. User presses enter → the list stops rendering, raw mode is restored, and
   the selected installs run in order: cursor, claude, skills.
**Expected result:** the run installs exactly the selected channels, in that order,
and never leaves the terminal in raw mode.
**Errors & recovery:** an unrecognized key changes nothing and re-renders.
**Coverage:** `bin/super-ux.js:338-399`
**Product:** unobserved

### SCN-002: Quit the list without installing anything
**Traces:** ST-001, FLW-01, SCR-01 · **Status:** implemented
**Steps:**
1. User opens the list and selects two items.
2. User presses `q` (or esc, or ctrl+c).
**Expected result:** the selection is discarded, `Nothing selected.` prints, no
file is created or modified, raw mode is restored.
**Coverage:** `bin/super-ux.js:369-371`, `bin/super-ux.js:426-430`
**Product:** unobserved

### SCN-003: Confirm with nothing selected
**Traces:** ST-001, FLW-01, SCR-04 · **Status:** implemented
**Steps:**
1. User presses enter with every row `◯`.
**Expected result:** `Nothing selected.` and a clean exit. Not an error — choosing
nothing is a choice.
**Coverage:** `bin/super-ux.js:386-388`, `bin/super-ux.js:426-430`
**Product:** unobserved

### SCN-004: Select from piped stdin
**Traces:** ST-002, FLW-02, SCR-02 · **Status:** implemented
**Preconditions:** stdin is not a TTY.
**Steps:**
1. `echo "1,3" | npx super-ux` → the numbered list prints, then
   `Select [e.g. 1,3 | all | q]: `.
2. The buffered line `1,3` is consumed.
**Expected result:** items 1 and 3 install. `a`/`all`/`*` select everything; an
empty line, `q` or `quit` select nothing.
**Errors & recovery:** a line arriving between two questions is buffered by
the single persistent prompter rather than lost.
**Coverage:** `bin/super-ux.js:283-320`, `bin/super-ux.js:401-409`, `bin/super-ux.js:419-424`
**Product:** unobserved

### SCN-005: Reject an out-of-range selection
**Traces:** ST-002, FLW-02, SCR-02 · **Status:** implemented
**Steps:**
1. `echo "9" | npx super-ux`.
**Expected result:** `error: invalid selection '9'`, exit 1, nothing written. The
selection is never silently narrowed to the valid subset — a user who typed
`1,9` meant both.
**Coverage:** `bin/super-ux.js:322-336`, `bin/super-ux.js:407`
**Product:** unobserved

### SCN-006: Install into a project non-interactively
**Traces:** ST-004, FLW-03, SCR-04 · **Status:** implemented
**Steps:**
1. `npx super-ux --cursor ./proj` on an empty directory.
**Expected result:** every `.mdc` rule copied to `.cursor/rules/` with an
`install:` line; `docs/ux/{scenarios,foundation,flows,screens,README}.md`
seeded with `seed:` lines; `docs/ux/{audits,plans}/` created;
`docs/brand/{README,voice,terminology,facts,channels,strings}.md` and
`locales/en.md` seeded; `docs/ux/lint.py`, `docs/ux/doctor.py` and
`docs/brand/lint.py` written with `sync:` lines; a closing `done:` line
counting rules installed, rules skipped and documents seeded.
`docs/ux/vision.md` is **not** created.
**Coverage:** `bin/super-ux.js:105-198`, `bin/super-ux.js:510-512`
**Product:** unobserved

### SCN-007: Refuse a target that is not a directory
**Traces:** ST-004, FLW-03, SCR-04 · **Status:** implemented
**Steps:**
1. `npx super-ux --cursor ./README.md`.
**Expected result:** `error: './README.md' is not a directory`, exit 1, and no file
created anywhere — the check runs before the first write.
**Coverage:** `bin/super-ux.js:106-108`
**Product:** unobserved

### SCN-008: Never overwrite an existing base
**Traces:** ST-003, FLW-03, SCR-04 · **Status:** implemented
**Preconditions:** the target already has `docs/ux/scenarios.md` with real
content and one `.cursor/rules/*.mdc`.
**Steps:**
1. `npx super-ux --cursor ./proj` without `--force`.
**Expected result:** `keep:` for every existing document, `skip:` for the existing
rule with the hint `(use --force to overwrite)`, and both files byte-identical
afterwards. Content the user wrote is never a casualty of an install.
**Coverage:** `bin/super-ux.js:121-124`, `bin/super-ux.js:135-143`
**Product:** unobserved

### SCN-009: Refresh rules and linters with --force
**Traces:** ST-004, FLW-03, SCR-04 · **Status:** implemented
**Steps:**
1. `npx super-ux --cursor ./proj --force` on a project installed from an
   older release.
**Expected result:** every rule file replaced (`install:`), all three linters
re-synced (`sync:`), and every seeded document still reported `keep:`.
`--force` is about code, never about content.
**Coverage:** `bin/super-ux.js:510`, `bin/super-ux.js:122-128`, `bin/super-ux.js:175-190`
**Product:** unobserved

### SCN-010: Survive a linter missing from the payload
**Traces:** ST-003, FLW-03, SCR-04 · **Status:** implemented
**Preconditions:** the published package omits a script (a `files[]`
regression — this has happened in this family).
**Steps:**
1. `npx super-ux --cursor ./proj`.
**Expected result:** `warning:` naming the script, the destination it did not
reach, and the URL to fetch it; the rest of the install completes and exits
normally. A half-installed project with a stack trace as its only record is
worse than a named gap.
**Coverage:** `bin/super-ux.js:181-189`
**Product:** unobserved

### SCN-011: Seeded project passes both linters
**Traces:** ST-005, FLW-03, SCR-04 · **Status:** implemented
**Steps:**
1. Seed a fresh project.
2. Run `python3 docs/ux/lint.py`.
3. Run `python3 docs/brand/lint.py`.
**Expected result:** both exit 0. A first run that greets the user with errors
about the templates teaches them to ignore the linter, which is the one
habit this product cannot survive.
**Coverage:** `bin/super-ux.js:135-167`, `templates/scenarios.md`, `templates/screens.md`
**Product:** unobserved

### SCN-012: Offer the routing block from either door
**Traces:** ST-006, FLW-01, FLW-03 · **Status:** implemented
**Steps:**
1. Finish an install via the interactive menu.
2. Finish an install via `--cursor`.
**Expected result:** both paths call the launcher for this member. When the
launcher is unavailable, both print the same one-line command, in English,
matching the rest of the CLI. Two doors into one install must not behave
differently — they did until 2026-08-10.
**Coverage:** `bin/super-ux.js:453`, `bin/super-ux.js:472-486`, `bin/super-ux.js:513`
**Product:** unobserved

### SCN-013: Install the Claude Code plugin without the CLI
**Traces:** ST-001, FLW-01, SCR-06 · **Status:** implemented
**Preconditions:** no `claude` binary on PATH.
**Steps:**
1. Select the Claude Code plugin item and confirm.
**Expected result:** the two `/plugin` commands print for the user to paste inside
Claude Code, and the run continues to the remaining selections rather than
failing.
**Errors & recovery:** an already-added marketplace prints
`(marketplace may already be added — continuing)`; a failed install prints a
`warning:` and never aborts the other channels.
**Coverage:** `bin/super-ux.js:264-281`
**Product:** unobserved

### SCN-014: Read the help before running
**Traces:** ST-007, FLW-04, SCR-07 · **Status:** implemented
**Steps:**
1. `npx super-ux --help` (or `-h`).
**Expected result:** usage prints, listing the three menu items and, for the Cursor
item, every category it writes — rules, the `docs/ux` skeleton, the
`docs/brand` pack, all three linters, and that `vision.md` is not seeded.
Exit 0, nothing written.
**Coverage:** `bin/super-ux.js:71-98`, `bin/super-ux.js:490-493`
**Product:** unobserved

### SCN-015: Reject an unknown flag
**Traces:** ST-007, FLW-04, SCR-07 · **Status:** implemented
**Steps:**
1. `npx super-ux --instal`.
**Expected result:** `error: unknown mode '--instal'`, then the full usage, then
exit 1. The error names what was typed, and the recovery is on the screen.
**Coverage:** `bin/super-ux.js:505-509`
**Product:** unobserved

### SCN-016: Refuse the shadow the skills handoff would create
**Traces:** ST-001, ST-003, FLW-01, FLW-02, SCR-05 · **Status:** implemented
**Preconditions:** super-ux is installed as a Claude Code plugin — declared in
`~/.claude/plugins/installed_plugins.json` under `super-ux@<any marketplace>`,
or, as the fallback signal only, a `plugins/marketplaces/super-ux` directory.
**Steps:**
1. Select the skills item (`echo "1" | npx super-ux`, or item 1 in the menu).
**Expected result:** `refused:` naming what was found — the plugin spec read from
the JSON, or the marketplace directory — then why: the skills CLI
auto-detects Claude Code and would write a plain `~/.claude/skills/super-ux`
copy that shadows the plugin and serves the version it was copied from
forever. The remedy is in the refusal: both `claude plugin` update commands
carrying the real spec from the JSON, the family launcher, and `--force` as
the named override. Exit 3, the skills CLI never invoked, nothing written.
The check gates the Claude Code channel alone: `--cursor` still installs
into a project beside the plugin.
**Errors & recovery:** a missing or unparsable `installed_plugins.json` reads
as "no plugin" and the handoff proceeds — the fresh HOME is the common case,
and an installer that crashes on a parse error refuses the machines that
need it most. `npx super-ux --force` runs the picker anyway, recording the
two-channel choice instead of letting it happen by accident.
**Coverage:** `bin/super-ux.js:44-63`, `bin/super-ux.js:219-251`, `bin/super-ux.js:454-458`
**Product:** unobserved

### SCN-017: Be told how the next version arrives
**Traces:** ST-006, FLW-01, FLW-02, FLW-03 · **Status:** implemented
**Steps:**
1. Finish an install via the menu (any selection).
2. Finish an install via `--cursor`.
**Expected result:** both paths end with the same `Updates:` block naming the two
ways the next version arrives — `npx super-ux@latest` for this member and
the family launcher for every channel at once. An installer that never
mentions updates has still chosen an update model: never. The refused path
prints no `Updates:` block — its refusal already carries the update
commands, and repeating them under it would bury the remedy.
**Coverage:** `bin/super-ux.js:255-262`, `bin/super-ux.js:454-460`, `bin/super-ux.js:514`
**Product:** unobserved
