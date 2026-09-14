# Practice Selection Protocol

The deterministic bridge between the catalogs
([best-practices.md](best-practices.md) BP-001..241 — behavioral BP-001..078,
visual craft BP-079..090, Figma structure BP-091..100, components & controls
BP-101..115, web funnels BP-116..123, web2app BP-124..129, motion
BP-130..132, weight & responsiveness BP-133..135, accessibility in practice
BP-136..138, frustration telemetry BP-139..140, gamification BP-141..142,
personalization BP-143..144, trend governance BP-145..146, growth loops and
referral BP-147..151, empty states BP-152, authentication and form recovery
BP-153..156, motion craft BP-157..164, perceived quality BP-165..168,
generated-default tells BP-169..172, interface state and platform surfaces
BP-173..179, information architecture BP-180..181, verbal identity BP-182..206,
developer products BP-207..210, funnel wiring BP-211..215, product
dashboards BP-216..227, the long SaaS landing BP-228..234, long
time-to-value products BP-235..241;
[ux-design-principles.md](ux-design-principles.md) PRN-01..24)
and the two
functions that consume them: **design** (`ux-flows`, `ux-scenarios`) and
**audit** (`ux-audit`). Purpose: the right practices get considered at the
right step every time — nothing relevant silently skipped, nothing
irrelevant cargo-culted.

## Contents

