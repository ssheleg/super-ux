# Graph Report - super-ux  (2026-08-16)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1036 nodes · 1632 edges · 129 communities (51 shown, 78 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8f924dbb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- brand/lint.py
- brand_lint.py
- P-02: Multi-agent operator
- validate.py
- CLAUDE.md
- Step 2 — Mandatory consideration sets
- UX Best Practices Catalog BP-001..206
- UX Audit Report Template
- docs/brand README (how this product speaks)
- UX Contract (v4)
- package.json
- /ux — single entry point for all UX work
- brand_lint.py — the brand linter (35 deterministic checks)
- ux/lint.py
- ux_lint.py
- super-ux.js
- brand-voice skill
- Marketing copy — pages, posts and long form
- Surface registers — one voice, many surfaces
- Brand Contract v1 — the contract for docs/brand/
- doctor.py
- ux_doctor.py
- docs/brand/terminology.md — our words, banned words, entity and tier names
- super-ux — scenario-driven UI development for AI agents
- Register as a delta on the five axes
- Locales — one voice, several languages
- Voice packs — the archetype library
- The design chain — vision → foundation → flows → screens → scenarios → build → audit
- brand_lint_test.py
- bp_index.py
- The scenario-first hard rule
- peer-builder — the chosen voice pack
- ux_lint_test.py
- Failure mode — insider shorthand and performed honesty
- Invariants in every language
- validate — CI workflow
- best-practices.md — 206 proven practices
- closure
- One owner per fact (convention)
- The ssheleg skill family
- Plan — тир 1 находок аудита
- Brief — a public web surface gets a home, and the router learns the user's words
- super-ux — Scenario-Driven UI Development for AI Agents (Design Spec)
- install.sh
- /ux-doctor command
- release_preflight.py
- Idea or improvement template — which layer does it belong to?
- Code of Conduct (adapted from Contributor Covenant 2.1)
- git push --atomic origin main vX.Y.Z
- Acceptance — carry-over ledger закрыт
- README.md
- PR evidence checklist — what you ran and what it printed
- Changelog 0.10.0
- Changelog 0.11.0
- Changelog 0.12.0
- Changelog 0.12.1
- Changelog 0.1.0
- Changelog 0.2.0
- Changelog 0.30.1
- Changelog 0.3.0
- Changelog 0.4.0
- Changelog 0.5.0
- Changelog 0.6.0
- Changelog 0.7.0
- Changelog 0.8.0
- Changelog 0.9.0
- Never stamp a Checked date you did not earn
- Why the contracts are duplicated per skill
- The edit → sync → validate loop
- Stable IDs, never reused
- validate_skill_parity invariant
- validate_stated_numbers invariant
- Locale parity computed against strings.md
- Banned words
- Entity and tier names — exact spelling
- Brief — the web funnel gets its research method, its personalization contract, and a router for the layer that takes the money
- Design — the verbal identity layer: brand-voice + copywriting
- Principle — we name defects with file:line, not with adjectives
- GitHub Release Workflow
- GitHub Validate Workflow
- Search and answer engines: safety first, optimization second
- /brand-lint command
- /ux-audit command
- /ux-flows command
- /ux-foundation command
- /ux-lint command
- /ux-update command
- BP-002 Micro-commitments before conversion points
- BP-003 Start onboarding lean, grow it by iteration
- BP-004 Onboarding continues after the paywall
- BP-005 Loading screens that sell, not spin
- BP-006 Social proof early in onboarding
- BP-007 Use the user's name early
- BP-008 Story-style multi-screen intro
- BP-009 Persona-driven conversational guide
- BP-010 Echo the user's stated goal everywhere
- BP-011 Test placement of key asks
- BP-012 Anticipate hesitation with defaults
- BP-013 Sell the permission before the OS prompt
- BP-014 Offer SSO
- BP-015 Distinct visual identity
- BP-016 Scrollable, educating paywall
- BP-017 Meaningful second offers
- BP-018 Interactive story paywalls
- BP-019 Multi-page paywalls to cut cognitive load
- BP-020 "Choose your price"
- BP-021 Video on/before the paywall
- BP-022 Plan structure as a nudge (decoy/anchor)
- BP-023 Behavior-segmented offers
- BP-024 Lock icons on premium features
- BP-025 Upgrade CTAs beyond the paywall
- BP-026 "Free Edition" labeling
- BP-027 Second trial for returning users
- BP-028 Lifetime as a second offer
- BP-029 Simple paywall personalization
- BP-030 Web purchase flows beside IAP
- Wireframes & storyboards (optional artifacts)
- Scenarios Come Before Interface (the hard rule)
- The audit is read-only by default — a mismatch is a finding
- Heuristic Findings [PRN-NN] (deep depth)
- Register as a Delta Against the Five Axes
- Brand Same-Change Rule

