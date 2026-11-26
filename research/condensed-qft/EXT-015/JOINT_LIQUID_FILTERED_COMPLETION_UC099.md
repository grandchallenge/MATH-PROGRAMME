# EXT-015 follow-on / UC099 — full filtered derived gluing in the joint liquid category

**Theorem.** In the joint liquid parameter category of the renormalized free scalar, strict completion of an ordinary monomorphic cochain sequence represents derived completion. The completed bar computes the colimit in the category of all derived-complete filtered liquid complexes. In particular UC096 gives the Weiss colimit there, with its mapping-space property into arbitrary complete filtered targets. An increasing cover by finite subunions of intervals gives an explicit nonzero obstruction to taking the same colimit in the unfiltered category.

## 1. Joint liquid parameter modules have exact products

Fix the real liquid site and the category $\mathcal A=\mathrm{Liq}_p(\mathbb R)$ for the admitted $0<p\le 1$. Use the smooth finite-dimensional, second-countable parameter manifolds and local-diffeomorphism covers of 126 and 129, in a working universe for all site and diagram indices. Let $\mathcal O(M)=\underline{C^\infty(M)}$. Let $K$ be $\mathcal O$ or the actual regulator scalar sheaf $\mathbf C$ of 135, with the latter's $\mathcal O$ action and flat parameter differential. Let $\mathsf J_K$ be the category of manifold sheaves of liquid modules over $K$, with natural flat parameter connection and its Leibniz rule over $K$. At each $M$ the connection takes values in the actual finite idempotent summand $\underline{\Omega^1(M)}\otimes_{\mathcal O(M)}F(M)$ of a finite power, as in 126. Morphisms commute with the scalar action, pullback and connection. In particular the joint observables of UC096 are complexes in $\mathsf J_{\mathbf C}$.

Here are the categorical details for this joint category. A convenient presentation before the manifold sheaf condition is by the following unary operations in $\mathcal A$. For each parameter manifold $M$, include scalar multiplication, parametrized by the liquid object $K(M)$, and differentiation along each ordinary smooth vector field $X$ on $M$. For each smooth map $f:N\to M$ include pullback from $M$ to $N$. In each ordered pair of manifolds form the coproduct of tensor products of the operation objects for finite composable words. Impose concatenation, units, scalar multiplication, naturality, linearity in the vector field over ordinary smooth functions, the Leibniz and flatness relations, and the pullback chain rule, by quotienting by the generated liquid two-sided relation ideal. For relations with variable scalars use maps from $K(M)$ or its liquid tensors. For example the Leibniz relation with a fixed $X$ uses the morphism $\nabla_X^K:K(M)\to K(M)$. The tensor preserves coproducts and cokernels, so these presentations give a small liquid-linear operation category and its representations.

To see the equivalence with the declared presheaf operations, choose once on each $M$ a finite spanning frame of vector fields with a smooth splitting, with dual finite family of one-forms. Such a frame comes from the finite tangent idempotent of 126 §7's construction of the cotangent target. The operators along the frame reconstruct the connection by pairing with those one-forms. The relations expressing the frame idempotent are the smooth-function linearity relations, so this reconstructed map lands in the idempotent summand. Contraction with every $X$ gives its stipulated operator, and the finite frame detects both curvature and the chain rule. For a map $f:N\to M$, the differential of any vector field on $N$ decomposes in the pullback of the chosen frame of $M$ with finitely many smooth coefficient functions on $N$. The chain rule is therefore among the finite-word relations above. This construction yields exactly the finite-idempotent connection convention and uses the full liquid scalar multiplication.

