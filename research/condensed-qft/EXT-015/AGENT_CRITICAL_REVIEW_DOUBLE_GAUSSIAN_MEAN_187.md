# EXT-015 REACH / 187 — critical audit of two-hidden-Gaussian source, mean-map conormal and rapid no-go

**Review disposition: BOUNDED MATHEMATICAL ACCEPT WITH EXPLICIT SCOPES; independent nonauthor certification NOT claimed.** Verifier V187 and Adversary A187 are two source-locked logical passes by the same ChatGPT/GitHub identity. External mathematical refereeing, nonauthor APPROVED and MATHCERT are not represented by this review. Source primary186 must pass its own native protected merge and exact Git blob readback.

## 1. Exact identity and original source premises

Source: [DOUBLE_GAUSSIAN_HIDDEN_MEAN_SOURCE_186.md](DOUBLE_GAUSSIAN_HIDDEN_MEAN_SOURCE_186.md), corrected candidate PR3352 head 8de361b1222d650cfd8b278c204f27b94657be6c, Git blob a310c7b74db07dde683fb722fd16aa3036aa2110. The initial head 9c04d9c3afe705dac989277d43b3513581fd9336 was superseded by a **substantive scope clarification**, then head eb57cf5f3a70e6f6daf987d0eb3e9616e939f4f7 by a Markdown-only correction: the graph-regular rapid no-go assumes the identity partition and excludes new nonidentity partition source-jet inclusions. A critical review must use only the corrected head, not stale checks or the broad initial wording.

Protected inputs: scalar 105 blob a8ce66ff0edec33e2aff299550fca2089d671033, complete 108 blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6, parameter rows126 blob 5b05c6147d237ca1d22e4dcbce9262b0f038c163, joint source165 blob 24b82716d41d309438fcb7a97bbacab0b724afde, one-bridge174 blob 7c470ba092d917dc434a8883e5afaff7bce1dfc6, finite-width180 blob fac58764ac29e518ac522e0451a9c9829e86720b and polynomial183 blob e1d6473ac075b0e17eb354603b25b94d1208be19. Primary183 is protected via PR3348 merge 2af279aff16578031a8cd41aeb05b6e875a265e9; CP193 is protected via PR3349 merge 030344a264a16e8ab465c997981cfb99a281c521. Review184–185 is separately in PR3350 and must not be described as protected until verified.

## 2. V187 — two-edge Gaussian identity, exact physical Jacobian and source typing

For positive widths $a,b$, set $d^2=a^2+b^2$, $c=ab/d$, $\alpha=a^2/d^2$, $\beta=b^2/d^2$. Then $u=\beta y+\alpha h$, $v=y-h$ gives $y=u+\alpha v$, $h=u-\beta v$. The absolute determinant of $(u,v)\mapsto(y,h)$ is $|\!-\alpha-\beta|=1$. Gaussian square completion is exact:

$$
\frac{(z-y)^2}{a^2}+\frac{(z-h)^2}{b^2}
=\frac{(z-u)^2}{c^2}+\frac{v^2}{d^2}.
\tag{187.1}
$$

Both sides' normalized product densities agree because $cd=ab$. Therefore

$$
\kappa_{a\epsilon}(z-y)\kappa_{b\epsilon}(z-h)
=\kappa_{c\epsilon}(z-u)\kappa_{d\epsilon}(v).
\tag{187.2}
$$

This is a **two-edge** calculation on original physical vertices, not a formal external absolute Gaussian anchor. Original105 (105.4 and its finite edge closure), original108 (108.6–108.7), fixed scalar indices and legal proper pushforward admit each finite relative Gaussian edge with fixed cutoffs and an original permitted R1 coefficient. Multiplication by two scalar functions smooth for each positive regulator is not multiplication of two singular source counterterms. The complete projective coefficient stage contains the simple tensor; larger arbitrary completed tensors are not assumed to obey an unverified factorization.

For a smooth-through-zero scalar coefficient depending genuinely on the retained output $z$, the transformed multiplier **cannot** be moved out of the $v$ integral to form a $z$-independent compact input. Primary186 correctly restricts its exact terminal formula to the coefficient that separates from $z$ and proves only a weak-limit statement for the genuinely retained-$z$ smooth class. This distinction is essential.

**V187 PASS** on normalized identity, determinant, actual source grammar for finite relative Gaussian edges and the terminal/separable versus retained-output nonterminal distinction.

## 3. A187 — adversarial full original R1 cone and rapid counterexample

In the counterexample with $a=b=\sqrt2$ and $v=y-h$ separated from zero, the original input is a compact local multiple of

$$
T(x,y,h)=g(x)\psi(y-h)
\delta\!\left(x-\frac{y+h}{2}\right).
\tag{187.3}
$$

At every point of the conormal support, $x=(y+h)/2$ and $y\ne h$; hence $x\ne y$, $x\ne h$ and $y\ne h$. No original three-vertex partition diagonal intersects that nonzero conormal support. With a smooth retained-$z$ cutoff, its conormal has coordinate pattern

