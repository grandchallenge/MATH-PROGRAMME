# NS-CI-WP04 — Restricted theorem target scorecard

## Status

- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP04`
- Tracker: `MATH-PROGRAMME#61`
- State: `SHORTLIST_INTEGRATED_PROVISIONAL_LEAD_A2`
- Inputs: Referee-promoted WP01 and WP02 artifacts
- Provisional shortlist: `A2`, `D1`, `E1`
- Provisional lead: `NS-CI-R014-A2`
- Referee selection: none
- Output: one selected target `NS-CI-R014`, or an explicit no-selection decision

WP04 admits and ranks restricted theorem targets. It does not authorize broad mechanism generation, broad numerical experimentation, or continuum regularity claims.

WP03, the quantitative concentration observatory, remains closed. No current candidate has an approved computational task that could bear on its theorem status.

## Admission contract

Every candidate must provide:

1. domain, forcing, viscosity, initial-data class, solution class, and quantifiers;
2. exact additional hypothesis or restricted regime;
3. theorem conclusion and relationship to

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt;
```

4. Navier–Stokes scaling class of every hypothesis and conclusion;
5. WP01 fixture-clearance record;
6. WP02 theorem interfaces consumed;
7. nearest known theorem and source-audit state;
8. proof-obligation DAG;
9. strongest anticipated counterexample or failure mode;
10. falsification protocol;
11. formalization boundary;
12. proof that the candidate is narrower than the open theorem rather than a restatement of regularity.

## Hard rejection rules

A candidate is rejected before scoring if it:

- triggers an unresolved WP01 fixture;
- assumes `L^4_tL^6_x`, `L^\infty_tH^1_x`, or an equivalent regularity norm without a strictly weaker independently checkable hypothesis;
- hides a scale-breaking constant needed uniformly in a cutoff or mollification parameter;
- silently narrows the Fefferman data class or universal Leray–Hopf quantifier;
- relies on an imported theorem without source and hypothesis normalization;
- is already a classical theorem in the stated regime and offers no distinct bridge or quantitative refinement;
- uses numerical evidence as continuum proof;
- uses a formal interface as proof of its imported analytic fields.

## Prior-art triage result

MATHFORGE terminated the generic candidates as follows:

| Generic family | Disposition | Reason |
|---|---|---|
| `A` dyadic frequency-envelope control | replaced by `A2` | frequency-localized regularity is an established and crowded family; an exact critical gap was required |
| `B` geometric depletion | rejected | vorticity-direction and coherence criteria are established theorem families |
| `C` concentration or sparsity | rejected | geometric sparseness criteria are established, and audited work records the remaining scaling gap |
| `D` flux or commutator compensation | replaced by `D1` | analytic substrate exists, but a scale-uniform independent condition must be stated |
| `E` compact-support extension | replaced by `E1` | density alone does not identify every Leray–Hopf solution; uniformity and weak–strong identification must be explicit |
| `F` symmetry or structural class | rejected generically | classical regimes are known or too remote from the full theorem |

Recent 2026 claims concerning arbitrary-swirl axisymmetry and broader global regularity have been diverted to MATHFORGE issue `#20`. They are neither accepted prior art nor evidence that any theorem is closed.

## Provisional shortlist

### `NS-CI-R014-A2` — Critical dissipation-wavenumber criterion

Let `Lambda(t)` be the Cheskidov–Shvydkoy dissipation wavenumber. Determine whether

```math
\Lambda\in L^2(0,T)
\quad\Longrightarrow\quad
I_T(u)<\infty.
```

Under Navier–Stokes scaling,

```math
\Lambda_\lambda(t)=\lambda\Lambda(\lambda^2t),
```

so `Lambda in L2_t` is critical. The known audited source supplies a stronger sufficient condition `Lambda in L5/2_t` and universal a priori information `Lambda in L1_t`.

The decisive missing estimate is not the elementary frequency split. Low-frequency bounds lead to products such as

```math
\|u_{\le Q}\|_6^4
\lesssim
\Lambda^2\|u\|_2^2\|\nabla u\|_2^2,
```

