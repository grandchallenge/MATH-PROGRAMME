# EXT-015 REACH / 184 — critical verification of polynomial retained-Gaussian normal ordering

**Mathematical disposition: BOUNDED ACCEPT of the exact operator identity and conditional source exclusion.** This is a logically separated Verifier V184 and Adversary A184 review by the same model and GitHub account as the producer. It is **not** independent nonauthor APPROVED review, external referee assessment or MATHCERT certification. Protected primary183 custody is an additional requirement.

## 1. Exact source and protected premises

The source under review is [POLYNOMIAL_RETAINED_GAUSSIAN_NORMAL_ORDERING_183.md](POLYNOMIAL_RETAINED_GAUSSIAN_NORMAL_ORDERING_183.md), corrected exact candidate PR3348 head d209060780db840ebaeec1b0f374dc09630531fe, Git blob e1d6473ac075b0e17eb354603b25b94d1208be19. An earlier candidate head 8877bc22a54e0e12a25a5b3d0fa6b17ae72a5ea0 and blob ccffd61b0e69b7ee4ea5e09b97022e1944d2296a failed the native math Markdown boundary validator at three prose/inline-math junctions. The corrected source changes formatting, not mathematics, and requires fresh exact-head checks and protected GitHub merge/readback before this review can claim source custody.

Protected primary180 Git blob fac58764ac29e518ac522e0451a9c9829e86720b and PR3344 native merge 28d978e788c9a1930a00056a0044ae3f4a124469 establish the finite Gaussian-width independence lemma used here, within compact distributional terminal factorization. Source-locked mathematical critic181 blob 6904fbc6b17f7f5ea9492047d5c824c3eddaad86 and ledger182 blob c64d3bc45d9dfcf84b81d562c0ee7cc711d46e6b were read back protected main after PR3346 merge 68fb8a8adc4e672f2284179e5fdb94426ab30351. Original source contracts105,108,126 remain protected and unchanged.

The same-account source-locked PR3348 conversation COMMENT ID 6893777355 checked the first two commutator cases, but does not substitute for this complete bounded review or an external mathematical opinion.

## 2. V184 — verify the distributional Weyl-algebra intertwiner

Let $T_\sigma V(x,z)=\langle V(x,y),\kappa_\sigma(z-y)\rangle$ and $H_\sigma=y-\sigma^2\partial_y$. For $\sigma>0$, the distributional differentiation sign is decisive:

$$
\partial_z\kappa_\sigma(z-y)
=-\partial_y\kappa_\sigma(z-y),\qquad
(z-y)\kappa_\sigma(z-y)
=-\sigma^2\partial_z\kappa_\sigma(z-y).
\tag{184.1}
$$

Integration by parts against a compact distribution then gives, without any source inverse,

$$
z T_\sigma V=T_\sigma H_\sigma V,\qquad
\partial_z T_\sigma V=T_\sigma\partial_y V.
\tag{184.2}
$$

**Independent two-degree control.** For $V=\delta_0$, the right side of the first identity is $-\sigma^2\kappa_\sigma'$, exactly $z\kappa_\sigma$. For degree two, use $\partial_y y=y\partial_y+1$ to obtain

$$
H_\sigma^2
=y^2-2\sigma^2y\partial_y-\sigma^2
+\sigma^4\partial_y^2.
\tag{184.3}
$$

Since $y\delta_0=0$ and $y\delta_0'=-\delta_0$, the distributional outcome is

$$
H_\sigma^2\delta_0
=\sigma^2\delta_0+\sigma^4\delta_0''.
\tag{184.4}
$$

Convolving gives $\sigma^2\kappa_\sigma+\sigma^4\kappa_\sigma''=z^2\kappa_\sigma$ exactly. A naive commuting binomial would lose the nonzero $\sigma^2\delta_0$ correction and is invalid. Induction now proves $z^qT_\sigma V=T_\sigma H_\sigma^qV$ for all fixed finite $q$. With fixed-degree $p(x,z,\epsilon)$ smooth in $x$, each multiplier commutes with $H_\sigma$ and finite linearity gives the correctly ordered operator $p(x,H_\sigma,\epsilon)\partial_y^k$.

