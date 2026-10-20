# EXT-015D / D14 / 029 — GCL mathematical critical audit of regulated distributional BV

**Mathematical disposition:** ACCEPT the bounded arguments of [research result 028](D14_REGULATED_BV_SYZYGY_028.md) for: general Fréchet scalar-dual plot enrichment; higher liquid Ext dimension-shifting; smooth BV regularization on **all compactly supported distributional polynomial kernels**; the no-go for ordinary multiplication and nonzero smoothing kernels; the **Wick-twisted positive-scale differentiable prefactorization algebra**, its scale transport and completed Weiss descent; and the explicit unrestricted ultraviolet divergence. **Do not claim** a zero-scale quantum distributional BV theory, a universal enrichment of liquid modules, or higher source-syzygy Ext continuity. This audit is a distinct documented GCL mathematical argument under the existing authenticated identity, not an external-referee certificate.

**Protected proof custody:** [Result 028 / PR #2784](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2784), merged commit `05e4a2b0e0a3667e99d58916334bdd6bc3fadf79`.

**Source check:** Scholze, [*Lectures on Analytic Geometry*, Theorem 6.5, printed p. 35](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf), supplies compact projective real-liquid generators. Costello–Gwilliam, [Vol. I, Definitions B.2.1.1–B.2.1.2, B.6.0.7–B.6.1.1](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), supplies the distributional smooth plot and filtered differentiable categories. Costello–Gwilliam, [Vol. II, §7.2.3–7.2.4](https://people.math.umass.edu/~gwilliam/factorization2.pdf), explains positive-scale heat kernels/parametrices; **the specific mollifier/Wick proof here is independently derived**, not attributed to an unverified theorem of that book.

## A. General Fréchet scalar dual is a controlled extension, not a universal realization

For arbitrary Fréchet $E$, the plot rule $M\mapsto L_{\mathrm{cts}}(E,C^\infty(M))$ is a sheaf in the smooth parameter manifold, functorial under parameter pullback. Its value at a point is the continuous scalar dual $E'$. Differentiation on the output parameter gives a flat connection. Fréchet full faithfulness identifies the same set with liquid maps $\underline E\to\underline{C^\infty(M)}$. These statements require **no nuclear tensor theorem**. For the special source $C^\infty(V)$ they reproduce the literal compact-distributional Costello–Gwilliam DVS plots; for general Fréchet sources they **define** an analogous plot object but do not identify its tensor powers with distributional kernels on products. This preserves the precise scope of Theorem 28.1.

## B. Higher original liquid Ext: verify the exact syzygy boundary

Choose actual liquid projectives $P_i$ surjecting onto successive syzygies $K_{i-1}$ of the original nuclear Fréchet test-function source $H$. The long exact Ext sequence gives $\mathrm{Ext}^{n+1}(H,T)\cong\mathrm{Ext}^{n}(K_0,T)$ for $n\ge1$ and further reduces to first Ext of $K_{q-2}$. The connecting maps are natural in the coefficient $T$, so the comparison square commutes after $T=G_b$ and passage to the colimit. At $q=2$ the problem is exactly **Ext¹ for $K_0$**, not the previous first-Ext theorem for $H$.

**Verdict:** Theorem 28.2 is true and useful as an exact mathematical reduction. It would be **false to claim** that it proves the comparison for $K_0$, or that a projective syzygy is necessarily a Fréchet space.

## C. Distributional regulator acts on arbitrary correlated kernels

A compactly supported distribution $T$ on $U^n$ acts on **all** $C^\infty(U^n)$ functions. For a fixed smooth kernel $L(x_i,x_j)$, define the contraction of coordinates $i,j$ by evaluating $T$ on the product of $L$ with a lifted smooth test function on the remaining variables. This yields a compactly supported distribution on $U^{n-2}$ because projected supports of compact sets are compact. This operation is a continuous map on the relevant strong distributional spaces and smooth on B.2.1.1 plots: its parameter map is obtained by precomposition with one continuous linear operator between smooth-function Fréchet spaces.

This construction **does not require** writing $T$ as a sum of decomposable tensors. It therefore legitimately includes diagonals, derivatives of delta distributions and nonfactorizable compact kernels. Every positive-scale mollifier $K_\epsilon(x,y)=\epsilon^{-1}\kappa((x-y)/\epsilon)$ is smooth and acts by such contractions. Its free BV operator $\Delta_\epsilon$ is well-defined on the entire finite-polynomial distributional kernel collection.

## D. Why ordinary disjoint-open product cannot be a quantum chain map

For $x\ne y$, take small disjoint opens around them. Contract the even delta generator at $x$ with the odd delta generator at $y$; the result is $K(x,y)$. If ordinary multiplication were a quantum chain map, this **cross contraction** would vanish for every pair, hence $K=0$ off the diagonal, and by continuity also on the diagonal. Theorem 28.3 is a genuine **universal no-go for nonzero smooth kernels with the ordinary product**. Its hypothesis is important: it does not prohibit *corrected* scale-dependent factorization operations.

## E. Verify the Wick primitive, BV commutator and all factorization diagrams

Take a smooth compactly supported even $\kappa$ of total integral one, and set

$$
P_\epsilon(t)=\frac12\int|t-s|\kappa_\epsilon(s)\,ds.
$$

As distributions $(|t|/2)''=\delta_0$, hence $P_\epsilon''=\kappa_\epsilon$. Thus the smooth **symmetric even-even contraction** $B_\epsilon$ on polynomial distributional kernels satisfies $[B_\epsilon,d]=\Delta_\epsilon$: applying $d$ replaces each odd linear argument by its second derivative, and subtracting the opposite order cancels the even-even contractions, leaving only even-odd contractions against $D P_\epsilon=K_\epsilon$. The additional graded commutator $[B_\epsilon,\Delta_\epsilon]$ vanishes because both are constant-kernel pairwise contraction operations and $B_\epsilon$ differentiates only even generators. The formal exponential $W_\epsilon=e^{\hbar B_\epsilon}$ is well-defined and invertible: each polynomial coefficient is of finite arity, and $B_\epsilon$ lowers arity by two.

These identities yield

$$
W_\epsilon d W_\epsilon^{-1}
=d+\hbar\Delta_\epsilon.
$$

For any disjoint family of opens, define $\mu_\epsilon=W_{\epsilon,V}\mu_{\mathrm{cl}}(\bigotimes W_{\epsilon,U_i}^{-1})$. This is a chain map because it conjugates the classical map by chain isomorphisms. All operadic associativity/compatibility diagrams commute: intermediate $W^{-1}W$ factors cancel. **Naturality under inclusion is independently checked:** each contraction is defined by restricting the *same* global $P_\epsilon(x-y)$, and extension by zero commutes with the contractions. The constructed maps are DVS-smooth by the argument in Section C. Completed formal coefficients and split finite powers of $\hbar$ give the B.6 filtration.

**Verdict:** Theorem 28.5 is proved for the **Wick-corrected** maps on arbitrary compact distributional polynomial kernels at **positive scale**. It is not a theorem that the original symmetric multiplication remains a cochain map.

## F. Positive-scale Weiss descent and scale transport

Since $\{W_{\epsilon,U}\}_U$ is a **natural isomorphism of the entire classical and regulated prefactorization diagrams**, it identifies their completed Weiss Čech diagrams. The classical compact distributional polynomial Weiss comparison has already been established in [024–025](AGENT_CRITICAL_REVIEW_FREE_SCALAR_025.md). Completion in $\hbar$ is the inverse limit of split finite quotient towers; the successive quotient kernels are copies of the classical Čech comparison. Hence the B.6 finite-fibration criterion applies in every cohomological degree. **Corollary 28.5a accepted at each positive regulator scale.**

For $\epsilon,\eta>0$, the strict transport map $W_\eta W_\epsilon^{-1}$ intertwines both the differentials and the Wick-twisted factorization maps. Its cocycle identity is exact. Since $\kappa$ is even and normalized, $P_\epsilon(t)=|t|/2$ outside the regulator radius, so $P_\eta-P_\epsilon$ has compact support in $t=x-y$. The compact-range assertion concerns **scale change**, not global strict locality of the individual Wick multiplication. **Theorem 28.6 accepted.**

## G. Adversarial ultraviolet test

Choose the even and odd delta distributions at the *same point*. Their mixed BV contraction is $\kappa_\epsilon(0)=\epsilon^{-1}\kappa(0)$, divergent as $\epsilon\to0$. Similarly an even delta-second-derivative paired with an even delta gives $B_\epsilon$ coefficient $P_\epsilon''(0)=\kappa_\epsilon(0)$. Both are valid compactly supported distributional polynomial kernels. Hence neither the unrestricted BV operator nor the Wick operator has a coefficientwise zero-scale limit on **all** such kernels. This is a rigorous no-go for a naive unrestricted limit, not for a renormalized extension or a microlocally restricted domain. **Theorem 28.7 accepted.**

The finite [rational regression fixture 028](fixtures/check_regulated_wick_bv_028.py) independently checks 36 BV/commutator/Wick/scale algebra monomials and 36 mixed disjoint-factorization products with exact signs. Those tests verify the implemented identities in bounded finite mode; they do **not** establish continuity or smoothness for infinite-dimensional distributions, which is why the preceding exact arguments are necessary.

## H. Critical verdict and correctly open successors

| Mathematical obligation | Verdict |
| --- | --- |
| Scalar continuous-dual DVS plots from arbitrary Fréchet sources | **ACCEPT** |
| Original higher liquid Ext support comparison | **OPEN**; exact reduction to projective syzygy first Ext **ACCEPT** |
| Positive-scale BV on arbitrary compact distributional polynomial kernels | **ACCEPT** |
| Nonzero smooth BV regulator with *ordinary* disjoint-open multiplication | **IMPOSSIBLE** under stated axioms |
| Wick-corrected positive-scale quantum prefactorization, all-degree completed Weiss descent, exact scale cocycle | **ACCEPT** |
| Unrestricted distributional BV/Wick limit as regulator tends to zero | **IMPOSSIBLE** without restriction or renormalization |
| Microlocal UV domain/counterterms; general source-syzygy liquid Ext; interacting quantum theory | **OPEN** |

**Next mathematical obligation:** Specify one nontrivial microlocal or regularized domain of distributional kernels closed under the relevant contractions and scale transports, and prove whether its **zero-scale** BV and factorization limit exists; otherwise construct explicit counterterms for a first singular class. Independently decide the first-syzygy Ext¹ output-stage comparison for the original test-function-valued source. Agent work continues within the existing GCL authority; no Human Steward routine approval.
