# QFT-COND-004 / FC-007 — Triangular filtered dg bridge

**Disposition:** Two rigorous **negative controls** show that the split-weight completed liquid category in [CF-001](COMPLETE_FILTERED_LIQUID_WEISS_006.md) cannot be a full model for Costello–Gwilliam's complete filtered cochain category. A **positive finite-dimensional theorem** replaces strictly weight-preserving maps/differentials with upper-triangular ones and proves equivalence to the algebraic finite-filtered category. No infinite-dimensional enriched analytic equivalence or novelty priority is asserted.

**Research tracker:** [QFT-COND-004](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2603).

## 1. The source's actual contract

Costello–Gwilliam, *Factorization Algebras in Quantum Field Theory*, Vol. 1, **B.5.0.3**, require complete filtered complexes $V=\varprojlim_N V/F^NV$ and allow **all filtration-preserving maps**, not just weight-preserving maps. The weak equivalences are **associated-graded quasi-isomorphisms**. Definitions **B.5.0.4–B.5.0.6** supply completed coproducts, tensor products and factorization descent; **B.6.0.7–B.6.1.1** also impose differentiable cofibrations and smooth multilinear maps.

Our [CF-001](COMPLETE_FILTERED_LIQUID_WEISS_006.md) used

$$
\mathcal{CF}^{\mathrm{spl}}_p
=\mathrm{Fun}(\mathbb N_0^{\mathrm{disc}},
D(\mathrm{Liq}_p(\mathbb R))),
$$

whose morphisms and cochain differentials preserve **each** quantum weight. Its completed Weiss theorem is valid in this declared category; it must not be promoted to an equivalence of all B.5 or B.6 objects.

## 2. FC-0A: a continuous filtered automorphism omitted by CF-001

Take $A=\mathbb R[[x]]$ with tail filtration $F^NA=x^N\mathbb R[[x]]$. The substitution

$$
f(x)=x+x^2
$$

is an invertible continuous **filtration-preserving** algebra map: any input divisible by $x^N$ stays divisible by $x^N$, and a power series with invertible linear coefficient has a unique formal compositional inverse.

Yet $f$ sends weight one to the sum of weights one and two. No **diagonal-only** map in $\mathcal{CF}^{\mathrm{spl}}_p$ realizes $f$. Thus the *canonical* weightwise inclusion of CF-001 into the full complete filtered algebraic category is **not full**, already on one formal coordinate. This refutes that proposed comparison, not all abstract possible equivalences.

## 3. FC-0B: higher-weight differential and derived obstruction

Define a two-term complex with $a$ in cohomological degree $0$, $b$ in degree $1$, and

$$
d(a)=b,\qquad d(b)=0.
$$

Install the decreasing filtration

$$
F^0C=C,\quad F^1C=\mathbb Rb,\quad F^2C=0.
$$

This is a finite, separated, complete filtration by subcomplexes. Its **total** cochain complex is acyclic, whereas its associated graded has zero differential:

$$
\mathrm{gr}^0_F C=\mathbb Ra[0],
\qquad
\mathrm{gr}^1_F C=\mathbb Rb[-1].
$$

Therefore $H^0(\mathrm{gr}^0_F C)=\mathbb R$ and $H^1(\mathrm{gr}^1_F C)=\mathbb R$, while $H^*(C)=0$.

Any strictly weight-preserving split complex with equivalent associated graded has nonzero total cohomology, because its weight components are subcomplexes and their total is a **finite direct sum**. Any zigzag of associated-graded quasi-isomorphisms between finite filtered complexes induces a total quasi-isomorphism, by finite-filtration induction. Hence **no such zigzag** identifies $C$ with a strictly weight-preserving split complex.

**Conclusion FC-0B:** CF-001 is **not essentially surjective** onto the finite complete filtered derived category with associated-graded weak equivalences. Admitting off-diagonal *maps* alone will not cure the obstruction; differentials must also be allowed to raise weight.

## 4. FC-1: exact finite-dimensional triangular equivalence

Fix finite weight length $L$. Let $\mathrm{Fil}_{\mathrm{fin},L}(\mathbb R)$ be bounded cochain complexes of finite-dimensional real vector spaces with a decreasing finite filtration $F^0C=C$, $F^LC=0$ by subcomplexes and filtration-preserving cochain maps.

