# EXT-015 REACH / UC082 — the original CH class survives differentiable realization

**Candidate theorem.** For the original real-liquid objects $H,G$ and the exact smooth realization $J$ of UC079, the map

$$
J_*:\mathrm{Ext}^2_{\mathcal A}(H,G)\longrightarrow
\mathrm{Ext}^2_{\mathsf D}(JH,JG)
\tag{UC082.1}
$$

is injective in ZFC. Under CH the original UC024 class is nonzero on the right. It remains outside the image from all differentiable compact-support stages. In the subsequent observable comparison its image is zero by UC079.

## 1. Actual categories and frozen presentation

Here $\mathcal A=\mathrm{Liq}_p(\mathbb R)$ for the original fixed $0<p\leq1$ and admitted site bound, and $\mathsf D$ is the current category of differentiable module sheaves with natural flat connections of 129 and UC079. In particular this is the external differentiable Ext group at the intermediate endpoint of UC079.3. The sheaf category is on ordinary second-countable smooth parameter manifolds with local-diffeomorphism covers. The section functor on every such manifold is exact by the partition-of-unity proof of 129 §7. The exact colimit-preserving functor $J$ is the sheafification of $(\underline{C^\infty(M)}\otimes_R X)(*)$. Use $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$ and $G=\varinjlim_bG_b$ with the original $G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)}$. CP294 binds 267cf0c7545285e5f29dc16585840cbb691271f5 on research/reach-differentiable-ext-uc082-input-20261124.

| Frozen source | Git blob |
| --- | --- |
| [Original weight-stage realization](FIXED_SOURCE_WEIGHT_LOCALIZATION_018.md) | 81018f669afc062127877a3984e915f1fbea6f39 |
| [Original actual presentation](R3_EVALUATED_RELATION_COVER_067.md) | 7069938ce1e75f946e2f4ff70fcabb2f073065e9 |
| [Actual weight-stage acyclicity and cochain model](R3_POSITIVE_SUPPORT_ATTEMPT_084.md) | 932be6cc3445182a8423b23cc4840fe7ad685ced |
| [Measure generators and nuclear liquid input](LIQUID_PROFILE_RECORD_BRIDGE_091.md) | c517fe1ae46bcaa9f4a3fc0e64381ae8096bfe27 |
| [Weighted matrix description](R3_NEW_INPUT_AUDIT_094.md) | f0732cb96a27f540a2209a54d43ced97abb94503 |
| [Current differentiable sheaf category](SOURCE_CONTROLLED_PROCOCHAIN_APPLICABILITY_129.md) | 9b3f38f476646bf6ee395701d8b033cc8d3c265c |
| [Conditional CH cocycle](R3_GLOBAL_SUPPORT_DICHOTOMY_UC022.md) | a04aa1f9d420a96eb0a782f0e3914d0724972710 |
| [CH acceptance](R3_GLOBAL_SUPPORT_ACCEPTANCE_UC024.md) | 0f3b36f362d2636fed10c2a5492f546eb0d1f29b |
| [Typed transfer criterion](R3_INTEGRATION_DEPENDENCY_AUDIT_UC037.md) | 99ff425d8e1e046bce1c6da66112ed22f21b38ce |
| [Exact smooth realization and Yoneda map](SMOOTH_DERIVED_MAPPING_COMPARISON_UC079.md) | f0a05ad29f27883d8dd4d3078d486f572438e067 |
| [Current comparison acceptance](SMOOTH_DERIVED_MAPPING_ACCEPTANCE_UC081.md) | 1875486fe9dd7a5572f49399ab2afe66ab1815ab |

For the proof use the admitted isomorphisms of 018, 067 and 084: $H\simeq\underline s=\varinjlim_{r\in\mathscr R}T_r$ and $G\simeq E=\bigoplus_n B_n$, where $B_n=\underline s$ and $s$ is the nuclear Fréchet space of rapid sequences. The finite coordinate prefixes $E_N$ and the actual support stages factor through each other. The order $r\preceq t$ on positive rapid weights is domination by one constant, taken modulo mutual domination. Denote the normalized generators of $T_r$ by $g_i^r$, which map to $r_i e_i$ in the physical sequence coordinates. Each $T_r$ is the actual scaled copy of the reduced free liquid measure module on $S_\infty=\mathbb N\cup\{\infty\}$ from 084, with normalized basis corresponding to $\delta_i-\delta_\infty$. A morphism from $T_r$ is determined by the normalized generators and the zero value at $\infty$, by the free-module adjunction and the split reduction. The transition $i_{r,t}$ sends $g_i^r$ to $(r_i/t_i)g_i^t$. We do not assign a new topology to any liquid syzygy.

