# EXT-015 REACH / 040 — distinct hostile mathematical review of the fixed-atom counterterm BV model

**Review status:** Source-locked GCL mathematical critic pass with distinct reasoning and recorded limitations. This is *not* an outside referee certificate. **Source candidate:** [R2 atomic-jet BV/039 PR #2814](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2814), head 8c93a7220a2386590218fe416792ff64a97cfb92. **Protected baseline at review initiation:** a86de10156ad4463fb4131beb7d2c3776be888a2. The original smoothed free-field result is D14/028–029; moving-point obstruction is R2/036; earlier finite-part extension is R2/032–034.

## 1. Correct handling of derivative Dirac signs

The candidate chooses the sign-normalized distribution jet $j_{a,k}=(-1)^k\delta_a^{(k)}$, so its action on a smooth test function $f$ is **exactly** $f^{(k)}(a)$. Pairing two such jets against $P_\epsilon(x-y)$ therefore yields $\partial_x^k\partial_y^lP_\epsilon(a-b)$, with no unaccounted factor $(-1)^{k+l}$. Applying the free operator $\partial_x^2$ sends $j_{a,k}$ to $j_{a,k+2}$, because the parity of $k$ and $k+2$ agrees. Thus the free algebra differential in 039 is correctly typed.

## 2. Independent quadratic Wick/BV derivation

Write $e_i$ for even generators, $\theta_j$ for odd generators, and let $d=\sum_{a,k}e_{a,k+2}\partial^L_{\theta_{a,k}}$. Define the even quadratic contraction operator $B=\frac12\sum_{i,j}p_{ij}\partial_{e_i}\partial_{e_j}$ with symmetric constant coefficients. On every polynomial, the operator commutator obeys

$$
[B,d]=
\sum_{a,k,i}p_{i,a(k+2)}
\partial_{e_i}\partial^L_{\theta_{a,k}}.
$$

This is verified by acting on polynomial monomials, with the second derivative of $B$ hitting the coefficient $e_{a,k+2}$ of $d$. All third-derivative terms cancel pairwise. On distinct sites, the exact propagator $|a-b|/2$ has zero derivatives of total order at least two. On coincident sites the jet of $\lambda(x-y)^2/2$ has only $p_{a0,a2}=p_{a2,a0}=\lambda$ and $p_{a1,a1}=-\lambda$. Consequently the commutator is *exactly* $\lambda\sum_a\partial_{e_{a,0}}\partial^L_{\theta_{a,0}}$.

Odd derivatives at different labels anticommute, so the BV operator squares to zero. It anticommutes with $d$ because no coefficient of $d$ depends on $e_{a,0}$; the constant even derivatives making $B$ commute with the mixed BV derivatives. No infinite summation difficulty occurs: every polynomial uses only finitely many variables and the operators lower polynomial degree. The BCH series for $W_\lambda dW_\lambda^{-1}$ terminates after the first commutator. This independently checks the full algebraic identities on **arbitrary finite-degree** elements, not just the atomic two-generator example.

The seeded rational testbench [039](fixtures/check_fixed_atomic_bv_039.py) additionally verified these identities on 125 two-site polynomials, but cannot replace the general variable-index algebra argument.

## 3. Regulator and locality hostile check

For an even, mass-one smooth mollifier $\kappa$ supported in $[-1,1]$, and a fixed finite set of atom labels, whenever $\epsilon$ is smaller than every nonzero separation $|a-b|$, the affine function $|z|/2$ is unchanged by convolution with $\kappa_\epsilon$ in neighborhoods of each difference $a-b$. Thus **all** derivatives at those nonzero differences agree with the unregulated propagator, not merely the zeroth order value.

At equal atom labels, the proposed counterterm subtracts each coefficient $p^\epsilon_{a k,a l}-p^\lambda_{a k,a l}$. It is genuinely an operator on the full fixed-label polynomial algebra, locally supported on equal labels, and cancels **all** divergent atomic jet pairings. The resulting renormalized even Wick operator equals the prescribed finite one on each polynomial for sufficiently small $\epsilon$. Iterations do not create new labels, so the same finite-site separation condition suffices for exponential conjugation. This is stronger than convergence.

**Important limitation:** "local" here means *diagonal in fixed atomic labels*. The counterterm is not yet constructed as a continuous distribution-valued extension along varying collision parameters, and need not obey locality in the stronger differential-geometric or interacting Epstein–Glaser sense without separate proof.

## 4. Prefactorization coherence and exact limits

The free graded polynomial functor on fixed labeled jets admits extension-by-zero under inclusions and classical multiplication from disjoint opens. Wick operators are natural under inclusions because no contracted coefficient depends on the ambient open. Therefore their conjugation yields unit, permutation and associativity identities and cochain compatibility by diagram transport. Cross-atom Wick contractions may remain long-ranged at distinct sites, as in D14; the cochain differential itself uses only identical label pairing.

**Hostile controls:**

1. The arbitrary finite scheme parameter $\lambda$ is not selected canonically. Different choices yield cochain-isomorphic free prefactorization structures by an explicit local quadratic operator; that is an algebraic scheme ambiguity, not physical uniqueness.
2. If atom locations vary and collide, the off-diagonal propagator has a cusp. R2/036 therefore forbids declaring a $C^1$ real-valued moving-point Wick plot for the same coefficient prescription. The fixed-label theory avoids, rather than solves, that topological obstruction.
3. The domain is not all compact distributional kernels; it is the polynomial subspace generated by finite point jets, with no general Schwartz kernel product, continuous family topology, or completed Costello–Gwilliam B.6 Weiss equivalence established.
4. This is a *free* algebraic BV model. No nontrivial interaction, renormalized quantum master equation for an interaction functional, nonperturbative effect or general curved-background covariance is proved.
5. An unbounded formal collection of jet labels is a set-indexed algebraic direct sum, not a convergent operator series; the domain of each polynomial is finite.

## 5. Mathematical disposition

**ACCEPT as bounded candidate mathematics:** R2/039 Theorems 39.1–39.2 and Corollary 39.3 are internally consistent on the **full algebraic polynomial domain generated by fixed labeled Dirac jets**, with correct signs, exact local counterterm subtraction, coherent nonzero square-zero second-order BV and algebraic prefactorization. This is a legitimate **restricted GB2 constructive milestone**, subject to protected source admission. The label-level locality must not be promoted into a stronger claim about smooth collision-parameter renormalization.

**Remaining GB2 scientific obligation:** extend the bounded construction to genuinely distribution-valued **moving-collision** configuration spaces with well-chosen smooth wavefront-controlled plots, nested/overlapping renormalization and quantum master equation checks. Integrate only after R1 fixed-cone multilinear/topological support and the R3 genuine higher liquid Ext result are independently resolved.

**Governance:** This review is a distinct role-scoped non-authoring pass under the established authenticated GCL identity, not an independent login or fabricated external expertise. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains OPEN after admitting a restricted construction.
