# Practice Selection Protocol

The deterministic bridge between the catalogs
([best-practices.md](best-practices.md) BP-001..100 — behavioral BP-001..078,
visual craft BP-079..090, Figma structure BP-091..100;
[ux-design-principles.md](ux-design-principles.md) PRN-01..16) and the two
functions that consume them: **design** (`ux-flows`, `ux-scenarios`) and
**audit** (`ux-audit`). Purpose: the right practices get considered at the
right step every time — nothing relevant silently skipped, nothing
irrelevant cargo-culted.

## Step 1 — Product profile

Build once from `foundation.md` (ask the user for missing dimensions; store
answers in the foundation):

| Dimension | Values |
|---|---|
| Platform | mobile-ios, mobile-android, web, voice, ai-chat (multi-select) |
| Money model | none, subscription, freemium, hybrid, one-time |
| Distribution | app-store, web-direct, both |
| Acquisition | paid-ads, organic, both |
| Forms present | yes/no (signup, checkout, data entry) |
| Analytics present | yes/no |

## Step 2 — Mandatory sets from the profile

`ALWAYS` applies to every product: PRN-01..16, BP-001.

| Profile fact | Mandatory consideration set |
|---|---|
| any graphical UI | BP-079..090 (visual craft: typography, color, layout) |
| Figma enabled | BP-091..100 (file structure, SCR-ID frame naming, tokens, variants, auto layout) |
| mobile-* | BP-049..054 |
| mobile-ios | + BP-031, BP-033 (OS surfaces, widgets — as opportunities) |
| web | BP-052, BP-058, BP-059 |
| forms: yes | BP-050, BP-055..057 |
| voice | BP-060..065 |
| ai-chat | BP-063..066 |
| money ≠ none | BP-067..074 |
| subscription / hybrid | + BP-016..030 (paywalls), BP-031..039 (retention/lifecycle) |
| freemium / hybrid | + BP-024..027, BP-073, BP-074 |
| app-store | BP-075, BP-076 |
| paid-ads | BP-043, BP-077, BP-078 |
| analytics: yes | BP-040..048 |

"Mandatory consideration" = each practice in the set gets an explicit
verdict (Step 4), not automatic adoption.

## Step 3 — Per-artifact checklists

When designing or auditing a specific flow/artifact, pull its row ON TOP of
the Step-2 sets:

| Artifact | Checklist |
|---|---|
| Onboarding flow | BP-002..015, BP-069, BP-072, BP-077; PRN-11, PRN-12 |
| Paywall flow | BP-016..023, BP-028..030, BP-069, BP-070; PRN-08; honesty anti-pattern (principles doc) |
| Upgrade-at-limit flow | BP-024..026, BP-073, BP-074 |
| Trial start/end | BP-070, BP-071, BP-072, BP-019 (trial anxiety) |
| Cancel / winback flow | BP-017, BP-027, BP-035; PRN-03 |
| Rating prompt flow | BP-076; PRN-16 |
| Forms / checkout | BP-050, BP-055..057; PRN-05, PRN-09 |
| Navigation / IA | BP-049, BP-051..053; PRN-06, PRN-14 |
| Permissions / notifications | BP-013, BP-036..038 |
| Lifecycle / email sequences | BP-034, BP-039, BP-071 |
| Voice / chat dialog | BP-060..066; PRN-01, PRN-03, PRN-09 |
| Empty / first-use states | BP-004, BP-012; screen rules (principles doc) |
| Store listing | BP-075, BP-077 |
| Analytics / experiment design | BP-040..048 |
| Screen build / visual polish | BP-079..090; PRN-08, PRN-15 |
| Reading surfaces (articles, docs, long copy) | BP-079, BP-081, BP-086, BP-087 |
| Data tables / dashboards | BP-086, BP-088; PRN-06 |

## Step 4 — Compliance table (the record)

Every design pass and every deep audit produces one table per artifact:

```markdown
| Practice | Verdict | How / why not |
|----------|---------|---------------|
| BP-069 | applied | paywall at onboarding step 6, after value promise |
| BP-020 | rejected | fixed pricing is a brand decision (owner: user) |
| BP-070 | deferred | until A/B infra exists; trigger: analytics live |
| PRN-12 | adapted | default template instead of "suggest for me" |
```

Verdicts: `applied` / `adapted` (how) / `rejected` (why — a reason, not a
shrug) / `deferred` (what unblocks it). Rules:

- Every practice from the mandatory sets and the artifact row gets a
  verdict. No silent skips.
- `applied`/`adapted` must be visible in the artifact (flow node, scenario
  field, plan row) — a verdict without a trace is fiction.
- Rejections owned by the user (taste, brand, strategy) are recorded as
  such and NOT re-litigated on every pass.
- In design: the table lives in the flow entry (collapsible) or the UX
  plan. In audit: in the report's Practice compliance section.

## Anti-cargo-cult rule

A practice is applied only when it serves a traced job/story of THIS
product (BP-001 discipline). The mandatory sets force the *consideration*,
never the adoption. When two practices conflict (e.g. BP-069 first-session
paywall vs a deliberate freemium-led motion per BP-067), the foundation's
Monetization section decides — and the conflict + decision goes into the
compliance table.
