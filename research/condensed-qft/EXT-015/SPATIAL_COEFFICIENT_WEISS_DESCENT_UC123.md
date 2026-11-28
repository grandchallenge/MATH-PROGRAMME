# EXT-015 follow-on / UC123 — physical Weiss descent for coefficient modules

**Theorem.** Let $U$ be any physical open for the declared one-dimensional Gaussian/Wick collision model. Let $A(U)$ be its completed collision algebra $D(U)$, or any one of the actual affine overlap algebras $C^a(U)$ for $a\ge0$. For a nonempty Weiss cover $(U_i)_{i\in J}$, restriction of scalars gives an equivalence of stable infinity categories

$$

  \mathrm{Mod}_{A(U)}(\mathcal K)
  \simeq
  \lim_{\sigma\in\mathcal I_J^{\mathrm{op}}}
       \mathrm{Mod}_{A(U_\sigma)}(\mathcal K).
  \tag{UC123.1}

$$

Here $\mathcal I_J$ is the category of all labelled Čech tuples, including those with empty physical intersection $U_\sigma$. For a cutoff that keeps weights strictly below $N$, it suffices for the cover to put every set of at most $N-1$ points in a common patch. Two separated intervals already give a counterexample to ordinary open-cover descent for coefficients when weight two is kept.

## Category and two gluing directions

Use ZFC, the real liquid site at fixed $0<p\le1$, the joint parameter category of UC099, the regulator scalar $K=\mathbf C$, and the admitted scale and rapid relation of UC111. Use the complete nonnegative decreasing filtered category $\mathcal K$ with the completed derived tensor of UC105. Put $B=B^\wedge$ for the common completed vacuum and $\mathcal V=\mathrm{Mod}_B(\mathcal K)$. This is a presentable stable symmetric monoidal category with separately colimit-preserving tensor over $B$. Regard the indicated commutative algebras over $B$ also as associative algebras in $\mathcal V$. Their left modules in $\mathcal V$ are their modules in $\mathcal K$, with the underlying action of $B$ obtained by restriction. All tensors below are derived. The cutoff version uses $\tau_N$ from UC120 and the monoidal categories $\mathcal K_{<N}$ and $\mathcal V_N=\mathrm{Mod}_{\tau_N B}(\mathcal K_{<N})$.

An object $\sigma$ of $\mathcal I_J$ is a tuple $(i_0,\ldots,i_n)$. For a nondecreasing map $[m]\to[n]$, there is an arrow to the pulled-back tuple, and the corresponding inclusion goes from $U_\sigma$ to that tuple's intersection. This is the category of elements over $\Delta^{\mathrm{op}}$ of the simplicial set with simplices in degree $n$ given by $J^{n+1}$. Its groupoidification is the realization of that simplicial set, which is contractible because $J$ is nonempty. For a covariant diagram over $\mathcal I_J$, left Kan extension to $\Delta^{\mathrm{op}}$ takes the coproduct over tuples in each degree. In $\mathcal V$ this is the usual full labelled Čech realization. The contractible indexing space depends on keeping the empty intersections with their common vacuum.

In (UC123.1) the spatial maps are restrictions of actions along inclusions of observables. In UC120 the affine maps are extensions of scalars along maps between algebraic overlaps on one fixed physical open. The distinction matters for comparing the two results.

## UC123.2 — gluing all tensor powers in the ambient category

Write $U_{\mathcal V}$ for the underlying object functor from associative algebras in $\mathcal V$. For each $s\ge0$ the augmented diagram of underlying tensor powers

$$

  \mathop{\mathrm{colim}}_{\sigma\in\mathcal I_J}
       U_{\mathcal V}A(U_\sigma)^{\widehat\otimes_B s}
   \longrightarrow U_{\mathcal V}A(U)^{\widehat\otimes_B s}
  \tag{UC123.2}

$$

is an equivalence. The term for $s=0$ is constant at $B$ and uses the contractible indexing space.

For $D$, use the actual real polynomial presentation on the singleton and higher block generators from UC108 and UC111. For $C^a$, use UC117.2 with its natural comparison to the actual overlap, so there are singleton generators and odd marked block generators with the finite label space $L_a$. The real models are graded free as modules over $\mathbb R[\hbar]$, with homogeneous bases and zero cochain differentials. Their ordinary tensor powers over $\mathbb R[\hbar]$ compute the derived powers. The coefficient and completion functor of UC108 is strong symmetric monoidal and preserves colimits. Applying it to the relative bars identifies those powers with the completed powers over $B$, naturally for all opens, including component mergers.