## God Nodes (most connected - your core abstractions)
1. `brand_lint.py — the brand linter (35 deterministic checks)` - 37 edges
2. `check()` - 29 edges
3. `UX Best Practices Catalog BP-001..206` - 28 edges
4. `main()` - 27 edges
5. `read()` - 25 edges
6. `Step 2 — Mandatory consideration sets` - 22 edges
7. `/ux — single entry point for all UX work` - 19 edges
8. `read()` - 16 edges
9. `read()` - 16 edges
10. `P-02: Multi-agent operator` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Do NOT trigger for bug fixes, refactors, tests, docs` --semantically_similar_to--> `Anti-cargo-cult rule`  [INFERRED] [semantically similar]
  templates/vision-rule.md → plugins/super-ux/skills/references/practice-selection.md
- `5. Principles` --semantically_similar_to--> `Anti-cargo-cult rule`  [INFERRED] [semantically similar]
  templates/vision.md → plugins/super-ux/skills/references/practice-selection.md
- `Brand voice — hard rule (super-ux)` --semantically_similar_to--> `PRN-22 — One voice, many registers`  [INFERRED] [semantically similar]
  templates/claude-rule.md → plugins/super-ux/skills/references/ux-design-principles.md
- `Never quote a number with no row in facts.md` --semantically_similar_to--> `PRN-23 — Every claim is checkable`  [INFERRED] [semantically similar]
  templates/claude-rule.md → plugins/super-ux/skills/references/ux-design-principles.md
- `No humor, exclamation marks or emoji where the user can lose something` --semantically_similar_to--> `PRN-24 — Never joke about the user's loss`  [INFERRED] [semantically similar]
  templates/claude-rule.md → plugins/super-ux/skills/references/ux-design-principles.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The brand pack under brand-contract v1** — docs_brand_terminology_product_terms, docs_brand_channels_register_delta, docs_brand_locales_en_locale_delta [EXTRACTED 1.00]
