# EXT-015 follow-on / UC111 — Weiss gluing for the derived affine collision relations

**Theorem.** For the admitted renormalized free scalar in the complete filtered joint liquid category, the affine self-tensor of UC108 extends to all physical opens of the line, with the same shared vacuum and disjoint products. It satisfies completed derived Weiss descent. At total weight $w$ the intrinsic degree $-q$ summand glues over a Weiss cover of order $k$ as soon as $k\ge w-q$, if $2q\le w$. For $w-q\ge2$ this bound is optimal as a uniform guarantee. A cover by proper subunions of $w-q$ disjoint intervals can miss a class of that weight and degree.

## 1. All opens and the actual relative tensor

Use ZFC, the fixed real liquid site with $0<p\le1$, the joint category of UC099, and its completed tensor of UC105 over the regulator scalar $K=\mathbf C$. Fix the admitted Wick scale and whole-source rapid relation. Let $T_b$ be the ordinary real dual of the polynomials on the line of degree at most $b$. Restriction gives the same test space on every nonempty interval. For an arbitrary physical open $U$ define ordinary real weight-graded spaces

$$
X(U)=\bigoplus_{I\in\pi_0(U)}T_1,\qquad
J(U)=\bigoplus_{I\in\pi_0(U),\,b\ge2}T_b .
\tag{UC111.1}
$$

The generator from $T_b$ has weight $b$. Use the polynomial algebras $D_{\mathbb R}(U)$ and $P_{\mathbb R}(U)$ of UC108.1 with these spaces and with $\hbar$ of weight two. The fold $\pi$ is the identity on singletons and the common vacuum. Its value on each higher block is the singleton polynomial on that same component specified by UC093 §4. It commutes with inclusion even when components merge. The coefficient and completion functor $\mathfrak F$ of UC108 §2 gives $D(U)$ and $P(U)$. Here $D(U)$ is the actual all-open moment model of UC096. For the admitted whole-source comparison the affine readout on an infinite-component open is obtained on every compact source stage by the finite-component formula. A compact subset meets finitely many components, by the finite subcover of its component cover. Its images under any fixed inclusion occupy finitely many containing components. The compatible evaluations on those stages and their genuine parameter rows give the same fold using the UC096 whole-source argument. This readout uses the coproduct over occupied components.

Let $E(U)=P(U)\widehat\otimes^L_{D(U)}P(U)$. The polynomial coordinate change $\xi\mapsto\rho(\xi)$, with $\rho$ as in UC108.2, is defined on the direct sum over all components. The Euler contraction of the Koszul resolution still applies, since every polynomial and exterior monomial uses finitely many variables. The graded-free resolutions and the antisymmetrized bar comparison of UC108 apply to the resulting infinite homogeneous basis as well. Exactness of the real bar and the graded-projective cone argument have no finite-rank assumption. The functor $\mathfrak F$ takes this bar and its realization to the actual completed bar. Thus there is an all-open natural comparison

$$
E(U)\simeq\mathfrak F\bigl(E_{\mathbb R}(U)\bigr),
\qquad
E_{\mathbb R}(U)=
\mathbb R[\hbar]\otimes_{\mathbb R}\mathrm{Sym}_{\mathbb R}X(U)
                  \otimes_{\mathbb R}\Lambda^\bullet J(U),
\tag{UC111.2}
$$

with zero differential and $\Lambda^q$ in cochain degree $-q$. The comparison uses UC108.3 on each wedge, so the exterior signs and component-merger maps apply to each product. No arbitrary dual of the space of all piecewise affine fields is used.

For disjoint $U,V$, the generators of $U\sqcup V$ are the direct sums of their two sets. The algebraic symmetric and signed exterior decomposition gives the map $E_{\mathbb R}(U)\otimes_{\mathbb R[\hbar]}E_{\mathbb R}(V)\to E_{\mathbb R}(U\sqcup V)$ as an isomorphism. These graded complexes have free homogeneous bases over $\mathbb R[\hbar]$ and zero differential, so the corresponding relative bar computes that tensor. The compatible shuffle map on the bars is precisely the signed multiplication of the displayed representatives by UC108.3. Apply $\mathfrak F$ and its comparison of the relative bars to obtain the disjoint-union equivalence over the actual completed vacuum $B^\wedge$. The maps for disjoint inputs inside a larger open are these maps followed by the inclusions, which gives symmetry, associativity and unit through the explicit inclusion and product rules. The empty open has $E(\varnothing)=B^\wedge$. The underlying comparison with the renormalized disjoint Wick products on $D$ is the one in UC096.

