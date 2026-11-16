# EXT-015 REACH / 193 — source-locked critical verification of zero-energy hidden means and the disconnected Wick control

**Mathematical disposition: BOUNDED ACCEPT of the frozen primary192 within its expressly specified original-source subclasses; all-history membership and residual W acyclicity remain OPEN.** Verifier V193 and Adversary A193 are logically distinct source-bound passes carried out by the same ChatGPT/GitHub account. This is not an independently authenticated nonauthor APPROVED review, external referee report or MATHCERT mathematical certification.

## 1. Immutable source and review questions

The exact frozen primary is [ZERO_ENERGY_SOURCE_MECHANISM_AUDIT_192.md](ZERO_ENERGY_SOURCE_MECHANISM_AUDIT_192.md), Git blob 6003987b03980ae65ead3e286109be1eed02c8c7, on branch research/reach-zero-energy192-primary-frozen-20261115 at exact commit 311ab74479dd2104de623bf597ec945e06236a64. Its parent protected input is c999e3090f2483b5ee85a63dfaf35f09aa9cc290; the source remains separate from the unmerged working branch and this reviewing document. No earlier draft or stale head substitutes for this blob.

The original mathematical contracts used are scalar105 (Git blob a8ce66ff0edec33e2aff299550fca2089d671033), completed mixed histories108 (587c15fd6e24f6e6b14de574ff878221cdbd5cb6), parameter rows126 (5b05c6147d237ca1d22e4dcbce9262b0f038c163), first Green core165 (24b82716d41d309438fcb7a97bbacab0b724afde), Gaussian-width independence180 (fac58764ac29e518ac522e0451a9c9829e86720b), polynomial183 (e1d6473ac075b0e17eb354603b25b94d1208be19), and the separately admitted canonical nonpolynomial186–188 / network energy189–191. The protected double-Gaussian mean supplement DOUBLE_GAUSSIAN_HIDDEN_MEAN_SOURCE_186.md is a *different* manuscript from canonical NONPOLYNOMIAL_GAUSSIAN_SOURCE_AUDIT_186.md; its original source was read back from PR3352, exact merge 3dc09319b417272b3c1ec35b74e2bb30392e5c31 and Git blob 7985fec06cb3134110b16afa4aa4fc5b71444341. The supplementary critic/ledger is separately undergoing PR3354 admission; none of the canonical 187–191 result numbers is reassigned.

The critic tests four nontrivial items independently: the true weighted-mean R1 cone and rapid-tail decomposition; the static-target microlocal compactness lemma; the exact terminal-source obstruction with no hidden Gaussian inverse; and the legality and nonrapid defect of the disconnected Wick source.

## 2. V193 — reconstruct the weighted-mean cone/rapid decomposition

Use the actual fixed two-edge history with original R1 coefficient F on physical coordinates (x,y,h), terminal independent retained coordinate z and distinct fixed positive widths a,b. Set

$$
d=(a^2+b^2)^{1/2},\quad c=ab/d,\quad
\alpha=a^2/d^2,\quad\beta=b^2/d^2,\quad
u=\beta y+\alpha h,\quad v=y-h.
\tag{193.1}
$$

The absolute coordinate Jacobian is 1. Completing the square gives normalized Gaussian identity $\kappa_{a\epsilon}(z-y)\kappa_{b\epsilon}(z-h)=\kappa_{c\epsilon}(z-u)\kappa_{d\epsilon}(v)$. This identity is used only on already typed original physical vertices. The result does not declare the weighted mean to be an original physical vertex-forgetting operation or a new R1 coefficient stage.

For an output forbidden covector (tau,-tau) at x=u, its pullback at fixed v is (tau,-beta tau,-alpha tau) in (x,y,h). When x=u and v=0, these are conormal to the original three-vertex diagonal: their sum vanishes and all three coordinates coincide. The original closed permitted cone excludes those directions. Compact normalized covector spheres and the closed graph cone give a positive angular separation on a small fixed neighborhood in (x,u,v). Choose a fixed smooth v cutoff theta equal to one near zero. Its near-zero part W has wavefront avoiding a fixed forbidden output cone and moderate off-cone Sobolev estimates; this uses the actual noncharacteristic pushforward estimates of108, not a postulated exact-cone map for all v.

