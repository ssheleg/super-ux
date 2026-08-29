# User Flows

<!-- Managed with super-ux (ux-contract v4). The HOW layer. -->

How a person moves through super-ux's own installer. Screens are referenced
by `SCR-NN` and specified once in `screens.md`.

## Task analysis

The user's task is *"get this working in my project"*. Everything else is
overhead. Three entry shapes cover it: they know nothing (menu), they know
exactly what they want (`--cursor`), or they want to read first (`--help`).
Every flow ends in one of two states: files written and itemized, or nothing
written and a reason given.

## Index

| ID | Flow | Entry | Screens |
|----|------|-------|---------|
| FLW-01 | Interactive install | `npx super-ux` on a TTY | SCR-01, SCR-03, SCR-04, SCR-05, SCR-06 |
| FLW-02 | Piped / non-TTY install | `npx super-ux` with piped stdin | SCR-02, SCR-03, SCR-04, SCR-05, SCR-06 |
| FLW-03 | Direct project install | `npx super-ux --cursor <dir>` | SCR-04, SCR-06 |
| FLW-04 | Read before running | `npx super-ux --help` | SCR-07 |

## Flows

**No flow carries a `Status:`.** Four of them did, reading `confirmed`, and
the contract gives this layer no status at all — so the value sat outside
every enum, unrefused and unaccepted. A flow's delivery state is *measured*
through the screens it traverses, which is the whole point of `U057`; a
status declared here would be the inherited verdict that rule refuses,
written into the record. `U075` now says so on every layer with no enum.

### FLW-01: Interactive install
**Traces:** ST-001, ST-003, ST-006

```mermaid
flowchart TD
    A[npx super-ux] --> B{stdin and stdout are TTY?}
    B -- no --> F02[FLW-02]
    B -- yes --> M[SCR-01 multi-select list]
    M -- q / esc / ctrl+c --> Q[exit, nothing written]
    M -- enter, nothing selected --> N["SCR-04 'Nothing selected.'"]
    M -- enter, cursor selected --> D[SCR-03 project directory prompt]
    M -- enter, no cursor item --> R
    D --> R[SCR-04 install log]
    R --> C{claude item selected?}
    C -- yes --> P[SCR-06 plugin install output]
    C -- no --> S
    P --> S{skills item selected?}
    S -- yes --> G{super-ux plugin in this home?}
    S -- no --> O
    G -- "no, or --force" --> K[SCR-05 skills CLI picker]
    G -- "yes, no --force" --> RF["SCR-05 refused: remedy, exit 3"]
    K --> O[SCR-04 routing-block offer]
    RF --> O
```

Every terminal node writes either files plus an itemized log, or nothing
plus a stated reason. There is no third outcome. The skills handoff is
gated (SCR-05): while super-ux is installed as a Claude Code plugin, the
skills CLI would recreate the plain `~/.claude/skills/super-ux` copy that
shadows it, so the handoff is refused with the remedy printed and exit 3;
`--force` records the two-channel choice. A successful run ends with the
`Updates:` block naming how the next version arrives.

### FLW-02: Piped / non-TTY install
**Traces:** ST-002, ST-003

```mermaid
flowchart TD
    A[npx super-ux, stdin piped] --> L[SCR-02 numbered list + prompt]
    L -- "empty / q / quit" --> N["SCR-04 'Nothing selected.'"]
    L -- "a / all / *" --> ALL[every item selected]
    L -- "1,3" --> SEL[items 1 and 3]
    L -- out of range or not a number --> E["SCR-04 error: invalid selection"]
    ALL --> D
    SEL --> D[SCR-03 directory prompt, if cursor selected]
    D --> R[SCR-04 install log]
    R --> K["SCR-05 gated skills handoff, if skills selected (as in FLW-01)"]
    E --> X[exit 1, nothing written]
```

The prompter buffers lines that arrive between questions; a second prompter
would drop them. That is why one instance spans the whole flow. The skills
item runs through the same gated handoff as FLW-01: refused with exit 3
while the super-ux plugin is installed, unless `--force`.

### FLW-03: Direct project install
**Traces:** ST-004, ST-005, ST-006

```mermaid
flowchart TD
    A["npx super-ux --cursor DIR [--force]"] --> V{DIR exists and is a directory?}
    V -- no --> E["SCR-04 error: not a directory"] --> X[exit 1, nothing written]
    V -- yes --> RU[copy .mdc rules]
    RU --> RX{rule exists and no --force?}
    RX -- yes --> SK["skip: line"]
    RX -- no --> IN["install: line"]
    SK --> UX
    IN --> UX[seed docs/ux skeleton]
    UX --> BR[seed docs/brand pack]
    BR --> LI{script present in package?}
    LI -- yes --> SY["sync: three linters"]
    LI -- no --> WA["warning + where to get it, install continues"]
    SY --> DN[SCR-04 done line with all three counts]
    WA --> DN
    DN --> OF[SCR-04 routing-block offer]
```

`vision.md` is deliberately **not** seeded by any path: an empty vision
reads as a decided one.

### FLW-04: Read before running
**Traces:** ST-007

```mermaid
flowchart TD
    A["npx super-ux --help"] --> U[SCR-07 usage] --> Z[exit 0, nothing written]
    B["npx super-ux --bogus"] --> ER["SCR-04 error: unknown mode"] --> U2[SCR-07 usage] --> X[exit 1]
```