- **Brand Voice Layer Implementation** — docs_evidence_briefs_2026_08_05_brand_voice_layermd_brand_voice_layer, docs_evidence_plans_2026_08_05_brand_voice_layermd_brand_voice_layer_plan, plugins_super_ux_skills_copywriting_skill_copywriting, plugins_super_ux_skills_references_ai_tellsmd_ai_tells [EXTRACTED 1.00]
- **The docs/brand/ pack — the six files brand-contract v1 governs** — plugins_super_ux_skills_references_brand_contract_voice_md, plugins_super_ux_skills_references_brand_contract_terminology_md, plugins_super_ux_skills_references_brand_contract_facts_md, plugins_super_ux_skills_references_brand_contract_channels_md, plugins_super_ux_skills_references_brand_contract_strings_md, plugins_super_ux_skills_references_brand_contract_locales_md [EXTRACTED 1.00]
- **Release Process** — github_workflows_release_yml, github_workflows_validate_yml, changelog_0_38_2 [EXTRACTED 1.00]
- **super-ux Design Chain** — claude_md, readme_md, docs_agent_sync_md, docs_evidence_backlog_md, docs_evidence_retro_md, docs_evidence_verification_md, docs_evidence_briefs_2026_08_04_tier1_audit_findings_acceptance_md [EXTRACTED 1.00]
- **The three composition gates added in 0.32.0** — contributing_validate_stated_numbers, contributing_validate_skill_parity, contributing_validate_seeded_scripts, contributing_edit_sync_validate_loop [EXTRACTED 1.00]
- **Tier 1 Audit Findings Process** — docs_evidence_briefs_2026_08_04_tier1_audit_findingsmd_tier1_audit_findings, docs_evidence_plans_2026_08_04_tier1_audit_findingsmd_tier1_audit_findings_plan, docs_evidence_specs_2026_08_04_tier1_audit_findings_designmd_tier1_audit_findings_design [EXTRACTED 1.00]
- **The super-ux traceability chain — vision → foundation → flows → screens → scenarios** — docs_ux_readme_pipeline, docs_ux_vision_essence, docs_ux_foundation_st_004, docs_ux_flows_flw_03, docs_ux_screens_scr_04, docs_ux_scenarios_scn_006 [EXTRACTED 1.00]
- **Validation Pipeline** — github_workflows_validate_yml, changelog_0_39_0, changelog_0_34_0 [EXTRACTED 1.00]
- **Web Surface and Routing Feature** — docs_evidence_briefs_2026_08_10_web_surface_and_routingmd_web_surface_and_routing, docs_evidence_briefs_2026_08_10_web_surface_and_routing_acceptancemd_web_surface_and_routing_acceptance, docs_evidence_plans_2026_08_10_web_surface_and_routingmd_web_surface_and_routing_plan [EXTRACTED 1.00]
- **Degrade rather than block — the named degraded modes across the installer surface** — docs_ux_vision_principle_degrade_not_block, docs_ux_foundation_accessibility_regime, docs_ux_screens_scr_04, docs_ux_screens_scr_06, docs_ux_scenarios_scn_010, docs_ux_scenarios_scn_013 [INFERRED 0.85]
- **What super-ux installs into a target project: two hard rules and two checkers** — templates_claude_rule_ux_scenarios_hard_rule, templates_claude_rule_brand_voice_hard_rule, templates_vision_rule_vision_alignment_hard_rule, templates_readme_lint_py, templates_readme_doctor_py [INFERRED 0.85]
- **The ID Traceability Spine (ST/JTBD/JRN to FLW to SCR to SCN to string rows)** — templates_foundation_user_story_entry, templates_flows_flow_entry_fields, templates_scenarios_traces_field, templates_brand_strings_registry_columns [INFERRED 0.95]

## Communities (129 total, 78 thin omitted)

### Community 0 - "brand/lint.py"
Cohesion: 0.06
Nodes (79): _alternatives(), apply_fixes(), _around(), check_ai_tells(), check_bot_safety(), check_channels(), check_consistency(), check_contract() (+71 more)

### Community 1 - "brand_lint.py"
Cohesion: 0.06
Nodes (79): _alternatives(), apply_fixes(), _around(), check_ai_tells(), check_bot_safety(), check_channels(), check_consistency(), check_contract() (+71 more)

### Community 2 - "P-02: Multi-agent operator"
Cohesion: 0.06
Nodes (75): B020 — one action under two names, B021 — registry text disagrees with the source, B023 — a location that no longer resolves, Interpolated messages left unregistered, and why, String menu.nothing — "Nothing selected", Interface string registry (docs/brand/strings.md), The word prefix is the vocabulary (install:/skip:/keep:/seed:/sync:/warning:/error:), FLW-01: Interactive install (+67 more)

