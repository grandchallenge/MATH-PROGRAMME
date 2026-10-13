RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0864-S01
PROBLEM_ID: 864
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let A subset [N] have at most ONE integer sigma with two or more unordered representations sigma=a+b, a<=b, a,b in A; diagonal representations a+a COUNT. The one exceptional integer can have arbitrarily many representations. Let F(N) be the maximum |A|, and estimate it, particularly whether F(N)~(2/sqrt3)*sqrt N. Do not replace this with a one-collision or all-sum Sidon condition.

## Dated status and primary evidence
Pinned teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89: OPEN, 2025-08-31; maintained https://www.erdosproblems.com/864 still OPEN (checked 2026-10-13). Primary P. Erdős and R. Freud, 'On sums of a Sidon-sequence', JNT 38 (1991) 196–205, DOI 10.1016/0022-314X(91)90083-N; original P. Erdős, 'Some of My Forgotten Problems in Number Theory', 1992 pp.39–40, https://hrj.episciences.org/125/pdf. The 1991 publisher bibliographic abstract and the 1992 historical source were independently located; the entire 1991 proof is not certified.

## Strongest verified interface
For Sidon B subset [1,N/3] of size (1/sqrt3+o(1))*sqrt N, A=B union (N-B) has (2/sqrt3+o(1))*sqrt N elements. Sums within each half are unique; cross sums N+(b_i-b_j) are unique except the repeated diagonal difference zero, yielding one exceptional sum sigma=N. Thus F(N)>=(2/sqrt3+o(1))*sqrt N. Conversely, splitting any admissible A below and above sigma/2 yields Sidon subsets, since their pair sums lie respectively below and above sigma, apart from a possible midpoint element. Standard Sidon bounds then give F(N)<=(sqrt2+o(1))*sqrt N, weaker than the conjectured sharp constant. Independent exact monotone backtracking gives F(20)=8 with witness {1,2,4,8,13,17,19,20}; only repeated sum is 21, with four representations. An independent exhaustive enumeration of all C(20,9)=167960 nine-element subsets proves no admissible size nine. Reproducible fixture finite_863_864.py/json is on cohort branch worktree; these finite values are not novel or asymptotic proofs.

## Proposed bounded successor task
Input: a Sidon predicate with unordered diagonal-inclusive pair sums, unique exceptional sigma, and a standard Sidon size bound for intervals. Formalize the exceptional-sum split and derive F(N)<=(sqrt2+o(1))*sqrt N, preserving the midpoint case. Acceptance: reviewed proof or Lean lemma with no sorries; independent reproduction of F(20)=8 and the four-sum witness. Falsify with an admissible set whose lower or upper half has a repeated nonexceptional sum, or a failed finite certificate. Stop before claiming the proposed 2/sqrt3 sharp upper bound; a sharper task must couple the two halves arithmetically.

## Prerequisites and blocker
Primary 1991 construction's full proof is not line-by-line certified. The asymptotic gap from sqrt2 to 2/sqrt3 remains the substantive open research question. No protected Formal Conjectures statement is admitted for #864.

## Reuse and claim boundary
Used original papers and maintained catalogue with independently reproduced finite checks. No solution, priority claim, formal certification, review or editorial acceptance. Do not mistake the finite enumeration for proof of the asymptotic conjecture.
