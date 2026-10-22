## Unreleased: M2 wave 3, portfolios, creators and LLM referrals from GP Bullhound (2026-10-22)

- **Objective.** Milestone M2 wave 3 (G5, G9, the attribution half of G7, R1, R4) from GP Bullhound's *Consumer Subscription Software* (October 2025), every figure checked on its page with `pdftotext`.
- **Done.** BP-246..247 (bundles across a portfolio; the portfolio as one account with two retention lines), routed in `practice-selection.md`; `funnel-research.md` *AI answers as an acquisition channel* (LLM referrals as their own channel, R4), routed from the `analytics: yes` row, with the citation-source audit named as the seo-aeo-audit skill's; `ux-flows` money moments state the *Your own numbers* metric and band a subscription-surface change targets (R1); `channel-playbooks.md` *Creators and ambassadors* (G9). Copies synced; counts in README, `product-frameworks.md`, `docs/brand/facts.md` and the graph label moved to 247. Branch `feat/m2-wave3`, local commit, not pushed; no version bump.
- **Decision.** `product-frameworks.md` gains no framework: it holds models that decide which question is asked, and the portfolio model is an operating model whose screen consequences fit BP-247. Only its catalog count moved.
- **Open.** No gate reads R1 or R4; both are text a design review applies.
- **Next task.** Review and merge `feat/m2-wave3`, then a minor release (0.66.0) and the sshlg-skills pin bump.

## v0.65.0: M2 wave 1, subscription growth from GP Bullhound (2026-10-22)

- **Objective.** Milestone M2 wave 1 (G1, G2, G3, G4, G6, G10, R3): strengthen the subscription guidance from GP Bullhound's *Consumer Subscription Software* (October 2025), every figure cited by page.
- **Done.** `funnel-research.md` *Your own numbers* (unit economics with bands, four cohort states, locals and tourists); BP-242..245 with source key `[GPB25]`, routed in `practice-selection.md`; the test panel's locals/tourists rule in `templates/test-panel.md` and `ux-foundation`; copies synced; counts in README, `product-frameworks.md`, `docs/brand/facts.md` and the graph label moved to 245. Branch `feat/m2-subscription-growth`, local commit, not pushed.
- **Open.** task-pipeline 1.101.0's `design_gate.py panel` is the reader of the locals/tourists rule (released after this one).
- **Next task.** After merge: tag `v0.65.0`, watch the release run, then the sshlg-skills pin bump; M2 wave 3 here (G5 bundles and the portfolio model, G9 creator programs, the attribution half of G7, R1 and R4).

## v0.64.0: the test panel, and a voice checker named by its tools (2026-10-22)

- **Objective.** The operator's design-review gate (2026-10-22) needs a ten-portrait test panel; super-ux owns its format. Remove a private product name from `copywriting`.
- **Done.** `templates/test-panel.md` (synced into `ux-foundation`), the *The test panel* section, the generic voice-checker wording; version 0.64.0.
- **Next task.** After merge: tag `v0.64.0`, watch the release run; task-pipeline 1.100.0 ships the design-tester that reads this panel; then the sshlg-skills pin bump.

# Current follow-up: short descriptions, 0.63.0 (2026-10-20)

Branch `desc-budget-1020`. All seven skill descriptions cut to 279 to 393
characters (4,426 to 2,436 in total) and the fifteen command descriptions to one
sentence (2,424 to 1,116), because the operator's skill listing was full and 81
skills showed no description. Removed trigger phrases live verbatim under
`## Triggers` in each SKILL.md body. `validate.py` now fails a description over
500 characters, one without "Not for", and a command over 120. Descriptions are
single-quoted YAML so `Triggers:` can use a colon instead of a spaced hyphen
(the no-dash rule). Evidence: [verification ledger](evidence/verification.md),
section 2026-10-20. Gate: `npm test` alone, exit 0.

