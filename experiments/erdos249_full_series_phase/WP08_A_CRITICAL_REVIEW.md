# Erdős #249 — WP08-A qualified adversarial mathematical review

**Review:** non-authoring, logically separate GCL Adversary/Referee pass staffed by the **same authenticated agent** as source author. This is not a separately credentialed independent theorem review, Lean replay, historical-novelty adjudication, or MATHCERT certification.  
**Workstream:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500); original Erdős #249 **OPEN**.  
**Reviewed manuscript SHA-256:** 7242a78dccfca9f7fefb2c52d7d17ac49f99bcd1c9ca9063d25a5158fe1b12f6.  
**Reviewed exact module SHA-256:** 2040f7374a13260706060edfcca8ba00ecfac5ab88198c8ce67435ff62f86059.  
**Reviewed existing registered tests SHA-256:** 15967b6f9cb8d796fd61a487b890e55ac627f7be98ba89174aaf82c33149bbb1.  
**Exact source head at full replay:** 1ff10c1b7cda620b1a0372a97273aaa044701fce.  
**Source replay:** 38/38 full-suite tests PASS; manuscript mathematical gate PASS.

## 1. Does the finite integer recurrence contain an unnoticed boundary error?

For any fixed depth L and integer coefficients a(n),

$$
A_{N,L}=\sum_{j=1}^L2^{L-j}a_{N+j}.
$$

Expanding the next window gives exactly

$$
A_{N+1,L}=2A_{N,L}-2^L a_{N+1}+a_{N+L+1}.
$$

The same formula applies to the difference of two sequences. At $X\ge64$, $L=\lfloor\log_2X\rfloor+4$ makes $Q=2^L$ satisfy $8X<Q\le16X$, and $N+L+1<3X$ whenever $X\le N\le2X-2$. These exact inequalities are essential: the centered residue comparison would fail if a possible congruence wrap had magnitude $Q$. The proof's upper bound of at most $3.5X$ is strictly below $Q$. Independent direct-versus-rolling tests exercise all endpoints.

## 2. Does the totient mean supply enough endpoints with large coefficient values?

Yes. The identity $\varphi(n)/n=\sum_{d\mid n}\mu(d)/d$, absolute convergence of $\sum\mu(d)/d^2=6/\pi^2$, and the elementary harmonic bound for floor-sum errors yield

$$
\sum_{n\le Y}\varphi(n)/n=(6/\pi^2)Y+O(\log Y).
$$

Subtract at the two endpoints of the interval of length $X-1$, starting at $X+L+1$ with $L=O(\log X)$. If $g$ indices satisfy $\varphi(n)/n\ge1/2$, then total ratio is at most $g+(X-1-g)/2$, forcing $g\ge(12/\pi^2-1)X-O(\log X)$. Since $6/\pi^2>1/2$, this is a positive-density set. The proof only uses a **classical** mean identity, not an unproved independent-prime model.

For every such endpoint, both adjacent centered residues smaller than $X/6$ would produce an integer $z$ with $|z|<X/2$ and $\varphi(n)\equiv z\pmod Q$, although $X/2\le\varphi(n)<3X$. Their difference lies strictly between 0 and $Q$, an impossibility. Each qualifying start is touched by at most two endpoints; the resulting count has leading coefficient $6/\pi^2-1/2$. The normalized gap is at least $1/96$, including the case $X$ is an exact power of two.

## 3. Does the six-divisibility comparison use genuine multiplicativity?

Yes. When $6\mid n$, Euler's product proves $\varphi(n)/n\le(1-1/2)(1-1/3)=1/3$. With $c_n=\lfloor n/2\rfloor$, the difference $\varphi(n)-c_n$ lies between $-n/2$ and $-n/6$ (including valid weak endpoints). The same exact residue recurrence then requires one of the two adjacent **complete finite-tail differences** to be at least $X/(18Q)\ge1/288$ away from an integer. Multiples of six are separated by six indices, so their neighboring two-start pairs are disjoint, yielding $X/6-O(1)$ **distinct** affected starts, not a result requiring an independence assumption.

## 4. Does over-log phase rigidity apply to all linearly bounded targets?