To see the Čech equivalence before realization in $\mathcal V$, decompose each real power by monomial shape. A shape fixes the exponent of the one shared $\hbar$, and records in each of the $s$ ordered factors the numbers of generators of each size and parity. If there are $r$ generators in the shape at total weight $w$, then $r\le w$ since each generator has positive weight. Its real coefficient space is the component vector space $\mathbb R[\pi_0(U^r)]$ tensored with the ordinary moment spaces and, for odd generators, their copy spaces $L_a$. Take coinvariants by the permutations of equal-kind positions inside each factor, with the exterior sign on odd positions. This is the same signed construction as UC111.4 with ordered factor labels. It is natural because each inclusion acts on ordered components and leaves the real coefficient spaces fixed. For $r=0$ it is constant with one empty component tuple. For $r>0$, the patches $U_i^r$ cover $U^r$ whenever the cover puts every set of up to $r$ points together. The component chain argument of UC096 and UC111 applies to these product opens. Real tensor and finite signed coinvariants preserve its exact augmented complex. This proves the claimed augmented realization for each shape, and direct sums and the coefficient functor give (UC123.2). Although the number of powers $s$ needed below is unbounded, their shapes of weight $w$ each use at most $w$ component labels.

The same argument proves (UC123.2) in weights below $N$ with the stated finite cover assumption. Since $\tau_N$ is strong symmetric monoidal and preserves colimits, this is an equivalence of the tensor-power diagram in $\mathcal V_N$. For $N=1$ only the constant shape is needed.

## UC123.3 — associative gluing

