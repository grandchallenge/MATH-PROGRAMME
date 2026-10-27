# EXT-015 REACH-R2 / 065 — nested derivative-jet forest on a five-vertex source and six-vertex host

**Status:** bounded mathematical source candidate requiring exact-head critical review and protected admission. This extends the fixed-source Gaussian jet action of [R2/061](R2_FILTERED_NORMAL_JET_INSERTION_061.md) and the external-quotient associativity theorem [R2/063](R2_TWO_QUOTIENT_JET_ASSOCIATIVITY_063.md) to a genuinely **nested chain of singular prepared sources**: the three-loop K4 source, a four-loop five-vertex source containing K4, and a five-loop six-vertex host containing both. Unlike the previous smooth-complement-only theorems, the five-vertex source itself receives a nonzero normal second-derivative counterterm after its *entire* proper 1PI forest has been prepared.

**Exact setting:** fixed labeled undifferentiated unit Gaussian delta edges, one common positive regulator, one-dimensional vertex positions, the source-local pole-only subtraction convention of R2/051 and R2/057, and vertex-disjointness (not mere edge-disjointness) for disconnected forest components. This is not an all-graphs Zimmermann character, BV nilpotence/QME, normal-topology Weiss descent or liquid higher Ext.

## 1. The nested graph family and full forest inventory

On vertices $0,1,2,3$, let $K$ be the six-edge complete graph, with lexicographically labeled edges

$$
01,\ 02,\ 03,\ 12,\ 13,\ 23.
\tag{65.1}
$$

Adjoin vertex 4 via $04,14$ to obtain the five-vertex eight-edge graph $F$, and then adjoin vertex 5 via $05,15$ to obtain the six-vertex ten-edge graph $G$:

$$
K\subsetneq F=K\cup\{04,14\}
\subsetneq G=F\cup\{05,15\}.
\tag{65.2}
$$

All three are connected and bridgeless, hence 1PI in the graph convention. Their cycle ranks are respectively 3, 4, 5. Their exact unit spanning-tree counts, obtained from their reduced Laplacians, are

$$
\boxed{\tau(K)=16,\qquad\tau(F)=40,\qquad\tau(G)=96.}
\tag{65.3}
$$

**Lemma 65.1 (complete proper forest inventory).** The graph $F$ has exactly 36 proper 1PI cyclic sources; the graph $G$ has exactly **85** proper 1PI cyclic sources, by intrinsic cycle rank

| Rank | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: |
| Number of proper 1PI sources in $G$ | 18 | 35 | 24 | 8 |

Every pair of 1PI sources in $G$ meets in at least one vertex. Hence the only compatible proper Zimmermann forests are strict **nested chains** of edge subgraphs. Enumerating all edge subsets and strict containments gives the following exact count:

| Forest cardinality | 0 | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Number | 1 | 85 | 605 | 1179 | 672 |

The total is **2542** proper forests. In particular the chain $K\subsetneq F\subsetneq G$ exists, and there is no disconnected divergent pair to multiply.

**Proof.** Enumerate each nonempty proper subset of the ten labeled edges. Retain a subset precisely if its induced nonisolated vertex graph remains connected after removing each chosen edge. There are exactly 85 such proper subsets, with the rank multiplicities in the table. Direct vertex-set comparison of each pair excludes a vertex-disjoint pair. Every compatible forest therefore is a strict edge-inclusion chain. Define $N_\gamma(1)=1$ and $N_\gamma(r+1)=\sum_{\beta\subsetneq\gamma}N_\beta(r)$ over the 85 proper sources, in increasing edge count. The totals over $\gamma$ yield 85, 605, 1179, 672 and no higher chains. The exact integer enumeration is replayed by [fixture 065](fixtures/check_nested_gaussian_jet_forest_065.py). $\square$

## 2. Exact intrinsic pole recursion including delta derivatives

For any connected 1PI graph $\gamma$ in this finite subgraph family, write $h_\gamma=|E_\gamma|-|V_\gamma|+1$. Root at its least labeled vertex and use the independent normal coordinates $y=(x_v-x_{\mathrm{root}})_{v\ne\mathrm{root}}$. Denote by $\tau_\gamma$ its reduced-Laplacian determinant and by $H_\gamma$ its inverse.

For a multiindex $\alpha$ of **even** order $|\alpha|<h_\gamma$, define the normalized prepared moment $m_{\gamma,\alpha}$ recursively. The bare Gaussian moment is

