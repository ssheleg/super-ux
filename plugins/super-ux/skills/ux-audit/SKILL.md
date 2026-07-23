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

## Evidence discipline (non-negotiable)

Every verdict must cite `file:line` evidence. Could not find or verify
something? The verdict is **BLOCKED** with the exact reason — never a guess,
never a courtesy PASS. An audit that flatters the codebase is worthless.

## Depth levels

| Depth | Passes run |
|---|---|
| `quick` | 1. Scenario pass only |
| `standard` (default) | 1. Scenario pass + 2. Flow conformance |
| `deep` | 1–2 + 3. Heuristic pass (PRN-01..16) + 4. Practice pass (selection protocol) + 5. Coverage pass |

Passes:

1. **Scenario pass** — the loop below: code vs every scoped scenario.
2. **Flow conformance** — code vs flow diagrams: every node reachable,
   every edge (incl. error edges) wired, screen states from the flow table
   present.
3. **Heuristic pass** — implemented flows vs PRN-01..16
   ([ux-design-principles.md](../references/ux-design-principles.md));
   findings `[PRN-NN] (severity) node — issue -> fix`.
4. **Practice pass** — per
   [practice-selection.md](../references/practice-selection.md): profile →
   mandatory sets + per-artifact checklists (money flows get their rows);
   output a compliance table (applied / adapted / rejected / deferred /
   **missing** — applicable but absent, as suggestion findings `[BP-NNN]`).
   Respect recorded user-owned rejections — don't re-litigate them.
5. **Coverage pass** — the chain itself: orphan stories/flows/scenarios,
   journey stages without scenarios, jobs without stories, unused personas.

## The loop

1. **Scope.** Read the base (and foundation/flows, if present). Scope is
   `$ARGUMENTS` if given (`all`, `feature:<name>`, `SCN-010..SCN-020`,
   `coverage`, `practices`, `heuristics`), default `all`; depth keyword
   (`quick`/`deep`) selects the depth, default `standard`. Single-pass
   scopes (`coverage`/`practices`/`heuristics`) run just that pass. Note
   the git SHA of `docs/ux` — it goes into the report header. Skip
   `retired` scenarios.
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
7. **Produce the UX plan.** With the user's go-ahead, turn FAIL/PARTIAL
   findings into `docs/ux/plans/YYYY-MM-DD-<scope>.md` per the contract's
   UX-plan format: target interface per affected screen (elements, states,
   behavior) + a CREATE/MODIFY/DELETE change table where every row traces
   to scenario/flow/finding/principle IDs, prioritized by Frequency ×
   Severity × Solvability (worst user damage first, not the easiest diff).
8. **Offer autonomous execution.** Point at the plan file and offer — don't
   auto-run — the project's pipeline: task-pipeline plugin
   (`/task-pipeline` on the plan) if installed, else superpowers
   writing-plans → subagent-driven execution. The plan is written to be
   executable without this conversation.

## Pass semantics

Heuristic (`PRN-NN`) and practice (`BP-NNN`) findings are suggestions —
opportunities, never blockers; they don't change scenario verdicts, unless
the violation breaks a scenario (then it's a normal finding on that
scenario). Practices are opportunities selected by the protocol, not a
style gate.

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
