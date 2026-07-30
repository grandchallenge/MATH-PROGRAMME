# OZ-RT-APERY-BROW-001

This package audits and formal-replays the exact single-digit Apéry harmonic B-row congruence:

```text
p^3 b_(ap+r) ≡ b_a a_r (mod p)
```

for prime `p >= 5`, `1 <= a < p`, and `0 <= r < p`, under the locked source normalization.

## Evidence

- `DIRECT_PROOF_AUDIT.yaml` records an independent line-by-line audit of the direct p-adic proof and the recurrence/minimal-form representation route.
- `SEMANTIC_CORRESPONDENCE.yaml` maps the paper integral row, double-sum companion, minimal harmonic sum, and recurrence-defined Lean sequence.
- `LEAN_REPLAY.yaml` fixes the pinned source files and five declaration-level replay targets.
- `REVIEW_REGISTER.yaml` records the eight-role disposition.
- `validate.py` and `tests/test_oz_rt_apery_brow.py` fail closed on scope, source-identity, formalization, novelty, and irrationality inflation.

## Formalization boundary

Lean proves the congruence for the exact recurrence-defined classical companion and proves that the minimal harmonic sum equals that sequence. The separate paper equality between the classical double sum and the minimal sum is independently accepted but is not claimed to be kernel-checked.

## Gate

After both target workflow jobs pass against the exact PR head, the Referee may accept the exact theorem and authorize `OZ-RT-LB-INSTANCE-001`.

The package does not authorize the multi-digit modulo-`p^3` law, `NEW_AFTER_AUDIT`, a priority claim, or a new irrationality conclusion.
