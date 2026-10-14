RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0870-S01
PROBLEM_ID: 870
DISPOSITION: STATUS_CONFLICT
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
The maintained Erdős #870 asks whether, for every k>=3, some c(k)>0 guarantees a minimal at-most-k additive subbasis whenever an at-most-k basis has at least c(k) log n unordered positive-summand representations for every sufficiently large n. The 1988 Erdős–Nathanson Part 3 Problem 3 uses exactly-h basis language, a different convention. For A={n>=1:n=1 mod 3}, every positive integer is a sum of at most three members, but every exact three-term sum is 0 mod 3. The distinction is material.

## Dated status and primary evidence
Original: Erdős–Nathanson, Partitions of Bases into Disjoint Unions of Bases (1988), Part 3 Problem 3, printed p.8, https://users.renyi.hu/~p_erdos/1988-25.pdf . Pinned teorth catalogue 536408716724a2402bdfa7c1d764bf83d64a8c89 lists OPEN/unformalized. The modern maintained formulation is https://www.erdosproblems.com/870 . D. C. Turturean publicly claims a negative solution at commit a732dee4fbbef41e8a300aef264a3bc1bf505862 (2026-06-26), https://github.com/davidturturean/erdos-870/tree/a732dee4fbbef41e8a300aef264a3bc1bf505862 . The external exact-head GitHub Actions run https://github.com/davidturturean/erdos-870/actions/runs/28247948505 reports success; detailed logs have expired, so no literal axiom output was independently read.

## Strongest verified interface
Source inspection in the offline audit reports that Main.lean targets Erdos870Target, Defs.lean uses BasisAtMost, LogRepLowerBound and ContainsNoMinimalSubbasis, and RAtMost counts positive-term multisets. This is a source-level match to the modern at-most-k convention, not to the historical exact-h formulation. A finite independent combinations-with-repetition versus dynamic-programming fixture for A={1,2,3,5,8,13}, k=2,3,4, n=1..30 checks the counting convention, not the infinite theorem. No independent Lean replay or certification is claimed.

## Proposed bounded successor task
Checkout exact SHA a732dee4fbbef41e8a300aef264a3bc1bf505862 with Lean v4.30.0-rc2 and pinned Mathlib d6dab93da86c64219ab1497ffadce1a66aa04701. Run lake exe cache get, lake build, lake env lean Erdos870/Main.lean and capture literal #print axioms erdos_870, theorem type, dependency SHAs and k=3 versus k>=4 reductions. Accept only with reproducible build and axiom receipts and explicit semantic mapping. Stop on missing dependency, new axiom, failed build or semantic mismatch.

## Prerequisites and blocker
Independent kernel replay and editorial exact-h versus at-most-k reconciliation remain outstanding. External green CI is not GCL mathematical certification. No protected GCL formal statement is admitted for #870.

## Reuse and claim boundary
Reuses the 1988 original, maintained #870, pinned Turturean source and CI metadata, and prior offline finite semantics checks. This is a bounded source-audit return only, not a proof, status adjudication, protected merge or editorial admission.
