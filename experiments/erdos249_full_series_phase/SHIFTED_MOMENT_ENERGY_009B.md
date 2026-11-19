# Erdős #249 — WP09-B: shifted-totient second moments and Cook phase-energy transfer

**Research issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Programme:** ERDOS-249-S-WP09-B/1, bounded scientific analysis.  
**Exact predecessor:** [protected WP09-A at 91a22c07f08da23b009e98f35f6d5279ee1748b7](SHIFTED_FIRST_HARMONIC_009A.md).  
**Original Erdős #249:** OPEN. **MATHCERT:** NOT_SUBMITTED. No proof of the irrationality of the full binary totient series.

## 1. Source lock and target

Let $h\ge1$ be fixed. The exact first-harmonic numerator in Will Cook's *The Binary Totient Series* is

$$
D_{h,N,L}=\sum_{j=1}^{L}2^{L-j}
[\varphi(N+h+j)-\varphi(N+j)],\qquad
E_{h,N,L}=\exp(2\pi iD_{h,N,L}/2^L).
$$

Source: [Cook 2026, exact pinned Git commit 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), source blob 547ed9ed83500181a2e55047ce5df569b7cb49ac. Cook's sufficient criterion requires a first-harmonic **saving of at least one tenth** for every fixed $h$ on arbitrarily late blocks at a depth satisfying

$$
2^L\ge16(2X+h+L+2).
\tag{1}
$$

His groupwise **weighted** exponential cancellation condition remains open. WP09-A proved a much weaker strict saving from selected positive-density large signed differences. Here we replace that threshold counting by a **global second moment**, combined with a deterministic $\ell^2$ transfer from arithmetic differences to Cook's exact fractional phases.

