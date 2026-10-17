RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0476-S01
PROBLEM_ID: 476
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For prime $p$ and finite $A\subseteq\mathbb F_p$, let $A\widehat{+}A=\{a+b:a,b\in A,a\ne b\}$. The bound is $|A\widehat{+}A|\ge\min(p,2|A|-3)$ for $|A|\ge2$; for $|A|<2$ interpret the lower bound as zero. The stronger $m$‑subset theorem states $|\{\sum_{a\in B}a:B\subseteq A, |B|=m\}|\ge\min(p,m(|A|-m)+1)$ for $1\le m\le|A|$.

## Dated status and primary evidence
Visually inspected Erdős–Graham (1980), printed p.95, PDF index 90, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf. Inspected the 1994 authors' publisher-hosted primary abstract: Dias da Silva–Hamidoune, *Cyclic Spaces for Grassmann Derivatives and Additive Theory*, *Bull. London Math. Soc.* 26 (1994), 140–146, https://doi.org/10.1112/blms/26.2.140, explicitly asserting the stronger theorem. The full seven-page original proof was not read. The live tracker https://www.erdosproblems.com/476 reports PROVED (LEAN); this does not confer GCL certification. The pinned GCL provider at google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020, path FormalConjectures/ErdosProblems/476.lean, blob 4121b3846deffa6c7a651231a564c20e65394a14, ends in 'sorry' and cites an external Lean proof not compiled in this audit. Pinned registry blob 90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5 maps #476 to issue #1746.

## Strongest verified interface
An independent complete two-case polynomial argument using the finite-grid coefficient lemma proves the inequality; see accompanying six-section editorial/0476.md. For $p\ge2k-3$, the coefficient of $X^{k-1}Y^{k-2}$ in $(X-Y)(X+Y)^{2k-4}$ is nonzero modulo $p$. For $p<2k-3$, the coefficient of $X^{k-1}Y^{p-k+1}$ in $(X-Y)(X+Y)^{p-1}$ equals $2(-1)^{k-2}$ modulo odd $p$ and is nonzero. Exact finite tests verify every subset for primes $p\le13$, including saturated and small-cardinality cases. This is a mathematical derivation, not Lean replay or reproduction of the 1994 exterior-algebra proof.

## Proposed bounded successor task
EC004-0476-LEAN-REPLAY: pin the external Lean proof commit and toolchain; compile without 'sorry' or extra axioms; compare restricted-sumset definition, prime assumption and cardinality inequality to the original. Capture exact logs and hashes; stop on the first missing dependency or mismatch. Separately inspect all pages 140–146 of the 1994 paper to verify its stronger $m$‑term proof.

## Prerequisites and blocker
The statement and established solution are source-grounded, but the 1994 full proof is not independently read and external Lean is not replayed. The article is an unaccepted editorial draft, not GCL MathCert or source-complete certification. The issue-comment return remains UNPOSTED after execution safety rejection.

## Reuse and claim boundary
Reused 1980 original, 1994 authors' abstract, pinned Lean provider and tracker. Polynomial derivation and finite computations were performed for this audit. No external worker, formal certificate, protected admission, or novelty claim.
