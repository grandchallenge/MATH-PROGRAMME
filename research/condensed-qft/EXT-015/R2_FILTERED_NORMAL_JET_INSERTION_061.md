# EXT-015 REACH-R2 / 061 — exact filtered normal-jet insertion and a positive attachment criterion

**Status:** bounded mathematical source candidate; exact-head critical review and protected admission required. This is a **positive construction** following the obstruction of [R2/059](R2_K4_DELTA_JET_INSERTION_OBSTRUCTION_059.md) and [R2/060](AGENT_CRITICAL_REVIEW_K4_EDGE_JET_OBSTRUCTION_060.md). It constructs the correct action of positive-regulator complement kernels on **all finite-order normal delta jets**, proves order independence under successive edge insertions, and exactly evaluates the first genuine partial-diagonal example: the K4 counterterm attached to a new fifth vertex by Gaussian edges. For arbitrary external edge multiplicities, its quotient-integrated scalar contact is proportional to a weighted sum of K4 effective resistances and vanishes precisely when every attachment shares the same original source vertex.

**Not claimed:** a renormalization functor on all forests, singular products of overlapping diagonals, a full BV operator and square-zero/QME relation, normal-topology Weiss descent, or higher liquid Ext.

## 1. Local jets form a module, not a value-evaluation rule

Let $y\in\mathbb R^d$ be linear coordinates normal to a fixed source collision diagonal; $t$ denotes surviving quotient coordinates. Define the finite normal delta-jet space of order at most $m$:

$$
\mathcal J_m
=\left\{\sum_{|\alpha|\le m}c_\alpha(t)\partial_y^\alpha\delta(y):
c_\alpha\in C^\infty(t)\right\}.
\tag{61.1}
$$

Coefficients may depend on a positive regulator $\epsilon$; in the Gaussian applications they are smooth for every $\epsilon>0$.

**Theorem 61.1 (exact normal-jet module action).** Multiplication by any smooth complement $f(y,t)$ defines the finite action

$$
\boxed{
\mathcal M_f[\partial_y^\alpha\delta_y]
=\sum_{\beta\le\alpha}(-1)^{|\beta|}
{\alpha\choose\beta}
(\partial_y^\beta f)(0,t)\,
\partial_y^{\alpha-\beta}\delta_y.
}
\tag{61.2}
$$

It obeys, **as an exact identity of distributions**,

$$
\mathcal M_f\mathcal M_g=\mathcal M_g\mathcal M_f
=\mathcal M_{fg},\qquad
\mathcal M_1=\mathrm{id},\qquad
\mathcal M_f\mathcal J_m\subseteq\mathcal J_m.
\tag{61.3}
$$

Thus any finite number of individually smooth regulated Gaussian edges can be inserted in any order into the *same fixed source jet* without ambiguity. A permitted change of linear normal coordinates transports the action covariantly because it is just ordinary multiplication of distributions.

**Proof.** Pair $\partial_y^\alpha\delta_y$ with $f(y,t)\varphi(y,t)$, apply the multivariate Leibniz formula at $y=0$, and compare signs with the distributional definition of derivatives of delta. Composition follows from associativity of multiplication of smooth functions; it also follows by collecting their ordinary jets through order $m$. No product of two singular diagonal distributions occurs. Every term reduces the derivative order by $|\beta|$, so the filtration is preserved. $\square$

For $m=2$ and a symmetric matrix $H$, abbreviate $L_H=H:\partial_y^2$. The useful explicit specialization of (61.2) is

$$
\boxed{
f\,L_H\delta_y=f_0 L_H\delta_y
-2(H\nabla_yf)_0\cdot\nabla_y\delta_y
+(L_Hf)_0\delta_y,
\quad f_0=f(0,t).
}
\tag{61.4}
$$

**Crucial distinction:** quotient-value insertion $f_0 L_H\delta$ discards the normal *first* and *second* jets of $f$. It is valid only under additional vanishings; its general failure was quantified in R2/059.

For a product of $k$ regulated normalized Gaussian edges the normal derivatives in (61.2) are explicit Hermite polynomials in quotient coordinates divided by regulator powers. Therefore the action is finite and admits a regulator-degree filtration; this is an exact algebraic statement, **not** a uniform estimate on arbitrary changing test families.

