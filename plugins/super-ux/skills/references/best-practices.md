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
  `lifecycle` `winback` `analytics` `testing` `checkout` `navigation`
- **Mechanism:** `personalization` `social-proof` `commitment` `scarcity`
  `anchoring` `friction-reduction` `habit` `reward` `segmentation`
  `attribution` `activation` `feedback` `error-recovery`
- **Domain:** `subscription-app` `mobile` `ios` `android` `web` `freemium`
  `email` `push` `widgets` `voice` `ai-chat` `forms`
- **Channel of effect:** `conversion` `engagement` `trust` `revenue`
  `insight` `accessibility` `performance`
- **Visual craft:** `typography` `color` `layout` `readability` `dark-mode`
  `visual-hierarchy` `microcopy`

## Practices

Source key: **[48Laws]** = "48 Laws of Subscription App Success" (Botsi,
2025); **[HIG]** = Apple Human Interface Guidelines (2025, Liquid Glass era);
**[M3]** = Material Design 3 / M3 Expressive (Google, 2025); **[NNg]** =
Nielsen Norman Group research; **[Baymard]** = Baymard Institute large-scale
usability testing (2025); **[WCAG]** = WCAG 2.2 (W3C, Level AA); **[webdev]**
= web.dev Core Web Vitals; **[VUI]** = converged voice-interface guidance
(Amazon/Google conversation-design checklists, 2024–2026); **[RC25]** =
RevenueCat State of Subscription Apps 2025 (75k+ apps, $10B revenue);
**[PLG25]** = OpenView / ProductLed 2025 SaaS benchmarks; **[ASO25]** =
converged ASO industry guidance 2025 (AppTweak/AppFollow/asomobile);
**[Type]** = converged typography research (Baymard line-length studies,
USWDS, Bringhurst, Dyson & Haselgrove reading-speed research).

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

### Mobile interfaces

