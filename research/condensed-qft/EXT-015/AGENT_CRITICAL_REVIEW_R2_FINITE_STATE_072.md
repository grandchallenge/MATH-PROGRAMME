# EXT-015 REACH / 072 — critical audit of finite Laurent-state insertion

**Provenance:** distinct logical mathematical critic pass after the author source was frozen, within the same Codex session/account. This is not external independent certification.

**Exact source:** commit `4b4137e4022d00c6fa9a0d8730d1382d4fde6eac`; [071](R2_FINITE_LAURENT_INSERTION_OBSTRUCTION_071.md) blob `13d1441dd5a745f7726d6b01843b2129331e4b2d`; [fixture](fixtures/check_finite_laurent_insertion_obstruction_071.py) blob `126b28d742ff4d115faa0d6f952cf4ec50b46460`.

## 1. Domain and failed diagram are actually specified

The domain is the real span of the fixed-cutoff polynomial Gaussian families in (71.2). Insertion is multiplication of ordinary smooth functions at strictly positive regulator, not multiplication of limiting delta distributions. Multiplying by the additional Gaussian power stays in that span. Taylor expansion after the scaled Gaussian substitution supplies a bounded-below distributional Laurent series; at each chosen family its negative part is finite.

Thus the retained data and required output in (71.4) exist on the stated domain. Equal retained inputs would have equal outputs under any proposed factor, even a nonlinear one. No assumption of linearity of the unknown factor is needed.

**Assessment:** the contract is well-typed. The source does not prove that every member of this polynomial module is the output of a particular fixed graph or subtraction scheme; any application to a smaller graph domain must first verify that domain contains the witness pairs.

## 2. The elementary arbitrary-insertion witness

The uninserted difference in (71.5) begins at Laurent degree twice the chosen positive integer. Choosing that degree above the retained cutoff makes the truncated states exactly equal, including for negative cutoffs. After insertion the explicit scaling exponents cancel. The normalized Gaussian integral in (71.7) is positive and gives the displayed nonzero scalar delta.

The first odd moment is zero. Taylor remainder bounds on a bounded test family give the claimed strong order-two remainder. The cutoff equals one in a fixed neighborhood of the origin, so the omitted tail is exponentially small, including after any of the fixed polynomial factors used here.

The inserted difference has no negative powers. Subtracting the two whole-amplitude pole parts therefore leaves exactly the same nonzero finite discrepancy.

**Assessment:** support Theorem 71.1 and its stated finite-part consequence.

## 3. Fixed insertion: the Hermite witness uses the full domain

For Theorem 71.2, standard Gaussian orthogonality makes all moments of the even Hermite polynomial below its degree vanish. Its moment at its own degree is that degree's factorial. Consequently the source difference begins exactly at the degree stated in (71.10), with a nonzero even delta derivative. The chosen degree can exceed any finite cutoff even when the insertion is held fixed.

The insertion changes the Gaussian variance. Taking the expectation of the Hermite generating function gives the exponential with quadratic coefficient equal to half the variance minus one. Its even Taylor coefficient is exactly (71.11). Since the changed variance is strictly below one, that value is nonzero for every nonnegative chosen Hermite index, including the index zero case.

After insertion the scaling starts at degree zero, so the resulting nonzero expectation is an actual finite delta term. Evenness removes the first correction; the same Gaussian Taylor argument controls the remainder. There is no uniform-in-degree estimate in the theorem and none is needed: each witness has a fixed polynomial.

**Assessment:** support Theorem 71.2 on the stated unbounded-degree polynomial module. This does not refute a separately bounded-degree or richer-state construction.

## 4. Hostile controls and independent limitations

The exact fixture has 104 varying-cutoff controls and 104 fixed-insertion/Hermite controls. It checks the exponent balance, equality of retained states, unchanged negative part, exact orthogonality and nonzero changed-variance moments with rational arithmetic and formal positive normalization. It does not numerically integrate the Gaussian, prove a strong topology estimate, or settle an infinite-dimensional BV identity. The analytic source supplies the arbitrary-cutoff argument.

The witness is a failure of one explicit source-truncation factorization diagram. It supplies neither a commutator on an already constructed global BV algebra nor an overlapping proper-forest identity. In particular, agreement with whole-amplitude finite part is a hypothesis of the rejected contract; it is not silently imposed on the admitted proper-subgraph forest scheme.

The normal complement-jet construction of 061 retains the jets required by each insertion. It is compatible with this result, which rules out one uniform finite Laurent cutoff on the module under discussion. Additional regulator-dependent data, bounded domains or a different proven prescription may escape the hypotheses.

**Verdict:** accept the two bounded no-go theorems and their exact failed diagram as source-semantic mathematical returns. Keep GB2 / #2797, R4 / #2657 and the larger parent OPEN. This audit is a same-session logical critic pass; it creates no external referee, MATHCERT, deployment, publication or protected-bypass authority.