On the complementary v support with distance delta greater than zero from zero, every differentiated Gaussian factor has a fixed power of epsilon inverse times an exponential of negative delta-squared over a positive constant times epsilon-squared. The evaluated complete coefficients have one fixed negative Sobolev order and polynomial regulator moderation per derivative. After multiplication and proper pushforward, the far-v output R is therefore O(epsilon^L) in **one finite Sobolev order for every L**. The same fixed cutoffs, widths, original compact support and original graph cone work for each parameter row; finite fixed seminorm estimates extend to the projective completed coefficient stage. This is the key distinction from an unproved decomposition in which the Sobolev order grows with desired rapidness.

**V193 PASS Proposition192.1 with its terminal factorization, original closed R1 cone, actual complete stage and retained-z independence hypotheses.** It is NOT exact positive-regulator effective R1 preservation: the already protected separate double-mean example has a forbidden effective cone arising from v separated from zero, and is correctly absorbed by the rapid part.

## 3. A193 — dyadic proof of the static forbidden-wavefront lemma

Suppose a fixed compact distribution U is expressed locally as W_epsilon+R_epsilon, with W moderate in all positive Sobolev orders microlocally outside one fixed cone and R rapid in one fixed negative Sobolev order H^{-t}. Let B be an order-zero properly supported cutoff outside that cone, and Delta_j a dyadic frequency shell. Then there exist finite N_m, and for every L a constant C_L, such that

$$
\|\Delta_j BU\|_{L^2}
\le C_m2^{-jm}\epsilon^{-N_m}
  +C_L2^{jt}\epsilon^L.
\tag{193.2}
$$

For any requested output H^q norm, choose m above 2q+4 and a small positive gamma such that gamma times max(N_m,0) is less than m/2. Evaluate the identity at epsilon=2^{-gamma j} (allowed because **U is static**). The first right term decays faster than 2^{-j m/2}, enough for H^q summation. Choose L so that gamma L exceeds t+q+2; the second is also summable. Since q was arbitrary, BU is smooth. This proof does NOT assert a uniform negative-Sobolev inverse Gaussian operator or infer the claim from the weak limit alone. It requires off-cone bounds for every fixed m, one fixed t for all rapid powers, and an epsilon-independent target U. Those conditions cannot be dropped.

**A193 PASS Lemma192.2.** Applied to the *static* forced target width coefficient f(x) delta_0(u) from protected180, it excludes the nonzero (tau,-tau) diagonal wavefront. The argument excludes exact equality for the actual finite terminal two-hidden-mean histories of192.2, including finite transferred terminal derivatives, but does **not** establish modulo-rapid nonmembership: Gaussian deconvolution of a rapid output may be super-polynomially unbounded. It also does not cover truly retained-output scalar multipliers or nonidentity partitions. **A193 PASS Corollary192.3 in that exact bounded scope, not as a universal 108 source theorem.**

## 4. V193/A193 — independent construction and hostile controls for the disconnected Wick source

The original R1 coefficient used in192.9 is a fixed compact smooth cutoff times delta_0(y) on independent physical vertices (x,z,y). Its wavefront carries only a y covector; at a full or partial vertex partition, a conormal has the required zero sum within each collision block, so a pure nonzero y covector cannot be a forbidden partition conormal. Both scalar factors P_{b epsilon}(x-y) and kappa_epsilon(z-y) are actual original105 Wick/Gaussian edges. Product, fixed scalar cutoff, independent R1 simple tensor and proper forgetting are the typed original108 maps, with no illegal multiplication of two singular counterterms. In the front chart x-y=epsilon X, P_{b epsilon}(epsilon X)=epsilon P_b(X) is exact; strict faces have the unregulated absolute cusp plus an exponentially flat smooth tail. This supplies fixed front/strict indices and finite stage/126 parameter maps, rather than mere smoothness for positive epsilon. The exact output is

$$
\widetilde A_\epsilon(x,z)
=\chi(x)P_{b\epsilon}(x)\rho(z)\kappa_\epsilon(z).
\tag{193.3}
$$

The weak limit is rho(0) f(x) delta_0(z), with the same forbidden diagonal wavefront as the unresolved core. Thus any statement asserting that **all** admitted completed sources have permitted-R1 leading physical wavefront is already false in this actual simple-tensor sector.