### Community 3 - "validate.py"
Cohesion: 0.08
Nodes (61): changelog_version(), check(), check_description_canon(), check_floor(), check_routed_triggers_still_advertised(), _dedent_block(), _disclose_routing(), front_matter() (+53 more)

### Community 4 - "CLAUDE.md"
Cohesion: 0.04
Nodes (50): Changelog 0.16.0, Changelog 0.16.1, Changelog 0.16.2, Changelog 0.17.0, Changelog 0.17.1, Changelog 0.18.0, Changelog 0.19.0, Changelog 0.20.0 (+42 more)

### Community 5 - "Step 2 — Mandatory consideration sets"
Cohesion: 0.07
Nodes (50): Anti-cargo-cult rule, best-practices.md catalog (BP-001..206), BP-001 — traced-job discipline, BP-067 — freemium-led motion, BP-069 — first-session paywall placement, BP-070 — reverse trial, BP-129 — whole-chain web2app measurement, BP-138 — accessibility regime (EAA / ADA) (+42 more)

### Community 6 - "UX Best Practices Catalog BP-001..206"
Cohesion: 0.06
Nodes (47): Behavioral practices cluster BP-001..078, Visual craft cluster BP-079..090 (typography, color, layout), Figma structure cluster BP-091..100, Components & controls cluster BP-101..115, Web funnels cluster BP-116..123 (landing, pricing, checkout, billing, cancel), Web-to-app funnel cluster BP-124..129, Motion cluster BP-130..132 (token scale, reduced motion, scroll-driven floors), Page weight & responsiveness cluster BP-133..135 (+39 more)

### Community 7 - "UX Audit Report Template"
Cohesion: 0.06
Nodes (45): Cascade Check to Downstream Layers, Figma On/Off Choice Asked Once Per Project, INVEST Stories with Given/When/Then Criteria, JTBD Four Forces Quality Bar, Frequency x Severity x Solvability Scoring, Product Mechanics Recorded Even When None, Reviews and Support Tickets Are Evidence Already Sitting There, ux-foundation Skill (+37 more)

### Community 8 - "docs/brand README (how this product speaks)"
Cohesion: 0.05
Nodes (42): Per-Feature and Per-Product Completeness Checklists, Scope and Limits (absence never means PASS), Channel Record Fields (Register/Format/Limits/Forbidden/CTA/Proof/Locales), Channels Template (one record per surface), Forbidden Splits Platform Physics from Brand Choice, Marketing Surfaces (landing hero, X, Reddit, …), Product Surfaces (primary action, error, empty state, paywall, destructive confirm), Surface Names Are Contract Keys (delete, never rename) (+34 more)

### Community 9 - "UX Contract (v4)"
Cohesion: 0.07
Nodes (38): SCN-001: First-run onboarding — happy path, UX Contract (v4), super-ux System Map, UX Design Principles — How the Agent Thinks, ux-audit, ux-flows, ux-foundation, super-ux System Map (vision) (+30 more)

### Community 10 - "package.json"
Cohesion: 0.06
Nodes (33): author, name, url, bin, super-ux, bugs, url, description (+25 more)

### Community 11 - "/ux — single entry point for all UX work"
Cohesion: 0.08
Nodes (30): /brand-init command, Never invent a fact to fill a table, plugin scripts/brand_lint.py, Never seed an empty vision.md, /ux-init command, Routing row: "what do best practices say" → practices / heuristics audit, Routing row: "check everything works" / audit → ux-audit, Routing row: "the copy is inconsistent" / "tone of voice" → brand-voice (+22 more)

### Community 12 - "brand_lint.py — the brand linter (35 deterministic checks)"
Cohesion: 0.08
Nodes (28): B001 (E) — a file under docs/brand/ has no contract marker, B002 (E) — markers disagree across the pack, B003 (W) — voice.md is draft while strings.md holds agreed rows, B004 (E) — Derived-from cites an id absent from foundation.md, B005 (W) — foundation.md changed after Last calibrated, B020 (E) — one action carries two different names, B021 (E) — a registered string diverged from the code, B022 (W) — a code string has no registry row (+20 more)

