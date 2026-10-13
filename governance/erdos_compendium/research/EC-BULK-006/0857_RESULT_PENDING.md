RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0857-S01
PROBLEM_ID: 857
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For fixed k>=3 and n>=0, m(n,k) is the least t such that every family of at least t DISTINCT subsets of [n] contains k distinct sets with the same pairwise intersection (a k-sunflower). The subsets need not have equal size: this is the non-uniform/weak sunflower problem. Estimate m(n,k) as n tends to infinity. Erdős originally used common pairwise UNION, equivalent via complement inside [n]. Primary original: Erdős, 'Some Extremal Problems in Combinatorial Number Theory' (1970), printed pp.127-128, https://users.renyi.hu/~p_erdos/1970-21.pdf .

## Dated status and primary evidence
Pinned teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89: OPEN, 2025-08-31, admitted formal statement. Maintained https://www.erdosproblems.com/857 fetched 2026-10-13 (HTTP 200): still asks for estimates. Original 1970 pp.127-128 directly inspected. Naslund and Sawin, 'Upper bounds for sunflower-free sets', Forum of Mathematics, Sigma 5 (2017), e15, published 2017-06-27, https://doi.org/10.1017/fms.2017.12 ; primary arXiv:1606.09575 abstract supplies |F|<=3n sum_{j<=n/3} C(n,j) <= (3/2^(2/3))^(n(1+o(1))) for 3-sunflower-free families. Frozen Formal Conjectures 857.lean, https://github.com/google-deepmind/formal-conjectures/blob/85f863718beeec7b58a3a1926ee92e3472bc2020/FormalConjectures/ErdosProblems/857.lean , defines m via sInf and states a conjectural answer(sorry) asymptotic with `by sorry`; no proof. No open/solved status drift detected.

## Strongest verified interface
For universe U=[n], (U\A) union (U\B)=U\(A intersect B). Complement is bijective, so union-sunflowers and intersection-sunflowers have the same extremal threshold. Naslund-Sawin's 2017 theorem yields m(n,3)<=1+3n sum_{j<=n/3} C(n,j) and exponential upper base 3/2^(2/3). This is a primary published theorem, not a claim of a sharp asymptotic. Independent exhaustive enumeration of all families of subsets of [n], checking all distinct triples for equal pairwise intersections, gave m(1,3)=3, m(2,3)=4, m(3,3)=6, m(4,3)=9. The n=1 value is vacuous because only two distinct subsets exist. These are finite checks, not a proof of an asymptotic formula.

## Proposed bounded successor task
Inputs: Erdős 1970 pp.127-128, Naslund-Sawin 2017, protected 857.lean and exact exhaustive fixtures n=1..4,k=3. Prove in Lean that complement preserves family size and translates common pairwise intersection into common pairwise union; derive m(n,k)=1+max cardinality of sunflower-free families for finite n. Accept type-checked equivalence and independently reproduced m(n,3)=3,4,6,9. Falsify with an explicit family exposing a duplicate, n=0 or empty-family semantic mismatch. Stop before filling the unknown asymptotic `answer(sorry)` or asserting an improved exponential bound.

## Prerequisites and blocker
Need compiled review of IsSunflower, sInf and n,k boundary conventions in the admitted Lean source; not a blocker to this source audit. The full 2017 polynomial-method proof was not independently reproduced. Do not conflate this weak non-uniform problem with the uniform-size sunflower conjecture #20.

## Reuse and claim boundary
Used original Erdős 1970 pp.127-128, current #857 page, primary Naslund-Sawin 2017 abstract, frozen 857.lean and GCL issue #2128. Finite values are exhaustive checks; no Lean certificate, mathematical certification, new general theorem or editorial acceptance is claimed.
