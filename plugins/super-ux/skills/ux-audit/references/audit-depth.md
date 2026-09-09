# Audit depth levels — how far each pass goes

Split out of `ux-audit/SKILL.md` on 2026-09-10, when its body measured 4882 tokens
past the house working limit of 4750. The depth a run picks is a LOOKUP made once at
the start; what stays in the SKILL is the loop that walks it.

## Contents

- [Audit depth levels — how far each pass goes](#audit-depth-levels--how-far-each-pass-goes)

| Depth | Passes run |
|---|---|
| `quick` | 1. Scenario pass only |
| `standard` (default) | 1. Scenario pass + 2. Flow conformance |
| `deep` | 1–2 + 3. Heuristic pass (PRN-01..24) + 4. Practice pass (selection protocol) + 5. Coverage pass |

Passes:

1. **Scenario pass** — the loop below: code vs every scoped scenario.
2. **Flow & screen conformance** — code vs flow diagrams (every node
   reachable, every edge incl. error edges wired) AND code vs `screens.md`
   (every registered screen's states rendered, elements present, `Coverage`
   accurate). A screen whose code diverges from its record → `drifted`
   finding; flip its Status to `drifted`. When Figma is enabled, check each
   state has a frame link and flag empty/obviously-stale links (a link the
   registry marks but the design lost); with the Figma MCP connected,
   `get_metadata` confirms the frame still exists under its expected
   `SCR-NN/<Screen>/<state>` name without pulling full design context.
   **A screen carrying a `Web surface:` block is checked against it too:**
   the route the code actually serves vs `Route`, whether the answer survives
   with JS disabled vs `Without JS`, whether the emitted structured data
   matches `Entity` and the visible content, and whether the indexation
   directives agree with `Indexable`. Divergence is `drifted` like any other.
   Where `screens.md` declares `Web surfaces: no` while the code serves a
   public route, that is a finding against the declaration, not the screen.
   The live-page audit — rendering, crawl reach, competitors, the SERP — is
   the **seo-aeo-audit** companion's job; this pass checks the record against
   the code, and hands the rest over rather than guessing at it.
3. **Heuristic pass** — implemented flows vs PRN-01..24
   ([ux-design-principles.md](ux-design-principles.md));
   findings `[PRN-NN] (severity) node — issue -> fix`.
4. **Practice pass** — per
   [practice-selection.md](practice-selection.md): profile →
   mandatory sets + per-artifact checklists (money flows get their rows);
   output a compliance table (applied / adapted / rejected / deferred /
   **missing** — applicable but absent, as suggestion findings `[BP-NNN]`).
   Respect recorded user-owned rejections — don't re-litigate them.
   Four dimensions this pass verifies in code rather than by discussion,
   because they fail silently: the reduced-motion branch exists for every
   animated surface and content survives without scroll effects (BP-131,
   BP-132); the page-weight budget is stated somewhere and the heavy pages
   meet it (BP-133); the narrow viewport and 200% zoom reflow hold, with no
   hover-only affordance (BP-134, BP-135); roles sit only where no native
   element says it, with every `aria-*` reference resolving (BP-136). An
   accessibility claim backed only by a scanner is BLOCKED, not PASS — the
   evidence is a keyboard and screen-reader walk of the top flows (BP-137).
   When `screens.md` → Design system records a `Style pack`
   ([visual-identity.md](visual-identity.md)), check the built UI
   honors it: tokens referenced instead of raw values, the pack's bans
   respected, dark mode from its twin — a screen ignoring the recorded pack
   is `drifted`, not a taste debate. No pack recorded and the visual layer
   looks improvised → suggest the **sheleg-design** companion once, as an
   opportunity finding.
5. **Coverage pass** — the chain itself: orphan stories/flows/screens/
   scenarios, journey stages without scenarios, jobs without stories, unused
   personas, screens not used by any flow, flows referencing missing
   `SCR-IDs`, screen states without Figma frames (when Figma enabled).