#### BP-049: Primary actions in the thumb zone
- **Do:** put primary destinations and actions in a bottom tab bar (3–5 items, icon + label); keep destructive/rare actions out of the easy-reach zone.
- **Why:** one-handed grip reaches bottom-center comfortably, top corners poorly (Hoober's grip research); bottom placement cuts interaction cost.
- **Apply when:** any mobile app navigation or primary-action placement.
- **Tags:** mobile, navigation, friction-reduction, engagement
- **Source:** [NNg]/[M3]/[HIG]

#### BP-050: Tap targets — platform sizes, WCAG floor
- **Do:** 44×44 pt (iOS) / 48×48 dp (Android) for interactive elements; never below 24×24 CSS px or equivalent spacing (WCAG 2.2 SC 2.5.8, Level AA).
- **Why:** small targets cause mis-taps and are an accessibility failure, not a style choice.
- **Apply when:** every interactive element; audits check the floor.
- **Tags:** mobile, web, accessibility, friction-reduction
- **Source:** [HIG]/[M3]/[WCAG]

#### BP-051: Never gesture-only for critical actions
- **Do:** gestures are accelerators, not the only path: every gesture-reachable action has a visible alternative; gesture hints (chevrons, swipe affordances) where gestures matter.
- **Why:** gestures are invisible — users must know, remember, and execute them; hidden-only interactions kill discoverability.
- **Apply when:** swipe-to-delete, pull-to-refresh, long-press menus, custom gestures.
- **Tags:** mobile, navigation, friction-reduction, accessibility
- **Source:** [NNg]

#### BP-052: Visible navigation beats hidden
- **Do:** expose primary navigation (tabs, visible labels); hamburger/overflow menus only for secondary content.
- **Why:** NN/g repeatedly shows hidden navigation drops content discoverability — users assume unseen features don't exist.
- **Apply when:** information architecture of any app or site.
- **Tags:** mobile, web, navigation, engagement, insight
- **Source:** [NNg]

#### BP-053: Follow the platform's current design language
- **Do:** iOS: clarity/deference/depth, floating adaptive controls, concentric rounded geometry (Liquid Glass era); Android: M3 Expressive — containment in rounded surfaces to group related elements, spring-based motion for feedback, emphasized type scale for hierarchy. Deviate only where the job demands it.
- **Why:** platform-native patterns are what users already know (Jakob's law), and OS-level components carry accessibility/motion behavior for free.
- **Apply when:** building or restyling native mobile UI.
- **Tags:** mobile, ios, android, trust, engagement
- **Source:** [HIG]/[M3]

#### BP-054: Motion as feedback, not decoration
- **Do:** animate to confirm actions, show state changes, and direct attention (spring/physical motion, ≤300ms for common transitions); honor reduced-motion settings.
- **Why:** motion that communicates status supports PRN-01; motion that merely decorates adds latency and vestibular problems.
- **Apply when:** any transition/animation decision.
- **Tags:** mobile, web, feedback, accessibility, engagement
- **Source:** [M3]/[HIG]

### Web apps, forms & performance

#### BP-055: Minimize form fields, ask only what the job needs
- **Do:** cut every field not required to complete the job; single-column layout; sensible input types and autocomplete attributes.
- **Why:** checkout complexity alone makes ~18% of users abandon; each field is friction with measurable cost.
- **Apply when:** any form — signup, checkout, settings.
- **Tags:** forms, web, mobile, checkout, friction-reduction, conversion
- **Source:** [Baymard]

#### BP-056: Guest path first, account later
- **Do:** make guest checkout/usage the most prominent option; offer account creation AFTER the job is done (one tap, data already collected).
- **Why:** forced account creation is a top abandonment cause; half of e-commerce sites still bury the guest option.
- **Apply when:** any flow where an account is not strictly required to deliver value.
- **Tags:** checkout, forms, conversion, friction-reduction, web
- **Source:** [Baymard]

#### BP-057: Automate address & location input
- **Do:** autocomplete address lookup; autodetect city/region from postal code; never make users type what the system can infer.
- **Why:** majority of mobile sites still lack it; typing structured data on mobile is error-prone friction.
- **Apply when:** any address/location collection.
- **Tags:** forms, checkout, mobile, friction-reduction, conversion
- **Source:** [Baymard]

#### BP-058: Respond within perception budgets
- **Do:** visible response to any interaction ≤200ms (INP "good"); skeletons/progress for longer work; optimistic UI where safe.
- **Why:** INP is measured on every interaction — slow feedback reads as "broken", and Core Web Vitals gate search visibility at the 75th percentile.
- **Apply when:** web apps and hybrid views; audits treat >200ms uncued waits as findings.
- **Tags:** web, performance, feedback, conversion
- **Source:** [webdev]

#### BP-059: WCAG 2.2 AA as the baseline, not the stretch goal
- **Do:** contrast ≥4.5:1 text, visible focus states, full keyboard paths, labels tied to inputs, target-size floor (BP-050), no info by color alone; test with a screen reader on key flows.
- **Why:** accessibility failures exclude users and are increasingly a legal exposure; retrofitting costs more than building in.
- **Apply when:** every scenario's UI elements; heuristic audits include it.
- **Tags:** web, mobile, accessibility, trust
- **Source:** [WCAG]

### Voice & conversational interfaces

#### BP-060: Tiered confirmations by risk
- **Do:** explicit confirmation only for sensitive/irreversible actions (payments, deletions, bookings); implicit short acknowledgement for routine commands; always an undo path.
- **Why:** confirming everything adds cognitive load; confirming nothing destroys trust exactly where errors are costly.
- **Apply when:** designing any voice or chat command set.
- **Tags:** voice, ai-chat, trust, error-recovery, friction-reduction
- **Source:** [VUI]

#### BP-061: Error recovery: say what was heard, offer the fix
- **Do:** on misrecognition, state plainly what the system understood, what went wrong, and one concrete way to fix it; constrained vocabulary for critical commands; context-specific help instead of generic "try again".
- **Why:** voice errors are invisible — without echoing the system's interpretation the user can't diagnose anything (PRN-09 applied to VUI).
- **Apply when:** every voice/chat error branch in flows and scenarios.
- **Tags:** voice, ai-chat, error-recovery, trust
- **Source:** [VUI]/[NNg]

#### BP-062: Support barge-in and interruption
- **Do:** let users interrupt TTS/long responses at any time; on interruption stop output immediately, checkpoint dialog state, and treat the interruption as the new intent.
- **Why:** forcing users to listen to the end violates user control (PRN-03); experienced users know what they want.
- **Apply when:** any spoken output longer than a short acknowledgement.
- **Tags:** voice, friction-reduction, engagement
- **Source:** [VUI]

#### BP-063: Design for deviation, not linear scripts
- **Do:** every dialog state accepts topic switches, corrections ("no, the other one"), and out-of-scope requests with graceful redirection; never dead-end on "I didn't understand".
- **Why:** NN/g finds linear-flow bots collapse the moment users deviate — and users always deviate.
- **Apply when:** conversation design for voice assistants and chatbots.
- **Tags:** voice, ai-chat, error-recovery, engagement
- **Source:** [NNg]

#### BP-064: Pair voice with visual state where a screen exists
- **Do:** on multimodal devices show what was recognized and what's happening on screen while speaking; voice for input speed, screen for confirmation and dense output (lists, comparisons).
- **Why:** speech is transient and low-bandwidth for output; the screen carries recognition transparency and recall.
- **Apply when:** voice features in mobile/web apps, smart displays.
- **Tags:** voice, mobile, web, feedback, trust
- **Source:** [VUI]

#### BP-065: Keep spoken turns short, latency cued
- **Do:** one idea per spoken turn, front-load the answer; sub-150ms audio cues to mark turn start/end; fill unavoidable processing gaps with brief, honest status.
- **Why:** users can't skim audio — long turns overload working memory; uncued silence reads as failure.
- **Apply when:** writing any TTS/agent response copy.
- **Tags:** voice, feedback, performance, engagement
- **Source:** [VUI]

#### BP-066: Show AI limits and control honestly
- **Do:** in AI-driven interfaces state capability boundaries up front, expose what context the system used, make output editable/regenerable, and keep a human-visible way to verify consequential results.
- **Why:** trust in conversational AI hinges on context transparency, user control, and clear authority boundaries — overclaiming produces one bad surprise and churn.
- **Apply when:** any LLM/assistant feature surface.
- **Tags:** ai-chat, trust, error-recovery, insight
- **Source:** [NNg]

### Monetization models & conversion economics

#### BP-067: Choose the monetization model with data, not ideology
- **Do:** decide hard paywall vs freemium vs hybrid explicitly, in the foundation: hard paywalls convert downloads-to-paid ~5× better than freemium (12.1% vs 2.2% median) with similar year-one retention; freemium wins only when free users feed growth loops (virality, content, network) or ads.
- **Why:** the model dictates every downstream flow; picking freemium "to be nice" without a growth loop just burns conversion.
- **Apply when:** foundation stage of any monetized product; challenge inherited models during Improve.
- **Tags:** pricing, paywall, freemium, revenue, conversion, subscription-app
- **Source:** [RC25]

#### BP-068: Hybrid monetization beats subscription-only
- **Do:** offer consumables, one-time unlocks, or lifetime alongside subscriptions where the product allows; route subscription-averse segments to one-time purchases (see BP-028).
- **Why:** 2025 data shows apps mixing purchase types earn and retain more; subscription-only is fading.
- **Apply when:** revenue design for apps with separable value units (credits, packs, features).
- **Tags:** pricing, revenue, subscription-app, segmentation
- **Source:** [RC25]

#### BP-069: Show the paywall in the first session
- **Do:** paywall appears during onboarding, after the value promise is established — not hidden behind days of usage. Trial starts overwhelmingly happen on day 0; design the first session as the primary conversion surface.
- **Why:** >80% of trial starts occur immediately upon download; the "let them fall in love first" strategy mostly means never showing the offer.
- **Apply when:** onboarding + paywall flow design (with BP-002/BP-005/BP-010 priming).
- **Tags:** onboarding, paywall, conversion, subscription-app
- **Source:** [RC25]

#### BP-070: Trial design: friction and length are levers
- **Do:** pick trial type consciously: opt-out (card required) converts ~31% vs opt-in ~9% but suppresses volume; longer trials (17–32 days) show the highest trial-to-paid (~46%) ONLY when paired with engagement during the trial — extension without activation does nothing.
- **Why:** trial parameters are conversion levers with measured trade-offs, not defaults to copy.
- **Apply when:** designing or A/B-testing any trial.
- **Tags:** pricing, paywall, testing, conversion, subscription-app
- **Source:** [RC25]/[PLG25]

#### BP-071: The first 14 days decide conversion
- **Do:** concentrate activation nudges, value proof, and conversion offers in days 0–14; ~60% of SaaS conversions happen there, ~80% by day 30. After day 30, switch to winback economics (BP-035).
- **Why:** effort spent on late-funnel persuasion has a hard data ceiling.
- **Apply when:** lifecycle design, email/push sequencing, trial length choice.
- **Tags:** lifecycle, activation, conversion, retention
- **Source:** [PLG25]

#### BP-072: Activation before monetization pressure
- **Do:** define and instrument the activation metric (BP-040) and drive users to it BEFORE heavy upsell pressure; winners hold 60%+ activation. Monetization prompts on unactivated users → discounts and churn.
- **Why:** paying users who never activated refund and cancel; activation is the strongest conversion predictor across models.
- **Apply when:** sequencing onboarding steps vs monetization asks.
- **Tags:** activation, onboarding, conversion, retention, analytics
- **Source:** [PLG25]

#### BP-073: Freemium boundary = value metric, visibly metered
- **Do:** gate the paid tier on the product's value metric (projects, seats, usage, exports — what scales with the job), keep the free tier genuinely useful for the core job at small scale, and show consumption progress (e.g. "2/3 free projects") BEFORE the wall hits.
- **Why:** median freemium→paid is only 2.6% — the boundary placement is the whole game; invisible limits convert as anger, visible ones as anticipation.
- **Apply when:** splitting free vs paid functionality; with BP-024/BP-025/BP-026 for surfacing.
- **Tags:** freemium, pricing, scarcity, conversion, trust
- **Source:** [PLG25]

#### BP-074: Upgrade prompts at the moment of hitting value limits
- **Do:** trigger the upgrade offer exactly when the user attempts the gated action (4th project, locked export), with the offer framed around finishing THAT job; one tap from limit to paywall to done.
- **Why:** intent peaks at the blocked action — contextual upgrade beats scheduled campaigns (BP-025 generalized with a trigger rule).
- **Apply when:** every gated feature's flow — the limit branch is a first-class flow edge, not a dead end.
- **Tags:** freemium, paywall, conversion, friction-reduction
- **Source:** [PLG25]/[48Laws]

### Store listing, ratings & acquisition coherence

#### BP-075: Store listing is the first screen of onboarding
- **Do:** treat the listing as part of the UX chain: 5–8 screenshots ordered benefit → USP → social proof → core scenarios; first 2 must work standalone (5–10 seconds of attention decide install); preview video where motion sells; A/B via store tools.
- **Why:** screenshots alone move page conversion 20–35%; the listing sets the expectation onboarding must then confirm.
- **Apply when:** any store-distributed product; audits compare listing promises vs actual first-session scenarios.
- **Tags:** onboarding, conversion, mobile, social-proof
- **Source:** [ASO25]

#### BP-076: Engineer the 4.0+ rating loop
- **Do:** ask for a rating only right after a success moment (goal completed, streak, aha) and never mid-task or after an error; intercept negatives first ("Enjoying? no → feedback form, yes → store prompt"); reply to reviews; fix top review complaints as UX findings.
- **Why:** below 4.0 acquisition stalls (90% of featured apps are 4.0+), and stores rank on rating + retention signals; the prompt moment decides the score.
- **Apply when:** every product with store ratings — the rating prompt is a scenario with its own flow, states, and timing rules.
- **Tags:** retention, trust, conversion, mobile, lifecycle
- **Source:** [ASO25]

#### BP-077: Ad-to-onboarding message coherence
- **Do:** the creative's promise, the store listing, and the first onboarding screens must tell one story: same benefit, same words, same visual; segment onboarding by acquisition source/campaign where volumes justify (with BP-043 HDYHAU to verify).
- **Why:** ROAS dies at the seams — a user sold "X" who lands in generic "welcome" churns before the paywall; funnel coherence is a UX property, not a marketing one.
- **Apply when:** any paid acquisition; audits check first-session scenarios against live creatives' promises.
- **Tags:** onboarding, attribution, conversion, revenue, trust
- **Source:** [ASO25]/[48Laws]

#### BP-078: Web-to-app funnels for owned conversion
- **Do:** where economics matter, run the quiz/onboarding + payment on the web BEFORE the store (web2app): full attribution, ~3–4% processing fees vs 15–30% IAP, flexible pricing/trials; app then starts already-paid with a login handoff scenario.
- **Why:** the highest-grossing subscription apps increasingly convert on web and use the app for delivery; store rules for external flows keep loosening (BP-030).
- **Apply when:** paid-acquisition-heavy products with LTV to protect; design the web funnel with the same scenario rigor as the app.
- **Tags:** onboarding, pricing, revenue, web, attribution, subscription-app
- **Source:** [RC25]/[48Laws]

### Visual design, typography & color

#### BP-079: Body text baseline: 16px / 1.5 / 45–75 CPL
- **Do:** body text ≥16px (or platform equivalent), line height ≥1.5× font size, measure 45–75 characters per line (target ~66; raise line height to 1.6–1.7 when lines run long); enforce via max-width on text containers.
- **Why:** eye-tracking and reading-speed research (Dyson & Haselgrove; Baymard) converge on this window — shorter lines break scanning rhythm, longer lines lose the return sweep.
- **Apply when:** any reading surface — articles, descriptions, settings copy, empty states.
- **Tags:** typography, readability, web, mobile, accessibility
- **Source:** [Type]

#### BP-080: One type system: ≤2 typefaces, consistent scale
- **Do:** one body face + optionally one display face; headings 1.3–1.6× of body per level on a fixed scale; hierarchy via size + weight + spacing, not via new fonts; define the scale once and reuse everywhere.
- **Why:** every extra face/size is a new visual rule the reader must learn; a consistent scale makes hierarchy legible pre-attentively.
- **Apply when:** any product; audits flag ad-hoc font sizes outside the scale.
- **Tags:** typography, visual-hierarchy, readability, trust
- **Source:** [Type]/[M3]/[HIG]

#### BP-081: Contrast floors, softened extremes
- **Do:** text contrast ≥4.5:1 (≥3:1 for ≥24px/bold ≥19px); avoid pure #000-on-#FFF for long reading — near-black on near-white reads softer at identical compliance; secondary text stays ≥4.5:1, "muted" is not an excuse.
- **Why:** WCAG floors are the legal/perceptual minimum; maximal harshness causes fatigue and halation for astigmatic readers.
- **Apply when:** every text/background pair, both themes.
- **Tags:** color, typography, accessibility, readability
- **Source:** [WCAG]/[Type]

#### BP-082: 60-30-10 palette, one scarce accent
- **Do:** ~60% dominant neutral, ~30% secondary, ~10% accent; ONE saturated accent reserved for primary actions and key states — the accent appears exactly where you want the eye to go; extend the palette with tints/shades of existing hues before adding new ones.
- **Why:** accent scarcity IS the visual hierarchy — an accent used everywhere ranks nothing; limited palettes read as intentional and calm.
- **Apply when:** defining or auditing any color system; audits flag accent-colored non-primary elements.
- **Tags:** color, visual-hierarchy, engagement, trust
- **Source:** [M3]/[HIG]

#### BP-083: Semantic colors are a contract
- **Do:** red = destructive/error, green = success, amber = warning, accent = action — assigned once, never repurposed (no red sale banners next to red delete buttons); meaning never carried by color alone (icon/label always present).
- **Why:** users build a color→meaning map in minutes; one violation poisons trust in every other color signal (and color-only fails color-blind users).
- **Apply when:** any state/feedback design; audits check for repurposed semantics.
- **Tags:** color, feedback, accessibility, trust, error-recovery
- **Source:** [M3]/[WCAG]

#### BP-084: Dark mode is a designed palette, not inversion
- **Do:** surfaces in dark gray (not pure black), depth via lighter-surface elevation; desaturate accents for dark backgrounds (saturated colors vibrate on dark); re-verify every contrast pair per theme; respect the OS theme by default.
- **Why:** inverted light palettes fail contrast and vibrate; tonal elevation replaces shadows that darkness eats.
- **Apply when:** any dark theme; audits run the contrast pass in both themes.
- **Tags:** color, dark-mode, accessibility, readability
- **Source:** [M3]/[HIG]

#### BP-085: Spacing system on a 4/8pt grid
- **Do:** all paddings, gaps, and sizes from one scale (multiples of 4/8); spacing encodes grouping — related elements sit measurably closer than unrelated ones (proximity beats borders); pick per-level spacing once, reuse everywhere.
- **Why:** a spacing system makes layouts feel coherent without anyone knowing why; proximity is the strongest free grouping signal (Gestalt).
- **Apply when:** every layout; audits flag off-scale one-off values.
- **Tags:** layout, visual-hierarchy, readability
- **Source:** [M3]/[HIG]

#### BP-086: Whitespace is hierarchy, density is a mode
- **Do:** generous space around the primary content/action; increase density only where the job is scanning many items (tables, lists) — and then be uniformly dense; never fill freed space with decoration.
- **Why:** space signals importance pre-attentively; mixed density reads as clutter even when aligned.
- **Apply when:** screen layout decisions, dashboard vs reading surfaces.
- **Tags:** layout, visual-hierarchy, readability, engagement
- **Source:** [Type]/[M3]

#### BP-087: One grid, honest alignment
- **Do:** single layout grid per screen; left-align body text (RTL-aware); center only short display lines; every element's edge aligns with something — no orphan offsets.
- **Why:** the eye detects misalignment faster than it reads; centered long text destroys the return sweep.
- **Apply when:** any layout; audits flag multi-grid screens and centered paragraphs.
- **Tags:** layout, typography, readability
- **Source:** [Type]

#### BP-088: Tabular figures for data
- **Do:** numbers in tables, timers, counters, and prices use tabular (monospaced-figure) variants and consistent decimal places; align numeric columns right.
- **Why:** proportional figures jitter as values change and misalign columns — comparison becomes work.
- **Apply when:** any numeric UI; dashboards, carts, timers.
- **Tags:** typography, readability, insight
- **Source:** [Type]

#### BP-089: Microcopy: verbs, sentence case, stable names
- **Do:** buttons say what happens ("Save changes", not "Submit"/"OK"); sentence case throughout; an action keeps one name across the whole flow (button "Publish" → toast "Published"); labels label, examples demonstrate — one job per string.
- **Why:** interface vocabulary is navigation signage; renamed actions and vague verbs force re-reading and erode confidence.
- **Apply when:** every user-facing string; part of scenario UI-elements review.
- **Tags:** microcopy, readability, trust, friction-reduction
- **Source:** [NNg]/[HIG]

#### BP-090: Subtract decoration until only signal remains
- **Do:** separate content with spacing or background shifts before reaching for borders; one separation device per boundary; cut ornaments that encode nothing (gratuitous gradients, shadows, dividers stacked on gaps).
- **Why:** every visual element competes for attention; decoration that carries no information taxes the elements that do (PRN-08 applied to pixels).
- **Apply when:** visual polish passes and audits — count separation devices per boundary.
- **Tags:** layout, visual-hierarchy, readability, engagement
- **Source:** [M3]/[NNg]
