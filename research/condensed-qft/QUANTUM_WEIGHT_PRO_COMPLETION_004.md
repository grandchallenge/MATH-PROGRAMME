# QFT-COND-004 / QW-001 — Quantum-weight pro-completion: preserved locality at every stage, failed locality after naive realization

**Status:** restricted **positive and negative theorems** for the smooth-kernel free quantum BV model. The finite quantum-weight truncations are factorization algebras; they form a pro-object *in factorization algebras*. Their inverse limit taken in ordinary derived liquid vector spaces is **not generally Weiss-local**. The negative theorem detects a nonzero **quantum cohomological** class of the massive scalar field. These claims have **not** undergone an independent originality/priority review.

**Research issue:** [QFT-COND-004](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2603).  
**Prerequisites:** [compact-support polynomial BV Weiss descent](COMPACT_SUPPORT_FACTORISATION_003.md); [classical degree-product no-go](DEGREE_COMPLETION_WEISS_NO_GO_004.md).

> **PRO-001 successor audit:** [Pro-valued Weiss non-descent](PRO_VALUED_WEISS_NO_GO_005.md) proves that the **same quantum-weight tower also fails Weiss descent as a pro-valued observable assignment**, detected by compatible local maps to a constant real coefficient object that cannot be represented with one global finite-weight cutoff. This does **not** invalidate the prior theorem that the tower is a *pro-object in the category of Weiss-local factorization algebras*. The distinction has been established by a full quantum BV cohomological witness.

## 1. Exact construction and hypotheses

Fix real $0<p\le1$, $m>0$, and the stable symmetric monoidal category

$$
\mathcal C_p=D(\mathrm{Liq}_p(\mathbb R)).
$$

Scholze's *Lectures on Analytic Geometry*, Theorem 6.5, supplies the p-liquid derived category and compact projective generators. On Euclidean opens $U\subseteq\mathbb R$ let $A_p(U)$ be QFT-COND-003's **filtered-colimit nuclear Fréchet compact-support object**. Define the BV generator complex in cohomological degrees $-1,0$:

$$
E_p(U)=[A_p(U)^{-1}\xrightarrow{P}A_p(U)^0],
\quad P=-\partial_x^2+m^2.
$$

Let $S_r(U)=\mathrm{Sym}^r_{\mathcal C_p}E_p(U)$ denote a finite *derived liquid* symmetric power (with $S_0=\underline{\mathbb R}$). The polynomial quantum differential is

$$
D=d+\hbar\Delta_{\mathrm{BV}}.
$$

The local BV contraction is defined on **smooth compact kernels only**, as in QFT-COND-003; it lowers symmetric degree by two and raises $\hbar$ -power by one. The kinetic differential preserves both degrees. Thus the **quantum weight**

$$
w=r+2k
$$

is invariant under $D$ on $\hbar^k S_r(U)$. Define its finite-weight subcomplex and truncation:

$$
W_w(U)=\bigoplus_{\substack{k,r\ge0\\2k+r=w}}
\hbar^kS_r(U),
\qquad
T_N(U)=\bigoplus_{0\le w<N}W_w(U).
\tag{1}
$$

Each $W_w$ is a cochain complex for $D$. Since multiplication adds weights and $D$ preserves weight, the quotient of the polynomial object by weight at least $N$ is $T_N$; its disjoint-open factorization maps descend. Transition maps $T_{N+1}\to T_N$ split as **cochain maps** because weights do not mix. The canonical pro-object is

$$
\mathbf T(U)=\{T_N(U)\}_{N\ge1}
\in\mathrm{Pro}(\mathcal C_p).
$$

Its *ordinary derived-category realization* is the homotopy inverse limit

$$
\widehat Q(U)=\mathrm{holim}_N T_N(U)
\simeq\prod_{w\ge0}W_w(U).
\tag{2}
$$

The product is taken in $\mathcal C_p$. It is not asserted to be the bornological completion used in any other formulation of QFT.

**Caution on further BV structure:** the raw odd BV bracket drops weight by two without a compensating $\hbar$. Consequently truncation may not preserve an *unscaled BD bracket*. We claim coherent factorization multiplication and the quantum chain differential, not an inherited unrestricted BD bracket.

## 2. Positive result: the completed tower has stagewise locality

**Theorem QW-1.** For each finite $w$, $W_w$ is a Weiss homotopy cosheaf. For each finite $N$, $T_N$ is a factorization algebra valued in $\mathcal C_p$. Thus $\mathbf T$ defines a **pro-object in the category of such factorization algebras**.

