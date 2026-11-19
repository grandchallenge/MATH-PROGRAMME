# Erdős #249 WP09-B — source-normalized adversarial mathematical review

**Review mode:** Distinct logical GCL Axiomatist/Adversary/Referee audit performed by **the same authenticated agent** after writing the theorem. Not an independently authenticated mathematician, external novelty investigation, Lean proof, MATHCERT review or authority to certify the original Erdős problem.  
**Research issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500), OPEN / GCL Worker Queue Project #2 In Progress; original Erdős #249 OPEN.  
**Reviewed source:** [SHIFTED_MOMENT_ENERGY_009B.md](SHIFTED_MOMENT_ENERGY_009B.md).  
**External source lock:** Will Cook's 2026 [exact first-harmonic manuscript](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), commit 3368d1e69467aec111eb3244843ad3542171ff96, blob 547ed9ed83500181a2e55047ce5df569b7cb49ac; R. Balasubramanian, S. Giri, P. Srivastav, [shifted multiplicative correlations](https://arxiv.org/abs/1511.02221), J. Number Theory 174 (2017), 221–238.

## A. Is the Euler-product second moment exactly correct?

Yes, modulo ordinary mathematical review of the provided finite divisor algebra. For $f(n)=\varphi(n)/n$, the Möbius expansion gives

$$
\sum_{n\le T} f(n)f(n+h)
=\sum_{\substack{d\le T,\ e\le T+h\\(d,e)\mid h}}
\frac{\mu(d)\mu(e)}{de}
\left(\frac{T}{[d,e]}+O(1)\right).
$$

The CRT condition $(d,e)\mid h$ is essential; omitting it would create false local factors. The total counting-error cost is bounded by $\sum_{d\le T,e\le T+h}1/(de)=O_h((\log(2T))^2)$. The infinite main series is absolutely convergent, because its omitted tail for $d>T$ is bounded by

$$
\sum_{d>T,e\ge1}\frac1{de[d,e]}
\ll\sum_{d>T}\frac{\log(2d)}{d^2}
\ll\frac{\log(2T)}T.
$$

The symmetric $e>T+h$ tail is no larger in order. The resulting fixed-shift error is indeed $O_h((\log(2T))^2)$, without an unproved probabilistic assumption.

For every prime $p$, the $d=p,e=1$ and $d=1,e=p$ choices each contribute $-p^{-2}$; the $d=e=p$ choice contributes $+p^{-3}$ **only if $p$ divides $h$**. Therefore

$$
A=\prod_p(1-2/p^2+1/p^3),\qquad
B_h=\prod_{p\mid h}(1-2/p^2+1/p^3)
    \prod_{p\nmid h}(1-2/p^2)
$$

are the correct self and shifted mixed constants, respectively. The normalized difference variance is $V_h=2(A-B_h)$. This is compatible with prior shifted-product literature; the review makes **no novelty claim**.

The exact finite-prime CRT tests independently enumerate one full primorial period and reproduce all three rational values $A_P,B_{h,P},2(A_P-B_{h,P})$, including a zero-variance control when every included prime divides $h$. That confirms the local factors but cannot replace the absolute-convergence proof.

## B. Is the variance strictly positive for every fixed shift?

Yes. Let $b_p=1-2/p^2$, so $b_2=1/2$. For $p\ge3$,

$$
0\le\sum_{p\ge3}2/p^2
<2\sum_{n\ge3}n^{-2}
\le2(1/9+1/3)=8/9.
$$

The finite union bound on positive products gives $B_*=\prod_pb_p>1/18$. For any prime $p\nmid h$, the corresponding factor in $A$ exceeds that in $B_h$ by $p^{-3}$, and all other factors in $A$ are no smaller. Therefore $A-B_h\ge B_*/p^3$ and $V_h>1/(9p^3)$. There is at least one such prime because $h$ is fixed and has finitely many prime divisors.

**Scope:** The estimate decays as the least omitted prime grows. It is **not** a uniform constant over arbitrary shifts $h$. A fixed numerical evaluation of a truncated Euler product is not evidence that the full variance has exactly that decimal value; the code returns rigorous rational tail intervals and labels approximate finite-prime numbers as illustrative only.

## C. Is the unnormalized cubic moment expansion valid?

Yes. The exact identity

$$
\varphi(n+h)-\varphi(n)
=n(f(n+h)-f(n))+hf(n+h)
$$

shows that the mixed and $h^2$ terms contribute at most $O_h(X^2)$ on a dyadic interval. The normalized square-difference partial sums equal $V_hT+O_h(\log^2(2T))$ by Theorem A. Abel summation against $n^2$ produces the main term $V_h\int_X^{2X}t^2dt=(7/3)V_hX^3$ with error $O_h(X^2\log^2(2X))$. Shifting the endpoints by Cook's $L=O_h(\log X)$ changes at most $O_h(\log X)$ summands, each bounded by $O_h(X^2)$; this does not change the leading coefficient. The claimed moving-depth second moment is therefore valid, for each **fixed** $h$, with no distributional extrapolation from numerical observations.

## D. Is the finite phase-energy inequality correct, with exact endpoints?

Yes. Write $r_N=\mathrm{cen}_Q(D_{h,N,L})$ for $X\le N<2X$. The exact recurrence gives

