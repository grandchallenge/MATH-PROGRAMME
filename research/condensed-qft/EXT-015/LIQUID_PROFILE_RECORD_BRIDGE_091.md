# EXT-015 REACH / 091 — actual liquid profile and subtraction-record bridge

**Disposition:** M1 construction candidate under the protected full plan [090](REACH_CONDENSED_RENORMALIZATION_PLAN_090.md). The theorem below concerns the concentrated finite-profile class, its actual records and completed shared-regulator composition. It is not a zero-scale quantum construction, a statement about all ambient plots, or original R3. Source-bound review 092 and acceptance ledger 093 are separate obligations.

## 1. Category, input cut and precise theorem

The protocol was protected and exactly read back in PR #2896 at e06b00010c080663461488f23fea819a24d91063 before construction. Original R0/R1 and the separate 087–089 result remain completed; original R2/R3/R4 remain open.

| Input | Frozen Git blob |
| --- | --- |
| [090, full protocol](REACH_CONDENSED_RENORMALIZATION_PLAN_090.md) | 6b642bf10c3328bb64d37474e290810fb45cbca1 |
| [087, actual subtraction records](R2_CONSISTENT_SUBTRACTION_RECORDS_087.md) | 452c494bcdc94ba94e52ae50c7b4d1eb3240ca83 |
| [088, source-bound critic](AGENT_CRITICAL_REVIEW_CONSISTENT_HOST_088.md) | c1cebf1a5c846097ca8f80724c4ea62638d1a404 |
| [089, separate-objective ledger](CONSISTENT_HOST_ACCEPTANCE_089.md) | 600a269ffd47b84b1bc9c671125aea3bf61a2f80 |

Fix $0<p\le1$ and use $\mathcal L=\mathrm{Liq}_p(\mathbb R)$ with its liquid tensor and fixed sufficiently large size convention. All modules below are objects in that heart, or in its derived category when the superscript $L$ is displayed. Write $R=\mathbb R_{<p}$ for its tensor unit. Use

$$
V_d=\underline{\mathcal S(\mathbb R^d)},\quad V_0=R,\quad
B=R[\epsilon],\quad A=B[\epsilon^{-1}],\quad
\Phi_d=A\otimes_R V_d.
\tag{91.1}
$$

The polynomial/Laurent algebra objects have their finite-sum grading, not a topology permitting convergent infinite Laurent sums. Let

$$
X=\underline{C^\infty((0,\infty))},\qquad
E_d=\underline{\mathrm{Hom}}_{\mathcal L}(V_d,X).
\tag{91.2}
$$

This is the ordinary internal Hom, not a claim of derived concentration.

**Theorem 91.1.** For every finite $d,e\ge0$:

1. Evaluation $\epsilon^m f\mapsto[\epsilon^{m-d}f(y/\epsilon)]$ defines a monomorphism $\mathrm{ev}_d:\Phi_d\to E_d$. On each profinite test, its image is exactly the actual finite-profile families with continuous Schwartz coefficients in one common finite homogeneity stage.
2. Moment maps give real-linear liquid morphisms PP and CT, with a unique strong Laurent expansion uniform on those compact families and on bounded Schwartz test families. The actual pole/remainder record image has addition as its inverse onto the evaluated image.
3. The module $\Phi_d$ is flat over $A$ and the natural equivalence below realizes completed exterior composition with the shared regulator.
4. The record isomorphism respects the explicitly reprojected regulator action. Vertex derivatives are linear over $A$; regulator rescaling is semilinear. The scalar disjoint unit, graded symmetry and associativity are preserved.
5. Neither equality with the ambient-subspace topology nor reconstruction from formal Laurent coefficients follows. Both false enlargements have controls in section 8.

$$
\Phi_d\otimes_A^L\Phi_e\simeq\Phi_{d+e}.
\tag{91.3}
$$

The concentrated physical family associated to a finite element is

$$
T_\epsilon(y)=\sum_{m\in F}\epsilon^{m-d}f_m(y/\epsilon),
\qquad F\subset\mathbb Z\text{ finite}.
\tag{91.4}
$$

This is precisely 087.3 after grouping $m=-h$. The actual functions, rather than graph presentations, determine the input.

## 2. Categorical and Schwartz inputs, with exact scope

