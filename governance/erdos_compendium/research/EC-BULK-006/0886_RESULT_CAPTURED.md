RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0886-S01
PROBLEM_ID: 886
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For every fixed real epsilon>0, does there exist constant K_epsilon (independent of n) such that all sufficiently large positive integers n have at most K_epsilon positive divisors d in the STRICT open interval (sqrt(n),sqrt(n)+n^(1/2-epsilon))? At the critical epsilon=1/4 width is n^(1/4). Historical known 1997 result concerns [sqrt(n),sqrt(n)+C*n^(1/4)] for FIXED C and permits bound 1+C², not a universal K independent of C; separate #887 requires such an absolute K. Distinguish all n versus squares and exact strict/closed endpoints.

## Dated status and primary evidence
Paul Erdős & Moshe Rosenfeld, 'The factor-difference set of integers', Acta Arithmetica 79(4) (1997) 353–359 DOI 10.4064/aa-79-4-353-359, journal page https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/79/4/109554/the-factor-difference-set-of-integers, Proposition 4.1 yields at most 1+C² divisors in CLOSED interval [sqrt n,sqrt n+C*n^(1/4)] eventually and exhibits infinitely many n with >=4 above-root divisors within 16*n^(1/4). Current maintained https://www.erdosproblems.com/886 OPEN and attributes stronger conjecture to Ruzsa. Tsz Ho Chan, 'Factors of a perfect square', Acta Arithmetica 163 (2014) 141–143 DOI 10.4064/aa163-2-4, publisher abstract source https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/163/2/82006/factors-of-a-perfect-square proves at most five divisors for perfect squares in SYMMETRIC window of width n^(1/4)*(log n)^(1/7). Original 1997 printed text indexed with proposition formulas, not independently fully replayed via pdf reader; no GCL Lean proof. Formal Conjectures 886.lean publicly defines the open theorem using real-power intervals, body sorry, not verified proof.

## Strongest verified interface
Independently proved perfect-square one-sided-gap lemma: if n=t²=ab and a<t<b, let a=t-u,b=t+v with positive integers u,v. Expanding gives t(v-u)=uv>0; hence v>u>=1, so v-u>=1, thus uv=t(v-u)>=t and v²>uv>=t. Therefore b-t=v>sqrt(t)=n^(1/4); no perfect square n has divisor in (sqrt n,sqrt n+n^(1/4)). Exact CHAD finite_885_886.py/json checks ALL t=2..2000 using integer-only (d-t)^2<C²*t equivalence for integer C=1,2,3; C=1 count ZERO, C=2 max2, C=3 max3 in that finite range. This is a rigorous special-family lemma, not a solution of all-n Ruzsa conjecture or wider epsilon<1/4 case.

## Proposed bounded successor task
Input positive integer t, factors a*b=t², a<t<b, and integer δ=b-t>0. Target no integer divisor b in strict (t,t+sqrt t) via t(v-u)=uv. Acceptance: complete proof or pinned no-placeholder Lean lemma with literal axiom output and exact square family regression t<=2000, including strict endpoints. Reject any putative counterexample with (b-t)^2<t, or equality mishandled. Next distinct research: n nonsquare, epsilon in (0,1/4), seek n-independent counts without inferring from n=t² or critical-width results. STOP at finite square-family lemma until genuine all-n bound or counterexample.

## Prerequisites and blocker
General Ruzsa conjecture OPEN; critical width 1997 proof and Chan 2014 special theorem not independently kernel-replayed, formal provider theorem still only a statement. Finite tests cannot establish arbitrary epsilon and all n.

## Reuse and claim boundary
Source-locked existing 1997/2014 published results, explicit elementary perfect-square proof, exact integer fixture. No new general theorem, Lean certificate, protected review/merge, public MathJax proof, or V2 editorial admission claimed.
