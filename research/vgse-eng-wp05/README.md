# VGSE-ENG-WP05 — exact cycle-invariant quotient reconstruction

**Governed work:** `VGSE-CYCLE-INVARIANT-QUOTIENT-RECONSTRUCTION-001`  
**Protected start:** `dc0e579ce8f9dddf04045b6eea2669d8fa533003`  
**Terminal candidate:** `CYCLE_INVARIANT_QUOTIENT_RECONSTRUCTION_PARTIAL`

## Question

Can the eight-dimensional WP01 mathematical weight quotient be reconstructed exactly from invariant products of the C05 embedding geometry?

## Answer

Partly.

The exact cancellation mechanism is real. But the graph does not have eight independent closed cycles. It has only three.

The eight-dimensional gauge-invariant weight space decomposes naturally as:

[
8=3	ext{ closed cycles}+5	ext{ boundary paths}.
]

For the three closed cycles, every branch-dependent discrete-holomorphic factor cancels exactly. The geometry therefore exposes the signed weight invariants directly:

[
-rac67,qquad -rac4{21},qquad rac{18}{175}.
]

All five retained C05 branches reproduce those three values to numerical replay precision.

For the other five directions, the same internal factors cancel, but one boundary factor survives at each path endpoint. The raw geometric products consequently vary substantially across branches. Once the certified branch boundary factors are divided out, the remaining five exact weight invariants are recovered:

[
1,quad 1,quad rac{25}{3},quad -rac72,quad rac{25}{2}.
]

Thus:

- **geometry alone:** 3 of 8 quotient directions;
- **geometry + certified branch boundary calibration:** all 8 directions.

## Exact quotient chart

The five path monomials and three cycle monomials form a complete integer basis of the gauge-invariant lattice.

Their positive versions (y) satisfy

[
log y=Alog x,
]

where (x) is the protected WP01 coordinate vector and (A) is the integer matrix in `QUOTIENT_CHART.json`.

[
det A=-1.
]

So the natural graph invariant basis is not merely full rank; it is unimodularly equivalent to the WP01 chart.

## Why this is not yet a full geometry inverse

The five boundary factors used to normalize the path products come from the algebraic branch data (zeta,widetildezeta). WP05 has not shown how to recover those factors from embedding coordinates alone.

Calling the calibrated reconstruction a geometry-only map would therefore hide exactly the information still missing.

## Artifacts

- `GRAPH_INCIDENCE.json` — protected graph, orientations, signs.
- `GAUGE_ACTION.json` — exact 8-by-16 gauge action.
- `INVARIANT_LATTICE.json` — five path + three cycle basis.
- `CANCELLATION_DERIVATION.md` — exact cancellation proof and boundary obstruction.
- `BRANCH_REPLAY.json` — five-branch numerical replay.
- `QUOTIENT_CHART.json` — exact unimodular map to/from WP01.
- `RESULTS.json` — bounded disposition.
- `CLAIM_LEDGER.json` — claim classes and exclusions.
- `NEXT_ACTION.md` — exact reopening boundary.
- `analyze_wp05.py`, `test_wp05.py` — deterministic artifact replay.

## Deterministic replay

```bash
python research/vgse-eng-wp05/analyze_wp05.py --check
python research/vgse-eng-wp05/test_wp05.py
```

## Claim boundary

These are mathematical graph and embedding facts. They do not establish source correspondence, mechanics, manufacture, product behavior, patentability, or commercial value.