$$
b_{\gamma,\alpha}
=\tau_\gamma^{-1/2}\,
\mathbb E_{N(0,H_\gamma)}[y^\alpha].
\tag{65.4}
$$

If $\beta\subsetneq\gamma$ is a proper 1PI source, split the vertex coordinates into $u$ normal to the collision of $\beta$ and $q$ normal to the quotient graph $\gamma/\beta$. The smooth complement edges have quadratic form

$$
u^TA_{\gamma|\beta}u+
2u^TB_{\gamma|\beta}q+q^TD_{\gamma|\beta}q,
\qquad D_{\gamma|\beta}\succ0.
\tag{65.5}
$$

The variable $y^\alpha$ is expressed as a polynomial $\Phi_\alpha(u,q)$ in these split coordinates. Let $[u^\eta]$ extract the coefficient of the monomial $u^\eta$. The exact normalized insertion moment of the **previously prepared source** $\beta$ is

$$
\begin{aligned}
I_{\gamma\leftarrow\beta,\alpha}
={}&(\det D_{\gamma|\beta})^{-1/2}
\sum_{\substack{|\eta|\ \mathrm{even}\\|\eta|<h_\beta}}
m_{\beta,\eta}\,
\mathbb E_{N(0,D_{\gamma|\beta}^{-1})}
\bigg[
[u^\eta]\Big(
e^{-\frac12u^TA_{\gamma|\beta}u-u^TB_{\gamma|\beta}q}
\Phi_\alpha(u,q)\Big)
\bigg].
\end{aligned}
\tag{65.6}
$$

**Theorem 65.2 (complete finite source-local jet-forest recursion).** For this graph family define, in strictly increasing source edge count,

$$
\boxed{
m_{\gamma,\alpha}
=b_{\gamma,\alpha}
-\sum_{\substack{\beta\subsetneq\gamma\\ \beta\ {\rm 1PI}}}
I_{\gamma\leftarrow\beta,\alpha}.
}
\tag{65.7}
$$

Then the intrinsic overall local subtraction is

$$
\boxed{
C_{\gamma,\epsilon}
=(2\pi)^{-h_\gamma/2}
\sum_{\substack{|\alpha|\ {\rm even}\\|\alpha|<h_\gamma}}
\frac{m_{\gamma,\alpha}}{\alpha!}\,
\epsilon^{-h_\gamma+|\alpha|}
\partial_y^\alpha\delta_\gamma.
}
\tag{65.8}
$$

Every coefficient in (65.8) depends only on the corresponding source graph, not the containing supergraph. The recursion implements every compatible proper forest **exactly once**, including chains of up to four proper sources in $G$. No multiplication of overlapping singular delta distributions is formed. After all proper source insertions and subtraction of (65.8), the remainder tends strongly to zero, uniformly on bounded compact smooth test families, with $O(\epsilon)$ remainder.

**Proof.** A connected Gaussian graph of cycle rank $h$ has the exact normalized amplitude

$$
T_{\gamma,\epsilon}
=(2\pi)^{-h/2}\tau_\gamma^{-1/2}
\epsilon^{-h}\rho_{\gamma,\epsilon},
\tag{65.9}
$$

where $\rho_{\gamma,\epsilon}$ is a centered probability Gaussian with covariance $\epsilon^2H_\gamma$ in relative coordinates. Its Taylor expansion on smooth compact tests is an even-power local delta-jet series with remainder controlled by all Gaussian moments. For a proper prepared source, the coefficient of $\partial^\eta\delta$ is $m_{\beta,\eta}/\eta!$, so pairing with the smooth complement and a polynomial test produces **exactly** the coefficient extraction in (65.6), with the quotient Gaussian normalized by $(\det D)^{-1/2}$. The sign for every derivative order here is positive because only even total derivative degrees occur; mixed odd derivatives at intermediate stages are retained through the $u^TBq$ exponential. The Gaussian powers combine to the common overall scale $\epsilon^{-h_\gamma+|\alpha|}$.

