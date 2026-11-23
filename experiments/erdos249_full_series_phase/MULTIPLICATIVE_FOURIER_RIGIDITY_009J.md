# Erdős #249 — WP09-J: positive-density multiplicative Fourier rigidity at Cook scale

**Scientific issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Predecessor:** protected [WP09-I PR #3649](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3649), merge 4f0c20e2b0b901687bb9a6627b0ac502b28341a8.  
**Cook primary source lock:** [revision 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*.  
**Claim:** Effective positive-density **real Fourier** bound for a coprime **multiplicativity-defect character**, rather than Cook's **original full overlapping phase**. Original 10% first-harmonic, weighted 14X/25 good-set cofactor correlation, and Erdős #249 irrationality remain OPEN. MATHCERT NOT_SUBMITTED.

## 1. Inputs and explicit arithmetic scale

Let b be an integer-valued coefficient sequence with, for all j≥1,

$$
\boxed{
0\le b(j)\le j,\quad b(j)\equiv\varphi(j)\pmod2,\quad
|b(j)-\varphi(j)|\le2.
}
\tag{1}
$$

This class contains the genuine totient and WP09-I's explicitly dyadic-rational shadow. Put $\epsilon=b-\varphi\in\{-2,0,2\}$. If b differs from phi, then some **fixed n≥3** has $|\epsilon(n)|=2$: the envelope and parity force equality at j=1,2.

For a positive integer P, define

$$
X=nP,\qquad E_P=3+\operatorname{bitlength}(2P),
\qquad
\mathcal R=\{P\le m<2P:m\equiv1\pmod n\}.
\tag{2}
$$

Let L be the **least** legal Cook depth for h=1:

$$
Q=2^L\ge16(2X+L+3).
\tag{3}
$$

Impose the explicit effective gates

$$
\boxed{
P\ge32nE_P,\qquad P\ge32(n+3),\qquad L+2\le X.
}
\tag{4}
$$

Every fixed n satisfies these for all sufficiently large P. Minimality of L gives
$2^{L-1}<16(2X+L+2)$, hence

$$
\boxed{32X<Q<96X.}
\tag{5}
$$

All m in $\mathcal R$ are coprime to n. Define the exact multiplicative defect

$$
\Delta_b(n,m)=b(nm)-b(n)b(m).
\tag{6}
$$

For the **actual** phi, $\Delta_\varphi(n,m)=0$ identically. The new real Fourier detector of bounded deviations is

$$
\mathcal D_b(n,P)
=\sum_{m\in\mathcal R}
\left[1-\cos(2\pi\Delta_b(n,m)/Q)\right].
\tag{7}
$$

## 2. Theorem A: a positive-density CRT/Euler-product progression

**Theorem A.** Under $P\ge32nE_P$, define
$\mathcal H=\{m\in\mathcal R:\varphi(m)\ge m/3\}$. Then

$$
\boxed{|\mathcal R|\ge P/n-1,\qquad|\mathcal H|\ge P/(5n).}
\tag{8}
$$

**Proof.** The exact true totient ratio identity is
$f(m)=\varphi(m)/m=\sum_{d\mid m}\mu(d)/d$. Put

$$
C_n=\sum_{\substack{d\ge1\\(d,n)=1}}\frac{\mu(d)}{d^2}
=\prod_{p\nmid n}(1-p^{-2})
\ge6/\pi^2>3/5,
\tag{9}
$$

where the last strict inequality follows from $\pi^2<10$.

For each d≤2P coprime to n, the congruences m≡1 modulo n and m≡0 modulo d choose exactly one class modulo nd. The number of its members in the half-open interval [P,2P) differs from P/(nd) by at most one. If gcd(d,n)>1, there are no solutions. Thus, by exact Möbius inversion and the CRT,

$$
\left|
\sum_{m\in\mathcal R}\frac{\varphi(m)}m
-\frac Pn C_n
\right|
\le\sum_{d\le2P}\frac1d
+\frac Pn\sum_{d>2P}\frac1{d^2}
<2+\log(2P)<E_P.
\tag{10}
$$

This is a deterministic progression counting estimate; it uses no prime number theorem and no independence assumption.

Since $P/n\ge32E_P$,

$$
F=\sum_{m\in\mathcal R}f(m)
\ge(3/5-1/32)P/n
=\frac{91}{160}P/n.
\tag{11}
$$

Let W denote $|\mathcal R|$. Counting one congruence class gives
$P/n-1\le W\le P/n+1\le(33/32)P/n$, hence

$$
\frac FW\ge\frac{91}{165}>\frac12.
\tag{12}
$$

If H is the count of $f(m)\ge1/3$ inside $\mathcal R$, then
$F\le H+(W-H)/3=W/3+2H/3$, so H≥W/4. As P/n≥32, $W/4\ge(P/n-1)/4\ge P/(5n)$. QED.

## 3. Theorem B: uniform positive-density real Fourier separation

**Theorem B (effective Fourier rigidity).** Under (1)–(4), if
$|\epsilon(n)|=2$, then

$$
\boxed{
\mathcal D_b(n,P)
\ge\frac P{23040\,n^3}.
}
\tag{13}
$$

Equivalently, the real exponential sum of **actual integer multiplicative defects** satisfies

$$
\boxed{
\operatorname{Re}\sum_{m\in\mathcal R}
\exp(2\pi i\Delta_b(n,m)/Q)
\le|\mathcal R|-\frac P{23040n^3}.
}
\tag{14}
$$

There is also the **uniform normalized real saving**

$$
\boxed{
\frac1{|\mathcal R|}
\operatorname{Re}\sum_{m\in\mathcal R}
\exp(2\pi i\Delta_b(n,m)/Q)
\le1-\frac1{24000n^2}.
}
\tag{15}
$$

For true phi, the corresponding normalized Fourier mean is **exactly 1**.

**Proof.** Write $\epsilon=b-\varphi$. On the coprime progression,

$$
\begin{aligned}
\Delta_b(n,m)
&=\epsilon(nm)-\epsilon(n)\varphi(m)-b(n)\epsilon(m).
\end{aligned}
\tag{16}
$$

At the chosen n, $|\epsilon(n)|=2$; globally $|\epsilon|\le2$ and $0\le b(n)\le n$. Therefore

$$
2\varphi(m)-2(n+1)
\le|\Delta_b(n,m)|
\le2\varphi(m)+2(n+1).
\tag{17}
$$

For m in $\mathcal H$, $\varphi(m)\ge m/3$ and $m\ge P\ge32(n+3)$, giving

$$
\boxed{\frac m2\le|\Delta_b(n,m)|\le3m.}
\tag{18}
$$

With P≤m<2P and $32nP<Q<96nP$,

$$
\boxed{
\frac1{192n}<\frac{|\Delta_b(n,m)|}Q
<\frac{3}{16n}\le\frac1{16}.
}
\tag{19}
$$

The scaled multiplicative defect lies inside the central unit-circle arc; there is **no possible integer winding**. The elementary inequality

$$
1-\cos(2\pi t)\ge8t^2\quad(|t|\le1/2)
\tag{20}
$$

implies for each good m a real deficit at least $1/(4608n^2)$. Theorem A gives at least P/(5n) such m; every other contribution to $\mathcal D_b$ is nonnegative. Hence (13) and (14) follow.

Finally $|\mathcal R|\le(33/32)P/n$, giving

$$
\frac{\mathcal D_b(n,P)}{|\mathcal R|}
\ge\frac1{23760n^2}>\frac1{24000n^2}.
\tag{21}
$$

This proves (15). The result is uniform over **all placements and both signs** of every other admissible two-unit correction. QED.

## 4. Theorem C: a quantitative asymptotic Fourier characterization of phi

Let $\mathscr B_2$ denote precisely the class (1). For fixed n≥3 let

$$
\mathcal F_b(n,P)=
\frac1{|\mathcal R|}
\operatorname{Re}\sum_{m\in\mathcal R}
\exp\left(
\frac{2\pi i[b(nm)-b(n)b(m)]}{2^{L_1(nP)}}
\right).
\tag{22}
$$

**Theorem C.** For b in $\mathscr B_2$ the following are equivalent:

1. b equals genuine Euler totient at every integer.
2. For every fixed n≥3, $\mathcal F_b(n,P)$ tends to 1 as P tends to infinity through integers.
3. For every fixed n≥3, $\limsup_{P\to\infty}\mathcal F_b(n,P)=1$.

**Proof.** If b=phi, the defect is zero for every coprime pair, hence all means are identically 1. Conversely, if b differs at some n, parity and the envelope force n≥3 and $|\epsilon(n)|=2$. By Theorem B, for all sufficiently large P,

$$
\limsup_{P\to\infty}\mathcal F_b(n,P)
\le1-\frac1{24000n^2}<1,
\tag{23}
$$

contradicting statement 3. Therefore all three are equivalent.

This shows the positive-density Fourier detector is strong enough to recover **exact multiplicativity and coefficients** within the parity-compatible two-unit neighborhood, despite being an averaged rather than pointwise test.

## 5. Theorem D: the protected rational shadow is detected explicitly at n=21

WP09-I defines the exact dyadic-rational K=8 shadow by

$$
\gamma_8=\sum_{j=1}^{24}\varphi(j)/2^j
=\frac{5736255}{4194304},\qquad
\delta_8=\sum_{j>24}\varphi(j)/2^j>0,
\tag{24}
$$

and takes the canonical binary digits of $x_8=2^7\delta_8$.
We can identify the **first modified coefficient** using just four genuine totient values:

$$
\varphi(25)=20,\ \varphi(26)=12,\quad
\varphi(27)=18,\ \varphi(28)=12.
\tag{25}
$$

The exact finite contribution is

$$
2^{20}\sum_{j=25}^{28}\frac{\varphi(j)}{2^j}
=\frac{20}{32}+\frac{12}{64}
+\frac{18}{128}+\frac{12}{256}=1.
\tag{26}
$$

The remaining positive tail satisfies

$$
0<2^{20}\sum_{j>28}\frac{\varphi(j)}{2^j}
\le2^{20}\sum_{j>28}\frac j{2^j}
=\frac{30}{256}=\frac{15}{128}.
\tag{27}
$$

Therefore

$$
\boxed{
1<2^{20}\delta_8<\frac{143}{128}<2.
}
\tag{28}
$$

Since $2^{13}x_8=2^{20}\delta_8$, the canonical binary digits satisfy

$$
\boxed{
b_1=\cdots=b_{12}=0,\qquad b_{13}=1,\qquad
a_8(21)=\varphi(21)-2=10.
}
\tag{29}
$$

So **n=21** is an exact nonzero correction of the specific protected WP09-I rational shadow, requiring no oracle for the unknown irrationality status of the original series. Theorems B–C yield for every large P passing (4):

$$
\boxed{
\mathcal F_{a_8}(21,P)\le
1-\frac1{24000\cdot21^2},
\qquad
\mathcal F_\varphi(21,P)=1.
}
\tag{30}
$$

The K=8 shadow nevertheless has every sufficiently late **original complete Cook phase** of real part >0.9, by WP09-I. This is an explicit **positive-density, high-frequency arithmetic-Fourier discriminator** that the previous single-prime and short-time cocycle statistics lacked.

## 6. Reproducibility and preserved epistemic boundary

The source [multiplicative_fourier_rigidity.py](multiplicative_fourier_rigidity.py) computes the exact four-totient first-modification certificate, returns only **integer gates and exact rational** theorem constants, and checks the full positive-density arithmetic count on an actual totient sieve. It tests a worst-case algebraic defect interval for **all** admissible two-unit corrections, without pretending to compute the enormous-index canonical shadow bits.

Its optional finite cosine diagnostic uses a **one-flip coefficient comparator**, not WP09-I's rational shadow; the theorem itself is analytic and holds uniformly for the actual rational shadow. The registered tests append to the existing [tests/test_erdos249_full_series_phase.py](../../tests/test_erdos249_full_series_phase.py); same-agent logical adversarial checks are in [WP09_J_CRITICAL_REVIEW.md](WP09_J_CRITICAL_REVIEW.md).

For the explicit n=21, P=20000, $X=420000$, the least Cook depth is L=24, $Q=16777216$, and the progression has exactly 952 multipliers, all 952 satisfying $\varphi(m)\ge m/3$ in that particular finite instance. This is a **finite exact-integer sample**, not the proof of the cofinal theorem.

**Remaining boundary:** The observable $\mathcal F_b$ is a **multiplicative-defect character**. It is not Cook's original phase
$\exp(2\pi iD^\varphi_{h,N,L}/Q)$ or Cook's good-set cofactor-weighted sum. The actual $\varphi$ has zero defect, whereas the rational shadow has positive-density Fourier defect. To prove irrationality one still needs a quantitative transfer from **exact coprime factorization and two-adic carries** to the **overlapping full-window weights** in Cook's source-locked $14X/25$ estimate, or another genuinely sufficient original-phase inequality.

No Lean kernel certification, independently authenticated specialist review, theorem-priority claim, or MATHCERT. Original Erdős #249 OPEN; #3500 OPEN.
