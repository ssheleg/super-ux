# Figma Integration (optional design surface, default ON)

super-ux designs the UX chain in markdown (foundation → flows → screens →
scenarios). When the user wants visual mockups, the same design work is
mirrored into **Figma** via the Figma MCP — every frame built from the flow's
screen/state spec, the recorded style pack, and the visual-craft practices
(BP-079..090). This is an opt-in capability, **enabled by default**;
text-only design is always a valid fallback.

## Contents

- [When to ask](#when-to-ask)
- [Preflight (only when Figma is chosen)](#preflight-only-when-figma-is-chosen)
- [Which tool for which job](#which-tool-for-which-job)
- [Recording the file (foundation.md → Design tooling)](#recording-the-file-foundationmd--design-tooling)
- [Design loop with Figma (inside ux-flows Design)](#design-loop-with-figma-inside-ux-flows-design)
- [Improve mode with Figma](#improve-mode-with-figma)
- [Keeping Figma in sync (same-change rule)](#keeping-figma-in-sync-same-change-rule)
- [Boundaries](#boundaries)


## When to ask

At the START of any design task (`/ux` step 0, `ux-flows` Design), ask once,
plainly:

> "Design the interface visually in Figma as we go (mockups you can open and
> edit), or keep it text-only? (Figma is the default.)"

Record the answer in `foundation.md` → Design tooling (below). Don't ask
again per flow — the project-level choice holds until the user changes it.

## Preflight (only when Figma is chosen)

1. **MCP present?** Check for the official Figma MCP tools (`use_figma`,
   `get_design_context`, `get_metadata`, `create_new_file`). If absent,
   recommend connecting it — do NOT block the chain:
   > "Figma design needs the Figma MCP connected. Add it via /mcp (or your
   > claude.ai connectors), then I'll mirror mockups as we design. Until
   > then I'll keep the markdown flows and wireframes, and sync to Figma
   > once it's connected."
   Continue text-only; the flows/wireframes are the source of truth and
   Figma catches up later.
2. **Load Figma's own skill first — every time.** The MCP gates its main
   tools behind guidance skills, and skipping them is the most common cause
   of hard-to-debug failures. Before `use_figma` → `/figma-use`; before
   `create_new_file` → `/figma-create-new-file`; before `get_design_context`
   → `/figma-design-to-code`. If the slash-command form isn't installed,
   read the equivalent MCP resource (`skill://figma/<name>/SKILL.md`, listed
   by the server's own skill tools). These are the API's rules, not
   super-ux's — follow them verbatim and don't hand-guess the calls.
3. **File location recorded?** If Design tooling has no Figma file yet,
   create one — `whoami` first for the plan key (ask which team/org when the
   user has several), then `create_new_file` with `editorType: "design"` —
   or ask the user for the target file URL. Write the URL into
   `foundation.md` immediately, before drawing anything, so the location is
   never lost.
4. **Design system?** If the project has a Figma library / design system,
   pull it (`get_libraries` / `search_design_system`) and build on its
   components and tokens instead of inventing new ones. `get_variable_defs`
   reads the variables (tokens) already defined on a node — use it to check
   what exists before creating a parallel set.
5. **Style pack?** If there is no design system yet, settle the visual
   identity BEFORE drawing: read `screens.md` → Design system → `Style pack`,
   and when it's empty use the **sheleg-design** companion skill to pick one
   (or offer its one-time install once, then continue either way). Its token
   file becomes the Figma variable collections. Full protocol and the
   division of labor: [visual-identity.md](visual-identity.md).

**File structure & naming:** organize the file and name pages, frames,
components, and tokens per [figma-structure.md](figma-structure.md)
(BP-091..BP-100). The key rule: frames are named `SCR-NN/<Screen>/<state>`
to match `screens.md` exactly, so lookup is deterministic and drift is
checkable.

## Which tool for which job

Names from the official Figma MCP. Treat the list as a map, not a contract:
if a tool is missing in the user's setup, degrade to what is there and say
so — never invent a call.

| Need | Tool |
|---|---|
| Write anything into Figma (frames, components, variables, layout, fixes) | `use_figma` — runs JS against the Plugin API; **load `/figma-use` first** |
| Capture a *web app* page pixel-perfect the first time | `generate_figma_design` where the setup exposes it (run beside `use_figma`, which rebuilds it on design-system components). Non-web and from-scratch work: `use_figma` only |
| A new file to work in | `whoami` → `create_new_file` (`editorType` design / figjam / slides); **load `/figma-create-new-file` first** |
| Read a design for implementation (code + screenshot + context) | `get_design_context`; **load `/figma-design-to-code` first** |
| Cheap structure read — does the frame exist, is it named right | `get_metadata` (node ids, names, types, sizes; omit `nodeId` to list pages) |
| Just the picture | `get_screenshot` |
| Tokens already defined on a node | `get_variable_defs` |
| The project's library / design system | `get_libraries`, `search_design_system` |
| Icons, illustrations, exports in or out | `download_assets`, `upload_assets` |
| Figma ↔ code component mapping (deepens `Coverage`) | `get_code_connect_map`, `get_code_connect_suggestions`, `add_code_connect_map` — `get_design_context` already uses Code Connect when it's set up |
| Mirror a flow onto a FigJam board | `get_figjam`, `generate_diagram` (`/figma-use-figjam`) |

`node-id` comes from the frame's URL (`?node-id=1-2` → `1:2`); a file key
from `figma.com/design/:fileKey/...`. Both live in `screens.md` links
already, which is why the deep-links are worth keeping accurate.

## Recording the file (foundation.md → Design tooling)

`foundation.md` → Design tooling records the on/off choice and the file
URL. The **design system** details and all **per-screen/per-state frame
links** live in `screens.md` (the UI map):

```markdown
## Design system            (in screens.md)
- **Style pack:** <sheleg-design pack, or "none — platform defaults">
- **Figma library:** <url/name, or "none">
- **Tokens in code:** <src/theme/tokens.ts>
- **Component source:** <src/components/>
- **Assets:** <icons/illustrations location>
```

**Every screen state has a frame link.** In `screens.md` each screen's
States table carries a Figma frame deep-link per state (success / empty /
error / loading). No state in a Figma-enabled project is without its frame
link; a state with an empty frame cell is an incomplete-design finding. The
Index's `Figma` column links the screen's page for quick access.

## Design loop with Figma (inside ux-flows Design)

For each flow, AFTER the flow diagram + screen/state table are agreed:

1. Build the mockup in Figma from the flow's screen list and each screen's
   declared states (loading / empty / error / success) — one frame per
   screen-state that matters, on the flow's page.
2. Build on the recorded **style pack** (visual-identity.md): its tokens
   become the file's variable collections, its type scale/spacing/motion the
   frame defaults, its bans hard limits. Then apply the visual-craft
   practices as hard constraints, not suggestions — the pack supplies the
   values, the practices are the floor they must clear:
   type system and 16/1.5/45–75 reading spec (BP-079..081), 60-30-10
   palette with one scarce accent and semantic-color contract
   (BP-082..083), dark-mode palette if in scope (BP-084), 4/8pt spacing and
   proximity grouping (BP-085..087), tabular figures for data (BP-088),
   verb/sentence-case microcopy (BP-089), decoration subtraction (BP-090) —
   plus the platform language (BP-053) and tap-target floors (BP-050).
3. One primary action per frame, visually dominant (screen rules in
   [ux-design-principles.md](ux-design-principles.md)); every interactive
   element meets the target-size floor.
4. Structure the file and name every frame per
   [figma-structure.md](figma-structure.md): the flow's page named
   `FLW-NN · <name>`, each frame `SCR-NN/<Screen>/<state>`, built on the
   library's components and token variables (BP-093..BP-098). Follow the
   Figma MCP's own skills for the API — `/figma-use` before every
   `use_figma` call, `/figma-generate-design` when translating a whole page
   or view, `/figma-create-new-file` before creating a file. Don't
   hand-guess the calls.
5. Write each state's frame deep-link into that screen's States table in
   `screens.md`, and the screen's page link into the Index `Figma` column.
   Present the mockup for approval alongside the flow.

The compliance table (practice-selection protocol) records the visual-craft
BPs as `applied` with the Figma frame as their evidence.

## Improve mode with Figma

When improving existing UX and Figma is on: import current screens
(`get_design_context` — load `/figma-design-to-code` first — or
`get_screenshot` from a provided file, or build from code), produce
before → after frames next to the flow's before → after diagrams, and cite
the same `PRN-NN`/`BP-NNN` on the redesigned frames.

## Keeping Figma in sync (same-change rule)

When an interface changes and Figma is enabled: update the affected frame(s)
AND their links in `screens.md` in the same change as the code/flow change —
never leave the map pointing at a stale or deleted frame. A screen whose
code diverges from its `screens.md` record, or whose Figma link is broken/
stale, is a `drifted` finding surfaced by audits. The registry (`screens.md`)
is the index that makes this checkable: one row per screen, one frame per
state, coverage to code — the single place that ties UX, UI, Figma, and code
together.

## Boundaries

- Figma is a rendering of the chain, never a replacement: flows, screens,
  and scenarios remain the source of truth; a frame that drifts from its
  screen record is a finding.
- Never let a missing/unauthenticated MCP block design — degrade to
  markdown + wireframes and sync later.
- Don't publish or share the Figma file anywhere; the user owns
  distribution.
