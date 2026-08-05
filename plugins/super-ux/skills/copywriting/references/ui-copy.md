# UI copy — the strings inside the product

Craft for the twelve product surfaces listed in
[brand-contract.md](brand-contract.md). Register deltas per surface live in
[surface-registers.md](surface-registers.md); this file is about the strings
themselves.

Interface copy is read differently from marketing copy in one way that
changes every rule: **it is read hundreds of times by the same person.** A
line that is charming on the first read is an obstruction on the fortieth.
Where the two bodies of craft disagree, this is why.

## The four laws

1. **One action, one name.** An action carries the same word everywhere it
   appears — button, confirmation, toast, history, notification, docs.
   `Publish` → `Published`, never `Publish` → `Submitted`. Two names for one
   action is `B020`, and it is the most common defect in a product built
   screen by screen, because each screen was individually correct.

2. **Buttons are verb phrases naming the outcome.** `Save changes`, not
   `Submit`. `Delete project`, not `OK`. The user should be able to predict
   the result from the label alone, with the surrounding sentence covered.

3. **One job per string.** A label labels. Help text explains. An example
   demonstrates. A placeholder is not a label, and a label is not
   instructions — placeholder text disappears exactly when the user needs it.

4. **Sentence case throughout.** Title Case On Buttons reads as a
   proper noun and slows scanning. Declared once in `voice.md`, enforced as
   `B024`.

## Errors

Three facts, in this order:

1. **What happened**, in the product's own vocabulary — not the exception's.
2. **What was not affected.** The one products skip and users need most.
   "Your draft was saved" turns a failure into an interruption.
3. **One next step**, phrased as something the user can actually do.

```
✗  Error: unexpected failure (code 500)
✗  Something went wrong! Please try again later 😅
✓  We could not publish Atlas. Your changes are saved.
   Try again, or publish without the attachments.
```

Never blame the user. Never say "unexpected" — it tells the reader the team
was surprised, which is not reassuring. Never show a code without a sentence
beside it; a code alone is a support ticket the user has to write.

**A blocked action names the blocker and the unblocking step.** "You do not
have permission" is half a message; "Only owners can delete a project. Ask
<name>, or leave the project instead" is a whole one.

## Empty states

Teach; never apologise. Three jobs in order: what belongs here, why it is
worth putting there, and the single action that starts it.

```
✗  No projects yet.
✓  Projects hold the files and settings for one piece of work.
   Create your first one and everything else has somewhere to live.
   [ Create project ]
```

Distinguish the three kinds, because they need different copy: **nothing yet**
(teach), **nothing matched** (offer to widen or clear the filter, and show
what the filter was), **nothing left** (confirm completion, do not imply
failure).

## Loading and progress

Under ~400ms, say nothing — a flash of text is worse than a pause. Longer
than that, name what is happening in the product's own words. Longer than
about ten seconds, say what the user can do meanwhile.

Never claim progress the system cannot observe. A bar that sits at 90% is a
lie the user remembers longer than the wait.

## Confirmations and destructive actions

Name the **object**, the **consequence**, and whether it is **reversible**.
The confirming button repeats the destructive verb.

```
✓  Delete project "Atlas"?
   This removes 340 files and cannot be undone.
   [ Cancel ]  [ Delete project ]
```

`OK` on a destructive confirm is a defect: the user clicks it having read
only the button. If the action is reversible, say so — it is the difference
between a confirmation and an interrogation. If undo exists, prefer undo over
a dialog entirely.

## Forms

Labels above fields, always visible. Requirements stated **before** the user
types, not after they fail — "at least 12 characters" belongs under the field
from the start, not in a red message afterwards.

Validation messages say what is wrong and what is valid, in that order:
`Card numbers are 16 digits. This one has 15.` Never `Invalid input`.

Optional and required: mark whichever is rarer, once, consistently.

## Notifications, toasts and email

A toast is the past tense of the action's verb. `Published.` Nothing else
fits in the time it is on screen.

A push notification with no object is a notification that gets disabled.
`Atlas finished building` — not `Something happened in your workspace`.

Transactional email: one purpose per message, named in the subject and
delivered in the first sentence.

## Permissions and asks

State the trade before the ask: what the product will do with the access, and
what it can do without it. A permission prompt that appears before the value
is visible is refused, and a refusal is expensive because the second ask
costs more than the first.

## Numbers, dates and names in the interface

Every figure a user sees in the product is either their own data or a fact
from `facts.md`. There is no third source. Dates are absolute where a
decision depends on them (`3 June 2026`) and relative where recency is the
point (`2 hours ago`); never relative past about a week.

## Accessibility is copy work too

The accessible name is the visible label wherever a visible label exists —
a button reading `Delete` with an accessible name of `Remove item` is two
names for one action, which is `B020` with a screen reader as the witness.
Alt text describes the function in context, not the picture. An icon-only
control still needs a name, and that name is a verb phrase like any other
button.
