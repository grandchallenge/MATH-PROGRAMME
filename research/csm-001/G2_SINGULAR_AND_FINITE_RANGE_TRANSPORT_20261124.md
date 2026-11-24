# CSM-G2-WP09 — singular domination obstruction and finite-range block transport

**Status:** internally proved refutation and constructive sufficient theorems. Originality UNADJUDICATED; no MATHCERT, independent mathematical certification or claim promotion. Continues WP07 and WP08. The general unrestricted closure proposition is false; the conditional transport proposition below is proved.

## 1. Singular spectral separation alone is not sufficient

Consider the stationary two-dimensional nonnegative transfer family on three symbols:

$$
A=\begin{pmatrix}1/2&0\\0&1/4\end{pmatrix},\qquad
B=\begin{pmatrix}0&0\\0&1/4\end{pmatrix},\qquad
C=\begin{pmatrix}1/4&1/4\\1/4&1/4\end{pmatrix}.
$$

Their sum is positive stochastic with stationary row $\pi=(1/2,1/2)$. Every word has positive mass because its second diagonal entry is positive. The actual-word row and column spans each contain two independent vectors, for example the empty-word vectors and the vectors for $A$. Thus the realization is minimal, not a reducible nonobservable padding.

Every word containing $B$ or $C$ has rank one; the all-$A$ word of length $n$ has singular ratio $2^{-n}$. The WP07 uniform spectral-gap condition therefore holds for **every** word, with constants 1 and 1/2, despite singular generators. But

$$
p(B\mid A^n)=\frac{p(BA^n)}{p(A^n)}
=\frac{1}{4(2^n+1)}.
$$

This tends to zero and the lower quasi-Bernoulli concatenation ratio is $2/(2^n+1)$, also tending to zero. There is no uniform positive reverse conditional version.

There is a stronger, two-sided obstruction. Condition on $n$ copies of $A$ on each side of the central site, with a $B$ at both exterior endpoints. The probabilities of the central symbols $(A,B,C)$ are exactly $(1/3,1/3,1/3)$ for every $n$. Replace both endpoint symbols with $C$. Write $t=2^{-n}$; the central probability vector is the normalization of

$$
\left(\frac12+\frac14t^2,\ \frac14t^2,\ \frac14(1+t)^2\right),
$$

and tends to $(2/3,0,1/3)$. All these conditioning cylinders have positive mass. They converge to the same all-$A$ exterior, so a continuous two-sided conditional would force their conditional averages to have the same limit. This contradiction rules out quasilocality itself. It does not depend on a choice of a version on a measure-zero exterior.

**Disposition:** the spectral-only implication for singular minimal generators is REFUTED. The example is an elementary explicit probability-model obstruction, consistent with the established need for extra nondegeneracy in semi-invertible dominated splitting. No novelty of the general obstruction mechanism is claimed.

## 2. Corrected singular criterion using one-symbol non-nullness

Assume a stationary full-support finite-state observed process as in WP07, with a minimal linear representation $p(w)=\ell M_w r$ of dimension $d$. Suppose

$$
\frac{\sigma_2(M_w)}{\sigma_1(M_w)}
\le K\gamma^{|w|},\qquad 0<\gamma<1.
$$

In dimension one take the ratio to be zero. No generator is required to be invertible. Impose uniform two-direction **one-symbol** non-nullness: some $c>0$ satisfies

$$
p(aw)\ge c p(w),\qquad p(wa)\ge c p(w)
\tag{1}
$$

for every symbol $a$ and every word $w$.

**Theorem.** The gap and (1) together are equivalent to the existence of a strictly positive reverse conditional function with exponentially decaying logarithmic variations. They imply WP07's quasi-Bernoulli lower bound, uniform relative factorization and exponentially summable two-sided Gibbs interaction.

**Proof.** Necessity follows from WP07: positive exponential logarithmic variations imply the quasi-Bernoulli lower bound and exponential normalized exterior-square decay in the minimal representation. The concatenation lower bound implies (1), with $c=b\min_a p(a)$.

For sufficiency, WP07 proves the uniform comparison $\|M_w\|_2\le Jp(w)$ using fixed actual-word bases, independently of invertibility or the quasi-Bernoulli bound. Thus

$$
\|\bigwedge^2 M_w\|_2\le J^2K\gamma^{|w|}p(w)^2.
$$

For $q(a\mid w)=p(aw)/p(w)$, the change when a letter $z$ is appended is

