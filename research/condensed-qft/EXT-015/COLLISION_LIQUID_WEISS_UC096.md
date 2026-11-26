# EXT-015 follow-on / UC096 — internal liquid Weiss descent for collision moments

**Theorem.** In the fixed real liquid site and ZFC, extend the actual collision-moment comparison of UC093 to every open subset of the physical line, including infinitely many components and the empty open. For every nonempty Weiss cover, its augmented Čech realization is an equivalence in the joint liquid-valued parameter category at each total weight. This gives derived gluing in the completed split weight towers and an equivalence on their actual completed Čech models. The comparison intertwines the admitted disjoint Wick products. The fixed-profinite-test differentiable version is obtained by its own representative formulas.

## 1. All physical opens

Use the actual source objects $\mathbf F$ of 108/126/135, the common regulator algebra $\mathbf C$ and the matching Wick classicalization of 111. Work first with the classical arities, use the same $\hbar$ of weight two on all opens, and restore the quantum maps by $W_s^{-1}$ for the fixed admitted positive scale parameter $s$. Write $\mathcal I(U)$ for the open interval components of $U$, and let $T_b$ be the finite free real liquid dual of the polynomials of degree at most $b$ on the line. Restriction identifies the polynomial tests on every nonempty interval with these global polynomials. At each arity use precisely

$$
D_{\mathrm{pol}}(U)=
\mathbf C[\hbar]\otimes_R
\mathrm{Sym}_R\left(\bigoplus_{I\in\mathcal I(U),\, b\ge 1}T_b\right).
\tag{UC096.1}
$$

A generator indexed by $(I,b)$ has arity and weight $b$. The direct sum and polynomial expressions are taken in liquid parameter modules. At a fixed weight they are coproducts of scalar copies indexed by finite monomials. A component maps under inclusion to its containing component, with the same polynomial moment coordinates. Extend these maps by symmetric multiplication and the common vacuum. Complete by the product of the weight pieces.

A compact whole source stage has all its physical vertices in a finite union of components, and its genuine parameter and regulator derivative rows use one such union on their local cover. UC076 §2 proves the actual orthogonal occupancy coproduct decomposition, using 135.1 to rehost each output rectangle, including its hidden vertices. Ordered rectangles refine each symmetric occupancy by finitely many choices. The UC093 block moments on each summand give the comparison to (UC096.1). The inverse moment sections and homotopies can be chosen in the occupied components for each arity. The coproduct of these maps and identities gives a split chain homotopy equivalence on the whole arity. Here split means that the forward chain map has an objectwise chain section and its kernel is contractible. The projections and moment sections use the actual entire source representatives and rapid relation of UC076 and UC093, with the same genuine rows. Local finite collections yield the maps on the liquid parameter sheaves. The same finite stage identities hold directly on the fixed-test representatives.

To verify naturality for an inclusion of arbitrary opens, test on one whole compact stage. Both its occupied components and their images in the larger open form finite unions of components. The naturality of UC093 on those unions applies to the entire stage, including any merger of components. Independence of the chosen finite unions follows by the same identities for their finite join. This verifies naturality on the cover-local whole sources and hence on the actual quotient. The same argument with a finite family of compact source stages proves the disjoint product diagram, using the shared vacuum. In the case of disjoint inputs, no block joins two inputs. All these operations act before fixed-test evaluation. Formula (UC096.1) is a coproduct of moment generators. Its construction has no use for dualizing the full space of piecewise affine fields on an infinitely disconnected open.

**First test.** Let $I_j=(2^{-2j-1},2^{-2j})$ for $j\ge 1$, and $U=\bigsqcup_{j\ge1} I_j$. Cover by the increasing finite unions $U_N=\bigcup_{j\le N}I_j$. This is a Weiss cover, and every monomial of fixed arity occurs in some $U_N$. At each weight the filtered union of its scalar coproducts gives exactly the corresponding piece of (UC096.1). Its Čech calculation is already split over the reals. For each monomial the indices that contain all its components form a nonempty tail, so its augmented tuple complex is the full simplex on those indices. At the parameter point and coefficient singleton, choose the mass generator $e_j$ of an actual pair block in $I_j$. The series with weight $2j+2$ coordinate $\hbar^je_j$ is admitted in the completed model. No single $U_N$ represents this series, since projection to the pair coordinate in $I_j$ detects every $j>N$. The completed gluing must therefore perform support gluing at each weight before assembling the series. Conversely the fixed-weight coproduct excludes a section with a nonzero pair coefficient on every component at that same point and weight. The UC076 locally finite parameter reading of the coproduct still allows different finite supports on different parameter neighborhoods.

## 2. Block centers and a topological Čech lemma