- [Step 1 — Product profile](#step-1--product-profile)
- [Step 2 — Mandatory sets from the profile](#step-2--mandatory-sets-from-the-profile)
- [Step 3 — Per-artifact checklists](#step-3--per-artifact-checklists)
- [Step 4 — Compliance table (the record)](#step-4--compliance-table-the-record)
- [Anti-cargo-cult rule](#anti-cargo-cult-rule)


## Step 1 — Product profile

Build once from `foundation.md` (ask the user for missing dimensions; store
answers in the foundation):

| Dimension | Values |
|---|---|
| Platform | mobile-ios, mobile-android, web, voice, ai-chat (multi-select) |
| Money model | none, subscription, freemium, hybrid, one-time |
| Distribution | app-store, web-direct, both |
| Purchase surface | none, in-app (IAP), web checkout, web2app (web funnel → app) |
| Acquisition | paid-ads, organic, both |
| Forms present | yes/no (signup, checkout, data entry) |
| Analytics present | yes/no |
| Personalization | none, rule-based, inferred/model-driven |
| Engagement mechanics | none, streaks/tiers, points/badges/leaderboards |

## Step 2 — Mandatory sets from the profile

`ALWAYS` applies to every product: PRN-01..24, BP-001. PRN-22..24 are
the verbal ones — one voice with per-surface registers, every claim
checkable, no levity where the user can lose something. They read as brand
rules and are therefore easy to file as optional, but any product with text
has them, which is every product with an interface.

| Profile fact | Mandatory consideration set |
|---|---|
| any graphical UI | BP-079..090 (visual craft: typography, color, layout) — the **floor**; the concrete palette/type/motion come from the recorded style pack ([visual-identity.md](visual-identity.md)) |
| any graphical UI (controls) | BP-101..115 (which control for the job; states; platform component of record) — see [component-guidelines.md](component-guidelines.md) |
| any graphical UI (motion) | BP-054, BP-130..132 (token scale, reduced motion, scroll-driven floors), BP-157..164 (does it animate at all, durations, easing, origin, interruptibility, hover gating) |
| any graphical UI (look) | BP-145, BP-146 (trend adopted through its mechanism, with the compensation named), BP-165..168 (icon family, emoji, pressed states, scrim), BP-169..172 (defaults that read as generated) |
| Figma enabled | BP-091..100 (file structure, SCR-ID frame naming, tokens, variants, auto layout) |
| mobile-* | BP-049..054, BP-164, BP-178 |
| mobile-ios | + BP-031, BP-033 (OS surfaces, widgets — as opportunities) |
| web | BP-052, BP-058, BP-059, BP-133..138, BP-173, BP-176, BP-179 (weight budget, baseline viewport, input capability, native semantics, real evidence, regime) |
| forms: yes | BP-050, BP-055..057, BP-143, BP-156, BP-175 |
| account / sign-in present | BP-119, BP-153..155 (password rules, manager-friendly field, a passwordless door) |
| voice | BP-060..065 |
| ai-chat | BP-063..066 |
| money ≠ none | BP-067..074 |
| subscription / hybrid | + BP-016..030 (paywalls), BP-031..039 (retention/lifecycle) |
| freemium / hybrid | + BP-024..027, BP-073, BP-074, BP-147..151 (the loop the free tier feeds) |
| app-store | BP-075, BP-076 |
| paid-ads | BP-043, BP-077, BP-078 |
| web-direct / both, money ≠ none | BP-116..123 (landing → pricing → checkout → billing → cancel) |
| purchase surface: web checkout or web2app | + BP-127, BP-128 (storefront rules, billing duties), BP-212..215 (stand-up order, the three decisions on collected data, sourced legal text, the access ladder) |
| purchase surface: web2app | + BP-124..126, BP-129 (funnel, handoff, deferred deep link, whole-chain measurement) |
| analytics: yes | BP-040..048, BP-139, BP-140 |
| personalization ≠ none | BP-143, BP-144, BP-211 (what the branch may vary, and its default) |
| the funnel stores anything about a person | BP-213, BP-214 — and this row has no "no" branch on a funnel with a quiz or a checkout |
| engagement mechanics ≠ none | BP-141, BP-142, BP-032 |

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
| Cancel / winback flow | BP-017, BP-027, BP-035, BP-123; PRN-03 |
| Rating prompt flow | BP-076; PRN-16 |
| Forms / checkout | BP-050, BP-055..057, BP-119, BP-120, BP-143, BP-156; PRN-05, PRN-09 |
| Sign-up / sign-in / password | BP-119, BP-153..156; PRN-05, PRN-09 |
| Growth loop / referral program | BP-147..151, BP-067, BP-073 |
| Landing / campaign page | BP-116, BP-117, BP-229, BP-230, BP-231, BP-077, BP-132, BP-133, BP-169..172; PRN-08 |
| Long self-serve SaaS landing | BP-228..234, BP-240, BP-116..121; PRN-08 |
| Product dashboard / tool home | BP-216..227, BP-235..241, BP-045, BP-152, BP-173, BP-180; PRN-06, PRN-14 |
| Integration / connect-a-source flow | BP-235, BP-209, BP-004, BP-012 |
| Product with a months-long time-to-value | BP-237, BP-236, BP-238, BP-072, BP-073 |
| KPI card, metric strip, chart block | BP-217..222, BP-227, BP-045; PRN-06 |
| Dense table or ranked list | BP-222, BP-223, BP-224, BP-226; PRN-06 |
| In-product upgrade prompt | BP-233, BP-024..026, BP-073, BP-074 |
| Developer landing (API, SDK, CLI, MCP) | BP-207, BP-208, BP-117, BP-116; PRN-08 |
| Capability / per-feature page | BP-210, BP-208, BP-194..197; PRN-23 |
| First-run or setup checklist | BP-209, BP-004, BP-012, BP-206 |
| Pricing page (web) | BP-118, BP-022, BP-073; PRN-08 |
| Abandonment recovery | BP-121, BP-017, BP-035; PRN-09 |
| Dunning / failed payment | BP-122, BP-128; PRN-01, PRN-09 |
| Web2app funnel + paid handoff | BP-124..129, BP-211..215, BP-030, BP-078; PRN-01, PRN-09 |
| Quiz / survey-driven offer | BP-211, BP-002, BP-010, BP-029, BP-143; PRN-02, PRN-12 |
| Post-payment access delivery | BP-215, BP-125, BP-126, BP-121; PRN-01, PRN-09 |
| Reading a funnel market before designing one | `funnel-research.md` FR-01..FR-07, then BP-001 |
| Navigation / IA | BP-049, BP-051..053, BP-173, BP-180, BP-181; PRN-06, PRN-14 |
| Any user-visible string | BP-182, BP-185, BP-189; PRN-22 |
| Error, empty or loading state | BP-186, BP-187, BP-188; PRN-24 |
| Landing, pricing or feature page | BP-190..193; PRN-23 |
| Paywall, popup, consent or cancellation ask | BP-206; PRN-24 |
| Content aimed at search or answer engines | BP-194..197; PRN-23 |
| Social, changelog, ads or email surface | BP-183, BP-184, BP-198..200 |
| App Store or Google Play listing | BP-201, BP-205 |
| Permissions / notifications | BP-013, BP-036..038 |
| Lifecycle / email sequences | BP-034, BP-039, BP-071 |
| Voice / chat dialog | BP-060..066; PRN-01, PRN-03, PRN-09 |
| Empty / first-use states | BP-004, BP-012, BP-152; screen rules (principles doc) |
| Store listing | BP-075, BP-077 |
| Analytics / experiment design | BP-040..048 |
| Screen build / visual polish | BP-079..090, BP-130, BP-145, BP-146, BP-165..172; PRN-08, PRN-15 |
| Reading surfaces (articles, docs, long copy) | BP-079, BP-081, BP-086, BP-087 |
| Data tables / dashboards | BP-086, BP-088; PRN-06 |
| Animated / scroll-driven surface | BP-054, BP-130..132, BP-133, BP-157..164; PRN-01, PRN-08 |
| Destructive or irreversible action | BP-174, BP-175, BP-187; PRN-03, PRN-05, PRN-24 |
| Multi-locale surface | BP-177, BP-202..205; PRN-02, PRN-22 |
| Long list / table / feed | BP-179, BP-086, BP-088; PRN-06 |
| Responsive layout pass | BP-134, BP-135, BP-050, BP-087 |
| Accessibility pass | BP-059, BP-081, BP-083, BP-136..138; PRN-01, PRN-04 |
| Gamified / streak surface | BP-141, BP-142, BP-032, BP-035; PRN-16 |
| Personalized / adaptive surface | BP-143, BP-144, BP-077; PRN-02, PRN-12 |

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
- **Granularity, because "every practice" does not scale and pretending it does
  produces the skip it forbids.** A mobile subscription product pulls roughly
  **150 practices for a single flow**; the worked example above has four rows, and
  the honest output at that scale is a compliance table longer than the design it
  documents. So: **per-practice verdicts for the artifact row and for anything the
  artifact actually touches; one band verdict — with its reason — for each
  remaining set.** A band reads `BP-002..015 — rejected (band): onboarding
  practices, no onboarding surface in this flow`. A band with no reason is a
  silent skip wearing a table row, and a set that turns out to contain one
  practice the artifact touches is un-banded and given its own row. This was
  improvised by a fresh-context agent that ran the pass at real scale, said it was
  deviating, and was right to.
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

Style pack vs practices: the pack owns identity (palette, type pairing,
motion tokens, bans) and wins on look; the practices own floors (contrast,
tap targets, line length, spacing rhythm) and win on safety. Record any
conflict and its resolution in the table like any other.