$$
q(a\mid wz)-q(a\mid w)
=\frac{p(awz)p(w)-p(aw)p(wz)}{p(w)p(wz)}.
$$

The numerator is the exterior pairing of the fixed row $\ell M_a\wedge\ell$, the matrix $\bigwedge^2 M_w$ and the fixed column $M_zr\wedge r$. Their norms, other than the word matrix, are bounded uniformly over the finite alphabet. The second inequality in (1) bounds the denominator below by $c p(w)^2$. Consequently each one-letter extension changes the conditional by at most $D\gamma^{|w|}$ for a finite $D$ independent of letters and words. Summing the geometric tail over any number of appended symbols gives uniform Cauchy convergence and exponential variation. The first inequality in (1) supplies the positive lower bound $c$ for all these probabilities and their limits. The logarithm is Lipschitz on $[c,1]$. Martingale convergence identifies the limit with the reverse conditional. WP07 then supplies quasi-Bernoulli and the explicit two-sided interaction. QED.

The hypothesis (1) still quantifies over all words. It has simple finite sufficient witnesses in the original nonnegative realization: the componentwise inequalities $T_a\mathbf1\ge c\mathbf1$ and $\pi T_a\ge c\pi$ for all letters. No necessity of these particular entrywise tests is claimed. This separates the singular repair from the stronger global concatenation hypothesis used in WP07; it does not assert a universal finite decision algorithm.

## 3. Exact history lift for arbitrary finite-range kernels

Let the source have transfers $T_a$, stationary row $\pi$, and alphabet $I$. Fix a memory length $r\ge1$. A stochastic finite-range readout is specified by $H(z\mid ha)$ on windows consisting of a history $h\in I^r$ and a new letter $a\in I$, with independent randomization at each output site conditional on the complete source. Finite anticipation can be converted to this convention by a fixed index shift of the stationary output law.

The lifted states are pairs $(h,i)$ of the recent input history and the current source hidden state. The labelled transfer for output $z$ has entries

$$
S_z((h,i),(k,j))
=\sum_{a:\,\mathrm{shift}(ha)=k}T_a(i,j)H(z\mid ha).
\tag{2}
$$

The stationary row is $\widehat\pi(h,i)=(\pi T_h)_i$. Its sum is one. Direct summation over old histories and letters proves $\widehat\pi\sum_z S_z=\widehat\pi$, using $\pi Q=\pi$. Drop precisely the zero-mass states: stationarity of nonnegative transfers implies no transition from a positive-mass state into a zero-mass state. The remaining unlabelled transfer $\widehat Q=\sum_z S_z$ is stochastic. It and the retained state set are independent of the chosen stochastic kernel.

Expanding a product of (2) along paths recovers

$$
p_{\rm out}(z_1\cdots z_n)=
\sum_{a_1\cdots a_{n+r}}
p_{\rm in}(a_1\cdots a_{n+r})
\prod_{j=1}^{n}H(z_j\mid a_j\cdots a_{j+r}).
$$

This is the exact law of a sliding-window channel, not a disjoint-block approximation. In particular all the overlapping input symbols are shared in the sum. Several coupled input tracks can be encoded as one product alphabet, with a joint finite-state realization; no independence assumption about those tracks is needed. Cascades of finite-range channels with fresh conditional randomization can be implemented by repeating this lift. We do not identify a cascade with a single independent-output kernel on the original unaugmented input when shared intermediate randomness would make that identification false.

## 4. Block mixed-exterior theorem

Let $S_z$ be any stationary finite nonnegative transfer family, for example (2), on retained states with positive stationary row $\widehat\pi$. Fix a block length $s\ge1$ and write $D_w=S_w$ for every word $w$ of length $s$.

Choose a common pivot state $h_*$ and nonnegative anchored cone bounds $L_i,R_i$ with $L_{h_*}=R_{h_*}=1$. Require that the stationary row and all-ones column lie in their respective cones. Assume:

1. Every complete block has positive pivot $D_w(h_*,h_*)$.
2. Every complete block preserves the anchored row and column cones of WP07. Individual one-letter transfers need not preserve them.
3. The WP08 polarized exterior-square map satisfies the **complete-block** estimate

$$
\eta=\max_{|u|=|v|=s}
\frac{\|\mathcal P(D_u,D_v)\|_\infty}
{D_u(h_*,h_*)D_v(h_*,h_*)}<1.
\tag{3}
$$

