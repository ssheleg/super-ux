# Graph Report - /Users/sshlg/DATA/super-ux  (2026-08-05)

## Corpus Check
- 90 files · ~113,836 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 698 nodes · 1353 edges · 38 communities (35 shown, 3 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.89)
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

## God Nodes (most connected - your core abstractions)
1. `UX Best Practices Catalog BP-001..206` - 31 edges
2. `Step 2 — Mandatory consideration sets from the profile` - 28 edges
3. `UX Design Principles — How the Agent Thinks` - 25 edges
4. `check()` - 20 edges
5. `UX Contract v4 (scenario-format)` - 19 edges
6. `ux-audit — Scenario Audit Loop (skill)` - 19 edges
7. `read()` - 18 edges
8. `main()` - 17 edges
9. `Brand Contract v1 (reference)` - 17 edges
10. `foundation.md — the WHY layer` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Scope and limits section in the audit report` --semantically_similar_to--> `/brand-lint command`  [INFERRED] [semantically similar]
  docs/superpowers/specs/2026-08-04-tier1-audit-findings-design.md → plugins/super-ux/commands/brand-lint.md
- `Audit verdict fork — REFINE / REDESIGN / NEW` --semantically_similar_to--> `Fix-plan prioritization — Frequency × Severity × Solvability`  [INFERRED] [semantically similar]
  CHANGELOG.md → README.md
- `A rule nobody can verify is a suggestion` --semantically_similar_to--> `One owner per fact — two definitions is drift with a delay fuse`  [INFERRED] [semantically similar]
  .github/ISSUE_TEMPLATE/feature_request.md → CONTRIBUTING.md
- `Audit report 'Scope and limits' — absence never means PASS` --semantically_similar_to--> `Never stamp a Checked date you did not earn`  [INFERRED] [semantically similar]
  CHANGELOG.md → CONTRIBUTING.md
- `Published is a claim until the registry serves it — poll loop` --semantically_similar_to--> `sshlg-skills member pin — a release that misses it is invisible`  [INFERRED] [semantically similar]
  .github/workflows/release.yml → CONTRIBUTING.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The traceable UX chain: foundation → flows → screens → scenarios → audit** — readme_ux_foundation, readme_ux_flows, readme_ux_scenarios, readme_ux_audit, readme_ux_chain, readme_hard_rule, readme_ux_lint [EXTRACTED 1.00]
- **The release gate chain — preflight, atomic push, version sync, publish, downstream verification** — contributing_release_preflight_py, contributing_atomic_push, contributing_release_checklist, _github_workflows_release_version_sync_gate, _github_workflows_release_publish_job, _github_workflows_release_registry_poll, contributing_family_pin, docs_superpowers_retro_standing_instruction_1 [INFERRED 0.85]
- **The verbal identity layer — contract, two skills, linter, catalog cluster** — readme_brand_layer, readme_brand_voice, readme_copywriting, readme_brand_lint, changelog_release_0_30_0, docs_superpowers_plans_2026_08_05_brand_voice_layer_task1_brand_contract, docs_superpowers_plans_2026_08_05_brand_voice_layer_task13_brand_lint [EXTRACTED 1.00]
- **docs/brand/ file set forming brand-contract v1** — docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_voice_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_terminology_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_facts_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_channels_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_strings_md, docs_superpowers_specs_2026_08_05_brand_voice_copywriting_design_locales_files [EXTRACTED 1.00]
- **WHY -> HOW -> WHAT initialization chain** — plugins_super_ux_commands_ux_init_command, plugins_super_ux_commands_ux_foundation_command, plugins_super_ux_commands_ux_flows_command, docs_superpowers_specs_2026_07_19_super_ux_design_scenario_base_contract [EXTRACTED 1.00]
- **Bounded humanize pass — guards that stop the rewrite** — plugins_super_ux_skills_references_ai_tells_severity_scale, plugins_super_ux_skills_references_ai_tells_density_threshold, plugins_super_ux_skills_references_ai_tells_change_rate_guard, plugins_super_ux_skills_references_ai_tells_semantic_preservation_check, plugins_super_ux_skills_references_ai_tells_naturalness_grade [EXTRACTED 1.00]
- **Practice routing: profile → mandatory sets → checklists → compliance table → audit** — plugins_super_ux_skills_references_practice_selection_product_profile, plugins_super_ux_skills_references_practice_selection_mandatory_sets, plugins_super_ux_skills_references_practice_selection_per_artifact_checklists, plugins_super_ux_skills_references_practice_selection_compliance_table, plugins_super_ux_skills_references_best_practices_md, plugins_super_ux_skills_references_best_practices_index_by_tag, plugins_super_ux_skills_ux_audit_skill_practice_pass [EXTRACTED 1.00]
- **The brand pack layer (voice → register → surface → locale → proof)** — plugins_super_ux_skills_references_brand_contract_v1, plugins_super_ux_skills_references_brand_contract_voice_md, plugins_super_ux_skills_references_brand_contract_channels_md, plugins_super_ux_skills_references_brand_contract_facts_md, plugins_super_ux_skills_references_surface_registers_register_model, plugins_super_ux_skills_references_voice_packs_pack_contract, plugins_super_ux_skills_references_localization_length_coefficient [EXTRACTED 1.00]
- **The UX design chain (foundation → flows → screens → scenarios → audits → plans)** — plugins_super_ux_skills_references_scenario_format_foundation_md, plugins_super_ux_skills_references_scenario_format_flows_md, plugins_super_ux_skills_references_scenario_format_screens_md, plugins_super_ux_skills_references_scenario_format_scenarios_md, plugins_super_ux_skills_references_scenario_format_audit_report, plugins_super_ux_skills_references_scenario_format_ux_plan, plugins_super_ux_skills_references_scenario_format_same_change_rule [EXTRACTED 1.00]
- **The docs/ux Artifact Chain (foundation to flows to screens to scenarios to audits)** — templates_foundation_foundation_template, templates_flows_flows_template, templates_screens_screens_template, templates_scenarios_scenarios_template, templates_audit_report_audit_report_template, templates_readme_ux_pipeline [EXTRACTED 1.00]
- **The docs/brand Pack under brand-contract v1** — templates_brand_voice_voice_template, templates_brand_terminology_terminology_template, templates_brand_facts_facts_template, templates_brand_channels_channels_template, templates_brand_strings_strings_template, templates_brand_locale_locale_template, templates_brand_readme_brand_contract_v1 [EXTRACTED 1.00]
- **The ID Traceability Spine (ST/JTBD/JRN to FLW to SCR to SCN to string rows)** — templates_foundation_user_story_entry, templates_flows_flow_entry_fields, templates_screens_screen_entry_fields, templates_scenarios_traces_field, templates_brand_strings_registry_columns [INFERRED 0.95]

## Communities (38 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (104): Behavioral practices cluster BP-001..078, BP-001 Adapt competitor tactics, don't copy them, Visual craft cluster BP-079..090 (typography, color, layout), Figma structure cluster BP-091..100, Components & controls cluster BP-101..115, Web funnels cluster BP-116..123 (landing, pricing, checkout, billing, cancel), Web-to-app funnel cluster BP-124..129, Motion cluster BP-130..132 (token scale, reduced motion, scroll-driven floors) (+96 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (62): Bug report template — quote the file that says so, Idea or improvement template — which layer does it belong to?, A rule nobody can verify is a suggestion, PR evidence checklist — what you ran and what it printed, CHANGELOG section extraction into release notes, Post-release npx smoke test from a clean cwd, publish job — npm publish --provenance, Published is a claim until the registry serves it — poll loop (+54 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (60): Finding, _alternatives(), apply_fixes(), check_ai_tells(), check_bot_safety(), check_channels(), check_consistency(), check_contract() (+52 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (59): brand_lint.py — the deterministic brand linter, channels.md — one record per surface (register, limits, bans), facts.md — the only source of any figure in public copy, The five fixed axes (Confidence, Register, Distance, Humor, Density), B061 — humor banned on error, destructive confirm, billing, paywall, locales/<code>.md — per-locale delta, Brand Contract v1 (reference), README.md `Sources:` block — the paths that get scanned (+51 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (42): Additive and optional keeps the contract at v4, Audit verdict fork — REFINE / REDESIGN / NEW, Story Kill criteria — metric, threshold, deadline, 0.27.0 — tier-1 findings from auditing 51 external skills, 0.27.1 — re-cut of 0.27.0 on the correct base, 0.28.0 — carry-over ledger closed (BP-157..179, PRN-17..21), Audit report 'Scope and limits' — absence never means PASS, Scenario Telemetry field (object_action, snake_case) (+34 more)

### Community 5 - "Community 5"
Cohesion: 0.14
Nodes (37): changelog_version(), check(), check_description_canon(), front_matter(), load_json(), main(), Path, Everything the installer CLI copies must be inside the npm tarball. `npm… (+29 more)

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (33): author, name, url, bin, super-ux, bugs, url, description (+25 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (29): BP-152 empty state states, teaches and gives a path, NN/g Designing Empty States in Complex Applications, brand-contract v1 artifact contract (docs/brand/), channels.md — one record per surface, ux-audit scope copy, locales/<code>.md — per-locale delta, One-way dependency: brand derives from foundation, Pack Failure mode field (+21 more)

### Community 8 - "Community 8"
Cohesion: 0.19
Nodes (18): fail(), fs, installClaudePlugin(), installCursor(), installSkillsCli(), main(), makePrompter(), menu() (+10 more)

### Community 9 - "Community 9"
Cohesion: 0.20
Nodes (18): check_links(), check_unique_and_gaps(), err(), figma_enabled(), find_ux_dir(), ids(), index_ids(), main() (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.17
Nodes (18): CLAUDE.md scenario-first hard rule snippet, BP-156 rejected form preserves work and names the way out, WCAG 2.2 SC 3.3.7 Redundant Entry, Brand voice hard rule in CLAUDE.md, brand_lint.py, B020 — one action, two names, B030 — number in public copy absent from facts.md, B061 — no humor, exclamation or emoji on loss surfaces (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.18
Nodes (17): ux-scenarios skill (v0.1 design), UX action menu (11 actions), /ux-audit command, /ux entry point, /ux-doctor command, Contract drift versus internal consistency, /ux-flows command, Settle the style pack before drawing (+9 more)

### Community 12 - "Community 12"
Cohesion: 0.19
Nodes (14): Reverse Mode (Flows from Code), Same-Change Update Rule (flows + screens + Figma), Per-Feature and Per-Product Completeness Checklists, Init from Existing Code (inventory sweep), Screens Traversed Table (SCR-ID + states used), Update in the Same Change, Scenario Coverage Field (file:line evidence), Errors & Recovery Field (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.17
Nodes (12): Diverge Before Converging, Improve Workflow (Heuristic Evaluation to Redesign), Practice Pass with Compliance Table, Task Analysis Method, Throwaway Prototype Step, ux-flows Skill, Frequency x Severity x Solvability Scoring, Product Mechanics Recorded Even When None (+4 more)

### Community 14 - "Community 14"
Cohesion: 0.17
Nodes (12): Cascade Check to Downstream Layers, ux-scenarios Skill, B071 — Locale Parity Below Threshold Warns, B021 — Code No Longer Matches the Row, B022 — String in Code With No Registry Row, B023 — Location That No Longer Resolves, Registry Columns (Key/Text/Location/Scenario/Status), String Statuses (agreed/proposed/drifted/orphan) (+4 more)

### Community 15 - "Community 15"
Cohesion: 0.38
Nodes (10): brand_contract_state(), diagnose(), find_ux_dir(), fix(), main(), marker(), Path, Only the changes that cannot be wrong. (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.20
Nodes (11): The Build Gate, Settle the Visual Identity (one locked style pack), Figma On/Off Choice Asked Once Per Project, Visual Identity Is ONE Locked Style Pack, Do Not Write Interface Code Until the Chain Is Approved, Design Tooling Section (Figma on/off + file URL only), Design Before You Build, Design System Block (style pack, Figma library, tokens, components, assets) (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.25
Nodes (11): INVEST Stories with Given/When/Then Criteria, Foundation Validate Pass (integrity, quality, coverage), Scenario Traceability Rules, Entry Points Field (all of them: screen, deep link, push, CTA), FLW-NN Entry Fields (Traces/Goal/Entry points/Success exit/Task analysis), User Flows Template (flows.md), Mermaid Flowchart Block (branches and error recovery edges), Flow Wireframe Pointer (wireframes/FLW-NN.md) (+3 more)

### Community 18 - "Community 18"
Cohesion: 0.22
Nodes (11): Scenarios Come Before Interface (the hard rule), Retire, Never Delete, UX Audit Report Template, Base Version (git SHA of docs/ux at audit time), Finding ID Scheme AUD-YYYY-MM-DD-NN, Overall Verdict REFINE/REDESIGN/NEW, Per-Scenario Verdicts PASS/PARTIAL/FAIL/BLOCKED, UX Scenarios Hard Rule (+3 more)

### Community 19 - "Community 19"
Cohesion: 0.27
Nodes (10): B060 — AI-marker density in marketing documents, Humanization guards, Brand routing table (user words to action), Humanize mode, Change-rate guard (over 50% do not ship), Density threshold (~10 markers per 500 words), Naturalness grade A-D on the result, Semantic-preservation checklist (+2 more)

### Community 20 - "Community 20"
Cohesion: 0.29
Nodes (10): Money Moments Are First-Class Flows, JTBD Four Forces Quality Bar, Reviews and Support Tickets Are Evidence Already Sitting There, ux-foundation Skill, Derived-from (PER-NN, JTBD-NN from docs/ux/foundation.md), UX Foundation Template (foundation.md), Journey Entry JRN-NN (stage rows: action, touchpoint, emotion, pain, opportunity), JTBD Entry JTBD-NN (Statement/Personas/Type/Forces/Success metric) (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.25
Nodes (9): B030 — public number with no facts row blocks, B031 — missing Source or past Review by warns, Fact Row Fields (Fact/Value/Source/Checked/Review by/Public), Facts Template (the only source of any public figure), Proof That Is Not a Number (testimonials, awards, press), Public: no — figures that exist and must never be quoted, Narrative Block (Hero/Enemy/Product role/Promise), Brand Voice Hard Rule (+1 more)

### Community 22 - "Community 22"
Cohesion: 0.39
Nodes (8): Audit report format (docs/ux/audits), Audit verdicts PASS/PARTIAL/FAIL/BLOCKED, scenarios.md format contract, Scenario-first methodology, SCN-NNN id and status lifecycle rules, Target-project docs/ux contract, ux-audit skill batch loop (v0.1 design), Scope and limits section in the audit report

### Community 23 - "Community 23"
Cohesion: 0.29
Nodes (8): Channel Record Fields (Register/Format/Limits/Forbidden/CTA/Proof/Locales), Channels Template (one record per surface), Forbidden Splits Platform Physics from Brand Choice, Marketing Surfaces (landing hero, X, Reddit, …), Product Surfaces (primary action, error, empty state, paywall, destructive confirm), Length Coefficient, Length Notes (constraint reaches the primary-locale original), No Humor/Exclamation/Emoji on Error, Destructive, Billing, Paywall

### Community 24 - "Community 24"
Cohesion: 0.52
Nodes (7): BP-147 growth loop named before freemium, BP-148 virality through the product artifact, BP-149 plan K near 0.2 and design cycle time, BP-150 reward in product units, on invitee milestone, BP-151 referral abuse designed against, not discovered, [Viral26] converged virality/referral benchmarks 2026, Virality and referral cluster (REQ-01)

### Community 25 - "Community 25"
Cohesion: 0.43
Nodes (6): main(), parse(), (id, title, tags, checked) for every entry, in catalog order. `checked` is ""…, Practices whose review date has aged past `months`, oldest first., render(), stale_report()

### Community 26 - "Community 26"
Cohesion: 0.47
Nodes (6): Cursor rules (.mdc) variant, test/validate.py repo validator, Catalog entries BP-147..156, practice-selection.md routing update (REQ-05), New taxonomy tags: virality, referral, auth, validate_catalog() catalog integrity check

### Community 27 - "Community 27"
Cohesion: 0.33
Nodes (6): Scope and Limits (absence never means PASS), Surface Names Are Contract Keys (delete, never rename), A Missing Fact Is Reported, Never Invented, docs/brand/lint.py Copy Linter, Sources Block (B006 — no clean run over an unread surface), Both Linters Gate Done-ness (CI/pre-commit)

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (6): Register as a Delta Against the Five Axes, Failure Mode (the degenerate form of this voice), The Five Fixed Axes (Confidence/Register/Distance/Humor/Density), Invariant in Every Language, Voice Pack as Starting Position, Voice Template (the identity file)

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (6): Address Form (decided once, not per string), Locale Header Fields (Locale/Primary/Address form/Coefficient/Humor/Never translated/Reviewed by), B020 — One Action, Two Names, A Decision Registry, Not a Message Catalog, Entity and Tier Names — B012 (one spelling everywhere), One Action Keeps One Name

### Community 30 - "Community 30"
Cohesion: 0.40
Nodes (5): Required Disclaimers Table, Dead Idioms Table (replacement does the same job), Keywords Researched in Market, Never Translated, Legal Differences Treated as Required Strings, Locale Delta Template (locales/<code>.md)

### Community 31 - "Community 31"
Cohesion: 0.40
Nodes (5): Brand Commands (/brand, /brand-init, /brand-update, /brand-lint, /copy), brand-contract v1, docs/brand README (how this product speaks), docs/ux README (seeded folder guide), docs/ux/lint.py Integrity Linter

### Community 32 - "Community 32"
Cohesion: 0.40
Nodes (5): Banned List Seeded from ai-tells.md, Banned Words — B011, Glossary (grounded before it is leaned on), Product Terms — B010, Terminology Template (the dictionary the linter reads)

### Community 33 - "Community 33"
Cohesion: 0.67
Nodes (4): BP-153 password rules by 800-63B-4: length and breach check, BP-154 password field does not fight the password manager, BP-155 passwordless offered as an equal door, [NIST] SP 800-63B rev 4 Digital Identity Guidelines

### Community 34 - "Community 34"
Cohesion: 0.67
Nodes (3): closure(), main(), Every contract reachable from `seed` by following links between contracts.

## Knowledge Gaps
- **84 isolated node(s):** `fs`, `path`, `readline`, `{ spawnSync }`, `ROOT` (+79 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `docs/brand README (how this product speaks)` connect `Community 31` to `Community 32`, `Community 14`, `Community 21`, `Community 23`, `Community 28`, `Community 30`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **What connects `fs`, `path`, `readline` to the rest of the system?**
  _84 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05078416728902166 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05182443151771549 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.08302485457429931 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.06545879602571596 - nodes in this community are weakly interconnected._
- **Should `Community 4` be split into smaller, more focused modules?**
  _Cohesion score 0.06504065040650407 - nodes in this community are weakly interconnected._