Let $\{U_i\}_{i\in \Lambda}$ be a nonempty set-indexed Weiss cover of $U$. A finite set of points of $U$ is contained in some $U_i$. For each nonnegative integer $r$, the opens $U_i^r$ cover $U^r$, including tuples with repetitions. Put $U^0=\{*\}$ for every $U$, including the empty open. For a tuple of cover labels $\mathbf i=(i_0,\ldots,i_a)$ write $U_{\mathbf i}=\bigcap_j U_{i_j}$. Then the intersections of the product patches are precisely $U_{\mathbf i}^r$. They may have arbitrarily many components. Each component is a product of intervals and is convex. For $r=0$ every labelled intersection is the point.

For arity $n$, choose an ordered list of block sizes $\mathbf b=(b_1,\ldots,b_r)$ in nondecreasing order with $\sum b_\ell=n$. Let $G_{\mathbf b}$ be the product of the symmetric groups permuting blocks of equal size. In the monomials of this shape, (UC096.1) has the following explicit description.

$$
\left(\coprod_{\eta\in\pi_0(U^r)}
  \mathbf C\otimes_R T_{b_1}\otimes_R\cdots\otimes_R T_{b_r}
\right)_{G_{\mathbf b}} .
\tag{UC096.2}
$$

The component label is the ordered list of interval components of the block centers. The group permutes these labels together with their equal-size moment factors. The formula includes the empty shape with $r=0$ and scalar $\mathbf C$. A monomial is an unordered list of these decorated blocks, which gives exactly (UC096.2). When two blocks have centers in the same interval they retain their separate positions in the ordered list before the symmetric quotient. The formulas allow coinciding center points. This identifies inclusions in (UC096.2) with the maps of components of the product opens, even where several components merge.

Here is the topological comparison over ordinary real vector spaces. Write $\mathbb R[\pi_0(X)]$ for the free vector space on components. The augmented alternating tuple complex of the diagram $\mathbb R[\pi_0(U_{\mathbf i}^r)]$ is exact, with augmentation to $\mathbb R[\pi_0(U^r)]$. To prove this, use a first-quadrant double complex with singular chains $C_q(U_{\mathbf i}^r;\mathbb R)$ in the vertical direction and alternating deletion of cover labels in the horizontal direction. The canonical vertical augmentation takes each point to its component and sends chains of positive dimension to zero. Since all the components are convex, each vertical augmentation to the free component vector space is a quasi-isomorphism. The same applies on the whole $U^r$. These maps are natural for the open inclusions.

