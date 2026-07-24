# DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md

## Domain

**Domain 02: Three-Dimensional Incompressible Navier–Stokes / Critical Integrability**

- Campaign identifier: `NS-CI-001`
- Canonical tracker: `MATH-PROGRAMME#55`
- Primary domain: the unforced Cauchy problem on `ℝ³`
- Secondary domain: the periodic problem on `𝕋³`, tracked as a separate hypothesis profile
- Initial result status: `OPEN`
- Programme state: `WP00_SOURCE_AND_EQUIVALENCE_INTEGRATION`

## Corrected canonical challenge

Fix viscosity `ν > 0`. Let `u₀` be a smooth divergence-free vector field on `ℝ³` satisfying Fefferman's rapid-decay condition

```math
|\partial_x^\alpha u_0(x)|\le C_{\alpha,K}(1+|x|)^{-K}
```

for every multi-index `α` and every `K`. Let `u` be a Leray–Hopf weak solution of

```math
∂_t u + (u·∇)u + ∇p = νΔu,
\qquad ∇·u = 0,
\qquad u(0)=u₀.
```

Determine whether, for every finite `T > 0`,

```math
I_T(u) := ∫₀ᵀ ‖u(t)‖_{L⁶(ℝ³)}⁴\,dt < ∞.
```

This is the critical Ladyzhenskaya–Prodi–Serrin pair `(q,p)=(4,6)`, where `q` is the time exponent and `p` the space exponent:

```math
2/q + 3/p = 2/4 + 3/6 = 1.
```

### Restricted compact-support lane

The initialized condition `u₀∈C_c^∞(ℝ³)` is retained as restricted target `NS-CI-R-COMPACT`. It is strictly narrower than the official rapidly decreasing data class. A compact-support theorem cannot be promoted as the full whole-space Clay positive branch without a separate data-class extension theorem.

## Exact campaign posture

The programme separates four logically distinct objects:

1. the energy-class estimate actually available;
2. the missing critical time-integrability estimate;
3. the conditional regularity theorem that consumes that estimate;
4. the correspondence between universal critical integrability and global smoothness.

The campaign must not confuse a criterion for regularity with a proof that the criterion always holds.

## Why this formulation is useful

The Leray–Hopf bounds give

```math
u ∈ L^∞(0,T;L²_x) ∩ L²(0,T;H¹_x).
```

Sobolev control gives

```math
u ∈ L²(0,T;L⁶_x),
```

but the challenge asks for `L⁴(0,T;L⁶_x)`. The exponent gap cannot be repaired by finite-interval inclusion: `L⁴(0,T) ⊂ L²(0,T)`, not conversely.

Under Navier–Stokes scaling

```math
u_λ(x,t)=λu(λx,λ²t),
```

one has `I_T(u_λ)=I_{λ²T}(u)`. The target sits exactly at the scale-invariant boundary.

## Audited formulations and correspondence

### A. Full-data Leray–Hopf formulation

For every Fefferman-class rapidly decreasing smooth divergence-free datum, every Leray–Hopf solution belongs to `L⁴(0,T;L⁶)` on every finite interval.

### B. Maximal strong-solution formulation

For the unique maximal `H¹` strong solution on `[0,T_*)`, the classical continuation estimate gives

```math
T_*<∞
\quad\Longrightarrow\quad
∫₀^{T_*} ‖u(t)‖₆⁴\,dt = ∞.
```

### C. Quantitative continuation formulation

The reconstructed estimate is

```math
‖∇u(t)‖₂²
≤ ‖∇u₀‖₂²
\exp\!\left(Cν^{-3}∫₀ᵗ‖u(s)‖₆⁴ds\right).
```

A finite critical integral therefore controls the `H¹` norm and permits continuation through the local strong theory.

### D. Official positive-branch implication

The full-data formulation is sufficient for Fefferman's whole-space Clay statement (A), using global Leray weak existence, the operational LPS theorem, weak–strong uniqueness, and local strong theory.

### E. Reverse correspondence

Bidirectional equivalence is not yet promoted. The reverse direction requires a source-normalized proof that the exact globally smooth solution class in the official statement belongs to `L⁴_tL⁶_x` on each finite interval and identifies every Leray–Hopf solution through weak–strong uniqueness.

The approved campaign wording is **sufficient for Clay statement (A)**, not **equivalent to the Clay problem**, until that bridge is complete.

## Theorem spine

```text
NS-CI-D000  Equation, viscosity, full data class, domain, forcing, and solution classes
NS-CI-D001  Mixed-norm convention and endpoint policy
NS-CI-L002  Leray–Hopf energy inequality
NS-CI-L003  Homogeneous/inhomogeneous Sobolev bridge to L⁶
NS-CI-C004  Energy-class consequence u ∈ L²_tL⁶_x
NS-CI-O005  Abstract L²_t ↛ L⁴_t obstruction
NS-CI-L006  Navier–Stokes scaling law
NS-CI-C007  Scale invariance of I_T
NS-CI-L008  Operational LPS regularity/uniqueness at (4,6)
NS-CI-L009  Weak–strong uniqueness bridge
NS-CI-L010  Blow-up/continuation alternative through I_T
NS-CI-B011  Full-data critical integrability implies Clay statement (A)
NS-CI-B012  Reverse strong-class correspondence
NS-CI-T013  Universal critical-integrability challenge
NS-CI-R014  Restricted theorem target, selected only after WP00 promotion
NS-CI-R-COMPACT  Compact-support restricted lane
```