Next task: none here; the hub re-pins 0.63.0 in its own change.

---

# Current follow-up: retrieval crawlers, landing promises, Copylot sweep, 0.62.0 (2026-10-19)

Branch `feat/seo-landing-copylot` (FEED-SEO-1019 wave 2, member super-ux). `B050`
now judges retrieval agents only, read in RFC 9309 groups; `seo-aeo-safety.md`
carries the crawler policy as two decisions and points its technical floor at
seo-aeo-audit's brief mode (0.28); `landing-pages.md` adds LP-21..LP-24;
`copywriting` runs `copylot.check` beside the brand linter with a stated
fallback; synthetic respondents are hypotheses (`research-evidence.md`,
`ux-foundation`, `ux-scenarios`); `audit-depth.md` adds the quarterly fresh-user
walk. Evidence: [verification ledger](evidence/verification.md), section
2026-10-19. Gate: `npm test` run alone, exit 0.

Open: the seo-aeo-audit `references/build-time.md` link resolves only once
seo-aeo-audit 0.28 merges; Copylot's `web` register and `web-page` format do not
exist yet, so the copywriting sweep runs its documented fallback until they ship.

Next task: review and merge the PR; the coordinator owns preflight, tag,
publication and the hub pin.

---

# Current follow-up: no em dash in new text, 0.61.0 (2026-10-18)

Owner decision relayed by the operator on 2026-10-18: the em dash (U+2014) is not
written in any text for people, in any language; the grammatical Russian dash only
where no rewrite reads naturally. Branch `feat/no-em-dash`. `ai-tells.md` AT-06 is a
hard ban with two layers; new code `B067` in `brand_lint.py`; `copywriting`
Non-negotiable; `brand-voice` seeds the invariant; hard rule and Cursor rule updated.
Gates run alone, each exit 0: `test/validate.py` (5507), `test/brand_lint_test.py`
(206), `test/ux_lint_test.py` (196), `docs/brand/lint.py`, `docs/ux/lint.py`,
`npm run test:audit`, `test/installer_test.js`, `test/evals_validate.py`,
`test/display_copy_test.py`, `test/social_preview.py`. Planted deletion of `B067`:
5 fixtures red.

Next task: none in this repository; the hub pins 0.61.0 and ships the always-on rule.

---

# Current follow-up — WebKit (Safari) first, 0.60.0 candidate (2026-10-16)

Branch `docs/safari-first` (family iteration ITER-1016, REQ R15): new shared contract
`plugins/super-ux/skills/references/browser-engine.md` (WebKit first, Chromium as a
stated fallback, a Chromium-only check reported as exactly that). `ux-audit` links it
from the RUNTIME tier and the live pass and adds `engine` to the capture record;
`funnel-research.md` walks funnels in WebKit first. Copies synced with
`python3 test/sync_references.py`. Version 0.59.3 → 0.60.0; ledger section; facts row
`repo validator checks` re-measured at 5502. Regression
`test/audit_regressions/safari-first.py` (watched failing 5 of 5 first). Gate:
`npm test` exit 0. ux-audit body 4435 tokens (cl100k_base), 309 lines.

Next task: review the draft PR; the coordinator owns preflight, the annotated tag,
publication and the umbrella pin.

---

# Current follow-up — retained board controls

[Owner process packet](evidence/runs/2026-10-13-r30-board-retention/README.md)
adds existing duplicate-id and width checks to the repository's actual audit gate.
No production parser or payload changes. Next: exact-source focused replay and
independent review, then normal candidate admission; broader parser grammar remains
outside this bounded persistence correction.

---

# Current state — super-ux 0.59.3 published

[Published readback and bounded closures](evidence/runs/2026-10-13-fw00-published/README.md)
record the accepted journey/copy contracts and resolve stale B-025/B-026 statuses.
The earlier candidate entries below remain historical. Unknown ownership and
metrics remain unknown; no model or installed acceptance is claimed.

