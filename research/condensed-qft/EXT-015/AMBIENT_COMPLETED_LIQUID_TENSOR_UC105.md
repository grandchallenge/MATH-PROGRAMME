# EXT-015 follow-on / UC105 — the ambient completed tensor over the shared vacuum

**Theorem.** The joint liquid parameter category with flat connection has flat projective generators, realized by finite jets along smooth maps. Its derived tensor induces a colimit-preserving completed filtered tensor and hence a symmetric relative tensor over the one completed vacuum. The latter is defined for two arbitrary complete filtered inputs. The category with one action of $\hbar$ in UC102 is its module category, and the free-input product and the actual disjoint Wick maps agree with this ambient product. Two inputs annihilated by $\hbar$ give an explicit additional negative-cohomological-degree class.

## 1. The joint category and its generator

Use the fixed real liquid site, ZFC and the joint Grothendieck category $\mathsf J_K$ of UC099 for $K=\mathbf C$, the regulator scalar sheaf. The construction also applies to $K=\mathcal O$ with the same convention. Thus a parameter manifold $N$ is a smooth finite-dimensional second-countable manifold, $\mathcal O(N)=\underline{C^\infty(N)}$, and all module actions over $K(N)$ and connection maps are liquid morphisms. The derivative on $K$ obeys the Leibniz rule and flatness. Write $R$ for the real liquid tensor unit. Tensor products at an individual manifold in this section are the ordinary relative liquid tensors. All indices are taken in the working universe of UC099.

For a fixed parameter manifold $M$ let $D_M^k=(J^k_M)^\vee$ be the real vector bundle whose fiber at $x$ is the dual of the jets through order $k$ of smooth real functions at $x$. This is the finite-dimensional jet bundle, using the full Taylor jet through order $k$. A smooth map $f:N\to M$ has an associated ordinary Fréchet space

$$
L_f^k(N)=\Gamma(N,f^*D_M^k).
$$

Choose a fixed extremally disconnected coefficient test $E$ and set $P_E=\mathcal M_{<p}(E)$. Define the presheaf with values in liquid modules

$$
G_{M,E}(N)=
\bigoplus_{f:N\to M}
  \mathrm{colim}_{k\ge0}
   \left(K(N)\otimes_{\mathcal O(N)}\underline{L_f^k(N)}\right)
   \otimes_R P_E .
\tag{UC105.1}
$$

Here the order inclusions are dual to jet truncation and the sum is over all smooth maps in the parameter site. Both colimits are liquid ones. Define the action on the $P_E$ factor by constant coefficients. For $g:L\to N$, pull the coefficients and the jet sections back and send the label $f$ to $f\circ g$. This is continuous on each Fréchet jet space and respects the scalar balance over $\mathcal O(N)$.

There is an intrinsic flat connection on the sum. For a vector field $Y$ on $N$ and a smooth jet section $\lambda$ along $f$, define the order at most $k+1$ section $\partial_Y^f\lambda$ by differentiating, in $N$, the smooth real functions $\lambda(n)(j^ku(f(n)))$ as $u$ varies over smooth scalar tests on $M$. In a chart in the source, write $\lambda=\sum_\alpha c_\alpha(n)\partial^\alpha|_{f(n)}$ with $|\alpha|\le k$. The formula is

$$
\partial_Y^f\lambda
=\sum_\alpha (Yc_\alpha)\partial^\alpha|_{f(n)}
 +\sum_{\alpha,l}c_\alpha(Yf^l)\partial^{\alpha+e_l}|_{f(n)}.
\tag{UC105.2}
$$

The formula is coordinate independent, because its two sides agree on scalar tests and any jet at a point is the jet of a compact smooth test there. It is a continuous finite-order map between the indicated Fréchet section spaces, by the local derivative formula on each compact. Extend to (UC105.1) by the Leibniz formula for $\nabla^K_Y$ on $K(N)$, and keep $P_E$ constant. The $\mathcal O(N)$ balance holds because (UC105.2) obeys the smooth-coefficient Leibniz rule. Flatness on the jet sections follows by taking the commutator of the actual derivatives of each scalar test pairing and using the bracket of vector fields on $N$. With the scalar factor the mixed Leibniz terms cancel and the $K$ connection is flat. The chain rule holds by differentiating the same pairings after pullback along $g$. The finite-idempotent cotangent convention of UC099 assembles the directional operators into the prescribed liquid connection. Thus all the presheaf operations are defined, and manifold sheafification as in UC099 gives $G_{M,E}^\#$ in $\mathsf J_K$.

