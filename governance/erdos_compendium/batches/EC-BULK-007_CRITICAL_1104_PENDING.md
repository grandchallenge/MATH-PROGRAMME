# EC-BULK-007 predetermined critical sample #1104

**Disposition: PRIMARY-PROOF-AND-INDEPENDENT-CRITICAL-REVIEW-PENDING.** Not source-fidelity acceptance, not a certified sample review.

## Exact mathematical interface

For simple graphs on EXACTLY n vertices that are TRIANGLE-FREE (no K3), let f(n) be the maximum vertex chromatic number. Do not substitute K4-free or use graph EDGE count m in the same function. The sharp leading constant remains open despite known order sqrt(n/log n).

- Canonical catalogue: https://www.erdosproblems.com/1104, status OPEN, maintained update January 21 2026.
- Original source issue: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2375#issuecomment-6168366293
- Draft: governance/erdos_compendium/editorial/1104.md
- Frozen formal-conjectures: google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020, ErdosProblems/1104.lean; existing lower/upper declarations have unproved bodies.

## Externally published known bounds

The site records (1-o(1))*sqrt(n/log n) <= f(n) <= (2+o(1))*sqrt(n/log n).

2022 Davies–Illingworth, The chi-Ramsey Problem for Triangle-Free Graphs, SIAM J Discrete Math 36(2) 1124–1134, published author abstract independently checked for sqrt2 upper-constant improvement, from 2sqrt2 to 2.

2025 Hefty–Horn–King–Pfender lower-bound construction is reported by the catalogue. The full primary proof and exact o(1) regime have NOT been independently audited, and the leading constant is not yet determined. Neither theorem is to be credited as new GCL work.

## Exact finite witness

ci/erdos_compendium_007_phase11_checks.py constructs Mycielskian of 5-cycle, yielding 11 vertices, 20 edges, no triangles and chromatic number exactly 4. Direct exact backtracking checks no 3-colouring and finds a 4-colouring. This only shows f(11)>=4, not asymptotic bounds or the leading constant.

## Mandatory proof/critical review obligations

1. Fetch source bytes of BOTH 2022 and 2025 primary manuscripts, hash/pin immutable versions, and verify theorem statement with constants, logarithms, order and o(1) dependencies.
2. Independently review the construction lower bound and the upper argument; distinguish chromatic from list chromatic where applicable.
3. Compare exact finite witness with a distinct combinatorial certificate, ideally Mycielski's general theorem or independent enumeration.
4. Review formal file's meanings for max over graphs on n vertices and status of lower/upper versus exact constant.
5. Perform a genuine independent source-based critical mathematical and exposition review, record APPROVE or REVISE with theorem pages.

Critical sample completion stays 0/20 at this checkpoint. No protected publication, Lean kernel certification or original theorem claimed.
