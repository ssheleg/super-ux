# UX Foundation

<!-- Managed with super-ux (ux-contract v4). The WHY layer. -->

The WHY layer for **super-ux's own user-facing surface**: the installer CLI
(`bin/super-ux.js`) and its interactive menu. The skills and commands are
read by agents, not operated by humans; the installer is the one place a
person types something.

Traces up to `vision.md`. Nothing here may contradict its anti-vision.

## Personas

### P-01: Solo builder shipping with an agent
Runs Claude Code or Cursor on their own product. Comfortable in a terminal,
impatient with setup. Found super-ux from a README or a post; has thirty
seconds of patience before deciding it is not worth it. Does not know — and
must never need to know — what a "skill", a "layer" or a "contract version"
is. **Status:** confirmed

### P-02: Multi-agent operator
Runs several agents across many repositories (Claude Code, Cursor, Codex,
opencode). Cares about one thing the solo builder does not: whether a
channel is current, and whether two channels are serving different versions
of the same skill. Reads `--help` before running anything. **Status:**
confirmed

## Jobs to Be Done

### JTBD-01
When I start letting an agent write my UI, I want a written model of what
the product should do, so I stop re-explaining it every prompt and stop
finding rewritten screens I already approved. **Forces:** push — silent
rewrites; pull — a file the agent must read; anxiety — "another process to
maintain"; habit — prompting and hoping. **Status:** confirmed

### JTBD-02
When I install a dev tool, I want to know exactly what it put on my disk and
that it did not overwrite my work, so I can undo it and keep trusting it.
**Forces:** push — tools that scatter files; pull — an itemized log; anxiety
— clobbering an existing base; habit — reading the diff afterwards.
**Status:** confirmed

### JTBD-03
When I run several agents, I want one command that brings every channel to
the same version, so I never debug a difference that is only a stale copy.
**Forces:** push — a shadowing plain copy serving a frozen version; pull —
one launcher; anxiety — half-updated state; habit — updating whichever
channel broke. **Status:** confirmed

## Customer journeys

### JRN-01: First install
| Stage | Action | Touchpoint | Emotion | Pain | Opportunity |
|---|---|---|---|---|---|
| Discover | reads the README | GitHub / npm | 3 | unclear which channel is theirs | one Quick start per agent |
| Decide | picks a channel | README | 3 | three install paths, no default | interactive menu that asks |
| Install | runs `npx super-ux` | CLI menu | 4 | none if the menu is legible | multi-select, nothing preselected |
| Confirm | reads the output | CLI log | 4 | "did it touch my files?" | one line per file, `keep:` for skips |
| Continue | runs `/ux` | agent | 5 | none | the entry point takes over |

### JRN-02: Refresh after a release
| Stage | Action | Touchpoint | Emotion | Pain | Opportunity |
|---|---|---|---|---|---|
| Notice | sees a new version | npm / release | 3 | no signal in-product | version in `--help` |
| Update | runs the family launcher | CLI | 4 | a bare `skills update` shadows the plugin | README names the one safe command |
| Verify | re-runs `--cursor --force` | CLI | 4 | fear of losing the base | `keep:` proves it was untouched |

## Monetization

None. MIT, no paid tier, no telemetry, no hosted component — see the
anti-vision, which refuses the hosted service that would create one.

## Product mechanics

- **Personalization:** none. The installer holds no state between runs.
- **Engagement:** none by design. The CLI is used at most a few times per
  project; anything that rewards repeat visits would be a defect.
- **Accessibility regime:** the interactive list requires a TTY. Every path
  it offers is reachable without one — `selectFallback` on piped stdin, and
  `--cursor` with no prompt at all. Colour is never the only signal: state
  is carried by `◉`/`◯` and by the `install:` / `skip:` / `keep:` / `sync:`
  word prefix.

## Design tooling

- **Figma:** disabled
- **Reason:** the entire surface is a terminal. There is no frame to draw,
  and a Figma file for ANSI output would be a record nobody could keep true.
