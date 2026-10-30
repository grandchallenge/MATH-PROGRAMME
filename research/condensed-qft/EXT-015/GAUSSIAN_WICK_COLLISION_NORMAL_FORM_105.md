# EXT-015 REACH / 105 — an actual Gaussian/Wick integral normal form

**Disposition: construction candidate with a scalar zero-scale closure theorem and an unresolved mixed-coefficient extension.** This return gives an explicit positive-regulator normal form with complete liquid coefficient stages. An exact projective change of coordinates identifies the heat collision maps with restrictions of many-body maps. This proves closure of the scalar Gaussian/Wick and finite collision-jet sector in a power/logarithmic enlargement, including its boundary quotient. General distributional R1 coefficients require an additional theorem. This is not the full M2 exit theorem or GB2. Review106 and ledger107 are separate.

## 1. Frozen inputs, category and the claim under test

The protected scientific input is e7caf6bce90b6c2ae49b2154149be5b5a6706cdd, preserved on branch `research/reach-gaussian-wick-input-frozen-20261030`. CP039 binds the user-authorized closure attempt before construction. Work in the real liquid heart with fixed $0<p\le1$, ZFC and the same one-dimensional physical spacetime and interval basis. All finite vertex dimensions below describe configurations of that model.

| Dependency | Exact Git blob |
| --- | --- |
| Protocol090 | 6b642bf10c3328bb64d37474e290810fb45cbca1 |
| Actual-family subtraction087 | 452c494bcdc94ba94e52ae50c7b4d1eb3240ca83 |
| Liquid realization091 | c517fe1ae46bcaa9f4a3fc0e64381ae8096bfe27 |
| Full normal-profile and collision geometry096 | ee15ed47d90123bdd958dcb4a93cd51b428c1702 |
| Actual collar-source image099 | bcdd5328c52361403b54c24c662c336bff4ce7ae |
| Broad-domain projection obstruction102 | a4767b539bdd1127a001d51ac81c5ef1cf526e07 |

The eleven-edge host,277 proper sources, two legal disjoint spinneys, all fixed finite decorations and the marked identity of087 are mandatory. The target is closure under the operations actually used by that model. No unrestricted product of singular distributions, or product of overlapping source counterterms, enters the claim.

The new mechanism is an integral formula with independent noise variables for edges and a finite physical linear projection. Its definition quantifies over explicit coefficient spaces and finite linear data. It is not the instruction to apply arbitrary words of operations and retain the word as a state. Equal evaluated kernels are identified.

## 2. Complete coefficients with a necessary joint wavefront condition

Let $w\in\mathbb R^N$ be physical vertex coordinates, $z\in\mathbb R^m$ auxiliary noise variables, and $K$ a fixed compact physical support. Let $E_{K,\Gamma}$ be a fixed normal distribution sector in $w$, with support in $K$ and closed wavefront cone $\Gamma$. For an original R1 input the cone avoids every partial-diagonal conormal, including simultaneous collisions. Other compositions below are admitted only with the stated noncharacteristic coefficient maps; no arbitrary R1 multiplication is added.

Write $\Gamma^0=\{(w,z;\xi,0):(w;\xi)\in\Gamma\}$. Define a coefficient space by the closed graph intersection

