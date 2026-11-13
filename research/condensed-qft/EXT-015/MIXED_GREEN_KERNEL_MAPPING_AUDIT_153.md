# EXT-015 REACH / 153 — mixed Green-kernel mapping-input audit

**Disposition: bounded positive microlocal lemma; 150.L NOT PROVED.** This is a *primary, unreviewed* mathematical return. The positive theorem below shows that the existing compact Green primitive preserves exclusion of pure diagonal conormals at every fixed positive regulator, with finite normal-topology estimates on fixed compact/conic stages. The augmented Green-kernel product is an unambiguous ambient distribution, but neither observation supplies a representative in the existing complete mixed source image. No completed-liquid equivalence, residual acyclicity, original R3 or REACH integration is asserted. Distinct nonauthor mathematical review and protected admission are pending.

## 1. Locked question and exact dependencies

The governing question is [150.L](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md): does the compact partial Green primitive of every *distinct-retained-block* 108.7 history have a **finite representation in the existing** mixed source histories, with one fixed choice of supports, R1 cones, scalar index families, normal jets, proper densities, completed coefficients, and all mixed parameter-row estimates?

Keep ZFC, fixed real $\mathrm{Liq}_p(\mathbb R)$, $0<p\leq1$, the existing one-dimensional physical model, complete source image $\mathcal P_2$ of [108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md), quotient $\mathcal Z_2$, and parameter rows of [126](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md). In particular, no enlargement of the source category or counterterm prescription is authorized. No prior accepted scientific assertion is reopened.

