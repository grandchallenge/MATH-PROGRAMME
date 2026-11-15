# EXT-015 REACH / 189 — a positive Gaussian network energy diagnostic

**Disposition: conditional source diagnostic.** A finite positive Gaussian network linking the retained cusp coordinate to a different prescribed boundary value has a quantitative energy gap away from the joint corner. For an actually typed compact moderate amplitude, this makes the whole output uniformly rapid on that patch. The first cusp core is nonrapid there. This excludes such a factorization of that core, including modulo the existing rapid relation. It does not classify arbitrary legal histories or disconnected network branches.

## 1. Frozen contract and factorization hypothesis

CP199 binds this primary after protected186–188, exact merge `f71362ef0fba3a3b73d023a63f74efc3651b2bc3`, preserved on `research/reach-186-188-protected-anchor-20261115`. Work in ZFC, fixed real liquid modules with $0<p\le1$, the physical interval basis, original105/108 source grammar and126 parameter rows. Immediate inputs are [108](MIXED_R1_NORMAL_PROFILE_PUSHDOWN_108.md), [165](JOINT_ANCHOR_CUSP_GREEN_SOURCE_165.md), [183](POLYNOMIAL_RETAINED_GAUSSIAN_NORMAL_ORDERING_183.md), and [186](NONPOLYNOMIAL_GAUSSIAN_SOURCE_AUDIT_186.md). The scalar class and uniform rapid ideal are unchanged.

Require an **actual finite factorization on a fixed compact source stage**. After imposing its declared partition relations, use the true block coordinates and physical density. Suppose the whole evaluated integrand is a finite sum of terms consisting of a smooth Gaussian product times a compact distributional amplitude $u_\epsilon$, followed by permitted finite physical derivatives, partition pushforward and proper forgetting. For every fixed mixed parameter/regulator derivative, the amplitude has one polynomially moderate negative Sobolev norm as in108.2. Its order is fixed independently of the requested rapidness power. Geometry, Gaussian widths, compact support and derivative lists are fixed across126 rows. Completed coefficients are allowed only with these actual whole-amplitude bounds.

This is a factorization hypothesis to be proved for a history, not an operation of dividing any evaluated history by a Gaussian. A singular anchored constraint must be retained in its actual block coordinates or in its distributional amplitude; it is not silently replaced by a scalar boundary value.

## 2. Finite graph energy

Let a finite graph have positive fixed edge weights $w_e$. Prescribe values at selected boundary vertices and let the remaining vertices have real hidden coordinates $v$. Its energy is

$$
E(v)=\sum_{e=\{i,j\}}w_e(v_i-v_j)^2.
\tag{189.1}
$$

**Lemma189.1.** The unconstrained hidden minimum exists, modulo constants on components without boundary vertices. It is zero exactly when all prescribed values in each connected component agree.

**Proof.** On each component with a prescribed vertex, the quadratic form on hidden variations is positive definite: zero energy forces every variation constant, and its fixed boundary value is zero. Therefore its affine quadratic minimization has a minimizer. A component without prescribed vertices has a constant zero-energy assignment. Finally a zero sum of positive squares forces every edge difference to vanish, hence constancy on each component. Conversely assign the common prescribed value on each component. This proves the criterion. Additional source partition constraints restrict the set being minimized and cannot lower the unconstrained minimum. The stated equivalence refers to unconstrained hidden variables; constrained zero-energy feasibility must be checked separately. $\square$

For a path $\gamma$ between vertices with prescribed values $r,s$, telescoping and weighted Cauchy–Schwarz give

$$
(r-s)^2
\le\left(\sum_{e\in\gamma}w_e^{-1}\right)
\left(\sum_{e\in\gamma}w_e(v_i-v_j)^2\right),
\qquad
E\ge\frac{(r-s)^2}{R_\gamma},\quad
R_\gamma=\sum_{e\in\gamma}w_e^{-1}.
\tag{189.2}
$$

This lower bound is independent of all hidden values, so it survives restriction to the actual block coordinates. One must verify that the endpoint prescriptions remain the claimed distinct values after that restriction.

## 3. Rapidness of an actually factored source

Use retained boundary values $x,z$ and, when genuinely available, an anchor0. Fix a compact output patch with $|x|\ge\delta>0$ and $|z|\le\delta/2$. A surviving path from $x$ to0 or from $x$ to $z$ gives $E\ge\eta>0$ there, with $\eta=\delta^2/(4R_\gamma)$ sufficient. For widths $a_e\epsilon$, set $w_e=a_e^{-2}$. The edge product has the form

$$
G_\epsilon(v)=C\epsilon^{-m}\exp\left(-\frac{E(v)}{2\epsilon^2}\right),\qquad C>0.
\tag{189.3}
$$

**Proposition189.2.** Under the factorization hypothesis of section1 and the positive energy gap on a fixed neighborhood of the relevant compact source support, the localized output is uniformly rapid in one fixed negative Sobolev order for each mixed derivative. The order is independent of the requested rapidness power.

