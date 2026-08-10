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

## Closed

| id | Row | Closed by |
|---|---|---|
| B-006 | `graphify-out/graph.json` was stale at 756 nodes from 2026-08-06 — no `vision`, no new gates, no `docs/ux` or `docs/brand`. | Rebuilt 2026-08-10: **1091 nodes · 2111 edges · 71 communities** over 114 files. The recorded blocker — "needs an LLM key" — was a misread of the headless CLI path: with no `GEMINI_API_KEY`, semantic extraction falls to the host agent's own subagents, which is the documented default, not a degraded mode. Four subagents covered the 39 uncached docs; 59 came from the content-keyed cache. `--code-only` was never needed. Staleness block replaced by build notes in `GRAPH_REPORT.md`. |