Let $F$ be the free associative algebra functor in $\mathcal V$ and $T=U_{\mathcal V}F$. The underlying free algebra is the coproduct of the tensor powers, including the unit at exponent zero. The forgetful functor is conservative and preserves geometric realizations. The augmented simplicial resolution of an algebra $H$ by $F T^q U_{\mathcal V}H$ in simplicial degree $q$ realizes to $H$. Indeed, after forgetting, the monad unit gives a split augmented simplicial object. Conservation and preservation of realization give the assertion in algebras. These are the free-algebra and sifted-colimit properties in [Lurie, *Higher Algebra*, Proposition 4.1.1.18 and Proposition 3.2.3.1](https://people.math.harvard.edu/~lurie/papers/HA.pdf).

For each $q$, the functor $T^q$ expands as a coproduct of tensor powers, by distribution of the tensor over coproducts. The indexing choices are the lengths of words at each of the $q$ iterations and are independent of the open. Equation (UC123.2) thus commutes with this construction on the given diagram. Since $F$ is a left adjoint, the colimit of the free resolutions in each simplicial degree is the free resolution over $U$. Geometric realization and the colimit over tuples commute as colimits of associative algebras. This proves the canonical equivalence

$$

 \mathop{\mathrm{colim}}_{\sigma\in\mathcal I_J}^{\mathrm{Alg}_{E_1}(\mathcal V)}
 A(U_\sigma)\simeq A(U).
 \tag{UC123.3}

$$

The same proof in $\mathcal V_N$ establishes the cutoff result. This calculation uses the additive Čech comparison for all the indicated powers to establish the associative colimit. In particular, it identifies the relations needed to act on arbitrary left modules.

## UC123.4 — descent of actions and maps

For a diagram of associative algebras with colimit $H$ over a weakly contractible index, restriction identifies the module category of $H$ with the limit of the module categories. Here is the argument in the presentable closed category $\mathcal V$ used here. The forgotten diagrams have limit the constant base category $\mathcal V$, since the groupoidification of the index is contractible. For an underlying object $M$, the space of module structures with specified underlying object is the space of associative algebra maps from $H$ to the endomorphism algebra of $M$. Use the internal Hom endomorphism algebra with multiplication by composition and the endomorphism-object characterization of actions in [Lurie, *Higher Algebra*, Theorem 4.7.1.34](https://people.math.harvard.edu/~lurie/papers/HA.pdf). The same space for a coherent family of actions is the limit of these mapping spaces for the local algebras. This is equivalent to the space for $H$ by its associative colimit. This also treats actions on arrows: apply the argument in the arrow category $\mathrm{Fun}([1],\mathcal V)$ with pointwise tensor. A module over the constant algebra diagram is an arrow of modules. The arrow category is closed and presentable, and the constant algebra functor preserves colimits into its algebra category, since algebra diagrams there are pointwise. Comparing the fibers over underlying objects and underlying arrows gives equivalences on the cores of the module categories and of their arrow categories. The mapping spaces are the fibers over endpoint pairs in the arrow cores. Thus the canonical comparison is fully faithful and essentially surjective. Applying this to (UC123.3) proves (UC123.1), including the claim at finite cutoffs.

These comparisons respect restriction of covers to smaller opens because the maps are the restriction functors and the Čech augmentations. They work for the empty open with the constant vacuum diagram. For disjoint opens, the natural separated external tensor over $B$ restricts to the same tensor of the patch actions on separated subopens. This follows from the actual disjoint algebra identifications of UC111 and UC117 and tensoring the actions over the same vacuum.

## UC123.5 — a hostile cover and a boundary between the two comparisons

Let $U=U_L\sqcup U_R$ be two separated intervals covered by the two intervals. In $\mathcal V$ take a split coefficient with one copy of $K$ in each of weights zero, one and two, written $e_0,e_1,e_2$. Give it the vacuum action through $B\to K$, with $\hbar$ acting by zero. On the left choose one singleton mass generator acting as $L(e_0)=e_1$ and zero on the other two grades. On the right choose the corresponding generator acting as $R(e_1)=e_2$ and zero on the other two grades. All other positive generators on each patch act as zero. These are module actions via the strict polynomial models, realized in $\mathcal V$. They agree on the empty intersection with the identity as the underlying identification, so give coherent data on all labelled tuples. The two singleton observables commute in the global algebra. In a global module their induced actions on the associated grades must commute since both have cochain degree zero. But $RL(e_0)=e_2$ and $LR(e_0)=0$. This distinction survives equivalence of the family, since an equivalence respecting the overlap identification transports both actions by the same graded equivalence on the shared underlying module. The unit copy is nonzero. This proves failure of essential surjectivity for the ordinary cover, including after a cutoff retaining weight two. The example works for $D$ and each $C^a$ using their respective polynomial and exterior generators. It makes no sharpness claim for larger finite orders.

It is possible to restrict a full affine descent system in space by first applying the inverse totalization of UC120, then restricting the resulting collision-algebra module and taking its affine descent system on the smaller open. The direct termwise spatial restriction of an affine system can fail its ordinal compatibility. Take $D(U)$ on one interval, whose affine family is $(C^a(U))_a$. At the empty open each overlap algebra is $B$, with identity ordinal maps. The termwise restrictions of $P(U)$ and $C^1(U)$ to $B$ are inequivalent: in weight two the latter has the three cochain-degree-minus-one pair relation classes of UC111 and the former is in degree zero. Hence they cannot be the first two terms of an affine descent system at the empty open. This gives the failure of direct restriction and an explicit transport using totalization. The result is for coefficient modules of the declared free scalar and its actual affine overlaps. It leaves the independently typed support comparison of UC088 in its original scope.

## Frozen inputs

| Input | Git blob |
| --- | --- |
| [COLLISION_LIQUID_WEISS_UC096.md](COLLISION_LIQUID_WEISS_UC096.md) | `c4feef41ff9954cff6ccb3f503c3bfc617b3a920` |
| [JOINT_LIQUID_FILTERED_COMPLETION_UC099.md](JOINT_LIQUID_FILTERED_COMPLETION_UC099.md) | `8124c1c3d7283c8642536415b8b0064de49781e7` |
| [AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md](AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md) | `61968c2deae30f0f9d7a9b382b4cfa3c098bfe1c` |
| [AFFINE_READOUT_DERIVED_RELATIONS_UC108.md](AFFINE_READOUT_DERIVED_RELATIONS_UC108.md) | `e281fd2413ab0713d4e3c825f7d02ea38b55f322` |
| [AFFINE_RELATIONS_WEISS_DESCENT_UC111.md](AFFINE_RELATIONS_WEISS_DESCENT_UC111.md) | `84565945085336d86ab731355f9029328018aec7` |
| [EXPLICIT_AFFINE_OVERLAP_DIAGRAM_UC117.md](EXPLICIT_AFFINE_OVERLAP_DIAGRAM_UC117.md) | `b19dbf62564cd7e37273533ac12984d662621ebb` |
| [AFFINE_COEFFICIENT_DESCENT_UC120.md](AFFINE_COEFFICIENT_DESCENT_UC120.md) | `e3d5109f7f8cfca782a69c7ef23146cc197a3bd0` |
