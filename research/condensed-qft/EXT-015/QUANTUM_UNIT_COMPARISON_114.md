# EXT-015 REACH / 114 — the scalar-unit cone at total weight zero

**Disposition: bounded typed comparison obstruction, proposed for review.** The accepted enriched quantum model has an actual total-weight-zero object larger than the corrected scalar-field unit. The canonical unit map is split in the real liquid heart, and its derived cone contains an explicit nonzero Laurent subobject. Consequently a strict weight-preserving quasi-isomorphism, or a comparison required to be a quasi-isomorphism on weight-zero associated graded, cannot identify these two models. This does not close M5/R4 or the full programme. Review115 and ledger116 remain separate.

## 1. Category, frozen objects and the exact comparison

Work in the real liquid heart $\mathcal A=\mathrm{Liq}_p(\mathbb R)$ for fixed $0<p\le1$, and its cohomological derived category $D(\mathcal A)$, in ZFC. Fix a nonempty physical interval $U$ in the admitted one-dimensional model. The frozen input cut is0638ad20e702516ac7b33c549adedb4df3970581 on `research/reach-unit-input-frozen-20261031`; CP065 binds this construction before mathematics.

| Dependency | Exact Git blob |
| --- | --- |
| Corrected scalar field-source bridge026 |45681b9e459ac27b45d800847888bc3f7166baf2 |
| Its critical audit027 |54cfabad8f4b29d819aa3bfb753f260834f4be42 |
| Laurent/profile realization091 |c517fe1ae46bcaa9f4a3fc0e64381ae8096bfe27 |
| Mixed domain and enriched boundary108 |587c15fd6e24f6e6b14de574ff878221cdbd5cb6 |
| Quantum record theorem111 |b7b1e5f970904d6e7de065a4fedd382e212a3022 |
| Its distinct review112 |f1c2053d25c71bac169432bb28a7c91819d89147 |
| Quantum acceptance113 |e9e0ff6ff3719c23b895e21e9d1e96117a393efe |

Write $R=\mathbb R_{<p}$. The corrected026 field source has zeroth symmetric power $R[0]$. Its scalar observable unit is the real complex $\mathbb R[0]$, with canonical liquid realization $R[0]$. This is the source of the comparison below. There is no reversion to the wrong-variance026.1 object with test-function coefficients.

The distinction between external and internal Hom matters.026 writes external liquid Hom and derived-Hom complexes of real vector spaces. At arity zero the projective singleton makes the external scalar derived Hom equal to $\mathbb R[0]$, whose canonical realization is $R[0]$. This does not identify an arbitrary external Hom set with an internal liquid object. The present comparison uses only the canonical observable-unit realization $R[0]$ and an actual object of $\mathcal A$; it asserts no new internal derived-Hom calculation.

Let $\mathcal P_0$ be108's actual scalar-family image, let $\mathcal I_0^{\mathrm{rap}}$ be its ambient fixed-order rapid subobject, and put

$$
\mathcal Z_0=\mathcal P_0/
(\mathcal P_0\cap\mathcal I_0^{\mathrm{rap}}).
\tag{114.1}
$$

The canonical map under test is

$$
u:R[0]\longrightarrow\mathcal Z_0[0],
\qquad c\longmapsto[\epsilon\mapsto c].
\tag{114.2}
$$

It is the accepted quantum unit at total weight zero. This is a comparison of actual scalar families modulo the stated rapid ideal, not a formal dimension count.

## 2. Actual Laurent scalars survive the rapid quotient

Use091's algebra object

$$
A=R[\epsilon,\epsilon^{-1}]
=\bigoplus_{m\in\mathbb Z}R\epsilon^m.
\tag{114.3}
$$

At scalar dimension zero its evaluated family is exactly $\sum_m c_m\epsilon^m$. The admitted scalar source stages and Laurent closure of108 give a map $A\to\mathcal P_0\to\mathcal Z_0$. No graph labels or extra scalar slots are involved.

**Lemma114.1.** The map $A\to\mathcal Z_0$ is a monomorphism in $\mathcal A$, on every profinite test. Its constant summand is(114.2).

