# EC-BULK-007 — Erdős #1094 predetermined critical sample

**Review state: PENDING PRIMARY SOURCE / INDEPENDENT SECOND PASS.** Not a completed critical review, not mathematical certification or protected admission.

## Exact open conjecture and quantifiers

For all integer pairs (n,k) with n>=2k and k>=2, the least prime divisor of binom(n,k) is <=max(n/k,k) with only finitely many exceptional pairs. The exact `finitely many` quantifier must NOT be strengthened without proof to the historical claim of exactly fourteen exceptions; eventual validity for each fixed k also does NOT prove a uniform finite set across unbounded k.

- Original published sources to inspect: Erdős, Lacampagne, Selfridge, *Prime factors of binomial coefficients and related problems*, *Acta Arithmetica* (1988), pp.507–523, and *Estimates of the least prime factor of a binomial coefficient*, *Mathematics of Computation* (1993), pp.215–224.
- Source catalogue: https://www.erdosproblems.com/1094 (OPEN).
- Authenticated return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2365#issuecomment-6166439929
- Unaccepted draft: governance/erdos_compendium/editorial/1094.md
- Pinned formal-conjectures 1094.lean: category research open and theorem proof body unproved.

## Independently checked finite witnesses

Exact integer math.comb plus prime-divisibility checks verified the full original list of fourteen exceptional pairs:

(7,3),(13,4),(23,5),(14,4),(44,8),(46,10),(47,10),(47,11),(62,6),(74,10),(94,10),(95,10),(241,16),(284,28).

For each, no prime <=max(n/k,k) divides the binomial coefficient. The linked #1093 deficiency is defined and positive, with exact examples deficiency(7,3)=1, deficiency(47,11)=4, and deficiency(284,28)=9. A bounded exhaustive search for 2<=k<=10, 2k<=n<=200 finds eleven exceptional pairs, all in the historical fourteen. This is **finite evidence only**. Reproducibility receipt: governance/erdos_compendium/batches/EC-BULK-007_FINITE_CHECKS_PHASE9.json and executable ci/erdos_compendium_007_phase9_checks.py.

## Obligations before the sample can be marked complete

1. Obtain and hash both primary papers; inspect the actual printed theorem and exact candidate list with page references, including edge cases k=1, n=2k and integer versus rational inequality.
2. Independently replay prime-divisibility with Legendre factorial valuations, not merely the same math.comb implementation. Check all fourteen and exact bounded sweep.
3. Research later literature for uniform finite-exception results; avoid equating the fixed-k eventual theorem with a uniform theorem in two variables.
4. Review the actual frozen Lean statement's quantifiers, theorem attribution and assumptions, without treating an unproved body as kernel certification.
5. Conduct an independent critical review of mathematical exposition, then record sourced APPROVE or REVISE. No routine human per-article approval required, but critical reviewer must actually inspect sources.

**Disposition: CRITICAL_REVIEW_PENDING.** Do not advance the twenty-sample completion count or claim the conjecture has been solved.
