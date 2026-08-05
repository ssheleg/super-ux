# Pipeline retrospective — super-ux

One file per project. Stage 0 of every run reads the standing instructions
below **in full** before its first question.

## Standing instructions

Hard cap: ten. Each carries the run stamp it was written at. Retire an entry
the moment any of its three triggers fires — it became a mechanical check,
the paths or commands it names are gone, or it has not fired in five run
stamps — and log the deletion as one line under *Retired*.

1. **(2026-08-05)** Before tagging any release, run
   `python3 test/release_preflight.py`. A clean tree and a green validator
   describe the repo, not the remote. *(Retire when a hook or CI runs it
   automatically.)* — **fired on v0.28.0, v0.29.0 and v0.30.0: passed all
   three, every push used `--atomic` as it prints. The failure it was written
   for has not recurred.** Checked against all three retirement triggers at
   the v0.30.0 run: still not automated, paths intact, fired within five
   stamps. Kept.

2. **(2026-08-05)** **Never read a gate's verdict through a pipe.** Run the
   gate alone, check `$?`, then print. `python3 test/validate.py | tail -2 &&
   git commit` commits on a red validator, because `tail` exits 0 and `&&`
   reads the pipeline's status, not the gate's. *(Retire when a hook enforces
   it, or after five stamps with no recurrence.)*

## Retired

*(nothing yet)*

## Run stamps

Newest last.

| Date | Task | Diverged? |
|---|---|---|
| 2026-08-05 | Tier-1 audit findings → BP-147..156, audit scope section, catalog validator; v0.27.0 → v0.27.1 | yes — see below |
| 2026-08-05 | Carry-over ledger closed → BP-157..179, PRN-17..21, three optional contract fields, prototype step, catalog index; v0.28.0 | no |
| 2026-08-05 | Contract doctor + the audit's four unclaimed findings; v0.29.0 | no |
| 2026-08-05 | Verbal identity layer — brand-contract v1, brand-voice + copywriting, brand_lint.py, BP-182..205, PRN-22..24; v0.30.0 | yes — see below |

---

## 2026-08-05 — a tag published a tree four releases old

**Symptom.** `git push origin main --follow-tags` was rejected for `main`
(non-fast-forward) but pushed `v0.27.0` anyway. CI accepted the tag, and a
public GitHub release v0.27.0 was built from a tree that predated
0.26.2–0.26.5 — missing the MIT declarations, the `/ux-audit` front-matter
fix, `displayName`, and the npm-publish workflow. Evidence:
`git merge-base --is-ancestor origin/main v0.27.0` → false;
`gh release list` showed v0.27.0 as Latest.

**Surfaced at** stage 8 (release), on the push itself.

**Owned by** stage 0. The harvest recorded "clean, everything pushed" as a
fact about the repository and that fact was never re-verified across the
whole run. Six commits landed on the remote in between.

**Root cause,** two parts that only fail together:

1. Freshness was treated as durable. Every local signal available at tag
   time — clean tree, green validator, four manifests agreeing on the
   number — describes the repo and says nothing about the remote.
2. `git push --follow-tags` is not atomic. A rejected branch ref does not
   roll back the tag that travelled with it, so the repository ends in a
   state where the tag is public and the branch is not. Neither half looks
   wrong on its own.

**What saved it from being worse:** the broken tree predated the workflow
that publishes to npm, so it could not publish itself. npm stayed on 0.26.5
until the corrected 0.27.1. That was luck, not design.

**Fix, by grade.**

- *Mechanical check (taken):* `test/release_preflight.py` — fetches, refuses
  when `HEAD` does not contain `origin/main`, re-checks the four-way version
  sync, and prints the `--atomic` push line. Verified against the incident
  tree in an isolated worktree: it names the exact four missing releases.
- *Documentation (taken):* the release steps in `CONTRIBUTING.md` now run the
  preflight and push branch and tag together with `--atomic`. The same edit
  removed a stale step — `npm publish` had been described as a human 2FA step
  since before CI gained `PUBLISH_NPMJS`.
- *Standing instruction (taken, #1 above):* run the preflight before tagging,
  until something runs it automatically.

**The check that catches it next time:** the preflight's ancestor test. It is
the only one of the four that needs the network, which is exactly why the
failure was invisible without it.

### A second, smaller divergence

Verifying the preflight, I tested it by checking out an old commit *over the
working tree* (`git checkout <sha> -- .`), which silently reverted an
unrelated fix in `cursor/rules/ux-audit.mdc`. Caught immediately by
`git status`, restored, and re-tested in a throwaway `git worktree` instead.
No standing instruction: the lesson is specific enough to be a note, and
notes expire. **Expires 2026-08-19** (two runs): verify destructive-looking
things in a worktree, never over the tree you are working in.

---

## 2026-08-05 — a red gate was committed through, twice removed

**Symptom.** `sshlg-skills` v0.19.0 was tagged and pushed while its own
validator was reporting two failures: the `skills/super-ux` submodule still
pointed at the 0.26.5 commit, and the README table still printed 0.26.5. The
tag is public and superseded by v0.19.1. Evidence: the validator's two lines
appear in the same command output as the successful push.

**Surfaced at** stage 8 (release), one command after it was caused.

**Owned by** stage 8. The gate ran, said no, and was not heard.

**Root cause.** The command was
`python3 test/validate.py 2>&1 | tail -2 && git add -A && git commit …`.
`tail` exits 0 whatever it reads, and `&&` tests the *pipeline's* status, not
the gate's — so a red validator became a green-looking prefix. The output was
even printed; it scrolled past above a successful push line, which is the
worst possible presentation: visible, and structurally ignored.

**Second finding, older and quieter.** The pin the release exists to move had
been stale at 0.26.5 for **four** releases — 0.27, 0.28 and 0.29 all shipped
without touching it, so `npx sshlg-skills list` reported and `update`
installed a version nobody was publishing. `CONTRIBUTING.md` warns about
exactly this in prose. Nothing checks it, which is why prose was not enough.

**Fix, by grade.**

- *Standing instruction (taken, #2 above):* never read a gate's verdict
  through a pipe. Run it alone, check the exit code, then print.
- *Mechanical check (taken):* `sshlg-skills` `test/check_pins.py`, gated in
  CI, released as v0.20.0. It verifies ownership before reporting drift — a
  name that exists is not a name that belongs to us, and `task-pipeline` on
  npm is someone else's 0.1.0. On its first run it found `sheleg-design`
  pinned at 1.3.4 against a published 1.7.0, so the check paid for itself
  before it was merged. C-06 closed.
- *Documentation (taken):* the stale manual `npm publish` step in
  `CONTRIBUTING.md` was replaced this run — every repo in the family has
  published from CI on a `v*` tag since that text was written.

**The check that catches it next time:** the standing instruction, until the
registry comparison exists. Both halves of this run's release were verified
after the fact with `npx sshlg-skills@latest list`, which is the assertion the
pipeline should have made before the tag rather than after it.
