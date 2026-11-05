# EXT-015 REACH / 147 — the full diagonal-jet contribution at weight two

**Disposition.** This primary candidate constructs an intrinsic split cochain projection onto all finite diagonal jets of the actual two-slot class. Its graded symmetric diagonal complex has cohomology equal to three copies of the retained scalar object in degree zero. These give a split summand of the scalar-relative weight-two comparison cone. The complementary cone is not computed. Distinct nonauthor review and protected admission remain pending.

## 1. Contract, category and inputs

Work in ZFC, in the real liquid heart $\mathcal A=\mathrm{Liq}_p(\mathbb R)$ for fixed $0<p\le1$, on the existing one-dimensional model. Let $U$ be a nonempty open interval. Use the actual mixed source image $\mathcal P_n(U)$ and its quotient $\mathcal Z_n(U)$ by the uniform finite-order rapid relation of 108. Use the source-controlled parameter rows of 126 for the separate differentiable assertion. The scalar algebra is $\mathcal C$ of 135 and 141. No analytic source, finite normalization or counterterm is changed.

CP165 binds the input cut 36f99a5fc0e9da839d779ce3b20264dda48ce141 on research/reach-diagonal-jets-input-frozen-20261105. The 88-input manifest has SHA256 41836d165a10d28329b37e02e49dcbcd6aac9c3c57a7b1bace1ebee003175bf0. It includes the 82 scientific sources read back after 144–146. The immediate dependencies are [108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md), [111](RENORMALIZED_QUANTUM_STRUCTURE_111.md), [117](R1_WICK_DRESSED_QUANTUM_COMPARISON_117.md), [126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md), [135](SOURCE_CONTROLLED_COMPLETED_WEISS_135.md), [141](SCALAR_RELATIVE_WEIGHT_ONE_COMPARISON_141.md) and [144](SCALAR_RELATIVE_WEIGHT_TWO_COMPARISON_144.md), with their admitted reviews and ledgers.

Write $M(U)=\mathcal Z_1(U)$ for the underlying one-slot coefficient object, without its two-term field differential, and $T=\partial_x$ on this coefficient object. Set

$$
x=\frac{x_1+x_2}{2},\qquad z=x_2-x_1,\qquad
A=\frac{T}{2}-\partial_z,\qquad B=\frac{T}{2}+\partial_z.
\tag{147.1}
$$

The coordinate Jacobian has absolute value one. Thus $a(x)\delta_0(z)$ means the diagonal pushforward of the actual one-slot density $a$, with no missing density factor. In polynomial notation $u^j a$ will mean $a(x)\delta_0^{(j)}(z)$; there is no factorial in this convention.

**Theorem 147.1.** The full labelled two-slot classical coefficient complex admits a split cochain projection to

$$
K_\Delta(U)=
\left(M(U)[u]\otimes\Lambda(e_1,e_2),
\ (T/2-u)^2\iota_1+(T/2+u)^2\iota_2\right),
\qquad |e_i|=-1 .
\tag{147.2}
$$

Here $M[u]=\bigoplus_{j\ge0}M u^j$ is the polynomial object, with finite degree on cover-local source lifts. The projection commutes with slot exchange, which sends $u$ to $-u$, exchanges $e_1,e_2$, and fixes $x$. Let $K_\Delta^{\mathrm{sym}}$ denote the invariant complex for this graded action. Then

$$
H^i(K_\Delta^{\mathrm{sym}})=
\begin{cases}
\mathcal C^{\oplus3},&i=0,\\
0,&i\ne0.
\end{cases}
\tag{147.3}
$$

The projection annihilates the entire ordinary scalar pairing with the R1 two-slot complex. Consequently the actual derived comparison of 144 has a cone with split summand $K_\Delta^{\mathrm{sym}}\simeq\mathcal C^{\oplus3}[0]$. Its remaining summand is left uncomputed. At each fixed profinite test the corresponding source-controlled differentiable module-sheaf complexes have the separate projection and cohomology statement, compatible with their flat parameter connection.

## 2. Center-valued normal regularity for distinct-block histories

Take one fixed finite collection of complete sources 108.7. At positive regulator, each source has compact support in a fixed subset of $U^2$. It suffices to work in the coordinates (147.1) after extending by zero outside this compact physical support. All cutoffs below are fixed and independent of the regulator and the parameter. Each requested regulator or mixed parameter derivative is treated as the derivative of the whole source before choosing any test.

