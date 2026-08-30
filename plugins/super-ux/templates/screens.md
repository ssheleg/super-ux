# UI Screen Registry

<!-- Managed with super-ux (ux-contract v4). The design map: every screen and
state with its Figma frame, wireframe, code coverage, and related UX/UI
resources. Update in the same change as any interface change; when Figma is
enabled, update the frame and re-verify its link in the same change. A screen
whose code diverges from its record here is a "drifted" finding. -->

## Index

| ID | Screen | Used by | Figma | Status | Coverage |
|----|--------|---------|-------|--------|----------|

## Design system

<!-- Style pack = the locked visual identity every frame and built screen obeys.
Pick it with the sheleg-design companion skill (workbench for product UI /
dashboards / tools, instrument-console, editorial-luxury, or a new pack on its
contract) before drawing anything; record its token file below. -->
- **Style pack:** <pack name, or "none — platform defaults">
- **Figma library:** <url/name, or "none — platform defaults">
- **Tokens in code:** <where color/type/spacing tokens live, e.g. src/theme/tokens.ts>
- **Component source:** <shared UI components dir, e.g. src/components/>
- **Assets:** <icons/illustrations location>

## Web surfaces

<!-- Does this product have pages a search engine or an AI answer engine will
read — a landing, pricing, docs, blog? Answer once, here. "no" silences the
check; flip it to "yes" the moment a public page is designed, and give every
public screen the **Web surface:** block shown below. This is decided at design
time on purpose: once a page is live its URL is in other people's links and its
structure is what an answer engine already quoted, so an audit afterwards finds
the problem it can no longer fix. -->
- **Web surfaces:** no

## Screens

<!-- One entry per screen (see ux-contract v4 for field rules):

### SCR-01: <name>
- **Used by:** <FLW-… and the step(s)>
- **Purpose:** <the job step this screen serves>
- **Elements:** <each element; mark the ONE primary action>
- **States:**
  | State | Trigger | Figma frame | Behavior |
  |-------|---------|-------------|----------|
  | success | default | <frame deep-link> | <what shows> |
  | empty | <trigger> | <frame deep-link> | <prompt to act> |
  | error | <trigger> | <frame deep-link> | <message + recovery> |
  | loading | <trigger> | <frame deep-link> | <skeleton/progress> |
- **Web surface:** (only when this screen is a public URL; all five required)
  - **Route:** </pricing — the path, readable and stable>
  - **Answers:** <the ONE question this page answers; a second question is a second page>
  - **Indexable:** <yes | no + why | canonical → /other-path>
  - **Without JS:** <what a reader gets with no JS executed — the answer, or nothing>
  - **Entity:** <schema.org type + the thing it describes, matched to visible content>
- **Wireframe:** wireframes/SCR-01.md (optional)
- **Coverage:** <file:line, or "none yet">
- **Scenarios:** <SCN-… touching this screen>
- **Resources:** <related components, shared assets, API/data deps, links>
- **Status:** designed | built | drifted | retired
-->
