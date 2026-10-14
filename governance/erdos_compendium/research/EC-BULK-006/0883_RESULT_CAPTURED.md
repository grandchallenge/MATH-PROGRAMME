RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0883-S01
PROBLEM_ID: 883
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For A subset [n], G(A) is the simple coprime graph: distinct a,b adjacent exactly when gcd(a,b)=1. Write b(n)=floor(n/2)+floor(n/3)-floor(n/6). Under |A|>b(n), does G(A) contain every odd simple cycle C_q with q<=n/3+1? Separately, for every fixed ell>=1 and sufficiently large n, is a complete K_(1,ell,ell) present? Distinct graph vertices, floors and the strict threshold matter. These are two different questions, and only the first remains open.

## Dated status and primary evidence
Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 reports OPEN (Aug 31 2025), unformalized and source-refresh required; no protected FC statement. Maintained https://www.erdosproblems.com/883 edited Oct 24 2025 still marks the odd-cycle bound OPEN and reports solved fixed-tripartite case. PRIMARY Paul Erdős and Gábor N. Sárközy, 'On cycles in the coprime graph of integers', Electronic Journal of Combinatorics 4(2) (1997), paper #R8 https://www.combinatorics.org/ojs/index.php/eljc/article/download/v4i2r8/pdf/ , printed p2 Theorem 1 directly inspected: there exist c>0 and n0 such that n>=n0 and |A|>b(n) force ALL C_(2j+1) with 1<=j<=cn. It does NOT prove the conjectured upper length n/3+1. PRIMARY Gábor N. Sárközy, 'Complete tripartite subgraphs in the coprime graph of integers', Discrete Mathematics 202 (1999) pp227-238, DOI 10.1016/S0012-365X(98)00359-8, original publisher abstract independently checked; fixed-ell case is proved, in fact ell grows logarithmically. The maintained page states conservatively ell much greater than log n/loglog n. Its stronger precise iterated-logarithm quantitative bound needs source-locking before formal certification.

## Strongest verified interface
Let B_n={m<=n: 2 divides m or 3 divides m}. Inclusion-exclusion gives |B_n|=b(n). Partition B_n into evens and odd multiples of 3. Every pair within the even class shares factor 2 and every pair within the odd-multiple-of-3 class shares factor 3, so G(B_n) is bipartite and has no odd cycles. Thus the strict density threshold is sharp for triangles. GCL's reproducible exact finite_883_884.py fixture tests all n=3..12 GCD graphs with two independent triangle predicates, verifies the extremal bipartite example, and enumerates all strictly superthreshold subsets. For n=12, each of the 299 superthreshold subsets contains C3 and C5. These exact finite checks cannot prove the long-cycle conjecture. The 1997/1999 large-n results are published sources, not independently kernel-proved by GCL.

## Proposed bounded successor task
Input n>=3, B_n as defined, the simple coprime graph predicate, and the exact n<=12 finite fixture. Target: prove the floor cardinality |B_n|=b(n) and G(B_n) bipartite, hence odd-cycle-free, and formally align the simple-cycle predicate with direct GCD adjacency. Acceptance: complete paper lemma or pinned no-sorry Lean build with literal axiom report, two independently matching triangle algorithms, and all 299 n=12 superthreshold cases. Falsification: an odd cycle contained in B_n or a mismatched edge/triangle/cycle in the exact fixture. Stop at the finite interface; do not claim the unproved optimal odd-cycle length bound.

## Prerequisites and blocker
The primary 1997 and 1999 long proofs have not been independently reproduced or Lean-replayed. The sharp constant c=1/6 in the Erdős–Sárközy odd-cycle range is unresolved. There is no protected GCL formal statement for #883; this is a source-and-bounded-task audit, not an unselected Solve campaign.

## Reuse and claim boundary
Reused 1997 original theorem and 1999 publisher abstract, maintained catalogue, and locally derived exact density and bipartiteness lemma; finite fixture prepared offline and not yet CHAD-validated/branch-committed. This source return claims no new asymptotic theorem, independent full proof certification, protected editorial review, PR merge, or V2 admission.
