# OZ-RT-LB-INSTANCE-001 — Franel

This package supplies the first complete concrete application of the abstract Theorem LB.

For every prime `p` with `p != 2` and every `a,r<p`, the target is

```text
p^2 bFranel(a p+r) ≡ bFranel(a) franel(r) (mod p),
```

where

```text
franel(n)  = Σ_k C(n,k)^3,
bFranel(n) = Σ_k C(n,k)^3 [(1/4)H_k^(2) + (3/4)H_k^2 - (3/4)H_k H_(n-k)].
```

## Evidence

- `HYPOTHESIS_AUDIT.yaml` records complete H1, H2, H3, H4, H4c, Hw, and H5 discharge.
- `SEMANTIC_BOUNDARY.yaml` fixes the exact explicit-sum statement and the recurrence-equivalence boundary.
- `LEAN_REPLAY.yaml` pins the abstract theorem and Franel instance declarations.
- `REVIEW_REGISTER.yaml` records the eight-role verdict.
- `validate.py` and `tests/test_oz_rt_lb_instance.py` reject scope, source, hypothesis, recurrence, novelty, and irrationality inflation.

## Boundary

Lean proves the explicit-sum theorem. The source reports numerical agreement with a recurrence-defined Franel second solution, but that equality is not formalized and is not part of this theorem disposition.

Successful exact-head CI and merge authorize `OZ-RT-BZ-T3-001`. They do not authorize sharp-12, novelty, priority, or irrationality claims.
