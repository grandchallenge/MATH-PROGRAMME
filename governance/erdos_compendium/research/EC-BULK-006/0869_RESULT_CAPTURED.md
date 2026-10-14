RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0869-S01
PROBLEM_ID: 869
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let B,C be disjoint positive-integer sets with B+B and C+C each cofinite. Must their union A contain an inclusion-minimal asymptotic basis D of order 2? Here minimal means D is a basis but deleting any single d from D destroys eventual two-term coverage. The negative resolution must show NO subbasis of A is minimal, not merely that A itself is nonminimal. Count unordered two-term representations a<=b, including diagonals.

## Dated status and primary evidence
Erdős–Nathanson, 'Partitions of Bases into Disjoint Unions of Bases', Journal of Number Theory 29 (1988), Part 3 Problem 4, printed p.8, https://users.renyi.hu/~p_erdos/1988-25.pdf. Frozen catalogue teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 labels DISPROVED. Maintained https://www.erdosproblems.com/869 records negative resolution. Primary Daniel Larsen, 'Three Questions of Erdős–Nathanson on Asymptotic Bases of Order 2', arXiv:2603.03472v1, 2026-03-03, https://arxiv.org/abs/2603.03472, Theorem 1 establishes independence of divergent representation, disjoint decomposition into bases, and existence of a minimal subbasis; P2=true and P3=false furnishes the counterexample. Theorem 2 uses a staged construction with reserved canary targets. Primary preprint abstract independently rechecked 2026-10-13; full probabilistic proof has NOT been independently reproduced by GCL.

## Strongest verified interface
For disjoint finite B,C the exact identity for unordered representations is r_{B union C}(n)=r_B(n)+r_C(n)+|{(b,c) in B x C:b+c=n}|. Every finite target-cover instance has an inclusion-minimal subcover by iterative deletion, so finite data alone cannot refute infinite minimal-subbase existence. In finite_869_870.py, a seeded partition of [160] into |B|=87, |C|=73 has both bases cover targets 60..160; count decomposition checked for n=2..320, and a minimal finite cover of size 51 has a loss-of-target certificate per element. These are elementary finite checks; the infinity-stage deletion property is Larsen's external theorem input.

## Proposed bounded successor task
Input: original 1988 problem, arXiv:2603.03472v1 Theorems 1–2 and staged construction, finite exact fixture. Target: independently prove the canary-to-deletion lemma for every asymptotic subbasis D, together with ordinary-target coverage, preserving all stage and cofinite quantifiers. Acceptance: source-locked full proof of both steps or a concrete falsification of an intermediate statement; finite fixture equality is only a regression check. Stop short of claiming independently reviewed infinite probabilistic construction if its hypotheses cannot be reconstructed.

## Prerequisites and blocker
Larsen's complete infinite staged argument, random events and canary coverage have not been independently line-by-line audited or Lean-replayed. No GCL protected proof formalization is admitted. Do not infer infinite conclusions solely from finite coverage.

## Reuse and claim boundary
Used the original 1988 paper, Larsen 2026 preprint, maintained catalogue and GCL finite work. No novel solution, formal certification, protected review, protected merge, or V2 editorial admission is asserted.