**V184 PASS the exact finite polynomial normal-ordering and the required commutator sign.**

## 3. A184 — adversarial source and cone audit

Differentiation and smooth polynomial multiplication in $(x,y)$ do not enlarge distributional wavefront sets and do not enlarge supports. For a finite fixed polynomial and positive $\epsilon$, each effective input is therefore still a compact distribution of finite order in the **original** physical coordinates and inherits the same conic wavefront exclusion as its effective upstream input. This is not a general statement that every legal nonidentity partition inclusion produces an effective R1 coefficient: such an inclusion may create a diagonal jet before polynomial normal ordering. The primary correctly makes the target-width exclusion conditional on the **evaluated effective** upstream cone, not merely on a permitted remote R1 input.

After normal ordering, finite widths are precisely the terminal-factorized form of protected primary180. This establishes a necessary condition for exact local representation: each non-target block vanishes and the target block is $f(x)\delta_0(y)$. If width one is absent, the target is impossible regardless of the source cone. If the width-one effective coefficients all avoid the forbidden $(\tau,-\tau)$ conormal, their sum cannot equal that cusp-times-delta distribution. The result is **not** all-history nonmembership, since the effective-cone hypothesis may fail for a nonidentity partition map. It does not prove rapid-equivalence nonmembership, because exact analyticity/width independence cannot simply be applied after subtracting an arbitrary uniform-rapid family.

The hostile nonpolynomial identity has the correct Gaussian normalization. Put $c^{-2}=a^{-2}+b^{-2}$; multiplying $\kappa_{a\epsilon}(z)$ by $\exp(-z^2/(2b^2\epsilon^2))$ gives $(c/a)\kappa_{c\epsilon}(z)$. This is a genuine analytical width-changing mechanism; it says nothing about whether a nonpolynomial **retained-output scalar** of that form is admitted by the full original 105/108 stages, R1 cone, all heat corners, proper density and 126 derivative rows. Infinite Taylor normal ordering is equally unlicensed without one fixed complete source stage and compatible regulator estimates.

**A184 PASS the bounded exact polynomial terminal theorem; REJECT promotion to arbitrary nonpolynomial scalar stages, arbitrary nonidentity partition jets, modulo-rapid, universal 150.L, residual W acyclicity, full A source verdict, original R3, full126.14, higher weights, lifting or M5/R4.**

## 4. Review decision and successor

| Mathematical claim | V184/A184 decision |
| --- | --- |
| Exact $z^qT_\sigma$ normal ordering, with noncommutative corrections | ACCEPT |
| Finite Hermite derivatives plus fixed-degree retained-output polynomial multipliers | ACCEPT under actual terminal factorization |
| Fixed compact support and cone preservation by this normal-ordering operation | ACCEPT |
| Exact source $A$ with no target-width block | EXCLUDE under terminal polynomial factorization |
| Exact source $A$ with target-width block whose **effective** input has permitted R1 cone | EXCLUDE |
| Arbitrary nonidentity partition maps preserve effective R1 cone | UNPROVED |
| Nonpolynomial Gaussian width-changing scalar is a legal complete original source operation | UNPROVED |
| Uniform rapid quotient, full first-core status, universal 150.L and residual W acyclicity | OPEN |

**Canonical bounded scope: POLYNOMIAL_RETAINED_NORMAL_ORDERING_PROVED__TERMINAL_COMPACT_WIDTH_CLASSIFICATION__EFFECTIVE_R1_CONDITIONAL__NONPOLYNOMIAL_AND_PARTITION_OPEN.** Source-lock ledger185 to the final **protected** primary183 merge and actual Git blob. Continue to genuine nonpolynomial source mechanisms under original all-corner 105/108/126 contracts; avoid an unlimited Taylor expansion or assuming a Green inverse is a legal source operation.