**Lemma.** The sheaf $G_{M,E}^\#$ is the projective generator $Q_{M,E}$ representing $F\mapsto F(M)(E)$ in UC099.

For the universal map $P_E\to G_{M,E}(M)$ use the label $\mathrm{id}_M$, the order-zero function evaluation on the diagonal of $M$, and the scalar unit. Compose with sheafification. Given a liquid map $u:P_E\to F(M)$, the proposed morphism to $F$ is determined locally on a patch of $N$ whose image under $f$ lies in a source chart $M_0\subset M$. The map on a coordinate jet in that chart is

$$
a\,\partial^\alpha|_{f(n)}\otimes v
\longmapsto a\, f^*\bigl(\nabla_{\partial}^{\,\alpha}(u(v)|_{M_0})\bigr).
\tag{UC105.3}
$$

The formula in $v$ means a liquid map out of $P_E$, using the actual linear operators, pullbacks and bilinear scalar multiplication. On that patch the jet module through order $k$ has a finite basis of coordinate tests, which makes (UC105.3) a liquid morphism from the local coefficient object. In changing charts, induction on the order gives the same finite chain rule for compositions of covariant derivatives as for iterated partial derivatives of scalar functions. At each step the smooth coefficient is differentiated by Leibniz, and the coordinate derivatives commute by flatness. The resulting change of matrix is exactly the transformation of $D_M^k$. Thus the formulas glue by the sheaf axiom in $F$ for all liquid coefficients. On a given $N$ this defines a map from each summand and finite order of (UC105.1), then from their liquid colimits. Compatibility with the connection on $N$ follows by differentiating (UC105.3): the Leibniz term hits $a$, and the chain rule hits its pullback with the coefficient $Yf^l$ multiplying the next source derivative. These are exactly the two terms in (UC105.2). The rule is natural for every smooth pullback in $N$ and preserves the scalar action. It therefore extends uniquely from the presheaf to its sheafification.

For uniqueness, restrict first to such a patch with image in $M_0$. Apply the coordinate derivatives to the universal order-zero element, restricted from $M$ to $M_0$, and then pull back along $f|_N:N\to M_0$ on that patch. Formula (UC105.2) gives exactly the coordinate jet $\partial^\alpha|_{f(n)}$. Multiplication by coefficients generates its finite order summand there. Hence any map extending $u$ must give (UC105.3) on these patches, and therefore on the whole presheaf and its sheafification. Evaluation at the universal element and (UC105.3) are inverse. This proves the lemma even for a constant map $f$, where all higher jets are generated by differentiating in the source chart before pulling back.

## 2. Tensor-flatness and the unbounded derived tensor

Define the joint tensor of two module sheaves as the manifold sheafification of their objectwise relative tensor. It has the sum connection on the two factors. The sum is balanced by the Leibniz rule over $K$, and its commutator is flat by the two factor flatness identities. Pullbacks and finite-idempotent parameter targets give the same tensor on charts.

The following check lets us compute using the presheaf (UC105.1). On the ordinary open site of each parameter manifold, use stalks in $\mathcal A$, defined by the filtered colimits over open neighborhoods. Projective coefficient evaluation on every extremally disconnected $E'$ commutes with those colimits and with the plus constructions of UC099. It therefore identifies the evaluated stalk with the ordinary real sheaf stalk and detects sheafification equivalences jointly. The stalk of a presheaf relative tensor is the relative tensor of the stalks. Indeed the neighborhood diagonal is cofinal in a finite product of neighborhood systems, and the liquid tensor and the balancing coequalizer commute with filtered colimits. These two facts imply that a sheafification equivalence in either variable remains a sheafification equivalence after the presheaf tensor. Hence for a sheaf $F$ the tensor with $G_{M,E}^\#$ is the sheafification of $N\mapsto F(N)\otimes_{K(N)}G_{M,E}(N)$. They also verify associativity, symmetry and the unit $K$ for sheafified tensor and its cocontinuity in each variable. The comparison respects the connections by the local Leibniz formula.

