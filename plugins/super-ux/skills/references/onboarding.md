# Onboarding: designing the path to the first value

The practice catalog's *Onboarding & early experience* section holds the
tactics. This file holds the order they go in, and it rests on one thing being
decided first: **where the path leads**. `product-frameworks.md` PF-07 defines
that destination as activation, the first moment the user gets what they came
for. Onboarding designed without it is a tour, and a tour is what a team builds
when it has not decided what the user is for.

The rules below are ordered as the work is: the destination, then the entry,
then the path, then what happens when the path fails, then what makes the
second session different from the first.

## Contents

- [The eighteen](#the-eighteen)
- [The destination](#the-destination)
- [The entry](#the-entry)
- [The path](#the-path)
- [When the path fails](#when-the-path-fails)
- [After the first session](#after-the-first-session)
- [The readiness check](#the-readiness-check)

## The eighteen

| id | Rule | Fails as |
|---|---|---|
| ON-01 | The destination is named before the first screen is drawn | a product tour |
| ON-02 | Time to value is measured, never estimated | a number nobody can move |
| ON-03 | Signup asks for what the first value needs and nothing more | a form that costs more than the product |
| ON-04 | Value comes before the account wherever the product allows | a wall in front of a stranger |
| ON-05 | The empty state is the first onboarding screen | a blank page with a shrug |
| ON-06 | A tour is what you build when you could not fix the interface | a carousel nobody reads |
| ON-07 | Teaching happens at the moment of use | six tips before the first click |
| ON-08 | Sample data is a loan, and its repayment is designed | a workspace nobody can clear |
| ON-09 | Setup that pays off later is deferred and reversible | a wizard before the value |
| ON-10 | One primary track, one visible way out of it | a corridor with no doors |
| ON-11 | Progress is stated in steps that exist | an invented percentage |
| ON-12 | Every abandonment point is a state with a way back | a user who cannot resume |
| ON-13 | Failure during onboarding is the most expensive failure the product has | a generic error at minute two |
| ON-14 | An invite or an import is asked for after value, never before | work demanded on credit |
| ON-15 | Each permission is asked where its benefit is visible | a permission wall on launch |
| ON-16 | Onboarding ends, and the product says so | a state the user never leaves |
| ON-17 | The second session is designed, and it is not the first repeated | a product that forgets |
| ON-18 | Return after a lapse is its own design | onboarding shown to an expert |

## The destination

### ON-01. The destination is named before the first screen is drawn

Write the activation moment as one sentence with an observable in it, and put
it in `scenarios.md` where it can be checked. "The user understands the
product" is not one. "A first report is generated and opened" is.

Everything downstream is decided by this sentence: which fields signup can
justify asking for, what the empty state must offer, where the tour would have
gone. A team that cannot write it does not have an onboarding problem yet, it
has a `PF-07` problem.

### ON-02. Time to value is measured, never estimated

The distance from first arrival to `ON-01`'s observable, as a distribution
rather than an average. The average hides the shape, and the shape is the
finding: two clusters mean two paths, and one of them is failing.

Estimating it instead is the standard failure, because the team estimating has
done the task a thousand times. The person who has done it once is the subject.

## The entry

### ON-03. Signup asks for what the first value needs and nothing more

Every field is justified by the destination or it is deleted. A field collected
because sales will want it later is a cost paid by every user for the benefit
of a few, and it is paid at the least trusted moment there is.

Where a field is genuinely needed later, ask later. Progressive profiling is in
the catalog for this.

### ON-04. Value comes before the account wherever the product allows

Let the stranger do the thing, then ask them to keep it. The account then has a
reason the user already believes, and the work they have done is the argument
for creating it.

This is not always possible and the test is honest: does the first value
require identity, storage or money? If not, the wall is habit rather than
necessity.

### ON-05. The empty state is the first onboarding screen

It is what a new account actually shows, so it is the screen the most users see
in the state where they know least. It carries three things: what goes here,
why it is worth it, and the single action that starts it. A blank area with an
icon is a design that was not done.

## The path

### ON-06. A tour is what you build when you could not fix the interface

Before designing a tour, name the screen it explains and ask why the screen
needs explaining. Most tours are documentation for a layout problem, and the
cheaper fix is the layout.

Where a tour survives that question, it is short, skippable without penalty,
and it never blocks the action it describes.

### ON-07. Teaching happens at the moment of use

A tip attached to a control the user is about to touch is read. The same tip
shown in a sequence before they touch anything is not, because nothing has
given them a reason to hold it.

The consequence for structure: onboarding is distributed through the product
rather than concentrated at the front of it, and that means it has no single
screen to review, which is why it gets skipped in design review.

### ON-08. Sample data is a loan, and its repayment is designed

Sample content makes an empty product legible and it creates a second problem
the moment the user starts working: their real work now sits beside fiction.
Design the exit. Sample items are visibly marked, removable in one action, and
they disappear on their own once real content exists.

### ON-09. Setup that pays off later is deferred and reversible

Integrations, team settings, notification preferences: none of these are
between the user and the first value, so none of them belong before it. Where
one is genuinely required, say what it unlocks in the same sentence that asks
for it.

Reversible matters as much as deferred. A choice made in the first two minutes
was made with the least information the user will ever have.

### ON-10. One primary track, one visible way out of it

A new user cannot evaluate three equally weighted options, because evaluating
them is the expertise they do not have yet. Offer one recommended path, and
make the exit visible rather than hidden, so the person who knows better is not
trapped in a path built for someone else.

### ON-11. Progress is stated in steps that exist

"Step 2 of 4" is a promise, and it is checkable. A percentage bar that advances
by design rather than by work is not, and users learn to distrust it within one
product.

If the number of steps varies by choice, say so rather than picking an average.

## When the path fails

### ON-12. Every abandonment point is a state with a way back

People leave onboarding mid-way, close the tab, run out of time. Each of those
moments is a state the product is in, and it either has a resume or it silently
loses the work. Enumerate the points from the flow, and give each one a return
path: an email with a link back, a saved draft, a resumable position.

### ON-13. Failure during onboarding is the most expensive failure the product has

The same error at minute two and at month two costs different amounts, because
at minute two the user has no evidence that the product works and no reason to
try again. Errors on this path get the specific message, the recovery action
and the human escape hatch, and they never say "something went wrong".

`ui-copy.md` governs the wording; this rule is about which failures get the
budget.

### ON-14. An invite or an import is asked for after value, never before

Both ask the user to spend something they have not yet decided is worth
spending: a colleague's attention, or their own data. Asked before the value,
they read as a cost of entry. Asked after, they read as an extension of
something that already worked.

### ON-15. Each permission is asked where its benefit is visible

Notifications, location, contacts, calendar. Every one of these is a question
whose answer depends on a benefit, so it is asked at the moment the benefit is
on screen, with the reason in the sentence. A permission wall on launch is the
whole benefit argument compressed into a system dialog the product does not
control.

A refusal is a legitimate answer and the product works after it. Where it
genuinely cannot, that is a scenario, not a dialog.

## After the first session

### ON-16. Onboarding ends, and the product says so

An onboarding state with no exit is a product permanently addressed to a
beginner. Name the condition that ends it, make the ending observable to the
user, and stop the prompts on the same event.

### ON-17. The second session is designed, and it is not the first repeated

The returning user knows one thing and has forgotten another, and they arrive
with an expectation set by what they did last time. The second session shows
the work they left, not the welcome they already saw. A product that greets a
returning user identically has told them that nothing they did was recorded.

### ON-18. Return after a lapse is its own design

Someone coming back after months is neither new nor current: their data is
stale, the interface has changed, and their memory is partial. Showing them the
new-user onboarding insults them; showing them nothing strands them. The design
is a short reconciliation: what changed, what state their work is in, and one
action to resume.

## The readiness check

Onboarding is a behaviour, so most of this is measured rather than grepped, and
the honest form of this section is a list of measurements with what each one
answers. Every line below needs events instrumented before it can be asked,
which is itself the first finding on most products.

| Measure | Answers | Defect it exposes |
|---|---|---|
| Distribution of time from arrival to the `ON-01` observable | ON-02 | two clusters mean two paths and one is failing |
| Activation rate split by cohort and by entry source | ON-01 | a single average hiding a dead channel |
| Drop-off per named step of the flow | ON-12 | the step nobody returns from |
| Share of users who see the empty state and take its action | ON-05 | an empty state that is decoration |
| Tour completion against activation, compared | ON-06 | a tour that correlates with nothing |
| Rate of error events on the onboarding path | ON-13 | the failure being paid for at the worst moment |
| Permission grant rate by prompt location | ON-15 | a wall asked before its benefit |
| Second-session return rate and what that session shows | ON-17 | a product that greets a returning user as new |

Two of these can be checked without analytics, and should be, because they are
the cheapest: walk the path in a clean account and count the fields before the
first value (ON-03), and close the tab at each step, then return, and record
what happens (ON-12).
