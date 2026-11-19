# Erdős #249 WP08-B — critical review and adversarial claim boundary

**Role:** qualified, separately scoped GCL Adversary/Referee logical pass, **same authenticated agent as author**. This is not independent externally authenticated mathematical review, Lean checking, MATHCERT certification or historical priority adjudication.  
**Research issue:** [#3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500), OPEN; original full-series irrationality conjecture OPEN.

## Prior-art adversarial cross-check

Will Cook's *The Binary Totient Series* (2026, revised October 2026), [first-harmonic source](https://github.com/wcook04/plectis-erdos/blob/main/paper/249/erdos-249-binary-totient-series.tex), already separates the largest prime factor from its small cofactor, imposes a lower totient ratio on the cofactor, and obtains prime-number-theorem group estimates. Crucially, Cook isolates a **weighted first-harmonic correlation** as an unproved obligation after controlling unweighted group means. This WP does **not** claim that its prime-cofactor grouping or PNT count is novel, nor that the exact residual identity for a finite-prime rational Euler comparator proves Cook's outstanding weighted bound. The present bounded phase-difference theorem should be judged only for its exact stated contents; external theorem priority remains unassessed.

## A. Does the unique-large-prime identity really hold?

Yes, under the exact strict inequality $y^2>3X$ and $n<3X$. If $n$ had two prime factors exceeding $y$, with multiplicity, their product would exceed $3X$, a contradiction. For its unique omitted prime $p$, the cofactor $m=n/p<3X/y<y$, and all prime factors of $m$ are therefore included in the cutoff. In particular $p$ is coprime to $m$ and appears only once, so

$$
g_y(pm)=p\varphi(m),\qquad \varphi(pm)=(p-1)\varphi(m).
$$

This gives the exact positive residual $\varphi(m)$. The code separately sieves **all** large prime factors up to the entire finite observation limit, not only primes in $(y,2y]$, and rejects multiple assignments. Independent coprimality and finite-Euler-product checks supplement but do not replace the all-index algebraic proof. The identity is not asserted for unrestricted $n$ or a fixed $y$ outside this single-large-prime regime.

## B. Is the quantitative adjacent-pulse phase threshold correct?

For $n=pm$ with $p\le2y$ and $2\varphi(m)\ge m$, the pulse has magnitude $\varphi(m)\ge X/(4y)$. The exact sliding residue recurrence for the *difference* of totient and finite Euler approximation makes $r_{N+1}-2r_N$ congruent to $-\varphi(m)$ modulo $Q=2^L$. If both centered residues are smaller than $X/(12y)$, their linear combination is less than $X/(4y)$; it cannot equal the negative pulse. Their difference in absolute value is less than $X/(4y)+3X/y< Q$ because $8X<Q$. Thus congruence is impossible. At least one of two adjacent starts has centered absolute residue at least $X/(12y)$; after dividing by $Q\le16X$, its phase distance is at least $1/(192y)$. No unstated uniform rounding of real phases occurs.

The good endpoints are distinct because their prime $p>y$ is unique; each resulting pair of starts intersects at most two pairs. This yields at least half the good endpoints in distinct qualifying starts. This is **an effective finite theorem**, even if no primes happen to occur in the nominated interval.

## C. Is the moving-prime asymptotic genuinely uniform in the specified power range?

Yes. The count of $m$ with $pm\in I_X$ is $X/p+O(1)$ and their maximum index is $O(X/p)$. The classical totient mean gives a uniform error $O(\log X)$ for each such interval, since $p\le2y\le2X^{1-\varepsilon}$. The fraction with $2\varphi(m)\ge m$ has the valid lower bound $\beta=12/\pi^2-1>0$ from the mean and the pointwise upper bound $\varphi(m)/m\le1$. Summing across distinct omitted primes gives an explicit lower bound

$$
\#\mathcal G_{X,y}\ge
\beta X\sum_{y<p\le2y}\frac1p
-O(\pi(2y)\log X).
$$

By the **classical prime number theorem**, the reciprocal prime sum is $(\log2+o(1))/\log y$ and $\pi(2y)=O(y/\log y)$. With $y\le X^{1-\varepsilon}$, the cumulative error is $o(X/\log y)$. With $y\ge X^{1/2+\varepsilon}$, the crucial strict prime-uniqueness inequality holds for all sufficiently large $X$. Therefore the manuscript's leading constant is exactly $\beta\log2/2$. The uniform range is meaningful only when $0<\varepsilon<1/4$, as explicitly stated. No prime-independence heuristic or stronger error term is silently used.

**Limitation:** the guaranteed *fraction* of starts is only order $1/\log y$ and the guaranteed *gap* is only order $1/y$; these both vanish as $X,y$ grow. The theorem is uniform in the declared cutoff range but is **not** a fixed positive-density or fixed positive-gap statement independent of $y$.

## D. Is the rational comparator legitimate?

For finite $y$, $g_y$ has a complete exactly rational binary series by the finite Möbius Euler formula already proved and protected-admitted in WP08-A. The residual is nonnegative and vanishes for all $n\le y$, so the strict upper approximation $0<S_y-S<(y+2)/2^y$ follows from an elementary geometric tail and the existence of primes above any fixed $y$. There is **no useful common denominator bound**, and no conclusion that a limit of rationals is irrational.

The additional hostile rational patch is **not the same comparator at every scale**. For each fixed finite pair of parameters $X$ and $y$, it agrees with the actual totient exactly on every coefficient used by the finite tails of length $L$ in $[X,2X)$ and equals $g_y$ elsewhere. It is a **finite modification** of an already rational full series, hence is itself rational. This demonstrates that observing the finite prime escape on one scale cannot by itself exclude rational full sums, while leaving cofinal all-scale hypotheses entirely open. Claiming otherwise would be mathematically false.

## E. Does this solve the analytic-tail or denominator obstacle?

No. Theorem B proves an exact finite-phase discrepancy between the actual totient and a *moving rational finite-prime approximation*, not an inequality for the complete infinite scaled totient tail. Its phase threshold $1/(192y)$ tends to zero, while the standard omitted-tail bound at $L=\lfloor\log_2X\rfloor+4$ remains of constant order. Even if a stronger correction estimate were found, one must still control all hypothetical rational denominators and the sign of the correction. The signed infinite-tail bridge and Cook's source-locked sufficient harmonic estimate remain **unproved**.

The natural successor is a **joint prime-pulse and discarded-tail correlation** at an explicitly controlled deeper depth, checked against the moving-scale rational patch and WP07-E interpolation. Any future lemma must specify an observed or deduced sign and denominator quantifier; increasing the exact finite sample size is not enough.

## F. Source checks, memory and provenance

The code reuses the already protected totient/finite-window recurrence implementation and adds a dedicated efficient finite-Euler sieve, a unique-large-prime witness sieve, exact integer numerator/centered-residue certificates, prime union count, and an explicit rational-patch adversary. It **does not compute enormous rational denominator products** and therefore avoids unnecessary CPU/RAM use. The seven new hostile tests supplement the 38 preexisting governed full-series tests. Exact source replay and SHA256s are frozen in the associated execution receipt; success of tests or workflow is not independent mathematical certification.

**Verdict:** ACCEPT_WITH_SCOPE, subject to Cook 2026 prior-art attribution, for four bounded manuscript results (exact sparse pulse, exact effective phase escape, prime-number-theorem asymptotic aggregation, and strict rational finite-prime approximation), plus the rational finite-patch hostile control. **Reject promotion to irrationality.** Keep research issue #3500 OPEN / In Progress, original Erdős #249 OPEN and MATHCERT NOT_SUBMITTED.
