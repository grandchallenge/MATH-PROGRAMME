RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0859-S01
PROBLEM_ID: 859
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For integer t>=1 let E_t={n>=1: there exists a finite set S of DISTINCT positive divisors of n with sum_{d in S}d=t}. Define d_t=lim_{X->infinity}|E_t intersect [1,X]|/X, which exists. Is d_t asymptotic to c1/(log t)^c2 for some fixed positive c1,c2 as t->infinity? Source: P. Erdős, 'Some Extremal Problems in Combinatorial Number Theory' (1970), printed pp.130-131, Section 3, equations (31)-(33), https://users.renyi.hu/~p_erdos/1970-21.pdf . This is a subset sum over DIVISORS, not over all integers <=t, and summands must be distinct.

## Dated status and primary evidence
Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89: OPEN, last update 2025-08-31. Maintained #859 and history/859 indexed in October 2026 still OPEN; no reported solution in comments. Erdős 1970 printed p.130 proves d_t exists and tends to zero and provides upper/lower power-of-log bounds on pp.130-131, while suggesting a specific power-law asymptotic at Eq.(33). Original source directly inspected. Protected Formal Conjectures file https://github.com/google-deepmind/formal-conjectures/blob/85f863718beeec7b58a3a1926ee92e3472bc2020/FormalConjectures/ErdosProblems/859.lean defines `DivisorSumSet` with a finite subset of `Nat.divisors n`, states the open asymptotic and an auxiliary density theorem, and retains `sorry` placeholders; its `DivisorSumSet 0 = Set.univ` is a separately proved trivial lemma. No Lean proof of the open question is present.

## Strongest verified interface
Elementary exact periodicity: put L_t=lcm(1,2,...,t). Every representation of t uses distinct summands d<=t; its lcm m divides L_t, and n supports that representation exactly when m|n. Thus E_t is a FINITE UNION of sets of multiples of m|L_t, and membership depends only on n mod L_t. Consequently d_t is a rational number and can be computed exactly as (# favorable residues in [1,L_t])/L_t. Also d_t>=1/t, since t itself is a divisor of every multiple of t. This refines the elementary t!-period argument in Erdős's original p.130, but no novelty is claimed. Independent exact computations by (a) all distinct partitions of t into divisor candidates, reducing to minimal LCM witnesses, and (b) direct subset-sum bitset over divisors of each n in one full period agree for every 1<=t<=12. Values: d_1=1, d_2=1/2, d_3=2/3, d_4=1/2, d_5=d_6=7/15, d_7=16/35, d_8=3/7, d_9=17/45, d_10=2/5, d_11=13/33, d_12=43/99. These are finite exact values, not evidence of the power-law limit.

## Proposed bounded successor task
Input: Erdős 1970 printed p.130, protected 859.lean, and governance/erdos_compendium/research/EC-BULK-006/finite_859.py. Formalize for each t>=1 the equivalence `n in DivisorSumSet t` iff some minimal witness m|L_t divides n, prove the period L_t and existence/rationality/positivity of the natural density, and test t=1..12. Acceptance: a Lean proof without `sorry` of the finite periodicity and HasDensity lemma with correct n=0 and t=0 boundary handling, plus exact agreement with independent rational fixtures; falsification by explicit (n,t) violating the witness equivalence or density mismatch. Do NOT attempt to infer c1,c2 from twelve values. Stop at the periodicity/density lemma and hand off asymptotic estimates to a separate research problem.

## Prerequisites and blocker
Original 1970 primary source, pinned Lean file and finite arithmetic evidence are available. Lean compilation and semantic review of Nat.divisors(0), HasDensity and natural-density conventions remain outstanding. Erdős's power-law exponent and constant remain open. An authenticated issue-bound RESULT/1 comment is pending because the external write action was blocked; the existence of this local file is NOT a posted return or protected mathematical acceptance.

## Reuse and claim boundary
Used the 1970 original pp.130-131, maintained #859/history/859, pinned GCL issue #2130, protected 859.lean and two independent local finite arithmetic implementations. The finite periodicity lemma is elementary and may be known; no novelty or general asymptotic theorem is claimed. No Lean certificate, independent editorial acceptance, GitHub issue-comment return or public publication is asserted.