Define $\mathrm{TriDG}_{L}(\mathbb R)$:

- **Objects:** graded real vector spaces $V_i^q$ ($0\le i<L$), finite-dimensional in every cohomological degree, and degree-one maps $D_{ji}:V_i\to V_j[1]$ for $j\ge i$, satisfying

  $$
  \sum_{i\le j\le k}D_{kj}D_{ji}=0
  \qquad (i\le k).
  \tag{T1}
  $$

- **Morphisms:** degree-zero matrices $f_{ji}:V_i\to W_j$ with $j\ge i$, satisfying $D_Wf=fD_V$.

- **Composition:**

  $$
  (g\circ f)_{ki}
  =
  \sum_{i\le j\le k}g_{kj}f_{ji}.
  \tag{T2}
  $$

The realization sends such a matrix complex to $\bigoplus_i V_i$ with differential $D$ and filtration $F^n=\bigoplus_{i\ge n}V_i$.

**Theorem FC-1 (ordinary finite filtered equivalence).** This realization is an equivalence of categories

$$
\mathrm{TriDG}_{L}(\mathbb R)
\simeq\mathrm{Fil}_{\mathrm{fin},L}(\mathbb R).
\tag{T3}
$$

It preserves and reflects **associated-graded quasi-isomorphisms** and hence induces an equivalence of their relative localizations.

**Proof.** The matrix condition (T1) is exactly $D^2=0$ and $D_{ji}=0$ for $j<i$ is exactly preservation of the decreasing filtration. A linear map between realized objects preserves filtration exactly when its matrix is upper-triangular, and it is a cochain map exactly when it commutes with $D$. This establishes **full faithfulness**. Given a target object, choose real-linear complements to each filtration inclusion $F^{i+1}C^q\subset F^iC^q$ in each cohomological degree. This splits the **underlying graded vector space**, yielding an upper-triangular (not necessarily diagonal) differential. The realized object is isomorphic to the original filtered cochain complex, giving essential surjectivity. Under this identification the associated-graded differential is the diagonal block $D_{ii}$, so the weak equivalences and their localizations agree. $\square$

**Finite analytic coefficient case.** Finite-dimensional real vector spaces realize as finite free p-liquid real modules, for which the liquid tensor and ordinary tensor agree and no higher Tor appears. Consequently FC-1 gives an exact finite-free coefficient bridge to the **underlying algebraic finite-dimensional B.5 sector**. On finite-dimensional standard differentiable vector spaces, real-linear maps are smooth. No equivalence of infinite-dimensional differentiable pro-cochains is inferred.

## 5. FC-2: Weiss descent propagates across finite filtrations

The full comparison requires a theorem that does **not** assume a weight-preserving differential. The following result is one such theorem.

**Theorem FC-2 (finite-filtered Weiss propagation).** Let $\mathcal C$ be any stable cocomplete infinity-category, and let $X$ be a covariant assignment from Euclidean opens to **filtered objects of length $L$** of $\mathcal C$, with filtration-preserving structure maps. Suppose every associated-graded assignment

$$
U\longmapsto
\mathrm{gr}^i_FX(U)
=
\mathrm{cofib}\bigl(F^{i+1}X(U)\to F^iX(U)\bigr),
\qquad 0\le i<L,
$$

satisfies Weiss homotopy-cosheaf descent. Then the **entire filtered assignment** satisfies Weiss descent in the finite filtered category (whose colimits are computed levelwise).

**Proof.** For a Weiss cover, form the canonical augmented Čech comparison $c$ in the category of finite filtration diagrams. It is a morphism of filtered objects. Evaluation at any filtration stage commutes with colimits because the diagram-category colimits are levelwise. In a stable category the cofiber functor is exact and preserves colimits, so $\mathrm{gr}^i_F(c)$ is precisely the Čech comparison for $\mathrm{gr}^i_FX$, hence an equivalence by hypothesis. The exact triangles

$$
F^{i+1}X\longrightarrow F^iX\longrightarrow\mathrm{gr}^i_FX
$$

and downward induction from $F^LX=0$ show that $F^i(c)$ is an equivalence for every $i$. Thus $c$ is a filtered equivalence. $\square$

