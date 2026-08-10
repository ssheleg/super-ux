# Graph Report - .  (2026-08-10)

## Corpus Check
- 117 files · ~149,775 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1126 nodes · 2052 edges · 76 communities (52 shown, 24 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 120 edges (avg confidence: 0.84)
- Token cost: 380,015 input · 0 output

## Community Hubs (Navigation)
- Slash Commands and the Routing Table
- Scenario Format and Audit Contract
- Brand Linter (project copy)
- Brand Linter (plugin script)
- Practice Catalog and Selection
- UX Foundation Layer
- Repo Validator (test/validate.py)
- Best-Practice Catalog Clusters
- Installer Flows, Journeys and Stories
- Retros and Composition Gates
- npm Package Manifest
- Brand Check Codes B001–B006
- UX Linter (project copy)
- UX Linter (plugin script)
- Pipeline Records — Briefs, Plans, Acceptance
- Installer CLI (bin/super-ux.js)
- The v0.33.0 Copy Checks (B007, B026)
- Vision Layer and the Open Board
- Carry-Over Ledger and Code Graph
- Channel Records and Field Limits
- Style Pack and Surface Registers
- Release Discipline and the Web-Surface Declaration
- ux-contract v4 and Glossary
- Reference Sync and the Composition Gates
- Hard Rules and Stated Numbers
- Voice Axes and Verbal Practices
- Fact Sourcing and Comparison Honesty
- The Web Surface Block and Its Companion
- Web-Surface Requirements and the Journey Gap
- The Nine Vision Sections
- Family Catalogue and the Copy Brief Gap
- Contract Doctor (project copy)
- Contract Doctor (plugin script)
- The String Registry
- Brand Commands and Seeded Scripts
- Channel Playbooks and Completeness
- Terminology and Product Terms
- The Six Voice Packs
- Localization and Locale Deltas
- A Rule With One Source Text
- Virality and Referral Practices
- Practice Index Generator
- Brand Contract v1 and Its Commands
- Shipping Instructions and the Third Companion
- Facts Template and Non-Numeric Proof
- Banned Words and the Glossary
- The Seeded Project Skeleton
- Brand Lint Fixtures
- npm Release and Publish Jobs
- UX Lint Fixtures (new in 0.33.0)
- Password and Auth Practices
- Reference Closure Sync
- Shell Installer
- Release Preflight
- Code of Conduct and Security Policy
- Ledger Assumptions
- Extractor Requirements R-11/R-12
- PR Evidence Checklist
- Changelog Release Notes
- Version Sync Gate
- Why Contracts Are Duplicated
- Stable IDs
- Locale Parity
- Banned Words Marker
- Entity and Tier Names
- Ladder Walk Extras
- Checked Dates From BP-182
- Known-Red Until Sync
- R-07 Command and Template Count
- R-10 Figure Detection
- /ux-lint Command
- Scenarios Before Interface
- Read-Only Audit Stance
- Heuristic Findings Pass
- Register as a Delta
- Brand Same-Change Rule

## God Nodes (most connected - your core abstractions)
1. `brand_lint.py — the brand linter (35 deterministic checks)` - 44 edges
2. `/ux — single entry point for all UX work` - 32 edges
3. `UX Best Practices Catalog BP-001..206` - 28 edges
4. `check()` - 24 edges
5. `Step 2 — Mandatory consideration sets` - 23 edges
6. `best-practices.md catalog (BP-001..206)` - 23 edges
7. `read()` - 22 edges
8. `Brand Contract v1 — the contract for docs/brand/` - 22 edges
9. `main()` - 21 edges
10. `super-ux System Map — the whole system on one page` - 20 edges

## Surprising Connections (you probably didn't know these)
- `5. Principles` --semantically_similar_to--> `Anti-cargo-cult rule`  [INFERRED] [semantically similar]
  templates/vision.md → plugins/super-ux/skills/references/practice-selection.md
- `Do NOT trigger for bug fixes, refactors, tests, docs` --semantically_similar_to--> `Anti-cargo-cult rule`  [INFERRED] [semantically similar]
  templates/vision-rule.md → plugins/super-ux/skills/references/practice-selection.md
- `A plain skills copy shadows the plugin` --semantically_similar_to--> `Transitive-closure reference sync (sync_references.py)`  [INFERRED] [semantically similar]
  README.md → CHANGELOG.md
- `A rule nobody can verify is a suggestion` --semantically_similar_to--> `One owner per fact (convention)`  [INFERRED] [semantically similar]
  .github/ISSUE_TEMPLATE/feature_request.md → CONTRIBUTING.md
- `Validator written first, red while files are missing` --semantically_similar_to--> `A rule nobody can verify is a suggestion`  [INFERRED] [semantically similar]
  docs/superpowers/plans/2026-07-19-super-ux.md → .github/ISSUE_TEMPLATE/feature_request.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The three composition gates added in 0.32.0** — contributing_validate_stated_numbers, contributing_validate_skill_parity, contributing_validate_seeded_scripts, contributing_edit_sync_validate_loop [EXTRACTED 1.00]
- **The brand pack under brand-contract v1** — docs_brand_terminology_product_terms, docs_brand_facts_single_source_of_figures, docs_brand_channels_register_delta, docs_brand_locales_en_locale_delta, changelog_brand_contract_v1 [EXTRACTED 1.00]
- **The composition gates added after the 2026-08-10 audit** — docs_superpowers_retro_2026_08_10_composition, docs_superpowers_retro_validate_stated_numbers, docs_superpowers_retro_validate_skill_parity, docs_superpowers_retro_validate_seeded_scripts, docs_superpowers_retro_validate_hard_rule_copies, docs_superpowers_retro_shape_vs_composition [EXTRACTED 1.00]
- **docs/brand/ file set forming brand-contract v1** — docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_voice_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_terminology_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_facts_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_channels_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_strings_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_locales_files [EXTRACTED 1.00]
- **The super-ux traceability chain — vision → foundation → flows → screens → scenarios** — docs_ux_readme_pipeline, docs_ux_vision_essence, docs_ux_foundation_st_004, docs_ux_flows_flw_03, docs_ux_screens_scr_04, docs_ux_scenarios_scn_006 [EXTRACTED 1.00]
- **Degrade rather than block — the named degraded modes across the installer surface** — docs_ux_vision_principle_degrade_not_block, docs_ux_foundation_accessibility_regime, docs_ux_screens_scr_04, docs_ux_screens_scr_06, docs_ux_scenarios_scn_010, docs_ux_scenarios_scn_013 [INFERRED 0.85]
- **Bounded humanize pass — guards that stop the rewrite** — plugins_super_ux_skills_references_ai_tells_severity_scale, plugins_super_ux_skills_references_ai_tells_density_threshold, plugins_super_ux_skills_references_ai_tells_change_rate_guard, plugins_super_ux_skills_references_ai_tells_semantic_preservation_check, plugins_super_ux_skills_references_ai_tells_naturalness_grade [EXTRACTED 1.00]
- **Practice selection — profile, mandatory sets, artifact checklist, compliance record** — plugins_super_ux_skills_references_practice_selection_product_profile, plugins_super_ux_skills_references_practice_selection_mandatory_sets, plugins_super_ux_skills_references_practice_selection_per_artifact_checklists, plugins_super_ux_skills_references_practice_selection_compliance_table, plugins_super_ux_skills_references_practice_selection_anti_cargo_cult_rule [EXTRACTED 1.00]
- **What super-ux installs into a target project: two hard rules and two checkers** — templates_claude_rule_ux_scenarios_hard_rule, templates_claude_rule_brand_voice_hard_rule, templates_vision_rule_vision_alignment_hard_rule, templates_readme_lint_py, templates_readme_doctor_py [INFERRED 0.85]
- **The docs/brand Pack under brand-contract v1** — templates_brand_voice_voice_template, templates_brand_terminology_terminology_template, templates_brand_facts_facts_template, templates_brand_channels_channels_template, templates_brand_strings_strings_template, templates_brand_locale_locale_template, templates_brand_readme_brand_contract_v1 [EXTRACTED 1.00]
- **The ID Traceability Spine (ST/JTBD/JRN to FLW to SCR to SCN to string rows)** — templates_foundation_user_story_entry, templates_flows_flow_entry_fields, templates_scenarios_traces_field, templates_brand_strings_registry_columns [INFERRED 0.95]
- **The five Web surface fields as design-time twins of the live-page checks** — changelog_web_surface_block, changelog_web_surface_route, changelog_web_surface_answers, changelog_web_surface_indexable, changelog_web_surface_without_js, changelog_web_surface_entity, changelog_seo_aeo_audit_companion [EXTRACTED 1.00]
- **B-007 closed across board, brief, plan, changelog and the project's own dogfooded chain** — docs_superpowers_backlog_b_007, docs_superpowers_briefs_2026_08_10_web_surface_and_routing_r_01, docs_superpowers_plans_2026_08_10_web_surface_and_routing_t2, changelog_web_surface_block, docs_ux_screens_web_surfaces, changelog_v0_33_0 [EXTRACTED 1.00]
- **The gate suite — each gate run alone and read by its own exit code** — github_workflows_validate_repo_consistency, github_workflows_validate_brand_lint_tests, github_workflows_validate_ux_lint_tests, github_workflows_validate_plugin_strict, readme_ux_lint, readme_brand_lint [INFERRED 0.85]
- **The UX chain — vision → foundation → flows → screens → scenarios → audits → plans** — plugins_super_ux_skills_references_scenario_format_vision_md, plugins_super_ux_skills_references_scenario_format_foundation_md, plugins_super_ux_skills_references_scenario_format_flows_md, plugins_super_ux_skills_references_scenario_format_screens_md, plugins_super_ux_skills_references_scenario_format_scenarios_md, plugins_super_ux_skills_references_scenario_format_audit_report, plugins_super_ux_skills_references_scenario_format_ux_plan [EXTRACTED 1.00]
- **The five required fields of a Web surface: block** — plugins_super_ux_skills_references_scenario_format_route_field, plugins_super_ux_skills_references_scenario_format_answers_field, plugins_super_ux_skills_references_scenario_format_indexable_field, plugins_super_ux_skills_references_scenario_format_without_js_field, plugins_super_ux_skills_references_scenario_format_entity_field [EXTRACTED 1.00]
- **The docs/brand/ pack — the six files brand-contract v1 governs** — plugins_super_ux_skills_references_brand_contract_voice_md, plugins_super_ux_skills_references_brand_contract_terminology_md, plugins_super_ux_skills_references_brand_contract_facts_md, plugins_super_ux_skills_references_brand_contract_channels_md, plugins_super_ux_skills_references_brand_contract_strings_md, plugins_super_ux_skills_references_brand_contract_locales_md [EXTRACTED 1.00]

## Communities (76 total, 24 thin omitted)

### Community 0 - "Slash Commands and the Routing Table"
Cohesion: 0.05
Nodes (84): /ux-flows command, Never seed an empty vision.md, /ux-init command, Routing row: "what do best practices say" → practices / heuristics audit, Routing row: "check everything works" / audit → ux-audit, Routing row: "the copy is inconsistent" / "tone of voice" → brand-voice, Routing row: "does the copy match the brand" → ux-audit copy scope, Routing row: "design it" / "how should it look" → flows, visual identity settled first (+76 more)

### Community 1 - "Scenario Format and Audit Contract"
Cohesion: 0.05
Nodes (74): Audit report format (docs/ux/audits), Audit verdicts PASS/PARTIAL/FAIL/BLOCKED, Cursor rules (.mdc) variant, CLAUDE.md scenario-first hard rule snippet, scenarios.md format contract, Scenario-first methodology, SCN-NNN id and status lifecycle rules, Target-project docs/ux contract (+66 more)

### Community 2 - "Brand Linter (project copy)"
Cohesion: 0.10
Nodes (55): _alternatives(), apply_fixes(), check_ai_tells(), check_bot_safety(), check_channels(), check_consistency(), check_contract(), check_facts() (+47 more)

### Community 3 - "Brand Linter (plugin script)"
Cohesion: 0.10
Nodes (55): _alternatives(), apply_fixes(), check_ai_tells(), check_bot_safety(), check_channels(), check_consistency(), check_contract(), check_facts() (+47 more)

### Community 4 - "Practice Catalog and Selection"
Cohesion: 0.08
Nodes (56): Anti-cargo-cult rule, best-practices.md catalog (BP-001..206), BP-001 — traced-job discipline, BP-067 — freemium-led motion, BP-069 — first-session paywall placement, BP-070 — reverse trial, BP-129 — whole-chain web2app measurement, BP-138 — accessibility regime (EAA / ADA) (+48 more)

### Community 5 - "UX Foundation Layer"
Cohesion: 0.05
Nodes (51): Cascade Check to Downstream Layers, Figma On/Off Choice Asked Once Per Project, INVEST Stories with Given/When/Then Criteria, JTBD Four Forces Quality Bar, Frequency x Severity x Solvability Scoring, Product Mechanics Recorded Even When None, Reviews and Support Tickets Are Evidence Already Sitting There, ux-foundation Skill (+43 more)

### Community 6 - "Repo Validator (test/validate.py)"
Cohesion: 0.10
Nodes (49): changelog_version(), check(), check_description_canon(), _dedent_block(), front_matter(), load_json(), main(), _prose_files() (+41 more)

### Community 7 - "Best-Practice Catalog Clusters"
Cohesion: 0.06
Nodes (49): Behavioral practices cluster BP-001..078, BP-001 Adapt competitor tactics, don't copy them, Visual craft cluster BP-079..090 (typography, color, layout), Figma structure cluster BP-091..100, Components & controls cluster BP-101..115, Web funnels cluster BP-116..123 (landing, pricing, checkout, billing, cancel), Web-to-app funnel cluster BP-124..129, Motion cluster BP-130..132 (token scale, reduced motion, scroll-driven floors) (+41 more)

### Community 8 - "Installer Flows, Journeys and Stories"
Cohesion: 0.12
Nodes (44): R-08: The seeded project passes both linters from the first second, R-13: The installer speaks one language, offers routing from both doors, help matches writes, FLW-01: Interactive install, FLW-02: Piped / non-TTY install, FLW-03: Direct project install, FLW-04: Read before running, Task analysis — three entry shapes, two terminal states, JRN-01: First install journey (+36 more)

### Community 9 - "Retros and Composition Gates"
Cohesion: 0.06
Nodes (39): Retro 2026-08-05 — a repeat audit found what a green suite could not, Retro 2026-08-10 — a green suite that had never been asked a question about composition, Absence has one side — a comparison needs two, so absence must be asked for by name, check_changelog_headings — a version documented twice ships the previous release's notes, Shape checks versus composition checks, Standing instruction 3 — a new check runs against the seeded template first, validate_brand_lint_coverage — every emitted code needs a fixture and a contract row, validate_hard_rule_copies — driven by the HARD_RULES pair list (+31 more)

### Community 10 - "npm Package Manifest"
Cohesion: 0.06
Nodes (33): author, name, url, bin, super-ux, bugs, url, description (+25 more)

### Community 11 - "Brand Check Codes B001–B006"
Cohesion: 0.07
Nodes (32): R-20 validation on nicegram-business data, B001 (E) — a file under docs/brand/ has no contract marker, B002 (E) — markers disagree across the pack, B003 (W) — voice.md is draft while strings.md holds agreed rows, B004 (E) — Derived-from cites an id absent from foundation.md, B005 (W) — foundation.md changed after Last calibrated, B020 (E) — one action carries two different names, B021 (E) — a registered string diverged from the code (+24 more)

### Community 12 - "UX Linter (project copy)"
Cohesion: 0.16
Nodes (26): check_links(), check_unique_and_gaps(), check_vision(), check_web_surface(), entry_blocks(), err(), figma_enabled(), find_ux_dir() (+18 more)

### Community 13 - "UX Linter (plugin script)"
Cohesion: 0.16
Nodes (26): check_links(), check_unique_and_gaps(), check_vision(), check_web_surface(), entry_blocks(), err(), figma_enabled(), find_ux_dir() (+18 more)

### Community 14 - "Pipeline Records — Briefs, Plans, Acceptance"
Cohesion: 0.10
Nodes (23): Acceptance — tier-1 audit findings (v0.27.1), Brief — tier-1 findings from the 51-skill audit, Carry-over ledger (deferred work, never empty), Locked REQ list — add freely, remove only with the operator, A practice missing from practice-selection.md is unreachable, Brief — verbal identity layer (brand-voice + copywriting), I-2 — one release instead of three, risk compensated by R-20, Acceptance — carry-over ledger empty (+15 more)

### Community 15 - "Installer CLI (bin/super-ux.js)"
Cohesion: 0.18
Nodes (19): fail(), fs, installClaudePlugin(), installCursor(), installSkillsCli(), main(), makePrompter(), menu() (+11 more)

### Community 16 - "The v0.33.0 Copy Checks (B007, B026)"
Cohesion: 0.14
Nodes (19): B007 — a voice names one admired and one refused brand, B026 — a label, button, menu item or title takes no full stop, brand-contract v1, brand_lint.py — deterministic brand checks, menu.nothing full-stop fix, test/ux_lint_test.py — UX linter fixture harness, Release 0.33.0 — the second reader gets a field, String menu.nothing — "Nothing selected" (+11 more)

### Community 17 - "Vision Layer and the Open Board"
Cohesion: 0.13
Nodes (19): Four routing rows and the composite brief, Release 0.31.0 — the vision layer, vision skill and /vision, B-001 — no check that a target project's installed vision rule still matches the template, B-003 — the B022 literal extractor is a regex, not a tokenizer, B-005 — a seeded but unwritten vision.md lints clean, B-006 (closed) — the code graph was stale at 756 nodes, B-008 (closed) — the plain-word routing table was thinner than the capability behind it (+11 more)

### Community 18 - "Carry-Over Ledger and Code Graph"
Cohesion: 0.13
Nodes (19): Acceptance record - verbal layer v0.30.0 (25/25 REQ), C-02 decision - no Checked: backfill, C-03 code graph (698 nodes, 1353 edges, 38 communities), Carry-over ledger C-01..C-06, .graphifyignore, sync_references.py, validate_brand_contract, validate_brand_field_ownership (+11 more)

### Community 19 - "Channel Records and Field Limits"
Cohesion: 0.18
Nodes (16): BP-206 - the wording of the exit, C-04 upstream reconciliation, B040 (E) — a field exceeds its surface limit, B073 (E) — a field overflows under the locale's coefficient, docs/brand/channels.md — one record per surface (register, limits, bans), Channel Playbooks — the physics of each surface, Physics decays — every ranking behaviour carries a checked date, Platform physics per marketing surface (+8 more)

### Community 20 - "Style Pack and Surface Registers"
Cohesion: 0.15
Nodes (15): Style pack — one locked visual identity, Surface: destructive confirm, Surface: empty state, Surface: primary action, Register as a delta on the five axes, Dead idioms table, Length coefficient and its effective limits, Locale delta file (en, primary) (+7 more)

### Community 21 - "Release Discipline and the Web-Surface Declaration"
Cohesion: 0.15
Nodes (15): Web surfaces: yes|no — project-level declaration, Run each gate alone and read its own exit code, git push --atomic origin main vX.Y.Z, The edit → sync → validate loop, release_preflight.py, Test from a packed tarball, not the working tree, B023 — a location that no longer resolves, B-004 — screens.md coverage ranges are never re-resolved (+7 more)

### Community 22 - "ux-contract v4 and Glossary"
Cohesion: 0.19
Nodes (14): Bug report template — quote the file that says so, ux-contract v4, validate_stated_numbers gate, Glossary — chain, layer, trace, orphan, contract, style pack, register, Failure mode — insider shorthand and performed honesty, D1 — additive to v4, not a new contract version, D2 — a block inside screens.md, not a new docs/ux/web.md, The defect — the contract never mentions indexability (+6 more)

### Community 23 - "Reference Sync and the Composition Gates"
Cohesion: 0.18
Nodes (14): Transitive-closure reference sync (sync_references.py), Release 0.32.0 — composition gates, validate_seeded_scripts gate, validate_skill_parity gate, A skill exists in seven places or it does not exist, validate_seeded_scripts invariant, validate_skill_parity invariant, B-002 — validate_seeded_scripts does not prove the destination path is the one the reader is told to run (+6 more)

### Community 24 - "Hard Rules and Stated Numbers"
Cohesion: 0.15
Nodes (14): Brand voice hard rule (super-ux), Never stamp a Checked date you did not earn, validate_stated_numbers invariant, Surface: changelog, Surface: error, Surface: landing hero (the README), Proof that is not a number, Public: no — figures that exist and must never be quoted (+6 more)

### Community 25 - "Voice Axes and Verbal Practices"
Cohesion: 0.20
Nodes (14): Verbal identity cluster BP-182..206, B007 (W) — ## Voice references names no admired or no refused brand, The five fixed voice axes (Confidence, Register, Distance, Humor, Density), docs/brand/voice.md — pack, axes, narrative, invariants, locales, What travels and what does not (invariant vs reconsidered per locale), Keywords are researched per market, never translated, Locales — one voice, several languages, Parity declared rather than hidden (B071) (+6 more)

### Community 26 - "Fact Sourcing and Comparison Honesty"
Cohesion: 0.20
Nodes (14): B030 (E) — a figure in public copy has no row in facts.md, B031 (W) — a fact has no source, or is past its Review by, docs/brand/facts.md — canonical figures, the only source, Comparison-page honesty rule (concede something real), Four inputs before writing (action, reader, their words, proof), The grounding model (prerequisite vs introduced), Marketing copy — pages, posts and long form, Page structure (headline → final CTA) and page types (+6 more)

### Community 27 - "The Web Surface Block and Its Companion"
Cohesion: 0.19
Nodes (13): seo-aeo-audit as the third companion, Web surface field: Answers (the ONE question this page answers), Web surface: block (five-field screen record), Web surface field: Entity, Web surface field: Indexable, Web surface field: Route, Web surface field: Without JS, B-007 (closed) — a public web surface had no home in the chain (+5 more)

### Community 28 - "Web-Surface Requirements and the Journey Gap"
Cohesion: 0.15
Nodes (13): UX scenarios hard rule (super-ux), B-011 — a journey has no owner field, R-05 — ux-flows asks the web-surface question once, beside Figma and the style pack, R-06 — ux-audit checks a built public screen against its record, T4 — ux-flows/SKILL.md asks the web-surface question, T5 — ux-audit/SKILL.md verifies a built public screen and hands off, companion: task-pipeline, The design chain — vision → foundation → flows → screens → scenarios → build → audit (+5 more)

### Community 29 - "The Nine Vision Sections"
Cohesion: 0.18
Nodes (13): 6. Anti-vision, 2. Core idea, 1. Essence, 7. Horizon, 5. Principles, Do NOT trigger for bug fixes, refactors, tests, docs, Misaligned protocol — name, offer two paths, wait, Vision alignment — hard rule (super-ux) (+5 more)

### Community 30 - "Family Catalogue and the Copy Brief Gap"
Cohesion: 0.22
Nodes (11): The family catalogue moves with the release, B-012 — the copy brief has no success metric or constraint, D7 — no new field for facts on a marketing page, docs/brand/ — the brand layer, A plain skills copy shadows the plugin, skill: brand-voice, skill: copywriting, The ssheleg skill family (+3 more)

### Community 31 - "Contract Doctor (project copy)"
Cohesion: 0.38
Nodes (10): brand_contract_state(), diagnose(), find_ux_dir(), fix(), main(), marker(), Path, Only the changes that cannot be wrong. (+2 more)

### Community 32 - "Contract Doctor (plugin script)"
Cohesion: 0.38
Nodes (10): brand_contract_state(), diagnose(), find_ux_dir(), fix(), main(), marker(), Path, Only the changes that cannot be wrong. (+2 more)

### Community 33 - "The String Registry"
Cohesion: 0.27
Nodes (10): B020 — one action under two names, B021 — registry text disagrees with the source, Interpolated messages left unregistered, and why, Interface string registry (docs/brand/strings.md), The word prefix is the vocabulary (install:/skip:/keep:/seed:/sync:/warning:/error:), Accessibility regime — every TTY path reachable without one, colour never the only signal, Design tooling — Figma disabled, the whole surface is a terminal, Design system — no style pack, state vocabulary, selection glyphs (+2 more)

### Community 34 - "Brand Commands and Seeded Scripts"
Cohesion: 0.25
Nodes (9): /brand-init command, Never invent a fact to fill a table, plugin scripts/brand_lint.py, Contract drift (project vs contract version), plugin scripts/ux_doctor.py, /ux-doctor command, Brand voice hard rule (installed block), plugin scripts/ux_lint.py (+1 more)

### Community 35 - "Channel Playbooks and Completeness"
Cohesion: 0.25
Nodes (9): Per-Feature and Per-Product Completeness Checklists, Channel Record Fields (Register/Format/Limits/Forbidden/CTA/Proof/Locales), Channels Template (one record per surface), Forbidden Splits Platform Physics from Brand Choice, Marketing Surfaces (landing hero, X, Reddit, …), Product Surfaces (primary action, error, empty state, paywall, destructive confirm), Length Coefficient, Length Notes (constraint reaches the primary-locale original) (+1 more)

### Community 36 - "Terminology and Product Terms"
Cohesion: 0.29
Nodes (8): B010 (E) — a banned word appears in a registered string, B011 (E) — a generic word used where a product term exists, B012 (E) — an entity or tier name spelled inconsistently, docs/brand/terminology.md — our words, banned words, entity and tier names, Product surface registers (primary action → docs and help), Errors carry three facts (what happened, what survived, one next step), The four laws of UI copy, UI copy — the strings inside the product

### Community 37 - "The Six Voice Packs"
Cohesion: 0.46
Nodes (8): Pack: calm-expert, Pack: editorial-premium, Voice packs — the archetype library, Pack: operator-brief, The pack contract (nine fields every pack carries), Pack: peer-builder, Pack: plain-service, Pack: playful-consumer

### Community 38 - "Localization and Locale Deltas"
Cohesion: 0.25
Nodes (8): Address Form (decided once, not per string), Dead Idioms Table (replacement does the same job), Locale Header Fields (Locale/Primary/Address form/Coefficient/Humor/Never translated/Reviewed by), Keywords Researched in Market, Never Translated, Locale Delta Template (locales/<code>.md), B020 — One Action, Two Names, A Decision Registry, Not a Message Catalog, Entity and Tier Names — B012 (one spelling everywhere)

### Community 39 - "A Rule With One Source Text"
Cohesion: 0.29
Nodes (7): A rule nobody can verify is a suggestion, A hard rule has one source text in templates/, Vision alignment hard rule (super-ux), One owner per fact (convention), Forbidden carries both halves: physics and brand, Validator written first, red while files are missing, Task 1 — author brand-contract v1 (single definition of every field)

### Community 40 - "Virality and Referral Practices"
Cohesion: 0.52
Nodes (7): BP-147 growth loop named before freemium, BP-148 virality through the product artifact, BP-149 plan K near 0.2 and design cycle time, BP-150 reward in product units, on invitee milestone, BP-151 referral abuse designed against, not discovered, [Viral26] converged virality/referral benchmarks 2026, Virality and referral cluster (REQ-01)

### Community 41 - "Practice Index Generator"
Cohesion: 0.43
Nodes (6): main(), parse(), (id, title, tags, checked) for every entry, in catalog order. `checked` is ""…, Practices whose review date has aged past `months`, oldest first., render(), stale_report()

### Community 42 - "Brand Contract v1 and Its Commands"
Cohesion: 0.29
Nodes (7): Brand Commands (/brand, /brand-init, /brand-update, /brand-lint, /copy), brand-contract v1, docs/brand README (how this product speaks), B021 — Code No Longer Matches the Row, B022 — String in Code With No Registry Row, String Statuses (agreed/proposed/drifted/orphan), Interface Strings Registry Template

### Community 43 - "Shipping Instructions and the Third Companion"
Cohesion: 0.33
Nodes (6): Idea or improvement template — which layer does it belong to?, Every link in a skill is a shipping instruction, R-07 — seo-aeo-audit offered as the third companion, recommend-never-force, Original v0.1.0 implementation plan (historical), T6 — seo-aeo-audit becomes the third companion, system-map.md — the whole system on one page

### Community 44 - "Facts Template and Non-Numeric Proof"
Cohesion: 0.33
Nodes (6): B031 — missing Source or past Review by warns, Facts Template (the only source of any public figure), Proof That Is Not a Number (testimonials, awards, press), Public: no — figures that exist and must never be quoted, Required Disclaimers Table, Legal Differences Treated as Required Strings

### Community 45 - "Banned Words and the Glossary"
Cohesion: 0.33
Nodes (6): Fact Row Fields (Fact/Value/Source/Checked/Review by/Public), Banned List Seeded from ai-tells.md, Banned Words — B011, Glossary (grounded before it is leaned on), Product Terms — B010, Terminology Template (the dictionary the linter reads)

### Community 46 - "The Seeded Project Skeleton"
Cohesion: 0.40
Nodes (6): docs/brand/ as the sibling root, Seeded docs/ux/README.md, docs/ux/doctor.py — the contract doctor, docs/ux/lint.py — the integrity/drift linter, The four seeded rules (design before build, same change, no drift, lint it), Two files answer a "what" question

### Community 47 - "Brand Lint Fixtures"
Cohesion: 0.47
Nodes (5): case(), fix_idempotent(), main(), Write a temp pack and compare the codes returned. `files` land inside the brand…, `--fix` clears what it claims to, and the second run has nothing left. A fixer…

### Community 48 - "npm Release and Publish Jobs"
Cohesion: 0.40
Nodes (5): Post-release npx smoke test from a clean cwd, publish job — npm publish --provenance, Published is a claim until the registry serves it — poll loop, release job — tag → validator → GitHub release, Dual auth — NPM_TOKEN automation token and OIDC trusted publishing

### Community 49 - "UX Lint Fixtures (new in 0.33.0)"
Cohesion: 0.40
Nodes (4): case(), Compose a screens.md with an optional Web surfaces declaration., Run the linter over a temp tree and compare the messages it kept. Matching is…, screens()

### Community 50 - "Password and Auth Practices"
Cohesion: 0.67
Nodes (4): BP-153 password rules by 800-63B-4: length and breach check, BP-154 password field does not fight the password manager, BP-155 passwordless offered as an equal door, [NIST] SP 800-63B rev 4 Digital Identity Guidelines

### Community 51 - "Reference Closure Sync"
Cohesion: 0.67
Nodes (3): closure(), main(), Every contract reachable from `seed` by following links between contracts.

## Knowledge Gaps
- **182 isolated node(s):** `fs`, `path`, `readline`, `{ spawnSync }`, `ROOT` (+177 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `/ux-rule command` connect `Brand Commands and Seeded Scripts` to `Slash Commands and the Routing Table`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `/ux — single entry point for all UX work` connect `Slash Commands and the Routing Table` to `Voice Axes and Verbal Practices`, `Carry-Over Ledger and Code Graph`, `Brand Check Codes B001–B006`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **What connects `fs`, `path`, `readline` to the rest of the system?**
  _182 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Slash Commands and the Routing Table` be split into smaller, more focused modules?**
  _Cohesion score 0.05249569707401033 - nodes in this community are weakly interconnected._
- **Should `Scenario Format and Audit Contract` be split into smaller, more focused modules?**
  _Cohesion score 0.050351721584598295 - nodes in this community are weakly interconnected._
- **Should `Brand Linter (project copy)` be split into smaller, more focused modules?**
  _Cohesion score 0.09610389610389611 - nodes in this community are weakly interconnected._
- **Should `Brand Linter (plugin script)` be split into smaller, more focused modules?**
  _Cohesion score 0.09610389610389611 - nodes in this community are weakly interconnected._