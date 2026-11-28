# EXT-015 follow-on / UC117 — a direct model for every affine overlap

**Theorem.** For the admitted renormalized free scalar on the line, the affine polynomial algebra and the marked collision-moment spaces determine an explicit cosimplicial algebra. Its maps add consecutive differences and send a collapsed difference to zero. Its completed liquid realization is equivalent to the actual derived affine overlap diagram of UC114. The comparison is natural on all opens and respects disjoint products over the shared vacuum. On one interval its signed weight-four calculation recovers the six quadratic products at stage two.

## 1. The input and the direct diagram

Use ZFC, the fixed real liquid site with $0<p\le1$, and the complete filtered joint category of UC099 and UC105 with regulator scalar $K=\mathbf C$. Keep the admitted Gaussian/Wick scale and the same whole-source rapid quotient. For an open $U\subset\mathbb R$, take $X(U)$ and $J(U)$ from UC111.1. Thus $X(U)$ has the two singleton moments in each component, and $J(U)$ has the marked moment duals of polynomials of degree at most $b$ in each component for every block size $b\ge2$. Each block has weight $b$. The ordinary real affine polynomial algebra is $P_{\mathbb R}(U)=\mathbb R[\hbar]\otimes\mathrm{Sym}_{\mathbb R} X(U)$, where $\hbar$ has weight two. Use the weight-preserving coefficient and completion functor $\mathfrak F$ of UC108.

For $[n]=\{0,\ldots,n\}$, let $L_n$ be the kernel of the sum map $\mathbb R^{n+1}\to\mathbb R$. The basis of the ambient vector space is $t_0,\ldots,t_n$. Put $u_i=t_i-t_{i-1}$ for $1\le i\le n$. A nondecreasing map $\alpha:[n]\to[m]$ sends $t_i$ to $t_{\alpha(i)}$ and preserves the sum map. Its induced map on $L_n$ is

$$
u_i\longmapsto \sum_{\alpha(i-1)<j\le\alpha(i)}u_j .
\tag{UC117.1}
$$

The sum is zero for a collapsed pair. Composition is strict because the original maps on all the $t_i$ compose. Define the real cosimplicial algebra

$$
E_{\mathbb R}^n(U)=P_{\mathbb R}(U)
      \otimes_{\mathbb R}\Lambda^\bullet(J(U)\otimes_{\mathbb R}L_n).
\tag{UC117.2}
$$

A generator with exterior length one has cochain degree minus one and the weight of its collision block. The internal differential is zero. The maps are the identity on $P_{\mathbb R}$ and extend (UC117.1) by exterior multiplication. This is a direct recipe from the affine and marked moment spaces. Inclusions send each component to its containing component by the dual polynomial restriction used in UC111. The labels in $L_n$ refer to copies of the affine readout and are independent of the physical components.

## 2. Comparison with the actual overlaps

Write $D_{\mathbb R}$ for the actual collision algebra of UC108.1 on $U$. Its affine readout is $\pi$ and its singleton section is $\sigma$. Set $\rho(\xi)=\xi-\sigma\pi(\xi)$ for $\xi\in J(U)$. The polynomial change UC108.2 identifies $D_{\mathbb R}$ with $P_{\mathbb R}\otimes\mathrm{Sym}_{\mathbb R} J$ in these variables, with $\pi\rho=0$.

Let $Q=D_{\mathbb R}\otimes_{\mathbb R}\Lambda^\bullet J$ be the commutative Koszul differential graded algebra with differential sending each odd generator for $\xi$ to $\rho(\xi)$. Its augmentation to $P_{\mathbb R}$ is a quasi-isomorphism by the Euler contraction of UC108 §2. Its terms are graded free modules over $D_{\mathbb R}$ in nonpositive cochain degrees, so it is a K-flat complex. Finite ordinary tensor powers have the same graded-freeness and bounded-above property. Consequently

$$
Q^n=Q^{\otimes_{D_{\mathbb R}}(n+1)}
   =D_{\mathbb R}\otimes_{\mathbb R}
      \Lambda^\bullet(J\otimes_{\mathbb R}\mathbb R^{n+1})
\tag{UC117.3}
$$