$$
(\xi_x,\xi_z,\xi_y,\xi_h)
=(\tau,0,-\tau/2,-\tau/2).
\tag{187.4}
$$

The only possible equality on the support involving the retained $z$ is a single pair $z=x$, $z=y$ or $z=h$ (the remaining three are pairwise distinct); none of those pair-partition conormals has the nonzero other-vertex covectors in (187.4). Therefore the original **four-vertex** R1 partial-partition exclusion still holds, not just the three-vertex version. Fixed compact cutoffs permit one fixed allowed graph cone and physical support. Its terminal mean pushdown, however, is exactly $C_\epsilon g(x)\delta(x-u)$, which has the **forbidden effective two-vertex** $(\tau,-\tau)$ cone. This is a real legal-source counterexample to an unqualified effective-R1 preservation assertion.

The separated support $\delta<|v|<2\delta$ implies $C_\epsilon>0$ for every positive $\epsilon$, but $C_\epsilon$ and every fixed regulator derivative are bounded by inverse powers times $\exp(-\delta^2/(8\epsilon^2))$. The normalized remaining kernel has only polynomial inverse-regulator Sobolev growth; consequently the full output belongs to the **original fixed-order rapid ideal**. This means the effective conormal counterexample is **invisible in the enriched quotient**. An adversary cannot use it as a nontrivial class in residual W or as an exact source of $A$.

**A187 PASS** for an exact positive-regulator conormal failure within a legal R1 source and for its regulator-flat quotient classification. **REJECT** any claim that this counterexample refutes a general quotient-level conormal invariant.

## 4. V187/A187 — separate graph-regular no-go and its true boundary

Theorem186.2 assumes an identity-partition two-bridge source, finite fixed widths, scalar multipliers smooth through regulator zero, and compact coefficients extending through zero in **one fixed permitted R1 normal graph stage**. Under those hypotheses the normalized pair of Gaussian edges is a two-direction approximate identity. The original R1 cone excludes the normal conormal of $y=h$ and the triple partition; thus the pullback $T_0(x,z,z)$ is well-defined and excludes the conormal of $x=z$ by 108 Section4. One can first restrict in the $v=y-h$ direction, then approximate identity in $u$; a smooth retained-$z$ coefficient yields its value on the same diagonal. The output's weak limit is the permitted R1 distribution

$$
\rho(z)m_0(x,z,z,z)T_0(x,z,z).
\tag{187.5}
$$

By contrast, the remaining Green core has weak limit $\rho(0)\chi(x)|x|\delta_0(z)/2$, with forbidden nonzero $(\tau,-\tau)$ at the joint origin. A fixed-order rapid difference has zero weak limit. Hence exact equality **or** equality modulo the original rapid ideal is impossible in this graph-regular identity-partition source class.

The scope conditions are all necessary to the proof. A source including an allowed scalar stage that has a singular zero-scale Green/Wick boundary, negative Laurent poles, or a nonidentity partition jet cannot be tested by automatically taking the smooth trace (187.5). The already **legal** second Green arm in protected168 has the same singular weak leading profile as $A$; thus the mere existence of a cusp-times-delta weak limit is not a *global* source obstruction. The no-go relies on the **restricted R1-only smooth scalar trace**, not an invented universal R1 weak-limit property.

**V187/A187 ACCEPT the restricted modulo-rapid no-go; KEEP OPEN original arbitrary scalar/partition histories and the full first-core source.**

## 5. Bounded critic decision

| Claim | Critical disposition |
| --- | --- |
| Exact two hidden Gaussian product and effective weighted mean | PASS |
| Full original four-vertex R1 legality of off-diagonal mean-conormal example | PASS |
| Effective R1 cone preserved under every legal hidden Gaussian mean map | FALSE, bounded exact counterexample |
| That specific counterexample represents a nonzero enriched rapid-quotient class | FALSE, regulator-flat |
| Graph-regular identity-partition smooth-scalar double bridge represents $A$ modulo rapid | EXCLUDED |
| Full original source $A$, arbitrary nonidentity source jets, genuinely singular scalar stages | OPEN |
| Universal Lemma 150.L, residual W acyclicity, original R3, full126.14, higher weights, lifting, M5/R4 | OPEN |

**Canonical status: TWO_BRIDGE_MEAN_EXACT__POSITIVE_EFFECTIVE_CONE_FAILURE__FLAT_COUNTEREXAMPLE__REGULAR_IDENTITY_PARTITION_RAPID_NO_GO__GENERAL_SOURCE_OPEN.** Ledger188 must bind the protected source186 exact blob and actual merge; same-account mathematical criticism is not external certification. Next substantive189 must test *admitted singular scalar Green/Wick stages with two hidden Gaussian edges and genuinely nonidentity partition jets*, retaining original all-corner stage and 126 contracts.