**Theorem.** These finite conditions prove all-word exponential observable factorization, positive Hölder reverse conditionals and the exponentially summable two-sided Gibbs interaction of WP07. They survive every subsequent sitewise stochastic postprocessing with nonempty incoming support for every retained output label, at the same block length and contraction bound.

**Proof.** Positive block pivots imply full word support for multiples of $s$; every shorter or intermediate-length word can be extended to a multiple of $s$, so it too has positive mass.

First show all-length message-cone invariance for the stationary boundary vectors. For arbitrary word $w$, choose a padding length $t$ making $|w|+t$ divisible by $s$. By stationarity,

$$
\widehat\pi S_w=\sum_{|v|=t}\widehat\pi S_v S_w,
\qquad
S_w\mathbf1=\sum_{|v|=t}S_w S_v\mathbf1.
$$

Each summand is a whole-block message in the appropriate convex cone; the sum remains there. Thus all row and column word messages satisfy the WP07 anchor bounds, although single letters may violate the cone tests on arbitrary initial messages. The quasi-Bernoulli lower bound is

$$
b=\frac1{(\sum_iL_i)(\sum_i\widehat\pi_iR_i)}.
$$

For a word $w=uv$ where the prefix $u$ consists of $q$ complete blocks and $|v|<s$, exterior multiplicativity and positive pivot supermultiplicativity give

$$
\|\bigwedge^2 S_u\|_\infty
\le\eta^q\,p(u)^2/\widehat\pi_{h_*}^2.
$$

Let $F$ be the maximum of 1 and the normalized exterior-square norms $\|\bigwedge^2 S_v\|_\infty/p(v)^2$ for all nonempty words of length below $s$. It is finite. By submultiplicativity and the lower concatenation bound,

$$
\frac{\|\bigwedge^2 S_w\|_\infty}{p(w)^2}
\le\frac{F}{\widehat\pi_{h_*}^2 b^2}\eta^{\lfloor |w|/s\rfloor}.
$$

The WP07 exterior pairing in the original nonnegative realization now yields the exact conservative relative defect estimate

$$
|E_w(x,y)|\le
\frac{F}{\widehat\pi_{h_*}^2 b^4\min_i\widehat\pi_i}
\eta^{\lfloor |w|/s\rfloor}.
$$

For $\eta=0$, decay is exact from the first whole block onward. Otherwise the block rate is exponential in the ordinary word length. The WP07 reconstruction proves the Gibbs conclusion.

Under sitewise stochastic postprocessing, each new complete-block transfer is a nonnegative linear combination of old complete-block transfers, with coefficients equal to products of local channel probabilities. For every retained new word at least one such coefficient is positive. The cones, positive pivots and mixed bound are therefore inherited by WP08's bilinear calculation applied to complete blocks. The summed transition and stationary row remain unchanged. The remainder constant can be recomputed, or uniformly bounded by $\max(1,(\min_i\widehat\pi_i)^{-2})$, since for a nonnegative matrix the row-sum norm of its exterior square is at most the square of its maximum row sum. This gives closure under arbitrary finite cascades of subsequent sitewise channels. QED.

**Finite cost:** for a given $s$, there are $|Z|^s$ block matrices, at most $|Z|^{2s}$ ordered mixed pairs, and finite vertex tests of anchored coordinate boxes. This is an exact sufficient check, not a tractability promise or necessity result.

## 5. Kernel-independent transport: a whole family of overlapping readouts

A stronger sufficient criterion avoids enumerating all labelled blocks or even choosing the entire kernel. Use the source history lift and its unlabelled transition $\widehat Q$ from Section 3. Choose a reference input symbol $a_0$, a source hidden state $i_0$, a retained anchor $h_*=(a_0^r,i_0)$, and a block length $s\ge1$.

Assume the channel satisfies

$$
H(z\mid a_0^{r+1})\ge\alpha>0
$$

for every output label, with no restriction on other windows beyond stochasticity. They may be deterministic, coupled, or have arbitrary structural zeros. Assume the reference return mass $c_*=(T_{a_0}^s)(i_0,i_0)>0$. Put $m_*=\alpha^s c_*>0$. For each retained state $j$ define

$$
g_j=\frac{\max_i\widehat Q^s(i,j)}{m_*},
\qquad
K=\max(1,g_{h_*}),
\qquad
e=\sum_{j\ne h_*}g_j.
$$

**Theorem (kernel-independent block transport).** If

$$
e<1/2,\qquad 2Ke+e^2<1,
\tag{4}
$$

