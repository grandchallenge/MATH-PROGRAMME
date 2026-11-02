# EXT-015 REACH / 129 — current pro-cochain applicability on the source-controlled model

**Disposition: positive object and morphism applicability audit, with explicit lifting and descent limits.** The constructed source-controlled model satisfies the actual author-volume definition of a differentiable pro-cochain complex. Its total-weight filtration has degreewise monomorphic inclusions and is strictly complete; the structural multilinear maps satisfy the required additive filtration rule. The R1 and physical comparison maps are filtered morphisms but not filtered weak equivalences. Split truncation projections are not automatically fibrations in the book's injective model structure; their right-lifting status remains unproved. Extended target Weiss descent, full recovery126.14, original R3 and full M5/R4 remain open. Review130 and ledger131 are separate.

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

## 2. Checked definitions and the index convention

The following is the compact contract extracted from that edition. Definition5.1.2 uses module sheaves with natural flat connections;5.2.1 tests cochain quasi-isomorphisms on every manifold, equivalently on stalks. Appendix C Theorem2.2.1 makes that category Grothendieck abelian. Definition4.0.1 uses a negative filtration, completion by the quotient limit, and associated-graded quasi-isomorphisms for filtered weak equivalences. Definition4.4.1 requires additive filtration preservation for multilinear maps. Proposition5.3.1 has degreewise monomorphisms as injective-model cofibrations and a right-lifting condition as fibrations. Lemma5.6.1 characterizes cofibrant sequences by their successive monomorphisms. Theorem5.6.6 identifies the completed cone with a homotopy colimit. The tower comparison4.3.1 additionally requires bounded, eventually constant towers of epimorphisms. These are distinct tests.

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

**Theorem129.1 (current object applicability).** For every fixed profinite $S$, the object(129.3), with $F_{-N}=T^N$, is a differentiable pro-cochain complex under the checked Definition C.4.0.1. Its filtration sequence is cofibrant under Lemma C.5.6.1. The actual quantum structural maps have the required filtered typing.

**Proof.** Each weight is a cochain object in $\mathrm{DVS}_{\mathrm{mod}}$ by126 and(129.2). Product sections and connections are componentwise; the finite cotangent idempotent makes the one-form target compatible with those products. Thus the tail is a connection-stable cochain subobject. The inclusion $T^{N+1}V^S\to T^NV^S$ has the actual graded and cochain retraction deleting weight $N$. In every cohomological degree it is a monomorphism of module sheaves, for every manifold. Hence the negative filtration has the required monomorphisms and is a cofibrant sequence under the checked criterion.

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

## 7. Completion, homotopy colimits and the theorem that is actually available

The infinite quotient tower is generally not eventually constant: a new weight can appear at every step. For each fixed $r$, its further quotient modulo $T^r$ stabilizes literally once all weights below $r$ are present. These two statements are different. The eventually-constant/bounded hypotheses of C.3.0.5 and C.4.3.1 cannot be applied to the full infinite tower merely by citing this quotient stabilization. No such invocation is needed for(129.5).

The same verified edition supplies a more appropriate construction for future gluing diagrams. Its category $\mathrm{DVS}_{\mathrm{mod}}$ is Grothendieck abelian, and our actual filtrations have the degreewise monomorphisms required for cofibrant sequences. For any small diagram of these checked complete filtered objects and filtered maps, C.5.6.5–5.6.6 supplies the completed bar/cone construction as a model for its homotopy colimit in the localization at filtered weak equivalences. Its direct sums are the completed direct sums of C.4.1.1, not an uncompleted support colimit silently identified with completion. This application is valid for each fixed profinite coefficient test as a diagram of actual differentiable cochain complexes.

This result constructs a homotopy-colimit object; it does not prove that a particular augmentation to $V^S(U)$ is a filtered weak equivalence. A Weiss theorem still needs its actual diagram and its weightwise augmentation comparison. Nor is a general commutation of a liquid-valued homotopy colimit with evaluation on arbitrary $S$ asserted. The explicit split weights and their compatible coefficient tests do not imply such a general exactness theorem.

Thus current homotopy-colimit applicability is positive, while extended target Weiss descent remains a separate mathematical question. Unknown injective-model fibrancy of the split quotient tower does not negate the object or completed-cone theorem; it blocks only an argument that actually requires that fibrancy.

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
| Required filtration/cofibration conditions |Current negative filtration, strict completion, additive multimaps and degreewise monomorphic tails are verified directly |
| Model-fibration lifting, if used |Exact right-lifting/fibrant-kernel question in Lemma129.2 remains unproved; not needed for basic current object membership or the cited completed-cone construction |
| Completed extended Weiss comparison |Not proved; the current category supplies the homotopy-colimit model, not the augmentation equivalence |
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

This audit verifies a current differentiable pro-cochain object, its filtered structural maps, its cofibrant filtration sequence and the applicability of the current completed-cone homotopy-colimit construction on the explicit source-controlled model. It also identifies actual non-equivalences of the two comparison maps and the exact unproved fibration criterion. These are positive and negative typed conclusions, not a full integration verdict.

All real-liquid source, parameter and normal-profile domains remain those accepted in126. All277 proper sources, both legal spinneys, arbitrary fixed finite decorations, nonzero moment-flat profiles and087's finite normalization are unchanged. Current support/descent and lifting unknowns do not demonstrate errors in accepted R0/R1/R2 scopes, and the older R1 fibration terminology is not silently replaced by the present model-structure criterion. Original R3, full126 recovery, M5/R4 and both parents remain open.

The parent and this construction context are coauthors. The parent recovered and verified the full official author-linked source, supplied categorical/model-structure checks and the explicit weightwise cone criterion, and tested the support-localization boundary; the construction role read the actual Appendix C body and supplied the object and map application proofs and clause audit. Distinct nonauthor130 must inspect the frozen primary before acceptance. This is same-system scrutiny with shared scientific dependencies, not external certification. No numerical fixture, Python, Git, tracker or external mutation was used to establish these mathematical claims. The text was read from the retained full native extraction; no assertion rests only on the table of contents or earlier partial cache. Source freeze, one correction, required checks, protected admission/readback and tracker reconciliation remain separate.
