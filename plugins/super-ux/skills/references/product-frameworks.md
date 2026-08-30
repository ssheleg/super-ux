# Product frameworks: which one answers this question, and where it lies

The practice catalog holds 241 tactical rules with sources. This file holds
the layer above them: the named models that decide **which** question is being
asked, in what order, and against what. A team with 241 practices and no model
applies whichever one it read most recently.

Every framework below carries the same four parts, and the third is the one
that makes this file worth reading: **what it is**, **when it applies**, **when
it misleads**, and **what it costs**. A framework presented without its failure
mode is a belief, and a pack that ships beliefs teaches an agent to apply them
where they do not hold.

None of these replaces the chain. `vision.md` says what the product refuses to
become, `foundation.md` who it is for, `flows.md` how they move,
`scenarios.md` what must be true. These decide what to put into that chain and
how to argue about it.

## Contents

- [The twelve](#the-twelve)
- [Discovery: what is true of the people](#discovery-what-is-true-of-the-people)
- [Prioritisation: what to build next](#prioritisation-what-to-build-next)
- [Measurement: what to watch](#measurement-what-to-watch)
- [Behaviour: why it does or does not happen](#behaviour-why-it-does-or-does-not-happen)
- [Where each one enters the chain](#where-each-one-enters-the-chain)

## The twelve

| id | Framework | Answers | Fails as |
|---|---|---|---|
| PF-01 | Forces of progress | why people do **not** switch | four boxes filled from imagination |
| PF-02 | Switch interview | how the forces are actually learned | a tidied story told long after |
| PF-03 | Value proposition canvas | whether the offer meets a named pain | a canvas nothing can falsify |
| PF-04 | Opportunity solution tree | which unmet need a solution serves | a roadmap with extra steps |
| PF-05 | North star and its inputs | what the whole org is moving | a metric chosen for being measurable |
| PF-06 | AARRR | which stage the problem lives in | a funnel drawn over a loop |
| PF-07 | Activation and time to value | when the user first gets what they came for | a correlation mistaken for a mechanism |
| PF-08 | Fogg behaviour model | why one behaviour did not happen | motivation reached for first |
| PF-09 | Hook model | how a behaviour becomes a habit | compulsion sold as engagement |
| PF-10 | Kano model | which features earn satisfaction and which only lose it | a survey cited years after it decayed |
| PF-11 | Service blueprint | where a failure is organisational, not interface | a blueprint for a single screen |
| PF-12 | Double diamond | when converging early is the mistake | a shape adopted as a schedule |

## Discovery: what is true of the people

### PF-01. Forces of progress

**What it is.** Four forces act on anyone considering a change: the **push** of
the current situation, the **pull** of the new one, the **anxiety** about the
new, and the **habit** of the present. A switch happens when push and pull
together exceed anxiety and habit.

**When it applies.** Any product someone must leave something else to adopt,
which is nearly all of them. Its whole value is the right-hand pair: most teams
work only on push and pull, because features and marketing are the levers they
own, while the reason nobody switched was anxiety about migration and the habit
of a spreadsheet.

**When it misleads.** The forces are reconstructed from what people say, and a
team that fills the four boxes without talking to anyone who actually switched
has written fiction in a diagram. Anxiety in particular is the force people are
least able to name about themselves.

**What it costs.** Six to ten interviews, and the discipline to stop when the
same forces repeat.

### PF-02. Switch interview

**What it is.** An interview with someone who recently started or stopped using
something, reconstructed backwards from the moment of the decision: what
happened the day they first thought about it, what they tried in between, what
finally made them act.

**When it applies.** Whenever `foundation.md` needs customer language rather
than invented language. The timeline is the instrument: asking *why* invites a
rationalisation, and asking *what happened next* invites a memory.

**When it misleads.** Memory is reconstructive and tidies itself with distance.
An interview about a decision six months old returns a story with a clean
motive that the decision did not have. Interview within weeks, and treat
anything older as a hypothesis.

**What it costs.** Forty-five minutes each and a recruiting problem, which is
the real reason teams skip it.

### PF-03. Value proposition canvas

**What it is.** Two halves checked against each other: the customer's jobs,
pains and gains on one side; the product's features, pain relievers and gain
creators on the other. The output is not the canvas, it is the **fit check**:
every pain reliever must point at a pain someone named.

**When it applies.** When a feature list exists and nobody can say which of it
matters. It is fastest at finding the reverse problem: a pain with nothing
pointing at it.

**When it misleads.** The boxes fill easily with plausible entries, and a
plausible entry is indistinguishable from a real one once written down. A
canvas whose entries carry no source is decoration. Require each pain to cite
an interview, a ticket or a measured drop-off, and the canvas becomes honest
and half as full.

**What it costs.** An hour, and the willingness to leave boxes empty.

## Prioritisation: what to build next

### PF-04. Opportunity solution tree

**What it is.** A desired **outcome** at the root; **opportunities**, which are
unmet needs stated in the customer's words, as branches; **solutions** as
leaves; **experiments** below those. A solution is only comparable to another
solution on the same branch.

**When it applies.** When a backlog holds twenty good ideas and no way to argue
between them. The tree makes the argument structural: two solutions under one
opportunity compete, two under different opportunities do not, and a solution
under no opportunity is somebody's preference.

**When it misleads.** An outcome that is secretly an output corrupts the whole
tree: "ship the new editor" as a root produces branches that rationalise a
decision already made. And a tree drawn once and never pruned becomes a
roadmap, which is the thing it was drawn to replace.

**What it costs.** Continuous, not one-off. Its value is entirely in being
revised, which is why it is abandoned most often.

### PF-10. Kano model

**What it is.** Features sorted into **must-be** (absent, satisfaction
collapses; present, nobody notices), **performance** (more is linearly better),
**delighter** (absent, nobody minds; present, satisfaction jumps), plus
**indifferent** and **reverse**, which the popular version drops and which are
where the surprises are.

**When it applies.** When a team is arguing about whether to polish or to add,
because the model says those are different currencies. A must-be feature is
judged by whether it fails, never by how good it is; spending on making a
must-be excellent buys nothing.

**When it misleads.** The categories decay. Every delighter becomes a must-be
once competitors ship it, and the interval is often a year. A Kano survey cited
three years after it was run is not evidence, it is a claim about a market that
no longer exists.

**What it costs.** A survey with a specific paired-question format, which most
teams get wrong by asking a single question.

## Measurement: what to watch

### PF-05. North star and its inputs

**What it is.** One metric representing value **delivered to the user**,
decomposed into three to five input metrics that teams can actually move. The
decomposition is the artifact; the single number is only its headline.

**When it applies.** When several teams are moving separate numbers and nobody
can say whether the product improved. It works by making the trade visible: an
input that rises while the north star does not has found a local optimum.

**When it misleads.** Chosen for measurability rather than for value, it points
the whole organisation at the wrong thing with unusual efficiency: sessions per
user rewards making the product harder to finish with. And a single number
hides the segment where it is falling, so it is read beside a cohort split or
not at all.

**What it costs.** Instrumentation, and one genuinely difficult argument about
what value means here.

### PF-06. AARRR

**What it is.** Acquisition, activation, retention, revenue, referral. Five
stages that name **where** a problem lives.

**When it applies.** As a triage instrument. Its worth is almost entirely in
stopping a retention problem from being answered with acquisition spend, which
is the most common expensive mistake in this list.

**When it misleads.** It draws a funnel over what is often a loop. In a product
where users bring users, referral feeds acquisition, and reading the stages
linearly understates the compounding. And **activation is undefined** inside
this model, so a team can report an activation rate that means nothing until
`PF-07` has been done.

**What it costs.** Little. It is a vocabulary, not a study, and it should be
treated as one.

### PF-07. Activation and time to value

**What it is.** **Activation** is the first moment a user gets the value they
came for. **Time to value** is how long that took. Finding it: identify the
early behaviour that separates users who stay from users who leave, then design
the shortest honest path to it.

**When it applies.** Before any onboarding work. Onboarding cannot be designed
against an undefined destination, which is why so much of it is a product tour.
See `onboarding.md`, where the whole assembly rests on this.

**When it misleads.** The behaviour that correlates with retention is not
necessarily the cause of it. "Users who add seven collaborators retain" usually
means users who already had a team to bring were going to stay; pushing a lone
user to invite seven people tests the theory and often refutes it. Treat the
correlate as the hypothesis and the intervention as the experiment.

**What it costs.** A retention curve split by early behaviour, which needs
events instrumented before the question is asked.

## Behaviour: why it does or does not happen

### PF-08. Fogg behaviour model

**What it is.** A behaviour occurs when **motivation**, **ability** and a
**prompt** arrive together. Missing any one, it does not, and the model's use
is that it tells you which of the three to change.

**When it applies.** Any single moment that should happen and does not: the
invite not sent, the setting not configured, the trial not converted. Ability
is almost always the cheapest of the three to raise, and almost always the last
one teams try.

**When it misleads.** It explains one occurrence, not a pattern. A behaviour
that needs a prompt every time has not become a habit, and treating repeated
prompting as success produces a product that only works while it is nagging.

**What it costs.** Nothing to apply. Its discipline is asking about ability
before motivation.

### PF-09. Hook model

**What it is.** Trigger, action, variable reward, investment. The fourth step
is the one products skip: the user putting something of their own in, which
both improves the next use and raises the cost of leaving.

**When it applies.** Products whose value genuinely compounds with use, where a
returning user is better served than a new one.

**When it misleads.** This is the framework most easily turned against the
person it is applied to, and the pack states that plainly rather than in a
footnote. Variable reward tuned to maximise return frequency rather than
delivered value is a dark pattern with a diagram, and the tell is simple: if
the user would object on being shown the mechanism, it is not a hook, it is a
trap. Beyond that, **most products should not be habit-forming.** A tax tool
used twice a year, a service that files a claim, a tool bought to finish
something: for these, a lower usage frequency is the product working.

**What it costs.** Little to apply and a great deal to apply badly, which is
why it sits here with its objection attached.

### PF-11. Service blueprint

**What it is.** A journey map extended downwards past the **line of
visibility**: what the user does, what the frontstage shows, what happens
backstage, and which support processes carry it.

**When it applies.** Where the experience crosses systems or people. It finds
the class of failure no interface review can, because the defect is a handoff:
the email nobody owns, the queue with no fallback, the manual step that only
works on weekdays.

**When it misleads.** It is expensive and repays only where handoffs exist.
Drawing one for a single-screen tool produces a diagram of one arrow and
teaches a team that the method is theatre.

**What it costs.** Days, and access to the people who run the backstage, which
is usually the harder half.

### PF-12. Double diamond

**What it is.** Two diamonds: discover then define, develop then deliver. Four
phases, two of which widen and two of which narrow.

**When it applies.** As a naming device for the two convergence points, which
are decisions somebody must make and sign. Its real content is the instruction
not to converge on the first plausible answer, and that instruction is
correct.

**When it misleads.** It describes a shape, not a process, and it is routinely
adopted as a schedule. A team doing six weeks of discovery regardless of what
week two found has taken the drawing and left the idea. The diamonds are also
drawn as one pass when in practice they recur per decision.

**What it costs.** Nothing, which is exactly why it is adopted without the part
that is hard.

## Where each one enters the chain

| Chain layer | Frameworks that feed it |
|---|---|
| `vision.md` | PF-12 at the first convergence; PF-05 for what the vision is measured by |
| `foundation.md` | PF-01, PF-02, PF-03 for personas, jobs and customer language |
| `flows.md` | PF-07 for the destination, PF-08 per step, PF-11 where the flow leaves the product |
| `screens.md` | PF-10 for what is a must-be and therefore judged by failure |
| `scenarios.md` | PF-07 makes activation a scenario with an observable, not a slogan |
| the board | PF-04 for arguing between solutions, PF-06 for which stage owns the problem |

Two of them are ordering constraints rather than inputs, and getting them
backwards wastes the work: **`PF-07` before any onboarding design**, because
onboarding without a defined destination is a tour; and **`PF-02` before
`PF-01`**, because the forces are an output of the interviews and not a
worksheet to fill in beforehand.
