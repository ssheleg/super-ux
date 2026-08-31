# Evaluation results

**Status: authored, schema-validated, executed 2026-08-31 against two models.**

CI still proves only that the files are shaped correctly and that the validator
catches a planted invalid trigger class — it does not run an agent session. The
rows below are dated runs; their method and its limits are stated under
**Method**, because a rate with no method is a number nobody can re-measure.

| Date | Version | Model | Trigger pass rate (train / validation) | Scenario lines passed | Installed alongside | Notes |
|---|---|---|---|---|---|---|
| 2026-08-31 | 0.52.2 (probe list = v0.52.0 descriptions, unchanged through 0.52.2) | Claude Code Agent-tool alias `haiku` | 8/8 / 6/6 (14/14 overall) | not run on this model | ssheleg family: super-ux 0.52.0 (installed plugin), task-pipeline 1.79.1, make-skill 0.25.1, sheleg-design 1.58.1, seo-aeo-audit 0.25.7, agent-sync 1.18.6, sheleg-dev 0.11.0, agent-stack 0.17.0, telegram-dev 0.1.9 | one blind probe per query; per-query answers below |
| 2026-08-31 | 0.52.2 (probe list = v0.52.0 descriptions, unchanged through 0.52.2) | Claude Code Agent-tool alias `sonnet` | 8/8 / 6/6 (14/14 overall) | 12/12 (s01 4/4, s02 4/4, s03 4/4) | same family list as the row above | one blind probe per query; scenario receipts below |

## Per-query answers, 2026-08-31 (the receipt behind the rates)

| Query | Expected | `haiku` answered | `sonnet` answered |
|---|---|---|---|
| q01 | ux-flows or ux-scenarios | ux-scenarios | super-ux:ux-flows |
| q02 | ux-foundation | ux-foundation | super-ux:ux-foundation |
| q03 | ux-flows | ux-flows | ux-flows |
| q04 | ux-audit | ux-audit | super-ux:ux-audit |
| q05 | brand-voice | brand-voice | brand-voice |
| q06 | copywriting | copywriting | copywriting |
| q07 | vision | vision | vision |
| q08 | not this pack | sheleg-design | sheleg-design |
| q09 | not this pack | stripe-billing | stripe-billing |
| q10 | not this pack | task-pipeline | task-pipeline |
| q11 | not this pack | evidence-docs | task-pipeline |
| q12 | not this pack | none | none |
| q13 | not this pack | seo-aeo-audit | seo-aeo-audit |
| q14 | not this pack | agent-orchestrator | agent-orchestrator |

## Scenario line results, 2026-08-31 (`sonnet` only)

**s01 — Scenario-first feature** (fresh agent, empty git repository): 4/4.
Wrote `foundation.md` (2 personas, 2 JTBD, 9 stories) before any screen;
mapped success, offer-accept, offer-decline, retry/failure and
pending-cancellation return states across 9 screens and 10 scenarios; the
pack's own `ux_lint.py` over the output: 0 errors, 1 warning (`U057`, no code
exists yet to cite as coverage — the honest state of a design-only pass);
boundaries held — low-fi wireframes only, store billing handled as flow states,
no visual identity invented.

**s02 — As-built UX audit** (fresh agent, checkout of this repository at
`519d612`): 4/4, one caveat. Audited `bin/super-ux.js` against all 17 scenarios
(14 PASS / 3 PARTIAL / 0 FAIL / 0 BLOCKED, verdict REFINE); findings carry
`file:line` on both sides (e.g. `bin/super-ux.js:428` prints `Nothing selected`
where `scenarios.md:62` quotes a trailing period); the report separates
could-not-verify from defects, though no absent scenario arose to exercise that
branch; the product was left untouched and the fix path offered rather than
auto-run. The agent's own report discloses one early non-hermetic live call
(a real `claude plugin marketplace add`, verified afterwards to have changed
nothing); every subsequent probe used a hermetic PATH.

**s03 — Brand and copy** (fresh agent, a seeded 15-line CLI with deliberately
off-voice strings): 4/4. Created `docs/brand/` (voice, terminology, facts,
channels, strings) before touching a string; one voice with per-surface
registers; every rewritten error names the failure, states what was not
affected, and gives one recovery step; nothing invented — the placeholder URL
and the opaque error id were flagged in `facts.md` as open instead of being
given fabricated values. `python3 docs/brand/lint.py` over the result:
`brand pack is clean`, exit 0.

## Method, 2026-08-31

- **Trigger cases** — for each of the 14 queries, ONE fresh, blind subagent
  (Claude Code Agent tool, `general-purpose`) per model, whose whole prompt was
  the query verbatim + the 28 installed family skills as `name — description`
  lines (read from the installed plugin caches) + "Which ONE skill would you
  invoke, or none? Answer with the name only." Relay runners launched the
  probes and were instructed to add nothing to the prompt. Scoring was fixed
  before any result was read: a positive query passes iff the intended skill is
  named (q01 accepts `ux-flows` or `ux-scenarios`, per its `why`); a negative
  passes iff the answer is `none` or a skill outside this pack.
- **Scenarios** — one fresh `sonnet` subagent per scenario in a scratch
  workspace, prompt = one working-directory line + the scenario query verbatim;
  each `expected_behavior` line scored from the agent's report and the on-disk
  artifacts, with the pack's linters re-run over the outputs by the scorer.
- **Limits, stated rather than hidden**: the README asks each query three
  times — this run asked once per query per model (28 probes), so routing
  nondeterminism is sampled, not characterised. Probes saw only the 28-skill
  family list; the machine's full roster is larger, and the scenario agents ran
  against that full roster (the harness loads every installed skill). The Agent
  tool exposes model aliases (`haiku`, `sonnet`), not snapshot ids — the exact
  model id behind an alias is not resolvable from this harness and is not
  claimed. Scenario runs were interactive-free: lines that would need a human
  in the loop (approval steps) were scored on what the agent did instead, and
  s01/s03 record `draft`/`proposed` statuses for exactly that reason.
