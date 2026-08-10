# Plan — web surface in the contract, and a router that speaks

Ten tasks. Every REQ from the brief appears in exactly one `Implements:` row;
the set-comparison at the bottom is the gate for leaving stage 4.

| # | Task | Implements |
|---|---|---|
| T1 | `check_web_surface()` in `plugins/super-ux/scripts/ux_lint.py` — TDD: the fixture that plants a partial block goes red first, then the check | R-02, R-03 |
| T2 | The `Web surface:` block defined once in `references/scenario-format.md`, under the screen entry; contract marker unchanged | R-01, R-12 |
| T3 | `templates/screens.md` gains the project-level declaration and a commented example block; the check must pass on it untouched | R-04 |
| T4 | `ux-flows/SKILL.md` asks the web-surface question in the same step it asks about Figma and the style pack | R-05 |
| T5 | `ux-audit/SKILL.md` verifies a built public screen against its record and hands off to the companion | R-06 |
| T6 | `seo-aeo-audit` becomes the third companion — `commands/ux.md`, `references/system-map.md`, `README.md`, with its real install commands | R-07 |
| T7 | `commands/ux.md` — four new routing rows and the composite-brief decomposition rule; the `.mdc` Cursor channel updated in the same change | R-08, R-09 |
| T8 | `python3 test/sync_references.py`, then every gate alone, each read by its own exit code | R-10 |
| T9 | Dogfood — super-ux's own `docs/ux/screens.md` answers the new question | R-11 |
| T10 | Release v0.33.0 — four version places, preflight, atomic push, CI verdict read, registry polled | R-13 |

## Set comparison

- Brief REQs: R-01 … R-13 (13)
- Union of `Implements:` above: R-01, R-02, R-03, R-04, R-05, R-06, R-07, R-08,
  R-09, R-10, R-11, R-12, R-13 (13)
- **Equal.** No REQ is unplanned, no task is unrequested.

## Order

T1 → T2 → T3 close the contract-and-gate loop and must run in that order: the check
is written red, the contract gives it something to be right about, and the template is
the first input it sees (standing instruction #3). T4–T7 are independent of each other.
T8 is a barrier. T9 needs T1–T3. T10 is last.