- **Style pack:** not applicable — no visual layer. See
  `screens.md` → Design system.

## User stories

### ST-001: Choose what to install, in plain words
As P-01, I want to pick which channels to install from a list, so that I do
not have to learn three commands to try the tool.
**Priority:** must
**Acceptance criteria:**
- Given a TTY, when I run `npx super-ux` with no arguments, then a
  multi-select list appears with nothing preselected.
- Given the list, when I press `a`, then every item toggles on; pressing `a`
  again toggles them all off.
- Given the list, when I press enter with nothing selected, then the tool
  exits saying nothing was selected and writes no files.
**Kill criteria:** if the menu is the reason installs fail, replace it with
three documented one-liners.
**Status:** delivered
**Product:** unobserved

### ST-002: Install without a terminal that can do raw mode
As P-02, I want the menu to work when stdin is piped, so that I can install
from a script or a Dockerfile.
**Priority:** must
**Acceptance criteria:**
- Given piped stdin, when I run `npx super-ux`, then a numbered list prints
  and a `Select [e.g. 1,3 | all | q]:` prompt reads one line.
- Given the input `1,3`, when it is parsed, then items 1 and 3 are selected.
- Given input naming an item that does not exist, then the run fails with
  `error: invalid selection '<input>'` and writes nothing.
**Status:** delivered
**Product:** unobserved

### ST-003: See exactly what was written
As P-02, I want one line per file with its fate, so that I can tell an
install from an overwrite without reading a diff.
**Priority:** must
**Acceptance criteria:**
- Given an existing rule file and no `--force`, then the line reads
  `skip:` and the file is byte-identical afterwards.
- Given an existing `scenarios.md`, then the line reads `keep:` and the file
  is never overwritten, with or without `--force`.
- Given the run finishes, then the closing line counts rules, skips and
  seeded documents — not one of the three.
**Status:** delivered
**Product:** unobserved

### ST-004: Install into a project non-interactively
As P-02, I want `--cursor <dir>` to install without asking anything, so that
I can put it in a setup script.
**Priority:** must
**Acceptance criteria:**
- Given `--cursor <dir>` on a directory that exists, then rules, the
  `docs/ux` skeleton, the `docs/brand` pack and all three linters are
  written with no prompt.
- Given a path that is not a directory, then the run fails with
  `error: '<path>' is not a directory` and writes nothing.
- Given `--force`, then rule files and linters are replaced and the
  scenario base and brand pack are still never touched.
**Status:** delivered
**Product:** unobserved

### ST-005: Land in a state that already passes its own checks
As P-01, I want the seeded project to lint clean immediately, so that my
first experience of the linter is not a wall of errors about templates.
**Priority:** must
**Acceptance criteria:**
- Given a freshly seeded project, when I run `python3 docs/ux/lint.py`, then
  it exits 0.
- Given the same project, when I run `python3 docs/brand/lint.py`, then it
  exits 0.
**Status:** delivered
**Product:** unobserved

### ST-006: Be told how to make the skills apply by default
As P-02, I want the installer to offer the family routing block, so that the
skills engage without me repeating myself in every project.
**Priority:** should
**Acceptance criteria:**
- Given the launcher is available, when an install finishes, then it is
  invoked for this member.
- Given the launcher is absent, then the one command to run is printed, in
  the same language as the rest of the CLI.
- Given either install path — the menu or `--cursor` — then the offer is
  made. Two doors into one install must not behave differently.
**Status:** delivered
**Product:** unobserved

### ST-007: Read what the tool does before running it
As P-02, I want `--help` to describe what each menu item actually writes, so
that I can decide without running it first.
**Priority:** should
**Acceptance criteria:**
- Given `--help` or `-h`, then usage prints and nothing is written.
- Given an unknown flag, then the run fails, prints usage, and exits 1.
- Given the help text, then what it says item 2 writes matches what
  `installCursor` writes.
**Status:** delivered
**Product:** unobserved
