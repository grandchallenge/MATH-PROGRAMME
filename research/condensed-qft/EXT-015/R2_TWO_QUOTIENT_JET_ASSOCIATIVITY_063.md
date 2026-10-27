# EXT-015 REACH-R2 / 063 — two-stage Gaussian quotient transport of a differentiated source counterterm

**Status:** bounded mathematical source candidate; exact-head critical review and protected admission required. The source-local normal-jet module of [R2/061](R2_FILTERED_NORMAL_JET_INSERTION_061.md) and its [R2/062 critical audit](AGENT_CRITICAL_REVIEW_FILTERED_NORMAL_JETS_062.md) treated the first nontrivial single surviving quotient coordinate. The present theorem admits *arbitrarily many anchored smooth Gaussian quotient vertices*, derives a positive geometric criterion for their collective jet contact, and proves independence of **successive external-coordinate elimination order**. A six-vertex graph with a genuine two-stage quotient and a source normal second-derivative counterterm produces a new exact order-independent nonzero contact.

**Not claimed:** the comparison of two *singular* overlapping or nested source counterterms, a full prepared forest for the six-vertex graph, a global BV square-zero/QME theorem, Weiss descent or liquid Ext. The only singular source in this result is the inherited K4 normal delta jet; all newly inserted edge kernels are smooth for each positive regulator.

## 1. A multi-quotient network attached to a fixed singular source

Use the labeled four-vertex source K4, with vertex 4 as root and internal coordinates

$$
y=(x_1-x_4,x_2-x_4,x_3-x_4),\qquad
H=Q_{K4}^{-1}=\tfrac14(I+J),\qquad
L=H:\partial_y^2,\quad\delta_y=\delta(y).
\tag{63.1}
$$

The *fixed intrinsic* prepared overall source counterterm, already independently verified and protected-admitted in [R2/051](R2_K4_NESTED_OVERLAP_FOREST_051.md), is

$$
C_{K4,\epsilon}
=A\epsilon^{-3}\delta_y+B\epsilon^{-1}L\delta_y,\quad
A=\pi^{-3/2}\left(\sqrt3-\tfrac34+\tfrac{5\sqrt2}{48}\right),\quad
B=-\frac{7\sqrt2}{288\pi^{3/2}}.
\tag{63.2}
$$

Introduce $m\ge1$ external quotient vertices, with positions relative to root $q=(q_1,\ldots,q_m)$. Add $k$ labeled, positive-weight Gaussian edges, each connecting a source vertex to an external vertex or two external vertices. No new source-to-source edge is used in this theorem. Every connected component of the graph induced on external vertices is required to have at least one attachment to a source vertex. Use the normalized unit Gaussian on every labeled edge:

$$
\kappa_\epsilon(u)=(2\pi)^{-1/2}\epsilon^{-1}e^{-u^2/(2\epsilon^2)}.
\tag{63.3}
$$

The product of all new edges is a smooth positive-regulator complement

$$
F_\epsilon(y,q)
=(2\pi)^{-k/2}\epsilon^{-k}
\exp\left[-\frac{1}{2\epsilon^2}
\left(y^TDy-2y^TCq+q^TMq\right)\right].
\tag{63.4}
$$

Here $D$ is a nonnegative diagonal $3\times3$ matrix of source-to-external attachment multiplicities excluding source root 4; $C$ is the $3\times m$ source-to-external incidence-multiplicity matrix; $M$ is the grounded $m\times m$ external weighted Laplacian, incorporating all source-to-external and external-to-external edges. The attachment hypothesis implies $M$ is strictly positive definite.

For external-complement graphs with nonunit positive edge weights $w_e$, the same block quadratic form works with weighted sums, and the corresponding product normalization differs by the explicit factor $\prod_e w_e^{1/2}$ if each kernel has variance $\epsilon^2/w_e$. The exact constants below are stated for **unit** edges; the algebraic Schur complement and positivity statements extend to arbitrary positive weights.

## 2. General exact pushforward and source-jet transport

Define the reduced quotient form and normalization

$$
S=D-CM^{-1}C^T,\qquad
Z=(2\pi)^{-(k-m)/2}\det(M)^{-1/2},\qquad
\Theta=\mathrm{tr}(HS).
\tag{63.5}
$$

**Theorem 63.1 (multi-quotient normal-jet transport).** For every $\epsilon>0$ the quotient integral of the smooth complement is exactly

$$
G_\epsilon(y)=\int_{\mathbb R^m}F_\epsilon(y,q)\,dq
=Z\epsilon^{m-k}\exp[-y^TSy/(2\epsilon^2)].
\tag{63.6}
$$

The product of this smooth complement with the *unchanged* singular K4 source, pushed forward along all quotient coordinates, is the exact distributional identity

$$
\boxed{
\int_{\mathbb R^m}F_\epsilon(y,q)C_{K4,\epsilon}\,dq
=Z\left[
(A-B\Theta)\epsilon^{m-k-3}\delta_y
+B\epsilon^{m-k-1}L\delta_y\right].
}
\tag{63.7}
$$

