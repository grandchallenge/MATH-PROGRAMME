# EXT-015 REACH-R1 / 069 — locally normal plots and a completed free zero-scale Weiss model

**Status:** new bounded mathematical candidate, requiring source-locked critical audit. This constructs a differentiable free zero-scale model on the admitted microlocal kernel domain using locally uniform normal-sector plots. It proves completed Weiss descent in an explicit total-weight filtration. It does not identify this plot structure with an ordinary locally convex inductive-limit topology, prove a uniform positive-regulator endpoint, or extend the domain to excluded collision kernels.

**Inputs:** fixed-fiber free model [030](D21_MICROLOCAL_ZERO_SCALE_BV_030.md), hostile plot audit [033](R0_CRITICAL_AUDIT_D21_033.md), and fixed-sector continuous contractions [035](R1_NORMAL_CONE_CONTINUOUS_CONTRACTIONS_035.md), with review [038](AGENT_CRITICAL_REVIEW_REACH_038.md). The imported tensor estimate is Brouder–Dang–Helein, [Theorem 4.6](https://arxiv.org/abs/1409.7662), for the normal topology. Differentiable spaces, flat connections, multimorphisms and completed pro-cochains use Costello–Gwilliam's [Appendix B](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), Definitions B.1.0.3, B.1.3.1 and B.6.0.7–B.6.1.1, in that draft's numbering. The construction below checks these structures directly.

## 1. The differentiable space is specified by its plots

For an open $U\subset\mathbb R$, let $\mathscr C_n(U)$ be the compact distributional kernels of 030, with wavefront avoiding every nonzero partial-diagonal conormal, including simultaneous disjoint collisions. For a compact $K\Subset U^n$ and closed admissible cone $\Gamma$, use the fixed normal sector

$$
E_{n;K,\Gamma}(U)=
\{T:\mathrm{supp}(T)\subset K,\ \mathrm{WF}(T)\subset\Gamma\}
\tag{69.1}
$$

with its induced normal locally convex topology, as in 035.

A plot $f:M\to\mathscr C_n(U)$ is **locally normal** if around each parameter point it is a Bastiani-smooth map into one sector (69.1). The sector is common on that parameter neighborhood, not chosen separately at every parameter value.

**Lemma 69.1.** These plots, with ordinary parameter differentiation, define a differentiable vector space in the stated Costello–Gwilliam sense.

**Proof.** Constants lift to a sector. Smooth parameter pullback preserves a local sector lift, and the definition is local, so plots glue. For addition, two local lifts map continuously into the larger sector with support $K_1\cup K_2$ and cone $\Gamma_1\cup\Gamma_2$, which remains closed and admissible. Smooth scalar multiplication uses the usual locally convex scalar action on that common sector. All parameter derivatives of a sector-smooth map still take values smoothly in the same sector.

Define $\nabla_X f$ by the parameter derivative along a vector field $X$. Different local sector lifts give the same distributional derivative, so these definitions agree on overlaps. The chain rule gives naturality under parameter pullback, the product rule gives Leibniz, and commuting parameter derivatives gives a flat connection. Locally the resulting 1-form is a finite coordinate sum, so it is in the required $\Omega^1(M)\otimes_{C^\infty(M)}C^\infty(M,\mathscr C_n(U))$. $\square$

This defines a sheaf of plots with a flat connection; it does not assume existence, regularity or completeness of a global locally convex union. Completeness below is completeness of the specified filtered differentiable object.

## 2. Hypocontinuity supplies actual smooth multimorphisms

**Lemma 69.2.** If a bilinear map $\beta:E\times F\to G$ of locally convex spaces is hypocontinuous with respect to bounded sets in both variables, then for Bastiani-smooth maps $f:M\to E$ and $g:M\to F$ from a finite-dimensional manifold, $\beta(f,g)$ is Bastiani-smooth and

$$
\partial^\alpha\beta(f,g)
=
\sum_{\gamma\le\alpha}
{\alpha\choose\gamma}
\beta(\partial^\gamma f,\partial^{\alpha-\gamma}g).
\tag{69.2}
$$

**Proof.** Work on a relatively compact parameter coordinate neighborhood. The image of each derivative on a smaller compact neighborhood is compact, hence bounded. Hypocontinuity bounds $\beta$ uniformly when one factor ranges in such a bounded set. Splitting a difference into a change in its first factor and a change in its second proves continuity of the composite.

For a coordinate difference quotient use

$$
\frac{\beta(f(t+h),g(t+h))-\beta(f(t),g(t))}{h}
=
\beta\!\left(\frac{f(t+h)-f(t)}h,g(t+h)\right)
+
\beta\!\left(f(t),\frac{g(t+h)-g(t)}h\right).
\tag{69.3}
$$

The first quotient converges to the derivative of $f$ and the second to that of $g$. Hypocontinuity against the bounded images controls the first difference; separate continuity controls the fixed-factor difference. This proves the derivative formula and its continuity. Repeat with derivatives to obtain (69.2). No joint continuity of $\beta$ on arbitrary unbounded input neighborhoods is asserted. $\square$

For fixed normal sectors, exterior tensor product is hypocontinuous into the sector with cone

$$
\Gamma_{\boxtimes}
=
(\Gamma_1\times\Gamma_2)
\cup(\Gamma_1\times0)
\cup(0\times\Gamma_2),
\tag{69.4}
$$

with the appropriate base zero sections. This is the cited Theorem 4.6.

**Theorem 69.3.** If $U_1,U_2\subset V$ are disjoint, exterior product defines a smooth bilinear map with compatible flat connection

$$
\mathscr C_n(U_1)\times\mathscr C_m(U_2)
\longrightarrow\mathscr C_{n+m}(V).
\tag{69.5}
$$

The finite-arity Wick-conjugated disjoint structure maps of 030 are smooth multimorphisms for the locally normal plots.

**Proof.** Local input plots have fixed compact supports and cones. Their tensor has support $K_1\times K_2$ and cone (69.4). No collision block meeting both input opens exists on that support. If an output covector were conormal to a remaining partial diagonal, its nonzero input factor would already be forbidden by that factor's complete partial-diagonal exclusion. Thus the output sector is admissible. Extension into $V$ has no boundary wavefront since supports are compact inside the input opens. Lemma 69.2 gives smoothness and exactly the connection product rule.

The operators in a finite-arity Wick exponential are finite sums/composites of the continuous linear normal-sector contractions proved in 035. Finitely many output cones and supports can be enlarged by finite unions. Thus the exponentials and their inverses preserve locally normal plots. Compose them with (69.5) to obtain the Wick-conjugated maps. The graded signs and algebraic identities are precisely those already fixed in 030; smoothness does not change them. $\square$

Finite permutation invariants use the finite Reynolds projection. Supports and cones may first be enlarged by their finite permutation orbits. Differentiation preserves the sectors, so the classical differential is smooth as well.

## 3. An explicit complete filtration

Let $C_n^\bullet(U)$ denote the graded-symmetric classical kernel complex of arity $n$ from 030 with this differentiable structure. Its cohomological degrees lie in the finite interval $[-n,0]$. Let $B_0$ and $\Delta_0$ have the admitted zero-scale meanings, with $B_0$ lowering arity by two, and use the exact conjugation

$$
W_0=\exp(\hbar B_0),
\qquad
d_q=W_0^{-1}d_{\mathrm{cl}}W_0
=d_{\mathrm{cl}}+\hbar\Delta_0.
\tag{69.6}
$$

The normalization of $B_0$ is the one fixed by this identity in 030. Give $\hbar^k C_n$ total weight $w=n+2k$ and define

$$
A_w^\bullet(U)=
\bigoplus_{\substack{n,k\ge0\\n+2k=w}}
\hbar^k C_n^\bullet(U),
\qquad
\widehat A^\bullet(U)=\prod_{w\ge0}A_w^\bullet(U),
\qquad
F^N\widehat A=\prod_{w\ge N}A_w.
\tag{69.7}
$$

Both differentials and $W_0^{\pm1}$ preserve total weight. Each weight contains finitely many arities, and each Wick exponential is finite on that weight. The completion is formal; no numerical value of $\hbar$ or convergence of an analytic perturbation series is claimed.

**Proposition 69.4.** Equation (69.7) is a differentiable pro-cochain complex in B.6.0.7. Tail inclusions are cofibrations and truncation maps are differentiable fibrations. Its Wick-conjugated disjoint structure maps are filtration-compatible smooth multimorphisms in B.6.1.1.

**Proof.** Give products componentwise plots and connection. A product plot whose low weights vanish is exactly a plot in the tail; hence a tail has the subspace differentiable structure. This verifies the cofibration condition directly. Finite truncation projections have smooth zero-extension chain sections, since weight is preserved. Their quotient diffeology is therefore the displayed finite product, and they are fibrations. The inverse limit of truncations is exactly the componentwise product with its connection.

The output coefficient of any weight below $N$ in a finite-input product involves finitely many input weight combinations below $N$. Theorem 69.3 therefore proves smoothness on each quotient, and hence on the product. Input filtration degrees add, so the multilinear maps preserve the required filtration. Associativity, graded symmetry, unit and compatibility with $d_q$ follow by conjugating the classical diagrams with the natural smooth maps $W_0^{\pm1}$. $\square$

This uses the differentiable multicategory, not an unsupported assertion that arbitrary differentiable spaces possess a topological tensor product. The completed coefficient operations are defined through their finite weight quotients, as required by B.6.

## 4. Completed differentiable Weiss descent

Use the Weiss convention that every finite subset, including the empty subset, is contained in a cover member; thus the index family is nonempty. The arity-zero unit is treated with the augmented nerve, not dropped.

**Theorem 69.5.** The classical and Wick-conjugated free quantum objects (69.7) satisfy completed differentiable Weiss descent for every such cover.

**Proof at fixed classical arity.** If $\{U_i\}$ is a Weiss cover of $U$, then $\{U_i^n\}$ covers $U^n$. Choose a smooth locally finite partition of unity $\{\chi_i\}$ subordinate to this tuple-space cover, averaged over the finite permutation group when necessary. Multiplication by a fixed smooth function is continuous on a normal sector and does not enlarge its wavefront.

The augmented cosheaf Čech complex of compact kernels has its usual horizontal homotopy: multiply by $\chi_j$ and insert the index $j$, with the alternating Čech signs. The support lies in the new intersection and $\sum_j\chi_j=1$ gives the homotopy identity. On a local sector plot with support $K$, only finitely many partition functions meet $K$. The output thus lies locally in a finite differentiable coproduct of intersection sectors and depends smoothly on parameters. The same is true after parameter differentiation, so the homotopy is smooth and compatible with flat connections.

This is a horizontal homotopy in each cochain degree. It need not commute with $d_{\mathrm{cl}}$, which differentiates physical kernels. Use the horizontal-first bounded double-complex argument instead: the vertical cohomological interval $[-n,0]$ is finite, so for a fixed total degree only finitely many Čech degrees occur. Horizontal exactness on every parameter stalk therefore proves that the augmented total complex is a weak equivalence of differentiable cochain complexes. Finite graded invariants preserve this argument. At arity zero the nonempty augmented nerve of the constant unit is contractible.

**Finite weight and quantum transport.** Each classical weight is a finite sum of these arity complexes. Thus every finite-weight augmentation is a differentiable equivalence. Naturality of $W_0$ under open inclusions conjugates the quantum Čech diagram and its augmentation to the classical diagram at that same weight, so the quantum result follows too.

**Completion.** Build the Čech coproduct by completing after taking the ordinary differentiable coproduct at each finite weight quotient, exactly as B.6.0.8 specifies. The truncation towers on both sides are split differentiable fibrations. Modulo a fixed $F^r$ they stabilize once the truncation exceeds $r$. The map on each successive fiber is the already proved weightwise differentiable equivalence. These are all three hypotheses of B.6.0.11; consequently the completed augmentation is an equivalence. $\square$

There is no claim that an uncompleted support colimit of complete objects equals this construction. Support and cover-index bounds may grow with total weight, as the completed coproduct permits. The obstruction in 021 remains a valid hostile control.

## 5. Scope and remaining R1 obligations

**Constructed:** a genuine sheaf of locally normal plots with flat parameter connection, smooth disjoint multilinear maps, the completed total-weight free zero-scale pro-cochain model, explicit filtration lifting properties and completed differentiable Weiss descent on that model.

**Not proved:** that this diffeology is induced by a regular/complete ordinary locally convex inductive union over supports and cones; uniform smooth dependence of the *positive-scale family* at regulator zero in that global topology; equivalence with a renormalized domain containing excluded colliding distributions; or the liquid-derived integration map of R4.

This is a positive construction on the stated refined plot class, not a repair of the refuted ambient-strong plot class. No general joint-continuity assertion has been substituted for hypocontinuity. The [fixture](fixtures/check_locally_normal_weiss_069.py) checks the algebraic parameter product rule, finite-arity grading, Čech signs and total-weight truncation/transport identities; the infinite normal-topology and differentiable arguments are the proofs above. The existing R0 oscillatory family remains a required negative control.

The broader [R1 issue #2796](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2796) must retain the unproved identification/regulator comparison obligations unless its exact acceptance scope is reconciled through review. Parent REACH is not complete from this construction alone.
