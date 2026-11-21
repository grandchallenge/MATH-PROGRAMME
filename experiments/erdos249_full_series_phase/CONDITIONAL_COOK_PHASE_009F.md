# Erdős #249 — WP09-F: fixed-prime conditional modulo-one Cook exponential sums

**Scientific issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Predecessor:** protected WP09-E [PR #3614](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3614), merge ec879c5aafab55c823059c3c06178f1e85219b7f.  
**Primary source lock:** Will Cook, *The Binary Totient Series*, [revision 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*.  
**Scope:** a nonzero **modulo-one** real-part saving for the **actual complete Cook phases conditioned on a fixed prime residue class or pair**, uniformly at the genuine growing least admissible depth. Not Cook's required 10% global saving, not irrationality, not MATHCERT.

## 1. Definitions and exact effective conditions

Fix integers $h,X,L\ge1$, let $Q=2^L$, $s=L+1$, and choose **any fixed prime $p$ not dividing $h$**. In applications use the first such prime. Set

$$
\begin{aligned}
f(n)&=\frac{\varphi(n)}n,\\
d_h(n)&=\varphi(n+h)-\varphi(n),\\
D_N&=D_{h,N,L}=\sum_{j=1}^L2^{L-j}d_h(N+j),\\
E_N&=\exp(2\pi iD_N/Q),\\
E_X^*&=3+\mathrm{bitlength}(3X).
\end{aligned}
\tag{1}
$$

The notation $E_X^*$ is an **integer error majorant**, distinct from the complex phases $E_N$. Assume the following exactly checkable conditions:

$$
\boxed{
s+h\le X,\qquad
X\ge40p^2\max(E_X^*,h+4),\qquad
Q\ge16(2X+h+L+2).
}
\tag{2}
$$

Define two **distinct** residue classes

$$
r_+=-s\bmod p,\qquad r_-=-s-h\bmod p.
\tag{3}
$$

For either $r\in\{r_+,r_-\}$ define the finite source, pair, and single-class sets

$$
\begin{aligned}
S_r&=\{X\le N\le2X-2:N\equiv r\pmod p\},\\
T_r&=\{X\le N\le2X-1:N\equiv r\text{ or }r+1\pmod p\},\\
I_a&=\{X\le N<2X:N\equiv a\pmod p\}.
\end{aligned}
\tag{4}
$$

If $p=2$, $T_r$ is the whole block; otherwise the pair comprises exactly the two indicated residue classes. Both signs below are genuine actual-totient arithmetic, not randomized prime independence.

## 2. Main result: true modulo-one exponential-sum cancellation

**Theorem A (prime-conditional Cook first-harmonic and cocycle saving).** Under (2), for **each** of $r=r_+$ and $r=r_-$ the following hold:

**Arithmetic input, with explicit signs:**

$$
\boxed{
\begin{aligned}
\sum_{\substack{X\le N<2X\\N\equiv r_+\pmod p}}
 d_h(N+s)&\ge\frac{X^2}{2p^2},\\
\sum_{\substack{X\le N<2X\\N\equiv r_-\pmod p}}
 d_h(N+s)&\le-\frac{X^2}{2p^2},\\
\left|\sum_{N\in S_r}d_h(N+s)\right|&\ge\frac{X^2}{4p^2},\\
\sum_{N\in S_r}d_h(N+s)^2&\ge\frac{X^3}{32p^3}.
\end{aligned}}
\tag{5}
$$

**True conditional exponential sum for the actual modular Cook cocycle:**

$$
\boxed{
\mathrm{Re}\sum_{N\in S_r}
 E_{N+1}\overline{E_N}^{\,2}
\le |S_r|-\frac{X^3}{4p^3Q^2}.
}
\tag{6}
$$

**True conditional exponential sum for the original Cook phases themselves:**

$$
\boxed{
\mathrm{Re}\sum_{N\in T_r}E_N
\le |T_r|-\frac{X^3}{20p^3Q^2}.
}
\tag{7}
$$

Consequently, there exists at least one explicitly restricted residue $a\in\{r,r+1\}\bmod p$ such that

$$
\boxed{
\frac1{|I_a|}\mathrm{Re}\sum_{N\in I_a}E_N
\le1-\frac{X^2}{80p^2Q^2}.
}
\tag{8}
$$

The last statement does **not** identify in advance which of the two neighboring classes gives the saving; the pair (7) is unconditional for each indicated $r$.

Unlike WP09-E, (6)–(8) are **modulo-one statements** about exponentials of the actual Cook phases. The original window has *all* $L$ terms, the chosen prime is fixed once h is fixed, and the bounds do not rely on fixed L.

### Cofinal source-locked Cook-depth corollary

Let $L=L_h(X)$ be the **least integer $L\ge h$** satisfying the Cook source-locked size condition in (2). For each fixed h, (2) holds at all sufficiently large X, and $L_h(X)>h$ eventually. At those X the preceding integer-depth minimality implies

$$
32X<Q<32(2X+h+L+1)\le96X.
\tag{9}
$$

Thus, with $p$ fixed depending only on h:

$$
\boxed{
\begin{aligned}
\mathrm{Re}\sum_{N\in S_r}E_{N+1}\overline{E_N}^{\,2}
&\le\left(1-\frac1{73728p^2}\right)|S_r|,\\
\mathrm{Re}\sum_{N\in T_r}E_N
&\le |T_r|-\frac{X}{184320p^3},\\
\exists a\in\{r,r+1\}:\
\mathrm{Re}\sum_{N\in I_a}E_N
&\le\left(1-\frac1{737280p^2}\right)|I_a|.
\end{aligned}}
\tag{10}
$$

The full Cook real first harmonic therefore has the further valid (but **weak**) saving

$$
\mathrm{Re}\sum_{N=X}^{2X-1}E_N
\le\left(1-\frac1{184320p^3}\right)X.
\tag{11}
$$

Equation (11) is **not** claimed to improve the generally stronger global WP09-B variance bound $1-V_h/2500$. The new advance is **arithmetic-progression localization** of an actual modulo-one saving with an explicit fixed prime, not a larger overall deficit.

## 3. Lemma: a weighted extension of WP09-E's genuine totient progression identity

Let $H=s+h\le X$ and $0\le k\le H$, with $s\le H$. Define the exact integer weight

$$
W=\sum_{N=X}^{2X-1}(N+s)
=\frac{X(3X-1)}2+sX.
\tag{12}
$$

Let $\mu_p=\prod_{q\ne p,\ q\ {\rm prime}}(1-q^{-2})>3/5$. The weighted **actual totient ratio** progression satisfies for every residue $r\bmod p$:

$$
\boxed{
\left|
\sum_{\substack{X\le N<2X\\N\equiv r\pmod p}}
 (N+s)f(N+k)
-\frac Wp\mu_p
 \left(1-\frac1p\mathbf1_{\{r+k\equiv0\pmod p\}}\right)
\right|\le5XE_X^*.
}
\tag{13}
$$

**Proof.** The exact Möbius divisor expansion is

$$
f(m)=\sum_{d\mid m}\frac{\mu(d)}d.
$$

For $d\le M=2X+H\le3X$, the two congruences $N\equiv r\pmod p$ and $N+k\equiv0\pmod d$ either have one solution modulo $pd$ when $p\nmid d$, one solution modulo $d$ when $p\mid d$ and the residues are compatible, or none. For any one residue progression modulo any positive integer $m$, the discrepancy of the number of elements in every initial part of $[X,2X)$ from its expected length divided by m has absolute value at most one. Summation by parts against the increasing integer weight $N+s$ yields the **uniform weighted discrepancy**

$$
\left|
\sum_{\substack{X\le N<2X\\N\equiv a\pmod m}}(N+s)
-\frac Wm
\right|\le (2X-1+s)+(X-1)\le4X.
\tag{14}
$$

Multiplying by $\mu(d)/d$ and summing gives an error at most
$4X\sum_{d\le M}1/d\le4X(1+\log M)$.
The main term extended from $d\le M$ to all d has absolute tail at most

$$
W\sum_{d>M}\frac1{d^2}\le W/M\le X.
$$

The remaining Euler factors are **exact** and identical to the WP09-E fixed-prime residue computation; the main term is the displayed factor of W. Finally $E_X^*=3+\mathrm{bitlength}(3X)>1+\log M$, so
$4X(1+\log M)+X\le5XE_X^*$.
This proves (13), with no prime-number theorem, unproved independence, or growth assumption on L beyond H≤X. QED.

## 4. Extract two signed arithmetic sources

Apply (13) with $k=s$ and $k=s+h$. The main terms cancel except for the single p-divisibility contrast. As

$$
d_h(N+s)=(N+s)[f(N+s+h)-f(N+s)]+h f(N+s+h),
\tag{15}
$$

at $r_+$ the p-local contribution to the weighted difference is **positive** and at $r_-$ it is **negative**, with magnitude $\mu_p W/p^2$. Each weighted ratio error is at most $5XE_X^*$; hence their difference has error at most $10XE_X^*$.

For $r_+$, the remainder $h f(N+s+h)$ is nonnegative. Using $W\ge(3X^2-X)/2$, $\mu_p>3/5$, and $10XE_X^*\le X^2/(4p^2)$, we obtain

$$
\sum_{\substack{X\le N<2X\\N\equiv r_+\pmod p}}d_h(N+s)
\ge \frac{9X^2-3X}{10p^2}-\frac{X^2}{4p^2}
\ge\frac{X^2}{2p^2}.
\tag{16}
$$

For $r_-$, the remainder is at most $h(X/p+1)\le2hX/p$ since X≥p, which is at most $X^2/(40p^2)$ by the second threshold in (2). Therefore

$$
\sum_{\substack{X\le N<2X\\N\equiv r_-\pmod p}}d_h(N+s)
\le-\frac{9X^2-3X}{10p^2}
+\frac{X^2}{4p^2}+\frac{X^2}{40p^2}
\le-\frac{X^2}{2p^2}.
\tag{17}
$$

Here the last inequalities use the automatically valid $X\ge3$.

The final index $N=2X-1$ either is not in the chosen class or contributes one term with

$$
|d_h(N+s)|\le N+s+h<3X
\quad\text{(because }s+h\le X\text{)}.
$$

The threshold $X\ge40p^2 E_X^*$ gives $3X\le X^2/(4p^2)$. Removing this possible endpoint gives the truncated first-moment magnitude in (5). Finally $|S_r|\le X/p+1\le2X/p$ and Cauchy–Schwarz imply

$$
\sum_{N\in S_r}d_h(N+s)^2
\ge\frac{(X^2/(4p^2))^2}{2X/p}
=\frac{X^3}{32p^3}.
\tag{18}
$$

This establishes all four arithmetic assertions in (5). QED.

## 5. The exact modulo-one phase transfer

The **full** Cook numerator has the exact integer identity

$$
D_{N+1}-2D_N
=d_h(N+L+1)-Qd_h(N+1).
\tag{19}
$$

Thus the phase cocycle itself obeys

$$
\boxed{
E_{N+1}\overline{E_N}^{\,2}
=\exp\left(2\pi i\,d_h(N+s)/Q\right).
}
\tag{20}
$$

Because $Q\ge16(2X+h+L+2)>32X$ and
$|d_h(N+s)|<3X$, its right-hand side is contained in the centered interval $(-1/2,1/2)$ **before** the exponential. The elementary pointwise inequality

$$
1-\cos(2\pi u)\ge8u^2,\qquad |u|\le1/2
\tag{21}
$$

now gives the direct one-class cocycle saving

$$
\begin{aligned}
|S_r|-\mathrm{Re}\sum_{N\in S_r}E_{N+1}\overline{E_N}^{\,2}
&=\sum_{N\in S_r}\bigl[1-\cos(2\pi d_h(N+s)/Q)\bigr]\\
&\ge\frac8{Q^2}\sum_{N\in S_r}d_h(N+s)^2\\
&\ge\frac{X^3}{4p^3Q^2}.
\end{aligned}
\tag{22}
$$

For the **original Cook phases** (not only their ratio), let $\theta_N\in[-1/2,1/2)$ be the centered fractional representative of $D_N/Q$. By (19) and the fact that $|d_h(N+s)|/Q<1/2$,

$$
\frac{|d_h(N+s)|}{Q}
=\left\|\theta_{N+1}-2\theta_N\right\|_{\mathbb R/\mathbb Z}
\le|\theta_{N+1}-2\theta_N|.
\tag{23}
$$

The elementary two-vector Cauchy–Schwarz inequality is

$$
(\theta_{N+1}-2\theta_N)^2
\le5(\theta_N^2+\theta_{N+1}^2).
\tag{24}
$$

For $N\in S_r$, the indices $N$ and $N+1$ belong to **two different residue classes**, $r$ and $r+1\bmod p$. Furthermore each index appears at most once in the resulting two-class sum. Therefore

$$
\sum_{N\in S_r}d_h(N+s)^2/Q^2
\le5\sum_{N\in T_r}\theta_N^2.
\tag{25}
$$

Apply (21) again to the actual full $E_N=\exp(2\pi i\theta_N)$:

$$
|T_r|-\mathrm{Re}\sum_{N\in T_r}E_N
\ge8\sum_{N\in T_r}\theta_N^2
\ge\frac{8}{5Q^2}\sum_{N\in S_r}d_h(N+s)^2
\ge\frac{X^3}{20p^3Q^2}.
\tag{26}
$$

This proves (6) and (7). Since $T_r=I_r\sqcup I_{r+1}$, one class carries at least half this deficit. As $|I_a|\le2X/p$, dividing by the class size gives (8). Importantly, (23) measures **distance to an integer** and hence cannot suffer the unwrapped-winding failure exposed in WP09-E.

For the least Cook depth $L_h(X)>h$, minimality gives $Q/2<16(2X+h+L+1)$, while $s+h=L+h+1\le X$. Thus $Q<96X$, yielding all three normalized bounds in (10). The full-block bound (11) follows because $1-\mathrm{Re}E_N\ge0$ for all remaining indices. QED.

## 6. Precisely what has and has not been proved

The theorem is a true **conditional exponential-sum bound for the actual full Cook phase** on two explicitly described p-residue classes, and an existential single-class bound. The exact conditional cocycle is itself a one-class exponential sum of a shifted actual totient difference, whose cancellation is quantified without fixed-L assumptions.

However, even the resulting full-block saving $1/(184320p^3)$ falls **far short** of Cook's required $1/10$ saving. It also does **not** give the source-locked first prime/cofactor weighted correlation

$$
\mathrm{Re}\sum_{N\in\mathcal G}w_N(z_N-\bar z_{m_N})\le14X/25,
$$

nor the alternative good-set bound $603X/1000$. These involve strongly overlapping, exponentially weighted phases and cannot be inferred from the finite one-step cocycle transfer. The $5$-norm inequality and restricted source moment intrinsically consume most of the possible gain.

**Independent progress relative to WP09-E:** WP09-E showed substantial *unwrapped* cubic real energy across the full growing window. The present theorem proves actual **modulo-one nonconcentration**, conditional on a fixed prime, at the same genuine Cook depths. This removes the specific *all phases are integers* generic countermodel for this Euler-totient setting but does not preclude rational-comparator countermodels with small yet nonzero phase deficits.

### Source-dependent claim ledger

| Claim | Evidence |
| --- | --- |
| Weighted progression identity (13), explicit constant $5XE_X^*$ | Self-contained exact divisor expansion and uniform Abel-summation error |
| Both signed residue-class shifted-totient first moments (5) | Actual Euler totient, exact finite threshold |
| Single-residue cocycle real-part deficit (6) | Exact full-Cook cocycle and centered cosine bound |
| Two-class and existential one-class **actual Cook phase** deficits (7)–(8) | True modulo-one theorem, not an unwrapped surrogate |
| Cofinal Cook least-depth absolute savings (9)–(11) | Exact minimum-depth inequality; valid for fixed h and large X |
| Cook 10% global saving, 14X/25 weighted cofactor estimate, original series irrationality | **OPEN** |
| Independent human specialist mathematical certification, Lean kernel proof, MATHCERT | **NOT_SUBMITTED** |

## 7. Reproducibility

The exact integer producer and verifier are [conditional_cook_phase.py](conditional_cook_phase.py). It checks signed residue-class arithmetic with integer multiplication, the full unabridged original Cook numerator via the WP09-E rolling recurrence, the modulo-Q cocycle congruence at every tested index, the exact centered-residue transfer, and both real Fourier deficit lower envelopes. The optional complex-trigonometric values are **diagnostics only**; the exact integer and analytic inequalities are the proof checks.

Hostile controls extend the existing governed
[tests/test_erdos249_full_series_phase.py](../../tests/test_erdos249_full_series_phase.py). No new CI lane or route, separate policy modification, authority expansion, or certification is sought. Same-agent logically scoped Axiomatist, Verifier, Adversary and Referee scrutiny is recorded in [WP09_F_CRITICAL_REVIEW.md](WP09_F_CRITICAL_REVIEW.md), with the epistemic limitation explicitly stated.

**Research disposition:** a bounded conditional actual-Cook exponential-sum theorem; issue #3500 and original Erdős #249 remain OPEN, MATHCERT NOT_SUBMITTED. The next substantive objective is **quantitative multistep amplification or Cook's weighted prime/cofactor bound** strong enough to reach 10%, not another unwrapped moment estimate.
