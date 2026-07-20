# UX Best Practices Catalog (living)

A growing, tag-indexed catalog of proven UX/growth practices. Agents consult
it when designing foundations, drafting scenarios, and auditing: filter by
tags, apply what fits the product, ignore what doesn't. Practices are
**suggestions with a mechanism**, not rules — a practice is adopted only
when it serves a job/story in the project's foundation.

**How to add entries:** next `BP-NNN` id (never reuse), one practice per
entry, own-words summary, mechanism (`Why`), applicability (`Apply when`),
tags from the taxonomy (extend taxonomy when genuinely needed), source
attribution. Keep entries under ~6 lines.

## Tag taxonomy

- **Stage:** `onboarding` `paywall` `pricing` `post-paywall` `retention`
  `lifecycle` `winback` `analytics` `testing`
- **Mechanism:** `personalization` `social-proof` `commitment` `scarcity`
  `anchoring` `friction-reduction` `habit` `reward` `segmentation`
  `attribution` `activation`
- **Domain:** `subscription-app` `mobile` `ios` `freemium` `email` `push`
  `widgets`
- **Channel of effect:** `conversion` `engagement` `trust` `revenue`
  `insight`

## Practices

Source key: **[48Laws]** = "48 Laws of Subscription App Success" (Botsi,
2025).

### Onboarding & early experience

#### BP-001: Adapt competitor tactics, don't copy them
- **Do:** before reusing a flow seen elsewhere, name the psychology behind it (commitment, social proof, loss aversion), check it fits your product's value and audience, then test an adapted version.
- **Why:** tactics work through user mindset, not layout; verbatim copies miss the mechanism.
- **Apply when:** any "competitor X does Y" proposal appears.
- **Tags:** onboarding, paywall, testing, conversion, subscription-app
- **Source:** [48Laws] L1

#### BP-002: Micro-commitments before conversion points
- **Do:** add small interactive steps (draw to confirm, pick a goal, choose preferences) before account creation / trial / paywall.
- **Why:** active participation raises emotional investment; invested users drop less.
- **Apply when:** designing onboarding ahead of any big ask.
- **Tags:** onboarding, commitment, conversion, mobile
- **Source:** [48Laws] L2

#### BP-003: Start onboarding lean, grow it by iteration
- **Do:** first version captures only what's needed to reach first value; measure drop-off per step; add richness in small increments.
- **Why:** long invented flows overwhelm users and hide which step works.
- **Apply when:** greenfield onboarding, or an onboarding rewrite is proposed wholesale.
- **Tags:** onboarding, testing, activation, friction-reduction
- **Source:** [48Laws] L3

#### BP-004: Onboarding continues after the paywall
- **Do:** after paywall (converted or not), route into a guided first task, repeat the value message, personalize next screens from onboarding answers — never dump onto a generic dashboard.
- **Why:** activation and early retention are decided right after conversion; a blank home screen wastes peak intent.
- **Apply when:** designing post-paywall/post-signup experience.
- **Tags:** post-paywall, onboarding, activation, retention, personalization
- **Source:** [48Laws] L4

#### BP-005: Loading screens that sell, not spin
- **Do:** replace generic loaders before the paywall with value messaging, social proof, or personalized copy.
- **Why:** primes intent in dead time; excited users convert better.
- **Apply when:** any loading/preparation moment exists before a conversion point.
- **Tags:** onboarding, paywall, social-proof, conversion
- **Source:** [48Laws] L5

#### BP-006: Social proof early in onboarding
- **Do:** show "X people use this", press mentions, testimonials during onboarding; personalize testimonials to the user's stated goal when possible.
- **Why:** users are still evaluating; trust cues lower perceived risk.
- **Apply when:** onboarding of an evaluating (not yet committed) user.
- **Tags:** onboarding, social-proof, trust, conversion
- **Source:** [48Laws] L6

#### BP-007: Use the user's name early
- **Do:** capture first name early and surface it in the next screens ("Let's get you started, [Name]").
- **Why:** simple human personalization raises engagement cheaply.
- **Apply when:** onboarding collects a name anyway.
- **Tags:** onboarding, personalization, engagement
- **Source:** [48Laws] L7

