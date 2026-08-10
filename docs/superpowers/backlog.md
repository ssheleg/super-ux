# Board — super-ux

The work-list between runs. Stage 0 reads it and quotes the open count;
stage 10 files every unresolved ledger row here with an id.

Priority is derived, not assigned: **Frequency × Severity × Solvability**,
the same scale the UX plans use. A row with no evidence column is a wish,
not a task.

| id | Row | Priority | Source | Status |
|---|---|---|---|---|
| B-001 | `check_vision` warns when a `vision.md` exists with no alignment rule, but nothing checks that the rule installed by the `vision` skill still matches `templates/vision-rule.md` **in a target project**. The repo gate covers the shipped pair only. | 2×3×2 = 12 | audit 2026-08-10, stage 10 | open |
| B-002 | `validate_seeded_scripts` proves a command names both source and destination; it does not prove the destination path is the one the instruction tells the reader to run. A renamed destination in one of the two places would still pass. | 2×3×3 = 18 | audit 2026-08-10, stage 10 | open |
| B-003 | The B022 literal extractor is a regex, not a tokenizer. It cannot see strings inside multi-line template literals, so `usage()` is invisible to the registry. Documented in `docs/brand/strings.md` → Not registered; a real fix needs a per-language extractor. | 3×2×1 = 6 | dogfood 2026-08-10 | open |
| B-004 | `docs/ux/screens.md` records coverage as `file:line` ranges that no check re-resolves. `ux_lint.py` verifies coverage exists, not that it lands. The same class as `B023` in the brand linter, which does re-resolve. | 3×2×2 = 12 | dogfood 2026-08-10 | open |
| B-005 | `templates/vision.md` ships all nine headings with only comments beneath them. `read()` strips comments, so a project that seeds it and never writes a word lints clean until it is marked `approved`. The gate is status, and status is self-declared. | 2×2×3 = 12 | dogfood 2026-08-10 | open |
| B-010 | `test/ux_lint_test.py` exists but covers only `check_web_surface`. Every check that predates it — ID gaps, index sync, flow/screen references, traces, vision — still has no fixture, so the UX linter's older half is a gate nobody has watched fail. The brand linter has carried one per code since v0.30.0. | 3×2×2 = 12 | run 2026-08-10 | open |
| B-011 | A journey has no owner field. `JRN-NN` records stages, actions, pains and opportunities; nothing names who owns an opportunity or the map itself, and a map with no named owner is updated once and then forgotten. Source: michaelbell.co.uk *What is a user journey* (2026), which cites NN/g and Salesforce. Needs a contract field, a template row and a linter check. | 2×2×3 = 12 | run 2026-08-10 | open |
| B-012 | The copy brief takes four inputs (action, reader, their words, proof) and no success metric, no constraint, and no reference to the voice's newly required `Admired`/`Refused` pair. A marketing piece with no stated metric cannot be reviewed against anything but taste. Also unfiled: the NN/g finding that a reader consumes ~20–28% of the words on a page, which is the evidence under "front-load the answer" and currently appears nowhere. Source: ameliepollak.com *How to hire a B2B SaaS copywriter* (2026). | 2×2×3 = 12 | run 2026-08-10 | open |

## Closed

| id | Row | Closed by |
|---|---|---|
| B-006 | `graphify-out/graph.json` was stale at 756 nodes from 2026-08-06 — no `vision`, no new gates, no `docs/ux` or `docs/brand`. | Rebuilt 2026-08-10: **1091 nodes · 2111 edges · 71 communities** over 114 files. The recorded blocker — "needs an LLM key" — was a misread of the headless CLI path: with no `GEMINI_API_KEY`, semantic extraction falls to the host agent's own subagents, which is the documented default, not a degraded mode. Four subagents covered the 39 uncached docs; 59 came from the content-keyed cache. `--code-only` was never needed. Staleness block replaced by build notes in `GRAPH_REPORT.md`. |
| B-007 | **A public web surface had no home in the chain.** | Closed in v0.33.0. `screens.md` answers `Web surfaces: yes|no` once, and a public screen carries a five-field `Web surface:` block — `Route`, `Answers`, `Indexable`, `Without JS`, `Entity` — each the design-time twin of a check `seo-aeo-audit` runs on the live page. `check_web_surface` in `ux_lint.py` with 14 fixtures; `ux-flows` asks, `ux-audit` verifies, `seo-aeo-audit` becomes the third companion. Contract stays v4. |
| B-008 | **The plain-word routing table was thinner than the capability behind it.** | Closed in v0.33.0. Four rows added to `commands/ux.md`: funnel/monetization/pricing/checkout, design/visuals/style, SEO/findability, mobile app/platform — each routing to the action and the practice set that already existed behind it. |
| B-009 | **A composite request mapped to one route.** | Closed in v0.33.0. Step 0 of `/ux` now maps every matching row, orders them by chain position, and states the sequence in one line before running the first. |