**Prior art:** Correlation formulas for normalized shifted totients belong to the classical multiplicative-function literature, including Balasubramanian, Giri and Srivastav, *On correlations of certain multiplicative functions*, J. Number Theory 174 (2017), 221–238, [arXiv 1511.02221](https://arxiv.org/abs/1511.02221). They are **not** claimed new. The bounded phase-energy bridge and its limitations are presented with an independent elementary proof here, without a novelty claim.

## 2. Theorem A — exact shifted-totient second-moment constant

Set $f(n)=\varphi(n)/n$ for $n\ge1$. For each prime $p$ put

$$
a_p=1-\frac2{p^2}+\frac1{p^3},\qquad
b_{h,p}=
\begin{cases}
a_p,&p\mid h,\\
1-2/p^2,&p\nmid h.
\end{cases}
$$

Both prime products converge absolutely to strictly positive numbers:

$$
A=\prod_pa_p,\qquad
B_h=\prod_pb_{h,p},\qquad
\boxed{V_h=2(A-B_h).}
\tag{2}
$$

**Theorem A.** For every fixed positive integer $h$,

$$
\boxed{
\sum_{n\le T}f(n)f(n+h)
=B_hT+O_h((\log(2T))^2)
}
\tag{3}
$$

and

$$
\boxed{
\sum_{n\le T}[f(n+h)-f(n)]^2
=V_hT+O_h((\log(2T))^2).
}
\tag{4}
$$

In particular $V_h>0$, with a completely explicit rational lower bound. If $p$ is **any** prime not dividing $h$, then

$$
\boxed{V_h>\frac1{9p^3}>0.}
\tag{5}
$$

### Proof of the correlation formula

The finite exact Möbius identity gives

$$
f(n)=\sum_{d\mid n}\frac{\mu(d)}d.
$$

Expanding the product in (3) leads to pairs $(d,e)$ with $d\mid n$ and $e\mid n+h$. The congruences are compatible precisely if $(d,e)\mid h$, by the integer CRT. A compatible pair contributes

$$
\frac{T}{[d,e]}+O(1)
$$

indices. Summing the errors with coefficient $1/(de)$ up to $d\le T$ and $e\le T+h$ costs $O_h((\log(2T))^2)$.

The infinite main series is absolutely convergent:

$$
B_h=\sum_{d,e\ge1\,;\,(d,e)\mid h}
\frac{\mu(d)\mu(e)}{de[d,e]}.
\tag{6}
$$

To justify replacing the finite main sum by the infinite one, note

$$
\sum_{d>T}\sum_{e\ge1}\frac1{de[d,e]}
=\sum_{d>T}\sum_{e\ge1}\frac{(d,e)}{d^2e^2}
\ll\sum_{d>T}\frac{\log(2d)}{d^2}
\ll\frac{\log(2T)}T.
$$

The analogous tail with $e>T+h$ has the same bound. Multiplication by $T$ therefore contributes only $O_h(\log(2T))$.

Since only squarefree $d,e$ contribute, the local Euler factor at $p$ has terms from choosing neither, the first, the second, or both. The two single choices sum to $-2/p^2$. Choosing both contributes $+1/p^3$ only when $p\mid h$. Thus the Euler factors of (6) are exactly $b_{h,p}$.

The same calculation with $h=0$ gives the self-correlation $\sum_{n\le T}f(n)^2=AT+O((\log(2T))^2)$. Shifting the index by fixed $h$ gives $\sum_{n\le T}f(n+h)^2=AT+O_h((\log(2T))^2)$. Expand the square of the difference to obtain (4). QED.

### Strictly positive constant without a conjectural independence model

Let

$$
B_*=\prod_p(1-2/p^2).
$$

The factor at $p=2$ is $1/2$. For primes at least three, use the elementary inequality $\prod_i(1-x_i)\ge1-\sum_i x_i$ for $0\le x_i\le1$, and

$$
\sum_{p\ge3}\frac2{p^2}
<
2\sum_{n=3}^{\infty}\frac1{n^2}
\le2\left(\frac19+\int_3^\infty\frac{dt}{t^2}\right)
=\frac89.
$$

Consequently

$$
\boxed{B_*>\frac1{18}.}
\tag{7}
$$

For any fixed prime $p\nmid h$, its factor in $A$ exceeds the corresponding factor in $B_h$ by exactly $p^{-3}$; at every other prime the factor of $A$ is no smaller. Factoring out the selected prime and comparing the remaining positive products gives

$$
A-B_h\ge\frac1{p^3}
\prod_{q\ne p}(1-2/q^2)
\ge\frac{B_*}{p^3}.
$$

Thus $V_h=2(A-B_h)>1/(9p^3)$. This proves a quantitative nonzero variance for every shift, even if $h$ is divisible by many small primes. QED.

## 3. Theorem B — cubic arithmetic energy on every large Cook block

Write $d_h(n)=\varphi(n+h)-\varphi(n)$ and let $L=L_h(X)$ be the least positive integer satisfying (1). For each fixed $h$, $L=O_h(\log X)$ and $L\ge h+26$ for all sufficiently large $X$.

**Theorem B.** For every fixed $h$, as $X\to\infty$,

$$
\boxed{
\sum_{n=X+L+1}^{2X+L-1}d_h(n)^2
=\frac73V_hX^3+O_h(X^2(\log(2X))^2).
}
\tag{8}
$$

**Proof.** From $\varphi(n)=nf(n)$,

$$
d_h(n)=n[f(n+h)-f(n)]+hf(n+h).
$$

Since $0\le f(n)\le1$ and $h$ is fixed, squaring and summing over $n\asymp X$ changes the leading $n^2[f(n+h)-f(n)]^2$ contribution by at most $O_h(X^2)$.

Equation (4) gives a summatory mean $V_hT+O_h((\log(2T))^2)$ for the nonnegative sequence $[f(n+h)-f(n)]^2$. Partial summation against $n^2$ shows

$$
\sum_{X\le n<2X}n^2[f(n+h)-f(n)]^2
=V_h\int_X^{2X}t^2\,dt
+O_h(X^2(\log(2X))^2).
$$

The integral is $(7/3)X^3$. Moving the endpoints by $O_h(\log X)$ only changes the sum by $O_h(X^2\log X)$ because every summand is at most $O_h(X^2)$. This gives (8). QED.

## 4. Theorem C — deterministic squared-energy transfer to Cook's real harmonic

This theorem is valid for **any integer coefficient sequence** with the stated local difference bound, not only totients.

Let $Q=2^L$ and

$$
D^a_{h,N,L}
=\sum_{j=1}^{L}2^{L-j}[a(N+h+j)-a(N+j)].
$$

Suppose for all $n$ in $I_{X,L}=[X+L+1,2X+L-1]$,

$$
|a(n+h)-a(n)|<Q/2.
\tag{9}
$$

Let $r_N$ be the integer representative of $D^a_{h,N,L}$ in $[-Q/2,Q/2)$, and write $d^a_h(n)=a(n+h)-a(n)$.

**Theorem C (finite exact energy transfer).**

$$
\boxed{
X-\mathrm{Re}\sum_{N=X}^{2X-1}
\exp(2\pi iD^a_{h,N,L}/Q)
\ge
\frac8{9Q^2}\sum_{n=X+L+1}^{2X+L-1}[d^a_h(n)]^2.
}
\tag{10}
$$

**Proof.** The exact sliding recurrence, already protected in WP09-A, implies

$$
r_{N+1}-2r_N\equiv d^a_h(N+L+1)\pmod Q.
$$

Because $|d^a_h(n)|<Q/2$, that coefficient difference is a minimal-absolute representative in its residue class. Hence

$$
|d^a_h(N+L+1)|\le|r_{N+1}-2r_N|.
$$

Let $r=(r_X,\ldots,r_{2X-1})$. The finite difference operator $r\mapsto(r_{N+1}-2r_N)_{X\le N<2X-1}$ has Euclidean operator norm at most three, by the triangle inequality and the fact that shifting/truncating does not increase the Euclidean norm. Thus

$$
\sum_{n\in I_{X,L}}[d^a_h(n)]^2
\le9\sum_{N=X}^{2X-1}r_N^2.
\tag{11}
$$

For the centered residues, $|r_N|/Q\le1/2$. The elementary inequality $1-\cos(2\pi t)=2\sin^2(\pi t)\ge8t^2$ for $|t|\le1/2$ gives

$$
X-\mathrm{Re}\sum_NE^a_{h,N,L}
\ge\frac8{Q^2}\sum_Nr_N^2.
$$

Combine with (11). No probabilistic independence, prime-number theorem, Gaussian approximation, or unproved phase mixing is used. QED.

For the **actual totient**, (9) holds automatically at Cook's admissible depth: $\varphi(n)\in[0,n]$ gives $|d_h(n)|\le n+h<2X+L+h<Q/2$.

## 5. Theorem D — amplified unconditional saving for every fixed shift

For the least Cook-admissible depth,

$$
32X<Q<32(2X+h+L+1)=64X+O_h(\log X).
\tag{12}
$$

Apply the exact inequality (10) to the actual totient and substitute Theorem B. We obtain

$$
\begin{aligned}
\liminf_{X\to\infty}\frac1X
\left(
X-\mathrm{Re}\sum_{N=X}^{2X-1}E_{h,N,L_h(X)}
\right)
&\ge\frac89\frac{(7/3)V_h}{64^2}\\
&=\boxed{\frac{7V_h}{13824}}>0.
\end{aligned}
\tag{13}
$$

Since $7/13824>1/2500$, the following strict, explicit bound is valid for all sufficiently large $X$ after fixing $h$.

**Theorem D (second-moment Cook-harmonic saving).**

$$
\boxed{
\mathrm{Re}\sum_{N=X}^{2X-1}
\exp(2\pi iD_{h,N,L_h(X)}/2^{L_h(X)})
\le
\left(1-\frac{V_h}{2500}\right)X.
}
\tag{14}
$$

For every prime $p\nmid h$, the saving obeys the unconditional numerical lower bound

$$
\boxed{
\frac{V_h}{2500}>\frac1{22500p^3}.
}
\tag{15}
$$

This is **much stronger** than the tiny sign-threshold constant in WP09-A for small shifts, and it is based on the whole squared-difference mass rather than selected contrast endpoints. But it does **not** meet Cook's required saving $X/10$; the strongest claimed result remains strictly weaker than the original irrationality criterion.

### An exact methodological ceiling

The right side of the transfer estimate (10) is a *guaranteed lower bound*, not the actual harmonic saving. Even if the arithmetic differences maximized their permitted size, this lower bound alone could not certify ten-percent cancellation. Indeed for any $0\le a(n)\le n$ and fixed $h$,

$$
|d_h^a(n)|\le2X+L+h=(2+o(1))X,
$$

and $Q>32X$ by (1), so the particular lower-bound expression in (10) has the upper bound

$$
\boxed{
\frac8{9Q^2}\sum_{n\in I_{X,L}}[d_h^a(n)]^2
\le\left(\frac1{288}+o(1)\right)X
<\frac X{10}
}
\tag{16}
$$

as $X\to\infty$. Equivalently, for the right side of (10) alone to certify a $0.1X$ deficit, the squared coefficient energy would need to satisfy

$$
\sum_{n\in I_{X,L}}[d_h^a(n)]^2
\ge\frac{9Q^2X}{80}
>\frac{576}{5}X^3,
$$

whereas the linear coefficient envelope limits the same quantity to at most $(4+o(1))X^3$. The missing factor exceeds $144/5=28.8$ asymptotically. No refinement of the **two-point arithmetic second-moment estimate alone** can supply that factor within the exact inequality (10).

This is an **obstruction to this single-step squared-energy certificate as a complete irrationality proof**, not an upper bound on actual cancellation. To reach Cook's $10\%$ threshold one must use genuinely global phase distribution, multiple-step correlations, or the unresolved weighted prime/cofactor cancellation. Merely sharpening the coefficient second moment cannot close that gap through (10).

## 6. Prior-art and hostile-scope review

**Classical versus this WP.** The shifted correlation Euler factors in (2)–(4) are classical and compatible with the shifted-multiplicative-correlation literature, notably [Balasubramanian–Giri–Srivastav (2017)](https://arxiv.org/abs/1511.02221). The direct elementary proof is included for source audit. The dyadic $\ell^2$ phase-energy transfer in (10), and its application and ceiling in (13)–(16), are bounded consequences; **no theorem-level priority is claimed**.

**Rational hostile control.** WP09-A gave explicit affine-periodic coefficients $a(n)$ with $0\le a(n)\le n$, exact rational full binary sum, and large positive and negative shifted differences at a selected shift. Its second moment is strictly positive too. The general transfer inequality (10) applies to those rational sequences. Thus an explicit nonzero variance and a strict small exponential saving for a selected $h$ are **compatible with a rational complete series**. This does not refute Cook's all-shift sufficient criterion, nor establish its 10% requirement.

**No unproved weighted cancellation promoted.** Cook's first unknown estimate,

$$
\mathrm{Re}\sum_{N\in\mathcal G}w_N(z_N-\bar z_{m_N})\le14X/25,
$$

remains open. Our two-point normalized correlation cannot control the exponential of the many other overlapping totient contributions inside $w_N$. The exact all-shift phase cocycle from WP09-A likewise exposes higher-order correlations whose cancellation is not implied by any pairwise second-moment result.

## 7. Claims, executable scope and next obligation

| Statement | Evidence classification |
| --- | --- |
| A: classical normalized shifted totient second moment with explicit positive Euler-product constant and fixed-shift logarithmic error | Complete elementary source proof; no novelty |
| B: actual shifted unnormalized totient-difference mass $(7/3)V_h X^3+O_h(X^2\log^2 X)$ on Cook's moving-depth block | Partial summation proof |
| C: exact finite phase-energy transfer for any integer coefficients with local differences below $Q/2$ | Algebraic modulo $Q$ and operator-norm proof; exact finite hostiles |
| D: actual Cook first-harmonic saving at least $V_hX/2500$ for every fixed $h$ and all sufficiently large $X$ | Unconditional bounded theorem, **far weaker** than Cook's 10% |
| Ceiling: the stated single-step $\ell^2$ certificate cannot itself reach a 10% deficit | Exact envelope and admissibility comparison, no claim about actual phase behavior |
| Strong Cook weighted correlation, first-harmonic 10%, complete-tail irrationality contradiction | **OPEN** |
| Original Erdős #249 / theorem novelty / independent authenticated proof certification | **OPEN / NOT_CLAIMED / MATHCERT NOT_SUBMITTED** |

Executable arithmetic and exact checker: [shifted_moment_energy.py](shifted_moment_energy.py). Tests extend existing governed [test_erdos249_full_series_phase.py](../../tests/test_erdos249_full_series_phase.py); no new CI routing or protected policy change. They use exact rational CRT finite-prime controls and exact integer phase-energy inequalities. Finite computations do **not** certify the infinite asymptotic; its proof is analytic and provided above.

**Next mathematical attack:** Prove a true *multi-step* phase-energy amplification or weighted exponential correlation for the actual totient at Cook's admissible depth. The certificate ceiling (16) rules out closing the 10% target merely by refining this particular second-moment bridge. Keep #3500 OPEN / Project #2 In Progress, parent #3201 and original Erdős #249 OPEN, MATHCERT NOT_SUBMITTED.
