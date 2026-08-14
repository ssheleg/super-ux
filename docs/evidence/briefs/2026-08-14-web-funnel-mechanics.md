# Brief — the web funnel gets its research method, its personalization contract, and a router for the layer that takes the money

**Run:** 2026-08-14 · **Target:** super-ux v0.40.0, sheleg-dev v0.4.4, sshlg-skills v0.55.0
**Mode:** grilled — seven branches asked, seven answered by the operator. Two answers
overruled the recommendation and are marked below.

**Source of the task.** A 42-page vendor guide, *How to vibe-code web2app funnels*
(FunnelFox, 2026), read in full. The operator asked for every mechanic and insight in it
to reach the family's knowledge references.

## Source ledger

| Source | What it gave this run |
|---|---|
| The PDF (42pp, 6 452 words) | Extracted with `pdftotext -layout`, read whole. Its design content is largely **already in the catalogue**; the gaps are listed under *What was actually missing* |
| `docs/evidence/backlog.md` | **14 open rows.** B-016 records that the board **reuses ids** — `B-011`, `B-012`, `B-013` each appear in both tables. Next free id is therefore **B-020**, not B-011 |
| `docs/evidence/verification.md` | 48 rows, **4 at `never`**. Next free id **R-27**. R-22 cites "B-016" where the board files that row as **B-017** — a stale cross-reference, logged below |
| `docs/evidence/retro.md` (508 lines, read in full) | Five standing instructions, all binding. **#4 shaped a decision this run** — a set gets ids before it gets a coverage claim, which is why `funnel-research.md` ships enumerable steps. #2 governs how every gate below is read |
| `CLAUDE.md` (super-ux) | `plugins/super-ux/skills/references/` is the source of truth; `sync_references.py` runs in the same change. Every link in a skill is a shipping instruction |
| `best-practices.md` + index | **210 practices, 82 tags.** The `web2app` tag already holds BP-124..129; `paywall` holds seventeen |
| `sheleg-dev/ad-tracking` | `SKILL.md:317` already owns `event_id` deduplication; `meta-linkedin.md:47` already owns hashed advanced matching. Neither is a gap |
| `sheleg-dev/stripe-billing` | Dunning is covered *inside* Stripe (`webhook-events.md:119`). Dependence *on* Stripe is not covered anywhere |
| `lib/routers-registry.js` (umbrella) | **Measurement that killed a premise:** line 31 already routes funnels to `super-ux`. The real gap is that `sheleg-dev` has **no router at all** |
| `graphify-out/graph.json` | 1206 nodes, built 2026-08-11, **stale** — its labels still say "206 practices" and six commits have landed since. Stage 9 refreshes it |
| `agent_sync.py check` | **Unhealthy in both repos** — 11 problems in the umbrella, 3 in super-ux, all introduced by today's own coordination commits. Became module M0 |

## What was actually missing

Measured before anything was written, because the catalogue is large enough that
"add the funnel practices" would otherwise have produced duplicates.

**Already covered, left alone:** BP-001 adapt-don't-copy · BP-005 loading screens that
sell · BP-010 / BP-029 goal echo and paywall personalization · BP-022 / BP-118 tier
anchoring · BP-070 trial levers · BP-017 second offers · BP-116 one promise from ad to
first screen · BP-121 abandonment as a flow · BP-124..129 the whole web2app band ·
`event_id` dedup and hashed matching in `ad-tracking`.

**Genuinely absent, and this run's scope:**

1. **The method for reading a funnel market.** Where competitor funnels are visible, the
   only signals available when revenue is not, what to record per funnel, how a corpus
   becomes a pattern, and the limit — the details holding a funnel together do not show
   from outside.
2. **The personalization *contract*.** The catalogue says to personalize; nothing says
   what must **not** vary, that a skipped question needs a default branch, or how the
   thing is checked.
3. **The stand-up order.** No practice states that a funnel must be publicly addressable
   before it can take money, or instrumented before it takes traffic.
4. **What a generated funnel omits silently** — access control on the answers, the
   consent moment, the deletion path. None of the three is visible on any screen.
5. **The legal text.** Nothing forbids generating a privacy policy.
6. **The access ladder** and the rule that a link carries a token rather than a person.
7. **Provider concentration** — assigned to `sheleg-dev`, not here.
8. **Where a purchase event comes from** — assigned to `sheleg-dev`, not here.

## Decisions taken (grill)