All proper singular source pairs intersect in vertices, so each proper forest is a chain. By induction on edge number, the prepared counterterm of each source incorporates its own shorter nested chains. Consequently the immediate-subgraph subtraction in (65.7) incorporates **all** nested forest chains once, and adds none twice. For rank $h\le5$, the negative Laurent orders are exactly those with even $|\alpha|<h$; the next term after subtracting all these orders is $O(\epsilon)$ in the strong distribution topology on bounded compact test families. Gaussian tail bounds control the cutoff outside a neighborhood of the full diagonal. This proves (65.8) and the limit. $\square$

**Scope of the proof:** This is an **exhaustive finite-graph and Gaussian-specific construction** with rational Wick moments and algebraic determinant factors, not a theorem that the same recursive subtraction commutes with arbitrary graph operations.

## 3. First genuinely nested singular derivative source

For $K$, the protected R2/051–052 coefficients appear in exactly the normalization of (65.8):

$$
m_{K,0}
=\frac5{12}-\frac{3\sqrt2}{2}+2\sqrt6,
\qquad
m_{K,(1,1)}=-\frac7{72},
\qquad
m_{K,(1,2)}=-\frac7{144}.
\tag{65.10}
$$

(The coordinate indices in this section are 1-based labels on the nonroot vertices. For a monomial $y_1^2$, the source coefficient multiplying $\partial_{y_1}^2\delta$ is $m_{K,(1,1)}/2$.)

Inserting this fully prepared K4 source into $F$ produces an **exact nonzero** K4-derived quadratic moment contribution

$$
\boxed{
I_{F\leftarrow K,(1,1)}=-\frac{7\sqrt2}{144}.
}
\tag{65.11}
$$

After subtracting **all 36** proper 1PI sources of $F$ with their intrinsic recursions, its new overall normal quadratic moment is

$$
\boxed{
\begin{aligned}
b_F:=m_{F,(1,1)}
={}&\frac{\sqrt{10}}{50}
-\frac{52\sqrt{21}}{441}
+\frac{7\sqrt2}{144}
-\frac{\sqrt5}{25}
+\frac{4\sqrt{15}}{25}
-\frac{\sqrt6}{18}<0.
\end{aligned}
}
\tag{65.12}
$$

Its negativity is rigorously checked by interval enclosure of each square root with integer square bounds. Thus the **five-vertex source itself** needs a derivative-of-delta counterterm at order $\epsilon^{-2}$. This derivative correction is genuinely prepared from sources including the older derivative-bearing K4; it was not fitted to any six-vertex host.

Embed the prepared $F$ source in $G$ by multiplying by the two remaining Gaussian edges $05,15$. Integrating only the new vertex's relative coordinate $q=x_5-x_0$ gives the smooth quotient factor

$$
\int\kappa_\epsilon(q)\kappa_\epsilon(y_1-q)\,dq
=\frac{1}{2\sqrt{\pi}\epsilon}
\exp\!\left[-\frac{y_1^2}{4\epsilon^2}\right].
\tag{65.13}
$$