**Proof.** By091's compactness in the abelian heart, a section of $A$ on a profinite test $T$ has one finite Laurent window with continuous real coefficient functions. Suppose its evaluated section maps to zero in(114.1). Lift to an extremally disconnected cover $S\to T$ on which the rapid image has an actual fixed-stage lift; compactness gives finitely many relevant stages there. Equality is equality of actual scalar curves.

At any point of $S$ a nonzero finite Laurent polynomial has a smallest exponent $m$ with nonzero coefficient. Its ratio to $\epsilon^m$ tends to that coefficient as $\epsilon\downarrow0$. Such a function cannot be $O(\epsilon^L)$ for every $L$. At arity zero every finite Sobolev order is just the absolute-value norm on $\mathbb R$; increasing a distribution order cannot hide this leading term. Hence every Laurent coefficient vanishes at every point of $S$. These are continuous real coefficient functions in a concrete finite-window source, so they vanish as a section. Descent along the cover proves zero on $T$.

This uses an extremally disconnected cover for the rapid-image lift, not projectivity of an arbitrary profinite free object. Point detection was used only for the concrete continuous scalar coefficients, not for arbitrary internal-Hom sections. It proves the kernel is zero on every profinite test, and hence the asserted monomorphism. $\square$

In particular $1$ and $\epsilon^{-1}$ are linearly independent actual classes. Positive powers such as $\epsilon$ survive as well: they vanish at finite physical evaluation but are not rapid to every order. The conclusion is therefore not limited to a pole-divergence example.

## 3. The scalar coefficient image and the real-linear splitting

The physical coefficient maps of108 give an actual liquid morphism

$$
F_0=\mathrm{CT}_{\mathrm{phys}}:
\mathcal Z_0\longrightarrow R,
\qquad F_0u=\mathrm{id}_R.
\tag{114.4}
$$

On(114.3) it extracts the coefficient of $\epsilon^0$. Its existence and continuity follow from the fixed-source uniform coefficient estimates, before image descent. It is not evaluation at a positive regulator and is not regulator-linear.

An intrinsic description clarifies how much of $\mathcal Z_0$ is being asserted. Let $\Lambda$ be the fixed set of physical exponent/logarithm labels occurring in105/108's admitted scalar index families. Put $J_0=\prod_{(r,l)\in\Lambda}R$ in the liquid heart. On each fixed source stage extend its coefficient list by zero outside its index family.108's actual coefficient uniqueness makes these maps compatible with source enlargements and equal evaluated families, giving a liquid map $\mathcal P_0\to J_0$. Define $\mathcal C_0^{\mathrm{coeff}}$ to be its actual image. Then

$$
\mathcal Z_0\simeq\mathcal C_0^{\mathrm{coeff}}.
\tag{114.5}
$$

Indeed a rapid scalar curve has all coefficients zero by uniqueness. Conversely, when every coefficient vanishes,108's uniform scalar remainder estimates give $|\partial_\epsilon^k f_\epsilon|=O(\epsilon^L)$ for every $k,L$. At a point there is no distinction between Sobolev orders; the fixed-order condition is automatic. This is precisely the rapid stage. On a profinite source lift, those estimates bound each rapid seminorm by finitely many source seminorms on the closed coefficient kernel, so they supply a continuous rapid-stage lift, not merely pointwise rapidness. Extremally disconnected descent proves the same kernel equality in the liquid heart and gives(114.5).

Only the actual coefficient image is asserted. This does not identify it with every formal array, assume realization of arbitrary index families, or use an ambient topology that admits escaping-index plots. The Laurent subobject of Lemma114.1 already suffices for the obstruction.

Put $K_{\mathrm{unit}}=\ker(F_0)$. The maps(114.2)–(114.4) give an explicit splitting in the heart:

$$
\mathcal Z_0\simeq R\oplus K_{\mathrm{unit}},
\qquad
z\longmapsto\bigl(F_0z,\ z-uF_0z\bigr).
\tag{114.6}
$$

There is a monomorphism

$$
A/R\hookrightarrow K_{\mathrm{unit}},
\qquad [a]\longmapsto a-uF_0a.
\tag{114.7}
$$

To see this in the heart, the coefficient-zero projection on $A$ splits its constant summand. Lemma114.1 is monic, and the composite to $K_{\mathrm{unit}}$ kills exactly that constant summand on every profinite test. Thus(114.7) is an actual subobject, not an assertion based solely on vector-space sizes. It contains the nonzero class of $\epsilon^{-1}$.

