# OZ-RT-BZ-T3-008

`SYMMETRIC_2D_RAW_JET_DIVERGENCE_001`

This campaign is the mathematically distinct successor to `OZ-RT-BZ-T3-007`. It replaces the one-direction fibre-recurrence ansatz by a direct finite two-dimensional divergence search for the exact locked Brown-Zudilin T3 cell.

The locked target remains

```text
sum_{k=0}^n sum_{l=0}^n T(n,k,l) * (W1(k,l) + 2*w5_sym(n,k,l)) = 0.
```

No T1-top representative is substituted.

## Declared divergence class

The search asks whether

```text
F(n,k,l) = Delta_k P(n,k,l) + Delta_l Q(n,k,l)
```

with

```text
Delta_k P = P(n,k,l) - P(n,k+1,l)
Delta_l Q = Q(n,k,l) - Q(n,k,l+1)
```

and

```text
P = T * k*(n+1-k) / ((k+1)^3*(k+l+1))
      * sum_M p_M(n,k,l) M(n,k,l)

Q = tau(P)
```

where `tau` is exact `k <-> l` exchange and `M` runs over all 198 protected normalized weight-five raw-jet monomials.

The coefficient polynomials `p_M(n,k,l)` are independent for every monomial and are searched at total degrees `0`, `1`, and `2`.

The boundary factors vanish at both ends of the finite square. Therefore an exact cell identity in this class would telescope the double sum directly; it would not require the recurrence propagation used by the earlier fibre routes.

## Why the symmetric search is complete for this class

The exact target is invariant under `tau`. The full two-flux ansatz is closed under `tau`: the coefficient envelope, basis, denominator family, and boundary factors all exchange exactly.

If an unrestricted pair `(P,Q)` solves the declared two-flux problem, then

```text
P_sym = (P + tau(Q))/2
Q_sym = tau(P_sym)
```

also solves it. The field has characteristic zero, and the rank prime `1000003` is odd. Therefore restricting to `Q=tau(P)` loses no solutions inside this declared swap-closed ansatz.

This completeness statement is local to the declared class. It does not exclude different denominator families, larger polynomial coefficient degrees, nonlinear jet representations, or other proof mechanisms.

## Exact bounded result

The first development grids produced equal modular coefficient and augmented ranks:

| coefficient degree | grid | coefficient rank | augmented rank |
|---|---:|---:|---:|
| 0 | `n<=8`, 280 rows | 154 | 154 |
| 1 | `n<=13`, 1,010 rows | 544 | 544 |
| 2 | `n<=18`, 2,465 rows | 1,309 | 1,309 |

Those equal ranks are retained as **finite-grid aliasing only**. They are not candidate evidence.

Expanding the exact grids resolves the aliases:

| coefficient degree | final grid | unknowns | coefficient rank | augmented rank |
|---|---:|---:|---:|---:|
| 0 | `n<=20`, 3,306 rows | 198 | 198 | 199 |
| 1 | `n<=20`, 3,306 rows | 792 | 792 | 793 |
| 2 | `n<=22`, 4,319 rows | 1,980 | 1,980 | 1,981 |

For degree 2, `Q2_RANK_WITNESS.json` retains an explicit 1,980-row full-rank coefficient minor. Adding the exact grid row with index `3674`, point `(21,16,16)`, gives a 1,981-row augmented witness of rank 1,981.

All ranks are over `GF(1000003)`. Every declared rational denominator and every protected raw-derivative normalization multiplier is nonzero modulo that prime. A full-rank coefficient minor and a one-rank-higher augmented minor therefore exhibit rational affine inconsistency for the corresponding declared ansatz.

The bounded terminal is

```text
SYMMETRIC_2D_WEIGHT5_DIVERGENCE_BOUNDED_CLASS_EXHAUSTED
```

This is an exact negative result for the declared coefficient-degree `0..2` symmetric two-dimensional raw-jet divergence class. It is not evidence that T3 is false.

## Claim boundary

The campaign has

```text
proof_effect: NONE
promotion_effect: NONE
T3: OPEN_WITH_CHARACTERIZED_BLOCKER
```

T3 is neither proved nor refuted. T1-top is not substituted for T3. DEPTH, Sharp-12, MATHCERT, `GRAPH_CERTIFIED`, source authority, novelty, priority, publication, patentability, deployment, and commercial claims are unchanged.

## Successor

With the declared symmetric 2D class exhausted, the next mathematically distinct route is

```text
T3_SEQUENCE_RECURRENCE_EXTRACTION_001
```

No theorem effect follows from selecting that successor.

## Reproduction

- `producer.py` regenerates the final affine-rank certificates from the protected 198-monomial basis.
- `verify.py` reconstructs the T3 source cell independently, reverses basis/grid ordering, and replays the affine ranks.
- `validate.py` binds authority, basis/normalization identities, symmetry completeness, finite-grid alias provenance, final ranks, witness identity, terminal state, and nonclaims.
- `Q2_RANK_WITNESS.json` retains the exact degree-2 maximal-minor row witness.
