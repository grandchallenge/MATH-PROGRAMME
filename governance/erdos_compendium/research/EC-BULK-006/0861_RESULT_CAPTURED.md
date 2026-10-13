RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0861-S01
PROBLEM_ID: 861
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
A Sidon set S in [N] has all unordered sums a+b, including a=b, distinct. Let f(N) be maximal Sidon cardinality and A(N) the number of all such subsets. Original Cameron-Erdos questions: does A(N)/2^f(N) tend to infinity? Is A(N)=2^((1+o(1))*f(N))? They are separate questions.

## Dated status and primary evidence
Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 records SOLVED at 2025-08-31. Original Erdős 1992 p.38, equations (13)-(14): https://hrj.episciences.org/125/pdf. Primary published proof: David Saxton and Andrew Thomason, 'Online containers for hypergraphs, with applications to linear equations', JCTB 121 (2016) pp.248-283, Theorem 1.10 and Section 5 lower-bound proof: https://arxiv.org/html/1611.01433 (read 2026-10-13). Maintained https://www.erdosproblems.com/861 confirms first YES, second NO. No protected GCL formalization or independent Lean proof certification.

## Strongest verified interface
For prime p let q=p(p-1) and take a modular Sidon set S subset [q] with |S|=p-1 (Ruzsa). Assign each s in S to exactly one of five states: omitted, or in one of four translated blocks S+i*q, i=0,1,2,3. Each of the 5^(p-1) resulting subsets of [4q] is Sidon: reduction of equal sums modulo q forces equal unordered base pairs; unique assignment prevents a lifted collision. As f(N)~sqrt(N) and consecutive primes have ratio approaching 1, A(N)>=2^((log_2 sqrt(5)+o(1))*sqrt(N)), with log_2 sqrt(5)>1. Therefore A(N)/2^f(N)->infinity and A(N)=2^((1+o(1))*f(N)) is FALSE. This is an exposition of the published theorem, not a new proof. Exact independently implemented enumeration gives A(10)=216,f(10)=4 and A(20)=6845,f(20)=6; bitmask cross-check through N=13.

## Proposed bounded successor task
Input: modular Sidon S subset [q], Saxton-Thomason Section 5 and finite_861.py. Prove the four-translate/five-choice lifting lemma, including pairs a=a, and give a formal source-locked statement with explicit modular Sidon hypotheses. Acceptance: reviewed complete proof or compiled Lean theorem without sorry, plus separate exhaustive constructions for p=3 (25 sets) and p=5 (625 sets). Falsify with two genuinely distinct unordered pairs with equal integer sums. Stop before claiming reproof of Ruzsa's modular-base existence or independent asymptotic certification.

## Prerequisites and blocker
Ruzsa modular Sidon existence and the asymptotic prime-density step are external inputs. Full independent Lean compilation and literal axiom readback have not been performed. The community SOLVED label does not mean GCL editorial acceptance.

## Reuse and claim boundary
Used the original question, the primary 2016 proof, frozen/current status, existing cohort fixture and source research. Finite calculations are exact local checks, not asymptotic proof replay. No new priority, solved-status change, protected admission or certification is asserted.
