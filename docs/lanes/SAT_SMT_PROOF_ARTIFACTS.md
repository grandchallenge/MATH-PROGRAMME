# SAT and SMT Proof Artifacts to Certificate

## Obligation

Use this lane for a bounded Boolean or theory instance whose exact encoding can produce a model or independently checkable proof artifact.

## MATHFORGE

MATHFORGE builds candidate encodings, compares solver routes, records solver and proof-format provenance, and retains models, traces, and failed encodings as provider evidence.

## MATHSOLVE

MATHSOLVE verifies the source-to-formula translation, declares the resource budget, and selects a proof-producing solver and independent checker appropriate to the obligation.

## MATHCERT

MATHCERT reconstructs the encoding, checks the SAT model or UNSAT proof artifact, and verifies that the checked result maps back to the named source proposition.

## Allowed statuses

`encoded`, `solver_result`, `proof_checked`, `ready_for_mathcert`, `rejected`.

## Rejection policy

Reject solver output without an exact encoding and version, reject UNSAT without a checked proof artifact, and reject SAT without a model that satisfies the original source constraints.

## Package

The package root is `lanes/sat_smt_proof`. Its toy fixture supplies a checked contradiction for `x AND NOT x`.

## Claim boundary

A checked SAT or SMT artifact certifies only the exact encoded instance. It does not establish an unstated family, asymptotic claim, or informal source interpretation.
