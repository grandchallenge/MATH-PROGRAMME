# CSM-G2-WP07 — observable spectral separation without rank-one resets

**Status:** internally proved candidate characterization and finite exact certificate; originality UNADJUDICATED. No MATHCERT or independent mathematical certification. This extends WP06 beyond its marked-reset class, for **exponential** regularity; it does not classify every absolutely summable Gibbs interaction.

## 1. Observable factorization

Let a stationary full-support finite-alphabet process have a nonnegative finite-dimensional transfer representation

$$
p(w)=\pi T_w\mathbf1,\qquad T_w=T_{w_1}\cdots T_{w_n},
\qquad \pi Q=\pi,\qquad Q=\sum_a T_a.
$$

The row $\pi$ is a strictly positive stationary probability row and $Q$ is stochastic. Write $p(\varnothing)=1$. For arbitrary finite contexts $u,v$ and separator word $w$, define

$$
E_w(u,v)=\frac{p(uwv)p(w)}{p(uw)p(wv)}-1.
$$

This is the relative conditional-independence defect for two specified contexts given the whole intervening word; it is not ordinary mixing with the intervening word unobserved. All denominators are positive by full support.

A quasi-Bernoulli lower bound means that for some $b>0$,

$$
p(uv)\ge b\,p(u)p(v)
\tag{QB}
$$

for all finite words. An upper bound $p(uv)\le p(u)p(v)/\min_i\pi_i$ is automatic in the nonnegative representation, since $\pi T_u$ has coordinate sum $p(u)$ and each coordinate of $T_v\mathbf1$ is at most $p(v)/\min_i\pi_i$.

## 2. Theorem: uniform observable factorization

The following statements are equivalent:

(A) There is a strictly positive reverse conditional function $g(a\mid x_1x_2\ldots)$ for the stationary law whose logarithm has exponentially decaying variations, uniformly over all future words.

(B) There are $C<\infty$, $0<\theta<1$, such that

$$
|E_w(u,v)|\le C\theta^{|w|}
\tag{1}
$$

for **all** words $u,v,w$, and (QB) holds.

(C) In any fixed minimal linear representation $p(w)=\ell M_w r$ of dimension $d_*$, (QB) holds, and for constants $C'<\infty$, $0<\theta'<1$,

$$
\frac{\|\bigwedge^2 M_w\|}{p(w)^2}
\le C'(\theta')^{|w|}
\tag{2}
$$

for all words. In dimension one interpret the exterior square as zero.

Each condition implies that the stationary law satisfies a translation-invariant Gibbs specification for an exponentially summable interval interaction. This last implication is proved directly below. The claim does not assert necessity for all quasilocal or uniformly absolutely summable Gibbs measures with slower variation.

### A implies B

Let $q(a\mid t)=p(at)/p(t)$ for a finite future $t$. It is the conditional average of $g(a\mid\cdot)$ over the cylinder of $t$. If two finite future words share a prefix of length $k$, both averages lie between the minimum and maximum of $g$ on that cylinder. Therefore the difference of their logarithms is bounded by $D\theta^k$ for some $D<\infty$. Factor the left context $u$ from right to left using finite conditional probabilities. In the two conditional probabilities $p(uwv)/p(wv)$ and $p(uw)/p(w)$ the compared futures share the separator $w$ and a suffix of $u$ of increasing length. Consequently

$$
\left|\log(1+E_w(u,v))\right|
\le \sum_{j=0}^{|u|-1}D\theta^{|w|+j}
\le \frac{D}{1-\theta}\theta^{|w|}.
$$

For $w=\varnothing$ this proves (QB) with $b=\exp(-D/(1-\theta))$. Exponentiating the uniform bound gives (1), with a changed finite constant.

### B implies A

Take $u=a$ in (1). Since

$$
1+E_w(a,v)=\frac{q(a\mid wv)}{q(a\mid w)},
$$

the logarithmic discrepancy is bounded by $2C\theta^{|w|}$ whenever the right side of (1) is at most $1/2$. The remaining finitely many lengths have a uniform logarithmic bound because (QB) gives $q(a\mid t)\ge b p(a)>0$ for every finite $t$. Thus the finite conditional functions are uniformly Cauchy as the future grows. Their positive limit $g$ has exponential logarithmic variations (compare two continuations with their shared prefix). Martingale convergence identifies it with a version of the reverse conditional law. This proves A.

