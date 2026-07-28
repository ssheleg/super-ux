# Visual Identity — the sheleg-design companion (recommended, never forced)

super-ux decides **what the interface must be**: which screens exist, which
states they show, what each element does, which control fits the job
([component-guidelines.md](component-guidelines.md)), and the craft floors
every screen must clear (BP-079..090 in
[best-practices.md](best-practices.md) — type scale, contrast, spacing grid,
microcopy).

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
   yes, use it to pick the pack for this product and write the pack name +
   its token file location into `screens.md` → Design system.
   - product UI — dashboards, admin panels, internal/dev tools, settings →
     `workbench` (quiet light/dark, ships both themes);
   - dark, high-signal instrument surfaces → `instrument-console`;
   - warm editorial / brand-led marketing → `editorial-luxury`;
   - a cinematic scroll-driven landing or hero → the pack **plus** the
     motion methodology (that is what the skill is built for);
   - nothing fits → author a new pack against the skill's pack contract
     rather than free-styling one screen at a time.
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
   `Style pack: none — platform defaults` and move on.

## Using it with Figma (the default surface)

Inside the `ux-flows` Design loop (see
[figma-integration.md](figma-integration.md)), after the flow diagram and the
screen/state table are agreed and **before** frames get drawn:

- take the pack's tokens as the **Figma variable collections** (primitive →
  semantic → component, per BP-095) instead of hand-picking colors per frame;
  the pack's ready-made token CSS is the same source the code will use, so
  Figma and code start from one vocabulary;
- apply the pack's type scale, spacing, texture and motion tokens to every
  `SCR-NN/<Screen>/<state>` frame — the visual-craft practices are then
  satisfied *by construction*, and the compliance table records them
  `applied` with the pack as evidence;
- honor the pack's **bans** (each pack names what it never does) — a banned
  effect on a frame is a finding, not taste;
- the pack's light/dark twin (where it ships one) means the dark variant is a
  designed palette, not an inversion (BP-084).

## Using it at build time (no Figma)

Same order, fewer artifacts: pick the pack → copy its token file into the
project's token location → record both in `screens.md` → Design system →
build screens from the chain's specs against those tokens. The chain still
decides structure and behavior; the pack decides how it looks.

## What the audit checks

When a `Style pack` is recorded, the deep audit's practice pass verifies the
built UI actually uses it: tokens referenced rather than raw values, the
pack's bans respected, dark mode from the pack's twin. A screen that ignores
the recorded pack is a `drifted` finding like any other divergence — an
identity chosen once and then abandoned per screen is exactly the drift this
companion exists to remove.

## Boundaries

- Recommend, don't force: the user owns the look, the tooling, and the
  decision to install anything. One offer, then respect the answer.
- sheleg-design never overrides the chain: it cannot add a screen, change a
  flow, or relax a scenario. Structure and behavior stay super-ux's.
- If a project already has a design system (Figma library, token file,
  component dir), that IS the identity — record it and skip the pack
  question. Two identities is worse than any single one.
