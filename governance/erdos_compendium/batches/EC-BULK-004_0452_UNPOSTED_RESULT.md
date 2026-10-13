RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0452-S01
PROBLEM_ID: 452
DISPOSITION: SOURCE_LOCK_READY
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization

Let $\omega(n)=|\{p\text{ prime}:p\mid n\}|$ count *distinct* prime divisors, without multiplicity. For real $x>e$ define $L(x)$ as the maximum cardinality of a consecutive block of integers $I\subseteq[x,2x]$ satisfying $\omega(n)>\log\log n$ for **every** $n\in I$ (natural logarithms). Erdős asks for the asymptotic size of $L(x)$, not merely whether such blocks exist. In particular, the 1980 source asks whether $L(x)$ could reach $(\log x)^k$ for arbitrarily large fixed $k$ (a speculation, not a theorem). The known CRT lower bound is $L(x)\ge(1+o(1))\log x/(\log\log x)^2$; the $o(1)$ is as $x\to\infty$. Neither the density-$1/2$ theorem nor finite examples settles the maximum-block growth question.

## Dated status and primary evidence

Primary original: P. Erdős and R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), printed p. 90, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=86 . The page states the density $1/2$ result, the CRT lower bound, and the possibility of arbitrarily large fixed powers of $\log x$; the printed page was visually checked on 2026-10-13. Earlier primary proof: P. Erdős, “Note on the Number of Prime Divisors of Integers,” *J. London Math. Soc.* 12 (1937), 308–314, DOI 10.1112/jlms/s1-12.48.308, author archive https://users.renyi.hu/~p_erdos/1937-02.pdf . The archived scan's printed p. 313 proves $\#\{n\le X:\omega(n)>\log\log n\}=X/2+o(X)$; this page and the argument's notation were visually inspected. Maintained secondary catalogue https://www.erdosproblems.com/452 reported OPEN and last edit 2025-10-28 in the accessible search-index snapshot consulted 2026-10-13; direct live page access returned HTTP 403, so a *fresh direct* site-status assertion is blocked. Pinned teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89, data/problems.yaml blob 4e60263a80af6207aca494d2e1388e44fa372889, reports OPEN and last update 2025-08-31. The issue's pinned formal-statement metadata says YES, whereas the accessible maintained snapshot says NO: record this formalization-metadata drift without treating either as GCL formal certification.

## Strongest verified interface

A self-contained reconstruction of the CRT lower bound (not a solution to the open growth question): fix $0<\varepsilon<1$ and take $L=\lfloor(1-\varepsilon)\log x/(\log\log x)^2\rfloor$, $m=\lceil\log\log(2x)\rceil+1$. The prime number theorem supplies at least $Lm$ distinct primes in $(L,(1+\varepsilon/4)\log x]$ for all sufficiently large $x$, since the interval contains $(1+\varepsilon/4+o(1))\log x/\log\log x$ primes and $Lm=(1-\varepsilon+o(1))\log x/\log\log x$. Assign $m$ distinct primes $p_{j,k}>L$ to each $1\le j\le L$. The Chinese remainder theorem gives $a\pmod Q$ with $a+j\equiv0\pmod{p_{j,k}}$ for every pair $(j,k)$, where $Q=\prod_{j,k}p_{j,k}$. Since $\log Q\le Lm\log((1+\varepsilon/4)\log x)=(1-\varepsilon+o(1))\log x$, eventually $Q\le x^{1-\varepsilon/2}$. Thus a representative $a$ may be chosen in $[x,2x-L]$. Every $a+j$ has at least $m>\log\log(a+j)$ distinct prime factors. Letting $\varepsilon\downarrow0$ yields the asserted asymptotic lower bound. The only non-elementary input in this reconstruction is the prime number theorem for selecting enough small primes; no claim is made that this reproduces the original authors' shortest proof.

Checked finite CRT fixture: choose $L=3$, and four primes for each offset: $[5,7,11,13]$, $[17,19,23,29]$, $[31,37,41,43]$. The moduli are $5005,215441,2022161$, pairwise coprime; $Q=2180460221945005$ and $a=2099999228442114$ satisfies $a+j\equiv0$ modulo the respective modulus for $j=1,2,3$. Since $\log\log(a+3)<4$, each of the three consecutive integers qualifies. This verifies arithmetic and strict threshold, not any asymptotic estimate.

## Proposed bounded successor task

EC004-0452-CRT-BOUND-REPLAY: independently check the above explicit CRT arithmetic and give a complete epsilon-quantified proof of the PNT prime-supply estimate and $Q\le x^{1-\varepsilon/2}$ for fixed $\varepsilon>0$. Input: $\omega$ counts distinct primes; $I$ is an integer interval in $[x,2x]$; natural logarithms; use a clearly stated prime number theorem. Acceptance: exact integer divisibility and $\omega(a+j)>\log\log(a+j)$ for $j=1,2,3$, plus a written proof with all $x$-dependent rounding terms bounded. Falsification: any failed modular congruence, a prime assigned to two offsets, or a quantifier gap in the uniform selection of $Lm$ primes. Stop at the classical lower bound and report the remaining gap to any superlogarithmic power; do not present a finite search as resolution.

## Prerequisites and blocker

The 1980 original and 1937 primary theorem are accessible and inspected. The PNT is invoked as established external mathematics, not independently proved here. A direct October 2026 live erdosproblems.com page readback is unavailable (HTTP 403); a dated accessible index snapshot supports OPEN but does not exclude unindexed recent changes. The 1937 archive scan begins at printed p. 309 rather than p. 308; the decisive p. 313 theorem is present. No formal proof is locally replayed. This is a documentary source lock with these explicit status and formalization boundaries, not a proof of the open problem.

## Reuse and claim boundary

Sources reused: original 1980 p. 90, Erdős's 1937 p. 313, pinned 2025 catalogue, maintained-page indexed snapshot, and the original GCL issue #1722. Independently reconstructed here: prime-count asymptotic, CRT modulus bound, finite three-integer witness, and exact quantifier distinction between a lower bound and the unknown optimal growth. No external worker, independent-account review, Lean replay, protected admission, source-return posting, or novelty claim is asserted. This text is a *local draft* until an authenticated issue comment and readback exist.
