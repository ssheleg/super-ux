# Clickable flow prototypes — review the journey, not isolated screens

Recommend a runnable, clickable preview for a new or substantially changed
multi-screen journey, onboarding, checkout, permission flow or complex recovery
path. When the operator asks to click through the flow, it is a deliverable.
A wording-only change or a settled single-state screen does not need a new app.

## Start from the scenario model

Draft the flow and its scenario set together, then use the preview to refine both.
Do not wait for final scenario approval to make a review prototype: that would
make the evidence needed for approval depend on approval itself. Production UI
implementation still follows the agreed chain.

Enumerate entry points, screen-state nodes, transitions and terminal outcomes.
For each in-scope scenario include its happy path, alternative decisions, error
and recovery paths, back/cancel, and returning-user variants. Include interrupted,
pending and externally owned outcomes when the platform cannot report success
or failure immediately. Bound repeat loops and explain equivalence classes;
"all variations" means the declared state/transition model, not infinite paths.

Use FLW, SCR and scenario IDs already in the project. While a scenario is being
drafted, mark its temporary ID and replace it before handoff. Avoid a separate
untraceable vocabulary for the prototype.

## What the operator receives

- A screen map beside the active screen, with the current node highlighted.
- Clickable controls that follow the real flow edges; a visible back/reset action.
- A scenario selector and explicit controls for simulated success, empty, error,
  denied, timeout and pending outcomes relevant to this flow.
- Deep links or stable entry controls for each screen-state, so reviewers and
  later agents can reopen a specific case without replaying a long journey.
- Realistic representative content, long text and populated/empty variants;
  synthetic values are labelled and are never evidence about the product.
- A coverage receipt: scenario → transitions → screen-states → preview locator
  → walked / not walked / deferred with reason. Declared coverage and observed
  clickthrough are different columns.

The preview may be a local HTML file, a small local app, or a connected design
prototype when that tool is available and chosen. Use the host's file/browser
preview to show it when possible; record how another agent can reopen it.
Figma is optional for this preview. Missing browser access means clickthrough
is NOT_RUN; a screenshot or generated file alone is not an observed journey.

## Safe simulation and honest evidence

Use an in-memory state model with a deterministic reset. Simulate payments,
credentials, destructive actions and server errors; do not send real requests
to prove the prototype. Mock controls must be visibly labelled as simulation.
Do not fabricate waiting periods to imply work took place.

Walk at least the primary path and each high-risk recovery branch. Enumerate
unwalked branches instead of reporting the prototype as fully verified. A cheap
graph check can catch unknown targets, unreachable required states and missing
recovery edges; it does not replace clicking through the actual preview.

This is review scaffolding, not production UI. It can be executable before the
production build gate. Do not add production persistence, services or a component
framework merely to make the preview. Reuse existing infrastructure when useful.

## Keep decisions and handoff linked

UX owns transitions, states and scenario coverage. Visual direction belongs to
sheleg-design; a low-fidelity flow preview does not approve palette, typography
or visual craft. Compare visual alternatives separately when those are unsettled.

After review, update flows, screens and scenarios together. Record accepted
decisions, rejected alternatives and remaining unknowns. A prototype click does
not promote implementation Coverage or Product outcome status.

Keep a retrievable preview artifact and its revision/digest linked from the flow
or implementation packet until the approved behavior is implemented and its
decision record no longer depends on the sketch. If the preview is retired,
retain the coverage receipt and the decision; mark its locator retired rather
than leaving a broken link. The next implementer receives those links with the
scenario IDs, not only a screenshot or a chat summary.