#### BP-008: Story-style multi-screen intro
- **Do:** first-open intro as auto-advancing story screens (IG-style) with skip, instead of a static carousel.
- **Why:** familiar pattern, lower initial drop-off, keeps momentum.
- **Apply when:** first app open needs orientation content.
- **Tags:** onboarding, engagement, mobile, friction-reduction
- **Source:** [48Laws] L8

#### BP-009: Persona-driven conversational guide
- **Do:** a coach/mascot persona that appears early, reacts to choices ("Great choice! Based on your goal of X…") and stays through onboarding into the paywall.
- **Why:** human, continuous guidance beats sterile checklists; value feels continuous.
- **Apply when:** products with coaching/assistant potential.
- **Tags:** onboarding, personalization, engagement, trust
- **Source:** [48Laws] L9

#### BP-010: Echo the user's stated goal everywhere
- **Do:** capture 1–2 zero-party data points (goal, preference) early and re-insert the exact phrase across onboarding and the paywall ("Your plan is tailored for [goal]"). String insertion first, ML never first.
- **Why:** cheap, testable relevance boost.
- **Apply when:** onboarding asks any goal/preference question.
- **Tags:** onboarding, paywall, personalization, conversion
- **Source:** [48Laws] L10

#### BP-011: Test placement of key asks
- **Do:** treat account creation, push opt-in, paywall position as movable; e.g. account creation right after welcome (high intent) instead of before the paywall; split big asks apart.
- **Why:** the same ask converts differently at different intent moments.
- **Apply when:** onboarding has multiple asks stacked or misplaced.
- **Tags:** onboarding, testing, conversion, friction-reduction
- **Source:** [48Laws] L11

#### BP-012: Anticipate hesitation with defaults
- **Do:** at decision-heavy steps add "Suggest for me" / sensible defaults so users can proceed without deciding.
- **Why:** decision paralysis is a drop-off point; guided choice keeps flow.
- **Apply when:** any step requires choosing from many options; critical for audiences prone to decision fatigue.
- **Tags:** onboarding, friction-reduction, engagement
- **Source:** [48Laws] L12

#### BP-013: Sell the permission before the OS prompt
- **Do:** before push/email permission, show concrete benefits with previews of actual notifications; trigger the system prompt only after.
- **Why:** understood value → opt-in; opt-in → engagement channels that lift retention and conversion.
- **Apply when:** any OS permission ask (push, email, location…).
- **Tags:** onboarding, push, trust, engagement, conversion
- **Source:** [48Laws] L13

#### BP-014: Offer SSO
- **Do:** if account creation exists, offer Apple/Google SSO alongside email.
- **Why:** usually improves signup conversion; forced email-only is friction.
- **Apply when:** any account-creation flow.
- **Tags:** onboarding, friction-reduction, conversion
- **Source:** [48Laws] L14

#### BP-015: Distinct visual identity
- **Do:** custom illustrations, mascot, or consistent visual motif in onboarding and primary screens.
- **Why:** recognition + emotional engagement lift conversion in crowded categories.
- **Apply when:** product risks looking like "another utility app".
- **Tags:** onboarding, trust, engagement, conversion
- **Source:** [48Laws] L15

### Paywalls & monetization

#### BP-016: Scrollable, educating paywall
- **Do:** long vertical paywall: value highlights, testimonials with real faces, FAQ for objections, optional founder story.
- **Why:** lets undecided users explore at their pace instead of feeling blocked; education + social proof reduce uncertainty.
- **Apply when:** static single-screen paywall underperforms; considered purchase.
- **Tags:** paywall, social-proof, trust, conversion, subscription-app
- **Source:** [48Laws] L16

#### BP-017: Meaningful second offers
- **Do:** after a declined paywall: limited-time discount, cheap lifetime, "why didn't you subscribe?" mini-survey driving the next offer, contextual re-engagement on app open. Think in paywall sequences, not one shot.
- **Why:** 90%+ don't convert on the first paywall; they're not lost, they need a different angle.
- **Apply when:** any conversion funnel with a primary paywall.
- **Tags:** paywall, pricing, winback, conversion, segmentation
- **Source:** [48Laws] L17

