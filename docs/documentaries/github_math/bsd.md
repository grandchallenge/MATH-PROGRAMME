# The Hidden Music of Elliptic Curves

**Source status:** Open Millennium Prize Problem · BSD-001 · No proof claimed.

> **GitHub equation reader; automatically generated from the original manuscript.**
> The [illustrated documentary](../bsd.md) has the canonical layout, figures and reader controls.
> This is not independent mathematical or publication certification.

A note to the reader

## Exact objects first; the open boundary always visible

Birch and Swinnerton–Dyer links the rational-point structure of an elliptic curve to the behaviour of its $L$​-function at $s=1$. The conjecture remains open in general.

This browser edition is a derivative, source-normalized exposition. Its numbered plates render exact mathematical objects, exact finite computations, or quantified theorem structure whenever the adjacent concept permits it. Wolfram Language is the canonical semantic-master language for the revised plates; the committed web graphics are deterministic publication derivatives. The plates are pedagogical, not proof evidence. Definitions, equations, source links, campaign records, and trust labels govern the mathematics.

**Edition status:**

Open Millennium Prize Problem; documentary exposition; no proof claim.

**Open conjecture**

For every elliptic curve $E/\mathbb{Q}$, BSD predicts $\mathop{\mathrm{rank}}E(\mathbb{Q})=\mathop{\mathrm{ord}}_{s=1}L(E,s)$. The universal leading-term formula and general finiteness of $\mathop{\mathrm{Sha}}(E/\mathbb{Q})$ remain open.

**Claim boundary**

Finite computation, parity, Selmer bounds, family averages, one-prime results, $p$​-adic formulas, and analytic-rank-zero-or-one theorems do not by themselves establish the universal complex conjecture.

Chapter I

## Rational points: one exact doorway

An elliptic curve over $\mathbb{Q}$ can be written in short Weierstrass form

$$
E:y^2=x^3+Ax+B,\qquad 4A^3+27B^2\ne0.
$$

**Definition**

An elliptic curve over $\mathbb{Q}$ is a smooth projective genus-one curve equipped with a rational base point. A short Weierstrass model has nonzero discriminant.

Its real points form continuous curves. Its rational points form a finitely generated abelian group, but finding all generators can be difficult.

The congruent-number problem gives a concrete entry point. A positive integer $n$ is the area of a rational right triangle exactly when

$$
E_n:y^2=x^3-n^2x
$$

has a rational point of infinite order. For $n=5$, the exact point

$$
P=\left(\frac{25}{4},\frac{75}{8}\right)
$$

lies on $E_5:y^2=x^3-25x$ and corresponds to a rational right triangle with sides $3/2$, $20/3$, and $41/6$. Its area is exactly $5$.

**Finite-window guardrail**

Displaying a real curve and one rational point does not determine the Mordell–Weil rank and does not prove BSD.

> **Plate I.** Plate I The ancient question of rational solutions Fallback predecessor plate. With JavaScript enabled, the reviewed exact-object successor is activated at this stable source reference. [Illustration](../../assets/documentaries/bsd/plate_curve.svg). *Alt text:* An illustrated map from rational right triangles and cubic curves to sparse rational points, torsion, rank, and the limits of finite search.

Chapter II

## The chord–tangent group law

A nonsingular cubic carries an addition law. A line through two points meets the cubic a third time; reflecting that third intersection across the horizontal axis gives the sum. A tangent supplies doubling.

Plate II fixes one exact rational example on

$$
E:y^2=x^3-x+1.
$$

The points $P=(0,1)$ and $Q=(1,1)$ lie on $E$. Their horizontal chord $y=1$ meets $E$ again at $R=(-1,1)$. Reflection gives

$$
P+Q=-R=(-1,-1).
$$

**Established theorem · Mordell–Weil**

$E(\mathbb{Q})\cong\mathbb{Z}^r\oplus E(\mathbb{Q})_{\mathrm{tors}}$. The integer $r$ is the algebraic rank.

Canonical heights measure the independent free directions. The determinant of their height pairing is the regulator that appears in the strong BSD formula.

