RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0860-S01
PROBLEM_ID: 860
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For each prime p<=n, select a different multiple of p in a fixed interval uniformly over its integer starting point m. Erdős-Pomerance (1980) use (m,m+H], containing H integers; the maintained question uses literal (m,m+h), containing h-1 integers for integral endpoints. Thus h=H+1 for the exact optimal integer parameters. The all-moduli F(n) and prime-only h_P(n) are different functions.

## Dated status and primary evidence
Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 marks problem OPEN (2025-08-31), with historical n^(3/2)/(log n)^(1/2) upper bound. Erdős and Pomerance, 1980 printed p.159: https://math.dartmouth.edu/~carlp/PDF/matching.pdf. Primary new paper Kaizhe Chen and Samuel Korsky, 'Improved Bounds for Distinct Multiples in Intervals', arXiv:2607.26450v2, Theorems 1.2 and 1.3, https://arxiv.org/html/2607.26450v2, inspected 2026-10-13. Authors claim h_P(n)<<n^(4/3)/(log n)^(1/3) and h_P(n)>=n exp[((log 2)/2-o(1))*log n/loglog n]. These supersede weaker v1 estimates. Status remains open because the true asymptotic order is not determined.

## Strongest verified interface
For each residue m modulo primorial Q=prod_{p<=n}p, connect each prime p to integers in {m+1,...,m+H} divisible by p. Hall's condition |union_{p in S} N(p)|>=|S| for EVERY subset S of prime vertices is necessary and sufficient for distinct multiples. The entire condition depends only on m modulo Q. Two independently checked exact computations, bipartite matching and Hall enumeration in governance/erdos_compendium/research/EC-BULK-006/finite_860.py, find optimal right-closed H(2,3,5,7,11)=(2,4,6,10,14). Literal open-interval h is H+1. The 2026 asymptotic bounds are attributed primary-paper claims; their proofs were not independently reproduced.

## Proposed bounded successor task
Given n in {2,3,5,7,11}, prove prime-neighborhood periodicity and the exact finite Hall equivalence, with correct repeated-divisibility and endpoints. Acceptance: checked paper lemma or Lean proof and two independent exact programs yielding H=(2,4,6,10,14) for ALL residues; falsification by a residue and prime subset with contradictory Hall/matching outcomes. Stop before claiming improved asymptotic constants, priority or an unselected Solve campaign.

## Prerequisites and blocker
Specify right-closed versus open conventions and freeze the exact primary arXiv v2. Independent scrutiny of Chen-Korsky Sections 2, 4 and 5, including uniform progression estimates, remains an open proof-review task. No protected formal statement has been admitted.

## Reuse and claim boundary
Reused the existing GCL #860 editorial draft, original 1980 source, authors' 2026 v2 and exhaustive local fixture. This source return is evidence for adjudication only. No new mathematical proof, independent review, formal certificate or protected editorial acceptance is claimed.
