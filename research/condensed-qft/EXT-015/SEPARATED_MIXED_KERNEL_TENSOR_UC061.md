# EXT-015 REACH / UC061 — relative tensor for the actual separated two-slot kernels

**Candidate disposition.** On two disjoint nonempty open intervals, the matching quantum exterior product gives a relative derived tensor equivalence onto the actual source-controlled mixed sector with one slot in each interval. It is compatible with total-weight completion over the common vacuum algebra. The inverse is given, after Wick classicalization, by the four independent affine moments and the compact Green homotopy acting on whole original histories. The same calculation works on the current differentiable module sheaf at every fixed profinite test.

## 1. Domain and exact source identities

Work in ZFC and in the category of real liquid modules at fixed $0<p\leq1$. Let $U_1,U_2$ be disjoint nonempty open intervals in the physical line and $U=U_1\sqcup U_2$. The closures of the intervals may touch. Fix a positive Wick scale $s$. Use the original full source-controlled coefficient sheaf of 126, the scalar algebra $\mathbf C(M)$ of 135.6, and the original uniform fixed-order rapid relation. At a manifold parameter point write $\mathcal C$ for the liquid scalar object. For fixed profinite $S$, use the actual differentiable module sheaves and their connection as in 129 and UC058, with filtered multilinear maps in the current C.4.4.1 and C.4.5 convention. [Costello–Gwilliam, Appendix C](https://www.cambridge.org/core/books/abs/factorization-algebras-in-quantum-field-theory/homological-algebra-in-differentiable-vector-spaces/CB7577A6C2E0F5151FE79806CC88ABE6)

CP280 binds protected cut df2a66ceabc2abb368cc7aef0dfdfa86af762871 on retained ref research/reach-separated-mixed-tensor-uc061-input-20261123. Its relevant mathematical sources are:

| Source | Exact blob |
| --- | --- |
| [Mixed source and rapid relation 108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | `587c15fd6e24f6e6b14de574ff878221cdbd5cb6` |
| [Quantum Wick structure 111](RENORMALIZED_QUANTUM_STRUCTURE_111.md) | `b7b1e5f970904d6e7de065a4fedd382e212a3022` |
| [Matching R1 composition 117](R1_WICK_DRESSED_QUANTUM_COMPARISON_117.md) | `e95b1155ebb2018a80d2dc559560730fd7ea6594` |
| [Whole parameter rows 126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | `5b05c6147d237ca1d22e4dcbce9262b0f038c163` |
| [Exact localization and scalars 135](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md) | `62d91e9d5f38fc85cf2793507d887d526eccce7a` |
| [One-slot moments 141](SCALAR_RELATIVE_WEIGHT_ONE_COMPARISON_141.md) | `de6b608c8def91dd0b8b2d98fe410348ac92a17d` |
| [Actual diagonal projection 147](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md) | `89b3d4a835f3750114e983854585e33d8184cb1f` |
| [Ordered two-slot Koszul homotopy 150](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | `03deca9212a9bea56743e482e5cb79edb46b9d7f` |
| [Whole-history distinct-block lift UC044](GENERAL_INCIDENT_SCALAR_GREEN_LIFT_UC044.md) | `81e1492d12e9439a04d7b7df562fe68d3738ada5` |
| [Connected weight-two computation UC047](RESIDUAL_WEIGHT_TWO_CONTRACTION_UC047.md) | `c582d45523a63288b339204574f33ac17820e327` |
| [Derived pairing and completed field tensor UC058](REGULATOR_VALUED_DERIVED_COMPLETED_PAIRING_UC058.md) | `f46fbf85c635a8d90b8c357032fdd8c14120caaa` |

Let $X_1(U_i)$ denote the actual one-slot coefficient complex, with degrees $-1,0$. Use the labelled classical two-slot complex on $U$ before graded symmetrization. On this labelled complex, write $p_{12}$ for multiplication of actual kernels by the characteristic function of the component $U_1\times U_2$ of $U^2$. This function is locally constant on $U^2$. Let $Z_{12}$ denote its image as an actual complex, with the original quotient and parameter rows. This sector is taken from the full original two-slot histories, which may be coupled and may have hidden vertices.

The projector is a whole-source map. On a fixed finite collection of complete stages use the common compact output support to choose a fixed smooth physical cutoff in $U_1\times U_2$, equal to one on the part of that support in $U_1\times U_2$. This part is compact since the component is closed in $U^2$. The cutoff agrees on a neighborhood of the whole support with the indicated locally constant function. The source multiplication of 108 acts continuously on those stages and gives exactly the projected output, including on derivatives of distributions. The result is independent of such choices by whole-family equality. Its idempotence, commutation with the physical differentials and preservation of the rapid relation hold in the actual envelope by the same cutoff argument. Equation 135.1 and its induced rapid comparison apply on the fixed supports. Thus the projector descends through the original image, rapid quotient and parameter sheaf without identifying all pointwise supports with an unproved image condition.

Let $\tau$ exchange slots with the graded exterior signs, and let $\sigma=(1+\tau)/2$. The two ordered mixed rectangles are disjoint. On the invariant mixed component, $\sigma$ from $Z_{12}$ is an isomorphism onto that component with inverse $2p_{12}$. Indeed $p_{12}\tau$ vanishes on $Z_{12}$, and invariance identifies the second ordered part of any mixed invariant with the exchange of its first part. This fixes the normalization to match the averaged exterior product of UC058. It does not identify the two distinct affine moments of the two physically labelled intervals.

## 2. The compact Green homotopies with separate support

Choose compact smooth dual bumps $b_{i,0},b_{i,1}$ inside $U_i$ with moments $\int x^a b_{i,b}(x)\,dx=\delta_{a b}$ for $a,b\in\{0,1\}$. For example use the normalized bump and its negative derivative as in 141 and subtract the first moment from the mass bump by the prescribed correction. For a compact ordered kernel $v$ set

$$
m_{i,a}(v)=\int x_i^a v\,dx_i,\qquad
B_i(v)=\sum_{a=0}^1 b_{i,a}(x_i)m_{i,a}(v),\qquad
h_i(v)=e*_{x_i}(1-B_i)v,\qquad e(t)=|t|/2 .
\tag{UC061.1}
$$

These operations keep the full regulator functions. An integral in a missing variable means proper distributional pushforward with the ordinary physical density. For fixed supports the moment tests use a smooth cutoff equal to one on a neighborhood of the support. If the two coordinate supports are contained in compact sets $K_1\Subset U_1$ and $K_2\Subset U_2$, the output of $h_i$ has support in the rectangle with coordinate $i$ enlarged to the compact interval hull of $K_i$ and its two bump supports. The other coordinate support is unchanged. Outside the hull the convolution kernel is affine in the integrated coordinate and the two moments of $(1-B_i)v$ vanish, as distributions in the spectator. Since each $U_i$ is an interval, this hull is compactly contained in $U_i$. No positive global separation of the entire intervals is used.

Here is the source-stage check for (UC061.1).

- For the moments, multiply by the chosen smooth test and forget slot $i$ using 108. The result has compact support in the spectator interval. If spectator histories still have hidden vertices in $U$, rehost them in the spectator interval by 135.1 with a fixed cutoff equal to one on their complete evaluated support. Exterior composition with the fixed bump in the other interval gives $B_i$. The all-vertex moments use the actual scalarization of 135.2. All these maps act continuously on the original complete stages, with one finite output list of scalar stages for the chosen history and independent of its relaxed graph order.
- For $h_i$, first extend to a common ambient connected interval, for example the physical line. Localize each fixed whole input stage to the ordered rectangle by the fixed physical cutoff for $p_{12}$. Move this cutoff through the outer source derivatives with the full finite Leibniz formula. Every same-retained-block contribution is zero because the cutoff and its derivatives vanish on a neighborhood of the retained diagonal at every positive regulator. One is left with an exact finite collection of distinct-retained-block histories even when there are hidden or simultaneous source collisions. Apply UC044 to this collection in the ambient interval with the two chosen bumps in $U_i$ for the integrated coordinate. It applies to arbitrary admissible dependence on the integrated vertex and gives the actual compact formula (150.5) with its signed moments and original full scalar stages. The proof of that one-coordinate formula uses only these two bumps and a compact window on that coordinate. It does not require coincident bump choices for the spectator. On each whole stage the preceding hull argument puts the entire evaluated result in a fixed compact subset of $U_1\times U_2$. Choose one compact cutoff in that rectangle equal to one near this resulting support and apply 135.1 to rehost the whole output in $U$. Its evaluated output is the same actual family, so the original ordered sector is preserved.

Fixed choices for windows, cutoffs and rehosting depend only on the compact supports and geometry of each complete stage, not on the representative within that stage, the regulator, or its graph-order refinement. Continuous stage maps extend on the completed projective mixed coefficients. The identities are identities of the entire evaluated families; thus different choices give the same maps on the actual images.

For each mixed parameter/regulator derivative, (150.6) bounds the compact operator by the input fixed finite $H^{-t}(\mathbb R^2)$ norm on its common compact support, with no regulator loss and no dependence on the requested rapid decay power. A larger finite $t$ may be used once for that derivative. This bound follows from the compact difference kernel in $L^1$, a fixed smooth output cutoff and the bounded partial moment and bump maps in (150.5). The rehosting step has exact evaluation and the induced rapid relation of 135.1. Hence every originally negligible entire difference stays negligible, including cancellations between input histories. These operations commute with parameter differentiation by the fixed distributional formulas, and with scalar multiplication by a regulator function because it is constant in both spatial slots. Apply the continuous source operations to the actual compatible rows of 126, and descend whole equality and the rapid intersection through the cover-local source lifts on profinite tests. This proves the claimed maps in the liquid sheaf and separately on the actual smooth fixed-test complexes with their connection.

## 3. The mixed complex and the exterior comparison

On compact distributions the identities are

$$
D_i h_i=1-B_i,\qquad h_iD_i=1,\qquad m_{i,a}D_i=0,\qquad D_i=\partial_{x_i}^2.
\tag{UC061.2}
$$

They follow from $e''=\delta_0$ and integration by parts against the affine moment tests. Operations belonging to different coordinates commute. Use the labelled exterior complex with degree-minus-one generators $e_1,e_2$ and $d=\sum_iD_i\iota_i$. Set $H_i=h_i e_i\wedge$ and let $\Pi_i$ apply $B_i$ when $e_i$ is absent and be zero when $e_i$ is present. The separate identities (UC061.2) give $dH_i+H_id=1-\Pi_i$; the cross terms cancel by $\iota_j(e_i\wedge)+(e_i\wedge)\iota_j=\delta_{ji}$. The maps $\Pi_i$ are cochain maps. Hence the actual cochain homotopy on $Z_{12}$ is

$$
H=H_1+\Pi_1H_2,\qquad dH+Hd=1-\Pi_1\Pi_2 .
\tag{UC061.3}
$$

For example on $v e_1\wedge e_2$ the two mixed derivatives give $d(v e_1\wedge e_2)=-D_2v e_1+D_1v e_2$, and the contribution from $\Pi_1H_2d$ is zero since $\Pi_1$ kills the exterior degree two component. Then $H_1d$ is the identity there by $h_1D_1=1$. These operations stay inside $Z_{12}$ by section 2, including the intermediate $\Pi_1H_2$.

The product $\Pi_1\Pi_2$ is reinsertion of the four affine moments $m_{1,a}m_{2,b}$ against the four pure bump products $b_{1,a}\boxtimes b_{2,b}$, and is zero off degree zero. Thus there is an actual cochain homotopy equivalence

$$
Z_{12}\simeq \mathbf C(M)^{\oplus4}[0]
\tag{UC061.4}
$$

at each manifold in the liquid model, and the same split representative and homotopy after evaluation on each fixed $S$. At the parameter point the coefficient in (UC061.4) is $\mathcal C$. The affine moments are natural for enlarging either interval while keeping the two occupied components disjoint, since the tests are restrictions of the same affine functions. The particular bumps and homotopies can depend on the intervals.

Over the liquid scalar algebra, 141 gives the homotopy equivalences from the one-slot complexes to the two free moment generators, by maps linear over actual scalar functions. Their relative derived tensor is therefore represented by $\mathbf C(M)^{\oplus4}[0]$, using the finite free modules concentrated in degree zero. The ordinary exterior product on the two complexes compares with this representative by its values on those four generators. These are exactly the bump products in (UC061.4). By direct scalar balancing, the induced derived comparison into the full actual ordered mixed sector is an equivalence. The independently constructed fixed-test comparison uses the same finite free representatives and the actual ordinary product on their generators. It does not require evaluation on $S$ to commute with arbitrary derived tensor products.

## 4. Shared vacuum completion and matching quantum product

Write $B=\mathbf C(M)[\hbar]$ with $\hbar$ of weight two and cochain degree zero. As in UC058, take the graded polynomial models and complete total weight by products of the weight pieces. The one-slot component carried by a given interval in the classicalized model consists of the module $B\otimes_{\mathbf C(M)}X_1(U_i)$ with its generator complex of weight one. The ordered mixed target is $B\otimes_{\mathbf C(M)}Z_{12}$ with its generator complex of weight two. These descriptions follow from the actual arity and vacuum entries, with no collisions connecting the two retained component labels. The action of $B$ is scalar multiplication and a shift of the common vacuum power. They have the same finite free homotopy models as in section 3, with weights shifted by the indicated amounts. Thus the derived relative tensor over $B$ in this bidegree is represented by the four copies of $B$ shifted to weight two. The comparison sends those generators to the symmetric mixed bumps using $\sigma$. Taking the inverse limit of the finite total-weight cutoffs gives a homotopy equivalence to the mixed sector, with every identity and homotopy given weight by weight. The completion does not use interchange of tensor with arbitrary products.

For the matching quantum maps use the image of this mixed sector under $W_s$ in the full weight-graded quantum model. The quantum mixed projection is the conjugate of the classical one. The Wick maps commute with multiplication by the common regulator and vacuum scalars and preserve total weight and support inclusions. The product is exactly $W_s\mu_{\mathrm{cl}}(W_s^{-1},W_s^{-1})$. The one-slot parts have trivial Wick correction, while the target mixed part is the transported one just specified. A mixed observable with two even slots may acquire an arity-zero contribution times $\hbar$ under $W_s$. This term is included. For a control take normalized nonnegative smooth inputs in the two intervals. Their compact supports are strictly ordered and separated, even when the open endpoints touch. On these supports the cross pairing in the Wick contraction is $P_0(x-y)=|x-y|/2$ modulo the actual rapid relation, by 111 and 117. Its mass pairing with the two inputs is strictly positive; the quantum cross term cannot be dropped. The cochain and tensor comparisons are compatible with the support inclusions and the parameter connection, using the same 111 and 126 Wick transport. In the finite affine-solution target of UC058, the four moments of section 3 are exactly the four bilinear affine coefficients from the two separate components.

As a low-weight consequence, the two-input relative comparison for $U=U_1\sqcup U_2$ is an equivalence through total weight two. To see the other summands, in the classicalized model the sectors in weights zero and one are the common vacuum and the two single-component one-slot sectors. In weight two there is one common $\hbar$ vacuum, the two pure two-slot sectors and the mixed sector. The pure sectors are exactly the two-slot complexes of their individual intervals by the same output-component projector and the localization 135.1. Tensoring with the other factor's vacuum is the relative unit map on each pure sector. The bidegree sum is preserved by the relative tensor over $B$, which has arity zero and nonnegative weight. Thus the mixed summand computed above is the only extra comparison needed in that weight. Conjugate by $W_s$ for the stated quantum prescription.

## 5. Controls and boundary

All four moment coordinates are independent in (UC061.4); in particular there is no relation between the two mixed affine moments. For a support control, extend both intervals into one connected interval. The difference of the two symmetric mixed bump terms $b_{1,1}\boxtimes b_{2,0}$ and $b_{1,0}\boxtimes b_{2,1}$ is nonzero in the mixed cohomology of the disjoint union by the four moments. Its extension to the connected interval has zero symmetric affine moments. It has zero diagonal extraction by 147 since its supports were separated and the bump histories are distinct-block. It is therefore a boundary in the connected classical weight-two model by UC047. The Wick transports give the corresponding statement for the matching quantum maps. This tests the difference between the comparison on the disjoint union and its further support map to a connected target.

A regulator scalar such as the nonzero Laurent class $\epsilon^{-1}$ can multiply any of the four bump generators. Its entire affine moment is that scalar. Its physical finite coefficient vanishes, so replacing the scalarization with physical finite readout would destroy this control. The fixed norms in section 2 address the original negligible-error relation, not a test for vanishing of formal moments. No general equality with an uncompleted or absolute real tensor of mixed history spaces follows.

The theorem concerns exactly the source-controlled real and liquid parameter rule and the first separated mixed bidegree. Higher bidegrees can have collisions inside an occupied interval and require new support-controlled homotopies. The larger prior family recovery obstruction UC055 and the independent original R3 comparison keep their separate scopes. Exact-source nonauthor review and protected readback are required for admission. No numerical fixture is used in place of the whole-history proof.