Moreover, any ordering of the $m$ quotient integrations gives **exactly the same distribution** and the same full derivative-jet coefficients. The naïve rule that freezes the quotient complement at the source collision before applying its normal derivatives misses the local term

$$
\boxed{
\mathfrak C_\epsilon=-BZ\Theta\,\epsilon^{m-k-3}\delta_y.
}
\tag{63.8}
$$

**Proof.** Complete the square in $q$ using the positive definite $M$:

$$
q^TMq-2y^TCq
=(q-M^{-1}C^Ty)^TM(q-M^{-1}C^Ty)
-y^TCM^{-1}C^Ty.
\tag{63.9}
$$

The standard Gaussian integral yields (63.6) with the exact determinant. At $y=0$,

$$
G_\epsilon(0)=Z\epsilon^{m-k},\quad
(\nabla_yG_\epsilon)(0)=0,\quad
(LG_\epsilon)(0)=-Z\Theta\epsilon^{m-k-2}.
\tag{63.10}
$$

Apply the distributional Leibniz action of [Theorem 61.1](R2_FILTERED_NORMAL_JET_INSERTION_061.md) to $G_\epsilon\delta_y$ and $G_\epsilon L\delta_y$, retaining both the Hessian contact and the original normal second jet. This gives (63.7) and the difference (63.8). All products of singular distributions are avoided because $F_\epsilon$ is smooth for each $\epsilon>0$; its rapid Gaussian decay in $q$ permits fiberwise integration of the delta-jet coefficients against compact tests.

For any permutation of quotient coordinates, iterative Gaussian integration applies a succession of Schur complements. Both their determinant products and final reduced matrix equal $\det M$ and $S$ by elementary block Gaussian elimination. Equivalently, Fubini's theorem for the rapidly decaying smooth complement commutes with differentiation of its finite normal jets in $y$. Thus the intermediate expressions can differ, but the full jet and final contact are independent of elimination order. $\square$

## 3. Sharp geometric zero-contact criterion

**Theorem 63.2 (positive Dirichlet-energy obstruction and exact zero set).** For the described anchored Gaussian network,

$$
S\succeq0,\qquad
\Theta=\mathrm{tr}(HS)\ge0,
\tag{63.11}
$$

and

$$
\boxed{
\Theta=0\quad\Longleftrightarrow\quad
\text{each connected external-vertex component attaches to exactly one source vertex}.
}
\tag{63.12}
$$

If any external connected component attaches to two or more distinct original K4 vertices, then $\Theta>0$. Because the inherited $B<0$, its omitted scalar contact (63.8) then has a strictly **positive coefficient**.

**Proof.** The full block quadratic energy is the sum of squares of edge differences between source or external coordinates. For fixed source $y$, minimizing over external coordinates $q$ yields $y^TSy$ by (63.9), so $S$ is positive semidefinite. The positive definite $H$ implies $\mathrm{tr}(HS)=0$ exactly when $S=0$. If an external component attaches to only one source vertex, set every external coordinate in that component equal to its attached source coordinate; this makes every edge difference vanish *for arbitrary source positions* and proves that this component contributes no reduced energy. If a component attaches to distinct source vertices $i,j$, choose source positions with $y_i\ne y_j$. Any path through that external component between the two attachments has strictly positive total squared-difference energy under every choice of external coordinates (a finite path cannot have all differences zero when its endpoints disagree); consequently $S\ne0$. This proves (63.12). $\square$

This strengthens the single-fifth-vertex resistance criterion of R2/061 to **arbitrary anchored external networks**. The criterion is geometric; neither $A$ nor $B$ has been refitted to the containing graph.

## 4. Exact six-vertex double-quotient witness

Take a genuine six-vertex graph consisting of K4 on $1,2,3,4$ and four additional labeled edges

$$
15,\quad25,\quad56,\quad36,
\tag{63.13}
$$

with external coordinates $t=x_5-x_4$, $s=x_6-x_4$. The full graph has six vertices, ten edges and cycle rank five. The complement has $k=4$ edges and $m=2$ quotient coordinates. Its exact matrices are

$$
D=I_3,\qquad
C=\begin{pmatrix}1&0\\1&0\\0&1\end{pmatrix},\qquad
M=\begin{pmatrix}3&-1\\-1&2\end{pmatrix},
\quad\det M=5,
\quad M^{-1}=\frac15\begin{pmatrix}2&1\\1&3\end{pmatrix}.
\tag{63.14}
$$

Their Schur complement is

$$
S=\frac15\begin{pmatrix}
3&-2&-1\\
-2&3&-1\\
-1&-1&2
\end{pmatrix},\qquad
\boxed{\Theta=\mathrm{tr}(HS)=\frac25},
\quad Z=\frac{1}{2\pi\sqrt5}.
\tag{63.15}
$$

