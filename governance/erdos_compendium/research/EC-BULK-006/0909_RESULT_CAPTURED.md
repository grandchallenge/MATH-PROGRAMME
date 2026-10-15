RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0909-S01
PROBLEM_ID: 909
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For every integer n>=2, does there exist a topological space S with topological DIMENSION dim S=n but dim(S x S)=n instead of 2n? YES, published Anderson–Keisler 1967. Dimension is INDUCTIVE/covering topological dimension for separable metric spaces, not vector-space linear rank. S is a highly noncompact subspace of Euclidean R^(n+1), not an ordinary n-dimensional manifold or compact cube. A fixed one space, its cartesian square. The 1967 original theorem is much STRONGER: for any Euclidean ambient exponent q>=1 one K subset R^q has dim K=dim K^s=dim K^omega=q-1 for all finite s>=1 and countably infinite product omega.

## Dated status and primary evidence
Erdős historical [Er82e] https://www.erdosproblems.com/909 current PROVED and cites Anderson and Keisler [AnKe67]. Primary R. D. Anderson and J. E. Keisler 'An Example in Dimension Theory', Proceedings American Mathematical Society 18 no4 (1967) pp709–713, DOI 10.1090/S0002-9939-1967-0215288-0, exact issue bibliographic https://www.jstor.org/stable/i335948 and primary publisher https://pubs.ams.org/journals/proc/1967-018-04/S0002-9939-1967-0215288-0. Theorem 1 on p712: for given positive q and fixed s construct K subset R^q with dim K=dim K^s=q-1. Theorem 2, introduced pp709 and stated p712: ONE K works for all finite s and omega, dimensions q-1. Scholarly primary-page review https://erdosproblems.ai/wiki/library/analysis/anderson_1967_example_dimension_theory records actual scanned page clause inspection and proof NOT independently reconstructed. Source proofs use transfinite continuum-hitting/sphere-avoidance and four dimension-theory lemmas. Original Erdős 1982 page not independently image checked here. No formalized statement indicated in maintained catalogue and no GCL Lean kernel.

## Strongest verified interface
Elementary rigorous instantiation: given Anderson–Keisler published Theorem 2 for q=n+1, substitute s=1 and s=2 to obtain dim K=dim(KxK)=q-1=n, hence affirmative #909. No need two separate constructions for different powers. GCL finite fixture finite_908_909.py/json checks q=n+1 and s=1..6 for n=1..9, 54 integer substitutions. Finite 1..4 point discrete sets have dim0 since singleton open refinement has order1; every finite discrete square still dim0; exact fixture exhaustively checks every open-cover family n<=4 (n4 32297 valid among 32768 families). Ordinary cube [0,1]^n is dim n and square [0,1]^(2n) is dim2n, showing usual compact manifold is wrong object. Finite point samples cannot establish the unusual infinitely constructed space's dimension, so do NOT call finite check independent proof of Anderson–Keisler theorem.

## Proposed bounded successor task
Formalize exact implication from published all-finite-powers theorem for arbitrary q to Erdos target n>=2, fixing product topology, same K for all s and setting q=n+1, s=1,2. Acceptance complete elementary proof or pinned no-sorry Lean with literal axiom report plus 54 finite index substitutions, finite discrete cover check. Then independently reconstruct 1967 original Theorems1/2 including transfinite choice over nondegenerate continua, countable avoiding spheres, lemmas1–4 and dimension bounds, precisely distinguishing fixed s from all s and countable products. Stop short of claiming general topological theorem proven by GCL finite fixture.

## Prerequisites and blocker
Original 1967 5-page primary proof not independently replayed (source statements and summary inspected by prior scholarly review). Transfinite dimension-theory lemmas and axiom dependencies not kernel formalized, no protected GCL mathematical review or main editorial admission.

## Reuse and claim boundary
Reuses established Anderson–Keisler 1967 mathematical result, maintained catalogue historical pointer and accurate theorem-card primary source account, independently proves logical q=n+1 substitution and finite discrete cover examples. No new topology theorem, independent original-proof check, Lean proof, protected merge, deployed MathJax browser verification or V2 admission.
