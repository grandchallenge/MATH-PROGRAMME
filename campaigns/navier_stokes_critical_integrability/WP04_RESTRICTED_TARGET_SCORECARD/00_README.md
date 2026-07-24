# NS-CI-WP04 — Restricted theorem target scorecard

## Status

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP04`
- Tracker: `MATH-PROGRAMME#61`
- State: `REFEREE_SELECTED_RESEARCH_TARGET_A2`
- Inputs: Referee-promoted WP01 and WP02 artifacts
- Selected target: `NS-CI-R014-A2`
- Selected-target status: `SELECTED_RESEARCH_TARGET_UNPROVED`
- Auxiliary bridge: `NS-CI-R014-E1`
- Re-entry candidate: `NS-CI-R014-D1` only after an independent hypothesis is supplied

WP04 has selected one theorem-grade restricted research target. Selection authorizes analytic proof and falsification work on the statement; it does not assert truth, novelty, or progress on universal global regularity.

WP03, the quantitative concentration observatory, remains closed. No numerical result may validate A2 or the universal theorem.

## Selected statement

Fix `nu>0`. Let `u0` be a smooth divergence-free rapidly decreasing vector field on `R3`, let `T>0`, and let `u` be a Leray–Hopf solution on `[0,T]`. Let `Lambda(t)` be the Cheskidov–Shvydkoy whole-space dissipation wavenumber. Prove or disprove

```math
\Lambda\in L^2(0,T)
\quad\Longrightarrow\quad
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt<\infty.
```

A source-aligned sufficient intermediate target is

```math
\Lambda\in L^2(0,T)
\quad\Longrightarrow\quad
f(t)=\|\omega_{\le Q(t)}(t)\|_{B^0_{\infty,\infty}}\in L^1(0,T).
```

The imported low-mode theorem then gives regularity, while WP02 supplies the critical-integral and continuation interfaces.

## Why A2 was selected

### Exact source gap

The primary source proves on the active set

```math
c\nu\Lambda^2
\lesssim
f(t)
\lesssim
C\Lambda^{5/2}\|u(t)\|_2,
```

regularity from `f in L1_t`, regularity from `Lambda in L5/2_t`, and `Lambda in L1_t` for every Leray–Hopf solution. It explicitly leaves a gap between the universal exponent `1` and sufficient exponent `5/2`.

Under Navier–Stokes scaling,

```math
\Lambda_\lambda(t)=\lambda\Lambda(\lambda^2t),
```

so `Lambda in L2_t` is exactly critical. A bounded targeted source search located no exact whole-space `L2_t` criterion. This is a source-audit statement, not a novelty claim.

### Non-circular statement

The hypothesis is a frequency-threshold observable. It does not assume `L4_tL6_x`, uniform `H1`, or a named LPS/Besov criterion. The full Fefferman data class and universal Leray–Hopf quantifier are preserved.

### Exact adversarial obstruction

The source envelope alone does not prove A2. For the abstract profile

```math
\Lambda(t)=t^{-9/20},
```

`Lambda^2` is integrable on `(0,1)` while `Lambda^(5/2)` is not. Elementary low-frequency Sobolev estimates also produce a product of two unrelated `L1_t` coefficients. The direct estimate

```math
f\lesssim\Lambda^{3/2}D_{\le Q}^{1/2}
```

requires cubic rather than quadratic integrability under standard Hölder closure.

A2 therefore requires genuinely equation-specific information rather than a corrected elementary interpolation.

## Authorized A2 attack lanes

The analytic ledger is maintained in MATHSOLVE issue `#24` and the associated work package.

1. **Source reconstruction:** exact definition, constants, active set, low-mode coefficient, and imported theorem hypotheses.
2. **Dyadic level-set packing:** seek the missing half-power gain between `sum 2^(2k)|E_k|` and `sum 2^(5k/2)|E_k|`.
3. **Excursion and dwell-time control:** derive, rather than assume, temporal restrictions on high-`Lambda` threshold crossings.
4. **Weighted dissipation:** seek a scale-critical correlation, sign, flux, or cancellation estimate avoiding products of unrelated `L1` functions.
5. **Direct high/low decomposition:** exploit high-mode viscous absorption while closing the low-mode term without hidden `H1`.
6. **Abstract packet adversary:** falsify proposed intermediate estimates without presenting kinematic packets as Navier–Stokes solutions.

