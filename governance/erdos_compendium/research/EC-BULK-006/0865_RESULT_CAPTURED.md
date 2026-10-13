RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0865-S01
PROBLEM_ID: 865
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For A subset [N], seek three distinct a,b,c in A such that a+b,a+c,b+c are all IN A. Let f3(N) be the least integer cardinality forcing this configuration. Problem #865 asks for sharp threshold f3(N)=5N/8+O(1); both original members and their pair sums must lie in A. Distinctness applies to a,b,c.

## Dated status and primary evidence
Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 recorded PROVED (LEAN), dated July 2, 2026. Maintained https://www.erdosproblems.com/865 reports solved. Ricky Cipollini, 'A sharp 5/8 bound for an Erdős-Sós pairwise-sums problem', arXiv:2606.29361 submitted June 28 2026, https://arxiv.org/abs/2606.29361, claims unconditional self-contained 5/8+O(1) upper bound. The abstract explicitly distinguishes an earlier CONDITIONAL Lean-formalized reduction from the entire unconditional mathematical proof. Additional public standalone formal development in Jayyhk/erdos-lean commit 078023fb42853105e51c825e24e909e4faf0e69d, path problems/865/Erdos865.lean, claims theorem 8*|A|<=5*N+53 and #print axioms with only standard axioms, but exact pinned build/output not independently reproduced by GCL.

## Strongest verified interface
For M>=1, A_M=[M,2M] union [4M,8M] is triple-free with |A_M|=5M+2 inside [8M]. Distinct-triple exact verification for M=1,2,3,4,5,8,12,20,40 passes in finite_865_866.py/json; this verifies lower-bound sharpness examples, NOT general upper theorem. The cited Cipollini paper proves the sharp 5N/8+O(1) upper claim mathematically; the external standalone Lean source's claimed 8|A|<=5N+53 would suffice if correctly compiled with matching exact predicates. No independent GCL formal certification.

## Proposed bounded successor task
Input: 2026 Cipollini theorem, frozen FormalConjectures predicate, exact standalone Lean source+toolchain commit (Lean v4.28.0, mathlib 8f9d9cff6bd728b17a24e163c9402775d9e6a365), finite sharpness sets. Target: establish semantic equivalence of all three predicates and reproduce exact-source Lean theorem for 8|A|<=5N+53 with literal #print axioms output and no project axioms/placeholders. Acceptance: matched formal statement plus clean pinned kernel check; falsify by a finite predicate mismatch, a failed exact build, or a triple-free set violating the bound. Stop at this bounded equivalence/replay gate, not an unselected Solve job.

## Prerequisites and blocker
Original proof and external Lean source have NOT been line-by-line or kernel independently audited. Protected provider statement may still contain sorry placeholders; do not treat statement declaration as a proof. External code's source-level grep is not an axiom audit.

## Reuse and claim boundary
Used maintained statement, primary arXiv abstract, external formal source metadata and exact finite construction. No novelty, solved-status change, independent Lean certification, protected review or editorial admission claimed.
