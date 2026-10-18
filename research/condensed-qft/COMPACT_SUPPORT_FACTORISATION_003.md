# QFT-COND-003 — Liquid compact-support BV observables and Weiss descent

**Disposition:** restricted **positive result** for smooth-kernel, *polynomial* classical and free quantum BV observables in real $p$ -liquid modules, with a separate rigorous **negative finding** for naive projective LF tensor products. This is a reconstruction of known free-field factorization mathematics using established Clausen–Scholze liquid tensor results; **no originality, interacting-field theorem, Lean certification or physical prediction is claimed**.

**Tracker:** [QFT-COND-003](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2601).  
**Predecessor:** [QFT-COND-002 derived Schwartz comparison](DERIVED_SCHWARTZ_TENSOR_002.md).  
**Scope:** nonempty open subsets of finite-dimensional Euclidean space, with empty-open unit adjoined; finite polynomial degree and $\mathbb R[\hbar]$. No completed symmetric-power product, $\hbar$ -adic completion, distributional diagonal multiplication, or renormalization.

## 1. Exact realization of compactly supported functions

Fix $0<p\le1$, $d\ge1$ and $m>0$. Work in the symmetric monoidal stable category $\mathcal C_p=D(\mathrm{Liq}_p(\mathbb R))$. For an open $U\subseteq\mathbb R^d$ and a compact set $K\Subset U$, denote by $\mathcal D_K(U)$ the nuclear Fréchet space of smooth real functions supported in $K$. Define the **liquid compact-support object** by

$$
A_p(U)=\underset{K\Subset U}{\mathrm{colim}}\,
\underline{\mathcal D_K(U)}.
\tag{C1}
$$

The displayed colimit is taken *in the abelian category of real p-liquid modules*, not via a claim of full faithfulness for the generally nonmetrizable LF space $C_c^\infty(U)$. Every Euclidean open is sigma-compact, so a cofinal countable compact exhaustion computes the same object. Changing exhaustion leaves this colimit canonically unchanged. Extending a function by zero along $U\subseteq V$ is continuous on each support stage and gives $A_p(U)\to A_p(V)$.

Theorem 4.11 and Remark 4.12 of Clausen–Scholze show that nuclear Fréchet spaces are flat for the liquid tensor and their liquid tensor agrees with the classical *Fréchet* completed projective tensor. Filtered colimits are exact in this Grothendieck abelian category and liquid tensor preserves colimits. Hence $A_p(U)$ is liquid-tensor-flat. Differential operators preserve compact supports; the formally self-adjoint elliptic operator

$$
P=-\Delta+m^2:A_p(U)\longrightarrow A_p(U)
$$

is therefore a canonical local morphism.

