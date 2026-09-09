# The state-stress matrix — pressure applied to every state, on paper first

Load this when a scenario set is being audited or built out and the question
is *which states exist and what must be VISIBLE in each* — before a browser
opens, and instead of trusting the happy path.

## The row contract

One row = one **scenario × state × action → expected visible result**, plus
the pressure dimension that produced it. A row that cannot name what the user
SEES is not a row; "the request succeeds" is a backend fact, not a visible
result.

| Field | Rule |
|---|---|
| scenario | the scenario id from `docs/ux/scenarios.md` — a row belongs to one |
| state | one of the state taxonomy below |
| action | what the user (or the world) does |
| expected visible result | what the screen observably shows — element, text, position |
| pressure | which dimension this row stresses (content volume, timing, repetition, interruption, concurrency) |
| evidence | `fixture` / `hypothesis` / `observed` — see marking |

## The state taxonomy — four empties are four states

**Empty is not one state.** The matrix requires all four, separately:

- **first-use** — the user has never had content here. No illustration is
  required: an empty state needs a next action and one line of orientation;
  a mandatory mascot is decoration doctrine, not this matrix's demand.
- **cleared** — the user HAD content and removed it. Saying "nothing here yet"
  to someone who deleted things is a small lie; the state may acknowledge it.
- **no-results** — a filter or search returned nothing. The query stays
  visible and editable; the escape is showing how to widen it.
- **error-empty** — the list failed to load. NEVER dressed as empty: an error
  names the failure and the retry, because "you have no messages" over a dead
  connection is a fabricated fact.

Beyond the empties, every matrix covers: **loading** (a loading state shows
that WAITING is happening — it never simulates computation with fake progress
that measures nothing), **drafts** (unsaved input survives navigation or the
row says it does not), **retry** (what the second attempt looks like, and what
happened to the first), **cancel** (mid-flight cancellation leaves a named
state, not a limbo), and **concurrent submit** (double-click, two tabs — one
effect, and the row says which). Financial actions are stressed with
**fixtures only — no real charge, refund or transfer is ever triggered by a
matrix run**; the row marks the boundary it verified.

## Content pressure — minimum / typical / maximum, from the domain

Each content-bearing row states three volumes, and the numbers come from the
DOMAIN, not from taste: minimum (the legal shortest — one item, one
character), typical (what the median user actually has — cite where that
came from), maximum (the retention policy's ceiling, the API's page size, the
longest real name in the dataset). **Synthetic content is marked synthetic**
— a screenshot full of invented averages reads as evidence and is not.

## Evidence marking — fixture / hypothesis / observed

Every row carries exactly one:

- **fixture** — the state was produced by a controlled fixture; reproducible,
  but says nothing about production frequency;
- **hypothesis** — the row is designed but has never been seen running; it is
  work to schedule, not evidence;
- **observed** — the state was seen on the actual render. A screenshot or an
  interaction trace attaches to EXACTLY ONE row — a gallery of screenshots
  "covering" a table proves nothing row by row.

**A static source pass never promotes a scenario to implemented.** The matrix
is read against the ux-audit evidence tiers (`ux-audit` step 3): a row whose
expected visible result depends on the runtime is BLOCKED until a test, a
browser check or an observed trace exists — file:line proves the text of the
branch, not that a user sees it.
