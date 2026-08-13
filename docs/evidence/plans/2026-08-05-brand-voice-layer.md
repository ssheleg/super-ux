# Verbal identity layer — implementation plan

> **For agentic workers:** execute this plan task-by-task under the task-pipeline
> stage-5 build doctrine — isolated workspace, one implementer per task, a review
> with all three verdicts after each (spec compliance, REQ satisfied, code
> quality). Steps use `- [ ]` checkboxes.

**Goal:** give super-ux a verbal identity layer — a versioned `docs/brand/`
contract, two skills that define and apply it, and a deterministic linter that
makes copy drift as findable as chain drift.

**Architecture:** `docs/brand/` is a new artifact root beside `docs/ux/`, carrying
`brand-contract v1`. `brand-voice` owns it; `copywriting` reads it and never
writes it; `brand_lint.py` proves the machine-checkable half; a new `copy` scope
in `ux-audit` judges the rest. Six voice packs ship as a library in a reference;
per-project calibration produces `voice.md`.

**Tech stack:** Markdown skills and references (Agent Skills spec), stdlib-only
Python 3 scripts, Node installer (`bin/super-ux.js`), GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-05-brand-voice-copywriting-design.md`
**Brief:** `docs/superpowers/briefs/2026-08-05-brand-voice-layer.md`

## Global constraints

Every task's requirements implicitly include this section.

- **One owner per fact.** A field, rule, or path is defined in exactly one file
  and referenced everywhere else.
- **Markdown line width ~78 columns.**
- **IDs are stable and never reused:** `BP-NNN`, `PRN-NN`, and the new `B0NN`
  linter codes.
- **Practice entry shape:** `Do` / `Why` / `Apply when` / `Tags` / `Source`, under
  ~6 lines, tags drawn from the taxonomy at the top of `best-practices.md`, then
  wired into `practice-selection.md`. New practices (`BP-182` and above) carry a
  sixth field, `Checked`. `BP-001..181` are not touched.
- **Skill front matter:** opens with `Use when`, pairs each Russian trigger beside
  its English equivalent, stays under 1024 characters. `claude plugin validate
  --strict` fails otherwise.
- **Skill bodies, references, templates, and linter messages are English.**
- **Python is stdlib-only**, matching `ux_lint.py` and `ux_doctor.py`.
- **Tests are standalone scripts**, not pytest: `python3 test/<name>.py`, `main()`
  returns an exit code, prints `OK (n checks)` or `FAIL: <reason>`.
- **The tag `voice` is reserved for voice interfaces (VUI)** and must not be used
  by any new practice. The brand tag is `brand-voice`.
- **Installer asset paths stay literal strings** in `bin/super-ux.js` so
  `test/validate.py` can regex them.
- **Contract marker** `Contract: brand-contract v1` is the first line of every
  file under `docs/brand/`.

## Execution order

| Group | Tasks | Runs after |
|---|---|---|
| A | 1 | — |
| B | 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | A |
| C | 13, 14, 15, 16, 17 (sequential chain, one file) | B |
| D | 18, 19, 20 | B |
| E | 21, 22 | B |
| F | 23, 24 | E |
| G | 25, 26, 27, 28, 29, 30, 31 | C, D |
| H | 32, 33, 34, 35 (sequential) | F, G |
| I | 36, 37, 38, 39, 40 (sequential) | H |

---

### Task 1: the `brand-contract v1` contract

**Depends:** —

**Implements:** R-01 — *contract `brand-contract v1`: six file types plus
`README.md` and `lint.py`, marker in the header of each.* R-02 — *`voice.md`
carries pack, five axes as IS / IS NOT, narrative, `Locales`, `Locale parity
threshold`, `Derived-from`, `Status`, `Last calibrated`, invariants and
per-locale items.* R-03 — *shapes of `terminology.md`, `facts.md`,
`channels.md`, `strings.md`, `locales/<code>.md`.*

**Files:**
- Create: `plugins/super-ux/skills/references/brand-contract.md`

**Interfaces:**
- Consumes: nothing.
- Produces: the single definition of every `docs/brand/` field name, status
  value, and file name. Every later task quotes it and defines nothing itself.
  Names other tasks rely on: file names `voice.md` `terminology.md` `facts.md`
  `channels.md` `strings.md` `locales/<code>.md` `README.md` `lint.py`; header
  key `Contract: brand-contract v1`; `voice.md` keys `Voice pack` `Locales`
  `Locale parity threshold` `Derived-from` `Status` `Last calibrated`;
  `voice.md` axis names `Confidence` `Register` `Distance` `Humor` `Density`;
  narrative keys `Hero` `Enemy` `Product role` `Promise`; `strings.md` columns
  `Key` `Text (primary)` `Location` `Scenario` `Status` with statuses `agreed`
  `proposed` `drifted` `orphan`; `facts.md` columns `Fact` `Value` `Source`
  `Checked` `Review by` `Public`; `channels.md` record keys `Register` `Format`
  `Limits` `Forbidden` `CTA` `Proof` `Locales`; `locales/<code>.md` keys
  `Locale` `Primary` `Address form` `Length coefficient` `Humor`
  `Never translated` `Keywords` `Dead idioms` `Legal differences`; the
  `README.md` `Sources:` block keys `ui` `marketing` `store` `robots` `locales`.

**Definition of done:** the file defines every name in the Produces block, each
exactly once; it carries the full surface list (product and marketing) that
`channels.md` records; it states the three cross-cutting rules verbatim —
register moves axes but never crosses invariants, platform physics and brand
choice are separate fields, humor is forbidden on error / destructive confirm /
billing / paywall surfaces; `python3 test/validate.py` reports **no**
`brand-contract.md: missing …` line.

**Known-red until Group B lands.** The contract links `voice-packs.md`,
`surface-registers.md` and `ai-tells.md`, which Tasks 2, 3 and 8 create. The
validator's relative-link check therefore fails on exactly those three targets
until Group B completes, and that is correct: the links are what
`sync_references.py` follows to compute which contracts ship inside each skill,
so removing them to buy an early green would ship the contract without its
library. **The whole-validator green gate for Group A+B sits at the end of Task
12, not here.** Any link failure naming a target outside those three is a real
failure.

- [ ] **Step 1: write the failing check**

Add to `test/validate.py` inside `main()`, before the summary:

Use the validator's own helpers — `check(ok, msg)` and `read(path)` — never
`checks`/`failures` directly. House style, and `check` is what counts the check.

```python
def validate_brand_contract() -> None:
    src = ROOT / "plugins/super-ux/skills/references"
    text = read(src / "brand-contract.md")
    if not check(text is not None, "brand-contract.md is missing"):
        return
    for token in (
        "Contract: brand-contract v1", "voice.md", "terminology.md",
        "facts.md", "channels.md", "strings.md", "locales/<code>.md",
        "Locale parity threshold", "Derived-from", "Last calibrated",
        "Confidence", "Register", "Distance", "Humor", "Density",
        "Hero", "Enemy", "Product role", "Promise",
        "agreed", "proposed", "drifted", "orphan",
        "Length coefficient", "Sources:",
    ):
        check(token in text, f"brand-contract.md: missing `{token}`")
