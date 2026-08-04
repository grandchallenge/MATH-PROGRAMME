# OZ-RT-BZ-T3-001 — Brown–Zudilin T3

This package resumes the exact compact top-row bridge identity:

```text
Σ_{k,l=0}^n T(n,k,l)·(W¹(k,l)+2 w5_sym(n,k,l)) = 0,  for every n ≥ 0.
```

The target, normalization, endpoints, harmonic conventions, and Brown–Zudilin recurrence are locked in `OZ_RT_BZ_T3_001.json`.

## Result

No unbounded symbolic proof and no exact source-normalized counterexample were obtained.

The pinned source reports that the fixed-letter local/residue classes, two-variable jets, and moment-tower extensions fail as certificate classes. The remaining admissible route is a creative-telescoping certificate over `Q(n,k,l)`, either

```text
T·defect = Δ_k R + Δ_l S
```

or a two-stage fiber telescoper. At the pinned revision there is no committed producer, candidate certificate, locked ansatz/degree bound, or independently replayable proof object.

Disposition:

`OPEN_WITH_CHARACTERIZED_BLOCKER`

## Evidence boundary

The independent X007 replay checks exact compact sums for `0 ≤ n ≤ 34` and recurrence residuals for `0 ≤ n ≤ 31`. These are finite evidence only.

The package does not prove or refute T3, does not unconditionally prove the compact top row, does not repair quarantined Lean declarations, and does not advance sharp-12. T1-top and DEPTH remain separately open.
