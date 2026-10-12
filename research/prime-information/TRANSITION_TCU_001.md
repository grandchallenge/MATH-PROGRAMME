# The Information Geometry of Prime Factorization
## Transition Problem TCU-001: a uniform saddle-point correlation law

**Research state:** active mathematical target, **not proved**.  
**Version:** 0.1, 2026-10-11.  
**Owner:** GCL mathematical research, MATHFORGE → MATHSOLVE; certification reserved to MATHCERT.  
**Rendered mathematical edition:** [Read the transition research note with typeset equations](https://grandchallenge.github.io/MATH-PROGRAMME/PRIME_INFORMATION_TRANSITION/).  
**Companion:** [Synthesis manuscript](MANUSCRIPT.md).

### 1. The central question

Let $2\le y\le X$ and let $N$ be uniformly distributed on

$$
S(X,y)=\{n\le X:P^+(n)\le y\},\qquad \Psi(X,y)=|S(X,y)|.
$$

Write $V_p=v_p(N)$ and $k=\pi(y)$. The total correlation is

$$
T(X,y)=\sum_{p\le y}H(V_p)-\log\Psi(X,y).
$$

It measures the dependence imposed on the prime exponents by the single global inequality $\sum V_p\log p\le\log X$.

Put $t=\log X$, $u=t/\log y$, and define the finite Euler product

$$
Z_y(s)=\prod_{p\le y}(1-p^{-s})^{-1},\quad
M_y(s)=\sum_{p\le y}\frac{\log p}{p^s-1},\quad
\sigma_y^2(s)=\sum_{p\le y}\frac{(\log p)^2p^s}{(p^s-1)^2}.
$$

There is a unique positive counting saddle point $\alpha=\alpha(X,y)$ satisfying $M_y(\alpha)=t$.

**Target TCU-001 (conjectural, not a proved theorem).** Establish an explicit and genuinely uniform error function $\varepsilon(X,y)\to0$ as *both* $y\to\infty$ and $u=\log X/\log y\to\infty$, with

$$
\boxed{T(X,y)=\log\!\bigl(\alpha\sqrt{2\pi\sigma_y^2(\alpha)}\bigr)-1+\varepsilon(X,y).}
$$

If this is false without additional growth conditions, isolate a counterregime and identify its correction term. The target is a **two-sided** result, not a one-sided bound, and it must be compatible with fixed-prime, sparse-prime, Dickman and saddle-point descriptions wherever those apply.

### 2. Exact master decomposition (proved algebraically)

Define the product reference measure $Q_s$ on all positive integers whose prime factors do not exceed $y$:

$$
Q_s(V_p=j)=(1-p^{-s})p^{-sj}.
$$

For the actual marginal $P_p=\mathcal L(V_p)$, define

$$
\Delta=t-\mathbb E_P[\log N]\ge0,\qquad K_s=\sum_{p\le y}D(P_p\Vert Q_{p,s})\ge0.
$$

Then for **every** $s>0$,

$$
\begin{split}
T(X,y)&=D(P\Vert Q_s)-K_s,\\
D(P\Vert Q_s)&=\log Z_y(s)+s(t-\Delta)-\log\Psi(X,y).
\end{split}
$$

This identity is finite and exact. It is a KL chain rule, not an approximation.

Hildebrand--Tenenbaum's saddle-point counting theorem [HT93, Theorem 1.6, equation (1.22)] gives uniformly for $X\ge y\ge2$,

$$
\Psi(X,y)=\frac{X^\alpha Z_y(\alpha)}
{\alpha\sqrt{2\pi\sigma_y^2(\alpha)}}
\left(1+O(1/u+\log y/y)\right).
$$

Consequently **in ranges where $u,y\to\infty$**, taking logarithms yields

$$
\boxed{
T(X,y)=\log\!\bigl(\alpha\sqrt{2\pi\sigma_y^2(\alpha)}\bigr)
-\alpha\Delta-K_\alpha+O(1/u+\log y/y).
}\tag{M}
$$

This is the master transition formula. It reduces TCU-001 to **two separately testable obligations**:

$$
\boxed{\alpha\Delta=1+o(1),\qquad K_\alpha=o(1)}
$$

uniformly as $u,y\to\infty$. The two obligations are sufficient, not asserted necessary separately from the targeted combination. Never infer their truth merely from the counting theorem.

### 3. An exact local influence representation (proved algebraically)

Let $W\sim\mathop{\mathrm{Exp}}(s)$ independent of $Q_s$ and

$$
E=\sum_{p\le y}V_p\log p+W.
$$

Its density is

$$
f_E(t)=\frac{s e^{-st}}{Z_y(s)}\Psi(e^t,y).
$$

The conditional law $\mathcal L((V_p)_p\mid E=t)$ is exactly the uniform distribution on integers not exceeding $e^t$ whose prime factors are at most $y$. For each prime $p$, let $f_{-p}$ denote the density of

$$
E_{-p}=\sum_{\substack{q\le y\\q\ne p}}V_q\log q+W.
$$

Then

$$
\boxed{
P_p(j)=Q_{p,s}(j)\,\frac{f_{-p}(t-j\log p)}{f_E(t)}
\quad(j\ge0).
}\tag{L}
$$

The ratio is interpreted as $0$ for negative arguments. This follows directly from the density factorization of $(V_p,E)$. It is a useful route to the local limit theorem because removing one prime is a controlled perturbation of the full energy.

Set

$$
R_{p,j}(t)=f_{-p}(t-j\log p)/f_E(t).
$$

Then

$$
K_s=\sum_{p\le y}\sum_{j\ge0}Q_{p,s}(j)\,R_{p,j}\log R_{p,j}
$$

exactly, and the elementary chi-squared inequality gives the **finite bound**

$$
\boxed{
0\le K_s\le
\sum_{p\le y}\sum_{j\ge0}Q_{p,s}(j)(R_{p,j}-1)^2.
}\tag{I}
$$

This upper bound is nonasymptotic. A summable local-energy influence estimate making the right-hand side $o(1)$ would close the second obligation in TCU-001. It would also avoid the uncontrolled step of summing pointwise error terms over a growing set of primes.

### 4. Boundary tests that any theorem must pass

**Fixed $y$, $X\to\infty$.** Let $k=\pi(y)$. The continuum simplex calculation gives

$$
T(X,y)\longrightarrow C_k=\log(k!)-k\log k+k-1.
$$

At the counting saddle $\alpha$, $\alpha\Delta\to k/(k+1)$ and $K_\alpha\to1/(k+1)$. In particular **neither term can be discarded when $k$ stays fixed**, even if $u\to\infty$. This is why the target explicitly requires $y\to\infty$.

**Sparse-prime joint limit.** The internal working Note 007 derives a finite-dimensional simplex inequality. If $k\to\infty$ and

$$
k^3\sum_{p\le y}\log p=o(\log X),
$$

it gives

$$
T(X,y)=\tfrac12\log(2\pi k)-1+o(1),\quad
\alpha\Delta\to1,\quad K_\alpha\to0.
$$

**Status:** author-derived / internal proof; external certification and novelty not established. Its original manuscript and replay identifiers are recorded in [README](README.md).

**Fixed $u>1$, $y\to\infty$.** The internally derived Dickman expansion has the form

$$
T(X,y)=\log\log y+\gamma-1-\log\rho(u)-J(u)+o(1),
$$

where

$$
J(u)=\int_0^1
\frac{a_u(v)\log a_u(v)-a_u(v)+1}{v}\,dv,
\qquad a_u(v)=\rho(u-v)/\rho(u).
$$

The fixed $u$ law and the growing $u$ law are not interchangeable without uniform remainder estimates. Earlier internal Notes 003--005 propose such refinements; their full proof details must be re-audited before promotion.

**Unrestricted cutoff.** At $y=X$, the known total-correlation asymptotic is $\log\log X+\gamma-1+o(1)$. But here $u=1$ and the TCU-001 hypothesis $u\to\infty$ fails: this is a compatibility example, *not* a test within the conjectured domain.

### 5. Work packages

- **TCU-WP1, slack local law:** Prove $\alpha\Delta=1+o(1)$ uniformly for $y,u\to\infty$, preferably with an explicit bound in terms of $\alpha\sigma_y(\alpha)$ and a verified local limit error for the exponential-smoothed energy.
- **TCU-WP2, single-prime leave-one-out local law:** Compare $f_{-p}(t-j\log p)$ to $f_E(t)$ in the weighted $L^2$ sense under $Q_{p,\alpha}$ of (I), uniformly over all $p\le y$ and $j\ge0$. Track prime-power tails separately.
- **TCU-WP3, matching transition:** Combine (M), WP1 and WP2; obtain a uniform explicit remainder and reconcile it with both the sparse simplex and Dickman regimes. If the target fails, construct a rigorously sourced counterregime.
- **TCU-WP4, reproducible falsification:** Independently enumerate accessible $(X,y)$, compute exact $T,\Delta,K_\alpha,\sigma$, and compare predictions; include $k=1$, fixed small $k$, $u$ close to $1$, moderate $u$, and growing $k$ controls. Numerical agreement is not proof.
- **TCU-WP5, priority and source audit:** Compare against HT93, Tenenbaum 2023, literature on probabilistic smooth numbers, conditional local limit theorems, and entropy of logarithmic combinatorial structures. Record theorem-level novelty only after review.

### 6. Research hygiene

- A theorem proved *under imported analytic estimates* must display the exact estimates and their valid ranges.
- Author self-review, a separate script, and GitHub CI are **not independent mathematical certification**.
- Do not infer factoring speedups or an RH result from this information-theoretic observable.
- A failed TCU-001 conjecture is a legitimate result if the obstruction is rigorous.
- Repository admission documents the investigation, not its mathematical certification.

### Primary references

[HT93] A. Hildebrand and G. Tenenbaum, *Integers without large prime factors*, Journal de Théorie des Nombres de Bordeaux **5** (1993), 411–484, https://doi.org/10.5802/jtnb.101 . Theorem 1.6 and equation (1.22) provide the counting saddle formula.

[T23] G. Tenenbaum, *Sur le biais d'une loi de probabilité relative aux entiers friables*, JTNB **35** (2023), 481–493, https://doi.org/10.5802/jtnb.1253 . Relevant caution concerning the biased canonical smooth-number measure.

[Tao25] T. Tao, *Smooth numbers and max-entropy* (2025), https://terrytao.wordpress.com/2025/09/15/smooth-numbers-and-max-entropy/ .

[DG93] P. Donnelly and G. Grimmett, *On the asymptotic distribution of large prime factors*, JLMS **47** (1993), 395–404, https://doi.org/10.1112/jlms/s2-47.3.395 .