```

Call it from `main()` beside the other `validate_*` functions.

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/validate.py`
Expected: FAIL — `brand-contract.md missing`

- [ ] **Step 3: write the contract**

Author `plugins/super-ux/skills/references/brand-contract.md` containing, in
order: the marker rule; a file table; a fully worked skeleton for each of the six
files using the exact keys in the Interfaces block; the surface list; the three
cross-cutting rules; and the `Sources:` block definition with its five keys.

- [ ] **Step 4: run it and confirm the contract checks pass**

Run: `python3 test/validate.py`
Expected: the check count rises by 26, no `brand-contract.md: missing …` line,
and exactly three broken-link failures naming `voice-packs.md`,
`surface-registers.md` and `ai-tells.md` — see *Known-red* above.

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/skills/references/brand-contract.md test/validate.py
git commit -m "feat(brand): brand-contract v1 — the docs/brand/ artifact contract"
```

---

### Task 2: voice pack library

**Depends:** [1]

**Implements:** R-04 — *six voice packs, each carrying all eight fields of the
pack contract including `Failure mode`.*

**Files:**
- Create: `plugins/super-ux/skills/references/voice-packs.md`

**Interfaces:**
- Consumes: axis names and narrative keys from `brand-contract.md` (Task 1).
- Produces: pack ids `operator-brief` `calm-expert` `peer-builder`
  `editorial-premium` `plain-service` `playful-consumer`, and the eight pack
  fields `Name` `Use for` `Not for` `Axes` `Narrative template` `Lexicon`
  `Pack bans` `Register deltas` `Ready lines` `Failure mode`.

**Definition of done:** all six packs present; each carries every field; each
`Failure mode` names a concrete degeneration, not a warning; the pack contract is
stated once at the top; `python3 test/validate.py` green.

- [ ] **Step 1: write the failing check**

Add to `test/validate.py`:

```python
PACKS = ("operator-brief", "calm-expert", "peer-builder",
         "editorial-premium", "plain-service", "playful-consumer")
PACK_FIELDS = ("Use for", "Not for", "Axes", "Narrative template", "Lexicon",
               "Pack bans", "Register deltas", "Ready lines", "Failure mode")


def validate_voice_packs() -> None:
    src = ROOT / "plugins/super-ux/skills/references"
    text = read(src / "voice-packs.md")
    if not check(text is not None, "voice-packs.md is missing"):
        return
    for section in text.split("\n## ")[1:]:
        name = section.split("\n", 1)[0].strip()
        if name not in PACKS:
            continue
        for field in PACK_FIELDS:
            check(field in section, f"voice-packs.md: {name} missing `{field}`")
    for pack in PACKS:
        check(f"\n## {pack}\n" in text, f"voice-packs.md: pack `{pack}` missing")
```

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/validate.py`
Expected: FAIL — `voice-packs.md missing`

- [ ] **Step 3: write the six packs**