### Community 13 - "ux/lint.py"
Cohesion: 0.16
Nodes (26): check_links(), check_unique_and_gaps(), check_vision(), check_web_surface(), entry_blocks(), err(), figma_enabled(), find_ux_dir() (+18 more)

### Community 14 - "ux_lint.py"
Cohesion: 0.16
Nodes (26): check_links(), check_unique_and_gaps(), check_vision(), check_web_surface(), entry_blocks(), err(), figma_enabled(), find_ux_dir() (+18 more)

### Community 15 - "super-ux.js"
Cohesion: 0.18
Nodes (19): fail(), fs, installClaudePlugin(), installCursor(), installSkillsCli(), main(), makePrompter(), menu() (+11 more)

### Community 16 - "brand-voice skill"
Cohesion: 0.13
Nodes (15): Acceptance — вербальный слой, v0.30.0, Brief — вербальный слой: brand-voice + copywriting, Verbal identity layer — implementation plan, Brand action menu, /brand entry point, Brand routing table (user words to action), /brand-update command, /copy command (+7 more)

### Community 17 - "Marketing copy — pages, posts and long form"
Cohesion: 0.20
Nodes (14): B030 (E) — a figure in public copy has no row in facts.md, B031 (W) — a fact has no source, or is past its Review by, docs/brand/facts.md — canonical figures, the only source, Comparison-page honesty rule (concede something real), Four inputs before writing (action, reader, their words, proof), The grounding model (prerequisite vs introduced), Marketing copy — pages, posts and long form, Page structure (headline → final CTA) and page types (+6 more)

### Community 18 - "Surface registers — one voice, many surfaces"
Cohesion: 0.22
Nodes (14): B040 (E) — a field exceeds its surface limit, B073 (E) — a field overflows under the locale's coefficient, docs/brand/channels.md — one record per surface (register, limits, bans), Channel Playbooks — the physics of each surface, Physics decays — every ranking behaviour carries a checked date, Platform physics per marketing surface, Length coefficient (multiplies every field limit per locale), Store field limits and the two structural differences (+6 more)

### Community 19 - "Brand Contract v1 — the contract for docs/brand/"
Cohesion: 0.19
Nodes (13): B006 (E) — README.md has no Sources: block, nothing to scan, B007 (W) — ## Voice references names no admired or no refused brand, B042 (E) — a link in a body where the surface's physics forbid it, B061 (E) — humor where the user is losing something, Brand Contract v1 — the contract for docs/brand/, The five fixed voice axes (Confidence, Register, Distance, Humor, Density), Humor is forbidden where the user is losing something, Platform physics and brand choice are separate fields (+5 more)

### Community 20 - "doctor.py"
Cohesion: 0.38
Nodes (10): brand_contract_state(), diagnose(), find_ux_dir(), fix(), main(), marker(), Path, Only the changes that cannot be wrong. (+2 more)

### Community 21 - "ux_doctor.py"
Cohesion: 0.38
Nodes (10): brand_contract_state(), diagnose(), find_ux_dir(), fix(), main(), marker(), Path, Only the changes that cannot be wrong. (+2 more)

### Community 22 - "docs/brand/terminology.md — our words, banned words, entity and tier names"
Cohesion: 0.22
Nodes (10): Empty states, authentication & form recovery cluster BP-152..156, B010 (E) — a banned word appears in a registered string, B011 (E) — a generic word used where a product term exists, B012 (E) — an entity or tier name spelled inconsistently, docs/brand/terminology.md — our words, banned words, entity and tier names, Product surface registers (primary action → docs and help), Empty states teach; three kinds need different copy, Errors carry three facts (what happened, what survived, one next step) (+2 more)