## Prior-art family dispositions

| Generic family | Disposition | Reason |
|---|---|---|
| `A` dyadic frequency-envelope control | replaced by selected `A2` | generic frequency-localized regularity is established; A2 isolates the critical source gap |
| `B` geometric depletion | rejected | established vorticity-direction and coherence theorem family |
| `C` concentration or sparsity | rejected | established sparseness criteria and an audited unclosed scaling gap |
| `D` flux or commutator compensation | replaced by `D1`, not selected | no independent non-tautological hypothesis has been supplied |
| `E` compact-support extension | replaced by auxiliary `E1` | useful bridge, but the uniform approximation bound carries the substantive regularity content |
| `F` symmetry or structural class | rejected generically | classical or low-leverage regimes |

Recent 2026 arbitrary-swirl and broader global-regularity claims are isolated in MATHFORGE issue `#20`. They are neither accepted prior art nor imported evidence.

## Council scorecard at selection

Scores are 0–5. Higher is better except execution cost, where higher means more costly.

| Dimension | A2 | D1 | E1 |
|---|---:|---:|---:|
| leverage | 5 | 4 | 3 |
| non-circularity | 4 | 1 | 4 |
| prior-art distance | 3 | 3 | 2 |
| scale compatibility | 5 | 4 | 3 |
| proof tractability | 2 | 2 | 4 |
| formalizability | 4 | 3 | 4 |
| falsifiability | 4 | 4 | 3 |
| full-problem relevance | 5 | 4 | 4 |
| information value if false | 5 | 4 | 3 |
| execution cost | 3 | 4 | 2 |

A2 is selected because it has the highest leverage, exact critical scaling, an independently defined hypothesis, a source-identified exponent gap, and high information value even if all natural mechanisms fail.

## Other candidate dispositions

### D1 — retained only under re-entry conditions

D1 seeks a uniform compensated enstrophy inequality

```math
\Pi_N
\le
\theta\nu\|\Delta u^N\|_2^2
+a(t)\|\nabla u^N\|_2^2,
\qquad
\theta<1,\quad a\in L^1_t.
```

This is an interface that already packages the closure. D1 may re-enter only after a separately checkable shell-transfer or commutator hypothesis `H_D` is defined and shown to imply the interface with constants uniform in `N`.

### E1 — auxiliary bridge

E1 records the exact compactness, lower-semicontinuity, quantifier, and weak–strong-uniqueness requirements needed to transfer a critical bound uniform under compactly supported approximation of a fixed Schwartz datum. It may proceed as a bridge lemma but is not the principal target.

## Three-pillar execution

- **MATHFORGE PR `#19`:** source ledger, route terminations, exact A2 scalar and exponent fixtures, and claimed-proof diversion.
- **MATHSOLVE PR `#23` and issue `#24`:** selected theorem statement, proof-obligation DAG, elementary route terminations, and active equation-specific attack lanes.
- **MATHCERT PR `#22`:** scaling, cutoff covariance, quantifier-order, and imported-interface audit. The first kernel-checked slice may address A2 scaling and adversarial exponent fixtures only.

## WP03 boundary

WP03 remains closed by default. A later request may authorize a narrowly specified computation solely to falsify a proposed intermediate packing, excursion, or shell-transfer inequality. Numerical trajectories cannot prove A2, universal finiteness, or absence of blow-up.

## Exit conditions for A2

A2 advances only through one of these governed outcomes:

1. a complete proof survives Verifier, Adversary, Formalist, Amanuensis, and Referee review;
2. a strict narrower lemma with independent value is proved and promoted;
3. the admitted mechanisms terminate with exact gaps, producing a Referee-approved no-go or retirement record.

## Current decision

`NS-CI-R014-A2` is selected as the first restricted research target. It remains unproved. Mechanism generation is open only within its exact analytic lanes. Broad numerical work, theorem claims, novelty claims, and universal regularity claims remain closed.