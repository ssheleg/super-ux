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
  `lifecycle` `winback` `analytics` `testing` `checkout` `billing` `cancel`
  `navigation`
- **Mechanism:** `personalization` `social-proof` `commitment` `scarcity`
  `anchoring` `friction-reduction` `habit` `reward` `segmentation`
  `attribution` `activation` `feedback` `error-recovery` `gamification`
  `trend-governance` `virality` `referral`
- **Domain:** `subscription-app` `mobile` `ios` `android` `web` `freemium`
  `landing-page` `web2app` `email` `push` `widgets` `voice` `ai-chat` `forms`
  `auth` `responsive` `figma` `design-system` `handoff` `maintainability`
- **Channel of effect:** `conversion` `engagement` `trust` `revenue`
  `insight` `accessibility` `performance` `page-weight` `legal`
- **Visual craft:** `typography` `color` `layout` `readability` `dark-mode`
  `visual-hierarchy` `microcopy` `motion`
- **Components:** `component` `control` `navigation-ui` `dialog` `forms-ui`
  `selection` `feedback-ui`

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
USWDS, Bringhurst, Dyson & Haselgrove reading-speed research); **[CRO26]** =
converged web-funnel and billing benchmarks 2026 (Baymard checkout research,
ChartMogul/Paddle trial and failed-payment data, landing- and pricing-page
A/B aggregations); **[W2A26]** = converged web2app practitioner guidance 2026
(RevenueCat/Adapty/Superwall funnel benchmarks; Apple and Google storefront
policy after the April 2025 US anti-steering ruling); **[WebAIM]** = WebAIM
Million 2025 (automated accessibility scan of the top 1,000,000 home pages);
**[HTTPArchive]** = HTTP Archive / CrUX 2025–26 field data (page weight,
Core Web Vitals, font and viewport share, incl. Statcounter resolution
share); **[CSq]** = digital-experience benchmarks 2025 (Contentsquare
session/frustration data, FullStory rage-click reporting, PwC experience
survey); **[A11yLaw]** = accessibility-compliance reporting 2025 (Level
Access State of Digital Accessibility, UsableNet litigation tracking, the
European Accessibility Act in force since June 2025); **[WSG]** = W3C Web
Sustainability Guidelines 1.0; **[SDT]** = self-determination-theory
motivation research and published gamification post-mortems; **[NIST]** =
NIST SP 800-63B rev. 4, Digital Identity Guidelines (August 2025);
**[Viral26]** = converged virality and referral benchmarks 2026 (B2B SaaS
K-factor distributions, viral-cycle timing, referral-program industry
reports).

Figures from `[CRO26]`/`[W2A26]`/`[CSq]`/`[HTTPArchive]` are industry
aggregates, not laws: they justify the *shape* of a practice, and the
product's own numbers overrule them the moment they exist. Vendor-published
survey figures (design-tool and marketing-suite "state of" reports) are
treated as directional only and never as a practice's sole justification.

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
- **Apply when:** any transition/animation decision; the system behind it — duration/easing tokens, reduced motion, scroll-driven surfaces — is BP-130..132.
- **Tags:** mobile, web, feedback, accessibility, engagement, motion
- **Source:** [M3]/[HIG]

### Web apps, forms & performance

#### BP-055: Minimize form fields, ask only what the job needs
- **Do:** cut every field not required to complete the job; single-column layout; sensible input types and autocomplete attributes.
- **Why:** checkout complexity alone makes ~18% of users abandon; each field is friction with measurable cost, and checkout-design work measures among the highest-yield UX changes there is (Baymard puts a well-executed rebuild at roughly a third more completed orders).
- **Apply when:** any form — signup, checkout, settings; what to ask *later* instead of now is BP-143.
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
- **Apply when:** web apps and hybrid views; audits treat >200ms uncued waits as findings. What you ship over the wire to make that budget reachable is BP-133.
- **Tags:** web, performance, feedback, conversion
- **Source:** [webdev]

#### BP-059: WCAG 2.2 AA as the baseline, not the stretch goal
- **Do:** contrast ≥4.5:1 text, visible focus states, full keyboard paths, labels tied to inputs, target-size floor (BP-050), no info by color alone; test with a screen reader on key flows.
- **Why:** accessibility failures exclude users, and they are the norm rather than the exception — automated scans of the top million home pages fail ~95% of them, on a small number of repeating defects. The legal side is no longer hypothetical either (BP-138).
- **Apply when:** every scenario's UI elements; heuristic audits include it. How it fails in practice, and what actually fixes it: BP-136..138.
- **Tags:** web, mobile, accessibility, trust
- **Source:** [WCAG]/[WebAIM]

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
- **Do:** decide hard paywall vs freemium vs hybrid explicitly, in the foundation: hard paywalls convert downloads-to-paid ~5× better than freemium (12.1% vs 2.2% median) with similar year-one retention; freemium wins only when free users feed a growth loop (BP-147..151 — virality, content, network) or ads.
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
- **Apply when:** any paid acquisition; audits check first-session scenarios against live creatives' promises. Segmenting by what the user told you, over time, is BP-143/BP-144.
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
- **Why:** WCAG floors are the legal/perceptual minimum; maximal harshness causes fatigue and halation for astigmatic readers. This is also the single most common accessibility defect in the field — roughly four out of five scanned home pages carry low-contrast text — so it is the first thing to check, not the last.
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

### Figma structure & design-file maintenance

Full navigation/build guide: [figma-structure.md](figma-structure.md).
Source key here: **[FigBP]** = Figma official Best Practices;
**[FigLearn]** = Figma Learn help center; **[DSC]** = Design Systems
Collective (Figma Variables playbook, 2025/26); **[ZH]** = zeroheight
design-system org guides.

#### BP-091: Cover + index as the first two pages
- **Do:** page 1 is a Cover (file name, status, owner, last-updated) built as a component; page 2 is an Index mapping every subsequent page to its flow/feature. Everything else follows.
- **Why:** a file opens on its cover — the agent (and humans) identify and navigate it at a glance instead of scanning frames.
- **Apply when:** every Figma file the project maintains.
- **Tags:** figma, design-system, maintainability, handoff
- **Source:** [FigBP]/[ZH]

