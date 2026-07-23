# NS-CI-WP00 — Next executable step

## Objective

Discharge the source and semantic bridge debt required to state the campaign without hidden assumptions.

## Input

1. Official Clay problem description by Charles L. Fefferman.
2. Primary Prodi, Serrin, and Ladyzhenskaya sources.
3. A primary or authoritative source for Leray–Hopf existence and the energy inequality on `ℝ³`.
4. An authoritative local strong-existence and maximal-time theorem for smooth divergence-free data.
5. An authoritative weak–strong uniqueness theorem in a hypothesis profile compatible with items 3 and 4.

## Operation

Create `WP00_SOURCE_AND_EQUIVALENCE_AUDIT.md` with one record per imported theorem:

```text
theorem identifier
bibliographic source
verbatim or faithfully normalized statement
domain
initial-data class
solution class
space-time exponents
endpoint inclusions/exclusions
forcing convention
conclusion
hypotheses not used by the campaign
hypotheses missing from the campaign
notation translation
reviewer
review date
```

Then write the implication proof

```text
universal L4_tL6_x integrability
    -> conditional regularity on every finite interval
    -> agreement of weak and strong solutions while the strong solution exists
    -> exclusion of finite maximal time
    -> global smooth solution in the selected R3 formulation.
```

Also audit the reverse direction needed for the word `equivalent`:

```text
global smoothness in the selected formulation
    -> finite L4_tL6_x integral on every finite interval
    -> weak-solution formulation through weak-strong uniqueness.
```

If any arrow needs stronger decay, regularity, or uniqueness hypotheses than the campaign currently states, weaken the public correspondence claim rather than concealing the gap.

## Output artifacts

- `04_PROBLEM_AND_STATUS_AUDIT.md`
- updated `10_CLAIM_LEDGER.yaml`
- updated `09_PROOF_DEBT.json`
- updated `06_DEPENDENCY_DAG.json`
- completed Agent Council findings for Axiomatist, Prospector, Verifier, Adversary, Formalist, Amanuensis, and Referee

## Completion test

The step is complete only when:

- every imported theorem has an authoritative source;
- the selected theorem statements have matching domains and solution classes, or explicit transfer lemmas;
- the use of `equivalent` is justified bidirectionally or replaced by a one-way implication;
- `NS-CI-D001` through `NS-CI-D005` are discharged or narrowed;
- the Referee can reproduce the implication chain from the committed artifacts alone;
- no campaign document implies a new Navier–Stokes result;
- the agent-review record has no unrecorded blocking obligation.

## Spine effect

- Primary node advanced: `NS-CI-L010`
- Secondary node clarified: `NS-CI-T011`
- Debt targeted: `NS-CI-D001`, `NS-CI-D002`, `NS-CI-D003`, `NS-CI-D004`, `NS-CI-D005`

## Stop condition

Do not proceed to mechanism generation or broad numerical experimentation if the equivalence audit fails. First repair the challenge statement and quantifiers.