# EXT-015 REACH-R3 / 067 — evaluated relation cover and injectivity in every degree

**Status:** bounded mathematical candidate. This constructs an actual projective relation cover of the reduced liquid kernel from 037 and proves injectivity of the compact-output-stage comparison for every liquid source and every nonnegative Ext degree. It does **not** prove surjectivity of the original degree-two comparison. A source-locked critical pass and protected admission remain required.

**Fixed category and source:** $\mathcal A_p=\mathrm{Liq}_p(\mathbb R)$, $0<p\le1$, with the exact cover and chosen singleton splitting of [016](AGENT_CRITICAL_REVIEW_AB_016.md) and [037](R3_ALL_SINGLETON_LINEAR_RELATIONS_037.md). The initial protected evidence cut is `028c54adfc740bb93a30be55194b45c449a867ac`. No Fréchet structure on a liquid kernel is inferred.

## 1. Explicit relation coordinates

Write the admitted cover as

$$
P_{\mathrm{red}}=
\bigoplus_{b\in\mathcal B}\underline{\mathbb R}
\oplus
\bigoplus_{(T,u)\in\mathscr S_{\mathrm{prof}}}
\mathcal M_{<p}(T),
\qquad
\varepsilon_{\mathrm{red}}:P_{\mathrm{red}}\twoheadrightarrow H,
\qquad
K=\ker\varepsilon_{\mathrm{red}}.
\tag{67.1}
$$

Here $\mathcal B$ is the fixed Hamel basis used only in the free singleton coproduct, and $\mathscr S_{\mathrm{prof}}$ retains all original nonsingleton plot generators. Thus $K$ is exactly $K_{\mathrm{red}}$ of 037, not a replacement topological vector space.

