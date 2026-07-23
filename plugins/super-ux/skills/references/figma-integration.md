# Figma Integration (optional design surface, default ON)

super-ux designs the UX chain in markdown (foundation → flows → scenarios).
When the user wants visual mockups, the same design work is mirrored into
**Figma** via the Figma MCP — every frame built from the flow's screen/state
spec and the visual-craft practices (BP-079..090). This is an opt-in
capability, **enabled by default**; text-only design is always a valid
fallback.

## When to ask

At the START of any design task (`/ux` step 0, `ux-flows` Design), ask once,
plainly:

> "Design the interface visually in Figma as we go (mockups you can open and
> edit), or keep it text-only? (Figma is the default.)"

Record the answer in `foundation.md` → Design tooling (below). Don't ask
again per flow — the project-level choice holds until the user changes it.

## Preflight (only when Figma is chosen)

1. **MCP present?** Check for Figma MCP tools (e.g. `use_figma`,
   `generate_figma_design`, `create_new_file`, `get_design_context`). If
   absent, recommend connecting it — do NOT block the chain:
   > "Figma design needs the Figma MCP connected. Add it via /mcp (or your
   > claude.ai connectors), then I'll mirror mockups as we design. Until
   > then I'll keep the markdown flows and wireframes, and sync to Figma
   > once it's connected."
   Continue text-only; the flows/wireframes are the source of truth and
   Figma catches up later.
2. **File location recorded?** If Design tooling has no Figma file yet,
   create one (`create_new_file`) or ask the user for the target file URL,
   then write it into `foundation.md` immediately — before drawing anything,
   so the location is never lost.
3. **Design system?** If the project has a Figma library / design system,
   pull it (`get_libraries` / `search_design_system`) and build on its
   components and tokens instead of inventing new ones.

## Recording the file (foundation.md → Design tooling)

```markdown
## Design tooling
- **Figma:** enabled | disabled
- **Figma file:** <url>  (the single project file; one page per feature/flow group)
- **Design system:** <library name/url, or "none — using platform defaults">
```

**Every screen has a frame link.** The `flows.md` Screens & states table
gains a `Figma` column — one deep-link per screen (to its frame/node in the
design), and where states differ visually (empty / error), link those
frames too. No screen in a Figma-enabled project is without its frame link;
a screen with `Figma: —` is an incomplete-design finding. The flow entry
also carries a top-level `Figma:` link to the flow's page for quick access.

## Design loop with Figma (inside ux-flows Design)

For each flow, AFTER the flow diagram + screen/state table are agreed:

1. Build the mockup in Figma from the flow's screen list and each screen's
   declared states (loading / empty / error / success) — one frame per
   screen-state that matters, on the flow's page.
2. Apply the visual-craft practices as hard constraints, not suggestions:
   type system and 16/1.5/45–75 reading spec (BP-079..081), 60-30-10
   palette with one scarce accent and semantic-color contract
   (BP-082..083), dark-mode palette if in scope (BP-084), 4/8pt spacing and
   proximity grouping (BP-085..087), tabular figures for data (BP-088),
   verb/sentence-case microcopy (BP-089), decoration subtraction (BP-090) —
   plus the platform language (BP-053) and tap-target floors (BP-050).
3. One primary action per frame, visually dominant (screen rules in
   [ux-design-principles.md](ux-design-principles.md)); every interactive
   element meets the target-size floor.
4. Follow the Figma plugin's own skills for the API (`/figma-use` before
   `use_figma`, `/figma-generate-design` for translating a screen spec) —
   don't hand-guess the MCP calls.
5. Write each screen's frame deep-link into the Screens & states table's
   `Figma` column (and per-state frames where they differ), plus the flow's
   top-level `Figma:` page link. Present the mockup for approval alongside
   the flow.

The compliance table (practice-selection protocol) records the visual-craft
BPs as `applied` with the Figma frame as their evidence.

## Improve mode with Figma

When improving existing UX and Figma is on: import current screens
(`get_design_context` / `get_screenshot` from a provided file, or build from
code), produce before → after frames next to the flow's before → after
diagrams, and cite the same `PRN-NN`/`BP-NNN` on the redesigned frames.

## Boundaries

- Figma is a rendering of the chain, never a replacement: the flow diagram
  and scenarios remain the source of truth; a frame that drifts from its
  flow is a finding.
- Never let a missing/unauthenticated MCP block design — degrade to
  markdown + wireframes and sync later.
- Don't publish or share the Figma file anywhere; the user owns
  distribution.