## 2. Normalized parameter integration through extensions

For each $X\in\mathcal A$ and parameter manifold $M$, the partial derivative $\partial_\tau$ along the second factor of $M\times\mathbb R_\tau$, taken using the flat connection, gives the exact sequence

$$
0\longrightarrow JX(M)\overset{\mathrm{pr}^*}{\longrightarrow}
JX(M\times\mathbb R)\overset{\partial_\tau}{\longrightarrow}
JX(M\times\mathbb R)\longrightarrow 0 .
\tag{UC082.2}
$$

On a product of an open set with an interval, the identity for the scalar normalized primitive $\int_{\tau_0}^\tau$, with evaluation at any anchor $\tau_0$ in the interval, is a continuous linear identity of smooth-function spaces. It induces the same identity after liquid tensor with $X$ and singleton sections, before sheafification.

Here is the check after sheafification. For the kernel, a section with zero $\tau$ derivative locally has a presheaf representative whose derivative becomes zero after shrinking to a smaller product box. On that box the scalar identity identifies it with pullback from the box's parameter base, at any local anchor in its interval. For a fixed parameter point and compact segment of $\mathbb R$ from zero to a prescribed $\tau$, use finitely many such boxes and shrink their parameter bases together. The local equalities then propagate along the segment, by restriction and evaluation at common anchors. Thus the original section is pullback of its value at $\tau=0$. This is equality in the sheaf, including for objects with sections undetected by values at singleton points.

For surjectivity, near any fixed parameter point and any compact interval $[-L,L]$, $L>0$, finitely many product boxes supply local presheaf representatives on a common smaller parameter neighborhood times the respective time intervals. Take a finite smooth partition in $\tau$ with compact supports in those intervals summing to one near $[-L,L]$. Multiplication by each partition function and extension by zero in $\tau$ give continuous linear maps of scalar smooth-function factors. Applying them before tensor and summing produces a presheaf representative on the common neighborhood times $\mathbb R$ agreeing with the prescribed derivative on $(-L,L)$. Integrate this representative with anchor zero. The primitives on these product sets all have zero initial value. Their differences on overlaps vanish by the just-proved kernel assertion, since the overlaps on the time axis are intervals containing zero. The primitives therefore glue. This gives (UC082.2) without asserting that the presheaf was already a sheaf.

Now let

$$
0\longrightarrow JY\longrightarrow D\overset{q}{\longrightarrow}JX\longrightarrow0
\tag{UC082.3}
$$

be any short exact sequence in $\mathsf D$ with realized endpoints. The same derivative sequence is exact for $D$. For surjectivity, integrate the projection of a given section in $JX$, lift that primitive using exactness on $M\times\mathbb R$, and subtract its pullback of the initial value to normalize it. The derivative discrepancy lies in $JY$ and can be integrated there and added. For the kernel, project a zero-derivative section to $JX$, subtract the pullback of its actual initial value in $D$, and apply the kernel assertion in $JY$. For each such $D$, including $D=JX$, define $\int_0^1 f\,d\tau$ to be the value at one of the unique derivative primitive of $f$ with zero initial value. Uniqueness proves naturality in $M$ and under morphisms between these objects, and smooth module linearity for scalars independent of $\tau$. On charts the parameter derivatives commute with $\partial_\tau$ by flatness and commute with the initial value restriction. Thus the integral commutes with the flat connection along $M$. This construction supplies the integral for the actual middle object of an arbitrary extension in (UC082.3), without a convenient-space or completeness assumption on that object. For a realized presheaf expression it agrees with the continuous scalar integral tensored with the identity, by uniqueness.

