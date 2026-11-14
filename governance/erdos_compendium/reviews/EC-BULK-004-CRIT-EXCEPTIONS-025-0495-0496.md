# EC-BULK-004 critical source exceptions: Erdős #495 and #496

Observed 2026-10-14 CHAD local / 2026-10-15 UTC. Same-operator mathematical review; NOT independent-peer certification. Two issue-bound authenticated source returns:
- #495 https://github.com/grandchallenge/MATH-PROGRAMME/issues/1766#issuecomment-6185293937
- #496 https://github.com/grandchallenge/MATH-PROGRAMME/issues/1767#issuecomment-6185313478

## #495: preserve full Littlewood quantifiers

Original Erdős 1961 pp.238–239, item I.34, original 34-page PDF downloaded onto CHAD and original text pp.238–239 inspected. Nearest-integer distance ||x||=min_{m in Z}|x-m|, not ordinary absolute value; liminf is along positive integer n and uses same n in both factors. The actual universally quantified conjecture remains OPEN. Pinned FC 495.lean blob cc482279adad714d350cc28cec14b5821b777874 has sorry in answer/theorem, no certification. If either coordinate is rational, n clearing its denominator gives exact zero terms. If liminf n||n alpha||=0 for either factor, the product is bounded by (n/2)||n alpha|| and its liminf is zero for every other factor. This is elementary and independent of the open two-badly-approximable case.

Einsiedler–Katok–Lindenstrauss, Annals 164 (2006), 513–560, exact published p.515 Conjecture 1.2 and p.516 Theorem 1.5 visually inspected in original PDF. The exceptional set Xi={pairs with positive liminf} has Hausdorff dimension 0 and is countable union of compact box-dimension-zero subsets. Dim_H(Xi)=0 does NOT imply Xi=empty. Status OPEN. Finite tests cannot settle liminf for sqrt2,sqrt3 or general pairs.

## #496: real source/semantic conflict; do not paper over

**Current catalogue [#496] assertion is false literally**. For every irrational real alpha and every epsilon>0 it demands positive integer x,y,z such that |x²+y²-alpha z²|<epsilon. For alpha=-sqrt2 (irrational), x,y,z>=1 gives |...|=x²+y²+sqrt2 z²>=2+sqrt2; choosing epsilon=1 disproves this exact universal claim. The elementary statement is not to be labeled PROVED without fixing the hypothesis alpha>0.

Original Erdős (1961) printed pp.238–239 asks both |alpha(x²+y²)-z²|<epsilon and |x²+y²-alpha z²|<epsilon, and says **integers**, without expressly excluding the zero triple. Consequently literal allowance of (0,0,0) would trivialize it. The intended nontrivial indefinite Oppenheim problem needs explicit nonzero vectors and alpha>0 for the present coefficient normalization. Primary PDF retrieved directly from https://users.renyi.hu/~p_erdos/1961-22.pdf, pp.238–239 text extracted.

Margulis, *Discrete subgroups and ergodic theory* (1989), pp.377–398, is historically cited as proof of the Oppenheim conjecture. The general published theorem concerns values of NONDEGENERATE INDEFINITE irrational quadratic forms in dimension >=3 on NONZERO integer lattice vectors. The precise indefinite hypothesis is independently confirmed on published first page of Einsiedler–Katok–Lindenstrauss, Annals 164 (2006) p.513, inspected. For alpha>0 irrational, Q=diag(1,1,-alpha) is nondegenerate, indefinite and not proportional to rational form, so the standard Oppenheim theorem applies to Z³\{0}. **Additional exact proof obligation**: demonstrate approximating triples with every coordinate nonzero before using independent sign reflection to obtain strictly positive x,y,z. Unrestricted nonzero vectors are not the same quantified domain as all-positive coordinates. The Margulis 1989 full original was not directly read; no independent transitive proof replay or formal certification claimed.

Pinned teorth catalogue classifies #496 PROVED and pinned FC-GDM-85F86371 does not contain 496.lean. Preserve metadata as reported while recording STATUS_CONFLICT for literal text. The issue-bound source return and same-operator article are *not* authorization to change protected status. Source correction and positive-coordinate bridge are separate bounded editorial issues. Exact finite Fraction tests confirm negative-sign lower bounds, positive-sign indefiniteness, spurious zero triple and sign-reflection only for nonzero coordinates. No finite arithmetic establishes Oppenheim.

## Editorial and custody conclusion

Both six-section manuscripts are UNACCEPTED_DRAFT with provenance, precise hypotheses, bounded fixtures, and explicit mathematical limits. #495 is OPEN, #496 historical PROVED only with corrected indefinite sign hypotheses; as written #496 is false. No new research theorem or priority claim. Protected main admission and deployed-site mathematics verification remain separate.