## Dependency architecture

```text
D000 ─┬─> L002 ─> L003 ─> C004 ─> O005
      ├─> D001 ────────────────┐
      └─> L006 ─> C007 ────────┼─> T013
                                │
L008 ─> L009 ─> L010 ─> B011 ──┘
                         │
                         └─> Clay statement (A)

Clay smooth class ─> B012 ─> reverse formulation  [pending]
source audit + adversarial review ─> R014
```

`O005` is an obstruction node, not a negative result about Navier–Stokes. It proves only that the standard energy-class information is insufficient by itself.

## Work Package sequence

### WP00: Foundation, status, and equivalence audit

Status: substantive audit complete; governance integration and Referee gate pending.

Delivered:

- corrected full initial-data class;
- solution-class and domain dictionary;
- exact scaling calculation;
- energy-to-`L²_tL⁶_x` derivation;
- abstract exponent-gap witness;
- primary-source ledger with explicit audit states;
- quantitative LPS and continuation reconstruction;
- one-way Clay implication and reverse-correspondence debt;
- theorem spine, claim ledger, proof debt, MATHCERT handoff, and Agent Council review.

### WP01: Energy-gap obstruction and false-proof atlas

Goal: catalogue invalid routes from the energy inequality to the critical estimate.

Required failures include:

- reversed finite-measure embedding;
- illegal interpolation in time;
- hidden use of `L^∞_tH¹_x`;
- circular invocation of regularity;
- unjustified pressure estimates;
- scale-breaking truncations whose constants diverge;
- numerical boundedness presented as continuum proof;
- compact-support results silently promoted to the full rapid-decay class.

### WP02: Conditional regularity and continuation ledger

Goal: preserve the exact theorem chain consuming `L⁴_tL⁶_x`, including the critical nonlinear estimate, constants, approximation steps, and imported theorem interfaces.

### WP03: Quantitative concentration observatory

Goal: build reproducible diagnostics for concentration in shell models, Galerkin truncations, and verified smooth benchmark flows.

Boundary: computations may test mechanisms. They cannot certify global regularity or rule out singularity in the continuum equation.

### WP04: Restricted theorem target

Goal: select one theorem-grade restricted target only after WP00 governance promotion. Candidates must be ranked by leverage, non-circularity, prior-art status, scale compatibility, formalizability, and falsifiability.

### WP05: Certification substrate

Goal: formalize safe statements and interfaces: scaling identities, mixed-norm algebra, energy/Sobolev consequences, implication structure, and visible imported hypotheses.

## Three-pillar split

### MATHFORGE

- primary-source and current-status audit;
- historical theorem extraction with audit states;
- taxonomy of regularity criteria;
- false-proof and claimed-proof triage;
- restricted-regime candidate generation;
- non-probative computational diagnostics.

### MATHSOLVE

- theorem spine and proof-debt ownership;
- quantitative LPS reconstruction;
- continuation and correspondence map;
- restricted-target selection;
- explicit route termination when a mechanism fails.

### MATHCERT

- formal statement hygiene;
- mixed-norm and scaling identities;
- energy/Sobolev bridge where library support permits;
- conditional implication interfaces with provenance;
- proof objects only for closed lemmas, never for the open universal estimate.

## Foundational profile

- Carrier: real-valued vector fields and distributions on `ℝ³ × [0,T]`.
- Ambient structures: measure spaces, Banach/Sobolev spaces, distributions, nonlinear PDE, weak and strong solution classes.
- Classical base: standard classical mathematics with ordinary choice as used in analysis.
- Witness policy: existential weak solutions are literature-derived until reconstructed; computational trajectories are not witnesses for the continuum universal claim.
- Pathology risk: high, due to weak convergence, concentration, endpoint estimates, nonuniqueness outside audited classes, and semantic drift between data and solution concepts.

Registry promotion remains deferred until MSC/arXiv mappings and knowledge-graph nodes are independently audited.

## Source-audit state

1. Fefferman official statement: audited.
2. Prodi original theorem: extracted; modern formulation gap recorded.
3. Serrin original metadata: audited; theorem body pending.
4. Ladyzhenskaya original full-text location: audited; mathematical translation pending.
5. Leray original paper: identified; modern Ożański–Pooley reconstruction used operationally; exact historical theorem map pending.
6. Modern operational LPS statement: audited at `(4,6)`.
7. Current official open status: audited on 2026-07-23.

## Claim boundary

This campaign does not claim:

- universal finiteness of `I_T`;
- a new regularity criterion;
- a weakening of the Millennium problem;
- evidence against finite-time singularity from numerical experiments;
- novelty for the challenge formulation;
- that a compact-support theorem alone settles the full whole-space branch;
- completed bidirectional equivalence with the official statement.

## Current executable gate

Integrate the WP00 audit into the claim ledger, proof-debt register, theorem DAG, and Agent Council review. Mechanism generation and numerical experimentation remain closed until:

- the corrected data class is consistent across artifacts;
- one-way implication language replaces unaudited equivalence language;
- the Referee confirms that all remaining gaps are recorded;
- CI validates the integrated bundle.