> **Plate II.** Plate II Two ledgers in the same hand Fallback predecessor plate. With JavaScript enabled, the reviewed exact chord–tangent successor is activated at this stable source reference. [Illustration](../../assets/documentaries/bsd/plate_harmony.svg). *Alt text:* A paired arithmetic and analytic panorama links the Mordell–Weil group of rational points to the vanishing of an elliptic-curve L-function.

Chapter III

## Counting at a good prime

Reduce a suitable integral equation modulo a prime $p$. At a prime of good reduction define

$$
a_p=p+1-\#E(\mathbb{F}_p),
$$

and

$$
L_p(E,s)=\left(1-a_pp^{-s}+p^{1-2s}\right)^{-1}.
$$

For $E_5:y^2=x^3-25x$ at $p=13$, exact enumeration gives $19$ affine solutions. Including the point at infinity,

$$
\#E_5(\mathbb{F}_{13})=20,\qquad a_{13}=13+1-20=-6.
$$

Hence

$$
L_{13}(E_5,s)=\left(1+6\cdot13^{-s}+13^{1-2s}\right)^{-1}.
$$

The finite sample in Plate III is exact for the displayed primes. It is not an estimator of rank.

**Imported established result · modularity**

Every elliptic curve over $\mathbb{Q}$ is modular. Its $L$​-function therefore has analytic continuation and a functional equation centred at $s=1$.

> **Plate III.** Plate III From prime counts to the central point Fallback predecessor plate. With JavaScript enabled, the reviewed exact finite-field successor is activated at this stable source reference. [Illustration](../../assets/documentaries/bsd/plate_bridge.svg). *Alt text:* Prime-by-prime point counts are assembled into Euler factors and an L-function whose behaviour at the central point is compared with rank.

Chapter IV

## The strong BSD ledger

The rank statement is

$$
\mathop{\mathrm{rank}}E(\mathbb{Q})=\mathop{\mathrm{ord}}_{s=1}L(E,s).
$$

The strong form predicts the first nonzero Taylor coefficient as an arithmetic factorization. If $r=\mathop{\mathrm{rank}}E(\mathbb{Q})$ and $\mathop{\mathrm{Sha}}(E/\mathbb{Q})$ is finite, then under the displayed normalization,

