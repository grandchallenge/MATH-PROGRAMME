RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0892-S01
PROBLEM_ID: 892
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Given arbitrary increasing positive integer b_1<b_2<..., characterize existence of an INFINITE primitive sequence a_1<a_2<... (no distinct terms divide one another) satisfying a_n<=C*b_n for a SINGLE constant C independent of n. Auxiliary clause: if no nontrivial gcd(b_i,b_j)=b_k, does existence follow? Historical ESS convention tests gcd equality ONLY for inputs b_i,b_j that are not divisible by each other, unlike literal 2026 informal comments that might mean only i=j=k is trivial; literal broad ban already implies b itself primitive and trivial a=b. Third independent clause: characterize exponent sequences n_i with one infinite primitive A satisfying |A ∩ [1,2^{n_i}]|>=c*2^{n_i} for ALL i, one constant c>0.

## Dated status and primary evidence
Erdős, Sárközy, Szemerédi, 'On divisibility properties of sequences of integers', Debrecen 1968, Colloq Math Soc Janos Bolyai 2 (published 1970), pp35–49, historical exact general question printed p37, gcd-free question p42, convention p41 EXCLUDES comparable pairs when testing gcd equalities; original indexed citation and source-grounded independent July 2026 research report https://erdosproblemaday.com/report/892, but original printed page image not directly GCL screenshot checked in this execution. Erdős 'A survey of problems in combinatorial number theory' Ann Discrete Math 6 (1980) p101 reiterates the general and density questions. Maintained https://www.erdosproblems.com/892 edited Apr6 2026 remains OPEN, two public comments Feb2026 confirm gcd word ambiguity, frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 OPEN. Erdős (1935), 'Note on sequences of integers no one of which is divisible by any other', proves convergence of sum 1/(a_n log a_n) over infinite primitive sequences; Erdős–Sárközy–Szemerédi (1967) 'On a theorem of Behrend' proves sum_{a<x,a in A}1/a=o(log x/sqrt(loglog x)). Therefore analogous b conditions are NECESSARY. Martin–Pomerance, 'Primitive sets with large counting functions', Publ Math Debrecen 79 (2011) 521–530 DOI 10.5486/PMD.2011.5051, Theorem1 proves an approximate converse for regular counting functions with convergent weighted integral, NOT arbitrary b_n.

## Strongest verified interface
Finite exact theorem for each N>=1: maximal cardinality of primitive subset A⊂[1,N] equals ceil(N/2). Lower witness upper half floor(N/2)+1..N, primitive because double any member>N. Upper bound partition [1,N] into ceil(N/2) chains by unique ODD PART m of each integer, each chain {m,2m,4m,...} totally ordered by divisibility; at most one element of primitive A per chain. CHAD exact finite_892_893.py/json validates chain theorem for N<=24, independently enumerates all 2^N subsets N<=15, and checks B={2,4,9} satisfies historical incomparable-input gcd-free but is NOT primitive due to 2|4 (while literal all-distinct-index gcd ban fails). This is finite semantic/interface evidence, not infinite characterization or construction.

## Proposed bounded successor task
Input source-exact 1970 p41 historical gcd restriction; finite primitive subset predicate; odd-part map for positive integers. Prove odd-part chains partition [1,N] and primitive size <=ceil(N/2), with upper-half witness; prove literal all-pair gcd ban implies primitivity and historical incomparable-gcd ban differs via B={2,4,9}. Acceptance complete elementary proof or pinned Lean no-sorry with literal axiom output, brute maxima N<=15, explicit source page-level condition. Falsify by an oversized primitive subset or incorrect gcd configuration. Then independently source-check Martin–Pomerance 2011 hypotheses for one smooth b_n family, stop without arbitrary b_n iff classification or all n_i density claim.

## Prerequisites and blocker
Historical 1970 original page image not independently inspected; maintained abbreviated 'nontrivial' is ambiguous, must not certify wording without historical convention. Full 1935/1967 necessary-condition analytic proofs not independently replayed; no independently certified 2011 sufficiency for arbitrary sequences, and no full solution. Protected Formal Conjectures statement unformalized per live page.

## Reuse and claim boundary
Used source-indexed historical papers, maintained catalogue, Martin–Pomerance primary published theorem metadata, independent exact finite antichain/gcd proof and CHAD script. No infinite general theorem, priority, protected review/merge, Lean proof, deployed browser render or V2 admission claimed.
