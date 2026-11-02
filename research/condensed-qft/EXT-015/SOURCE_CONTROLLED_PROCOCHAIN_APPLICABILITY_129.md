# EXT-015 REACH / 129 — current pro-cochain applicability on the source-controlled model

**Disposition: corrected positive pro-cochain and completed-bar applicability on the explicit source-controlled model.** The direct negative filtration, strict completion and additive structural maps are proved. Review130 demonstrates that the book's generic C.5.6.1 sequence-cofibrancy criterion is incorrect, including for strictly complete split product tails. That inference is withdrawn. Actual projective-sequence cofibrancy remains unproved. Section7 instead proves the completed-bar universal property independently for the checked module-sheaf category; it does not use the failed criterion. Base cochain cofibrations, the non-equivalence cones and the exact unproved fibration test remain distinct. Extended target Weiss descent, full recovery126.14, original R3 and full M5/R4 remain open. This is the single author correction, awaiting exact-source130 readback and ledger131 reconciliation.

## 1. Frozen inputs and the actual primary text

Work in real liquid modules for fixed $0<p\le1$, ZFC and the existing physical interval model. CP107 binds this primary audit froma2e14adab7d4fe11827ff7eabc6f66736649c2a1 on `research/reach-procochain-input-frozen-20261102`. The59-source input manifest has SHA256 `5ceaa2c0c993365556e04be391a37afa8c3ca0099f5eed90132743183cf929fb`. Critical scientific inputs are:

| Input | Exact Git blob |
| --- | --- |
| Authoritative full plan090 |6b642bf10c3328bb64d37474e290810fb45cbca1 |
| R1 locally normal model069 |b3f6fe6651cc1ea59dfdf5f52990576c4f7018c2 |
| Mixed analytic domain108 |587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Enriched quantum theorem111 |b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| Unit comparison114 |ee4bfb46c5565b90d6f9015765edc8a773b0997a |
| R1 quantum comparison117 |e95b1155ebb2018a80d2dc559560730fd7ea6594 |
| Retained module-sheaf theorem123 |c5195a38414e3b45dbf75bb89b0db055ce01a5a2 |
| Corrected source-controlled realization126 |5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| Its final review127 |74c47f1329d414fdf65f85cb3fdda8712852e65f |
| Its acceptance128 |0084cc18ad122d5e5d4e30032f51bbd096d3e15e |

