# NS-CI-WP01 — Referee-promoted false-proof atlas

## Status

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP01`
- Parent: `MATH-PROGRAMME#55`
- Provider: `grandchallenge/MATHFORGE#17`
- State: `REFEREE_PROMOTED_ROUTE_REJECTION_ATLAS`

WP01 is an eliminative artifact. It proves only that specified arguments fail in their stated forms. It does not refute universal critical integrability, imply blow-up, or validate a route merely because that route passes the atlas.

## Protected target

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt<\infty
```

for every finite `T`, every smooth divergence-free rapidly decreasing datum in the full Fefferman class, and every corresponding Leray–Hopf solution.

## Canonical fixtures

| ID | Rejected route | Exact obstruction |
|---|---|---|
| `FP-001` | finite time gives `L²_t\to L⁴_t` | `t^{-1/3}\in L²(0,1)\setminus L⁴(0,1)` |
| `FP-002` | energy interpolation reaches `(4,6)` | it reaches `(4,3)`; `p=6` forces `q=2` |
| `FP-003` | insert `\sup_t\|u\|_6` | hidden `L^\infty_tH^1_x` assumption |
| `FP-004` | circular Grönwall closure | `X\le Ke^{cX}` gives no upper bound |
| `FP-005` | test arbitrary Leray–Hopf solutions by `-\Delta u` | test and time pairing unavailable |
| `FP-006` | pressure cancellation supplies admissibility | algebra does not create regularity |
| `FP-007` | fixed Galerkin finiteness passes to the limit | `N^4` loss |
| `FP-008` | mollified finiteness passes to the limit | `\varepsilon^{-4}` loss |
| `FP-009` | compact support equals full rapid decay | strict subclass; extension theorem missing |
| `FP-010` | finite numerical outputs prove continuum finiteness | no resolution-uniform verified bound |
| `FP-011` | formalized premise is a proved premise | kernel checks implication only |
| `FP-012` | swap time and space exponents | reversed Serrin sum is `13/12` |
| `FP-013` | interior theorem is the global theorem | initial-time/global bridges missing |
| `FP-014` | one selected solution proves a universal claim | weak–strong uniqueness bridge required |

## Adversarial findings

Exact fixtures replay in MATHFORGE CI. FP-010 is explicitly limited to inference from fixed finite-dimensional approximations; verified a posteriori analysis and simulations used for mechanism falsification remain permitted. Counter-route attempts either trigger another fixture or add a genuinely new estimate.

The atlas is extensible, not exhaustive.

## Route-admission rule

A triggered fixture requires the route record to state the failed inference, fixture ID, termination or narrowing decision, nearest viable restricted statement, new estimate required, scaling behavior, and non-circularity argument.

## Integration and promotion

WP01 agrees with WP00, WP02, and MATHCERT. Verifier, Adversary, Amanuensis, and Referee reviews are complete; no blocking obligations remain. Merge this governance PR before WP02; the WP02 branch carries the combined artifact ledger.
