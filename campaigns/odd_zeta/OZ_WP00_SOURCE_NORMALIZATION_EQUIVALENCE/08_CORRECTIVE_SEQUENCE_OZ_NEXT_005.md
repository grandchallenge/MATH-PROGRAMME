# OZ-NEXT-005 — Corrective sequence

## Decision

The corrective sequence is admitted as four linked obligations. It does not complete `OZ-WP00` and does not authorize successor work.

## OZ-NEXT-005A — Sharp-12 proof and certificate reconciliation

The source package does not contain a complete machine certificate for the uniform sharp-12 theorem.

The accepted dependency boundary is:

1. The Brown–Zudilin `Q`-row recurrence certificate is independently replayed.
2. The exact `n=2` failure of the uncorrected denominator claim and factor-12 clearing identity is Lean-replayed.
3. The source paper proves the conditional arithmetic chain from `(T1-top)` and `(DEPTH)` to the `p >= 5` headline.
4. `(DEPTH)` is a finite linear-algebra certificate, not an independently proved universal theorem.
5. `(T1-top)` is finitely verified and explicitly not certified.
6. Theorem B is separately finitely verified and explicitly not certified. It is required for the middle row, not for the top-row `P_n` headline.
7. The `p=2` and `p=3` components are outside the accepted `p >= 5` conditional chain and remain separate.

Effective disposition:

```text
OZ-MSS-S006    STATED_ONLY / CONDITIONAL_CHAIN
OZ-CER-E004    INCOMPLETE_CERTIFICATE_LEDGER
SHARP-12 p>=5  NOT REFEREE-ACCEPTED
```

No statement may describe the sharp-12 law as unconditional, certified, or replayed.

## OZ-NEXT-005B — Computation environment and replay normalization

The package normalizes the previously incomplete computation lanes:

- `OZ-CMP-X002`: exact anchor replay for `audit.py validate`; the large record-point calculation remains a bounded-time lane and is not required for theorem status.
- `OZ-CMP-X005`: independent verification of the submitted order-4 degree-19 recurrence against the exact locked sequence terms. The missing `fleet_*.txt` reconstruction inputs prevent independent reconstruction of the operator; only verification of the submitted operator is accepted.
- `OZ-CMP-X007`: independent exact replay of both compact sums through `n=34` and their order-3 recurrence residuals through `n=31`. This remains finite evidence and does not prove identity `(T3)`.

All commands run against the two pinned source commits in CI. Python version and installed dependency versions are captured in the workflow artifact.

## OZ-NEXT-005C — Nearest-prior-art acquisition and specialist comparison

The workflow acquires exact versioned PDFs for the nearest comparison set and records byte lengths and SHA-256 identities. The comparison concerns theorem scope, not keyword similarity.

The conservative specialist findings are:

- Malik–Straub proves Lucas congruences for the fifteen integral sporadic Apéry-like rows.
- Gorodetsky gives representations and stronger Lucas/supercongruence consequences for integral rows.
- Straub proves Gessel–Lucas congruences modulo `p^2` and two-term supercongruences for the fifteen integral rows.
- Chamberland–Straub treats Apéry limits and recurrence-solution quotients, not the submitted harmonic companion congruence.
- Liu–Zhang–Zhi supplies a Lean 4 irrationality proof for `zeta(3)` based on Beuker's method and is a formalization comparator, not prior art for the submitted B-row theorem.

On the reviewed theorem statements, none of these sources states the submitted harmonic second-row congruence or the abstract character-twisted H1–H5 companion theorem. This supports only `APPARENTLY_NEW_PENDING_REVIEW`. It does not authorize `NEW_AFTER_AUDIT` because the search is not exhaustive and the claimed theorem still requires specialist proof review.

## OZ-NEXT-005D — Lean placeholder quarantine and dependency audit

The dependency boundary is declaration-level:

Clean conditional infrastructure includes `BZRec`, the initial-value lemmas, and the uniqueness theorems that accept a `BZRec` hypothesis.

Quarantined declarations include:

- `ZetaLucas.BZCF.bz_creative_telescoping`;
- `ZetaLucas.BZCF.PhatSum_eq_Phat` and `ZetaLucas.BZCF.PSum_eq_PBZ`;
- `ZetaLucas.BZStar.star_creative_telescoping`;
- `ZetaLucas.BZStar.PStarSum_eq_Phat`.

The workflow must show `sorryAx` on the quarantined declarations and no `sorryAx` on the named conditional infrastructure. A file-level “sorry-free” label is prohibited when a downstream declaration imports a quarantined theorem.

## Referee disposition

```text
OZ-NEXT-005A  COMPLETE_WITH_NEGATIVE_RECONCILIATION
OZ-NEXT-005B  COMPLETE_FOR_NORMALIZED_FINITE_REPLAY
OZ-NEXT-005C  COMPLETE_FOR_NAMED_NEAREST-SOURCE SET; NOVELTY STILL PENDING
OZ-NEXT-005D  COMPLETE_WITH_DECLARATION QUARANTINE
OZ-WP00       OPEN
```

Remaining blockers are the unproved `(T1-top)` identity, the non-promoted `(DEPTH)` certificate, specialist proof review of the harmonic B-row and H1–H5 applications, exhaustive novelty review, and the eight open irrationality bridges.