Fix the condensed universe and a small projective generating family
$\mathscr G=\{\mathcal M_{<p}(S)\}$ with $S$ extremally disconnected. This is the projective-generator input of Scholze, [Analytic Geometry, Theorem 6.5](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf#page=35). Do not impose the original Fréchet cover's continuum bound on this new kernel without a separate proof.

For $S$ in that family define the actual set of relation plots

$$
\mathscr R(S)=
\left\{
r\in\mathrm{Hom}(\mathcal M_{<p}(S),P_{\mathrm{red}}):
\varepsilon_{\mathrm{red}}r=0
\right\}.
\tag{67.2}
$$

Compactness of this generator makes each $r$ supported in finitely many summands of (67.1). Hence (67.2) is explicitly the set of finite tuples

$$
r=(a_b,\mu_{T,u}),
\qquad
a_b\in\underline{\mathbb R}(S),\quad
\mu_{T,u}\in
\mathrm{Hom}(\mathcal M_{<p}(S),\mathcal M_{<p}(T)),
\qquad
\sum_b a_b b+\sum_{T,u}u_*\mu_{T,u}=0
\ \text{in }H(S).
\tag{67.3}
$$

The final equality is an equality of whole plots parameterized by $S$. The measure-channel maps are not restricted to finite point measures. No discontinuous Hamel-coordinate map out of $H$ is used.

## 2. Genuine projective cover and its next kernel

Set

$$
P_1=
\bigoplus_{\substack{S\in\mathscr G\\r\in\mathscr R(S)}}
\mathcal M_{<p}(S).
\tag{67.4}
$$

On the summand $(S,r)$ define $d_1$ by the actual morphism $r$ into $P_{\mathrm{red}}$. Since $\varepsilon_{\mathrm{red}}d_1=0$, it factors uniquely as $d_1=i q$ with $i:K\hookrightarrow P_{\mathrm{red}}$. Put $K_1=\ker q$.

**Theorem 67.1.** This gives a genuine exact sequence in $\mathcal A_p$,

$$
0\longrightarrow K_1
\overset{j}{\longrightarrow}P_1
\overset{q}{\longrightarrow}K
\longrightarrow0,
\tag{67.5}
$$

with $P_1$ projective. For every generating test $T$, $K_1(T)$ is explicitly the finite-tuple relation set

$$
\left\{
(\nu_{S,r}):
\nu_{S,r}\in
\mathrm{Hom}(\mathcal M_{<p}(T),\mathcal M_{<p}(S)),
\quad
\sum_{S,r}r\circ\nu_{S,r}=0
\ \text{in }\mathrm{Hom}(\mathcal M_{<p}(T),P_{\mathrm{red}})
\right\}.
\tag{67.6}
$$

Consequently, naturally in every liquid target $V$,

$$
\mathrm{Ext}^2(H,V)
\simeq\mathrm{Ext}^1(K,V)
\simeq
\frac{\mathrm{Hom}(K_1,V)}
{\{\psi j:\psi\in\mathrm{Hom}(P_1,V)\}}.
\tag{67.7}
$$

**Proof.** Coproducts of projectives are projective in this category: Hom from the coproduct is a product of exact real-vector-space-valued functors. Every morphism from a generator to $K$ corresponds under its inclusion to one $r$ in (67.2), and hence lifts along the corresponding summand of $P_1$. Thus Hom from every projective generator sends $q$ to a surjection. These generators detect epimorphisms, so $q$ is epic. The kernel is formed in the liquid category; compactness on $T$ makes the evaluation of (67.4) a finite-support sum, yielding (67.6). The long exact Ext sequence of (67.5) and projectivity of $P_1$ give its cokernel formula. Projectivity of $P_{\mathrm{red}}$ in (67.1) supplies the first dimension shift. $\square$

This is an evaluated-generator construction of the actual relation cover. It does not assert that $P_1$ is finite, countably generated, compact, minimal, Fréchet, or useful for a Baire argument.

**Presentation independence.** Given two projective epimorphisms onto the same $K$, projectivity lifts each one through the other. A difference of two lifts factors through the other's kernel. Composing a kernel-to-target map with that difference is the restriction of a map from the projective domain, hence a boundary. The induced cokernel maps in (67.7) are therefore independent of the lifts and inverse to one another. This verifies resolution independence without identifying a kernel with a Fréchet space.

## 3. The output filtration gives injectivity in every degree

Use the admitted real LF target isomorphism of 018/019,

$$
G=\underline{\mathcal D(\mathbb R)}
\simeq E=\bigoplus_{n\ge1}B_n,
\qquad B_n=\underline s,
\qquad E_N=\bigoplus_{n\le N}B_n.
\tag{67.8}
$$

The underlying classical representation is corroborated by the explicit sequence-space construction of [Bargetz–Debrouwere–Nigsch](https://arxiv.org/abs/2107.00245), Theorems 1.1–1.2. Here its real form and liquid/strict-LF realization are exactly the admitted hypotheses of 018/019. No new assertion about arbitrary LF targets is imported.

Each actual support stage $G_b$ is Fréchet, so its map into $E$ lands continuously in some finite prefix $E_N$. Conversely each Fréchet $E_N$ maps into some compact support stage $G_c$. These are the admitted fixed-Fréchet-to-strict-LF factorization statements; they concern these coefficient objects, not $K$ or $K_1$.

**Theorem 67.2 (all-source, all-degree injectivity).** For every $A\in\mathcal A_p$ and every integer $m\ge0$,

$$
\theta_A^m:
\varinjlim_b\mathrm{Ext}^m(A,G_b)
\longrightarrow\mathrm{Ext}^m(A,G)
\quad\text{is injective}.
\tag{67.9}
$$

In particular this settles injectivity, but not surjectivity, of the R3 comparison $\theta_K^1$, equivalently $\theta_H^2$.

**Proof.** Let $\xi\in\mathrm{Ext}^m(A,G_b)$ become zero in the full target. Factor $G_b\to G\simeq E$ through some $E_N$, and let $\eta$ be the image of $\xi$ in $\mathrm{Ext}^m(A,E_N)$. The inclusion $E_N\hookrightarrow E$ has the coefficient projection as a retraction. Functoriality of Ext therefore makes its induced map split injective, in every degree and for every $A$. Thus $\eta=0$.

Now factor $E_N\to E\simeq G$ through $G_c$, enlarging $c$ to have $c\ge b$. The composite $G_b\to E_N\to G_c$ agrees with the actual support inclusion: the two maps agree after the monomorphism $G_c\hookrightarrow G$. Hence the image of $\xi$ in $\mathrm{Ext}^m(A,G_c)$ is zero, as required for injectivity of the filtered colimit comparison. No hypothesis on the topology of $A$ was used. $\square$

Equivalently, the coefficient systems $G_b$ and $E_N$ are cofinal as ind-objects by their actual two-way stage factorizations. This yields

$$
\varinjlim_b\mathrm{Ext}^m(A,G_b)
\simeq\bigoplus_n\mathrm{Ext}^m(A,B_n).
\tag{67.10}
$$

The canonical finite-sum inclusion into full-target Ext is injective by the same coordinate retractions. This is not an assertion that Ext commutes with an infinite coproduct.

## 4. Exact remaining degree-two surjectivity channels

Write $P=\prod_n B_n$ and $Q=P/E$. Exactness of products follows by evaluation on the projective generators, and thus a projective resolution of $H$ gives

$$
\mathrm{Ext}^m(H,P)\simeq\prod_n\mathrm{Ext}^m(H,B_n).
\tag{67.11}
$$

Let $\rho^2:\mathrm{Ext}^2(H,E)\to\prod_n\mathrm{Ext}^2(H,B_n)$ be the coordinate map and put $\mathrm{Ph}^2=\ker\rho^2$. The target long exact sequence gives the actual identity

$$
\mathrm{Ph}^2
\simeq
\mathrm{coker}\left[
\mathrm{Ext}^1(H,P)\longrightarrow\mathrm{Ext}^1(H,Q)
\right].
\tag{67.12}
$$

There is an exact sequence of real vector spaces

$$
0\longrightarrow\mathrm{Ph}^2
\longrightarrow\mathrm{coker}(\theta_H^2)
\longrightarrow
\frac{\mathrm{im}(\rho^2)}
{\bigoplus_n\mathrm{Ext}^2(H,B_n)}
\longrightarrow0.
\tag{67.13}
$$

**Proof.** Equation (67.11) follows by applying Hom from a projective resolution and taking products of cochain complexes; real-vector-space products are exact and commute with their cohomology. Exactness for $0\to E\to P\to Q\to0$ proves (67.12). The image in (67.10) consists of finite-coordinate Ext classes; its intersection with $\ker\rho^2$ is zero by coordinate retractions. Taking the coordinate image of the quotient by that finite-coordinate subgroup proves (67.13). $\square$

Thus the still-unsolved verdict is exactly two questions: does every first-Ext class with coefficient $Q$ lift to coefficient $P$, and does every realizable degree-two coordinate family have finite support? Neither is supplied by Theorem 67.1 or by ordinary Hom factorization.

Equivalently, in the actual evaluated cover (67.5), the remaining lemma is

$$
\forall f:K_1\to G,\quad
\exists b,\ f_b:K_1\to G_b,\ \psi:P_1\to G:
\qquad
f=\iota_b f_b+\psi j.
\tag{67.14}
$$

All objects and maps in this quantifier are fixed above. A negative verdict requires an actual $f$ violating (67.14), not an unbounded representative that is a boundary.

## 5. Hostile controls and scope

For a nonzero chosen point in each $B_n$, the map $\bigoplus_n\underline{\mathbb R}\to E$ taking its generator indexed by $n$ to that point in the summand indexed by $n$ has no finite output prefix. Its source is projective, so its positive-degree Ext groups vanish. This actual infinite categorical control shows why support escape of a map and support escape of an Ext class must not be confused. It also shows why injectivity alone cannot imply a general finite-support statement for maps.

The [exact fixture](fixtures/check_evaluated_relation_cover_067.py) checks the finite relation/relation-of-relation identities, changes of projective presentation modulo boundaries, coefficient retraction and a support-escaping boundary control in exact rational linear algebra. It does not test the infinite quantifier (67.14) or prove a nonzero liquid Ext class.

**Achieved:** genuine evaluated relation cover of the actual reduced liquid kernel; resolution-independent cocycle/boundary formula; injectivity of every source's support-stage comparison in every degree; exact two-channel degree-two surjectivity residual.

**Not achieved:** original degree-two surjectivity, all higher-degree surjectivity, R1 differentiable Weiss, global renormalized BV/QME or R4 integration. Keep [R3 #2798](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2798) and the parent issues open. Registration of the larger workset does not change this boundary.
