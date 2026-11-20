# Erdős #249 — WP09-C: an effective joint local-phase law for shifted totients

**Scientific issue:** MATH-PROGRAMME #3500.  
**Claim class:** bounded noncertifying arithmetic theorem; original Erdős #249 OPEN; MATHCERT NOT_SUBMITTED.  
**Date:** 2026-11-20.  
**Exact antecedents:** GCL WP09-A/B, especially SHIFTED_MOMENT_ENERGY_009B.md.  
**Primary problem-specific source:** Will Cook, *The Binary Totient Series* (2026, revised October), pinned at [3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac.

## 1. Exact distinction between local and Cook phases

Fix a finite nonempty collection of triples $(w_i,u_i,v_i)$, with integer weights and nonnegative integer offsets. Assume some weight is nonzero. Define

$$
W=\sum_i|w_i|,\quad H=\max_i(u_i,v_i),\quad
f(n)=\frac{\varphi(n)}n,\quad
Z_X(Q)=\frac1X\sum_{n=X}^{2X-1}
\exp\left(\frac{2\pi i}{Q}\sum_iw_i[\varphi(n+u_i)-\varphi(n+v_i)]\right).
\tag{1}
$$

Here $X$ and $Q$ are positive integers, $X\ge64$, and $Q\ge32X$. The single-shift cocycle in GCL WP09-B is the choice $(w,u,v)=(1,h,0)$.

**Important firewall:** Formula (1) is a characteristic function of finitely many *local* shifted differences, scaled by $Q$. It is NOT Cook's original phase

$$
E_{h,N,L}=\exp\left(2\pi i\sum_{j=1}^{L}
\frac{\varphi(N+h+j)-\varphi(N+j)}{2^j}\right),
\tag{2}
$$

whose number of contributing positions grows with $L\asymp\log X$ and whose early terms have amplitudes of order $X$. No conclusion about a tenth-saving in (2) is asserted.

## 2. Effective finite-prime characteristic theorem

For integer $y\ge2$ put $P_y=\prod_{p\le y}p$ and

$$
f_y(n)=\prod_{\substack{p\le y\\p\mid n}}\left(1-\frac1p\right),
\qquad
\Delta_y(a)=\sum_iw_i[f_y(a+u_i)-f_y(a+v_i)].
\tag{3}
$$

The product defining $f_y$ is periodic modulo $P_y$. For $\rho\ge32$ define the finite, explicitly computable mean

$$
C_y(\rho)=\frac1{P_y}\sum_{a\bmod P_y}
\int_1^2\exp\left(\frac{2\pi i t}{\rho}\Delta_y(a)\right)\,dt.
\tag{4}
$$

This is an **exactly defined finite expression**. Its period values $\Delta_y(a)$ are rational, and the integral is elementary. The float evaluation in the executable is not an interval certificate.

**Theorem A (effective local joint characteristic).** Let $\rho=Q/X$, with the parameters above, and let $P_y$ be unrestricted mathematically (the executable imposes a finite resource cap). Then

$$
\boxed{\begin{aligned}
|Z_X(Q)-C_y(\rho)|
\le{}&
\frac{4\pi HW}{Q}\\
&+\frac{8\pi W}{\rho}
 \left[\frac1y+\frac{1+\log(2X+H)}X\right]\\
&+\frac{P_y}{X}\left(2+\frac{4\pi W}{\rho}\right).
\end{aligned}}
\tag{5}
$$

Furthermore the limit $C(\rho)=\lim_{y\to\infty}C_y(\rho)$ exists for all $\rho\ge32$, uniformly with respect to such $\rho$, and

$$
\boxed{|C(\rho)-C_y(\rho)|\le\frac{8\pi W}{\rho y}.}
\tag{6}
$$

In particular, uniformly for **arbitrary** integer $Q\ge32X$, when the triples are fixed,

$$
\boxed{Z_X(Q)=C(Q/X)+O_{W,H}\left(\frac{\log\log X}{\log X}\right).}
\tag{7}
$$

The only inputs are elementary prime-factor arithmetic, counting multiples in an interval, and periodic Riemann sums. There is no probabilistic prime independence, unproved prime distribution, or high-degree correlation assumption.

### Proof of Theorem A

**Step 1: replace the actual totient ratio by finite-prime ratios.** Since each omitted Euler factor lies in $[0,1]$,

$$
0\le f_y(m)-f(m)
\le\sum_{\substack{p>y\\p\mid m}}\frac1p.
\tag{8}
$$

For each fixed nonnegative offset $s\le H$, the interval $X+s\le m<2X+s$ has length $X$. Every prime $p$ divides at most $X/p+1$ terms. Consequently

$$
\frac1X\sum_{n=X}^{2X-1}[f_y(n+s)-f(n+s)]
\le
\sum_{p>y}\frac1{p^2}
+\frac1X\sum_{p\le2X+H}\frac1p
\le \frac1y+\frac{1+\log(2X+H)}X.
\tag{9}
$$

The last inequality only enlarges the prime sums to integer sums. It does not invoke the prime number theorem.

**Step 2: account for changing the scale $n+s$ to $n$.** For every $s\le H$,

$$
\varphi(n+s)=(n+s)f(n+s)=nf(n+s)+sf(n+s),
$$

so the absolute error in the weighted sum after replacing all shifted totients by $n f_y(n+s)$ is bounded on average by

$$
2HW+2nW\left[\frac1y+\frac{1+\log(2X+H)}X\right]
$$

after using $n<2X$ in the final average. More explicitly, the unscaled offset error is at most $2HW$ and the mean of the ratio error is at most $2W$ times (9). The inequality $|e^{2\pi iu}-e^{2\pi iv}|\le2\pi|u-v|$ and $n/Q<2/\rho$ give the first two terms of (5).

**Step 3: equidistribute finite residue classes, not prime factors.** Write

$$
G_a(t)=\exp(2\pi it\Delta_y(a)/\rho).
$$

Each function is bounded in modulus by one and satisfies

$$
|G_a'(t)|\le\frac{4\pi W}{\rho},
$$

because $|\Delta_y(a)|\le2W$. The values $n/X$ with $n\equiv a\pmod{P_y}$ form a mesh of spacing $P_y/X$. A one-dimensional bounded-variation Riemann-sum comparison, including the two possible boundary intervals, yields per residue an unnormalized discrepancy at most $2+\int_1^2|G_a'(t)|dt$. Summing over the $P_y$ residue classes and dividing by $X$ gives the last term of (5). This establishes Theorem A's first assertion.

**Step 4: pass to all primes.** If $y'\ge y$, average both $C_{y'}$ and $C_y$ over residues modulo $P_{y'}$. For either shifted argument $a+s$, an omitted prime $p\in(y,y']$ divides a uniformly sampled residue modulo $P_{y'}$ with exact probability $1/p$. Therefore

$$
\frac1{P_{y'}}\sum_{a\bmod P_{y'}}
|f_{y'}(a+s)-f_y(a+s)|
\le\sum_{p>y}\frac1{p^2}\le\frac1y.
\tag{10}
$$

Since $t\le2$ in (4), the exponential Lipschitz inequality and the $2W$ total weighted shifted terms give

$$
|C_{y'}(\rho)-C_y(\rho)|\le\frac{8\pi W}{\rho y}.
$$

The Cauchy limit and (6) follow with the same bound. The estimate is uniform in $\rho\ge32$.

**Step 5: choose an effective moving prime support.** For sufficiently large $X$, let

$$
y=\left\lfloor\frac{\log X}{4\log\log X}\right\rfloor.
$$

Then $y\to\infty$ and, without any estimate for primes,

$$
P_y\le y!\le y^y\le X^{1/4}
$$

for sufficiently large $X$. Combining (5) and (6) gives (7). Every constant can be chosen from the fixed triples. QED.

## 3. Exact single-shift symmetry and contact with WP09-B

For a single triple $(1,h,0)$, the map $a\mapsto-a-h\bmod P_y$ reverses $\Delta_y(a)$, since $f_y(-m)=f_y(m)$. Hence $C_y(\rho)$, and therefore $C(\rho)$, is **real**.

Define the limiting second moment $V_h$ from WP09-B:

$$
V_h=2\left[\prod_p\left(1-\frac2{p^2}+\frac1{p^3}\right)
-\prod_{p\mid h}\left(1-\frac2{p^2}+\frac1{p^3}\right)
 \prod_{p\nmid h}\left(1-\frac2{p^2}\right)\right]>0.
\tag{11}
$$

The exact finite CRT calculation yields
$\lim_{y\to\infty}P_y^{-1}\sum_a\Delta_y(a)^2=V_h$.
Taylor's theorem for cosine, bounded by $|\Delta_y|\le1$, now gives the **quantitative** expansion

$$
\boxed{
\left|\,C(\rho)-\left(1-\frac{14\pi^2V_h}{3\rho^2}\right)\right|
\le\frac1{24}\left(\frac{4\pi}{\rho}\right)^4,\quad\rho\ge32.
}
\tag{12}
$$

Thus the whole one-step *local* complex characteristic, not merely its variance, has a fully characterized arithmetic limit. The integral $\int_1^2t^2dt=7/3$ explains the coefficient in (12). This is a refinement of the arithmetic input to WP09-B, **not a solution of its transfer loss**.

For example the independently calculable finite-prime model at $h=1$, $y=11$, $\rho=32$ gives approximately $1-\mathrm{Re}C_y=0.00986529$. The displayed decimal is illustrative and **not** an independently certified bound on the true limit; (6) supplies the rigorous truncation envelope.

## 4. Why this cannot be promoted to Cook's needed conclusion

The exact Cook sliding recurrence in WP09-A/B supplies the **one-step cocycle**

$$
E_{h,N+1,L}\overline{E_{h,N,L}}^{\,2}
=\exp\left(\frac{2\pi i}{2^L}
 [\varphi(N+L+h+1)-\varphi(N+L+1)]\right).
\tag{13}
$$

Theorem A gives the joint local distribution of any *fixed* finite collection of the right-hand-side terms at comparable scale $2^L\asymp X$, and can support a fixed-order cocycle analysis.

It does **not** give equidistribution of the full left-side Cook phase, because the original phase contains $L\asymp\log X$ overlapping coefficients weighted by $2^{-j}$, and is not controlled to constant angular accuracy by the *elementary error estimate (9)* with a fixed finite set of primes: that estimate gives only an $O(X/y)$ bound. Making **this bound** $o(1)$ would require $y\gg X$, for which the period $P_y$ is far beyond the available $X$ block and the periodic comparison is ineffective. This does not rule out a smaller actual error from additional arithmetic cancellation.

This is a precise **two-scale obstruction to applying the present theorem**, not a proof that every possible arithmetic method must fail. It shows that the next positive producer must couple many scales or control Cook's source-locked weighted prime/cofactor correlation directly. A constant-saving on local differences, even on every fixed finite set, does not establish the needed one-tenth saving for $E_{h,N,L}$ or the good-base $603X/1000$ condition.

## 5. Reproducibility, antecedents and claim ledger

The executable [joint_local_prime_law.py](joint_local_prime_law.py) computes exact rational CRT profiles and moments, evaluates finite trigonometric integrals numerically, and exposes the non-certified analytic error formula in (5). The governed existing full-series test file contains independent small-prime factor oracles, exact-period moment checks, finite-totient phase checks, cutoff bounds, malformed-argument rejection and a countercheck that the Cook phase is not the local cocycle.

Classical shifted multiplicative-function correlations were studied by R. Balasubramanian, S. Giri and P. Srivastav, *On correlations of certain multiplicative functions*, Journal of Number Theory 174 (2017), 221–238, DOI 10.1016/j.jnt.2016.10.001. The finite-prime periodic approximation and elementary characteristic-function limit are submitted as a **self-contained bounded reconstruction**, without theorem-level novelty, historical priority or independent mathematical certification. Existing Cook first-harmonic work and WP09-A/B remain the exact antecedents.

| Claim | Status |
| --- | --- |
| Effective joint local characteristic, equations (5)–(7) | Proved in this bounded manuscript; exact hostile finite tests required |
| Finite-prime single-shift symmetry and expansion (12) | Proved using protected WP09-B classical second moment |
| True Cook phase weighted cancellation of 10% on every fixed shift | OPEN |
| Cook's good-base estimate, at most 603X/1000 | OPEN |
| Original Erdős #249 full-series irrationality | OPEN |
| Lean replay / MATHCERT / independent human mathematical certificate | NOT_SUBMITTED |

**Next research obligation:** establish a logarithmically many-step actual-totient phase-product correlation with quantitative cancellation across the genuinely weighted Cook window. Keep #3500 and Project #2 In Progress, do not close original Erdős #249 from this bounded result.