Transfer outer physical derivatives through the final projection. A forgotten-coordinate derivative gives zero; the two retained derivatives become $A,B$. If the retained labels lie in the same partition block, forgetting the other vertices gives an actual one-slot family $a_\epsilon(x)$. The derivative transfer expands into a finite sum of $T$ derivatives of that family times finite derivatives of $\delta_0(z)$. These coefficient maps are continuous maps of complete sources to finite one-slot sources. Their scalar index families, geometry and finite derivative lists are fixed independently of the relaxed coefficient orders in a parameter row.

Suppose instead that the two labels lie in distinct blocks. Before derivative transfer the map from block coordinates to $(x,z)$ is a surjective linear map on those two coordinates, followed by forgetting the remaining vertices. At $z=0$, the pullback of a nonzero pure normal covector $(0,\zeta)$ is the opposite-covector pair on those blocks and zero elsewhere. It is forbidden by the R1 partition-conormal condition, also where other blocks coincide. Proper pushforward on the fixed source compact therefore gives an output wavefront cone avoiding the pure normal directions over $z=0$. The output cone can be chosen closed: restrict to the fixed source compact and use the injective linear transpose on the retained coordinate pair. On the corresponding compact unit covectors, closure and avoidance give a common strip $|z|<\eta$ and a constant $C_0$ such that the localized cone satisfies

$$
|\zeta|\le C_0|\xi|,
\tag{147.4}
$$

where $\xi$ is the center frequency. If the compact support does not meet $z=0$, choose a strip disjoint from it. Multiply by a compact product cutoff equal to one on the required smaller strip and center support. The existing complete source estimates supply a global finite distribution-order bound and rapid Fourier decay off this cone, with a finite inverse regulator power for each requested seminorm.

Here is a precise consequence needed below; it is weaker than smoothness jointly in $(x,z)$. The localized distinct-block output $v_\epsilon$ can be written on a smaller strip as a distribution-valued smooth function $g_\epsilon(z)$ in $x$. For each fixed number $k$ of normal derivatives there is a finite $r_k$, independent of the desired rapidness power, with

$$
\sup_{|z|<\eta/2}
\|\partial_z^k g_\epsilon(z)\|_{H^{-r_k}_x}
\le C_k\epsilon^{-N_k}.
\tag{147.5}
$$

The constants are bounded by finite seminorms of the fixed complete source, and the same assertion holds for each fixed mixed derivative uniformly on admitted compact parameter sets.

To prove it directly, use the Fourier transform in both variables. A compact-support distribution estimate gives

$$
|\widehat v_\epsilon(\xi,\zeta)|
\le C\epsilon^{-N}(1+|\xi|+|\zeta|)^q
\tag{147.6}
$$

for a finite $q$ and a finite source seminorm. Outside a slightly larger cone than (147.4), each chosen Fourier decay order has its own finite source bound and regulator loss. Invert only the $\zeta$ Fourier transform. Inside $|\zeta|\le C_1(1+|\xi|)$, the integral with factor $\zeta^k$ is bounded by a constant times $(1+|\xi|)^{q+k+1}$. Outside that region choose an off-cone decay order larger than $k+2$; its integral converges and has a polynomial bound in $\xi$, with a finite regulator loss. Choose $r_k$ larger than the resulting polynomial degree plus one. The weighted squared integral in $\xi$ converges, uniformly in $z$. Dominated convergence using one more such derivative bound proves continuity and differentiability in successively weaker finite Sobolev spaces. This proves (147.5) with finite seminorm bounds. In particular $k=0$ requires just one fixed finite center order.

