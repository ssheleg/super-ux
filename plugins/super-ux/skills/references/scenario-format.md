# Scenario Format Contract (v1)

This is THE contract for `docs/ux/scenarios.md` and `docs/ux/audits/*` in a
target project. Both the `ux-scenarios` and `ux-audit` skills — and the
Cursor rules — follow it. Do not deviate from field names, statuses, or
verdicts; tooling and audits key off them.

## Files in the target project

```
docs/ux/
├── scenarios.md              # the scenario base (source of truth)
└── audits/
    └── YYYY-MM-DD[-scope].md # one report per audit run
```

## `docs/ux/scenarios.md`

Ordered structure:

1. **Header comment** (first line after the title):
   `<!-- Managed with super-ux (scenario-format v1). Update in the same change as any user-facing behavior change. -->`
2. **Index** — one table row per scenario, kept in sync with the entries:

   ```markdown
   | ID | Title | Feature | Persona | Status | Last audit |
   |----|-------|---------|---------|--------|------------|
   | SCN-001 | First-run onboarding — happy path | onboarding | new-user | validated | 2026-07-19 PASS |
   ```

3. **Personas** — every persona referenced by a scenario, 1–3 sentences each
   (who they are, what they know, what they want).
4. **Scenarios** — grouped by feature under `## <feature>` headings.

### Scenario entry

```markdown
### SCN-001: First-run onboarding — happy path
- **Persona:** new-user
- **Feature:** onboarding
- **Entry point:** first launch, no saved state
- **Preconditions:** none
- **Steps:**
  1. User opens the app for the first time and sees the welcome screen
  2. User taps "Create project", types a name, confirms
- **Expected result:** user lands on the main screen with the project created and visible
- **UI elements:** welcome screen, "Create project" button, name field, confirm button
- **States covered:** loading, empty, error, success
- **Errors & recovery:** name empty -> inline "Name is required", field focused; save fails -> toast with retry, input preserved
- **Status:** draft
- **Coverage:** none yet
```

Field rules:

- **Persona** — must name a persona defined in the Personas section.
- **Entry point** — where the user starts (URL, screen, app state).
- **Steps** — numbered, from the user's point of view, one action per step.
- **Expected result** — what the user sees when it works; observable, not
  internal ("project appears in the sidebar", not "record inserted").
- **UI elements** — every button, field, link, dialog, toast the user
  touches or sees in this scenario. This list is what the audit checks for.
- **States covered** — which of `loading | empty | error | success` this
  scenario exercises.
- **Errors & recovery** — for each failure the user can hit: what they see
  and how they recover. "Nothing can fail" must be stated explicitly.
- **Status** — `draft | validated | implemented | retired` (see lifecycle).
- **Coverage** — `file:line` (or file) references to the implementing code,
  or `none yet`.

### ID rules

- Format `SCN-NNN` (zero-padded, sequential). IDs are **never reused**.
- Retired scenarios keep their entry with `Status: retired` and a one-line
  reason — never delete entries.

### Status lifecycle

```
draft ──(human approves)──> validated ──(audit confirms coverage)──> implemented
  └──────────────────────────(scenario no longer true)──────────────> retired
```

- New and changed scenarios enter as `draft`.
- Only a human decision moves `draft` → `validated`.
- Only an audit with verdict PASS moves `validated` → `implemented`.

### Completeness checklists

Per feature, the base must contain at minimum:

- the happy path;
- every error path the user can hit;
- the empty state (nothing created yet / no results);
- the loading state where the wait is user-visible;
- destructive-action confirmation, where applicable;
- the returning-user variant, where behavior differs from first use.

Per product, the base must cover:

- first-run onboarding;
- every core feature flow;
- settings / configuration;
- multi-entity flows (e.g. creating the second project, switching between
  them);
- account and data lifecycle (sign-out, deletion, export), where applicable.

## Audit report — `docs/ux/audits/YYYY-MM-DD[-scope].md`

```markdown
# UX Audit — YYYY-MM-DD

- **Scope:** all | feature:<name> | SCN-001..SCN-020
- **Method:** static code trace [+ live run]
- **Base version:** <git SHA of scenarios.md at audit time>

## Summary

- Totals: PASS n / PARTIAL n / FAIL n / BLOCKED n
- Top issues: <the findings that most damage the user experience>
- Recommended next actions (prioritized): 1. ... 2. ...

## Batch 1: <feature> (SCN-001..SCN-005)

### SCN-001 — PASS
- **Evidence:** src/onboarding/Wizard.tsx:12, src/onboarding/routes.ts:4

### SCN-002 — PARTIAL
- **Evidence:** src/projects/List.tsx:30
- **Findings:**
  - [AUD-2026-07-19-01] (major) empty state renders a blank panel instead of
    the "Create your first project" prompt -> add the empty-state branch

## Findings register

| # | Scenario | Severity | Finding | Suggested fix |
|---|----------|----------|---------|---------------|
| AUD-2026-07-19-01 | SCN-002 | major | blank empty state | add empty-state branch |
```

### Verdicts

- **PASS** — every listed UI element exists and is wired; all listed states
  handled; errors surfaced honestly.
- **PARTIAL** — the flow exists but gaps were found (missing state, missing
  element, silent error).
- **FAIL** — the flow is missing or broken.
- **BLOCKED** — could not verify; say exactly why. Never guess: a verdict
  without `file:line` evidence must be BLOCKED, not PASS.

### Severity

`critical` (user cannot complete the flow / data loss), `major` (flow
completes but the experience is broken or dishonest), `minor` (polish).

### After a run

- Update the `Last audit` column in `scenarios.md` (`YYYY-MM-DD VERDICT`).
- Flip `validated` → `implemented` where the audit confirmed coverage.
- Findings feed planning: offer to turn FAIL/PARTIAL into a work plan.
