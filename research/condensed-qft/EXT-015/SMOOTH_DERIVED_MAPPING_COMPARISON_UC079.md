# EXT-015 REACH / UC079 — smooth derived realization and the fate of the original degree-two classes

**Candidate result.** The original support-valued liquid mapping complexes admit an exact smooth realization in the current differentiable module-sheaf category. There is an explicit support-natural derived comparison from their completed weight diagram to the actual source-controlled Gaussian/Wick observables. It kills the original degree-two classes upon passage to observables. The original support diagram and the observable diagram cannot be weightwise equivalent over ZFC, already at the vacuum. Under CH there is an additional weight-one obstruction even after replacing the vacuum by the correct unit. The two conditional verdicts concern the original support comparison; neither changes support comparison for the actual observable diagram.

## 1. Objects and category

Fix the original real liquid category $\mathcal A=\mathrm{Liq}_p(\mathbb R)$, with $0<p\leq1$, the original site convention, tensor unit $R$, and $H,G_b,G$ of 067. In particular $G_b$ is the liquid realization of smooth functions supported in $[-b,b]$ for integers $b\geq1$, and $G=\varinjlim_bG_b$. Use the nuclear Fréchet realizations $E_w$ of 022, so $E_0=R$ and $E_1=H$. Use the current Costello–Gwilliam differentiable category $\mathsf D$ of sheaves of smooth modules with natural flat connections, as checked in 129. The coefficient test for the observable category is the profinite singleton, written $*$; the parameter manifold point is written $\mathrm{pt}$. Use the published comparison machinery only in the named category. CP292 binds protected input 44505f800088e6c81afe47a81d8af74628f0f610 on retained ref research/reach-derived-mapping-uc079-input-20261124.