$$
\frac{L^{(r)}(E,1)}{r!}=\frac{\Omega_E\,\mathop{\mathrm{Reg}}(E/\mathbb{Q})\,\#\mathop{\mathrm{Sha}}(E/\mathbb{Q})\,\prod_p c_p}{\#E(\mathbb{Q})_{\mathrm{tors}}^2}.
$$

The factors have different jobs. $\Omega_E$ is an archimedean period; the regulator measures the Mordell–Weil lattice; $c_p$ records bad-prime component data; torsion contributes a finite denominator; and $\mathop{\mathrm{Sha}}$ measures locally soluble torsors that may fail globally.

**Three obligations, not one slogan**

Rank equality, finiteness of $\mathop{\mathrm{Sha}}$, and the normalized leading-term identity are logically distinct. Establishing one does not silently establish the others.

> **Plate IV.** Plate IV The strong BSD ledger Fallback predecessor plate. With JavaScript enabled, the reviewed quantified dependency successor is activated at this stable source reference. [Illustration](../../assets/documentaries/bsd/plate_overture.svg). *Alt text:* A decorative ledger surrounds the leading-term formula with period, regulator, Tamagawa, torsion, and Tate–Shafarevich contributions.

Chapter V

## The exact theorem frontier

The frontier is governed by quantifiers and scope. Mordell–Weil finite generation and modularity hold for every elliptic curve over $\mathbb{Q}$. Through modularity, Gross–Zagier, and Kolyvagin, the established analytic rank zero or one terrain gives matching algebraic rank and finite $\mathop{\mathrm{Sha}}$.

The higher-rank and universal leading-term frontier remains open: rank equality for every elliptic curve over $\mathbb{Q}$, general finiteness of $\mathop{\mathrm{Sha}}$, and the complete normalized complex leading-term formula.

**Established low-rank terrain**

Analytic rank $0$ or $1$ yields the matching Mordell–Weil rank and finite $\mathop{\mathrm{Sha}}$ for elliptic curves over $\mathbb{Q}$.

**Still open universally**

For every elliptic curve over $\mathbb{Q}$: equality of algebraic and analytic rank, finiteness of $\mathop{\mathrm{Sha}}$, and the complete complex leading-term formula.

> **Plate V.** Plate V Islands of theorem, ocean of conjecture Fallback predecessor plate. With JavaScript enabled, the reviewed quantified theorem-frontier successor is activated at this stable source reference. [Illustration](../../assets/documentaries/bsd/plate_frontier.svg). *Alt text:* A map distinguishes established modularity and low-rank results from the unresolved higher-rank and universal leading-term frontier.

Technical appendix A

## Elliptic curves and the Mordell–Weil group

For $E:y^2=x^3+Ax+B$, the discriminant is $\Delta=-16(4A^3+27B^2)\ne0$. The projective point $O=[0:1:0]$ is the identity.

For distinct $P=(x_1,y_1)$ and $Q=(x_2,y_2)$ with $x_1\ne x_2$,

$$
m=\frac{y_2-y_1}{x_2-x_1},\qquad x_3=m^2-x_1-x_2,\qquad y_3=-y_1+m(x_1-x_3).
$$

Then $P+Q=(x_3,y_3)$. Associativity belongs to the algebraic-group structure; the chord picture alone is not its proof.

For a basis $P_1,\ldots,P_r$ of the free part, the canonical height pairing gives

$$
\mathop{\mathrm{Reg}}(E/\mathbb{Q})=\det\bigl(\langle P_i,P_j\rangle\bigr),
$$

with empty determinant $1$ when $r=0$.

Technical appendix B

## The $L$​-function and analytic rank

The Euler product converges absolutely initially for $\mathop{\mathrm{Re}}(s)>3/2$. Modularity identifies it with the $L$​-series of a weight-two newform. A standard completed normalization is

$$
\Lambda(E,s)=N^{s/2}(2\pi)^{-s}\Gamma(s)L(E,s),
$$

satisfying $\Lambda(E,s)=w_E\Lambda(E,2-s)$. The analytic rank is

$$
r_{\mathrm{an}}(E)=\mathop{\mathrm{ord}}_{s=1}L(E,s).
$$

The root number gives $(-1)^{r_{\mathrm{an}}}=w_E$. This is analytic parity; it is not by itself algebraic rank equality.

Technical appendix C

## The strong formula and normalization discipline

Authors distribute real periods, archimedean factors, completed-function terms, and local conventions differently. A comparison must reconcile those conventions before comparing symbols or numbers.

**Normalization guardrail**

A missing period component, factorial, torsion square, bad-prime factor, or completed-function term can create a false disagreement—or a false proof. Symbol matching is not normalization matching.

The phrase “BSD is true for this curve” must identify whether it means rank equality, finite $\mathop{\mathrm{Sha}}$, the full complex leading term, a $p$​-part, or a computational certificate for a fixed curve.

Technical appendix D

## Selmer groups, descent, and the hidden term

Kummer theory yields

$$
0\longrightarrow E(\mathbb{Q})/nE(\mathbb{Q})\longrightarrow \mathop{\mathrm{Sel}}_n(E/\mathbb{Q})\longrightarrow \mathop{\mathrm{Sha}}(E/\mathbb{Q})[n]\longrightarrow0.
$$

For a prime $p$,

$$
0\longrightarrow E(\mathbb{Q})\otimes\mathbb{Q}_p/\mathbb{Z}_p\longrightarrow \mathop{\mathrm{Sel}}_{p^\infty}(E/\mathbb{Q})\longrightarrow \mathop{\mathrm{Sha}}(E/\mathbb{Q})[p^\infty]\longrightarrow0.
$$

Descent converts an infinite search into finite covering and local-solubility problems and can give an upper bound on rank. The bound is sharp only after the relevant Tate–Shafarevich contribution is controlled.

**Selmer guardrail**

Selmer corank is not automatically Mordell–Weil rank. A nontrivial $p$​-primary Tate–Shafarevich contribution may remain.

Technical appendix E

## Known results and claim-level trust matrix

| Claim | Trust class | Qualification |
| --- | --- | --- |
| $E(\mathbb{Q})$ is finitely generated | established | Mordell–Weil theorem |
| Every elliptic curve over $\mathbb{Q}$ is modular | imported established | supplies continuation and functional equation |
| Analytic rank $0$ or $1$ gives matching algebraic rank and finite $\mathop{\mathrm{Sha}}$ | imported established | exact low-rank terrain |
| Universal rank equality | open | no finite computation, parity theorem, or family result promotes it |
| Universal finiteness of $\mathop{\mathrm{Sha}}$ | open | separate from rank equality |
| Universal complex leading-term formula | open | requires every normalization and arithmetic factor |
| A fixed-curve rigorous computation | bounded evidence or certificate | does not imply the universal statement |
| A $p$​-adic or one-prime theorem | hypothesis-sensitive theorem terrain | not identical to the global complex formula |
| Exact-object documentary plates | pedagogical | reproducible representation; never proof evidence |

**Final claim boundary**

This web edition changes presentation, not theorem strength. It does not prove BSD, provide a new reduction, independently verify the complete literature, or make a novelty or priority claim.

Sources and programme crosswalk

## Governing literature and campaign record

Andrew Wiles, [The Birch and Swinnerton–Dyer Conjecture](https://www.claymath.org/wp-content/uploads/2022/05/birchswin.pdf), official Millennium Problem description.

B. J. Birch and H. P. F. Swinnerton-Dyer, [“Notes on elliptic curves II”](https://doi.org/10.1515/crll.1965.218.79) (1965).

Christophe Breuil, Brian Conrad, Fred Diamond, and Richard Taylor, [“On the modularity of elliptic curves over $\mathbb{Q}$”](https://doi.org/10.1090/S0894-0347-01-00370-8) (2001).

Benedict Gross and Don Zagier, [“Heegner points and derivatives of $L$​-series”](https://doi.org/10.1007/BF01388809) (1986).

V. A. Kolyvagin and D. Yu. Logachev, [“Finiteness of the Shafarevich–Tate group and the group of rational points for some modular abelian varieties”](https://www.mathnet.ru/eng/aa47) (1989/1990).

[Clay Mathematics Institute: Birch and Swinnerton–Dyer Conjecture](https://www.claymath.org/millennium/birch-and-swinnerton-dyer-conjecture/).

Programme links: [Domain 04](../../domains/birch_swinnerton_dyer/) · [canonical master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_04_BIRCH_SWINNERTON_DYER_MASTER_PLAN.md) · [campaign artifacts](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/birch_swinnerton_dyer) · [review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/birch_swinnerton_dyer)

## Edition record

This browser edition uses exact-object-first visual pedagogy. The revised BSD plate sequence is bound to a Wolfram Language semantic master, deterministic static delivery assets, and the stable-source activation resolver.

The web edition is derivative. The committed pointer is a source record; the checksum-locked complete illustrated source bundle is the authoritative source artifact. MathJax 3.2.2 is a version-pinned network enhancement, and the source TeX remains present when it is unavailable.

**Web claim boundary:** Browser-native, source-normalized exposition of rational points, the Mordell–Weil group, the Hasse–Weil L-function, low-rank theorem terrain, and the strong BSD formula. Numerical agreement, parity, Selmer bounds, family results, one-prime theorems, and p-adic analogues are not promoted to the universal complex conjecture.

[Web-edition data](../bsd.edition.json)[Reusable schema](../documentary_web.schema.json)[Source record](../sources/the_hidden_music_of_elliptic_curves.tex)[Artifact manifest](../ARTIFACT_MANIFEST.json)

Rendered PDF

16,582,087 bytes ·

`36254378e11fd22a067944838341ae04fedbd13e5ea588180023874d7ba49ce9`

·

`metadata_only`

Complete LaTeX source

50,500 bytes ·

`9b7b95702a5305c51e66e026d44ddf3003029808edb3009ed1b2fcbc92e6b2b4`

·

`metadata_only`

Authoritative complete illustrated source bundle

16,995,210 bytes ·

`c0782575453227311630e17c443a4dea08091b3a3824bc23a1af17f5bd0d8377`

·

`metadata_only`
