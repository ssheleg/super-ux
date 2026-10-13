# R30: retain the existing board guard's negative controls

Base: accepted `f974e7f212ddf2482569ab8399091f5d8336c31c`.
The [independent eleven-owner map](https://github.com/ssheleg/sshlg-skills/blob/df8cc795f861ded3537fb575002cb86422ced9d1/docs/evidence/completion-1013/r30-eleven-owner-closure.md)
found working UX board guards with centrally retained plants, but no owner-owned
regression that repeats the duplicate-id and extra-cell defects.

This task adds those two cases to the existing public-validator subprocess harness.
It selects an existing row, requires a unique source match and changed plant bytes,
then requires exit 1 plus the intended owner diagnostic. The healthy case and
three existing release cases stay. The production parser is unchanged; its bounded
header/row syntax and escaped-pipe limitations are not expanded by these controls.
The fixture owns and removes each copied tree; the source checkout is not planted.

Validation and independent review are recorded below before normal integration.
This repository-only change needs no version, release or installed update.

The first focused public entry run passed six actual validator processes: healthy0,
duplicate-id1, extra-cell1, removed ancestry1, shallow checkout1, and quoted full
depth0. Every refusal required its intended diagnostic; `process-first.json`
retains complete output. A header-only correction replaces the old prose divergence
claim with `diverges: none`, because the mechanism's uppercase constants do not
differ. The case-specific explanation remains a normal comment. Final exact-source
replay and payload parity follow before admission; no broad suite claim is borrowed.

The new handoff link adds one checked document reference. The first structural
run correctly refused the recorded5489 versus actual5490; `structural-first.txt`
retains that failure. The measured fact is updated to5490, without changing the
validator or removing the added check. This is documentation propagation, not a
new production guard or a claim of broader parser support.