## 3. Rapid transitions split every relevant pulled-back extension

Suppose $\delta_i=r_i/t_i$ is rapid. Put $\alpha_i=\sqrt{\delta_i}$. There are actual liquid maps

$$
a_{r,t}:T_r\longrightarrow\underline s,\quad g_i^r\longmapsto\alpha_i e_i,
\qquad
m_t:\underline s\longrightarrow T_t,\quad (x_i)\longmapsto \sum_i x_i g_i^t .
\tag{UC082.4}
$$

The first map is the null plot $\alpha_i e_i\to0$ in $s$, extended by the universal property of the reduced free module. To verify the second directly, take a compact profinite plot into $s$. All its weighted sup seminorms are bounded. For any fixed $0<q_0<p$ the sums of absolute $q_0$ powers of the sequence coordinates are uniformly bounded. The finite quotients of $S_\infty$ isolating finitely many indices are cofinal. On each quotient the measure with reduced coefficients as displayed has a sum of absolute powers of order $q_0$ bounded by twice that uniform bound, since the last tail coefficient is minus the sum of the isolated coefficients and $q_0\leq1$. Those finite coordinates are continuous in the plot. They give a compatible continuous plot into the fixed bounded measure stage of exponent $q_0$, by the defining compact inverse-limit description. The construction is linear and natural on all profinite tests. Thus it is the actual liquid morphism to the reduced free module, then to $T_t$ by its normalized identification. In particular the transition factors as $m_t$ after multiplication of the $s$ coordinates by $\alpha_i$, after $a_{r,t}$. The identity is tested on the normalized generators by their universal property. [Scholze, Lectures on Analytic Geometry, Definition 6.3 and Theorem 6.5](https://arxiv.org/pdf/2605.03655)

Choose smooth real bumps $\varphi_i$ in pairwise disjoint intervals inside $(1/(i+1),1/i)$ with $\int_0^1\varphi_i(\tau)^2\,d\tau=1$. Scale a single fixed compact smooth bump by length proportional to $(i(i+1))^{-1}$ with the usual square-root normalization. Every derivative supremum of a fixed order grows at most polynomially in $i$. It follows that

$$
v(\tau)=(\alpha_i\varphi_i(\tau))_i\in s,\qquad
\mathcal L(x)(\tau)=\sum_i x_i\varphi_i(\tau)
\tag{UC082.5}
$$

are respectively a smooth curve with values in $s$ and a continuous linear map $s\to C^\infty(\mathbb R)$. Indeed, every differentiated seminorm tail of the former tends uniformly to zero using rapidness of $\alpha$, and each differentiated scalar sum of the latter is bounded by a sufficiently high rapid seminorm of $x$. These estimates include the common accumulation point $\tau=0$. The nuclear Fréchet tensor model of UC079 makes $J(\underline s)$ the actual sheaf of smooth families with values in $s$, by the admitted Fréchet isomorphism $s\simeq\mathcal D_{[-1,1]}$ and the jointly smooth compact kernel description there.

Apply (UC082.3) to an arbitrary differentiable extension of $JT_t$ by $JG$. The curve $\gamma=J(m_t)(v)$ in $JT_t(\mathbb R)$ lifts to a section $b\in D(\mathbb R)$ by exactness on $\mathbb R$. For a section $u\in JT_r(M)$, use $a_{r,t}$ to form the smooth family with values in $s$ $x=J(a_{r,t})(u)$. In the jointly smooth scalar family $k_u(m,\tau)=\mathcal L(x(m))(\tau)$ the former estimates also control every parameter derivative on compact sets. Put

$$
s_M(u)=\int_0^1 k_u(m,\tau)\,\mathrm{pr}_{\mathbb R}^*b\,d\tau
\quad\hbox{in }D(M).
\tag{UC082.6}
$$

This is a natural smooth module map in $u$ and commutes with parameter connections, by the integral and the continuous scalar kernel rule. Projecting to $JT_t$, its output is the image under $J(m_t)$ of the integral of $k_u(m,\tau)v(\tau)$, by the proved naturality. Coordinate $i$ of that integral in $s$ is $\alpha_i x_i(m)$, by disjoint supports and unit squared integrals. This identifies the entire projected map with $J(i_{r,t})$ using (UC082.4). The equality uses the actual maps through the integral in $s$ and the reduced free module. It does not assume singleton detection for $D$ or for arbitrary liquid objects. Equation (UC082.6) thus splits the pulled-back differentiable extension. In particular, for rapid ratio,

$$
\mathrm{Ext}^1_{\mathsf D}(JT_t,JG)\longrightarrow
\mathrm{Ext}^1_{\mathsf D}(JT_r,JG)
\quad\hbox{is zero}.
\tag{UC082.7}
$$

Neither a projectivity assumption on $JT_r$ nor a vanishing assumption on the original differentiable Ext group at any one stage is used. The fast diagonal factor in (UC082.5) is essential for the lift used here.

## 4. The two inverse Hom diagrams agree on derived limits

Write $A_r=\mathrm{Hom}_{\mathcal A}(T_r,G)$ and $C_r=\mathrm{Hom}_{\mathsf D}(JT_r,JG)$. The natural map $A_r\to C_r$ is injective since equality after $J$ gives equality on normalized generator values by singleton evaluation (UC079.2), and those values determine the liquid morphism. Let $Q_r$ be its cokernel in real vector spaces.

We use a genuine degree-zero comparison for the single intervening source $\underline s$. A morphism $\psi:J(\underline s)\to JG$ is determined by its point-value linear map $L:s\to\bigoplus_n s$ since the output sheaf is concrete, with smooth families locally in a finite coordinate prefix by UC079.2. If the image of $L$ were in no finite prefix, choose a sequence of inputs with outputs escaping successive prefixes. Multiply each input by a nonzero scalar so that the scaled inputs can be joined in one smooth curve with values in $s$ through zero. Explicitly use the distinct polynomially shrinking intervals of §3, a bump equal to one at the center of each interval, and scale the input at index $i$ so its first $i$ seminorms are at most $(1+i)^{-i}$. The seminorm derivative tails then vanish for every fixed request at the common accumulation point. The image curve is locally in one output prefix at that point, contradicting the escaping outputs. Therefore $L$ takes values in some finite prefix $E_N$. If $L:s\to s^N$ were discontinuous, a null sequence with outputs failing one seminorm test would have a subsequence of inputs small enough in its first $i$ seminorms to interpolate without scaling. Projection of the smooth output curve to $E_N$ would then fail continuity, a contradiction. Thus $L$ is continuous into that actual finite prefix, defines a liquid map, and its image under $J$ agrees with $\psi$ on all sections by concreteness of the output. This comparison is used only in degree zero.

If $r/t$ is rapid, the transition of §3 factors through $\underline s$. The restriction to $JT_r$ of any morphism in $C_t$ therefore comes from a liquid map in $A_r$, by applying the preceding degree-zero comparison after precomposing with the second factor of (UC082.4) including the diagonal multiplier. Thus $Q_t\to Q_r$ is zero for rapid ratio.

The order-preserving self-map $\sigma([r])=[\sqrt r]$ of $\mathscr R$ satisfies $r\preceq\sigma(r)$, and the ratio at that transition is rapid. It is well-defined on domination classes. It is cofinal for inverse limits after reversing the order: the objects above a given $r$ after applying $\sigma$ form a nonempty directed set, so the appropriate comma nerve is contractible. Hence restriction to that reindexed system induces an equivalence on derived inverse limits. The transition natural transformation from the reindexed inverse system $Q_{\sigma(r)}$ to $Q_r$ is strictly zero. It also induces the inverse to restriction on derived limits, by the canonical compatibility of the limit cones. Therefore $R\varprojlim Q=0$. The short exact sequence of inverse systems now gives

$$
R\varprojlim A_r \simeq R\varprojlim C_r .
\tag{UC082.8}
$$

The same $\sigma$ gives zero transitions in (UC082.7), and in particular the inverse limit of the local differentiable first Ext groups is zero. This step requires no choice of a well-ordered CH ladder.

## 5. Injectivity on the actual degree-two groups

Since $J$ preserves filtered colimits, $\varinjlim_r JT_r=JH$. Use the augmented source bar resolution of this colimit. It is exact since filtered colimits are exact, or by applying $J$ to the exact liquid source bar. Against a bounded-below injective resolution $I^\bullet$ of $JG$, the total Hom complex of the bar computes $\mathrm{Ext}_{\mathsf D}(JH,JG)$ by the K-injective target. Its double complex has columns given by the Roos products over strings $r_0\preceq\cdots\preceq r_a$ with vertical entries $\mathrm{Hom}_{\mathsf D}(JT_{r_0},I^q)$. Use the sign $\delta+(-1)^a d$ of 084. The row of vertical degree-zero cycles is the Roos complex of $C_r$.

For the degree-two edge injection, suppose a cocycle $c$ in that row becomes a total boundary. A total degree-one primitive $(u,v)$ has bidegrees $(0,1)$ and $(1,0)$. Its equations are $du=0$, $\delta u-dv=0$, and $\delta v=c$. Therefore the vertical classes of $u$ form an inverse-limit family of the local differentiable first Ext groups. That limit is zero by §4. We can choose a componentwise $w$ of bidegree $(0,0)$ with $u=dw$. It follows that $v-\delta w$ is vertically closed and $\delta(v-\delta w)=c$. This is a boundary already in the Roos row of $C_r$. Thus the edge from $\varprojlim^2 C_r$ into the actual differentiable second Ext is injective. The argument considers every total primitive and uses no collapse of the higher differentiable rows.

On the liquid side the local higher Ext vanishes for the exact $T_r,G$ by 084.5. This identifies the analogous liquid edge from $\varprojlim^2 A_r$ with $\mathrm{Ext}^2_{\mathcal A}(H,G)$, as in 84.16. The edge comparison is the one induced by $J$. To see the compatibility on complexes, choose a bounded-below liquid injective resolution of $G$, apply $J$, and map its resulting exact resolution to $I^\bullet$ extending the identity of $JG$. The latter comparison exists by target injectivity. Applying $J$ and this chain map in the same bar strings gives the map on the two Hom totalizations. It is $J_*$ on the actual derived groups and on the original spliced two-extensions. On their vertical degree-zero cycles it restricts to $A_r\to C_r$. Equations (UC082.8) and the differentiable edge injection now prove (UC082.1), with no CH premise in this proof.

## 6. The CH class and bounded-stage corrections

Let $z$ be the genuine degree-two class of UC024 under CH on the original $H,G$. It is nonzero, so (UC082.1) gives $J_*z\ne0$ in the group of UC079.3. For the fixed representative by $f:K_1\to G$, this also proves that its induced first extension of $J(K)$ does not come by pullback from an extension of $J(P_{\mathrm{red}})$ in the criterion of UC079.3.

The projections of $z$ to every coordinate $B_n$ are zero by UC024. Consequently the projections of $J_*z$ to the corresponding differentiable Ext groups are zero by naturality. Suppose $J_*z$ had a representative from some $\mathrm{Ext}^2_{\mathsf D}(JH,JG_b)$. The support map factors through one actual $E_N$ before applying $J$, by the original cofinal support comparison. Then $J_*z$ would be in the image of the split inclusion of $J(E_N)$. Retraction to $J(E_N)$ and its finitely many coordinate projections would give zero, since finite direct sums split on Ext. This contradicts $J_*z\ne0$. Thus the original CH cokernel class also survives the induced cokernel map for the actual chart of compact-support objects in the intermediate differentiable groups. This tests every differentiable bounded-stage correction, not only those lifted from liquid classes.

The derived comparison and boundary calculations use the actual external Ext groups before evaluation on the bump of UC079. That later observable map still sends the class to zero. PH1 gives the original upper isomorphism in degree two on its own assumptions; injection (UC082.1) supplies no surjectivity assertion for the intermediate differentiable support comparison. The old concrete B.6 category is separate. The mathematical controls are the all-derivative lift at the accumulating time intervals, the sheaf kernel test without singleton detection, the arbitrary total primitive, and the explicit finite-prefix contradiction. Finite fixtures cannot prove those assertions. This candidate is a bounded transfer theorem, with distinct critical review and protected readback still to follow.