then **every** channel in the indicated family satisfies the block mixed-exterior criterion with

$$
L_{h_*}=R_{h_*}=1,\quad
L_j=2g_j,\quad R_j=K/(1-e)\quad(j\ne h_*),
\qquad \eta\le2Ke+e^2.
$$

In particular the criterion is checkable from the source and a single local likelihood bound, independently of the values of the kernel elsewhere.

**Proof.** For every output word of length $s$, the contribution of the constant-reference input path from the anchor back to itself is at least $m_*$. No other path subtracts mass. Also every output block transfer $D$ is entrywise bounded by $\widehat Q^s$, since summing over all output words of length $s$ gives $\widehat Q^s$. Thus, after dividing by its positive pivot, every normalized block has anchor-column entries at most $K$ and all other column entries at most $g_j$. Its anchor pivot equals one.

For a row normalized to anchor coordinate one with other coordinates bounded by $2g_i$, its total mass is at most $1+2e<2$. Multiplying by a normalized block gives anchor coordinate at least one and coordinate $j\ne h_*$ at most $(1+2e)g_j\le2g_j$. This proves row cone invariance. For a column with anchor one and other coordinates at most $R=K/(1-e)$, the new anchor is at least one, and every nonanchor coordinate is at most $K+Re=R$. This proves column invariance; $R\ge1$ includes the all-ones column.

Stationarity of the whole-block transition gives, for every nonanchor coordinate,

$$
\widehat\pi_j=\sum_i\widehat\pi_i\sum_{|w|=s}D_w(i,j)
\le g_j\sum_{|w|=s}D_w(h_*,h_*)\le g_j.
$$

It follows that $\widehat\pi_{h_*}\ge1-e$ and $\widehat\pi_j/\widehat\pi_{h_*}\le2g_j$, so the stationary row belongs to its cone.

Finally take two pivot-normalized blocks. Put $c_{h_*}=K$ and $c_j=g_j$ otherwise. The absolute value of each polarized minor with column pair $k,l$ is at most $2c_kc_l$, by its four-term bilinear expansion. Summing over all column pairs bounds every row sum of the mixed exterior square by

$$
2K\sum_{j\ne h_*}g_j+
2\sum_{\substack{k<l\\k,l\ne h_*}}g_kg_l
\le 2Ke+e^2.
$$

This proves (3) and completes the theorem. QED.

This is a restrictive but genuinely uniform class of source-to-channel transport statements. It is not obtained by checking particular output words at an empirical horizon. It certifies subsequent finite-range layers whenever their own source-to-lift bounds pass; failure at a layer is not a negative Gibbs decision. The theorem applies to arbitrary local kernels **subject to the specified reference-path and source-concentration inequalities**; it does not claim that WP08's original certificate alone is sufficient for arbitrary history lifts.

## 6. Exact genuinely overlapping specimens and obstruction

Use binary sources and a window of length three. The channel outputs fair noise on input 000 and otherwise outputs deterministic parity. It shares two input letters between adjacent windows. It is not a staggered-independent-track or a sitewise mixture on the original alphabet.

### Biased iid input

Let the source probability of one be $1/256$. In the four-state history lift, block length two has unlabelled transition rows equal to the iid distribution of the new two-letter history. Here $\alpha=1/2$, $K=4$ and $e=2044/65025$. The uniform theorem (4) gives the upper bound $1067466736/4228250625$, which is less than 0.253. The **actual** mixed contraction for the parity channel is exactly $8/85$, less than 0.095. The one-step cone check with the constructed bounds fails.

Both labelled matrices are invertible, and the minimal observable dimension is four (exact Hankel rank). In particular no word is a rank-one reset in any equivalent finite presentation, by WP07. The all-zero labelled transfer is a weighted permutation: history 00 has its own self-loop, while 01, 11 and 10 form a cycle. No positive power is strictly positive. More strongly, those two history sectors cannot be joined through any all-zero observed word. Thus global fibre mixing in this particular hidden presentation fails, but the relative weights yield exponential contraction. The output is not iid: exact adjacent-symbol probabilities fail factorization. We do not claim absence of every alternative fibre-mixing or positive realization.

### Non-iid two-state input

Put $\delta=1/1024$ and take

$$
T_0=\begin{pmatrix}1-2\delta&\delta\\1-3\delta&\delta\end{pmatrix},
\qquad
T_1=\begin{pmatrix}\delta&0\\2\delta&0\end{pmatrix}.
$$

