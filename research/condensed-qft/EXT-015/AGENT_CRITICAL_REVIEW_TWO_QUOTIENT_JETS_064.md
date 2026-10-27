# EXT-015 REACH / 064 — exact-head critical audit of multi-quotient normal-jet transport

**Verdict: BOUNDED ACCEPT.** A distinct logical GCL mathematical critic pass on [R2/063 source PR #2862](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2862), exact author HEAD \`7c1b1dc89e5c5527f24a611cabaa741492a18be1\`, R2/063 source blob \`dc8ebc1534bb5a4d851a424632ea0277fb02cd0e\`, and [standard-library exact fixture](fixtures/check_two_quotient_jet_associativity_063.py) blob \`8ace6119c88416a32d72b72d3ea22d1051440554\`. The logical critic and author use the established GCL same-authentication model; this is not an independent external referee or MATHCERT certification. The source PR's protected merge is a separate condition.

## 1. Mathematical scope and potentially invalid shortcuts

The source is a **single** fixed K4 singular normal delta jet with nonzero second-derivative coefficient. It is multiplied by *smooth positive-regulator Gaussian complement edges* and integrated over external quotient vertices. No two singular diagonals are multiplied. The theorem proves consistency of arbitrary orders of **Gaussian external-vertex elimination**, not independent renormalization of two overlapping singular subgraphs. Calling it a two-singular-source Zimmermann forest theorem would be incorrect.

Hostile failures considered:

1. Passing from a delta *value* at its collision point to a differentiated source jet without retaining the smooth complement Hessian.
2. Interchanging a nonintegrable quotient Gaussian integral with a singular distribution; this is why every external connected component must be anchored to a source vertex.
3. Losing determinant factors or powers of the regulator in sequential Schur complements.
4. Mistaking zero contact for a criterion about the number of edges rather than the number of **distinct attached source vertices per external component**.
5. Treating a finite rational fixture as proof for every external graph or as evidence of a global BV/QME identity.

**Decision:** The statement correctly restricts all five potential failure modes.

## 2. Independent distribution and Schur audit

With K4 source covariance $H=(I+J)/4$ and counterterm

$$
C_\epsilon=A\epsilon^{-3}\delta_y+
B\epsilon^{-1}(H:\partial_y^2)\delta_y,
\tag{64.1}
$$

write the smooth complement in relative coordinates $(y,q)$ as

$$
F_\epsilon=(2\pi)^{-k/2}\epsilon^{-k}
\exp[-(y^TDy-2y^TCq+q^TMq)/(2\epsilon^2)].
\tag{64.2}
$$

The anchored-component hypothesis gives $M\succ0$. Gaussian completion of squares yields the exact quotient normalization and reduced quadratic form

$$
Z=(2\pi)^{-(k-m)/2}(\det M)^{-1/2},
\qquad S=D-CM^{-1}C^T.
\tag{64.3}
$$

The quotient Gaussian has value $Z\epsilon^{m-k}$, zero first normal derivative, and second-normal trace $-Z\epsilon^{m-k-2}\mathrm{tr}(HS)$ at $y=0$. Independently evaluate the pairing with a compact source test $\varphi$:

$$
\langle G_\epsilon C_\epsilon,\varphi\rangle
=Z\left[
(A-B\Theta)\epsilon^{m-k-3}\varphi(0)
+B\epsilon^{m-k-1}(H:\partial_y^2)\varphi(0)
\right],
\quad\Theta=\mathrm{tr}(HS).
\tag{64.4}
$$

The sign of the Hessian contact is **minus B** because the Gaussian Hessian is negative at zero; the inherited K4 $B$ is negative, so the correction is positive. There is no omitted first-derivative term after complete quotient integration since the integrated Gaussian is even in $y$.

**Decision:** ACCEPT (63.6)–(63.8). The determinant, regulator powers, sign and derivative-order filtration are correct.

## 3. Independent geometric positivity and exact zero set

The reduced quadratic form has a variational characterization

$$
y^TSy=\min_q\sum_{e\ \mathrm{complement}}
(\text{difference of its two endpoint coordinates})^2.
\tag{64.5}
$$

Consequently $S\succeq0$. As $H\succ0$, $\mathrm{tr}(HS)=0$ iff $S=0$. This occurs if each connected external-vertex component is attached to a single original source vertex: every external position can then equal its source attachment and **all** new edge energies vanish regardless of source positions. Conversely, if an external component attaches to two distinct original K4 vertices, choose different source positions at those endpoints. A path through that component necessarily carries strictly positive minimum Dirichlet energy, so $S\ne0$ and $\Theta>0$.

**Hostile qualification:** Direct source-to-source complement edges are excluded; permitting them would require treating a direct edge as another connectivity path between source vertices and revising the stated criterion. A completely unanchored external component is excluded because the free translational mode would make $\det M=0$. The theorem does not falsely claim the criterion in either excluded case.

**Decision:** ACCEPT (63.11)–(63.12).

## 4. Two elimination orders and mixed normal probes

For the six-vertex graph with new labeled edges $15,25,56,36$, independently derive

$$
M=\begin{pmatrix}3&-1\\-1&2\end{pmatrix},\quad
M^{-1}=\frac15\begin{pmatrix}2&1\\1&3\end{pmatrix},\quad
\det M=5.
\tag{64.6}
$$

The source-to-quotient incidence matrix has columns $c_t=(1,1,0)^T$ and $c_s=(0,0,1)^T$. Contract with $H$ to obtain the exact losses:

$$
\begin{aligned}
t\rightarrow s:\quad&
\frac{c_t^THc_t}{3}=\frac12,\quad
\frac{(c_s+c_t/3)^TH(c_s+c_t/3)}{5/3}=\frac35,\\
s\rightarrow t:\quad&
\frac{c_s^THc_s}{2}=\frac14,\quad
\frac{(c_t+c_s/2)^TH(c_t+c_s/2)}{5/2}=\frac{17}{20}.
\end{aligned}
\tag{64.7}
$$

Both loss sums equal $11/10$, while $\mathrm{tr}(HD)=3/2$. Hence $\Theta=2/5$ regardless of the legal integration order. The external-quotient normalization is in each order $Z=1/(2\pi\sqrt5)$. Thus the source-contact increment beyond freezing the quotient value is

$$
-BZ\Theta\,\epsilon^{-5}\delta_y
=\frac{7\sqrt{10}}{7200\pi^{5/2}}\epsilon^{-5}\delta_y.
\tag{64.8}
$$

This constant is **not** the R2/059 parallel-edge contact nor the R2/061 one-external-vertex contact; the geometry and quotient determinant are different.

For an adversarial mixed test that locally equals $y_1t$ or $y_1s$, source delta and pure second-normal derivative of the test alone vanish. The Leibniz *cross term*, involving one derivative of the smooth complement, survives. Directly using $\mathbb E[qq^T]=\epsilon^2M^{-1}$ gives coefficients $2(HCM^{-1})_{1t}=7/10$ and $2(HCM^{-1})_{1s}=3/5$. Their nonzero and unequal values exclude any scalar-only or premature quotient-value insertion rule. The test $y_1^2$ independently recovers the unchanged intrinsic second-normal-derivative coefficient because $(H:\partial_y^2)y_1^2=1$.

**Decision:** ACCEPT the exact graph witness and four hostile probes.

## 5. Verification and release boundary

The standard-library [R2/063 fixture](fixtures/check_two_quotient_jet_associativity_063.py) uses exact \`Fraction\` linear algebra, not fitted floating-point data. Authenticated CHAD replay \`060b81da42f74f09bc29a9fb79ebea1f\` PASS: two Schur elimination orders, fixed determinant 5, effective contact $\Theta=2/5$, the exact positive radical coefficient, two mixed normal probes and **480** anchored simple two-external-vertex edge patterns (28 zero-contact; 452 positive-contact), with no unexplained cases. R2/063 mathematical Markdown preflight \`80558f172d3b4a458249a2237efc9a69\` PASS. The finite fixture is a hostile check of the graph formulas, not a substitute for the variational all-network proof or Gaussian distribution argument.

**Final verdict: ACCEPT R2/063 as a bounded multi-quotient Gaussian delta-jet theorem with exact external-elimination associativity.** Do not infer a coherent *two-singular-source* forest recursion or generalized BV/QME statement. The next substantive task remains the construction of an intrinsic derivative-bearing **proper five-vertex** source and its nested insertion into a six-vertex graph, with exact all-proper-subgraph forest bookkeeping. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains open.

**Protected admission:** first merge source PR #2862; then merge the exact-head review PR created for this document. Read back both plus the fixture from protected \`main\` before declaring R2/063–064 admitted.