**Proof.** For fixed $w$, filter the complex $W_w$ by decreasing $\hbar$ power:

$$
F^jW_w(U)=
\bigoplus_{\substack{k\ge j\\2k+r=w}}\hbar^kS_r(U).
$$

The differential preserves $F^j$, and every graded subquotient is

$$
F^jW_w/F^{j+1}W_w
\simeq(\hbar^jS_{w-2j},d).
$$

Each such finite classical symmetric degree satisfies Weiss descent by the proved QFT-COND-003 compact-support kernel and Čech argument. The filtration has only finitely many steps. Since homotopy colimits are exact in any stable infinity-category, finite extension induction establishes descent for $W_w$. Finite sums give descent for $T_N$.

The coherent disjoint-open product is obtained by extension by zero, external tensoring and projection to weights below $N$. Its differential commutes with these structure maps: $P$ is local, and the BV contraction has no mixed terms between disjoint opens. Multiplication adds weights, so truncation by weights at least $N$ is multiplicatively valid. The standard associativity, symmetry and unit follow from the underlying polynomial formulas. The maps between truncations preserve all these structures. $\square$

**Boundary:** a **pro-object of Weiss cosheaves** is not *automatically* a Weiss cosheaf **with values in** the pro-category: the latter assertion requires computing potentially infinite Čech homotopy colimits in $\mathrm{Pro}(\mathcal C_p)$. Theorem QW-1 asserts the former, not the latter.

## 3. Negative result: quantum-weight inverse limit fails ordinary Weiss descent

**Theorem QW-2.** For the free massive scalar field just defined, $\widehat Q(U)$ in (2) is **not** a Weiss homotopy cosheaf in $\mathcal C_p$. This failure is detected by a genuine degree-zero *quantum BV* cocycle.

**Proof.** Consider the separated bounded intervals and their unions

$$
I_j=(3j,3j+1),\quad
U=\coprod_{j\ge1}I_j,\quad
U_k=\coprod_{j=1}^{k}I_j.
$$

The increasing family $\{U_k\}$ is a genuine Weiss cover: every finite configuration lies in one $U_k$. Its Čech homotopy colimit in $\mathcal C_p$ is the filtered colimit over $k$.

For each $j\ge1$ define the moment functional on liquid compact-support field generators by

$$
\ell_j(f)=\int_{I_j}e^{mx}f(x)\,dx.
$$

It is continuous at every nuclear Fréchet support stage and extends to a morphism into $\underline{\mathbb R}$. Since $(-\partial_x^2+m^2)e^{mx}=0$, compact-support integration by parts shows $\ell_j(Pg)=0$. Choose $f_j$ supported inside $I_j$ with $\ell_j(f_j)=1$. The moment functional defines a chain map $E_p(U)\to\underline{\mathbb R}[0]$.

For the **quantum** complex $W_j$, define

$$
\lambda_j:W_j(U)\longrightarrow\underline{\mathbb R}[0]
$$

by projection to the $\hbar^0S_j(U)$ summand and application of the $j$ -fold symmetric moment $\ell_j^{\otimes j}$. This is a chain map for the full quantum differential $D$: its $\hbar^0$ projection kills the image of $\hbar\Delta$, while the kinetic differential is killed by $\ell_j(Pg)=0$.

The monomial

$$
z_j=x_{f_j}^{\,j}\in W_j(U)^0
$$

is a closed quantum cocycle because $d(x_{f_j})=0$ and $\Delta$ requires an antifield generator. Its class is nonzero since $\lambda_j(z_j)=1$. The categorical product (2) therefore contains the cocycle $z=(z_1,z_2,\ldots)$, mapping under $\prod_{j\ge1}\lambda_j$ to the diagonal $(1,1,\ldots)$ in $\prod_j\underline{\mathbb R}$.

For each $k$, $\ell_j$ vanishes identically on functions supported in $U_k$ whenever $j>k$. Thus the composite from $\widehat Q(U_k)$ to $\prod_j\underline{\mathbb R}$ factors through the first $k$ coordinates. By passage to filtered colimits we obtain a factorization

$$
\mathrm{colim}_{k}\widehat Q(U_k)
\longrightarrow
\bigoplus_{j\ge1}\underline{\mathbb R}
\longrightarrow
\prod_{j\ge1}\underline{\mathbb R}.
\tag{3}
$$