## 2. K4 source and nontrivial partial diagonal

Use the [protected R2/051](R2_K4_NESTED_OVERLAP_FOREST_051.md) K4 source with original vertices $1,2,3,4$, root $x_4$, internal relative coordinates

$$
y=(x_1-x_4,x_2-x_4,x_3-x_4),\qquad
Q=4I-J,\quad H=Q^{-1}=\tfrac14(I+J),
\quad L=H:\partial_y^2.
\tag{61.5}
$$

The K4 **prepared overall local counterterm** is fixed by its source, independently of any containing graph:

$$
C_{K4,\epsilon}
=A\epsilon^{-3}\delta_y+B\epsilon^{-1}L\delta_y,
\quad
A=\pi^{-3/2}\left(\sqrt3-\tfrac34+\tfrac{5\sqrt2}{48}\right),
\quad B=-\pi^{-3/2}\tfrac{7\sqrt2}{288}.
\tag{61.6}
$$

Attach a fifth vertex $x_5$ by $n_j\ge0$ new separately labeled Gaussian edges from original source vertex $j$ to vertex 5, with $k=\sum_{j=1}^4n_j\ge1$, and set $t=x_5-x_4$, $y_4=0$. All edges use the same positive-regulator normalized Gaussian

$$
\kappa_\epsilon(u)=(2\pi)^{-1/2}\epsilon^{-1}e^{-u^2/(2\epsilon^2)}.
\tag{61.7}
$$

The smooth *complement* to the K4 source is

$$
F_{n,\epsilon}(y,t)
=\prod_{j=1}^4\kappa_\epsilon(y_j-t)^{n_j}.
\tag{61.8}
$$

Write $v=(n_1,n_2,n_3)^T$ and $D=\operatorname{diag}(n_1,n_2,n_3)$. The exact normal jets at the partial source collision are

$$
\begin{aligned}
F_0(t)&=(2\pi)^{-k/2}\epsilon^{-k}
  \exp[-kt^2/(2\epsilon^2)],\\
(\nabla_yF)_0&=\frac{t}{\epsilon^2}vF_0,\\
(D_y^2F)_0&=F_0\left[
  \frac{t^2}{\epsilon^4}vv^T-\frac1{\epsilon^2}D\right].
\end{aligned}
\tag{61.9}
$$

**Theorem 61.2 (exact positive-regulator partial-diagonal insertion).** Substituting (61.9) into the *source-fixed* counterterm gives

$$
\boxed{
\begin{aligned}
F_{n,\epsilon}C_{K4,\epsilon}
={}&F_0\Bigg\{
\left[A\epsilon^{-3}
+B\epsilon^{-1}\left(
\frac{t^2}{\epsilon^4}v^THv
-\frac1{\epsilon^2}\operatorname{tr}(HD)
\right)\right]\delta_y\\
&\hspace{1em}-\frac{2Bt}{\epsilon^3}(Hv)\cdot\nabla_y\delta_y
+\frac B\epsilon L\delta_y
\Bigg\}.
\end{aligned}
}
\tag{61.10}
$$

The formula is valid as a distribution on the **partial diagonal** $y=0$ with the surviving quotient variable $t$, for every $\epsilon>0$ and all nonnegative integer multiplicities $n$. It depends on the complement only through its normal two-jet. If the $k$ complement edges are inserted one at a time and in any order, formula (61.3) gives exactly the same result.

**Proof.** The logarithmic gradient of (61.8) is $-\epsilon^{-2}\sum_jn_j(y_j-t)e_j$; its log Hessian is $-\epsilon^{-2}D$. Differentiate once and twice at $y=0$ to obtain (61.9), then apply (61.4) to the second-jet part of (61.6) and ordinary multiplication to its scalar part. Order independence is exactly Theorem 61.1. $\square$

In particular, the quotient-variable dependence produces the first-derivative-delta term proportional to $t(Hv)$, which generally vanishes only at $t=0$, **not** as a partial-diagonal distribution.

## 3. Integrating the external coordinate: exact resistance criterion

Integrate out $t$, holding test functions in $y$ fixed. This is well defined for the displayed Gaussian distribution because its coefficients decay rapidly in $t$ at every $\epsilon>0$. Define

