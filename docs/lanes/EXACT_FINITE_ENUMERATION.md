# Exact Finite Enumeration to Certificate

## Obligation

Use this lane when the theorem obligation is explicitly finite. The carrier, bound, equivalence relation, generation rule, and pruning rule must be fixed before enumeration starts.

## MATHFORGE

MATHFORGE defines the bounded search object, generates exact cases, records symmetry or pruning reductions, and emits a deterministic witness ledger. It must preserve enough information to reconstruct every omitted equivalence class.

## MATHSOLVE

MATHSOLVE checks that the finite screen matches the intended local obligation. It separates a bounded theorem from any unbounded conjecture and selects the smallest replayable representation.

## MATHCERT

MATHCERT recomputes the canonical finite carrier, replays exact generation and pruning, checks the count and witness digest, and certifies only the stated bounded proposition.

## Allowed statuses

`bounded`, `enumerated`, `replayed`, `ready_for_mathcert`, `rejected`.

## Rejection policy

Reject implicit bounds, unreconstructable pruning, floating-point identity tests, and any inference from a finite range to an unbounded statement.

## Package

The package root is `lanes/exact_finite_enumeration`. It contains the input schema, handoff schema, and a complete toy enumeration of the subsets of a two-element labelled set.

## Claim boundary

A complete finite enumeration proves only the stated finite range. It does not establish the corresponding asymptotic or universal conjecture.