**Detection:** Scholze's Theorem 6.5 states that the objects $\mathcal M_{<p}(S)$ for extremally disconnected profinite $S$ are **compact projective generators**. At $S=*$, $\mathcal M_{<p}(*)=\underline{\mathbb R}$ is the monoidal unit. Compactness implies that a map from the unit into the coproduct of real units factors through some finite partial sum. Such a map cannot give $(1,1,\ldots)$ after inclusion into the product. Consequently $z$ cannot be lifted from $\mathrm{colim}_k\widehat Q(U_k)$, even on derived cohomology. The Weiss comparison is not an equivalence. $\square$

**Exact claim boundary:** the counterexample applies to the **categorical inverse-limit realization** of the quantum-weight filtration on a disconnected Euclidean open. It neither disproves any stagewise pro-factorization theorem nor asserts failure of all bornological, local-support, renormalized or $\hbar$ -adically completed QFT constructions.

## 4. A typed and computable obstruction

Let $\mathcal U$ be a Weiss cover, $J$ its Čech indexing category, and suppose every finite truncation $T_N$ satisfies descent on that cover. Then the comparison for the realized inverse limit factors through the canonical interchange map

$$
\kappa_{\mathcal U}:
\mathrm{hocolim}_{J}\mathrm{holim}_N T_N
\longrightarrow
\mathrm{holim}_N\mathrm{hocolim}_{J}T_N.
\tag{4}
$$

**Proposition QW-3 (exact iff criterion).** The realized completed object has Weiss descent for $\mathcal U$ **if and only if** the obstruction object

$$
\mathfrak O_{\mathcal U}
=\mathrm{cofib}(\kappa_{\mathcal U})
$$

vanishes.

**Proof.** The second part of the comparison, from $\mathrm{holim}_N\mathrm{hocolim}_J T_N$ to $\mathrm{holim}_N T_N(U)$, is an equivalence by stagewise descent. Therefore the cofiber of the global Weiss comparison is precisely $\mathfrak O_{\mathcal U}$. $\square$

QW-2 gives a **nonzero compact-generator-detected witness** for this obstruction. To test a candidate corrected completion, compute maps from the compact projective generating family of Theorem 6.5 into its comparison cone, with explicit cohomological degrees. Checking only a finite number of truncations can **certify a negative witness**, but cannot establish a universal infinite equivalence.

The transition tower (1) is **split at the cochain level**, so its inverse limit is already the categorical product (2). In this example the failure is not attributable to an exotic nonsplit $\varprojlim^1$ of truncations. It is the failure of **Čech homotopy colimits to commute with the infinite product**.

## 5. Verification, literature and research boundary

The deterministic standard-library fixture \`research/condensed-qft/fixtures/quantum_weight_weiss.py\` checks exact integer/rational weights, the differential's preservation of quantum weight, compatibility of the finite truncation maps, and the support-escape obstruction over arbitrarily large finite cases. Its finite controls are **not** a proof of the infinite theorem; the compactness argument above supplies that proof.

**Imported mathematics:** Scholze, [*Lectures on Analytic Geometry*](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf), Theorem 6.5 (p-liquid categories and compact generators); Clausen–Scholze, [*Condensed Mathematics and Complex Geometry*](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf), Theorem 4.11/Remark 4.12 (nuclear Fréchet tensor); [Gwilliam–Rejzner, *Relating Nets and Factorization Algebras: Free Field Theories*](https://link.springer.com/article/10.1007/s00220-019-03652-9); [Gwilliam on Weiss descent](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.70152); [Costello–Gwilliam, *Factorization Algebra*](https://arxiv.org/abs/2310.06137).

**Claim taxonomy:** quantum weight invariance is an elementary identity and has antecedents in quantum BV filtrations; finite truncation descent is a sourced reconstruction of known free-factorization methods; QW-2 is an explicit internally derived **quantum-level extension** of the prior classical counterexample with **no claim of external novelty or priority**; QW-3 is a formal comparison principle.

**Unresolved:** whether there is a **descent-compatible analytic or pro-liquid completion** preserving full quantum observables and compatible with established differentiable pro-cochain factorization theory. In particular, this note does not claim a pro-category Weiss cosheaf or a new interacting/QFT-renormalization theorem. The next step is a comparison in an explicitly chosen completed target category, not an inference from stagewise computations alone.