### B and C are equivalent

Use actual words to choose row and column bases $\ell M_{u_i}$ and $M_{v_j}r$ of the minimal representation, each containing the empty word. Minimality gives both spans full dimension. The matrices of these bases, $L$ and $R$, are invertible. For each separator define the finite observable Hankel slice

$$
H_w(i,j)=p(u_i w v_j)= (LM_wR)_{ij}.
$$

Its empty-word entry is $p(w)$. Every entry is nonnegative and at most $p(w)$ by stationarity and cylinder inclusion, even without (QB). Hence in fixed coordinates $\|M_w\|$ and $p(w)$ are comparable by constants independent of $w$. The same observation applies to all norms in finite dimension.

Under B, write

$$
H_w(i,j)=\frac{H_w(i,0)H_w(0,j)}{p(w)}+\varepsilon_{ij}.
$$

By (1) and the cylinder bound, $|\varepsilon_{ij}|\le C\theta^{|w|}p(w)$. The first matrix on the right has rank one and entries at most $p(w)$. Expanding any two-by-two minor, its rank-one contribution cancels and all remaining terms are bounded by a constant times $\theta^{|w|}p(w)^2$. Thus the exterior-square norm of $H_w$ has this bound. Multiplicativity of exterior powers and fixed invertible $L,R$ give (2).

Conversely suppose C. For arbitrary contexts define $\ell_u=\ell M_u$ and $r_v=M_vr$. In the fixed bases, the normalized vectors $\ell_u/p(u)$ and $r_v/p(v)$ are uniformly bounded. Indeed evaluation of $\ell_u$ on every fixed column basis element gives $p(uv_j)\le p(u)$, and evaluation of $r_v$ on every fixed row basis element gives $p(u_i v)\le p(v)$. Inverting the fixed basis matrices gives the asserted uniform bounds. The exact exterior identity is

$$
p(uwv)p(w)-p(uw)p(wv)
=(\ell_u\wedge\ell)(\bigwedge^2 M_w)(r_v\wedge r).
$$

The sign follows from the determinant with rows $\ell_u,\ell$ and columns $r_v,r$. The right side is bounded in absolute value by a constant times $p(u)p(v)\|\bigwedge^2 M_w\|$. Dividing by $p(uw)p(wv)$ and using (QB) twice gives B. QED.

**Finite observable probes.** It is enough, in B, to check the normalized anchored minors

$$
\frac{|p(u_iwv_j)p(w)-p(u_iw)p(wv_j)|}
     {p(u_i)p(v_j)p(w)^2}
$$

for fixed actual-word bases and all separator words with the same exponential bound; the same expansion of $H_w$ proves C. WP04 obtains actual-word spans from a nonminimal realization with probe lengths at most the original dimension minus one; choose independent rows and columns in the reduced pairing. The proof eliminates unobservable modes. It does not turn the all-word decay condition itself into a finite decision algorithm.

## 3. Spectral-only characterization for invertible minimal transfers

Assume $d_*\ge2$ and every minimal generator $M_a$ is invertible. Then A, B and C are equivalent to the **single** uniform singular-value-gap condition

$$
\frac{\sigma_2(M_w)}{\sigma_1(M_w)}
\le K\gamma^{|w|},\qquad 0<\gamma<1.
\tag{3}
$$

In particular no separate (QB) hypothesis is needed in this invertible case.

C implies (3) by the Euclidean exterior-square identity $\|\bigwedge^2 M_w\|_2=\sigma_1(M_w)\sigma_2(M_w)$ and the fixed comparison $\|M_w\|\asymp p(w)$ established above.

