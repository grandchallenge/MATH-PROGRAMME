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

## Purpose

WP01 records exact reasons that common proposed shortcuts fail. Its function is eliminative: it prevents the campaign from repeatedly spending effort on arguments already blocked by function-space geometry, inadmissible weak manipulations, nonuniform approximation constants, quantifier drift, or trust-boundary erasure.

A failed proof route is not evidence that the open statement is false.

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
| `FP-004` | feed Grönwall back into the target | reduces to `X\le Ke^{cX}`, which gives no upper bound | circular closure |
| `FP-005` | test every weak solution by `-\Delta u` | `\Delta u` and the time pairing are unavailable in the energy class | test admissibility |
| `FP-006` | pressure cancellation validates the test | algebraic cancellation does not create missing regularity | formal manipulation |
| `FP-007` | fixed Galerkin smoothness passes to the limit | Bernstein produces an `N^4` critical-norm loss | cutoff nonuniformity |
| `FP-008` | mollification passes critical control | smoothing produces an `\varepsilon^{-4}` loss | regularization nonuniformity |
| `FP-009` | compact support covers the official data class | `C_c^\infty\subsetneq\mathcal S`; extension requires uniform stability | data-class drift |
| `FP-010` | finite numerical values prove continuum finiteness | no verified resolution-uniform critical bound | numerical overclaim |
| `FP-011` | formalized assumption is a formalized proof | kernel checks only the implication from the imported assumption | trust-boundary erasure |
| `FP-012` | `(4,6)` may be reversed | `L^6_tL^4_x` has Serrin sum `13/12`, not `1` | notation drift |
| `FP-013` | interior regularity is the global theorem | initial-time, decay, energy, and global uniqueness bridges are missing | theorem-scope drift |
| `FP-014` | one selected solution proves the universal claim | existential construction needs weak–strong uniqueness to cover every solution | quantifier drift |

The complete calculations and machine-readable fixtures live in the provider artifacts.

## Adversarial semantic determination

The Verifier replayed `FP-001`, `FP-002`, `FP-007`, `FP-008`, and `FP-012`. The exact arithmetic, interpolation, cutoff, smoothing, and exponent-order calculations are correct.

The Adversary attempted to evade each fixture without changing its hypotheses. Every attempted evasion either triggered another fixture or introduced a genuinely new estimate or theorem interface. No fixture was found to reject a valid route under its stated assumptions.

The numerical fixture is interpreted narrowly: finite values from fixed finite-dimensional approximations do not imply a resolution-uniform continuum theorem. It does not prohibit verified a posteriori numerical analysis or simulations used to falsify mechanisms.

The atlas is extensible, not exhaustive. New failed routes receive new fixture identifiers.

## Required response to a triggered fixture

When a proposed route triggers a fixture, the route record must state:

1. the exact failed inference;
2. the fixture identifier;
3. whether the route is terminated or narrowed;
4. the nearest viable restricted statement;
5. any new estimate required to bypass the obstruction;
6. how that estimate respects Navier–Stokes scaling;
7. why the replacement is not already equivalent to assuming regularity.

Passing the atlas does not validate a route. It establishes only that these known failure modes have been avoided.

## Claims

### WP01-C001

The standard energy estimates do not imply the target through finite-measure inclusion or interpolation.

Status: `PROVED_IN_PACKAGE` by `FP-001` and `FP-002`.

### WP01-C002

Fixed-cutoff and fixed-mollification finiteness do not provide a cutoff-uniform continuum estimate.

Status: `PROVED_IN_PACKAGE` by the explicit `N^4` and `\varepsilon^{-4}` losses in `FP-007` and `FP-008`.

### WP01-C003

Testing by `-\Delta u` and pressure cancellation are conditional strong-level manipulations, not unconditional Leray–Hopf estimates.

Status: `PROVED_AS_FUNCTION_SPACE_DIAGNOSTIC`; approximation details remain governed by WP02.

### WP01-C004

A compact-support theorem is not the full-data theorem without a separate uniform extension bridge.

Status: `PROVED_AS_LOGICAL_DATA_CLASS_BOUNDARY`.

### WP01-C005

Finite-dimensional numerical or formal artifacts cannot promote the open continuum claim without explicit uniform error or imported-assumption disclosure.

Status: `GOVERNANCE_BOUNDARY`.

## Cross-document integration

Checked against:

- WP00's corrected Fefferman full data class and one-way correspondence language;
- theorem-spine nodes `NS-CI-C004`, `O005`, `L008`, `L010`, `B011`, and `T013`;
- WP02 entries `CR-003` through `CR-011`;
- MATHCERT's provenance-bearing imported-interface boundary.

No blocking conflict remains.

## What WP01 rules out

WP01 rules out only the listed arguments in their listed forms. It does not rule out:

- equation-specific cancellations;
- scale-summable frequency envelopes;
- geometric depletion of vortex stretching;
- a new monotone or coercive quantity;
- an independently small critical quantity;
- a rigorous data-class extension theorem;
- verified numerical diagnostics used for falsification rather than proof.

## Acceptance record

- [x] Exact scalar exponent witness supplied and replayed.
- [x] Energy interpolation calculation supplied and replayed.
- [x] Hidden strong-norm and circularity diagnostics reviewed.
- [x] Galerkin and mollification losses displayed and replayed.
- [x] Data-class, theorem-scope, and quantifier drift reviewed.
- [x] Numerical and formal trust boundaries reviewed.
- [x] Verifier review complete.
- [x] Adversary scope review complete.
- [x] Amanuensis consistency review complete.
- [x] Referee promotion approved.
- [x] Provider Forge CI passed in workflow run `30058521633`.
- [x] Programme policy CI passed in workflow run `30058238368`.

## Promotion decision

WP01 is the canonical route-rejection atlas for `NS-CI-001`.

This promotion does not open mechanism generation automatically. A future mechanism package must cite the fixtures it has checked, identify its new estimate, and pass its own prior-art, scaling, and Referee gates.

## Next executable step

Keep the atlas active as an admission gate for future route records. Add new fixtures when a materially distinct false proof is encountered. WP01 itself has no blocking review debt.