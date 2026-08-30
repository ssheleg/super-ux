# Internal screens: the product after the argument is won

A landing page persuades a stranger and an onboarding path delivers a first
value. This file covers everything after that: the screens someone uses because
they already decided, where the job is no longer persuasion but **not wasting
the time of a person who came to do something**.

These screens are where products actually fail, and they fail quietly. Nobody
A/B tests a settings page, no analyst reports on a list view, and the defects
compound because each screen was reviewed alone and full of data.

The catalog holds the tactics. This file holds the questions a screen must
answer before it is drawn, and the states it must be drawn in.

## Contents

- [The eighteen](#the-eighteen)
- [What the screen is for](#what-the-screen-is-for)
- [The four states are one design](#the-four-states-are-one-design)
- [Lists and the data in them](#lists-and-the-data-in-them)
- [Actions and their consequences](#actions-and-their-consequences)
- [Numbers, roles and rhythm](#numbers-roles-and-rhythm)
- [The readiness check](#the-readiness-check)

## The eighteen

| id | Rule | Fails as |
|---|---|---|
| IS-01 | The screen answers one question the user arrived with | a page of everything |
| IS-02 | It names what it shows, over what scope, as of when | a number with no referent |
| IS-03 | The screen after sign-in is the work, not a summary of it | a dashboard nobody uses twice |
| IS-04 | A dashboard nobody can act on is a report, and is named one | charts as decoration |
| IS-05 | Empty, loading, failed and full are one design | three states drawn later, badly |
| IS-06 | "Nothing yet" and "nothing matches" are different screens | a filter that looks like a bug |
| IS-07 | Loading shows the shape and does not move content on arrival | a layout that jumps under the cursor |
| IS-08 | Every column earns its place | a table read by nobody |
| IS-09 | The most common action does not require opening the row | four clicks for the daily task |
| IS-10 | Opening a detail never loses the position in the list | work restarted after every item |
| IS-11 | A filter declares itself and offers one way to clear | an empty screen with a hidden cause |
| IS-12 | Search states what it searched and what it excluded | a result set nobody can trust |
| IS-13 | A bulk action names the count and the scope before it runs | a mistake at the scale of the selection |
| IS-14 | Destructive is reversible, or confirmed with the consequence named | a dialog that says "are you sure" |
| IS-15 | A long operation reports progress and survives navigation | a tab nobody may close |
| IS-16 | Every number carries unit, period and freshness | a figure argued over for an hour |
| IS-17 | What a role cannot do is an explained absence | a dead control and a support ticket |
| IS-18 | Density and rhythm are decided once for the product | screens from four different products |

## What the screen is for

### IS-01. The screen answers one question the user arrived with

Write the question before the layout: "which of these needs me today", "what
happened to this one", "how do I change that". A screen serving three questions
serves the most senior stakeholder's, and the other two get a widget.

The test is subtraction. Remove any element and ask whether the question is
still answered; if it is, the element was there for a different question.

### IS-02. It names what it shows, over what scope, as of when

Scope and recency are not chrome, they are part of the claim. A figure without
"last 30 days, excluding cancelled, as of 09:15" is a number two people will
read differently, and the disagreement surfaces in a meeting rather than on the
screen.

### IS-03. The screen after sign-in is the work, not a summary of it

The most common reason someone opens a product is to continue. A landing screen
that summarises rather than resumes adds a step to the most frequent path in
the product, every time, for everyone.

Where a summary genuinely is the job, that is the exception and it is stated:
a monitoring tool is opened to check, not to continue.

### IS-04. A dashboard nobody can act on is a report, and is named one

The distinction is whether an action lives beside the number. If it does not,
the artifact is a report, and calling it a dashboard sets an expectation the
screen cannot meet. Reports are legitimate; a report labelled as a dashboard
gets rebuilt every year by someone who assumes it was meant to do more.

## The four states are one design

### IS-05. Empty, loading, failed and full are one design

Drawing full first and the others later is the default and it is the cause of
most of what follows. The three non-full states then get whatever the framework
does by itself, which is a spinner, a blank area and a red sentence.

Design them together, in one pass, on one artboard. `screens.md` records states
per screen for exactly this reason, and a screen with only one state recorded
is not designed.

### IS-06. "Nothing yet" and "nothing matches" are different screens

The first is a new user with an opportunity and it takes the empty-state
treatment from `onboarding.md` ON-05. The second is an experienced user with a
filter and it needs the opposite: the filter named, and one action to widen it.

Showing the first to the second is the defect people report as "the search is
broken", and they are right, because the screen told them there is nothing.

### IS-07. Loading shows the shape and does not move content on arrival

A skeleton that matches the eventual layout tells the user what is coming and
holds the space it will need. Content that arrives into an unreserved space
moves everything under it, and the cost is a click on the wrong thing.

Reserve the space in the loading state or the layout shifts. There is no third
option.

## Lists and the data in them

### IS-08. Every column earns its place

A column is justified by one of three uses: scanning for the right row, sorting
or filtering by it, or deciding without opening the row. A column that does
none is carried by every user on every visit for the benefit of the one request
that added it.

Where a field is needed rarely, it belongs in the detail view or behind a
column chooser whose default excludes it.

### IS-09. The most common action does not require opening the row

Find the action performed most often against a list item and count the clicks.
If the count includes opening and returning, the list is a directory of links
rather than a working surface, and the daily cost is the frequency times the
difference.

### IS-10. Opening a detail never loses the position in the list

Scroll position, selection, filter, sort and page all survive the return. This
breaks most often in single-page applications where the detail is a route
change, and the symptom is a user who processes items slowly and cannot say
why.

### IS-11. A filter declares itself and offers one way to clear

An active filter is visible on the screen it affects, not only in the panel
that set it. One control clears everything, and it is not the browser back
button.

The strongest form of this defect is a filter that persists across sessions
without saying so: the user returns days later to a product that appears to
have lost their data.

### IS-12. Search states what it searched and what it excluded

Which fields, whether archived items are included, whether it matched whole
words. Without it, an empty result is ambiguous between "not present" and "not
searched", and those demand opposite next actions.

## Actions and their consequences

### IS-13. A bulk action names the count and the scope before it runs

"Delete 1,240 items" is a different sentence from "Delete selected", and the
difference is the entire safeguard. Where the selection is "all matching the
filter" rather than "all visible", say which, because the two differ by orders
of magnitude and the user is looking at the smaller one.

### IS-14. Destructive is reversible, or confirmed with the consequence named

Reversible is the better answer and it is usually cheaper than it looks: a
soft delete with an undo window removes the need for the dialog entirely.

Where confirmation is genuinely required, the dialog names what is lost and
what cannot be recovered, and the confirming verb repeats the action rather
than saying "OK". `ui-copy.md` governs the wording, and the no-humour rule
applies to every one of these surfaces.

### IS-15. A long operation reports progress and survives navigation

An import, an export, a bulk edit, a report build. Each needs a state the user
can leave and return to, and a result they are told about. An operation that
only exists while its tab is open is a feature with a hidden precondition, and
nothing on the screen states it.

## Numbers, roles and rhythm

### IS-16. Every number carries unit, period and freshness

The screen version of the rule `facts.md` enforces for copy. A number that
appears in two places with two values is the defect users lose trust over
fastest, and the cause is almost always two queries with different scopes,
neither of which is stated.

### IS-17. What a role cannot do is an explained absence

A control that is present, enabled, and fails on click teaches the user that
the product is broken. A control that is present and disabled with no reason
teaches them it is arbitrary. Either remove it for that role, or disable it
with the reason and the person to ask.

This is a scenario, not a styling decision, because the behaviour differs per
role and each variant is a path someone takes.

### IS-18. Density and rhythm are decided once for the product

Row heights, spacing scale, type scale, how much fits on a screen. Decided per
screen, they produce an application that reads as several applications, and the
drift is invisible to whoever is looking at one screen at a time.

This is `sheleg-design`'s layer and it is named here because internal screens
are where the drift accumulates: they are added one at a time, by different
people, under deadline, and nobody reviews them side by side.

## The readiness check

Internal screens are checked by being visited in the states nobody develops in.
Every line below is a walk, not a query, and each takes minutes.

| Walk | Rules it checks |
|---|---|
| Open every screen in a brand-new account with no data | IS-05, IS-06 |
| Apply a filter that matches nothing | IS-06, IS-11 |
| Throttle the network to slow 3G and reload each screen | IS-07 |
| Block the primary request and reload | IS-05 |
| Load a list with more rows than anyone tested | IS-08, IS-10, IS-13 |
| Open an item from position 200 of a list and come back | IS-10 |
| Select all matching a filter, then read the confirmation | IS-13 |
| Run the longest operation and navigate away mid-way | IS-15 |
| Sign in as the most restricted role and open every screen | IS-17 |
| Put four screenshots of different screens side by side | IS-18 |
| Count clicks for the single most frequent task in the product | IS-09 |
| Find one number that appears on two screens and compare them | IS-02, IS-16 |

The last two are the ones teams skip and the ones that find the most, because
neither can be answered by looking at a single screen, which is the only way
internal screens are ever reviewed.
