# E041 density transfer: bounded run matrix

The present programme separates mathematical proof, computer checking, and conjectural exploration. Code changes are admitted only under protected GitHub checks; proof evidence is not MATHCERT certification.

| Track | Method | Acceptance | State |
| --- | --- | --- | --- |
| E3 two-term padding | Lean 4.29.1 with pinned mathlib | Compiler exit 0; source SHA-256; no admitted holes | Kernel checked |
| Source-index affine H3 | Lean 4.29.1 with pinned mathlib | Compiler exit 0; source SHA-256; no admitted holes | Kernel checked |
| Affine cubic growth | Lean 4.29.1 core | Compiler exit 0; source SHA-256; no admitted holes | Kernel checked |
| Actual image H3 | Full written proof | Inverse of injective affine image and sum/card identity | Written proof; not a separate kernel theorem |
| Counting liminf equivalence | Full written proof | Ordered enumeration and counting growth equivalence | Written proof; not a separate kernel theorem |
| Finite adversarial replays | Python standard-library unittest | Exact E3-to-H3 prefixes, count identity, M3 countercase | Four tests passed |
| Multiscale M3 packing | Elementary written proof | Number of three-term multisets fits into sum range | Proved elementary lemma |
| Dyadic shell-energy deficit | OPEN new claim | Independent proof or counterexample | Unresolved; no solution promotion |

The source-locked proof files use Lean 4.29.1; mathlib git commit 5e932f97dd25535344f80f9dd8da3aab83df0fe6. Colab is not used to certify this mathematical result; the local authenticated CHAD Lean compiler supplies verification and provenance. A new Colab job would need explicit protected registration and an authorized issue, rather than reusing the previous finite #41 one-shot receipt.

## Shell-energy adversarial audit, October 2026

| Task | Evidence | Disposition |
| --- | --- | --- |
| Finite cubic convolution inequality | [SHELL_HARDY_AUDIT.md](SHELL_HARDY_AUDIT.md), rational arithmetic tests | Written proof, Lean 4.29.1 checks the cubic two-term identity with exit 0, plus 5 exact Python test methods |
| Critical-density shell/cesaro equivalence | Quantitative constants 1/288 and 1 in finite inequality (2) | Proved for any nonnegative shell occupancies |
| Packing-only hostile profile | Rare empty dyadic-shell gaps, limit 7/12 for shell energy | Refutes derivation from ordinary cubic packing plus density dips, **not** an M3 counterexample |
| Exact M3 finite-window valleys | Equivalent statement (V), powered by uniformly bounded u_k | Proved, conditional on the standard packing bound |
| Original M3 shell-energy deficit | Docket #2622, multiscale gate | OPEN, stronger target |

This audit does not certify the full Erdős conjecture or authorize a new worker task without queue governance.

## Cross-pattern Hall method audit

| Bound | Status |
| --- | --- |
| Generic shell-pattern Hall injection | Elementary written proof; all patterns including repeated shell labels |
| Two-adjacent-shell mixed-pattern inequality | Elementary written proof, arithmetic Lean certificate and hostile x=y=7 fixture |
| Universal-Hall counterprofiles, gapped and ungapped | Written infinite proof; seven new deterministic tests of numeric and actual finite M3 fixtures |
| Original finite-window valley for actual M3 | OPEN: range-only Hall constraints are insufficient |

Consult [CROSS_PATTERN_HALL.md](CROSS_PATTERN_HALL.md). A feasible shell-occupancy profile need not be an M3 set.

## Additive-shadow / second-moment track

| Obligation | Status |
| --- | --- |
| Exact cubic shadow cardinality and cross-block disjointness | Written proof, finite exhaustive checks on genuine M3 fixtures; not a full Lean set-injection proof |
| Diameter and difference-shadow inequalities | Written elementary corollaries; finite hostile tests |
| Distinct-integer second-moment inequality | Written sorted-integer proof; exact-rational and integer checks |
| XXY/XYY cross-pattern moment counterfixture | Exact witness, individual patterns injective and Hall-feasible, combined moment slack -1872 |
| Polynomial/variance algebra and fixture calculations | Lean 4.29.1 kernel-checked when receipt GREEN |
| Infinite M3 finite-window density valley | OPEN; no solution promotion |

See [ADDITIVE_SHADOW_MOMENTS.md](ADDITIVE_SHADOW_MOMENTS.md) and ADDITIVE_SHADOW_RECEIPT.json.
\n## Arbitrarily many cubic-shadow blocks

| Obligation | Verification | State |
| --- | --- | --- |
| Exact first/second moments of T(X) | Written count proof; exhaustive finite genuine B3 enumeration | Proved |
| Cross-block centroid/variance identity (CROSS) | Written proof for any finite r; exact-rational tests on disjoint partitions | Proved |
| Translation covariance and parity obstruction | Exact algebra and concrete B3 anchored collision | Proved |
| Polynomial algebra certificates | Pinned Lean 4.29.1 exit 0 when final receipt GREEN | Separate kernel checks |
| Persistent lower density implies shadow collision | Scale test finds no divergent factor | Unresolved |
| Complete Erdős #41 solution | Not claimed | OPEN |

See [CROSS_SCALE_SHADOW_MOMENTS.md](CROSS_SCALE_SHADOW_MOMENTS.md); no mathematical certification or protected dispatch follows automatically.

## Exact pair-sum autocorrelation / cross-block spectra

| Obligation | Verified method | State |
| --- | --- | --- |
| B3 pair-sum autocorrelation selector | Complete written triple-multiset injection proof; genuine B3 exhaustive/block tests | PROVED |
| Cross-P_X/P_Y difference exclusion | Written color-multiplicity contradiction; random genuine B3 partitions | PROVED |
| Full A-indexed Gram eigenspectrum | Closed-form block-matrix decomposition; randomized quadratic-form certificates | PROVED |
| Naive PSD-only or independently summed cross-spectra strategy | Exact cardinality-only eigenvalues; genuine B3 overlapping cross-spectra witness | OBSTRUCTED |
| Arithmetic/polynomial Lean receipts | Lean 4.29.1 exit 0 when recorded in SHADOW_CORRELATION_RECEIPT.json | SEPARATELY CHECKED |
| Genuine infinite M3 density valley and shell energy deficit | No growing contradiction established | OPEN |

## Fourth-moment off-spectrum additive energy

| Obligation | Method | State |
| --- | --- | --- |
| Pair-sum energy exact spectrum decomposition | B3 selector plus integer Counter proof | Written exact theorem |
| Cauchy fourth-moment lower bound | Sum of pair-pair differences, support diameter bound | Written exact theorem |
| D^(5/3) off-spectrum bound | Finite-block critical-size conditional inequalities | Proved conditionally, not a B3 density solution |
| Positive genuine M3 fixtures and negative fake-B3 clusters | Five new deterministic exact-rational tests | Passed |
| Lean arithmetic certificates | Pinned Lean 4.29.1, log and source hash | Independently checked only when receipt GREEN |
| Infinite cross-scale overlap contradiction | Not obtained | OPEN |

See [OFF_SPECTRUM_FOURTH_MOMENT.md](OFF_SPECTRUM_FOURTH_MOMENT.md). No theorem certification or Solve dispatch is inferred.
