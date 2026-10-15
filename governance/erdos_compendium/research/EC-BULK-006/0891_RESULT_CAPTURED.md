RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0891-S01
PROBLEM_ID: 891
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For fixed k>=2, first primes p1=2<p2=3<..., P_k=product_{j=1}^k p_j. Does there exist n0(k) such that for EVERY n>=n0(k) the half-open integer block [n,n+P_k) contains an m with omega(m)>k, where omega counts DISTINCT prime factors? Original k2 question: does each sufficiently late block of SIX integers contain a number with >=3 distinct prime factors? Do not count repeated powers as separate prime factors, or silently replace block length Pk with longer Schinzel length.

## Dated status and primary evidence
Erdős and Selfridge, 'Some problems on the prime factors of consecutive integers', Illinois Journal of Mathematics 11 (1967), pp428–430, DOI 10.1215/ijm/1256054564, archived https://combinatorica.hu/~p_erdos/1967-21.pdf, printed p430 cites Schinzel's consequence of Pólya's k-smooth gap theorem: eventual success for longer length P_{k-1}*p_{k+1}. Erdős–Selfridge could not reduce that length to Pk even k2. A. Schinzel, 'Unsolved Problem 31', Elemente der Mathematik 14 (1959), 82–83, original historical ten-consecutive-number special case for k2. Maintained https://www.erdosproblems.com/891 OPEN; frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 OPEN; no completed formal Lean proof. Full 1967 PDF page-image not independently captured during this execution, primary indexed text and bibliographic record confirmed. Maintained thread https://www.erdosproblems.com/forum/thread/891 attributes to Weisenberg a conditional Dickson prime-tuples obstruction to shortening length to Pk-1; NOT an unconditional disproof of length Pk.

## Strongest verified interface
Any positive m<Pk has fewer than k DISTINCT prime factors, since the least product of k distinct primes is Pk. With L=lcm(1,...,Pk-1), for each m<Pk, Lq+m=m*((L/m)q+1). If Dickson conjecture's admissibility and simultaneous prime output apply to these linear factors, each Lq+m has at most k distinct prime factors: m has <=k-1 and linear factor adds <=1. This EXPLAINS conditional sharpness for Pk but is NOT a GCL proof of Dickson/admissibility nor a result about the conjectured full Pk interval. Exact CHAD finite_891.py/json checks EVERY start n=1..100000 for k2 (L6), k3 (L30), k4 (L210), with omega via smallest-prime-factor sieve. Failing starts: k2 exactly 69, last observed n=4372; k3 464, last 8615; k4 4575, last 50841. At n=4372 the six supports have sizes 2,1,2,2,2,2. These are FINITE statements; 'last observed' is not eventual theorem.

## Proposed bounded successor task
Source-locked finite primorial and interval predicate proof: for any k>=2, prove every positive integer m<Pk has omega(m)<k, prove equivalence of half-open interval existence predicate and a sliding-window indicator, and replay exact finite sieve/case counts through n=100000 for k=2,3,4. Acceptance: complete paper proof or pinned no-sorry Lean with literal axioms, all six n4372 factorizations, exact failure counts, and no off-by-one/prime-power mismatch. Falsify by a value below Pk with k distinct primes, an incorrect window count, or an unverified prime factorization. Stop before inferring all sufficiently large n from finite search.

## Prerequisites and blocker
Full primal 1967 and Schinzel 1959 page image not independently source-captured; conditional Dickson linear family admissibility not independently established or implied unconditionally. The six-integer eventual conjecture remains open, no kernel proof.

## Reuse and claim boundary
Reused primary bibliographic results, maintained catalogue and public conditional discussion; independently derived primorial lemma and ran exact finite CHAD fixture. No novel infinite theorem, protected review/merge, Lean certificate or public rendered-site admission claimed.
