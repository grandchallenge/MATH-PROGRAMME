# QFT-COND-004 — Naive degree completion obstructs Weiss descent

**Status:** explicit **negative theorem** for a precise categorical product completion of *classical* free massive scalar BV polynomial observables; source-backed compactness and a direct proof. This is a mathematical diagnostic, **not** a claim of originality over all existing factorization-algebra literature or a statement about established renormalized quantum observables.

**Research tracker:** [QFT-COND-004](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2603).  
**Positive predecessor:** [QFT-COND-003](COMPACT_SUPPORT_FACTORISATION_003.md) proves Weiss descent for the *direct sum* of smooth-kernel finite polynomial degrees, including the polynomial free quantum BV differential, using the correctly defined liquid tensor. The present negative result concerns taking their **infinite product** instead.

> **Quantum-level extension:** [QW-001 — Quantum-weight pro-completion and realized Weiss obstruction](QUANTUM_WEIGHT_PRO_COMPLETION_004.md) proves that finite quantum-weight truncations of the actual free quantum BV complex form a pro-object in factorization algebras, while their **categorical inverse-limit realization** again fails Weiss descent on the same genuine cover. The obstruction is detected by full quantum BV cochain maps; it does **not** imply a failure of every completed quantum factorization formalism.

## 1. Exact completion and claim

Fix $0<p\le1$, a real mass $m>0$, and $\mathcal C_p=D(\mathrm{Liq}_p(\mathbb R))$. For each open $U\subset\mathbb R$ let $A_p(U)$ be the filtered-colimit liquid compact-support test object of QFT-COND-003. The free BV generator is the two-term cochain complex

$$
E_p(U)=[A_p(U)^{-1}\xrightarrow{P}A_p(U)^0],
\qquad P=-\partial_x^2+m^2.
$$

Define the **naive degree-completed classical observable object**

$$
\boxed{
\widehat{\mathrm{Obs}}^{\mathrm{cl}}_p(U)
=
\prod_{r\ge0}\mathrm{Sym}^r_{\mathcal C_p}(E_p(U)).
}\tag{N1}
$$

This is the **categorical product** in the stable derived liquid category. Each finite symmetric degree uses the *derived liquid tensor* and characteristic-zero symmetric coinvariants. The differential preserves polynomial degree. The assignment is covariant under extension by zero.

**Theorem N-1 (Weiss failure for naive degree product).** There is a nonempty sigma-compact open $U\subset\mathbb R$ and a genuine Weiss cover $\{U_k\}$ for which the canonical map

$$
\underset{k}{\mathrm{colim}}\,
\widehat{\mathrm{Obs}}^{\mathrm{cl}}_p(U_k)
\longrightarrow
\widehat{\mathrm{Obs}}^{\mathrm{cl}}_p(U)
\tag{N2}
$$

is **not** an equivalence in $\mathcal C_p$. For the nested cover below, the filtered colimit computes the Weiss Čech homotopy colimit. The failure can be detected by actual degree-zero cocycles and field-equation moment maps, not merely by an inability to match literal chain representatives.

## 2. Explicit massive-scalar proof

For each integer $j\ge1$ set

$$
I_j=(3j,3j+1),\qquad
U=\coprod_{j\ge1}I_j,\qquad
U_k=\coprod_{1\le j\le k}I_j.
$$

The intervals are separated and escape to infinity. Every finite collection of points of $U$ lies in some $U_k$, so $\{U_k\}_{k\ge1}$ is **a Weiss cover**, not merely an ordinary cover. Since the cover is increasing, its Čech homotopy colimit agrees with the filtered colimit in (N2).

For each $j$, choose $f_j\in C_c^\infty(I_j,\mathbb R)$, nonnegative and normalized by

$$
\ell_j(f_j)=1,\qquad
\ell_j(g)=\int_{I_j}e^{mx}g(x)\,dx.
$$

This is a continuous linear functional at each nuclear Fréchet support stage and defines a liquid morphism $\ell_j:A_p(U)\to\underline{\mathbb R}$. It vanishes on $A_p(U_k)$ if $j>k$. Since $P(e^{mx})=0$ and all supports are compact in $U$, integration by parts gives

$$
\ell_j(Pg)=0.
$$

Therefore $\ell_j$ defines a cochain map $E_p(U)\to\underline{\mathbb R}[0]$ that kills the degree-minus-one antifields and sends the degree-zero field $x_g$ to $\ell_j(g)$. Taking the $j$ -fold symmetric tensor and symmetric coinvariants yields

$$
\lambda_j:\mathrm{Sym}^j E_p(U)\longrightarrow
\underline{\mathbb R}[0].
$$

The degree-zero closed field monomial $z_j=x_{f_j}^{\,j}$ satisfies $\lambda_j(z_j)=1$. Thus the product universal property constructs a morphism

$$
z:\underline{\mathbb R}[0]\longrightarrow
\widehat{\mathrm{Obs}}^{\mathrm{cl}}_p(U)
$$

with $j$ -th projection $z_j$; applying $\prod_{j\ge1}\lambda_j$ gives the diagonal map $\underline{\mathbb R}\to\prod_{j\ge1}\underline{\mathbb R}$ represented by $(1,1,1,\ldots)$.

For each **fixed** $k$, the map $\lambda_j$ vanishes on $\mathrm{Sym}^j E_p(U_k)$ whenever $j>k$. Consequently the composite from the left-hand side of (N2) to the product of real coefficient units **factors through their coproduct**:

