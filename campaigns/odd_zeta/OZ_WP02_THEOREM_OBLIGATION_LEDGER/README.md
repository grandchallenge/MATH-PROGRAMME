# OZ-WP02 — Source-normalized theorem and proof-obligation ledger

This package fixes the theorem statements, normalization maps, proof effects, dependency DAGs, and promotion gates for the ordered odd-zeta research programme.

## Files

- `THEOREM_LEDGER.yaml` — exact theorem scopes and current dispositions;
- `NORMALIZATION_REGISTER.yaml` — symbol, modulus, prime-range, and factor-six locks;
- `PROOF_OBLIGATIONS.yaml` — dependency graph and lane-specific completion gates;
- `validate.py` — deterministic fail-closed validation;
- `REVIEW_REGISTER.yaml` — eight-role review.

## Validation

```bash
python3 campaigns/odd_zeta/OZ_WP02_THEOREM_OBLIGATION_LEDGER/validate.py
```

Successful exact-head CI and merge authorize `OZ-RT-APERY-BROW-001`. The ledger itself proves no open theorem and authorizes no novelty or irrationality claim.
