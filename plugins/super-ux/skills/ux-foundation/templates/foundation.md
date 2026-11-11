# UX Foundation

<!-- Managed with super-ux (ux-contract v5). The WHY layer: personas, actors,
jobs to be done, customer journeys, user stories. Update when the understanding
of users changes; capabilities.md and scenarios.md trace to the IDs defined
here. -->

## Personas

<!-- ### P-01: <name>
1-3 sentences: who they are, what they know, what they want. Grounded in
data/observation, recognizable by a real user.
- **Agent use:** none | some | most (<evidence: RE-NN, the brief, an interview>)
-->

## Actors

<!-- The non-human performers: agents acting for a persona, automations and
outside systems. People stay in Personas.
### A-01: <name>
- **Kind:** agent | system
- **Acts for:** P-01
- **Grant:** <the scope it holds; never wider than its principal's role>
-->

## Jobs to Be Done

<!-- ### JTBD-01: <short job name>
- **Statement:** When <situation>, I want to <motivation>, so I can <expected outcome>.
- **Personas:** P-01
- **Type:** functional | emotional | social
- **Forces:** push: <...>; pull: <...>; anxiety: <...>; habit: <...>
- **Success metric:** <observable user outcome, not a feature>
-->

## Customer journeys

<!-- ### JRN-01: <persona>, <job> (JTBD-01)
- **Owner:** unknown
| # | Stage | User action | Performed by | Touchpoint | Emotion (1-5) | Pain | Opportunity |
|---|-------|------------|--------------|------------|---------------|------|-------------|
Performed by: the P- and A- ids that do this stage.
-->

## Monetization

<!-- When the product earns money (choose with data, BP-067..070):
- **Model:** hard paywall | freemium | hybrid | trial (type, length), and why
- **Value metric:** <what the paid tier meters>
- **Free boundary:** <what stays free, where the visible limit sits>
- **Purchase surface:** in-app (IAP) | web checkout | web2app (web funnel -> app); BP-030/BP-078/BP-127, and which storefronts
- **Money moments:** <paywall placement, upgrade triggers, checkout, failed payment, cancel, rating prompts, winback>
- **Acquisition coherence:** <the one story ad -> landing/listing -> onboarding tells>
-->

## Product mechanics

<!-- Two dimensions the practice-selection profile reads; record them once,
even when the answer is "none":
- **Personalization:** none | rule-based | inferred/model-driven; BP-143/BP-144 (what gets asked when, and how a wrong inference is corrected)
- **Engagement mechanics:** none | streaks/tiers | points/badges/leaderboards; BP-141/BP-142 (which traced job each mechanic reinforces, and the recovery path when progress is lost)
- **Accessibility regime:** none stated | EAA (EU) | ADA (US) | both; BP-138, with the owner
-->

## Design tooling

<!-- Visual mockups in Figma are optional (default on). Ask the user at the
start of design; record the choice here (see figma-integration). Figma is a
set of files in the product's folder, one per surface the product has; the
design-system details and frame links live in docs/ux/screens.md (the UI
map). This section records the on/off choice and where the files are.
- **Figma:** enabled | disabled
- **Figma folder:** <team / project the product's files live in>
- **Figma files:**
  | Surface | File | Holds |
  |---------|------|-------|
  | App | <url> | every SCR-NN frame of the product |
  | Web | <url> | landing, pricing, docs pages |
  | ASO | <url> | store screenshots, icon, preview frames |
-->

## User stories

<!-- ### ST-001: <short name>
- **Story:** As <persona>, I want <capability>, so that <benefit>.
- **Traces:** JTBD-01, JRN-01/#2
- **Acceptance criteria:**
  - Given <precondition>, when <action>, then <observable result>.
- **Priority:** must | should | could
- **Kill criteria:** <metric below threshold by date -> drop | iterate, or omit>
- **Status:** proposed
- **Product:** unobserved
-->