$$
\underset{k}{\mathrm{colim}}\,
\widehat{\mathrm{Obs}}^{\mathrm{cl}}_p(U_k)
\longrightarrow
\bigoplus_{j\ge1}\underline{\mathbb R}
\longrightarrow
\prod_{j\ge1}\underline{\mathbb R}.
\tag{N3}
$$

The coefficient unit $\underline{\mathbb R}$ is **compact in $\mathcal C_p$**; this is the $D(\mathrm{Liq}_p)$ specialization explicitly used in Clausen–Scholze, *Condensed Mathematics and Complex Geometry*, Lecture IX, immediately before Definition 9.1 and Proposition 9.2. Hence any map from the unit to a filtered colimit of finite partial sums factors through some **finite** partial sum. In particular the diagonal morphism $(1,1,\ldots)$ cannot factor through the coproduct inclusion in (N3): after composing with the $j$ -th coordinate projection, it is nonzero for arbitrarily large $j$.

If (N2) were an equivalence, the map $z$ would lift along it, forcing this impossible factorization. Therefore (N2) is **not** an equivalence. The $\ell_j$ annihilate kinetic boundaries, so the obstruction persists in the degree-zero derived category. $\square$

The argument uses the actual **massive** free scalar kinetic operator. It does not rely on a zero differential or an artificial finite-dimensional truncation. The noncompact disconnected geometry is essential to the explicit witness.

## 3. What fails, and what does not

At each finite symmetric degree $r$, the positive QFT-COND-003 theorem gives Weiss descent. The failure comes from incorrectly interchanging an infinite product with a filtered colimit:

$$
\underset{k}{\mathrm{colim}}\,
\prod_{r\ge0}\mathrm{Sym}^r E_p(U_k)
\not\simeq
\prod_{r\ge0}
\underset{k}{\mathrm{colim}}\,
\mathrm{Sym}^r E_p(U_k).
\tag{N4}
$$

The right-hand side admits families with a different compact support at each degree, escaping every fixed cover member. The left-hand side forces a common stage of support when detected by the moment maps. This is the central **completion-versus-locality** obstruction.

**Positive boundary:** the finite-degree direct-sum *polynomial* classical and free quantum factorization objects of QFT-COND-003 retain Weiss descent. Nothing here contradicts that theorem.

**Negative boundary:** the precise naive product completion (N1) fails Weiss descent, even for the free massive scalar. This is a stronger and distinct finding from the classical locally convex LF-projective tensor failure documented in QFT-COND-003.

**Still open:** whether support-controlled, bornological, other derived analytic, or $\hbar$ -adic completions restore Weiss descent. In particular, N-1 does **not** establish failure for every completed BV model, every connected open, the conventional renormalized factorization algebra, or the $\hbar$ -adically complete free quantum theory.

## 4. Exact finite witnesses and reproducibility

A bounded discrete witness tests the quantifier structure of the obstruction without pretending to prove its infinite limit.

For fixed finite $N$, model the first $N$ separated components and the first $N$ polynomial degrees. Let the degree- $r$ observable be supported exclusively in component $r$. No finite stage $U_k$ with $k<N$ contains all these degreewise supports, even though every individual degree appears in some member. Increasing $N$ displays the necessity of an unbounded common support stage. The actual proof above supplies the infinite product and nonzero cohomological moment maps.

The existing [finite Weiss/BV fixture](fixtures/finite_weiss_bv.py) tests which point configurations evade bounded-degree Weiss covers. An additional exact finite completion fixture tests the cross-degree support obstruction. Neither numerical fixture substitutes for N-1.

## 5. Evidence and next research gate

| Claim | State | Evidence |
| --- | --- | --- |
| Compact-support liquid realization / polynomial Weiss descent | Source-backed predecessor | QFT-COND-003; Clausen–Scholze; Costello–Gwilliam |
| Compactness of the $p$ -liquid real unit | Published theorem | Clausen–Scholze, *Complex Geometry*, Lecture IX |
| N-1, failure of naive categorical symmetric-degree product | **Direct proof** | Massive field-equation moment maps, directed Weiss cover, compactness contradiction |
| Degreewise bounded fixtures | Reproducible finite checks | Exact standard-library Python |
| Novel priority versus broader QFT literature | Not certified | This is an internally derived explicit completion counterexample, requiring independent novelty audit |
| Corrected support-controlled or $\hbar$ -adic completion | **OPEN** | Need new completion functor, exact comparison and derived-limit/descent analysis |

**Primary references:**

- Clausen and Scholze, *Condensed Mathematics and Complex Geometry*, Lecture IV and Lecture IX: https://people.mpim-bonn.mpg.de/scholze/Complex.pdf.
- Costello and Gwilliam, *Factorization Algebras in Quantum Field Theory*, free-field chapters: https://people.math.umass.edu/~gwilliam/vol1may8.pdf.
- Scholze, liquid compact-support test functions: https://mathoverflow.net/questions/500784/liquid-versions-of-the-vector-spaces-of-test-functions-and-distributions/500821.
- Original GCL source proof: [QFT-COND-003](COMPACT_SUPPORT_FACTORISATION_003.md).

**Next decision:** design a **locally supported completion**, or one which is first completed locally and then Weiss-cosheafified, and compare it with N-1's naive product. A theorem proving corrected descent or a second counterexample would be a genuinely stronger contribution.
