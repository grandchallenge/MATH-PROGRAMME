RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0876-S01
PROBLEM_ID: 876
DISPOSITION: STATUS_CONFLICT
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
An infinite increasing A={a_1<a_2<...} is sum-free in the subset-sum sense if no a in A is the sum of two or more DISTINCT smaller members. Ask how small individual gaps a_{n+1}-a_n can be, especially whether they can be <n. Literal all-index inequality is false already for n=1, so the intended eventual-index reading needs primary source fidelity. This predicate is weaker than #875 admissibility: {4,5,6,7,8} is #876-sum-free but 4+5+6=7+8, violating #875.

## Dated status and primary evidence
Deshouillers, Erdős and Melfi, 'On a Question About Sum-Free Sequences', Discrete Mathematics 200 (1999), pp.49–54, https://libra.unine.ch/bitstreams/142bfa87-1d9c-44b6-8269-2b2903cdc132/download, PRIMARY PDF visually inspected on 2026-10-14. Theorem 1 proves zero asymptotic density, Theorem 3 produces sum-free A with a_{n+1}/a_n ->1, and Theorem 4 produces, for each delta>0, a_n~n^(3+delta). They do NOT assert eventually gaps<n. Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 and maintained https://www.erdosproblems.com/876 mark OPEN. July 18 2026 Liam Price/GPT-5.6 Sol Pro proposed proof recorded by https://www.erdosproblemaday.com/report/876 claims for EVERY infinite sum-free A, limsup (a_{n+1}-a_n)/n=infinity. The report marks it PARTIAL CLAIM / SKIPPED, not verified; underlying submitted proof was inaccessible to GCL. Do not promote the status based on its abstract.

## Strongest verified interface
For finite A subset [1,N] with the same distinct-smaller-summand ban, the maximum possible size H(N) equals floor(N/2)+1 EXACTLY. Lower bound: A={ceil(N/2),...,N} works, because two distinct members sum beyond N. Upper bound: with maximum m in A, of each disjoint pair {x,m-x}, x!=m-x, at most one can belong to A; possible midpoint m/2 is allowed (repeated smaller terms prohibited), and m itself contributes one. Hence |A|<=floor(m/2)+1<=floor(N/2)+1. Finite verifier finite_875_876.py/json independently tested 1,942 terminal-interval cases, 36 finite formula assertions, direct-vs-DP agreement at N=8,10,12,14, and six larger DP extrema. This finite theorem DOES NOT imply the submitted infinite limsup claim.

## Proposed bounded successor task
Input: actual July 2026 submission including every lemma, the 1999 Theorems 3–4 constructions, and exact infinite subset-sum-free predicate. Target: independently prove or refute the universal normalized-gap statement limsup (a_{n+1}-a_n)/n=infinity. Method: expose quantifiers, audit each density-to-gap implication and test candidate lemmas on known polynomial growth examples; formalize if feasible with pinned dependencies. Acceptance: source-accessible complete proof independently reviewed or a valid infinite counterexample with bounded normalized gaps. Falsify by a counterexample to any intermediate lemma. Stop before declaring #876 solved unless the proof clears independent adjudication; a separate bounded Lean proof of the exact finite H(N) is legitimate.

## Prerequisites and blocker
Original Erdős 1998 chapter not directly inspected for all-index versus eventual inequality. July 2026 submitted argument unavailable to independent reviewer; only third-party SKIPPED/PARTIAL description available. No protected Formal Conjectures statement or successful Lean axiom replay for #876.

## Reuse and claim boundary
Reused and visually inspected primary 1999 paper, maintained community record and independent finite fixtures. The finite H(N) result is elementary, not a new solution to the infinite problem. No novel infinite theorem, independent 2026 proof certification, protected review, merge, public browser check or editorial admission claimed.