## 2. Signed component chains and the finite gluing bound

A Weiss cover of order $k$ here means a nonempty open cover for which every subset of at most $k$ points is contained in one patch. Use the full labelled tuple Čech diagram with all labelled intersections. A Weiss cover has this property for every finite $k$. At weight $w$ and intrinsic cochain degree $-q$ of (UC111.2), choose an exponent $h$ of $\hbar$, a number $a$ of singleton factors, and a nondecreasing list of $q$ exterior block weights $b_i\ge2$. The list satisfies

$$
w=2h+a+\sum_{i=1}^{q}b_i,\qquad r=a+q\le w-q .
\tag{UC111.3}
$$

A shape consists of these data. Write $G=S_a\times\prod_{b\ge2}S_{\#\{i:b_i=b\}}$ and write $\chi$ for the product of sign characters on the exterior factors, trivial on $S_a$. Its coefficient space at $U$ is canonically

$$
\left(
\mathbb R[\pi_0(U^r)]\otimes T_1^{\otimes a}\otimes
  T_{b_1}\otimes\cdots\otimes T_{b_q}\otimes\mathbb R_\chi
\right)_G .
\tag{UC111.4}
$$

The ordered centers specify the interval labels of every factor. The permutation group acts both on the ordered components and on the corresponding tensors. The sign twist produces the exterior powers, including the vanishing of a repeated identical exterior generator, while the singleton factors are symmetric. This is the symmetric and exterior quotient on the tensor basis, so it intertwines the actual component fold even when labels coincide. Inclusions are the maps on components of the product opens. The centers may coincide as points. The vacuum has $r=0$ and uses $U^0=\{*\}$ for every $U$, including $\varnothing$.

For a shape of length $r\le k$, the cover condition implies the patches $U_i^r$ cover $U^r$ by applying it to the distinct entries of the tuple. The component Čech lemma of UC096 §2 then gives exactness of the augmented alternating tuple complex on $\mathbb R[\pi_0(U_{\mathbf i}^r)]$, where $U_{\mathbf i}$ is a labelled intersection. In that argument each component of a product open is convex. Augment singular chains on each product patch to its component space, and in the other direction contract the tuple rows of the small chains on each simplex by adding a cover label containing that simplex. Small singular chains compute the full singular chains for the product open cover by subdivision. The augmentation and component comparison are equivariant for coordinate permutations. [Hatcher, Algebraic Topology, Proposition 2.21](https://pi.math.cornell.edu/~hatcher/AT/ATch2.pdf#page=23)

Tensor the exact augmented component complex with the real coefficient factors in (UC111.4) and take the finite signed coinvariants. Averaging over $G$ is a splitting idempotent over the reals even for the sign-twisted representation. It gives exactness after all these operations. Only after taking the signed quotient use the real scalar copower of UC102, which carries the splitting of the exact real complex to a contraction in the joint liquid category. The maps use constant real coefficients and commute with the parameter connection. This proves gluing for the shape shifted to degree $-q$. Normalize the full labelled Čech complex if desired by removing its split degeneracy summand. There are finitely many shapes for each pair $(w,q)$. Equation (UC111.3) therefore gives the bound for their direct sum. This is a statement about the intrinsic degree summand of the split model. The realization itself also has the Čech degrees. The vacuum summand is the full simplex on the nonempty cover label set since every labelled intersection contributes the same scalar.

For a Weiss cover every shape glues. The real weight-graded augmented realization is then an equivalence, and $\mathfrak F$ preserves its realization in the complete filtered category by UC108. Thus the complete augmentation is an equivalence of the actual derived relative tensor diagrams by naturality of their bar comparison. Equivalently, each associated weight is the exact sum of the above Čech complexes and the complete augmentation is detected by those weights by UC099. This proof assembles the finite-weight local supports through completion. Disjoint products use the same augmentation maps and the signed product of (UC111.2). The completed tensor over $B^\wedge$ preserves these realizations in each argument by UC105, so gluing can be performed before or after a disjoint product.

## 3. Sharpness and controls

Let $2q\le w$ and $r=w-q\ge2$. Take $U$ to be a disjoint union of $r$ nonempty intervals and use the cover by all $r-1$ component subunions. It is Weiss of order $r-1$. Choose one nonzero mass coordinate of a pair relation in each of $q$ different components, and one singleton mass coordinate in each of the remaining $w-2q$ components. Their product with exterior signs for the pair relations is a nonzero monomial in (UC111.2) with weight $w$ and degree $-q$. Every patch and intersection omits at least one of these labels. The component inclusions keep all the other labels, so projection to this monomial annihilates the entire augmented source realization. The target coordinate is nonzero already at the admitted point test. This proves failure in degree $-q$ for the intrinsic weight and degree summand, even after completion. Since this cover is also Weiss of order $k$ for every $1\le k<r$, the uniform bound is sharp. The cases $r=0,1$ are covered by the vacuum and the ordinary open cover case.

For example, in weight four and degree minus two on two separate intervals, each interval contributes the exterior square of its three pair relations. An ordinary cover by the individual intervals therefore supplies six of the fifteen target coordinates. It misses the nine mixed products, one pair relation from each interval. If two relation factors are identified by a component merger, (UC111.4) instead gives the zero repeated wedge, in agreement with UC108. For an increasing Weiss cover by finite subunions of countably many intervals, the successive classes $\hbar^j e_j$, where $e_j$ is a pair relation in the interval with index $j$, give a completed series with weight $2j+2$ entries. Each entry is represented on a finite subunion. No single finite subunion represents the series, as projection to any missed component shows. This detects the order of local gluing and weight completion.

## Scope and exact inputs

This is a statement about the actual completed relative tensor built from the specified moment algebra and its affine readout. Its products use the polynomial model with the admitted comparison for disjoint regions. The original support-valued liquid Ext comparison has its separate objects and verdict. Finite occupancy and the joint real scalar copower supply the liquid result before any fixed-profinite-test evaluation.

Input protected cut 323066f82c53f88c1e74d92532e65e196478db0f.

| Principal input | Git blob |
| --- | --- |
| [COLLISION_LIQUID_ALL_WEIGHTS_UC093.md](COLLISION_LIQUID_ALL_WEIGHTS_UC093.md) | 21c4c2f62714f44a307ecca01676ae7900cd8f3e |
| [COLLISION_LIQUID_WEISS_UC096.md](COLLISION_LIQUID_WEISS_UC096.md) | c4feef41ff9954cff6ccb3f503c3bfc617b3a920 |
| [JOINT_LIQUID_FILTERED_COMPLETION_UC099.md](JOINT_LIQUID_FILTERED_COMPLETION_UC099.md) | 8124c1c3d7283c8642536415b8b0064de49781e7 |
| [COMPLETED_FILTERED_VACUUM_PRODUCTS_UC102.md](COMPLETED_FILTERED_VACUUM_PRODUCTS_UC102.md) | 6d5b07f01a87fbcbd94d7ecafbf19e4b6423c339 |
| [AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md](AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md) | 61968c2deae30f0f9d7a9b382b4cfa3c098bfe1c |
| [AFFINE_READOUT_DERIVED_RELATIONS_UC108.md](AFFINE_READOUT_DERIVED_RELATIONS_UC108.md) | e281fd2413ab0713d4e3c825f7d02ea38b55f322 |
| [AFFINE_READOUT_RELATIONS_ACCEPTANCE_UC110.md](AFFINE_READOUT_RELATIONS_ACCEPTANCE_UC110.md) | b23376c4e7eb59e009abfab1b31c46ebe4a6c744 |
