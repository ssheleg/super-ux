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
- [Recording the files (foundation.md → Design tooling)](#recording-the-files-foundationmd--design-tooling)
- [Design loop with Figma (inside ux-flows Design)](#design-loop-with-figma-inside-ux-flows-design)
- [Improve mode with Figma](#improve-mode-with-figma)
- [Keeping Figma in sync (same-change rule)](#keeping-figma-in-sync-same-change-rule)
- [Boundaries](#boundaries)
- [Sources](#sources)


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
3. **Files recorded — one per surface?** A product's Figma is a **set of
   files in the product's folder**, one per surface it has: **App** (the
   product's screens), **Web** (landing, pricing, docs pages), **ASO** (store
   screenshots, icon, preview frames). One file for everything mixes three
   audiences, three review cadences and three export pipelines, and the
   surfaces nobody recorded go missing first. For each surface the product
   has and Design tooling does not list yet, create the file — `whoami`
   first for the plan key (ask which team/org when the user has several),
   then `create_new_file` with `editorType: "design"` in the product's
   folder — or ask the user for its URL. Write each URL into `foundation.md`
   → Design tooling immediately, before drawing anything, so no location is
   ever lost. A surface the product does not have gets no file.
4. **Design system?** If the project has a Figma library / design system,
   pull it (`get_libraries` / `search_design_system`) and build on its
   components and tokens instead of inventing new ones. `get_variable_defs`
   reads the variables (tokens) already defined on a node — use it to check
   what exists before creating a parallel set.
5. **Style pack?** If there is no design system yet, settle the visual
   identity BEFORE drawing: read `screens.md` → Design system → `Style pack`,
   and when it's empty `/sheleg-design` decides it (or offer its one-time
   install once, then continue either way). An underdetermined brief draws
   **one key screen in one state** first and gets its direction picked on a
   2-up sheet before any other frame exists. The chosen pack's token file
   becomes the Figma variable collections. Full protocol and the division of
   labor: [visual-identity.md](visual-identity.md).

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
| Capture a *web app* page pixel-perfect the first time | `generate_figma_design` where the setup exposes it, **into the surface's recorded file** (Improve mode below; run beside `use_figma`, which rebuilds it on design-system components). Non-web and from-scratch work: `use_figma` only |
| Annotate a frame, mark it ready for dev, attach a code link | `use_figma` — `annotations`, `devStatus` (read it back), `addDevResourceAsync` (design loop steps 5 and 7) |
| A new file to work in | `whoami` → `create_new_file` (`editorType` design / figjam / slides); **load `/figma-create-new-file` first** |
| Read a design for implementation (code + screenshot + context) | `get_design_context`; **load `/figma-design-to-code` first** |
| Cheap structure read — does the frame exist, is it named right | `get_metadata` (node ids, names, types, sizes; omit `nodeId` to list pages) |
| Just the picture | `get_screenshot` |
| Tokens already defined on a node | `get_variable_defs` |
| The project's library / design system | `get_libraries`, `search_design_system` |
| Icons, illustrations, exports in or out | `download_assets`, `upload_assets` |
| Figma ↔ code component mapping (deepens `Coverage`) | `/figma-code-connect` first; `get_code_connect_map`, `get_code_connect_suggestions`, `send_code_connect_mappings`, `add_code_connect_map` — `get_design_context` already uses Code Connect when it's set up, and the mapping moves with the component's API (same-change rule below) |
| Mirror a flow onto a FigJam board | `get_figjam`, `generate_diagram` (`/figma-use-figjam`) |

`node-id` comes from the frame's URL (`?node-id=1-2` → `1:2`); a file key
from `figma.com/design/:fileKey/...`. Both live in `screens.md` links
already, which is why the deep-links are worth keeping accurate.

## Recording the files (foundation.md → Design tooling)

`foundation.md` → Design tooling records the on/off choice, the folder and
**one file per surface**:

```markdown
## Design tooling           (in foundation.md)
- **Figma:** enabled
- **Figma folder:** <team / project the product's files live in>
- **Figma files:**
  | Surface | File | Holds |
  |---------|------|-------|
  | App | <url> | every SCR-NN frame of the product |
  | Web | <url> | landing, pricing, docs pages |
  | ASO | <url> | store screenshots, icon, preview frames |
```

A row per surface the product actually has; a missing row is a surface with
no design home. The **design system** details and all **per-screen/per-state
frame links** live in `screens.md` (the UI map):

```markdown
## Design system            (in screens.md)
- **Style pack:** <the pack /sheleg-design chose, or "none — platform defaults">
- **Director record:** <docs/design/<surface>/director-record.md, or "none — sheleg-design not installed">
- **Axes:** viewport: <widths>; theme: <themes>; text: <sizes>; locale: <locales>
- **Figma library:** <url/name, or "none">
- **Tokens in code:** <src/theme/tokens.ts>
- **Component source:** <src/components/>
- **Assets:** <icons/illustrations location>
```

**`none` declines a pack, not the floor.** With `sheleg-design` installed,
its `SLOP_MARKERS.md` catalogue applies to every frame under `Style pack:
none` exactly as under a pack: its `review` rows are read in the critique
below, and where code exists `npx sheleg-design-skill --lint <dir>` runs and
its result is recorded. Companion absent, or a version without `--lint` →
`Markers: NOT_RUN — <reason>`, never a pass.
[visual-identity.md](visual-identity.md) has the table.

**Every screen state has a frame link.** In `screens.md` each screen's
States table carries a Figma frame deep-link per declared state — `default`,
`loading`, `empty`, `error`, `offline`, `long-content`, `keyboard-up`,
`first-run`, whichever apply. No state in a Figma-enabled project is without
its frame link; a state with an empty frame cell is `U020`. The Index's
`Figma` column links the screen's page for quick access.

## Design loop with Figma (inside ux-flows Design)

For each flow, AFTER the flow diagram + screen/state table are agreed. The
**flow approval** is about those two — structure and behaviour — and is never
given or withheld on how a frame looks:

0. **Direction first, when the brief is underdetermined.** One key screen in
   one state, two directions only when the fork is real, the human picks on
   a 2-up mini sheet; only then the remaining frames
   ([visual-identity.md](visual-identity.md) → Directions before frames).
1. Build the mockup in Figma from the flow's screen list and each screen's
   declared states — one frame per screen-state, on the flow's page, in the
   App, Web or ASO file the surface belongs to.
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
   **Then annotate the frame natively.** Each frame carries one Figma
   annotation, set through `use_figma` (`frame.annotations = [{ labelMarkdown
   }]`), naming the scenario id(s) the state serves, the state, and the
   `PRN-NN` heuristics it was built against:
   `SCN-004 · state: error · PRN-03, PRN-09`. Figma's own guidance is to
   annotate "design intent that's hard to capture from visuals alone"
   ([structure your file](#sources)); in this chain the intent is those ids,
   and an annotation travels with the frame into Dev Mode where the
   `screens.md` row does not. A frame with no annotation is unfinished, not
   decorative; the same `get_metadata` pass that checks names reads them back.
6. **Resize each frame across its viewports, then critique it.** Before the
   critique, read the screen's `Axes: viewport` widths (its own line, or the
   Design system default) and resize the frame to each one through
   `use_figma` (`frame.resize(width, frame.height)`), take a `get_screenshot`
   at each width, and put the frame back at its designed width. Record one
   line per frame in the critique — `resize: 360 ok, 768 ok, 1280 fails (nav
   wraps under the logo)` — and write each failing width as a triple like any
   other finding. Figma: "Resize the frame in Figma to check that it behaves
   as expected before generating code" ([structure your file](#sources)).
   This is the narrow-width check BP-134 runs on the build, moved to where a
   fix costs a frame instead of a component; a frame laid out in absolute
   positions cannot reflow, and that is the finding (auto layout,
   [figma-structure.md](figma-structure.md)). No `use_figma` in the session →
   `resize: NOT_RUN`, said in the approval request.

   **Critique the frames before anyone approves them.** `get_screenshot`
   each frame (the key screen's first, then every new state) and read the
   picture — not the layer tree — against the director record's `Rubric`
   (sheleg-design), the `SLOP_MARKERS.md` `review` rows and the BP-079..090
   floors. Write every finding as a triple, **region → defect → fix**
   ("hero, top third → two competing accents → keep the brand accent, mute
   the badge"), fix it, and re-render within a budget of one round, two at
   most; what is still open after that goes to the human as `unresolved`,
   not into a third round. The triples go into the director record's
   `Critique`; with no director record (companion absent), into the flow
   entry, and the rubric used is the floors plus the pack's bans, said so.
   No `get_screenshot` in the session → the critique is `NOT_RUN`, and the
   approval request says so instead of implying the frames were looked at.
7. **Art-direction approval is a second decision.** Present the frames with
   the critique beside them and ask for the look: the art-direction approval,
   separate from the flow approval (`ux-flows` step 8 presents both). Record it on the flow:
   `**Art direction:** approved <date> — critique: <director record#critique
   or link>`. An approval that cites no critique is `U085`.

   **Then hand the approved frames to dev**, frame by frame:
   - **Link the scenario and the code.** Extend the frame's annotation with
     the scenario's home and the code path from the screen's `Coverage`
     line: `SCN-004 in docs/ux/scenarios.md · code:
     src/onboarding/Welcome.tsx`. No code yet → `code: none yet`, filled by
     the change that builds the screen (same-change rule below). Where the
     code is reachable by URL, also attach it as a dev resource
     (`frame.addDevResourceAsync(url, name)`), which Figma surfaces on the
     layer in Dev Mode ([structure your file](#sources)).
   - **Mark it ready for dev.** The Plugin API declares `devStatus` writable:
     `frame.devStatus = { type: 'READY_FOR_DEV', description: 'Art direction
     approved <date>' }`, on a node directly under a page or section, never
     inside another node that already has a status ([Plugin API](#sources)).
     The frames sit directly on the flow page, so the restriction holds. Read
     the property back in the same `use_figma` call. The Figma MCP's own
     documentation does not say that `use_figma` accepts this write on every
     plan and seat, so a throw, or a read-back that is not `READY_FOR_DEV`,
     is not retried: fall back to the convention, stated as one. The
     annotation's first line becomes `Ready for dev · <date>`, the frame
     moves into a section named `Ready for dev` on its flow page, and the
     flow records `**Dev status:** annotation only — <the error>`. A frame is
     reported as marked only when the read-back showed the status.

The compliance table (practice-selection protocol) records the visual-craft
BPs as `applied` with the Figma frame as their evidence.

## Improve mode with Figma

When improving existing UX and Figma is on, **capture what ships before
redesigning it**, into the file that already holds that surface:

- **Where.** The surface's **recorded** file — its App or Web row in
  `foundation.md` → Design tooling — on a page named `Captured · <date>`
  (page order in [figma-structure.md](figma-structure.md)). Never a new
  file, never drafts: a capture outside the recorded file is a location
  nobody wrote down, which Preflight step 3 exists to prevent. No row for
  that surface yet → create its file per Preflight step 3 first.
- **How, for a web surface.** `generate_figma_design` converts "live UI from
  your browser into editable Figma frames" ([code to canvas](#sources)).
  Pass it the recorded file's URL, and confirm that URL is a Design file
  first (`get_metadata` on it): Figma's documentation says that when "the
  URL doesn't correspond to a Figma Design file, your client defaults to
  creating a new file instead". Writing into an existing file outside
  drafts needs a Full seat and edit permission (same page). Without them,
  stop and say so; do not capture somewhere else. Name the captured frames
  `SCR-NN/<Screen>/<state>` like any other page.
- **Otherwise.** A non-web surface, or a setup without
  `generate_figma_design`: import onto the same `Captured` page with
  `get_screenshot` from a provided file, `get_design_context` (load
  `/figma-design-to-code` first) or a rebuild from code, and say which.

The captured page is the **before** and stays as captured: it is evidence,
not a draft. Produce the after frames on the flow's page next to the flow's
before → after diagrams, and cite the same `PRN-NN`/`BP-NNN` on the
redesigned frames.

## Keeping Figma in sync (same-change rule)

When an interface changes and Figma is enabled: update the affected frame(s)
AND their links in `screens.md` in the same change as the code/flow change —
never leave the map pointing at a stale or deleted frame. A screen whose
code diverges from its `screens.md` record, or whose Figma link is broken/
stale, is a `drifted` finding surfaced by audits. The registry (`screens.md`)
is the index that makes this checkable: one row per screen, one frame per
state, coverage to code — the single place that ties UX, UI, Figma, and code
together.

**Core components carry a Code Connect mapping, and it moves with their
API.** A component the screens repeat (button, input, card, nav item; the
set [figma-structure.md](figma-structure.md) names) is mapped to its code
component with `/figma-code-connect` (the Figma MCP's skill;
`get_code_connect_suggestions`, then `send_code_connect_mappings` or
`add_code_connect_map`). Figma calls this "the #1 way to get consistent
component reuse in code" ([structure your file](#sources)), and
`get_design_context` then hands the next agent the real component instead
of a guess. **A change that alters a mapped component's API** (a prop, a
variant, its import path) **updates its mapping in the same change** —
"When component APIs change in your codebase, update the corresponding Code
Connect mappings" ([Code Connect](#sources)). A stale mapping is worse than
none: it hands out a call that no longer compiles, with Figma's authority
behind it. A setup without Code Connect (the tools absent or refused) says
so on the Design system block, `Code Connect: none — <reason>`, rather than
leaving the gap unrecorded.

## Boundaries

- Figma is a rendering of the chain, never a replacement: flows, screens,
  and scenarios remain the source of truth; a frame that drifts from its
  screen record is a finding.
- Never let a missing/unauthenticated MCP block design — degrade to
  markdown + wireframes and sync later.
- Don't publish or share the Figma files anywhere; the user owns
  distribution.

## Sources

Read 2026-10-08. Quotes above are from these pages; where a page is silent,
the text above says so instead of filling the gap.

- Structure your file: <https://developers.figma.com/docs/figma-mcp-server/structure-figma-file/>
  (annotations, resizing frames, dev resources, Code Connect).
- Code to canvas: <https://developers.figma.com/docs/figma-mcp-server/code-to-canvas/>
  (`generate_figma_design`: targets, the new-file default, seat rules).
- Code Connect: <https://developers.figma.com/docs/figma-mcp-server/code-connect-integration/>
  (mapping upkeep when a component's API changes).
- Plugin API: <https://developers.figma.com/docs/plugins/api/DevStatus>,
  <https://developers.figma.com/docs/plugins/api/node-properties> (`devStatus`
  writable, its placement restriction) and
  <https://developers.figma.com/docs/plugins/api/Annotation> (`annotations`).
- Claude Code for designers: <https://www.figma.com/resource-library/claude-code-for-designers/>
  (the round trip these steps sit in: code pushed back to the canvas "as
  native layers you can edit", and Dev Mode for the hand-off).
