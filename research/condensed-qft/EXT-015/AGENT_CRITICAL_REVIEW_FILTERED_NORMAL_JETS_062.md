# EXT-015 REACH / 062 — critical audit of the filtered normal-jet module and fifth-vertex contact

**Logical GCL mathematical critic; bounded ACCEPT, not external mathematical certification.** Reviewed source [R2/061](R2_FILTERED_NORMAL_JET_INSERTION_061.md) at the **exact author head** \`7e8dc5801ad1f494f1f4b9169b63de13cdf0c71c\` from [source PR #2860](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2860), together with [exact fixture 061](fixtures/check_filtered_normal_jet_insertion_061.py). This review is intentionally a different mathematical analysis from the author's proof, under the existing GCL one-authentication/role-scoped review model.

## 1. Audit of all-orders algebra and hidden singular products

For the source-normal delta jet $\partial_y^\alpha\delta_y$ and a smooth positive-regulator complement $f(y,t)$, independently compute the distribution pairing with an arbitrary compact smooth test:

$$
\begin{aligned}
\left\langle f\partial_y^\alpha\delta_y,\varphi\right\rangle
&=(-1)^{|\alpha|}\partial_y^\alpha(f\varphi)(0,t)\\
&=\sum_{\beta\le\alpha}(-1)^{|\beta|}
{\alpha\choose\beta}(\partial_y^\beta f)(0,t)
\left\langle\partial_y^{\alpha-\beta}\delta_y,\varphi\right\rangle.
\end{aligned}
\tag{62.1}
$$

Here the first expression is understood fiberwise in $t$, followed by integration against the surviving quotient test. The signs are exact: for a first derivative the coefficient of $\delta$ is **minus** $\partial f$, whereas for a second derivative the Hessian coefficient has **plus** sign. No multiplication of two singular collision deltas is used. Insertion order is an exact consequence of $f(gT)=(fg)T=g(fT)$ for smooth $f,g$; applying the formula twice necessarily obeys all Leibniz cross terms. The action preserves the finite derivative-order filtration even when the coefficients vary with $\epsilon$.

**Verdict:** ACCEPT Theorem 61.1 as a general algebraic distribution identity for a **fixed source collision**. Do not extend it without proof to simultaneously overlapping source diagonals or a full forest character.

## 2. Adversarial independent quotient integral

The fixed K4 source has $H=Q^{-1}=(I+J)/4$, $A>0$ and inherited negative $B=-7\sqrt2/(288\pi^{3/2})$. Let $n_1,\ldots,n_4$ count edges to a fifth vertex, with $k=\sum n_j$ and the fourth source normal coordinate zero.

Directly integrate the **smooth complement** before differentiating in any K4 normal coordinate. The Gaussian integral is

$$
G_{n,\epsilon}(y)
=\int_{\mathbb R}\prod_{j=1}^4\kappa_\epsilon(y_j-t)^{n_j}\,dt
=K_k\epsilon^{1-k}\exp[-y^TS_ny/(2\epsilon^2)],
\quad S_n=D-\frac{vv^T}{k}.
\tag{62.2}
$$

This is an independently justified Gaussian completion-of-squares identity, rather than an assumption that the original delta jet is the same as its scalar value. At the source diagonal,

$$
G_{n,\epsilon}(0)=K_k\epsilon^{1-k},\quad
\nabla_yG_{n,\epsilon}(0)=0,\quad
(LG_{n,\epsilon})(0)
=-K_k\epsilon^{-k-1}\mathrm{tr}(HS_n).
\tag{62.3}
$$

Apply the jet pairing again to $G_{n,\epsilon}C_{K4,\epsilon}$, now after quotient integration:

$$
\int F_{n,\epsilon}C_{K4,\epsilon}\,dt
=K_k\left[
(A-B\Theta_n)\epsilon^{-(k+2)}\delta_y
+B\epsilon^{-k}L\delta_y
\right],\quad
\Theta_n=\mathrm{tr}(HS_n).
\tag{62.4}
$$

The result agrees with applying the partial-diagonal identity **before** Gaussian integration. This order-of-operations check is stronger than comparing one numerical coefficient.

**Verdict:** ACCEPT the partial-diagonal and quotient-integrated formulas, including the first-derivative term away from the locus where $t=0$ and its cancellation when paired with $t$-independent tests.

## 3. Weighted resistance and precise zero set

An independent variance decomposition writes

$$
S_n=\frac1k\sum_{i<j}n_in_j(e_i-e_j)(e_i-e_j)^T,
\qquad e_4=0.
\tag{62.5}
$$

Since every distinct pair of vertices in unit K4 has effective resistance $1/2$,

$$
\boxed{
\Theta_n
=\mathrm{tr}(HS_n)
=\frac1{2k}\sum_{i<j}n_in_j.
}
\tag{62.6}
$$

This expression is exactly zero when no pair of *distinct* source vertices has two positive attachment multiplicities. For nonzero $k$, that happens precisely when all attached edges meet **one** source vertex. In the latter case one can check the result without any matrix: translating the single attached source coordinate against the integrated external vertex leaves $\int\kappa_\epsilon(y_j-t)^kdt$ independent of $y$. If different source vertices are attached, the quadratic form is nonconstant and $\mathrm{tr}(HS_n)>0$ by positive definiteness of $H$.

**Hostile cases:** Two identical attachments at one vertex give $\Theta=0$; two distinct attachments give $\Theta=1/4$; three distinct source-vertex attachments give $\Theta=1/2$; multiplicities $(2,1,0,0)$ give $\Theta=1/3$. The formula also works when vertex 4 (the root) is one of the attachment locations. It would be incorrect to say *every* extra edge generates an integrated contact term: a bridge or multiple edges to a single source vertex do not.

**Verdict:** ACCEPT the theorem's sharp zero-contact criterion and the sign $\mathfrak C=-BK_k\Theta_n\epsilon^{-(k+2)}\delta_y$, positive for genuinely multi-vertex attachments in this specific K4 source scheme.

## 4. Independent two-edge test-pairing verification

For $n=(1,1,0,0)$, direct Gaussian covariance gives $K_2=1/(2\sqrt\pi)$, $\Theta=1/4$, $Hv=(3/4,3/4,1/2)$. Using the inherited source coefficient $B$:

$$
-BK_2\Theta\,\epsilon^{-4}\delta_y
=\frac{7\sqrt2}{2304\pi^2}\epsilon^{-4}\delta_y.
\tag{62.7}
$$

This is **not** the earlier R2/059 one-parallel-edge contact $7/(576\pi^2)$: the new external-vertex graph has different quotient geometry and an additional Gaussian integration.

The source-insertion pairing against a compact test agreeing with $\varphi=y_1t$ near the full diagonal is

$$
\langle F_{n,\epsilon}C_{K4,\epsilon},\varphi\rangle
=\frac{3B}{8\sqrt\pi}\epsilon^{-2}
=-\frac{7\sqrt2}{768\pi^2}\epsilon^{-2}
+O(e^{-c/\epsilon^2}).
\tag{62.8}
$$

The quotient-value-only insertion instead predicts zero on this mixed test, because neither $\delta_y$ nor $L_y\delta_y$ acting on $y_1t$ has a nonzero normal value or second derivative. For a test agreeing with $y_1^2$, the pairing is $B\epsilon^{-2}/(2\sqrt\pi)$, independently confirming retention of the original second-normal-jet coefficient. For a constant test the contact in (62.7) is visible at order $\epsilon^{-4}$; for $t^2$ the scalar and normal-Hessian contributions combine with coefficient $A/(4\sqrt\pi)+5B/(16\sqrt\pi)$ at order $\epsilon^{-2}$. These four distinct probes exclude a coincidentally correct scalar with a wrong first-jet implementation.

**Verdict:** ACCEPT R2/061's first genuine partial-diagonal mixed-coordinate witnesses and coefficient normalization.

## 5. Exact fixture, limitation, and release decision

The standard-library rational fixture independently checked 189 attachment multiplicity vectors (total edge count up to six), all pairwise K4 effective resistances, insertion-order permutations for several branching and repeated-edge multisets, and the constant/linear-mixed/quadratic test moments. CHAD exact fixture receipt \`4d4fd61672de46e7a4acfff7424eb97a\` PASS. The source mathematical Markdown gate receipt \`0ac3f746bfb64a5faf180c62397825cf\` PASS. The finite verification is **not** the proof of the all-orders jet representation; (62.1) is.

**Final disposition: ACCEPT the bounded jet module and exact fifth-vertex contact theorem** for a fixed K4 source embedded into smooth positive-regulator external Gaussian edges. This recovers a coherent insertion operation missing in R2/059, but it is **not** a full solution of REACH-R2: no overlap between two singular source delta jets was tested, and no global BPHZ/BV/QME, completed Weiss descent or higher liquid Ext theorem follows.

**Admission requirements:** Protected-merge the pinned source PR #2860 first and this role-scoped critical review second, pass the relevant exact-head protected checks, and read back both plus the fixture from protected main. Keep [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) open for a genuine nested multi-source delta-jet compatibility result.
