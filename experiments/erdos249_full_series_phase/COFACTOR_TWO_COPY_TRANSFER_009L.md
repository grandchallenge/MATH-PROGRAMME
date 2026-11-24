# Erdős #249 — WP09-L: cofactor two-copy transfer and certified actual-totient specimens

**Scientific issue:** [#3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500). **Protected predecessor:** [WP09-K PR #3678](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3678), merge 9ca7784599521f71c9befa4c0c49361f5e732eb9. **Primary source:** Will Cook, *The Binary Totient Series*, [revision 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*.

**Claim class:** An exact sufficient two-copy correlation inequality for Cook's original unresolved 14X/25 weighted good-set first bound; an explicit cofinal no-go for arguments using only unweighted cofactor phase means; rigorous finite certificates for the **actual original Euler-totient Cook phases**, using rational root-of-unity enclosures. The cofinal s=26 first bound, full all-h Cook tenth-saving and original Erdős #249 irrationality remain **OPEN**; MATHCERT NOT_SUBMITTED.

## 1. Source-exact setup

Fix source-legal integers h,s,L,X with L≥s+h, Q=2^L≥16(2X+h+L+2), and t=L-s+1. The **actual** Cook phase is

$$
E_N=\exp(2\pi iD_N/Q),\qquad
D_N=\sum_{j=1}^L2^{L-j}[\varphi(N+h+j)-\varphi(N+j)].
\tag{1}
$$

For N in [X,2X), write N+t=m_Np_N where p_N is its largest prime factor. Cook's exact source classes, with 0<eta<1, are

$$
\begin{aligned}
\mathcal A&=\{N:m_N\le\lfloor\sqrt X/2\rfloor,\
p_N>2\lfloor\sqrt X\rfloor\},\\
\mathcal G&=\{N\in\mathcal A:\varphi(m_N)\ge\eta m_N\}.
\end{aligned}
\tag{2}
$$

On A, p_N>m_N, so phi(N+t)=phi(m_N)(p_N-1). Cook isolates the exact factor

$$
z_N=\exp\left(
2\pi i\,(2^h-1)\varphi(m_N)(p_N-1)/2^t
\right),\qquad w_N=E_N/z_N.
\tag{3}
$$

Write G_m={N in G:m_N=m}, g_m=|G_m|, and G=|G|=sum g_m. Since the good condition depends **only on m**, every retained G_m equals the **complete** source A cofactor group, so its z-mean is precisely Cook's source z-bar. Define

$$
Z_m=\sum_{N\in G_m}z_N,\qquad
W_m=\sum_{N\in G_m}w_N,\qquad
A_m=\sum_{N\in G_m}E_N,
\qquad
Z_1=\sum_m|Z_m|.
\tag{4}
$$

The missing source-locked term is

$$
\boxed{
\mathrm{Re}\,S\le14X/25,\qquad
S=\sum_{N\in\mathcal G}w_N(z_N-Z_{m_N}/g_{m_N}).
}
\tag{5}
$$

At **canonical** s=26, eta=1/1000, and the least admissible depth, Cook's pinned manuscript gives, on sufficiently large blocks, the other three needed estimates. Its group-mean result supplies $Z_1\le X/100$, while its count gives G>67X/100. Both are source inputs, **not new WP09-L results**.

## 2. Theorem A: cofactor two-copy transfer

Define the exact original full-Cook within-cofactor two-copy energy

$$
\boxed{
C_E=\sum_{m:g_m>0}\frac{|A_m|^2}{g_m}
=\sum_m\frac1{g_m}\sum_{N,M\in G_m}
\exp\left(2\pi i(D_N-D_M)/Q\right).
}
\tag{6}
$$

The second expression is real and nonnegative as it is the exact square of the cofactor-group phase sum.

**Theorem A (sufficient weighted-to-two-copy transfer).** For any source-legal X,h,s,L,eta and the actual source-defined phases,

$$
\boxed{
|S|\le\sqrt{G C_E}+Z_1.
}
\tag{7}
$$

Consequently, if G>0, $Z_1<14X/25$, and

$$
\boxed{
G C_E\le(14X/25-Z_1)^2,
}
\tag{8}
$$

then Cook's unresolved first real weighted bound (5) follows. In the canonical source setting, the stronger **cofinal mathematical obligation**

$$
\boxed{
C_E\le\frac{(11X/20)^2}{G}
}
\tag{9}
$$

would suffice, because Cook's source gives $Z_1\le X/100$ on all sufficiently large X. This cofinal inequality is **not proved here**.

**Proof.** Using the complete G_m groups and the definition of z-bar,

$$
\boxed{
S=\sum_m\left(A_m-\frac{W_m Z_m}{g_m}\right).
}
\tag{10}
$$

Since each |w_N|=1, $|W_m|\le g_m$, hence
$|S|\le\sum_m|A_m|+\sum_m|Z_m|$.
The groupwise Cauchy–Schwarz inequality yields

$$
\sum_m|A_m|
\le\sqrt{\left(\sum_mg_m\right)
\left(\sum_m|A_m|^2/g_m\right)}
=\sqrt{G C_E}.
$$

This proves (7)–(9). The theorem makes **no** independence assumption about the overlapping totient source terms in w.

## 3. Theorem B: equivalent prime-pair phase-spread target

Define the genuine two-copy phase-spread energy

$$
\boxed{
V_E=\sum_m\frac1{2g_m}\sum_{N,M\in G_m}|E_N-E_M|^2.
}
\tag{11}
$$

Expanding squared chords exactly gives

$$
\boxed{V_E=G-C_E.}
\tag{12}
$$

Thus (8) is **equivalent** to

$$
\boxed{
V_E\ge G-(14X/25-Z_1)^2/G.
}
\tag{13}
$$

In the canonical large-X source setting the stronger sufficient target is

$$
\boxed{
V_E\ge G-(11X/20)^2/G.
}
\tag{14}
$$

At representative occupancy G=67X/100, this asks for a phase-spread energy of approximately 0.2185 X. It is a **concrete arithmetic prime-pair correlation** on actual original complete Cook phases whose prime factors share cofactor m, rather than the much longer WP09-K multiplicative-defect words.

The usual residual-weight Cauchy bound is different. Let

$$
C_W=\sum_m|W_m|^2/g_m,\quad C_Z=\sum_m|Z_m|^2/g_m.
$$

Centering both factors within each good group gives the exact identity and bound

$$
S=\sum_m\sum_{N\in G_m}(w_N-\bar w_m)(z_N-\bar z_m),
\qquad
\boxed{|S|\le\sqrt{(G-C_W)(G-C_Z)}.}
\tag{15}
$$

The new criterion (8) controls the **actual product E=wz**, not the separate dispersions of w and z. It can certify (5) even when (15) is numerically too weak.

## 4. Theorem C: unweighted cofactor means alone are provably insufficient

Take arbitrary admissible unit-modulus residual weights

$$
\boxed{w_N^{\mathrm{adv}}=\overline{z_N}.}
\tag{16}
$$

These weights are **not** claimed to equal the actual other-totient contribution. But they are valid adversarial witnesses against a source-mean-only inference. In fact E_N^{adv}=1 for every good index and, exactly,

$$
\boxed{
S^{adv}=\sum_mg_m(1-|\bar z_m|^2)=G-C_Z.
}
\tag{17}
$$

Because $|\bar z_m|\le1$, $C_Z\le Z_1$. Therefore Cook's own source-stated cofinal bounds G>67X/100 and $Z_1\le X/100$ imply

$$
\boxed{
S^{adv}>66X/100>14X/25.
}
\tag{18}
$$

Meanwhile the source second term for these adversarial weights is
$\sum_m g_m|\bar z_m|^2=C_Z\le X/100$.

**Theorem C (quantitative information boundary).** The actual source's cofactor counts, unweighted prime-phase group means and small second-term estimate cannot imply its first bound for arbitrary unit-modulus residual weights. There is a rigorous **one-tenth-of-X gap**. A genuine proof must exploit the actual arithmetic *joint* behavior of w and z, or the equivalent original-Cook prime-pair energy in Theorem B. This is a logical no-go, not a counterexample for the genuine Euler totient.

## 5. Theorem D: finite actual-totient certificates with exact rational root enclosures

The source file [cofactor_two_copy_transfer.py](cofactor_two_copy_transfer.py) computes actual phi, largest prime factors, and **exact** original full D numerators using the original sliding recurrence plus three independent direct-oracle checks. The genuine source z-factor is embedded in the **same** Cook modulus:

$$
Z_N\equiv(2^h-1)\varphi(m_N)(p_N-1)2^{s-1}\pmod{Q},
\quad z_N=e^{2\pi i Z_N/Q},\quad w_N=e^{2\pi i(D_N-Z_N)/Q}.
\tag{19}
$$

No floating trigonometry is used for certification. Every real and imaginary root component is computed as a scaled **integer** with a proven error less than 32/10^15. Here is the complete error budget:

1. Machin's exact identity for pi, $\pi=16\arctan(1/5)-4\arctan(1/239)$, with 50 alternating rational terms and signed next-term remainders gives exact rational pi bounds. These certify $\lfloor10^{15}\pi\rfloor=3141592653589793$ and $\pi<22/7$.
2. Centering r modulo Q, then taking the integer floor of $2r\lfloor10^{15}\pi\rfloor/Q$ changes the true scaled angle by fewer than **two** integer units.
3. Thirteen integer Taylor recurrence terms give each cosine or sine an accumulated rounding error at most **25** units. The remaining terms are bounded by $(22/7)^{28}/28!<10^{-15}$ and $(22/7)^{29}/29!<10^{-15}$, respectively.
4. Consequently each root component has absolute error below $\varepsilon=32/10^{15}$. All group energy errors are propagated deterministically: $|C_E-C_E^{fixed}|\le8G\varepsilon$, and $|\mathrm{Re}S-\mathrm{Re}S^{fixed}|\le10G\varepsilon$. The source group absolute sum Z1 is upper-enclosed via exact integer square roots plus $2G\varepsilon$.

All success/failure flags therefore follow from **exact rational inequalities**, not numerical tolerance or a floating model.

### Source-exact finite example

Authenticated CHAD read-only exact replay: capture 1a5cd638d5cb4cf69dee44253949d003; exact-outward-interval follow-up 06997094e74245029d873be58c730e72. At X=16384, h=1, eta=1/1000, L=20, the certified (outward-rounded four-decimal) intervals are:

| Quantity normalized by X | s=8 | s=12 |
| --- | --- | --- |
| Isolated index t | 13 | 9 |
| Good indices and distinct cofactor groups | 9525; 64 | 9526; 64 |
| Full original Cook real first harmonic | [0.0071,0.0072] | [0.0071,0.0072] |
| Source missing weighted first term Re S | [0.0006,0.0007] | [0.0043,0.0044] |
| Absolute source group mean Z1 | [0.0746,0.0747] | [0.0292,0.0293] |
| True cofactor two-copy energy C_E | [0.0033,0.0034] | [0.0033,0.0034] |
| Adversarial weight first term, G-C_Z | [0.5606,0.5607] | [0.5790,0.5791] |
| Exact two-copy sufficient gate (8) | **PASS** | **PASS** |
| Generic separate-weight Cauchy gate (15) | **INSUFFICIENT** | **INSUFFICIENT** |

Both finite weighted first terms are **rigorously below 14X/25**, and both finite true original first harmonics are **rigorously below 9X/10**, for these exact parameters. The separate-weight Cauchy estimate, even with exact root enclosures, is larger than 14X/25, while the new two-copy gate succeeds.

**Essential scientific limitation:** s=8 or 12 at X=16384 is **not** the canonical cofinal s=26 regime. Neither G>0.67X nor Z1≤0.01X is true in these specimens, and the other three source-locked canonical Cook estimates are NOT asserted. A single finite h=1 block cannot prove arbitrarily late blocks for every fixed shift. No irrationality claim is made.

## 6. Next actual proof obligation

Prove, for every fixed shift h on arbitrarily late canonical s=26, eta=1/1000 Cook-legal blocks, the true arithmetic cofactor-group two-copy estimate

$$
\boxed{
\sum_{m:g_m>0}\frac1{g_m}
\left|\sum_{N\in G_m}
\exp(2\pi iD^\varphi_{h,N,L}/2^L)
\right|^2
\le\frac{(11X/20)^2}{G}.
}
\tag{20}
$$

Equivalently prove the actual **cofactor-sharing prime-pair phase-spread** inequality (14). By Theorem A and Cook's other three source-established estimates, that would imply the original full 10% first harmonic on the required cofinal blocks. It is now the precisely isolated **source-sensitive two-copy arithmetic frontier**, not a claim of its proof. Original Erdős #249 remains OPEN; no MATHCERT.