The fixed-cone source continuity used here is the normal topology, together with the graph refinements of 108 and 117. Proper pushforward and exterior tensoring with a fixed compact distribution are supplied by [Brouder–Dang–Hélein, Theorems 6.3 and 4.6](https://arxiv.org/pdf/1409.7662). Those theorems are used with compact supports and the stated cones. The regulator and completed-coefficient estimates come from 108; they are not conclusions about arbitrary distribution families from wavefront avoidance alone.

All estimates extend to the completed coefficient stages because each target bound uses finitely many source seminorms. Outer derivatives only request finitely many additional orders. Adding the finite histories yields, near the diagonal,

$$
v_\epsilon(x,z)=g_\epsilon(x,z)
+\sum_{j=0}^{m}a_{j,\epsilon}(x)\delta_0^{(j)}(z),
\tag{147.7}
$$

where $g$ satisfies (147.5), and each $a_j$ belongs to the actual one-slot positive source image. The jet order $m$ is fixed by the finite histories, not by a regulator value. This statement allows singular center distributions.

## 3. Intrinsic extraction and uniform rapid descent

The finite jet in (147.7) is unique. Choose $\chi\in C_c^\infty(\mathbb R)$ equal to one near zero, and put

$$
p_{j,h}(z)=\frac{(-1)^j}{j!}z^j\chi(z/h),\qquad 0<h\le1.
\tag{147.8}
$$

Its pairing with $\delta_0^{(l)}$ is exactly $1$ for $l=j$ and $0$ for every other $l$, including all $l>j$. Pair (147.7) with $\psi(x)p_{j,h}(z)$. The smooth-in-normal-variable term has absolute value at most

$$
C h^{j+1}\epsilon^{-N}\|\psi\|_{H^{r_0}_x}.
\tag{147.9}
$$

For a fixed positive regulator it tends to zero as $h\to0$. Thus actual equality of whole kernels determines each $a_j$ by all its center test pairings. This also proves that a distinct-block contribution cannot hide a nonzero diagonal jet.

The extraction on any finite source sum is the finite sum of the same-block coefficient maps in §2, with zero on the distinct-block terms. These are continuous maps to finite actual one-slot sources. Uniqueness makes them independent of the chosen history, including relations between completed coefficients. On profinite tests use the cover-local complete source lifts of 108 and 126. Equality in the positive envelope gives equality of the actual coefficient pairings on these concrete lifts. The maps therefore descend to the actual positive image. This argument does not test arbitrary quotient sections by their points.

Now let one derivative of the whole input be rapid in a fixed $H^{-t}_{x,z}$, and increase $t$ to a nonnegative integer if needed. Insert a fixed compact cutoff equal to one near all supports. Differentiating the product test in (147.8) gives

$$
\|\theta(x,z)\psi(x)p_{j,h}(z)\|_{H^t_{x,z}}
\le C_{t,j}h^{-t}\|\psi\|_{H^t_x}.
\tag{147.10}
$$

This deliberately coarse bound suffices. Take $r=\max(t,r_0)$, with the same fixed center support cutoffs. The dual bound from (147.9)–(147.10) is

$$
\|a_{j,\epsilon}\|_{H^{-r}_x}
\le C\left(h^{-t}\|v_\epsilon\|_{H^{-t}_{x,z}}
+h^{j+1}\epsilon^{-N}P(v)\right),
\tag{147.11}
$$

where $P(v)$ denotes a finite fixed source seminorm bound for the moderate smooth part. For a desired output decay power $L$, choose an integer $b$ with $b(j+1)>N+L$, put $h=\epsilon^b$ for sufficiently small regulator, and request the input rapid seminorm of power $L+bt$. The output is $O(\epsilon^L)$ in the same $H^{-r}_x$. The order $r$ depends on the fixed input source and this derivative request, but not on $L$. The remaining compact positive-regulator range is controlled by source seminorms.

Apply this to each differentiated whole source before choosing $h$. Extraction commutes with actual regulator and parameter derivatives because its source maps do, and uniqueness identifies the resulting coefficients. Thus no derivative of a moving test is being discarded. On a lifted source/rapid intersection, each output rapid seminorm is bounded by finitely many source seminorms and one input rapid seminorm. This proves continuous descent to the actual rapid subobject, including cancellation between arbitrary histories. Compact profinite coefficient sets and compact parameter sets have the uniform bounds used in (147.11).

Conversely the insertion $a\mapsto a(x)\delta_0^{(j)}(z)$ preserves rapidness with a fixed finite Sobolev loss. For compact center support its Fourier transform is $(i\zeta)^j\widehat a(\xi)$. If $s>j+1/2$ and $s\ge t+j+1/2$, integration in $\zeta$ bounds its $H^{-s}_{x,z}$ norm by a constant times the $H^{-t}_x$ norm of $a$. Increasing $s$ strictly if necessary gives the same bound for every rapidness power. Finite sums and all mixed derivatives obey these bounds.

Define the diagonal insertion $I:M[u]\to\mathcal Z_2^{\mathrm{lab}}$ using the retained-label duplication in a source history and the finite normal derivatives. Duplication puts the two external labels in the same existing partition block; it does not multiply distributions. Its coefficient maps are continuous on complete sources. Extraction defines $P$ in the other direction, and the preceding estimates show

$$
PI=1.
\tag{147.12}
$$

The polynomial description refers to the coproduct object, equivalently the filtered colimit of its finite partial sums. The abelian compactness of free profinite liquid modules in 91.2 gives the finite-degree assertion on profinite sections; cover-local coefficient lifts are then used for the source and quotient maps. No projectivity of a general profinite test is inferred. Allowing arbitrary fixed finite decorations does not admit infinite jet sums or an escaping-degree ambient plot. The same coefficient estimates establish the identification with this coproduct through actual images and rapid quotients. [Finite-stage argument 91.2](LIQUID_PROFILE_RECORD_BRIDGE_091.md)

For the parameter object, apply the fixed finite coefficient maps to the genuine rows of 126. Their output scalar indices and geometric histories do not change when the row Sobolev orders are relaxed. The pairing identity and (147.11) preserve equality of entire evaluated rows and their uniform rapid relations. After taking the actual image, quotient and parameter sheafification, $P,I$ act on the source-controlled sheaves at each fixed profinite test and commute with the flat parameter connection. No full prior-family recovery or general interchange with derived evaluation is used.

## 4. The diagonal complex and scalar comparison

Both physical derivatives preserve the decomposition (147.7): they differentiate the smooth-normal term within that class, and act on the finite jets by $T/2-u$ and $T/2+u$. Hence $P,I$ intertwine the actual labelled classical differential with (147.2), including its exterior signs. Reflection in $z$ gives the slot-exchange action stated in §1, so the maps descend through graded symmetrization. Since $2$ is invertible over the real scalar unit, invariants and coinvariants are identified by averaging, and this operation is exact.

For a scalar-extended R1 two-slot input there is only a distinct-block source. The underlying R1 coefficient avoids the diagonal conormal, and multiplying by an actual regulator scalar does not add a physical singularity. Its diagonal extraction is therefore zero. This is an identity of the actual bilinear pairing into the labelled complex and then its symmetric part. By tensor adjunction it annihilates the ordinary tensor comparison. The derived comparison of 144 factors through this ordinary cochain pairing, so its diagonal projection is zero without a flatness or t-exactness assumption.

In the labelled and symmetric categories let $Y=\ker P$. Equation (147.12) gives the actual cochain decomposition

$$
Z_2=K_\Delta\oplus Y,
\tag{147.13}
$$

with symmetrization understood for the unlabelled model. The ordinary comparison factors through $Y$, hence so does its derived-to-ordinary composite. Its cone is the direct sum of $K_\Delta$ and the cone of this factored map. These are actual maps, not a decomposition inferred from only the vector-space cohomology.

Use the scalar-linear Wick conjugation from 144 to transport these maps to total quantum weight two. The other summand is the $\hbar$ scalar comparison, which is an isomorphism after scalar extension. Thus it contributes zero cone. No positive-scale identity is being transferred through an unproved zero-scale quotient: the operations used here already act on the admitted enriched quotient.

## 5. Higher compact center primitives on the actual coefficient object

For $k=1,3$ define the moment map

$$
m^{(k)}(a)=
\bigl(\langle a,1\rangle,\ldots,\langle a,x^{k-1}\rangle\bigr)
\ \in\mathcal C^{\oplus k}.
\tag{147.14}
$$

These are actual scalar curves by smooth decoration and all-vertex forgetting, with the same whole-source scalarization estimates as 141.3. They preserve the rapid relation by fixed compact test bounds and have fixed output scalar indices across parameter rows.

Choose compact smooth bumps $b_i$ with these moments equal to the standard basis and write $b^{(k)}(c)=\sum_i b_i c_i$. Such bumps can be obtained by an invertible triangular change among $\rho,\rho',\rho''$ for a compact $\rho$ of integral one. With $\mu_i=\langle\rho,x^i\rangle$, for $k=3$ one explicit choice is

$$
b_0=\rho+\mu_1\rho'+(\mu_1^2-\mu_2/2)\rho'',\qquad
b_1=-\rho'-\mu_1\rho'',\qquad b_2=\rho''/2.
\tag{147.15}
$$

For $k=1$ take $b_0=\rho$. Let $e_k(t)=t_+^{k-1}/(k-1)!$, with $e_1$ the Heaviside distribution. Its derivative of order $k$ is $\delta_0$. The operator

$$
h_k(a)=e_k*\bigl(a-b^{(k)}m^{(k)}(a)\bigr)
\tag{147.16}
$$

has support in the convex hull of the input and bump supports, compactly inside $U$. To the left the kernel vanishes, and to the right it is a polynomial of degree $k-1$ whose pairings vanish. Distributional convolution gives

$$
T^k h_k=1-b^{(k)}m^{(k)},\qquad h_kT^k=1.
\tag{147.17}
$$

The whole-source membership proof of 141.4–141.6 applies with these kernels as follows. Reduce every retained outer derivative to the common translation coordinate of its entire block history. In a compact product atlas the collision heat geometry depends only on relative variables. Choose fixed cutoffs $\chi$ in the center and $\kappa$ on the translation line so that $k_0=\kappa e_k$ agrees with $e_k$ on all required differences. Then $k_0\in L^1$ and its center convolution followed by $\chi$ is bounded on each fixed global negative Sobolev space. The normal-topology tensor/pushforward argument of 141.4 has exactly the same covector relation for this fixed compact kernel. Its enclosing cone consists of common-center translates of the input cone, and continues to exclude all partition conormals.

For a scalar coefficient depending on center and relative variables, Fourier-expand only its center dependence in that fixed product atlas. Each Fourier coefficient decays faster than every fixed power in every requested scalar-stage seminorm, by repeated integration by parts in the tangential center coordinate. Multiplication of the R1 coefficient by a cutoff mode has at most polynomial growth in every requested graph seminorm. The just-proved continuous convolution preserves that estimate. Their product is summable in the completed projective source stage, using a Fourier decay order larger than the graph growth order plus two. The relative scalar indices, support and finite histories remain fixed. The evaluated sum equals convolution of the entire source, since the relative scalar factors commute with center convolution. Forgetting the other vertices commutes with it by the compact distributional pairing. Rehost in $U$ by 135.1, as in 141, and subtract the smooth finite-rank moment corrections. This constructs (147.16) in the actual one-slot source class.

This argument uses the properties just checked for each $e_k$; it does not assume closure under arbitrary relative primitives. On any fixed support (147.16) is the sum of a truncated $L^1$ convolution bounded in $H^{-t}$ and finitely many smooth output factors paired with fixed compact tests. Thus

$$
\|h_k(a)\|_{H^{-t}}\le C_t\|a\|_{H^{-t}}
\tag{147.18}
$$

after the usual fixed cutoffs. It commutes with regulator and parameter derivatives, respects whole evaluated equality, and preserves uniform rapidness at the same order for each derivative. The continuous complete-source maps act on the genuine parameter rows with fixed history and scalar choices. These facts establish (147.17) on the actual liquid quotient and separately on the fixed-test differentiable sheaves.

In particular $T$ and $T^3$ are monomorphisms of the actual coefficient object, and

$$
M/T^kM\cong\mathcal C^{\oplus k},\qquad k=1,3.
\tag{147.19}
$$

The quotient identification is by (147.14), with the explicit local lifts supplied by $h_k$. It is not an inference from pointwise cohomology.

## 6. Monic reduction, signs and the three surviving quantities

Put $N=M[u]$, $f=(T/2-u)^2$ and $g=(T/2+u)^2$. Division by the monic polynomial $f$ is a finite triangular algorithm in each polynomial degree, using only powers of the admitted operator $T$. It is therefore a continuous finite source construction on each lift and gives

$$
N/fN\cong M\oplus uM,\qquad u^2=Tu-T^2/4.
\tag{147.20}
$$

Multiplication by $f$ is injective: the leading coefficient of a finite polynomial is unchanged in its highest output degree. Modulo $f$, $g=2Tu$, and its map on (147.20) is

$$
(a,b)\longmapsto
\left(-T^3b/2,\;2Ta+2T^2b\right).
\tag{147.21}
$$

Its kernel is zero by the monomorphisms in (147.19). Replacing the input coordinate $a$ by $a+Tb$ shows that its image is $T^3M\oplus uTM$, with harmless nonzero real factors. Thus the labelled Koszul complex has

$$
H^0(K_\Delta)\cong(M/T^3M)\oplus u(M/TM)
\cong\mathcal C^{\oplus3}\oplus\mathcal C,\qquad
H^{-1}(K_\Delta)=H^{-2}(K_\Delta)=0.
\tag{147.22}
$$

For explicit exactness in degree minus one, a cycle $(a,b)$ satisfies $fa+gb=0$. Injectivity of $g$ on $N/fN$ implies $b=fc$; monic division constructs $c$ on a cover-local finite lift. Then $a=-gc$, and $(a,b)=d(c e_1\wedge e_2)$ with the convention $d(c e_1\wedge e_2)=(-gc,fc)$. Degree minus two uses injectivity of $f$. Degree-zero lifting uses the finite divisions and the actual moment primitives (147.17). All these constructions exist on finite coefficient lifts in the liquid heart and on the parameter rows, so the categorical exactness is proved rather than assumed from arbitrary-profinite projectivity.

In the joint quotient by $f,g$ one also has $Tu=0$ and $u^2=-T^2/4$. Hence reflection fixes the $M/T^3M$ term and negates the $u(M/TM)$ term. Exact averaging kills the latter in the graded symmetric complex and proves (147.3).

The three scalar detectors have a particularly simple formula. For the extracted finite jet $\sum_j a_j u^j$, in degree zero set

$$
\nu_0=m_0(a_0),\qquad
\nu_1=m_1(a_0),\qquad
\nu_2=m_2(a_0)-\frac12m_0(a_2).
\tag{147.23}
$$

Set them to zero on the negative degrees. Polynomial reduction proves these are cochain maps; alternatively expand $f,g$ and use $m_l(Ta)=-l\,m_{l-1}(a)$. Terms of degree at least three in $u$ give zero in (147.22). On labelled degree zero the fourth detector is $m_0(a_1)$ and is odd under exchange. The section for the three even detectors is $\sum_{i=0}^2b_i c_i$ in normal degree zero, with the bumps of (147.15). It has composite identity with (147.23), and (147.22) proves the detector is a quasi-isomorphism on the whole symmetric diagonal complex.

The first detector is exactly the integrated delta-mass detector of 144. The new information consists of its first center moment and the corrected second moment. They are independent retained scalar classes, not merely three real numbers obtained by finite extraction. For instance every scalar Laurent class can multiply each bump section.

Combining (147.13), (147.22) and the Wick reduction gives the claimed split $\mathcal C^{\oplus3}[0]$ in the actual derived comparison cone. At fixed profinite test the same formulas and exact constructions give $\mathbf C(-)(S)^{\oplus3}[0]$ for the diagonal differentiable complex with connection. This is a separate calculation on actual module sheaves; no evaluation of a liquid-derived tensor is interchanged with a differentiable construction.

## 7. Hostile controls, limitations and return conditions

- All finite normal derivatives are retained before taking cohomology. For $\rho(x)\delta_0''(z)$ with mass-one $\rho$, the second detector is $-1/2$. Indeed its class equals that of $-\rho''(x)\delta_0(z)/4$. Omitting the transverse second derivative from (147.23) would fail on a genuine boundary.
- The labelled calculation has four scalar classes. Graded slot exchange removes precisely the odd relative first-derivative class. The wedge sign in degree minus two is included in the cycle calculation; an ungraded symmetrization is not substituted.
- A smooth-in-normal-variable regulator mollifier has every diagonal coefficient zero, even if its distributional limit is a delta. Equation (147.11) prevents identifying it with the nonzero diagonal section by the actual rapid relation.
- The normal-regular remainder is allowed to be singular in the center. Joint smoothness is neither required nor asserted. Fixed cone avoidance and finite-order source bounds are essential for the uniform estimate.
- Completed coefficients and cancellations between histories are checked before quotienting. An infinite normal-jet series or a family escaping every finite source stage is not inserted into the polynomial object.
- The center primitives use compact interval hulls. No componentwise cohomology claim on arbitrary disconnected opens is inferred. Support extension between nonempty intervals respects extraction and the global moments; the compact bump choices and primitive homotopies need not themselves be natural.
- The maps are scalar-linear and commute with the actual parameter connection. They do not prove that every prior retained smooth family has the source-controlled witnesses of 126.14, or establish a general derived tensor-evaluation comparison.

One primary construction is presented. The substantive analytic claims are the center-valued normal estimate, the fixed-order coefficient extraction on the rapid intersection, and the complete-source extension of the compact primitives. The standalone exact [algebra fixture](fixtures/check_diagonal_jet_algebra_147.py) checks the Koszul identities, monic reduction matrix, reflection and detector controls using rational arithmetic. It supplies no infinite-dimensional conclusion. Distinct critical review must check the analytic arguments and rederive the finite algebra against the frozen inputs.

The complementary weight-two cone, higher weights, full prior-family recovery, actual sequence and kernel lifting, the remaining derived and multiplicative comparisons, original R3, full M5/R4 and both parent objectives remain open. R0, R1, R2 and the fixed-host procedure retain their admitted scopes.
