# EC-BULK-007 critical sample #1090 — pending proof replay

**Status:** REVIEW_PENDING_PRIMARY_AND_LEAN_REPLAY. This is NOT a completed critical review.

- Source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2361#issuecomment-6162323194
- Source: https://www.erdosproblems.com/1090 and https://www.erdosproblems.com/forum/thread/1090
- Formal snapshot: google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020, ErdosProblems/1090.lean with unresolved sorry and an external plby/lean-proofs v4.29.1 link.
- Unaccepted draft: governance/erdos_compendium/editorial/1090.md

## Exact theorem boundary

The statement requires a finite planar set A such that, under any 2-colouring, one Euclidean line contains at least k points and ALL points of A on that line are monochromatic. This is stronger than merely finding k collinear points of one colour. A Feb 27 2026 forum report explicitly distinguishes an original weaker formal statement from a purported corrected Lean proof.

## Standard Hales–Jewett geometric reduction

Two-colour Hales–Jewett on the finite alphabet grid {0,...,k-1}^N supplies a monochromatic combinatorial line. Choose a generic linear projection from R^N to R^2 injective on the finite grid and introducing no new collinear triple. Such a map exists because finitely many point collisions and unwanted collinearities each define a proper algebraic zero set of matrix coefficients. A combinatorial line contains exactly k points of the grid; preserving absence of extra collinearity guarantees its projected geometric line contains exactly those k points. This is an established standard reduction, not a novel theorem or Lean certificate.

Independent finite fixture in ci/erdos_compendium_007_phase8_checks.py checks the map L(x,y,z)=(x+7y+49z,x+13y+169z) on 27 grid points: all images distinct, 2925 triples tested, 49 original collinear triples and zero new collinear triples. This does not establish that dimension 3 is enough for Hales–Jewett.

## Required before critical approval

Inspect Erdős 1975 p.106, Hales–Jewett source and Graham–Selfridge historical proof. Pin external Lean proof commit and its transitive dependencies; verify kernel check, full strong quantifier, no sorry/admit and no unsupported axioms. Complete an independent second-pass review. Until then 0/20 deterministic reviews completed, no protected source-fidelity approval.
