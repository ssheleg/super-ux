## UX scenarios — hard rule (super-ux)

- `docs/ux/scenarios.md` is the source of truth for all user-facing
  behavior; `docs/ux/foundation.md` (personas, JTBD, journeys, stories) and
  `docs/ux/flows.md` (user flows) are the WHY and HOW layers scenarios
  trace to.
- Any change that touches user-facing behavior MUST update
  `docs/ux/scenarios.md` (and affected flows) in the same change.
- Any new feature or project STARTS with the chain: which job does it
  serve, which journey stage, which story — then flows and scenarios,
  validated against the existing base, approved.
- **Do NOT write interface code until the UX workflow is done first:** the
  foundation → flows → scenarios chain is designed and approved, and — when
  Figma is enabled (default) — the UI is mocked up in Figma with every
  screen linked to its frame. Building UI before this is the exact mistake
  super-ux exists to prevent.
- Use `/ux` as the entry point; skills: `ux-foundation`, `ux-flows`
  (flows + Figma mockups), `ux-scenarios` for maintenance, `ux-audit` for
  evidence-backed verification.
