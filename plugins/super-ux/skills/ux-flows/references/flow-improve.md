# Improve: heuristic evaluation to redesign

The procedure `ux-flows` runs in its Improve workflow. Moved here from the skill
body on 2026-10-20 to keep that body inside its token budget; the text is unchanged
apart from link paths.

Follow the improvement procedure in the principles doc, strictly:

1. Prerequisite: flows exist (run Reverse first if not).
2. Walk every flow against PRN-01..24 + journey pains; record violations
   `[PRN-NN] node — what breaks — severity (4..1)`.
3. Redesign proposals: trace to a pain/job/story; cite `PRN-NN`/`BP-NNN`;
   show flow before → after (two mermaid diagrams); state the expected
   observable effect. No untraced "make it nicer" changes. When Figma is
   enabled, produce before → after frames beside the diagrams
   ([figma-integration.md](figma-integration.md)).
4. Approved proposals land in THREE places, same session: flow Updates
   (+ scenario cascade) AND a concrete UX plan
   (`docs/ux/plans/YYYY-MM-DD-<scope>.md`, contract format): target
   interface per screen + CREATE/MODIFY/DELETE table, every row traced,
   prioritized Frequency × Severity × Solvability.
5. Hand the plan to delivery. Say what the user has in hand (this plan, the
   `docs/ux/` chain, Figma frames). The ssheleg **task-pipeline** plugin
   implements it: installed → `/task-pipeline <plan file>`; not installed →
   its optional one-time install is in `system-map.md` → Companions, or
   implement by hand. Same-change rule holds; re-audit after.