Author the pack contract, then one `## <pack-id>` section per pack with all nine
field labels. `Failure mode` examples to hit the bar: `operator-brief` degrades
into military-jargon parody; `playful-consumer` into cringe; `calm-expert` into
corporate mush; `editorial-premium` into beautiful emptiness; `plain-service`
into flatness that reads as indifference; `peer-builder` into insider shorthand
that excludes newcomers.

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/validate.py`
Expected: `OK (n checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/skills/references/voice-packs.md test/validate.py
git commit -m "feat(brand): six voice packs with mandatory failure modes"
```

---

### Tasks 3–10: the remaining references

Each task below creates exactly one file, has **Depends: [1]**, and shares no
file with its group siblings. Each ends with the same three steps: run
`python3 test/validate.py` (green), run `python3 test/sync_references.py`
(prints a per-skill contract count), and commit with
`git commit -m "docs(brand): <file> reference"`.

**Definition of done, common to all eight:** the file exists at
`plugins/super-ux/skills/references/<name>.md`; it defines nothing that
`brand-contract.md` already defines and instead links it; it is under ~78 columns;
`python3 test/validate.py` is green.

| Task | File | Implements | Must contain |
|---|---|---|---|
| 3 | `surface-registers.md` | R-07 | the register-delta model; the full product and marketing surface list; the rule that register moves axes but never crosses invariants; the rule that platform physics and brand choice occupy separate fields |
| 4 | `ui-copy.md` | R-07 | per-state microcopy craft for the eleven product surfaces; button labels as verb phrases; one action keeps one name across a flow; error copy states what happened, what to do, and what was preserved; links to BP-089 |
| 5 | `marketing-copy.md` | R-07 | page structures for landing, pricing, feature, about, blog; the seven-sweep editing pass (clarity, voice and tone, so-what, prove-it, specificity, emotion, zero risk) with the loop-back rule; the grounding model for long form (prerequisite versus introduced) |
| 6 | `channel-playbooks.md` | R-07 | one playbook per marketing surface: X, Reddit, LinkedIn, HN and Product Hunt, blog, changelog, ads, lifecycle email — each separating platform physics from brand choice |
| 7 | `seo-aeo-safety.md` | R-07 | the safety/optimization split; the veto list (blocked AI crawlers, self-contradiction, title-content mismatch, missing author, YMYL without disclaimer); the absolute no-fabrication rule with its three reasons; front-loading, evidence density, extractability, entity clarity; per-engine differences |
| 8 | `ai-tells.md` | R-07 | the marker catalogue with S1/S2/S3 severities; the A–D naturalness grade applied to the result; the change-rate guard at 50%; the mandatory semantic-preservation checklist (numbers, dates, proper nouns, causal direction, negations, direct quotes, core claim); the ~10-per-500-words rewrite threshold |
| 9 | `localization.md` | R-07 | the primary-as-source-of-meaning rule; the parity-declaration rule; length coefficients; dead idioms; per-locale keyword research |
| 10 | `store-copy.md` | R-07 | App Store and Google Play field limits; the iOS keyword-field rules (no space after comma, no plurals, no words already in the title); description structure; the screenshot-caption progression from feature to action to benefit |

---

### Tasks 11–12: project templates

**Depends:** [1]

**Implements:** R-02, R-03 — *the `voice.md` field set and the shapes of the
other five files, as seeded artifacts.*

**Files:**
- Task 11 — Create: `templates/brand/README.md`, `templates/brand/voice.md`,
  `templates/brand/terminology.md`, `templates/brand/facts.md`
- Task 12 — Create: `templates/brand/channels.md`, `templates/brand/strings.md`,
  `templates/brand/locale.md`

**Interfaces:**
- Consumes: every field name from `brand-contract.md` (Task 1).
- Produces: the files `bin/super-ux.js` seeds (Task 29) and `brand_lint.py`
  parses (Tasks 13–17). `templates/brand/README.md` carries the `Sources:` block
  with keys `ui` `marketing` `store` `robots` `locales`, commented so a fresh
  project can fill it in one pass.

**Definition of done:** every template's first line is
`Contract: brand-contract v1`; every field named in `brand-contract.md` appears
in the corresponding template; a project seeded from these templates passes
`python3 docs/brand/lint.py` with exit code 0 once Task 17 exists;
`python3 test/validate.py` green.

- [ ] **Step 1: write the failing check**

Add to `test/validate.py`:

```python
BRAND_TEMPLATES = ("README.md", "voice.md", "terminology.md", "facts.md",
                   "channels.md", "strings.md", "locale.md")


def validate_brand_templates() -> None:
    tdir = ROOT / "templates/brand"
    for name in BRAND_TEMPLATES:
        text = read(tdir / name)
        if not check(text is not None, f"templates/brand/{name} is missing"):
            continue
        first = text.splitlines()[0].strip() if text.splitlines() else ""
        check(
            first == "Contract: brand-contract v1",
            f"templates/brand/{name}: first line must be the contract marker",
        )
```

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/validate.py`
Expected: FAIL — seven `templates/brand/… missing` lines.

- [ ] **Step 3: write the templates**

Each template is the skeleton from `brand-contract.md` with placeholder rows
marked `<…>` and one worked example row, so the shape is unambiguous.

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/validate.py`
Expected: `OK (n checks)`

- [ ] **Step 5: commit**

```bash
git add templates/brand test/validate.py
git commit -m "feat(brand): project templates for the docs/brand contract"
```

---

### Task 13: `brand_lint.py` skeleton, sources parsing, contract checks

**Depends:** [1, 11, 12]

**Implements:** R-08 (codes B001–B006, exit codes) — *`brand_lint.py`: codes
B001..B073 including B006; exit codes 0/1/2; `--fix` on three codes only;
stdlib-only.*

**Files:**
- Create: `plugins/super-ux/scripts/brand_lint.py`
- Create: `test/brand_lint_test.py`

**Interfaces:**
- Consumes: field names from `brand-contract.md`; template shapes from Tasks 11–12.
- Produces, relied on by Tasks 14–17:
  - `Finding = namedtuple("Finding", "code severity path line message")`
  - `SEVERITY_ERROR = "error"`, `SEVERITY_WARN = "warn"`
  - `def load_sources(brand_dir: Path) -> dict[str, list[str]]` — parses the
    `Sources:` block from `README.md`, returns key → list of glob patterns.
  - `def check_contract(brand_dir: Path) -> list[Finding]`
  - `def run(brand_dir: Path, fix: bool = False) -> list[Finding]` — calls every
    `check_*` in order and concatenates.
  - `def main() -> int` — `0` clean, `1` warnings only, `2` any error.
  - CLI flags: positional path (default `docs/brand`), `--fix`, `--brief`,
    `--json`.
  - Test helper in `test/brand_lint_test.py`:
    `def case(name: str, files: dict[str, str], expect_codes: set[str]) -> None`
    writing `files` into a `tempfile.TemporaryDirectory()` and asserting the set
    of codes returned by `run()` equals `expect_codes`.

**Definition of done:** `python3 test/brand_lint_test.py` prints `OK (n checks)`
and exits 0; a brand directory seeded from `templates/brand/` yields no findings;
removing the `Sources:` block yields exactly `{"B006"}`; the script imports only
`argparse`, `json`, `re`, `sys`, `collections`, `pathlib`, `fnmatch`.

- [ ] **Step 1: write the failing test**

Create `test/brand_lint_test.py`:

```python
#!/usr/bin/env python3
"""Fixture-per-code tests for brand_lint.py (stdlib only)."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "plugins/super-ux/scripts"))

import brand_lint  # noqa: E402

checks = 0
failures: list[str] = []

MARKER = "Contract: brand-contract v1"

MINIMAL = {
    "README.md": MARKER + "\n\nSources:\n  ui: src/**/*.ts\n",
    "voice.md": MARKER + "\nVoice pack: operator-brief\nLocales: en (primary)\n"
                "Locale parity threshold: 80%\nDerived-from: PER-01\n"
                "Status: validated\nLast calibrated: 2026-08-05\n",
    "terminology.md": MARKER + "\n",
    "facts.md": MARKER + "\n",
    "channels.md": MARKER + "\n",
    "strings.md": MARKER + "\n",
}


def case(name: str, files: dict, expect_codes: set) -> None:
    global checks
    checks += 1
    with tempfile.TemporaryDirectory() as tmp:
        brand = Path(tmp) / "brand"
        brand.mkdir()
        for rel, body in files.items():
            target = brand / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding="utf-8")
        got = {f.code for f in brand_lint.run(brand)}
    if got != expect_codes:
        failures.append(f"{name}: expected {sorted(expect_codes)}, got {sorted(got)}")


def main() -> int:
    case("clean minimal base", MINIMAL, set())
    case("no Sources block",
         {**MINIMAL, "README.md": MARKER + "\n"}, {"B006"})
    case("missing marker",
         {**MINIMAL, "voice.md": "Voice pack: x\n"}, {"B001"})
    case("mixed contract versions",
         {**MINIMAL, "facts.md": "Contract: brand-contract v2\n"}, {"B002"})
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"{len(failures)} failure(s) out of {checks} checks")
        return 1
    print(f"OK ({checks} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/brand_lint_test.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'brand_lint'`

- [ ] **Step 3: minimal implementation**

Create `plugins/super-ux/scripts/brand_lint.py` with the module docstring, the
`Finding` namedtuple, `load_sources`, `check_contract` implementing B001, B002,
B003, B004, B005, B006, `run`, and `main` with the three exit codes and the four
CLI flags. `check_contract` reads the first line of every `*.md` under the brand
directory for the marker, compares versions across files, and reports B006 when
`README.md` has no `Sources:` block.

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/brand_lint_test.py`
Expected: `OK (4 checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/scripts/brand_lint.py test/brand_lint_test.py
git commit -m "feat(brand): brand_lint.py — contract and sources checks (B001-B006)"
```

---

### Task 14: terminology and consistency checks (B010–B025)

**Depends:** [13]

**Implements:** R-08 (codes B010–B025).

**Files:**
- Modify: `plugins/super-ux/scripts/brand_lint.py`
- Modify: `test/brand_lint_test.py`

**Interfaces:**
- Consumes: `Finding`, `load_sources`, `run` from Task 13.
- Produces: `def check_terminology(brand_dir, sources) -> list[Finding]` and
  `def check_consistency(brand_dir, sources) -> list[Finding]`, both registered
  in `run`.

**Definition of done:** one fixture per code proves it fires on the violation and
stays silent on the clean variant; `python3 test/brand_lint_test.py` green;
B020 detects two different strings bound to the same scenario and action key.

- [ ] **Step 1: write the failing tests**

Append to `test/brand_lint_test.py` in `main()`:

```python
    banned = MARKER + "\n\n## Banned\n| Word | Why | Use instead |\n" \
             "| leverage | filler | use |\n"
    case("banned word in a string",
         {**MINIMAL, "terminology.md": banned,
          "strings.md": MARKER + "\n| Key | Text (primary) | Location | Scenario | Status |\n"
                                 "| a.b | Leverage this | src/a.ts:1 | SCN-001 | agreed |\n"},
         {"B010"})
    case("one action, two names",
         {**MINIMAL,
          "strings.md": MARKER + "\n| Key | Text (primary) | Location | Scenario | Status |\n"
                                 "| action.publish | Publish | src/a.ts:1 | SCN-001 | agreed |\n"
                                 "| action.publish | Submit | src/b.ts:2 | SCN-001 | agreed |\n"},
         {"B020"})
    case("non-verb button label",
         {**MINIMAL,
          "strings.md": MARKER + "\n| Key | Text (primary) | Location | Scenario | Status |\n"
                                 "| button.ok | OK | src/a.ts:1 | SCN-001 | agreed |\n"},
         {"B025"})
```

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/brand_lint_test.py`
Expected: FAIL — three lines reporting `expected [...], got []`.

- [ ] **Step 3: implement**

Add `check_terminology` (B010 banned word, B011 generic word where a product term
exists, B012 inconsistent entity or tier spelling) and `check_consistency`
(B020 one action two names, B021 code diverged from the registry, B022 code string
with no registry entry, B023 dangling `file:line`, B024 casing, B025 non-verb
button label). Register both in `run`.

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/brand_lint_test.py`
Expected: `OK (7 checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/scripts/brand_lint.py test/brand_lint_test.py
git commit -m "feat(brand): terminology and consistency checks (B010-B025)"
```

---

### Task 15: facts and channel-physics checks (B030–B043)

**Depends:** [14]

**Implements:** R-08 (codes B030–B043).

**Files:**
- Modify: `plugins/super-ux/scripts/brand_lint.py`
- Modify: `test/brand_lint_test.py`

**Interfaces:**
- Consumes: `Finding`, `run`, `load_sources`.
- Produces: `def check_facts(brand_dir, sources) -> list[Finding]` and
  `def check_channels(brand_dir, sources) -> list[Finding]`, registered in `run`.

**Definition of done:** a number present in marketing copy but absent from
`facts.md` yields B030; a title over its declared limit yields B040 and the limit
is multiplied by the locale's `Length coefficient` when a non-primary locale is
being checked; iOS keyword-field violations yield B041; fixtures cover each code.

- [ ] **Step 1: write the failing tests**

Append three cases to `main()` covering B030 (unsourced `42%` in a marketing
file), B040 (a 71-character title where the channel declares 60), and B041 (an
iOS keyword field containing `task, tasks`).

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/brand_lint_test.py`
Expected: FAIL — three `expected [...], got []` lines.

- [ ] **Step 3: implement**

`check_facts` implements B030, B031, B032. `check_channels` implements B040
(limits with locale coefficient), B041 (iOS keyword field), B042 (link in body),
B043 (hashtag count).

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/brand_lint_test.py`
Expected: `OK (10 checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/scripts/brand_lint.py test/brand_lint_test.py
git commit -m "feat(brand): facts and channel-physics checks (B030-B043)"
```

---

### Task 16: bot-safety and AI-marker checks (B050–B061)

**Depends:** [15]

**Implements:** R-08 (codes B050–B061).

**Files:**
- Modify: `plugins/super-ux/scripts/brand_lint.py`
- Modify: `test/brand_lint_test.py`

**Interfaces:**
- Consumes: `Finding`, `run`, `load_sources`.
- Produces: `def check_bot_safety(brand_dir, sources) -> list[Finding]` and
  `def check_ai_tells(brand_dir, sources) -> list[Finding]`, registered in `run`.

**Definition of done:** a `robots.txt` disallowing `GPTBot` while `channels.md`
declares AI search a target yields B050; a marketing document where one
non-stopword token exceeds 1% of word count yields B051; a filler opener yields
B052; an exclamation mark in an error-surface string yields B061; the A–D grade
appears in the B060 message.

- [ ] **Step 1: write the failing tests**

Append four cases covering B050, B051, B052, and B061.

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/brand_lint_test.py`
Expected: FAIL — four `expected [...], got []` lines.

- [ ] **Step 3: implement**

`check_bot_safety` implements B050 (crawler agents `GPTBot`, `ClaudeBot`,
`PerplexityBot`, `Google-Extended`), B051 (1% token density over a stopword
list), B052 (filler openers), B053 (missing byline), B054 (title–body mismatch).
`check_ai_tells` implements B060 (S1/S2/S3 counts, warning at any S1 or three
S2, error at three S1, message carries the A–D grade) and B061 (humor,
exclamation, or emoji on error, destructive confirm, billing, or paywall
surfaces).

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/brand_lint_test.py`
Expected: `OK (14 checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/scripts/brand_lint.py test/brand_lint_test.py
git commit -m "feat(brand): bot-safety and AI-marker checks (B050-B061)"
```

---

### Task 17: locale checks and the `--fix` subset (B070–B073)

**Depends:** [16]

**Implements:** R-08 (codes B070–B073, `--fix`).

**Files:**
- Modify: `plugins/super-ux/scripts/brand_lint.py`
- Modify: `test/brand_lint_test.py`

**Interfaces:**
- Consumes: `Finding`, `run`, `load_sources`.
- Produces: `def check_locales(brand_dir, sources) -> list[Finding]` and
  `def apply_fixes(brand_dir, findings) -> int` returning the number of files
  rewritten. `apply_fixes` handles exactly B024, B041, and B023 (only when the
  string is unchanged and matches exactly one new location).

**Definition of done:** a locale declared in `voice.md` with no
`locales/<code>.md` yields B070; parity below the declared threshold yields B071
with a percentage in the message; `--fix` on a B024 fixture rewrites the file and
a second run reports no findings (idempotence); `--fix` never touches any other
code; `python3 test/brand_lint_test.py` green.

- [ ] **Step 1: write the failing tests**

Append cases for B070, B071, B073, plus an idempotence case that runs
`brand_lint.apply_fixes` twice and asserts the second call returns 0.

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/brand_lint_test.py`
Expected: FAIL — four `expected [...], got []` lines.

- [ ] **Step 3: implement**

Add `check_locales` (B070, B071, B072, B073) and `apply_fixes`. Wire `--fix` in
`main` so it runs `apply_fixes` and then re-runs `run` for the report.

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/brand_lint_test.py`
Expected: `OK (18 checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/scripts/brand_lint.py test/brand_lint_test.py
git commit -m "feat(brand): locale checks and the --fix subset (B070-B073)"
```

---

### Task 18: the `brand-voice` skill

**Depends:** [1, 2, 3, 9]

**Implements:** R-05 — *skill `brand-voice`: modes Init / Calibrate / Update /
Validate plus a status mode when invoked with no task.*

**Files:**
- Create: `plugins/super-ux/skills/brand-voice/SKILL.md`

**Interfaces:**
- Consumes: `references/brand-contract.md`, `references/voice-packs.md`,
  `references/surface-registers.md`, `references/localization.md`.
- Produces: the four mode names other documents reference — `Init`, `Calibrate`,
  `Update`, `Validate`.

**Definition of done:** front matter opens with `Use when`, pairs Russian
triggers beside English ones, is under 1024 characters; the body states that the
pack derives from `foundation.md` and never the reverse, and that a missing
foundation means degraded mode with `Derived-from: inferred`; the no-task status
mode reports pack presence, `voice.md` status, unresolved facts, locale parity,
and open linter findings, then proposes exactly one next action;
`claude plugin validate plugins/super-ux --strict` passes;
`python3 test/sync_references.py` copies the four references into the skill.

- [ ] **Step 1: write the failing check**

Run: `python3 test/validate.py`
Expected: at this point the validator's skill-directory sweep reports the new
directory has no `SKILL.md` once the directory exists; create the directory
first to see it fail.

- [ ] **Step 2: confirm the failure**

Run: `mkdir -p plugins/super-ux/skills/brand-voice && python3 test/validate.py`
Expected: FAIL — a message naming `brand-voice` without `SKILL.md`.

- [ ] **Step 3: write the skill**

Author the front matter and the four modes. Keep the body under 250 lines and
push depth into the references.

- [ ] **Step 4: run the gates**

Run: `python3 test/sync_references.py && python3 test/validate.py && claude plugin validate plugins/super-ux --strict`
Expected: sync prints `brand-voice: 4 contract(s) shipped`; validator `OK`;
plugin validation passes.

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/skills/brand-voice test/validate.py
git commit -m "feat(brand): brand-voice skill — init, calibrate, update, validate"
```

---

### Task 19: the `copywriting` skill

**Depends:** [1, 4, 5, 6, 7, 8, 10]

**Implements:** R-06 — *skill `copywriting`: Write / Edit / Adapt / Humanize;
reads the pack as its first action; never writes to `docs/brand/`.*

**Files:**
- Create: `plugins/super-ux/skills/copywriting/SKILL.md`

**Interfaces:**
- Consumes: `references/brand-contract.md`, `ui-copy.md`, `marketing-copy.md`,
  `channel-playbooks.md`, `seo-aeo-safety.md`, `ai-tells.md`, `store-copy.md`.
- Produces: the four mode names `Write`, `Edit`, `Adapt`, `Humanize`.

**Definition of done:** front matter meets the canon; the body carries the
boundary sentence verbatim — the skill never writes to `docs/brand/`, and a
missing term or fact is reported, never invented; every mode starts by reading
the pack and hands off to `brand-voice` when none exists;
`claude plugin validate plugins/super-ux --strict` passes.

- [ ] **Step 1: write the failing check**

Run: `mkdir -p plugins/super-ux/skills/copywriting && python3 test/validate.py`
Expected: FAIL — a message naming `copywriting` without `SKILL.md`.

- [ ] **Step 2: confirm the failure**

Run: `python3 test/validate.py`
Expected: the same failure, reproduced.

- [ ] **Step 3: write the skill**

- [ ] **Step 4: run the gates**

Run: `python3 test/sync_references.py && python3 test/validate.py && claude plugin validate plugins/super-ux --strict`
Expected: sync prints `copywriting: 7 contract(s) shipped`; validator `OK`.

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/skills/copywriting
git commit -m "feat(brand): copywriting skill — write, edit, adapt, humanize"
```

---

### Task 20: commands

**Depends:** [1]

**Implements:** R-12 — *commands `/brand`, `/brand-init`, `/brand-update`,
`/brand-lint`, `/copy`.*

**Files:**
- Create: `plugins/super-ux/commands/brand.md`, `brand-init.md`,
  `brand-update.md`, `brand-lint.md`, `copy.md`

**Interfaces:**
- Consumes: mode names from Tasks 18 and 19.
- Produces: the five command names referenced by `README.md` and `system-map.md`.

**Definition of done:** `brand.md` is the single entry — inspect, silent repair,
status, menu with exactly one recommended action — and is idempotent;
`brand-lint.md` runs `python3 docs/brand/lint.py`; every command carries a
`description` front-matter field; `python3 test/validate.py` green.

- [ ] **Step 1: write the failing check**

Add to `test/validate.py` the five expected command file names in the existing
commands sweep.

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/validate.py`
Expected: FAIL — five missing-command lines.

- [ ] **Step 3: write the commands**

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/validate.py`
Expected: `OK (n checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/commands test/validate.py
git commit -m "feat(brand): /brand, /brand-init, /brand-update, /brand-lint, /copy"
```

---

### Task 21: catalog — taxonomy tags and BP-182..205

**Depends:** [1, 3, 4, 5, 6, 7, 9, 10]

**Implements:** R-13 — *BP-182..205 minimum, six clusters of at least four,
fields `Do`/`Why`/`Apply when`/`Tags`/`Source`/`Checked`.* R-15 — *new tags in
the taxonomy; the tag `voice` not reused by any new practice.*

**Files:**
- Modify: `plugins/super-ux/skills/references/best-practices.md`

**Interfaces:**
- Consumes: the practice entry shape from `CONTRIBUTING.md`.
- Produces: ids `BP-182` through at least `BP-205`, and the tags `brand-voice`
  `copy` `narrative` `terminology` `channel-physics` `seo` `aeo` `aso` added to
  the taxonomy block at the top of the file.

**Definition of done:** at least 24 practices in one contiguous run from BP-182;
six clusters with at least four each; every entry carries all six fields; no
entry uses the tag `voice`; `python3 test/validate.py` green including the
catalog validator.

- [ ] **Step 1: write the failing check**

Add to `test/validate.py`:

`BP-182` is where the sixth field starts; `BP-001..181` keep five and must not
be touched. The reserved-tag check applies to the whole catalog, old and new.

```python
BRAND_FIRST_BP = 182


def validate_brand_practices() -> None:
    src = ROOT / "plugins/super-ux/skills/references"
    text = read(src / "best-practices.md") or ""
    ids = sorted(int(n) for n in re.findall(r"^#### BP-(\d{3}):", text, re.M))
    if not check(bool(ids), "best-practices.md: no practices parsed"):
        return
    check(
        max(ids) >= 205,
        f"brand practices: catalog ends at BP-{max(ids):03d}, need BP-205 or higher",
    )
    for num in range(BRAND_FIRST_BP, max(ids) + 1):
        body = re.search(rf"^#### BP-{num:03d}:.*?(?=^#### |\Z)", text, re.M | re.S)
        if not check(body is not None, f"BP-{num:03d} is missing"):
            continue
        chunk = body.group(0)
        for field in ("- **Do:**", "- **Why:**", "- **Apply when:**",
                      "- **Tags:**", "- **Source:**", "- **Checked:**"):
            check(field in chunk, f"BP-{num:03d}: missing {field}")
    for num, tags in re.findall(r"^#### BP-(\d{3}):.*?- \*\*Tags:\*\* (.+)",
                                text, re.M | re.S):
        check(
            not re.search(r"(?:^|[ ,`])voice(?:[ ,`]|$)", tags),
            f"BP-{num}: uses `voice`, which is reserved for voice interfaces "
            f"-- the brand tag is `brand-voice`",
        )
```

- [ ] **Step 2: run it and confirm it fails**

Run: `python3 test/validate.py`
Expected: FAIL — `brand practices: highest is BP-181, need BP-205+`

- [ ] **Step 3: write the practices**

Add the eight tags to the taxonomy block, then the six clusters: voice and
consistency, product microcopy, conversion copy, bot safety, channel physics,
localization.

- [ ] **Step 4: run it and confirm it passes**

Run: `python3 test/validate.py`
Expected: `OK (n checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/skills/references/best-practices.md test/validate.py
git commit -m "feat(catalog): BP-182..205 — brand voice, copy, bot safety, locales"
```

---

### Task 22: principles PRN-22..24

**Depends:** [1]

**Implements:** R-14 — *PRN-22, PRN-23, PRN-24.*

**Files:**
- Modify: `plugins/super-ux/skills/references/ux-design-principles.md`

**Interfaces:**
- Consumes: the existing PRN entry shape in the same file.
- Produces: `PRN-22` one voice, many registers; `PRN-23` every claim is
  checkable; `PRN-24` the interface never jokes about the user's loss.

**Definition of done:** three principles present in the file's existing shape;
each names the practice that enforces it; `python3 test/validate.py` green.

- [ ] **Step 1: write the failing check**

```bash
grep -c "^### PRN-2[234]" plugins/super-ux/skills/references/ux-design-principles.md
```
Expected: `0`

- [ ] **Step 2: confirm the failure**

Run the grep above.
Expected: `0`

- [ ] **Step 3: write the principles**

- [ ] **Step 4: confirm**

Run: `grep -c "^### PRN-2[234]" plugins/super-ux/skills/references/ux-design-principles.md`
Expected: `3`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/skills/references/ux-design-principles.md
git commit -m "feat(principles): PRN-22..24 — voice, checkable claims, no jokes about loss"
```

---

### Task 23: wire the new practices into selection

**Depends:** [21]

**Implements:** R-13.

**Files:**
- Modify: `plugins/super-ux/skills/references/practice-selection.md`

**Interfaces:**
- Consumes: the id range and tags from Task 21.
- Produces: selection rows that make BP-182..205 reachable by task type.

**Definition of done:** every id from BP-182 upward appears in at least one
selection row; `python3 test/validate.py` green (its reachability check covers
this).

- [ ] **Step 1: write the failing check**

Run: `python3 test/validate.py`
Expected: FAIL — unreachable-practice failures for the new ids.

- [ ] **Step 2: confirm the failure**

Run the same command.

- [ ] **Step 3: add the selection rows**

- [ ] **Step 4: confirm it passes**

Run: `python3 test/validate.py`
Expected: `OK (n checks)`

- [ ] **Step 5: commit**

```bash
git add plugins/super-ux/skills/references/practice-selection.md
git commit -m "docs(catalog): make BP-182..205 reachable from practice selection"
```

---

### Task 24: regenerate the practices index

**Depends:** [21, 23]

**Implements:** R-13.

**Files:**
- Modify: `plugins/super-ux/skills/references/best-practices-index.md`

**Interfaces:**
- Consumes: the catalog from Task 21.
- Produces: a fresh index that the validator's freshness check accepts.

**Definition of done:** `python3 plugins/super-ux/scripts/bp_index.py` regenerates
the file; `python3 test/validate.py` green including the freshness check.

- [ ] **Step 1: confirm staleness is detected**

Run: `python3 test/validate.py`
Expected: FAIL — a stale-index failure.

- [ ] **Step 2: regenerate**

Run: `python3 plugins/super-ux/scripts/bp_index.py`
Expected: the script prints the practice and tag counts.

- [ ] **Step 3: confirm it passes**

Run: `python3 test/validate.py`
Expected: `OK (n checks)`

- [ ] **Step 4: commit**

```bash
git add plugins/super-ux/skills/references/best-practices-index.md
git commit -m "chore(catalog): regenerate the practices index for BP-182..205"
```

---

### Tasks 25–31: integration

Each task modifies files no sibling in the group touches. All have
**Depends: [1, 17, 18, 19, 20]** unless noted.

| Task | Files | Implements | Deliverable | DoD check |
|---|---|---|---|---|
| 25 | `plugins/super-ux/skills/ux-audit/SKILL.md`, `plugins/super-ux/commands/ux-audit.md` | R-09 | scope `copy`: tone drift, the any-other-SaaS-page test, so-what failures, unproven claims, narrative coherence, pack failure-mode detection, register mismatch — verdicts with `file:line` | `grep -c "copy" plugins/super-ux/skills/ux-audit/SKILL.md` ≥ 1 and the scope table lists it |
| 26 | `plugins/super-ux/scripts/ux_doctor.py`, `test/brand_lint_test.py` | R-10 | the doctor reads `Contract: brand-contract vN` from `docs/brand/` and reports stale or mixed versions alongside the ux contract | a fixture brand dir marked `v0` makes `ux_doctor.py --brief` name it |
| 27 | `plugins/super-ux/skills/references/scenario-format.md`, `templates/scenarios.md` | R-11 | optional `Strings:` field on a scenario, listing `strings.md` keys; absence is never an error | `grep -n "Strings:" plugins/super-ux/skills/references/scenario-format.md templates/scenarios.md` finds both |
| 28 | `plugins/super-ux/skills/references/system-map.md` | R-18 | the brand layer in the pipeline diagram and the file table, with `docs/brand/` and its owner skill | `grep -c "docs/brand" …/system-map.md` ≥ 2 |
| 29 | `bin/super-ux.js`, `package.json` | R-16 | seeds `docs/brand/` from `templates/brand/`, copies `brand_lint.py` to `docs/brand/lint.py`, literal paths only; `files` gains the script | `python3 test/validate.py` payload check green |
| 30 | `cursor/rules/*.mdc`, `templates/claude-rule.md` | R-17 | the brand hard rule in both channels, same shape as the scenario-first rule | `grep -rl "brand" cursor/rules templates/claude-rule.md` finds both |
| 31 | `README.md` | R-18 | the two skills, five commands, `docs/brand/` layer, and the linter documented | `grep -c "docs/brand" README.md` ≥ 1 |

Each ends with `python3 test/validate.py` green and a conventional commit.

---

### Task 32: validator extensions and CI wiring

**Depends:** [21, 24, 25, 26, 27, 28, 29, 30, 31]

**Implements:** R-01, R-15, R-16.

**Files:**
- Modify: `test/validate.py`
- Modify: `.github/workflows/validate.yml`

**Interfaces:**
- Consumes: every check function added by earlier tasks.
- Produces: a single `python3 test/validate.py` run covering brand contract,
  templates, packs, practices, tags, and payload; plus a CI step running
  `python3 test/brand_lint_test.py`.

**Definition of done:** all brand checks are called from `main()`;
`.github/workflows/validate.yml` runs `python3 test/brand_lint_test.py` as its own
step; both commands green locally.

- [ ] **Step 1: confirm the linter test is not in CI**

Run: `grep -c "brand_lint_test" .github/workflows/validate.yml`
Expected: `0`

- [ ] **Step 2: add the step and wire the checks**

- [ ] **Step 3: confirm**

Run: `python3 test/validate.py && python3 test/brand_lint_test.py && grep -c "brand_lint_test" .github/workflows/validate.yml`
Expected: two `OK (…)` lines and `1`.

- [ ] **Step 4: commit**

```bash
git add test/validate.py .github/workflows/validate.yml
git commit -m "test: brand checks in the validator and the linter test in CI"
```

---

### Task 33: reference sync

**Depends:** [32]

**Implements:** R-07 — *ten new references authored and distributed to both
skills.*

**Files:**
- Modify: `plugins/super-ux/skills/brand-voice/references/*`,
  `plugins/super-ux/skills/copywriting/references/*` (generated)

**Definition of done:** `python3 test/sync_references.py` reports a contract count
for every skill and writes zero files on a second consecutive run;
`python3 test/validate.py` green.

- [ ] **Step 1: sync**

Run: `python3 test/sync_references.py`
Expected: one line per skill, then `sync complete (n file(s) written/removed)`.

- [ ] **Step 2: confirm idempotence**

Run: `python3 test/sync_references.py`
Expected: `sync complete (0 file(s) written/removed)`

- [ ] **Step 3: validate**

Run: `python3 test/validate.py`
Expected: `OK (n checks)`

- [ ] **Step 4: commit**

```bash
git add plugins/super-ux/skills
git commit -m "chore: sync brand contracts into every skill that links them"
```

---

### Task 34: end-to-end install test

**Depends:** [33]

**Implements:** R-19 — *`npm pack` → project in /tmp → `python3
docs/brand/lint.py` exits 0 on a fresh seed.*

**Files:**
- None modified. This task produces evidence.

**Definition of done:** a project seeded from a packed tarball contains
`docs/brand/` with all seven files and `lint.py`, and the linter exits 0.

- [ ] **Step 1: pack and seed**

```bash
npm pack && mkdir -p /tmp/bt && tar xzf super-ux-*.tgz -C /tmp/bt
mkdir /tmp/bt/proj && node /tmp/bt/package/bin/super-ux.js --cursor /tmp/bt/proj
```
Expected: the installer lists the seeded files including `docs/brand/`.

- [ ] **Step 2: lint the seeded project**

```bash
cd /tmp/bt/proj && python3 docs/brand/lint.py; echo "exit=$?"
```
Expected: `exit=0`

- [ ] **Step 3: clean up**

```bash
rm -rf /tmp/bt super-ux-*.tgz
```

- [ ] **Step 4: record the evidence in the plan's task list**

Paste both outputs into the build log for the acceptance stage.

---

### Task 35: real-project smoke

**Depends:** [34]

**Implements:** R-20 — *the contract is initialized on one real project that has
`docs/ux`, and the linter is run there.*

**Files:**
- None in this repo. Writes `docs/brand/` inside the chosen target project.

**Definition of done:** one project under `~/DATA` that already has `docs/ux/`
gets `docs/brand/` seeded and calibrated through `brand-voice` Init; the linter
runs there and its output is recorded verbatim; any finding that reveals a
contract defect goes back to Task 1 rather than being worked around in the
linter.

- [ ] **Step 1: pick the target**

```bash
for d in ~/DATA/*/; do [ -d "$d/docs/ux" ] && echo "$d"; done
```
Expected: a list; choose the project with the largest scenario base.

- [ ] **Step 2: seed and calibrate**

Run `brand-voice` Init against that project.

- [ ] **Step 3: lint**

```bash
cd <target> && python3 docs/brand/lint.py; echo "exit=$?"
```
Expected: findings are allowed; a crash, a false B001 on a correct file, or a
check that cannot be satisfied by any legal artifact is a contract defect.

- [ ] **Step 4: record and decide**

Record the output. If a contract defect surfaced, stop and return to Task 1.

---

### Task 36: release preparation

**Depends:** [35]

**Implements:** R-21 (version bump), R-24 (CHANGELOG), R-25 (stale CONTRIBUTING
step).

**Files:**
- Modify: `package.json`, `.claude-plugin/marketplace.json`,
  `plugins/super-ux/.claude-plugin/plugin.json`, `CHANGELOG.md`,
  `CONTRIBUTING.md`

**Definition of done:** all four version locations read `0.30.0`; `CHANGELOG.md`
has a `## 0.30.0 — 2026-08-05` section describing the layer; the family-catalogue
section of `CONTRIBUTING.md` replaces `npm publish --access public` with the
commit-and-tag flow, because `sshlg-skills` publishes from its own CI with
`PUBLISH_NPMJS=true`; `python3 test/validate.py` green.

- [ ] **Step 1: confirm the stale step is present**

Run: `grep -n "npm publish --access public" CONTRIBUTING.md`
Expected: one hit.

- [ ] **Step 2: bump and edit**

- [ ] **Step 3: confirm**

Run: `python3 test/validate.py && grep -c "npm publish --access public" CONTRIBUTING.md`
Expected: `OK (n checks)` then `0`.

- [ ] **Step 4: commit**

```bash
git add package.json .claude-plugin/marketplace.json \
  plugins/super-ux/.claude-plugin/plugin.json CHANGELOG.md CONTRIBUTING.md
git commit -m "chore(release): 0.30.0 — verbal identity layer"
```

---

### Task 37: merge, preflight, tag, push

**Depends:** [36]

**Implements:** R-21 — *release 0.30.0: four-way bump, preflight exit 0,
`--atomic` push, CI green.*

**Definition of done:** `main` contains the work; `python3
test/release_preflight.py` exits 0; branch and tag pushed together with
`--atomic`; both workflows green; the GitHub release exists and npm shows 0.30.0.

Standing instruction #1 from `docs/superpowers/retro.md` governs this task: the
preflight runs **before** the tag, because a clean tree and a green validator
describe the repo and say nothing about the remote.

- [ ] **Step 1: merge to main**

```bash
git checkout main && git merge --no-ff feat/brand-voice-layer
```

- [ ] **Step 2: preflight**

```bash
python3 test/release_preflight.py; echo "exit=$?"
```
Expected: `exit=0` and a printed `--atomic` push line.

- [ ] **Step 3: tag and push together**

```bash
git tag v0.30.0
git push --atomic origin main v0.30.0
```

- [ ] **Step 4: watch CI**

```bash
gh run list --limit 3
```
Expected: `validate` and `release` both succeed.

- [ ] **Step 5: confirm the artifacts**

```bash
gh release view v0.30.0 --json tagName,isLatest
npm view super-ux version
```
Expected: the tag is Latest and npm reports `0.30.0`.

---

### Task 38: family catalogue

**Depends:** [37]

**Implements:** R-22 — *the member pin in `sshlg-skills` is bumped, the launcher
is committed and tagged, and `npx --yes sshlg-skills@latest list` shows 0.30.0.*

**Definition of done:** `skills.json` pins super-ux at 0.30.0; the launcher's own
version, changelog, and tag are bumped; its CI publishes it; the `list` output
names 0.30.0.

- [ ] **Step 1: bump the pin**

```bash
cd ~/DATA/sshlg-skills
grep -n "super-ux" skills.json
```

- [ ] **Step 2: bump, commit, tag**

Edit `skills.json`, the launcher version and its changelog, then tag. Its own
`release.yml` publishes with `PUBLISH_NPMJS=true` — do not run `npm publish`.

- [ ] **Step 3: confirm**

```bash
npx --yes sshlg-skills@latest list | grep super-ux
```
Expected: `0.30.0`

---

### Task 39: refresh local installs

**Depends:** [38]

**Implements:** R-23.

- [ ] **Step 1: update**

```bash
npx --yes sshlg-skills@latest update
```

- [ ] **Step 2: confirm no shadow copies**

```bash
for d in ~/.claude/skills/*/; do n=$(basename "$d"); \
  [ -e ~/.claude/plugins/marketplaces/"$n" ] && echo "SHADOW: $n"; done
```
Expected: no output.

---

### Task 40: documentation, wiki, retrospective

**Depends:** [39]

**Implements:** R-24 — *CHANGELOG, README, wiki, retro stamp.*

**Definition of done:** the project wiki carries the 0.30.0 entry;
`docs/superpowers/retro.md` gains a run stamp, its standing instructions are
pruned against the three retirement triggers before anything is added, and an
entry is written only if the run diverged; the carry-over ledger's counts are
printed beside the acceptance verdict.

- [ ] **Step 1: update the wiki**

Use the `wiki-update` skill against the projects vault.

- [ ] **Step 2: prune, then stamp the retro**

Check standing instruction #1 against its three triggers, log any deletion as one
line under *Retired*, then append the run stamp.

- [ ] **Step 3: write the acceptance**

Create `docs/superpowers/briefs/2026-08-05-brand-voice-layer-acceptance.md` with
the REQ coverage table, the carry-over counts, and the ladder walk.

- [ ] **Step 4: commit**

```bash
git add docs/superpowers
git commit -m "docs: wiki, retro stamp and acceptance for v0.30.0"
```

---

## Self-review

- REQ coverage: 25 in brief, 25 covered, difference ∅
  (R-01 T1,T11,T12,T32 · R-02 T1,T11 · R-03 T1,T12 · R-04 T2 · R-05 T18 ·
  R-06 T19 · R-07 T3–T10,T33 · R-08 T13–T17 · R-09 T25 · R-10 T26 · R-11 T27 ·
  R-12 T20 · R-13 T21,T23,T24 · R-14 T22 · R-15 T21,T32 · R-16 T29,T32 ·
  R-17 T30 · R-18 T28,T31 · R-19 T34 · R-20 T35 · R-21 T36,T37 · R-22 T38 ·
  R-23 T39 · R-24 T36,T40 · R-25 T36)
- Named checks: 41 named, 41 resolve, 0 marked `review` — `test/validate.py`,
  `test/sync_references.py`, `test/release_preflight.py`, `bp_index.py`,
  `claude plugin validate`, `npm pack`, `gh run list`, `gh release view`,
  `npx sshlg-skills` all exist and were run or read during stage 0
- Decisions: checked against the brief's I-table and the options rejected at
  design time — no task re-opens I-1..I-7; the single-release choice (I-2) is
  carried by Task 35 rather than re-litigated
- Cost: 7 new artifact surfaces / 31 linter codes / 25 REQ now, versus
  6 surfaces / ~30 codes / 24 REQ at stage 2 — proportionate; the growth is
  R-25, discovered by verifying the release path against CI
- Hygiene: 8 checks, 2 findings, 0 open — the stale `npm publish` step became
  R-25; the reserved `voice` tag became a validator check in Task 21
- Placeholders: 0 · Ambiguity: 3 found, 3 resolved inline (linter test runner is
  a standalone script not pytest; `--fix` limited to exactly three codes;
  `Checked` applies from BP-182 only)
