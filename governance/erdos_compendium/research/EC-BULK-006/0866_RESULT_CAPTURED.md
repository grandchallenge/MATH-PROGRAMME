RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0866-S01
PROBLEM_ID: 866
DISPOSITION: STATUS_CONFLICT
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let A subset [2n] with |A|>=n+t. Find k distinct INTEGER b_i (unrestricted variant g_k) or distinct POSITIVE integers b_i (variant h_k) such that ALL b_i+b_j, i<j, lie in A. Crucial: the pairwise sums themselves are NOT required distinct; b_i need not be elements of A. The least such surplus is g_k(n) or h_k(n). The 1992 original refers to unrestricted distinct integers; later papers distinguish positive version.

## Dated status and primary evidence
Pinned teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 states OPEN (2025-08-31) with historical g3,g4,g5 remarks. Original P. Erdős, 'Some of My Forgotten Problems in Number Theory' 1992 printed p.41, https://hrj.episciences.org/125/pdf. Choi, Erdős, Szemerédi 1975 Acta Arith 27 pp37-50, https://users.renyi.hu/~p_erdos/1975-39.pdf. Wouter van Doorn, arXiv:2605.00040 (April 2026) distinguishes integer/positive g_k,h_k. John Erlbacher 2026-07-08 frozen release records large-n h4=4 and partial k5. NEW PRIMARY Wouter van Doorn and John Erlbacher, 'The cardinality of a set containing the pairwise sums of four positive integers', arXiv:2609.39314, submitted 2026-09-30 updated 2026-10-01, https://arxiv.org/abs/2609.39314, proves h4(n)=4 for ALL n>=6 and calls it optimal; authors report Aristotle formalization, not independently kernel replayed by GCL. Maintained catalogue's old blanket OPEN status and unqualified g4 bounds are materially stale.

## Strongest verified interface
Source-reported exact thresholds: g3(n)=1 (n>=3), g4(n)=3 (n>=2), h3(n)=2 (n>=4), h4(n)=4 (n>=6); finite exception h4(5)=5. An exact independent subset-zeta forcing program enumerated ALL A subsets [2n] for n=2..7 and distinct candidate b tuples, using the SET of six pair sums without imposing sum distinctness. It matches g4(n)=3 for n=2..7; h4(3,4,6,7)=4; h4(5)=5. In n=5, A=[10] minus {5} is a nine-element positive-four-tuple counterexample; for n=6 all 66 ten-element subsets force a positive quadruple. Exact fixture finite_865_866.py/json on CHAD is finite evidence only. General k>=5 is NOT settled by the sharp k=4 theorem.

## Proposed bounded successor task
Input: original 1992 unrestricted quantifier, 2026 arXiv 2605.00040 and 2609.39314 positive statements, and exact finite fixture. Target 1: formalize semantic distinction g_k vs h_k and prove finite witness-mask equivalence allowing repeated pair sums; acceptance independent direct brute-vs-mask checks at n=5,6 and no-sorry Lean equivalence. Target 2: pin September 2026 theorem's exact Aristotle-generated Lean source/dependencies and reproduce h4(n)=4 for n>=6 with literal compiler/axiom output. Falsify by a mask/direct mismatch or a valid positive-free set size >=n+4 for n>=6. Stop at four-variable claim and leave k>=5 separate.

## Prerequisites and blocker
Authors' formalization has NOT been independently compiled or axiom audited. Do not merge g with h or infer a universal solution for all k from k=3,4. Source-fidelity to all positive and boundary conventions is essential.

## Reuse and claim boundary
Reused older primary sources, two dated 2026 papers and exact finite computation; new theorem is attributed, not an original GCL proof. No independent formal certificate, mathematical status promotion, review or protected admission claimed.
