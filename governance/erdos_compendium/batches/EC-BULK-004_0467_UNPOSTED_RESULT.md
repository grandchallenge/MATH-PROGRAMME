RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0467-S01
PROBLEM_ID: 467
DISPOSITION: PARTIAL
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Erdős–Graham (1980), printed p.93, asks whether the primes below a cutoff can be divided into two classes, with one residue per prime, so that every integer below the cutoff belongs to a selected residue class from EACH part. The modern reconstruction specifies all positive integers $1\le n<x$, primes $p\le x$, and all sufficiently large $x$. The primary print does NOT specify the lower bound or asymptotic quantifier. Reading 'every integer below $x$' literally over all integers makes the claim impossible: CRT constructs an integer avoiding one chosen residue per prime, and translating by negative multiples of their product gives arbitrarily negative uncovered integers.

## Dated status and primary evidence
Primary: P. Erdős and R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory*, Monographie 28 (1980), printed p.93, PDF page index 88, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf, visually inspected 2026-10-13; PDF byte hash not independently recomputed. Pinned upstream source teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89, data/problems.yaml, Git blob 4e60263a80af6207aca494d2e1388e44fa372889, marks #467 OPEN (2025-08-31), with 'ambiguous statement'. Protected GCL registry blob 90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5 maps to issue #1737 and STATEMENT_CAPTURE_REQUIRED. The indexed modern page explicitly warns of missing original quantifiers. An external July 2026 report claims a stronger finite obstruction through 7012, but its checker was not independently replayed here.

## Strongest verified interface
Under the positive-integer interpretation let $N=p-1$ for prime cutoff $p$, and let $C(N)=\sum_{q\le p}\lceil N/q\rceil$ over primes $q$. Take the first at most ten primes $S$. For each two-colouring of $S$, put weight $w(q,r)=\lfloor N/(qr)\rfloor$ on each monochromatic prime pair and take a maximum-weight spanning forest in each colour. Let $L(N,S)$ be the MINIMUM total maximum-forest weight over all colourings. Any two-colour covering must satisfy

$$

C(N)\ge 2N+L(N,S).

$$

Proof: every covered integer has at least one hit of each colour; a forest on its active prime vertices has at most $k-1$ edges per nonempty colour, so the number of active forest edges is bounded by total hits minus two. CRT guarantees at least $\lfloor N/(qr)\rfloor$ common hits for each prime pair. Sum and optimize. Exact integer tests on authenticated CHAD exclude EVERY prime endpoint $p<607$: the deficit $C-2N-L$ is strictly negative. At $p=601$ it is $-1$; at $p=607$ it is $+1$ and the test is inconclusive, NOT a construction. Prime-endpoint reduction therefore excludes every real $2\le x<607$ under the positive-integer interpretation. This independent result is weaker than the unreplayed external 7012 report and has no asymptotic implication.

## Proposed bounded successor task
EC004-0467-FOREST-REPLAY: (a) source-owner semantic adjudication of the missing positive-integer and cutoff quantifiers; (b) replay the exact forest verifier on a second runner, including the CRT overlap inequality and every prime endpoint below 607; (c) extend the selected small-prime forest to twelve primes and record the first inconclusive endpoint. Acceptance: two identical integer certificates and explicit statement normalization; falsification: one incorrect overlap bound or endpoint. Stop after the finite extension; do not launch a Solve campaign. A uniform proof would need a two-pool covering lemma and a property-B colouring of the witness hypergraph, not just two-fold uncoloured coverage.

## Prerequisites and blocker
PARTIAL because the original quantifiers are genuinely ambiguous. The source statement must not be silently promoted to a protected lock. No claim of a proof or disproof of the asymptotic problem. The external 7012 verifier and related #689 solution claims were not replayed. This RESULT/1 is locally staged UNPOSTED: authenticated GitHub issue-comment writes are blocked by execution safety checks. No admission or MathCert.

## Reuse and claim boundary
Reused the original primary 1980 page, pinned registry and upstream catalogue, and indexed modern interpretation. The forest-incidence proof and exact CHAD test are accountable internal research; no independent external worker, novelty, protected approval or mathematical certification is claimed. Original issue comments and other cohort work remain untouched.
