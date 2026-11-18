# Erdős #249 WP07-A — source-critical mathematical adversarial review

**Review object:** \`MOVING_LOGLOG_INTEGRALITY_007.md\` SHA-256 \`06d5338a44f0c455f1977cd8b656de95c6ab676fd77388f26c10ee7bcea86c3f\`.  
**Exact executed code:** \`moving_loglog_integrality.py\` SHA-256 \`193830f789c3178b9bbdfbe4dcf4226d86c6f6cf0bca4b68248849e466bc437e\`.  
**Exact tests:** \`test_erdos249_moving_loglog_integrality.py\` SHA-256 \`b0eefc16d624d50f3dc48b48cf3f08bf4a54d1954cbc1c2e896534cf5def1063\`.  
**Independent-review authority:** no. This is a non-authoring logical Adversary/Referee pass performed by the **same authenticated GCL agent** in a distinct role; it is not an independently authenticated specialist, human mathematical referee, Lean replay, or MATHCERT certification.  
**Original Erdős #249:** OPEN.

## A. Is the source's heavy analytic input correctly isolated?

Yes. The manuscript takes as **external classical input**, rather than proving, the Selberg–Delange moment bound for fixed $0<z<1$:

$$
\sum_{n\le Y} z^{\omega(n)}\ll_z Y(\log Y)^{z-1}.
$$

This is the standard $\omega(n)$ moment estimate, not a derived consequence of finite tests or a novelty claim. The Dirichlet Euler product has $\zeta(s)^z$ as its singular component. The elementary deductions after this input are separately reviewable. Their admitted status must **not** imply independent verification of the classical Selberg–Delange proof.

## B. Does the valuation bound omit the even prime?

No. For every distinct odd prime $p\mid n$, $\varphi(n)$ contains a factor $p-1$ and hence a factor two. The distinct prime $p=2$ is at most one lost contributor, yielding $\nu_2(\varphi(n))\ge\omega(n)-1$ even for $n=1,2$. The executable tests independently compare the totient sieve against coprime counting and distinct-prime count against trial division.

## C. Are the exceptional bound and exponent correct?

For $L=\lfloor\alpha\log\log X\rfloor$, failure at one $j\le L$ implies $\omega(N+j)\le L$. Taking $z=\alpha$, Markov's inequality gives an exceptional proportion at most

$$
O_\alpha\left(L\alpha^{-L}(\log X)^{\alpha-1}\right).
$$

Since $\alpha^{-L}\le(\log X)^{-\alpha\log\alpha}$ and

$$
I(\alpha)=1-\alpha+\alpha\log\alpha>0
$$

for every fixed $0<\alpha<1$, the resulting bound is $O_\alpha(\log\log X\,(\log X)^{-I(\alpha)})\to0$. The change from $X$ to $3X$ in the moment upper bound has only a fixed-factor effect. The union bound accounts for **all** $j$; no false independence across neighboring totient values was assumed. The harmonic supremum is uniform because each good position has phase exactly one for **all integer harmonics**, and a bad position's phase discrepancy is bounded by two.

## D. Is there a dangerous converse or unproved true-tail replacement?

The finite sum may be integral even when some component is nonintegral: at $N=1,L=2$ the components are $1/2$ and $2/4$, summing to one. The source proves a sufficient **termwise** condition and correctly treats the exceptional set for nonintegral finite sums as a subset. The tests include this hostile converse failure.

The positive true tail lower bound uses only the first omitted term and $2\varphi(n)^2\ge n$, already established in the earlier protected GCL record. For $L=O(\log\log X)$ it grows at least as a power of $\sqrt X$ divided by a fixed power of $\log X$. **A growing positive tail does not imply its fractional part is nonintegral**, and neither large true error nor small finite phase discrepancy controls the true infinite phase.

## E. Is the mathematics actually relevant to the source-locked open obligation?

This is an unconditional **negative structural result** about shallow moving depths, contingent on a classical cited theorem. It does not prove or refute the good-base Fourier saving at $L(X)\asymp\log_2 X$ required in Will Cook's Theorem 3.5(b); the latter is a qualitatively deeper range. It is not a new irrationality criterion. The parent research workstream must remain OPEN until a totient-specific cofinal producer survives the rational and lacunary controls.

## F. Concurrent protected-admission hazard

WP06 PR #3499 is already in the protected merge queue and modifies the same policy-component file as this WP07-A candidate. The two topic branches must **not** be force-merged or rebased merely for numeric freshness. However, if WP06 changes that exact shared file on protected main before WP07 admission, a **material closure overlap** exists and the candidate policy-component map must be reconciled before protected admission. Re-run affected exact-head checks on the reconciled code. Do not drop either registered test path; no direct protected writes or review gate weakening.

**Disposition:** ACCEPT_WITH_SCOPE for the moving-depth manuscript deductions, eleven exact tests and the independently sourced classical theorem input. **Not** a full solution, mathematical certification, priority claim, external independent review, or authorization to close the parent #3500 research goal.
