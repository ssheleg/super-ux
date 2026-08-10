---
description: Single entry point for all UX work — status across every layer (vision, foundation, flows, screens, scenarios, audits, brand), then a menu of applicable actions (init, design, update, validate, audit, write copy, plan fixes)
---

Single entry point for super-ux. The user is NOT expected to know the
skills, layers, or commands inside this plugin — routing is your job.
Idempotent: safe to run any number of times, at any project stage.

## 0. Understand the task (before anything technical)

If `$ARGUMENTS` already states the task, map it via the routing table and
skip the question. Otherwise ask ONE plain question — "What do you want to
get done with the product's UX?" — with a few examples in everyday words
(new product, new feature, "the UX feels bad", "check that everything
works", "make a fix plan"). Never ask the user to choose between skills or
layers — that vocabulary is internal.

**If the task involves designing or improving the interface** (routes 1, 3,
4), and the foundation's Design tooling section hasn't recorded a Figma
choice yet, ask one more plain question: "Design the interface visually in
Figma as we go, or text-only? (Figma is the default.)" Record the answer in
`foundation.md` → Design tooling. If Figma is chosen and the Figma MCP isn't
connected, recommend connecting it and proceed text-only until it is (see
figma-integration reference).

**Visual identity, same moment:** if `screens.md` → Design system has no
`Style pack` and the project has no design system of its own, use the
**sheleg-design** companion skill to pick one (`workbench` for product UI /
dashboards / tools, `instrument-console`, `editorial-luxury`, or a new pack
on its contract) and record the pack + its token file; a cinematic
scroll-driven landing also takes its motion methodology. Not installed →
offer the one-time install once (`/plugin marketplace add
ssheleg/sheleg-design-skill` + `/plugin install
sheleg-design@sheleg-design-skill`, or `npx sheleg-design-skill` in the
project) and continue on platform defaults either way — recommend, don't
force. Division of labor: the visual-identity reference.

Routing table (user's words → action from the menu below):

| User says (any language) | Route to |
|---|---|
| "new product", "from scratch" / "стартуем проект", "с нуля" | 1 then 2 then 4 then 6 (vision first, then the chain) |
| "what are we even building", "product vision", "where is this going" / "видение", "что мы вообще строим", "куда идём" | 1 |
| "new feature", "I want to add X" / "новая фича", "хочу добавить X" | 7 (validate idea vs chain — and vs the anti-vision if `vision.md` exists) then 4/6 for the new parts |
| "the UX is bad", "clunky", improve, redesign / "UX плохой", "неудобно" | 5 (Improve) |
| "check everything works", audit, "run the scenarios" / "проверь что всё работает", "прогони по сценариям" | 8 |
| "what is missing", gaps, coverage / "чего не хватает" | 9 |
| "what do best practices say" / "как лучше по практикам" | 10 |
| "the copy is inconsistent", "tone of voice", "how should this sound" / "текстовка разная везде", "тон оф войс" | 11 |
| "write the button/error/landing/post" / "напиши текст", "перепиши", "заголовок", "лендинг" | 12 |
| "does the copy match the brand" / "проверь тексты по бренду" | 13 |
| "what to fix first", plan / "что чинить в первую очередь", "план" | 14 |
| "don't know", "just take a look" / "просто посмотри" | run 1–3 of Inspect, recommend from state |

Three layers sit outside the chain and are reached only from here, so never
answer from the chain alone: **vision** (what the product is and refuses to
become), **brand-voice** and **copywriting** (how it speaks). A user who says
"the texts are a mess" is not asking for a scenario.

## 1. Inspect state

- Hard rules in the project's instruction file (`CLAUDE.md` / `AGENTS.md` /
  `GEMINI.md` — whichever it has): `## UX scenarios — hard rule (super-ux)`,
  and `## Vision alignment — hard rule (super-ux)` when `vision.md` exists.
- `docs/ux/vision.md`? If yes: `Status`, `Last reviewed`, whether all nine
  sections are filled, and whether the alignment rule is installed. A vision
  with no rule is a document nothing reads — say so.
- `docs/brand/voice.md`? If yes: the recorded pack, its `Status`, facts
  carrying `⚠ TBD` or no source, locale parity, and the brand linter's error
  and warning counts (`python3 docs/brand/lint.py`). If `docs/brand/` is
  absent and the product has user-facing text, that is a gap, not a
  non-issue.
- `docs/ux/foundation.md`? If yes: counts of personas / JTBD / journeys /
  stories by status.
- `docs/ux/flows.md`? If yes: flow count, `inferred` vs confirmed, stories
  without flows.
- `docs/ux/screens.md`? If yes: screen count by status
  (designed/built/drifted), screens missing Figma frames (when Figma on),
  screens missing coverage.
- `docs/ux/scenarios.md`? If yes: scenario counts by status, features,
  `Traces` filled or not, `Last audit` values.
- Latest report in `docs/ux/audits/` (date, totals, open findings) and any
  unexecuted plan in `docs/ux/plans/`.
- **Run the linter** `python3 docs/ux/lint.py` and fold its errors/warnings
  into the status — it is the fastest, deterministic read of what's stale,
  drifted, or missing (lost Figma frames, broken traces, orphans).
- **Run the doctor** `python3 docs/ux/doctor.py` and report the contract
  state alongside it. The linter checks the chain against itself and stays
  silent when the whole base is written to an old contract; the doctor is
  what notices. If it reports a mixed or stale contract, say so before
  offering any other action — designing on top of a base three versions
  behind is how the versions got mixed in the first place.

## 2. Repair silently (no menu needed for these)

- Rule missing → install it (as `/ux-rule`).
- `docs/ux/` missing → create skeleton (seed `scenarios.md`,
  `foundation.md`, `flows.md`, `screens.md`, `README.md`; copy **both**
  `lint.py` and `doctor.py` from the plugin's `scripts/`; `audits/` and
  `plans/` dirs) — as `/ux-rule` does. Never tell the user to run a script
  this step did not put there.
- `docs/ux/vision.md` is **never** seeded silently: an empty vision reads as
  a decided one. Offer action 1 instead.

## 3. Status report

Compact table across every layer: vision (present? status, alignment rule
installed?), foundation (present? entry counts, assumptions unvalidated),
flows (count, `inferred` vs confirmed), screens (by status, missing
frames/coverage), scenarios (total/by status, traced %, features), audits
(last run, PASS/PARTIAL/FAIL/BLOCKED totals, open findings), brand (pack,
status, unsourced facts, locale parity), plus both linters' error/warning
counts.

A layer that is absent gets a row saying so. An omitted row reads as a
passing one.

## 4. Action menu

Offer ONLY the applicable actions, numbered, with a one-line why; let the
user pick (multiple allowed). Full catalog:

1. **Write the vision** — `vision` — when `docs/ux/vision.md` is missing and
   the product's direction is what's actually in question, or a feature keeps
   feeling off-strategy. Writes the nine layers AND installs the alignment
   rule; a vision with no rule is skipped work, not a shortcut.
2. **Build the WHY layer** — `ux-foundation` Init (interview or reverse) —
   when foundation is missing/empty.
3. **Update foundation** — `ux-foundation` Update — when user knowledge
   changed.
4. **Design flows & screens** — `ux-flows` Design/Reverse — when stories
   exist without flows, or an existing product has no `flows.md`; registers
   every screen and state in `screens.md` (and its Figma frames when Figma
   is on).
5. **Improve existing UX** — `ux-flows` Improve — heuristic evaluation
   (PRN-01..24) of current flows → traced before/after redesign proposals.
6. **Build/extend scenarios** — `ux-scenarios` Init or Update — when
   scenarios missing, or flows/stories lack scenario coverage.
7. **Validate the chain** — `ux-scenarios` Validate (+ `ux-foundation`
   Validate) — before building a new feature, or when traceability is
   doubtful. With `vision.md` present, the idea is checked against the
   anti-vision and the alignment test first: a feature that fails there is
   not a scenario problem.
8. **Audit code vs scenarios & flows** — `ux-audit` (all / feature:X;
   depth `deep` adds heuristic + practice + coverage passes) — when
   validated scenarios were never audited, or code changed since the last
   audit; recommend `deep` before releases and after big UX changes.
9. **Coverage audit** — `ux-audit` scope `coverage` — orphan
   stories/flows/scenarios, journey gaps.
10. **Best-practices / heuristics review** — `ux-audit` scope `practices` or
    `heuristics`: tagged catalog (`BP-NNN`) and principles (`PRN-NN`)
    suggestions.
11. **Define or recalibrate the voice** — `brand-voice` Init or Update (or
    `/brand` for the verbal-identity menu) — when `docs/brand/` is missing
    and the product has user-facing text, or when positioning, pricing or
    naming moved. Seeds `docs/brand/` **and** `docs/brand/lint.py`.
12. **Write or fix copy** — `copywriting` (or `/copy <surface>`) — any string,
    error, empty state, landing, pricing page, post, store listing or email.
    Requires a pack; with none, route to 11 first rather than improvising a
    voice.
13. **Audit the copy** — `ux-audit` scope `copy` — tone drift, unproven
    claims, the any-other-SaaS test, and whether the voice overshot into the
    failure mode its own pack declared. The judgement twin of
    `python3 docs/brand/lint.py`; report both.
14. **Plan fixes** — produce `docs/ux/plans/YYYY-MM-DD-<scope>.md` from the
    latest audit/Improve results: target interface per screen +
    CREATE/MODIFY/DELETE change table, every row traced, prioritized
    Frequency × Severity × Solvability. Then say what the user has in hand
    (plan, audit report, `docs/ux/` chain, Figma) and recommend — don't
    force — implementing it autonomously by best practices with the ssheleg
    **task-pipeline** plugin: installed → `/task-pipeline <plan file>`; not
    installed (optional one-time) → `/plugin marketplace add
    ssheleg/task-pipeline` + `/plugin install task-pipeline@task-pipeline`;
    or superpowers writing-plans / by hand — user's call.
15. **Nothing** — everything green; rerun `/ux` after the next change.

Recommend exactly one action as the default (mark it "recommended"), based
on the state: no vision and the user is starting or steering the product →
1; no foundation → 2; stories without flows → 4; flows without scenarios →
6; drafts pending → validate/review; never audited or stale → 8; user-facing
text with no `docs/brand/` → 11; open findings → 14; user said "the UX is
bad" / "UX плохой" → 5; user said the copy is inconsistent → 11.

Additional context from the user: $ARGUMENTS
