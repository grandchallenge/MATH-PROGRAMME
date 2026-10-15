RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0901-S01
PROBLEM_ID: 901
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: YES

## Exact statement and normalization
Let m(n) be the minimum number of edges of an n-uniform finite hypergraph whose vertex set cannot be 2-coloured without a monochromatic edge (equivalently, without Property B). Determine the asymptotic order of m(n) as n tends to infinity. This is NOT the already-settled weaker conjecture m(n)/2^n -> infinity.

## Dated status and primary evidence
Pinned 2025-08-31 source OPEN. Maintained https://www.erdosproblems.com/901 last edited 2025-12-28 still OPEN, no new solution claim. Erdős–Lovász, 'Problems and results on 3-chromatic hypergraphs and some related questions', Infinite and Finite Sets II (1975), pp609–627, p610; Erdős 1963/1964 constructions; Radhakrishnan–Srinivasan, 'Improved bounds and algorithms for hypergraph 2-coloring', Random Structures & Algorithms 16 (2000), pp4–32. Grill–Linzmayer, 'Improved Lower Bounds for Property B', arXiv:2403.05674 (2024), reports finite improvements, not closure of the asymptotic gap. Full analytic proofs not independently replayed.

## Strongest verified interface
Published asymptotic bounds: m(n) = Omega(2^n sqrt(n/log n)) and m(n) = O(n^2 2^n). The conjectural order n 2^n remains unsettled. Elementary independent bound: m(n) >= 2^(n-1), because a uniformly random red/blue colouring makes a given n-edge monochromatic with probability 2^(1-n), and a union bound gives positive probability of a proper colouring for fewer than 2^(n-1) edges (at equality union bound alone is inconclusive). Independently executed on CHAD an exhaustive two-colouring verifier: the 3-edge triangle (n=2) and 7-edge Fano plane (n=3) are not 2-colourable; deleting any one edge restores Property B. This verifies the examples, not global minimality or asymptotic order.

## Proposed bounded successor task
Input: n-uniform hypergraphs encoded by finite edge-bitsets; target: formalize exact Property B equivalence and verify minimal non-2-colourable witnesses for n=2,3, then reproduce one precisely stated finite lower-bound lemma from Grill–Linzmayer. Method: SAT/bitmask exhaustive colouring plus independent certificate checker; test edge deletion and random relabellings. Acceptance: byte-stable witness, every colouring obstructed, all single-edge deletions colourable, primary lemma hypotheses faithfully reproduced. Falsification: any valid colouring of the claimed obstruction or counterexample to claimed lower-bound lemma. Stop at the first unsupported primary-source hypothesis.

## Prerequisites and blocker
Obtain and source-lock full original Erdős–Lovász p610 and Grill–Linzmayer theorem text before claiming proof replay. No Solve campaign authorized. The source packet says 'statement formalized yes' but GCL admitted FC snapshot has no #901 statement; maintained page says 'formalised statement no'. This is provenance drift, not evidence of GCL formal certification.

## Reuse and claim boundary
Reuses catalogue bibliography and published asymptotic statements; CHAD finite fixture independently checks only two witnesses and single-edge deletion. No new asymptotic result, Lean proof, editorial protected admission, or independent reviewer approval is claimed.
