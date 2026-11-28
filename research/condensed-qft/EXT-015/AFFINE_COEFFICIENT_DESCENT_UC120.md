# EXT-015 follow-on / UC120 — effective descent for affine coefficient modules

**Theorem.** On every physical open $U$ of the line, extension of scalars along the actual derived affine overlap diagram induces an equivalence

$$
  \mathrm{Mod}_{D(U)}(\mathcal K)
    \xrightarrow{\;\sim\;}
  \lim_{[a]\in\Delta}\mathrm{Mod}_{C^a(U)}(\mathcal K),
  \qquad C^a(U)=P(U)^{\widehat\otimes_{D(U)}(a+1)}.
  \tag{UC120.1}
$$

This is an equivalence of symmetric monoidal stable infinity categories. Its inverse is totalization of the underlying compatible modules over $D(U)$. It respects extension of coefficients for open inclusions, separated external products over the common completed vacuum, and the empty region.

## Category and hypotheses

Use ZFC and the same fixed $0<p\le1$, real liquid site, joint parameter category $\mathsf J_K$ and regulator scalar $K$ as UC099 and UC105. Put $\mathcal D=D(\mathsf J_K)$. The ambient category $\mathcal K$ consists of sequences $X_{i+1}\to X_i$ in $\mathcal D$ for $i\ge0$ with $\lim_i X_i=0$. Its symmetric tensor is the completed Day tensor of UC105. All modules and tensors below are derived. Use UC111's collision algebra $D(U)$, affine algebra $P(U)$, augmentation $\pi:D(U)\to P(U)$ and completed vacuum $B^\wedge$, with the same Gaussian/Wick and rapid quotient conventions. The actual augmented diagram is UC114's, with the explicit cosimplicial presentation of UC117.

On the right of (UC120.1) a map $[a]\to[b]$ acts by extension of scalars along $C^a(U)\to C^b(U)$. A compatible system includes equivalences $C^b(U)\widehat\otimes_{C^a(U)}Y_a\simeq Y_b$, with their higher coherences. This is the category of full descent data.

## UC120.2 — finite weight cutoffs and complete coefficients

For $N\ge1$ let $\mathcal K_{<N}$ consist of sequences zero in indices $i\ge N$, and define

$$
  (\tau_N X)_i=
  \begin{cases}
    \mathrm{cofib}(X_N\to X_i)& i<N,\\
    0&i\ge N.
  \end{cases}
$$

The inclusion of $\mathcal K_{<N}$ is the right Kan extension from the finite interval $0,\ldots,N$ of a diagram zero at $N$. At each $i>N$, the indexing category for the right Kan extension has initial object $N$, so the limit is zero. In the finite diagram, maps from the constant diagram on $X_N$ to $Y$ are maps $X_N\to Y_N$, since $N$ is initial. Their mapping space is contractible for $Y\in\mathcal K_{<N}$. Taking the cofiber of the natural map from the constant diagram on $X_N$ to $X$ thus gives the reflector $\tau_N$. Limits in both sequence categories are levelwise. Finite cofibers commute with all limits in a stable category, so $\tau_N$ preserves all limits as well as all colimits. The category $\mathcal K_{<N}$ is stable and presentable by its finite diagram description.

The grade in weight $i<N$ of $\tau_N X$ is $\mathrm{cofib}(X_{i+1}\to X_i)$, by the cofiber triangles, including $i=N-1$. At weights at least $N$ it is zero. Finite induction from the zero tail shows that $\tau_N$ inverts exactly the equivalences on grades below $N$. Those equivalences are stable under tensoring with any object of $\mathcal K$ by UC105.6, since the grades add with nonnegative indices. The localization therefore carries the symmetric tensor with $\tau_N$ strong monoidal. The tensor preserves colimits separately by applying the reflector to the ambient tensor on representatives. For $M\ge N$, the factorization $\tau_N\tau_M\simeq\tau_N$ is strong monoidal for the successive localized tensors. In particular the truncations preserve relative tensor products and their coherences, by applying them to the actual two-sided bars.

There is a symmetric monoidal equivalence

$$
  \mathcal K\simeq\lim_{N\ge1}\mathcal K_{<N}.
  \tag{UC120.2}
$$

Indeed, for each $i$, take the limit of the finite cofiber sequences $X_N\to X_i\to(\tau_NX)_i$ over $N>i$. Completeness and exactness of the limit identify the last term with $X_i$. Conversely, for a compatible tower $(X^{(N)})_N$ the zero-extended sequences have transition maps given by the units of the reflectors and the specified equivalences $\tau_N X^{(N+1)}\simeq X^{(N)}$. The adjunctions for the nested cutoffs give these maps with the composition coherences. Their levelwise limit belongs to $\mathcal K$, since the two limits over weight and cutoff commute and each finite sequence has zero tail. Applying $\tau_N$ to this limit yields $X^{(N)}$, since $\tau_N$ preserves limits and the truncated tower is eventually equivalent to $X^{(N)}$. Both constructions are functorial, proving (UC120.2) on objects and maps. The cutoff functors are strong monoidal, and the target limit tensor is coordinatewise.