$$
K_k=(2\pi)^{-(k-1)/2}k^{-1/2},\qquad
S_n=D-\frac1k vv^T.
\tag{61.11}
$$

Completing the square in (61.8) gives the exact equality of smooth functions

$$
\int_{\mathbb R}F_{n,\epsilon}(y,t)\,dt
=K_k\epsilon^{1-k}
\exp\left[-\frac{y^TS_ny}{2\epsilon^2}\right].
\tag{61.12}
$$

This quotient kernel is a **possibly degenerate** Gaussian as a function of $y$, but it is smooth for every $\epsilon>0$; the source delta jet makes its derivative evaluation unambiguous. Using (61.4) after the integral,

$$
\boxed{
\int_{\mathbb R}F_{n,\epsilon}C_{K4,\epsilon}\,dt
=K_k\left[
(A-B\Theta_n)\epsilon^{-(k+2)}\delta_y
+B\epsilon^{-k}L\delta_y
\right],
\quad \Theta_n=\operatorname{tr}(HS_n).
}
\tag{61.13}
$$

**Theorem 61.3 (positive resistance formula and complete zero-contact criterion).** For the K4 covariance $H$,

$$
\boxed{
\Theta_n
=\frac1k\sum_{1\le i<j\le4}n_in_j
(e_i-e_j)^TH(e_i-e_j)
=\frac{1}{2k}\sum_{i<j}n_in_j
\ge0,
}
\tag{61.14}
$$

where $e_4=0$ in the three normal coordinates. In particular,

$$
\boxed{
\Theta_n=0\quad\Longleftrightarrow\quad
\text{all }k\text{ external edges meet the same K4 vertex}.
}
\tag{61.15}
$$

The rule that **freezes the complement at the source collision before applying $L\delta$** omits the exact integrated scalar contact

$$
\boxed{
\mathfrak C_{n,\epsilon}
=-B K_k\Theta_n\,\epsilon^{-(k+2)}\delta_y.
}
\tag{61.16}
$$

It has a strictly positive coefficient whenever the external attachments meet at least two distinct source vertices, because the inherited source coefficient $B$ is negative. No redefinition of $A$ or $B$ is needed in the supergraph.

**Proof.** Introduce the four source-incidence vectors $e_i\in\mathbb R^3$, $e_4=0$. The weighted-variance identity reads

$$
S_n=\frac1k\sum_{i<j}n_in_j(e_i-e_j)(e_i-e_j)^T.
\tag{61.17}
$$

Since $H=(I+J)/4$, every distinct original-vertex pair in K4 has effective resistance $(e_i-e_j)^TH(e_i-e_j)=1/2$. Contract (61.17) with $H$ to get (61.14). Every summand is nonnegative and positive exactly for attachments at different vertices, yielding (61.15). For (61.13), the quotient kernel of (61.12) has value $K_k\epsilon^{1-k}$, vanishing first normal derivative at zero and normal Hessian $-K_k\epsilon^{-k-1}S_n$. The Leibniz rule (61.4) then gives exactly the scalar shift $-BK_k\Theta_n\epsilon^{-(k+2)}$ and the unchanged leading jet term. $\square$

This is a **graph-geometric** criterion: the missing local correction is weighted by pairwise source effective resistances between attachment points, rather than a constant chosen ad hoc for the containing graph.

## 4. A two-edge collision, with four independent hostile probes

Take the first nontrivial fifth-vertex graph with one edge $15$ and one edge $25$, i.e. $n=(1,1,0,0)$, $k=2$. This new graph has five vertices and eight labeled edges, with cycle rank four. Here

$$
v=(1,1,0),\quad
Hv=(3/4,3/4,1/2),\quad
v^THv=3/2,\quad
\operatorname{tr}(HD)=1,\quad
\Theta_n=1/4,\quad K_2=1/(2\sqrt\pi).
\tag{61.18}
$$

Thus before quotient integration, with $F_0=\kappa_\epsilon(t)^2$,

$$
\begin{aligned}
F_{n,\epsilon}C_{K4,\epsilon}
=F_0\Big[&
\left(A\epsilon^{-3}
+B\epsilon^{-1}(\tfrac{3t^2}{2\epsilon^4}
-\epsilon^{-2})\right)\delta_y\\
&-\frac{2Bt}{\epsilon^3}
(\tfrac34\partial_{y_1}
+\tfrac34\partial_{y_2}
+\tfrac12\partial_{y_3})\delta_y
+\frac B\epsilon L\delta_y\Big].
\end{aligned}
\tag{61.19}
$$

