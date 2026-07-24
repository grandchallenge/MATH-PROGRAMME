# NS-CI-WP00 — Foundation, source, status, and correspondence audit

## Metadata

- Domain: Three-dimensional incompressible Navier–Stokes
- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP00`
- Canonical tracker: `MATH-PROGRAMME#55`
- Primary type: status spine, source audit, obstruction audit, and correspondence map
- Global theorem-spine node advanced: `NS-CI-B011`
- Incoming dependencies: official Clay statement; Leray weak/strong theory; Prodi–Serrin regularity; weak–strong uniqueness
- Claim status: local derivations checked; operational regularity interfaces audited; universal estimate open
- Certification target: human audit followed by selective theorem-prover formalization
- Foundational profile: present
- Promotion state: governance integration pending

## 1. Result-status box

| Field | Value |
|---|---|
| Result status | `SUBSTANTIVE AUDIT COMPLETE / OPEN PROBLEM` |
| Conditional on | Standard R3 Leray–Hopf, H1 strong-solution, and weak–strong interfaces recorded in the source audit |
| Strongest supported claim | `L4_tL6_x` is the exact critical coefficient closing the H1 continuation and weak–strong uniqueness estimates; universal control for Fefferman's full rapidly decreasing data class is sufficient for Clay statement (A) |
| Not claimed | Universal finiteness, global regularity, a new criterion, bidirectional equivalence, or full Clay coverage from compact-support data alone |
| Support-route class | `CONTINUUM_PROOF`, `NEGATIVE_RESULT`, `PRIMARY_SOURCE_AUDIT`, `LITERATURE_DERIVED` |
| Foundational profile | Continuum PDE over `R`; high pathology and semantic-drift risk |
| Certification state | Human-audit checked; formal certification pending |
| First executable step | Complete Amanuensis and Referee integration, run CI, then decide WP01/WP02 promotion |

## 2. Foundational profile

```yaml
foundational_profile:
  carrier_type: continuum
  ambient_structure:
    - real_vector_spaces
    - measure_spaces
    - Banach_spaces
    - Sobolev_spaces
    - distributions
    - nonlinear_partial_differential_equations
  regularity:
    - weak_solution
    - energy_class
    - strong_solution
    - smooth_solution
  axiom_profile:
    base: classical_analysis
    choice_usage: standard_functional_analysis
    excluded_middle: used
    large_cardinal_usage: none
    determinacy_usage: none
  witness_policy:
    existence_claim: literature_derived
    witness_location: analytic_construction_or_source_theorem
  certification_target:
    - human_audit
    - Lean
  pathology_risk:
    level: high
    notes: Weak convergence, concentration, endpoint estimates, data-class drift, solution-class drift, and circular regularity arguments are principal risks.
```

## 3. Lay executive companion

### The object

The energy inequality controls kinetic energy and the time-integrated spatial gradient. In three dimensions this implies that the velocity has a finite `L6` norm squared in time.

### The obstruction

The desired integral uses the fourth power in time. This is not a cosmetic strengthening. Under the natural zooming symmetry of Navier–Stokes, the fourth-power `L6` integral is unchanged. It is exactly the coefficient that appears when the nonlinear term is balanced against viscosity in the `H1` estimate.

### The restricted target

The official whole-space Clay branch permits every smooth divergence-free datum whose derivatives decay faster than every power. Compactly supported smooth data form a useful restricted subclass, but they are not the whole official class.

### What this package achieved

1. Corrected the canonical initial-data class to Fefferman's full rapidly decreasing class.
2. Retained compact support as a named restricted lane.
3. Audited an operational Prodi–Serrin theorem at `(4,6)` for R3 Leray–Hopf solutions.
4. Reconstructed the exact H1 continuation and weak–strong uniqueness estimates.
5. Established a checked one-way implication from universal full-data critical integrability to Clay statement (A).
6. Refused to promote bidirectional equivalence until the reverse bridge is source-normalized.

### What this package did not achieve

It did not prove the universal integral finite. The concentrating obstruction field is not a Navier–Stokes solution. The source audit and classical reconstruction organize the open problem; they do not solve it.

