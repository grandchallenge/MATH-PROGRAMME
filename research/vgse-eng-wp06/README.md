# VGSE-ENG-WP06 — boundary calibration identifiability

**Governed work:** `VGSE-BOUNDARY-CALIBRATION-IDENTIFIABILITY-001`  
**Protected start:** `316495598b61a7959515b44a77ff94a77605984d`  
**Terminal candidate:** `BOUNDARY_CALIBRATION_FIVE_DIMENSIONAL_OBSTRUCTION`

## Core answer

There are two different mathematical categories that had been conflated.

### Source-defined t-embedding

The primary source defines geometric edge weights as Euclidean dual-edge lengths and requires, via TE3, that those lengths be gauge-equivalent to the graph weights with all boundary gauges fixed to one.

Therefore:

[
oxed{	ext{true t-embedding geometry}Rightarrow	ext{full weight quotient}}
]

All eight quotient directions are geometry-identifiable. No separate boundary-factor reconstruction is needed.

### Algebraic Kenyon–Smirnov realization without TE3

For the broader primitive factorization used in the retained C05 construction, six independent positive boundary rescalings preserve the entire embedding geometry while moving the five boundary-path quotient coordinates with rank five.

Therefore:

[
oxed{	ext{primitive geometry without TE3}Rightarrow 3/8	ext{ determined}+5/8	ext{ ambiguous}}
]

The one-dimensional kernel of the six-parameter action is the global bipartite rescaling.

## C05 finding

The current C05 evidence certifies discrete-holomorphic extension, exact primitive closure, the prescribed boundary, convex planar noncrossing geometry, Kawasaki equalities, and boundary-angle inequalities.

It does not record TE3.

A replay of the retained generated coordinates against the protected C04 weight class fails TE3 on all five branches by a very large margin. The simplest invariant requires (P_{12}=1); observed values are only (0.01184)–(0.02240).

The three closed-cycle coordinates still agree to about (10^{-13}), exactly explaining the WP05 result.

Because this conformance failure is currently a numerical replay, WP06 does **not** directly rewrite the protected C05 adjudication. An independent MATHCERT interval/exact TE3 replay is the next certification action.

## Artifacts

- `SOURCE_DEFINITION_AUDIT.json`
- `TE3_REPLAY.json`
- `BOUNDARY_SYMMETRY.json`
- `QUOTIENT_ACTION.json`
- `NORMALIZATION_AUDIT.json`
- `IDENTIFIABILITY_PROOF.md`
- `RESULTS.json`
- `CLAIM_LEDGER.json`
- `analyze_wp06.py`
- `test_wp06.py`

## Replay

```bash
python research/vgse-eng-wp06/analyze_wp06.py --check
python research/vgse-eng-wp06/test_wp06.py
```

## Boundary

These are mathematical identifiability and terminology/conformance results only. No C06 or physical/commercial claim follows.