The primary contract is Costello–Gwilliam, *Factorization Algebras in Quantum Field Theory*, Volume I, author final draft dated8May2016, specifically Chapter3 section5 and Appendix C sections2–5. The [author's official page](https://websites.umass.edu/ogwilliam/) links the exact [full university-hosted PDF](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/8/48667/files/2025/04/vol1may8.pdf). The full324-page asset was obtained and Appendix C's body, not merely its contents or the earlier cached first181 pages, was read.

| Retained primary evidence | Identity |
| --- | --- |
| Full PDF |1,361,330bytes; SHA256 `267c00893175fd955bf2408afa7b6dcb63647f3e4d2b0ec6553255040bc3f4c4` |
| Full native extracted text |SHA256 `1a50485d2285722e79f6462c4479d7048042c7df52fa8a4e714ee96d50af1a68` |
| Author-page bytes containing that exact link |SHA256 `c5617b79d05a0b368e9a118a71a89a8ed7c0c005fd054a5654c2a6306a435a6c` |
| Literature-contract metadata |SHA256 `f59fd4c706adde0729b26cf19f3fb5751e776fafdb3680e9eac2055bdbeafc6a` |

The earlier people.math.umass.edu transport timed out; no byte identity for that uncollected asset is claimed. The independently verified author-page link supplies the present source. The earlier MPIM403 operation remained untouched. This is not an identification with the older522-page concrete draft or its B.6 numbering.

The primary129 was frozen asc8555f50db715112a7d0e55a4fa1a8ff3c64f24d, source9f7adcbb4776bd084b23fa71703d61a391cc84c1. Nonauthor130's consolidated request is sourcee0ee59ebfd8fd8b42730d963407ba657672c9e38, frozen at9072a62e63827b1c5bc20d0551a6f93ff3dee57e on persistent `research/reach-procochain-review-frozen-20261102`. CP111 binds this one correction. The demonstrated error, its counterexamples and the replacement proof below are recorded explicitly; the final statement of C.5.6.6 is not declared refuted merely because its printed proof uses an incorrect intermediate identification.

## 2. Checked definitions and the index convention

The checked contract uses module sheaves with natural flat connections(5.1.2), all-manifold quasi-isomorphisms(5.2.1), a Grothendieck abelian category(C.2.2.1), negative complete filtrations and graded weak equivalences(C.4.0.1), additive multimaps(C.4.4.1), and base injective-model cofibrations/fibrations(C.5.3.1). The bounded eventually-constant tower test is C.4.3.1. The printed sequence criterion C.5.6.1 is incorrect; sections6–7 distinguish that error from the independently repaired completed-cone conclusion.

We apply these definitions directly below. In particular we do not replace the right-lifting condition by existence of a section, or replace eventual constancy of a whole tower by constancy of each fixed tail quotient. The construction itself uses the module-sheaf convention, which admits the nonconcrete source-controlled families already exhibited in120/126.

Use $\mathrm{DVS}_{\mathrm{mod}}$ for this precise category. The book's filtration is indexed by nonpositive integers, increasing toward $F_0V=V$. For our positive tail notation $T^NV$, the dictionary is

$$
F_{-N}V=T^NV,\qquad
\mathrm{Gr}_{-N}V=F_{-N}V/F_{-N-1}V.
\tag{129.1}
$$

This fixes the indexing rather than importing the older B.6 convention.

## 3. The actual source-controlled objects, on both tests

Let $\mathbf F_n(U)$ be126's liquid-valued parameter sheaf on its explicit whole-source witness rule. Its real manifold restriction is $\mathfrak F_{\mathrm{src},n}^J$, with the natural monic comparison to the larger prior retained sheaf. Only at a manifold parameter point is its liquid coefficient value the full $\mathcal Z_n$ on every profinite test. Full real-manifold recovery of the larger sheaf is still the unproved126.14.

Fix a profinite coefficient test $S$. Define the real parameter sheaf

$$
V_n^S(U)(M)=\mathbf F_n(M;U)(S).
\tag{129.2}
$$

It is a $\mathrm{DVS}_{\mathrm{mod}}$ object. Indeed evaluation on $S$ preserves the matching limits of the manifold sheaf condition. Smooth parameter scalars act through coefficient sections constant on $S$. The liquid one-form target in126 is a finite idempotent summand; evaluating on $S$ gives the same finite idempotent on the section module. It is therefore exactly $\Omega^1(M)\otimes_{C^\infty(M)}V_n^S(U)(M)$. Naturality, the Leibniz rule and flatness are the actual126 identities after evaluation. No exactness of general profinite evaluation is used.

Give the finite graded parity/symmetry components their111 cochain degrees and put, at a fixed positive scale,

$$
V_w^S(U)=\bigoplus_{n+2k=w}\hbar^kV_n^S(U),
\qquad
V^S(U)=\prod_{w\ge0}V_w^S(U),
\qquad
T^NV^S=\prod_{w\ge N}V_w^S.
\tag{129.3}
$$

Here $n,k\ge0$. The differential $Q_s=d+\hbar\Delta_s$ preserves $w$: $d$ preserves arity, while $\Delta_s$ deletes two slots and gains one quantum power. Each weight contains finitely many arities and has cohomological degrees in $[-w,0]$. The same construction applies to the actual R1 source and the full classical physical-distribution target of126, with the latter carrying $d$ rather than an undefined quantum operator on all distributions.

Each fixed $S$ is being treated as an actual real module-sheaf object under(129.2). A homotopical theorem in that category is not automatically a theorem about a combined liquid-valued homotopy colimit, nor is a quasi-isomorphism automatically preserved by evaluation on arbitrary $S$.

## 4. Direct verification of the pro-cochain object and its maps

**Theorem129.1 (current object applicability).** For every fixed profinite $S$, the object(129.3), with $F_{-N}=T^N$, is a differentiable pro-cochain complex under the checked Definition C.4.0.1. The actual quantum structural maps have the required filtered typing. No projective-sequence cofibrancy conclusion is included.

**Proof.** Each weight is a cochain object in $\mathrm{DVS}_{\mathrm{mod}}$ by126 and(129.2). Product sections and connections are componentwise; the finite cotangent idempotent makes the one-form target compatible with those products. Thus the tail is a connection-stable cochain subobject. The inclusion $T^{N+1}V^S\to T^NV^S$ has the actual graded and cochain retraction deleting weight $N$. In every cohomological degree it is a monomorphism of module sheaves, for every manifold. These are the negative-filtration monomorphisms required by C.4; they do not establish a projective-sequence lifting property.

The finite quotient is the actual finite weight sum

$$
V^S/T^NV^S\cong\bigoplus_{w<N}V_w^S.
\tag{129.4}
$$

Projection and zero-extension give these identities as cochain and connection-compatible sheaf maps, not only on ordinary points. A compatible family in all finite quotients specifies exactly one section in every weight. Therefore

$$
V^S\xrightarrow{\ \cong\ }
\varprojlim_N V^S/T^NV^S
\tag{129.5}
$$

is an isomorphism of actual differentiable cochain complexes. It is stronger than the required completion quasi-isomorphism. No exactness of an infinite product is needed: the inverse maps assemble the prescribed coordinates.

For a legal disjoint structure map, the output of fixed total weight uses finitely many input weight choices and contraction matchings. Ordinary composition adds arities and quantum powers; a Wick contraction removes two slots and contributes one $\hbar$. Consequently output total weight is the sum of input total weights. Inputs in tails $T^{N_i}$ therefore land in $T^{\sum_iN_i}$. This is precisely the additive condition under(129.1). The source estimates and all-jet ideal preservation of126 supply actual multilinear module-sheaf maps and the connection Leibniz rule. Matching ordinary maps use117's separate cross-kernel rapid estimate, not a false claim that Wick conjugation preserves ordinary products.

The Wick cochain isomorphisms, scale transports, R1 comparison and physical classicalizing comparison preserve total weight by the same finite arity/quantum count. They are filtered cochain maps on their actual source and target objects. The fixed-scale source kernels and target subtraction-record operations retain their already proved domains. A general auxiliary projection used to DEFINE an analytic coefficient is not thereby a weight-preserving observable map: the count just proved applies to the stated structural quantum/comparison maps. $\square$

This theorem is independent of the missing surjectivity126.14. It proves applicability on the explicit source-controlled model, not transfer of these properties to every family of the larger retained sheaf.

## 5. Weak equivalences and actual comparison cones

For the strict weight splitting, $\mathrm{Gr}_{-N}V^S=V_N^S$. Thus a strict weight-preserving comparison is a filtered weak equivalence exactly when every weight map is a differentiable quasi-isomorphism, with the all-manifold test of5.2.1. A pointwise vector-space identification alone would not establish that condition.

The actual Wick cochain isomorphisms and the scale transports are isomorphisms on the source-controlled module sheaves, with inverses and finite weightwise formulas. They therefore are filtered weak equivalences on every fixed $S$. An admitted weight-preserving record-scheme isomorphism, with every operator transported as in111, has the same conclusion. This says nothing about an unspecified new local correction or a change of coefficient base.

The R1 map $J_s$ and the physical map $F_{q,s}$ are filtered morphisms but not filtered weak equivalences. It suffices to use the real coefficient singleton and the manifold parameter point. In total weight zero their actual maps are

$$
\mathbb R[0]\xrightarrow{u(*)}\mathcal Z_0(*)[0]
\xrightarrow{F_0(*)}\mathbb R[0],
\qquad F_0(*)u(*)=1.
\tag{129.6}
$$

Let $K_{\mathrm{unit}}=\ker(F_0)$ be the real-liquid kernel of114. It contains its nonzero $A/R$ subobject, witnessed at the point by $\epsilon^{-1}$. The explicit unit cone and the split retraction give the following point-complex tests:

$$
\mathrm{Cone}(u(*))\simeq K_{\mathrm{unit}}(*)[0],
\qquad
\mathrm{Cone}(F_0(*))\simeq K_{\mathrm{unit}}(*)[1].
\tag{129.7}
$$

For the second identity the cohomological point cone has $\mathcal Z_0(*)$ in degree $-1$, $\mathbb R$ in degree zero, and differential $F_0(*)$; the split unit contracts its complementary two-term summand. Both cones are nonzero. Thus the zeroth graded maps already fail the required all-manifold quasi-isomorphism test. This uses the actual point values of the accepted liquid objects, not an identification of liquid-derived and differentiable-derived categories. Nonnegative quantum powers and weight preservation prevent a higher-weight boundary from removing this factor. Even for ordinary completed cochain quasi-isomorphism, the finite binary splitting into weight zero and its tail leaves that nonzero cone factor. No infinite-product cohomology claim is involved.

The physical map also remains nonmultiplicative: opposite Laurent powers have zero separate finite values and nonzero finite value of their product. It is not a factorization morphism merely because it is a filtered cochain morphism. The monic comparison from $\mathfrak F_{\mathrm{src}}^J$ to the larger $\mathfrak F^J$ has no proved surjectivity modulo uniform rapid jets. No weak-equivalence claim about that larger-family comparison is supplied here.

## 6. Cofibrations, sections and the unproved right-lifting property

Current model-structure terminology must be kept separate from the older differentiable lifting terminology used in069. Proposition C.5.3.1 defines an injective-model cofibration by degreewise monicity and a fibration by its right lifting against all acyclic cofibrations. These are the criteria audited here; they are not an identification of enrichment categories or a reopening of R1's accepted older statements.

The tail inclusions in Theorem129.1 are current injective-model cofibrations. On the real manifold axis the accepted R1 arrow is also degreewise monic as a map of module sheaves: source plots are concrete and its point map is monic, so a zero image forces the source section to vanish. Hence it is an injective-model cofibration. It is not an acyclic cofibration, by(129.7). The accepted monic real comparison to the larger retained module sheaf is likewise a cofibration of underlying differentiable cochain complexes; this does not establish any pro-category or equivalence property for that larger target.

The finite quotient transitions have stronger certificates than abstract epimorphisms: for $E_N=\bigoplus_{w<N}V_w^S$,

$$
p_N:E_{N+1}\cong E_N\oplus V_N^S\longrightarrow E_N
\tag{129.8}
$$

have actual zero-extension chain sections for all manifold parameters. Nevertheless those sections do not prove the injective-model fibration criterion.

**Lemma129.2 (the exact fibration test for these projections).** In that model structure $p_N$ is a fibration if and only if $V_N^S\to0$ is a fibration. Similarly $V^S\to E_N$ is a fibration if and only if its tail kernel is fibrant.

**Proof.** Pulling a fibration projection back along $0\to E_N$ gives its kernel map to zero, proving necessity. Conversely the projection $E_N\oplus V_N^S\to E_N$ is the pullback of $V_N^S\to0$, proving sufficiency. The same argument applies to the split tail projection. It uses stability of the right-lifting property under pullback, directly verified by pulling back a lifting square. $\square$

No fibrancy theorem for all these weight or tail complexes is supplied. In particular no extension of every map from an acyclic monomorphism into the kernel has been constructed. Their model-fibration status is therefore unresolved, not refuted. This is not a missing hypothesis of basic C.4.0.1 object membership, which Theorem129.1 has verified independently. If a later proof chooses a fibrant-tower homotopy-limit argument, it must establish the actual lifting condition or use a justified replacement; a split section is insufficient.

For interval inclusions the existing maps are natural with projected support bounds. The proof of a cochain comparison or a filtration splitting should not be substituted for a new support-lifting theorem. In particular the stronger reverse physical-localization issue in section8 remains distinct from these parameter and weight splittings.

### 6.1. The generic sequence-cofibrancy criterion fails

Here are the two explicit controls from130, with their full lifting argument. They concern the literal projective diagram model on $I=\mathbb Z_{\le0}$, with arrows toward zero, and the permitted base category of real vector spaces. They refute the generic C.5.6.1 converse; they do not by themselves prove failure of projective cofibrancy for our particular differentiable sequence.

First let $X_n=\mathbb R[0]$, with identity arrows. Put

$$
E_n=\bigoplus_{k\ge-n}\mathbb R e_k,\qquad
\sigma_n\left(\sum a_ke_k\right)=\sum a_k,\qquad
K_n=\ker\sigma_n,\qquad n\le0.
$$

The sums are algebraic, and all transitions are tail inclusions. The augmentations
$Y_n=[K_n\hookrightarrow E_n]\to X_n$, in degrees minus one and zero, are degreewise epimorphic quasi-isomorphisms. Their kernels are disks $[K_n\xrightarrow{1}K_n]$. Such a disk is an injective object of $\mathrm{Ch}(\mathrm{Vect}_{\mathbb R})$: a map to it is specified by a linear map from the degree-zero term, and that map extends across any degreewise monomorphism. An epimorphism with this injective kernel has right lifting against every monomorphism: split off the kernel, and extend the difference of a partial lift as a map to that kernel. Thus $Y\to X$ is an objectwise trivial fibration in the stated projective sequence model.

A lift of $\mathrm{id}_X$ would choose compatible vectors $v_n\in E_n$ with $\sigma_n(v_n)=1$. Inside $E_0$ they would all be the same vector in $\bigcap_nE_n=0$, which is impossible. Hence $X$ is not projectively cofibrant although every transition is a base cofibration. There is no leftmost index from which the erroneous induction could start.

### 6.2. Strict completion and split tails do not repair the generic criterion

Let instead $G_n=\prod_{k\ge-n}\mathbb R$, embedded in $G_0=\mathbb R^{\mathbb N}$ by zero in earlier coordinates. Its transitions are split monomorphisms and its quotient-limit completion is an actual isomorphism onto $G_0$.

For $j\le0$, write $P_j(C)$ for the free diagram equal to zero before $j$ and to $C$ at and after $j$. The natural map

$$
E=\bigoplus_{j\le0}P_j(G_j)\longrightarrow G
$$

sums the tail inclusions. It is onto at every index because its summand $j=n$ is onto at index $n$. With kernel $K$, the diagram $[K\hookrightarrow E]\to G[0]$ is again an objectwise trivial fibration, by the disk argument above.

A projective-sequence lift would give a natural linear section $s:G\to E$. At index zero its component $t_j:G_0\to G_j$ vanishes on $G_{j-1}$, since the summand $P_j(G_j)$ is absent at index $j-1$. Thus every $t_j$ factors through the finite-dimensional quotient $G_0/G_{j-1}$ and has finite-dimensional image. The image of the composite $G_0\xrightarrow{s_0}E_0\to G_0$ is contained in the algebraic sum of countably many such finite-dimensional images, so has at most countable Hamel dimension. But the vectors $(1,a,a^2,\ldots)$, $a\in\mathbb R$, are linearly independent by the finite Vandermonde determinant. Consequently $G_0$ has uncountable Hamel dimension, and that composite cannot be the identity.

This second strictly complete example disproves the generic inference even with split transitions. Neither example is asserted to be a trivial-fibration witness in the differentiable category. The actual129 projective-sequence cofibrancy question remains unproved. Its base cochain cofibrations and strict C.4 object do not depend on that question.

## 7. Independent completion and completed-bar proof

The infinite quotient tower is generally not eventually constant: a new weight can appear at every step. For each fixed $r$, its further quotient modulo $T^r$ stabilizes literally once all weights below $r$ are present. These two statements are different. The eventually-constant/bounded hypotheses of C.3.0.5 and C.4.3.1 cannot be applied to the full infinite tower merely by citing this quotient stabilization. No such invocation is needed for(129.5).

The following proof replaces the failed sequence identification in the printed proof of C.5.6.6. Fix a profinite test throughout, and set $A=\mathrm{DVS}_{\mathrm{mod}}$. All constructions in this section are in this real module-sheaf category, not evaluations of a proposed liquid-valued colimit.

**Theorem129.4 (independent completed-bar applicability).** Let $\mathrm{Mono}$ be the category of sequences in $\mathrm{Ch}(A)$ whose transition maps are degreewise monomorphic, and let $\mathrm{CompleteMono}$ be its full subcategory satisfying C.4.0.1 completion by a quasi-isomorphism. Give both categories the associated-graded weak equivalences $W_F$. For any actual small strict diagram in $\mathrm{CompleteMono}$, the ordinary direct-sum bar totalization followed by strict quotient completion represents its homotopy colimit in $\mathrm{CompleteMono}[W_F^{-1}]$. This holds for the source-controlled objects above. Their projective-sequence cofibrancy and raw-tower fibrancy are not hypotheses.

**Proof, step1: exact manifold sections and products.** In the checked category kernels and cokernels are created on underlying sheaves of $C^\infty$ modules, with the induced flat connections(C.2.1.1). Let $B\to C$ be an epimorphism, and $c\in C(M)$. Locally on $M$ this section lifts to sections $b_i\in B(U_i)$. Covers by surjective local diffeomorphisms have local inverse branches, so ordinary open lifts suffice. Choose a locally finite smooth partition of unity $\chi_i$ subordinate to such a cover, with $\mathrm{supp}\chi_i\subset U_i$. The section $\chi_ib_i$ extends by zero to $M$: on $U_i\setminus\mathrm{supp}\chi_i$ it equals zero, giving the required gluing with the zero section on $M\setminus\mathrm{supp}\chi_i$. The locally finite sum of these extensions lifts $c$. No convergence or infinite summation axiom in $B$ is needed, because the sum is finite on a neighborhood of every point.

Thus $\Gamma_M:A\to\mathrm{Vect}_{\mathbb R}$ is exact for every usual smooth parameter manifold $M$. These functors jointly detect exactness. Products are computed sectionwise: the componentwise flat connection has the correct target because $\Omega^1(M)$ is a finite idempotent summand of a finite free $C^\infty(M)$ module, as proved in123/126. Finite idempotent images commute with products, so this is the product in $A$. A product of epimorphisms is onto after every $\Gamma_M$, using the choice of a preimage in each factor. It follows that products are exact in $A$, namely $A$ satisfies AB4*. Filtered colimits and coproducts are exact because $A$ is Grothendieck. This is an exactness assertion about manifold sections of $A$, never about evaluation on an arbitrary profinite test in the liquid heart.

**Step2: the correct sequence replacement.** Let $\mathrm{Seq}=\mathrm{Fun}(I,\mathrm{Ch}(A))$, $I=\mathbb Z_{\le0}$, and $W_L$ be levelwise quasi-isomorphisms. Its projective diagram model exists from the combinatorial injective base model C.5.3.1. The standard diagram-model presentation identifies $\mathrm{Seq}[W_L^{-1}]$ with
$\mathscr D=\mathrm{Fun}(I,D(A))$; this uses the levelwise projective model, not the erroneous description of its cofibrant objects. The base model, its functorial replacements, and the derived diagram presentation are the model-category infrastructure used here. The diagram presentation means derived limits/colimits below are those of actual homotopy-coherent diagrams, not limits in the bare cochain homotopy category.

Only the forward direction of the disputed criterion is needed, and it has a direct proof. A projectively cofibrant sequence is a retract of a transfinite composite of pushouts of free generating base cofibrations $P_j(B)\to P_j(C)$. Such a generating base map is degreewise monomorphic. Suppose the current sequence is monomorphic. After one such attachment, the terms at and after $j$ fit into short exact rows with old term as subobject and common quotient $C/B$. The map between two consecutive rows is the old monomorphism on their left terms and the identity on their right terms. It is therefore a monomorphism on the middle terms, by the kernel part of the snake lemma. At the crossing from $j-1$ to $j$, the new arrow is the old monomorphism followed by the monomorphic pushout inclusion. Before $j$ nothing changes. Exactness of filtered colimits preserves these monomorphisms at transfinite stages, and retracts preserve them. Starting with the zero diagram proves

$$
\text{projectively cofibrant sequence}\ \Longrightarrow\
\text{monomorphic sequence}.
$$

Let $Q\to\mathrm{id}$ be a functorial projective cofibrant replacement. It takes values in $\mathrm{Mono}$ and is a natural levelwise quasi-isomorphism. On arbitrary sequences define $W_F$ by the derived successive cofibers; on $\mathrm{Mono}$ these agree with the ordinary associated graded. Every map in $W_L$ lies in $W_F$. Naturality of $QX\to X$ and the two-out-of-three property on these derived graded maps show that $Q$ preserves $W_F$. Inclusion and $Q$ therefore induce inverse equivalences

$$
\mathrm{Mono}[W_F^{-1}]
\simeq\mathrm{Seq}[W_F^{-1}]
\simeq\mathscr D[W_F^{-1}].
$$

Their two composites are connected to the identity by the natural maps $QX\to X$, already in $W_F$. There is no assertion that an arbitrary object of $\mathrm{Mono}$ is itself projectively cofibrant.

**Step3: the derived completion localization.** The nerve of $I$ is contractible, since $0$ is terminal. Hence the constant-diagram functor $\mathrm{Const}:D(A)\to\mathscr D$ is fully faithful, and its right adjoint $R\!\varprojlim$ satisfies $R\!\varprojlim\mathrm{Const}(C)\simeq C$. The stable category $\mathscr D$ has all the limits and colimits used here. Define

$$
\mathsf L(X)=\mathrm{cofib}
\left(\mathrm{Const}\left(R\!\varprojlim_I X\right)\longrightarrow X\right).
$$

Derived limit is exact: as a right adjoint it preserves finite limits, and these equal finite colimits in a stable category. Consequently $R\!\varprojlim\mathsf L(X)=0$. For any $Y$ with $R\!\varprojlim Y=0$, adjunction gives
$\mathrm{Map}(\mathrm{Const}(C),Y)\simeq *$ for every $C$. Applying $\mathrm{Map}(-,Y)$ to the defining cofiber therefore gives $\mathrm{Map}(\mathsf L(X),Y)\simeq\mathrm{Map}(X,Y)$. Thus $\mathsf L$ is the reflector onto the full subcategory of derived-limit-zero sequences, and in particular preserves colimits.

A map $f$ lies in $W_F$ exactly when every successive cofiber of its cofiber sequence vanishes: successive cofiber is an exact functor in a stable category. This says exactly that all transitions of $\mathrm{cofib}(f)$ are equivalences. The maps to its value at the terminal index then exhibit it as a constant diagram. Conversely a constant diagram has zero successive cofibers. Finally $\mathsf L(Z)=0$ exactly when $Z$ is constant, by the defining cofiber and the fully faithful adjunction. It follows that $\mathsf L$ inverts exactly the $W_F$ maps, and its unit $X\to\mathsf L(X)$ is itself in $W_F$, since its cofiber is a shift of a constant diagram. Therefore the reflector presents precisely $\mathscr D[W_F^{-1}]$.

**Step4: ordinary quotient completion agrees with this localization.** For a monomorphic sequence $X_n\subset X_0$, put $Y_N=X_0/X_{-N}$, $N\ge0$. Its transition maps $Y_{N+1}\to Y_N$ are degreewise epimorphisms. Products of complexes compute derived products here: exact products preserve acyclic complexes and quasi-isomorphisms. More explicitly, products of fibrant injective-model complexes are fibrant because a lifting problem to the product is solved componentwise, so a product of fibrant replacements computes the derived product and is quasi-isomorphic to the ordinary one.

For this countable quotient tower the map $1-\mathrm{shift}$ on the ordinary product is degreewise epimorphic. After each exact $\Gamma_M$, its equation
$z_N-p_Nz_{N+1}=b_N$ is solved by choosing $z_0$ and recursively lifting $z_N-b_N$ through the onto transition $p_N$. Thus the usual product-fiber formula for the derived limit is represented by the kernel complex of $1-\mathrm{shift}$, namely

$$
\varprojlim_NY_N\simeq R\!\varprojlim_NY_N.
$$

Here the product-fiber formula is the countable-tower derived-limit formula in a stable category; exact products and the displayed onto map identify its homotopy fiber with the ordinary kernel complex. There is no appeal to eventual constancy or to fibrancy of this raw quotient tower.

The exact triangles $X_{-N}\to X_0\to Y_N$ give, on taking derived limit, a triangle
$R\!\varprojlim X\to X_0\to R\!\varprojlim Y$. Therefore the book's quasi-isomorphism $X_0\to\varprojlim Y_N$ holds exactly when $R\!\varprojlim X=0$.

For completeness an actual strict completion functor is available without any lifting-choice functor. Set

$$
\widehat X_0=\varprojlim_NY_N,\qquad
(\mathsf C X)_{-N}=\ker(\widehat X_0\longrightarrow Y_N).
$$

Every projection $\widehat X_0\to Y_N$ is degreewise epimorphic. Indeed after every $\Gamma_M$ a prescribed term lifts recursively upward in the tower, and its lower terms are obtained by transition maps. Hence the quotient of $\widehat X_0$ by this kernel is exactly $Y_N$. Taking successive kernels identifies the associated graded of $\mathsf C X$ with that of $X$: explicitly the relevant graded term is $\ker(Y_{N+1}\to Y_N)=X_{-N}/X_{-N-1}$. The canonical map $X\to\mathsf C X$ is therefore in $W_F$. The new sequence is strictly complete, since its quotient tower is precisely $Y_N$ and its zeroth term is their limit. These constructions are natural, using only limits and kernels.

It follows by two-out-of-three with the natural units that $\mathsf C$ preserves $W_F$. The inclusion of $\mathrm{CompleteMono}$ and $\mathsf C$ induce inverse relative equivalences

$$
\mathrm{CompleteMono}[W_F^{-1}]
\simeq\mathrm{Mono}[W_F^{-1}].
$$

This also includes the merely quasi-complete objects of C.4.0.1: their unit to strict completion is in $W_F$, and the equivalence with the derived-limit-zero subcategory follows from the preceding quotient-limit calculation. An ordinary strict adjunction to that merely quasi-complete category is not assumed.

**Step5: the completed bar has the claimed universal property.** Take an actual strict small diagram $D:\mathcal I\to\mathrm{CompleteMono}$. Form the usual simplicial bar, with each term the coproduct indexed by finite composable strings in $\mathcal I$, and its direct-sum cochain totalization $B_{\mathcal I}D$. Its filtration arrows are degreewise monomorphisms, because each is a coproduct of the input monomorphisms; coproducts in the Grothendieck category are exact. Direct-sum totalization preserves that monicity degree by degree. Thus $B_{\mathcal I}D\in\mathrm{Mono}$.

At each sequence index, the ordinary Grothendieck cochain bar theorem C.5.2.2/C.5.4.6 identifies this totalization as the derived colimit in $D(A)$. This is the base theorem proved before the disputed filtered-sequence lemma. Naturality in the sequence index gives the colimit in $\mathscr D$, since colimits of functor diagrams are computed objectwise. The reflector $\mathsf L$ preserves colimits, so its image is the colimit of the localized input diagram in $\mathscr D[W_F^{-1}]$. The strict completion $\mathsf C(B_{\mathcal I}D)$ is $W_F$ equivalent to $B_{\mathcal I}D$ and lies in $\mathrm{CompleteMono}$. By steps2–4 it represents that same colimit in $\mathrm{CompleteMono}[W_F^{-1}]$.

This proves the independent completed-bar theorem. The relevant completed direct sum is quotient completion of the filtered direct-sum totalization, not the uncompleted support colimit identified with its completion. The result is a theorem for actual fixed-test module-sheaf diagrams. It asserts no commutation of arbitrary profinite evaluation with a liquid colimit or a liquid-valued homotopy colimit. $\square$

The theorem supplies a homotopy-colimit object, not a proof that an augmentation to $V^S(U)$ is a weak equivalence. The latter still needs its actual all-manifold weightwise comparisons. Unknown model fibrancy in Lemma129.2 affects only an argument that invokes that extra right-lifting property.

**Proposition129.3 (the actual augmentation criterion).** Fix $S$ and an actual small strict weight-preserving diagram $D^S$ of these objects, with augmentation to $V^S(U)$. Write $D_w^S$ for its weight $w$ diagram. The completed cone augmentation is a filtered weak equivalence if and only if every ordinary weightwise cone augmentation is a differentiable quasi-isomorphism:

$$
\mathrm{Gr}_{-w}\widehat{\mathrm{Cone}}_{\mathcal I}(D^S)
\cong\mathrm{Cone}_{\mathcal I}(D_w^S),
\qquad
\epsilon\text{ is a filtered weak equivalence}
\ \Longleftrightarrow\
\epsilon_w\text{ is a quasi-isomorphism for every }w.
\tag{129.8a}
$$

The last condition uses every parameter manifold, as in5.2.1; it is not a point-only test. No claim that the target Weiss augmentations satisfy it is included.

**Proof.** In the uncompleted bar cone, replace each object by its finite quotient below weight $N$. Coproducts are exact in the stated Grothendieck category, and direct-sum totalization commutes with the finite weight sum. Thus the quotient cone is exactly the finite sum of the ordinary cones for $w<N$. Completing gives the product of those weightwise cones, by the same explicit coordinate assembly as(129.5). Its tail quotient and associated graded are therefore the indicated finite prefix and individual weight cone. This is an explicit splitting calculation, not general commutation of associated graded with inverse limits. The augmentation preserves these coordinates, so Definition C.4.0.1 gives the equivalence in(129.8a). The argument is internal to the differentiable category for fixed $S$ and asserts no commutation with a liquid-valued colimit. $\square$

## 8. Original M5 clauses and the remaining support/descent gate

The original090 M5 asks for actual typed integration, smooth/connection/support and lifting conditions, completed extended Weiss descent and cones or failed lifts where equivalence is not proved. The present audit separates their dispositions:

| Original clause | Current evidence and exact scope |
| --- | --- |
| Correct scalar-field variance and original R3 distinction |026's corrected scalar field-source remains separate from the original $H,G_b,G$ comparison; no degree-two consequence here |
| Units and arity zero |114's actual unit cone and(129.7) obstruct the stated real-scalar weightwise equivalences; no silent coefficient-base change |
| Typed R1/enriched/physical arrows |117/123/126 give the actual source-controlled quantum R1 arrow and classicalizing physical arrow, with their explicit triangle and limitations |
| Smooth manifold and profinite enrichment |126 supplies the combined model on its witness-controlled subrule and the full liquid coefficient object at a manifold point; full prior-family recovery126.14 is still unresolved |
| Connection compatibility |Proved on that model and its actual maps; the nonconcrete retained data remain;120's point-evaluated connection is not reinstated |
| Support naturality |Forward interval inclusion and projected compact supports are proved; reverse source-history localization is not thereby established |
| Required filtration/base-cofibration conditions |Negative filtration, strict completion, additive multimaps and base degreewise-monomorphic cofibrations are verified directly; actual projective-sequence cofibrancy remains unproved |
| Model-fibration lifting, if used |Exact right-lifting/fibrant-kernel question in Lemma129.2 remains unproved; not needed for basic current object membership or independent Theorem129.4 |
| Completed extended Weiss comparison |Not proved; independent Theorem129.4 supplies the homotopy-colimit model, not the augmentation equivalence |
| Cones and failed comparison conditions |Nonzero weight-zero cones are explicit; other weightwise cones and support/lifting questions remain to be computed |
| Full prior retained sheaf and M5/R4 verdict |No properties are transferred from the source-controlled construction to all $\mathfrak F^J$;126.14 and the other integration requirements remain open |

A precise support issue precedes any reuse of R1's partition-of-unity proof. Let $V\subset U$ and let $\chi$ have compact support in $V^n$. An actual class in $\mathcal P_n(U)$ may be presented as $q_*[a_\epsilon T]$, with forgotten auxiliary physical vertices anywhere in $U$. Multiplying its OUTPUT by $\chi$ gives $q_*[(\chi\circ q)a_\epsilon T]$. This proves output cutoff closure in $U$; it does not move those forgotten source coordinates into $V$. No accepted result shows that the resulting class has an admissible source history wholly in $V$.

For the boundary and its actual parameter families the needed condition may be weaker than exact positive-family rehosting. A sufficient local form is: for every such cutoff and source-controlled class, find a source-controlled family $v$ on $V$ such that

$$
\chi u-\mathrm{ext}_{V,U}v
\quad\text{is uniformly rapid in every mixed jet on }U,
\tag{129.9}
$$

with the fixed finite orders and actual coefficient-cover semantics. Compatible intersection relations would be needed for the resulting Čech argument. Exact positive-family rehosting would suffice but is stronger. This source-history localization modulo the actual rapid ideal has not been proved or refuted. Output support by itself is not the missing source witness.

A possible later mechanism is to split auxiliary vertices into regions near the retained outputs and regions separated from them. Separated Gaussian bridges are rapid; separated Wick kernels differ from their smooth $P_0$ restrictions by rapid terms. One would then have to absorb the remaining auxiliary pushdown into admissible regular R1 coefficients, with the correct scalar indices, all completed relations and mixed bounds. That last step and its compatibility are unproved. This audit records the new mechanism for a later bounded attempt; it does not execute a second construction cycle here or replace full normal data by physical coefficients.

Only after an actual weightwise target Čech comparison has been established can the current completed-cone machinery supply the desired completed target statement. R1's admitted proof is not inherited by this larger source class. The unresolved126.14 concerns recovery of the prior full parameter sheaf and is separately unchanged; a new attempt at that gap still needs a documented mechanism. No pro-category terminology settles either question.

## 9. Acceptance boundary and provenance

This corrected audit verifies a current differentiable pro-cochain object, its filtered structural maps and base cochain cofibrations, and independently proves completed-bar homotopy-colimit applicability on the explicit source-controlled model. The printed generic C.5.6.1 converse is refuted by two literal vector-space controls. The actual model's projective-sequence cofibrancy is not proved or disproved, and it is not required by the replacement argument. The two actual non-equivalence cones, the independent formal criterion(129.8a), and the exact unproved fibration criterion are preserved. These are typed conclusions, not a full integration verdict.

All real-liquid source, parameter and normal-profile domains remain those accepted in126. All277 proper sources, both legal spinneys, arbitrary fixed finite decorations, nonzero moment-flat profiles and087's finite normalization are unchanged. Current support/descent and lifting unknowns do not demonstrate errors in accepted R0/R1/R2 scopes, and the older R1 fibration terminology is not silently replaced by the present model-structure criterion. Original R3, full126 recovery, M5/R4 and both parents remain open.

The parent and this construction context are coauthors. The parent recovered and verified the full official author-linked source, supplied categorical/model-structure checks, the explicit weightwise cone criterion, the hostile sequence tests and the route for the independent completion repair. The construction role read the actual Appendix C body, supplied the object/map application and clause audit, and checked and wrote the corrected proof. Distinct nonauthor130 independently verified the two counterexamples and issued the consolidated adverse request; its exact-source readback of this one correction remains required. No approval of the repaired proof is inferred from informal producer notes. This is same-system scrutiny with shared scientific dependencies, not external certification. No numerical fixture, Python, Git, tracker or external mutation was used to establish these mathematical claims. The text was read from the retained full native extraction; no assertion rests only on the table of contents or earlier partial cache. Frozen primary, this single correction, final review, required checks, protected admission/readback and tracker reconciliation remain separate.
