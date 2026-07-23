# Figma File Structure — How the Agent Builds & Navigates

How to organize a project's Figma file so an agent finds any screen
deterministically, keeps it in sync with `screens.md`, and never gets lost.
The workflow (when to ask, MCP preflight, sync) lives in
[figma-integration.md](figma-integration.md); this is the file's internal
structure and the naming that ties Figma to the super-ux chain. Practices:
BP-091..BP-100 in [best-practices.md](best-practices.md).

## The one idea: names ARE the index

Every Figma object is named to match a super-ux ID, so mapping is 1:1 and
lookup is deterministic — no hunting, no guessing.

```
screens.md  SCR-01 "Welcome", state "empty"
      │  same key
      ▼
Figma      page "FLW-01 · Create project" → frame "SCR-01/Welcome/empty"
```

To find a screen's frame: read the `SCR-ID` in `screens.md`, open the flow's
page, select the frame `SCR-NN/<Screen>/<state>`. To update after a code
change: same path, edit the frame, refresh the deep-link in that screen's
States table. That is the whole navigation model.

## Page order (BP-091, BP-092)

```
1. Cover            file name · status · owner · last-updated (a component)
2. Index            table: page → flow/feature, quick links
3. Design system    tokens, primitives, semantic aliases, components (or a linked library)
4. FLW-01 · <name>  all frames for flow 1
5. FLW-02 · <name>  …
…
N. Scratch          drafts / explorations (kept out of the working pages)
```

- One page per flow or tight feature group; page name starts with the
  `FLW-ID` (or feature name) so it's findable from `flows.md`.
- Drafts live on Scratch (or a separate file), never mixed into working
  pages — clutter slows load and confuses navigation.

## Frame naming (BP-093) — the backbone

- `SCR-NN/<Screen>/<state>` per screen-state that matters, e.g.
  `SCR-03/Paywall/error`. Slash nesting groups them in the layer panel.
- States use the contract vocabulary: `loading` `empty` `error` `success`
  (plus meaningful extras like `default`, `first-run`).
- Exactly the states listed in that screen's `screens.md` States table —
  no more, no fewer. A missing frame for a listed state is a drift finding;
  a frame with no state row is an orphan.
- The frame's deep-link goes into the States table's Figma cell; the page's
  link goes into the Index `Figma` column.

## Components, variants, tokens (BP-094..BP-098)

- **Naming:** purpose, not appearance, and matching code — `button/primary`,
  `input/default`, `color/background/subtle`, `spacing/gap/md`. Slash `/`
  creates the nested groups.
- **Variables = tokens, three tiers:** primitive → semantic alias →
  component reference; grouped into collections (color / spacing / type);
  modes for light/dark/density. Components reference semantic tokens, never
  raw values.
- **Variants vs components:** variants = states/sizes of ONE object;
  different objects = different components. Every interactive component
  carries hover / active / disabled / loading / error variants — these are
  the same states scenarios and PRN-01/PRN-09 demand.
- **Auto layout on every container** (hug/fill, token padding/gap); absolute
  position only for true overlays. This is what makes frames translate to
  real layout code.
- **Reuse the existing library** (`get_libraries` / `search_design_system`)
  before creating anything; fork only with a recorded reason.

## Layer hygiene (BP-099)

Rename layers that carry meaning (`nav`, `primary-cta`, `error-text`); group
by structure; delete hidden/orphan layers; keep the tree shallow. Figma
code-gen and Figma AI read the layer tree — meaningful names produce
meaningful code. Skip renaming purely decorative leaves.

## Recording the convention (BP-100)

`screens.md` → Design system records: the Figma library/file URL, the token
locations (Figma collections ↔ code token files), the naming convention in
force, and the governance owner who keeps Figma and code tokens in sync.
One convention, agreed up front, one owner — start simple, evolve on
friction.

## What the agent checks (maintenance)

- Every `screens.md` screen-state has a matching, correctly-named frame with
  a live deep-link (the linter flags empty frame cells; frame existence and
  naming are verified against Figma when the MCP is connected).
- No orphan frames (a frame whose `SCR-ID`/state isn't in `screens.md`).
- New screens build on library components/tokens, not one-offs.
- Page and frame names still match the current `flows.md`/`screens.md` IDs
  after any rename.