and the product of `Lambda^2 in L1_t` with the energy dissipation density in `L1_t` is not automatically integrable. A2 therefore requires a new equation-specific decorrelation, weighted dissipation, or frequency-transfer estimate. Any proof that multiplies unrelated `L1` quantities triggers WP01.

**State:** admissible, provisional lead, unproved, exact-prior-art confirmation pending.

### `NS-CI-R014-D1` — Scale-uniform shell-flux compensation

For `u^N=P_{<=N}u`, define

```math
\Pi_N(t)=\langle P_{\le N}((u\cdot\nabla)u),-\Delta u^N\rangle.
```

The desired interface is

```math
\Pi_N
\le
\theta\nu\|\Delta u^N\|_2^2
+a(t)\|\nabla u^N\|_2^2,
\qquad
\theta<1,\quad a\in L^1_t,
```

uniformly in `N`. This interface closes by Grönwall, but it is not itself an admissible hypothesis. D1 remains blocked until an independently checkable shell-transfer or commutator condition `H_D` is stated and shown to imply the interface.

**State:** shortlisted with formulation debt; not presently selectable.

### `NS-CI-R014-E1` — Uniform compact-support-to-Schwartz bridge

For a fixed Schwartz datum, assume divergence-free compactly supported approximants converge in explicit initial-data topologies and their global strong solutions satisfy a critical bound uniform in the approximation index. Prove that compactness, lower semicontinuity, LPS regularity, and weak–strong uniqueness transfer the bound to every Leray–Hopf solution from the Schwartz datum.

E1 is a bridge theorem. Pointwise finiteness for each approximant does not suffice; the quantifier order must be

```text
for every T, there exists K_T, for every n,
```

rather than

```text
for every n, there exists K_(T,n).
```

**State:** admissible bridge fallback; high tractability but limited mechanism leverage.

## Preliminary Council scorecard

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

The scorecard is not a vote. A2 leads because it is critical, independently stated, source-anchored, and exposes a precise missing estimate. D1 is blocked by a missing independent hypothesis. E1 is the tractable bridge fallback.

## Proof-obligation architecture

```text
MATHFORGE prior-art and claim triage
  -> A2 exact-source confirmation
  -> A2 adversarial reduction attempts
  -> MATHCERT scaling and statement audit
  -> Verifier assessment of the missing A2 weighted estimate
  -> Referee comparison: A2 vs E1, with D1 blocked unless H_D is supplied
  -> select at most one NS-CI-R014 or record no selection
```

The full candidate DAGs are maintained in MATHSOLVE PR `#23`; scaling and formalization boundaries are maintained in MATHCERT PR `#22`.

## Remaining blocking obligations

1. Confirm by targeted source audit that the exact `Lambda in L2_t -> I_T<infinity` criterion is not already established.
2. Attempt to reduce A2 to a known Besov/LPS criterion or a WP01 failure.
3. Determine whether a plausible equation-specific estimate can cross the product-of-`L1` obstruction.
4. Either supply an independent `H_D` for D1 or reject D1 as a tautological interface.
5. Normalize the topology and imported compactness interfaces for E1.
6. Complete claimed-proof triage of the recent axisymmetric-swirl manuscripts without transferring their status into WP04.
7. Obtain Referee selection or explicit no-selection.

## Three-pillar state

- **MATHFORGE `#18` / PR `#19`:** initial prior-art triage complete; shortlist produced; exact source confirmation and claimed-proof triage remain.
- **MATHSOLVE `#22` / PR `#23`:** theorem statements, proof DAGs, and preliminary scores produced; A2 leads provisionally.
- **MATHCERT `#21` / PR `#22`:** shortlist scaling and formalizability audit produced; A2 is exactly critical, D1's compensation coefficient is critical, and E1 is primarily a quantifier bridge.

## Current decision

No target is selected. `NS-CI-R014-A2` is the provisional lead. WP03, broad numerical work, theorem promotion, and novelty claims remain closed.