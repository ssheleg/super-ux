# Graph Report - /Users/sshlg/DATA/super-ux  (2026-08-06)

## Corpus Check
- 90 files · ~115,840 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 756 nodes · 1474 edges · 55 communities (49 shown, 6 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34
- Community 35
- Community 36
- Community 37
- Community 38
- Community 39
- Community 40
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 46
- Community 47
- Community 48
- Community 49
- Community 50
- Community 51
- Community 52
- Community 53
- Community 54

## God Nodes (most connected - your core abstractions)
1. `UX Best Practices Catalog BP-001..206` - 30 edges
2. `Step 2 — Mandatory consideration sets from the profile` - 28 edges
3. `UX Design Principles — How the Agent Thinks` - 24 edges
4. `Brand Contract v1` - 22 edges
5. `check()` - 21 edges
6. `brand_lint.py (docs/brand/lint.py)` - 20 edges
7. `read()` - 19 edges
8. `Acceptance record - verbal layer v0.30.0 (25/25 REQ)` - 19 edges
9. `ux-audit — Scenario Audit Loop (skill)` - 19 edges
10. `main()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `voice-packs.md (pack library)` --semantically_similar_to--> `Audit report verdict - REFINE / REDESIGN / NEW`  [INFERRED] [semantically similar]
  plugins/super-ux/skills/references/brand-contract.md → CHANGELOG.md
- ``Checked:` catalog field` --semantically_similar_to--> `docs/brand/facts.md`  [INFERRED] [semantically similar]
  CHANGELOG.md → plugins/super-ux/skills/references/brand-contract.md
- `Inventory sweep into strings.md` --semantically_similar_to--> `ux-scenarios skill (v0.1 design)`  [INFERRED] [semantically similar]
  plugins/super-ux/skills/brand-voice/SKILL.md → docs/superpowers/specs/2026-07-19-super-ux-design.md
- `Scope and limits section in the audit report` --semantically_similar_to--> `/brand-lint command`  [INFERRED] [semantically similar]
  docs/superpowers/specs/2026-08-04-tier1-audit-findings-design.md → plugins/super-ux/commands/brand-lint.md
- `A rule nobody can verify is a suggestion` --semantically_similar_to--> `One owner per fact — two definitions is drift with a delay fuse`  [INFERRED] [semantically similar]
  .github/ISSUE_TEMPLATE/feature_request.md → CONTRIBUTING.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The release gate chain — preflight, atomic push, version sync, publish, downstream verification** — contributing_release_preflight_py, contributing_atomic_push, contributing_release_checklist, _github_workflows_release_version_sync_gate, _github_workflows_release_publish_job, _github_workflows_release_registry_poll, contributing_family_pin [INFERRED 0.85]
- **The traceable UX chain: foundation → flows → screens → scenarios → audit** — readme_ux_foundation, readme_ux_flows, readme_ux_scenarios, readme_ux_audit, readme_ux_chain, readme_hard_rule, readme_ux_lint [EXTRACTED 1.00]
- **The verbal identity layer — contract, two skills, linter, catalog cluster** — readme_brand_layer, readme_brand_voice, readme_copywriting, readme_brand_lint, docs_superpowers_plans_2026_08_05_brand_voice_layer_task1_brand_contract, docs_superpowers_plans_2026_08_05_brand_voice_layer_task13_brand_lint [EXTRACTED 1.00]
- **Gates that replaced a warning written in prose** — docs_superpowers_retro_release_preflight_py, docs_superpowers_retro_check_pins_py, docs_superpowers_retro_check_changelog_headings, changelog_validate_brand_lint_coverage, changelog_validate_catalog, docs_superpowers_briefs_2026_08_05_brand_voice_layer_acceptance_validate_brand_field_ownership [INFERRED 0.75]
- **docs/brand/ file set forming brand-contract v1** — docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_voice_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_terminology_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_facts_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_channels_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_strings_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_locales_files [EXTRACTED 1.00]
- **WHY -> HOW -> WHAT initialization chain** — plugins_super_ux_commands_ux_init_command, plugins_super_ux_commands_ux_foundation_command, plugins_super_ux_commands_ux_flows_command, docs_superpowers_specs_2026_07_19_super_ux_design_scenario_base_contract [EXTRACTED 1.00]
- **Bounded humanize pass — guards that stop the rewrite** — plugins_super_ux_skills_references_ai_tells_severity_scale, plugins_super_ux_skills_references_ai_tells_density_threshold, plugins_super_ux_skills_references_ai_tells_change_rate_guard, plugins_super_ux_skills_references_ai_tells_semantic_preservation_check, plugins_super_ux_skills_references_ai_tells_naturalness_grade [EXTRACTED 1.00]
- **The docs/brand/ pack — one contract, seven artifacts, one linter** — plugins_super_ux_skills_references_brand_contract_voice_md, plugins_super_ux_skills_references_brand_contract_terminology_md, plugins_super_ux_skills_references_brand_contract_facts_md, plugins_super_ux_skills_references_brand_contract_channels_md, plugins_super_ux_skills_references_brand_contract_strings_md, plugins_super_ux_skills_references_brand_contract_locales_code_md, plugins_super_ux_skills_references_brand_contract_readme_sources_block, plugins_super_ux_skills_references_brand_contract_brand_lint_py [EXTRACTED 1.00]
- **Practice routing: profile → mandatory sets → checklists → compliance table → audit** — plugins_super_ux_skills_references_practice_selection_product_profile, plugins_super_ux_skills_references_practice_selection_mandatory_sets, plugins_super_ux_skills_references_practice_selection_per_artifact_checklists, plugins_super_ux_skills_references_practice_selection_compliance_table, plugins_super_ux_skills_references_best_practices_md, plugins_super_ux_skills_references_best_practices_index_by_tag, plugins_super_ux_skills_ux_audit_skill_practice_pass [EXTRACTED 1.00]
- **The UX design chain (foundation → flows → screens → scenarios → audits → plans)** — plugins_super_ux_skills_references_scenario_format_foundation_md, plugins_super_ux_skills_references_scenario_format_flows_md, plugins_super_ux_skills_references_scenario_format_screens_md, plugins_super_ux_skills_references_scenario_format_scenarios_md, plugins_super_ux_skills_references_scenario_format_audit_report, plugins_super_ux_skills_references_scenario_format_ux_plan, plugins_super_ux_skills_references_scenario_format_same_change_rule [EXTRACTED 1.00]
- **The UX chain — each layer traces to the one above** — plugins_super_ux_skills_references_system_map_foundation_md, plugins_super_ux_skills_references_system_map_flows_md, plugins_super_ux_skills_references_system_map_screens_md, plugins_super_ux_skills_references_system_map_scenarios_md, plugins_super_ux_skills_references_system_map_pipeline [EXTRACTED 1.00]
- **The docs/ux Artifact Chain (foundation to flows to screens to scenarios to audits)** — templates_foundation_foundation_template, templates_flows_flows_template, templates_screens_screens_template, templates_scenarios_scenarios_template, templates_audit_report_audit_report_template, templates_readme_ux_pipeline [EXTRACTED 1.00]
- **The docs/brand Pack under brand-contract v1** — templates_brand_voice_voice_template, templates_brand_terminology_terminology_template, templates_brand_facts_facts_template, templates_brand_channels_channels_template, templates_brand_strings_strings_template, templates_brand_locale_locale_template, templates_brand_readme_brand_contract_v1 [EXTRACTED 1.00]
- **The ID Traceability Spine (ST/JTBD/JRN to FLW to SCR to SCN to string rows)** — templates_foundation_user_story_entry, templates_flows_flow_entry_fields, templates_screens_screen_entry_fields, templates_scenarios_traces_field, templates_brand_strings_registry_columns [INFERRED 0.95]

## Communities (55 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (60): Finding, _alternatives(), apply_fixes(), check_ai_tells(), check_bot_safety(), check_channels(), check_consistency(), check_contract() (+52 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (44): Scope and Limits (absence never means PASS), Channel Record Fields (Register/Format/Limits/Forbidden/CTA/Proof/Locales), Channels Template (one record per surface), Forbidden Splits Platform Physics from Brand Choice, Marketing Surfaces (landing hero, X, Reddit, …), Product Surfaces (primary action, error, empty state, paywall, destructive confirm), Surface Names Are Contract Keys (delete, never rename), B030 — public number with no facts row blocks (+36 more)

### Community 2 - "Community 2"
Cohesion: 0.13
Nodes (39): changelog_version(), check(), check_description_canon(), front_matter(), load_json(), main(), Path, Everything the installer CLI copies must be inside the npm tarball. `npm… (+31 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (33): author, name, url, bin, super-ux, bugs, url, description (+25 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (34): Channel Playbooks — the physics of each surface, Physics decays — every ranking behaviour carries a checked date, Platform physics per marketing surface, What travels and what does not (invariant vs reconsidered per locale), Keywords are researched per market, never translated, Length coefficient (multiplies every field limit per locale), Locales — one voice, several languages, Parity declared rather than hidden (B071) (+26 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (32): Behavioral practices cluster BP-001..078, BP-001 Adapt competitor tactics, don't copy them, Components & controls cluster BP-101..115, Web funnels cluster BP-116..123 (landing, pricing, checkout, billing, cancel), Web-to-app funnel cluster BP-124..129, Frustration telemetry cluster BP-139..140, Engagement mechanics cluster BP-141..142 (gamification), Personalization & progressive profiling cluster BP-143..144 (+24 more)

### Community 6 - "Community 6"
Cohesion: 0.18
Nodes (19): fail(), fs, installClaudePlugin(), installCursor(), installSkillsCli(), main(), makePrompter(), menu() (+11 more)

### Community 7 - "Community 7"
Cohesion: 0.18
Nodes (19): CLAUDE.md scenario-first hard rule snippet, ux-scenarios skill (v0.1 design), Brand voice hard rule in CLAUDE.md, UX action menu (11 actions), /ux-audit command, /ux entry point, /ux-doctor command, Contract drift versus internal consistency (+11 more)

### Community 8 - "Community 8"
Cohesion: 0.20
Nodes (18): check_links(), check_unique_and_gaps(), err(), figma_enabled(), find_ux_dir(), ids(), index_ids(), main() (+10 more)

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (18): Audit report 'Scope and limits' section (required), PRN-17..21 - motivation principles, PRN-22..24, Acceptance record - verbal layer v0.30.0 (25/25 REQ), R-20 validation on nicegram-business data, validate_brand_contract, validate_brand_field_ownership, validate_voice_packs (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.21
Nodes (18): Verbal identity cluster BP-182..206, Every interactive component ships all its states, Comparison-page honesty rule (concede something real), Design anti-patterns (stop signals), Forward mode vs backwards mode (inferred tagging), Heuristic evaluation procedure for improving existing UX, UX Design Principles — How the Agent Thinks, Heuristics checklist PRN-01..PRN-10 (after Nielsen) (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.18
Nodes (17): Figma structure cluster BP-091..100, The Figma design loop inside ux-flows Design, Figma Integration (optional design surface), Figma preflight (MCP present, load Figma's own skill, file, library, style pack), Figma sync rule and boundaries (a rendering, never a replacement), Which Figma MCP tool for which job, Frame naming SCR-NN/<Screen>/<state> — the backbone, What the agent checks (frame parity, orphans, token references) (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.17
Nodes (17): docs/brand/channels.md, The five fixed voice axes, B061 — humor banned on error, destructive confirm, billing, paywall, Locale parity threshold, locales/<code>.md — per-locale delta, Brand Contract v1 (reference), README.md `Sources:` block — the paths that get scanned, Channel surface list (product and marketing) (+9 more)

### Community 13 - "Community 13"
Cohesion: 0.16
Nodes (16): BP-152 empty state states, teaches and gives a path, NN/g Designing Empty States in Complex Applications, channels.md — one record per surface, PRN-22 one voice, many registers, Register deltas never cross invariants, Topology B — two skills split by verb, voice.md — axes, narrative, invariants, Brand routing table (user words to action) (+8 more)

### Community 14 - "Community 14"
Cohesion: 0.27
Nodes (16): Audit report format (docs/ux/audits/YYYY-MM-DD.md), UX Contract v4 (scenario-format), scenarios.md — the WHAT layer (use-case scenarios), Scope and limits section (not optional), Traceability rules (orphans in either direction are findings), ux-contract v4 (field names, ID schemes, statuses, verdicts), UX plan format (target interface + CREATE/MODIFY/DELETE), The verdict fork — REFINE / REDESIGN / NEW (+8 more)

### Community 15 - "Community 15"
Cohesion: 0.19
Nodes (15): BP-157..164 - motion craft, BP-165..168 - perceived quality, BP-169..172 - generated-default tells, brand_lint fixture suite (32 fixtures, one per code), PER-NN vs P-NN persona id defect, validate_brand_lint_coverage, C-03 code graph (698 nodes, 1353 edges, 38 communities), .graphifyignore (+7 more)

### Community 16 - "Community 16"
Cohesion: 0.19
Nodes (15): BP-156 rejected form preserves work and names the way out, WCAG 2.2 SC 3.3.7 Redundant Entry, brand_lint.py, B020 — one action, two names, B030 — number in public copy absent from facts.md, B061 — no humor, exclamation or emoji on loss surfaces, Absolute prohibition on fabricated facts, facts.md — canonical sourced figures (+7 more)

### Community 17 - "Community 17"
Cohesion: 0.19
Nodes (14): Bug report template — quote the file that says so, brand_lint_test.py CI step (fixture per check code), Stable IDs, never reused (SCN/FLW/SCR/ST/BP/PRN), Tasks 13–17 — brand_lint.py check families B001..B073, Task 1 — author brand-contract v1 (single definition of every field), Brand layer — docs/brand/, brand-contract v1, docs/brand/lint.py — 31 deterministic copy checks, skill brand-voice (defines and holds the identity) (+6 more)

### Community 18 - "Community 18"
Cohesion: 0.22
Nodes (14): Visual craft cluster BP-079..090 (typography, color, layout), Motion cluster BP-130..132 (token scale, reduced motion, scroll-driven floors), Page weight & responsiveness cluster BP-133..135, Trend adoption & visual debt cluster BP-145..146, Step 4 — Compliance table (applied / adapted / rejected / deferred), Style pack vs practices — identity wins on look, floors win on safety, Screen & interaction rules (one primary action, states, a11y in text), What the audit checks when a Style pack is recorded (+6 more)

### Community 19 - "Community 19"
Cohesion: 0.19
Nodes (14): Reverse Mode (Flows from Code), Same-Change Update Rule (flows + screens + Figma), Per-Feature and Per-Product Completeness Checklists, Init from Existing Code (inventory sweep), Screens Traversed Table (SCR-ID + states used), Update in the Same Change, Scenario Coverage Field (file:line evidence), Errors & Recovery Field (+6 more)

### Community 20 - "Community 20"
Cohesion: 0.23
Nodes (13): Audit report verdict - REFINE / REDESIGN / NEW, benchmark:<competitor> audit scope, Moderated test tasks generated from scenarios.md, ux-audit scope `copy`, Scenario `Strings:` field (optional), Scenario `Telemetry` field (optional), UX contract v4, The costliest ledger item was the cheapest — the assumption made it dear (+5 more)

### Community 21 - "Community 21"
Cohesion: 0.24
Nodes (13): Cursor rules (.mdc) variant, test/validate.py repo validator, BP-147 growth loop named before freemium, BP-148 virality through the product artifact, BP-149 plan K near 0.2 and design cycle time, BP-150 reward in product units, on invitee milestone, BP-151 referral abuse designed against, not discovered, Catalog entries BP-147..156 (+5 more)

### Community 22 - "Community 22"
Cohesion: 0.23
Nodes (12): A rule nobody can verify is a suggestion, PR evidence checklist — what you ran and what it printed, Tag must match the manifests (version sync gate), claude plugin validate --strict conformance step, git push --atomic — --follow-tags lets a tag through alone, One owner per fact — two definitions is drift with a delay fuse, Why the contracts are duplicated into every skill, Release checklist — four-way version bump, preflight, tag (+4 more)

### Community 23 - "Community 23"
Cohesion: 0.21
Nodes (12): /ux-doctor and docs/ux/doctor.py, Contract marker line, The three rules that hold the verbal layer together, brand-contract v1 — the docs/brand/ contract, docs/brand/ as a separate root beside docs/ux/, Companions — sheleg-design and task-pipeline (offers, not dependencies), The four rules that keep agents in sync, super-ux System Map (+4 more)

### Community 24 - "Community 24"
Cohesion: 0.26
Nodes (12): brand-contract v1 artifact contract (docs/brand/), locales/<code>.md — per-locale delta, One-way dependency: brand derives from foundation, Registry adoption cost on legacy projects, strings.md — interface string decision registry, terminology.md — owned terms and banned words, /brand-init command, /brand-update command (+4 more)

### Community 25 - "Community 25"
Cohesion: 0.17
Nodes (12): Diverge Before Converging, Improve Workflow (Heuristic Evaluation to Redesign), Practice Pass with Compliance Table, Task Analysis Method, Throwaway Prototype Step, ux-flows Skill, Frequency x Severity x Solvability Scoring, Product Mechanics Recorded Even When None (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.17
Nodes (12): Cascade Check to Downstream Layers, ux-scenarios Skill, B071 — Locale Parity Below Threshold Warns, B021 — Code No Longer Matches the Row, B022 — String in Code With No Registry Row, B023 — Location That No Longer Resolves, Registry Columns (Key/Text/Location/Scenario/Status), String Statuses (agreed/proposed/drifted/orphan) (+4 more)

### Community 27 - "Community 27"
Cohesion: 0.24
Nodes (11): best-practices-index.md, BP-182..205 - brand and copy practices, bp_index.py, `Checked:` catalog field, Installer family routing block, BP-206 - the wording of the exit, C-02 decision - no Checked: backfill, C-04 upstream reconciliation (+3 more)

### Community 28 - "Community 28"
Cohesion: 0.20
Nodes (11): BP-147..151 - growth loops and referral, validate_catalog(), Acceptance — tier-1 audit findings (v0.27.1), Brief — tier-1 findings from the 51-skill audit, Carry-over ledger (deferred work, never empty), Locked REQ list — add freely, remove only with the operator, Brief — verbal identity layer (brand-voice + copywriting), I-2 — one release instead of three, risk compensated by R-20 (+3 more)

### Community 29 - "Community 29"
Cohesion: 0.38
Nodes (10): brand_contract_state(), diagnose(), find_ux_dir(), fix(), main(), marker(), Path, Only the changes that cannot be wrong. (+2 more)

### Community 30 - "Community 30"
Cohesion: 0.20
Nodes (11): The Build Gate, Settle the Visual Identity (one locked style pack), Figma On/Off Choice Asked Once Per Project, Visual Identity Is ONE Locked Style Pack, Do Not Write Interface Code Until the Chain Is Approved, Design Tooling Section (Figma on/off + file URL only), Design Before You Build, Design System Block (style pack, Figma library, tokens, components, assets) (+3 more)

### Community 31 - "Community 31"
Cohesion: 0.25
Nodes (11): INVEST Stories with Given/When/Then Criteria, Foundation Validate Pass (integrity, quality, coverage), Scenario Traceability Rules, Entry Points Field (all of them: screen, deep link, push, CTA), FLW-NN Entry Fields (Traces/Goal/Entry points/Success exit/Task analysis), User Flows Template (flows.md), Mermaid Flowchart Block (branches and error recovery edges), Flow Wireframe Pointer (wireframes/FLW-NN.md) (+3 more)

### Community 32 - "Community 32"
Cohesion: 0.22
Nodes (11): Scenarios Come Before Interface (the hard rule), Retire, Never Delete, UX Audit Report Template, Base Version (git SHA of docs/ux at audit time), Finding ID Scheme AUD-YYYY-MM-DD-NN, Overall Verdict REFINE/REDESIGN/NEW, Per-Scenario Verdicts PASS/PARTIAL/FAIL/BLOCKED, UX Scenarios Hard Rule (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.22
Nodes (10): BP-173..179 - interface state, platform surfaces and locale, BP-180..181 - information architecture, Story `Kill criteria` field (optional), docs/ux/flows.md, docs/ux/foundation.md, The UX chain pipeline, docs/ux/screens.md, sheleg-design companion (+2 more)

### Community 34 - "Community 34"
Cohesion: 0.25
Nodes (9): Post-release npx smoke test from a clean cwd, publish job — npm publish --provenance, Published is a claim until the registry serves it — poll loop, release job — tag → validator → GitHub release, Dual auth — NPM_TOKEN automation token and OIDC trusted publishing, Test the packed tarball, not the working tree, sshlg-skills member pin — a release that misses it is invisible, Install channels — plugin, Cursor rules, skills CLI, npx (+1 more)

### Community 35 - "Community 35"
Cohesion: 0.31
Nodes (9): Money Moments Are First-Class Flows, JTBD Four Forces Quality Bar, Reviews and Support Tickets Are Evidence Already Sitting There, ux-foundation Skill, UX Foundation Template (foundation.md), Journey Entry JRN-NN (stage rows: action, touchpoint, emotion, pain, opportunity), JTBD Entry JTBD-NN (Statement/Personas/Type/Forces/Success metric), Monetization Section (model, value metric, free boundary, purchase surface, money moments) (+1 more)

### Community 36 - "Community 36"
Cohesion: 0.22
Nodes (9): component-guidelines.md — which control for which job, Craft floors win on safety, the style pack wins on look, Figma surface — SCR-NN/<Screen>/<state> frame mapping, The hard rule — no interface code before the chain, sheleg-design companion (the look, style packs), skill ux-flows (HOW layer + UI map), skill ux-foundation (the WHY layer), skill ux-scenarios (docs/ux/scenarios.md) (+1 more)

### Community 37 - "Community 37"
Cohesion: 0.32
Nodes (8): Idea or improvement template — which layer does it belong to?, validate workflow job (push + PR gate), Code of Conduct (adapted from Contributor Covenant 2.1), Original v0.1.0 implementation plan (historical), super-ux — scenario-driven UI development for AI agents, system-map.md — the whole system on one page, No telemetry, no analytics, no phone-home, Private vulnerability reporting via GitHub Security Advisories

### Community 38 - "Community 38"
Cohesion: 0.39
Nodes (8): test/validate.py (repo validator), Incident: a red gate was committed through, Incident: a tag published a tree four releases old, test/release_preflight.py, Run stamp table, Standing instruction #1 - run the release preflight before tagging, Standing instruction #2 - never read a gate's verdict through a pipe, Standing instructions ledger

### Community 39 - "Community 39"
Cohesion: 0.25
Nodes (8): test/release_preflight.py — is HEAD ahead of origin?, What the ladder walk found beyond the plan (cursor rule, stale release step, REQ-13), Plan — verbal identity layer, 40 tasks in groups A..I, Fix-plan prioritization — Frequency × Severity × Solvability, task-pipeline companion (executes the UX plan), skill ux-audit (code vs the chain, file:line evidence), ux-design-principles.md — heuristics PRN-01..24, The audit is read-only by default — a mismatch is a finding

### Community 40 - "Community 40"
Cohesion: 0.39
Nodes (8): Audit report format (docs/ux/audits), Audit verdicts PASS/PARTIAL/FAIL/BLOCKED, scenarios.md format contract, Scenario-first methodology, SCN-NNN id and status lifecycle rules, Target-project docs/ux contract, ux-audit skill batch loop (v0.1 design), Scope and limits section in the audit report

### Community 41 - "Community 41"
Cohesion: 0.38
Nodes (7): Never stamp a Checked date you did not earn, A practice missing from practice-selection.md is unreachable, I-4 — Checked: only from BP-182 up, Task 21 — taxonomy tags and BP-182..205, best-practices.md — tag-indexed catalog of practices (BP-NNN), best-practices-index.md — generated tag index, practice-selection.md — profile → mandatory practice sets

### Community 42 - "Community 42"
Cohesion: 0.43
Nodes (7): ux-audit scope copy, Pack Failure mode field, Voice pack library — six archetypes, Brand action menu, /brand-lint command, brand-voice workflows: Init, Calibrate, Update, Validate, Machine-drafting markers catalog

### Community 43 - "Community 43"
Cohesion: 0.43
Nodes (6): main(), parse(), (id, title, tags, checked) for every entry, in catalog order. `checked` is ""…, Practices whose review date has aged past `months`, oldest first., render(), stale_report()

### Community 44 - "Community 44"
Cohesion: 0.33
Nodes (7): Accessibility-as-it-fails cluster BP-136..138, Cross-platform stance (component of record, native before ARIA), Product surface registers (primary action → docs and help), Accessibility is copy work too (accessible name = visible label), Errors carry three facts (what happened, what survived, one next step), The four laws of UI copy, UI copy — the strings inside the product

### Community 45 - "Community 45"
Cohesion: 0.60
Nodes (5): B060 — AI-marker density in marketing documents, Humanization guards, Change-rate guard (over 50% do not ship), Naturalness grade A-D on the result, AI-marker severity scale S1/S2/S3

### Community 46 - "Community 46"
Cohesion: 0.40
Nodes (5): Register as a Delta Against the Five Axes, Voice failure mode, The Five Fixed Axes (Confidence/Register/Distance/Humor/Density), Voice Pack as Starting Position, Voice Template (the identity file)

### Community 47 - "Community 47"
Cohesion: 0.67
Nodes (4): BP-153 password rules by 800-63B-4: length and breach check, BP-154 password field does not fight the password manager, BP-155 passwordless offered as an equal door, [NIST] SP 800-63B rev 4 Digital Identity Guidelines

### Community 48 - "Community 48"
Cohesion: 0.67
Nodes (3): closure(), main(), Every contract reachable from `seed` by following links between contracts.

## Ambiguous Edges - Review These
- `benchmark:<competitor> audit scope` → `Moderated test tasks generated from scenarios.md`  [AMBIGUOUS]
  CHANGELOG.md · relation: conceptually_related_to
- `Installer family routing block` → `check_pins.py (sshlg-skills)`  [AMBIGUOUS]
  CHANGELOG.md · relation: shares_data_with

## Knowledge Gaps
- **97 isolated node(s):** `fs`, `path`, `readline`, `{ spawnSync }`, `ROOT` (+92 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `benchmark:<competitor> audit scope` and `Moderated test tasks generated from scenarios.md`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Installer family routing block` and `check_pins.py (sshlg-skills)`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **Why does `Invariants in every language` connect `Community 23` to `Community 46`, `Community 1`, `Community 12`, `Community 9`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `Voice Template (the identity file)` connect `Community 46` to `Community 1`, `Community 26`, `Community 23`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `docs/brand README (how this product speaks)` connect `Community 1` to `Community 26`, `Community 46`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Brand Contract v1` (e.g. with `BP-182..205 - brand and copy practices` and `docs/brand/voice.md`) actually correct?**
  _`Brand Contract v1` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fs`, `path`, `readline` to the rest of the system?**
  _97 weakly-connected nodes found - possible documentation gaps or missing edges._