#### BP-018: Interactive story paywalls
- **Do:** multi-screen story-like offer ("Reveal your discount"), multiple entry points, skip for users who already decided.
- **Why:** users choose their exploration depth; internalized value beats a blocking screen; great for sale campaigns.
- **Apply when:** sales/campaign offers; static paywall fatigue.
- **Tags:** paywall, engagement, conversion, scarcity
- **Source:** [48Laws] L18

#### BP-019: Multi-page paywalls to cut cognitive load
- **Do:** split value messaging, trial explanation, and pricing onto separate screens; address trial anxiety explicitly (what happens when, risk-free).
- **Why:** one overloaded screen forces too many decisions at once.
- **Apply when:** paywall crams benefits + trial terms + prices together.
- **Tags:** paywall, friction-reduction, trust, conversion
- **Source:** [48Laws] L19

#### BP-020: "Choose your price"
- **Do:** offer a bounded price choice (slider or few options) framed by value ("choose what feels fair").
- **Why:** agency + fairness framing; many pick above minimum.
- **Apply when:** mission-driven brands, price-sensitive audiences; keep the range managed.
- **Tags:** paywall, pricing, trust, revenue
- **Source:** [48Laws] L20

#### BP-021: Video on/before the paywall
- **Do:** short muted-by-default video (testimonial, walkthrough, demo) in or right before the paywall.
- **Why:** raises perceived quality and confidence; more engaging than static graphics.
- **Apply when:** product demos well visually; app already has video content.
- **Tags:** paywall, trust, engagement, conversion
- **Source:** [48Laws] L21

#### BP-022: Plan structure as a nudge (decoy/anchor)
- **Do:** structure tiers so the preferred plan stands out (e.g. trial only on annual; a mid plan priced to make annual look better). Avoid tiers that cannibalize high-LTV options.
- **Why:** anchoring and decoys shift choice toward higher-LTV plans without price cuts.
- **Apply when:** designing/reviewing the plan lineup.
- **Tags:** pricing, anchoring, revenue, subscription-app
- **Source:** [48Laws] L22

#### BP-023: Behavior-segmented offers
- **Do:** segment by first-session behavior: engaged users see standard/premium; low-engagement users see discount or extended trial.
- **Why:** intent differs; matching offer to intent lifts conversion without discounting everyone.
- **Apply when:** enough early behavioral signal exists.
- **Tags:** paywall, pricing, segmentation, conversion
- **Source:** [48Laws] L23

#### BP-024: Lock icons on premium features
- **Do:** show locks on gated content/features across the app (menus, lists, cards), not only at the paywall.
- **Why:** visible scarcity reminds free users what they're missing; lifts trial starts.
- **Apply when:** freemium apps with visible premium surface.
- **Tags:** freemium, scarcity, conversion
- **Source:** [48Laws] L24

#### BP-025: Upgrade CTAs beyond the paywall
- **Do:** put "Unlock"/"Upgrade" CTAs in settings, feature screens, profile, sidebars.
- **Why:** catches users at high-intent contextual moments.
- **Apply when:** freemium with recurring free usage.
- **Tags:** freemium, conversion, engagement
- **Source:** [48Laws] L25

#### BP-026: "Free Edition" labeling
- **Do:** label the free experience ("Free Edition") in headers/home/feature names.
- **Why:** light scarcity framing — constant subconscious reminder there's more.
- **Apply when:** freemium; avoid if it degrades brand feel.
- **Tags:** freemium, scarcity, conversion
- **Source:** [48Laws] L26

#### BP-027: Second trial for returning users
- **Do:** returning lapsed-trial users (freemium) get another free trial.
- **Why:** they likely missed the aha moment; self-initiated return + fresh trial restarts intent without price cuts.
- **Apply when:** freemium app with meaningful share of active-but-never-converted users.
- **Tags:** freemium, winback, retention, conversion
- **Source:** [48Laws] L27

#### BP-028: Lifetime as a second offer
- **Do:** offer an attractively-priced lifetime plan to non-converters or short-plan subscribers — not on the primary paywall.
- **Why:** subscription-averse users accept one-time purchases; wrong placement cannibalizes subscriptions.
- **Apply when:** second-offer stage; watch cannibalization.
- **Tags:** pricing, paywall, revenue, winback
- **Source:** [48Laws] L28