| Source | Protected Git blob, checked on current main |
| --- | --- |
| [105: heat geometry/scalar stage](GAUSSIAN_WICK_COLLISION_NORMAL_FORM_105.md) | `a8ce66ff0edec33e2aff299550fca2089d671033` |
| [108: complete mixed source](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md) | `587c15fd6e24f6e6b14de574ff878221cdbd5cb6` |
| [126: combined parameter rows](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | `5b05c6147d237ca1d22e4dcbce9262b0f038c163` |
| [147: diagonal jet splitting](WEIGHT_TWO_DIAGONAL_JET_COMPARISON_147.md) | `89b3d4a835f3750114e983854585e33d8184cb1f` |
| [150: residual cone and proposed primitive](COMPLEMENTARY_WEIGHT_TWO_COMPARISON_150.md) | `03deca9212a9bea56743e482e5cb79edb46b9d7f` |
| [151: corrected-source nonauthor review](AGENT_CRITICAL_REVIEW_COMPLEMENTARY_WEIGHT_TWO_151.md) | `222424fd3a3d9b49d4268120f24958512c3c5bfe` |

The protected [checkpoint CP183](../../governance/bounded_operation_checkpoints/EXT-015-REACH-COMPLETION-001.json) has blob `dbc63f10ca6f0723be3da0bf5f65e44c4e512859`. The preserved `research/reach-green-mapping-input-frozen-20261107` input ref and `research/reach-green-mapping-20261107` CP186 attempt are provenance; the latter has not been protected-admitted and contains no 153 manuscript. Current-main scientific blobs above agree with the prior accepted results. This note does **not** assert that the unavailable CHAD live validator ran.

## 2. Positive fixed-regulator microlocal theorem

Let $U\subset\mathbb R$ be an open interval; fix a compact set in $U^2$ and normalized bumps $b_0,b_1\in C_c^\infty(U)$ with
$

\int x^j b_k(x)\,dx=\delta_{jk}\quad(0\leq j,k\leq1).

$
For $i=1,2$, define $m_{i,j}$, $B_i=\sum_j b_j(x_i)m_{i,j}$, and
$

e(t)=\frac{|t|}{2},\qquad h_i v=e*_{x_i}(1-B_i)v,\qquad D_i=\partial_{x_i}^2.

$
These are exactly (150.3), with ordinary physical density, and $D_i h_i=1-B_i$. The subtraction gives compact output support inside the hull of the input and bump supports.

Write $\Delta=\{x_1=x_2\}$ and
$

N^*\Delta\setminus0
=\{(x,x;\tau,-\tau):\tau\neq0\}.

$

**Proposition 153.1 (positive-regulator noncreation of diagonal conormals).** If $v\in\mathcal E'(U^2)$ has
$

\mathrm{WF}(v)\cap(N^*\Delta\setminus0)=\varnothing,

$
then each compactly normalized $h_i v$ also has no wavefront on $N^*\Delta\setminus0$. On fixed compact supports and fixed closed input wavefront cones disjoint from this conormal, every localized output *normal-topology* seminorm in a sufficiently small conic neighborhood of $N^*\Delta$ is bounded by finitely many input normal seminorms and one global negative-Sobolev norm. Cutoffs, conic neighborhoods, and constants can be fixed across a parameter/regulator family whose input occupies the specified fixed stage. Each fixed mixed derivative obeys the corresponding finite estimate, but this proves no asymptotic scalar-stage closure.

**Proof.** All moment maps are proper distributional projections with a fixed smooth test in $x_i$. Thus $B_iv=\sum_jb_j(x_i)m_{i,j}v$ is smooth in $x_i$ with distribution coefficients in the other variable, and every nonzero covector of $B_iv$ has $x_i$-component zero. It cannot meet $N^*\Delta\setminus0$, where the $x_i$-component is necessarily nonzero.

By (150.4), $D_i h_iv=(1-B_i)v$. The operator $D_i$ is microlocally elliptic at **every** covector in $N^*\Delta\setminus0$, since its principal symbol there is $-\tau^2\neq0$. Microlocal elliptic regularity implies
$

\mathrm{WF}(h_i v)\cap(N^*\Delta\setminus0)
=\mathrm{WF}(D_i h_i v)\cap(N^*\Delta\setminus0)
=\varnothing.

$
This is a statement about the *output wavefront*, not about admissibility of the intermediate Green factor.

For the quantified version choose compact spatial cutoffs and a closed conic neighborhood of the target conormal avoiding the fixed input wavefront cone and the $\xi_i=0$ covectors of $B_i v$. A fixed microlocal parametrix for $D_i$ gives an output Fourier/normal seminorm bounded by finitely many input off-cone seminorms plus a lower-order global distribution seminorm of $h_iv$. The latter is controlled by (150.6), whose constant depends on the common compact supports/bump choices but not on the regulator or requested rapidness order. Applying the same fixed operators to each parameter/regulator derivative is legitimate because $h_i,B_i$ have no parameter dependence. The finite-loss bound holds for each derivative request on its fixed input stage. None of these estimates identifies an element of $E_{s,K,\Gamma}\widehat\otimes_\pi S_\lambda$ after the **full** mixed history projection. $\square$

**Corollary 153.2 (no positive-scale jet obstruction from the primitive).** Every distinct-retained-block output of 108.7 has the pure-normal avoidance of 147.4 at each fixed positive regulator. Applying $h_i$ in the ambient compact distribution space preserves that avoidance. Consequently any eventual source-admissible representative of this primitive could not acquire a nonzero intrinsic pure diagonal delta-jet contribution. This does not define the extraction map $P$ on a nonadmitted ambient kernel, nor prove that $h_i$ acts on $Y=\ker P$. The actual completed source lift and its zero-scale bounds remain the entire issue.

The same-block hostile input $\rho(x_2)\delta(x_1-x_2)$ of (150.15) **does not satisfy** the proposition's wavefront hypothesis and retains its genuine cusp obstruction. Thus the proposition does not inadvertently erase the accepted nonzero diagonal cone.

## 3. What an augmented Green edge does and does not permit

Let $T(y,z)$ be a compact R1 distributional coefficient on old block variables and $a_\epsilon$ a smooth scalar coefficient at a **fixed** $\epsilon>0$. Introduce a new output coordinate $x$, and consider the formal integrand
$

K_\epsilon(x,y,z)=\chi(x)e(x-y)\,a_\epsilon(y,z)\,T(y,z)

$
where $\chi$ is a fixed compact output cutoff. The original R1 factor pulls back with **zero** covector in the new $x$ direction, whereas every nonzero wavefront covector of $e(x-y)$ at $x=y$ has a nonzero $x$-component. Hence their wavefront sets contain no opposite pair. The Hörmander distribution product is well-defined at each fixed positive regulator. With compact support, its proper pushforward in $y$ is a well-defined ambient distribution.

**This ambient existence is not an admissible 108.7 source history.** The factor $e(x-y)$ is not smooth on the *positive-regulator interior* diagonal $x=y$. It therefore is not a scalar $S_\lambda$ coefficient of 105/108. If instead assigned to the R1 coefficient it has precisely a forbidden partition conormal on the newly introduced diagonal. The intermediate product is a legitimate distribution in an ambient enlarged space, not a product licensed by 108.4's typed operations. A finite source lift could still arise **after** integration, but neither product existence nor 105.4's ordinary b-fibration proves it.

The missing theorem is therefore not a distribution-product theorem. It is a **mixed pushforward/source-representation theorem**, uniform over the full augmented collision arrangement. It must account for:
1. the zero-width Green singularity at every positive-regulator intersection with old/retained/hidden vertices;
2. the actual physical density, jacobians, all simultaneous collision corners, and the resulting R1 output cones;
3. one fixed *finite* list of existing histories with allowed scalar index families, auxiliary weights, collision jets and completed coefficient stages; and
4. continuous source maps with finite seminorm bounds for every relaxed graph order and mixed derivative required by a true 126 parameter row, with actual equality of complete evaluated histories.

Existing 105.4 b-fibration geometry covers vertex forgetting in the established heat arrangement, not an enlarged class of interior conormal scalar factors. Existing 108.4 mixed closure allows specified legal operations and does not authorize inserting this new singular factor. A scalar pushforward theorem cannot be used after replacing its scalar-smooth input hypothesis by an R1-valued conormal factor without proving a mixed theorem.

## 4. Exact hostile and finite controls

- **Same-block cusp:** $v=\rho(x_2)\delta(x_1-x_2)$ gives the $|x_1-x_2|$ normal cusp in (150.16); it is excluded from Proposition 153.1 and remains nonadmitted.
- **Gaussian Fourier:** the fixed-stage constant-coefficient Fourier test of 150 §§6–7 refutes relative-mode rapid decay. Proposition 153.1 asserts only conormal avoidance/finite microlocal estimates, not the false fixed-stage Fourier decay or scalar polyhomogeneity.
- **Finite rational analogue:** [`fixtures/green_moment_control_153.py`](fixtures/green_moment_control_153.py) checks $G(n)=|n|/2$, $\Delta^2G=\delta_0$, exact zeroth/first-moment subtraction, finite support of the corrected Green primitive, and 242 exhaustive five-site integer inputs. This is only a finite algebra regression: it detects sign, normalization and support mistakes, **not** any infinite-dimensional wavefront, scalar-PHG or completed-tensor claim.

## 5. Mathematical verdict and next admissible input

| Question | Verified by 153 primary argument | Remaining obligation |
| --- | --- | --- |
| Ambient Green primitive and full equality | Prior 150.3–150.6 | No change |
| Pure diagonal wavefront after $h_i$ | Positive fixed-regulator Proposition 153.1 | Independent scrutiny of microlocal argument |
| Formal augmented Green product | Defined as distribution at fixed regulator | Not an existing scalar/R1 source |
| Output mixed R1 source and corner indices | NOT PROVED | New mixed conormal pushforward/lifting theorem |
| All profinite and parameter-row complete histories | NOT PROVED | Fixed-stage and all-mixed-row source continuity |
| Restricted lemma 150.L | **OPEN** | A legal source representative or a genuine restricted counterexample |
| Residual $W$ acyclicity, original R3, full REACH | **OPEN** | Do not infer from 153 |

**Admissible next scientific input:** construct a source-continuous mixed pushforward on the already-fixed complete scalar/R1 stages for the new interior Green conormal, covering all corner collisions, or produce a concrete **distinct-block** source whose output cannot be represented by the existing finite histories. A new formal edge, a smooth Gaussian replacement, a scalar b-fibration, a repetition of the failed Fourier ansatz, or a same-block cusp alone is not such an input.

**Custody boundary:** this is one new *primary* result and audit only. It must pass separate critical review, mathematical-document validation, protected CI and merged-main readback before a protected checkpoint may record acceptance. The prior accepted 150–152 and CP183 dispositions remain authoritative until then.
