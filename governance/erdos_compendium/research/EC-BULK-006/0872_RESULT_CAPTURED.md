RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0872-S01
PROBLEM_ID: 872
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Two players choose distinct integers in {2,...,n} while maintaining a primitive set (no selected element divides another). Prolonger maximizes terminal cardinality and Shortener minimizes it. The original 1992 question does not specify who moves first; protected FC 872 chooses Prolonger first. Weak question: eventually L_P(n)>=epsilon n for some epsilon>0. Strong question: eventually L_P(n)>=(1-epsilon)n/2 for every epsilon>0. Terminal positions are inclusion-maximal primitive sets, not necessarily maximum-size sets.

## Dated status and primary evidence
Original Erdős 1992 [Er92c] p.47 (printed page not newly inspected); https://www.erdosproblems.com/872 and /history/872 edited 2026-04-24, maintained OPEN. The page reports a 23/48 upper strategy; April 2026 forum claims a stronger <0.19n bound, not independently certified. Protected FormalConjectures commit 85f863718beeec7b58a3a1926ee92e3472bc2020, 872.lean blob e1c94bfaf9ff2964bfa2664d9af467ea42d6d26b defines Prolonger-first minimax with sorry targets.

## Strongest verified interface
Illegality is monotone under added selections; hence selected-antichain and remaining-legal-set minimax recursions are equivalent. Two independently implemented exact minimax solvers agreed for 2<=n<=30 for both first-player conventions. Values L_P(9)=5,L_S(9)=4; L_P(25)=11,L_S(25)=10; L_P(30)=13,L_S(30)=11. For terminal S, pi(n)-pi(floor(n/2)) <= |S| <= ceil(n/2), using isolated large primes and odd-part chains. No asymptotic theorem follows from the finite cases.

## Proposed bounded successor task
Use pinned FC 872 game definitions and offline finite_871_872.py/JSON. Prove monotone-illegality and recursion equivalence in Lean with explicit first-player parameter; prove L_P(9)=5 and L_S(9)=4 with checked finite computation. Accept only exact-head build, permitted axioms, and agreement with two independent Python solvers. Stop on any convention mismatch or failed proof.

## Prerequisites and blocker
Original 1992 printed source and adaptive strategy behind reported 0.19 upper bound require primary verification. The question remains open; no independent Lean replay or asymptotic proof claimed.

## Reuse and claim boundary
Reused maintained catalogue, protected FC definition and forum claim. Finite minimax and elementary bounds are bounded GCL computations, not independent proof of the asymptotic conjectures, editorial acceptance, protected mutation or admission.
