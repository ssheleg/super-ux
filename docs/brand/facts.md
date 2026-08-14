Contract: brand-contract v1

# Facts

**The only source of any figure in public copy.** A number on a public
surface with no row here is `B030` and blocks. A row with no `Source`, or one
past its `Review by`, is `B031` and warns.

A missing fact is reported, never invented to close a gap.

Every row below names a command that recomputes it. That is the point: this
project's own vision says numbers are derived, not stored, and a fact table
of hand-maintained integers would contradict it on the first release. The
2026-08-10 audit found three stale counts in the README (181 practices
against 206, 31 lint checks against 33, and a heuristic range four versions
old), all of which had agreed with themselves for months. On 2026-08-14 this
table was itself the stale one: 206 practices against 210, 33 lint checks
against 37, 3107 validator checks against 3240. Naming the command is not
the same as running it, and only running it produces a fact.

The same day, later: `B030` went red on `215` in the README before the run that
wrote it had touched this table. That is the intended sequence rather than a
near miss. The count moves in the catalogue, the README quotes it, and the gate
refuses the quote until a row here has been recomputed. Every row above was
re-run at that point, and two had moved: practices 210 → 215, validator checks
3240 → 3500, the last 150 of them from the Contents-anchor check this run added.

| Fact | Value | Source | Checked | Review by | Public |
|---|---|---|---|---|---|
| skills shipped | 7 | `ls plugins/super-ux/skills \| grep -v references \| wc -l` | 2026-08-14 | 2026-11-14 | yes |
| commands shipped | 15 | `ls plugins/super-ux/commands/*.md \| wc -l` | 2026-08-14 | 2026-11-14 | yes |
| Cursor rules shipped | 8 | `ls cursor/rules/*.mdc \| wc -l` | 2026-08-14 | 2026-11-14 | yes |
| practices in the catalog | 215 | `grep -c '^#### BP-' plugins/super-ux/skills/references/best-practices.md` | 2026-08-14 | 2026-11-14 | yes |
| design heuristics | 24 | highest `PRN-NN` in `ux-design-principles.md` | 2026-08-14 | 2026-11-14 | yes |
| brand-lint checks | 37 | unique `B0NN` codes emitted by `plugins/super-ux/scripts/brand_lint.py` | 2026-08-14 | 2026-11-14 | yes |
| repo validator checks | 3500 | `python3 test/validate.py` final line | 2026-08-14 | 2026-11-14 | no |
| agents reachable via the skills CLI | 70+ | vercel-labs/skills agent registry | 2026-08-14 | 2026-11-14 | yes |

`Public: no` marks figures that exist and must never be quoted — internal
margins, unreleased counts, anything under embargo. The linter treats
quoting one as the same failure as quoting a number that does not exist. The
validator's check count is `no` deliberately: it moves with every gate added
and would be stale in a public sentence within a week.

## Proof that is not a number

Testimonials, awards, certifications and press. Same rules: attributed,
dated, and re-checked.

| Claim | Attribution | Source | Checked | Review by | Public |
|---|---|---|---|---|---|
| none recorded | — | — | 2026-08-10 | 2026-11-10 | no |

There is nothing here, and that is written down rather than left blank so
nobody fills the gap from memory.

## Required disclaimers

None. The product makes no performance, security or outcome claim that would
need one.
