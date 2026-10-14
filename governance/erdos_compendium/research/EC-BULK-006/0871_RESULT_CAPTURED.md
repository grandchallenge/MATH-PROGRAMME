RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0871-S01
PROBLEM_ID: 871
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For an asymptotic additive basis A of order two, does divergence of the representation function force a partition A=B disjoint union C into two asymptotic bases? The answer is reported negative. The original counts ordered representations; the protected FormalConjectures statement counts unordered pairs. Exactly R_ord(n)=2 R_unord(n)-1_{n even and n/2 in A}; hence the two divergence hypotheses are equivalent. This identity does not by itself prove the counterexample.

## Dated status and primary evidence
Original Erdős–Nathanson, Partitions of bases into disjoint unions of bases, JNT 29 (1988), https://users.renyi.hu/~p_erdos/1988-25.pdf . D. Larsen, Three Questions of Erdős–Nathanson on Asymptotic Bases of Order 2, arXiv:2603.03472v1 (2026-03-03), https://arxiv.org/abs/2603.03472 reports independence of divergent representations, decomposability and minimal subbasis. Maintained https://www.erdosproblems.com/871 reports DISPROVED (LEAN), not independently certified here. Protected FormalConjectures commit 85f863718beeec7b58a3a1926ee92e3472bc2020 has 871.lean blob fdf5d953049115f140b1cff25b6376016566b1e8 with a sorry statement. External plby/lean-proofs 871.lean blob a004c9e4a1822d7c9dd0d2c1817febb62d8053cb claims not_erdos_871; no independent build performed.

## Strongest verified interface
The ordered/unordered identity and equivalence of divergence are elementary exact facts. The prepared offline audit checked 4,080 finite counting instances. External Lean theorem and Larsen's infinite counterexample are source-reported, not GCL kernel-certified or independently reproved.

## Proposed bounded successor task
Pin external 871 blob a004c9e4... and Lean v4.29.1/mathlib dependencies; clean-build Erdos871.not_erdos_871; capture literal #print axioms and all source SHAs; implement a semantic adapter negating the protected partition implication, checking Filter.atTop and unordered counting conventions. Accept only clean reproducible compilation, permitted axioms, no sorry in dependencies, exact semantic match. Stop at first failing dependency, quantifier mismatch, or unexpected axiom.

## Prerequisites and blocker
Exact dependency lock and independent Lean kernel replay, plus full primary-paper construction audit. The maintained catalogue and external CI are not independent mathematical certification.

## Reuse and claim boundary
Reused Larsen and Erdős–Nathanson sources, protected FC metadata, external Lean source inspection, and finite semantic checks. No independent infinite theorem proof, editorial acceptance, protected mutation or admission claimed.
