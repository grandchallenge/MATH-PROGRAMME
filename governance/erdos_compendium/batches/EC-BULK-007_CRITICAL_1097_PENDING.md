# EC-BULK-007 critical sample #1097 — pending exponent/proof equivalence review

**Disposition: INDEPENDENT_CRITICAL_REVIEW_PENDING_PRIMARY_SOURCES.** Not a completed critical review or mathematical certification.

- Canonical Erdős statement: https://www.erdosproblems.com/1097
- Authenticated RESULT/1: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2368#issuecomment-6167052162
- Draft: governance/erdos_compendium/editorial/1097.md

The correct object is the maximum number of DISTINCT positive differences d supporting a three-term arithmetic progression within n distinct integers. Original optimistic O(n^(3/2)) estimate is externally DISPROVED; sharp-order problem remains OPEN. Catalogue attributes a 1.77898... lower exponent to Lemm (2015), an improvement to AlphaEvolve (2025), and Katz–Tao (1999) 11/6 upper, linked through Bourgain (1999) restricted sum-difference exponent equivalence. These are external source claims; reproduce proof assumptions rather than certify by citation alone.

Finite receipt ci/erdos_compendium_007_phase10_checks.py verifies A={0,...,8} has difference set {1,2,3,4} and sparse A={0,1,3,4,9,10} none. Does NOT establish exponent bounds.

Mandatory reviewer steps: (1) obtain hashes/page-exact proofs for original GWNT and Bourgain, Katz–Tao, Lemm, and evolutionary-search report; (2) independently derive exponent equivalence with correct normalization of n, restricted graph G, sum and difference sets; (3) verify 1.77898 lower and 11/6 upper actually apply to 3-AP-difference count, including hidden epsilon/losses; (4) compare frozen FormalConjectures 1097.lean answer(False), proof placeholder, with any linked external proof and replay exact dependencies; (5) perform independent mathematical/expository reviewer disposition APPROVE or REVISE.

Until then, #1097 deterministic sample remains **INCOMPLETE**, no new theorem nor Lean proof is claimed.
