Contract: brand-contract v1

# docs/brand/ — how this product speaks

`docs/ux/` decides **what the product does**. This folder decides **how it
speaks** — in the interface, on the landing page, in the store listing, in a
post. One voice, many registers.

Owned by the `brand-voice` skill. Written by `copywriting`. Checked by
`python3 docs/brand/lint.py` and by `/ux-audit copy`.

| File | Holds |
|---|---|
| `voice.md` | the identity: pack, five axes, narrative, invariants |
| `terminology.md` | our words, banned words, entity and tier names |
| `facts.md` | canonical numbers and proof — the only source of a figure |
| `channels.md` | one record per surface: register, limits, bans |
| `strings.md` | interface string registry → `file:line` → scenario |
| `locales/<code>.md` | per-locale delta |

## Sources

**Fill this in before anything else.** The linter scans nothing outside these
paths, and refuses to report a clean run over a surface it never read
(`B006`). Delete the keys this project does not have — a declared-but-absent
source is worse than an omitted one.

```
Sources:
  ui:        src/**/*.{ts,tsx,js,jsx,vue,svelte}
  marketing: content/**/*.{md,mdx}
  store:     store/{ios,android}/*.md
  robots:    public/robots.txt
  locales:   src/locales/*.json
```

`ui` and `marketing` also classify findings — several checks apply to only
one of the two.

## The hard rule

Any change to public-facing text updates this folder in the same change, and
`python3 docs/brand/lint.py` exits clean before the work is called done.

## Commands

| Command | Does |
|---|---|
| `/brand` | status across every file, then one recommended action |
| `/brand-init` | pick a voice pack and calibrate it to this product |
| `/brand-update` | recalibrate after positioning or personas changed |
| `/brand-lint` | run the linter |
| `/copy` | write or edit copy for a named surface |