#### BP-029: Simple paywall personalization
- **Do:** one onboarding question → personalized paywall headline ("For users who want X").
- **Why:** perceived relevance lifts conversion; no ML needed.
- **Apply when:** onboarding collects any segmenting answer.
- **Tags:** paywall, personalization, conversion
- **Source:** [48Laws] L29

#### BP-030: Web purchase flows beside IAP
- **Do:** (where store rules allow) test web checkout links/in-app web views for purchases; start with post-paywall upsells, not the primary flow.
- **Why:** ~3-4% processor fees vs 15-30% IAP; flexible pricing/trials; drawer/modal web views convert better than browser redirects.
- **Apply when:** US storefront iOS apps; factor rejection risk, test carefully.
- **Tags:** ios, pricing, revenue, paywall
- **Source:** [48Laws] L30

### Retention, engagement & lifecycle

#### BP-031: OS-level surfaces for re-engagement
- **Do:** App Clips for pre-install value taste; Live Activities / lock-screen widgets for contextual reminders, streaks, offers.
- **Why:** value and presence outside the app without notification fatigue.
- **Apply when:** iOS products with glanceable state or previewable value.
- **Tags:** ios, widgets, retention, engagement
- **Source:** [48Laws] L31

#### BP-032: Variable rewards for habit
- **Do:** reward meaningful behaviors on a variable schedule around a consistent average (not every time, not random taps). A/B fixed vs variable, measure D7/D14.
- **Why:** unpredictable reinforcement builds stronger habits than fixed rewards.
- **Apply when:** repeated core actions exist; mind the ethics — tie to genuinely useful behaviors.
- **Tags:** retention, habit, reward, engagement
- **Source:** [48Laws] L32

#### BP-033: Widgets as quiet retention
- **Do:** a core-value widget (progress, streaks, next task) + Live Activities for real-time sessions.
- **Why:** glanceable presence beats push noise; widget adopters retain far better.
- **Apply when:** product has a metric worth glancing at daily.
- **Tags:** ios, widgets, retention, habit
- **Source:** [48Laws] L33

#### BP-034: Breadth of triggered email types
- **Do:** map email triggers to behaviors (signup, first core action, inactivity, trial ending) with distinct themes: value reinforcement, behavioral nudge, personalized opportunity, limited offer; send sequences, not blasts.
- **Why:** each funnel position needs a different message; one newsletter can't do lifecycle work.
- **Apply when:** email channel exists and the core funnel already converts.
- **Tags:** email, lifecycle, retention, conversion
- **Source:** [48Laws] L34

#### BP-035: Win-back at every lapse point
- **Do:** trigger tailored offers at cancellation, trial expiry, incomplete trials ("another trial", "save X% today"); the sooner after the lapse, the stronger.
- **Why:** the most under-used revenue lever; can add 10-25% to bottom line.
- **Apply when:** any churn/offboarding flow exists.
- **Tags:** winback, lifecycle, revenue, retention
- **Source:** [48Laws] L35

#### BP-036: Post-exit conversion push
- **Do:** minutes after a new user's first exit without trial, push a conversion offer deep-linking to a discount paywall.
- **Why:** new users have peak intent; a nudge catches the distracted.
- **Apply when:** push permission granted early; new-user funnel.
- **Tags:** push, conversion, lifecycle
- **Source:** [48Laws] L36

#### BP-037: Repeat the offer next day
- **Do:** if the first conversion push didn't land, send the same (or lightly tweaked) offer a day later, short and reminder-toned.
- **Why:** people forget; repetition captures the merely-distracted.
- **Apply when:** after BP-036 or any unanswered offer.
- **Tags:** push, conversion, lifecycle
- **Source:** [48Laws] L37

#### BP-038: Reminders tied to real usage cadence
- **Do:** identify the product's natural frequency and time reminders to it (morning for wellness, after-work for productivity).
- **Why:** aligned with user expectations — the only push users thank you for.
- **Apply when:** habit/recurring-use products.
- **Tags:** push, habit, retention, engagement
- **Source:** [48Laws] L38

