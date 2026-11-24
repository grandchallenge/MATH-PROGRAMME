# Erdős #249 — WP09-K: positive-density Cook-phase word modulus transfer

**Scientific issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500). **Predecessor:** [WP09-J PR #3651](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3651), protected merge 954795c4a7647f93a856cd5515221cf39df9b1e3. **Primary source lock:** Will Cook, *The Binary Totient Series*, revision [3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*.

**Scope:** An effective **complex modulus**, rather than only real-part, Fourier saving for all nontrivial parity-preserving two-unit perturbations of the actual totient. Its character is represented **exactly by a long product of genuine complete Cook phases**. This is not cancellation of the **one-point original Cook first harmonic**, the weighted 14X/25 cofactor estimate, or irrationality. These remain OPEN; MATHCERT NOT_SUBMITTED.

## 1. Explicit class and Cook scale

Let b be integer-valued on positive integers and satisfy

$$
\boxed{
0\le b(j)\le j,\quad
b(j)\equiv\varphi(j)\pmod2,\quad
|b(j)-\varphi(j)|\le2.
}
\tag{1}
$$

Put $\epsilon=b-\varphi$. Fix n≥3 with $|\epsilon(n)|=2$. The protected WP09-I dyadic-rational shadow with K=8 is an instance, at n=21.

Take P positive, divisible by 10. Set

$$
q=\mathrm{lcm}(2,n),\quad E_P=3+\mathrm{bitlength}(2P),\quad
X=nP,\quad
L=\min\{\ell\ge1:2^\ell\ge16(2X+\ell+3)\},\quad Q=2^L.
\tag{2}
$$

Use the explicit cofinal gates

$$
\boxed{
P\ge1000qE_P,\quad
P\ge100(n+1),\quad P\ge L+3,\quad L+2\le X.
}
\tag{3}
$$

All gates hold for sufficiently large P divisible by 10 when n is fixed. Minimality of L gives

$$
\boxed{32X<Q<96X.}
\tag{4}
$$

Define $\mathcal R=\{m:P\le m<2P,\ m\equiv1\pmod n\}$ and $W=|\mathcal R|$; all m are coprime to n.

## 2. Theorem A: two widely separated positive-density totient-ratio classes

Define

$$
\begin{aligned}
\mathcal A&=\{m:P\le m<11P/10,\ m\equiv1\pmod q\},\\
\mathcal B&=\{m:19P/10\le m<2P,\ m\equiv1\pmod q,\
10\varphi(m)\ge7m\}.
\end{aligned}
\tag{5}
$$

The sets are disjoint subsets of $\mathcal R$. Both contain only odd integers, because q is even.

**Theorem A.** Under (3),

$$
\boxed{
|\mathcal A|\ge P/(20q),\quad
|\mathcal B|\ge P/(50q),\quad
|\mathcal A|/W\ge1/80,\quad
|\mathcal B|/W\ge1/200.
}
\tag{6}
$$

**Proof.** Put $T=P/(10q)$. A single residue class of length P/10 has count between T−1 and T+1, so $|\mathcal A|\ge T-1\ge T/2$.

For $\mathcal B_0$ omit the ratio restriction in the second set. The genuine identity

$$
\varphi(m)/m=\sum_{d\mid m}\mu(d)/d
\tag{7}
$$

and the Chinese remainder theorem show that a divisor d coprime to q selects one residue class modulo qd, with count error at most one on the interval of length P/10. If gcd(d,q)>1, there are no solutions. Completing the absolutely convergent Euler product, and bounding the divisor-count errors by $H_{2P}$, gives

$$
\left|
\sum_{m\in\mathcal B_0}\varphi(m)/m-TC_q
\right|
\le H_{2P}+1/(20q)<E_P,
\qquad
C_q=\prod_{p\nmid q}(1-p^{-2}).
\tag{8}
$$

Since 2 divides q,

$$
C_q\ge\prod_{p\ne2}(1-p^{-2})=8/\pi^2>4/5.
\tag{9}
$$

The gate $T\ge100E_P$ implies

$$
F=\sum_{m\in\mathcal B_0}\varphi(m)/m\ge79T/100.
\tag{10}
$$

Also $|\mathcal B_0|\le T+1\le101T/100$. Thus its average totient ratio is at least $79/101>31/40$. If H members have ratio at least 7/10, the fact every ratio lies in [0,1] gives

$$
F\le (7/10)|\mathcal B_0|+(3/10)H.
$$

It follows that $H\ge|\mathcal B_0|/4\ge(T-1)/4\ge T/5$, proving the two count bounds. Finally $W\le P/n+1\le2P/n$ and q≤2n yield the two fraction bounds in (6). No probabilistic independence or prime number theorem was used.

## 3. Theorem B: a universal, phase-invariant complex modulus saving

Define the exact coprime multiplicativity-defect character

$$
\Delta_b(n,m)=b(nm)-b(n)b(m),\qquad
\chi_b(n,m)=\exp(2\pi i\Delta_b(n,m)/Q).
\tag{11}
$$

The genuine totient is multiplicative, hence $\Delta_\varphi(n,m)=0$ and $\chi_\varphi(n,m)=1$ for all m in $\mathcal R$.

**Theorem B.** Under (1)–(4), if $|\epsilon(n)|=2$, then

$$
\boxed{
\left|W^{-1}\sum_{m\in\mathcal R}\chi_b(n,m)\right|
\le1-\frac1{165888000\,n^2}.
}
\tag{12}
$$

This is a **modulus gap**, not just a signed real-part gap, so multiplying every character by the same arbitrary unit phase cannot remove it.

**Proof.** The exact multiplicativity of the true totient gives, whenever $(n,m)=1$,

$$
\Delta_b(n,m)=\epsilon(nm)-\epsilon(n)\varphi(m)-b(n)\epsilon(m).
\tag{13}
$$

Set $s=-\epsilon(n)/2\in\{-1,1\}$. Then

$$
s\Delta_b(n,m)=2\varphi(m)+e_m,\qquad |e_m|\le2(n+1).
\tag{14}
$$

For u in $\mathcal A$, $\varphi(u)\le u<11P/10$. For v in $\mathcal B$, $\varphi(v)\ge7v/10\ge133P/100$. Thus

$$
s\Delta_b(n,v)-s\Delta_b(n,u)
\ge(133/50-11/5)P-4(n+1)
\ge21P/50>P/3.
\tag{15}
$$

All these inequalities hold for arbitrary, even adversarial, placements and signs of every other allowed two-unit correction. On the other hand, for all m in $\mathcal R$,

$$
|\Delta_b(n,m)|\le2\varphi(m)+2(n+1)<201P/50.
\tag{16}
$$

The legal Cook envelope (4) therefore gives, for every u in $\mathcal A$ and v in $\mathcal B$,

$$
\boxed{
1/(288n)
<|\Delta_b(n,v)-\Delta_b(n,u)|/Q
<201/(800n)<1/2.
}
\tag{17}
$$

The phase **difference** lies strictly inside the principal arc; no modular winding is possible. The elementary chord inequality $2\sin(\pi t)\ge4t$ for $0\le t\le1/2$ implies

$$
|\chi_b(n,v)-\chi_b(n,u)|>1/(72n).
\tag{18}
$$

For any W unit complex numbers, there is an exact deterministic identity

$$
1-\left|W^{-1}\sum_j\chi_j\right|^2
=\frac1{2W^2}\sum_{i,j}|\chi_i-\chi_j|^2.
\tag{19}
$$

Keep only the two ordered sets of cross-pairs between $\mathcal A$ and $\mathcal B$. The fraction bounds (6) and chord bound (18) give

$$
1-\left|W^{-1}\sum\chi_b(n,m)\right|^2
\ge\frac1{80\cdot200\cdot72^2n^2}
=\frac1{82944000n^2}.
\tag{20}
$$

Since $1+|\mathrm{mean}|\le2$, the required modulus saving (12) follows. This proof needs no independence between overlapping windows or multiplicative inputs.

## 4. Theorem C: EXACT transport into original, complete Cook-phase words

For the same b, the **literal full original Cook phase** at shift h=1 and depth L is

$$
\boxed{
D^b_{1,N,L}
=\sum_{j=1}^L2^{L-j}[b(N+j+1)-b(N+j)],
\quad
E_N^b=\exp(2\pi iD^b_{1,N,L}/Q).
}
\tag{21}
$$

The original full-numerator sliding recurrence is

$$
D^b_{1,N+1,L}
=2D^b_{1,N,L}
-Q[b(N+2)-b(N+1)]
+[b(N+L+2)-b(N+L+1)].
\tag{22}
$$

Consequently the **genuine full-phase one-step cocycle** is

$$
C_N^b=E_{N+1}^b\,\overline{E_N^b}^{\,2}
=\exp\left(\frac{2\pi i}{Q}[b(N+L+2)-b(N+L+1)]\right).
\tag{23}
$$

For integers u,v≥L+2 define the oriented product

$$
T_b(u,v)=
\begin{cases}
\displaystyle\prod_{j=u}^{v-1}C_{j-L-1}^b,&u<v,\\
1,&u=v,\\
T_b(v,u)^{-1},&u>v.
\end{cases}
\tag{24}
$$

**Exact telescoping:** for every such u,v,

$$
\boxed{
T_b(u,v)=\exp(2\pi i[b(v)-b(u)]/Q).
}
\tag{25}
$$

Fix *any* anchor $m_0\in\mathcal R$. The P≥L+3 gate ensures the source indices of all phase words below are positive. Define

$$
\boxed{
\mathcal W_b(n;m,m_0)=T_b(nm_0,nm)\,T_b(m_0,m)^{-b(n)}.
}
\tag{26}
$$

**Theorem C (genuine full Cook-phase-word transfer).** For every m and $m_0$ in $\mathcal R$,

$$
\boxed{
\mathcal W_b(n;m,m_0)
=\exp\left(\frac{2\pi i}{Q}
[\Delta_b(n,m)-\Delta_b(n,m_0)]\right).
}
\tag{27}
$$

Therefore, for every nontrivial two-unit parity perturbation at n,

$$
\boxed{
\left|W^{-1}\sum_{m\in\mathcal R}\mathcal W_b(n;m,m_0)\right|
\le1-\frac1{165888000\,n^2}.
}
\tag{28}
$$

For the actual totient phi, **every one of these same full Cook-phase words equals exactly one**.

**Proof.** Equation (25) follows by multiplying (23) along an oriented interval; the terminal coefficient differences telescope exactly. Substitute (25) into (26). The numerator of its exponent is

$$
[b(nm)-b(nm_0)]-b(n)[b(m)-b(m_0)]
=\Delta_b(n,m)-\Delta_b(n,m_0).
$$

This proves (27). The anchor contributes an m-independent unit scalar; taking the modulus of the mean removes it and applies Theorem B. No unwrapped surrogate or independent-source approximation is involved.

**Critical limitation:** This result is an exact **LONG, weighted product** of many original complete Cook phases, with indices spanning distances of order nP. It is not Cook's original **one-point** first harmonic, and its modulus saving does not imply cancellation of that first harmonic.

## 5. Theorem D: explicit dyadic-rational shadow versus true totient, now in genuine Cook phases

Protected WP09-I constructed the explicitly dyadic-rational binary coefficient shadow $a_8$ with $0\le\varphi(j)-a_8(j)\le2$ and identical parity. WP09-J independently proved that its first modified coefficient is $a_8(21)=10$, compared with genuine $\varphi(21)=12$, using only the four source values $\varphi(25),\varphi(26),\varphi(27),\varphi(28)$ and a rigorous geometric-tail enclosure.

Set n=21, and choose any sufficiently large P multiple of ten satisfying (3). Then for every anchor $m_0\in\mathcal R$,

$$
\boxed{
\left|W^{-1}\sum_{m\in\mathcal R}
\mathcal W_{a_8}(21;m,m_0)\right|
\le1-\frac1{165888000\cdot21^2},
\qquad
W^{-1}\sum_{m\in\mathcal R}\mathcal W_\varphi(21;m,m_0)=1.
}
\tag{29}
$$

**This separates a genuine rational shadow from the actual Euler totient using only products of Cook's original complete phases.** Yet, as WP09-I proved, every *individual* original shadow Cook phase in any sufficiently late legal block has real part greater than $\cos(\pi/8)>0.9$. A high-order, long-range phase-word Fourier gap can therefore coexist with complete failure of Cook's 10% **one-point** criterion in the rational comparator.

## 6. Reproducibility and next exact obligation

The companion source [cook_phase_word_modulus.py](cook_phase_word_modulus.py) implements the explicit gates and rational constants, plus the **actual original full Cook numerator and its rolling/direct-replay checks**. For finite samples it verifies the oriented product against direct integer multiplicative-defect differences (actual phi, both admissible signs of a one-flip comparator, and the explicit WP09-I K=8 rational shadow). It also verifies the true two-range CRT population counts and signed-gap inequality using an exact Euler-totient sieve. Any floating complex-mean diagnostic is explicitly labelled *noncertifying* and uses a one-flip comparator, not the rational shadow's enormous-index digits.

The review [WP09_K_CRITICAL_REVIEW.md](WP09_K_CRITICAL_REVIEW.md) records distinct same-agent Axiomatist, Verifier, Adversary and Referee logical passes. It is not independently authenticated mathematical review or a Lean kernel proof.

| Obligation | Disposition |
| --- | --- |
| Two positive-density, signed-separated true totient-ratio populations with effective CRT gates | **PROVED** |
| Complex modulus Fourier gap for all two-unit parity perturbations | **PROVED** |
| Exact genuine full Cook-phase *long-word* realization and modulus transfer | **PROVED** |
| Quantitative high-order separation of original phi and the WP09-I rational shadow | **PROVED** |
| Original one-point 10% Cook real phase and source-locked 14X/25 cofactor-weighted correlation | **OPEN** |
| Original Erdős #249 irrationality, independent certification and MATHCERT | **OPEN / NOT_SUBMITTED** |

**Next mathematical boundary:** Extract a **one-point original Cook-phase** estimate, or the exact Cook good-set cofactor-weighted bound, from the nontrivial long-range phase-word correlation. A valid argument must quantitatively control the dependencies across overlapping windows. The present exact transfer does not provide that missing decorrelation estimate.