When the **intrinsic five-vertex derivative jet** acts on the second normal derivative of this complement, it creates the additional local scalar contact (relative to merely freezing the complement's value)

$$
\boxed{
\Delta_{F\hookrightarrow G,\epsilon}
=-\frac{b_F}{32\pi^{5/2}}\,
\epsilon^{-5}\delta_F>0.
}
\tag{65.14}
$$

This is the pushforward along $q$ of the embedded source correction and is supported on the **five-vertex source collision diagonal**. It should not be confused with the overall six-vertex counterterm before pushforward. In particular, (65.14) is a second nested singular-source contact: a derivative-bearing K4 contributes to the preparation of a derivative-bearing $F$, whose derivative in turn hits the new smooth complement.

**Proof of (65.14).** In source-normal coordinates $y_1=x_1-x_0$ the coefficient of $\partial_{y_1}^2\delta_F$ is $(2\pi)^{-2}(b_F/2)\epsilon^{-2}$. The quotient factor $f_\epsilon$ in (65.13) satisfies $f_\epsilon''(0)=-f_\epsilon(0)/(2\epsilon^2)$ and $f_\epsilon(0)=(2\sqrt\pi\epsilon)^{-1}$. The distributional Leibniz rule gives the extra scalar coefficient $-(2\pi)^{-2}b_F/(8\sqrt\pi)\epsilon^{-5}=-b_F/(32\pi^{5/2})\epsilon^{-5}$. $\square$

## 4. The full six-vertex host needs a fourth-derivative counterterm

The complete preparation of $G$ uses its 85 intrinsic proper source counterterms and therefore all 2542 compatible forest chains. Since $h_G=5$, the complete local negative Laurent part has the following three types:

$$
\overline R_{G,\epsilon}
=(2\pi)^{-5/2}\left[
\epsilon^{-5}m_{G,0}\delta_G
+\epsilon^{-3}\sum_{|\alpha|=2}\frac{m_{G,\alpha}}{\alpha!}\partial_y^\alpha\delta_G
+\epsilon^{-1}\sum_{|\alpha|=4}\frac{m_{G,\alpha}}{\alpha!}\partial_y^\alpha\delta_G
\right]+O_{\mathcal D'}(\epsilon).
\tag{65.15}
$$

There are exactly **86** independent monomial moment coefficients in the right-hand side: one scalar, 15 quadratic, and 70 quartic in five relative coordinates. The exact recursion (65.6)–(65.7) determines every one with rational Wick moments and squarefree-radical coefficients. It obeys both manifest graph automorphisms interchanging $2\leftrightarrow3$ and $4\leftrightarrow5$ (the latter exchanges the two external tips).

**Theorem 65.3 (a nonvanishing fourth-order pole).** On a smooth compact test function agreeing near the full diagonal with $(x_1-x_0)^4$, all scalar and second-order delta terms in (65.15) vanish, whereas the full prepared amplitude has exact nonzero leading coefficient

$$
\boxed{
m_{G,(1,1,1,1)}
=\frac{\sqrt6}{72}-\frac{\sqrt3}{32}<0.
}
\tag{65.16}
$$

Hence a scalar-plus-second-derivative subtraction **cannot** renormalize this complete five-loop Gaussian graph. Its intrinsically prepared counterterms require a nonzero fourth-derivative full-diagonal subtraction at order $\epsilon^{-1}$. With all 86 coefficients of (65.15) subtracted, the strongly distributional remainder is $O(\epsilon)$ and converges to zero.

**Proof.** Apply the source-moment recursion to every proper 1PI edge subgraph in increasing edge count, including the source $K$ and its supergraph $F$. Bare Gaussian moments are given by Wick pairings in $Q^{-1}$; every proper-source quotient and its mixed normal-jet contribution is computed by (65.5)–(65.6). The exact radical calculation for the quartic monomial reduces to (65.16), verified also against the two graph automorphisms and the full 86-component monomial family. Since $\sqrt6/72<\sqrt3/32$ is equivalent to $\sqrt2<9/4$, this coefficient is strictly negative without numerical approximation. Pairing with the indicated quartic test kills both lower-order local counterterms and detects precisely (65.16) at order $\epsilon^{-1}$. The uniform Gaussian fourth-moment expansion and sixth-moment remainder complete the strong limit after the full local subtraction. $\square$

## 5. Exact regression and remaining frontier

The accompanying [standard-library regression](fixtures/check_nested_gaussian_jet_forest_065.py) is an executable finite proof certificate for the algebraic assertions. It exhaustively enumerates 1PI edge subsets, 2542 nested forests and all 86 pole moments; independently rebuilds their reduced Laplacians, computes rational Wick moments and source-quotient Taylor jets, and carries all coefficients in an **exact squarefree-radical rational basis** with no floating point. It checks the protected K4 moments, the exact derivative insertion of K4 into the five-vertex source $F$ (65.11), the new five-vertex source derivative (65.12) and its strict sign, the fourth-order pole (65.16), all 86 tensor moments under two graph automorphisms, and the positive nested-source contact (65.14). The analytic strong-distribution estimate is proved above; the finite fixture checks the exact algebra and exhaustive combinatorics.

**Achieved:** A complete six-vertex, ten-edge, five-loop Gaussian proper 1PI forest with **two levels of genuinely singular derivative-bearing source corrections** and the first explicitly nonzero **fourth-derivative** overall pole in this thread.

**Not achieved:** a universal all-graph forest character, compatibility with arbitrary differentiated/Wick kernels, globally closed BV differential/nilpotence, interacting QME, Costello–Gwilliam B.6, or liquid higher Ext. The parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) stays OPEN.

**Next theorem-level obligation:** demonstrate or refute the same intrinsic subtraction under a graph where two independently prepared derivative-bearing proper sources have *overlapping but nonnested* diagonals, including exact hostile pairing on mixed normal tests. Review R2/065 at its exact head before protected admission.
