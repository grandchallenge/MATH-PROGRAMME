RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0863-S01
PROBLEM_ID: 863
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For r>=2, F_plus(N,r) is maximum size of A subset [N] with <=r unordered representations a+b=n, a<=b (diagonal allowed); F_minus(N,r) is maximum size with <=r representations a-b=n for n>=1 and a>b. Original question conditionally assumes F_plus~c_r sqrt N and F_minus~c'_r sqrt N and asks c'_r<c_r.

## Dated status and primary evidence
Frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 reports PROVED 2026-04-24; maintained https://www.erdosproblems.com/863 reports affirmative solution by combining the classical Erdős–Turán-type difference bound and Javier Cilleruelo, Imre Ruzsa and Carlos Trujillo, 'Upper and Lower Bounds for Finite B_h[g] Sequences', JNT 97 (2002) 26-34, DOI:10.1006/jnth.2001.2767, Theorem 2.1 (sum-set lower construction). Original Erdős (1992) p.39: https://hrj.episciences.org/125/pdf. The DOI abstract and maintained source report were directly checked; the author's primary PDF endpoint was intermittently unavailable, so the complete primary proof is not independently reproduced.

## Strongest verified interface
Set t=floor(r/2), L=(r+t)/sqrt(r+2t), U=sqrt(r). From CRT Theorem 2.1 liminf F_plus(N,r)/sqrt N>=L, and the classical positive-difference upper bound gives limsup F_minus(N,r)/sqrt N<=U. Exact identity L²-U²=t²/(r+2t)>0. Therefore liminf for sum sets strictly exceeds limsup for difference sets, and any existing constants satisfy c_r>c'_r. r=2: 3/2>sqrt2. Exact Fraction calculations r=2..12 and independent small-set predicate enumerations are in finite_863_864.py/json. Limit existence is NOT proved by these inequalities.

## Proposed bounded successor task
Inputs: the JNT 2002 Theorem 2.1 coefficient, the classical B2[r] difference-counting upper bound, inclusive unordered sums and positive ordered differences. Target: prove liminf/limsup gap and its implication for conditional limits for all r>=2, with a no-sorry Lean algebra/real asymptotics lemma or reviewed paper proof. Accept exact rational coefficient checks r=2..12 and a source-locked proof of the positive-difference upper bound; falsify with an r violating the squared-gap identity or a source convention mismatch. Stop before claiming existence of each c_r or independently certifying CRT's construction.

## Prerequisites and blocker
Full 2002 construction proof and asymptotic error term not line-by-line replayed; formal provider not admitted for #863. A source-aligned exact-definition comparison and the difference upper-bound proof should precede formal certification.

## Reuse and claim boundary
Uses original Erdős 1992 question, CRT JNT 2002 primary theorem record, maintained status, exact GCL finite checks, and prior cohort analysis. Published result is not a novel GCL solution. No independent Lean build, protected editorial review or certification claimed.