Use Scholze, [Lectures on Analytic Geometry, arXiv:2605.03655v1, Theorem 6.5](https://arxiv.org/pdf/2605.03655v1), for the real liquid heart, compact projective generators on **extremally disconnected** profinite sets, free-measure adjunction and derived liquid tensor. Use [Clausen–Scholze, arXiv:2605.11731v1, Lecture III and Theorem 4.11/Remark 4.12](https://arxiv.org/pdf/2605.11731v1) for internal-Hom closure, nuclear Fréchet flatness and agreement of liquid tensor with the usual completed tensor. No projectivity of a general profinite measure module is asserted. No source Fréchet space is inferred projective from flatness.

The nuclear Schwartz input can be seen directly through Hermite functions. For $d>0$, the harmonic oscillator $-\Delta+|y|^2+1$ has the Hermite basis $h_\alpha$ with eigenvalues $\lambda_\alpha=2|\alpha|+d+1$. Integration against powers of the oscillator makes the Hermite coefficients of a Schwartz function rapidly decreasing. Conversely the creation/annihilation relations, followed by Sobolev estimates, bound each fixed Schwartz seminorm of $h_\alpha$ by a polynomial in $\lambda_\alpha$. A rapidly decreasing coefficient sequence therefore converges in every Schwartz seminorm and reconstructs its Schwartz function. These estimates identify the topology with the rapidly decreasing Hermite-sequence topology.

Use Hilbert seminorms $\sum_\alpha|c_\alpha|^2\lambda_\alpha^{2N}$. Between sufficiently separated stages the singular values are $\lambda_\alpha^{-k}$, which are summable for $k>d$. The defining tower is therefore trace-class and nuclear, meeting Remark 4.12's hypotheses.

For completeness, the kernel identification is not finite separability. Equivalent seminorms on the sequence model are weighted sums $\sum_\alpha|c_\alpha|\lambda_\alpha^N$. For a joint rapidly decreasing array $c_{\alpha,\beta}$, the sum $\sum c_{\alpha,\beta}e_\alpha\otimes e_\beta$ converges in every projective tensor seminorm, since $\sum|c_{\alpha,\beta}|\lambda_\alpha^N\lambda_\beta^M$ is finite. These sums give the continuous inverse to the coefficient map. Tensor products of Hermite functions give

$$
V_d\otimes_R V_e
\simeq\underline{\mathcal S(\mathbb R^d)\widehat\otimes_\pi
\mathcal S(\mathbb R^e)}
\simeq V_{d+e},
\tag{91.5}
$$

and the higher derived tensors vanish by flatness. The case $d=0$ is the unit case. This argument uses the liquid completion supplied by the cited theorem, not the algebraic tensor of global sections.

## 3. Profinite sections and actual evaluated-family relations

We first justify the finite-stage assertion without making general profinite generators projective.

**Lemma 91.2.** For every profinite $T$, its free liquid module $\mathcal M_{<p}(T)$ is compact in the abelian category: Hom out of it commutes with filtered colimits.

**Proof.** Choose an extremally disconnected profinite cover $S\twoheadrightarrow T$, and an extremally disconnected cover $S'\twoheadrightarrow S\times_T S$. The effective coequalizer in condensed sets, followed by the free-liquid left adjoint, yields a right-exact presentation

$$
\mathcal M_{<p}(S')\longrightarrow\mathcal M_{<p}(S)
\longrightarrow\mathcal M_{<p}(T)\longrightarrow0.
\tag{91.6}
$$

Both left terms are compact projective by Theorem 6.5. Applying Hom identifies Hom out of the cokernel with a kernel of two Hom functors. Filtered colimits of real vector spaces are exact and commute with this finite kernel. The two compact terms thus prove the assertion. The first arrow need not be injective; this is not a bound on projective dimension. $\square$

**Correction of an inherited negative assertion.** Old018 section3 denied abelian compactness of the free object on the convergent-sequence profinite set. Lemma91.2 shows that denial was incorrect: an extremally disconnected cover/kernel-pair presentation suffices. The old relative factorization proof used a weaker true assertion and is retained. This is not a projectivity claim, a statement of unbounded derived compactness, or a solution of original R3. Current018 records the narrow correction; review092 binds the revised bytes.

As a liquid module,

$$
\Phi_d=\bigoplus_{m\in\mathbb Z}V_d
=\varinjlim_N\bigoplus_{|m|\le N}V_d.
\tag{91.7}
$$

Each finite stage is the usual finite product of Schwartz Fréchet spaces. Its profinite sections are continuous maps into that space by the admitted topological realization. Lemma 91.2 proves

$$
\Phi_d(T)=\varinjlim_N
\mathrm{Cont}\!\left(T,\bigoplus_{|m|\le N}\mathcal S(\mathbb R^d)\right).
\tag{91.8}
$$

Thus a section has one common finite homogeneity window; on compact $T$, its coefficients have uniform bounds in every Schwartz seminorm.

For each fixed $m$, define the actual pairing

$$
b_m(f,\phi)(\epsilon)=
\epsilon^m\int f(u)\phi(\epsilon u)\,du.
\tag{91.9}
$$

On $\epsilon\in[a,b]\subset(0,\infty)$, any regulator derivative is a finite sum of terms involving powers of $\epsilon$, polynomial factors in $u$ and derivatives of $\phi$. Its supremum is bounded by a Schwartz seminorm of $f$ times a Schwartz seminorm of $\phi$. Thus $b_m$ is jointly continuous into $C^\infty((0,\infty))$. The completed kernel theorem and liquid realization make it a liquid pairing $V_d\otimes_R V_d\to X$. Currying and taking the Laurent coproduct gives $\mathrm{ev}_d$. Multiplication by $\epsilon$ in $X$ agrees with shifting $m$, so evaluation is linear over $A$.

To prove it monic on a profinite $T$, suppose a finite-window section evaluates to zero. Pull back to every $t\in T$ and pair with every Schwartz $\phi$. For each positive $\epsilon$ the resulting smooth Schwartz kernel is zero as a distribution, hence as a function. Substituting $y=\epsilon u$ in (91.4) gives the vanishing finite Laurent polynomial $\sum_m\epsilon^m f_m(t,u)=0$. Its coefficients vanish for every $u$. Hence each continuous coefficient map $f_m:T\to\mathcal S$ is zero. This proves injectivity on all profinite tests, and equality of evaluated families gives exactly these relations.

The image is a categorical subobject with the finite-stage sections (91.8). Nothing identifies it with the condensation of the point-set image carrying a weaker ambient subspace topology. For general $T$, one can express the envelope sections by adjunction as
$\mathrm{Hom}_{\mathcal L}(\mathcal M_{<p}(T)\otimes_R V_d,X)$; only the constructed image has been identified here.

## 4. Moment maps and strong uniform subtraction

Let $\mu_\alpha(f)=\int u^\alpha f(u)\,du$. This is a continuous Schwartz functional. Define the local jet and pole objects

$$
J_{d,0}=\bigoplus_\alpha R\,\partial^\alpha\delta_0,\qquad
J_{d,-}=\bigoplus_{\substack{n<0\\\alpha}}
R\,\epsilon^n\partial^\alpha\delta_0.
\tag{91.10}
$$

For $d=0$, the sole multi-index is zero. Actual jet evaluation in $E_d$ is
$\phi\mapsto(-1)^{|\alpha|}\epsilon^n\partial^\alpha\phi(0)$.
For a finite profile input the Laurent coefficient is

$$
a_n=\sum_{\substack{m\in F,\ \alpha\\m+|\alpha|=n}}
\frac{(-1)^{|\alpha|}\mu_\alpha(f_m)}{\alpha!}
\partial^\alpha\delta_0.
\tag{91.11}
$$

Each fixed finite window has finitely many pole and constant coefficients, each a continuous moment. Therefore
$\mathrm{PP}T=\sum_{n<0}\epsilon^n a_n$ and $\mathrm{CT}T=a_0$ are real-linear liquid morphisms to (91.10). They are not claimed linear over $A$.

**Strong estimate.** Pair (91.4) with $\phi$ and Taylor-expand $\phi(\epsilon u)$ at zero. The global remainder of order $k$ is bounded by a constant times $\epsilon^{k+1}|u|^{k+1}$ and a derivative supremum of $\phi$. Schwartz moments of $f_m$ absorb that factor. For every integer $N$, subtracting the coefficients of degree less than $N$ leaves $O(\epsilon^N)$ uniformly on bounded sets of Schwartz tests and compact finite-stage profile families. When a requested order precedes the first coefficient, boundedness of the zeroth test seminorm gives the same estimate. For smooth parameter families the estimate applies also after each fixed finite number of parameter derivatives, locally in their common stage.

This is the strong topology of tempered distributions; restriction to bounded compact smooth tests gives the strong distribution estimate of 087. A different first nonzero coefficient would contradict its own leading-power estimate after pairing with one separating test. Hence the expansion is unique. The actual remainder $R_T=\mathrm{ev}_d(T)-\iota\mathrm{PP}T$ has strong limit $a_0$, uniformly on the stated families. Regular finite limits are reproduced. No infinite delta-jet series is asserted convergent.

Set $\mathscr Z_d$ to the categorical image of
$(\mathrm{PP},\mathrm{ev}_d-\iota\mathrm{PP})$.
It is monic on $\Phi_d$, since addition of the two components is the monic evaluation map. Consequently $\Phi_d\to\mathscr Z_d$ is an isomorphism, and addition identifies it with the categorical evaluated image in $E_d$. This proves an actual analytic-record inverse on every profinite test, not recovery from formal coefficients or graph provenance.


## 5. Flatness and completed composition over the shared regulator

For a module $M$ over $A$ in the heart, forgetting its action of $A$ is exact: the action on a kernel or cokernel is induced from the original maps. The free-module tensor identity gives

$$
M\otimes_A\Phi_d
\simeq U(M)\otimes_R V_d.
\tag{91.12}
$$

The right side is exact in $M$ because $V_d$ is flat. Thus $\Phi_d$ is flat over $A$, not necessarily projective. Computing the relative derived tensor with this flat factor and applying (91.5) gives

$$
(A\otimes_R V_d)\otimes_A^L(A\otimes_R V_e)
\simeq A\otimes_R(V_d\otimes_R V_e)
\simeq\Phi_{d+e}.
\tag{91.13}
$$

On elementary profiles it sends $(\epsilon^m f,\epsilon^n g)$ to
$\epsilon^{m+n}(f\boxtimes g)$. Evaluated at the same regulator this is exactly exterior multiplication of (91.4) in independent relative variables. The relation
$(\epsilon^r a)\otimes b=a\otimes(\epsilon^r b)$ is therefore respected as actual function equality; reallocating a regulator scalar is not remembered as a graph label.

Equation (91.13) extends the elementary operation through the completed Schwartz kernel theorem. It is not a claim that the algebraic tensor of global sections, or the tensor of sections on a profinite test, computes all sections of this liquid tensor. On decomposable parameter families it gives the actual pointwise exterior operation; the completed map is fixed by the continuous kernel theorem.

Associativity and graded symmetry follow from the natural associative kernel maps on finite homogeneity stages, their completed tensors, and their Laurent colimits. The same maps agree after evaluation, which is monic. Adding any later cochain parity uses the usual Koszul permutation, not a new choice of kernel signs. The disjoint unit is $1\in\Phi_0=A$.

For $d>0$, ordinary same-variable profile multiplication is the continuous map
$f\otimes g\mapsto fg$ on completed Schwartz tensors. Its actual family map is

$$
(\epsilon^m f,\epsilon^n g)\longmapsto
\epsilon^{m+n-d}(fg).
\tag{91.14}
$$

The dimension shift is essential. Equivalently use the diagonal profile pullback
$\mathcal S(\mathbb R^{2d})\to\mathcal S(\mathbb R^d)$ and multiply by $\epsilon^{-d}$. That pullback is continuous: derivatives restrict to the diagonal and the source's polynomial weights control the target's. This is a map linear over the balanced regulator algebra in each factor. There is no ordinary spatial unit in $\mathcal S(\mathbb R^d)$ for $d>0$.

Transport these maps to actual records using their addition inverse followed by their explicit moment subtraction. This multiplication is of the reconstructed smooth kernels. It is not an expansion into undefined overlapping products of singular record components.

## 6. Explicit scalar reprojection and vertex maps

Write $a_{-1}$ for the $\epsilon^{-1}$ coefficient of the pole component, and $N=a_0=\mathrm{CT}T$. As actual evaluated families the record actions are

$$
\begin{aligned}
\epsilon\cdot(C,R)&=(\epsilon C-a_{-1},\ \epsilon R+a_{-1}),\\
\epsilon^{-1}\cdot(C,R)&=
(\epsilon^{-1}C+\epsilon^{-1}N,\ \epsilon^{-1}(R-N)).
\end{aligned}
\tag{91.15}
$$

The first components lie in the pole object after the indicated cancellation. Each coefficient projection is a real-linear liquid map, so the formulas are genuine morphisms of the record object. Their addition reconstructs $\epsilon T$ and $\epsilon^{-1}T$, respectively. The inverse and ring identities now follow from the monic evaluation and the Laurent action on $\Phi_d$. This defines the action over $A$ on $\mathscr Z_d$ and makes the record isomorphism linear over $A$; it does not make PP or CT linear over $A$.

For instance the scalar unit case $T=\epsilon^{-1}$ has $\mathrm{PP}T=\epsilon^{-1}$ and $\mathrm{CT}T=0$, whereas $\mathrm{PP}(\epsilon T)=0$ and $\mathrm{CT}(\epsilon T)=1$. Naively shifting only the pole component fails.

A physical vertex derivative and a fixed polynomial multiplication act on profiles by

$$
\partial_{y_j}(\epsilon^m f)=\epsilon^{m-1}\partial_{u_j}f,
\qquad
y^\beta(\epsilon^m f)=\epsilon^{m+|\beta|}u^\beta f.
\tag{91.16}
$$

These continuous Schwartz operations define morphisms linear over $A$. On the envelope, the corresponding maps are precomposition with the transposed test operators. Applying them to the strong estimates shows they commute with PP and CT and act entrywise on the record. Integration by parts gives the same result from the moment formula, including odd derivatives. Parameter differentiation commutes as well on the explicitly admitted smooth families.

For a fixed invertible linear change of normal coordinates, its Schwartz pullback and the continuous transposed distributional pullback give the same coefficient extraction. No claim of arbitrary distributional pullback or arbitrary source insertion is made here.

## 7. Semilinear scale maps and restricted smooth families

For $s>0$, define $Q_sT$ by $(Q_sT)_\epsilon=T_{s\epsilon}$. On profiles,

$$
Q_s(\epsilon^m f)=s^m\epsilon^m\theta_s f,\qquad
(\theta_sf)(u)=s^{-d}f(u/s).
\tag{91.17}
$$

Both maps are continuous on a finite Schwartz stage. They satisfy
$\theta_s\theta_t=\theta_{st}$, and $Q_s$ is semilinear for the algebra automorphism
$\rho_s(\epsilon)=s\epsilon$: $Q_s(aT)=\rho_s(a)Q_sT$.
It must not be called linear over a fixed regulator algebra.

The change of variables gives
$\mu_\alpha(\theta_sf)=s^{|\alpha|}\mu_\alpha(f)$, so the actual coefficient $a_n$ becomes $s^na_n$. PP commutes with the corresponding pole rescaling, CT is invariant, and the full records preserve $Q_sQ_t=Q_{st}$. Balanced composition is compatible after this same base automorphism in every factor.

For smooth manifold parameters, admit locally one finite homogeneity window with coefficients smooth into the Schwartz Fréchet topology. Pullback, gluing and parameter differentiation are computed coefficientwise; uniqueness of the grouped profiles verifies overlap agreement. On compact parameter pieces all fixed derivatives have bounded Schwartz seminorms, giving the mixed estimates in section 4. Their actual pairings define continuous linear maps from the Schwartz tests into $C^\infty(M\times(0,\infty))$ locally, with PP/CT coefficients smooth in $M$.

This is an explicit restricted smooth enrichment, not an intrinsic differentiable structure on all liquid modules or all sections of $E_d$. It is not the completed physical Weiss theorem. The physical kernel class is still concentrated in fixed relative coordinates, before M2's compact localization and collision charts.

## 8. Hostile controls against false identifications

**Escaping homogeneity.** Fix $0\ne f\in\mathcal S(\mathbb R^d)$ and set
$T^{(k)}_\epsilon=e^{-k^2}\epsilon^{-d-k}f(y/\epsilon)$.
On every positive compact regulator interval, each fixed family Schwartz seminorm and each regulator derivative is bounded by $e^{-k^2}a^{-k}$ times a polynomial in $k$ and a fixed seminorm of $f$. Thus $T^{(k)}\to0$ in the ordinary positive-regulator smooth-family topology.

It gives a continuous plot from the profinite one-point compactification
$\mathbb N\cup\{\infty\}$ into that ambient topology, with value zero at infinity. It cannot be a section of $\Phi_d$ on that profinite set: every finite window omits a nonzero homogeneous coefficient of the sequence. Hence the categorical image has a strictly stronger admitted family structure. The theorem claims the image with (91.8), not ambient equality.

**All moments zero, actual record nonzero.** For $d>0$, choose a nonnegative, nonzero, real even smooth Fourier bump supported away from zero, and let $f$ be its inverse Fourier transform. Then $f$ is real Schwartz and all its moments vanish, since they are derivatives of the Fourier bump at zero. The actual element $f\in\Phi_d$ is nonzero and evaluates to a nonzero family, but every physical Laurent coefficient in (91.11) is zero.

Its record retains the full actual remainder. Multiplication by a Gaussian $g(u)=e^{-|u|^2/2}$ reveals a nonzero zeroth moment: the Fourier pairing $\int fg$ is strictly positive because the Gaussian Fourier transform is positive and the bump is nonnegative and nonzero. More sharply, the actual families
$A_\epsilon=\epsilon^{-d}f(y/\epsilon)$ and
$B_\epsilon=g(y/\epsilon)$ both have strong finite limit zero, but their same-variable product has the nonzero finite limit $(\int fg)\delta_0$.
This does not refute disjoint factorization or BV on some enriched domain; it refutes replacing all these records by their finite outputs while retaining that actual multiplication.

**Completed, not finite separable.** In two variables,
$k(x,y)=e^{-x^2-y^2+xy}$ is Schwartz. Its $y$ derivatives at zero are $e^{-x^2}$ times polynomials of every distinct degree. They are linearly independent. A finite expression $\sum_{i=1}^Ng_i(x)h_i(y)$ would put all those derivatives in a span of dimension $N$. Thus $k$ is a genuine completed-kernel control for (91.13).

**Finite evaluation is not multiplicative.** On two independent lines take $A_\epsilon=\epsilon^{-1}\kappa_\epsilon$ and the same $B$ in its independent variable. Each has CT zero; their completed exterior product has finite coefficient
$(\delta''\boxtimes\delta+\delta\boxtimes\delta'')/2$.
This is the known nonzero cross-coefficient control of 087, not an algebra-homomorphism claim about CT.

**The studied raw host belongs to this class.** Its connected Gaussian backbone dominates the marked $P_1$, derivatives and polynomial factors, so each raw profile is Schwartz as in 087. Auxiliary prepared forest remainders contain partial collision distributions and are not silently identified with raw elements of $\Phi_d$. Source-channel finite normalization and all 277 counterterm calculations remain the admitted separate results; no changed algorithm requires their expensive replay here.

## 9. Exact evidence, proof dependencies and limitations

The exact fixture [091](fixtures/check_liquid_record_maps_091.py) checks finite moment/jet maps, regulator reprojection and inverse shifts, signed vertex derivatives, balanced allocation, dimension shifts, semilinearity and nonzero disjoint cross coefficients. It imports no 087 producer and does not pretend to prove liquid flatness, profinite compactness or infinite-dimensional topology. Those arguments are sections 2–7.

The cited categorical inputs are the actual real-liquid theorem and nuclear Fréchet tensor calculation. The classical analytic inputs are the Schwartz/Fourier calculus, Hermite basis estimates, finite Taylor theorem and dominated polynomial moments. The proof neither uses scalar projectivity for an arbitrary Fréchet source nor changes the actual R3 objects.

Local execution uses CHAD Windows CPython 3.12.12 in the existing isolated project evidence environment, with explicit external GCL uv and bytecode caches. There is no admitted root uv lockfile; this mathematical evidence environment is unpinned. No dependencies, workflow, system-Python installation, hosted compute or deployment are introduced.

**Achieved by the candidate:** genuine liquid realization of the concentrated actual profile/record class; strong uniform moment maps; a completed relative derived tensor theorem; explicit scalar reprojection and semilinear transport.

**Not achieved:** compact physical localization, the regular R1 sector map, collision-chart gluing, zero-regulator boundary, renormalized BV/QME, extended Weiss descent, R3 degree-two surjectivity or positive full REACH integration. M2 and the independent R3 audit retain those obligations. Source-bound critical review, final editorial acceptance and protected readback must precede any claim of M1 admission.