For any commutative algebra $A$ in $\mathcal K$ put $A_N=\tau_N A$. Equation (UC120.2) gives

$$
  \mathrm{Mod}_{A}(\mathcal K)
    \simeq\lim_N\mathrm{Mod}_{A_N}(\mathcal K_{<N}).
  \tag{UC120.3}
$$

In the coordinatewise limit an algebra with a module is specified by the compatible diagrams for the two-colored algebra and module operad. The functor categories on this fixed operad preserve target limits. The conditions on inert morphisms and operations are checked in each coordinate. Taking the fiber over the algebra $A$ gives (UC120.3), including module maps. The equivalence is symmetric monoidal because the cutoff functors carry relative tensors to relative tensors. It is natural in $A$ for extension of scalars by the same bar calculation.

## UC120.3 — descent at each cutoff

Write $D=D(U)$, $P=P(U)$ and $I=\mathrm{fib}(D\to P)$. Let $I_N=\tau_N I$, the fiber for $D_N\to P_N$ by exactness. Each copy of $I$ has minimum weight two by UC114. The nonnegative weights in the relative bar then show that $I^{\widehat\otimes_D k}$ has zero grades below $2k$. For $k=\lceil N/2\rceil$ we get

$$
 I_N^{\widehat\otimes_{D_N}k}
 \simeq \tau_N\bigl(I^{\widehat\otimes_D k}\bigr)=0.
 \tag{UC120.4}
$$

Work in the presentable stable category $\mathrm{Mod}_{D_N}(\mathcal K_{<N})$, with separately colimit-preserving tensor over $D_N$. The punctured cube on $k$ copies of the map $D_N\to P_N$ has a term $P_N^{\widehat\otimes_{D_N}|S|}$ for every nonempty subset $S$ of its positions. Iterating the fibers of the unpunctured cube gives the left side of (UC120.4), by exactness of tensor. It follows that the finite limit of the punctured cube is $D_N$. Its terms belong to the thick tensor ideal generated by $P_N$. Finite limits stay in this ideal by stability, so it contains the tensor unit $D_N$. Thus $P_N$ is descendable in this module category.

Mathew's descent theorem applies in this stable, presentably symmetric monoidal category. The Amitsur algebras there are the actual $C^a_N=\tau_NC^a$, by the bar calculation. Modules over them are the modules over $C^a_N$ in $\mathcal K_{<N}$ since $C^a_N$ is a algebra over $D_N$. Consequently extension of scalars is an equivalence

$$
  \mathrm{Mod}_{D_N}(\mathcal K_{<N})
    \simeq\lim_{[a]\in\Delta}\mathrm{Mod}_{C^a_N}(\mathcal K_{<N}).
  \tag{UC120.5}
$$

The proof uses neither a dualizability assumption on the affine algebra nor a bound on the number of components of $U$.

## UC120.4 — effective descent and operations

Comparison (UC120.5) is natural under cutoffs because both sides use extension of scalars and the cutoffs preserve the relative bars. Apply (UC120.3) to $D$ and every $C^a$ and interchange the two category limits. This proves (UC120.1) for the canonical comparison. The argument interchanges category limits, so it requires no interchange of an arbitrary relative tensor with an infinite limit of underlying modules.

For a compatible system $Y$, adjunction turns its extension-of-scalars equivalences into a cosimplicial diagram of modules over $D$ $(\mathrm{Res}^{C^a}_{D}Y_a)_a$. The mapping space from the canonical image of a module over $D$ $M$ to $Y$ is the limit of the termwise mapping spaces from $C^a\widehat\otimes_D M$ to $Y_a$. By adjunction it is the mapping space from $M$ to

$$
  \mathrm{Tot}_{[a]\in\Delta}\mathrm{Res}^{C^a}_{D}Y_a .
  \tag{UC120.6}
$$

Here the cosimplicial maps encode the given coherences. This gives the right adjoint of (UC120.1), hence its inverse. For an already fully compatible system, UC114 and (UC120.6) show that its recovered module below weight $N$ is computed from degrees at most $\lceil N/2\rceil-1$. This statement concerns the recovered underlying module, with the action given by the limit in modules over $D$.