**Proof.** Insert fixed smooth compact cutoffs in the output patch and source support, choosing their supports inside a slightly larger patch with a positive energy gap. On that fixed compact set every physical or regulator derivative of (189.3) is its exponential times a finite polynomial in the coordinates and inverse regulator. Hence, for each finite derivative request and every $k$,

$$
\|G_\epsilon\|_{C^k}\le C_k\epsilon^{-N_k}
\exp\left(-\frac{\eta}{4\epsilon^2}\right).
\tag{189.4}
$$

Fixed cutoff derivatives satisfy the same estimate. Multiplication on $H^{-s}$ by a compact smooth function has a bound by finitely many of its derivatives. Combine this bound with the amplitude's fixed-order polynomial moderation. For each mixed derivative the Leibniz rule gives finitely many products, each bounded by a polynomial times the decaying exponential. For every $L$ that quantity is $O(\epsilon^L)$, in the same negative Sobolev order. Increasing $L$ changes only the constant, not the order or stage.

Finite declared derivatives incur fixed losses of Sobolev order. Proper compact pushforward and finite partition-jet pushforward likewise incur fixed finite losses, by108's test/Sobolev estimates. They therefore preserve this rapidness. If the amplitude contains a delta anchor, choose a fixed neighborhood of its compact support where the energy gap holds and use the whole distributional multiplier estimate. This retains all normal derivative terms; restricting the exponential to the delta support alone would not justify the estimate for its jets.

The estimates apply to the whole completed amplitude, through its assumed moderate stage map, and to every mixed derivative in126's compatible rows. On profinite plots the finite source choices are cover-local and the actual test-pairing identities descend. Thus the statement is about the actual rapid subobject, not merely weak scalar pairings. A finite sum of terms satisfying the hypothesis is rapid as well. $\square$

## 4. The first cusp core is nonrapid on this patch

For the core of165, $A_\epsilon=f(x)\rho(z)\kappa_\epsilon(z)$, choose a compact smooth $\phi(x)$ supported in $|x|\ge\delta$ where $f$ is nonzero, with $\int f\phi\ne0$. Choose $\zeta(z)$ supported in $|z|<\delta/2$, equal to one near0. Then

$$
\lim_{\epsilon\downarrow0}\langle A_\epsilon,\phi\boxtimes\zeta\rangle
=\rho(0)\int f(x)\phi(x)\,dx\ne0.
\tag{189.5}
$$

This is ordinary Gaussian approximate-identity integration on a fixed smooth compact test. A fixed-order rapid family has rapidly small pairing with this test. Consequently no finite sum entirely satisfying Proposition189.2 equals $A$, either exactly or modulo the declared rapid relation. If another summand lacks the energy gap, no conclusion about the sum follows from this argument.

## 5. Balanced moving anchors as an ambient control

For fixed $a_j>0$ and real $\lambda_j$, set $S=\sum_j a_j^{-2}$, $c=S^{-1/2}$, $\bar\lambda=S^{-1}\sum_j a_j^{-2}\lambda_j$, and $V=\sum_j a_j^{-2}(\lambda_j-\bar\lambda)^2$. Completing the square gives the exact identity

$$
\prod_{j=1}^m\kappa_{a_j\epsilon}(z-\lambda_jx)
=(2\pi)^{-(m-1)/2}\epsilon^{-(m-1)}
\frac{c}{\prod_j a_j}
\kappa_{c\epsilon}(z-\bar\lambda x)
\exp\left(-\frac{Vx^2}{2\epsilon^2}\right).
\tag{189.6}
$$

Balancing the mean to0 leaves $V>0$ whenever any moving anchor is nonzero. Cancelling that residual damping by its inverse exponential violates polynomial moderation on any fixed patch $x\ne0$. Finite derivatives or Laurent factors do not remove the damping.

Equation(189.6) is an ambient algebraic control, not source admission for arbitrary constraints $h_j=\lambda_jx$. For example $f(x)\delta(h-\lambda x)$ has forbidden opposite $x,h$ covectors at the joint origin; an independent moving anchor is not automatically an R1 coefficient. Source legality and the energy calculation are different assertions.

## 6. Scope and next inference

This diagnostic covers a genuinely typed finite positive-Gaussian factorization with fixed widths, compact hidden variables and a surviving boundary path. It does not classify arbitrary Wick propagators, signed sums with undamped branches, complete scalar heat coefficients without the displayed factorization, or networks whose component carrying $x$ is disconnected from both $z$ and0. For those disconnected networks the energy gap vanishes; the remaining anchor/cusp cone issue requires a separate source argument.

The useful next target is the zero-energy part of actual legal histories: determine whether a history producing the anchored cusp core can avoid the coupled energy gap while retaining an admissible R1 coefficient after every partition and forgetting map. A full negative theorem requires an invariant covering all permitted histories and rapid equivalence. A positive theorem requires an actual complete source for the core. Neither is supplied here. Universal150.L, residual $W$ acyclicity, originalR3, full126.14 and final integration remain open.

One primary construction is submitted for distinct source-locked review190 and bounded ledger191. No numerical fixture establishes these analytic conclusions. Shared same-system review, protected admission and programme completion remain distinct states.