**Consequence.** FC-2 tolerates off-diagonal and filtration-raising differential components $D_{ji}$ with $j>i$—including the nontrivial example FC-0B—provided they define a compatible filtered prefactorization/cosheaf assignment and its associated graded has Weiss descent. This is a precise **derived local-to-global propagation principle**, not a requirement that the differential split. It proves only Weiss descent; coherent disjoint-open multiplication, complete tensor, and continuity must still be checked separately.

**A completed extension, conditional on the declared target.** Suppose a completion category takes objects with truncations $X/F^NX$, declares its completed Čech homotopy colimit by quotientwise Čech colimits followed by the derived inverse limit, and detects equivalences on all finite quotients. If every quotient is a finite-filtered assignment satisfying the hypotheses of FC-2, then the completed object has Weiss descent **in that declared target**. This is a formal, conditional theorem: it does not identify the completed target with Costello–Gwilliam B.6 or prove preservation of analytic smooth multilinear structures.

## 6. The next infinite-dimensional construction

For an infinite complete *underlying graded-split* object $X=\prod_{i\ge0}X_i$ one can specify an upper-triangular differential $D_{ji}:X_i\to X_j[1]$, $j\ge i$, with every finite truncation satisfying (T1), and upper-triangular filtration-preserving morphisms satisfying $D_Yf=fD_X$. In every fixed quotient $X/F^N$ all sums and products of blocks are finite. This defines a **coefficientwise computable** enriched-matrix presentation of complete filtered objects **when compatible underlying graded splittings exist**.

Unlike CF-001, the enlarged triangular category does **not** generally compute colimits componentwise on diagonal weights. Therefore the CF-001 weightwise Weiss proof cannot simply be copied after broadening morphisms and differentials. Nor does every filtration of nuclear Fréchet or LF spaces split continuously or satisfy the differentiable cofibration and smooth-multilinear requirements of B.6.

**Open theorem target:** construct a stable complete filtered p-liquid category with genuinely filtration-preserving morphisms, derived completed tensor and completed Čech colimits; prove Weiss descent for the smooth-kernel free BV assignment *in that larger category*; then compare analytic nuclear/strict filtrations with Costello–Gwilliam's differentiable pro-cochain model. If a functor fails to preserve smooth mapping structures or derived filtrations, exhibit its exact obstruction.

This is a more faithful next boundary than attempting to assert a full equivalence from matching filtered quotients alone.

## 7. Evidence, tests, priority limits

| Claim | Status |
| --- | --- |
| FC-0A excluded filtered automorphism | Direct proof; elementary formal-series mathematics |
| FC-0B filtered-acyclic versus graded-nonacyclic obstruction | Direct proof; elementary filtered homological algebra |
| FC-1 finite-dimensional triangular dg equivalence | Direct proof; classical finite linear algebra |
| FC-2 Weiss descent propagation across a finite filtration | Direct stable-category proof; applies to off-diagonal differentials |
| Finite free p-liquid coefficient correspondence | Published liquid module formalism |
| Infinite triangular matrix data under chosen graded splitting | Explicit candidate; no general descent or fully faithful functor proved |
| Full Costello–Gwilliam differentiable pro-cochain analytic equivalence | **OPEN** |
| Original mathematical priority, new QFT prediction, renormalization | **NOT CLAIMED** |

**Exact regression:** \`python3 research/condensed-qft/fixtures/triangular_filtered_comparison.py\` checks formal power-series inversion modulo increasing powers, the acyclic/graded cohomology mismatch, triangular matrix composition and square-zero conditions over the rational numbers. It is a finite adversarial control, not an analytic proof.

**Primary sources:** [Costello–Gwilliam, Volume 1, B.5–B.6](https://ncatlab.org/nlab/files/CostelloGwilliam-FactorizationAlgebras.pdf), especially B.5.0.3, B.5.0.4–B.5.0.6, B.6.0.7–B.6.1.1; [Scholze, *Lectures on Analytic Geometry*, Theorem 6.5](https://people.mpim-bonn.mpg.de/scholze/Analytic.pdf); [Clausen–Scholze, *Condensed Mathematics and Complex Geometry*, Thm. 4.11/Remark 4.12](https://people.mpim-bonn.mpg.de/scholze/Complex.pdf).