For each finite $k$, the jet coefficient in (UC105.1) is a finite idempotent summand of a finite sum of $K(N)$. To see this, split the jet bundle by order using a linear connection and a metric on the finite bundles. Its associated pieces are symmetric powers of the tangent bundle, whose global finite idempotent presentation is the one used in UC099. Pulling back gives the idempotents over $\mathcal O(N)$. Taking smooth section spaces, the finite splittings are continuous in the Fréchet structure and pass to liquid modules. Extending scalars to $K(N)$ preserves those splittings. The generator $P_E$ is flat in the liquid category by [Clausen and Scholze, Condensed Mathematics and Complex Geometry, Theorem 3.14](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf#page=30). Extension of scalars gives a flat module over $K(N)$ $K(N)\otimes_R P_E$: its tensor functor is the absolute liquid tensor with $P_E$ on the other underlying module. Thus every finite-order summand in (UC105.1) is flat over $K(N)$. Filtered colimits, coproducts and retracts preserve this flatness by exactness of those colimits in the liquid module categories. This supplies flatness of all $G_{M,E}(N)$.

A short exact sequence in $\mathsf J_K$ is exact on sections at $N$ as a liquid sequence, since UC099 gives exactness after every projective coefficient test. Tensor at $N$ with $G_{M,E}(N)$ and use its flatness. Exact sheafification and the stalk comparison just proved give exactness of tensor with $Q_{M,E}=G_{M,E}^\#$. These are therefore flat projective generators of $\mathsf J_K$. In this argument flatness is relative over the regulator scalar, and uses the admitted liquid flat measure maps.

This supplies an unbounded derived tensor of joint complexes. For precision, choose functorial resolutions obtained by the small object argument with the cochain sphere-to-disk inclusions on the set of $Q_{M,E}$ and all their cochain shifts. Grothendieck local presentability supplies a regular smallness bound for the chosen set. For a replacement map, right lifting against a sphere-to-disk inclusion matches a prescribed target generator in degree $m$ and a prescribed lift of its differential in degree $m+1$. After each exact $\mathrm{Hom}(Q_{M,E},-)$, choose zero differential data to lift all target cycles. Lift the differential of a general target element this way, then the element itself. A kernel cycle bounds in the kernel by choosing zero target data. Thus these right lifting properties give a degreewise epimorphic quasi-isomorphism, detected by the projective generators. A complex constructed from zero by these cells is K-flat: a pushout attachment has degreewise split inclusion and quotient a sum of shifts of the flat generators. Tensor with an acyclic complex using direct-sum totalization. The quotient tensors are acyclic, the induction uses the resulting degreewise exact sequences, and limit stages use exact filtered colimits. This proves each replacement is K-flat. Tensor of K-flat complexes stays K-flat by associativity, and their tensor preserves quasi-isomorphisms in each variable by applying it to the acyclic cone. The localized category of these replacements is the whole $D(\mathsf J_K)$, since the functorial replacement and its natural weak equivalence give inverse equivalences after localization. Hence this gives a symmetric monoidal derived tensor with unit $K$, exact and colimit-preserving separately. For the last assertion use cones and coproducts of K-flat complexes, which again are K-flat and give derived coproducts. Exactness and preservation of coproducts give preservation of all small colimits in the stable derived category.

## 3. The full completed filtered tensor

Write $\mathcal D=D(\mathsf J_K)$ and $\mathsf{Seq}=\mathrm{Fun}(\mathbb N^{\mathrm{op}},\mathcal D)$ as in UC099. The decreasing index is symmetric monoidal under addition. Use Day convolution, left Kan extending the external derived tensor along addition. Thus

$$
(X\star Y)_n=\mathrm{colim}_{a+b\ge n}
    \bigl(X_a\otimes_K^L Y_b\bigr),
\tag{UC105.4}
$$

with arrows in the summation category given by decreasing both indices. Both the convolution and the associated grade commute with colimits in the variables indicated. Its unit is $P_0(K)$. A step object $P_a(A)$ places $A$ in levels up to $a$ with the identity transitions, and zero above. The step formula from the convolution Kan extension is

$$
P_a(A)\star P_b(B)\simeq P_{a+b}(A\otimes_K^L B).
\tag{UC105.5}
$$

For each $a+b=n$, the map from $X_a\otimes_K^L Y_b$ into (UC105.4) factors to a map into $\mathrm{gr}_n(X\star Y)$ on the cofiber of the pushout of the two adjacent higher terms. The pushout is mapped into level $n+1$, with the adjacent maps agreeing on $X_{a+1}\otimes_K^L Y_{b+1}$. Exactness of tensor identifies that cofiber with $\mathrm{gr}_a X\otimes_K^L \mathrm{gr}_b Y$. Taking their sum defines the grade comparison. It is an equivalence by (UC105.5) on step objects. The step objects generate all diagrams under colimits by the evaluation/free-diagram bar, equivalently the co-Yoneda formula for the sequence index. Thus separate preservation of colimits proves

$$
\mathrm{gr}_n(X\star Y)
\simeq \bigoplus_{a+b=n}
 \mathrm{gr}_a X\otimes_K^L\mathrm{gr}_b Y .
\tag{UC105.6}
$$

Here the grade comparison is the natural one just constructed. This is the nonnegative decreasing form of the completed convolution principle in [Gwilliam and Pavlov, Theorem 1.13](https://arxiv.org/pdf/1602.01515#page=3).

UC099 proves that the completion reflector $\mathcal L$ inverts exactly the graded equivalences. By (UC105.6) that class is closed under convolution with any object. Consequently completion is a symmetric monoidal localization, and on the full category $\mathcal K$ of complete sequences the product is

$$
X\widehat\star Y=\mathcal L(X\star Y).
\tag{UC105.7}
$$

The coherence maps are obtained by applying $\mathcal L$ to the iterated convolutions, using the equivalences after inserting any of the completion units. Its unit is the same step $P_0(K)$. It preserves colimits separately since those colimits are obtained by applying the reflector to the colimits before completion. Convolution of $P_a(K)$ with a general $X$ is the index shift $T_a X$ in UC102 by the translation Kan extension, as is also checked on the step generators and extended by colimits. That shift preserves completeness, so (UC105.7) yields the same $T_a$.

## 4. One completed vacuum and the actual relative product

Set $K=\mathbf C$ and define the single polynomial vacuum before completion by

$$
B_{\rm pol}=\bigoplus_{j\ge0}P_{2j}(K).
$$

The monomial basis has exponent $j$, and multiplication in $\star$ adds exponents using (UC105.5) with the unit $K$. This defines the commutative algebra: the symmetries of its one shifted unit and the index addition identify each multiplication of a tuple with the summand of sum exponent. Its underlying associative algebra is the tensor algebra on $P_2(K)$. Its completion $B^\wedge=\mathcal L B_{\rm pol}$ is the commutative algebra in $\mathcal K$. At the strict level it is precisely the single formal series vacuum $K[[\hbar]]$ in the stated total-weight convention, as seen by the finite quotients in UC099.

Restriction of a $B^\wedge$ action to the generator gives a functor to the action category $\mathcal H$ of UC102. It is an equivalence. Indeed the two forgetful functors have the same free monad $\coprod_{j\ge0}^{\mathcal K}T_{2j}$ with multiplication given by addition of exponents. On the module side this follows from separate cocontinuity and (UC105.7). On the single-arrow side the free action and its adjunction are UC102.2, with the same addition law under iteration. Module colimits are created on underlying objects because tensor with the algebra preserves colimits, and both forgetful functors detect equivalences. Their monadic comparison therefore gives the asserted equivalence, by [Lurie, Higher Algebra, Theorem 4.7.3.5 and Example 4.7.3.9](https://people.math.harvard.edu/~lurie/papers/HA.pdf#page=685). In particular this identifies the homotopy-coherent action categories and their mapping spaces.

For any two complete vacuum modules the ambient relative product is the two-sided derived bar realization in $(\mathcal K,\widehat\star)$,

$$
X\widehat\otimes_{B^\wedge}Y
=\left|\,[q]\longmapsto
    X\widehat\star (B^\wedge)^{\widehat\star q}
                     \widehat\star Y\,\right|.
\tag{UC105.8}
$$

The commutative algebra gives the symmetric product, and the bar preserves colimits in each module variable by separate cocontinuity. The usual augmentation for a free module is split by the extra degeneracy, so a free module on $P_a(K)$ gives the product $T_aY$. These are the relative tensor constructions of [Lurie, Higher Algebra, Construction 4.4.2.7 and Corollary 4.4.2.15](https://people.math.harvard.edu/~lurie/papers/HA.pdf#page=576), with the completed tensor of (UC105.7). By the coproduct of these cells in UC102.3, (UC105.8) is precisely $\mathcal T_U(Y)$ for the actual moment model of $U$. All the physical maps and its opposite input versions are the ones already identified by the monomial comparison and Wick conjugation in UC102.6. Thus the actual factorization and Weiss maps agree with the ambient relative tensor. In particular geometric realization of a Weiss diagram commutes with this product in either variable, and the shared module unit on the empty physical open is $B^\wedge$.

## 5. Two nonfree inputs and the additional class

Let $Q$ be the vacuum module with $K[0]$ in filtration weight zero and zero action of $\hbar$. The generator multiplication $T_2 B^\wedge\to B^\wedge$ is the inclusion of its weight-at-least-two vacuum summands. Its concrete cofiber is $Q$. This follows at each filtration level from the shift and the strict series description, so the cofiber is also the specified homotopy cofiber in $\mathcal H$. The action on $Q$ is zero since only the constant term survives. Tensor the cofiber sequence with $Q$ using (UC105.8) and the free module rule. It gives

$$
Q\widehat\otimes_{B^\wedge}Q
\simeq \mathrm{cofib}(T_2Q\xrightarrow{0}Q)
\simeq Q\oplus (T_2Q)[1].
\tag{UC105.9}
$$

The arrow agrees with the zero action on the strict quotient. The mapping space from $T_2Q$ to $Q$ in $\mathcal H$ is contractible by UC102.2: its two underlying mapping spaces are step evaluations at $2$ and $4$, where $Q$ vanishes. This fixes the nullity also in the coherent action category. The term in brackets is in cohomological degree minus one at weight two. Its coefficient $K$ is nonzero at the admitted point test. Both inputs have zero $\hbar$ action and are nonfree. Formula (UC105.9) exhibits the derived contribution explicitly. The degree-zero ordinary balance would give the one constant quotient $Q$.

The constant-map jet test in §1 checks the source derivatives that a generator must retain even at a zero-rank pullback. At the other extreme the identity map gives the ordinary differential operator jets on the same manifold. The two-shift comparison (UC105.6) checks all finite total weights, including the vacuum, and the nonfree pair detects the higher contribution of relative derivation. The analytic objects and rules are the admitted renormalized free scalar and its original whole-source quotient.

## Exact inputs

Protected input a165717f8f6b6270cea09056372c30dc81df77f5. This is a bounded structural theorem.

| Principal input | Git blob |
| --- | --- |
| [RENORMALIZED_QUANTUM_STRUCTURE_111.md](RENORMALIZED_QUANTUM_STRUCTURE_111.md) | b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| [COMBINED_PARAMETER_LIQUID_REALIZATION_126.md](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [SOURCE_CONTROLLED_COMPLETED_WEISS_135.md](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md) | 62d91e9d5f38fc85cf2793507d887d526eccce7a |
| [ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md](ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md) | 1a876fb9009adcb881fcd0eca9ea672d38ee0a82 |
| [COLLISION_LIQUID_ALL_WEIGHTS_UC093.md](COLLISION_LIQUID_ALL_WEIGHTS_UC093.md) | 21c4c2f62714f44a307ecca01676ae7900cd8f3e |
| [COLLISION_LIQUID_WEISS_UC096.md](COLLISION_LIQUID_WEISS_UC096.md) | c4feef41ff9954cff6ccb3f503c3bfc617b3a920 |
| [JOINT_LIQUID_FILTERED_COMPLETION_UC099.md](JOINT_LIQUID_FILTERED_COMPLETION_UC099.md) | 8124c1c3d7283c8642536415b8b0064de49781e7 |
| [COMPLETED_FILTERED_VACUUM_PRODUCTS_UC102.md](COMPLETED_FILTERED_VACUUM_PRODUCTS_UC102.md) | 6d5b07f01a87fbcbd94d7ecafbf19e4b6423c339 |
| [COMPLETED_VACUUM_PRODUCTS_ACCEPTANCE_UC104.md](COMPLETED_VACUUM_PRODUCTS_ACCEPTANCE_UC104.md) | df08ca57f297b9ea244058fbf11dc7a021bc2cf0 |