### Community 23 - "super-ux — scenario-driven UI development for AI agents"
Cohesion: 0.28
Nodes (9): validate_seeded_scripts invariant, Brand same-change hard rule, docs/brand/ — the brand layer, docs/brand/lint.py — 35 deterministic checks (B001..B073), skill: brand-voice, skill: copywriting, super-ux — scenario-driven UI development for AI agents, /ux — the one command (+1 more)

### Community 24 - "Register as a delta on the five axes"
Cohesion: 0.25
Nodes (9): Surface: destructive confirm, Surface: empty state, Surface: primary action, Register as a delta on the five axes, Dead idioms table, Length coefficient and its effective limits, Locale delta file (en, primary), docs/brand/ — how this product speaks (+1 more)

### Community 25 - "Locales — one voice, several languages"
Cohesion: 0.31
Nodes (9): Verbal identity cluster BP-182..206, What travels and what does not (invariant vs reconsidered per locale), Keywords are researched per market, never translated, Locales — one voice, several languages, Parity declared rather than hidden (B071), Translate the job the string does, not the words (B072), The iOS keyword field (B041 — four rules), Store listings — App Store and Google Play (+1 more)

### Community 26 - "Voice packs — the archetype library"
Cohesion: 0.46
Nodes (8): Pack: calm-expert, Pack: editorial-premium, Voice packs — the archetype library, Pack: operator-brief, The pack contract (nine fields every pack carries), Pack: peer-builder, Pack: plain-service, Pack: playful-consumer

### Community 27 - "The design chain — vision → foundation → flows → screens → scenarios → build → audit"
Cohesion: 0.25
Nodes (8): companion: task-pipeline, The design chain — vision → foundation → flows → screens → scenarios → build → audit, figma-integration.md / figma-structure.md — the optional Figma surface, skill: ux-audit, skill: ux-flows (the HOW layer + the UI map), skill: ux-foundation (the WHY layer), skill: ux-scenarios, skill: vision

### Community 28 - "brand_lint_test.py"
Cohesion: 0.36
Nodes (7): case(), fix_idempotent(), git_date_beats_mtime(), main(), `--fix` clears what it claims to, and the second run has nothing left. A fixer…, Write a temp pack and compare the codes returned. `files` land inside the brand…, B005 dates a file by its commit, not by when it landed on this disk. A fresh…

### Community 29 - "bp_index.py"
Cohesion: 0.43
Nodes (6): main(), parse(), (id, title, tags, checked) for every entry, in catalog order. `checked` is ""…, Practices whose review date has aged past `months`, oldest first., render(), stale_report()

### Community 30 - "The scenario-first hard rule"
Cohesion: 0.33
Nodes (6): Bug report template — quote the file that says so, Test from a packed tarball, not the working tree, The scenario-first hard rule, scenario-format.md — the contract, ux_doctor.py — the contract doctor, docs/ux/lint.py + /ux-lint — the deterministic half

### Community 31 - "peer-builder — the chosen voice pack"
Cohesion: 0.33
Nodes (6): Admired reference: Stripe's API documentation, The five fixed voice axes, calm-expert — the runner-up pack, Brand narrative — hero, enemy, product role, promise, peer-builder — the chosen voice pack, Refused reference: the "We're thrilled to announce" launch-post register

### Community 32 - "ux_lint_test.py"
Cohesion: 0.33
Nodes (4): case(), The clean twin: these codes must NOT fire on this tree., Run the linter over a temp tree and compare the codes it emitted. Matching is…, silent()

### Community 33 - "Failure mode — insider shorthand and performed honesty"
Cohesion: 0.40
Nodes (5): Surface: changelog, Surface: landing hero (the README), Sources: block — what the linter is allowed to read, Glossary — chain, layer, trace, orphan, contract, style pack, register, Failure mode — insider shorthand and performed honesty

### Community 34 - "Invariants in every language"
Cohesion: 0.40
Nodes (5): Surface: error, Invariants in every language, companion: sheleg-design, Craft floors vs style pack — the boundary, visual-identity.md — the visual layer and its owner

