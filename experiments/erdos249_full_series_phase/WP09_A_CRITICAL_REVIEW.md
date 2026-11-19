# Erdős #249 WP09-A — qualified adversarial proof audit

**Review status:** Logical mathematical challenge pass performed by the **same authenticated GCL agent**, in a separate role and stage. This is not an independent credentialed mathematics referee, Lean replay, MATHCERT certification, novelty adjudication or permission to close the original Erdős problem.

**Issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500) OPEN; original Erdős #249 OPEN.  
**Cook antecedent pinned:** Will Cook, *The Binary Totient Series*, 2026 revised October; [source commit 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac. Cook's four-term weighted first-harmonic target and the $9X/10$ whole-phase sufficient condition remain UNSOLVED.

## A. The arithmetic progression argument is source-independent

Let $M\ge2$ be squarefree and $(a,M)=1$. The exact identity

$$
\frac{\varphi(n)}n=\sum_{d\mid n}\frac{\mu(d)}d
$$

implies that only $d$ coprime to $M$ contribute for $n\equiv a\pmod M$. The CRT gives one residue modulo $Md$ per such $d$, hence its contribution over an interval of length $X+O(1)$ is $\mu(d)/d$ times $X/(Md)+O(1)$. Summing errors over $d\le4X$ costs $O(\log X)$; the absolutely convergent square-divisor tail costs $O_M(1)$. The constant is

$$
C_M=\prod_{p\nmid M}(1-p^{-2})
=\frac{6/\pi^2}{\prod_{p\mid M}(1-p^{-2})}
\ge6/\pi^2>3/5.
$$

No prime-number theorem or claim of totient-value independence enters this deduction. The chosen modulus $M_h$ exists for **each fixed** $h$, because omitting finitely many primes dividing $h$ does not change divergence of $\sum_p1/p$, and a sufficiently long product of the remaining $(1-1/p)$ is at most $29/50$. The computational modulus cap of 1,000,000 is solely an implementation/resource limit, **not** a restriction on this theorem.

## B. The two signed families have the claimed sizes and gap

In each coprime class, if the fraction of indices with $\varphi(n)/n\ge\tau=3/5$ is $g/B$, then the mean is at most $\tau+(1-\tau)g/B$. The precise lower proportion is $(C_M-\tau)/(1-\tau)\ge\kappa=15/\pi^2-3/2>0$, giving $\kappa X/M-O_{M,h}(\log X)$ instances on both residue classes, as in the manuscript.

For negative differences take $n\equiv-h\pmod M$ with $\varphi(n)\ge3n/5$. Since $M\mid n+h$, $\varphi(n+h)\le(29/50)(n+h)$ and

$$
d_h(n)=\varphi(n+h)-\varphi(n)
\le-n/50+29h/50\le-X/100
$$

for $n\ge X\ge58h$. For positive differences take $n\equiv0\pmod M$ and $\varphi(n+h)\ge3(n+h)/5$. Then $\varphi(n)\le29n/50$, so $d_h(n)\ge n/50+3h/5\ge X/50$. Because $(h,M)=1$, these residue classes are disjoint. Crucially, this is a **signed lower bound of linear order in $X$ for each fixed shift**; the density constant may be extremely small when $M_h$ is large.

The finite tests check both signs for shifts $h=1,2,3,6$ against independent phi sieve and exact numerator recurrence. This does not turn a finite observation into the all-$h$ asymptotic theorem; the source proof does.

## C. The phase recurrence has the correct coefficient and wrap bound

Cook's integer numerator is $D_{h,N,L}=\sum_{j=1}^L2^{L-j}d_h(N+j)$, so

$$
D_{h,N+1,L}=2D_{h,N,L}-2^Ld_h(N+1)+d_h(N+L+1).
$$

For $r_N$ the centered residue modulo $Q=2^L$, the modular relation is $r_{N+1}-2r_N\equiv d_h(N+L+1)\pmod Q$ **with no discarded summands**. If $|d_h(n)|\ge X/100$ and both centered residues have magnitude below $X/300$, their difference $z$ has $|z|<X/100$. But $|d_h(n)|\le n+h<3X$ for the exact finite observation interval when $h+L+1\le X$, and $Q\ge16(2X+h+L+2)>32X$. Thus $z-d_h(n)$ is a **nonzero integer multiple of $Q$ of absolute value below $Q$**, contradiction. Each good endpoint yields at least one gap of $X/(300Q)$ among adjacent starts. A start belongs to at most two endpoint-pairs. The count $\kappa X/M-O_{M,h}(\log X)$ is valid after pairing the two signed families.

## D. Does the choice of depth preserve Cook's true quantifiers?

Yes, but only for all sufficiently large $X$ **after fixing $h$**. Choose the least $L$ with $2^L\ge16(2X+h+L+2)$. Then $L=O_h(\log X)$ and eventually $L\ge h+26$, so it is in Cook's common-depth permitted range. For all sufficiently large $X$, the previous depth $L-1$ fails the size inequality; thus

$$
2^L<32(2X+h+L+1)\le96X
$$

for $X\ge h+L+1$. Therefore the guaranteed finite phase distance is at least $1/28800$, on at least $\kappa X/(2M)$ starts after absorbing the logarithmic count error. The real part of each of their unit phases is at most $\cos(2\pi/28800)$, yielding the explicit $c_h$ in the manuscript. The auxiliary elementary bound $1-\cos(2\pi t)\ge8t^2$ on $0\le t\le1/2$ gives a fully algebraic estimate $c_h\ge4\kappa/(M_h28800^2)>0$. This is a real theorem for the **actual Cook exponential phases**.

**Critical scale limitation:** The proved saving is of order $10^{-10}/M_h$, vastly smaller than Cook's required $0.1$; the global $9X/10$ bound and Cook's open first term $\operatorname{Re}\sum_{\mathcal G}w_N(z_N-\bar z_m)\le14X/25$ are NOT established. An increase in depth decreases both the forced fractional separation and the omitted-tail radius in comparable proportions, so this one-step certificate by itself cannot bridge the mathematical gap.

## E. Is the additive-to-multiplicative cocycle exact?

For any integer coefficient sequence $a$ and any positive $h,k$ at a **common fixed L**, the identity

$$
D^a_{h+k,N,L}=D^a_{h,N,L}+D^a_{k,N+h,L}
$$

follows by telescoping the coefficient difference inside each binary-window summand. Exponentiating gives $E^a_{h+k,N,L}=E^a_{h,N,L}E^a_{k,N+h,L}$ and therefore $E^a_{h,N,L}=\prod_{r<h}E^a_{1,N+r,L}$. This is an exact **higher-order phase-correlation reduction**, not a theorem that correlations are small. The abstract unit process $u_N=i(-1)^N$ has zero mean on even blocks yet all neighboring products equal one; hence first-shift marginal cancellation alone does NOT imply the needed all-shift cancellation. The hostile is an abstract phase counterexample, not asserted a totient model.

## F. Does a rational complete series exhibit the same signs and weak cancellation?

Yes. For fixed $h$, choose any $M\ge3$ coprime to $h$ and define $a_n=n$ for $n\equiv\pm h\bmod M$, $a_n=0$ for $n\equiv0\bmod M$, and $a_n=\lfloor n/2\rfloor$ otherwise. The coefficients are bounded by $n$ and affine in $n$ on every class modulo $2M$, hence their *full* binary series is exactly rational, by summing geometric and derivative-geometric series on each residue class. Yet $a_{n+h}-a_n=-(n)$ on $n\equiv-h\bmod M$ and $a_{n+h}-a_n=n+h$ on $n\equiv0\bmod M$. Strong signed differences at a **chosen** $h$ and some corresponding harmonic saving therefore do not imply irrationality. The denominator of that rational series need not have multiplicative period $h$, so the example does not refute Cook's all-$h$ sufficient criterion.

## G. Claim disposition, prior art and workload integrity

**Accept with scope:** fixed-modulus progression totient mean; positive-density signs of each fixed shifted difference; exact Cook first-harmonic phase gap; explicit unconditional **weak** $c_h>0$ saving; exact shift cocycle; rational quasi-linear hostile counterexample. All are proved algebraically in the source. Do **not** assert this solves original Erdős #249, the global $9X/10$ harmonic requirement, Cook's weighted correlation, or any MATHCERT theorem.

Provenance: Cook 2026 already isolates the first-harmonic four-term problem, and G. Martin's 2006 shifted totient inequalities are an antecedent to order/sign arguments. No novelty or theorem priority is adjudicated. Tests and source formatting gates are not independent mathematical referees. Review is a logically separate same-agent pass, explicitly noncertifying.

**Research successor:** Quantitative amplification of the higher-order shift-one cocycle correlations **for actual totient**, or Cook's weighted prime/cofactor residual correlation. A fixed-sign CRT lemma cannot provide the required order-$0.1X$ cancellation by itself. Keep issue #3500, Project #2 In Progress, original #249 and parent #3201 OPEN, MATHCERT NOT_SUBMITTED.