| # | Question | Answer, and why |
|---|---|---|
| D1 | Practices only, or a new reference too? | **Both.** The market-reading method is a procedure with steps and outputs; it does not compress into six lines of Do/Why/Apply-when, and BP-001 already holds the "adapt, don't copy" slot |
| D2 | Does `sheleg-dev` come into this run? | **Yes, and the family routing with it** — *operator overruled the recommendation of super-ux-only.* The payment and analytics layers of a funnel are where the guide's sharpest material sits |
| D3 | What does "family routing" mean, given funnels are already routed? | **A ninth router for `sheleg-dev`.** The measurement above disproved the premise that funnels are unrouted; the surviving gap is that money, tracking, sign-in and speed route nowhere, so an agent building a paywall improvises the Stripe wiring and the pixel — the two failures the guide names |
| D4 | Where in `sheleg-dev`? | **Extend `stripe-billing` and `ad-tracking`.** A new skill would be a section wearing a skill's clothes |
| D5 | What notices if `funnel-research.md` falls behind? | **Enumerable `FR-` ids plus the existing gates** — standing instruction #4: a set without ids cannot have coverage computed over it. Byte-identity of the shipped copies, link resolution and the prose-count recomputation all apply the moment the file exists |
| D6 | How far does the release go? | **All the way** — tags, CI read before each tag, umbrella pins, then every local copy on this machine. Knowledge that does not reach an installed plugin reaches no session |
| D7 | The source is vendor-published. Attribute how? | **A new key, marked vendor, and every mechanism stands without it.** The catalogue's own rule already says vendor figures are directional and never a practice's sole justification |

## REQ table (frozen — adding is free, removing needs the operator)

### M0 — coordination, because the route runs through it

| REQ | Requirement | Verified by |
|---|---|---|
| REQ-01 | The umbrella guards only paths its own committed tree contains; the ten `skills/*` patterns are gone, each member already guarding its own release surfaces | `agent_sync.py check` exit 0 in the umbrella |
| REQ-02 | super-ux guards only files that exist, ignores `.env.agent-sync`, and has a snapshot | `agent_sync.py check` exit 0 in super-ux |

### M1 — super-ux knowledge

| REQ | Requirement | Verified by |
|---|---|---|
| REQ-03 | A practice states the personalization contract: named state keys, a mandatory default branch, and the boundary — wording and imagery vary, the product and its price never | The entry, its tags, and the regenerated index |
| REQ-04 | A practice states the stand-up order: publicly addressable before it takes money, instrumented before it takes traffic | The entry and the index |
| REQ-05 | A practice states the three decisions a collected answer carries that no screen shows — who may read it, when consent was taken, how it is deleted | The entry and the index |
| REQ-06 | A practice forbids generating the legal text and says what to do instead | The entry and the index |
| REQ-07 | A practice states the access ladder, its mandatory fallback, and that the link carries a short-lived token rather than a person | The entry and the index |
| REQ-08 | BP-118 states the smallest-natural-unit framing web funnels actually use | The entry's own text; title and tags unchanged, so the index is unaffected |
| REQ-09 | `funnel-research.md` exists, its steps carry `FR-` ids, it is linked from `ux-foundation` and `ux-flows`, and every shipped copy is byte-identical to the source | `sync_references.py`, then `validate_shipped_references` |
| REQ-10 | The new source key is in the legend, marked as vendor guidance, and no practice rests on that authority alone | The legend; each entry's *Why* read without its key |
| REQ-11 | Every count in prose equals the artifact it counts | `validate_stated_numbers` |
| REQ-12 | The check-count floor rises rather than silently falling | `test/floors.json` + `check_floor()` |

### M2 — sheleg-dev

| REQ | Requirement | Verified by |
|---|---|---|
| REQ-13 | `stripe-billing` names dependence on one provider as a decision with its own failure modes, distinct from the dunning it already covers | The reference section; sheleg-dev's own gate |
| REQ-14 | `ad-tracking` states that a purchase event originates in the payment webhook rather than the browser, and what follows for accuracy — extending the `event_id` material rather than repeating it | The edit; sheleg-dev's own gate |

### M3 — the umbrella

| REQ | Requirement | Verified by |
|---|---|---|
| REQ-15 | A ninth router declares `sheleg-dev` with all four required parts | the router-texts test, then `npm test` |
| REQ-16 | The routing block reaches the operator's file through `protect()`, a backup is taken, everything outside the sentinels survives byte for byte, and the command is idempotent | Three real runs against a real file, hashes compared |
| REQ-17 | Both members are pinned at the versions `skills.json` advertises | `test/validate.py`, then `check_pins.py` |
| REQ-18 | Released and installed: each tag cut only after its CI verdict was read, and every local copy on this machine updated | the CI verdict, `npm view`, `npx sshlg-skills@latest update` |

## Carry-over ledger

| Row | Status |
|---|---|
| R-22 in `verification.md` cites `B-016` for the `AT-` coverage gap; the board files it as `B-017` | open — a one-word fix, but it is a citation into a register whose id reuse is itself an open row (B-016) |
| The code graph is stale at "206 practices" | open — stage 9 refreshes it |
| The per-country approval-rate and card-churn figures in the guide are vendor-published | resolved at intake — no figure is restated; the mechanisms are written to stand without them |
| `agent-stack`, `make-skill`, `seo-aeo-audit`, `task-pipeline`, `agent-sync`, `sheleg-design` coordination configs were written in the same pass as the two found broken | open — only the two this run touches are repaired; the other six are unmeasured |