#### BP-039: Lifecycle marketing last, funnel first
- **Do:** fix product conversion and onboarding before investing in lifecycle tooling/people; expect ~10% revenue ceiling from lifecycle and budget accordingly; start with simple product-triggered messages.
- **Why:** most conversions happen day 0; campaigns amplify a funnel, they don't fix one.
- **Apply when:** prioritizing growth investments.
- **Tags:** lifecycle, analytics, revenue, testing
- **Source:** [48Laws] L39

### Analytics, segmentation & testing

#### BP-040: Specific activation metric
- **Do:** define activation as a concrete early behavior ("2 core actions in week 1") that is meaningful (tied to promised value), early, and predictive of retention — never vague "onboarded".
- **Why:** you can only optimize what predicts value.
- **Apply when:** setting up analytics; before any funnel optimization.
- **Tags:** analytics, activation, insight
- **Source:** [48Laws] L40

#### BP-041: Aha is a sequence, not a moment
- **Do:** map setup moments → aha moment → habit moments; make onboarding walk that path: explain why each step matters, reward progress, cut steps that don't lead to aha.
- **Why:** best-converting apps engineer the sequence instead of hoping for one big moment; deliver value AND make the user notice they received it.
- **Apply when:** designing onboarding/activation; defining journeys.
- **Tags:** activation, onboarding, analytics, habit
- **Source:** [48Laws] L41

#### BP-042: Validate activation by correlation
- **Do:** cohort-split by candidate event completion, compare retention AND revenue; for subscription apps validate against paid renewals per plan, not any retention metric; too little data → qualitative research instead.
- **Why:** an activation metric that doesn't predict renewals optimizes the wrong thing.
- **Apply when:** after drafting an activation metric (BP-040).
- **Tags:** analytics, activation, segmentation, insight
- **Source:** [48Laws] L42

#### BP-043: Ask "How did you hear about us?"
- **Do:** HDYHAU question later in onboarding (after key actions), joinable with analytics; compare self-reported vs attributed sources; wording of options changes distributions a lot — write carefully.
- **Why:** post-ATT attribution is imperfect; self-report reveals undercounted high-LTV channels.
- **Apply when:** meaningful acquisition spend; onboarding can absorb one more question.
- **Tags:** analytics, attribution, insight, onboarding
- **Source:** [48Laws] L43

#### BP-044: Rigorous A/B tests
- **Do:** pre-calc sample size and duration from baseline + minimum detectable effect; one variable per test; no early stopping even at significance; consistent random assignment; validate tracking before launch. Checklist: hypothesis, sample size, single variable, tracking, schedule.
- **Why:** everything else produces noise dressed as wins.
- **Apply when:** every experiment.
- **Tags:** testing, analytics, insight
- **Source:** [48Laws] L44

#### BP-045: KPIs by segment, never averages
- **Do:** break retention/conversion/ARPU/renewal by platform, geo, attribution source, zero-party answers, behavioral segments; target experiments at underperformers.
- **Why:** averages hide both problems and wins (18% average can be 23% UK / 13% DE).
- **Apply when:** any KPI review or dashboard design.
- **Tags:** analytics, segmentation, insight
- **Source:** [48Laws] L45

#### BP-046: Cohorts to isolate change
- **Do:** weekly/monthly install cohorts; compare retention curves across product updates and campaigns; look at drop-off patterns, not just totals.
- **Why:** without cohorts you can't tell whether a change moved anything.
- **Apply when:** measuring impact of releases/campaigns over time.
- **Tags:** analytics, segmentation, insight, testing
- **Source:** [48Laws] L46

#### BP-047: Segment A/B results for hidden wins
- **Do:** never read tests as binary; segment results by device, geo, onboarding answers, activation level; roll out variants only to segments that benefit.
- **Why:** a flat overall result can hide a strong lift in one segment.
- **Apply when:** analyzing any completed test (esp. "no difference" ones).
- **Tags:** testing, segmentation, analytics, insight
- **Source:** [48Laws] L47

#### BP-048: Behavior overrides stated preferences
- **Do:** record stated goals early, track actual usage, reassign segments when behavior diverges; refresh recommendations and messaging from the evolving segment.
- **Why:** stale zero-party personalization ends up contradicting what users actually do.
- **Apply when:** personalization runs on onboarding answers for more than a few weeks.
- **Tags:** personalization, segmentation, analytics, retention
- **Source:** [48Laws] L48
