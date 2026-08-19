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

**2026-08-20 — the sentence became a check.** For four releases "every row names
a command that recomputes it" was true of the *naming* and of nothing else, and
two of the rows named no command at all: `design heuristics` said "highest
`PRN-NN` in `ux-design-principles.md`" and `brand-lint checks` said "unique
`B0NN` codes emitted by …", which are descriptions of a count rather than a way
to get one. Recomputed by hand that day: six rows agreed and **`repo validator
checks` read 3500 against a measured 3539** — the table whose whole purpose is to
be the only source of any public figure was carrying a stale one, and it went
unnoticed because the row is `Public: no`, so no `B030` could ever point at it. A
wrong number nobody may quote is still a wrong number; it is just unfalsifiable
by the check that was watching.

`validate_facts_recompute` in `test/validate.py` now runs each `Source` and
compares its output with the `Value`. Every row is a real command, including the
self-referential one: `repo validator checks` runs `python3 test/validate.py` as
a child with `SUPER_UX_FACTS_RECOMPUTE_CHILD=1`, which skips the recomputation
and not the counting — so the child performs exactly as many checks as the parent
and the number it prints is the number the parent would print. The one row that
cannot be recomputed here says so in the words `not recomputable here:` and the
run **discloses** it (`unlooked: …`) instead of counting it as a pass: an
external registry has no command in this repository, and a row that admits it is
worth more than a row a loop skips while claiming to check everything.

| Fact | Value | Source | Checked | Review by | Public |
|---|---|---|---|---|---|
| skills shipped | 7 | `ls plugins/super-ux/skills \| grep -v references \| wc -l \| tr -d ' '` | 2026-08-20 | 2026-11-20 | yes |
| commands shipped | 15 | `ls plugins/super-ux/commands/*.md \| wc -l \| tr -d ' '` | 2026-08-20 | 2026-11-20 | yes |
| Cursor rules shipped | 8 | `ls cursor/rules/*.mdc \| wc -l \| tr -d ' '` | 2026-08-20 | 2026-11-20 | yes |
| practices in the catalog | 215 | `grep -c '^#### BP-' plugins/super-ux/skills/references/best-practices.md` | 2026-08-20 | 2026-11-20 | yes |
| design heuristics | 24 | `grep -c '^\| PRN-' plugins/super-ux/skills/references/ux-design-principles.md` | 2026-08-20 | 2026-11-20 | yes |
| brand-lint checks | 39 | `grep -o '"B[0-9]\{3\}"' plugins/super-ux/scripts/brand_lint.py \| sort -u \| wc -l \| tr -d ' '` | 2026-08-20 | 2026-11-20 | yes |
| repo validator checks | 3667 | `python3 test/validate.py \| sed -n 's/^OK (\([0-9]*\) checks)$/\1/p'` | 2026-08-20 | 2026-11-20 | no |
| agents reachable via the skills CLI | 70+ | not recomputable here: the vercel-labs/skills agent registry is an external list, and no command in this repository returns it | 2026-08-20 | 2026-11-20 | yes |

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