**Theorem 63.3 (two legal quotient orders, one differentiated source).** Eliminating $t$ first and then $s$ produces an intermediate K4-covariance trace loss of $1/2$ followed by $3/5$. Eliminating $s$ first and then $t$ produces respective losses of $1/4$ and $17/20$. Both result in

$$
\mathrm{tr}(HD)-\left(\frac12+\frac35\right)
=\mathrm{tr}(HD)-\left(\frac14+\frac{17}{20}\right)
=\frac25,
\qquad \det M=5.
\tag{63.16}
$$

Therefore the *same* fixed source counterterm inserted into the six-vertex graph has quotient-integrated form

$$
\boxed{
\int_{\mathbb R^2}F_\epsilon(y,t,s)C_{K4,\epsilon}\,dt\,ds
=\frac1{2\pi\sqrt5}\left[
\left(A-\frac25 B\right)\epsilon^{-5}\delta_y
+B\epsilon^{-3}L\delta_y
\right].
}
\tag{63.17}
$$

The omitted local scalar contact under a value-only quotient insertion is precisely

$$
\boxed{
\mathfrak C_\epsilon
=\frac{7\sqrt{10}}{7200\pi^{5/2}}\,
\epsilon^{-5}\delta_y\ne0.
}
\tag{63.18}
$$

For compactly supported tests equal near the full diagonal to the displayed polynomials, with Gaussian-exponentially small cutoff errors, the following distinguish **independent jet information**. Let $K=(2\pi\sqrt5)^{-1}$.

| Local test polynomial | Leading order in pairing | Exact coefficient |
| --- | --- | --- |
| $1$ | $\epsilon^{-5}$ | $K(A-\tfrac25B)$ |
| $y_1^2$ | $\epsilon^{-3}$ | $KB$ |
| $y_1t$ | $\epsilon^{-3}$ | $\tfrac7{10}KB$ |
| $y_1s$ | $\epsilon^{-3}$ | $\tfrac35KB$ |

The two **mixed** probes are nonzero and unequal. They detect the normal first-derivative jet *before* quotient integration and prevent a scalar-only approximation from accidentally passing a constant test.

**Proof.** The two elimination decompositions are exact applications of the scalar Schur complement; the loss terms in (63.16) arise respectively from the squared norms induced by $H$ of the source-to-external incidence columns divided by the corresponding conditional external precisions. Then (63.17)–(63.18) follow from (63.7)–(63.8). For the mixed probes pair $L\delta_y$ with $F_\epsilon(y,q)y_1q_a$ before quotient integration. Only the first derivative of the test and the first normal derivative of the complement contribute. Under the quotient Gaussian at the source collision, $\mathbb E[q_aq_b]=\epsilon^2(M^{-1})_{ab}$. Consequently the mixed coefficient is $2KB(HCM^{-1})_{1a}\epsilon^{-3}$; direct rational matrix multiplication gives $2(HCM^{-1})_{1t}=7/10$ and $2(HCM^{-1})_{1s}=3/5$. The quadratic normal test has $L(y_1^2)(0)=1$. Gaussian concentration makes cutoff errors exponentially small compared with each displayed power. $\square$

## 5. Exact controls, meaning and next mathematical gate

The [standard-library exact regression 063](fixtures/check_two_quotient_jet_associativity_063.py) verified $\det M=5$, both Schur complements, $\Theta=2/5$, the contact coefficient and the four independent test probes using rational matrices. It exhaustively tested **480** distinct anchored two-external-vertex simple attachment schemes, of which exactly **28** had zero contact and **452** had strictly positive contact, agreeing with the graph-theoretic zero-set criterion. Authenticated CHAD execution receipt \`060b81da42f74f09bc29a9fb79ebea1f\` returned PASS. The general-order and arbitrary finite-network statements are proved by the energy and Gaussian identities above; the finite regression is a hostile example check, not the proof.

**Achieved:** a nontrivial **two-level quotient-elimination associativity theorem** for the *same differentiated singular source* transported through a multi-vertex smooth Gaussian complement, with a sharp effective-energy criterion and an exact six-vertex contact. This is a stronger positive result than R2/061's single external quotient and is compatible with the non-continuity example R2/059.

**Still open:** a genuinely *nested pair of differentiated singular source counterterms* or two overlapping singular source diagonals, and a consistent full-graph forest/BV structure. The theorem here does **not** multiply two singular deltas, derive the *full* six-vertex forest counterterm, or assert global BPHZ, BV/QME, Weiss descent or higher Ext. Keep [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) open.

**Next mathematical obligation:** select a proper five-vertex 1PI graph whose intrinsic overall counterterm contains nonzero normal second derivatives, embed it as a proper nested source inside a six-vertex graph, and prove the source-wise *prepared forest* identity including derivatives of smooth complement factors. Compare the full nested and collapsed calculations with exact-head independent mathematical critique; do not treat this two-quotient module identity as such a forest theorem.
