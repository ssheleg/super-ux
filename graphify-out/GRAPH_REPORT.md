# Graph Report - .  (2026-08-10)

## Corpus Check
- 114 files · ~143,373 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1091 nodes · 2111 edges · 71 communities (50 shown, 21 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 147 edges (avg confidence: 0.85)
- Token cost: 627,765 total

## Build notes (2026-08-10)

Read these before quoting the numbers above.

- **Token split is unavailable, not zero.** No Gemini key is set on this machine,
  so semantic extraction ran through four host subagents. The harness reports one
  combined `subagent_tokens` figure per agent, not an input/output split. The
  `627,765` is that combined total; the generator's `output` field would be a
  fabricated zero, so the line above states the total instead.
- **140 of 2303 extracted edges (6.1%) dropped as dangling** and are absent from
  the 2111 edges built. Two causes, both structural: AST emits import edges to
  stdlib modules that are not nodes (`sys`, `re`, `pathlib`, `json`), and two
  files documenting the same artifact name it under their own path stem, so
  `CONTRIBUTING.md` describing `test/validate.py` yields `contributing_validate_py`
  while the AST node is `test_validate_*`. Nothing was silently repaired.
- **Three community pairs are exact twins** — `brand_lint.py`/`docs/brand/lint.py`,
  `ux_lint.py`/`docs/ux/lint.py`, `ux_doctor.py`/`docs/ux/doctor.py`. That is this
  project dogfooding itself: the plugin script and the copy it seeded into its own
  chain are two real files. The duplication is the design, not a graph defect.
- **A manifest is saved this time** (114 files stamped). The 2026-08-06 build
  saved none, which is why the following run's `detect_incremental` reported the
  entire corpus as new. `--update` is genuinely incremental from here.

## Community Hubs (Navigation)
- Slash Commands and Seeded Gates
- Scenario Format and Audit Contract
- UX Foundation Layer
- Brand Linter (project copy)
- Brand Linter (plugin script)
- Backlog, Retros and Composition Gates
- Best-Practice Catalog Clusters
- Repo Validator (test/validate.py)
- Installer Flows, Journeys and Stories
- Channel Records and Fact Sourcing
- npm Package Manifest
- Practice Catalog and Selection
- docs/ux Layout and ID Rules
- System Map and the Four Rules
- UX Linter (project copy)
- UX Linter (plugin script)
- Installer CLI (bin/super-ux.js)
- Vision Layer and Alignment Test
- Pipeline Records — Briefs, Plans, Acceptance
- UX and Voice Principles (PRN)
- Brand Contract v1 and Its Gates
- Audit Depth and Catalog Validation
- Voice Axes and Register Model
- Flow Design Rules and Modes
- Release Discipline and Reference Sync
- Skill Parity and Rule Installation
- UI Copy Laws and AI Tells
- Channel Playbooks and Platform Physics
- Screen and String Registries
- ux-audit Skill and Brand Rules
- Contract Doctor (project copy)
- Contract Doctor (plugin script)
- Localization and Store Listings
- The Build Gate and Hard Rules
- Composition Gates (v0.32.0)
- Voice File and Pack Validation
- brand-voice and copywriting Skills
- ux-contract v4 and Glossary
- Marketing Copy and Search Safety
- The Six Voice Packs
- Validator-First Discipline
- Carry-Over Ledger and Code Graph
- Virality and Referral Practices
- Practice Index Generator (bp_index.py)
- Register Delta and Locale Parity
- Brand Lint Fixtures
- npm Release and Publish Jobs
- Style Pack and Design Tooling
- Password and Auth Practices
- Reference Closure Sync
- Shell Installer
- Release Preflight
- Code of Conduct and Security Policy
- Family Catalogue and Plugin Shadowing
- Ledger Assumptions
- PR Evidence Checklist
- Changelog Release Notes
- Version Sync Gate
- Plugin Validate Strict
- Ladder Walk Extras
- Checked Dates From BP-182
- Known-Red Until Sync
- R-07 Command and Template Count
- R-10 Figure Detection
- /ux-lint Command
- Scenarios Before Interface
- No Telemetry Refusal
- Read-Only Audit Stance
- Heuristic Findings Pass
- Brand Same-Change Rule
- Foundation Derivation Marker

## God Nodes (most connected - your core abstractions)
1. `UX Best Practices Catalog BP-001..206` - 28 edges
2. `check()` - 24 edges
3. `Step 2 — Mandatory consideration sets` - 24 edges
4. `best-practices.md catalog (BP-001..206)` - 24 edges
5. `read()` - 22 edges
6. `main()` - 21 edges
7. `UX Design Principles — the reasoning playbook` - 21 edges
8. `docs/ux/foundation.md (the WHY layer)` - 21 edges
9. `/ux command (single entry point)` - 20 edges
10. `UX Contract v4` - 19 edges

## Surprising Connections (you probably didn't know these)
- `5. Principles` --semantically_similar_to--> `Anti-cargo-cult rule`  [INFERRED] [semantically similar]
  templates/vision.md → plugins/super-ux/skills/references/practice-selection.md
- `Do NOT trigger for bug fixes, refactors, tests, docs` --semantically_similar_to--> `Anti-cargo-cult rule`  [INFERRED] [semantically similar]
  templates/vision-rule.md → plugins/super-ux/skills/references/practice-selection.md
- `A rule nobody can verify is a suggestion` --semantically_similar_to--> `One owner per fact (convention)`  [INFERRED] [semantically similar]
  .github/ISSUE_TEMPLATE/feature_request.md → CONTRIBUTING.md
- `Every fact row names the command that recomputes it` --semantically_similar_to--> `validate_stated_numbers invariant`  [INFERRED] [semantically similar]
  docs/brand/facts.md → CONTRIBUTING.md
- `Forbidden carries both halves: physics and brand` --semantically_similar_to--> `One owner per fact (convention)`  [INFERRED] [semantically similar]
  docs/brand/channels.md → CONTRIBUTING.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **docs/brand/ file set forming brand-contract v1** — docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_voice_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_terminology_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_facts_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_channels_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_strings_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_locales_files [EXTRACTED 1.00]
- **Bounded humanize pass — guards that stop the rewrite** — plugins_super_ux_skills_references_ai_tells_severity_scale, plugins_super_ux_skills_references_ai_tells_density_threshold, plugins_super_ux_skills_references_ai_tells_change_rate_guard, plugins_super_ux_skills_references_ai_tells_semantic_preservation_check, plugins_super_ux_skills_references_ai_tells_naturalness_grade [EXTRACTED 1.00]
- **The docs/brand/ pack — one contract, seven artifacts, one linter** — plugins_super_ux_skills_references_brand_contract_voice_md, plugins_super_ux_skills_references_brand_contract_terminology_md, plugins_super_ux_skills_references_brand_contract_facts_md, plugins_super_ux_skills_references_brand_contract_channels_md, plugins_super_ux_skills_references_brand_contract_strings_md, plugins_super_ux_skills_references_brand_contract_locales_code_md, plugins_super_ux_skills_references_brand_contract_readme_sources_block, plugins_super_ux_skills_references_brand_contract_brand_lint_py [EXTRACTED 1.00]
- **The docs/brand Pack under brand-contract v1** — templates_brand_voice_voice_template, templates_brand_terminology_terminology_template, templates_brand_facts_facts_template, templates_brand_channels_channels_template, templates_brand_strings_strings_template, templates_brand_locale_locale_template, templates_brand_readme_brand_contract_v1 [EXTRACTED 1.00]
- **The ID Traceability Spine (ST/JTBD/JRN to FLW to SCR to SCN to string rows)** — templates_foundation_user_story_entry, templates_flows_flow_entry_fields, templates_screens_screen_entry_fields, templates_scenarios_traces_field, templates_brand_strings_registry_columns [INFERRED 0.95]
- **The brand pack under brand-contract v1** — docs_brand_voice_five_axes, docs_brand_terminology_product_terms, docs_brand_facts_single_source_of_figures, docs_brand_channels_register_delta, docs_brand_strings_decision_registry, docs_brand_locales_en_locale_delta, changelog_brand_contract_v1 [EXTRACTED 1.00]
- **The three composition gates added in 0.32.0** — contributing_validate_stated_numbers, contributing_validate_skill_parity, contributing_validate_seeded_scripts, changelog_composition_gates, contributing_edit_sync_validate_loop [EXTRACTED 1.00]
- **The design chain: vision → foundation → flows → screens → scenarios → build → audit** — readme_vision_skill, readme_ux_foundation_skill, readme_ux_flows_skill, readme_ux_scenarios_skill, readme_ux_audit_skill, changelog_screen_registry, readme_build_gate [EXTRACTED 1.00]
- **The super-ux traceability chain — vision → foundation → flows → screens → scenarios** — docs_ux_readme_pipeline, docs_ux_vision_essence, docs_ux_foundation_st_004, docs_ux_flows_flw_03, docs_ux_screens_scr_04, docs_ux_scenarios_scn_006 [EXTRACTED 1.00]
- **The composition gates added after the 2026-08-10 audit** — docs_superpowers_retro_2026_08_10_composition, docs_superpowers_retro_validate_stated_numbers, docs_superpowers_retro_validate_skill_parity, docs_superpowers_retro_validate_seeded_scripts, docs_superpowers_retro_validate_hard_rule_copies, docs_superpowers_retro_shape_vs_composition [EXTRACTED 1.00]
- **Degrade rather than block — the named degraded modes across the installer surface** — docs_ux_vision_principle_degrade_not_block, docs_ux_foundation_accessibility_regime, docs_ux_screens_scr_04, docs_ux_screens_scr_06, docs_ux_scenarios_scn_010, docs_ux_scenarios_scn_013 [INFERRED 0.85]
- **The super-ux chain: vision to foundation to flows to screens to scenarios to audits to plans** — plugins_super_ux_skills_vision_references_system_map_pipeline, plugins_super_ux_skills_vision_references_system_map_docs_ux_vision_md, plugins_super_ux_skills_vision_references_system_map_docs_ux_foundation_md, plugins_super_ux_skills_vision_references_system_map_docs_ux_flows_md, plugins_super_ux_skills_vision_references_system_map_docs_ux_screens_md, plugins_super_ux_skills_vision_references_system_map_docs_ux_scenarios_md, plugins_super_ux_skills_vision_references_system_map_docs_ux_audits_dir, plugins_super_ux_skills_vision_references_system_map_docs_ux_plans_dir [EXTRACTED 1.00]
- **Audit depth selects which of the five passes run** — plugins_super_ux_skills_ux_audit_skill_depth_levels, plugins_super_ux_skills_ux_audit_skill_scenario_pass, plugins_super_ux_skills_ux_audit_skill_flow_conformance_pass, plugins_super_ux_skills_ux_audit_skill_heuristic_pass, plugins_super_ux_skills_ux_audit_skill_practice_pass, plugins_super_ux_skills_ux_audit_skill_coverage_pass [EXTRACTED 1.00]
- **No interface code before the chain — enforced in four places** — plugins_super_ux_skills_ux_flows_skill_build_gate, plugins_super_ux_commands_ux_rule_ux_scenarios_hard_rule, plugins_super_ux_skills_vision_references_system_map_chain_first_rule, plugins_super_ux_commands_ux_init_ux_init [INFERRED 0.85]
- **The super-ux design chain — every layer traces to the one above** — plugins_super_ux_skills_references_scenario_format_vision_md, plugins_super_ux_skills_references_scenario_format_foundation_md, plugins_super_ux_skills_references_scenario_format_flows_md, plugins_super_ux_skills_references_scenario_format_screens_md, plugins_super_ux_skills_references_scenario_format_scenarios_md, plugins_super_ux_skills_references_scenario_format_audit_report, plugins_super_ux_skills_references_scenario_format_ux_plan [EXTRACTED 1.00]
- **Practice selection — profile, mandatory sets, artifact checklist, compliance record** — plugins_super_ux_skills_references_practice_selection_product_profile, plugins_super_ux_skills_references_practice_selection_mandatory_sets, plugins_super_ux_skills_references_practice_selection_per_artifact_checklists, plugins_super_ux_skills_references_practice_selection_compliance_table, plugins_super_ux_skills_references_practice_selection_anti_cargo_cult_rule [EXTRACTED 1.00]
- **What super-ux installs into a target project: two hard rules and two checkers** — templates_claude_rule_ux_scenarios_hard_rule, templates_claude_rule_brand_voice_hard_rule, templates_vision_rule_vision_alignment_hard_rule, templates_readme_lint_py, templates_readme_doctor_py [INFERRED 0.85]

## Communities (71 total, 21 thin omitted)

### Community 0 - "Slash Commands and Seeded Gates"
Cohesion: 0.06
Nodes (78): B020 — one action, two names, /brand-init command, Never invent a fact to fill a table, plugin scripts/brand_lint.py, Action menu (15 applicable actions), Contract drift (project vs contract version), plugin scripts/ux_doctor.py, /ux-doctor command (+70 more)

### Community 1 - "Scenario Format and Audit Contract"
Cohesion: 0.05
Nodes (73): Audit report format (docs/ux/audits), Audit verdicts PASS/PARTIAL/FAIL/BLOCKED, Cursor rules (.mdc) variant, CLAUDE.md scenario-first hard rule snippet, scenarios.md format contract, Scenario-first methodology, SCN-NNN id and status lifecycle rules, Target-project docs/ux contract (+65 more)

### Community 2 - "UX Foundation Layer"
Cohesion: 0.05
Nodes (57): Cascade Check to Downstream Layers, Figma On/Off Choice Asked Once Per Project, INVEST Stories with Given/When/Then Criteria, JTBD Four Forces Quality Bar, Frequency x Severity x Solvability Scoring, Product Mechanics Recorded Even When None, Reviews and Support Tickets Are Evidence Already Sitting There, ux-foundation Skill (+49 more)

### Community 3 - "Brand Linter (project copy)"
Cohesion: 0.10
Nodes (55): _alternatives(), apply_fixes(), check_ai_tells(), check_bot_safety(), check_channels(), check_consistency(), check_contract(), check_facts() (+47 more)

### Community 4 - "Brand Linter (plugin script)"
Cohesion: 0.10
Nodes (55): _alternatives(), apply_fixes(), check_ai_tells(), check_bot_safety(), check_channels(), check_consistency(), check_contract(), check_facts() (+47 more)

### Community 5 - "Backlog, Retros and Composition Gates"
Cohesion: 0.05
Nodes (52): B-001: Nothing checks the installed alignment rule in a target project, B-002: validate_seeded_scripts does not prove the destination path is the one the reader runs, B-003: The B022 literal extractor is a regex, not a tokenizer, B-004: screens.md coverage file:line ranges are never re-resolved, B-005: An unwritten seeded vision.md lints clean because the gate is self-declared status, B-006: graphify-out/graph.json is stale at 756 nodes from 2026-08-06, Derived priority — Frequency × Severity × Solvability, Retro 2026-08-05 — a repeat audit found what a green suite could not (+44 more)

### Community 6 - "Best-Practice Catalog Clusters"
Cohesion: 0.05
Nodes (51): Behavioral practices cluster BP-001..078, BP-001 Adapt competitor tactics, don't copy them, Visual craft cluster BP-079..090 (typography, color, layout), Figma structure cluster BP-091..100, Components & controls cluster BP-101..115, Web funnels cluster BP-116..123 (landing, pricing, checkout, billing, cancel), Web-to-app funnel cluster BP-124..129, Motion cluster BP-130..132 (token scale, reduced motion, scroll-driven floors) (+43 more)

### Community 7 - "Repo Validator (test/validate.py)"
Cohesion: 0.10
Nodes (49): changelog_version(), check(), check_description_canon(), _dedent_block(), front_matter(), load_json(), main(), _prose_files() (+41 more)

### Community 8 - "Installer Flows, Journeys and Stories"
Cohesion: 0.12
Nodes (44): R-08: The seeded project passes both linters from the first second, R-13: The installer speaks one language, offers routing from both doors, help matches writes, FLW-01: Interactive install, FLW-02: Piped / non-TTY install, FLW-03: Direct project install, FLW-04: Read before running, Task analysis — three entry shapes, two terminal states, JRN-01: First install journey (+36 more)

### Community 9 - "Channel Records and Fact Sourcing"
Cohesion: 0.06
Nodes (37): Scope and Limits (absence never means PASS), Channel Record Fields (Register/Format/Limits/Forbidden/CTA/Proof/Locales), Channels Template (one record per surface), Forbidden Splits Platform Physics from Brand Choice, Marketing Surfaces (landing hero, X, Reddit, …), Product Surfaces (primary action, error, empty state, paywall, destructive confirm), Surface Names Are Contract Keys (delete, never rename), B030 — public number with no facts row blocks (+29 more)

### Community 10 - "npm Package Manifest"
Cohesion: 0.06
Nodes (33): author, name, url, bin, super-ux, bugs, url, description (+25 more)

### Community 11 - "Practice Catalog and Selection"
Cohesion: 0.14
Nodes (33): Anti-cargo-cult rule, best-practices.md catalog (BP-001..206), BP-001 — traced-job discipline, BP-067 — freemium-led motion, BP-069 — first-session paywall placement, BP-070 — reverse trial, BP-129 — whole-chain web2app measurement, BP-138 — accessibility regime (EAA / ADA) (+25 more)

### Community 12 - "docs/ux Layout and ID Rules"
Cohesion: 0.17
Nodes (33): Audit report format (docs/ux/audits/YYYY-MM-DD.md), Scenario verdicts (PASS / PARTIAL / FAIL / BLOCKED), Coverage audit (scope: coverage), Customer journeys (JRN-NN), docs/ux/ file layout, docs/ux/flows.md (FLW-NN, the HOW layer), docs/ux/foundation.md (the WHY layer), ID rules (sequential, never reused) (+25 more)

### Community 13 - "System Map and the Four Rules"
Cohesion: 0.14
Nodes (22): task-pipeline handoff (recommended, not forced), super-ux System Map, The brand shelf, The chain shelf, Companion — task-pipeline, docs/brand/ — the verbal identity root (brand-contract v1), Entering mid-project, The four rules that keep agents in sync (+14 more)

### Community 14 - "UX Linter (project copy)"
Cohesion: 0.20
Nodes (20): check_links(), check_unique_and_gaps(), check_vision(), err(), figma_enabled(), find_ux_dir(), ids(), index_ids() (+12 more)

### Community 15 - "UX Linter (plugin script)"
Cohesion: 0.20
Nodes (20): check_links(), check_unique_and_gaps(), check_vision(), err(), figma_enabled(), find_ux_dir(), ids(), index_ids() (+12 more)

### Community 16 - "Installer CLI (bin/super-ux.js)"
Cohesion: 0.18
Nodes (19): fail(), fs, installClaudePlugin(), installCursor(), installSkillsCli(), main(), makePrompter(), menu() (+11 more)

### Community 17 - "Vision Layer and Alignment Test"
Cohesion: 0.17
Nodes (18): Two layers answer a "what" question, docs/ux/vision.md contract — nine sections, vision skill, Vision vs scenarios — the one mistake the map exists to prevent, Two files answer a "what" question, 6. Anti-vision, 2. Core idea, 1. Essence (+10 more)

### Community 18 - "Pipeline Records — Briefs, Plans, Acceptance"
Cohesion: 0.14
Nodes (16): Acceptance — tier-1 audit findings (v0.27.1), Brief — tier-1 findings from the 51-skill audit, Carry-over ledger (deferred work, never empty), Locked REQ list — add freely, remove only with the operator, Brief — verbal identity layer (brand-voice + copywriting), I-2 — one release instead of three, risk compensated by R-20, Acceptance — carry-over ledger empty, Brief — closing the carry-over ledger (v0.28.0) (+8 more)

### Community 19 - "UX and Voice Principles (PRN)"
Cohesion: 0.17
Nodes (16): Verbal identity practices (BP-182..206), Step 3 — Per-artifact checklists, The coercive twin (honesty stance), Cognitive principles (PRN-11..PRN-16), Nielsen heuristics checklist (PRN-01..PRN-10), PRN-01 — Visibility of system status, PRN-08 — Minimalist design, PRN-12 — Smart defaults (+8 more)

### Community 20 - "Brand Contract v1 and Its Gates"
Cohesion: 0.28
Nodes (15): Acceptance record - verbal layer v0.30.0 (25/25 REQ), R-20 validation on nicegram-business data, validate_brand_contract, validate_brand_field_ownership, Brand Contract v1, brand_lint.py (docs/brand/lint.py), B001..B073 check-code table (33 codes), Contract marker line (+7 more)

### Community 21 - "Audit Depth and Catalog Validation"
Cohesion: 0.16
Nodes (14): Audit depth levels quick/standard/deep, best-practices.md catalog (BP-NNN), best-practices-index.md generated tag index, Practice Selection Protocol, validate_catalog(), Never stamp a Checked date you did not earn, Proof that is not a number, A practice missing from practice-selection.md is unreachable (+6 more)

### Community 22 - "Voice Axes and Register Model"
Cohesion: 0.18
Nodes (13): brand-contract v1, brand_lint.py — 33 deterministic checks, validate_brand_lint_coverage, Surface: empty state, Surface: primary action, Register as a delta on the five axes, Dead idioms table, Length coefficient and its effective limits (+5 more)

### Community 23 - "Flow Design Rules and Modes"
Cohesion: 0.21
Nodes (13): Trend governance & perceived quality (BP-145..146, BP-165..172), Flow rules (node naming, entry points, error edges), Finding severity (critical / major / minor), Rule 1 — Chain-first, Anti-patterns (stop signals), Backwards mode (existing product), Flow design rules, Forward mode (new product or feature) (+5 more)

### Community 24 - "Release Discipline and Reference Sync"
Cohesion: 0.18
Nodes (12): Idea or improvement template — which layer does it belong to?, validate workflow job (push + PR gate), 0.27.0 tagged from a stale base, sync_references.py — transitive closure of skill links, Run each gate alone and read its own exit code, Every link in a skill is a shipping instruction, git push --atomic origin main vX.Y.Z, Why the contracts are duplicated per skill (+4 more)

### Community 25 - "Skill Parity and Rule Installation"
Cohesion: 0.20
Nodes (12): A rule must be installed where the running agent reads, vision skill and /vision, A skill exists in seven places or it does not exist, Vision alignment hard rule (super-ux), Stable IDs, never reused, validate_skill_parity invariant, Backwards mode — artifacts filled in from existing code, The design chain (vision → foundation → flows → screens → scenarios) (+4 more)

### Community 26 - "UI Copy Laws and AI Tells"
Cohesion: 0.20
Nodes (12): ai-tells.md (marker vocabulary), B061 — humor banned on error, destructive confirm, billing, paywall, locales/<code>.md — per-locale delta, Brand Contract v1 (reference), README.md `Sources:` block — the paths that get scanned, docs/brand/terminology.md, brand-contract v1 — the docs/brand/ contract, Four inputs before writing (action, reader, their words, proof) (+4 more)

### Community 27 - "Channel Playbooks and Platform Physics"
Cohesion: 0.26
Nodes (12): docs/brand/channels.md, Channel surface list (product and marketing), Channel Playbooks — the physics of each surface, Physics decays — every ranking behaviour carries a checked date, Platform physics per marketing surface, Length coefficient (multiplies every field limit per locale), Store field limits and the two structural differences, Marketing surface registers (landing hero → lifecycle email) (+4 more)

### Community 28 - "Screen and String Registries"
Cohesion: 0.20
Nodes (11): Figma integration surface, One owner per fact, UI Screen Registry (screens.md), Style pack — one locked visual identity, Surface: destructive confirm, strings.md as a decision registry, What is deliberately not registered, The word prefix is the vocabulary (+3 more)

### Community 29 - "ux-audit Skill and Brand Rules"
Cohesion: 0.20
Nodes (11): ux-audit skill, UX plan (docs/ux/plans/), Brand voice hard rule (super-ux), Surface: error, Public: no — figures that exist and must never be quoted, facts.md — the only source of any public figure, Brand same-change hard rule, One action, one name (B020) (+3 more)

### Community 30 - "Contract Doctor (project copy)"
Cohesion: 0.38
Nodes (10): brand_contract_state(), diagnose(), find_ux_dir(), fix(), main(), marker(), Path, Only the changes that cannot be wrong. (+2 more)

### Community 31 - "Contract Doctor (plugin script)"
Cohesion: 0.38
Nodes (10): brand_contract_state(), diagnose(), find_ux_dir(), fix(), main(), marker(), Path, Only the changes that cannot be wrong. (+2 more)

### Community 32 - "Localization and Store Listings"
Cohesion: 0.24
Nodes (11): Verbal identity cluster BP-182..206, What travels and what does not (invariant vs reconsidered per locale), Keywords are researched per market, never translated, Locales — one voice, several languages, Parity declared rather than hidden (B071), Translate the job the string does, not the words (B072), The grounding model (prerequisite vs introduced), Optimization — structure that makes content extractable (+3 more)

### Community 33 - "The Build Gate and Hard Rules"
Cohesion: 0.22
Nodes (9): Bug report template — quote the file that says so, Explicit build gate before interface code, UX scenarios hard rule (super-ux), Test from a packed tarball, not the working tree, Narrative: hero, enemy, product role, promise, Do not write interface code until the chain is approved, The hard rule installed into CLAUDE.md, docs/ux/doctor.py + /ux-doctor (+1 more)

### Community 34 - "Composition Gates (v0.32.0)"
Cohesion: 0.25
Nodes (9): brand_lint_test.py CI step (fixture per check code), Composition gates (0.32.0), validate_seeded_scripts, validate_skill_parity, validate_stated_numbers, validate_seeded_scripts invariant, validate_stated_numbers invariant, Every fact row names the command that recomputes it (+1 more)

### Community 35 - "Voice File and Pack Validation"
Cohesion: 0.31
Nodes (9): validate_voice_packs, The five fixed voice axes, Locale parity threshold, docs/brand/voice.md, voice-packs.md (pack library), Voice failure mode, Narrative block (Hero, Enemy, Product role, Promise), Reconsidered per locale (+1 more)

### Community 36 - "brand-voice and copywriting Skills"
Cohesion: 0.32
Nodes (8): brand-voice skill, copywriting skill, Six shipped voice packs with declared degeneration, Locale parity computed against strings.md, Voice pack: peer-builder, The brand layer — docs/brand/, skill brand-voice (README), skill copywriting (README)

### Community 37 - "ux-contract v4 and Glossary"
Cohesion: 0.29
Nodes (8): ux-contract v4, ux_doctor.py contract doctor, ux_lint.py deterministic linter, Surface: changelog, Surface: landing hero (the README), Sources: block — what the linter is allowed to read, Glossary — chain, layer, trace, orphan, contract, style pack, register, Failure mode: insider shorthand and performed honesty

### Community 38 - "Marketing Copy and Search Safety"
Cohesion: 0.32
Nodes (8): Comparison-page honesty rule (concede something real), Marketing copy — pages, posts and long form, Page structure (headline → final CTA) and page types, The seven sweeps (clarity → zero risk), Search and answer engines — safety first, The absolute rule — no fabricated facts, quotes, statistics or experts, Technical floor (robots.txt, no-JS rendering, semantic HTML, schema), The safety veto list (blocked crawlers, clickbait mismatch, no byline)

### Community 39 - "The Six Voice Packs"
Cohesion: 0.46
Nodes (8): Pack: calm-expert, Pack: editorial-premium, Voice packs — the archetype library, Pack: operator-brief, The pack contract (nine fields every pack carries), Pack: peer-builder, Pack: plain-service, Pack: playful-consumer

### Community 40 - "Validator-First Discipline"
Cohesion: 0.29
Nodes (7): A rule nobody can verify is a suggestion, A hard rule has one source text in templates/, One owner per fact (convention), Forbidden carries both halves: physics and brand, Validator written first, red while files are missing, Tasks 13–17 — brand_lint.py check families B001..B073, Task 1 — author brand-contract v1 (single definition of every field)

### Community 41 - "Carry-Over Ledger and Code Graph"
Cohesion: 0.29
Nodes (7): BP-206 - the wording of the exit, C-02 decision - no Checked: backfill, C-03 code graph (698 nodes, 1353 edges, 38 communities), C-04 upstream reconciliation, Carry-over ledger C-01..C-06, .graphifyignore, sync_references.py

### Community 42 - "Virality and Referral Practices"
Cohesion: 0.52
Nodes (7): BP-147 growth loop named before freemium, BP-148 virality through the product artifact, BP-149 plan K near 0.2 and design cycle time, BP-150 reward in product units, on invitee milestone, BP-151 referral abuse designed against, not discovered, [Viral26] converged virality/referral benchmarks 2026, Virality and referral cluster (REQ-01)

### Community 43 - "Practice Index Generator (bp_index.py)"
Cohesion: 0.43
Nodes (6): main(), parse(), (id, title, tags, checked) for every entry, in catalog order. `checked` is ""…, Practices whose review date has aged past `months`, oldest first., render(), stale_report()

### Community 44 - "Register Delta and Locale Parity"
Cohesion: 0.33
Nodes (6): Register as a Delta Against the Five Axes, B071 — Locale Parity Below Threshold Warns, The Five Fixed Axes (Confidence/Register/Distance/Humor/Density), Locale Parity Threshold, Voice Pack as Starting Position, Voice Template (the identity file)

### Community 45 - "Brand Lint Fixtures"
Cohesion: 0.47
Nodes (5): case(), fix_idempotent(), main(), Write a temp pack and compare the codes returned. `files` land inside the brand…, `--fix` clears what it claims to, and the second run has nothing left. A fixer…

### Community 46 - "npm Release and Publish Jobs"
Cohesion: 0.40
Nodes (5): Post-release npx smoke test from a clean cwd, publish job — npm publish --provenance, Published is a claim until the registry serves it — poll loop, release job — tag → validator → GitHub release, Dual auth — NPM_TOKEN automation token and OIDC trusted publishing

### Community 47 - "Style Pack and Design Tooling"
Cohesion: 0.70
Nodes (5): Style pack vs practices precedence, screens.md → Design system block, Design tooling section (Figma on/off + file URL), Companion — sheleg-design, Visual identity is ONE locked style pack

### Community 48 - "Password and Auth Practices"
Cohesion: 0.67
Nodes (4): BP-153 password rules by 800-63B-4: length and breach check, BP-154 password field does not fight the password manager, BP-155 passwordless offered as an equal door, [NIST] SP 800-63B rev 4 Digital Identity Guidelines

### Community 49 - "Reference Closure Sync"
Cohesion: 0.67
Nodes (3): closure(), main(), Every contract reachable from `seed` by following links between contracts.

## Knowledge Gaps
- **142 isolated node(s):** `fs`, `path`, `readline`, `{ spawnSync }`, `ROOT` (+137 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Brand Contract v1` connect `Brand Contract v1 and Its Gates` to `Voice File and Pack Validation`, `UI Copy Laws and AI Tells`, `Channel Playbooks and Platform Physics`, `ux-contract v4 and Glossary`?**
  _High betweenness centrality (0.209) - this node is a cross-community bridge._
- **Why does `ux-contract v4` connect `ux-contract v4 and Glossary` to `Brand Contract v1 and Its Gates`?**
  _High betweenness centrality (0.202) - this node is a cross-community bridge._
- **Why does `Glossary — chain, layer, trace, orphan, contract, style pack, register` connect `ux-contract v4 and Glossary` to `Skill Parity and Rule Installation`, `Audit Depth and Catalog Validation`?**
  _High betweenness centrality (0.145) - this node is a cross-community bridge._
- **What connects `fs`, `path`, `readline` to the rest of the system?**
  _142 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Slash Commands and Seeded Gates` be split into smaller, more focused modules?**
  _Cohesion score 0.057942057942057944 - nodes in this community are weakly interconnected._
- **Should `Scenario Format and Audit Contract` be split into smaller, more focused modules?**
  _Cohesion score 0.05060882800608828 - nodes in this community are weakly interconnected._
- **Should `UX Foundation Layer` be split into smaller, more focused modules?**
  _Cohesion score 0.05200501253132832 - nodes in this community are weakly interconnected._