$$
r_{N+1}-2r_N\equiv d_h(N+L+1)\pmod Q
$$

for $X\le N\le2X-2$; hence the **coefficient endpoint interval** is exactly $[X+L+1,2X+L-1]$, which has $X-1$ integers. If $|d_h(n)|<Q/2$, that coefficient is a minimal absolute representative of its congruence class and so $|d_h(n)|\le|r_{N+1}-2r_N|$.

The finite operator from the length-$X$ vector $r$ to its $X-1$ adjacent differences $r_{N+1}-2r_N$ has Euclidean operator norm at most $1+2=3$ (shift/truncate norm at most one). Thus the exact integer inequality $\sum d_h^2\le9\sum r_N^2$ has **no sampling, averaging or probability** inside it.

For centered $r_N$, the elementary concavity bound $\sin(\pi |r_N|/Q)\ge2|r_N|/Q$ holds and gives the real harmonic deficit

$$
\sum_{N=X}^{2X-1}[1-\cos(2\pi r_N/Q)]
\ge\frac8{Q^2}\sum r_N^2
\ge\frac8{9Q^2}\sum d_h^2.
$$

This genuinely concerns Cook's **actual first harmonic**, not a generic phase imitation. The finite tests compute the numerator residues with both the independently executed direct sum and the previously protected rolling recurrence, then check the complete integer $\ell^2$ inequality for multiple shifts. Hostile rational affine-periodic coefficients pass the same test, as they should.

## E. Are the strong depth quantifiers and numerical constants preserved?

Let $L_h(X)$ be the least positive integer satisfying $Q=2^L\ge16(2X+h+L+2)$. For each fixed $h$, $L=O_h(\log X)$, and strict minimality implies

$$
32X<Q<32(2X+h+L+1)=64X+O_h(\log X).
$$

The actual totient difference has magnitude below $n+h<2X+L+h<Q/2$, so the phase-energy transfer applies without any supplementary assumption.

Combining the cubic moment and depth asymptotic gives

$$
\liminf_{X\to\infty}\frac{X-\mathrm{Re}\sum_NE_{h,N,L_h(X)}}X
\ge\frac89\frac{7V_h/3}{64^2}
=\frac{7V_h}{13824}.
$$

Since $7/13824>1/2500$, the manuscript's explicit saving $c_h=V_h/2500>1/(22500p^3)$ holds for all sufficiently large $X$ after $h$ is fixed. It is a strict improvement over the earlier purely selected-sign constant, but **far below** Cook's needed $0.1$. No denominator exclusion follows.

## F. Structural countercheck: the method alone cannot prove ten-percent saving

The phase-energy certificate itself, not the true harmonic deficit, has an upper envelope. For any $0\le a(n)\le n$,

$$
|a(n+h)-a(n)|\le2X+L+h=(2+o(1))X
$$

on the coefficient interval, and Cook's admissible $Q>32X$. Therefore the specific lower-bound expression $(8/(9Q^2))\sum d_h^2$ is bounded above by $(1/288+o(1))X$, **less than 0.1X**. To reach 0.1X through this expression alone would require coefficient energy exceeding $(576/5)X^3$; the envelope permits at most $(4+o(1))X^3$. The gap is a factor greater than $144/5=28.8$ asymptotically.

This is **not** an upper bound on actual totient phase cancellation. It proves a limit on a specific proposed proof method, and prevents mistakenly promoting the second-moment lemma into Cook's unresolved result. The next needed input must involve genuinely global or higher-order phase correlations, not more refined estimates of the same two-point coefficient variance alone.

## G. Relationship to known rational hostiles and original conjecture

The WP09-A affine-periodic sequence has a rational complete binary sum, large shifted coefficient differences at a selected shift, positive squared-difference energy and corresponding strict finite-phase loss. It therefore passes the new generic energy inequality while **not** disproving any all-shift sufficient irrationality criterion.

The source-locked Cook first-harmonic weighted term, involving the unobserved phase weights $w_N$ on moving prime/cofactor groups, remains unproved. The unweighted normalized two-point correlation is not an estimate for those phase weights and cannot be substituted for one. There is no proof of the $0.9X$ whole-harmonic bound, denominator-uniform residue exclusion, or irrationality of the full binary totient series.

## H. Governance and decision

The source manuscript supplies full proofs of Theorems A–D and the narrow method ceiling. The executable proof controls use exact rational finite-prime CRT periods, strict exact integer phase-energy witnesses, rational hostile controls, and independent direct versus rolling arithmetic. Regression and Markdown gates must be replayed against the final **exact commit head**. A passing finite test is not a proof of the infinite correlation asymptotic; the mathematical proof above remains the decisive evidence.

**Adversarial disposition: ACCEPT_WITH_SCOPE**, for classical two-point normalized correlations, explicit fixed-shift variance, the derived unnormalized cubic moment, the exact finite Cook energy bridge, a stronger but small unconditional harmonic saving and the demonstrated 28.8-fold certificate ceiling. Review is a **same-agent logical pass**, not separately authenticated external mathematical independence, Lean checking, MATHCERT certification or priority adjudication. Retain original Erdős #249, parent #3201, issue #3500 and Project #2 OPEN/In Progress; MATHCERT NOT_SUBMITTED. The next substantive attack is an actual-totient *multi-step phase correlation* or Cook's weighted prime/cofactor exponential cancellation.
