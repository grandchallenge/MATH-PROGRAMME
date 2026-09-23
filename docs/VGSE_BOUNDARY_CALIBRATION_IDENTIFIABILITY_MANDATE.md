# VGSE-ENG-WP06 — Boundary Calibration Identifiability

**Governed work ID:** `VGSE-BOUNDARY-CALIBRATION-IDENTIFIABILITY-001`  
**Campaign:** `VGSE-001`  
**Tracker:** #1053  
**Protected start:** `797139a7aef1a445461e24151493885be38159f1`

## Question

Are the five boundary calibration directions missing from WP05 recoverable from admitted embedding geometry alone?

WP06 must distinguish two very different statements:

1. **Fixed-response catalogue.** The five protected C05 branches were generated from one already-fixed quotient/response. Identifying the branch from its geometry does not constitute recovery of the quotient.
2. **Structural inverse.** Given the labeled embedding geometry and graph, but not the known quotient, algebraic branch witness, or source correspondence, determine whether the quotient is unique.

Only the second answers the geometry-to-quotient question.

## Candidate boundary-rescaling symmetry

For each degree-one boundary vertex (U_i), let (eta_i) denote its discrete-holomorphic boundary factor and let (k_{B_i}>0) be its boundary-edge weight.

Test the positive rescaling

[
eta_imapsto c_ieta_i,qquad
k_{B_i}mapsto c_i^{-1}k_{B_i},qquad c_i>0,
]

with the complementary boundary datum rescaled inversely so that the prescribed boundary edge product remains fixed.

The first obligation is to determine exactly whether this transformation preserves:

- every primitive edge increment;
- every interior discrete-holomorphic equation;
- the prescribed boundary geometry;
- positivity and Kasteleyn signs;
- the C05 mathematical embedding conditions that do not already encode the known quotient.

If it does, compute its induced action on the WP05 invariant basis.

## Required quotient-rank test

WP05's five path basis rows have boundary exponents

[
(-B_1-B_2),quad
(-B_1+B_3),quad
(-B_1+B_4),quad
(-B_1-B_5),quad
(-B_1-B_6).
]

Under boundary rescaling, compute the exact linear map from

[
(log c_1,ldots,log c_6)
]

to the five logarithmic path coordinates.

Determine its rank and kernel exactly.

If the rank is five, then one fixed embedding admits a five-dimensional family of gauge-inequivalent quotient points unless an independently justified boundary normalization removes the symmetry.

## Anti-circularity test

A proposed recovery of the boundary factors is inadmissible as geometry-only if it consumes any of:

- the protected WP01 quotient values;
- the pinned response matrix or its arrangement forms;
- the algebraic branch witness (x,y);
- a lookup table over the five retained branches;
- source-to-pinned-C correspondence not independently established.

It is permitted to use these objects only to **check** a geometry-derived formula after that formula has been obtained independently.

## Branch-coordinate trap

The five C05 embeddings are distinct, so an interior coordinate may identify which of the five algebraic roots generated a branch. WP06 must not confuse this with structural quotient recovery.

If the map “geometry → branch label → already-known quotient” is the only full reconstruction available, classify it as circular for the structural inverse question.

## Terminal outcomes

Terminate at one of:

- `BOUNDARY_FACTORS_GEOMETRY_IDENTIFIABLE`
- `BOUNDARY_FACTORS_IDENTIFIABLE_WITH_CANONICAL_NORMALIZATION`
- `BOUNDARY_CALIBRATION_FIVE_DIMENSIONAL_OBSTRUCTION`
- `BOUNDARY_CALIBRATION_PARTIAL_IDENTIFIABILITY`
- `BOUNDARY_CALIBRATION_UNRESOLVED`

A negative identifiability theorem is a successful outcome.

## Required artifacts

Substantive branch `research/vgse-eng-wp06` must retain at least:

- `BOUNDARY_SYMMETRY.json`
- `QUOTIENT_ACTION.json`
- `IDENTIFIABILITY_PROOF.md`
- `NORMALIZATION_AUDIT.json`
- `RESULTS.json`
- `CLAIM_LEDGER.json`
- deterministic replay and tests.

## Claim boundary

WP06 concerns mathematical identifiability only. It does not establish VGSE-C06, source correspondence, mechanics, rigid foldability, collision freedom, finite thickness, material behaviour, manufacturing, product performance, patentability, or commercial value.

## Review and protection

Completion requires exact-head deterministic replay, distinct Adversary and Referee reviews, continuity rebind, required checks, native merge queue, protected-main readback, terminal checkpoint update, and tracker closure.
