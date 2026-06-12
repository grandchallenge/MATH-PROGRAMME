# Claim Boundary Doctrine

## The central rule

A mathematical statement must never be stronger than its support.

The programme therefore distinguishes discovery, evidence, proof, certification, and public claim.

```text
idea
  -> evidence
  -> claim
  -> support route
  -> certificate or proof boundary
  -> promoted status
```

If any arrow is missing, the status must remain provisional.

## Status is part of the mathematics

The status of a claim is not administrative metadata. It is mathematical content. It tells the reader what kind of reliance is permitted.

A claim ledger should make clear whether a statement is:

- proved in the present artifact;
- formalized but unproved;
- exactly computed;
- interval-certified;
- SAT/SMT-certified;
- derived from literature;
- heuristic;
- conjectural;
- a failed attempt;
- superseded;
- refuted.

## The five dangerous substitutions

### 1. Citation for proof

A citation may support historical or contextual claims. It does not certify a new derived claim unless the dependency is explicit.

### 2. Computation for theorem

A finite computation can verify a finite statement or sanity-check definitions. It does not prove an infinite theorem unless the finite-to-infinite bridge is itself proved.

### 3. Exposition for derivation

A beautiful explanation is valuable. It is not a proof unless the logical obligations are present.

### 4. Formal syntax for meaning

A theorem-prover statement that does not correspond to the intended human statement has not certified the intended claim.

### 5. Specialist confidence for certification

Expert review is valuable. It is not the same as a replayable certificate or checked proof.

## Promotion ladder

| Level | Status | Reader may rely on it as |
| --- | --- | --- |
| 0 | Lead | A possible direction |
| 1 | Heuristic | A useful intuition |
| 2 | Exact evidence | A checked finite/computational fact under stated assumptions |
| 3 | Proved locally | A theorem inside the Work Package |
| 4 | Certification-ready | A precise target with formal dependencies |
| 5 | Certified | A checked proof or replayed certificate |

## Review questions

Before promotion, ask:

1. What is the exact claim?
2. What is the support type?
3. What assumptions are active?
4. What artifact can an independent reviewer inspect?
5. What would refute or downgrade the claim?
6. What is the next certification action?

## Motto

> Trust is not a tone. Trust is a boundary.
