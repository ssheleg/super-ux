# Graph Report - .  (2026-08-10)

> **STALE as of 2026-08-14, and this says exactly how.** The graph below describes
> the tree at 1206 nodes and its labels still say "206 practices"; the catalog holds
> **215** and `funnel-research.md` does not appear in the graph at all
> (`funnel-research nodes: 0`). Eight commits have landed since it was built.
>
> **The refresh was attempted and did not run.** `graphify . --update` reported
> `11 code, 52 docs changed; 60 unchanged; 18 deleted` and then
> `error: no LLM API key found (52 doc/paper/image file(s) need semantic
> extraction)`. No LLM key is present in this environment — verified rather than
> assumed — and `graphify-out/graph.json` was left byte-for-byte unchanged, which
> `git status` confirms. `--code-only` would index without a key and is the wrong
> trade here: this repository is mostly doctrine, so a code-only graph would answer
> fewer questions than the stale one while looking current.
>
> The remaining path is the skill's documented fallback, where the host agent's own
> subagents do the semantic extraction. That was not taken in this run.
> Filed as a board row rather than left to be noticed.
>
> A stale graph is a false premise carrying the authority of a machine: a wrong doc
> gets argued with, a wrong graph gets believed. Read the two numbers above before
> trusting anything below them.

## Corpus Check
- 118 files · ~153,329 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1206 nodes · 2181 edges · 96 communities (66 shown, 30 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 115 edges (avg confidence: 0.84)
- Token cost: 159,126 input · 0 output

## Community Hubs (Navigation)
- Installer CLI (bin/super-ux.js)
- Brand Linter (project copy)
- doctor.py
- UX Linter (project copy)
- install.sh
- npm Package Manifest
- bp_index.py
- Brand Linter (plugin script)
- ux_doctor.py
- UX Linter (plugin script)
- brand_lint_test.py
- release_preflight.py
- sync_references.py
- ux_lint_test.py
- Repo Validator (test/validate.py)
- Contributor Surface and the Doctor
- Idea or improvement template — which layer does it belong to
- A rule nobody can verify is a suggestion
- PR evidence checklist — what you ran and what it printed
- release job — tag → validator → GitHub release
- Tag must match the manifests (version sync gate)
- CHANGELOG section extraction into release notes
- validate — CI workflow
- UX scenarios hard rule (super-ux)
- Hard Rules and Composition Gates
- Run each gate alone and read its own exit code
- Skill Parity and the 0.31–0.32 Releases
- Code of Conduct (adapted from Contributor Covenant 2.1)
- Why the contracts are duplicated per skill
- Stable IDs, never reused
- The family catalogue moves with the release
- The scenario-first hard rule
- The Reference Shelf
- The audit is read-only by default — a mismatch is a finding
- docs/brand/ — how this product speaks
- Locale parity computed against strings.md
- The String Registry and Its Codes
- Banned words
- Entity and tier names — exact spelling
- Glossary — chain, layer, trace, orphan, contract, style pack
- What the ladder walk found beyond the plan (cursor rule, sta
- Brand Contract Gates
- I-4 — Checked: only from BP-182 up
- The costliest ledger item was the cheapest — the assumption 
- The v0.33.0 Run — Brief, Plan, Release
- D1 — additive to v4, not a new contract version
- D3 — five fields, each the twin of an onpage check
- D4 — one project-level yes/no declaration
- UX Linter Codes and the Coverage Gate
- D6 — SEO gets a companion, not a /ux menu action
- D8 — v0.33.0 minor release
- R-08 — the /ux routing table speaks the four missing words
- Known-red until Group B lands — links are what sync follows
- Scenario Format and the Chain Contract
- Virality and referral cluster (REQ-01)
- BP-153 password rules by 800-63B-4: length and breach check
- Principle — we name defects with file:line, not with adjecti
- /brand-init command
- /ux-flows command
- /ux-init command
- /ux-lint command
- /ux — single entry point for all UX work
- Routing row: "new product" / "from scratch" → vision, then t
- Routing row: "check everything works" / audit → ux-audit
- Routing row: "what is missing" / gaps → coverage audit
- Brand Contract v1 and Its Sources
- Routing row: "will Google/ChatGPT find it" / SEO → Web surfa
- Practice Catalog and Its Generated Index
- Empty states, authentication & form recovery cluster BP-152.
- Verbal identity cluster BP-182..206
- docs/brand/facts.md — canonical figures, the only source
- docs/brand/channels.md — one record per surface (register, l
- Brand Pack Files and the Contract Marker
- Figma sync rule and boundaries (a rendering, never a replace
- Practice Selection Protocol
- Voice packs — the archetype library
- ux-foundation Skill
- UX Foundation Quality Bars
- Scenarios Come Before Interface (the hard rule)
- Per-Feature and Per-Product Completeness Checklists
- Audit Reports and Verdicts
- The Seeded Project Skeleton
- Scope and Limits (absence never means PASS)
- Heuristic Findings [PRN-NN] (deep depth)
- docs/brand README (how this product speaks)
- Brand Same-Change Rule
- Register as a Delta Against the Five Axes
- Fact Row Fields (Fact/Value/Source/Checked/Review by/Public)
- Locale Delta Template (locales/<code>.md)
- 0.30.2 — installer offers the family routing block
- 0.29.0 — /ux-doctor and doctor.py, IA practices, moderated t
- Releases 0.26–0.27
- 0.26.2 — shipped README corrected to the current family and 
- 0.23.1 — consistent American spelling across agent-facing fi
- ux-scenarios skill — scenario maintenance
- component-guidelines.md — which control for the job, platfor

## God Nodes (most connected - your core abstractions)
1. `brand_lint.py — the brand linter (35 deterministic checks)` - 43 edges
2. `ux_lint.py — the deterministic UX chain linter, seeded as docs/ux/lint.py` - 29 edges
3. `UX Best Practices Catalog BP-001..206` - 28 edges
4. `check()` - 26 edges
5. `/ux — single entry point for all UX work` - 26 edges
6. `validate_ux_lint_coverage — every emitted UX code needs a fixture and a contract row` - 26 edges
7. `read()` - 24 edges
8. `main()` - 23 edges
9. `Step 2 — Mandatory consideration sets` - 23 edges
10. `best-practices.md catalog (BP-001..206)` - 23 edges

## Surprising Connections (you probably didn't know these)
- `CI step: Claude Code conformance, plugin + marketplace --strict` --semantically_similar_to--> `validate_skill_parity — each skill asked for by name in five places`  [INFERRED] [semantically similar]
  .github/workflows/validate.yml → CHANGELOG.md
- `5. Principles` --semantically_similar_to--> `Anti-cargo-cult rule`  [INFERRED] [semantically similar]
  templates/vision.md → plugins/super-ux/skills/references/practice-selection.md
- `Do NOT trigger for bug fixes, refactors, tests, docs` --semantically_similar_to--> `Anti-cargo-cult rule`  [INFERRED] [semantically similar]
  templates/vision-rule.md → plugins/super-ux/skills/references/practice-selection.md
- `A rule nobody can verify is a suggestion` --semantically_similar_to--> `One owner per fact (convention)`  [INFERRED] [semantically similar]
  .github/ISSUE_TEMPLATE/feature_request.md → CONTRIBUTING.md
- `Forbidden carries both halves: physics and brand` --semantically_similar_to--> `One owner per fact (convention)`  [INFERRED] [semantically similar]
  docs/brand/channels.md → CONTRIBUTING.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The gate suite — each gate run alone and read by its own exit code** — github_workflows_validate_repo_consistency, github_workflows_validate_brand_lint_tests, github_workflows_validate_ux_lint_tests, github_workflows_validate_plugin_strict, readme_ux_lint, readme_brand_lint [INFERRED 0.85]
- **The three composition gates added in 0.32.0** — contributing_validate_stated_numbers, contributing_validate_skill_parity, contributing_validate_seeded_scripts, contributing_edit_sync_validate_loop [EXTRACTED 1.00]
- **The brand pack under brand-contract v1** — docs_brand_terminology_product_terms, docs_brand_facts_single_source_of_figures, docs_brand_channels_register_delta, docs_brand_locales_en_locale_delta, changelog_brand_contract_v1 [EXTRACTED 1.00]
- **docs/brand/ file set forming brand-contract v1** — docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_voice_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_terminology_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_facts_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_channels_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_strings_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_locales_files [EXTRACTED 1.00]
- **The super-ux traceability chain — vision → foundation → flows → screens → scenarios** — docs_ux_readme_pipeline, docs_ux_vision_essence, docs_ux_foundation_st_004, docs_ux_flows_flw_03, docs_ux_screens_scr_04, docs_ux_scenarios_scn_006 [EXTRACTED 1.00]
- **Degrade rather than block — the named degraded modes across the installer surface** — docs_ux_vision_principle_degrade_not_block, docs_ux_foundation_accessibility_regime, docs_ux_screens_scr_04, docs_ux_screens_scr_06, docs_ux_scenarios_scn_010, docs_ux_scenarios_scn_013 [INFERRED 0.85]
- **Bounded humanize pass — guards that stop the rewrite** — plugins_super_ux_skills_references_ai_tells_severity_scale, plugins_super_ux_skills_references_ai_tells_density_threshold, plugins_super_ux_skills_references_ai_tells_change_rate_guard, plugins_super_ux_skills_references_ai_tells_semantic_preservation_check, plugins_super_ux_skills_references_ai_tells_naturalness_grade [EXTRACTED 1.00]
- **The docs/brand/ pack — the six files brand-contract v1 governs** — plugins_super_ux_skills_references_brand_contract_voice_md, plugins_super_ux_skills_references_brand_contract_terminology_md, plugins_super_ux_skills_references_brand_contract_facts_md, plugins_super_ux_skills_references_brand_contract_channels_md, plugins_super_ux_skills_references_brand_contract_strings_md, plugins_super_ux_skills_references_brand_contract_locales_md [EXTRACTED 1.00]
- **Practice selection — profile, mandatory sets, artifact checklist, compliance record** — plugins_super_ux_skills_references_practice_selection_product_profile, plugins_super_ux_skills_references_practice_selection_mandatory_sets, plugins_super_ux_skills_references_practice_selection_per_artifact_checklists, plugins_super_ux_skills_references_practice_selection_compliance_table, plugins_super_ux_skills_references_practice_selection_anti_cargo_cult_rule [EXTRACTED 1.00]
- **What super-ux installs into a target project: two hard rules and two checkers** — templates_claude_rule_ux_scenarios_hard_rule, templates_claude_rule_brand_voice_hard_rule, templates_vision_rule_vision_alignment_hard_rule, templates_readme_lint_py, templates_readme_doctor_py [INFERRED 0.85]
- **The docs/brand Pack under brand-contract v1** — templates_brand_voice_voice_template, templates_brand_terminology_terminology_template, templates_brand_facts_facts_template, templates_brand_channels_channels_template, templates_brand_strings_strings_template, templates_brand_locale_locale_template, templates_brand_readme_brand_contract_v1 [EXTRACTED 1.00]
- **The ID Traceability Spine (ST/JTBD/JRN to FLW to SCR to SCN to string rows)** — templates_foundation_user_story_entry, templates_flows_flow_entry_fields, templates_scenarios_traces_field, templates_brand_strings_registry_columns [INFERRED 0.95]
- **The five required fields of a Web surface: block** — plugins_super_ux_skills_references_scenario_format_web_surface_field_route, plugins_super_ux_skills_references_scenario_format_web_surface_field_answers, plugins_super_ux_skills_references_scenario_format_web_surface_field_indexable, plugins_super_ux_skills_references_scenario_format_web_surface_field_without_js, plugins_super_ux_skills_references_scenario_format_web_surface_field_entity [EXTRACTED 1.00]
- **The three composition gates added after the 0.31.0 structural audit** — changelog_validate_stated_numbers, changelog_validate_skill_parity, changelog_validate_seeded_scripts [EXTRACTED 1.00]
- **The ux-contract v4 chain: vision, foundation, flows, screens, scenarios, audits, plans** — plugins_super_ux_skills_references_scenario_format_layer_vision, plugins_super_ux_skills_references_scenario_format_layer_foundation, plugins_super_ux_skills_references_scenario_format_layer_flows, plugins_super_ux_skills_references_scenario_format_layer_screens, plugins_super_ux_skills_references_scenario_format_layer_scenarios, plugins_super_ux_skills_references_scenario_format_layer_audits, plugins_super_ux_skills_references_scenario_format_layer_plans [EXTRACTED 1.00]

## Communities (96 total, 30 thin omitted)

### Community 15 - "Installer CLI (bin/super-ux.js)"
Cohesion: 0.18
Nodes (19): fs, path, readline, { spawnSync }, ROOT, MENU_ITEMS, usage(), fail() (+11 more)

### Community 3 - "Brand Linter (project copy)"
Cohesion: 0.10
Nodes (55): unfilled(), read(), Path, header_field(), table_rows(), load_sources(), check_contract(), Finding (+47 more)

### Community 32 - "doctor.py"
Cohesion: 0.38
Nodes (10): find_ux_dir(), Path, marker(), diagnose(), report(), fix(), brand_contract_state(), main() (+2 more)

### Community 12 - "UX Linter (project copy)"
Cohesion: 0.16
Nodes (26): err(), warn(), read(), Path, find_ux_dir(), ids(), index_ids(), refs() (+18 more)

### Community 7 - "npm Package Manifest"
Cohesion: 0.06
Nodes (33): name, version, description, bin, super-ux, files, bin, cursor (+25 more)

### Community 54 - "bp_index.py"
Cohesion: 0.43
Nodes (6): parse(), render(), stale_report(), main(), (id, title, tags, checked) for every entry, in catalog order. `checked` is ""…, Practices whose review date has aged past `months`, oldest first.

### Community 4 - "Brand Linter (plugin script)"
Cohesion: 0.10
Nodes (55): unfilled(), read(), Path, header_field(), table_rows(), load_sources(), check_contract(), Finding (+47 more)

### Community 34 - "ux_doctor.py"
Cohesion: 0.38
Nodes (10): find_ux_dir(), Path, marker(), diagnose(), report(), fix(), brand_contract_state(), main() (+2 more)

### Community 13 - "UX Linter (plugin script)"
Cohesion: 0.16
Nodes (26): err(), warn(), read(), Path, find_ux_dir(), ids(), index_ids(), refs() (+18 more)

### Community 59 - "brand_lint_test.py"
Cohesion: 0.47
Nodes (5): case(), fix_idempotent(), main(), Write a temp pack and compare the codes returned. `files` land inside the brand…, `--fix` clears what it claims to, and the second run has nothing left. A fixer…

### Community 64 - "sync_references.py"
Cohesion: 0.67
Nodes (3): closure(), main(), Every contract reachable from `seed` by following links between contracts.

### Community 60 - "ux_lint_test.py"
Cohesion: 0.33
Nodes (4): case(), silent(), Run the linter over a temp tree and compare the codes it emitted. Matching is…, The clean twin: these codes must NOT fire on this tree.

### Community 5 - "Repo Validator (test/validate.py)"
Cohesion: 0.10
Nodes (53): check(), read(), Path, raw_front_matter(), check_description_canon(), front_matter(), load_json(), changelog_version() (+45 more)

### Community 22 - "Contributor Surface and the Doctor"
Cohesion: 0.18
Nodes (14): Bug report template — quote the file that says so, Test from a packed tarball, not the working tree, docs/ux/lint.py + /ux-lint — the deterministic half, ux_doctor.py — the contract doctor, scenario-format.md — the contract, The defect — the contract never mentions indexability, R-01 — the screen record gains the optional five-field Web surface: block, R-02 — screens.md carries one project-level Web surfaces: declaration (+6 more)

### Community 56 - "Idea or improvement template — which layer does it belong to"
Cohesion: 0.33
Nodes (6): Idea or improvement template — which layer does it belong to?, Every link in a skill is a shipping instruction, system-map.md — the whole system on one page, R-07 — seo-aeo-audit offered as the third companion, recommend-never-force, Original v0.1.0 implementation plan (historical), T6 — seo-aeo-audit becomes the third companion

### Community 46 - "A rule nobody can verify is a suggestion"
Cohesion: 0.25
Nodes (8): A rule nobody can verify is a suggestion, Vision alignment hard rule (super-ux), A hard rule has one source text in templates/, One owner per fact (convention), Forbidden carries both halves: physics and brand, Validator written first, red while files are missing, Task 1 — author brand-contract v1 (single definition of every field), Tasks 13–17 — brand_lint.py check families B001..B073

### Community 61 - "release job — tag → validator → GitHub release"
Cohesion: 0.40
Nodes (5): release job — tag → validator → GitHub release, publish job — npm publish --provenance, Dual auth — NPM_TOKEN automation token and OIDC trusted publishing, Published is a claim until the registry serves it — poll loop, Post-release npx smoke test from a clean cwd

### Community 52 - "validate — CI workflow"
Cohesion: 0.29
Nodes (7): validate — CI workflow, CI step: Validate repo consistency (test/validate.py), CI step: Brand linter unit tests (fixture per check code), CI step: UX linter fixtures (test/ux_lint_test.py), CI step: Claude Code conformance, plugin + marketplace --strict, R-10 — hard-rule copies, Cursor rules and both manifests stay in sync, T8 — sync_references.py, then every gate alone by its own exit code

### Community 26 - "UX scenarios hard rule (super-ux)"
Cohesion: 0.15
Nodes (13): UX scenarios hard rule (super-ux), The design chain — vision → foundation → flows → screens → scenarios → build → audit, skill: vision, skill: ux-foundation (the WHY layer), skill: ux-flows (the HOW layer + the UI map), skill: ux-scenarios, skill: ux-audit, companion: task-pipeline (+5 more)

### Community 23 - "Hard Rules and Composition Gates"
Cohesion: 0.15
Nodes (14): Brand voice hard rule (super-ux), validate_stated_numbers invariant, validate_seeded_scripts invariant, Never stamp a Checked date you did not earn, docs/brand/lint.py — 35 deterministic checks (B001..B073), Sources: block — what the linter is allowed to read, Brand same-change hard rule, Surface: error (+6 more)

### Community 62 - "Run each gate alone and read its own exit code"
Cohesion: 0.50
Nodes (4): Run each gate alone and read its own exit code, The edit → sync → validate loop, release_preflight.py, git push --atomic origin main vX.Y.Z

### Community 8 - "Skill Parity and the 0.31–0.32 Releases"
Cohesion: 0.12
Nodes (32): A skill exists in seven places or it does not exist, validate_skill_parity invariant, 0.32.0 — 22 structural audit findings closed, three composition gates, dogfood chain, 0.31.0 — vision skill and /vision, the layer above ux-foundation, 0.30.1 (undated heading) — brand-contract owns all 33 codes, validate_brand_lint_coverage, code graph, 0.30.0 (undated heading) — verbal identity layer: brand-contract v1, brand-voice, copywriting, brand_lint.py, validate_run_instructions — every script path an instruction tells the reader to run must be seeded by some command, validate_seeded_scripts — every script an instruction names is copied there by some command (+24 more)

### Community 37 - "The family catalogue moves with the release"
Cohesion: 0.24
Nodes (10): The family catalogue moves with the release, super-ux — scenario-driven UI development for AI agents, docs/brand/ — the brand layer, skill: brand-voice, skill: copywriting, /ux — the one command, The ssheleg skill family, A plain skills copy shadows the plugin (+2 more)

### Community 36 - "The scenario-first hard rule"
Cohesion: 0.33
Nodes (10): The scenario-first hard rule, companion: sheleg-design, Craft floors vs style pack — the boundary, visual-identity.md — the visual layer and its owner, Invariants in every language, 0.22.0 — the visual layer gets an owner: sheleg-design and the Style pack field, sheleg-design companion — owns the visual layer and the style packs, visual-identity.md — one locked style pack as the product identity (+2 more)

### Community 11 - "The Reference Shelf"
Cohesion: 0.09
Nodes (27): best-practices.md — 206 proven practices, best-practices-index.md — generated tag index, practice-selection.md — profile → mandatory sets → compliance table, ux-design-principles.md — heuristics PRN-01..24, component-guidelines.md — which control for which job, Acceptance — tier-1 audit findings (v0.27.1), Brief — tier-1 findings from the 51-skill audit, Carry-over ledger (deferred work, never empty) (+19 more)

### Community 39 - "docs/brand/ — how this product speaks"
Cohesion: 0.25
Nodes (9): docs/brand/ — how this product speaks, Register as a delta on the five axes, Surface: primary action, Surface: empty state, Surface: destructive confirm, Locale delta file (en, primary), Length coefficient and its effective limits, Dead idioms table (+1 more)

### Community 0 - "The String Registry and Its Codes"
Cohesion: 0.05
Nodes (80): Interface string registry (docs/brand/strings.md), String menu.nothing — "Nothing selected", B020 — one action under two names, B021 — registry text disagrees with the source, B023 — a location that no longer resolves, The word prefix is the vocabulary (install:/skip:/keep:/seed:/sync:/warning:/error:), Interpolated messages left unregistered, and why, D2 — a block inside screens.md, not a new docs/ux/web.md (+72 more)

### Community 47 - "Glossary — chain, layer, trace, orphan, contract, style pack"
Cohesion: 0.25
Nodes (8): Glossary — chain, layer, trace, orphan, contract, style pack, register, peer-builder — the chosen voice pack, calm-expert — the runner-up pack, The five fixed voice axes, Brand narrative — hero, enemy, product role, promise, Failure mode — insider shorthand and performed honesty, Admired reference: Stripe's API documentation, Refused reference: the "We're thrilled to announce" launch-post register

### Community 19 - "Brand Contract Gates"
Cohesion: 0.15
Nodes (16): Acceptance record - verbal layer v0.30.0 (25/25 REQ), validate_brand_contract, validate_voice_packs, validate_brand_field_ownership, sync_references.py, Carry-over ledger C-01..C-06, C-03 code graph (698 nodes, 1353 edges, 38 communities), .graphifyignore (+8 more)

### Community 14 - "The v0.33.0 Run — Brief, Plan, Release"
Cohesion: 0.16
Nodes (24): Brief — a public web surface gets a home, and the router learns the user's words, R-13 — v0.33.0 ships: four version places, preflight, atomic push, CI verdict, registry, Plan — web surface in the contract, and a router that speaks, T10 — release v0.33.0, Set comparison — REQs equal the union of Implements:, 0.34.0 — UX linter codes U001..U054 and two coverage gates, 0.33.0 — Web surface block, routing rows, B007/B026, ux_lint fixture harness, test/ux_lint_test.py — fixture harness for the UX linter, 43 checks over 21 codes (+16 more)

### Community 10 - "UX Linter Codes and the Coverage Gate"
Cohesion: 0.15
Nodes (29): D5 — malformed block is an error, missing declaration a warning, validate_ux_lint_coverage — every emitted UX code needs a fixture and a contract row, ux_lint.py — the deterministic UX chain linter, seeded as docs/ux/lint.py, ux-design-principles.md — the design reasoning behind the formats, B-005 — templates/vision.md is all comments, and read() strips them, so an unwritten vision lints clean until marked approved (open, 12), UX Contract v4 — vision, foundation, flows, screens, scenarios, audits, The chain — Personas to Jobs to Journeys to Stories to Flows to Screens to Scenarios to Audits to Fix plans, docs/ux/vision.md — WHAT IT IS: essence, principles, anti-vision, alignment test (+21 more)

### Community 65 - "R-08 — the /ux routing table speaks the four missing words"
Cohesion: 0.67
Nodes (3): R-08 — the /ux routing table speaks the four missing words, R-09 — a composite brief is decomposed and ordered by chain position, T7 — commands/ux.md routing rows and composite-brief decomposition

### Community 1 - "Scenario Format and the Chain Contract"
Cohesion: 0.05
Nodes (74): Scenario-first methodology, Target-project docs/ux contract, scenarios.md format contract, SCN-NNN id and status lifecycle rules, Audit report format (docs/ux/audits), Audit verdicts PASS/PARTIAL/FAIL/BLOCKED, ux-scenarios skill (v0.1 design), ux-audit skill batch loop (v0.1 design) (+66 more)

### Community 53 - "Virality and referral cluster (REQ-01)"
Cohesion: 0.52
Nodes (7): Virality and referral cluster (REQ-01), BP-147 growth loop named before freemium, BP-148 virality through the product artifact, BP-149 plan K near 0.2 and design cycle time, BP-150 reward in product units, on invitee milestone, BP-151 referral abuse designed against, not discovered, [Viral26] converged virality/referral benchmarks 2026

### Community 63 - "BP-153 password rules by 800-63B-4: length and breach check"
Cohesion: 0.67
Nodes (4): BP-153 password rules by 800-63B-4: length and breach check, BP-154 password field does not fight the password manager, BP-155 passwordless offered as an equal door, [NIST] SP 800-63B rev 4 Digital Identity Guidelines

### Community 40 - "/brand-init command"
Cohesion: 0.25
Nodes (9): /brand-init command, plugin scripts/brand_lint.py, Never invent a fact to fill a table, /ux-doctor command, Contract drift (project vs contract version), plugin scripts/ux_doctor.py, /ux-rule command, Brand voice hard rule (installed block) (+1 more)

### Community 41 - "/ux-flows command"
Cohesion: 0.25
Nodes (9): /ux-flows command, UX scenarios hard rule (installed block), Routing row: "the UX is bad" / "clunky" → ux-flows Improve, Rule 1 — Chain-first (no UI code before the chain is approved), Rule 2 — Same-change (affected layers update in the SAME change), ux-flows (skill) — design HOW users move; owns flows.md and screens.md, The build gate — interface code waits for the finished chain, Prototype when the answer is not on paper (optional step) (+1 more)

### Community 48 - "/ux-init command"
Cohesion: 0.39
Nodes (8): /ux-init command, Never seed an empty vision.md, /vision command, vision skill, The nine vision layers, Anti-vision (what the product refuses to become), The alignment test (feature admission questions), Vision-alignment hard rule

### Community 33 - "/ux — single entry point for all UX work"
Cohesion: 0.20
Nodes (11): /ux — single entry point for all UX work, Routing row: "new feature" → validate idea vs chain and anti-vision, Routing row: "the copy is inconsistent" / "tone of voice" → brand-voice, Routing row: "write the button/error/landing/post" → copywriting, Routing row: "what to fix first" / plan → UX plan, Routing row: "the funnel" / "pricing page" / "checkout" → a funnel is a flow with screens, Routing row: "mobile app" / "iOS/Android" → foundation Platform first, Routing row: "don't know" / "just take a look" → inspect, then recommend (+3 more)

### Community 49 - "Routing row: "new product" / "from scratch" → vision, then t"
Cohesion: 0.32
Nodes (8): Routing row: "new product" / "from scratch" → vision, then the chain, Routing row: "what are we even building" / "product vision" → vision, super-ux System Map — the whole system on one page, Rule 3 — No drift (divergence is a finding, not a state), The map names a contract, it never links one, vision (skill) — what the product is and refuses to become, ux-scenarios (skill) — build and maintain the WHAT layer, System map — the copy shipped inside the vision skill

### Community 43 - "Routing row: "check everything works" / audit → ux-audit"
Cohesion: 0.22
Nodes (9): Routing row: "check everything works" / audit → ux-audit, Rule 4 — Run the linter before calling work done, ux-foundation (skill) — personas, JTBD, journeys, stories, task-pipeline (companion) — implements a finished UX plan end-to-end, /ux-lint — the drift linter (docs/ux/lint.py), ux-audit (skill) — the scenario audit loop, Benchmark scope (`benchmark:<competitor>`), Evidence discipline — every verdict cites file:line (+1 more)

### Community 42 - "Routing row: "what is missing" / gaps → coverage audit"
Cohesion: 0.22
Nodes (9): Routing row: "what is missing" / gaps → coverage audit, Routing row: "what do best practices say" → practices / heuristics audit, Routing row: "design it" / "how should it look" → flows, visual identity settled first, sheleg-design (companion) — the visual identity and motion methodology, What the audit checks when a Style pack is recorded, Depth levels — quick / standard / deep, Pass 2 — flow & screen conformance (incl. the Web surface check), Pass 4 — practice pass (BP-NNN compliance table) (+1 more)

### Community 20 - "Brand Contract v1 and Its Sources"
Cohesion: 0.17
Nodes (16): Routing row: "does the copy match the brand" → ux-audit copy scope, Brand Contract v1 — the contract for docs/brand/, docs/brand/voice.md — pack, axes, narrative, invariants, locales, The Sources: block in docs/brand/README.md, The five fixed voice axes (Confidence, Register, Distance, Humor, Density), Humor is forbidden where the user is losing something, Platform physics and brand choice are separate fields, Register moves the axes; it never crosses the invariants (+8 more)

### Community 27 - "Routing row: "will Google/ChatGPT find it" / SEO → Web surfa"
Cohesion: 0.19
Nodes (13): Routing row: "will Google/ChatGPT find it" / SEO → Web surface block at design time, seo-aeo-audit (companion plugin), Settle the second reader, in the same breath (design step 5), templates/screens.md — the seeded UI Screen Registry, Seeded default `Web surfaces: no`, R-02 — screens.md declares Web surfaces yes|no; absence is declared, not assumed (planted), Web surfaces: yes | no — answered once per project in screens.md, Web surface: block — the five required fields a public-URL screen carries (+5 more)

### Community 6 - "Practice Catalog and Its Generated Index"
Cohesion: 0.06
Nodes (45): Best-Practices Index (generated), Tag → BP-id index (82 tags, 206 practices), bp_index.py generator + drift validator, UX Best Practices Catalog BP-001..206, BP tag taxonomy (stage/mechanism/domain/channel/craft/verbal/components), BP-001 Adapt competitor tactics, don't copy them, Behavioral practices cluster BP-001..078, Visual craft cluster BP-079..090 (typography, color, layout) (+37 more)

### Community 38 - "Empty states, authentication & form recovery cluster BP-152."
Cohesion: 0.22
Nodes (10): Empty states, authentication & form recovery cluster BP-152..156, docs/brand/terminology.md — our words, banned words, entity and tier names, B010 (E) — a banned word appears in a registered string, B011 (E) — a generic word used where a product term exists, B012 (E) — an entity or tier name spelled inconsistently, Product surface registers (primary action → docs and help), UI copy — the strings inside the product, The four laws of UI copy (+2 more)

### Community 44 - "Verbal identity cluster BP-182..206"
Cohesion: 0.31
Nodes (9): Verbal identity cluster BP-182..206, Locales — one voice, several languages, What travels and what does not (invariant vs reconsidered per locale), Translate the job the string does, not the words (B072), Parity declared rather than hidden (B071), Keywords are researched per market, never translated, Store listings — App Store and Google Play, The iOS keyword field (B041 — four rules) (+1 more)

### Community 24 - "docs/brand/facts.md — canonical figures, the only source"
Cohesion: 0.20
Nodes (14): docs/brand/facts.md — canonical figures, the only source, B030 (E) — a figure in public copy has no row in facts.md, B031 (W) — a fact has no source, or is past its Review by, Marketing copy — pages, posts and long form, Four inputs before writing (action, reader, their words, proof), Page structure (headline → final CTA) and page types, The seven sweeps (clarity → zero risk), The grounding model (prerequisite vs introduced) (+6 more)

### Community 25 - "docs/brand/channels.md — one record per surface (register, l"
Cohesion: 0.22
Nodes (14): docs/brand/channels.md — one record per surface (register, limits, bans), B040 (E) — a field exceeds its surface limit, B073 (E) — a field overflows under the locale's coefficient, Channel Playbooks — the physics of each surface, Platform physics per marketing surface, Physics decays — every ranking behaviour carries a checked date, Length coefficient (multiplies every field limit per locale), Store field limits and the two structural differences (+6 more)

### Community 9 - "Brand Pack Files and the Contract Marker"
Cohesion: 0.08
Nodes (30): docs/brand/strings.md — interface string registry, docs/brand/locales/<code>.md — per-locale delta, The contract marker line (`Contract: brand-contract v1`), brand_lint.py — the brand linter (35 deterministic checks), B001 (E) — a file under docs/brand/ has no contract marker, B002 (E) — markers disagree across the pack, B003 (W) — voice.md is draft while strings.md holds agreed rows, B004 (E) — Derived-from cites an id absent from foundation.md (+22 more)

### Community 31 - "Figma sync rule and boundaries (a rendering, never a replace"
Cohesion: 0.20
Nodes (11): Figma sync rule and boundaries (a rendering, never a replacement), 0.24.0 — Figma MCP tool gates, tool map, cheap-tool drift checks, token parity, ux-flows skill — flows, screens registration and Figma mockups, figma-integration.md — the Figma MCP tool map and drift checks, figma-structure.md — Figma file structure, SCR-NN frame naming, token tiers, B-004 — screens.md coverage file:line ranges are never re-resolved by any check (open, 12), B023 — the brand linter check that does re-resolve a registry file:line, R-05 — ux-flows asks the web-surface question beside Figma and the style pack (observed) (+3 more)

### Community 2 - "Practice Selection Protocol"
Cohesion: 0.08
Nodes (59): Practice Selection Protocol, Step 1 — Product profile, Step 2 — Mandatory consideration sets, Step 3 — Per-artifact checklists, Step 4 — Compliance table (the record), Anti-cargo-cult rule, Style pack vs practices precedence, best-practices.md catalog (BP-001..206) (+51 more)

### Community 50 - "Voice packs — the archetype library"
Cohesion: 0.46
Nodes (8): Voice packs — the archetype library, The pack contract (nine fields every pack carries), Pack: operator-brief, Pack: calm-expert, Pack: peer-builder, Pack: editorial-premium, Pack: plain-service, Pack: playful-consumer

### Community 28 - "ux-foundation Skill"
Cohesion: 0.18
Nodes (13): ux-foundation Skill, Cascade Check to Downstream Layers, Figma On/Off Choice Asked Once Per Project, Product Mechanics Recorded Even When None, ux-scenarios Skill, Retire, Never Delete, UX Foundation Template (foundation.md), Persona Entry P-NN (+5 more)

### Community 18 - "UX Foundation Quality Bars"
Cohesion: 0.17
Nodes (17): JTBD Four Forces Quality Bar, Frequency x Severity x Solvability Scoring, INVEST Stories with Given/When/Then Criteria, Reviews and Support Tickets Are Evidence Already Sitting There, Foundation Validate Pass (integrity, quality, coverage), Scenario Traceability Rules, User Flows Template (flows.md), FLW-NN Entry Fields (Traces/Goal/Entry points/Success exit/Task analysis) (+9 more)

### Community 45 - "Per-Feature and Per-Product Completeness Checklists"
Cohesion: 0.25
Nodes (9): Per-Feature and Per-Product Completeness Checklists, Channels Template (one record per surface), Channel Record Fields (Register/Format/Limits/Forbidden/CTA/Proof/Locales), Forbidden Splits Platform Physics from Brand Choice, Product Surfaces (primary action, error, empty state, paywall, destructive confirm), Marketing Surfaces (landing hero, X, Reddit, …), Length Coefficient, Length Notes (constraint reaches the primary-locale original) (+1 more)

### Community 21 - "Audit Reports and Verdicts"
Cohesion: 0.15
Nodes (15): Moderated Test Tasks Generated from the Scenario Base, Init from Existing Code (inventory sweep), UX Audit Report Template, Per-Scenario Verdicts PASS/PARTIAL/FAIL/BLOCKED, Finding ID Scheme AUD-YYYY-MM-DD-NN, Overall Verdict REFINE/REDESIGN/NEW, Practice Compliance Table (deep audits), Base Version (git SHA of docs/ux at audit time) (+7 more)

### Community 17 - "The Seeded Project Skeleton"
Cohesion: 0.12
Nodes (20): Seeded docs/ux/README.md, Pipeline table (file → what it holds), Two files answer a "what" question, docs/brand/ as the sibling root, The four seeded rules (design before build, same change, no drift, lint it), docs/ux/lint.py — the integrity/drift linter, docs/ux/doctor.py — the contract doctor, Vision alignment — hard rule (super-ux) (+12 more)

### Community 30 - "Scope and Limits (absence never means PASS)"
Cohesion: 0.17
Nodes (12): Scope and Limits (absence never means PASS), Sources Block (B006 — no clean run over an unread surface), docs/brand/lint.py Copy Linter, Surface Names Are Contract Keys (delete, never rename), Facts Template (the only source of any public figure), B030 — public number with no facts row blocks, B031 — missing Source or past Review by warns, Public: no — figures that exist and must never be quoted (+4 more)

### Community 55 - "docs/brand README (how this product speaks)"
Cohesion: 0.29
Nodes (7): docs/brand README (how this product speaks), brand-contract v1, Brand Commands (/brand, /brand-init, /brand-update, /brand-lint, /copy), Interface Strings Registry Template, B021 — Code No Longer Matches the Row, B022 — String in Code With No Registry Row, String Statuses (agreed/proposed/drifted/orphan)

### Community 58 - "Fact Row Fields (Fact/Value/Source/Checked/Review by/Public)"
Cohesion: 0.33
Nodes (6): Fact Row Fields (Fact/Value/Source/Checked/Review by/Public), Terminology Template (the dictionary the linter reads), Product Terms — B010, Banned Words — B011, Glossary (grounded before it is leaned on), Banned List Seeded from ai-tells.md

### Community 51 - "Locale Delta Template (locales/<code>.md)"
Cohesion: 0.25
Nodes (8): Locale Delta Template (locales/<code>.md), Locale Header Fields (Locale/Primary/Address form/Coefficient/Humor/Never translated/Reviewed by), Address Form (decided once, not per string), Dead Idioms Table (replacement does the same job), Keywords Researched in Market, Never Translated, B020 — One Action, Two Names, A Decision Registry, Not a Message Catalog, Entity and Tier Names — B012 (one spelling everywhere)

### Community 35 - "0.30.2 — installer offers the family routing block"
Cohesion: 0.20
Nodes (10): 0.30.2 — installer offers the family routing block, 0.26.5 — displayName in both manifests, 0.23.2 — open-source hygiene: SECURITY.md, code of conduct, PR template, 0.21.0 — full-repo consistency pass; npx --cursor crash fixed, one owner per fact, 0.19.0 — shared contracts now ship with every skill (per-skill references/), B026 — a label, button, menu item or title takes no full stop, One owner per fact, bin/super-ux.js — the installer CLI and its interactive menu (+2 more)

### Community 29 - "0.29.0 — /ux-doctor and doctor.py, IA practices, moderated t"
Cohesion: 0.17
Nodes (12): 0.29.0 — /ux-doctor and doctor.py, IA practices, moderated test tasks, benchmark scope, ux_doctor.py — contract-version doctor, seeded as docs/ux/doctor.py, brand-voice skill — defines and holds the verbal identity, voice.md — voice pack, five axes as IS / IS NOT, narrative, invariants, Ledger run 2026-08-10 — web surface and routing, v0.33.0, 15 rows, 0 at never, R-01 — a public screen records five fields, each the design-time twin of a live-page check (observed), R-03 — a partial Web surface block errors; no silences; a URL entry point under no still warns (planted), R-07 — seo-aeo-audit is the third companion, install commands verified against the registry (observed) (+4 more)

### Community 16 - "Releases 0.26–0.27"
Cohesion: 0.11
Nodes (20): 0.27.1 — re-cut of 0.27.0 on the correct base, 0.27.0 — growth loops, empty states, auth/form recovery, audit Scope and limits, validate_catalog, 0.26.4 — /ux-audit front matter parsed as a YAML list and dropped every field, 0.26.3 — SPDX MIT licence declared where a user can see it, 0.26.1 — foundation contract section 7, Product mechanics, 0.26.0 — motion, page weight, accessibility as it fails, frustration telemetry, trend governance, 0.25.0 — web funnels BP-116..123 and web2app BP-124..129, purchase surface, 0.23.0 — hard rule corrected to the four-layer chain, CONTRIBUTING.md, README rewrite (+12 more)

### Community 57 - "ux-scenarios skill — scenario maintenance"
Cohesion: 0.40
Nodes (6): ux-scenarios skill — scenario maintenance, strings.md — the interface string registry, key to file:line to scenario, B022 — an interface literal with no registry row, B-003 — the B022 literal extractor is a regex, not a tokenizer, so multi-line template literals are invisible (open, 6), docs/ux/scenarios.md — WHAT: use-case scenarios, the source of truth for behavior, Strings: (optional) — the strings.md keys a scenario's steps depend on

## Knowledge Gaps
- **205 isolated node(s):** `fs`, `path`, `readline`, `{ spawnSync }`, `ROOT` (+200 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UX Contract v4 — vision, foundation, flows, screens, scenarios, audits` connect `UX Linter Codes and the Coverage Gate` to `Practice Selection Protocol`, `0.30.2 — installer offers the family routing block`, `Brand Pack Files and the Contract Marker`, `/ux-flows command`, `Routing row: "check everything works" / audit → ux-audit`, `Routing row: "new product" / "from scratch" → vision, then t`, `The Seeded Project Skeleton`, `Brand Contract v1 and Its Sources`, `Routing row: "will Google/ChatGPT find it" / SEO → Web surfa`, `0.29.0 — /ux-doctor and doctor.py, IA practices, moderated t`, `Figma sync rule and boundaries (a rendering, never a replace`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Why does `/ux-rule command` connect `/brand-init command` to `/ux-flows command`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `Brand Contract v1 — the contract for docs/brand/` connect `Brand Contract v1 and Its Sources` to `/ux — single entry point for all UX work`, `Empty states, authentication & form recovery cluster BP-152.`, `Brand Pack Files and the Contract Marker`, `UX Linter Codes and the Coverage Gate`, `Routing row: "new product" / "from scratch" → vision, then t`, `Brand Contract Gates`, `docs/brand/facts.md — canonical figures, the only source`, `docs/brand/channels.md — one record per surface (register, l`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **What connects `fs`, `path`, `readline` to the rest of the system?**
  _205 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Brand Linter (project copy)` be split into smaller, more focused modules?**
  _Cohesion score 0.09610389610389611 - nodes in this community are weakly interconnected._
- **Should `npm Package Manifest` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._
- **Should `Brand Linter (plugin script)` be split into smaller, more focused modules?**
  _Cohesion score 0.09610389610389611 - nodes in this community are weakly interconnected._