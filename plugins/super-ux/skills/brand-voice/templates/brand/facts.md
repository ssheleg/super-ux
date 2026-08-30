Contract: brand-contract v1

# Facts

**The only source of any figure in public copy.** A number on a public
surface with no row here is `B030` and blocks. A row with no `Source`, or one
past its `Review by`, is `B031` and warns.

A missing fact is reported, never invented to close a gap.

| Fact | Value | Source | Checked | Review by | Public |
|---|---|---|---|---|---|
| <what the number counts> | <448> | <api/catalog.json> | <2026-08-05> | <2026-11-05> | <yes> |
| <internal figure> | <$3.10> | <billing export> | <2026-08-05> | <2026-11-05> | <no> |

`Public: no` marks figures that exist and must never be quoted — internal
margins, unreleased counts, anything under embargo. The linter treats
quoting one as the same failure as quoting a number that does not exist.

## Proof that is not a number

Testimonials, awards, certifications and press. Same rules: attributed,
dated, and re-checked.

| Claim | Attribution | Source | Checked | Review by | Public |
|---|---|---|---|---|---|
| <…> | <name, role, company> | <where it was said> | <YYYY-MM-DD> | <YYYY-MM-DD> | <yes> |

## Required disclaimers

Text that must appear alongside specific claims — regulatory, contractual, or
promised. Locale differences live in `locales/<code>.md`.

| Claim it attaches to | Required text |
|---|---|
| <…> | <…> |
