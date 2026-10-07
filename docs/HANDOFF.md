# Direction-before-frames handoff, 2026-10-07

Branch `feat/direction-before-frames` prepares super-ux 0.58.0: `/sheleg-design`
decides the look (no pack list here), directions before frames, the
`Style pack: none` floor, flow and art-direction approvals split with a frame
critique between them, `visual-drift` in `ux-audit`, Figma as a file per
surface, states × axes per screen and the onboarding budget. Start with the
[0.58.0 changelog section](../CHANGELOG.md) and the
[verification ledger](evidence/verification.md) rows DF-U1a..DF-M2.

- Done: U1–U5 of the family plan plus the screen matrix and onboarding budget;
  seven new linter codes `U079`..`U085`, each watched failing on a planted
  defect; `npm test` and every CI step green locally.
- Open: review and merge, tag `v0.58.0`, npm publication, the umbrella pin in
  `sshlg-skills/skills.json`, refreshing local installs. None is implied by
  this branch.
- Depends on, outside this repo: sheleg-design's director record validator
  (`--check-record`) is not released yet; `visual-identity.md` runs it where
  the installed version ships it and records `NOT_RUN` otherwise. `--lint`
  shipped in sheleg-design 1.62.0.
- Not done on purpose: `EV-06` and `EV-07` are authored and anchor-checked,
  not run (paid, nondeterministic, run by a person per `test/evals/README.md`).
- Next task: review the PR, then release per `CONTRIBUTING.md` → Releasing.

---

# Short-video copy handoff, 2026-10-07

Branch `feat/short-video-copy` prepares super-ux 0.57.0: the short-video,
Instagram and X playbooks, `video-script.md`, `hooks.md`,
`research-outliers.md`, and four brand-lint codes (`B044` hook filter, `B045`
feed window, `B046` one ask, `B066` invisible characters). Start with the
[0.57.0 changelog section](../CHANGELOG.md) and the
[verification ledger](evidence/verification.md) rows SV-C1..SV-C8.

- Done: every task C1–C8 of the family plan, each check watched failing on a
  planted defect; `npm test` and every CI step green locally.
- Open: review and merge, tag `v0.57.0`, npm publication, the umbrella pin in
  `sshlg-skills/skills.json`, and refreshing local installs. None of these is
  implied by this branch.
- Not done on purpose: no Russian words-per-second coefficient (measured by
  reading aloud); `B044` scores English only; `B066` reports and never rewrites.
- Next task: review the PR, then release per `CONTRIBUTING.md` → Releasing.

---

# Display-copy guard handoff, 2026-10-01

Start with [DC-01 report](evidence/audits/2026-10-01-display-copy/report.md).
The branch prepares super-ux 0.56.3: semantic heading checks, source coverage,
selective warning gates and the copywriting delivery contract. The coordinator
owns independent review, merge, tag, npm publication and umbrella refresh.
Do not treat this branch or deterministic fixtures as a published release or
proof that every agent/model now follows the instruction.

---

# Sherlock family audit: handoff

This branch contains the prepared super-ux instruction changes from the family
audit. The runtime backlog has not been implemented or released.

Start with the [central handoff](https://github.com/ssheleg/sshlg-skills/blob/codex/sherlock-audit-handoff-20260907/docs/HANDOFF.md).
It links the 139 parent outcomes, 254 bounded task packets, module contracts,
source provenance, execution order and all member branch revisions.

Read the central repository manifest before choosing a task. Filter the plan by
this repository's module, then read one leaf and its prerequisites. Refresh source
hashes against the chosen checkout and materialize predecessor outputs before
editing. A prepared instruction is not evidence that an agent outcome improved.

Validation receipts for these instruction changes are in the central bundle.
Commit and push each completed task with its updated context and checks; leave a
new entry point for the following agent. Follow the [standing handoff rule](https://github.com/ssheleg/sshlg-skills/blob/codex/sherlock-audit-handoff-20260907/docs/working-rules/repository-handoff.md).
