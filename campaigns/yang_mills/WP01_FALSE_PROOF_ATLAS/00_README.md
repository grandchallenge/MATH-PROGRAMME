# YM-WP01 — Executable False-Proof Atlas

**Artifact ID:** `YM-WP01`  
**Campaign:** `YM-001`  
**Pillar:** MATHFORGE  
**Lifecycle:** `ACTIVE — INTERNAL REVIEW COMPLETE; REPOSITORY REVIEW REQUIRED`  
**Computation class:** `REGRESSION_AUDIT`  
**Certification state:** Not certified  
**Strongest supported claim:** The package deterministically rejects or narrows twenty recurrent invalid inferences about four-dimensional Yang–Mills existence and mass gap.  
**Claims not made:** No fixture proves or disproves the Clay problem, establishes that every route of a broad family fails, selects a mechanism, or authorizes numerical experimentation.  
**First executable step:** Run `python3 campaigns/yang_mills/WP01_FALSE_PROOF_ATLAS/replay.py`.

## Lay executive companion

A convincing-looking Yang–Mills argument can fail long before its difficult calculations begin. It may quietly replace a continuum theory with a lattice approximation, a physical spectral gap with one decaying correlator, or a theorem with an unreviewed manuscript claim.

This atlas makes those substitutions explicit. Each fixture records the first invalid inference, the missing theorem obligation, a minimal witness showing why the inference fails, the narrowest acceptable repair, and the WP02 theorem interfaces that govern the issue.

The atlas is eliminative infrastructure. It does not rank research mechanisms. Passing every fixture means only that these named semantic failures were not detected.

## Formal protected target

The protected terminal target is `YM-T-000`: for every compact simple gauge group, construct a nontrivial four-dimensional continuum quantum Yang–Mills theory satisfying the accepted axiomatic and ultraviolet profile, and prove a strictly positive finite gap above the vacuum in the reconstructed physical Hamiltonian.

Every fixture protects the distinction between that conjunction and a restricted, regulated, lower-dimensional, perturbative, numerical, or unverified substitute.

## Object and obstruction

The object is a machine-readable catalogue of invalid proof transitions. The principal obstruction is **interface loss**: an argument proves a statement in one representation, scale, dimension, volume, coupling regime, observable channel, or evidence class and silently promotes it across an unproved bridge.

The smallest exact counterexample pattern is a sequence of positive regulated gaps that tends to zero after the relevant limit or physical rescaling. Positivity at every finite stage does not imply a positive limiting lower bound.

## Known terrain and source audit

WP01 consumes the source-normalized interfaces in YM-WP02. It does not independently import theorem claims. Sources marked `NEEDS_*_AUDIT` or `UNVERIFIED_COMPLETE_SOLUTION_CLAIM` remain unusable as theorem premises.

The twenty fixtures cover:

1. fixed-lattice and finite-volume gaps;
2. strong-coupling versus continuum scaling;
3. confinement, area law, and channel decay substitutions;
4. reflection positivity and transfer-matrix overpromotion;
5. perturbative, lower-dimensional, Abelian, and large-`N` substitutions;
6. gauge-fixed, formal-integral, weak-limit, and classical/quantum conflations;
7. numerical spectroscopy and unreviewed solution claims;
8. physical-unit scaling, analytic continuation in coupling, and local stochastic dynamics.

## Trust quartet

**What is proved?** The package proves only finite documentary facts about its own fixture contract and the stated logical counterexamples.

**What is checked?** Deterministic replay checks the exact fixture count, IDs, required fields, allowed dispositions, WP02 links, protected target, and closed downstream gates.

**What remains open?** Every terminal Yang–Mills existence and physical-gap obligation remains open.

**What requires external verification?** Every imported theorem remains governed by WP02 source status; recent complete-solution claims require independent specialist audit.

## Theorem-spine slice and dependency DAG

```text
YM-WP00 source and equivalence lock
          |
          +--> YM-WP02 theorem interfaces
          |          |
          |          +--> source, scope, composition, and debt controls
          |
          +--> YM-WP01 fixtures
                     |
                     +--> reject or narrow invalid transitions
                     |
                     +--> downstream mechanism gate remains CLOSED
```

Each fixture names one or more `YM-T-*` interfaces. Unknown or dangling links fail replay.

## Failure and negative-result rule

A fixture may return only:

- `REJECT`: the inference is invalid as stated;
- `NARROW`: a restricted conclusion may survive after exact hypotheses and scope are restored.

A fixture must also state what the failure does **not** rule out. The atlas therefore blocks overreach without pretending to prove a universal impossibility theorem.

## Proof-debt register

WP01 inherits the dependency debts in `../WP02_THEOREM_LEDGER/04_DEPENDENCY_DEBT_GATE.json`. In particular, it does not discharge continuum-limit, OS-reconstruction, observable-completeness, or spectral-stability obligations.

## Certification boundary

The JSON atlas and replay script are software evidence. They are not mathematical certification. A future MATHCERT handoff could encode selected logical fixtures as formal implication counterexamples, but no such formalization is claimed here.

## First executable step

**Input:** `01_ATLAS.json`.  
**Operation:** execute `replay.py`.  
**Output:** deterministic pass/fail report.  
**Completion test:** exactly twenty valid fixtures, all interfaces resolvable by WP02, and all downstream gates closed.  
**Spine node advanced:** `YM-WP01-SEMANTIC-FIREWALL`.
