# EC-BULK-004 — #491/#492 same-operator mathematical and source review

Observed 2026-10-14. Authenticated reviewer/editor: fyremael. This is an adversarial reading of the editorial drafts by the **same operator**, not an independent mathematical certification or protected admission.

## Erdős #491: semantic fidelity

The original Erdős 1961 Problem I.30 (printed p.237, https://users.renyi.hu/~p_erdos/1961-22.pdf#page=17) was visually inspected. The mathematical input is a real-valued additive function satisfying f(ab)=f(a)+f(b) only if gcd(a,b)=1, together with uniformly bounded consecutive differences. The conclusion is f(n)=c log n+g(n) with g uniformly bounded. Erdős's older hypotheses of eventually small consecutive difference or monotonicity lead to exact log, but **must not** be imported into the weaker bounded-difference conjecture.

Wirsing (1970), *A characterization of log n as an additive arithmetic function*, *Symposia Mathematica* IV, 45–57, is the established resolving proof. First-person original author announcement abstract 681-A21 in *Notices AMS* (November 1970) claims an even one-sided lower bound as sufficient; the complete Wirsing 13-page proof text has **not** been directly inspected. Scholarly bibliographic corroboration and later mathematical summary support the PROVED catalogue label; no kernel proof certification claimed.

The testable failure of the falsely strengthened conclusion is exact: g(n)=t if 2|n and zero otherwise is additive for coprime inputs and has bounded jumps, but g(4)≠2g(2) and g is not identically zero. A finite set of prime-divisibility indicators with rational weights has absolute remainder bounded by the sum of absolute weights. Fixture tests/test_erdos_compendium_0491_additive_log.py checks the coprimality restriction and that exact family. The universal Wirsing theorem is **not** inferred from finite computation.

## Erdős #492: negative status and missing actual witness

Original 1961 p.238, Problem I.31, https://users.renyi.hu/~p_erdos/1961-22.pdf#page=18, visually inspected. Fix an infinite increasing integer sequence with a_(i+1)/a_i→1, define h_A(x)=(x-a_i)/(a_(i+1)-a_i) on half-open [a_i,a_(i+1)), and ask uniform distribution of h_A(alpha n) for almost all alpha. Fixed A quantifies **before** almost-every alpha. Distinguish failure of uniform distribution from finite rounding noise or exceptional rational alpha.

Refutation attributed to W. M. Schmidt, *Disproof of some conjectures on Diophantine approximations*, *Studia Sci. Math. Hungar.* 4 (1969), 137–144. Original Schmidt proof **not accessible or independently reconstructed**, a precisely stated source-fidelity gap. The maintained catalogue and external bibliography support DISPROVED classification, but do not permit inventing the concrete Schmidt sequence or its exceptional measure.

Arithmetic progression A={d,2d,3d,...} gives exact h_A(x)={x/d} for x≥d. For alpha/d irrational, Weyl's geometric-sum estimate implies uniform distribution; for rational alpha/d, finite residue cycling is NOT a counterexample to 'almost every alpha'. tests/test_erdos_compendium_0492_subdivision.py verifies these finite exact identities, half-open resets, and rational exceptional cases. No finite histogram can prove Schmidt's negative theorem.

## Custody and admission

Original source-return issues have authenticated RESULT/1 comments https://github.com/grandchallenge/MATH-PROGRAMME/issues/1762#issuecomment-6181731850 and https://github.com/grandchallenge/MATH-PROGRAMME/issues/1763#issuecomment-6181740411 . Both manuscripts have the required six headings and correct status PROVED and DISPROVED respectively, each UNACCEPTED_DRAFT. The protected GCL Formal Conjectures snapshot includes neither #491 nor #492. Full Wirsing 1970 and Schmidt 1969 bodies remain uninspected, not asserted as peer-verified.

Successor: obtain the missing original proof bodies for source-fidelity verification and preserve the specific additive/copime and subdivision/measure-theoretic quantifiers. Cohort-wide protected merge, independent official admission, and deployed-site rendering are not claimed.
