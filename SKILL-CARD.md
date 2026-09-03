# Skill Card — super-ux

## Identity

| Field | Value |
|---|---|
| Pack | `super-ux` |
| Version | `0.52.5` |
| Skills | `vision`, `ux-foundation`, `ux-flows`, `ux-scenarios`, `ux-audit`, `brand-voice`, `copywriting` |
| License | MIT |
| Source | https://github.com/ssheleg/super-ux |

## Job and boundary

Decide what a user-facing interface must do and how its words sound: vision,
personas and jobs, flows, screens, scenarios, evidence-backed audits and the
brand contract. Visual style belongs to `sheleg-design`; provider integrations
and backend mechanics stay outside this pack.

## Inputs and outputs

Inputs are product context, existing behavior and user evidence. Outputs live in
versioned `docs/ux/` and `docs/brand/` contracts, plus audit findings and
copy tied back to those contracts. A behavior change updates its scenario.

## Runtime and trust

The pack is Markdown plus standard-library linters and templates. It reads the
repository surfaces named in its contracts and writes only within the requested
product/documentation scope. Facts missing from the brand pack are reported,
never invented.

## Distribution

Install from npm/GitHub, through the Agent Skills CLI, or as the `super-ux`
Claude Code plugin.

## Verification

- Repository validator: `python3 test/validate.py`
- Contract linters and negative plants: repository test suite
- House audit: pinned `make-skill` auditor in `validate.yml`
- Behavioral data: `test/evals/`
- Evaluation status: designed and schema-validated; no model run claimed

## Known limits

The pack cannot replace missing user research with certainty. An inferred
foundation stays labelled inferred. A clean linter proves contract shape, not
that real users agree with the product decision.

