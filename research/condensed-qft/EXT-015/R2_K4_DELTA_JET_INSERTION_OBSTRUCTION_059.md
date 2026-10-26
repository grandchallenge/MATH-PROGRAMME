# EXT-015 REACH-R2 / 059 — a derivative-counterterm contact obstruction under cyclic edge insertion

**Status:** bounded mathematical source candidate; separate exact-head critical review and protected admission required. This is a **negative mathematical result** beyond the derivative-free source-counterterm calculation in [R2/057](R2_FULL_DOUBLE_BRIDGE_LOCAL_FOREST_057.md) and [R2/058](AGENT_CRITICAL_REVIEW_FULL_DOUBLE_BRIDGE_FOREST_058.md). The previously reviewed [K4 nested-forest calculation R2/051](R2_K4_NESTED_OVERLAP_FOREST_051.md) supplies a rank-three source with a **nonzero derivative-of-delta overall counterterm**. Adding any parallel Gaussian edge shows two exact failures of unqualified source-level transport: freezing the complement kernel at the contracted point loses an order-four local pole, and strong distributional convergence of the renormalized K4 source is **not** preserved by the same-scale new edge factor.

**Scope:** normalized unit Gaussians, one common regulator scale, labeled K4 graph plus one repeated edge, fixed zero-finite-part K4 subtraction scheme. This does not prove a BV/QME anomaly or the impossibility of a fully constructed graph-forest counterterm scheme. It identifies exactly the extra delta-jet Leibniz term such a scheme must include.

## 1. Source and target

Let $K_4$ have vertices $1,2,3,4$ and one labeled Gaussian delta edge between every unordered pair, with

$$
\kappa_\epsilon(t)=\epsilon^{-1}(2\pi)^{-1/2}
\exp(-t^2/(2\epsilon^2)).
\tag{59.1}
$$

Fix $x_4$ as root and relative coordinates $y=(x_1-x_4,x_2-x_4,x_3-x_4)$. Put

$$
Q=4I-J,\qquad
Q^{-1}=\frac14(I+J),\qquad
L=\sum_{i,j=1}^3(Q^{-1})_{ij}\partial_{y_i}\partial_{y_j},
\qquad \delta=\delta(y).
\tag{59.2}
$$

The complete prepared K4 amplitude $\overline R_{K_4,\epsilon}$ is the original six-edge Gaussian product minus all four intrinsic triangle, three square, and six *prepared* theta source counterterm insertions; the 18 nested forests are already included in the prepared theta coefficients. The protected Theorem 51.3 gives the actual K4 **overall local subtraction**

$$
C_{K_4,\epsilon}
=\frac A{\epsilon^3}\delta+
\frac B\epsilon L\delta,
\quad
A=\frac1{\pi^{3/2}}
\left(\sqrt3-\frac34+\frac{5\sqrt2}{48}\right),
\quad
B=-\frac{7\sqrt2}{288\pi^{3/2}}.
\tag{59.3}
$$