For the converse use the **external** Bochi–Gourmelon theorem, *Some Characterizations of Domination*, Theorem A, [arXiv:0808.3811v2](https://arxiv.org/html/0808.3811v2). Apply it to the locally constant invertible cocycle on the bi-infinite full shift with values in the minimal generators (reverse the itinerary order if needed to match the transfer multiplication convention). The uniform bound (3) over every finite word is precisely the uniform singular gap hypothesis at index one. It gives a continuous invariant splitting into a dominating line $E$ and a complementary bundle $F$, with uniform exponential relative contraction. Compactness bounds the norms of both splitting projections. Thus some constant $J\ge1$ satisfies

$$
\|M_w\|\le J\|M_w|_{E(x)}\|
$$

for every itinerary segment realizing $w$: decompose a unit vector into its two components and use the domination bound on the complementary component. This comparison is uniform in the complete itinerary. For any concatenation $uv$, choose one bi-infinite itinerary applying $v$ first, then $u$. Invariance and the one-dimensionality of $E$ make the norm along the dominating line exactly multiplicative. Therefore

$$
\|M_{uv}\|\ge J^{-2}\|M_u\|\|M_v\|.
$$

Using $\|M_w\|\asymp p(w)$ gives (QB). Condition (3) also implies (2) by the exterior-square identity. This proves the claimed equivalence with A using the established domination theorem; no independent replay of Bochi–Gourmelon is claimed. The necessity direction holds without invertibility. The extension to singular minimal generators without (QB) is **not** established here.

This is a spectral-only reformulation on the minimal observable module, not a claim to have discovered domination or general hidden-Markov filtering stability. It does not use exact resets. In the invertible case it even precludes them in every realization: the rank of $H_w$ is $d_*$, and any equivalent transfer representation factors this same slice through its word matrix, so that matrix must have rank at least $d_*$.

## 4. Direct Gibbs reconstruction

Given A, let $f(x)=-\log g(x_0\mid x_1x_2\ldots)$, and choose a reference letter $o$. Telescope $f$ by successively extending the finite observed prefix, filling its unused tail by $o^\infty$. Put the resulting difference terms on intervals starting at the present site, including the initial single-site term. The term on an interval of length $j+1$ is bounded in norm by a constant times $\theta^{j-1}$ for $j\ge1$. Counting all translates containing a given site gives a finite norm sum because $\sum_{j\ge1}(j+1)\theta^{j-1}<\infty$.

To verify the DLR identity, compare two cylinders on a large finite interval that agree outside a fixed central subinterval. Express the ratio of their probabilities as a product of finite reverse conditionals, working from the right endpoint toward the left. Factors to the right of the central interval cancel. Terms within the central interval converge to the ratios defined by $g$ uniformly as the right boundary recedes. Terms to the left at distance $j$ from the first changed symbol have logarithmic discrepancy bounded by a constant times $\theta^{j-1}$, uniformly in the boundary length and words. Hence dominated convergence identifies the infinite log-ratio with the sum of the differences of $f$ at those sites. Telescoping and absolute summability identify this sum with the difference of the constructed interval energies that intersect the central interval. Normalizing the finitely many competing interior configurations yields the Gibbs kernel. Martingale convergence identifies it with the conditional law given the entire exterior; continuity and strict positivity follow from the absolutely summable interaction. Conditioning within enclosing intervals gives the DLR identity for arbitrary finite subsets.

The proof is two-sided and does not identify arbitrary continuous one-sided g-measures with Gibbs measures.

## 5. Finite rational sufficient certificate in a nonnegative realization

The general criterion can be made finite in a useful class, without computing the minimal quotient. Fix a common pivot index $h$ and nonnegative rational bounds $L_i,R_i$ with $L_h=R_h=1$. Assume all generator pivots $T_a(h,h)$ are positive. Check that the row cone $x_i\le L_i x_h$ is invariant under right multiplication by every $T_a$ and that the column cone $y_i\le R_i y_h$ is invariant under left multiplication. Require that $\pi$ and $\mathbf1$ respectively belong to these cones. All vectors here are nonnegative. The invariance checks are finite: normalize the anchor coordinate to one and test each linear inequality at every vertex of the resulting coordinate box. The anchor output stays positive by the positive pivot.

For any words $u,v$, their row and column messages satisfy

$$
(\pi T_u)_h\ge\frac{p(u)}{\sum_i L_i},
\qquad
(T_v\mathbf1)_h\ge\frac{p(v)}{\sum_i\pi_i R_i}.
$$

Therefore (QB) holds with $b=1/((\sum_i L_i)(\sum_i\pi_i R_i))$.

For some block length $s\ge1$, verify the exact rational inequality

$$
\eta=\max_{|w|=s}
\frac{\|\bigwedge^2 T_w\|_\infty}{T_w(h,h)^2}<1.
\tag{4}
$$

For every word split it into full blocks of length $s$ and a remainder of length below $s$. Exterior-square norms are submultiplicative, whereas the pivot of a product of nonnegative matrices is at least the product of their pivots. Let $B_0$ be the maximum of 1 and the ratios in (4) for all nonempty remainders. Then

$$
\frac{\|\bigwedge^2 T_w\|_\infty}{p(w)^2}
\le \frac{B_0}{\pi_h^2}\eta^{\lfloor|w|/s\rfloor}.
$$

For the general exterior identity in the original nonnegative realization, the sum norm of $\pi T_u\wedge\pi$ is at most $p(u)$, and the maximum norm of $T_v\mathbf1\wedge\mathbf1$ is at most $p(v)/\min_i\pi_i$. Using the two (QB) bounds therefore proves the explicit rational estimate

$$
|E_w(u,v)|
\le\frac{B_0}{\pi_h^2 b^2\min_i\pi_i}\eta^{\lfloor|w|/s\rfloor}.
\tag{5}
$$

Also $q(a\mid t)\ge b p(a)$. This is a checked all-length proof, not empirical regression extrapolation. If $\eta=0$, the defect vanishes once a full block is present; this is also an exponential bound. Failure of the certificate has no converse implication. Complexity is exponential in the prescribed block length and hidden dimension for the reference vertex check, with exact rational arithmetic.

## 6. A reset-free, irreducible, infinite-memory positive specimen

Take three transfers

$$
T_0=\begin{pmatrix}1/2&0\\0&1/8\end{pmatrix},\quad
T_1=\begin{pmatrix}1/4&1/16\\0&1/8\end{pmatrix},\quad
T_2=\begin{pmatrix}3/16&0\\5/8&1/8\end{pmatrix}.
$$

Their sum is positive stochastic with stationary row $\pi=(10/11,1/11)$. Every generator is invertible and has structural zeros; all powers of $T_0$ have zeros. Both reachable spans have dimension two (already the empty word and symbol 0 are independent in each span), so the presentation is minimal. **No word can be an exact rank-one reset in any equivalent realization**, by the rank argument in Section 3. This also excludes finite Markov order, using the classical minimal-representation finite-order rank criterion recorded in WP04.

With anchor $h=0$, row bounds $(1,1)$ and column bounds $(1,10)$ the cone tests pass. In dimension two the exterior square is the determinant, and the generator ratios in (4) are $1/4,1/2,2/3$. Thus $\eta=2/3$, $b=11/40$, and (5) gives the completely explicit all-word result

$$
|E_w(u,v)|\le176(2/3)^{|w|}.
$$

The non-null lower bound is $21/320$. These constants are deliberately conservative. No claim is made that the process has no alternative strictly positive realization; the impossibility established here is of any exact rank-one reset word.

### Two overlapping layers with no reset in any realization

Take independent stationary copies $A_i,B_i$ of the preceding edge-observation process (the hidden chain and edge channels are realized by $Q$ and $T_a(s,t)/Q(s,t)$). The first layer emits $Y_i=(A_i,B_i)$ from adjacent hidden states. The deterministic second layer, using $Y_i,Y_{i+1}$, emits

$$
Z_i=(A_i,A_i+B_{i+1}\bmod 3).
$$

This is a genuinely overlapping pair readout, though its structure is special: after the fixed pointwise bijection it is the independent product of one stationary copy and a shifted second copy. The exact observed presentation has generators $T_a\otimes T_{(c-a)\bmod3}$ indexed by the final pair $(a,c)$. Its summed transition is positive and its minimal dimension is four: independent actual-word bases for each factor give full four-dimensional tensor spans by using equal-length probe words (in this example length one suffices because sums of one-letter messages reproduce the empty-word seed). All generators and their products are invertible. Thus no equivalent finite presentation can contain a rank-one word. The full observed alphabet has nine symbols.

Every cylinder probability factors into those of the two decoded coordinate words. Therefore its relative conditional-independence ratio is the product of the two base ratios. If each base defect is bounded by $e_k=176(2/3)^k$, the composite defect is bounded by $2e_k+e_k^2$, which is exponential in $k$. Its quasi-Bernoulli lower bound is at least $b^2$. Hence the composed law is Gibbsian by the proved theorem, with infinite Markov memory and no exact reset. This proves preservation in a specified nontrivial overlapping composition; it does not assert that arbitrary overlapping pair maps preserve the spectral gap.

## 7. Irreducible invertible hostile control

Use $T_0=(5/8)I$ and

$$
T_1=\begin{pmatrix}3/16&1/16\\1/32&3/32\end{pmatrix},\qquad
T_2=\begin{pmatrix}3/32&1/32\\1/16&3/16\end{pmatrix}.
$$

Again $Q$ is strictly positive stochastic, $\pi=(1/2,1/2)$, all matrices are invertible and the minimal dimension is two. The uniform gap (3) fails already along all-zero words since their two singular values are equal. The exact observable defect is

$$
E_{0^n}(1,1)=1/18
$$

for every $n\ge0$. The anchor cones with bounds $(1,3)$ and $(1,6)$ are invariant, but their contraction certificate rejects the scalar-identity background transfer. This is not merely a failure of a sufficient test: condition on a marker of type 1 at each end of an all-zero exterior neighborhood of radius $n$, leaving the center unspecified. Compare the otherwise identical exterior cylinder with markers of type 2. Since $T_0$ is scalar, all zero-run factors cancel. Direct exact cylinder computation gives, in the symbol order $(0,1,2)$,

$$
\left(190/301,123/602,99/602\right),
\qquad
\left(190/301,99/602,123/602\right).
$$

These fixed distinct conditional vectors occur for every $n$, on positive-probability exterior cylinders approaching all zeros. Any continuous conditional at all zeros would force both finite-cylinder averages to the same limit, so no quasilocal version exists. This negative control rules out Gibbsianity even though the hidden chain is irreducible, every word transfer is invertible, and a quasi-Bernoulli lower bound holds.

## 8. Evidence, prior art, and next boundary

The exact reference implementation is observable_exterior_square.py. The regression in tests/test_csm_observable_exterior_square.py checks every separator word through length four for the base model and two-letter blocks through length five, exact determinant identities, multiplicativity of exterior squares, the cone and rate certificate, the full minimal dimensions and invertibility, independent microscopic path enumeration of decoded overlapping cylinder laws through length three, and the persistent hostile conditional defect. The initial hostile cone fixture was too narrow; after repair all six tests passed at candidate b640dbc1647d4412717f2975de4024befab3666a, local capture c60047ed455f423589f4fba91c654041, independent attestation false. Final candidate source gate and native CI required.

**Novelty controls:** Bochi–Gourmelon Theorem A proves uniform singular gaps equivalent to dominated splitting for invertible cocycles; this is explicitly imported, not claimed new. Chazottes–Ugalde [arXiv:math/0211457](https://arxiv.org/abs/math/0211457) and Piraino [arXiv:1709.07561](https://arxiv.org/abs/1709.07561) give factor-map regularity via positivity/fiber mixing. Olivier–Thomas, *Projective Convergence of Inhomogeneous 2 x 2 Matrix Products* (2015), and Alain Thomas [arXiv:2205.09044](https://arxiv.org/abs/2205.09044), study uniform projective convergence and Gibbs or weak-Gibbs structures. The finite-word rank criterion is already classical as audited in WP04. The precise combination of observable Hankel-slice separation, conditional relative factorization, and invertible minimal-cocycle domination is a **candidate internal theorem**, not an adjudicated original contribution. Complete primary-statement concordance with these and related positive-realization and matrix-cocycle results remains required.

**Completed mathematical candidate:** uniform observable exponential factorization without resets; spectral-only necessary-and-sufficient criterion for positive Hölder reverse conditionals in the invertible minimal class; constructive Gibbs implication; finite rational sufficient certificate; explicit positive and negative reset-free irreducible models and an overlapping composition.

**Next substantive boundary:** CSM-G2_SINGULAR_MINIMAL_COCYCLE_AND_GENERAL_COMPOSITION_STABILITY_OPEN. Establish how (3) behaves under genuinely coupled overlapping composition rather than the staggered independent-track example, and whether singular minimal generators permit the spectral-only implication without a separately established (QB) bound. Novelty adjudication, specialist source review and MATHCERT remain separate.
