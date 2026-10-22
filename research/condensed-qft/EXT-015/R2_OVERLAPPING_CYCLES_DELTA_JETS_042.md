# EXT-015 REACH-R2 / 042 — overlapping cycles, nested subtractions and delta-jet locality

**Disposition: NEW BOUNDED MATHEMATICAL CANDIDATE; critical audit required.** Solves an explicit overlapping-subdivergence case left open by [041](R2_COLLISION_FORESTS_AND_CYCLE_COUNTERTERM_041.md), and proves a general *whole-graph* diagonal Taylor subtraction theorem for connected graphs with arbitrarily differentiated delta edges. The overlapping test implements a genuine nonmultiplicative three-subgraph subtraction and a final overall local counterterm. It does **not** establish a universal Zimmermann forest recursion compatible with all graph insertion, completed Costello–Gwilliam B.6 differentiable Weiss descent, a globally smooth BV operator on all collision distributions, or interacting quantum master equations.

**Starting protected main:** c576dca05260c35c8f150fa5c298353a47a591ce, 2026-10-22; original 041 research branch head b476cdf392f04c87145de1cef74f1d34c11926e1. **Publication safety boundary:** [CONTROL incident #44](https://github.com/grandchallenge/CONTROL/issues/44) remains open for the specific denied PR-creation action on 041. The mathematical calculations in 042 are a separately scoped candidate, **not** a disguised new attempt to publish or retry the denied 041 PR. Parent mathematical obligations [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) and [EXT-015D #2657](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2657).

## 1. Exact graph and wavefront setting

Choose an even smooth compactly supported mass-one function $\kappa$ that is nonnegative and strictly positive near zero. Put $\kappa_\epsilon(z)=\epsilon^{-1}\kappa(z/\epsilon)$.

The theta graph $G$ on vertices $1,2,3,4$ has the five edges

$$
E(G)=\{12,23,13,24,34\}.
\tag{42.1}
$$

It has cyclomatic number $5-(4-1)=2$. Critically, there are **three** proper cyclic subgraphs: triangles $A=(12,23,13)$ and $B=(23,24,34)$ and the square $C=(12,24,34,13)$. Every pair of these cycles overlaps in edges and/or vertices; they must **not** be combined in a product of simultaneous counterterms.

Introduce an oriented tree coordinate system of Jacobian one:

$$
u=x_1-x_2,\qquad
v=x_2-x_3,\qquad
w=x_3-x_4,\qquad s=x_3.
\tag{42.2}
$$

The regulated five-edge product is

$$
T_\epsilon(u,v,w,s)
=
\kappa_\epsilon(u)\kappa_\epsilon(v)
\kappa_\epsilon(u+v)\kappa_\epsilon(v+w)\kappa_\epsilon(w).
\tag{42.3}
$$

The full collision delta $\delta_G=\delta(u)\delta(v)\delta(w)$ is normalized with Lebesgue integration in $(u,v,w,s)$; its distribution derivatives are in the relative coordinates while $s$ remains a free root variable.

Let

$$
\begin{aligned}
c_3 &=\int_{\mathbb R^2}\kappa(a)\kappa(b)\kappa(a+b)\,da\,db,\\
c_4 &=\int_{\mathbb R^3}\kappa(a)\kappa(b)\kappa(c)\kappa(a+b+c)\,da\,db\,dc,\\
b_2 &=\int_{\mathbb R}\kappa(t)^2\,dt,\qquad
b_{2,2}=\int_{\mathbb R}t^2\kappa(t)^2\,dt,\\
W(a,b,c)&=\kappa(a)\kappa(b)\kappa(a+b)\kappa(b+c)\kappa(c),\\
M_0 &=\int_{\mathbb R^3}W(z)\,dz,\qquad
M_{ij}=\int_{\mathbb R^3}z_i z_j W(z)\,dz.
\end{aligned}
\tag{42.4}
$$

The coefficients are finite. $c_3,c_4,b_2,M_0$ are positive under the stated hypotheses. The weight $W$ has compact support and satisfies $W(-z)=W(z)$, hence **all odd total-degree moments vanish**.

## 2. All three proper cycle subtractions

Use the exact singular leading counterterms of isolated cycles as *subgraph-local* distributions, multiplying only the **remaining positive-regulator smooth edges**:

$$
\begin{aligned}
S_{A,\epsilon}
&=\frac{c_3}{\epsilon}\delta(u)\delta(v)
 \kappa_\epsilon(v+w)\kappa_\epsilon(w)
=\frac{c_3}{\epsilon}\delta(u)\delta(v)\kappa_\epsilon(w)^2,\\
S_{B,\epsilon}
&=\frac{c_3}{\epsilon}\delta(v)\delta(w)
 \kappa_\epsilon(u)\kappa_\epsilon(u+v)
=\frac{c_3}{\epsilon}\delta(v)\delta(w)\kappa_\epsilon(u)^2,\\
S_{C,\epsilon}
&=\frac{c_4}{\epsilon}\delta(u)\delta(v)\delta(w)
 \kappa_\epsilon(v)
=\frac{c_4\kappa(0)}{\epsilon^2}\delta_G.
\end{aligned}
\tag{42.5}
$$

The square $C$ spans all four vertices but remains a **proper edge subgraph** of $G$. It is easy to overlook; without it a purported forest subtraction is incomplete. These products are well-defined at every $\epsilon>0$ because the uncontracted factors are smooth. No product of $S_A$ and $S_B$ (or $S_C$) is taken.

**Theorem 42.1 (explicit overlapping cycle subtraction).** Put

$$
g_G=M_0-2c_3b_2-c_4\kappa(0)
\tag{42.6}
$$

and define the fully subtracted family

$$
R_\epsilon=
T_\epsilon-S_{A,\epsilon}-S_{B,\epsilon}
-S_{C,\epsilon}-\frac{g_G}{\epsilon^2}\delta_G.
\tag{42.7}
$$

Then $R_\epsilon$ converges **strongly** in $\mathcal D'(\mathbb R^4)$ as $\epsilon\downarrow0$, to the local finite distribution

$$
L_G=
\frac12\sum_{i,j\in\{u,v,w\}}
M_{ij}\,\partial_i\partial_j\delta_G
-\frac{c_3b_{2,2}}2
(\partial_u^2+\partial_w^2)\delta_G.
\tag{42.8}
$$

In fixed local charts the convergence remainder is $O(\epsilon^2)$ on bounded test-function sets with fixed compact support and uniformly bounded fourth derivatives. The result is invariant under exchanging the two endpoint triangles with the natural coordinate relabeling. A finite second-derivative local counterterm $-L_G$ changes the chosen renormalization scheme to one whose limit is zero.

**Proof.** Let $\phi(s,u,v,w)$ be a smooth compact test function. Substitute $(u,v,w)=\epsilon(a,b,c)$ in (42.3). With $\phi_s(z)=\phi(s,z)$,

$$
\langle T_\epsilon,\phi\rangle
=\epsilon^{-2}\int_{\mathbb R}\!\int_{\mathbb R^3}
W(z)\phi(s,\epsilon z)\,dz\,ds.
\tag{42.9}
$$

Taylor-expand $\phi(s,\epsilon z)$ to degree three about $z=0$. Parity of $W$ eliminates degree one and degree three, yielding

$$
\langle T_\epsilon,\phi\rangle
=
\frac{M_0}{\epsilon^2}\int\phi(s,0)\,ds
+\frac12\sum_{ij}M_{ij}\int
\partial_{ij}\phi(s,0)\,ds
+O(\epsilon^2).
\tag{42.10}
$$

The local delta and its second derivatives have exactly these test-function pairings (two derivatives give positive sign). From the first line of (42.5),

$$
\langle S_{A,\epsilon},\phi\rangle
=\frac{c_3}{\epsilon^2}
\int_{\mathbb R}\!\int_{\mathbb R}
\kappa(t)^2\phi(s,0,0,\epsilon t)\,dt\,ds
=\frac{c_3b_2}{\epsilon^2}
\int\phi(s,0)\,ds
+\frac{c_3b_{2,2}}2\int\partial_{ww}\phi(s,0)\,ds
+O(\epsilon^2).
\tag{42.11}
$$

Likewise $S_B$ contributes $c_3b_2\epsilon^{-2}\delta_G$ plus $(c_3b_{2,2}/2)\partial_{uu}\delta_G$. The square subgraph is **exactly** $c_4\kappa(0)\epsilon^{-2}\delta_G$; it contributes no finite derivative term. The overall subtraction (42.6) cancels the remaining $\epsilon^{-2}$ coefficient. What remains is (42.8). Compact supports of $W$ and $\kappa^2$ permit uniform Taylor bounds, proving strong convergence. $\square$

**Correct treatment of overlaps:** The three individual proper subgraph terms are compatible with their original isolated-cycle coefficients, but no two may be multiplied as simultaneous singular counterterms. For example, the formal product $\delta(u)\delta(v)\cdot\delta(v)\delta(w)$ contains $\delta(v)^2$ and fails the basic wavefront product criterion. Equation (42.7) is a *bounded Zimmermann-style one-graph subtraction*, not a universal theorem that graphwise counterterm insertions commute.

## 3. Exact rational hostile calculation

For the **finite-regularity algebraic control only**, use the even mass-one box density $\kappa_{\mathrm{box}}=\mathbf1_{\{|z|<1\}}/2$. It is deliberately not a legal smooth mollifier for the analytic theorem.

Direct exact integration gives

$$
c_3=\frac38,\qquad c_4=\frac13,\qquad
b_2=\frac12,\qquad b_{2,2}=\frac16,
\tag{42.12}
$$

and

$$
M_0=\frac7{48},\qquad
(M_{ij})_{i,j=u,v,w}=
\begin{pmatrix}
13/320 & -1/60 & 1/120\\
-1/60 & 1/30 & -1/60\\
1/120 & -1/60 & 13/320
\end{pmatrix}.
\tag{42.13}
$$

Thus the **complete** overlap coefficient is

$$
g_G=\frac7{48}-2\left(\frac38\right)\left(\frac12\right)
-\left(\frac13\right)\left(\frac12\right)
=-\frac{19}{48}.
\tag{42.14}
$$

The resulting finite local distribution is

$$
\begin{aligned}
L_G={}&-\frac7{640}(\partial_u^2+\partial_w^2)\delta_G
+\frac1{60}\partial_v^2\delta_G\\
&-\frac1{60}(\partial_u\partial_v+\partial_v\partial_w)\delta_G
+\frac1{120}\partial_u\partial_w\delta_G.
\end{aligned}
\tag{42.15}
$$

For a compact test function that agrees near the full diagonal with

$$
\phi(s,u,v,w)=h(s)
\bigl(1+2u^2+3v^2+5w^2+7uv+11vw+13uw\bigr),
\tag{42.16}
$$

the compensated pairing is **exactly** $-47/192\int h(s)\,ds$ whenever the regulator supports lie inside that polynomial neighborhood. This has no numerical error. The fixture [042](fixtures/check_overlapping_cycle_subtractions_042.py) checks the rational identities, all proper cycles, their overlap relations, the polynomial pairing and the local second-derivative coefficients.

## 4. A nested, attached-tree counterterm that closes

On four vertices, consider the triangular subgraph $A$ with an additional leaf edge $34$. In the same relative coordinates, its amplitude is

$$
N_\epsilon=
\kappa_\epsilon(u)\kappa_\epsilon(v)
\kappa_\epsilon(u+v)\kappa_\epsilon(w).
\tag{42.17}
$$

**Proposition 42.2 (triangle subdivergence with attached tree).** The subgraph-local subtraction alone,

$$
N_\epsilon-
\frac{c_3}{\epsilon}
\delta(u)\delta(v)\kappa_\epsilon(w)
\longrightarrow0
\quad\text{strongly in distributions},
\tag{42.18}
$$

with $O(\epsilon)$ remainder on compact test families of sufficiently many derivatives. No additional overall divergent local term is needed.

**Proof.** Use $(u,v,w)=\epsilon(a,b,c)$. The product prefactor is $\epsilon^{-1}$, and the triangle weight $\kappa(a)\kappa(b)\kappa(a+b)$ has vanishing first moments by simultaneous sign reversal. The inserted triangle counterterm matches the zeroth relative $(a,b)$ Taylor coefficient **at each fixed remaining edge coordinate $c$**. The residual quadratic relative Taylor terms are $O(\epsilon^2)$, multiplied by $\epsilon^{-1}$, so give $O(\epsilon)$. Integrate against the compactly supported remaining-edge kernel. $\square$

This is a precise instance of compatible subgraph-local subtraction in a graph with external edges, independent of the overlapping theta example.

## 5. Arbitrary connected graphs with delta-jet edges: whole-diagonal extension theorem

The previous examples use undifferentiated deltas. The following is an explicit extension theorem allowing derivatives on **every edge**; it is intentionally a *whole-graph* theorem and does not assert all required subgraph forest identities.

Let $G$ be any finite connected oriented graph on $n\ge2$ vertices with $m$ edges (parallel edges allowed). Give edge $e$ a nonnegative integer derivative order $r_e$. Choose a spanning tree and root coordinate $s$, with independent relative coordinates $z\in\mathbb R^{n-1}$ of Jacobian one, so every edge difference is an integer linear form $\ell_e(z)$. Form the compactly supported weight

$$
W_{G,\mathbf r}(z)=
\prod_{e\in E(G)}\kappa^{(r_e)}(\ell_e(z)),
\qquad
\omega=m+\sum_er_e-(n-1).
\tag{42.19}
$$

Compact support follows because the spanning-tree factors restrict every independent relative coordinate, even if some derivatives $\kappa^{(r_e)}$ vanish on part of their support. The regulated product is $\epsilon^{-(m+\sum r_e)}W_{G,\mathbf r}(z/\epsilon)$.

For every multi-index $\alpha$ define moments $\mu_\alpha=\int z^\alpha W_{G,\mathbf r}(z)\,dz$. Regard relative derivatives of $\delta_G=\prod_{j=1}^{n-1}\delta(z_j)$ as distributions with free root coordinate $s$.

**Theorem 42.3 (whole-graph local extension for arbitrary delta jets).** When $\omega\ge0$, define the singular local subtraction

$$
C_{G,\epsilon}=
\sum_{|\alpha|<\omega}
\frac{(-1)^{|\alpha|}\mu_\alpha}{\alpha!}
\epsilon^{|\alpha|-\omega}
\partial_z^\alpha\delta_G.
\tag{42.20}
$$

Then the renormalized distribution product converges strongly:

$$
T_{G,\epsilon}^{\mathbf r}-C_{G,\epsilon}
\longrightarrow
\sum_{|\alpha|=\omega}
\frac{(-1)^{|\alpha|}\mu_\alpha}{\alpha!}
\partial_z^\alpha\delta_G.
\tag{42.21}
$$

The convergence is $O(\epsilon)$ against uniformly bounded test families with sufficient derivatives. If $\omega<0$, the original regulated product tends to zero without subtraction. Under simultaneous reflection $z\mapsto-z$ and for even $\kappa$, the parity $W_{G,\mathbf r}(-z)=(-1)^{\sum r_e}W_{G,\mathbf r}(z)$ kills every moment of incompatible parity, often improving the convergence order.

**Proof.** The spanning tree gives a unit-determinant linear coordinate change. Under $z=\epsilon y$ the test pairing is

$$
\epsilon^{-\omega}
\int ds\,dy\,W_{G,\mathbf r}(y)\phi(s,\epsilon y).
\tag{42.22}
$$

Taylor-expand the test function in all relative directions through order $\omega$. The terms of degree less than $\omega$ have precisely the pairings of (42.20), because a derivative of delta pairs with $(-1)^{|\alpha|}\partial^\alpha\phi$. The degree $\omega$ term is (42.21). The remaining Taylor integral is bounded by $\epsilon^{\omega+1}$ times the appropriate test seminorm; the global prefactor is $\epsilon^{-\omega}$, yielding $O(\epsilon)$. The weight is compactly supported, so the estimate is uniform on bounded test-function sets. For $\omega<0$ the prefactor vanishes with positive order. $\square$

**Derivative compatibility, with an honest limitation.** For any fixed constant-coefficient vertex differential operator $D$, differentiation commutes with the strong distributional limit:

$$
D\bigl(T_{G,\epsilon}^{\mathbf r}-C_{G,\epsilon}\bigr)
\longrightarrow D\,L_{G,\mathbf r}.
\tag{42.23}
$$

By the Leibniz rule, the left side contains genuine sums of differentiated edge kernels; the differentiated counterterms are again local derivatives of delta on graph diagonals. This provides coherent jet control **for full vertex derivatives of each renormalized graph amplitude**. It does *not* by itself prove that a particular one-edge derivative insertion admits a universal subdivergence scheme independent of its containing graph.

**Power counting:** The superficial degree $\omega$ counts edges plus edge-jet derivatives minus independent relative dimensions. The counterterms use derivatives of the full collision delta up to that order, with no nonlocal tails. This is a constructive finite-dimensional extension, not a general physical theory.

## 6. Locality and exact remaining boundary

- **Achieved:** Complete proper-cycle inventory (three, not two) for the first overlapping theta graph; explicit individual proper-subgraph counterterms, an overall subtraction, a finite local limit, exact coefficients and parity control; a nested attached-tree check; a whole-graph extension for arbitrary finite connected delta-jet graphs; differentiation and translation covariance of distribution-valued renormalized limits.
- **Not established:** A universal recursive forest formula compatible with arbitrary nested and overlapping subgraph insertion; independence of graph presentation/counterterm scheme under arbitrary edge contractions; a complete second-order BV bracket/master equation for a domain containing all renormalized graphs; normal-topology multilinear plots and completed B.6 descent; liquid higher-Ext comparison.
- **Hostile control:** Treating the two overlapping triangle counterterms as commuting multiplicative operations would require $\delta(v)^2$, which is undefined. The correct graphwise sum avoids this. This specific impossibility is not a proof that a properly constructed forest formula cannot exist.
- **Provenance:** The mathematical source is a new GCL research branch, not protected-admitted or externally certified. The earlier SAFETY_HOLD on attempting to create a PR for 041 remains separate and cannot be bypassed by this material.

**Next precise mathematical obligation:** formulate a genuine local counterterm assignment for arbitrary subgraphs that satisfies the overlap/nesting recursion, compare the induced renormalized Wick/BV operators under graph gluing, and calculate any failure of the master equation as an explicit graph cocycle. This is a strictly stronger assertion than Theorems 42.1–42.3. Research tracker #2797 remains OPEN.
