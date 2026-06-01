# GRAND_CHALLENGE_WORK_PACKAGE_STANDARD.md

## Purpose

This standard defines what counts as a Grand Challenge Work Package. It is binding for MATHSOLVE and strongly recommended for MATHFORGE and MATHCERT companion documents.

A Grand Challenge Work Package is not a blog post, not a code dump, not a motivational memo, and not a theorem claim dressed in prose. It is a disciplined mathematical artifact that teaches the problem, records the state of the work, and makes its claims auditable.

## Required structure

Every Work Package must contain the following sections.

### 1. Lay executive companion

This section explains the problem to an intelligent non-specialist. It must answer:

- What is the object?
- Why does the problem matter?
- What would a solution mean?
- What did this package actually achieve?
- What did it not achieve?
- What is the next move?

This section must not exaggerate. It must not hide uncertainty. It must not condescend.

### 2. Formal problem statement

This section gives definitions, notation, hypotheses, and the exact target statement. If the problem has multiple equivalent formulations, list them and state which one the package uses.

### 3. Known terrain and status audit

This section records known results, special cases, partial bounds, solved variants, false-proof risk, and the present status of the problem. Each literature-derived claim must have a source.

### 4. Claim ledger

Every nontrivial claim in the package must be recorded in a ledger. The ledger must classify each claim as one of:

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

### 5. Theorem spine

This is the formal mathematical heart. It should contain theorem, proposition, lemma, corollary, definition, example, and counterexample statements. Even a synthesis package should have a proposition-like spine: reductions, equivalences, known theorem dependencies, and obstruction claims.

### 6. Proofs and computations

Provide proofs, proof sketches, exact computations, interval ledgers, scripts, reproducibility steps, or failure analysis. Every computation must specify arithmetic mode: floating point, exact rational, interval, symbolic, SAT/SMT, or other.

### 7. Failure analysis

A failed attempt is valuable if it exposes the structure of the obstruction. Record what was attempted, why it seemed plausible, where it failed, and what it teaches.

### 8. Certification boundary

State which claims are pencil-and-paper proved, machine checked, exactly computed, interval certified, heuristic, or still pending. This must be explicit.

### 9. MATHCERT handoff

List candidate Lean/equivalent definitions, theorem statements, exact certificate formats, missing libraries, formalization blockers, and first lemmas to check.

### 10. Next analytic target

A Work Package must end with a sharp next target. “Continue research” is not acceptable. The next target should be a theorem, reduction, finite screen, interval campaign, formalization milestone, or obstruction analysis.

## Quality bar

A Work Package is Grand-Challenge grade only if a reader can leave with:

1. a correct mental picture;
2. a precise formal statement;
3. a map of known terrain;
4. a list of actual claims;
5. a clear boundary between proof and evidence;
6. a concrete next target;
7. a path to certification.

## Anti-patterns

Reject Work Packages that:

- contain large claims with no ledger;
- use citations as proof;
- present floating-point output as theorem-grade evidence;
- hide dead ends;
- lack a lay companion;
- lack a next target;
- lack a certification handoff;
- make the project look bigger by being vaguer.

## Grand Challenge style

The expected style is ambitious but accountable. It should be spacious enough to teach, formal enough to audit, and honest enough to preserve trust. It should not sound like corporate strategy or research theatre.

## File bundle for each Work Package

```text
WP##_TITLE/
  00_README.md
  01_LAY_COMPANION.md
  02_PROBLEM_SPINE.md
  03_STATUS_AUDIT.md
  04_THEOREM_SPINE.md
  05_PROOFS_AND_COMPUTATIONS.md
  06_FAILURE_ANALYSIS.md
  07_CLAIM_LEDGER.yaml
  08_CERT_HANDOFF.md
  09_NEXT_TARGET.md
  artifacts/
    code/
    data/
    certificates/
    figures/
```