Set $R_{K_4,\epsilon}=\overline R_{K_4,\epsilon}-C_{K_4,\epsilon}$. Previous work proves $R_{K_4,\epsilon}\to0$ strongly on **fixed** smooth compact test families, with remainder $O_{\mathcal D'}(\epsilon)$.

Choose any existing edge $e=\{u,v\}$ and insert a **new distinctly labeled parallel edge** with factor

$$
f_{e,\epsilon}(y)=\kappa_\epsilon(y_u-y_v),
\qquad y_4=0.
\tag{59.4}
$$

The seven-edge multigraph has cycle rank four. The six possible choices of $e$ are related by the K4 automorphism group.

## 2. The missing derivative contact term

**Lemma 59.1 (local Gaussian two-jet insertion).** Let $a\in\mathbb R^3$ be the root-coordinate incidence vector of the new edge, so $y_u-y_v=a\cdot y$ and $a^TQ^{-1}a=1/2$. With $\kappa_0=(2\pi)^{-1/2}$, the exact distributional product at every positive $\epsilon$ is

$$
\boxed{
f_{e,\epsilon}C_{K_4,\epsilon}
=\kappa_0\left[
\frac{A-B/2}{\epsilon^4}\delta+
\frac B{\epsilon^2}L\delta
\right].
}
\tag{59.5}
$$

The *naive contracted-value prescription* $f_{e,\epsilon}(0)C_{K_4,\epsilon}$ incorrectly omits

$$
\boxed{
f_{e,\epsilon}C_{K_4,\epsilon}
-f_{e,\epsilon}(0)C_{K_4,\epsilon}
=\frac{7}{576\pi^2}\epsilon^{-4}\delta.
}
\tag{59.6}
$$

**Proof.** For every smooth $f$ and constant-coefficient $L=Q^{-1}:\partial^2$, the distributional Leibniz formula reads

$$
f\,L\delta=f(0)L\delta
-2\sum_{i,j}(Q^{-1})_{ij}(\partial_i f)(0)\partial_j\delta
+(Lf)(0)\delta.
\tag{59.7}
$$

This follows by evaluating $L(f\varphi)(0)$ on arbitrary smooth compactly supported tests $\varphi$. Here $\nabla f_{e,\epsilon}(0)=0$, $f_{e,\epsilon}(0)=\kappa_0/\epsilon$, and

$$
\partial_i\partial_j f_{e,\epsilon}(0)
=-\kappa_0\epsilon^{-3}a_i a_j,\qquad
(Lf_{e,\epsilon})(0)
=-\frac{\kappa_0}{2\epsilon^3}.
\tag{59.8}
$$

To verify the effective resistance, with $Q^{-1}=(I+J)/4$, each edge incidence vector is either $e_i-e_j$ or $e_i$, and each has quadratic form $a^TQ^{-1}a=1/2$. Substitution into (59.7) and (59.3) gives (59.5). Since $-\kappa_0 B/2=7/(576\pi^2)$, (59.6) follows. This is **a local contact contribution**, not a finite-difference numerical artifact. $\square$

**Hostile probes:** A test $\varphi$ that is one near the origin detects the omitted scalar term. For a test agreeing with $(y_u-y_v)^2$ near the origin, the scalar delta vanishes and $L\varphi(0)=2a^TQ^{-1}a=1$, giving the nonzero second-jet coefficient $-\frac7{288\pi^2}\epsilon^{-2}$. A scalar-only correction cannot reproduce that quadratic probe.

## 3. The stronger non-continuity obstruction

**Theorem 59.2 (same-scale edge insertion does not preserve renormalized zero limit).** For every choice of new parallel edge $e$,

$$
R_{K_4,\epsilon}\longrightarrow0
\quad\hbox{strongly in }\mathcal D'(\mathbb R^3),
\tag{59.9}
$$

yet for any $\varphi\in C_c^\infty(\mathbb R^3)$ identically one in a neighborhood of $0$,

$$
\boxed{
\lim_{\epsilon\downarrow0}
\epsilon^4\langle f_{e,\epsilon}R_{K_4,\epsilon},\varphi\rangle
=\frac1{\pi^2}\left(
\frac{53}{576}+\frac{\sqrt6}{48}-\frac{\sqrt3}{12}
\right)\ne0.
}
\tag{59.10}
$$

In particular $f_{e,\epsilon}R_{K_4,\epsilon}$ fails to have a finite distributional limit; on that probe it diverges at least as $\epsilon^{-4}$. The exact coefficient is negative (approximately $-1.2926421\cdot10^{-3}/\pi^2$).

**Proof.** Graph symmetry reduces to $e=\{1,2\}$. Because the new edge adds an independent rank-one incidence contribution $aa^T$ to the reduced Laplacian, the matrix determinant lemma gives

$$
\tau(K_4+e)=\det(Q+aa^T)=16(1+1/2)=24.
\tag{59.11}
$$

Thus the bare seven-edge product, integrated against a test one near the diagonal, contributes $\epsilon^{-4}/(8\sqrt6\pi^2)$ plus a Gaussian-exponentially small cutoff error. Consider the complete *prepared* K4 forest amplitude multiplied by $f_{e,\epsilon}$, still before applying $C_{K_4,\epsilon}$. Every term is a smooth positive-regulator kernel on its quotient together with independent collision deltas. The integrals near the diagonal are exact:

- **Four triangles:** exactly two contain both endpoints of $e$. Each contributes $c_3\kappa_0 b_3=1/(12\pi^2)$ at order $\epsilon^{-4}$; each of the other two changes the quotient from three to four parallel edges and contributes $c_3 b_4=1/(8\sqrt3\pi^2)$. Here $c_3=1/\sqrt{6\pi}$, $b_3=\int\kappa^3=1/(2\pi\sqrt3)$, and $b_4=\int\kappa^4=1/(4\sqrt2\pi^{3/2})$.
- **Three squares:** each spans all four vertices and gives $c_4\kappa_0^3=1/(8\pi^2)$, where $c_4=1/\sqrt{8\pi}$.
- **Six prepared theta sources:** each spans all four vertices and gives $g_\Theta\kappa_0^2$, where $g_\Theta=\pi^{-1}(1/(4\sqrt2)-1/\sqrt6-1/4)$ is the source-local prepared theta coefficient from R2/051, not the unprepared primitive Gaussian constant.

All proper terms are subtracted. Hence the coefficient of $\epsilon^{-4}$ in $f_{e,\epsilon}\overline R_{K_4,\epsilon}$ is

$$
\begin{aligned}
P={}&\frac1{\pi^2}\left[
\frac1{8\sqrt6}-\frac16-\frac1{4\sqrt3}
-\frac38-6\left(\frac1{8\sqrt2}-\frac1{2\sqrt6}-\frac18\right)\right]\\
={}&\frac1{\pi^2}\left(
\frac5{24}-\frac{3\sqrt2}8-\frac{\sqrt3}{12}
+\frac{25\sqrt6}{48}\right).
\end{aligned}
\tag{59.12}
$$

By Lemma 59.1, the coefficient in $f_{e,\epsilon}C_{K_4,\epsilon}$ is

$$
S=\frac{\kappa_0(A-B/2)}{1}
=\frac1{\pi^2}\left(
\frac{67}{576}-\frac{3\sqrt2}8+\frac{\sqrt6}2\right).
\tag{59.13}
$$

Subtracting $S$ from $P$ gives exactly the right side of (59.10). The constant is nonzero because the rational numbers $1,\sqrt3,\sqrt6$ are linearly independent over $\mathbb Q$; its negativity can also be checked with rational enclosing bounds for the square roots. The support of each Gaussian term is exponentially concentrated near the full collision diagonal, so replacing the constant test by a compact test equal to one there incurs exponentially small Gaussian tails, even after the displayed negative powers. For delta derivatives, the product-with-test identity (59.7) is exact. Therefore the limit in (59.10) holds.

There is no contradiction with the source limit (59.9): multiplying by $f_{e,\epsilon}$ evaluates the source remainder against an $\epsilon$-dependent test whose derivatives grow as negative powers of $\epsilon$; such tests are not a bounded subset of $\mathcal D$. $\square$

**Warning on vocabulary:** The term in (59.6) is a contact correction to an *incorrect frozen-complement rule*. The term in (59.10) is a demonstrated continuity obstruction for *one renormalized graph multiplied by a new same-scale edge*. Neither is by itself a BV cohomological anomaly or a proof that no full-graph BPHZ forest recursion exists.

## 4. Implications and sharp next obligation

The source-local K4 counterterm library is still correct: the need for an **extra Leibniz contact** does not permit redefining its coefficients to fit each containing supergraph. Instead, an admissible edge-insertion operation on delta jets must retain the full **jet of the regulated complement kernel**, not just its coincident value. For a second-derivative source counterterm, that includes its Hessian at the source diagonal, which produces a new scalar contact divergence of leading order. Likewise, the $O(\epsilon)$ remainder of an already renormalized graph is not uniformly small under multiplication by $\kappa_\epsilon$.

**Next mathematical gate:** on a family that includes rank-three sources and their one-edge extensions, define a compatible filtered local-jet insertion action and the necessary higher overall counterterms, or prove that the desired locality/factorization law fails under a specified set of module contracts. The exact R2/059 fixture [check_k4_edge_jet_obstruction_059.py](fixtures/check_k4_edge_jet_obstruction_059.py) verifies the six labeled edge cases, matrix-tree determinant 24, $a^TQ^{-1}a=1/2$, contact shift $7/(576\pi^2)$, each forest contribution, and the nonzero residual (59.10) using rational surd arithmetic; it is not a substitute for the analytic proof above.

**Claim boundary:** Theorem 59.2 concerns a fixed Gaussian source and a source-renormalize-then-insert operation, **not** full renormalization of the entire seven-edge supergraph. Do not claim failure of all possible forest counterterms or global BV nilpotence, quantum master equations, normal-topology Weiss descent, or liquid higher Ext from these computations. The parent research [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains open.
