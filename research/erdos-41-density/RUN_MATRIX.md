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

## Off-spectrum spectral-matching competition

| Mathematical obligation | Verification | Disposition |
| --- | --- | --- |
| Fixed-d matching among internal and external pair representations | Complete written B3 three-summand multiset proof | Proved |
| Pointwise sum of correlations at nonzero difference ≤block size | Finite B3 fixture tests and hostile non-B3 union | Proved |
| Exact first off-spectrum mass and quadratic budget | Rational polynomial identity, Counter tests | Proved |
| Spectral arithmetic certificate | Pinned Lean 4.29.1 compiler receipt and SHA256 when GREEN | Separate checks |
| Persistent B3 density forces collision | Ordinary capacity estimates have no accumulating scale factor | OPEN |

The finite theorem is not an automatic Forge/Solve/Cert transition.

## Translation-invariant B3 zero-sum fiber audit

| Obligation | Evidence | Status |
| --- | --- | --- |
| Fixed-nonzero-lag matching of positive unordered pair supports | Complete B3 triple-uniqueness proof; finite exhaustive and genuine 29-element checks | PROVED |
| Weighted fiber bound and quadratic-only diameter estimate | Exact arithmetic; bounded multi-block tests | PROVED |
| Arbitrarily many disjoint geometrically separated blocks share lag 1 | Explicit infinite base-16 B3 construction with carry-free digit proof; 20-block exhaustive check | PROVED |
| Non-B3 hostile test and incorrect spectral-disjointness assertion | Regression fixtures | REFUTED incorrect candidate |
| Lean arithmetic/digit algebra | Pinned toolchain receipt after compilation | SEPARATE arithmetic only |
| Density-sensitive higher-order overlap leading to Erdős #41 | Not obtained | OPEN |

The infinite example is intentionally sparse, with A(N)=O(log N); it is **not** a counterexample to Erdős #41.

## Density-forced geometric mixed-block mass

| Obligation | Method | Disposition |
| --- | --- | --- |
| Exact two-block mixed-center mass and weighted mass | Polynomial identities; genuine B3 deterministic tests | PROVED |
| Positive lower density forces x,y at separated geometric scales | B3 cubic finite counting bound and two lower-density endpoints | PROVED conditionally |
| Mixed support ≥3xy and c^4 N^(2/3)/24 | Pointwise B3 positive-pair matching | PROVED |
| Summation over many cuts | Exact representation span-multiplicity identity | PROVED; fake logarithmic factor excluded |
| Single-scale finite-critical examples | Bose-Chowla published modular B3 construction | Literature-grounded method boundary |
| Matching budget eventually exceeded for every c>0 | Lower demand order N, ambient budget order N^(4/3) | NOT PROVED; present argument insufficient |
| Original Erdős #41 | No infinite collision/density valley | OPEN |

Source: [DENSITY_FORCED_MIXED_BUDGET.md](DENSITY_FORCED_MIXED_BUDGET.md).

## Mixed-lag geometric dispersion and moments

| Obligation | Proof and test | Status |
| --- | --- | --- |
| Weighted mixed first/second moments | Exact independent-sampling variance identity; Fraction checks | PROVED |
| Two-sided extreme-type lag sets ≥xy | Fixed-lag positive-pair matching, sign-separated supports | PROVED |
| One-third total mixed weight outside central interval | Exact extreme-type weighted mass | PROVED |
| Density-sensitive ≥(c^4/72)N^(2/3) lags in each macroscopic tail | Previously proved separate-block density extraction | PROVED conditionally |
| Hostile non-B3 failure | Genuine finite example of failing support bounds | Verified |
| Lean polynomial receipts | Pinned 4.29.1 compiler; exact success only after receipt GREEN | Kernel arithmetic only |
| Mixed-lag upper o(N^(2/3)) or cross-scale weighted overload | No such bound established | OPEN |

See [MIXED_LAG_BALLISTIC_DISPERSION.md](MIXED_LAG_BALLISTIC_DISPERSION.md).
\n## Cross-scale mixed-lag collision energies

| Obligation | Verification | Result |
| --- | --- | --- |
| Exact cross-family centered-lag overlap energy | Direct pair-sum difference counting; independent integer correlation tests | PROVED |
| Same-center contribution zero for disjoint genuine B3 blocks | B2 injection from B3; hostile non-B2 fixture | PROVED |
| Within-family self-collision identity | Exact pair-sum autocorrelation on twice outer differences | PROVED |
| Global pressure with actual within energies | Cauchy–Schwarz with controlled occupied support size | PROVED, may be vacuous |
| No automatic logarithmic gain when partitioning inner B3 set | Exact missing cross-positive-pair identity | PROVED |
| Genuine finite B3 2/3-family overlap zero; 4-family nonzero | Executable deterministic enumeration | VERIFIED |
| Persistent positive B3 density forces matching overload | Missing density-sensitive cross-energy lower bound | OPEN |

Written proof: [CROSS_SCALE_OVERLAP_ENERGY.md](CROSS_SCALE_OVERLAP_ENERGY.md); no MATHCERT, mathematical resolution, or Solve dispatch.

## Density-localized zero-overlap selection

| Obligation | Method | Boundary |
| --- | --- | --- |
| Lag intervals disjoint when inner gaps exceed outer diameter | Exact integer interval endpoints | PROVED |
| B3 lower bound on actual occupied lag support | Weighted positive-pair matching | PROVED |
| Hypothetical positive lower density populates geometric inner shells | Cubic finite B3 upper bound, nested density lower bound | PROVED conditionally |
| Outer pigeonhole bin with controlled diameter and many B3 points | Explicit bin count B_k | PROVED conditionally |
| k(N) proportional to log N; all disjoint, polynomial support per family | Exact exponent inequalities | PROVED conditionally |
| Existing genuine B3 positive, hostile non-B3 tests | Deterministic tests | Verified |
| Full inner-color positive pairs against narrow outer bin | B3 finite interval upper bound, O_c(N^(17/18)) total | PROVED conditional method no-go |\n| Outer occupied bin count and cross-bin collision reduction | B3 short interval packing and exact off-diagonal energy | PROVED conditionally |\n| Complete mixed-spectrum collision under persistent density | Not deduced; selection-independent higher-order input missing | OPEN |

See [DENSITY_LOCALIZED_ZERO_OVERLAP.md](DENSITY_LOCALIZED_ZERO_OVERLAP.md). No Erdős #41 solved state, certification or Solve dispatch.