Their sum has both rows $(1-\delta,\delta)$, which is stationary. The observed law has minimal dimension two and itself passes WP08's mixed exterior certificate with anchor 0, $L=(1,1)$ and $R=(1,2)$. In particular this is a certified non-iid Gibbs source.

For the same length-three parity channel, the retained history lift has dimension six and minimal observable dimension five. For block length two the source-only bound has $K=4$, $e=3276/209101$ and

$$
\eta_{\rm upper}=\frac{5490851184}{43723228201}<0.126.
$$

This proves the entire family of binary stochastic kernels with fair output on 000 is Gibbs-preserving for this source, including every deterministic assignment on the other seven input windows. The actual parity channel's mixed contraction is

$$
\eta_{\rm actual}=\frac{42823925764}{1093080705025}<0.040.
$$

The output is not iid, and the one-step cone test again fails. Two other kernels in the same uniform family were checked exactly; the theorem, not the examples, establishes closure for the whole family.

### No unconditional block closure

The earlier biased iid XOR example (Kari–Taati, WP03) shows that even an iid Gibbs source with trivial exterior-square certificate can become nonquasilocal under a deterministic two-site sliding block rule. This is already a published obstruction, not a new mathematical result. In the new history lift the common positive block pivot fails. The source concentration test in (4) does not certify the biased XOR source/channel. In particular the claim of unrestricted transport of the WP08 witness through arbitrary overlapping kernels is false.

## 7. Evidence and prior art

Exact code: finite_range_block_certificate.py. Tests: tests/test_csm_finite_range_block_certificate.py. Independent path evaluation sums original source word probabilities against the products of local channel probabilities, without using the lifted matrices. Regression covers minimality, all-word singular-gap witnesses, exact contradictory two-sided probabilities, full support, actual history lifts, source-only bounds, two-block mixed certificates, sitewise channel closure, exact rate constants, permanent zeros, and hostile deterministic XOR. Preliminary exact tests passed 6/6 at candidate 74098fdc3439098f4fc1a89fc95e1d71e49e85f0, receipt b79297e20cda4dc8bf06803cddb22e76 (independent attestation=false). Exact specimen rate capture 0268054dc72a4ace823a73a278786345 used the same candidate. Final candidate source gate and CI must bind the final revision, including strengthened tests.

**Prior-art boundaries.** Ian D. Morris, [Dominated splittings for semi-invertible operator cocycles on Hilbert space](https://arxiv.org/abs/1403.0824), explicitly modifies the invertible singular-gap criterion for the semi-invertible case. Quas–Thieullen–Zarrabi, [Explicit bounds for separation between Oseledets subspaces](https://arxiv.org/abs/1808.07230), treats additional fast-invertibility conditions with singular gaps. The singular-cocycle difficulty is not claimed new. Our concrete obstruction and one-symbol non-nullness repair are scoped to stationary finite-dimensional observable probability representations.

Piraino, [Single site factors of Gibbs measures](https://arxiv.org/abs/1905.03803) and [Projections of Gibbs States for Hölder Potentials](https://arxiv.org/abs/1709.07561), gives important factor-map results under fibre-mixing hypotheses. [Fiber-Mixing Codes between Shifts of Finite Type and Factors of Gibbs Measures](https://www.mdpi.com/1099-4300/18/12/428), Definition 1 and Lemma 1, gives the finite bridge condition; its introduction attributes Markov-to-Gibbs preservation under fibre mixing to Yoo. Higher-block recoding is standard. The exact history lift, polarization, cone invariance and block grouping are not individually novelty claims. The specific kernel-independent source-column concentration criterion, valid in the demonstrated non-fibre-mixing labelled presentation, requires comparison to existing quantitative posterior and factor-map theorems. No exhaustive source-proof replay, novelty verdict, or public certification is asserted.

**Disposition:** singular spectral-only claim refuted, corrected non-null spectral characterization proved; general finite-range lift criterion and uniform sufficient transport theorem proved; universal unconditional closure refuted by known XOR. Candidate originality UNADJUDICATED.

**Next boundary:** CSM-G2_NONRARE_BLOCK_TRANSPORT_AND_OBSERVABLE_QUOTIENT_OPTIMALITY_OPEN. Replace the restrictive concentration condition (4) by a weight-sensitive observable quotient or projective condition able to transport certificates in nonrare, genuinely coupled sources; determine which structural hypotheses are necessary. The arbitrary finite-range map problem without additional hypotheses is already negative. Canonical issue #3136 remains open.