In each horizontal degree the chain groups are direct sums over labelled tuples. Augment in the horizontal direction to the small singular chains, whose individual simplices lie in one product patch. For each such simplex $\sigma$, its summands in this augmented row are the full simplex on the nonempty set of labels of patches containing its image. Prepend one such label as a cone operator. Its boundary identity contracts the augmented row. All rows are exact by taking the direct sum over simplices. The inclusion of small singular chains into all singular chains is a chain homotopy equivalence by barycentric subdivision for an open cover. [Hatcher, Algebraic Topology, Proposition 2.21](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf#page=23)

The horizontal and vertical comparisons of the double complex thus identify the augmented component Čech map as a quasi-isomorphism. The first-quadrant filtrations converge because each total chain degree has finitely many horizontal and vertical degree choices. The proof works for arbitrary physical covers and uses objectwise component homology. The chain map is equivariant for coordinate permutations, since the singular augmentations and all cover maps are. There is one full simplex on $\Lambda$ for the vacuum, with every labelled intersection retained even when the physical intersection is empty.

## 3. Derived liquid gluing and the actual completion

For the shape $\mathbf b$ tensor the real component chains with the ordinary real polynomial-moment basis factors and take the finite-group coinvariants. Real averaging makes coinvariants exact. Identifying equal label permutations in the target uses precisely this quotient. The resulting augmented real vector-space complex is exact. Choose a splitting contraction of this exact complex over the real field. Linearizing its real basis in the joint liquid parameter category means replacing each real basis vector by a scalar copy of $\mathbf C$ and each matrix by its column-finite matrix of real scalar maps. This uses coproducts and their universal property. Real linear maps take each algebraic basis vector to a finite sum, so the maps and the contraction identities extend on the sheaves. Changing real bases gives inverse column-finite matrices. Thus the linearization of the given augmented chain complex is canonically the liquid complex in (UC096.2), with a contraction. Equivalently one may use the real averaging idempotent to form its direct summand before linearization. The contraction commutes with the parameter connection because its coefficients are constant real scalars. Use the same construction directly in the fixed-test coefficient categories with their scalar sheaves. The contraction is built in the joint liquid category itself.

Use the actual full tuple Čech complex and its direct-sum totalization for each weight. In cochain degree, horizontal simplicial degree $a$ counts as $-a$. The usual degeneracy summand is contractible and the normalized complex represents the simplicial derived realization. Indeed the split degeneracies give its skeletal filtration with normalized pieces and alternating face differential. Exact coproducts in the liquid module categories identify the derived coproducts in each level with these actual coproducts. The finite sums for the arities of any particular weight, and the shape decompositions (UC096.2), therefore prove weightwise derived Weiss gluing for $D$. Equivalently the intersection-poset bar model can be used via the finite chain comparison of 135.3a, whose forward coefficient maps apply to these liquid modules. The physical augmentation and all comparison maps preserve weights. The scalar $\hbar$ shifts weight by two, and the contractions may be chosen once for each arity and used on all its $\hbar^k$ copies.

There is also a comparison of the actual completed source Čech model. At each arity and for each labelled intersection, the split moment equivalence from §1 has a contractible kernel. Form the direct sums of these kernels by Čech degree. Naturality of the forward moment comparison makes these kernels a Čech subcomplex. Equip them with vertical signed contractions $h$ chosen by summand, so that $d_v h+h d_v=1$. For the horizontal face differential $\delta$, the operator $1+\delta h$ is invertible by a finite series on each horizontal level since $\delta h$ lowers that level. Therefore the total kernel has contraction

$$
H=h(1+\delta h)^{-1}.
\tag{UC096.3}
$$

Indeed $(d_v+\delta)(1+\delta h)=(1+\delta h)d_v$ and $(d_v+\delta)h=1+\delta h-hd_v$. These identities give $(d_v+\delta)H+H(d_v+\delta)=1$. Each matrix entry is a finite composition of actual source maps. The comparison is degreewise split by the objectwise moment sections on the Čech summands, and its total kernel is contractible. Hence it is a chain homotopy equivalence. This argument applies directly in the joint parameter category and in each fixed-test version. It needs no natural choice of the individual contractions and uses the actual maps on the negligible-error quotient.

At each finite total-weight cutoff take the direct sum of the above realizations. The truncation maps just discard weights, so these realizations form the completed split tower. The completed model takes the product of the fixed-weight total complexes. The comparison with the moment Čech complex, its augmentation and the source moment equivalence on $U$ are homotopy equivalences after taking this product, since the actual homotopies assemble componentwise. This verifies the derived descent comparison in the split completed weight towers and the equivalence for the actual assembled complexes. The Čech coproducts in this construction occur within individual weights. Applying the natural inverse Wick map in the source gives the same result for its quantum differential and Wick structure maps.

## 4. Controls and scope

The finite exact fixture checks labelled Čech boundaries and ranks for the component model, including repeated patch labels, distinct intersection components that merge, the vacuum on empty intersections, and a cover by the two separate components with the mixed two-center sector missing. This last cover glues arity one and fails the Weiss condition, so the missing mixed monomial is a genuine cokernel in that test. Covering by all two-component subunions in a finite three-component model glues up to two centers and misses the three-distinct-center coordinate. These tests concern component combinatorics. The topological double complex proves the arbitrary-cover result. The all-open source proof uses the actual compact rehosting, moment maps, rapid remainder estimates and parameter rows of the frozen inputs.

The theorem concerns the same renormalized free scalar on the line. It keeps the common regulator vacuum, the collision observables, and finite occupations at fixed weight. It constructs the completed derived liquid descent in the specified weight-preserving split towers. The fixed-test differentiable statement is an additional direct realization. The original degree-two support comparison and the earlier obstruction for recovering every prior parameter family have their existing scopes.

## Exact inputs

Input protected cut 782f113fc8881927b4aba48aa93e49d1573a0cac. The original REACH and the completed finite-component collision-liquid returns are historical sources. This is one bounded research return.

| Principal source | Git blob |
| --- | --- |
| [MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | 587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| [RENORMALIZED_QUANTUM_STRUCTURE_111.md](RENORMALIZED_QUANTUM_STRUCTURE_111.md) | b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| [COMBINED_PARAMETER_LIQUID_REALIZATION_126.md](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [SOURCE_CONTROLLED_PROCOCHAIN_APPLICABILITY_129.md](SOURCE_CONTROLLED_PROCOCHAIN_APPLICABILITY_129.md) | 9b3f38f476646bf6ee395701d8b033cc8d3c265c |
| [SOURCE_CONTROLLED_COMPLETED_WEISS_135.md](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md) | 62d91e9d5f38fc85cf2793507d887d526eccce7a |
| [FINITE_PARTITION_TENSOR_UC073.md](FINITE_PARTITION_TENSOR_UC073.md) | 1201a231c6573fd09f71ecb74ceb667398cae58f |
| [ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md](ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md) | 1a876fb9009adcb881fcd0eca9ea672d38ee0a82 |
| [COLLISION_LIQUID_WEIGHT_TWO_UC092.md](COLLISION_LIQUID_WEIGHT_TWO_UC092.md) | 5cd16144edd52cb46829df41dd2e79e0c0a3df9f |
| [COLLISION_LIQUID_ALL_WEIGHTS_UC093.md](COLLISION_LIQUID_ALL_WEIGHTS_UC093.md) | 21c4c2f62714f44a307ecca01676ae7900cd8f3e |
| [COLLISION_LIQUID_ACCEPTANCE_UC095.md](COLLISION_LIQUID_ACCEPTANCE_UC095.md) | 342feb5256543396b9aa013ca9661c342c9fa54a |