### Community 35 - "validate — CI workflow"
Cohesion: 0.40
Nodes (5): CI step: Brand linter unit tests (fixture per check code), CI step: Claude Code conformance, plugin + marketplace --strict, CI step: Validate repo consistency (test/validate.py), CI step: UX linter fixtures (test/ux_lint_test.py), validate — CI workflow

### Community 36 - "best-practices.md — 206 proven practices"
Cohesion: 0.40
Nodes (5): best-practices.md — 206 proven practices, best-practices-index.md — generated tag index, component-guidelines.md — which control for which job, practice-selection.md — profile → mandatory sets → compliance table, ux-design-principles.md — heuristics PRN-01..24

### Community 37 - "closure"
Cohesion: 0.67
Nodes (3): closure(), main(), Every contract reachable from `seed` by following links between contracts.

### Community 38 - "One owner per fact (convention)"
Cohesion: 0.67
Nodes (3): A rule nobody can verify is a suggestion, One owner per fact (convention), Forbidden carries both halves: physics and brand

### Community 39 - "The ssheleg skill family"
Cohesion: 0.67
Nodes (3): The family catalogue moves with the release, A plain skills copy shadows the plugin, The ssheleg skill family

### Community 40 - "Plan — тир 1 находок аудита"
Cohesion: 0.67
Nodes (3): Brief — тир 1 находок из аудита 51 внешнего UX-скила, Plan — тир 1 находок аудита, Spec — тир 1 находок аудита

### Community 41 - "Brief — a public web surface gets a home, and the router learns the user's words"
Cohesion: 0.67
Nodes (3): Acceptance — web surface in the chain, and a router that speaks, Brief — a public web surface gets a home, and the router learns the user's words, Plan — web surface in the contract, and a router that speaks

### Community 42 - "super-ux — Scenario-Driven UI Development for AI Agents (Design Spec)"
Cohesion: 0.67
Nodes (3): super-ux Repo Implementation Plan, super-ux — Scenario-Driven UI Development for AI Agents (Design Spec), /ux-rule command

### Community 44 - "/ux-doctor command"
Cohesion: 0.67
Nodes (3): Contract drift (project vs contract version), plugin scripts/ux_doctor.py, /ux-doctor command

## Knowledge Gaps
- **305 isolated node(s):** `Wireframes & storyboards (optional artifacts)`, `Heuristic Findings [PRN-NN] (deep depth)`, `Register as a Delta Against the Five Axes`, `Page structure (headline → final CTA) and page types`, `B020 — one action under two names` (+300 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **78 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `docs/brand README (how this product speaks)` connect `docs/brand README (how this product speaks)` to `UX Contract (v4)`, `Brand Contract v1 — the contract for docs/brand/`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `templates/brand/voice.md — the seeded voice.md` connect `Brand Contract v1 — the contract for docs/brand/` to `docs/brand README (how this product speaks)`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `Brand Contract v1 — the contract for docs/brand/` connect `Brand Contract v1 — the contract for docs/brand/` to `UX Contract (v4)`, `brand_lint.py — the brand linter (35 deterministic checks)`, `Marketing copy — pages, posts and long form`, `Surface registers — one voice, many surfaces`, `docs/brand/terminology.md — our words, banned words, entity and tier names`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **What connects `Wireframes & storyboards (optional artifacts)`, `Heuristic Findings [PRN-NN] (deep depth)`, `Register as a Delta Against the Five Axes` to the rest of the system?**
  _305 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `brand/lint.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06107594936708861 - nodes in this community are weakly interconnected._
- **Should `brand_lint.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06107594936708861 - nodes in this community are weakly interconnected._
- **Should `P-02: Multi-agent operator` be split into smaller, more focused modules?**
  _Cohesion score 0.055855855855855854 - nodes in this community are weakly interconnected._