# Visual Identity — the sheleg-design companion (recommended, never forced)

super-ux decides **what the interface must be**: which screens exist, which
states they show, what each element does, which control fits the job
([component-guidelines.md](component-guidelines.md)), and the craft floors
every screen must clear (BP-079..090 in
[best-practices.md](best-practices.md) — type scale, contrast, spacing grid,
microcopy).

## Contents

- [Division of labor (state it to the user this way)](#division-of-labor-state-it-to-the-user-this-way)
- [When to bring it in](#when-to-bring-it-in)
- [Directions before frames](#directions-before-frames)
- [The floor under `Style pack: none`](#the-floor-under-style-pack-none)
- [Using it with Figma (the default surface)](#using-it-with-figma-the-default-surface)
- [Using it at build time (no Figma)](#using-it-at-build-time-no-figma)
- [What the audit checks](#what-the-audit-checks)
- [Boundaries](#boundaries)


It deliberately does **not** invent a look. A palette, a type pairing, a
texture, a motion vocabulary — invented per screen, they drift into a
collage; that is the visual half of the same drift this system exists to
prevent. So when the chain reaches VISUALIZE (Figma frames, wireframes) or
BUILD UI, the visual layer comes from a **locked style pack**, and the
ssheleg **sheleg-design** skill is where those packs live.

## Division of labor (state it to the user this way)

| Question | Owner |
|---|---|
| Which screens/states exist, what each does | super-ux (`screens.md`, scenarios) |
| Which control for the job, which states it ships | super-ux (BP-101..115) |
| Craft floors: 16/1.5/45–75, contrast, 4/8pt grid, verb microcopy | super-ux (BP-079..090) — the floor, never the identity |
| Palette, type pairing, texture, motion tokens, motifs, bans | **sheleg-design** style pack |
| Scroll-driven / particle / cinematic landing motion | **sheleg-design** (one clock, hold-then-redeploy, degrade to calm) |
| Motion floors: a token scale exists, reduced motion branches, content readable with no scroll effects | super-ux (BP-130..132) — the pack picks the values, not whether the floors apply |
| Whether a trend is adopted at all: its mechanism, its accessibility and weight cost, its review date, its compensation | super-ux (BP-145, BP-146) — recorded in the pack, never per screen |

The pack supplies concrete values for what the practices state as floors. On
conflict the pack wins on *identity* (its palette, its ease, its bans); the
practices win on *floors* (a pack may not push contrast below the WCAG floor
or tap targets under the platform minimum). Record the conflict and the
decision in the compliance table
([practice-selection.md](practice-selection.md)).

## When to bring it in

At the **start of design work** — the same moment as the Figma question, not
after frames exist:

1. **Is a style pack already recorded?** `screens.md` → Design system →
   `Style pack`. If yes, that is the identity; build every new frame and
   screen on it and don't re-litigate the look.
2. **Is `sheleg-design` available?** (a `sheleg-design` skill / the
   `/sheleg-design` command, or `styles/` from an in-project install). If
   yes, **`/sheleg-design` makes the visual decision** — from its own pack
   index and defaults, through its brief, cast and director record — and
   super-ux records the outcome: the pack name, its token file and the
   director record's path (`docs/design/<surface>/director-record.md`) in
   `screens.md` → Design system. super-ux keeps **no list of packs**. Until
   0.58.0 this step picked from three or four names copied out of a
   catalogue that had grown to dozens, and the copy was what an agent obeyed:
   the companion's index, its defaults and its director record were never
   consulted. A cinematic scroll-driven landing takes the companion's motion
   methodology as well; that too is its call, not this file's. Where the
   installed version ships the record validator
   (`npx sheleg-design-skill --check-record <file>`), run it before the
   frames go to approval; a version without it → the record check is
   `NOT_RUN`, said in the approval request, not skipped in silence.
3. **Not installed?** Recommend it once, plainly, and continue either way —
   text-only/platform-default design stays valid:
   ```
   # Claude Code (adds the /sheleg-design command):
   /plugin marketplace add ssheleg/sheleg-design-skill
   /plugin install sheleg-design@sheleg-design-skill
   # or drop the bundle into this project (any agent):
   npx sheleg-design-skill
   # or via the skills CLI (70+ agents):
   npx skills add ssheleg/sheleg-design-skill
   ```
   Never block the chain on it, never install it without the user's word,
   and never re-ask once the user has declined — record the decision as
   `Style pack: none — platform defaults` and move on. `none` declines a
   pack; it does not decline the floor below.

## Directions before frames

A brief is **underdetermined** when nothing on record settles the look: no
design system, no recorded pack, no brand or reference the brief names, or
the director record's `Fork` says the choice is open. Drawing every frame of
every flow in one guessed direction and then asking for approval is how a
look gets rejected after the expensive part is done. So the order is:

1. **First, one key screen in one state.** The screen that carries the flow's first
   value or its primary action, in `default`. Nothing else is drawn yet.
2. **Two directions only when the fork is real.** The director record's
   rubric is written *before* the directions exist (the same rule as the
   flow comparison in `ux-flows` step 2: the winner never writes the
   rubric). No real fork → one direction, and the record says why.
3. **The human picks on a 2-up mini sheet:** the two renders side by side —
   same screen, same state, same viewport and theme — with the rubric under
   them. The pick, the reason and what is taken from the loser go into the
   director record (`Fork`), and the pack it consolidates into goes into
   `screens.md` → Design system.
4. **Then the rest of the frames**, every screen and state, on the chosen
   direction's tokens.

The directions are sketched on **provisional semantic tokens**: declare only
the semantic roles (background, surface, text, accent, …) with working
values; two candidate identities are two provisional token sets, not a
contract violation. The **full reusable pack contract** (the thirteen
headings + `tokens/<pack>.css`) applies when a direction is CHOSEN and
consolidates into a pack for reuse or publication — a first sketch is never
blocked by thirteen headings, and a reusable pack still passes every one of
them. Free-styling one screen at a time remains the thing neither path
allows.

## The floor under `Style pack: none`

`Style pack: none — platform defaults` declines a pack. It does not switch
off the floor: when `sheleg-design` is installed, its `SLOP_MARKERS.md`
catalogue holds for every frame and every built screen, pack or no pack. A
pack may tighten the floor and never loosen it; a brief that explicitly asks
for a marked pattern wins only when the director record names the marker.

| What exists | What runs | What gets recorded |
|---|---|---|
| sheleg-design installed, code exists | `npx sheleg-design-skill --lint <dir>` — exit 1 on an S1 marker or an exceeded ratchet | command, commit, findings by severity — the director record's `Markers`, or the audit |
| sheleg-design installed, frames only | the catalogue's `review` rows read by eye during the frame critique ([figma-integration.md](figma-integration.md)) | the hits as critique triples |
| sheleg-design absent, or its installed version has no `--lint` | nothing | `Markers: NOT_RUN — <reason>` — never PASS |

`NOT_RUN` is the honest state of a check nobody ran; recording it as a pass
is how an unchecked surface reads as a clean one.

## Using it with Figma (the default surface)

Inside the `ux-flows` Design loop (see
[figma-integration.md](figma-integration.md)), after the flow diagram and the
screen/state table are agreed and **before** frames get drawn:

- take the pack's tokens as the **Figma variable collections** (in the tier
  model sheleg-design's
  [FIGMA_BRIDGE.md → Token tiers](https://github.com/ssheleg/sheleg-design-skill/blob/main/plugins/sheleg-design/skills/sheleg-design/FIGMA_BRIDGE.md#token-tiers) sets; BP-095)
  instead of hand-picking colors per frame;
  the pack's ready-made token CSS is the same source the code will use, so
  Figma and code start from one vocabulary. Creating them is a `use_figma`
  call (load `/figma-use` first); `get_variable_defs` reads back what a node
  actually references, which is how token parity gets verified instead of
  assumed;
- apply the pack's type scale, spacing, texture and motion tokens to every
  `SCR-NN/<Screen>/<state>` frame — the visual-craft practices are then
  satisfied *by construction*, and the compliance table records them
  `applied` with the pack as evidence;
- honor the pack's **bans** (each pack names what it never does) — a banned
  effect on a frame is a finding, not taste;
- the pack's light/dark twin (where it ships one) means the dark variant is a
  designed palette, not an inversion (BP-084);
- the frames are **critiqued before they go to approval**, and the art
  direction is approved separately from the flow — the critique, its
  triples and the two approvals are in
  [figma-integration.md](figma-integration.md).

## Using it at build time (no Figma)

Same order, fewer artifacts: `/sheleg-design` picks the pack (directions
first when the brief is underdetermined) → copy its token file into the
project's token location → record both in `screens.md` → Design system →
build screens from the chain's specs against those tokens. The chain still
decides structure and behavior; the pack decides how it looks.

## What the audit checks

When a `Style pack` is recorded, the deep audit's practice pass verifies the
built UI actually uses it: tokens referenced rather than raw values, the
pack's bans respected, dark mode from the pack's twin. On the Figma side the
same question is answered by `get_variable_defs` on the frame — a frame
carrying raw hexes where the pack has variables is the design-side twin of
hard-coded colors in code. A screen that ignores
the recorded pack is a `drifted` finding like any other divergence — an
identity chosen once and then abandoned per screen is exactly the drift this
companion exists to remove.

Where a screen has both a Figma frame and a running build, the audit can
compare the two pictures: the build captured in the frame's state, viewport
and theme, under the capture record of sheleg-design's `VISUAL_REVIEW.md`.
A difference is a `visual-drift` finding — the frame says one thing, the
screen shows another — and it is offered by default on brand and flagship
surfaces (`ux-audit` → Live pass and visual drift).

Where the pack — or the product's own taste — leans on a style with
documented debt (soft-shadow surfaces, deliberately raw layouts,
unconventional navigation, immersive 3D), the same pass checks that the
compensation BP-146 requires exists in the built UI: real boundaries and
visible focus states, a conventional path to every destination, the
reduced-motion branch, the weight budget. The look is the user's call; the
compensation is not optional.

## Boundaries

- Recommend, don't force: the user owns the look, the tooling, and the
  decision to install anything. One offer, then respect the answer.
- sheleg-design never overrides the chain: it cannot add a screen, change a
  flow, or relax a scenario. Structure and behavior stay super-ux's.
- If a project already has a design system (Figma library, token file,
  component dir), that IS the identity — record it and skip the pack
  question. Two identities is worse than any single one.
