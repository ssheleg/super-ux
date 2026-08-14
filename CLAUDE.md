# CLAUDE.md — super-ux

Guidance for agents working **on** super-ux. For using it, see `README.md`.

super-ux is the plugin that demands a design chain before UI code. It has a
user-facing interface of its own — the installer CLI and its interactive
menu in `bin/super-ux.js` — so it is bound by its own rules. It went three
months without them; the 2026-08-10 audit found four defects in that CLI
inside an hour of writing the scenarios it should have had.

## Where the artifacts are

| Path | What |
|---|---|
| `docs/ux/` | This project's own chain — vision, foundation, flows, screens, scenarios |
| `docs/brand/` | This project's own verbal identity, and the surfaces it governs |
| `docs/evidence/` | Pipeline records: briefs, specs, plans, `retro.md`, `backlog.md`, `verification.md` |
| `plugins/super-ux/skills/references/` | **Source of truth** for every contract. After editing, run `python3 test/sync_references.py` |
| `templates/` | Seeds seen by target projects — including both hard rules, whose only source these are |
| `docs/AGENT_SYNC.md` | How coordination is wired here, and what it does NOT guarantee. **Generated** from `.claude/agent-sync.json` — read it before editing a guarded file, and regenerate it in the same change that alters the config |

## Gates

Run each **alone** and read its own exit code. Never through a pipe: `tail`
exits 0 whatever it reads, so `validate.py | tail -2 && git commit` commits
on a red validator. That happened once, in this family, on a tag.

```sh
python3 test/validate.py          # repo consistency
python3 test/brand_lint_test.py   # one fixture per brand-lint code
python3 docs/ux/lint.py           # this project's own chain
python3 docs/brand/lint.py        # this project's own copy
python3 test/release_preflight.py # before any tag
```

Editing anything under `plugins/super-ux/skills/references/` requires
`python3 test/sync_references.py` in the same change — the per-skill copies
are what non-Claude agents actually receive.

**Every link in a skill is a shipping instruction.** `sync_references.py`
copies the transitive closure of a skill's links into that skill. One link
from `system-map.md` to `brand-contract.md` once put all nine brand
contracts inside every UX skill. The map names contracts; it links none.

## Adding a skill

A skill exists in seven places or it does not exist: its own directory, a
`cursor/rules/<name>.mdc`, the system map's skill list, both manifest
descriptions, and `commands/ux.md` so `/ux` can route to it.
`validate_skill_parity()` asks for each by name — because absence has one
side and no single file looks wrong.

## Adding a hard rule

The rule's text lives in `templates/`, and the command or skill that
installs it carries an identical embedded copy. Add the pair to `HARD_RULES`
in `test/validate.py`. A rule with two texts is the drift this plugin exists
to prevent.

## Releasing

See `CONTRIBUTING.md` → Releasing. Four version places, the preflight, and
`git push --atomic origin main vX.Y.Z` — `--follow-tags` is not atomic, and
a rejected branch still lets the tag through.

---

## UX scenarios — hard rule (super-ux)

- `docs/ux/scenarios.md` is the source of truth for all user-facing
  behavior; `docs/ux/foundation.md` (personas, JTBD, journeys, stories) and
  `docs/ux/flows.md` (user flows) are the WHY and HOW layers scenarios
  trace to.
- Any change that touches user-facing behavior or interface MUST update, in
  the same change: `docs/ux/scenarios.md`; affected flows; the affected
  screens in `docs/ux/screens.md` (the UI map — states, elements,
  coverage); and, when Figma is enabled, the Figma frame(s) plus their
  links in `screens.md`. A screen whose code diverges from its record, or a
  stale Figma link, is drift — the exact thing this system prevents.
- Any new feature or project STARTS with the chain: which job, which
  journey stage, which story it serves → the flow → the screens and their
  states → the scenarios. Validate against the existing base, get approval,
  and only then write code.
- Do NOT write interface code until that workflow is done — the chain is
  designed and approved for the change at hand, the affected scenarios and
  screens exist and are `validated`/`designed`, conflicts with existing
  scenarios are resolved, the user has approved them,
  and — when Figma is enabled (default) — the UI is mocked up in Figma with
  every screen linked to its frame. Building UI before this is the exact
  mistake super-ux exists to prevent.
- Visual identity is ONE locked style pack, recorded in `docs/ux/screens.md`
  → Design system and obeyed by every Figma frame and every built screen —
  picked with the **sheleg-design** companion skill when the project has no
  design system of its own (recommended, not required). Inventing a palette,
  type pairing, or motion per screen is visual drift.
- After any UX change and before calling the work done, run the linter
  `python3 docs/ux/lint.py` — it must pass (errors are drift/broken
  structure; wire it into CI/pre-commit).
- Use `/ux` as the entry point; skills: `vision` (what the product is and
  refuses to become), `ux-foundation`, `ux-flows` (flows + Figma mockups),
  `ux-scenarios` for maintenance, `ux-audit` for evidence-backed
  verification, `brand-voice` and `copywriting` for everything the user
  reads. Full map: the plugin's system-map reference.

## Brand voice — hard rule (super-ux)

- `docs/brand/` is the source of truth for how the product speaks:
  `voice.md` (axes, narrative, invariants), `terminology.md` (our words and
  the banned ones), `facts.md` (the only source of any public figure),
  `channels.md` (one record per surface), `strings.md` (the interface string
  registry), `locales/<code>.md`.
- Any change to public-facing text (an interface string, a landing page, a
  post, a store listing, an ad, an email) updates `docs/brand/` in the SAME
  change. A new string with no registry row is drift, not a detail.
- **Never quote a number that has no row in `facts.md`,** and never invent a
  fact, statistic, quote or expert to fill a gap. Report the gap instead.
- **One action keeps one name** across button, confirmation, toast, history,
  notification and accessible name. Search `strings.md` before naming one.
- **No humor, exclamation marks or emoji** on error, destructive confirm,
  billing or paywall surfaces, in any voice.
- **No rhetorical dash, and no full stop after a title.** A dash standing in
  for a full stop, a comma or a colon is the loudest machine-drafting marker
  the pack has, and a heading, button, menu item or page title is a name
  rather than a statement. The dash a language requires stays: the Russian
  copula, numeric ranges, direct speech. Choose the replacement from the
  meaning, because a comma, a colon and a full stop state three different
  relationships and find-and-replace picks the wrong one. `B062` and `B063`
  catch what a machine can prove; the rest is in the skill's `ai-tells.md`.
- Run `python3 docs/brand/lint.py` after any text change and before calling
  work done. It must exit clean; wire it into CI or pre-commit alongside the
  UX linter so copy drift cannot merge.

## Vision alignment — hard rule (super-ux)

Before planning any new feature, capability or significant change, check it
against `docs/ux/vision.md` — specifically the **anti-vision** and the
**alignment test**.

**Aligned** → proceed, and say in one line which part of the vision it serves.

**Misaligned** → stop and say so before writing code:
1. Name the conflict — which layer it contradicts, quoting that layer.
2. Offer two paths: (a) reshape the feature to fit, with the specific change;
   (b) amend the vision, saying which layer changes and what that costs.
3. Wait for the decision. Do not pick one silently.

**Do NOT trigger for:** bug fixes, refactors, dependency work, tests,
documentation, or anything with no user-facing surface. A vision check on a
typo fix is how a team learns to skip the check that matters.
