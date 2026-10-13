# FW05 — journey ownership and marketing brief, 2026-10-13

Owner: super-ux; branch `fix/fw05-journey-copy-contracts`; canonical base
`18d8ebefca9b9facc9579d65fe8ef4009bd78b82`. Entry: [HANDOFF](../../HANDOFF.md).
This is source and deterministic-fixture evidence, not a model compliance test.

## Recovery and decisions

B-025 still reproduced: `check_jobs` received a journey without Owner and emitted
no ownership finding. B-026 still reproduced: a marketing source with no brief
emitted no brief finding; `marketing-copy.md` still named four inputs. Baseline
fixtures passed: UX 189, brand 184. Local main `5cb3a60` was preserved; all work
uses an isolated branch from fetched canonical main and advisory FW05-UX lease.

- `scenario-format.md` owns the journey Owner definition; source template and
  ux-foundation point at it. Map ownership defaults to its opportunities unless
  an opportunity names an override. `U086` warns on missing, blank, placeholder
  or duplicate Owner; `unknown` means unassigned, not accepted or complete.
  The owner repository's two maps now say unknown rather than inventing a role.
- `brand-contract.md` owns `copy-brief.md`. It records Surface, Action, Reader,
  Customer words, Proof, Success metric, Constraints and Voice reference. Unknown
  is valid structure; a missing metric is not zero and a missing limit is not
  permission. Copywriting owns this task record, not voice/facts/approved targets.
- `B074` is advisory only when marketing sources exist and no brief exists.
  `B075` checks a present record's fields and its local voice pointer. A known
  voice reference requires `voice.md#voice-references` and its actual
  Admired/Refused pair inside that section. Other source truth stays a human or
  agent review obligation; the linter does not certify attribution or metrics.
- The reference is lazy: only a marketing writing task reads/updates the brief.
  Skill descriptions remain unchanged. Canonical contracts and templates are
  propagated by `python3 test/sync_references.py`, not edited in their copies.

The older B-026 percentage claim was checked against the primary
[NN/g article](https://www.nngroup.com/articles/how-little-do-users-read/), opened
2026-10-13. It is dated 2008-05-05 and estimates a reading upper bound from visit
duration, explicitly not eye tracking. `marketing-copy.md` preserves that scope;
no current audience estimate, target or conversion claim is derived from it.

## Checks

Focused green before final documentation:

- `python3 test/ux_lint_test.py`: 196 checks, exit 0.
- `python3 test/brand_lint_test.py`: 201 checks, exit 0.
- `python3 test/audit_regressions/fw05_journey_copy.py`: 18 controls, exit 0,
  including pristine seeds, declared-field/code-reader parity, unknowns, absence
  without marketing, advisory migration, a misbound voice pair and commented
  input. Temporary controls use a context manager and remove only their own tree.

`python3 test/validate.py`: 5474 checks, exit 0; raised the ratchet and refreshed
its self-referential fact from the actual gate output. `docs/ux/lint.py`: exit 0,
clean. `docs/brand/lint.py`: exit 0 with the expected B074 migration advisory for
the existing marketing surface; this is not a zero-warning claim.

Actual call-removal plants were run serially: remove `check_journey_owners` from
the public UX path, then remove `check_copy_brief` from the public brand path.
Their fixture suites exited 1 with the specific U086 missing-owner and B074
migration tests failing. Original bytes were restored in `finally`; dedicated
controls then passed. These assert reachability, not only pure helper behavior.

`npm pack --json` into an owned context-managed directory: archived brief seed
and both source linters byte-matched canonical files; archive removed on exit.
Workflow job bodies compare byte-identical to base. No description/front-matter
changed; copywriting adds a lazy marketing-only reference and its template.

Final full owner gate and independent review: pending. No release/install/native/
model verdict.

## Integration and next step

The validation workflow keeps job bodies unchanged. Nightly at 23:00
Europe/Warsaw is the default; deliberate frozen `ready_for_review` promotion is
the candidate exception. No push/opened/synchronize trigger. Diagnostic manual
dispatch is not PR ruleset acceptance, per
[GitHub check eligibility](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks#checks-from-some-workflow-jobs-are-not-evaluated).

After the focused/full gates, obtain independent review, freeze exact head,
promote once and merge normally only when genuine required checks pass. Version,
publication, umbrella pins and installed/native behavior are separate work.
