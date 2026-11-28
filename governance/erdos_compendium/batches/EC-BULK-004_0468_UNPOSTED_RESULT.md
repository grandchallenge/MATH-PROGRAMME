RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0468-S01
PROBLEM_ID: 468
DISPOSITION: PARTIAL
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For $n\ge1$ let $1<d_1<\cdots<d_k=n$ be all divisors of $n$ greater than 1, and let $D_n=\{d_1,d_1+d_2,\ldots,d_1+\cdots+d_k\}$. Erdős asks for the size of the NEW-sum set $D_n\setminus\bigcup_{m<n}D_m$. When defined, $f(N)=\min\{n:N\in D_n\}$. Is $f(N)=o(N)$, or at least for almost all $N$? The divisor 1 is EXCLUDED in the original statement; an alternate Guy-book convention including it must be explicitly reindexed.

## Dated status and primary evidence
Visually inspected the original P. Erdős and R. L. Graham (1980), *Old and New Problems and Results in Combinatorial Number Theory*, printed p.93, PDF page index 88, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf. Original PDF byte hash not independently recomputed. Protected GCL registry blob 90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5 maps #468 to issue #1738, triage STATEMENT_CAPTURE_REQUIRED. Pinned upstream teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89:data/problems.yaml, Git blob 4e60263a80af6207aca494d2e1388e44fa372889, marks OPEN (2025-08-31), OEIS A167485/A387502/A387503. The public discussion dated 2025-09-14 reports finite counts, not a theorem; no later primary proof of the asymptotic question was verified.

## Strongest verified interface
$f(1)$ and $f(4)$ are undefined: a one-term prefix is the smallest divisor greater than 1 and hence prime, while any prefix with at least two terms is at least $2+3=5$. An independent exact divisor sieve computed all $D_n$ for $1\le n\le10000$, retaining the earliest occurrence of each sum. There are exactly 924 new sums through $n=1000$ and 8697 through $n=10000$, reproducing the public finite report. Exactly 2969 values $1\le N\le10000$ have no witness with $n\le10000$; they may have later witnesses, so this is NOT an asymptotic obstruction. Concrete fixtures: $f(17)=10$ and $f(28)=102$. A naive divisor enumeration agrees with the sieve for every $n\le200$. Authenticated CHAD regression suite: six tests pass across #467/#468.

## Proposed bounded successor task
EC004-0468-PREFIX-CERT: compute the exact first-occurrence map $f_M$ for $M=100000$ using two independent divisor enumeration methods. Output new-sum counts, first-occurrence hashes and the list of $N\le M$ without witnesses below the cutoff. Accept only matching exact arithmetic, correct exclusion of divisor 1, and a fixed deterministic verification sample; falsify with a single mismatched prefix. Stop at $M$ and one clearly stated missing asymptotic lemma, without promoting finite trends to a theorem or launching a Solve campaign.

## Prerequisites and blocker
PARTIAL. The original primary statement is read, but the alleged Guy-book shift was not verified in that primary book, and no theorem proving $f(N)=o(N)$ or its almost-all variant has been source-verified. Eventual definedness must be handled explicitly. The issue-comment return remains UNPOSTED because authenticated writes are rejected by execution safety checks. No source-lock promotion, article admission or MathCert.

## Reuse and claim boundary
Reused the original 1980 source, pinned catalogue, issue #1738 and public experimental report for comparison only. The finite counts were reproduced independently by standard-library integer arithmetic on CHAD and in a separate sandbox. No external worker, novelty, asymptotic proof, certified Lean run, or protected merge is claimed. Original comments and EC-BULK-002/003 remain untouched.
