# YM-WP02 — Source-Normalized Theorem and Route Ledger

**Artifact ID:** `YM-WP02`  
**Campaign:** `YM-001`  
**Pillar:** MATHSOLVE  
**Lifecycle:** `ACTIVE — INTERNAL REVIEW COMPLETE; REPOSITORY REVIEW REQUIRED`  
**Computation class:** `NONE` for mathematical claims; deterministic validation only  
**Certification state:** Not certified  
**Strongest supported claim:** The package records typed, source-located interfaces for rigorous Yang–Mills terrain and blocks their use outside audited scope.  
**Claims not made:** No new theorem, best-known-result claim, complete literature survey, mechanism selection, numerical result, novelty claim, or solution of the Clay problem.  
**First executable step:** Run `python3 campaigns/yang_mills/validate_wp01_wp02.py`.

## Lay executive companion

Rigorous results called “Yang–Mills,” “mass gap,” or “construction” can concern very different objects. Some are exact in two dimensions. Some are conditional or local in three dimensions. Some establish a gap only for a fixed lattice in a strong-coupling regime. Some prove ultraviolet perturbative behaviour. None can be inserted into the four-dimensional Clay theorem without proving the missing interfaces.

This ledger records those interfaces rather than collecting theorem names. Each entry fixes dimension, gauge group, regulator, volume, coupling regime, quantifiers, normalization, hypotheses, conclusion, source locator, composition state, residual hypotheses, and claim boundary.

## Formal problem statement

The terminal target is `YM-T-000`, inherited from YM-WP00. It jointly requires:

- a nontrivial four-dimensional continuum quantum Yang–Mills theory for every compact simple `G`;
- an accepted Euclidean or Minkowski axiomatic profile and local gauge-invariant observables;
- ultraviolet concordance with asymptotic freedom;
- a reconstructed positive physical Hamiltonian;
- a strictly positive finite spectral gap above the vacuum.

No ledger record may weaken this conjunction by implicit substitution.

## Object and obstruction

The object is a typed source and theorem-interface ledger. The obstruction is compositional: valid results usually inhabit incompatible dimensions, regulators, volumes, groups, or coupling regimes.

The ledger distinguishes:

- terminal open target;
- regulated theorem;
- solved lower-dimensional analogue;
- conditional or nearby-model theorem;
- perturbative theorem;
- implication interface;
- open route contract;
- partial claim requiring audit;
- unverified complete-solution claim;
- institutional status.

## Source audit

`01_SOURCE_REGISTRY.json` contains primary or governing sources. Audit states are binding:

- `AUDITED*`: usable only within the recorded scope;
- `NEEDS_THEOREM_BODY_AUDIT`: not composable until exact theorem extraction;
- `UNVERIFIED_COMPLETE_SOLUTION_CLAIM`: never a theorem premise;
- `AUDITED_CURRENT`: current institutional status.

The ledger is intentionally non-exhaustive. It prioritizes theorem-shape diversity and the interfaces needed to protect the Clay target.

## Trust quartet

**What is proved?** No new Yang–Mills theorem is proved in this package.

**What is checked?** Source IDs, theorem fields, fixture links, noncomposable debts, and downstream gate closure are checked deterministically.

**What remains open?** Four-dimensional construction, OS reconstruction, nontriviality, local-observable construction, ultraviolet concordance, uniform regulator survival, and the physical mass gap.

**What requires external verification?** Sources `YM-SRC-016` through `YM-SRC-019`, especially recent manuscripts claiming complete or partial four-dimensional results.

## Theorem-spine slice

```text
2D exact / 3D partial / 4D RG / strong-coupling lattice / perturbation
                              |
                              v
                  typed theorem interfaces
                              |
                +-------------+-------------+
                |                           |
                v                           v
        complete OS profile       uniform regulator-survival
                |                           |
                +-------------+-------------+
                              v
                  physical continuum theory
                              |
                              v
                   physical Hamiltonian gap
```

Every downward arrow not already a theorem record is represented as dependency debt.

## Composition rule

A record is usable only when:

1. all `source_ids` resolve to audited sources;
2. its exact dimension, group, regulator, volume, and coupling regime match the intended use;
3. every hypothesis and residual hypothesis is discharged;
4. its `composition_state` permits the intended direction;
5. no WP01 fixture rejects the proposed transition.

See `03_COMPOSITION_RULES.md`.

## Proof-debt register

`04_DEPENDENCY_DEBT_GATE.json` records the unproved bridges. Unrecorded debt is a governance failure; recorded debt remains mathematically open.

## Certification boundary

The ledger supplies candidate statements and dependency routes for later formalization. It does not formalize constructive quantum field theory, OS reconstruction, spectral convergence, or any imported theorem.

## First executable step

**Input:** WP01 atlas, source registry, theorem ledger, and dependency gate.  
**Operation:** execute `validate_wp01_wp02.py` and its adversarial tests.  
**Output:** deterministic cross-package validation report.  
**Completion test:** all records complete, references resolved, all noncomposable interfaces debt-backed, and mechanism/numerical gates closed.  
**Spine node advanced:** `YM-WP02-SOURCE-NORMALIZED-INTERFACE-LEDGER`.