Kernels and cokernels of presheaf morphisms are formed objectwise with the induced operations. For kernels the composite into the quotient of the desired kernel vanishes by naturality, which gives the factorization. For cokernels use right exactness of liquid tensor. Products and coproducts have their universal operations, and filtered colimits are objectwise exact. The projective tests $P_E=\mathcal M_{<p}(E)$ for extremally disconnected $E$ are compact projective generators of $\mathcal A$ in the chosen site. They give exact evaluation, detect exactness and commute with filtered colimits. See [Scholze, Lectures on Analytic Geometry, Theorem 6.5](https://arxiv.org/pdf/2605.03655#page=35) and 126 §6 for the generator and sheafification consequences used here.

Manifold sheafification is computed on the underlying liquid presheaf. The two plus constructions commute with the projective tests $P_E$ because they use limits and filtered colimits. On those tests they are ordinary sheafification, which is exact. Scalars and derivatives extend by their local formulas, and the relations hold locally and agree on restrictions. Pullbacks and the connections then descend and satisfy the finite-idempotent rule. Consequently the resulting sheafification is left adjoint to inclusion and exact. The sheaf category has a generating set: for each $M,E$ freely place $P_E$ at $M$ in the operation presheaf and sheafify. The free presheaf is its tensor with the represented operation module from $M$, so the resulting $Q_{M,E}$ represents $F\mapsto F(M)(E)$. Their zero tests detect the zero sheaf. Filtered colimits are exact after sheafification of the exact pointwise filtered colimits. This proves the Grothendieck property, including a set of generators.

For an epimorphism $B\to C$ in $\mathsf J_K$ and $c\in C(M)(E)$, exact sheafification and projectivity of $P_E$ imply local lifts of $c$ to $B(V_i)(E)$ on an ordinary open cover. One may take ordinary opens because local diffeomorphisms admit open inverse branches. Choose a locally finite smooth partition of unity subordinate to these lifts. Multiply each lift by its partition function using the scalar section pulled back from the ordinary smooth function. Extend by zero outside the support of that function and sum locally. The sheaf identity glues this finite local sum to a lift in $B(M)(E)$. No derivatives are prescribed for the lift, and a section multiplied by a smooth function is an allowed section by the Leibniz rule. This proves exactness of all $F\mapsto F(M)(E)$ and, in particular, projectivity of the $Q_{M,E}$.

Products are formed in the joint category sectionwise. The product connection has the declared target because finite powers and finite idempotent summands commute with products. The exact functors $F\mapsto F(M)(E)$ preserve those products. A product of epimorphisms is therefore onto after each such functor, and these functors detect exactness. Thus products are exact in $\mathsf J_K$. This is the joint liquid analogue of 129 §7 step 1. Its proof uses the chosen projective coefficient tests.

## 2. Completion in the full filtered derived category

Set $\mathcal D=D(\mathsf J_K)$, the stable derived category with its homotopy-coherent diagrams, and set $\mathsf{Seq}=\mathrm{Fun}(\mathbb N^{\mathrm{op}},\mathcal D)$. A filtration is an arbitrary sequence with arrows $X_{n+1}\to X_n$. Its grade at $n$ is the cofiber of that arrow. A sequence is derived complete if $\lim_n X_n=0$ in $\mathcal D$. Limits, colimits and cofibers in this paragraph are derived. The exactness of products proved above also gives degreewise models for derived products of complexes, by taking injective-model replacements and using exactness to compare their products.

The completion reflector is

$$
\mathcal L X=\mathrm{cofib}\bigl(\mathrm{const}(\lim_n X_n)\longrightarrow X\bigr).
\tag{UC099.1}
$$

Indeed the sequence index has terminal object $0$ and contractible nerve, so the limit of a constant diagram is its value. Taking the limit of (UC099.1) proves completeness, since a limit in a stable category is exact. For any complete $Y$, maps from a constant diagram to $Y$ form a contractible mapping space, by the constant and limit adjunction. The defining cofiber then gives the mapping-space adjunction $\mathrm{Map}(\mathcal L X,Y)\simeq\mathrm{Map}(X,Y)$. The unit preserves all grades. Each grade is a colimit-preserving cofiber of two evaluations; the cofiber of a map inducing equivalences on grades has all its transitions invertible and is equivalent to a constant diagram. Therefore grades detect equivalences of complete sequences and the reflector inverts precisely the graded equivalences. This is the stable completion mechanism of [Gwilliam and Pavlov, Theorem 1.11](https://arxiv.org/pdf/1602.01515#page=3) and 129 §7 step 3, specialized here in the joint category.

For a concrete degreewise monomorphic sequence of complexes write $Q_n=X_0/X_n$. The countable quotient tower has degreewise epimorphic transitions. The comparison of its strict limit with its derived limit uses the fiber of $1-\mathrm{shift}$ on the product. Exact products model the derived product degreewise. After any of the exact tests $F\mapsto F(M)(E)$, the equation

$$
z_n-p_n z_{n+1}=b_n
$$

is solved degreewise by choosing $z_0$ and recursively lifting $z_n-b_n$. Thus $1-\mathrm{shift}$ is degreewise epimorphic and its strict kernel $\lim_n Q_n$ computes the derived limit. The same upward lifting from a prescribed value at any index proves that $\lim_n Q_n\to Q_n$ is epimorphic degreewise. It follows that the concrete strict completion is the following sequence.

$$
\widehat X_n=\ker\bigl(\lim_j Q_j\longrightarrow Q_n\bigr).
\tag{UC099.2}
$$

Its maps are monomorphisms and its successive quotients are the original grades. The short exact sequences for $X_n\subset X_0$ give a derived triangle $\lim_n X_n\to X_0\to\lim_n Q_n$. Comparing the fibers of $X_0\to Q_n$ and $\lim_j Q_j\to Q_n$ shows that the fiber of $X_n\to\widehat X_n$ is $\lim_j X_j$, with its canonical maps at every level. This is natural in $n$. Thus (UC099.2) is an actual representative of (UC099.1). The proof applies to monomorphic sequences with nonsplit successive quotients.

For any strict small diagram of such filtered complexes, take the ordinary direct-sum simplicial bar at each filtration index, with coefficients in $\mathsf J_K$. Its simplicial degeneracy splittings or its normalized skeleton identify the direct-sum total with the geometric realization, and exact coproducts compute the derived coproducts. This represents the levelwise homotopy colimit in $\mathsf{Seq}$. Its transitions remain monomorphic by the actual direct sums of the monomorphic arrows. Therefore its strict quotient completion (UC099.2) represents the homotopy colimit in the full category of derived-complete sequences. This comparison uses derived diagram objects and the mapping-space adjunction and the strict quotient proof.

## 3. The actual Weiss comparison in that category

Use $K=\mathbf C$. Equip the actual source $\mathbf F_s^\wedge(U)$ and the collision-moment comparison target of UC096 with their weight-tail filtrations in $\mathsf{Seq}$. Each such concrete sequence is already strictly complete by the product of its weights and so represents a complete object by §2. For a Weiss cover $\mathcal U$ use the full labelled tuple Čech diagram with Čech degree $a$ the coproduct over $a+1$ labels of the intersection values. All weights, including even vacuum weights and physically empty intersections, use the maps of UC096. The ordinary direct-sum realization is the filtered Čech model and its strict quotient completion is the representative of the complete filtered colimit. The finite-label intersection-poset bar of 135.3a gives the same answer by its finite, filtration-preserving chain comparisons. In the strict split source models, completion of the realization here agrees with the actual product of weightwise Čech complexes in UC096. The finite quotient below weight $n$ is the finite sum of those weightwise total complexes.

The grade of the completed augmentation to $\mathbf F_s^\wedge(U)$ is exactly the weightwise Čech augmentation proved an equivalence in UC096, internal to the joint liquid parameter category. Grade detection proves the augmentation is an equivalence of complete filtered sequence objects. In particular for **every** complete filtered object $Y$ in $\mathsf{Seq}$ there is an equivalence of mapping spaces

$$
\mathrm{Map}(\mathbf F_s^\wedge(U),Y)
\simeq
\lim_{[a]\in\Delta}
\prod_{(i_0,\ldots,i_a)}
\mathrm{Map}(\mathbf F_s^\wedge(U_{i_0,\ldots,i_a}),Y).
\tag{UC099.3}
$$

The right side uses the cover maps, and the mapping spaces are in the full complete filtered category. Formula (UC099.3) allows maps that mix weights subject to the filtration and allows nonsplit targets. A concrete test target has $Y_0=[\mathbf C\xrightarrow{1}\mathbf C]$ in degrees minus one and zero, $Y_1$ the degree-zero copy of $\mathbf C$, and $Y_n=0$ for $n\ge2$. It is a finite monomorphic filtration, hence complete. In $\mathcal D$ its level zero vanishes and its first tail is nonzero. Its grades are $\mathbf C[1]$ and $\mathbf C[0]$ at the first two indices. A split product of these grades at level zero would be nonzero. This tests the distinction between complete targets and split weights without any ambiguity from profinite evaluation.

The augmentation and comparison are natural for all physical inclusions, commute with the parameter connection, and intertwine the admitted disjoint Wick products by UC096. The same scalar $\hbar$ shifts the filtration by two on both sides. The formal grading identifies the associated grades of this comparison. The filtered universal property uses the full ambient complete sequence category.

## 4. Exact unfiltered failure on the same cover

Let $U$ and $U_N$ be the increasing cover by the finite unions of intervals of UC096 §1. In this case the moment model may be used for every open, by its natural chain equivalences with $\mathbf F_s^\wedge$. Write $D_w$ for one total weight of the moment model, concentrated in cochain degree zero, and write

$$
A=\mathrm{colim}_N\prod_{w\ge0}D_w(U_N),\qquad
D^\wedge=\prod_{w\ge0}D_w(U),\qquad
Z=\mathrm{coker}(A\longrightarrow D^\wedge).
\tag{UC099.4}
$$

The colimit in (UC099.4) is computed on these degree-zero objects because filtered colimits in $\mathsf J_{\mathbf C}$ are exact. It is also the unfiltered labelled Čech realization for this increasing cover. To see this identification, the functor from nonempty finite subsets of cover labels, ordered by reverse inclusion, to $\mathbb N$ sends the set to its minimum. Its undercategory for a fixed $N$ is the nonempty reverse-inclusion poset of finite subsets of indices at least $N$. The union of a finite collection gives a common object mapping to them, and its nerve is contractible. The functor is therefore homotopy final. With the finite Čech/bar comparison of 135.3a this identifies the realization. The map from $A$ to $D^\wedge$ is a monomorphism: it is a filtered union of the monomial submodules in the full product.

At the manifold point and coefficient singleton, the class with weight $2j+2$ coordinate $\hbar^j e_j$ for the mass coordinate of the pair block in $I_j$ is nonzero in $Z$. Every element in the image of $A$ at those tests comes from one stage $U_N$. Evaluation there commutes with filtered colimits, since sheafification is trivial at the manifold point, which has split covers, and the coefficient singleton is compact projective. Projection to the marked pair in $I_j$ for $j>N$ annihilates that entire stage. This proves a genuine unfiltered failure of the augmentation for the actual model.

The exact completion defect is visible in the tail tower of the ordinary colimit. Put $A_n=\mathrm{colim}_N\prod_{w\ge n}D_w(U_N)$ with its inclusions into $A$. Exact filtered colimits give $A/A_n=\bigoplus_{w<n}D_w(U)$, since every fixed-weight monomial is supported in finitely many components. These finite quotient towers have limit $D^\wedge$, also derived by §2. The triangle for tails therefore gives

$$
\lim\nolimits_n^{\mathrm{derived}}A_n
\simeq \mathrm{fib}(A\longrightarrow D^\wedge)
\simeq Z[-1].
\tag{UC099.5}
$$

The ordinary intersection of the tails is zero, since all coordinate projections of an element in it vanish. The derived limit has the nonzero cohomology object $Z$ in degree one. Equation (UC099.5) computes the defect for this model and cover, beyond the abstract support and limit controls of 021. Applying (UC099.1) removes exactly this tail-limit obstruction and yields the correct completion.

## Scope and exact inputs

This is a bounded theorem in the joint liquid parameter categories defined in §1, using the pre-existing source domain, negligible-error relation and all-open UC096. It gives the actual full filtered colimit and an unfiltered counterexample for the same free field. The historical degree-two support comparison has a different coefficient diagram. The nonzero object $Z$ in (UC099.5) comes from this countable weight completion, using ZFC.

Input protected cut 4150c19d66a30183897dd41712833924be1e2d73.

| Principal input | Git blob |
| --- | --- |
| [RENORMALIZED_QUANTUM_STRUCTURE_111.md](RENORMALIZED_QUANTUM_STRUCTURE_111.md) | b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| [COMBINED_PARAMETER_LIQUID_REALIZATION_126.md](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [SOURCE_CONTROLLED_PROCOCHAIN_APPLICABILITY_129.md](SOURCE_CONTROLLED_PROCOCHAIN_APPLICABILITY_129.md) | 9b3f38f476646bf6ee395701d8b033cc8d3c265c |
| [SOURCE_CONTROLLED_COMPLETED_WEISS_135.md](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md) | 62d91e9d5f38fc85cf2793507d887d526eccce7a |
| [ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md](ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md) | 1a876fb9009adcb881fcd0eca9ea672d38ee0a82 |
| [COLLISION_LIQUID_ALL_WEIGHTS_UC093.md](COLLISION_LIQUID_ALL_WEIGHTS_UC093.md) | 21c4c2f62714f44a307ecca01676ae7900cd8f3e |
| [COLLISION_LIQUID_WEISS_UC096.md](COLLISION_LIQUID_WEISS_UC096.md) | c4feef41ff9954cff6ccb3f503c3bfc617b3a920 |
| [COLLISION_LIQUID_WEISS_ACCEPTANCE_UC098.md](COLLISION_LIQUID_WEISS_ACCEPTANCE_UC098.md) | 7c96b8f1e8510a930831405632a097620868faa9 |
| [DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md](DERIVED_WEIGHT_COMPLETION_BOUNDARY_021.md) | 537b26091ba2a7b44dd69069f7614ea40542f0b5 |
