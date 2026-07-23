# Component & Control Guidelines — When To Use What

A decision reference for the visual components and controls a screen is made
of: which control fits which job, and the platform rules for it. Distilled
from verified design systems — Apple HIG, Material Design 3, W3C ARIA
Authoring Practices Guide (APG), GOV.UK Design System. Used when specifying a
screen's elements (`screens.md`), drawing wireframes/Figma, and auditing
(the heuristic/practice passes). Catalog entries: BP-101..115 in
[best-practices.md](best-practices.md).

The rule above all: **reach for the platform's standard component before
inventing one** (Jakob's law, PRN-14) — it ships with the accessibility,
states, and motion behavior you'd otherwise rebuild wrong.

## Choosing a control by the job

| The user needs to… | Use | Not |
|---|---|---|
| Trigger one primary action on a screen | one prominent button (HIG primary role / M3 filled) | multiple competing primaries |
| Trigger the screen's single most important create/compose action (mobile) | FAB (M3) | a button lost in a toolbar |
| Pick exactly one from 2–5 visible options | radio group | dropdown (hides choices) |
| Pick one from many (6+) options | select / menu, or a searchable combobox | a long radio list |
| Pick zero-or-more options | checkboxes | a multi-select users can't discover |
| Toggle one setting on/off, applies immediately | switch | a checkbox (checkbox = staged submit) |
| Choose from actions related to one action/selection | action sheet (mobile) / menu | an alert |
| Confirm or stop a destructive/consequential action | alert / confirmation dialog with named buttons | a silent immediate action |
| Enter a memorable date | 3-field day/month/year input (GOV.UK) | a calendar picker for birthdays |
| Enter a date to look up/browse | date picker | free-text parsing |
| Show/hide a chunk of secondary content | disclosure / accordion | a modal |
| Focus the user on a subtask, blocking the rest | modal dialog (ESC-closable, focus-trapped) | a full page nav when a modal fits |
| Move between top-level destinations (mobile <600dp) | bottom navigation bar, 3–5 items | a hamburger hiding primaries |
| Move between destinations (tablet 600–839dp) | navigation rail, 3–7 items | a phone nav bar stretched |
| Brief, low-priority, auto-dismissing feedback | toast / snackbar | an alert that blocks |

## Control rules worth auditing

### Buttons
- Exactly one primary per screen; assign primary to the most likely action —
  **never** to a destructive one, even if likely (HIG). Destructive actions
  use the destructive style. Labels are verbs (BP-089).

### Action sheets & alerts (mobile)
- Action sheet = choices *for an action*; alert = *unexpected* info/confirm
  with no extra choices. Use sheets sparingly — they interrupt.
- ≤4 buttons incl. Cancel (aim ≤3 choices + Cancel); destructive choice
  styled and placed where it's noticed, never adjacent to the likely tap.

### Selection controls
- Radios/checkboxes to the **left** of labels (screen-magnifier reach); the
  whole label is a tap target. State how many can be picked in a hint — the
  radio-vs-checkbox shape alone isn't understood (GOV.UK).
- Avoid select boxes where a small visible set of radios works — dropdowns
  hide choices and are hard for many users (GOV.UK).
- Switch flips immediately; checkbox is for staged/submit forms. Don't mix.

### Dialogs & overlays (web, ARIA APG)
- Modal: `role="dialog"` + `aria-modal="true"`; content behind is inert;
  **ESC closes**; focus moves in on open, is **trapped** while open, and
  **returns** to the trigger on close; Tab cycles within.
- Don't stack modals; don't use a modal for content a disclosure/accordion
  handles inline.

### Combobox (web, ARIA APG)
- `role="combobox"` owning a textbox; popup is listbox/grid/tree/dialog with
  the matching `aria-haspopup`; arrow keys move, Enter selects, ESC closes;
  reflect selection in the field.

### Navigation (M3)
- Bottom nav bar only for compact widths (<600dp); 3–5 destinations; always
  at the bottom (thumb zone, BP-049). Nav rail for 600–839dp, 3–7 items.
  Primary destinations are always visible, never hidden-only (BP-052).

### Feedback
- Toast/snackbar for transient, non-blocking confirmations; never put a
  required action only in a toast (it disappears). Blocking = dialog.

## Every interactive component ships all its states

Default is not a component. Each control provides: default, hover (pointer),
focus (visible ring — WCAG), active/pressed, disabled (with the reason
discoverable), loading where async, error where it can fail, selected where
applicable. Missing states are how PRN-01/PRN-09 silently fail — the audit
checks the state set, and Figma variants (BP-096) must carry them.

## Cross-platform stance

- Respect the host platform's component of record (HIG on Apple, M3 on
  Android, the project's design system on web). On web with no system, ARIA
  APG patterns are the accessibility contract and GOV.UK is a sound default
  for forms. Deviate only when the job demands it, and then keep keyboard +
  screen-reader behavior equivalent to the standard pattern.
