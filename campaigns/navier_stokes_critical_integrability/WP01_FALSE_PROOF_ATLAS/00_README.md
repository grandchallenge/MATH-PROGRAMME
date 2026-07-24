# NS-CI-WP01 — False-proof atlas

## Metadata

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP01`
- Parent tracker: `MATH-PROGRAMME#55`
- MATHFORGE tracker: `grandchallenge/MATHFORGE#16`
- Provider PR: `grandchallenge/MATHFORGE#17`
- Primary provider artifacts:
  - `grandchallenge/MATHFORGE:reports/discovery/ns_ci_001/false_proof_atlas.md`
  - `grandchallenge/MATHFORGE:reports/discovery/ns_ci_001/false_proof_fixtures.json`
  - `grandchallenge/MATHFORGE:reports/discovery/ns_ci_001/WP01_ADVERSARIAL_SEMANTIC_REVIEW.md`
- Result class: exact negative-route audit
- Promotion state: `REFEREE_PROMOTED_ROUTE_REJECTION_ATLAS`
- Promotion date: 2026-07-23

## Purpose and claim boundary

WP01 records exact reasons that common proposed shortcuts fail. Its function is eliminative: it prevents repeated investment in arguments already blocked by function-space geometry, inadmissible weak manipulations, nonuniform approximation constants, quantifier drift, or trust-boundary erasure.

A failed proof route is not evidence that the open statement is false. Passing the atlas does not validate a proposed mechanism.

## Canonical target protected

For every smooth divergence-free rapidly decreasing whole-space datum and every corresponding Leray–Hopf solution, determine whether

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt<\infty
```

for every finite `T>0`.

## Fixture ledger

| ID | False route | Exact obstruction | Protected boundary |
|---|---|---|---|
| `FP-001` | finite time upgrades `L²` to `L⁴` | `t^{-1/3}\in L²(0,1)\setminus L⁴(0,1)` | energy exponent gap |
| `FP-002` | energy interpolation yields `L⁴_tL⁶_x` | interpolation gives `L⁴_tL³_x`; `p=6` forces `q=2` | interpolation geometry |
| `FP-003` | insert `\sup_t\|u\|_6` | requires unproved `L^\infty_tH^1_x` | hidden strong norm |
| `FP-004` | feed Grönwall back into the target | `X\le Ke^{cX}` gives no upper bound | circular closure |
| `FP-005` | test every weak solution by `-\Delta u` | test and time pairing unavailable in the energy class | test admissibility |
| `FP-006` | pressure cancellation validates the test | cancellation does not create missing regularity | formal manipulation |
| `FP-007` | fixed Galerkin smoothness passes to the limit | Bernstein produces an `N^4` critical-norm loss | cutoff nonuniformity |
| `FP-008` | mollification passes critical control | smoothing produces an `\varepsilon^{-4}` loss | regularization nonuniformity |
| `FP-009` | compact support covers the official data class | strict subclass; extension requires uniform stability | data-class drift |
| `FP-010` | finite numerical values prove continuum finiteness | no verified resolution-uniform critical bound | numerical overclaim |
| `FP-011` | formalized assumption is a formalized proof | kernel checks only implication from the imported premise | trust-boundary erasure |
| `FP-012` | `(4,6)` may be reversed | reversed Serrin sum is `13/12`, not `1` | notation drift |
| `FP-013` | interior regularity is the global theorem | initial-time, decay, energy, and uniqueness bridges missing | theorem-scope drift |
| `FP-014` | one selected solution proves the universal claim | existential construction needs weak–strong uniqueness | quantifier drift |

## Adversarial determination

The exact fixtures were replayed in MATHFORGE CI. FP-010 was narrowed to the correct claim: finite outputs from fixed finite-dimensional approximations do not establish a resolution-uniform continuum theorem. Verified a posteriori analysis and simulations used for mechanism falsification remain permitted.

Counter-route attempts either triggered another fixture or introduced a genuinely new estimate or theorem interface. The atlas is extensible rather than exhaustive.

## Route-admission rule

A route triggering a fixture must record the failed inference, fixture ID, termination or narrowing decision, nearest viable restricted statement, required new estimate, its scaling behavior, and why it is not equivalent to assuming regularity.

## Cross-document integration

WP01 agrees with WP00's Fefferman data class and one-way correspondence language, WP02's strong-level and integrated weak–strong boundaries, and MATHCERT's imported-interface policy. No blocking conflict remains.

Merge order is WP01 governance PR first, followed by WP02. The WP02 branch carries the combined artifact-ledger state.

## Acceptance record

- [x] Exact arithmetic and scaling fixtures replayed.
- [x] Adversarial scope review complete.
- [x] Amanuensis cross-document review complete.
- [x] Referee promotion approved.
- [x] Provider Forge CI passed on the reviewed head.
- [x] Programme policy CI required green on the promoted governance head.

## Promotion decision

WP01 is the canonical route-rejection atlas for `NS-CI-001`. It has no blocking review debt. Future mechanism packages must cite the fixtures checked and pass separate prior-art, scaling, analytic, and Referee gates.