computes the derived relative tensor with $n+1$ affine factors. Inside (UC117.3), write $e_i(\xi)$ for the odd generator $\xi\otimes t_i$. Its internal differential is $\rho(\xi)$. The underlying strictly commutative complexes define commutative algebras in graded derived real complexes by symmetric monoidal localization. Their tensor over the algebra base is the commutative-algebra pushout, with underlying derived relative tensor. The map from the derived pushout of the copies of $Q$ to (UC117.3) is induced by the strict factor inclusions. Its underlying map is the ordinary comparison from the relative bar, which is an equivalence by K-flatness of the finite factors. The maps for all ordered-set maps match by the same factor-inclusion cocones. Thus the equivalence compares the cosimplicial algebras and their coaugmentation from $D_{\mathbb R}$. On (UC117.3) the map for $\alpha$ sends $e_i(\xi)$ to $e_{\alpha(i)}(\xi)$ and fixes $D_{\mathbb R}$. In particular the codegeneracy multiplying two adjacent factors identifies their generators with the exterior signs supplied by multiplication in the graded algebra. [Lurie, Higher Algebra, Proposition 3.2.4.7 and §4.4.2](https://people.math.harvard.edu/~lurie/papers/HA.pdf#page=371)

Map (UC117.2) into (UC117.3) by $\sigma$ on coefficients and the inclusion of the sum-zero subspace on the odd generators. Sum-zero generators are cycles, so this is a strict map of differential graded algebras. It commutes with every ordered-set map by the ambient linear formula. It is a quasi-isomorphism in each degree $n$. Indeed one can split $\mathbb R^{n+1}=L_n\oplus\mathbb R t_0$ at this stage. In this splitting (UC117.3) is the exterior algebra on the sum-zero cycles tensored over the reals with the Koszul resolution $Q$ on the copy indexed by $t_0$. The proposed map is the tensor of the exterior identity and the section from $P_{\mathbb R}$ to that copy of $Q$. The section is a quasi-isomorphism because the Koszul augmentation is one and their composite is the identity. The splitting proves equivalence at each stage. The map itself uses the sum-zero subspace and is natural without a choice of compatible splitting.

The strong symmetric monoidal and exact functor $\mathfrak F$ preserves the relative bar realizations by UC108. Applying it gives the natural equivalence of $\mathfrak F(E_{\mathbb R}^\bullet)$ and the actual completed affine overlap diagram. There is a coaugmentation of the direct model in the derived category given by the comparison through $\mathfrak F(Q^\bullet)$. In particular it is the cone $D(U)\to\mathfrak F(Q^\bullet)$ transported along the diagram equivalence. The totalization therefore recovers $D(U)$ by UC114. This argument applies the limit to an equivalence of diagrams already in the complete category.

## 3. Signs and the one-interval test through weight four

Use normalized cosimplicial cochains, the intersection of the kernels of the codegeneracies in each dimension, and truncate at the asserted stage. In cosimplicial degree $a$ use total differential $\delta+(-1)^a d$, where $d$ is the internal differential and $\delta$ is the alternating sum of cofaces. This computes the finite partial totalization of the real diagrams. The input complexes are in nonpositive cochain degrees and at fixed weight have bounded exterior length. Thus the normalized finite double complex applies, and the coefficient functor preserves the corresponding finite limits by exactness and the punctured-cube description in UC114. [Arone, Lambrechts, Turchin and Volić, §3](https://arxiv.org/pdf/math/0701350#page=6)

At stage one write $u_\xi=e_1(\xi)-e_0(\xi)$. The single relation satisfies

$$
d_{\rm tot}e_0(\xi)=\rho(\xi)+u_\xi .
\tag{UC117.4}
$$

Hence the actual augmentation carries the collision generator $\rho(\xi)$ to the class represented by $-u_\xi$ in the direct model. At stage two write $u_\xi=e_1(\xi)-e_0(\xi)$ and $v_\xi=e_2(\xi)-e_1(\xi)$. The cofaces from degree one send its adjacent difference, in order, to $v_\xi$, $u_\xi+v_\xi$, and $u_\xi$. The two codegeneracies kill $u_\xi$ and $v_\xi$, respectively, and relabel the surviving difference.

On a single interval let $V$ be the real three-dimensional pair moment space. The exterior length-two part in weight four at normalized cosimplicial degree one is $\Lambda^2 V$ on the $u$ generators. In degree two, the normalized length-two part has basis $u_\xi v_\eta$ for basis vectors $\xi,\eta\in V$. Indeed each codegeneracy kills one whole copy, and its restriction on the exterior square of the other copy is an isomorphism. There are nine ordered mixed terms. The normalized differential is

$$
\delta(u_\xi u_\eta)
= v_\xi v_\eta-(u_\xi+v_\xi)(u_\eta+v_\eta)+u_\xi u_\eta
= -u_\xi v_\eta+u_\eta v_\xi .
\tag{UC117.5}
$$

It is injective with the three antisymmetric directions as image. The six symmetric coordinates are the quotient in total degree zero. They are the actual quadratic products in the reconstructed algebra. In fact in the Koszul diagram compare the augmentation using the cochain in degrees zero and one with components $\rho(\xi)e_0(\eta)$ and $e_0(\xi)u_\eta$. The $u_\eta$ component is normalized. Direct application of the total differential gives

$$
d_{\rm tot}\bigl(\rho(\xi)e_0(\eta)+e_0(\xi)u_\eta\bigr)
   =\rho(\xi)\rho(\eta)+u_\xi v_\eta .
\tag{UC117.6}
$$

The two terms $\rho(\xi)u_\eta$ from the horizontal and signed internal maps cancel. The remaining horizontal term is $e_1(\xi)v_\eta-e_0(\xi)(u_\eta+v_\eta)+e_0(\xi)u_\eta=u_\xi v_\eta$. This includes the square when $\xi=\eta$. Thus the augmentation sends the ordered quadratic monomial to $-[u_\xi v_\eta]$, with symmetry precisely (UC117.5). Its image in stage one vanishes, and the three degree-minus-one terms of that partial stage are killed by (UC117.5) at stage two. The derived multiplication is the one from the natural commutative-algebra comparison.

For a general normalization check, the codegeneracy in position $i-1$ kills the whole space $J\otimes u_i$ and identifies all the other difference copies with the smaller ordered list. Its kernel is the exterior ideal containing that copy. The intersection over all positions is the span of exterior monomials that use every copy. At weight $w$ there is no normalization past cosimplicial degree $\lfloor w/2\rfloor$. This provides a direct finite-weight bound and in particular excludes further normalized terms in the weight-four calculation. The single common vacuum has no positive normalized degrees, since its codegeneracies are identities.

## 4. Arbitrary opens and disjoint products

All polynomials and exterior monomials use finitely many component labels. The construction therefore applies to every open, including countably many components and the empty open. The all-open actual moment and source comparison is the one of UC096 and UC111. The maps for inclusions, including component mergers, commute with both (UC117.1) and the change $\rho$ by naturality of restriction. On disjoint unions the singleton and higher block spaces are direct sums, so the affine and exterior factors give the tensor decomposition over the common $\mathbb R[\hbar]$. The same holds for the Koszul diagrams, with the exterior permutation signs on odd factors. The explicit comparison commutes with these product maps on every generator. After $\mathfrak F$, the derived relative products are over $B^\wedge$. Applying the limit cones as in UC114 gives the stated comparison of the reconstructed products. The empty-open diagram is constant at $B^\wedge$.

The fully explicit diagram concerns the admitted collision-moment algebra, its declared affine readout and the preserved regulator scalar. It gives a direct form of the overlap maps used by UC114. The original support-valued degree-two liquid comparison concerns different inputs.

Input protected cut 215da68c2c3d427464763822dbef689343b13560.

| Principal input | Git blob |
| --- | --- |
| [COLLISION_LIQUID_WEISS_UC096.md](COLLISION_LIQUID_WEISS_UC096.md) | c4feef41ff9954cff6ccb3f503c3bfc617b3a920 |
| [JOINT_LIQUID_FILTERED_COMPLETION_UC099.md](JOINT_LIQUID_FILTERED_COMPLETION_UC099.md) | 8124c1c3d7283c8642536415b8b0064de49781e7 |
| [COMPLETED_FILTERED_VACUUM_PRODUCTS_UC102.md](COMPLETED_FILTERED_VACUUM_PRODUCTS_UC102.md) | 6d5b07f01a87fbcbd94d7ecafbf19e4b6423c339 |
| [AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md](AMBIENT_COMPLETED_LIQUID_TENSOR_UC105.md) | 61968c2deae30f0f9d7a9b382b4cfa3c098bfe1c |
| [AFFINE_READOUT_DERIVED_RELATIONS_UC108.md](AFFINE_READOUT_DERIVED_RELATIONS_UC108.md) | e281fd2413ab0713d4e3c825f7d02ea38b55f322 |
| [AFFINE_RELATIONS_WEISS_DESCENT_UC111.md](AFFINE_RELATIONS_WEISS_DESCENT_UC111.md) | 84565945085336d86ab731355f9029328018aec7 |
| [AFFINE_COLLISION_RECONSTRUCTION_UC114.md](AFFINE_COLLISION_RECONSTRUCTION_UC114.md) | 2564ed9c29800d3c903393f4f99e5bcb85e0bf21 |
| [AFFINE_COLLISION_RECONSTRUCTION_ACCEPTANCE_UC116.md](AFFINE_COLLISION_RECONSTRUCTION_ACCEPTANCE_UC116.md) | 90fa57ae37f80f8c7337cbbe326420f72c19e371 |
