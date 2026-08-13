# Brief — a public web surface gets a home, and the router learns the user's words

**Run:** 2026-08-10 · **Board rows:** B-007, B-008, B-009 · **Target:** v0.33.0
**Mode:** autonomous — the operator delegated the whole run ("го до конца автономно"),
so every grill branch below is resolved with its recommended answer and recorded here
rather than asked.

## Source ledger

| Source | What it gave this run |
|---|---|
| `docs/superpowers/backlog.md` | **8 open rows.** B-007 (18), B-008 (18), B-009 (12) are this run's scope; B-001..B-005 stay open |
| `docs/superpowers/verification.md` | **0 rows at `never`** — every shipped REQ has been watched fail |
| `docs/superpowers/retro.md` | Three standing instructions, all binding: preflight before any tag; never read a gate through a pipe; **a new check runs against the seeded template first** |
| Carry-over ledgers (4 briefs) | **0 unresolved** |
| `graphify-out/graph.json` | Rebuilt today — 1091 nodes. Reach: 38 nodes originate in `scenario-format.md`, and `UX Contract v4` is a hub, so a contract edit touches the whole chain vocabulary |
| `seo-aeo-audit` → `references/onpage-checks.md` | **The grounding for every field name below.** O1–O5 name the checks an audit runs on a live page; the design-time record is built as their twin |
| `~/.claude/CLAUDE.md` → seo-llmo rule | The rule this run exists to make obeyable: a public surface is designed for two readers, **decided at design time, not by an audit afterwards** |
| `docs/ux/`, `docs/brand/` (own chain) | The dogfood target — super-ux must answer its own new question |

## The defect, stated once

`references/scenario-format.md` mentions indexability, robots, crawlers and schema
**zero times**. A landing page is registered in `screens.md` with Purpose, States,
Elements, Figma and Coverage, and nowhere to record that it is a URL a machine will
read. The operator's standing rule says that is decided at design time; `seo-aeo-audit`
is the afterwards. The chain designs the surface the rule governs and gives the rule
nowhere to land.

## Decisions taken (grill, resolved autonomously)

| # | Question | Answer, and why |
|---|---|---|
| D1 | New contract version, or additive to v4? | **v4, additive.** Precedent: v0.26.1 added optional foundation §7 and stayed v4; the earlier `C-01` closed on the same reading. An optional block breaks no existing base and needs no migration |
| D2 | A new `docs/ux/web.md`, or a block inside `screens.md`? | **A block inside `screens.md`.** A landing *is* a screen; a second file is a fourth copy of truth with its own orphan risk. No new **column** in the Index table either — columns are contract keys and adding one breaks every existing table |
| D3 | Which fields? | **Five, each the design-time twin of a check `seo-aeo-audit` runs later** — `Route` (O1 URL structure), `Answers` (O1 one page per query cluster), `Indexable` (O1/O2 canonical + indexation), `Without JS` (O3 crawlable `<a href>`, O4 the task module exists for a crawler), `Entity` (O1 structured data matched to visible content). One vocabulary on both ends |
| D4 | How does a project say it has no public surfaces? | **One project-level `Web surfaces:` line in `screens.md`, yes/no.** A declared absence is countable; a skip is not. `no` silences the check forever, and the reason is recorded beside it |
| D5 | Error or warning? | **Malformed or partial block → error. Missing declaration → warning.** The gate is shape, never self-declared status — that is B-005's lesson applied before it repeats |
| D6 | Does SEO get its own action in the `/ux` menu? | **No — it gets a companion.** `seo-aeo-audit` joins `sheleg-design` and `task-pipeline` on the same recommend-never-force contract. super-ux owns *what the surface must record*; the companion owns *whether the live page obeys it* |
| D7 | Facts on a marketing page — new field? | **No.** `docs/brand/facts.md` is already the only home of any public figure, and B030 already blocks an unsourced one. A second home would be the drift this plugin exists to prevent |
| D8 | Release size | **v0.33.0 minor.** Additive contract, new router behaviour, new companion |

## REQ table (frozen — adding is free, removing needs the operator)

| REQ | Requirement | Verified by |
|---|---|---|
| R-01 | The screen record gains an optional `Web surface:` block with exactly the five fields of D3, defined once in `references/scenario-format.md` | contract section present; `validate_stated_numbers` counts the fields |
| R-02 | `screens.md` carries one project-level `Web surfaces:` declaration; absence is declared, never assumed | `ux_lint.py` — new check, planted defect |
| R-03 | A partial or malformed block is an **error**; a missing declaration is a **warning**; `no` silences it | `ux_lint.py` fixtures, both branches planted |
| R-04 | The new check passes on the pristine `templates/screens.md` from the first second | fresh `node bin/super-ux.js --cursor <tmp>` then `docs/ux/lint.py` exit 0 — **standing instruction #3** |
| R-05 | `ux-flows` asks the web-surface question once, at the moment it already asks about Figma and the style pack | `ux-flows/SKILL.md` |
| R-06 | `ux-audit` checks a built public screen against its recorded block and hands off to the companion | `ux-audit/SKILL.md` |
| R-07 | `seo-aeo-audit` is offered as the third companion, recommend-never-force, with its real install commands | `commands/ux.md`, `references/system-map.md`, README |
| R-08 | The `/ux` routing table speaks the four missing words: funnel/monetization, visual design, web findability, app/platform | `commands/ux.md` |
| R-09 | A composite brief is decomposed — every matching row mapped, ordered by chain position, sequence stated before the first runs | `commands/ux.md` step 0 |
| R-10 | Both hard-rule copies, all Cursor rules and both manifests stay in sync | `test/validate.py` |
| R-11 | super-ux's own chain answers its own new question (dogfood) | `docs/ux/screens.md`, `docs/ux/lint.py` exit 0 |
| R-12 | Contract stays **v4** — nothing to migrate | `ux_doctor.py` reports v4, marker unchanged |
| R-13 | v0.33.0 ships: four version places, preflight, atomic push, CI verdict read, registry serving it | `release_preflight.py`, `gh run`, `npm view` |

## Carry-over ledger

*(empty at open — rows are added the moment anything is deferred)*
