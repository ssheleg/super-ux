---
name: ux-audit
description: Use when verifying the codebase against the UX scenario base - runs a batched, evidence-backed scenario audit and writes a versioned report to docs/ux/audits/. Triggers - "ux audit", "UX-аудит", "прогони по сценариям", pre-release UX verification, "check all buttons/states/errors", scenario compliance check.
---

# ux-audit — Scenario Audit Loop

Verify that the code actually delivers every scenario in
`docs/ux/scenarios.md`: every step reachable, every button present, every
state handled, every error honest. Output: a versioned report in
`docs/ux/audits/` plus updated audit statuses in the base.

**Format contract:** [scenario-format.md](../references/scenario-format.md)
(ux-contract v2) — report structure, verdicts (PASS / PARTIAL / FAIL /
BLOCKED), severities.

**Precondition:** `docs/ux/scenarios.md` exists. If it doesn't, stop and run
the `ux-scenarios` skill first — there is nothing to audit against.

**Full context:** when `docs/ux/foundation.md` exists, audit each scenario
WITH its chain — load the traced story's acceptance criteria (Given/When/
Then) as additional checks, and note whether the implementation actually
serves the job and journey stage, not just renders the elements. A flow
whose buttons all exist but whose job outcome is unreachable is PARTIAL at
best. When `docs/ux/flows.md` exists, also verify the code implements the
flow diagram: every node reachable, every edge (including error edges)
wired, screen states from the flow's table present — unimplemented
nodes/edges are findings on the traced scenarios.

**Heuristic pass (optional, scope `heuristics`):** walk implemented flows
against PRN-01..16 from
[ux-design-principles.md](../references/ux-design-principles.md); record
violations `[PRN-NN] (severity) node — issue -> fix`. Complements the
practices pass (`BP-NNN`); same suggestion semantics unless the violation
breaks a scenario (then it's a normal finding).

## Evidence discipline (non-negotiable)

Every verdict must cite `file:line` evidence. Could not find or verify
something? The verdict is **BLOCKED** with the exact reason — never a guess,
never a courtesy PASS. An audit that flatters the codebase is worthless.

## The loop

1. **Scope.** Read the base (and foundation, if present). Scope is
   `$ARGUMENTS` if given (`all`, `feature:<name>`, `SCN-010..SCN-020`,
   `coverage`), default `all`. Note the git SHA of `docs/ux` — it goes into
   the report header. Skip `retired` scenarios. Scope `coverage` audits the
   chain instead of the code: orphan stories/scenarios, journey stages
   without scenarios, jobs without stories, unused personas — same report
   format, findings reference layer IDs; skip steps 3's code checks.
2. **Batch.** Group scoped scenarios by feature, ~5–8 per batch. List the
   batches before starting so progress is visible.
3. **Audit each batch.** For large scopes dispatch parallel subagents — one
   batch per subagent, each returning per-scenario verdicts with evidence.
   Per scenario check, against the code:
   - entry point exists and is reachable;
   - every numbered step has a corresponding implementation path;
   - every listed UI element exists and is wired to a handler;
   - every listed state (loading / empty / error / success) has a rendering
     branch;
   - every listed error is surfaced to the user honestly (no silent catch,
     no fake success) with the described recovery;
   - the expected result observably occurs.
   Any gap → PARTIAL (or FAIL if the flow is missing/broken) with a finding
   `[AUD-YYYY-MM-DD-NN] (severity) description -> suggested fix`.
4. **Write the report** to `docs/ux/audits/YYYY-MM-DD[-scope].md` per the
   contract, batch by batch as results arrive — a crashed run must leave the
   completed batches on disk.
5. **Summarize.** Totals, top issues (worst user damage first), prioritized
   recommended actions. The summary must be readable standalone by someone
   who won't open the batch details.
6. **Update the base.** `Last audit` column (`YYYY-MM-DD VERDICT`) for every
   audited scenario; flip `validated` → `implemented` where the audit
   PASSed; never touch scenario content itself during an audit.
7. **Offer planning handoff.** Offer — don't auto-run — to turn FAIL/PARTIAL
   findings into a work plan via the project's planning workflow
   (superpowers writing-plans, task-pipeline, or the user's framework of
   choice). Prioritize findings by Frequency × Severity × Solvability (how
   many users/scenarios hit it × how badly it breaks the job × how cheaply
   it's fixed); the plan fixes the worst user damage first, not the easiest
   diff.

## Optional practices pass

On request (or scope `practices`), review scenarios and implementation
against [best-practices.md](../references/best-practices.md): select
practices by tags matching the product's stages and domain, check which
apply-but-are-absent. Report as `suggestion` findings referencing `BP-NNN`
(e.g. "[BP-013] permission asked without value preview") — practices are
opportunities, never blockers; they don't change scenario verdicts.

## Optional live pass

If the project has a runnable dev server and browser tooling is available,
replay the top scenarios live after the static pass: walk the steps as the
user, screenshot or transcribe what actually renders, and attach observed
evidence to the verdicts. Live evidence overrides static evidence when they
disagree. Off by default; offer it when the tooling is present.

## Definition of done

- Every scoped scenario has a verdict with evidence or an explicit BLOCKED
  reason — no scenario silently skipped.
- Report on disk, summary honest, base statuses updated.
- Findings offered to planning; nothing swallowed.
