# Erdős #249 — WP09-E: a fixed-prime projection survives Cook's entire growing window

**Scientific issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Previous exact protected admission:** WP09-D [PR #3605](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3605), protected merge 1fb1c241c44aacf86abf000fae3efa4069389019.  
**Original full-series irrationality:** OPEN. **MATHCERT:** NOT_SUBMITTED.  
**Claim:** a new bounded, unconditional, uniformly-in-depth **arithmetic energy** theorem for Cook's genuine complete dyadic weighted window; not a modular Fourier cancellation theorem.  
**Primary source lock:** Will Cook, *The Binary Totient Series*, [paper revision 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*.

## 1. The actual growing-window object

Let $h\ge1$ and $X\ge1$ be integers, and let $L\ge1$ be an integer depth. Define

$$
f(n)=\frac{\varphi(n)}n,\qquad
Q=2^L,\qquad
D_{h,N,L}=\sum_{j=1}^L2^{L-j}
[\varphi(N+h+j)-\varphi(N+j)].
\tag{1}
$$

Cook's actual first-harmonic is the complex phase

$$
E_{h,N,L}=\exp(2\pi iD_{h,N,L}/Q).
\tag{2}
$$

This paper studies its **unwrapped** argument $A_{h,N,L}=D_{h,N,L}/Q$ and the complete, genuinely growing ratio observable

$$
G_{h,N,L}=\sum_{j=1}^L2^{-j}[f(N+h+j)-f(N+j)].
\tag{3}
$$

Unlike WP09-C/D, the number of shifted terms $L$ is **not fixed**. In particular $L$ may be Cook's least admissible depth, which grows as $\log_2 X$. A crucial distinction remains: $A$ is a real rational argument; the first harmonic only sees its class **modulo integers**.

## 2. Main theorem: exact finite-X full-window lower bounds

Fix any prime $p$ with $p\nmid h$; for the strongest easily reproducible bound choose the *smallest* such prime, which depends only on h and **does not grow with L**. Let

$$
H=L+h,\qquad
E_X=3+\mathrm{bitlength}(3X)
=4+\lfloor\log_2(3X)\rfloor.
\tag{4}
$$

Here bitlength is the number of binary digits of a positive integer, so $E_X$ is an **integer** with $E_X>2+\log(3X)$ and no floating computation is needed to verify the threshold.

**Theorem A (effective uniform full-Cook-window energy).** If

$$
\boxed{
H\le X,\qquad
X\ge40p^2\max(E_X,h+4),
}
\tag{5}
$$

then for the **actual Euler totient**, at **every** admissible depth $L$ satisfying (5),

$$
\boxed{
\frac1X\sum_{N=X}^{2X-1}G_{h,N,L}^{\,2}
\ge\frac1{400p^3}.
}
\tag{6}
$$

Furthermore the unwrapped genuine Cook phase satisfies

$$
\boxed{
\sum_{N=X}^{2X-1}
\left(\frac{D_{h,N,L}}{2^L}\right)^2
\ge\frac{X^3}{1600p^3}.
}
\tag{7}
$$

There is **no fixed-L, fixed-weight, or growing-separating-prime hypothesis**. For every fixed h, the least Cook-admissible depth

$$
L_h(X)=\min\{L\ge h:2^L\ge16(2X+h+L+2)\}
\tag{8}
$$

satisfies (5) for all sufficiently large X. Thus the lower bounds hold cofinally at the *exact logarithmically growing depth* in the pinned Cook problem.

**Corollary (positive density of large unwrapped winding arguments).** Under (5), at least a proportion $1/(28800p^3)$ of indices $X\le N<2X$ satisfy

$$
\boxed{
\left|\frac{D_{h,N,L}}{2^L}\right|
\ge\frac{X}{\sqrt{3200p^3}}.
}
\tag{9}
$$

This is a positive-density **large-unwrapped-argument** statement. It is **not** a positive-density large fractional-part statement.

For example, the exact integer threshold (5) already holds at the actual minimum Cook depths for $(h,X)=(1,4096),(2,8192),(6,32768)$. The executable checks these actual numerators without numerical Fourier extrapolation.

## 3. Lemma: uniform arithmetic progressions for real totient ratios

Let $p$ be any prime, $X\ge1$, $0\le s\le H\le X$ and $r\bmod p$. Then

$$
\boxed{
\left|
\sum_{\substack{X\le n<2X\\n\equiv r\pmod p}}f(n+s)
-\frac Xp\mu_p
\left(1-\frac1p\,\mathbf1_{\{r+s\equiv0\pmod p\}}\right)
\right|\le E_X,
}
\tag{10}
$$

where

$$
\mu_p=\prod_{q\ \mathrm{prime},\,q\ne p}(1-q^{-2})
\ge\prod_q(1-q^{-2})
=\frac6{\pi^2}>\frac35.
\tag{11}
$$

**Proof, with uniform constants.** Use the exact finite divisor expansion

$$
f(m)=\sum_{d\mid m}\frac{\mu(d)}d.
$$

Every relevant divisor is at most $M=2X+H\le3X$. For $p\nmid d$, the two congruences $n\equiv r\pmod p$ and $n+s\equiv0\pmod d$ have one solution class modulo $pd$, hence count $X/(pd)+\epsilon_d$ with $|\epsilon_d|\le1$. For $p\mid d$, they are incompatible unless $r+s\equiv0\pmod p$; in that case the second congruence already implies the first and has count $X/d+\epsilon_d$, $|\epsilon_d|\le1$.

Multiplication by $\mu(d)/d$ and summation over $d\le M$ costs at most

$$
\sum_{d\le M}\frac1d\le1+\log M
$$

in counting errors, with **no dependence on p, s, or H**. Extending the density main terms from $d\le M$ to all positive d costs at most

$$
X\sum_{d>M}\frac1{d^2}
\le\frac XM\le1.
$$

The infinite main term factors exactly: among divisors prime to p it is $(X/p)\mu_p$; the additional squarefree divisors divisible by $p$, only when $r+s\equiv0$, contribute $-(X/p^2)\mu_p$. This is the stated expression. The total error is at most $2+\log(3X)<E_X$, proving (10). All steps use counting and the absolutely convergent Euler product; no prime equidistribution, PNT, or probabilistic independence is assumed. QED.

## 4. Key new step: a prime smaller than the growing window still detects the whole window

For each residue $u\bmod p$, define the exact dyadic weights

$$
q_u^{(L)}
=\sum_{\substack{1\le j\le L\\j\equiv u\pmod p}}2^{-j},
\qquad
t_u^{(L)}=q_{u-h}^{(L)}-q_u^{(L)}.
\tag{12}
$$

All denominators divide $Q=2^L$; the executable computes their **integer numerators** exactly.

Since $p\nmid h$, the residue classes $1$, $1+h$ and $1-h$ appearing below have the required distinctness **from 1**. For every $L\ge1$,

$$
q_1^{(L)}\ge\frac12,\qquad
q_u^{(L)}\le
\frac{\frac14}{1-2^{-p}}
\le\frac13\quad\text{for every }u\not\equiv1\pmod p.
\tag{13}
$$

The strict dyadic gap follows **independently of L**:

$$
\boxed{
t_{1+h}^{(L)}
=q_1^{(L)}-q_{1+h}^{(L)}\ge\frac16,\qquad
t_1^{(L)}
=q_{1-h}^{(L)}-q_1^{(L)}\le-\frac16.
}
\tag{14}
$$

Thus the finite CRT residue aliases from all overlapping shifts **do not destroy** the first, most heavily weighted dyadic contribution. Earlier WP09-D used a separating prime larger than the largest offset, costing a factor of order $(\log X)^{-3}$. Equation (14) permits a **fixed** prime and avoids this loss entirely.

Apply Lemma (10) termwise to the true $G$ in (3); the absolute coefficient mass is bounded by

$$
\sum_{j=1}^L2^{-j}+\sum_{j=1}^L2^{-j}<2.
$$

The common conditional mean cancels between the positive and negative shifts. Therefore for every $r\bmod p$,

$$
\boxed{
\left|
\sum_{\substack{X\le N<2X\\N\equiv r\pmod p}}
G_{h,N,L}
+\frac{X\mu_p}{p^2}t_{-r}^{(L)}
\right|\le2E_X.
}
\tag{15}
$$

For the **two distinct** residue classes $r=-1$ and $r=-1-h$ modulo p, (14) and $\mu_p>3/5$ give

$$
\left|\sum_{\substack{X\le N<2X\\N\equiv r\pmod p}}
G_{h,N,L}\right|
\ge\frac X{10p^2}-2E_X
\ge\frac X{20p^2},
\tag{16}
$$

where the last inequality uses $X\ge40p^2 E_X$.

Each residue class contains at most $X/p+1\le2X/p$ integers because (5) implies $X\ge p$. Cauchy–Schwarz **separately on each of the two classes** gives

$$
\sum_{\substack{X\le N<2X\\N\equiv r\pmod p}}
G_{h,N,L}^{\,2}
\ge
\frac{(X/(20p^2))^2}{2X/p}
=\frac X{800p^3}.
\tag{17}
$$

Adding the two disjoint residue classes establishes (6) exactly. This proof works for arbitrarily many overlapping terms because their **total dyadic coefficient mass is less than two**. QED for (6).

## 5. Transfer to the complete actual Cook numerator

The identity $\varphi(m)=m f(m)$ gives the **exact**, nonasymptotic decomposition

$$
\boxed{
\frac{D_{h,N,L}}{2^L}
=N\,G_{h,N,L}+R_{h,N,L},
}
\tag{18}
$$

where

$$
R_{h,N,L}
=\sum_{j=1}^L2^{-j}
[(h+j)f(N+h+j)-j f(N+j)].
$$

Because $0\le f(m)\le1$,

$$
\boxed{
|R_{h,N,L}|
\le\sum_{j=1}^\infty2^{-j}(h+2j)
=h+4.
}
\tag{19}
$$

In particular, the error depends on **h only**, not on the growing depth L.

Use the reverse triangle inequality in the actual finite Euclidean norm on the X indices and note $N\ge X$. Equations (6) and (19) imply

$$
\begin{aligned}
\left(\frac1X\sum_{N=X}^{2X-1}A_{h,N,L}^{\,2}\right)^{1/2}
&\ge X
\left(\frac1X\sum_{N=X}^{2X-1}G_{h,N,L}^{\,2}\right)^{1/2}
-(h+4)\\
&\ge\frac X{20p^{3/2}}-(h+4)
\ge\frac X{40p^{3/2}}.
\end{aligned}
\tag{20}
$$

The last step follows from $X\ge40p^2(h+4)$ since $p^2\ge p^{3/2}$. Squaring proves (7).

Also $|G_{h,N,L}|\le\sum_j2^{-j}<1$, so by (18) and $N<2X$, $|A_{h,N,L}|\le2X+h+4\le3X$ under (5). Let $k=1/(1600p^3)$ and let $\delta$ be the proportion of indices with $|A|\ge\sqrt{k/2}\,X$. The upper envelope gives

$$
kX^2\le\frac1X\sum A^2
\le \frac k2X^2+9\delta X^2,
\quad\text{hence}\quad
\delta\ge\frac k{18}=\frac1{28800p^3}.
$$

This establishes the density corollary. QED.

For each fixed h, the prime p is fixed. Cook's $L_h(X)$ grows logarithmically (since the required $2^L$ is of order X), so $H=L+h=o(X)$, while $E_X=O(\log X)$ and the finite threshold $40p^2\max(E_X,h+4)=O_h(\log X)$. Hence (5) holds at all sufficiently large exact Cook-admissible depths.

## 6. Exact hostility: an unwrapped second moment is not a modular first-harmonic bound

The central boundary is mathematical, not administrative. Equation (7) gives real **unwrapped** squared mass; Cook requires

$$
\boxed{
\mathrm{Re}\sum_{N=X}^{2X-1}
\exp(2\pi iA_{h,N,L})\le\frac9{10}X.
}
\tag{21}
$$

The implication from (7) to (21) is INVALID without new information about distances of $A_{h,N,L}$ from integers. For an explicit generic counterexample, take $A_N=N$ for each integer N. Then $\sum A_N^2\asymp X^3$ and a positive density of arguments are order X, yet $\exp(2\pi i A_N)=1$ **identically**. This counterexample is to the *abstract inference from unwrapped energy*, not to any actual-totient theorem.

The WP09-B exact sliding cocycle constrains the actual modulo-one residues and yields a small unconditional first-harmonic saving, but its single-step $\ell^2$ transfer provably has a ceiling below the required $10\%$ target. The new all-depth arithmetic projection does **not** evade that modular transfer obstruction automatically. It proves a genuine new necessary arithmetic ingredient at the correct growing depth; it does not prove the missing analytic exponential-sum cancellation.

The rational full-series controls of WP07-E further warn against turning finite local congruence or moment information into the original irrationality claim. The workstream remains OPEN.

**Next true target:** a **fixed-prime conditional exponential-characteristic or multi-step modular-cocycle bound** for the *exact actual Cook phases*, able to distinguish large unwrapped winding from near-integer aliasing. A proof that
$\mathrm{Re}\sum_{N\in\mathcal G}w_N(z_N-\bar z_{m_N})\le14X/25$
at arbitrarily late admissible blocks, or the equivalent strong full first-harmonic saving, would supply Cook's missing step. Existing pair correlations, the present projection, and a finite first-harmonic sample do not provide that result.

## 7. Reproducible tests and claim ledger

[full_window_prime_projection.py](full_window_prime_projection.py) implements the exact dyadic alias weights (including the **two residue classes with guaranteed opposite signs**), independent finite-prime CRT reconstruction, and the true full $D_{h,N,L}$ via a direct initialization and **different rolling recurrence**. Its execution certificate checks (5) as an exact **integer** condition and validates (7) with an integer cross-multiplication. It never upgrades finite evidence to an asymptotic Fourier saving.

Tests append to the **existing governed** full-series module [tests/test_erdos249_full_series_phase.py](../../tests/test_erdos249_full_series_phase.py); no extra CI lane, routing, or policy changes. A qualified same-agent adversarial logical review is in [WP09_E_CRITICAL_REVIEW.md](WP09_E_CRITICAL_REVIEW.md).

| Claim | Evidence class |
| --- | --- |
| Uniform arithmetic progression lemma (10) | Complete elementary CRT, divisor counting and Euler product proof |
| Fixed-prime two-residue dyadic separation (14) | Exact dyadic geometric estimate, any depth |
| True full-Cook-window variance (6), cubic unwrapped energy (7), large-winding density (9) | Unconditional arithmetic theorems, exact finite thresholds, actual totient |
| Finite actual $D$ rolling computation and CRT oracle | Bounded executable cross-checks, not independent proof certification |
| Actual exponential first-harmonic tenth-saving (21), weighted Cook cofactor bound, original irrationality | **OPEN** |
| Mathematical priority, separate human review, Lean kernel verification, MATHCERT | **NOT_CLAIMED / NOT_SUBMITTED** |

**Disposition:** WP09-E admits only the new **growing-window unwrapped energy** theorem. Do not mark Erdős #249 proved, certify the manuscript, or close scientific issue #3500.