## 4. Formal problem statement

### 4.1 Equation and full data class

Let `nu>0`. Let `u0` be smooth, divergence-free, and satisfy

```math
|\partial_x^\alpha u_0(x)|\le C_{\alpha,K}(1+|x|)^{-K}
```

for every multi-index `alpha` and every `K`. Consider

```math
\partial_t u-\nu\Delta u+(u\cdot\nabla)u+\nabla p=0,
\qquad \nabla\cdot u=0,
\qquad u(0)=u_0
```

on `R3`.

### 4.2 Leray–Hopf interface

The working weak class satisfies, in the standard whole-space convention,

```math
u\in L^\infty(0,T;L^2(\mathbb R^3))
\cap L^2(0,T;\dot H^1(\mathbb R^3)),
```

with distributional satisfaction of the equation, attainment of the initial datum, and the energy inequality.

### 4.3 Target

For every finite `T>0`, define

```math
I_T(u)=\int_0^T\|u(t)\|_{L^6(\mathbb R^3)}^4dt.
```

The canonical challenge asks whether `I_T(u)<infinity` for every admissible datum and every Leray–Hopf solution.

### 4.4 Compact-support restricted lane

`NS-CI-R-COMPACT` asks the same question under `u0 in C_c^infinity(R3)`. A result in this lane remains restricted unless accompanied by a proved extension to the full rapidly decreasing class.

## 5. Object and obstruction

### 5.1 Energy gives only `L2_tL6_x`

The energy inequality and Sobolev estimate give

```math
\int_0^T\|u(t)\|_6^2dt
\le C\nu^{-1}\|u_0\|_2^2.
```

On a finite interval `L4` embeds into `L2`, not conversely.

### 5.2 Exact abstract non-embedding

For a nonzero divergence-free `phi in C_c^infinity(R3)` set

```math
\lambda(t)=t^{-1/3},
\qquad v(t,x)=\lambda(t)^{3/2}\phi(\lambda(t)x).
```

Then

```math
\|v(t)\|_2=\|\phi\|_2,
\quad \|\nabla v(t)\|_2\asymp t^{-1/3},
\quad \|v(t)\|_6\asymp t^{-1/3}.
```

Thus `v` lies in the abstract energy space but not in `L4_tL6_x`. This rules out a generic interpolation shortcut, not the Navier–Stokes target.

### 5.3 Critical scaling

For

```math
u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
```

one has

```math
\int_0^T\|u_\lambda(t)\|_6^4dt
=\int_0^{\lambda^2T}\|u(s)\|_6^4ds.
```

## 6. Known terrain and source audit

The authoritative audit is `04_PROBLEM_AND_STATUS_AUDIT.md`. Its principal source states are:

| Source | Use | Audit state |
|---|---|---|
| Fefferman / Clay | Official R3 data class and positive branch | `AUDITED` |
| Leray 1934 | Historical weak/strong foundation | `PRIMARY_IDENTIFIED`; exact theorem concordance pending |
| Ożański–Pooley | Operational local strong, global weak, and weak–strong reconstruction | `AUDITED_AT_STATEMENT_LEVEL` |
| Prodi 1959 | Original uniqueness exponent law, including `(4,6)` | `AUDITED_WITH_FORMULATION_GAP` |
| Serrin 1962 | Historical regularity source | metadata audited; theorem body pending |
| Ladyzhenskaya 1967 | Historical uniqueness/smoothness source | full text located; translation pending |
| Modern explicit LPS statement | R3 Leray–Hopf operational interface | `AUDITED` |
| Clay current status | Open-problem status | `AUDITED_2026-07-23` |

Historical provenance gaps no longer block the operational WP00 theorem chain, but remain recorded debt.

## 7. Claim ledger and trust quartet

### Claim summary