The splitting is real-linear only. For example $F_0(\epsilon)=F_0(\epsilon^{-1})=0$ but $F_0(\epsilon\epsilon^{-1})=F_0(1)=1$. Thus $F_0$ is not an algebra or regulator-module quotient. This refutes those particular stronger interpretations of $F_0$, not every imaginable real-valued algebra character.

## 4. Exact derived cone and the total-weight obstruction

**Theorem114.2 (unit comparison cone).** In $D(\mathcal A)$,

$$
\mathrm{Cone}(u)\simeq K_{\mathrm{unit}}[0]\ne0.
\tag{114.8}
$$

The cone has a split retract containing $A/R$ in degree zero. Therefore the canonical unit comparison is not a quasi-isomorphism. Moreover $R[0]$ and $\mathcal Z_0[0]$ admit no real-liquid quasi-isomorphism, even without requiring that it be the canonical unit map.

**Proof.** Use the cohomological cone with $\mathrm{Cone}(u)^{-1}=R$, $\mathrm{Cone}(u)^0=\mathcal Z_0$, and differential $u$. Projection to $K_{\mathrm{unit}}$ is $z\mapsto z-uF_0z$ in degree zero. Its inclusion is the kernel inclusion. The degree-minus-one homotopy is $h^0=F_0:\mathcal Z_0\to R$; all other components are zero. Then $dh+hd=\mathrm{id}-ip$, using $F_0u=1$. This is an explicit liquid cochain homotopy equivalence, so proves(114.8) without any projective-resolution assumption for $\mathcal Z_0$.

Nonzero follows from(114.7). For the stronger object statement, both complexes are concentrated in degree zero, so a quasi-isomorphism would be an isomorphism of heart objects. Applying the singleton section functor would give a real-linear isomorphism of their point modules. The monomorphism $R\oplus R\hookrightarrow\mathcal Z_0$ supplied by $1,\epsilon^{-1}$ contradicts the one-dimensional point module of $R$. This use of points detects the asserted impossible isomorphism; the actual liquid monomorphism was proved separately in Lemma114.1. $\square$

Now take111's completed quantum object, with nonnegative powers of $\hbar$ and $w=n+2k$. Its actual weight-zero complex is

$$
\widehat{\mathcal O}_{\mathcal Z}^{(w=0)}(U)
=\mathcal Z_0[0],\qquad Q_{w=0}=0.
\tag{114.9}
$$

There is only the possibility $n=k=0$. There are no odd slots for $d$ and no pair for $\Delta$. A contraction from arity two would carry a positive power of $\hbar$ and lie in weight two; reaching weight zero would require the forbidden negative quantum power. The total differential preserves $w$, so higher arity and higher weight cannot turn $\epsilon^{-1}$ into a weight-zero boundary. Product completion does not change that statement: projection onto weight zero and inclusion from it are actual chain maps splitting off this one factor.

The corrected026 scalar field comparison has unit sector $R[0]$. Any proposed nonnegative-quantum, total-weight-preserving extension retaining that actual unit has the same source weight-zero sector, without needing a new higher-weight quantum dressing theorem here. A strict weight-preserving quasi-isomorphism to111's model is impossible by Theorem114.2. For the decreasing total-weight filtration, the same contradiction rules out any comparison required to induce a quasi-isomorphism on the weight-zero associated graded.

No infinite-product exactness theorem is needed. Split each completed complex into its weight-zero factor and its tail, a finite binary splitting. A strict weight-preserving map and its cone split accordingly. If its full cone were acyclic, its weight-zero map would be a quasi-isomorphism, contrary to Theorem114.2's object-level conclusion. For a unit-preserving map its weight-zero cone is exactly(114.8). A merely filtered quasi-isomorphism that is not required to be an associated-graded equivalence, or an unfiltered map mixing weights, is not excluded by this argument.

## 5. Unit, scale and accepted-record controls

Arity zero is the number of field slots, not an assertion that the physical open is empty. The computation is on each nonempty interval $U$. The zero-fold tensor source of026 is the tensor unit even there. It is not $\mathcal D(U)$, $C^\infty(U)$, or a one-vertex physical kernel space. No choice of value at the empty open was needed. Prescribing an empty-open value or a unit map at that open cannot remove(114.8) on a nonempty interval.