#### BP-092: One page per flow/feature, named to match the chain
- **Do:** group frames by flow or feature, one Figma page each, page name carrying the `FLW-ID`/feature (e.g. `FLW-01 · Create project`); keep drafts on a separate "Scratch" page or file so the working file stays lean.
- **Why:** page structure that mirrors `flows.md` lets an agent jump straight to the right page from a flow ID; draft clutter slows file load and confuses navigation.
- **Apply when:** organizing any multi-flow file.
- **Tags:** figma, maintainability, handoff
- **Source:** [FigBP]/[ZH]/[loopstudio]

#### BP-093: Frame names keyed to SCR-ID and state
- **Do:** name each screen frame `SCR-NN/<Screen>/<state>` (slash-nested), e.g. `SCR-01/Welcome/empty`; one frame per screen-state that matters. This is the exact key stored in `screens.md`.
- **Why:** deterministic 1:1 mapping between the `screens.md` States table and Figma frames — the agent finds and updates the right frame without guessing, and drift becomes checkable.
- **Apply when:** every screen mockup in a super-ux project (the anti-confusion backbone).
- **Tags:** figma, maintainability, handoff, design-system
- **Source:** [FigBP] + super-ux contract

#### BP-094: Purpose-based, code-matched naming (not appearance)
- **Do:** name components and variables by role, not looks: `button/primary` not `button/blue`, `color/background/subtle` not `color/gray-100`; match the name developers use in code (`size=small` in Figma == `size="small"` in code).
- **Why:** appearance names rot the moment the value changes; shared vocabulary removes the biggest design-to-code handoff friction.
- **Apply when:** naming any component, variant, or token.
- **Tags:** figma, design-system, handoff, maintainability
- **Source:** [DSC]/[FigLearn]/[ZH]

#### BP-095: Variables as tokens — primitive → semantic → component
- **Do:** define primitive values, alias them to semantic tokens, then reference semantics from components; group into named collections (color, spacing, typography); use modes for light/dark and density. Never hardcode a raw value on a component.
- **Why:** a three-tier token graph is what lets one change propagate everywhere and what maps cleanly to code tokens; raw values scattered on components can't be themed or synced.
- **Apply when:** building or maintaining the design system layer.
- **Tags:** figma, design-system, dark-mode, maintainability
- **Source:** [DSC]/[FigLearn]

#### BP-096: Variants for states of one object; separate components for different objects
- **Do:** use variants to hold states/sizes of a single component (button: default/hover/active/disabled/loading); make a new component when it's a different object. Every interactive component ships hover, active, disabled, loading, and error variants, not just default.
- **Why:** over-merged variants become unusable matrices; missing state variants mean the states never get designed — and PRN-01/PRN-09 fail in code.
- **Apply when:** building any component with states.
- **Tags:** figma, design-system, maintainability
- **Source:** [FigLearn]/[artofstyleframe]

#### BP-097: Auto layout on every container
- **Do:** wrap every frame and component in auto layout with hug/fill sizing, explicit padding and gap from spacing tokens; avoid absolute positioning except for genuine overlays.
- **Why:** auto layout makes components responsive and content-resilient, and produces structure that translates to real layout code; hand-placed frames break on any content change.
- **Apply when:** every frame and component.
- **Tags:** figma, design-system, maintainability, layout
- **Source:** [FigLearn]/[devot]

#### BP-098: Build on the existing library, don't reinvent
- **Do:** before creating anything, pull the project's Figma library / design system (`get_libraries`/`search_design_system`) and use its components and tokens; detach or fork only with a recorded reason.
- **Why:** parallel one-off components fragment the system and guarantee drift between screens and between design and code.
- **Apply when:** the project has any existing library; every new screen.
- **Tags:** figma, design-system, maintainability, handoff
- **Source:** [FigBP]/[ZH]

#### BP-099: Layer hygiene — name what matters, group meaningfully
- **Do:** rename layers that carry meaning (nav, primary-cta, error-text); group by structure not by accident; delete hidden/orphan layers; keep the layer tree shallow. Skip renaming purely decorative leaves.
- **Why:** an agent (and Figma AI / code-gen) reads the layer tree — meaningful names produce meaningful code and let others find things; "Frame 47 › Group 12" is noise.
- **Apply when:** before handoff and in maintenance passes.
- **Tags:** figma, maintainability, handoff
- **Source:** [FigLearn]/[FigBP]

#### BP-100: One naming convention + a governance owner
- **Do:** agree ONE naming/structure convention up front (pages, frames, components, tokens) and record it in `screens.md` Design system; name an owner responsible for keeping the file and the code tokens in sync. Start simple; evolve only when the team feels friction.
- **Why:** the best structure is the one the team actually keeps; convention without an owner rots, and over-engineered structure fails from complexity.
- **Apply when:** setting up the design file; revisited each audit.
- **Tags:** figma, design-system, maintainability, handoff
- **Source:** [FigBP]/[DSC]/[ZH]

### Components & controls (when to use what)

Decision reference + platform rules: [component-guidelines.md](component-guidelines.md).
Source key: **[HIG]** Apple Human Interface Guidelines; **[M3]** Material
Design 3; **[APG]** W3C ARIA Authoring Practices Guide; **[GOVUK]** GOV.UK
Design System.