An open inclusion transports both sides by extension of scalars. Its square with (UC120.1) commutes by associativity of scalar extension for the natural map of augmented diagrams of UC117. For disjoint $U,V$, the identifications $D(U\sqcup V)\simeq D(U)\widehat\otimes_{B^\wedge}D(V)$ and $C^a(U\sqcup V)\simeq C^a(U)\widehat\otimes_{B^\wedge}C^a(V)$ respect the coaugmentation and ordinal maps by UC114 and UC117. Thus base change of the external relative tensor over $B^\wedge$ gives the termwise external tensor of compatible systems. Both inverse constructions correspond under the equivalence. At $U=\varnothing$ the algebra and diagram are constant at $B^\wedge$, whose module category is recovered.

## UC120.5 — controls and limits of the theorem

- **Sharp bound on finite descent.** For a nonempty open choose one pair mass difference $r$ in a component, at weight two. If $2k<N$, its power of order $k$ is nonzero in $D_N$, by the polynomial calculation of UC114 at the parameter point and coefficient singleton. The multiplication map $I_N^{\widehat\otimes_{D_N}k}\to D_N$ hits that power. Thus the least positive exponent in (UC120.4) is $\lceil N/2\rceil$. In the whole category the fiber multiplication is nonzero for each positive exponent. In particular the untruncated $P$ on a nonempty open fails the finite tensor-nilpotence criterion for descendability. Its effective descent follows from the compatible finite weight results.
- **Unfiltered loss.** In the corresponding ordinary real polynomial model on an interval, the module $D_{\mathbb R}[r^{-1}]$ is nonzero. Its derived scalar extension to $P_{\mathbb R}$ is zero by flatness of localization and $\pi(r)=0$, so its whole Amitsur module diagram vanishes. The complete positive weight category in (UC120.1) is essential to the argument. This control uses ordinary unfiltered real modules.
- **A nontrivial filtration with zero first underlying object.** In the diagram of UC099 take $Y_0=[K\xrightarrow{1}K]$ in degrees $-1,0$, $Y_1=K[0]$ included in the last term, and $Y_i=0$ for $i\ge2$. Give it the module over $D$ structure via $D\to P\to K$, setting singleton and quantum generators to zero. Here $Y_0$ is acyclic, $Y_1\ne0$, and $\mathrm{gr}_0Y\simeq K[1]$, $\mathrm{gr}_1Y=K$. The theorem recovers this entire filtered object from its compatible system, including the relation between its two grades. Treating the module as its level-zero value would give zero.

The theorem concerns full compatible systems in a fixed complete nonnegative category. It gives no extension claim for arbitrary data given only on a finite partial diagram. The original support-stage comparison and the conditional degree-two verdicts of UC088 concern different objects and maps and are unaffected.

## Frozen inputs and literature

| Input | Git blob |
| --- | --- |
| [JOINT_LIQUID_FILTERED_COMPLETION_UC099.md](JOINT_LIQUID_FILTERED_COMPLETION_UC099.md) | `8124c1c3d7283c8642536415b8b0064de49781e7` |
| [AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md](AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md) | `61968c2deae30f0f9d7a9b382b4cfa3c098bfe1c` |
| [AFFINE_READOUT_DERIVED_RELATIONS_UC108.md](AFFINE_READOUT_DERIVED_RELATIONS_UC108.md) | `e281fd2413ab0713d4e3c825f7d02ea38b55f322` |
| [AFFINE_RELATIONS_WEISS_DESCENT_UC111.md](AFFINE_RELATIONS_WEISS_DESCENT_UC111.md) | `84565945085336d86ab731355f9029328018aec7` |
| [AFFINE_COLLISION_RECONSTRUCTION_UC114.md](AFFINE_COLLISION_RECONSTRUCTION_UC114.md) | `2564ed9c29800d3c903393f4f99e5bcb85e0bf21` |
| [EXPLICIT_AFFINE_OVERLAP_DIAGRAM_UC117.md](EXPLICIT_AFFINE_OVERLAP_DIAGRAM_UC117.md) | `b19dbf62564cd7e37273533ac12984d662621ebb` |
| [EXPLICIT_AFFINE_OVERLAPS_ACCEPTANCE_UC119.md](EXPLICIT_AFFINE_OVERLAPS_ACCEPTANCE_UC119.md) | `8db9b84e2ee93cfacb4fe45332548647e721b63c` |

For the categorical descent theorem and the fiber nilpotence criterion use [Akhil Mathew, *Examples of descent up to nilpotence*, Theorem 2.41 and Proposition 2.32](https://math.uchicago.edu/~amathew/Vancouver.pdf). The theorem there cites Proposition 3.22 of *The Galois group of a stable homotopy theory*. The comparison with finite Amitsur stages uses the punctured cube identification as in UC114 and [Mathew, Naumann and Noel, *Nilpotence and descent in equivariant stable homotopy theory*, Proposition 2.14](https://arxiv.org/pdf/1507.06869).
