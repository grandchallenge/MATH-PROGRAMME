RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0882-S01
PROBLEM_ID: 882
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let A subset [1,N] and Sigma(A) comprise sums of ALL NONEMPTY subsets of A, each element used once. Require Sigma(A) primitive under divisibility: NO distinct positive values u,v in Sigma(A) satisfy u|v or v|u. This applies to every restricted subset sum, not only to the original elements A. Determine maximum size |A| and the sharp additive lower-order term in its logarithmic growth. Distinct VALUES matter, but the primitive property itself forces distinct sums.

## Dated status and primary evidence
Erdős, Lev, Rauzy, Sándor and Sárközy, 'Greedy algorithm, arithmetic progressions, subset sums and divisibility', Discrete Mathematics 200 (1999), pp119–135, DOI https://doi.org/10.1016/S0012-365X(98)00385-9. The publisher bibliographic record and abstract were directly checked; full 1999 proof not independently replayed. Erdős original Eger 1998 chapter pp169–180 DOI https://doi.org/10.1515/9783110809794.169 not fully inspected. Maintained https://www.erdosproblems.com/882 marks SOLVED at leading logarithmic order; frozen teorth catalogue @536408716724a2402bdfa7c1d764bf83d64a8c89 likewise marks solved. The published construction is A_m={2^m-2^j:0<=j<m} inside [2^m-1], with m members. Maintained page reports sharper upper bound |A|<=log_2 N+(1/2)log_2 log N+O(1), but full reference proof is not independently replayed. An O(1) additive gap remains a possible improvement, not an established theorem.

## Strongest verified interface
An independent exact program checked the binary construction for m=1..10: all 2^m-1 nonempty subset sums are distinct and primitive under divisibility. Exhaustive finite maximization for N<=18 agrees with independent fixed-cardinality combinations checks through N<=12, including maximum values N=3 gives 2, N=7 gives 3, N=15 gives 4. Rigorous elementary injectivity lemma: if two different subsets have equal sum, cancel the intersection to get DISJOINT nonempty subsets U,V each with equal sum t. Then t and 2t are both nonempty subset sums (U and U union V) and are different values with t|2t, contradiction. Thus all 2^|A|-1 subset sums are distinct and <=N|A|, yielding 2^|A|-1<=N|A|, and the elementary weaker bound |A|<=log_2 N+O(loglog N). This does not reproduce the finer published one-half loglog coefficient.

## Proposed bounded successor task
Input exact nonempty-subset-sum map and primitive divisibility relation, with binary construction A_m. Target: prove primitive Sigma(A) implies injectivity of the subset-sum map, the elementary cardinality bound, and primitivity of every subset sum of A_m, retaining distinct-value semantics. Acceptance: complete paper proof or pinned no-sorry Lean kernel theorem, literal axiom report, independent m<=10 and N<=12 finite tests. Falsification by collision in a genuinely primitive Sigma(A), a pair of divisible binary-family values, or an incorrect finite extremum. Stop at finite construction and elementary bound until full 1999 upper-bound proof has independent source review.

## Prerequisites and blocker
Full 1999 upper theorem and original 1998 problem text not line-by-line inspected; stronger published asymptotics reported by catalogue without independent GCL proof replay. No Lean certificate, novel sharp additive estimate or approved independent review.

## Reuse and claim boundary
Reused 1999 primary bibliographic source and maintained status and independently checked exact finite/constructive lemmas. No new solution, source-priority claim, protected merge, formal certification, deployed browser rendering or editorial admission claimed.