$$
\mathcal A_{K,\Gamma,m}
=\mathcal S\bigl(\mathbb R^m_z,E_{K,\Gamma}\bigr)
\mathop{\times}_{\mathcal D'(\mathbb R^{N+m})}
\mathcal D'_{\Gamma^0}(\mathbb R^{N+m}),
\qquad
\mathcal P_{K,\Gamma,m}
=C^\infty([0,e_0],\mathcal A_{K,\Gamma,m}).
\tag{105.1}
$$

The first factor has every Schwartz seminorm in $z$, for every derivative in $z$ and every defining normal seminorm of $E_{K,\Gamma}$. The second factor has its normal topology. The two distributions are required to agree, not retained as independent data. Physical support in the second factor is also restricted to $K$.

**Lemma105.1.** These are complete Hausdorff locally convex spaces and their condensed realizations are liquid. They contain $T(w)\varphi(z)$ for every $T\in E_{K,\Gamma}$ and $\varphi\in\mathcal S(\mathbb R^m)$.

**Proof.** Fixed closed-cone normal spaces are complete by the input used and checked in099. Smooth Schwartz functions with values in a complete locally convex space are complete for the displayed seminorms: every Cauchy net and each derivative converge uniformly in each weighted seminorm, and the fundamental theorem of calculus identifies the limits as the derivatives. Both factors map continuously into ordinary distributions. Equality there is a closed condition because that target is Hausdorff. Hence the graph intersection is complete. The same argument with compact-interval smooth seminorms proves completeness of $\mathcal P$. The measure-extension argument of096/099 makes each complete locally convex realization liquid. The tensor $T\varphi$ has wavefront in $\Gamma^0$ and all the required Schwartz bounds, proving the last assertion. $\square$

The joint-cone condition is essential. Smooth dependence on $z$ with values in distributions in $w$ does not alone exclude joint wavefront with a nonzero noise covector. In(105.1) that exclusion is imposed and preserved by the stated maps. It cannot be inferred from scalarwise smoothness.

The following source maps preserve such stages, with a suitable fixed output cone and physical compact set: fixed physical derivatives, multiplication by a fixed smooth function with polynomially bounded noise derivatives on $K$, independent exterior products with their joined tensor cone, and explicitly noncharacteristic linear physical pullbacks. Smooth regulator dependence and its derivatives are included. For exterior factorization of R1 inputs use disjoint physical opens, as in069.3. Overlapping supports require their own noncharacteristic condition.

## 3. Explicit normal form

Put $P_0(t)=|t|/2$, and let each $F_e$ be a fixed derivative of $P_0$ or of $\delta_0$. These are one-dimensional tempered distributions. Set $F(v)=\boxtimes_{e=1}^mF_e(v_e)$. Choose finite linear data:

- a partition collision stratum $D$, with linear inclusion $i_D$ into the physical input configuration;
- difference forms $\ell_e$ on $D$, collected in $L:D\to\mathbb R^m$;
- a physical vertex-forgetting projection $q$ on that input configuration;
- a finite physical differential monomial $\partial^\beta$, a regulator power $\epsilon^k$, and $a\in\mathcal P_{K,\Gamma,m}$ in coordinates on $D$.

The represented actual family is

$$
\mathcal T_\epsilon(a)
=\epsilon^k q_*\partial^\beta(i_D)_*
\left[\int_{\mathbb R^m}
a(\epsilon,w,z)\,F(Lw+\epsilon z)\,dz\right],
\qquad \epsilon>0.
\tag{105.2}
$$

Use the actual coordinate densities in the pushforward and the absolute determinants of every invertible linear coordinate change. Compact physical support makes $q$ proper on the input support. For $m=0$ the bracket is simply $a(\epsilon,w)$, and for the identity partition $i_D$ is the identity. Finite sums are allowed. Source normal delta jets are represented by $(i_D)_*$ and $\partial^\beta$, rather than products of their singular kernels.

**Lemma105.2.** Formula(105.2) is defined and gives a continuous linear map from its coefficient stage to the ordinary positive-regulator kernel envelope. Its dependence on $\epsilon$ is smooth on every compact subinterval of $(0,e_0)$. The statement holds for continuous profinite coefficient families and locally fixed-stage smooth manifold families.

**Proof.** For fixed positive $\epsilon$, the map $(w,z)\mapsto Lw+\epsilon z$ is a submersion. Every nonzero covector in the pullback wavefront of $F$ has noise component $\epsilon\eta\ne0$. The coefficient has noise covector zero. Their product therefore satisfies the wavefront product condition. One can also define the bracket without that product notation: change variables $v=Lw+\epsilon z$ and pair the fixed tempered distribution $F(v)$ with

$$
\epsilon^{-m}a\bigl(\epsilon,w,(v-Lw)/\epsilon\bigr).
\tag{105.3}
$$

On a compact positive regulator interval this translation and dilation maps(105.1) continuously to Schwartz functions of $v$ with distributional $w$ coefficients. Physical support is compact. Every requested derivative produces only finitely many physical or noise derivatives, polynomial factors in $v$ and bounded inverse powers of $\epsilon$. The joint cone remains $\Gamma^0$ under this change of variables. Pairing a fixed tempered distribution is continuous in these Schwartz seminorms. It yields a distribution with physical wavefront contained in the chosen physical coefficient cone. Differentiation, stratum pushforward and proper $q_*$ are continuous in the ordinary distribution target; testing supplies the envelope map.

The same finite seminorm estimates apply uniformly to bounded coefficient sets. Compact images of profinite plots are bounded, so these are genuine continuous plotted maps. Derivative estimates give the specified manifold smoothness. No estimate uniform as $\epsilon\downarrow0$ is claimed in this lemma. $\square$

## 4. The actual Gaussian/Wick kernels are represented exactly

Let $\varphi(z)=(2\pi)^{-1/2}e^{-z^2/2}$. In ordinary tempered-distribution pairings,

$$
\int\varphi(z)\delta(t+\epsilon z)\,dz=\kappa_\epsilon(t),
\qquad
\int\varphi(z)P_0(t+\epsilon z)\,dz=P_\epsilon(t).
\tag{105.4}
$$

The first formula follows from the delta scaling rule with positive $\epsilon$. The second is exactly the Gaussian convolution defining the Wick propagator. Replacing either distribution by its derivative gives the corresponding physical derivative, since $\partial_t$ differentiates its argument with coefficient one. Tensoring the independent Gaussian noise densities represents a whole finite graph simultaneously, even with a disconnected Gaussian backbone or Wick bridges.

All277 proper sources, both spinneys and every fixed finite derivative, polynomial decoration or Laurent factor are instances of(105.2). Finite normal insertions use the indicated stratum pushforward and derivatives. R1 inputs are the case $m=0$, or $T(w)\varphi(z)$ when edges are added. The scalar unit is the zero-dimensional, zero-noise case with coefficient one. Compact cutoffs are coefficient multipliers, not an assertion that the uncut Wick profile is Schwartz.

The tail statement motivating this construction is precise: $P_1(u)-|u|/2$ and all its derivatives away from the origin decay faster than every inverse polynomial as $|u|\to\infty$. This follows from Gaussian tail integration in(105.4). At the origin this difference has the cusp inherited from $-|u|/2$; it is not a Schwartz function. Formula(105.2) retains the actual distribution $P_0$, so it does not make that false replacement.

## 5. Positive-scale closure and actual-family descent

**Theorem105.3.** Finite sums of(105.2) are closed, at positive regulator, under the following typed operations: physical derivatives and polynomial or smooth compact coefficient multipliers; regulator Laurent shifts and positive rescalings; legal disjoint exterior composition; addition of an actual Gaussian or Wick edge on the current output vertices; further proper physical vertex-forgetting; and the legal finite source-jet insertions against a smooth positive-regulator complement, including the full complement normal derivative rule. Every coefficient pullback/product must satisfy the already specified noncharacteristic conditions. The resulting maps descend through equality of evaluated positive-scale kernels.

**Proof.** Physical derivatives commute with linear pushforward by the corresponding output linear directions. A multiplier on output variables pulls back to a multiplier on input variables. Derivatives applied before a source-jet insertion give the finite distributional Leibniz rule, transferring the required derivatives to the whole complement and its coefficients. Derivatives of an edge replace $F_e$ by its derivative and multiply by the constant derivative of its difference form. Thus all these expressions remain finite sums of(105.2).

Adding an edge introduces one independent noise coordinate, its Gaussian density, and one difference form pulled back by $q$. This is still the same formula with $m+1$ variables. Disjoint exterior composition uses independent physical and noise variables, the product stratum and product projection; the coefficient exterior-product estimates are those of its fixed normal sectors. Compact supports in disjoint physical opens exclude the cross-collision conormals in the R1 case. Further vertex-forgetting replaces $q$ by the composite linear projection, with the same compact input support. Fubini here means the well-defined Schwartz/tempered pairings of Lemma105.2 and proper distributional pushforwards; it does not multiply overlapping source counterterms.

For a jet insertion, first take its stratum inclusion and write the finite distributional product rule with the actual smooth regulated complement. Its finite terms are normal derivatives of the complement restricted to that stratum, times delta derivatives there. Each edge restriction is obtained by restricting its linear difference form. Edges internal to a collapsed block give $F_e(\epsilon z_e)$ in the auxiliary expression, with the correct scaling recovered by its actual pairing. The original R1 restrictions are noncharacteristic by their admitted partial-diagonal cone exclusion. The resulting finite terms have the same type(105.2). A disjoint spinney uses its joint partition. Overlapping sources remain alternative preparations and their counterterms are never multiplied.

The regulator power changes $k$. For $\epsilon\mapsto s\epsilon$, restrict the interval if necessary and use $a(s\epsilon,w,z)$ with the linear noise substitution that moves $s$ into the Schwartz coefficient and its density. This substitution is continuous, preserves the joint noise cone and gives the usual semilinear regulator action. No degree-only action on an omitted logarithm is inferred.

Each of these operations is an operation on actual positive-scale distributions on its stated domain. If two source sums have identical evaluated family, applying the same such operation gives the same output family. Thus the source operations preserve the kernel of actual evaluation. Taking the image of the direct sum of complete coefficient stages gives liquid maps by the same image argument as099; continuous bilinear maps are interpreted through their bounded-set/profinite estimates, not an unsupported joint topology on all distribution spaces. On a general profinite test lift through an extremally disconnected cover, use finitely many source stages there by091 compactness, and descend the equality. No arbitrary-profinite projectivity is used. $\square$

The theorem is stronger than a calculation on one host: it provides explicit finite linear data for every allowed composition and a fixed coefficient mechanism for all finite graphs. Its limitation is equally concrete. It has proved continuity on compact positive regulator intervals; it has not identified its image with a domain whose full zero-scale boundary is preserved.

## 6. Hostile controls retained by the normal form

The identity $P_0''=\delta$ proves $P_\epsilon''=\kappa_\epsilon$ in(105.4) before projection or subtraction. For the host let $D=(\partial_5-\partial_4)/2$, $t=x_5-x_4$. Distributional differentiation of(105.2) gives the whole actual identity

$$
D^2(P_\epsilon(t)G_\epsilon)
=\kappa_\epsilon(t)G_\epsilon
+2P_\epsilon'(t)DG_\epsilon
+P_\epsilon(t)D^2G_\epsilon.
\tag{105.5}
$$

Both mixed terms are retained. The nonzero even-rank finite values and normal-jet signs are those of087; no numerical dependencies of those admitted calculations have changed. Equal allocations of a regulator scalar have the same evaluated kernel and hence the same positive normal-form image. The map is not an image of formal Laurent coefficients: a spatial moment-flat profile in the admitted local096 sector remains an actual nonzero profile wherever that sector is compared; nothing in(105.2) licenses quotienting it by its moments.

The broad counterexample102 is not imported merely because it has a smooth weighted collar lift. A finite formula(105.2) uses polynomial/sign/delta base distributions with complete Schwartz noise coefficients;102's inverse-square-root tail has not been shown to belong to that class. Conversely, its exclusion cannot be declared proved just by giving a graph label to this class. A zero-scale theorem must supply a stable analytic tail/index condition for the actual image.

## 7. Heat collision maps by an exact projective comparison

This is a new geometric mechanism, not an application of an infinity theorem to an unidentified space. Let $X=\mathbb R^{n-1}$ be relative coordinates with a retained anchor vertex; the centre coordinate is a passive parameter. Let $\mathcal S_X$ be all partition subspaces, including $0$ and $X$. For a vertex-forgetting relative projection $f:X\to Y$, restriction of a partition to the retained vertices shows

$$
f^{-1}(\mathcal S_Y)\subset\mathcal S_X,
\qquad f(\mathcal S_X)=\mathcal S_Y.
\tag{105.7}
$$

Indeed a preimage imposes just the retained equalities, with forgotten vertices singleton; any target partition is realized this way. The image of a source partition imposes exactly its restricted retained equalities. A partition-diagonal inclusion also has partition-subspace preimages, though it is not a quotient.

Put $W_X=\mathbb R_s\oplus X$ and use the intersection-closed linear system

$$
\mathcal L_X=
\{\mathbb R_s\oplus V:V\in\mathcal S_X\}
\cup\{\{0\}_s\oplus V:V\in\mathcal S_X\}.
\tag{105.8}
$$

It contains $0$ and $W_X$. The map $F(s,u)=(s,fu)$ is an admissible quotient of these linear systems by(105.7). The extra subspaces with $s=0$ are necessary: they include $\ker F$ and its intersections. They must not be silently omitted from the admissibility check.

**Lemma105.4 (heat-map comparison).** On compact physical coordinate patches, the vertex-forgetting map on the full collision spaces096 lifts to a b-fibration. Partition-diagonal inclusions lift to interior b-maps. These assertions include all simultaneous partitions, not only connected collision subsets.

**Proof.** In the radial compactification of $W_X$ use $\rho=(s^2+|u|^2)^{-1/2}$ and $\omega=(s,u)/(s^2+|u|^2)^{1/2}$. On the open hemisphere $\omega_s>0$, the exact coordinates

$$
\epsilon=\rho/\omega_s=1/s,
\qquad y=\omega_u/\omega_s=u/s
\tag{105.9}
$$

identify a boundary neighborhood with the physical heat half-space. For physical $y$ in a fixed compact set, $\omega_s$ is bounded below by a positive constant. The sphere at infinity of $\mathbb R_s\oplus V$ becomes exactly $\{\epsilon=0,y\in V\}$. Every sphere at infinity of $\{0\}_s\oplus V$ lies on $\omega_s=0$ and is disjoint from this patch. Their blowups do not change its preimage. Blowing up $\partial W_X$ itself is the identity. Thus the many-body iterated blowup, restricted to this patch, is exactly the full heat collision blowup of096, with the same inclusion order and the same smooth structure.

Under(105.9), $F$ is exactly $(\epsilon,y)\mapsto(\epsilon,fy)$. [Kottke, Theorem4.1](https://arxiv.org/pdf/1712.03902) applies to the checked systems(105.8), and restricts to the asserted b-fibration. For a partition inclusion the same preimage check makes $F$ admissible; the b-map part of that theorem applies. It maps positive regulator to positive regulator, so it is an interior b-map. Taking the product with the passive centre preserves these properties. If no physical vertex survives, first project all relatives to the zero vector space, then integrate the compactly supported centre variable; this last step is an ordinary product fibration. A different retained anchor is an invertible linear coordinate change preserving the partition arrangement. This covers every forgetting map used here. $\square$

No scalar asymptotic or distribution-coefficient theorem has been inferred from geometry alone. The additional conclusion below uses a stated scalar pushforward theorem.

## 8. A closed scalar power/logarithmic sector

Use real rational power index sets $E_H\subset\mathbb Q\times\mathbb N_0$ on each boundary hypersurface. Below every fixed power there are finitely many terms; each power has finitely many logarithmic degrees; include all nonnegative integer power shifts and lower logarithmic degrees. At every stage the index family, compact physical support, finite partition and finite differential orders are fixed. Allow changes of stage, never convergence through escaping index families in the ambient positive-regulator topology.

Let $\mathcal A^E(X_n)$ be scalar polyhomogeneous functions: smooth on the positive interior with compatible expansions in $r_H^\lambda(\log r_H)^k$, smooth tangential coefficients recursively polyhomogeneous at the remaining faces, and remainders bounded in every iterated b-derivative after truncation at each order. Give it the topology of all coefficient seminorms and all these remainder seminorms, as well as interior smooth seminorms. This specifies actual functions and their uniquely determined coefficients, not arbitrary coefficient arrays. Compact support is imposed in the physical variables; the regulator interval is local as before.

**Lemma105.5 (complete scalar stages).** These fixed-index spaces are complete Hausdorff locally convex spaces. Their condensed realizations are liquid. Positive evaluation is injective and their compatible formal boundary coefficients are well-defined liquid maps.

**Proof.** Use a finite corner atlas over the compact support. Induct on face dimension. At each truncation, subtract the finite expansion using fixed smooth collar extensions of its coefficient functions. The remaining weighted bounded smooth b-derivative space is complete: Cauchy nets converge in every weighted derivative supremum seminorm, and ordinary interior derivative identities pass to the limit. Store the interior function, the lower-dimensional coefficient functions and every such remainder in their product of complete spaces. The truncation identities and overlap identities are closed linear equations, so their solution space is complete. This argument supplies precisely the topology stated above; it makes no assertion about completion in the weaker interior topology. The liquid realization follows from the same complete-space integration criterion as099. If the actual function is zero, the smallest nonzero power/logarithmic term would contradict its paired asymptotic estimate. Induction on faces and powers proves uniqueness of all coefficients. Continuous coefficient maps consequently factor through actual evaluation. $\square$

Define the scalar jet sector $\mathcal C_n$ as the evaluated image of finite sums

$$
\partial^\beta(i_\sigma)_* a_\epsilon,
\qquad a\in\mathcal A^E(X_{|\sigma|}),
\tag{105.10}
$$

where $i_\sigma$ is a physical partition inclusion, with the actual induced density and its finite normal derivatives. This representation includes the identity partition. The fixed source stages are complete; the image is in the liquid heart. The positive-scale distributions, rather than the labels $\sigma$, determine equality. Their lifted jets have finite boundary weights and tangential distribution coefficients along the lifted partition submanifolds, transverse to the boundary as checked in099. The boundary record consists of all their compatible formal power/logarithmic face coefficients, with the full Taylor units for nonincident defining functions as in corrected099. It is the image of actual functions and jets, not the whole formal product.

**Theorem105.6 (scalar Gaussian/Wick closure).** On $\mathcal C_n$, legal scalar operations of the studied Gaussian/Wick model preserve the declared class and its full boundary quotient. They include physical derivatives, compact smooth and polynomial decorations, Laurent shifts, Gaussian/Wick edge multiplication, proper forgetting of physical vertices, disjoint composition and finite legal source-jet insertion against a scalar complement smooth at positive regulator. Both legal spinneys and arbitrary fixed finite decorations are covered. Overlapping counterterms are not multiplied. The conclusion holds on the specified liquid plots and locally finite-stage smooth parameter plots. It does not assert closure with general distributional R1 coefficients.

**Proof.** Raw Gaussian/Wick factors have finite-weight smooth lifts by096, and thus belong to these index stages. A physical derivative in the resolved charts is a finite sum of b-differential operators with finite monomial boundary poles and smooth coefficients: lift it off the boundary through the blowdown, whose finite iterated polar coordinate expressions have just such denominators. Hence it shifts indices by finitely many integers. Multiplication adds index sets; pullback along an interior b-map substitutes boundary monomials and their full smooth units, producing finite index sums and logarithmic binomial expansions. The coefficients and remainder estimates give continuous maps between their corresponding fixed stages. Lemma105.4 supplies all required scalar pullbacks, including restrictions to a partition.

For physical forgetting, attach the full density $d\epsilon\,dx$ before pushing forward. Its lift under each blowdown is a smooth nonvanishing b-density times a finite monomial in boundary defining functions; each polar blowup gives its radial Jacobian and converting to a b-density gives one further radial factor. These are finite integer shifts of the index family. Divide the pushed density by the corresponding lifted $d\epsilon\,dy$ on the target afterwards. On the positive interior this is exactly physical fiber integration, with no volume normalization omitted.

The scalar b-density pushforward theorem applies: [Grieser–Talebi–Vertman, Proposition2.8](https://jep.centre-mersenne.org/item/10.5802/jep.198.pdf). Its vertical-face integrability hypothesis is automatic on these heat patches. Indeed $q^*\epsilon=\epsilon$, and every source boundary face lies over regulator zero; no source boundary hypersurface maps to the target interior. Proper physical support supplies properness; for the centre integration use its fixed compact support. The target index family is obtained by dividing source exponents by the relevant positive b-exponents and taking finite extended unions for faces mapping to the same target face. In particular equal exponents may create logarithms. Finite rational index sets remain locally finite under these operations. They are not truncated back to finite poles. The scalar pullback and pushforward statements used here are exactly for scalar polyhomogeneous functions and densities; no distribution-valued extension is hidden in this citation.

Their usual remainder estimates are uniform in the fixed-index topology: in a monomial chart, finite expansion terms integrate explicitly, and each prescribed target remainder bound requires finitely many source remainder bounds of sufficiently high order. Integration over fixed compact tangential fibers and logarithmic radial intervals has a finite seminorm bound; a logarithm is bounded by any fixed negative power when estimating a remainder. A finite atlas gives continuity. Alternatively closedness of the scalar pushforward graph in the complete metrizable fixed-index spaces gives continuity, since interior proper integration is continuous and the stated theorem identifies its output stage. Thus bounded and profinite families obey one output-stage bound.

For a jet term, factor $q i_\sigma$ into forgetting block coordinates followed by the induced target partition inclusion. The first is another map from Lemma105.4. Transfer the constant physical derivatives through the linear map; derivatives in a forgotten direction integrate to zero, while the others give a finite output differential operator. This reduces its pushforward to the scalar case and a finite target jet. Multiplication of a jet by a scalar complement gives the finite normal Leibniz formula with every complement derivative, followed by restriction of those derivatives to the partition. Its scalar coefficients remain in the just-proved pullback stages. Disjoint spinneys use the joint partition. Recursive nested insertion uses successive inclusions and the same finite chain rule, rather than the undefined product of two dependent delta constraints. Disjoint exterior composition pulls both scalar coefficients to the combined collision space and multiplies there; the finite derivatives and inclusions behave by exterior product. This proves all asserted positive-scale closure with the calculated indices.

To check descent to the boundary, first note that a lifted source sum with zero actual positive evaluation has zero tangential-distribution-valued face coefficients. Pair with an arbitrary compact tangential test on a corner chart and apply uniqueness of a finite-below power/logarithmic expansion. This includes cancellations between different jet and pole presentations. All-profinite kernel containment follows as in099: on a source coproduct section compactness gives finitely many complete stages; their concrete continuous coefficient pairings separate the formal record. A general image section lifts after an extremally disconnected cover, and actual equality descends its record. No arbitrary-profinite projectivity is assumed.

Zero full boundary coefficients mean flatness to every order at every source face, in the stated conormal remainder topology. Products and b-map pullbacks preserve this flat ideal. Under a forgetting b-fibration, each target defining function pulls back to a finite monomial. The input can therefore absorb every requested target weight and every finite density or derivative shift. The same remainder estimates used for pushforward give arbitrarily high target vanishing. For jet terms use the factorization into scalar pushforward and target inclusion just proved. Hence every stated operator sends the full normalized flat kernel to the target flat kernel. The actual-family operators and their boundary maps are well-defined on the liquid image and its boundary quotient. $\square$

This supplies a general construction, not just the successful host example. Completion occurs inside fixed asymptotic stages. It therefore does not insert the escaping-index ambient plots excluded in091, nor identify arbitrary kernels with equal formal physical moments. A spatial moment-flat Schwartz profile has its nonzero full normal function as a front-face coefficient and survives this boundary. The scalar unit remains $1$ at arity zero.

For a compact physical test, forgetting all vertices gives a scalar power/logarithmic expansion in the original regulator. Its coefficient of $\epsilon^0(\log\epsilon)^0$ defines a distributional physical finite evaluation; the finite seminorm bounds above prove continuity in the test and uniformity on bounded test families. On the local Schwartz profile subdomain the expansion has precisely the admitted coefficients096/087, so this recovers087's normalization. It changes none of its proper counterterms. Rescaling retains the whole binomial rule for $\log(s\epsilon)=\log\epsilon+\log s$, and the full smooth units in other defining functions; it is not a degree-only scaling action.

The broad control102 is now contained in an enlarged scalar source and its nonzero logarithmic output is admitted. This is an explicit change from the finite-pole target tested there. No accepted finite-pole claim is reopened, because its blanket closure had not been claimed. The present theorem does not assert that an actual finite Gaussian/Wick expression forces a logarithm, or that its finite-pole subspace is itself closed.

## 9. The exact mixed-coefficient inference still needed

Let $X_n$ be the full collision space096.8. For the integral normal forms above, the missing statement is not the existence of raw graph lifts;096 already proves those. It is the following uniform projection assertion, including every legal source stratum and the actual physical density:

> After each physical vertex projection in(105.2), the actual kernel admits a finite-index full corner expansion on $X_n$, with distributional tangential coefficients in fixed complete normal sectors; all remainders and regulator derivatives satisfy the corresponding uniform estimates on bounded coefficient sets. The allowed powers and any logarithms are specified and stable under the same operations. If every normalized source face jet vanishes, every normalized target face jet vanishes. The actual-evaluation kernel continues to annihilate the full boundary record after liquid completion.

This is a statement about a zero-scale operator domain and its boundary quotient. Lemma105.2 gives none of its estimates at $\epsilon=0$. Polynomial growth in(105.4), finite positive-scale Fubini and equal graph presentations do not prove it. A power/logarithmic enlargement would require new complete asymptotic coefficient stages and this kernel/descent check; it is not automatically the finite-pole target099.

One attempted mechanism is ordered-polyhedron elimination. For fixed edge noise, $P_0$ and its derivatives are polynomial, sign or delta data on chambers cut by

$$
w_i-w_j+\epsilon z_e=0.
\tag{105.6}
$$

Eliminating internal physical vertices produces moving polyhedra whose matrices are constant incidence matrices. Their projected walls are output differences plus $\epsilon$ times finite path sums of noise variables; cycle constraints involve only noise. There are no external-variable determinant denominators in this finite linear elimination. Near a collision, fixed closed R1 cones are uniformly transverse to sufficiently small translated partition diagonals. Large noise can plausibly be controlled by Schwartz tails, provided the projection estimates lose only finitely many regulator powers in each fixed seminorm.

The unresolved step in that mechanism is a uniform all-corner theorem for these moving-polyhedron integrals with distributional R1 coefficients and the complete joint-cone amplitudes(105.1). Chamberwise formulas alone do not prove matching on a collision corner, uniformity as noise becomes unbounded, or preservation of every normalized flat jet. Lemma105.4 now proves the geometric part by an explicit comparison; Theorem105.6 proves the scalar power/logarithmic case and the finite jet case. It does not supply the distribution-coefficient output-cone and uniform asymptotic theorem. Nor has every complete noise coefficient of(105.1) been proved to have a scalar or distributional corner expansion. The positive normal-form image and the zero-scale scalar image are therefore different typed objects, with their proved common raw-model and scalar-jet comparisons only.

A useful hostile mixed test is already explicit. In physical coordinates $(c,c+y,x)$ choose compact cutoffs equal to one near zero, with $\int g(c)dc=1$, and the R1 distribution

$$
T(c,c+y,x)=g(c)\chi(y)\chi_3(x)\delta(x-y).
\tag{105.11}
$$

Its nonzero conormal covectors in the original three slots are multiples of $(1,-1,1)$ and have nonzero total sum. Every partial-partition conormal has total sum zero. Thus it belongs to a fixed compact admissible R1 sector. Actual contraction of the first two slots with $\kappa_\epsilon(y)$ gives

$$
\int dc\,dy\,\kappa_\epsilon(y)T(c,c+y,x)
=\chi(x)\chi_3(x)\kappa_\epsilon(x).
\tag{105.12}
$$

The coordinate determinant is one. The output is a smooth strong-distribution-valued regulator curve through zero by Gaussian test Taylor estimates, but it is a boundary layer at an arity-one physical point. That target has no pair collision to blow up. A theorem for arbitrary tangential distribution coefficients must handle this curve; it cannot treat all R1 coefficients as scalar smooth functions on collision charts. This calculation alone does not establish nonmembership in099: proving failure of every possible signed collar extension would require a further one-sided wavefront argument. In particular the wavefront of one chosen extension is not such a proof. No accepted R1 theorem fails: arity-one compact distributions are allowed there, and strong distributional smoothness is exactly the relevant endpoint property.

No claim is made here that logarithms cannot occur in the actual generated class. No actual Gaussian/Wick logarithmic counterexample has been constructed either. The elementary logarithm of102 therefore remains a control against enlarging the operator domain without proof, not a negative verdict on this model.

## 10. Acceptance boundary

The claims submitted for separate criticism are the positive normal form105.1–105.3, exact geometric comparison105.4, complete scalar stages105.5 and scalar/finite-jet closure105.6. The full mixed-coefficient closure target in section9 is unresolved. Consequently M2 is incomplete, M3 and dependent M5 are suspended on that gap, and original R2, R3, R4 and both parent objectives remain incomplete. R3 receives no new cocycle or normalization mechanism from this return.

This is one primary construction attempt, with the delegated positive normal form and the parent's projective-comparison mechanism integrated before freezing. One correction pass and distinct non-author106 precede acceptance. No new finite fixture is supplied: the new obligations concern complete coefficient stages, wavefront maps, uniform asymptotics and quotient descent. Existing exact277-source and Ward fixtures remain evidence for their unchanged finite statements, not evidence for the mixed-coefficient inference in section9.