#### BP-101: Use the platform's standard component before inventing one
- **Do:** reach for the host system's component of record (HIG on Apple, M3 on Android, the project's design system / ARIA APG patterns on web) before building a custom control.
- **Why:** standard components ship with accessibility, all interaction states, and motion behavior that a custom one silently omits (Jakob's law, PRN-14).
- **Apply when:** specifying any control; a custom control needs an explicit reason and equivalent keyboard/SR behavior.
- **Tags:** component, control, accessibility, maintainability
- **Source:** [HIG]/[M3]/[APG]

#### BP-102: One primary action, never destructive-as-primary
- **Do:** exactly one visually dominant primary action per screen, assigned to the most likely choice; a destructive action never gets the primary role even when it's the likely tap — style it destructive.
- **Why:** two primaries = no primary; a destructive primary invites costly mis-taps.
- **Apply when:** every screen with actions.
- **Tags:** control, visual-hierarchy, error-recovery
- **Source:** [HIG]/[M3]

#### BP-103: Radios for one-of-few, checkboxes for any-of, select for one-of-many
- **Do:** 2–5 visible mutually-exclusive options → radio group; zero-or-more → checkboxes; 6+ exclusive → select or searchable combobox. Add a hint stating how many can be picked; don't rely on shape alone.
- **Why:** matching the control to the selection cardinality is what makes the choice legible; users don't infer cardinality from radio-vs-checkbox shape (GOV.UK).
- **Apply when:** any selection input.
- **Tags:** selection, forms-ui, friction-reduction
- **Source:** [GOVUK]/[M3]

#### BP-104: Avoid select boxes where a small visible set works
- **Do:** prefer visible radios/segmented controls to a dropdown when the option set is small; reserve selects for genuinely long lists.
- **Why:** dropdowns hide choices and are hard for many users (motor, screen-magnifier, cognitive) — GOV.UK's field data.
- **Apply when:** ≤5 options, or whenever choices benefit from being seen.
- **Tags:** selection, forms-ui, accessibility
- **Source:** [GOVUK]

#### BP-105: Switch = immediate; checkbox = staged
- **Do:** use a switch for a setting that takes effect instantly; a checkbox for options confirmed on submit. Don't mix the two metaphors in one form.
- **Why:** the control signals when the change happens — a switch that needs a Save button, or a checkbox that acts instantly, breaks the user's model.
- **Apply when:** any toggle.
- **Tags:** control, selection, feedback-ui
- **Source:** [HIG]/[M3]

#### BP-106: Action sheet for action-choices, alert for unexpected confirms
- **Do:** action sheet = choices related to an action the user initiated; alert = unexpected info or a destructive confirm with no extra choices. Use sheets sparingly.
- **Why:** conflating them either buries confirmations or interrupts needlessly.
- **Apply when:** mobile choice/confirm moments.
- **Tags:** dialog, control, error-recovery
- **Source:** [HIG]

#### BP-107: Action sheets stay short, destructive placed safely
- **Do:** ≤4 buttons including Cancel (aim ≤3 choices + Cancel); style the destructive choice and place it where it's noticed but NOT adjacent to the likely tap.
- **Why:** long sheets can't be scanned at once; a destructive button next to the common one gets fat-fingered.
- **Apply when:** any action sheet / bottom-sheet menu.
- **Tags:** dialog, control, error-recovery
- **Source:** [HIG]

#### BP-108: Modal dialogs — trap focus, ESC closes, return focus
- **Do:** `role="dialog"` + `aria-modal="true"`; background inert; focus moves into the dialog on open, is trapped while open, returns to the trigger on close; ESC closes; Tab cycles within.
- **Why:** without focus management a modal is unusable by keyboard/SR users and leaks interaction to the inert background (APG).
- **Apply when:** any blocking overlay on web.
- **Tags:** dialog, accessibility, control
- **Source:** [APG]

#### BP-109: Don't stack modals; don't modal what a disclosure handles
- **Do:** one modal at a time; show/hide secondary content inline with a disclosure/accordion instead of a dialog.
- **Why:** stacked modals trap and disorient; over-modaling turns quick reveals into interruptions (PRN-11 progressive disclosure).
- **Apply when:** reveal/subtask decisions.
- **Tags:** dialog, component, friction-reduction
- **Source:** [APG]/[M3]

#### BP-110: Combobox — correct roles + full keyboard
- **Do:** `role="combobox"` owning a textbox; popup listbox/grid/tree/dialog with matching `aria-haspopup`; arrow keys move, Enter selects, ESC closes; the field reflects the selection.
- **Why:** an autocomplete without the APG roles/keys is invisible to assistive tech and unusable without a mouse.
- **Apply when:** any autocomplete/typeahead/searchable select.
- **Tags:** control, forms-ui, accessibility
- **Source:** [APG]

#### BP-111: Bottom nav for phones, rail for tablets, sized right
- **Do:** bottom navigation bar for compact widths (<600dp), 3–5 destinations, at the bottom; navigation rail for 600–839dp, 3–7 items. Primary destinations always visible.
- **Why:** matches thumb reach (BP-049) and window size; the wrong nav for the width wastes reach or space.
- **Apply when:** responsive app navigation.
- **Tags:** navigation-ui, mobile, component
- **Source:** [M3]

#### BP-112: FAB only for the screen's single most important action
- **Do:** use a FAB for the one primary create/compose action; a FAB menu (not stacked mini-FABs) for a few related actions; extended FAB when a label adds clarity.
- **Why:** the FAB's prominence is a budget — more than one destroys the "this is THE action" signal.
- **Apply when:** mobile screens with a dominant creative action.
- **Tags:** control, navigation-ui, mobile
- **Source:** [M3]

#### BP-113: Memorable dates as 3 fields, browsable dates as a picker
- **Do:** birthdays / known dates → a 3-field day/month/year text input; dates the user must look up or browse → a date picker.
- **Why:** forcing a calendar widget for a birthday is slow and error-prone; free-text parsing for a browsed date is fragile (GOV.UK).
- **Apply when:** any date entry — pick by whether the date is recalled or discovered.
- **Tags:** forms-ui, control, friction-reduction
- **Source:** [GOVUK]

#### BP-114: Transient feedback in toasts, required actions never only in a toast
- **Do:** toast/snackbar for brief, non-blocking confirmations; anything the user must act on goes in persistent UI or a dialog.
- **Why:** toasts auto-dismiss — a required action hidden there is missed (PRN-01 vs PRN-06).
- **Apply when:** success/undo/status messaging.
- **Tags:** feedback-ui, component, error-recovery
- **Source:** [M3]/[HIG]

#### BP-115: Every interactive component ships all its states
- **Do:** provide default, hover, focus (visible ring), active/pressed, disabled (reason discoverable), loading (async), error (fallible), selected (where applicable) — in code and as Figma variants.
- **Why:** missing states are exactly where system-status (PRN-01) and error-recovery (PRN-09) silently fail; "default only" is an unfinished control.
- **Apply when:** every control; the audit checks the state set.
- **Tags:** component, control, accessibility, feedback-ui
- **Source:** [M3]/[HIG]/[APG]

### Web funnels — landing, pricing, checkout, billing

The web-to-web money path: traffic → landing → signup → checkout → recurring
billing → cancel. Each step below is a flow with states and failure branches,
not a marketing page; treat them with the same scenario rigor as in-product
screens.

#### BP-116: One promise from ad to landing to first product screen
- **Do:** the ad headline, the landing hero, the signup screen, and the first in-product screen repeat the same benefit in the same words; one landing per campaign promise, never one landing for all traffic.
- **Why:** the relevance gap between ad and page is the most common cause of below-median landing conversion — the web twin of BP-077, and it sets CAC before any UI detail can.
- **Apply when:** any paid or campaign traffic entering a web funnel.
- **Tags:** landing-page, attribution, conversion, trust, web
- **Source:** [CRO26]/[ASO25]

#### BP-117: One page, one job — single CTA, proof at the decision point
- **Do:** one primary action per landing page, repeated down the page; place social proof (logos, numbers, testimonials) beside each CTA rather than only in a section at the bottom; secondary links must not compete with the CTA.
- **Why:** a large share of visitors never scroll to a bottom testimonial block, so proof placed there never enters the decision; competing CTAs split intent instead of stacking it.
- **Apply when:** every marketing or landing page inside a conversion funnel.
- **Tags:** landing-page, social-proof, visual-hierarchy, conversion, web
- **Source:** [CRO26]/[NNg]

#### BP-118: Pricing page — three tiers, one visibly recommended, annual framed in money
- **Do:** three tiers (five-plus creates decision fatigue), one marked recommended with a real visual anchor, monthly/annual toggle stating the annual saving as an absolute amount ("save $240/year"), and annual plans also shown as their monthly equivalent.
- **Why:** an unhighlighted lineup gives no entry point and measurably underconverts; absolute savings trigger loss aversion harder than a percentage, and monthly-equivalent framing lifts annual selection.
- **Apply when:** any self-serve pricing page — the web sibling of BP-022.
- **Tags:** pricing, anchoring, revenue, conversion, web
- **Source:** [CRO26]/[PLG25]

#### BP-119: Signup asks for the smallest identity that unblocks value
- **Do:** ask only what the next step actually consumes (email + SSO; name/company only if used immediately); require a card only when the trial is deliberately opt-out (BP-070), and say so before the form starts.
- **Why:** every field past the minimum costs conversion — opt-out signup collapses as the payment form lengthens, and wallet one-tap recovers much of it; opt-in trades volume for a lower trial-to-paid, which is a choice, not a default.
- **Apply when:** any web signup or trial start.
- **Tags:** forms, friction-reduction, pricing, conversion, web
- **Source:** [CRO26]/[PLG25]

#### BP-120: Total price visible before the last step, in the user's currency and tax rules
- **Do:** show the final amount — currency, VAT/sales tax, every fee — on the plan or cart step, not after the address form; localize price and payment methods by region; put wallets (Apple Pay / Google Pay) above the card form.
- **Why:** unexpected extra costs are the single biggest documented checkout-abandonment cause, with "couldn't see the total upfront" a separate one on top; wallets delete the form for most users.
- **Apply when:** any web checkout, subscription or one-time.
- **Tags:** checkout, pricing, trust, conversion, web
- **Source:** [Baymard]/[CRO26]

#### BP-121: Abandonment is a flow, not a leak
- **Do:** design the exit as a branch — persist cart/quiz state, issue a resume link (email or magic link) back to the exact step left, and send one recovery message repeating the original promise instead of opening a new pitch.
- **Why:** roughly 70% of carts are abandoned and much of that traffic never disqualified itself — it stalled on cost, forced account, or complexity; recovery only exists if the state survived the exit.
- **Apply when:** any multi-step web funnel with a payment step.
- **Tags:** checkout, winback, error-recovery, conversion, web
- **Source:** [Baymard]/[CRO26]

#### BP-122: Dunning is a UX surface, not a billing job
- **Do:** treat failed payment as a scenario — notice before card expiry, in-product banner with a one-tap update-card path (deep-linked, not "go to billing"), a retry schedule that ends in a real message, and a grace period that stays honest about the account's state.
- **Why:** involuntary churn reaches a double-digit share of total churn, expired cards dominate the failures, and recovery roughly doubles when retries are paired with an in-product multi-touch path instead of processor retries alone.
- **Apply when:** any recurring billing outside the stores.
- **Tags:** billing, lifecycle, retention, error-recovery, revenue
- **Source:** [CRO26]

#### BP-123: Cancel is self-serve and honest; save-offer once
- **Do:** cancellation reachable from settings in no more steps than upgrade; state exactly what happens and when (access until date, data retention, refund rule); at most one save offer (pause, downgrade, discount) with a reason survey — then let go and confirm in writing.
- **Why:** hidden or hostile cancel flows convert into chargebacks, store refunds, and 1-star reviews (and in several jurisdictions, regulatory exposure); the reason survey is the input BP-035 winback needs.
- **Apply when:** any subscription billed self-serve.
- **Tags:** cancel, trust, retention, winback, web
- **Source:** [CRO26]/[NNg]

### Web-to-app funnels (web2app)

BP-078 states the economics; this set is the design work. The store gap —
web purchase, then install — is a seam that silently destroys owned
conversion unless every branch across it is specified.

#### BP-124: The web funnel replaces onboarding, not just the paywall
- **Do:** run the quiz, goal-setting, value promise, and offer on the web (BP-002, BP-010, BP-069 apply verbatim), then hand a configured, already-paid account to the app; the app's first session starts at the first real task, never at a second onboarding.
- **Why:** moving only the payment screen keeps the store friction and makes the user answer the same questions twice; the gain comes from owning the whole pre-install experience.
- **Apply when:** paid-acquisition-heavy app products with LTV worth protecting (expands BP-078).
- **Tags:** web2app, onboarding, revenue, conversion, subscription-app
- **Source:** [W2A26]/[48Laws]

#### BP-125: The paid handoff is a first-class scenario with failure branches
- **Do:** specify install → identify (magic link / OTP / SSO under the same identity as the web purchase) → entitlement restore → activated home, plus the branches: wrong account, mail never arrived, purchase not yet propagated, second device, refunded. A paying user must never meet a paywall.
- **Why:** the store gap is where owned conversion dies quietly — paid on the web, landed in a free app; "restore purchase" as the only route is a support queue wearing a button.
- **Apply when:** every web2app funnel, and any web-checkout upsell beside IAP (BP-030).
- **Tags:** web2app, handoff, error-recovery, trust, subscription-app
- **Source:** [W2A26]

#### BP-126: Carry context across the store gap (deferred deep linking)
- **Do:** pass campaign, quiz answers, and entitlement through a deferred deep link / install-attribution SDK; degrade to the emailed magic link when the deep link is lost, and design that fallback screen deliberately instead of letting it be a cold start.
- **Why:** without it the install breaks the chain — the app cannot personalize from answers already given (BP-010), and paid attribution stops at the store page.
- **Apply when:** any web funnel that ends in an app install.
- **Tags:** web2app, attribution, personalization, handoff, mobile
- **Source:** [W2A26]/[ASO25]

#### BP-127: Store policy is a per-storefront variable, not a constant
- **Do:** branch the purchase surface by storefront and re-check the current rules before each ship: since the April 2025 US ruling, US-storefront iOS apps may link out to external purchases with no Apple commission; other storefronts still need the external-purchase-link entitlement with its own fee and disclosure sheet; the EU runs its own regime. Keep IAP as the fallback wherever linking out is not allowed.
- **Why:** one hardcoded global purchase flow gets the build rejected or the entitlement revoked — and these rules have changed repeatedly since 2024.
- **Apply when:** any app shipping external purchase links or web checkout (with BP-030, BP-078).
- **Tags:** web2app, ios, android, pricing, revenue
- **Source:** [W2A26]

#### BP-128: Web billing brings duties the store used to absorb
- **Do:** choose merchant-of-record vs direct processor consciously, then design what it obliges: tax display and remittance, SCA/3DS friction in the EU, refunds and chargebacks, receipts and invoices, and a self-serve billing portal — all user-facing scenarios, not back-office chores.
- **Why:** the ~3–4% processing advantage over 15–30% IAP is only real net of tax, fraud, refunds, and support; the store was doing that work invisibly before.
- **Apply when:** moving any purchase off IAP.
- **Tags:** billing, checkout, trust, revenue, web
- **Source:** [W2A26]/[CRO26]

#### BP-129: Measure the whole chain or you are optimizing half a funnel
- **Do:** define one funnel spanning web session → paywall view → purchase → install → identify → activation → retained, keyed to a single identity, with per-step drop-off and per-campaign cohorts (BP-045, BP-046); attribute install and activation back to the web step that sold them.
- **Why:** a funnel measured only to the purchase optimizes the sale and hides the handoff drop — the money moment is a paying, activated user, not a checkout event.
- **Apply when:** any web2app or web-checkout funnel that is live (with BP-040..048).
- **Tags:** web2app, analytics, attribution, activation, insight
- **Source:** [W2A26]/[PLG25]

### Motion & animation

BP-054 states the stance (motion communicates or it goes). These three are
the system that makes the stance auditable.

#### BP-130: Motion is a token scale, not a per-element decision
- **Do:** define durations and easings once as named tokens by role (instant/short/medium/long; standard, decelerate, accelerate, emphasized) and use only those; entering elements decelerate, leaving elements accelerate; distance scales duration, mass does not — big surfaces get one step longer, never three times longer.
- **Why:** ad-hoc timings are the motion twin of ad-hoc spacing (BP-085) — the interface reads as several products animating at once, and nothing can be tuned centrally.
- **Apply when:** any product with more than a handful of transitions; the concrete values come from the recorded style pack ([visual-identity.md](visual-identity.md)), the requirement to have a scale does not.
- **Tags:** motion, design-system, visual-hierarchy, feedback, maintainability
- **Source:** [M3]/[HIG]

#### BP-131: Reduced motion is a supported mode, not a courtesy
- **Do:** honor the OS reduced-motion setting — replace movement with cross-fades or instant state changes, never simply keep the animation and shorten it; anything that auto-plays, loops, or scrolls for more than five seconds gets a visible pause/stop control; large-transform effects (parallax, zoom-through, spin) are the first to go.
- **Why:** vestibular disorders make gratuitous motion genuinely disabling, and WCAG 2.2 treats this as normative (2.2.2 pause/stop/hide, 2.3.3 animation from interactions) — a decorative effect that cannot be turned off is a defect, not a flourish.
- **Apply when:** every animated surface; audits verify the reduced-motion branch actually exists in code rather than being assumed.
- **Tags:** motion, accessibility, web, mobile, trust
- **Source:** [WCAG]/[M3]

#### BP-132: Scroll-driven storytelling never owns the content
- **Do:** build the page so the full content is present and readable with no scroll effects at all, then add scroll-linked motion as enhancement; never reveal information only on scroll-trigger; keep one clock (a single scroll driver, not competing observers) and cap simultaneous animated layers.
- **Why:** content locked behind animation disappears for reduced-motion users, assistive tech, print, and any device where the effect janks — and the layered-effect pages that fail this are exactly the ones that also blow the weight budget (BP-133).
- **Apply when:** landing pages, cinematic hero sections, "scrollytelling" narratives — the cinematic craft itself belongs to the **sheleg-design** companion; this is the floor it may not go under.
- **Tags:** motion, landing-page, accessibility, performance, web
- **Source:** [WCAG]/[webdev]

### Page weight, responsiveness & device reality

#### BP-133: Set a page-weight budget and enforce it in review
- **Do:** state a per-page byte and script budget in the project docs and check it like a test; images in modern formats at the size actually displayed, explicit dimensions, lazy below the fold; one variable font, subset, self-hosted; no autoplay video hero; 3D/WebGL behind a static poster with its own budget and a no-WebGL path; watch DOM element count as a proxy for markup bloat.
- **Why:** the field median mobile page is now measured in megabytes with hundreds of kilobytes of script, and roughly half of sites fail Core Web Vitals — the median is the competition, not the target. Weight is felt as slowness first (BP-058), cost second, and carbon third.
- **Apply when:** any web surface, landing pages first; audits treat a missing/unenforced budget as a finding on the pages that miss it.
- **Tags:** performance, page-weight, web, landing-page, conversion
- **Source:** [HTTPArchive]/[webdev]/[WSG]

#### BP-134: Design at the real baseline viewport, break on content
- **Do:** design and review the small viewport first — a ~360×800 CSS-pixel phone is the most common screen on the web, not an edge case — then let breakpoints fall where the content breaks, not at device names; verify the layout at 320px width and at 200% browser zoom (WCAG 1.4.10 reflow: no two-dimensional scrolling, no clipped content).
- **Why:** mobile carries the majority of traffic and, in retail, of orders; "desktop first, then squeeze" produces layouts whose primary action lands below the fold exactly where most users are — and the reflow requirement fails silently until someone zooms.
- **Apply when:** any responsive web surface; audits check the narrow viewport and the zoom case explicitly.
- **Tags:** responsive, web, layout, accessibility, conversion
- **Source:** [HTTPArchive]/[WCAG]

#### BP-135: Input capability is not a device class
- **Do:** treat hover, fine pointer, and touch as independent capabilities: never put information or an affordance behind hover alone, keep focus styles distinct from hover styles, size targets for touch wherever touch is possible (BP-050), and test with a keyboard on the "mobile" layout and a finger on the "desktop" one.
- **Why:** touch laptops, tablets with trackpads, and phones with keyboards break the device→input assumption; a hover-only menu or tooltip simply does not exist for the users who cannot hover.
- **Apply when:** any web surface with hover affordances, tooltips, or hover-revealed controls.
- **Tags:** responsive, accessibility, web, control, friction-reduction
- **Source:** [WCAG]/[M3]/[HIG]

### Accessibility as it actually fails

BP-059 sets the standard. These three describe how real products miss it —
the defects are few and repetitive, which is what makes them checkable.

#### BP-136: Native semantics first, ARIA only for what HTML cannot say
- **Do:** reach for the native element (`button`, `a`, `label`, `input`, `dialog`, headings, lists) before any role; add ARIA only where no native equivalent exists (BP-107, BP-110 patterns); never label an element with the role it already has; every `aria-*` reference must resolve to an existing id, and every custom widget must carry its keyboard behavior — no exceptions.
- **Why:** field scans find pages using ARIA average roughly twice the detected errors of pages without it — ARIA is a promise the author must implement by hand, and a broken promise is worse than no promise: it overrides working native behavior.
- **Apply when:** any custom control, any component built without a platform library; audits flag roles applied on top of native semantics.
- **Tags:** accessibility, web, component, control, trust
- **Source:** [WebAIM]/[APG]

#### BP-137: Overlays are not remediation, and scanners are not coverage
- **Do:** fix the source markup; do not install an accessibility overlay/widget and call the product compliant; run automated checks for the mechanical defects, then walk the top flows by keyboard and by screen reader — that walkthrough is the actual evidence an audit cites.
- **Why:** overlays sit on top of broken markup, sometimes breaking assistive tech further, and businesses running them have been sued anyway; automated tools detect only the subset of criteria a machine can judge, so a clean scan means "no detected defects", never "accessible".
- **Apply when:** any accessibility claim, any remediation plan, any audit's accessibility evidence.
- **Tags:** accessibility, web, trust, legal
- **Source:** [A11yLaw]/[WebAIM]

#### BP-138: Accessibility is decided in the chain, not retrofitted after build
- **Do:** state the keyboard path, focus order, announcements, and contrast pairs in the scenario and the screen record, while the design is still text; treat the applicable regime (European Accessibility Act since June 2025 for in-scope products sold in the EU, ADA litigation exposure in the US) as a ship requirement with a named owner, like any other compliance constraint.
- **Why:** most teams still touch accessibility only after the UI exists, which is where it becomes expensive rework — deciding it in the chain costs a few lines per scenario, and it is the same artifact the audit later verifies.
- **Apply when:** every scenario touching interactive UI; a product with EU/US market reach records the regime decision in the foundation.
- **Tags:** accessibility, legal, trust, web, mobile
- **Source:** [A11yLaw]/[WCAG]

### Frustration telemetry

#### BP-139: Instrument frustration, not only conversion
- **Do:** capture the friction signals alongside the funnel — rage clicks, dead clicks, repeated failed submits, error loops, rapid back-and-forth navigation, field-level form abandonment — and segment them by screen, platform, and cohort (BP-045, BP-046); watch them on the flows where the money is (search, filters, product detail, checkout).
- **Why:** conversion tells you that something is wrong somewhere; frustration signals tell you which element on which screen; reducing them tracks with materially lower churn and deeper sessions in benchmark data, and a single bad experience is enough to lose a meaningful share of users outright.
- **Apply when:** any product with analytics; goes into the analytics plan with BP-040..048, not after launch.
- **Tags:** analytics, insight, feedback, conversion, web
- **Source:** [CSq]

#### BP-140: A recurring signal becomes a scenario, or it is decoration
- **Do:** route every repeating frustration cluster back into the chain — name the screen and scenario it belongs to, file it as a finding with a severity and an owner, and re-check it in the next audit; if no scenario covers the surface, that gap is the first finding.
- **Why:** dashboards accumulate signals nobody owns; the chain is what turns "rage clicks on the filter bar" into a fixed flow with a verdict, and closing the loop is what makes the telemetry worth its instrumentation cost.
- **Apply when:** any product where BP-139 signals are collected.
- **Tags:** analytics, insight, error-recovery, maintainability
- **Source:** [CSq]/[NNg]

### Engagement mechanics (gamification)

#### BP-141: Gamification amplifies the core job, never substitutes for it
- **Do:** attach points, levels, badges, or progress to the behavior that already delivers the product's value, and make the reward legible in the user's own terms ("3 lessons to your weekly goal"), not just a number going up; leaderboards only among comparable peers, and never as the sole framing.
- **Why:** extrinsic rewards bolted onto a job the user does not care about crowd out the intrinsic motive and stop working the moment the novelty fades; global leaderboards demotivate everyone outside the top, which is most of the audience.
- **Apply when:** any proposal to add game mechanics; each mechanic names the traced job/story it reinforces (BP-001 discipline) or it does not ship.
- **Tags:** gamification, retention, engagement, habit, reward
- **Source:** [SDT]/[48Laws]

#### BP-142: Loss-aversion mechanics need a recovery valve
- **Do:** pair any streak, tier, or accumulating-progress mechanic with a designed way back — a repair/freeze item, a grace window, a "resume where you left" path — and never make the loss moment the loudest notification the product sends.
- **Why:** the same loss aversion that drives daily return turns into a quit trigger the moment the streak breaks; without a valve the mechanic manufactures churn exactly at the point of highest engagement.
- **Apply when:** streaks, ladders, tiers, expiring progress; the recovery path is a first-class flow with its own scenario.
- **Tags:** gamification, retention, habit, winback, engagement
- **Source:** [SDT]/[48Laws]

### Personalization & progressive profiling

#### BP-143: Ask progressively — later, fewer, and only what unlocks something
- **Do:** split what you need to know across sessions instead of one long form: ask at the moment the answer changes what the user gets, remember it, and never ask again; derive what can be derived (locale, timezone, plan, device) rather than asking; each surviving question states what it unlocks.
- **Why:** every field costs completion (BP-055), but the answers still have to arrive — spreading the ask keeps the first conversion cheap while the profile fills over time, and re-asking known facts reads as a product that does not remember its users.
- **Apply when:** signup, onboarding, lead capture, anything currently trying to collect a full profile up front.
- **Tags:** forms, onboarding, personalization, friction-reduction, conversion
- **Source:** [Baymard]/[CRO26]

#### BP-144: Personalization is visible, correctable, and off by choice
- **Do:** show why the user is seeing something ("because you chose 'beginner'"), give a one-tap way to correct or reset the inference, and keep the unpersonalized path reachable; never let a wrong inference become unfixable state.
- **Why:** users expect personalization and mostly do not get it, but silent personalization is worse than none — an unexplained wrong guess reads as surveillance, and with no correction path the product keeps being wrong at the user forever.
- **Apply when:** recommendations, adaptive onboarding, segmented offers, any content ordered by inferred preference.
- **Tags:** personalization, trust, segmentation, engagement, insight
- **Source:** [NNg]/[48Laws]

### Trend adoption & visual debt

#### BP-145: Adopt a visual trend through its mechanism, with a review date
- **Do:** before adopting a trend (immersive 3D, maximalism, retro/neo-brutalist styling, an experimental navigation), write down four things: the mechanism it serves for this audience, its fit with the recorded identity, its cost in accessibility and weight, and the date it gets re-judged; then record it in the style pack rather than in one screen.
- **Why:** this is BP-001 applied to looks — trends are mechanisms with an expiry date, and a look adopted without one becomes debt nobody has the authority to remove; a trend applied per screen instead of per pack is drift by definition.
- **Apply when:** any "let's make it look like X" proposal, any redesign framed by a trend list rather than by a job.
- **Tags:** trend-governance, design-system, visual-hierarchy, maintainability
- **Source:** [NNg]/[48Laws]

#### BP-146: Trend styles with known debt ship only with the compensation named
- **Do:** for styles whose cost is documented, pay it explicitly — soft-shadow/neumorphic surfaces still need real ≥3:1 boundaries and visible focus states; deliberately raw "anti-design" keeps conventional labels, order, and target sizes; experimental navigation keeps a conventional path to every destination; immersive/3D obeys BP-131..133. If the compensation cannot be named, the style is rejected, not "tested in production".
- **Why:** these looks fail on the same two axes every time — affordance and contrast — and they fail for the users least able to work around it; naming the compensation is what separates a deliberate aesthetic from an accessibility regression.
- **Apply when:** any of these styles is proposed; audits check the compensation exists in the built UI, not just in the discussion.
- **Tags:** trend-governance, accessibility, visual-hierarchy, control, trust
- **Source:** [WCAG]/[NNg]/[WebAIM]

### Growth loops, virality & referral

#### BP-147: Name the growth loop before choosing freemium
- **Do:** if the model is freemium or any permanently free tier (BP-067), name the specific loop the free users feed — viral (they bring people), content (their output is public and found), or network (each user raises the product's value for the others) — and record it in the foundation beside the model. "Being generous" is not a loop.
- **Why:** BP-067 makes freemium defensible only when such a loop exists, and BP-073 puts the median free→paid conversion at 2.6% — without a named loop the free tier is conversion given away for nothing. Referred users also convert and retain better than organic ones, so the loop pays twice, but only if someone designed it.
- **Apply when:** choosing or revisiting a monetization model; any proposal to add a free tier.
- **Tags:** freemium, virality, conversion, revenue, insight
- **Source:** [RC25]/[PLG25]/[Viral26]

#### BP-148: Virality rides the product's output, not a "refer a friend" page
- **Do:** put the loop where the product already peaks: attribution on the artifact the user exports or shares, the link inside an invitation that was going out anyway, "invite your team" at the step where the work actually needs them, "share this result" on the screen that just produced value. A standalone referral page is the last mechanism to build, not the first.
- **Why:** sharing the output is the lowest-friction loop there is — it asks for no new behavior, only the decision to carry attribution on the artifact — while a referral page needs its own motivation, its own visit, and a reason to remember it exists.
- **Apply when:** the product exports, publishes, invites, or shares anything.
- **Tags:** virality, referral, engagement, conversion, activation
- **Source:** [Viral26]

#### BP-149: Plan for K around 0.2 and design the cycle time
- **Do:** model the viral coefficient at roughly 0.2 (the B2B SaaS average; 0.1–0.3 is typical, 0.3–0.7 is a strong result, above 1.0 belongs to a handful of collaboration products in a specific phase). Design the loop's cycle time alongside K — days for consumer products, weeks for B2B — because a fast loop with a moderate K beats a slow loop with a high one.
- **Why:** growth models built on K > 1 almost never come true, and the cycle time is the multiplier nobody computes: it decides how many times the coefficient compounds within the same quarter.
- **Apply when:** planning a growth loop; any financial model with an organic channel in it.
- **Tags:** virality, analytics, insight, revenue
- **Source:** [Viral26]

#### BP-150: Reward in the product's own unit, pay on the invitee's milestone
- **Do:** pay the referral in a unit of the product (seats, credits, storage, a period of the paid tier) rather than an unrelated discount or gift card, and release it when the invited user reaches a meaningful milestone — not when they register. Set the attribution window from the loop's cycle time (BP-149) instead of leaving it open.
- **Why:** an in-product reward returns the user to the product instead of teaching them to wait for discounts; paying on a milestone aligns the referrer with retention rather than with volume and removes the cheapest abuse route, which is the empty account.
- **Apply when:** any referral mechanic that pays a reward.
- **Tags:** referral, reward, retention, conversion, trust
- **Source:** [Viral26]

#### BP-151: Design against referral abuse before launch, not after
- **Do:** ship the safeguards with the program — verified address before any reward is credited, reward gated behind the qualifying action (BP-150), a rate limit on invitations per account — and watch for the signals afterwards: invitation conversion spiking against the program's own baseline, an unusual concentration of referrals on one account, invited accounts sharing devices or subnets.
- **Why:** a referral reward is the one mechanic in the product that pays for account creation, so it attracts abuse by construction rather than by bad luck; the safeguards are cheap before launch and become a payout dispute afterwards.
- **Apply when:** any referral program with a reward that has cash value or converts to one.
- **Tags:** referral, trust, revenue, analytics
- **Source:** [Viral26]

### Empty states, authentication & form recovery

#### BP-152: An empty state reports status, teaches, and offers a way in
- **Do:** give every empty container three layers — what happened (genuinely empty vs still loading vs failed, told apart), what this place is for and what will appear here, and a direct path to start: create the first item, and where it fits, inspect the feature on demo data. A blank panel with no words is a defect, not a neutral state.
- **Why:** an empty container is not neutral — it lowers confidence, hides the feature, and slows the task; the same space carrying an explanation and an action becomes onboarding exactly where the user already stands (BP-041), which is the one place onboarding does not have to interrupt anything.
- **Apply when:** any list, table, dashboard, inbox, or folder — first run and every state that empties again later.
- **Tags:** onboarding, activation, feedback-ui, microcopy, engagement
- **Source:** [NNg]

#### BP-153: Password rules follow length and screening, not composition
- **Do:** drop composition rules ("one uppercase, one digit, one symbol") — they are prohibited, not merely unfashionable; require at least 15 characters when the password is the only authenticator and at least 8 alongside a second factor; screen every new password against breach corpora, dictionary words, keyboard runs, and context terms (the product name, the user's own login); force a change only on evidence of compromise.
- **Why:** NIST SP 800-63B rev. 4 made this normative in August 2025 because composition rules produce predictable passwords and move the work into the user's memory, while length and breach screening act on the attack that actually happens.
- **Apply when:** any screen that creates, changes, or recovers a password.
- **Tags:** auth, forms, trust, legal, friction-reduction
- **Source:** [NIST]

#### BP-154: The password field must not fight the password manager
- **Do:** allow paste — it is a normative requirement, not a convenience; show the rules before the first attempt rather than after the rejection; offer a reveal toggle; set `autocomplete` correctly (`new-password` on creation, `current-password` on sign-in) so the platform and the manager both fill it.
- **Why:** blocking paste is prohibited precisely because it pushes people toward a password they can retype from memory, and WCAG 2.2 counts the same block as an accessible-authentication failure; rules revealed only after a rejection turn one attempt into a guessing loop.
- **Apply when:** every password field on every platform.
- **Tags:** auth, forms, friction-reduction, accessibility, trust
- **Source:** [NIST]/[WCAG]

#### BP-155: Offer a passwordless door where the account allows one
- **Do:** where the account does not need a password to function, present a one-time link or code, a passkey, or a platform provider as an equal way in — placed as a first-class option, not buried under "forgot your password". The password stays available; it stops being the only door.
- **Why:** the credential nobody has to invent is the one that cannot be reused from another breach, and 800-63B rev. 4 pushes deliberately toward phishing-resistant and syncable authenticators; on the signup side this is the same economy as BP-119 — ask for the smallest identity that unblocks value.
- **Apply when:** designing sign-in and sign-up for a product without a hard password requirement.
- **Tags:** auth, forms, friction-reduction, conversion
- **Source:** [NIST]

#### BP-156: A rejected form keeps the work and names the way out
- **Do:** on a validation failure keep everything already typed, move focus to the first field at fault, and say what to do next; "this address is already registered" leads to sign-in and recovery instead of ending there; a multi-step form keeps its progress across a reload.
- **Why:** clearing the form punishes the person who already did the work for a failure the system detected, and WCAG 2.2 treats re-asking for information the user has already given as a defect in its own right; PRN-09 asks a message to say what happened and how to recover, and a form that loses the input breaks the second half of that.
- **Apply when:** any form with validation; multi-step and long forms especially.
- **Tags:** forms, error-recovery, friction-reduction, conversion, accessibility
- **Source:** [WCAG]/[Baymard]
