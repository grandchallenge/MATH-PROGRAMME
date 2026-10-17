RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0477-S01
PROBLEM_ID: 477
DISPOSITION: STATUS_CONFLICT
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
The registered 2026 catalogue question asks whether some integer polynomial $f$ of degree at least two has a set $A\subseteq\mathbb Z$ such that each $n\in\mathbb Z$ has exactly one pair $(a,b)\in A\times f(\mathbb Z)$ with $n=a+b$. Uniqueness is of the value $b$, not of the input to $f$. The 1980 Erdős–Graham original, printed pp. 95–96, instead defines $S=\{f(1),f(2),\ldots\}$ and asks whether a direct sum $\mathbb Z=S+T$ can never exist. These are different questions for odd-degree polynomials, including $X^{13}$.

## Dated status and primary evidence
Visually inspected Erdős–Graham (1980), printed pp. 95–96, PDF indices 90–91, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf. Read all six pages of the upstream pipeline-math manuscript at Pengbinghui/pipeline-math commit 99d916ff32a90e77c98eb004537ccda409262346, papers/tiling-complement.pdf; SHA-256 b85d1afe4838507485cf22c8964b4a0301e7c472d6cb3d5b8d5cd6f9ae8bc083. Its Theorem 1.1 (p.1) claims an exact complement for all integer thirteenth powers. Its Lemma 1.4, Corollary 1.5, Proposition 1.6, Lemma 1.7 and Proposition 1.8 (pp.2–6) provide the claimed chain. Read Heath-Brown, arXiv:0806.4330v1, Theorem 2 (p.2), confirming the $B^{10/k}$ bound outside parametrized families, with $N\ll_F B$. Brownawell–Masser (1986) and Corvaja–Zannier (2011) are cited external interfaces, not independently proved here. The public September 2026 status account reports an affirmative answer, but an older cached problem page still displays OPEN; treat this as version drift, not mathematical refutation. The pinned formal-conjectures file at commit 85f863718beeec7b58a3a1926ee92e3472bc2020, blob 91b4a200cc564c859968d8a5a4e9531686cae3d7, uses $f(\{n\in\mathbb Z:n>0\})$, not the full integer image, and its theorem has a sorry placeholder. No Lean replay claimed.

## Strongest verified interface
For $B=\{m^{13}:m\in\mathbb Z\}$ and $D=B-B$, the manuscript derives, conditional on its two external theorem interfaces and its rational-curve exclusion, that for every fixed $c\notin B$ the number of $|t|\le T$ with $t^{13}-c\in D$ is $O_c(T^{5/6})$. The exponent follows from the explicit coordinate bound $|u|,|v|\ll_c T^{13/12}$ and Heath-Brown's $X^{10/13}$ count. A finite union of bad shifts has density zero, enabling a greedy construction of a complement for $B$. This is an author-recorded proof with independently checked algebraic transitions, not GCL certification. It does NOT by itself prove a complement for the historical positive-input set $S$.

## Proposed bounded successor task
Input: exact 1980 pp.95–96, pinned Lean file and the two 2026 constructions. Target: source-lock a theorem giving an exact complement for $\{f(n):n\ge1\}$, or document a counterexample to the claimed equivalence with $f(\mathbb Z)$. Method: inspect the complete primary Liam Price proof, verify positive-versus-nonnegative endpoint and the $\mathbb Z$‑image equivalence for even exponents, and check the two external analytic theorem hypotheses. Accept only a precise theorem/page and a matching quantifier map; falsify an equivalence claim by exhibiting a missing image element or an unproved tiling transfer. Stop at SOURCE_LOCK_READY or an explicit inaccessible-page blocker.

## Prerequisites and blocker
SOURCE_FIDELITY_EXCEPTION: original positive inputs versus modern all-integer inputs; pinned Lean formalization also uses positive inputs. A complete source audit of Price's original proof and the Brownawell–Masser height convention remains outstanding. No change to existing protected catalogue status, no editorial acceptance, no MathCert.

## Reuse and claim boundary
Reused the pinned GCL registry mapping (#477 -> issue #1747), historical original and external literature, with direct reading of the six-page manuscript and the Heath-Brown theorem statement. Finite checks, if attached separately, are illustrations only. No independent worker return was read or fabricated. This is prepared evidence, NOT an authenticated posted issue comment.