**Source audit:** Peter Scholze explicitly identifies good liquid versions of $C_c^\infty(U)$ as sequential colimits of nuclear Fréchet spaces, with the expected liquid tensor: [MathOverflow, 2025](https://mathoverflow.net/questions/500784/liquid-versions-of-the-vector-spaces-of-test-functions-and-distributions/500821).

## 2. The crucial negative result: projective LF tensor is wrong

**Proposition TOPO-0 (classical counterexample).** For $C_c^\infty(\mathbb R)$ with its strict LF topology, the kernel theorem uses the *completed inductive* tensor, not generally the projective completed tensor:

$$
\mathcal D(\mathbb R)\widehat\otimes_i\mathcal D(\mathbb R)
\cong\mathcal D(\mathbb R^2).
$$

There are continuous bilinear forms for the inductive tensor (separately continuous bilinear functionals) which are **not jointly continuous**, and hence do not extend through the projective tensor in the same way.

**Proof via a concrete distribution.** The locally finite sum

$$
T=\sum_{n\ge1}(\partial_x^n\delta_0)\otimes\delta_n
\quad\in\mathcal D'(\mathbb R^2)
$$

defines

$$
B(f,g)=\sum_{n\ge1}(-1)^nf^{(n)}(0)g(n).
$$

For each fixed $g$ only finitely many terms appear; for fixed $f$ the evaluation functionals at $n$ form a locally finite distribution. Therefore $B$ is separately continuous. Suppose it were jointly continuous. For a fixed compact support stage for $f$ near $0$, a controlling continuous seminorm would be bounded by a constant times finitely many derivative suprema through some order $N$. Choosing $g$ supported close to a single integer $n>N$ would then bound $f^{(n)}(0)$ by derivatives of order at most $N$, impossible for arbitrarily narrow rescaled bumps. Thus the bilinear form is not jointly continuous. $\square$

This is **not new**: compare Trèves, *Topological Vector Spaces, Distributions and Kernels*, Theorem 51.6, and the explicit 2026 discussion at https://mathoverflow.net/questions/511033/ . It rules out the unqualified shortcut

$$
\mathcal D(U)\widehat\otimes_\pi\mathcal D(V)
\stackrel{?}{\cong}\mathcal D(U\times V)
$$

as an isomorphism with the ordinary LF topologies. **Do not confuse the topology issue with a counterexample to the liquid tensor.**

## 3. Source-backed liquid compact-support kernel theorem

**Theorem LIQ-1.** For nonempty Euclidean opens $U,V$, the external product gives a canonical, extension-by-zero-compatible equivalence in $\mathcal C_p$,

$$
\boxed{
A_p(U)\otimes^{\mathbb L}_{\mathbb R,<p}A_p(V)
\simeq A_p(U\times V).
}
\tag{LIQ-1}
$$

Both sides lie in degree zero.

**Proof.** Tensor distributes over the two filtered colimits in (C1). At each compact Fréchet support stage it agrees with the completed nuclear Fréchet tensor, and higher liquid Tor vanishes. The classical smooth compact-support *inductive* kernel theorem identifies the filtered family of those stage tensor products with smooth kernels of compact support on the Cartesian product: rectangles of compact supports are cofinal for arbitrary compactly supported kernels, and local support-stage presentations agree with the classical test-function tensor construction. Their **filtered colimit** is exactly $A_p(U\times V)$. Flatness of the stages and exactness of filtered colimits give the derived assertion. $\square$

**Critical qualification:** The topological kernel theorem and compatibility with the compact-support stage presentation are imported, not proved by a finite fixture. LIQ-1 concerns the liquid filtered colimit, **not** the wrong full-LF projective tensor from TOPO-0. Iteration applies to every finite power $A_p(U)^{\otimes^{\mathbb L}n}\simeq A_p(U^n)$; no infinite product of symmetric degrees is asserted.

## 4. Constructing the free classical and quantum polynomial BV objects

Freeze cohomological grading explicitly. Let $E_p(U)$ have $E^{-1}_p(U)=A_p(U)$ and $E^0_p(U)=A_p(U)$, with differential $d_E=P:E^{-1}\to E^0$. Write a degree-zero field generator $x_f$ and degree-minus-one antifield generator $\theta_f$. Thus

$$
d(x_f)=0,\qquad d(\theta_f)=x_{Pf}.
$$

Define the **direct sum** of finite homotopy-symmetric powers:

$$
\mathrm{Obs}^{\mathrm{cl}}_p(U)
=\bigoplus_{n\ge0}\left(E_p(U)^{\otimes^{\mathbb L}n}\right)_{hS_n}.
\tag{CL-1}
$$

Since $n!$ is invertible over $\mathbb R$, the homotopy coinvariants identify with the usual graded symmetric coinvariants for each finite $n$. LIQ-1 identifies the degree- $n$ coefficient with $A_p(U^n)$, with finite field/antifield degree-label components. The differential $d$ is the derivation extending $P$.

The local odd BV pairing is given on generators by

$$
\{x_f,\theta_g\}=\int_U f(t)g(t)\,dt,\qquad
\{x_f,x_g\}=\{\theta_f,\theta_g\}=0.
$$

Define $\Delta_{\mathrm{BV}}$ as the graded-signed sum of all pairwise field/antifield contractions. On compactly supported **smooth** $n$ -variable kernels it is a diagonal restriction followed by integration in the paired coordinates, giving a continuous morphism to the $(n-2)$ -variable kernel object of cohomological degree $+1$.

**Lemma BV-1.** On these finite polynomial kernels,

$$
d^2=0,\quad \Delta_{\mathrm{BV}}^2=0,\quad
d\Delta_{\mathrm{BV}}+\Delta_{\mathrm{BV}}d=0.
$$

The first is immediate from the two-term generator differential, and the second is standard Koszul-sign cancellation for odd constant-coefficient contractions. The third reduces to invariance of the pairing under $P$. On two antifields the obstruction is the exact expression

$$
\int_U(Pf)g-\int_U f(Pg)=0,
$$

which vanishes by formal self-adjointness and compact support. The general identity follows from the order-one/order-two operator identities. A nonsymmetric kinetic matrix violates it (see the fixture).

Define the **polynomial free quantum** object over $\mathbb R[\hbar]$,

$$
\mathrm{Obs}^{q,\mathrm{poly}}_p(U)
=\left(\mathrm{Obs}^{\mathrm{cl}}_p(U)\otimes\mathbb R[\hbar],
d+\hbar\Delta_{\mathrm{BV}}\right).
\tag{Q-1}
$$

This is not an $\hbar$ -adically complete quantization. The smooth-kernel contraction does not multiply arbitrary singular distributions. In particular, it does **not** construct renormalized coincident-point operator products.

## 5. Coherent disjoint-open products and Weiss descent

**Theorem FA-1 (restricted positive construction).** The assignments $\mathrm{Obs}^{\mathrm{cl}}_p$ and $\mathrm{Obs}^{q,\mathrm{poly}}_p$ have coherent prefactorization maps for finite collections of disjoint Euclidean opens and satisfy Weiss homotopy-cosheaf descent for all **nonempty Weiss covers**. They therefore yield the corresponding free *polynomial* factorization objects in the stable p-liquid setting, with the empty-open unit treated separately.

**Prefactorization proof.** For disjoint $U_1,\ldots,U_r\subset V$, extend by zero and multiply external smooth kernels. The LIQ-1 equivalence and graded symmetrization yield maps from the tensor of the observable objects to the observable object on $V$. Associativity, symmetric-group equivariance and unit are inherited from external products. The kinetic differential is local; and mixed BV pairings between disjoint supports vanish. Consequently the maps also commute with $d+\hbar\Delta_{\mathrm{BV}}$. These natural strictly associative formulas specify the higher-coherent maps on passing to the stable symmetric monoidal infinity-category.

**Weiss descent proof, degree by degree.** A Weiss cover $\{U_i\}_{i\in I}$ of $U$ has the property that every finite collection of points lies in some $U_i$. For each integer $n\ge1$,

$$
U^n=\bigcup_{i\in I}U_i^n,
\qquad
\bigcap_{j=0}^{k} U_{i_j}^n
=\left(\bigcap_{j=0}^{k} U_{i_j}\right)^n.
\tag{W-1}
$$

Thus the degree- $n$ Čech diagram of polynomial observables is the **ordinary compact-support Čech diagram on $U^n$**, followed by a finite signed $S_n$ coinvariant operation. The compact-support Čech augmentation is a homotopy equivalence: a locally finite smooth partition of unity subordinate to the ordinary cover gives the usual alternating Čech contraction. Because every test kernel has compact support, only finitely many partition terms act on each support stage; all induced maps are liquid morphisms. Finite signed coinvariants are exact in characteristic zero. Differential operators $P$ commute with extension by zero, and the fixed-degree internal complexes are bounded, so the Čech homotopy-colimit map is an equivalence in the derived category. The $n=0$ unit term has a contractible nonempty indexing Čech simplex. Colimits commute with the direct sum over finite $n$. This proves the classical case.

**Quantum filtration proof.** Filter (Q-1) by generator degree $F_{\le N}$, with $d$ preserving degree and $\Delta_{\mathrm{BV}}$ lowering it by two. The associated grade is the classical degree- $N$ complex with coefficients $\mathbb R[\hbar]$. Each graded piece has Weiss descent by the previous paragraph. Exactness of homotopy colimits in a stable category gives descent inductively for each **finite** $F_{\le N}$; taking the filtered colimit proves the direct-sum polynomial quantum case. **No inverse limit, completed product, or convergence assertion is used.** $\square$

**Prior-art judgment:** The free-field factorization structure and partition-of-unity proof strategy are established in Costello–Gwilliam. FA-1 provides an explicitly typed p-liquid version using Clausen–Scholze analytic tensor, **not yet a mathematically original field-theory claim**. This does not claim a full interacting or renormalized quantum factorization algebra.

## 6. Hand examples and adversarial tests

For $d=1$, take $U_1=(-3,-1)$ and $U_2=(1,3)$ inside $V=(-4,4)$. A smooth kernel in $U_1$ and one in $U_2$ have vanishing mixed diagonal contraction, so their disjoint-open product is compatible with the quantum BV differential.

For an overlapping cover of $(-2,2)$ by $(-2,1)$ and $(-1,2)$, a subordinate smooth partition of unity decomposes each compactly supported test function. This proves degree-one compact-support Čech descent; the cover **is not Weiss** because it may miss a pair of separated points in the larger interval.

The finite adversarial test uses $X=\{0,1,2\}$. The opens $\{0,1\}$ and $\{1,2\}$ cover all points but miss the ordered pairs $(0,2)$ and $(2,0)$. Adding $\{0,2\}$ captures every pair but misses six ordered triples using all three distinct points. Thus testing only quadratic observables never establishes full Weiss descent. A genuine Weiss cover of this finite $X$ includes an open containing all three points.

For a two-generator BV model, the obstruction to anticommutation is $P_{12}-P_{21}$. Symmetric matrices give zero; an asymmetric matrix is a rigorous hostile fixture.

**Deterministic exact replay:**

~~~sh
python3 research/condensed-qft/fixtures/finite_weiss_bv.py
~~~

This checks exact finite configuration-space Čech $H_0$ ranks and BV compatibility. It is **not** a numerical substitute for the infinite-dimensional source and partition-of-unity proofs.

> **Completion caveat resolved negatively:** [QFT-COND-004 — naive degree-product Weiss no-go](DEGREE_COMPLETION_WEISS_NO_GO_004.md) constructs a genuine directed Weiss cover of countably separated intervals on which the categorical **infinite product of classical polynomial degrees fails descent**, detected in degree-zero cohomology by massive-scalar moment functionals. This does **not** contradict the finite direct-sum polynomial theorem below or establish failure for every corrected/adic completion.

## 7. Claim ledger and genuine frontier

| Boundary | Status | Support |
| --- | --- | --- |
| Nuclear Fréchet liquid tensor/flatness | Established source theorem | Clausen–Scholze, *Complex Geometry*, Theorem 4.11 / Remark 4.12 |
| Compact-support liquid ind-Fréchet construction | Established source construction | Scholze, 2025 MO answer; equation (C1) |
| Projective LF tensor substitution fails | Explicit classical obstruction | Test-function inductive kernel theorem; §2 |
| LIQ-1 compact-support liquid tensor | Sourced consequence | Filtered colimit and classical support-stage tensor |
| Free polynomial classical/quantum BV structure | Source-backed restricted construction | Smooth diagonal pairing, local $P$, graded-sign identities |
| Classical/quantum polynomial Weiss descent | Source-backed restricted theorem | (W-1), support Čech contraction, finite polynomial filtration |
| Arbitrary distribution products or renormalized coincident observables | **NOT PROVED** | Singular diagonals remain uncontrolled |
| Infinite completed symmetric algebra, $\mathbb R[[\hbar]]$ and descended inverse limits | **NOT PROVED** | Products, derived completions and Čech homotopy colimits can fail to commute |
| Gauge theory, anomaly classes, interactions or novel QFT prediction | **NOT PROVED** | Requires independent new hypotheses and proofs |

**Sources:** [Clausen–Scholze, *Condensed Mathematics and Complex Geometry*](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), Thm. 4.11/Remark 4.12; [Peter Scholze on liquid test functions](https://mathoverflow.net/questions/500784/liquid-versions-of-the-vector-spaces-of-test-functions-and-distributions/500821); [Costello–Gwilliam, *Factorization Algebras in QFT*](https://people.math.umass.edu/~gwilliam/vol1may8.pdf), Chapter 5; [Gwilliam, *Holomorphic field theories and higher algebra*](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.70152), Weiss definitions; [Trèves-type LF topology example](https://mathoverflow.net/questions/511033/what-kind-of-distributions-on-a-cartesian-product-are-jointly-continuous-bilinea); [Gwilliam–Rejzner free field comparison](https://arxiv.org/abs/1711.06674).

**Next research target (QFT-COND-004):** identify exact conditions under which degree-completed (infinite **product**) and $\hbar$ -adically completed free quantum BV observables satisfy Weiss descent in liquid modules; if not, construct a nonzero derived-limit cone. The finite **direct sum** theorem above does not settle this.
