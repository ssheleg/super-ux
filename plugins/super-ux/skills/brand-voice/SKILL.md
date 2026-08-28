---
name: brand-voice
description: Use when defining, calibrating or checking how a product speaks — tone of voice, brand voice, verbal identity, the words the product owns and the words it bans, canonical facts, per-surface register, locales. Triggers - "tone of voice" / "тон оф войс", "brand voice" / "голос бренда", "brandbook" / "брендбук", "our terminology" / "наша терминология", "how should this sound" / "как это должно звучать", "the copy is inconsistent" / "текстовка разная везде", starting any marketing surface, onboarding a product into docs/brand/. For writing the actual text, see copywriting.
license: MIT
---

# brand-voice — define and hold the verbal identity

> Part of **super-ux** — see [system-map.md](references/system-map.md) for the
> whole pipeline. After changes, run `python3 docs/brand/lint.py`.

`docs/ux/` decides **what the product does**. This skill decides **how it
speaks**, and owns `docs/brand/` in the target project.

**Format contract:** [brand-contract.md](references/brand-contract.md)
(brand-contract v1). Read it before writing or editing anything under
`docs/brand/`. Never deviate from its file names, field names or statuses —
the linter and the audit key off them.

**The pack library:** [voice-packs.md](references/voice-packs.md) — six
archetypes, each with a declared failure mode. The register model:
[surface-registers.md](references/surface-registers.md). Locales:
[localization.md](references/localization.md).

## Invoked with no task → status, then one next action

1. Report the state: is a pack recorded, what `voice.md` says its `Status`
   is, how many facts carry `⚠ TBD` or no source, locale parity, and the
   linter's error and warning counts.
2. Name every unresolved fact. **Never invent one to close a gap** — an
   unknown is reported, not filled.
3. Propose exactly **one** next action, usually the top open fact or the
   surface the user actually came for.

## Where the voice comes from

The pack is derived from `docs/ux/foundation.md` — personas, jobs, and the
deciding input: **what the user loses when the product fails.** A voice that
charms when the stakes are a playlist is intolerable when the stakes are
payroll.

The dependency runs one way. A persona never changes because a tone was
appealing. With no foundation, work in degraded mode: stamp
`Derived-from: inferred`, say plainly that the WHY layer should be built, and
continue rather than blocking.

## Choosing a workflow

| Situation | Workflow |
|---|---|
| No `docs/brand/` | Init |
| Pack chosen, product specifics missing | Calibrate |
| Positioning, personas or facts changed | Update |
| Consistency questioned, or before a launch | Validate |

Announce which one you are running.

## Init

1. **Read the foundation.** Personas, JTBD, journeys, stakes. Where it is
   absent, interview: who is this for, what are they accountable for, what
   does failure cost them.
2. **Read what already exists.** Interface strings, landing copy, README,
   store listing, recent posts. The current voice is data even when nobody
   chose it.
3. **Propose one pack with reasoning, plus one alternative.** Name why the
   runner-up loses. Let the user pick.
4. **Seed `docs/brand/`** from the plugin's `templates/brand/`, and fill the
   `Sources:` block first — nothing else can be checked until the linter
   knows where the project keeps its text.
5. **Inventory sweep** for `strings.md`: routes, screens, buttons, states,
   errors, empty states. Every string gets a row with its `file:line` and the
   scenario it serves. Dispatch parallel Explore subagents for a large
   codebase, one area each.
6. **Ask which humanization pass this project wants**, and write the answer to
   `voice.md`'s `Humanization pass:` field. `own` is the default and the only one
   that reads this pack's registers and facts; `npx sshlg-skills humanizers` shows
   what else is installed and how to install what is not. Ask once — the field
   exists so nobody is asked twice, and it selects a pass, never a verdict.
7. Everything starts `Status: draft`.

## Calibrate

The pack is a starting position; this is where it becomes the product's own.

- **Terminology.** Which generic words does this product replace, and with
  what. Seed the banned table from weak verbs, hedging chains and
  [ai-tells.md](references/ai-tells.md), then add what is specific here.
- **Facts.** Every number the product quotes, with a source, a checked date
  and a review date. Mark internal figures `Public: no`.
- **Channels.** One record per surface the product actually has. Register as
  deltas; `Forbidden:` always carries both the physics and the brand half.
- **Ready lines.** Six to ten, written for this product, not copied from the
  pack.
- **Failure mode.** Copy the pack's into `voice.md` so the audit can look for
  it by name.

Present section by section for approval. Approved moves `draft` →
`validated`.

## Update

1. Identify what changed — positioning, a persona, a price, a tier name, a
   new surface.
2. Apply the edits. A changed entity name propagates to `terminology.md`,
   `strings.md` and every locale in the same change.
3. Changed files drop to `Status: draft` until re-approved.
4. Re-stamp `Last calibrated`.

## Validate

1. **Integrity** — every field the contract requires is present; statuses are
   legal; `Derived-from` resolves against the foundation.
2. **Coverage** — every surface the product ships has a record; every locale
   declared has a file; every quoted number has a fact.
3. **Consistency** — run `python3 docs/brand/lint.py` and fold its findings
   in. It proves the mechanical half; report what it cannot see as questions
   for `/ux-audit copy`.
4. **Staleness** — foundation newer than the last calibration, facts past
   review, physics rules past their checked date.

## Definition of done

- Contract honored; the marker on every file.
- The user has seen and approved new or changed sections.
- `python3 docs/brand/lint.py` exits 0, or every remaining finding is
  reported with a reason.
- Unknowns stated as unknowns. Nothing invented to make a table look full.
