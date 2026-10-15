# EC-BULK-007 — #1151 Chebyshev interpolation 2026 proof/status review

**Status: REPORTED_EXTERNAL_SOLVE_AND_LEAN, SOURCE_EQUIVALENCE_PENDING.** Not a completed GCL kernel replay, not an independent critical review, and not editorial admission.

- Maintained catalogue: https://www.erdosproblems.com/1151 still OPEN in the top-level badge.
- Original issue return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2422#issuecomment-6181807570
- Chojecki (Ulam.ai) research note April 29, 2026, primitive-row Chebyshev-node spike construction.
- Allen Hart May 6 Lean formalization of Theorem 1.1(a), **nonempty closed target** at a fixed allowed evaluation point.
- Public independent July 25 report: https://erdosproblemaday.com/day/1151-chebyshev-lagrange-limit-sets ; reports source rebuild of 7,997 Lean jobs and target axioms [propext, Classical.choice, Quot.sound] with no sorryAx.
- Additional ProbXiv entry https://probxiv.com/problems/erdos-1151 cautions that formalization correctness and alignment with original statement are separate.

## Independent verification boundaries

The reported proof and community review predate GCL's audit. We have **not** rebuilt the Lean environment or checked all theorem/axiom dependencies ourselves. The current problem statement also leaves the fixed point $x_0$ ambiguous: arbitrary fixed point versus special Erdős point $x_0=\cos(p\pi/q)$ with odd $p,q$. An unrestricted all-$x_0$ reading can be false at interpolation nodes.

Theorem 1.1(a) handles **nonempty** closed target sets; the **empty** target requires an additional divergent construction. Erdős's 1943 corrigendum reportedly proves divergence for special $x_0$, while the 1943 added-in-proof claim about arbitrary closed sets was unproved in that source. Avoid circular citation of Erdős's unproved remark.

## Required checks

1. Pin 2026 Chojecki note and Hart Lean Git SHAs, build and run #print axioms; check sorryAx absence.
2. Compare Lean theorem with exact $x_0$ domain and ALL nonempty closed subsets of [-1,1]; check Chebyshev nodes, continuous f, real finite cluster points, and existential order.
3. Read Erdős, Annals of Mathematics 44 (1943) 647–651 original erratum for EMPTY target and independence of unproved 1943 remark.
4. Independently inspect primitive-row formula, spike leakage argument, no hidden hypotheses, and nonempty/empty glue.
5. Present evidence to canonical catalogue for up-to-date status, without claiming a new discovery or changing protected source issues.

The exact constant function f=1/2 case in phase17 fixture is a trivial one-point cluster example, **not** the general theorem.
