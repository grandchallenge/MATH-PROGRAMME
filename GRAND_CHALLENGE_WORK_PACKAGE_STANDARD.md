# GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md

## Purpose

This standard defines what counts as a Grand Challenge Work Package. It is
binding for MATHSOLVE and strongly recommended for MATHFORGE and MATHCERT
companion documents.

A Work Package is a controlled slice of one campaign theorem spine. It is not a
blog post, code dump, motivational memo, or isolated theorem claim. It teaches
the object, records the obstruction and proof debt, and makes the next move
auditable.

## Campaign rule

A domain has one evolving theorem spine and dependency DAG. Every Work Package
must name the global spine node it advances and the dependencies it consumes.

A new package may not be opened merely because the current one is difficult.
The escalation gate in section 13 must be satisfied first.

## Required structure

Every Work Package must contain the following sections.

### 1. Result-status box

Place this before the executive companion. It must state:

- result status;
- conditions on which the result depends;
- strongest supported claim;
- claims explicitly not made;
- computation class or `NONE`;
- certification state;
- first executable step.

### 2. Lay executive companion

Explain the object, obstruction, restricted target, actual achievement, limit,
and next move to an intelligent non-specialist. Do not exaggerate, conceal
uncertainty, or condescend.

### 3. Formal problem statement

Give definitions, notation, hypotheses, and the exact target statement. If
multiple equivalent formulations exist, state which one the package uses and
what correspondence must be justified.

### 4. Object and obstruction

Present a working model and the smallest exact calculation, counterexample, or
failed mechanism that exposes the principal obstruction. "The problem is hard"
is not an obstruction analysis.

### 5. Known terrain and source audit

Record known results, special cases, partial bounds, solved variants,
false-proof risks, and present status. Every literature-derived claim needs a
source and an audit state.

### 6. Claim ledger and trust quartet

Every nontrivial claim must appear in the claim ledger with one of:

```text
PROVED_IN_PACKAGE
COMPUTED_EXACTLY
INTERVAL_CERTIFIED
FORMALIZED
LITERATURE_DERIVED
HEURISTIC
CONJECTURAL
FAILED_ATTEMPT
NEEDS_AUDIT
SUPERSEDED
REFUTED
```

Display these four answers together:

1. What is proved?
2. What is checked?
3. What remains open?
4. What requires external verification?

### 7. Theorem-spine slice and dependency DAG

The local spine must identify every definition, reduction, bridge, theorem,
obstruction, and certificate node used by the package. For each node record:

- stable identifier;
- role;
- status;
- incoming dependencies;
- discharge criterion;
- linked proof-debt items.

### 8. Proofs and classified computations

Provide proofs, proof sketches, exact computations, interval ledgers, scripts,
reproducibility steps, or failure analysis. Every computation must specify its
arithmetic mode and exactly one pedagogical class:

```text
EXPLORATORY_EVIDENCE
REGRESSION_AUDIT
EXACT_FINITE_VERIFICATION
CONTINUUM_PROOF
```

The classification must agree with the claim ledger.

### 9. Failure and negative-result analysis

Record the attempted route, why it was plausible, the smallest exact
obstruction, what the obstruction rules out, what it does not rule out, and the
next viable restricted problem.

### 10. Proof-debt register

Classify unresolved obligations as:

```text
MISSING_LEMMA
UNPROVED_BRIDGE
EXTERNAL_SOURCE
COMPUTATIONAL_REPLAY
SEMANTIC_CORRESPONDENCE
ANALYTIC_ESTIMATE
FORMALIZATION_BLOCKER
```

Each item must name the blocked spine node, current evidence, discharge
condition, and intended route or owner.

### 11. Certification boundary and MATHCERT handoff

Separate mathematical status from certification state. List candidate formal
definitions, theorem statements, exact certificate formats, missing libraries,
formalization blockers, and first lemmas or witnesses to check.

### 12. First executable step

End with one bounded action. It must name:

- input;
- operation;
- output artifact;
- completion test;
- spine node advanced or debt item discharged.

"Continue research" is not acceptable.

### 13. Escalation gate

The next Work Package may be opened or promoted only when:

- the current theorem-spine slice has been audited;
- all dependencies are named;
- the proof-debt register is current;
- the trust quartet is complete;
- the first executable step is explicit;
- the proposed package names the spine node it advances.

Unresolved debt does not always block progression, but unrecorded debt does.

## Quality bar

A Work Package is Grand-Challenge grade only if a reader leaves with:

1. a correct mental picture of the object and obstruction;
2. a precise restricted target;
3. a map of the theorem spine and dependencies;
4. a list of actual claims;
5. a clear boundary between proof, checks, and conjecture;
6. a visible proof-debt register;
7. one executable next step;
8. a path to certification.

## Anti-patterns

Reject Work Packages that:

- contain large claims with no ledger;
- use citations as proof;
- present floating-point output as theorem-grade evidence;
- hide dead ends or proof debt;
- lack a lay companion;
- lack an exact obstruction;
- present an isolated theorem list with no dependencies;
- lack a first executable step;
- open a new package before auditing the current spine;
- make the programme look bigger by being vaguer.

## File bundle for each Work Package

```text
WP##_TITLE/
  00_README.md
  01_RESULT_STATUS.json
  02_LAY_COMPANION.md
  03_OBJECT_AND_OBSTRUCTION.md
  04_PROBLEM_AND_STATUS_AUDIT.md
  05_THEOREM_SPINE.md
  06_DEPENDENCY_DAG.json
  07_PROOFS_AND_COMPUTATIONS.md
  08_FAILURE_AND_NEGATIVE_RESULTS.md
  09_PROOF_DEBT.json
  10_CLAIM_LEDGER.yaml
  11_CERT_HANDOFF.md
  12_NEXT_EXECUTABLE_STEP.md
  artifacts/
    code/
    data/
    certificates/
    figures/
```

The compact single-file template remains acceptable for small packages, but it
must preserve the same information.
