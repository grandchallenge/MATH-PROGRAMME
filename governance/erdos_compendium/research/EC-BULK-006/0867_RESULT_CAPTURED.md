RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0867-S01
PROBLEM_ID: 867
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let A={a_1<...<a_t} subset [1,N] contain no i<j<k for which a_i+...+a_j=a_k. Each prohibited block has at least TWO consecutive entries; a singleton is not prohibited. Erdős conjectured f(N)<=N/2+O(1) for maximum such |A|. This finite sequence question differs from the related infinite-sequence problem #839.

## Dated status and primary evidence
Original Erdős 1992, 'Some of My Forgotten Problems in Number Theory', printed pp42-43: https://hrj.episciences.org/125/pdf. Primary published Don Coppersmith and Steven Phillips, 'On a Question of Erdös on Subsequence Sums', SIAM Journal on Discrete Mathematics 9(2) (1996), 173-177, DOI https://doi.org/10.1137/S0895480193244139, original publisher abstract independently reconfirmed 2026-10-13. It states f(N)>=13N/24-O(1) and f(N)<=(2/3-1/512)N+log N. Freud 1993 earlier lower 19N/36. Frozen and maintained https://www.erdosproblems.com/867 mark DISPROVED; external Aristotle Lean proof mentioned April 2026 but GCL has not obtained exact compiled source or axiom output.

## Strongest verified interface
Elementary argument: if t members of A lie in (x,2x], their t-1 consecutive pair sums are distinct forbidden values in (2x,4x]. Hence |A intersect (x,4x]|<=2x+1 and summing 4-adic bands yields f(N)<=2N/3+O(log N). Stronger 1996 bounds are primary-publication claims, not independently replayed line-by-line. Independent finite branch-and-bound and direct fixed-cardinality enumeration give f(10)=6, f(15)=9, f(20)=12; valid N=20 witness (4,5,6,7,8,10,12,14,16,17,19,20). All C(20,13)=77520 thirteen-subsets excluded. The published 13/24 lower coefficient disproves N/2+O(1).

## Proposed bounded successor task
Source-lock the full 1996 proof and reproduce its 13/24 infinite family and strengthened upper-counting lemma in explicit arithmetic. Independently fetch and pin the April 2026 reported Lean proof, compare i<j<k semantics, perform actual build and axiom audit. Acceptance: uniform paper proof/verified source and exact fixture agreement for N=10,15,20; falsification by a valid thirteen-element N=20 example or inconsistency in the exact construction. Stop if full source or formal dependency is unavailable.

## Prerequisites and blocker
1996 publisher abstract available and primary constants checked; full paper proof not line-by-line audited. External Lean claim NOT independently replayed. No GCL protected formal statement or independent mathematical certification established.

## Reuse and claim boundary
Used the original 1992 statement, primary 1996 publisher abstract, maintained record, and independently reproduced finite algorithms from the offline EC-BULK-006 research package. This is an authenticated source return only, not a novel asymptotic discovery, approved review, protected merge, or editorial admission.