Next: normal docs-only admission after focused checks and peer review, then hub
pin/readback reconciliation. No new version or release is required by these docs.

---

# FW05 release packaging — 2026-10-13

Branch `release/fw05-0.59.3` prepares patch 0.59.3 from accepted source
`c331b052c473adbd125cd3611ca28f73cfae1bc8` (PR42). Genuine validation run
`38340377527` passed at candidate `077f9b84aa1edfe63c330f52f0395fa1c50ea6b8`
before normal merge.
Full source and independent checks passed at implementation `b8305c5`; see the
[FW05 receipt](evidence/runs/2026-10-13-fw05-journey-copy.md). Registry and remote
tags read 0.59.2 before this preparation. Only package/plugin/marketplace/card
versions, changelog and release records change here.

Packaging validator passed: `python3 test/validate.py`, 5476 checks, exit 0.
Independent packaging review passed at `a039250ffccb20a40d97cd2af435e1800c702924`;
the reviewer inspected all nine files and independently passed 5476 structural checks.
Next: freeze PR43 for promotion and normal merge. Exact-source checks precede any annotated tag. No tag, publication, umbrella pin or installed
update is implied. Unknown ownership/metrics remain unresolved, not verified.

---

# FW05 journey and copy contracts — 2026-10-13

Branch `fix/fw05-journey-copy-contracts`, based on canonical `18d8ebe`, implements
B-025/B-026. Start with the [FW05 receipt](evidence/runs/2026-10-13-fw05-journey-copy.md).
The map Owner may be `unknown`; missing old fields are advisory. A marketing
brief is loaded only for a marketing writing task, never for unrelated work.
The brief's shape is checked, not the truth of its targets or evidence.

Full owner gate and independent bounded review passed at `b8305c5`; see receipt.
Next: freeze [PR42](https://github.com/ssheleg/super-ux/pull/42) for one deliberate
promotion and normal merge after required checks pass. The coordinator owns normal integration, version,
release, parent pins and installed/native acceptance; none follows from fixtures.
No agent/model behavioral eval was run by this change.

---

# Figma-practices handoff, 2026-10-08

Branch `feat/figma-practices` prepares super-ux 0.59.0: native annotations and a
ready-for-dev status on every approved frame, a resize pass before the critique,
Improve-mode capture into the surface's recorded file, the token tier model
delegated to sheleg-design, Code Connect upkeep, and routing words for
`ux-flows` and `copywriting`. Start with the
[0.59.0 changelog section](../CHANGELOG.md) and the
[verification ledger](evidence/verification.md) rows FP-1..FP-10.

- Done: every item of the 2026-10-08 Figma study; `validate_figma_practices`
  watched failing on 14 planted defects and on the `origin/main` text (37
  refusals); `npm test` and every CI step green locally.
- Open: review and merge, tag `v0.59.0`, npm publication, the umbrella pin in
  `sshlg-skills/skills.json`. None is implied by this branch.
- Depends on, outside this repo: the three links to sheleg-design's
  `FIGMA_BRIDGE.md#token-tiers` resolve on its `main` only once
  sheleg-design PR #41 merges (the heading is on its head `532a6b2`).
- The umbrella's selector cannot route the new phrases yet: "add a screen",
  "добавь экран", "макеты", "App Store description", "описание для App Store"
  return no route on `sshlg-skills` `origin/main`. Its completeness fixture will
  fail on the re-pin until `lib/triggers.js` gains them in the same change.
- Next task: review the PR, then release per `CONTRIBUTING.md` → Releasing.

---

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
- Revised after review: the matrix codes warn on format-1 registries and fail
  only on `<!-- screens-format: 2 -->`, which the seed writes; the doctor offers
  the migration and `/ux-update` performs it. Swept over 118 local registries:
  0 newly failing (the first cut newly failed 71). Ledger rows DF-MIG1..5.
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
