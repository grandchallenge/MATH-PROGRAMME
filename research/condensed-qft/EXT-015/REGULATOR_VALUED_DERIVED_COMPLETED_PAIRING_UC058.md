# EXT-015 REACH / UC058 — regulator-valued derived field pairing and completed multiplication

**Candidate disposition.** On the source-controlled model there is an actual regulator-valued pairing into the internal derived liquid Hom of the corrected smooth field source. It has natural differentiable representatives on every fixed profinite test and preserves the completed disjoint Wick products through the affine-solution model. The latter model has an explicit completed relative tensor isomorphism over the common vacuum algebra for a finite disjoint union. The pairing is an equivalence at weights zero and one on a nonempty interval. At weight two its fibre is the three regulator-valued diagonal classes, so even the regulator-valued derived pairing fails to be a weightwise equivalence.

## 1. Frozen scope and types

Work in ZFC, in real liquid modules $\mathcal A=\mathrm{Liq}_p(\mathbb R)$ at a fixed $0<p\leq 1$, with tensor unit $R$. Physical opens in this comparison are finite disjoint unions of nonempty open intervals of the line, including the empty union. The weight-two fibre calculation is on a single nonempty interval. Write $M$ for a smooth parameter manifold and $S$ for a fixed profinite coefficient test. Use the actual witness-controlled sheaf of 126, with coefficient complexes $\mathbf F_n(M;U)$ and vacuum algebra $\mathbf C(M)=\mathbf F_0(M;U)$ from 135.6. Quantum weight is $w=n+2k$ with $k\geq0$. Use a fixed positive Wick scale $s$ and the matching Wick compositions $\mu_{Q,s}$ of 111.10 and 126. The real differentiable category for each fixed $S$ is the module-sheaf category of 129; its filtered multimaps use C.4.4.1 and the relative scalar convention of C.4.5. The [author's full Volume I draft](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/8/48667/files/2025/04/vol1may8.pdf) has frozen SHA256 267c00893175fd955bf2408afa7b6dcb63647f3e4d2b0ec6553255040bc3f4c4.

CP278 binds protected input 4a6e513b6fa4d87c87c28c985c2149cd5cea32a3 on the retained ref research/reach-derived-completed-pairing-uc058-input-20261123. The principal inputs at that cut are as follows.

| Source | Exact blob |
| --- | --- |
| [Original work package D](WORK_PACKAGES.md) | `2b8c1403fede354ee1771f154fe6ba531cf5d497` |
| [Smooth field source 026](VARIANCE_OBSTRUCTION_SCALAR_DUAL_BRIDGE_026.md) | `45681b9e459ac27b45d800847888bc3f7166baf2` |
| [Actual pairing bounds 108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | `587c15fd6e24f6e6b14de574ff878221cdbd5cb6` |
| [Wick structure 111](RENORMALIZED_QUANTUM_STRUCTURE_111.md) | `b7b1e5f970904d6e7de065a4fedd382e212a3022` |
| [Whole coefficient rows 126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | `5b05c6147d237ca1d22e4dcbce9262b0f038c163` |
| [Differentiable pro-cochains 129](SOURCE_CONTROLLED_PROCOCHAIN_APPLICABILITY_129.md) | `9b3f38f476646bf6ee395701d8b033cc8d3c265c` |
| [Scalar and empty-open model 135](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md) | `62d91e9d5f38fc85cf2793507d887d526eccce7a` |
| [Contract audit 138](REACH_M5_REMAINING_CONTRACT_AUDIT_138.md) | `de621fb8f1ddd384c2ed0fce5f542068517e69cd` |
| [Weight one 141](SCALAR_RELATIVE_WEIGHT_ONE_COMPARISON_141.md) | `de6b608c8def91dd0b8b2d98fe410348ac92a17d` |
| [Diagonal projection 147](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md) | `89b3d4a835f3750114e983854585e33d8184cb1f` |
| [Two-slot split comparison 150](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | `03deca9212a9bea56743e482e5cb79edb46b9d7f` |
| [Residual contraction UC047](RESIDUAL_WEIGHT_TWO_CONTRACTION_UC047.md) | `c582d45523a63288b339204574f33ac17820e327` |
| [R3 dependency boundary UC037](R3_INTEGRATION_DEPENDENCY_AUDIT_UC037.md) | `99ff425d8e1e046bce1c6da66112ed22f21b38ce` |
| [Prior-family obstruction UC055](TWO_SLOT_UNIFORM_SOURCE_BOUNDS_UC055.md) | `8f546b89507123d5a4f7f7590046aba76b8e9877` |

Let $L(U)=\{f\in C^\infty(U):f''=0\}$, canonically affine on each component. Write $L(\varnothing)=0$. Use the cochain field source $\mathcal S_n(U)$ of 26.15, including $\mathcal S_0=R[0]$, formed from the real smooth two-term field complex with differential $\partial_x^2$. Put $P_n(U)=\mathrm{Sym}^n_R\underline{L(U)}$ in degree zero. Finite-dimensional symmetric powers here agree with classical ones. Denote the dual by $P_n(U)^\vee$.

## 2. Actual pairing into a natural model of internal derived Hom

The inclusion $P_n(U)\to\mathcal S_n(U)$ comes from actual solutions in degree zero and is natural under restriction of fields. On each component use the continuous contraction 26.12–13. Take the finite product over components and extend the maps and their homotopies to the finite classical completed tensor powers used to define $\mathcal S_n$. Averaging over the graded symmetry gives the homotopy equivalence with $P_n$. For the empty open the positive arity complexes vanish. This proof gives objectwise homotopies; it needs no natural choices of base points. The inclusion itself is natural.

For any liquid $D$ in degree zero, precomposition gives the natural internal cochain Hom comparison

$$
\underline{\mathrm{Hom}}^\bullet_{\mathcal A}(\mathcal S_n(U),D)
 \longrightarrow
 P_n(U)^\vee\otimes_R D[0].
\tag{UC058.1}
$$

This is a cochain homotopy equivalence, since internal cochain Hom carries the supplied finite chain homotopies contravariantly. The right side represents $\mathrm{R}\underline{\mathrm{Hom}}_{\mathcal A}(\mathcal S_n(U),D)$: $\mathcal S_n\simeq P_n[0]$ in the liquid derived category and $P_n$ is finite free over the unit and hence dualizable there. Hom out of it is a finite direct sum of the identity. This uses the internal derived tensor–Hom adjunction, not an assertion that external projectivity implies exactness of arbitrary internal Homs. [Clausen–Scholze, Lectures III and VIII](https://arxiv.org/pdf/2605.11731)

There is a canonical comparison from the actual **classicalized** coefficient complex to the left side of (UC058.1) at $D=\mathbf C(M)$. A degree component of the pairing with the corresponding smooth field tensor is

$$
(u,f)\longmapsto[\epsilon\longmapsto \langle u_\epsilon,f\rangle].
\tag{UC058.2}
$$

For cochain signs take the graded dual of the field tensor with the same Koszul convention as 026 §3 and 111. In one slot the transposed differential from degree $-1$ is $+\partial_x^2$. All arities use the finite graded tensors and the finite symmetrizer. Compact physical support makes pairing with unrestricted smooth $f$ meaningful.

Here is the simultaneous test bound needed for liquid currying. For a fixed history and scalar stage, use one compact physical cutoff in the support of the history to test $f$. Pull the test through the proper projection, normal derivatives and partition inclusion, retaining the physical densities. The proof of 108.2 then gives scalar half-line stages for these pairings just as in 135.2. Their index families and fixed auxiliary weights depend on the source scalar stages, geometry and finite derivatives. They are independent of $f$ and of the graph Sobolev orders in the compatible parameter rows. In particular the pullback test has smooth normal Taylor expansions and introduces only the nonnegative integer shifts already allowed. For each scalar coefficient or remainder seminorm the bound is a product of a finite source seminorm and a finite smooth-function seminorm on a fixed physical compact set. Indeed all transferred derivatives of $f$ on that set are bounded by finitely many derivatives in the original field coordinates; tangential distribution pairings and the radial pushforward estimate of 108.2 then give the asserted bound. On simple mixed tensors the source estimate factors through the corresponding projective seminorm, so it extends to the completed coefficient tensor. This verifies jointly continuous bilinear pairing at the whole-history stage, not only a list of separate scalar moments.

Apply the same pairing to all genuine coefficient rows; for a field tensor with no manifold dependence, its derivatives in the manifold parameter fall only on the row. Row compatibility follows from equality of the entire positive-scale evaluations. An actual uniform rapid jet of fixed finite Sobolev order pairs with a fixed finite test seminorm, independently of the requested decay power. A continuous profinite plot of smooth test functions has those seminorms bounded on the compact profinite test. Thus the same argument with cover-local whole-source witnesses proves compatibility with the actual equalities and rapid intersections on all profinite tests. Continuous bilinear maps on the fixed stages give liquid tensor maps, hence internal Hom maps by adjunction. These descend through the actual source quotients. The resulting target is a parameter sheaf because internal Hom out of a fixed object preserves the matching limits of the scalar sheaf. This extends the construction to the specified sheafification. It gives an actual liquid morphism before applying any fixed-test evaluation.

Integration by parts at positive regulator gives the cochain identity in (UC058.2). It descends by the just-proved equality rule. Pairing commutes with extension by zero in the observable and restriction in the test. Pullback on $M$ and differentiation of coefficient rows give the connection identity. More precisely the internal Hom target acts by $C^\infty(M)$ through the scalar output. The cotangent idempotent of 126 commutes with this Hom, since it uses only finite powers and a splitting, giving the prescribed one-form target before and after evaluation on $S$. This verifies a smooth multilinear compatible construction on the actual module-sheaf objects. No derived exactness of evaluation on arbitrary $S$ is needed: the chain homotopy equivalence (UC058.1) already holds on the representatives and is natural up to the unchosen inverse.

Compose (UC058.2) with $W_s^{-1}$ and (UC058.1), and take the stated finite sum in each total weight followed by the product. This gives the current differentiable pro-cochain morphism at every fixed $S$ represented by

$$
\Theta_s(M;U)\colon
 \prod_{w\geq0}\bigoplus_{n+2k=w}\hbar^k\mathbf F_n(M;U)
 \ \longrightarrow\
 \prod_{w\geq0}\bigoplus_{n+2k=w}
       \hbar^k\big(P_n(U)^\vee\otimes_R\mathbf C(M)\big)[0].
\tag{UC058.3}
$$

The source differential is $Q_s$; the displayed arity components on the left use the actual quantum differential across that weight. The right side has zero differential and models the named weightwise internal-derived Homs. The strict weight completion is literal: finite weight cutoffs give split projections and the inverse limit assembles their coordinates. On the derived side the product is also represented by the termwise product at each $M$. Indeed countable products in the liquid heart are computed in condensed real modules and are exact there on the extremally disconnected generators; exactness on those generators detects exactness. Thus no arbitrary exchange of tensor products with an infinite product is used. For the current differentiable finite-weight representatives the same identifications are made directly on their section sheaves. On the older concrete parameter convention the source-controlled construction has the evaluation failure of 120 and 126; the present assertion concerns the checked module-sheaf convention.

## 3. Matching disjoint products and the completed relative tensor

For a field solution $\phi\in L(U)$, a degree-zero symmetric observable of arity $n$ in (UC058.2) yields the homogeneous polynomial $\phi\mapsto \langle u_\epsilon,\phi^{\otimes n}\rangle$. Equalities of these polynomials determine the symmetric functional by polarization over the reals. Normalize the symmetric dual using this evaluation, which gives the usual polynomial multiplication with the averaged symmetrizer. The target disjoint map restricts the field solution to each input open and multiplies the resulting polynomials and vacuum scalars. On degree-zero classicalized observable inputs the pairing identity follows by testing the exterior product on the corresponding pure tensor and multiplying its actual positive-regulator scalar pairings. Symmetric averaging leaves that pure tensor fixed. Both sides vanish when the total cochain degree is negative because the target is in degree zero and the classicalized observable inputs have only nonpositive degrees. The sign rules are therefore the same as the graded cochain pairings. The identity for arbitrary elements follows from actual tensor exterior pairing, whole-stage continuity, and the same rapid and quotient descent as in section 2. Since $W_s^{-1}\mu_{Q,s}=\mu_{\mathrm{cl}}(W_s^{-1},\ldots,W_s^{-1})$, the identity proves compatibility with the matching quantum maps. The identical argument with the empty family of fields is the regulator scalar unit, including the vacuum on the empty physical open.

Here is the relative tensor whose comparison can be made exact. At $M$ put $B=\mathbf C(M)[\hbar]$ with weight $2$ on $\hbar$ and cochain degree zero. The finite-polynomial representative of the right side of (UC058.3) is the graded module over $B$

$$
D_{\mathrm{pol}}(U)=B\otimes_R\mathrm{Sym}_R(\underline{L(U)}^\vee).
\tag{UC058.4}
$$

The symmetric factor is graded by ordinary polynomial degree. Each homogeneous arity is a finite free module over $R$, so (UC058.4) is a graded direct sum of shifts of free modules over $B$. Consequently its relative derived tensor is the ordinary graded tensor, without a flatness premise about general mixed history spaces or the scalar ring as a liquid module over $R$. Complete this tensor in total weight by taking the product of its weight components, equivalently by the inverse limit of its finite weight truncations. The definition uses the graded polynomial models and puts a common $\hbar$ in both factors. It neither tensors two independent vacuum formal parameters nor postulates that an uncompleted tensor commutes with a product.

For finitely many disjoint physical opens $U_i$ of the stated finite-component type having union $U$, restriction identifies $L(U)$ with $\bigoplus_i L(U_i)$. Multiplying the polynomials pulled back from each $L(U_i)$ gives the natural graded symmetric-algebra isomorphism. Thus one has the actual comparison

$$
\widehat{\bigotimes}^{\,L}_{B,i}D_{\mathrm{pol}}(U_i)
 \ \xrightarrow{\sim}
 \prod_{w\geq0} D_{\mathrm{pol}}(U)_w[0]
\tag{UC058.5}
$$

with the completed tensor on the left defined by the preceding finite truncations. If the union sits inside a larger open, compose this isomorphism with the support-natural map from that union. The isomorphism respects unit, associativity, symmetry and all common vacuum powers. The empty union gives the completion of $B$. If two intervals are included in a connected larger interval, their independently affine solutions restrict from one common affine solution only along the actual restriction map; (UC058.5) is an isomorphism for the disjoint union, and the subsequent support map is exactly the pullback along that field restriction.

Evaluating (UC058.5) on $S$ is compatible with the analogous construction from the free modules over $\mathbf C(M)(S)[\hbar]$. To check this, compute at each fixed weight with the finite free coordinates of (UC058.4), then take the product. Evaluation preserves the needed limits and finite direct sums. The evaluated tensor comparison is thus computed directly by finite free modules and their coordinatewise completions. Its smoothness is the differentiability of the scalar multiplication on the actual $\mathbf C(-)(S)$ and the connection Leibniz rule. The compatibility proved for (UC058.3) applies to the completed disjoint products: each output weight is a finite sum with sum of input weights equal to that weight, even before passing to the limit. This gives a morphism respecting the C.4.4.1 structure and an exact completed relative tensor comparison on the actual derived-Hom representative. It does not identify the stronger graded tensor of the full mixed history quotients with that of the affine-solution model.

An absolute real tensor gives a different comparison even at the vacuum. For a two-point profinite $S$ and the manifold point, the canonical section-level multiplication takes $\mathbf C(*)(S)=\mathcal C(*)^2$ coordinatewise. The real tensor of the two nonzero complementary coordinate idempotents maps to zero. That pure real tensor is nonzero, as seen by projecting each factor to the specified coordinate and applying the scalar constant-coefficient retraction there. Balancing over the actual scalar algebra kills the crossed tensor in the domain. This test explains why (UC058.5) uses the stated relative base and why no strong statement about arbitrary evaluation of **real** tensor products is implicit.

## 4. Exact low-weight fibre on a nonempty interval

At weight zero $\Theta_s$ is the identity on the vacuum. At weight one $W_s=1$ and (UC058.3) is the two affine moments of 141, with the actual compact primitive giving the homotopy equivalence. These assertions hold in the liquid coefficient complex at the parameter point and separately on every source-controlled fixed-test parameter complex.

At weight two the target on an interval is the three symmetric affine functionals and the scalar $\hbar$ vacuum. After Wick classicalization the degree-zero section of $\Theta_s$ is given by the moment-dual compact bumps of 141 in the two slots, their graded symmetric combinations with the normalization of 150.8, and the identity on the vacuum. It is a cochain section since the target is in degree zero. In the liquid complex at the parameter point this section represents the scalar-extended R1 arrow $\alpha_{2,s}$: the finite moment model of the R1 side gives the three constant bump generators, and ordinary multiplication by the actual regulator scalar gives their images as in 150 and UC047. The same finite-generator statement is a section-level fact on the source-controlled parameter complexes. Its compatibility with (UC058.3) follows by taking the actual affine pairings on those bumps. There is no assertion of evaluation commuting with an arbitrary derived scalar extension.

For any split cochain map $\theta$ with section $b$, the fibre of $\theta$ is represented by $\ker\theta$, and the cone of $b$ is homotopy equivalent to that kernel. This follows by the actual splitting into the section and the kernel and contracting the identity cone. Apply UC047 to the section just identified. Thus at weight two, for the liquid coefficient point complex,

$$
\mathrm{Fib}(\Theta_{s,2})\simeq\mathcal C^{\oplus3}[0],
\qquad
\mathrm{Cone}(\Theta_{s,2})\simeq\mathcal C^{\oplus3}[1].
\tag{UC058.6}
$$

For each fixed $S$ the corresponding fibre on the actual differentiable module sheaf is $\mathbf C(-)(S)^{\oplus3}[0]$ by the same split calculation using UC047's parameter contraction. It suffices to test the singleton and parameter point to see that the arrow fails to be a filtered weak equivalence. A diagonal cycle can have nonzero ordinary affine moments. The corresponding cycle in the fibre is obtained by subtracting its moment-dual bump image, so the exact fibre does not require all raw diagonal cycles to be annihilated literally by moment evaluation. Its diagonal extraction remains the indicated one because the bumps are in the kernel of that extraction. On both complexes this argument shows why changing the variance or forgetting the actual diagonal projection would misidentify the comparison. Bump choices used in the contractions can depend on the interval; support naturality of $\Theta_s$ itself was proved in section 2.

## 5. Adjudication and remaining comparison

The theorem supplies the actual derived-Hom morphism with smooth parameter tests, its product compatibility over the specified scalar algebra, a computed completed relative tensor on its target, and a nonzero actual fibre at weight two. These statements use the full regulator-valued pairing, whereas the scalar finite readout in 114 has a different multiplicative boundary. Universal identification of the completed tensor of actual mixed history quotients with a geometric disjoint-union sector requires its own argument. Higher-weight fibres of this derived pairing also remain open.

The source contains exactly the witnesses of 126 used for its fixed-test Weiss theorem; UC055 prevents extending this by identifying the witness-controlled sheaf with the larger prior sheaf. The field-source pair in (UC058.1) is distinct from the original $H,G_b,G$ support comparison of 067 and UC024. No map transporting a class in that degree-two support cokernel enters the construction. Consequently the foundation-dependent original R3 verdict retains the dependency boundary of UC037. This is a bounded integration result with proof and hostile controls. Exact-source review and protected admission are separate.