The difference from the first core is exactly

$$
D_\epsilon=\chi(x)\bigl(P_{b\epsilon}(x)-e(x)\bigr)
\rho(z)\kappa_\epsilon(z).
\tag{193.4}
$$

Since $\partial_t P_{b\epsilon}(t)$ is smooth and e(t)=|t|/2 is not, the difference has a cusp for every positive regulator. The heat-semigroup identity provides the exact formula

$$
P_{b\epsilon}-e
=\int_0^{b^2\epsilon^2/2}\kappa_{\sqrt{2s}}\,ds,
\qquad
\int_{\mathbb R}(P_{b\epsilon}-e)(x)\,dx=b^2\epsilon^2/2.
\tag{193.5}
$$

For a fixed smooth compact test equal to one around the joint corner, Gaussian tails are flat away from the origin, and its pairing with D has leading coefficient b^2 rho(0) epsilon^2/2 plus O(epsilon^4). The leading coefficient is nonzero because b>0 and rho(0) is nonzero. Therefore D is **not** uniformly rapid in any fixed negative Sobolev order; matching the weak limit does not settle source membership modulo rapid. Under the joint scaling (x,z)=(epsilon X,epsilon Z), the nonzero profile is (P_b(X)-e(X))K(Z) multiplied by the true cutoffs, exactly as192.14. Its first fixed-test coefficient is a delta at both slots, but the whole profile is not replaced by that coefficient or an unbounded formal jet series.

**V193/A193 PASS the admitted disconnected Wick history, the exact difference identity, and the nonrapid joint-profile classification.** The equivalence between source status of A and D is an algebraic consequence of the actually admitted tilde A, both exactly and at the level of existence of a representative modulo the *unchanged* rapid ideal.

## 5. Hostile interpretations rejected and bounded decision

| Question | V193/A193 verdict |
| --- | --- |
| Exact weighted Gaussian mean on an actual finite legal two-bridge history | ACCEPT, without declaring the weighted mean an original vertex map |
| Near-zero-energy effective R1-cone moderate part plus fixed-order rapid tail | ACCEPT, conditional on original closed cone and all fixed source-stage hypotheses |
| Static singular target wavefront forced by a rapidly small defect | EXCLUDED by dyadic microlocal estimate; static-target hypothesis essential |
| Terminal independent-retained-z double-mean histories exactly equal the first core | EXCLUDED; not an arbitrary rapid-output no-go |
| Actual disconnected Wick source with the same forbidden leading weak limit | CONSTRUCTED and source-typed within105/108/126 |
| Nonrapid positive-regulator joint defect and exact source equivalence | ACCEPT, with mass b^2 epsilon^2/2 and fixed-test control |
| General retained-z scalars, nonidentity partition jets, arbitrary Wick/PHG source histories | OPEN |
| Exact or modulo-rapid source membership of D or A, universal150.L, residual W acyclicity, originalR3, full126.14, higher weights, lifting, M5/R4 | OPEN |

**Review decision: BOUNDED ACCEPT of exact frozen primary192 with zero author corrections**, subject to independent editorial integration, native protected admission and exact protected-main blob readback. One logical same-system review does not certify universal mathematics.

The next scientific target is a real source-level treatment of the nonrapid defect D with its full joint corner profile, not repetition of the false leading-wavefront invariant. Any proof of exclusion must cover permitted nonidentity partition histories and genuinely nonterminal 105 stages, or explicitly state a smaller class. Any proof of admission must construct one full original108 completed source with fixed all-face scalar indices, legal R1 cone, proper density, source-controlled126 rows, and no illicit infinite jet/inverse heat operation.

## Additional distinct-context source review

A separate nonauthor agent context also returned BOUNDED ACCEPT of the unchanged primary with zero corrections. Its exact review and ledger are preserved at commit 1dae27be574c9cb1e08e7a067d3e93a8ee73a762 on research/reach-zero-energy192-review-frozen-20261115, at this same review path. This context shares the Codex system and historical dependencies; it is not external certification. It explicitly restricts terminal derivatives to those transferred into compact effective inputs while retaining the common outer multiplier. The canonical source-bound V193/A193 review above is retained, and both conclusions agree. Concurrent branch updates were reconciled without replacing either frozen review record.