After quotient integration the resulting scalar shift beyond the frozen-complement rule is

$$
\boxed{
\mathfrak C_{(1,1,0,0),\epsilon}
=\frac{7\sqrt2}{2304\pi^2}
\,\epsilon^{-4}\delta_y\ne0.
}
\tag{61.20}
$$

Set $A_*=\pi^{3/2}A$ and $B_*=\pi^{3/2}B$. Choose compact smooth test functions agreeing with the displayed polynomials near the full diagonal $(y,t)=0$. Up to exponentially small Gaussian-tail errors, the **exact leading coefficients** of their pairing with the inserted source, after extracting $\pi^{-2}$, are

| Test polynomial $\varphi(y,t)$ | Laurent power | Coefficient after extracting $\pi^{-2}$ |
| --- | --- | --- |
| $1$ | $\epsilon^{-4}$ | $(A_*-B_*/4)/2$ |
| $t^2$ | $\epsilon^{-2}$ | $A_*/4+5B_*/16$ |
| $y_1t$ | $\epsilon^{-2}$ | $3B_*/8$ |
| $y_1^2$ | $\epsilon^{-2}$ | $B_*/2$ |

For instance the **mixed probe** $y_1t$ detects the term involving $\nabla_y\delta_y$ that any quotient-value-only insertion misses; it is nonzero and equals $-7\sqrt2/(768\pi^2)\epsilon^{-2}$. The quadratic normal probe $y_1^2$ isolates the unchanged source second jet. The constant test distinguishes the new scalar contact in (61.20). These are genuinely different constraints on an insertion rule.

**Proof.** For the two-spoke quotient Gaussian, $\int F_0(t)dt=1/(2\sqrt\pi\epsilon)$ and its variance is $\epsilon^2/2$. The even moments satisfy $\mathbb E[(t/\epsilon)^{2m}]=(2m-1)!!/2^m$. Pair (61.19) with each displayed test and differentiate only in $y$. The four coefficients follow by exact integration, while the odd terms vanish on the specified tests. A cutoff equal to one around the origin leaves only Gaussian-exponentially small tails, smaller than every Laurent power. $\square$

## 5. Algebraic regression and precise scope

The [exact fixture 061](fixtures/check_filtered_normal_jet_insertion_061.py) uses only Python's standard library and rational arithmetic. It checks **189** distinct nonzero attachment multiplicity vectors $n$ with $k\le6$, proves the rational K4 resistance/variance identity and the exact zero-contact criterion on those examples, and exhaustively checks insertion-order independence of direct and sequential **normal two-jets** for five hostile multisets, including repeated and branching attachments. It directly evaluates eight independent polynomial monomial pairings and checks the radical-basis scalar contact (61.20) exactly, without floating point.

**Proof versus computation:** Theorem 61.1 is the full all-orders distributional module law; the fixture exercises its second-order Gaussian instance. Theorems 61.2–61.3 are algebraic/analytic identities for the **fixed K4 source embedded into a fifth-vertex Gaussian-edge family**; the fixture independently checks finite combinatorics and moments, not an unrestricted graph-forest induction.

**Achieved:** A genuinely positive finite normal-jet representation that makes successive smooth edge insertions order-independent, retains quotient-dependent first normal derivatives, and produces an exact source-intrinsic scalar contact weighted by effective resistance after quotient integration. The earlier R2/059 non-continuity result is respected: ordinary strong distribution convergence on fixed tests does not imply continuity under all same-scale Gaussian multipliers.

**Still open:** Extending this source-local jet module to families with two *overlapping singular source diagonals* and proving a coherent full-graph Zimmermann forest recursion with higher derivative counterterms, plus factor-local Wick-to-delta versus global BV/QME compatibility and the separate Weiss/liquid obligations of REACH-R2 [#2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797).

**Next theorem-level gate:** prove a two-level nested differentiated-counterterm insertion identity on a connected five- or six-vertex graph, including the correct Leibniz terms of the quotient complement, and decide whether the prepared forest result is invariant under two different legal nesting orders. Do not turn this into an operational or governance-only task.