| Claim ID | Statement | State |
|---|---|---|
| `C001` | Energy plus Sobolev yields `L2_tL6_x` | checked |
| `C002` | Abstract energy space does not imply `L4_tL6_x` | checked |
| `C003` | The target integral is scaling-critical | checked |
| `C004` | Operational LPS uniqueness/strongness at `(4,6)` | audited literature-derived |
| `C005` | Universal full-data critical integrability implies Clay (A) | checked one-way bridge |
| `C006` | The universal target remains open | audited current status |
| `C008` | Compact support alone is not the full official data class | audited |
| `C009` | Reverse equivalence remains pending | draft |

### What is proved?

The energy consequence, non-embedding witness, scaling identity, quantitative H1 estimate, weak–strong difference estimate, and one-way logical composition are proved or reconstructed in the package.

### What is checked?

The modern operational regularity theorem, official data class, and current open status are source-audited.

### What remains open?

The universal estimate, the reverse equivalence bridge, and every genuine mechanism intended to produce the missing integrability.

### What requires external verification?

The final Referee review; exact historical Serrin and Ladyzhenskaya extraction; the Leray theorem concordance; theorem-prover certification.

## 8. Theorem spine

The machine-readable graph is `06_DEPENDENCY_DAG.json`. Its central chain is

```text
energy -> L2_tL6_x
critical scaling + non-embedding -> exact obstruction
L4_tL6_x -> H1 control and weak-strong uniqueness
universal full-data L4_tL6_x -> Clay statement (A)
```

The reverse Clay-to-every-Leray–Hopf bridge remains a separate pending node.

## 9. Proofs and classified computations

WP00 uses no numerical evidence.

- Energy estimate: `CONTINUUM_PROOF`, conditional on the imported energy interface.
- Non-embedding witness: `NEGATIVE_RESULT` about function spaces.
- Scaling: `CONTINUUM_PROOF`.
- H1 and difference estimates: `CONTINUUM_PROOF_RECONSTRUCTION` of classical arguments.
- Source and status determinations: `PRIMARY_SOURCE_AUDIT` or explicitly labeled operational secondary statement.

## 10. Failure and negative-result analysis

### Rejected shortcut

`L2_tL6_x` does not upgrade to `L4_tL6_x` merely because the interval is finite.

### Rejected correspondence shortcut

A theorem only for compactly supported data does not automatically cover all rapidly decreasing smooth data.

### Rejected rhetorical shortcut

A conditional regularity criterion is not evidence that its hypothesis holds universally.

### Viable next work

WP01 may formalize the false-proof atlas. WP02 may preserve the quantitative continuation chain. Mechanism selection remains gated until governance integration completes.

## 11. Proof-debt register

`09_PROOF_DEBT.json` distinguishes resolved operational obligations from remaining debt. The only current blocking items are:

- `NS-CI-D011`: complete cross-document data-class integration;
- `NS-CI-D012`: Referee confirmation of the one-way implication and non-equivalence wording.

Historical and formalization debts are nonblocking and remain visible.

## 12. Certification boundary and MATHCERT handoff

The first formal targets remain:

1. mixed-norm scaling under Navier–Stokes dilation;
2. exact exponent arithmetic at `(4,6)`;
3. optionally, the abstract concentrating witness;
4. a provenance-bearing logical interface for imported PDE theorems.

The universal estimate must not be encoded as an axiom or presented as formally proved.

## 13. First executable step

- Input: the integrated source audit, corrected master plan, updated claim ledger, debt register, and theorem DAG.
- Operation: complete Amanuensis consistency review and independent Referee review.
- Output: updated Agent Council record and CI evidence.
- Completion test: `NS-CI-D011` and `NS-CI-D012` are discharged; no artifact calls the compact-support lane canonical; no artifact claims bidirectional equivalence; CI passes.
- Spine node advanced: `NS-CI-B011`.

## 14. Escalation gate

- [x] The theorem-spine slice has been audited.
- [x] All dependencies are named.
- [x] The proof-debt register is current.
- [x] The trust quartet is complete.
- [x] The foundational profile is present.
- [x] The first executable step is explicit.
- [ ] Cross-document data-class integration is independently checked.
- [ ] Referee confirms the correspondence boundary.

No mechanism generation or numerical experimentation begins before the final two checks.