| Frozen source | Exact Git blob |
| --- | --- |
| [Liquid profile and exact categorical inputs](LIQUID_PROFILE_RECORD_BRIDGE_091.md) | c517fe1ae46bcaa9f4a3fc0e64381ae8096bfe27 |
| [Original liquid weight models](POLYNOMIAL_WEIGHT_COMPLETED_BRIDGE_022.md) | 029ec3a15739513a5b1e3a3daa8f72e09a6ff482 |
| [Corrected field-source variance and scalar unit](VARIANCE_OBSTRUCTION_SCALAR_DUAL_BRIDGE_026.md) | 45681b9e459ac27b45d800847888bc3f7166baf2 |
| [Older B.6 model](R1_LOCALLY_NORMAL_COMPLETED_WEISS_069.md) | b3f6fe6651cc1ea59dfdf5f52990576c4f7018c2 |
| [Actual projective presentation](R3_EVALUATED_RELATION_COVER_067.md) | 7069938ce1e75f946e2f4ff70fcabb2f073065e9 |
| [Quantum Wick structure](RENORMALIZED_QUANTUM_STRUCTURE_111.md) | b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| [Real-scalar obstruction](QUANTUM_UNIT_COMPARISON_114.md) | ee4bfb46c5565b90d6f9015765edc8a773b0997a |
| [Combined parameter rows](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [Current differentiable completion](SOURCE_CONTROLLED_PROCOCHAIN_APPLICABILITY_129.md) | 9b3f38f476646bf6ee395701d8b033cc8d3c265c |
| [Exact rehosting and unit](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md) | 62d91e9d5f38fc85cf2793507d887d526eccce7a |
| [Original M5 comparison audit](REACH_M5_REMAINING_CONTRACT_AUDIT_138.md) | de621fb8f1ddd384c2ed0fce5f542068517e69cd |
| [R3 conditional acceptance](R3_GLOBAL_SUPPORT_ACCEPTANCE_UC024.md) | 0f3b36f362d2636fed10c2a5492f546eb0d1f29b |
| [R3 transfer criterion](R3_INTEGRATION_DEPENDENCY_AUDIT_UC037.md) | 99ff425d8e1e046bce1c6da66112ed22f21b38ce |
| [Current raw lifting obstructions](ACTUAL_WEIGHT_LIFTS_ACCEPTANCE_UC054.md) | 2d1e7303250cad889e14401bbb646b4998052f71 |
| [Corrected regulator-valued field target](REGULATOR_VALUED_DERIVED_COMPLETED_PAIRING_UC058.md) | f46fbf85c635a8d90b8c357032fdd8c14120caaa |
| [All-open relative tensor](ARBITRARY_SEPARATED_OPENS_INTEGRATION_UC076.md) | 1a876fb9009adcb881fcd0eca9ea672d38ee0a82 |

## 2. Exact realization with smooth parameter families

For a usual second-countable smooth manifold $M$, write $A_M=\underline{C^\infty(M)}$. Define the exact functor $J:\mathcal A\to\mathsf D$ by sheafifying the presheaf

$$
J_{\mathrm{pre}}(X)(M)=(A_M\otimes_R X)(*) .
\tag{UC079.1}
$$

The pullback for smooth maps is the actual pullback on the first tensor factor. Smooth functions act by multiplication on that factor, and the connection is induced by the ordinary exterior derivative from $C^\infty(M)$ to smooth one-forms. On a coordinate chart it acts by the partial derivatives on $A_M$, tensored with the identity on $X$. On an arbitrary manifold the one-form module is a finite idempotent summand of a free smooth module as used in 126 and 129. The liquid realization of the idempotent identifies the one-form target after tensor and evaluation with that same idempotent applied to $J_{\mathrm{pre}}(X)(M)$. The Leibniz rule, coordinate change and flatness follow from the continuous identities on the first tensor factor. They are given by linear identities at the level of the liquid tensor, and hence hold on all its sections. Chartwise sheafification gives the connection on $J(X)$ and respects arbitrary smooth pullbacks by their chain rule.

Each $A_M$ is nuclear Fréchet and therefore flat in the liquid tensor. The original profinite singleton is an extremally disconnected projective test; its liquid section functor is exact and preserves small colimits. These statements use the admitted site bound and 091. Thus (UC079.1) is exact at each manifold and commutes with small colimits there. Sheafification is exact for modules and preserves colimits. Kernels, cokernels and colimits in $\mathsf D$ are computed on the underlying module sheaves with the induced connections, as in 129. Therefore $J$ is exact and preserves small colimits. At the parameter point every cover splits, so sheafification leaves (UC079.1) unchanged there. We have canonical identities

$$
J(R)=\mathscr O,\qquad
J(X)(\mathrm{pt})=X(*),\qquad
J(G)=\varinjlim_b J(G_b),
\tag{UC079.2}
$$

where $\mathscr O$ is the smooth-function sheaf with ordinary derivative. The last equality is a sheaf colimit. One must allow different compact support stages locally on a noncompact parameter manifold. [Clausen–Scholze, Theorem 3.11 and Remark 4.12](https://arxiv.org/pdf/2605.11731) [Costello–Gwilliam, author Volume I, 5.1.2 and C.2](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/8/48667/files/2025/04/vol1may8.pdf)

For $K=[-b,b]$, the liquid kernel of the restriction $C^\infty(\mathbb R)\to C^\infty(\mathbb R\setminus K)$ is exactly $G_b$ by its actual plots. Flatness of $A_M$ and the nuclear Fréchet tensor calculation applied to these smooth-function spaces identify $(A_M\otimes_R G_b)(*)$ with the jointly smooth functions on $M\times\mathbb R$ that vanish outside $M\times K$. The nuclear calculation here is the usual completed smooth-function product tensor. The kernel identification is purely left exact and needs no claim that restriction onto the complement is surjective. These are already sheaves on $M$. Their connection differentiates the jointly smooth function in its parameter. For example a nonzero compact bump $\eta$ in $K$ gives the family $\eta(x)\exp(tx)$ over $M=\mathbb R$. Its derivatives at $t=0$ have infinite-dimensional span, so (UC079.1) uses genuine smooth families beyond algebraic finite-rank tensors of sections.

The exact functor $J$ applies termwise to complexes and induces a derived functor. It also induces natural maps of external derived Hom. For example, if $P^\bullet\to H[0]$ is the original projective resolution in nonpositive degrees, apply $J$ and use an injective resolution $I^\bullet$ of $J(X)$. On the Hom complexes the map is $f\mapsto a\circ J(f)$, where $a:J(X)\to I^\bullet$ is the augmentation. Exactness makes $J(P^\bullet)\to J(H)[0]$ a quasi-isomorphism, and the bounded below injective resolution computes the target derived Hom. No projectivity of $J(P^\bullet)$ is required. All derived maps here are maps in the current module-sheaf category.

For clarity the external Hom square into $\mathsf D$ uses the actual original representatives as well. A map $f:K_1\to X$ represents a two-extension by pushing out $K_1\hookrightarrow P_1$ along $f$, then splicing with $0\to K\to P_{\mathrm{red}}\to H\to0$ from 067. The differentiable comparison sends it to

$$
0\longrightarrow J(X)\longrightarrow J(P_1)\mathop{\sqcup}_{J(K_1)}J(X)
\longrightarrow J(P_{\mathrm{red}})\longrightarrow J(H)\longrightarrow0 .
\tag{UC079.3}
$$

The pushout and both exactness statements follow from the proved properties of $J$. By the long exact sequence in $\mathsf D$, the image is zero exactly when the first extension of $J(K)$ is the pullback of a class in $\mathrm{Ext}^1_{\mathsf D}(J(P_{\mathrm{red}}),J(X))$. This gives an explicit test for a different endpoint, namely the external differentiable map groups between the realized coefficient objects themselves. Those Ext groups are distinct from the observable complexes. The vanishing calculation below concerns the observable comparison.

## 3. Actual support-natural comparison to observables

Let

$$
L_w(X)=R\underline{\mathrm{Hom}}_{\mathcal A}(E_w,X)
$$

be the derived internal liquid Hom for $X=G_b$ or $G$. The input to the smooth observable comparison at weight $w$ is $J(L_w(X))$. This is a complex of differentiable module sheaves in the derived category. At the parameter point its actual derived sections are $R\mathrm{Hom}_{\mathcal A}(E_w,X)$, by (UC079.2) and the adjunction for the liquid tensor unit. Indeed $R$ is projective and $\mathrm{Hom}_{\mathcal A}(R,-)$ evaluates at the profinite singleton. This passage to smooth families preserves the original external classes at the parameter point.

Put $U_b=(-b-1,b+1)$ and $U=\mathbb R$. Write $V_w(U_b)$ for the actual cochain complex at weight $w$ and coefficient singleton in 129 and 135, with quantum differential at fixed positive scale $s$. Work first classically using the actual weight-preserving Wick isomorphism. Choose one smooth $h$ of mass one supported strictly inside $[-1,1]$. For $w\geq1$ there is a fixed liquid map $e_w:R\to E_w$, $1\mapsto h^{\odot w}$ using the very symmetric tensors of 022. Use $e_0=\mathrm{id}_R$. Derived evaluation at $e_w$ is the natural map $L_w(X)\to R\underline{\mathrm{Hom}}_{\mathcal A}(R,X)\simeq X[0]$. With a functorial injective coefficient resolution $I_X^\bullet$, the map is represented by
$\underline{\mathrm{Hom}}_{\mathcal A}(E_w,I_X^\bullet)\to I_X^\bullet\leftarrow X[0]$.
Here the internal Hom computes derived Hom because $E_w$ is a nuclear Fréchet summand, hence tensor by $E_w$ is exact. Equivalently the map is defined directly by the closed derived tensor adjunction.

After applying $J$, send $J(G_b)[0]$ into the actual classicalized weight $w$ cochains on $U_b$. For $w>0$, a jointly smooth compact family $g$ goes to

$$
g\longmapsto\mathrm{Sym}\bigl(g(x_1)h(x_2)\cdots h(x_w)\bigr)
\tag{UC079.4}
$$

in all-even arity $w$ and cochain degree zero, at vacuum power zero. For $w=1$ this is the original $g$. For $w=0$ use $\int_{\mathbb R} g(x)\,dx$ times the actual regulator unit. Each formula acts on genuine parameter rows. At positive arity the bounded compact smooth kernel with scalar factor $1$ is a whole source with the fixed support in $U_b^w$. All its mixed parameter derivatives lie in the same support-history class. These maps are continuous on fixed chartwise coefficient stages by the ordinary derivative seminorms for products with fixed bumps. The Fourier bounds for smooth compact coefficients give admissible normal graph bounds on these stages. The degree-zero kernel is a classical cocycle since the classical complex is nonpositive. The weight-zero integral is a continuous compact test pairing, applied on every row. These operations commute with parameter differentiation and with extension from one support stage to the next. Thus (UC079.4) and its scalar case are actual differentiable cochain maps, not assignments on point values.

Extend to $J(G)$ using (UC079.2) and physical support extension, then restore the actual weight-preserving Wick maps on the output. This gives compatible derived arrows $\lambda_{b,w}:J(L_w(G_b))\to V_w(U_b)$ and $\lambda_w:J(L_w(G))\to V_w(U)$, with the commutative square

$$
\begin{matrix}
\varinjlim_b J(L_w(G_b)) &\longrightarrow& J(L_w(G))\\
\downarrow &&\downarrow\\
\varinjlim_b V_w(U_b) &\overset{\beta_w}{\longrightarrow}& V_w(U).
\end{matrix}
\tag{UC079.5}
$$

Naturality holds on the stage diagram and on target inclusions containing the indicated source supports and the fixed bump. Filtered colimits are taken in the named sheaf category. The actual lower arrow is an isomorphism of complexes: at fixed weight there are finitely many arities and vacuum powers. Each local representative has finitely many entire compact histories and all genuine rows on that fixed support. These have support in some $U_b$. Equality can be tested in a larger $U_c$ using the whole rapid difference and the compact localization of 135. In particular extension between stages is monic for the induced rapid relation. These local surjectivity and equality statements identify the colimit sheaf with the output. Complete (UC079.5) after forming the colimit at each weight. The strict split product gives the maps at finite weight quotients and their limit by 129; exact products there also model the derived products. This gives the same weight order as 022 and never interchanges the uncompleted support colimit and an infinite product.

The comparison is a linear filtered cochain comparison. The choice of $h$ is explicit. The map from the old support-valued sources does not furnish additional nonlinear or monoidal operations on them. It is common to both the unit and first field-slot tests. Evaluation at the fixed $e_1$ also factors through the external derived $\mathsf D$ mapping comparison above after taking parameter-point sections: $J(e_1):\mathscr O\to J(H)$, and $R\mathrm{Hom}_{\mathsf D}(\mathscr O,J(X))=J(X)(\mathrm{pt})$. Indeed a morphism from $\mathscr O$ is determined by the value of $1$ at the point, whose pullbacks are horizontal; multiplication by a smooth scalar gives all other values. Point sections are exact, so the equality also holds derived. This factorization explains explicitly why external mapping extensions can be evaluated in the observable map without assuming the Ext group between their differentiable coefficient objects vanishes.

## 4. Vacuum obstruction and degree-two class test

**Vacuum in ZFC.** At weight zero the original tower is $J(G_b)[0]$ with its growing supports. The observable tower is the fixed regulator unit sheaf $\mathbf C(-)(*)[0]$ with identity transitions. If $c>b$, a smooth bump supported in $(b,c)$ gives a nonzero cokernel for $G_b(*)\to G_c(*)$. By (UC079.2) this also witnesses a nonzero cokernel after smooth realization. Any family of objectwise weightwise equivalences commuting with stage transitions would identify that nonisomorphism with the identity on the vacuum after point evaluation. This is impossible, irrespective of the chosen comparison maps or a linear identification of individual vacua. The explicit comparison itself has a separate kernel at every stage, detected by a nonzero derivative of a compact bump of integral zero. At $w=0$ there are no incoming cohomological boundaries on either side. Replacing the old weight-zero output by the actual unit comparison is the weight-zero part of the variance repair in 026 and UC058, and the further real-scalar unit cone of 114 retains its own scope.

**First field slot.** At $w=1$, taking degree two after evaluating the parameter point in (UC079.5) gives precisely the original top map $\theta_H^2$. This uses exact evaluation and exact filtered colimits, with $E_1=H$. The bottom groups are zero because the actual weight-one observable complexes have degrees $-1$ and $0$. More precisely both vertical maps factor through degree zero by the explicit evaluation and compact insertion. In the model using $I_X^\bullet$ every old liquid cocycle in positive degree becomes a boundary in $I_X^\bullet$ after evaluation, since it resolves $X[0]$. This is an actual vanishing of the image, not a conclusion obtained by identifying only the set of visible support indices.

Under CH, the nonzero cokernel class of UC024 survives in the same upper support comparison after smooth realization and point evaluation. At the observable endpoint it maps to zero in the lower cokernel. If an equivalence were required there, it would force its nonzero degree-two group on the full upper weight-one complex to be zero. Thus under CH, even a repair confined to the vacuum cannot produce a weightwise equivalence with the actual observables. Under PH1 the upper comparison is an isomorphism in degree two by UC024. That removes the degree-two *support cokernel* on the old side, while the lower comparison was already an isomorphism of complexes in ZFC. It gives no identification of the upper complexes with the observables and no claim that every upper degree-two group vanishes. CH and PH1 are not selected as programme foundations.

**Scope for final integration.** The original support-valued analogy with actual observables is obstructed as a natural weightwise equivalence, and (UC079.5) explicitly carries its degree-two classes to zero. This result is compatible with the corrected scalar/regulator-valued pairing of 026 and UC058, the current replacement-based completed gluing theorem, and the all-open relative product UC076. A general equivalence of derived categories, or survival of the CH class at the intermediate external differentiable Ext endpoint (UC079.3) before evaluating on $h$, is outside this calculation. The exact survival test at that intermediate endpoint is stated above. The older B.6 concrete plot and smooth lift conditions differ from the current C.5 module-sheaf category. No claim about raw sequence cofibrancy or projection fibrancy is obtained by smooth realization; UC054 and the corrected replacement argument retain their separate scopes. The ZFC vacuum obstruction also applies to any comparison in the older convention whose claimed equivalences induce these same cohomology and support maps at the point. This return supplies a bounded obstruction and the transfer square on actual observables. The original unconditional GC and integrated programme verdict require their own remaining adjudication.
