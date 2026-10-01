# DC-01: display-copy guard repair

Prepared from super-ux `18a4be53cd0f6b0e1a88b9457dda97c58b485a9a`
(version 0.56.2). `npm view super-ux version` returned 0.56.2 on 2026-10-01.
Candidate: 0.56.3. Integration, release and installed-channel refresh belong to
the coordinator; this report does not claim they happened.

## Diagnosis before implementation

| Verdict | Finding and evidence | Repair |
|---|---|---|
| GAP | AT-07 already prohibited terminal title periods, but `check_ai_tells` inspected only front matter and Markdown; `title_full_stop` exempted several sentences | semantic HTML heading parser and staccato/markup fixtures |
| GAP | HTML registry locations passed through quoted-code extraction, so attributes were read as copy | static visible blocks for B021/B022 |
| GAP | Declared glob matching nothing returned no finding; documented brace patterns were passed to pathlib unchanged | B009 coverage error and brace expansion |
| GAP | Default warnings exit 0, so an advisory run could be called a passing policy gate | repeatable/comma-separated `--fail-on`, unknown-code rejection |
| GAP | Copywriting named a project-local lint script that standalone installs may not have | resolve actual installed/project script, state missing coverage |
| PASS | Pre-change reproducer executed against the base implementation | `red.txt`: 9 tests, 6 assertion failures, 1 unrecognized-flag error, 2 negative controls passing |
| NOT-RUN | Agent/model outcome improvement | deterministic code tests do not measure model behavior |

## Implementation and boundaries

`plugins/super-ux/scripts/brand_lint.py` and its project-side mirror now inspect
HTML h1–h6, nested inline text, entities and explicit line breaks. Markdown ATX
headings retain source lines and inline formatting. B026 and B063 no longer
exempt staccato titles. Paragraph sentences, questions, ellipses, abbreviations,
versions and URLs are controls, not candidates for automatic stripping.

HTML excludes script, style, template, noscript, head and source-hidden elements;
`aria-hidden` alone stays visible. External CSS, JavaScript and responsive visual
layout require browser review. HTML attributes are outside this visible-copy
scan; accessible-name parity remains a separate review. B063 applies to declared
marketing/store sources. Project hero summaries and captions may use a stricter
local guard without changing every paragraph's punctuation.

Sources use comma brace expansion and de-duplicate overlapping patterns per key.
Unmatched non-robots globs are errors. Seed templates already instructed replacing
placeholder Sources; the former silent clean result is now explicitly refused.
The own UX chain records that behavior. B050 continues to own robots policy.

The canonical reference and copied skill closure carry the same rule. B060's
contract row was corrected to its existing advisory behavior; no authorship
verdict is inferred. Default warning behavior and the JSON findings array stay
compatible. `--fail-on` changes exit policy, not which advice is shown.

## Checks

| Command | Result |
|---|---|
| `python3 test/display_copy_test.py` | exit 0, 15 focused tests; pre-fix 9-case baseline in `red.txt` failed as described above |
| `python3 test/brand_lint_test.py` | exit 0, 103 checks |
| `python3 test/validate.py` | exit 0, 4826 checks; external agent-registry count and umbrella routed-trigger integration explicitly unlooked in this isolated member |
| `python3 docs/ux/lint.py` | exit 0, own chain consistent |
| `python3 docs/brand/lint.py` | exit 0, 0 errors and 1 existing B022 advisory (`claude --version` literal) |
| `npm test` | exit 0: validators, focused tests, UX 145 checks, installer 10 cases and all audit regression scripts |
| `python3 test/sync_references.py` | canonical references/templates copied into distributed closure |
| `claude plugin validate . --strict` | exit 0, marketplace accepted |
| `claude plugin validate plugins/super-ux --strict` | exit 0, plugin accepted |
| `npx --yes skills add . --list` | exit 0, 7 real skills |
| `npx --yes skills add <checkout> --skill copywriting --agent codex --yes --copy` from an isolated temporary project | exit 0, 13 installed files byte-identical to the canonical copywriting skill and its closure |
| `audit_skill.py <isolated-install>/copywriting --house --json` | exit 0, 19 PASS, no GAP; 196 lines, 2668 tokens (tiktoken) |
| `npm pack --dry-run --json` and temporary `npm pack` extraction | exit 0, 33-entry installer payload; packed linter byte-identical, standalone linter/installer help accepted; skills ship through the separate skills/plugin channel |
| `claude plugin eval plugins/super-ux --no-publish --trust-plugin --runs 1 --max-cost-usd 1` | exit 1, no runner-format eval cases under the plugin; no model run, no model-quality claim |
| `git diff --check` | exit 0 |

The Cursor copywriting rule had also missed the heading rule and retained an
obsolete blanket ban on editing `docs/brand/`, contradicting its strings registry
instruction. It now matches canonical file ownership and coverage/gate guidance;
`/copy` uses the same closing checklist. A channel-parity fixture guards the
critical wording. This is measured instruction parity, not measured model behavior.

Temporary absolute checkout paths in `red.txt` are normalized to `<checkout>`;
assertions and exception text are preserved.

## Consumer follow-up before integration

The coordinator ran the candidate against passioncode-ai.github.io and found
concatenated adjacent navigation/CTA labels. The focused fixture reproduced that
failure (`anchor-red.txt`), while a negative control kept inline prose links
whole. Boundaries now separate adjacent structural links without splitting
paragraph/heading links or ordinary prose around links.

The initial HTML B022 sweep was also too broad for an interface registry: it
flagged all visible marketing paragraphs on a file containing one registered
action. B022 now considers explicit links, controls, labels and status/alert
roles. B021 still checks any explicitly registered string against full visible
text, even in a heading-only file, and an attribute value cannot satisfy it.
Full visible copy remains available to documents/B063. A standalone current-
directory token (`git add .`, `<code>cd .</code>`) is not a decorative full stop.

`test/display_copy_test.py` now has 20 passing cases. The consumer scan at website
`f31b14a0b4a3fd4f4646e5ead64abe79cabb73f7` returns 0 errors and 185 B022 advisory
findings after narrowing the sweep. These are candidates for registry review,
not 185 proven missing decisions: repeated navigation, decorative arrow text and
CSS-styled whole-card link names require interpretation. The canonical copywriting gotcha also requires reapplying current punctuation
policy when restoring historical copy: an old snapshot is not an exception. The final house audit returns 19 PASS,
198 lines and 2694 tokens for that skill; closure sync changes zero files.
No website registry rows were added, and this is not called a clean brand review. The earlier B005 warning
is absent in the later consumer tree; that website calibration changed separately.

## Next task

Independently review this branch and run release preflight from its clean commit.
Then apply the family integration policy (PR/hosted checks, merge, annotated tag,
release receipts) and update the umbrella pins before refreshing installed
channels. Do not call the candidate a deployed skill until those receipts exist.