On total weight zero the Wick operator and all accepted Wick scale transports are the identity: their arity-lowering contractions have no slots. Thus the classicalized quantum comparison $\mathrm{CT}_{\mathrm{phys}}W^{-1}$ of111 reduces exactly to $F_0$ here. Its nonzero kernel(114.7) prevents treating that cochain comparison as a strict weightwise equivalence.

Actual regulator rescaling fixes $1$ and sends $\epsilon^{-1}$ to $s^{-1}\epsilon^{-1}$ for $s>0$. It therefore preserves the nonzero Laurent obstruction. It need not preserve $F_0$ on logarithmic zero-power families:111's binomial logarithm formula can add a finite constant. The cone statement is invariant under the actual rescaling automorphism; if a splitting is transported, its retraction is transported as well. No claim of scalar finite-scale invariance beyond the log-free historical scope is made.

For an admitted finite record-scheme isomorphism $U_L$ of111, transport the full comparison diagram:

$$
u_L=U_Lu,\qquad F_L=F_0U_L^{-1}.
\tag{114.10}
$$

Then $F_Lu_L=1$ and $\mathrm{Cone}(u_L)\simeq\mathrm{Cone}(u)$. This is invariance under the accepted change of record coordinates carrying the actual unit. It does not silently identify $F_L$ with the finite value of a changed remainder when $L(1)\ne0$. The default087 scheme is unchanged. A new model, a different coefficient object, or an operator correction changing the comparison problem is outside this invariance claim.

The comparison also does not use the original R3 objects $H,G_b,G$, any syzygy, or degree-two Ext continuity. $K_{\mathrm{unit}}$ is only the kernel in(114.6), with no relation to R3's reserved kernels. No higher-Ext result is inferred from the split unit calculation.

## 6. Exact limit of this return and next mathematical obligation

This return computes one actual M5 cone and proves one sharply typed obstruction. The accepted enriched model is not a weight-preserving replacement of the corrected scalar-field unit while both retain the coefficient choices just stated. Treating the physical finite map as a quasi-isomorphism would lose the actual Laurent and other coefficient data already retained by108/111.

It does not establish that no useful comparison arrow exists. The unit itself is a natural split injection and $F_0$ is a real-linear retraction. Nor does it rule out a separately specified coefficient enlargement, a genuinely different quotient, or an unfiltered equivalence; none is constructed or authorized as a replacement objective here. The original REACH goals and accepted R0/R1/R2 scopes are preserved.

The ambient category is real liquid, whereas091's completed composition was relative to $A$ and had $\Phi_0=A$. The present cone obstructs a direct comparison with the fixed real-scalar unit; it does not obstruct the existence of a unital real-algebra object or every comparison relative to a declared larger coefficient algebra. Replacing026's scalar target by $A$ or $\mathcal Z_0$ would be a separate base-change theorem requiring actual completed tensor, derived and parameter-family checks. No flatness or comparison equivalence for that change is inferred here.

The precise next lemma beyond the unit sector is an actually typed comparison among the corrected scalar field dual, the admitted R1 complex and111's enriched quantum complex, with the chosen coefficient objects and filtration explicit. A constant-family R1 map is not automatically a quantum cochain map: its regulated contraction can differ from the constant zero-scale contraction by terms that are small but not rapid. A proposed Wick-dressed map must therefore have its domain, graph-parameter smoothness, naturality, filtration shifts and quantum intertwining proved separately. Such a theorem would still inherit the weight-zero cone above if it transports the same unit. It is not supplied in this return.

Full M5 also still requires the actual smooth/connection, support, cofibration/fibration and completed extended Weiss comparisons or their correctly typed obstructions. This one cone does not adjudicate all of R4. Original R3 and both parent objectives remain open. No source is reopened merely because this new comparison fails.

This is one primary bounded attempt by a delegated same-system construction context, with substantive typing and cone checks from the parent. Distinct non-author115 must assess the exact frozen source before acceptance. There is no numerical fixture: the assertions are liquid monomorphisms, scalar remainder estimates and an explicit cochain contraction. No Python, Git, tracker, protected admission or external mutation was performed in preparing this draft; those subsequent custody and validation obligations are separate.
