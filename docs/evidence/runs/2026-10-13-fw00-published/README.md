# FW00: published journey and copy contracts

Source base: `a9a7a614f77a9788e154866396cb9b61215a28a3`.
The [independent four-row review](https://github.com/ssheleg/sshlg-skills/blob/3d4e897/docs/evidence/completion-1013/fw00-owner-closure-review.md) checked canonical contracts, seeds,
U086/B074/B075 and the qualified historical NN/g estimate. Its source/hash ledger
binds every named owner file. [Original FW05 evidence](../2026-10-13-fw05-journey-copy.md)
retains source controls, call-removal negatives and full source gate.

## Published readback

[publication.json](publication.json) is copied byte-for-byte from the
[hub receipt](https://github.com/ssheleg/sshlg-skills/blob/3d4e897/docs/evidence/completion-1013/releases/super-ux-0.59.3.json).
It records release source `f0261f68c1a7222508bd984dc7bac63805dbb76b`, all 33
published files equal to that source, registry integrity and all four successful
[release jobs](https://github.com/ssheleg/super-ux/actions/runs/38341429185).
This supersedes the earlier candidate's pending publication status.

B-025 and B-026 close for their implemented and published contracts only. Unknown
owners remain unassigned, missing old fields remain advisory, and neither metric
truth nor targets, conversion, native/model adherence or installed state is proved.
Original requirement text and old B-011/B-012 history remain unchanged.

## Validation and delivery

Only owner documentation changes. Focused structural/brand checks, unchanged npm
payload comparison and independent diff review precede normal PR integration.
Results are appended below. Next: the hub records this owner revision and performs
separate installed/native acceptance; those results are not borrowed from fixtures.

Focused `python3 -B test/validate.py` first refused the old recorded check count
(5482 versus actual 5489). The documentation adds seven checked references;
`docs/brand/facts.md` now records the measured 5489, and the corrected command
exited 0. Both original outputs are retained as `structural-first.log` and
`structural.log`; the guard was not relaxed. `python3 docs/brand/lint.py` exited 0,
with zero errors and the existing B074 missing-copy-brief advisory (`brand.log`).
All 34 current npm dry-run payload files match accepted owner base byte-for-byte
(`payload-parity.json`). The extra dry-run path is `plugins/super-ux/templates/README.md`, also present
in accepted owner base. Thus current dry-run parity is distinct from the frozen
33-file registry receipt; no new publish is claimed.
No full owner aggregate was repeated for these docs-only dispositions.