Yes, but only to exact finite-phase equality at *both neighboring starts*. If $0\le a_n,t_n\le n$ and the two scaled complete finite tails match modulo one for $N$ and $N+1$, the recurrence forces $Q$ to divide $a_{N+L+1}-t_{N+L+1}$. Its absolute value is less than $3X<Q$, hence it is exactly zero. This quantifier is narrower than a one-start claim and is why the theorem does not conflict with GCL WP07-E's **below-log** all-start rational interpolation. There is no claim that mere phase similarity or some sporadic matches force sequence identity.

## 5. Is the finite-prime escape theorem genuinely uniform over every fixed support?

For every **fixed** finite set of primes $P$, the integer coefficient $g_P(n)=n\prod_{p\mid n,p\in P}(1-1/p)$ is the finite divisor expansion $\sum_{d\mid M_P,\ d\mid n}\mu(d)n/d$. Therefore its **full infinite** binary series is the exact rational finite sum $\sum_{d\mid M_P}\mu(d)2^d/(2^d-1)^2$. This is the same known Möbius identity restricted to squarefree support; the priority belongs to antecedents, not to WP08-A.

For any fixed omitted prime $p\notin P$ and $p\mid n$, multiplicativity gives

$$
g_P(n)-\varphi(n)\ge g_P(n)/p\ge c_P n/p,
\qquad c_P=\prod_{q\in P}(1-1/q)>0.
$$

The centered-difference recurrence consequently forces one of two adjacent windows to have fractional distance at least $c_P/(48p)$. Among $X-1$ consecutive candidate endpoints, multiples of $p$ number $X/p-O(1)$; pairs are disjoint because $p\ge2$. **No prime theorem, smoothness assumption or unproved Euler-product limit estimate is invoked.**

The critically important limitation is that the constants depend on the **entire support** $P$ and the omitted prime $p$. This is *not uniform* as $P$ grows: neither the support weight $c_P$ nor the density $1/p$ has a fixed positive lower bound across larger prime sets. The finite sum's rational denominator is also unconstrained. No claim that the prime-escape tower settles the full infinite Euler product is permitted.

## 6. Can the stronger finite phase separation force irrationality via the tail estimate?

No. The actual positive omitted tail obeys

$$
0< R_{N,L}<\frac{N+L+2}{2^L}.
$$

The unconditional gap $X/(6Q)$ is smaller than the allowed tail correction, which can be order $2X/Q$, and the original rationality test must handle **every** hypothetical denominator and the signed one-sided residue. The proof does not establish that a finite residue remains separated after adding the omitted infinite tail. In addition, two **genuine rational** countermodels pass the same local phase-gap mechanisms: $\sum\lfloor3n/4\rfloor2^{-n}=14/15$ and the periodic-six defect model with exact sum $2582/3969$. Consequently no unsupported generic irrationality inference may be taken from the positive-density result.

The exact finite-prime approximants also have rational full sums while themselves exhibiting nontrivial finite-phase differences from totient. That is a useful distinction but not a full-series proof.

## 7. Numerical evidence, provenance and resource usage

The governed exact test file is **already registered** and retains 27 previous cases plus 11 new cases; no protected policy route, workflow or branch protection is changed. Tests independently check phi by direct coprime counts, direct versus rolling finite numerator arithmetic, the centered modulus, actual totient phase gaps, modular six-factor gaps, rational full-sum closed forms, exact finite-prime Euler product coefficients and sums, a sequence of omitted-prime examples, and invalid-source controls. A finite sample does not establish an all-$X$ density asymptotic; the manuscript proof does.

The exact finite-prime rational evaluator deliberately stops if the product of supported primes exceeds 512, to avoid expensive giant-integer denominators in constrained execution. This **implementation guard** does not restrict the symbolic Theorem D, and there is no policy authority change to remove the guard.

**Disposition:** ACCEPT_WITH_SCOPE for manuscript theorems A–D, the explicit and non-uniform prime-escape hierarchy, the exact hostiles, and the declared absence of an irrationality or novelty claim. Retain #3500 and original #249 OPEN / MATHCERT NOT_SUBMITTED. The next substantive mathematical obligation remains a totient-specific **uniform cofinal separation of the complete infinite binary tail** or Cook's already-source-locked sufficient harmonic saving.
