Contract: brand-contract v1

# Terminology

The dictionary the linter reads. Column one of **Product terms** and
**Banned** drives `B010` and `B011`; **Entity and tier names** drives `B012`.

## Product terms — always

Where the product has its own word, the generic one is a defect, not a
synonym.

| Our term | Never write | Applies to |
|---|---|---|
| the chain | the docs, the specs | the traced set of layers from vision to scenarios |
| scenario | use case, user story | one entry in `scenarios.md` |
| drift | inconsistency, mismatch | code diverging from its record |
| finding | issue, problem | one audited defect with `file:line` evidence |
| skill | module, capability | one directory under `plugins/super-ux/skills/` |
| the pack | the brandbook, the guidelines | `docs/brand/` and its voice record |
| contract | schema, spec | the versioned format every artifact obeys |

## Entity and tier names — exact spelling

One spelling, everywhere: interface, marketing, billing, support, docs.

| Name | Wrong forms seen |
|---|---|
| super-ux | Super UX, SuperUX, super_ux |
| sheleg-design | Sheleg Design, sheleg design |
| task-pipeline | Task Pipeline, taskpipeline |
| Claude Code | ClaudeCode, claude-code |
| Cursor | cursor (mid-sentence, as the product) |
| Codex | codex, OpenAI Codex |
| Claude Code plugin | plugin for Claude Code |

## Banned

Seeded at init from weak verbs, hedging chains and the marker vocabulary in
`ai-tells.md`. Calibration adds what is specific to this product.

| Word or phrase | Why | Use instead |
|---|---|---|
| leverage | filler verb | use |
| seamless | claims what it cannot show | name the step that disappeared |
| utilize | longer word, same meaning | use |
| robust | hides the number | the number |
| blazingly fast | benchmark claim with no harness | the measurement, or nothing |
| effortless | the effort moved, it did not vanish | who does the work now |
| unlock | metaphor standing in for a mechanism | what becomes possible, plainly |
| best-in-class | unarguable and unowned | the comparison, with the configuration |
| powerful | says nothing a reader can check | the specific capability |
| simply | hides the difficulty from the person about to meet it | the steps |

## Glossary

Terms this product uses in a specific sense. If a term is here, it is
grounded before it is leaned on.

| Term | Meaning |
|---|---|
| the chain | vision → foundation → flows → screens → scenarios, each tracing to the one above |
| layer | one file in the chain, owned by exactly one skill |
| trace | an ID reference upward, e.g. a scenario naming the story it serves |
| orphan | a screen, flow or scenario nothing above it points to |
| the contract | `ux-contract v4` — the field names and IDs every artifact obeys |
| style pack | the visual identity, owned by sheleg-design, recorded by reference |
| register | a per-surface delta on the five voice axes, never a new voice |
