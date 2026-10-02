# VGSE-ENG-WP05 — Exact Cycle-Invariant Quotient Reconstruction

**Governed work ID:** `VGSE-CYCLE-INVARIANT-QUOTIENT-RECONSTRUCTION-001`  
**Campaign:** `VGSE-001`  
**Programme:** `MATH-PROGRAMME`  
**Tracker:** #1048  
**Research phase:** fresh bounded successor to terminal WP04

## Primary question

Can the protected WP01 eight-dimensional positive weight quotient be reconstructed exactly from gauge-invariant cycle/path observables of a qualified C05 embedding?

The target is not an empirical fit. It is an exact structural map, if one exists,

[
Psi:mathcal G_{mathrm{C05}}longrightarrow mathcal Q,qquad
mathcal Q=(mathbb R_{>0})^8,
]

derived by eliminating the branch-dependent discrete-holomorphic factors in the retained t-embedding primitive.

## Authority and live bind

Read-only reconnaissance on 2026-09-23 bound this admission to:

- protected `MATH-PROGRAMME/main`: `4b78daac0b85298957b52e34687423e5442b5e51`;
- terminal predecessor checkpoint `VGSE-GEOMETRY-QUOTIENT-COUPLING-001`, state `TERMINAL`;
- predecessor terminal checkpoint merge `2b39c8507294ac673a8e8e175b22a87a7484feea`, verified as an ancestor of current protected main;
- protected WP04 substantive merge `05e384156859269221e77fdcd61606e06f56ddd1`;
- protected MATHCERT head `2f27aed33b32b4caf6ff8622c87cfd6d40e97607`;
- protected MATHSOLVE head `b0854bb7770296b610b655753bc62b27365b27bb`.

No duplicate cycle-invariant VGSE successor was found before mutation.

The Human Steward explicitly authorized proceeding to this successor after WP04 closure.

## Protected starting facts

Do not reopen these facts unless a contradiction is found.

1. WP01 identifies an eight-dimensional positive quotient of the 16 edge weights after internal-vertex gauge.
2. WP02 provides the protected quotient-response inverse.
3. WP03 provides the protected exact response-manifold feasibility relations.
4. WP04 establishes that existing geometry/quotient observations do not identify a general empirical map: the five generated C05 geometries all reuse one quotient fixture.
5. The protected C06 producer audit falsifies the visible Euclidean dual-edge-length bridge to pinned `C` under its declared semantics.
6. In the retained reconstruction, an oriented dual-edge increment is computed as
   [
   delta_e=f(w_e),s_e,k_e,widetilde f(b_e),
   ]
   where `k_e>0` is the graph weight, `s_e` is the Kasteleyn sign, and the two vertex factors depend on the discrete-holomorphic branch.

WP05 asks whether exact combinations of the (delta_e) cancel the vertex factors and expose the weight quotient.

## Central algebraic hypothesis

For an alternating closed walk in the bipartite graph, products of edge increments with alternating exponents may cancel every white and black vertex factor.

A prototype invariant is

[
I_C(delta)=
rac{prod_{j mathrm{odd}}delta_{e_j}}
     {prod_{j mathrm{even}}delta_{e_j}}.
]

If each incident vertex factor occurs with net exponent zero, then

[
I_C(delta)=
(	ext{known orientation/sign factor})
rac{prod_{j mathrm{odd}}k_{e_j}}
     {prod_{j mathrm{even}}k_{e_j}}.
]

This formula is a hypothesis until derived with the actual graph orientation, boundary edges, Kasteleyn convention, and complex-valued increments.

Do not assume magnitudes are sufficient. Do not discard phase unless the exact derivation licenses it.

## First substantive obligation — exact incidence algebra

Before evaluating numerical examples:

1. reconstruct the exact 16-edge bipartite incidence matrix;
2. encode internal-vertex gauge as an exponent-action matrix on positive weights;
3. compute the integer nullspace / invariant lattice of that action;
4. determine its rank without using the WP01 coordinate choice as an input;
5. derive which invariant-lattice elements are representable by closed alternating cycles or, if boundary vertices intervene, by declared path combinations;
6. derive the corresponding geometry-side products from the exact primitive factorization;
7. account explicitly for orientation reversal, complex phase, and Kasteleyn signs.

The natural invariant basis must be discovered from the graph first. Only afterward may it be compared with the eight protected WP01 quotient coordinates.

## Required falsification tests

The programme must actively try to break the cancellation claim.

At minimum:

- verify cancellation symbolically at every internal white and black vertex;
- detect invariants contaminated by boundary-vertex factors;
- test orientation reversal and cycle-basis changes;
- test sign conventions rather than taking absolute values by default;
- evaluate every surviving invariant independently on all five C05 branches;
- require branch agreement to the strongest precision justified by the retained evidence;
- compare geometry-derived invariant values with the corresponding exact invariants of the protected C04/WP01 weight representative;
- distinguish a genuine exact identity from numerical coincidence.

The five C05 branches are permitted here as repeated tests of branch-factor cancellation. They remain one quotient point and must not be described as five independent quotient observations.

## Exact quotient reconstruction test

If the natural invariant lattice has rank eight, determine whether its coordinates (y) and the protected WP01 coordinates (x) are related by an exact invertible monomial/rational chart transformation.

Prefer an integer exponent representation:

[
log y = Alog x
]

with (Ainmathbb Z^{8	imes 8}) when the mathematics permits it.

Record:

- the invariant basis;
- exponent matrix;
- determinant/rank;
- exact inverse when it exists;
- positivity/domain assumptions;
- singular or excluded loci;
- whether boundary-edge normalization is required.

Do not infer invertibility from numerical conditioning alone.

## Branch-invariance test

For every candidate invariant (I_j), evaluate

[
I_j(g_1),ldots,I_j(g_5).
]

If the exact cancellation hypothesis is correct, the five values should agree modulo only explicitly declared orientation/sign conventions.

Branch agreement is evidence for cancellation, not evidence for a general empirical (mathcal G	omathcal Q) law across quotient space.

## Minimum programme

1. recover graph incidence and gauge action;
2. compute the invariant lattice and rank;
3. derive cycle/path representatives;
4. prove or falsify nuisance-factor cancellation;
5. implement deterministic exact/symbolic replay where possible;
6. evaluate all five C05 branches;
7. compute the exact C04/WP01 weight-side invariant vector;
8. solve for the exact chart transformation to/from WP01 coordinates;
9. replay through WP02/WP03 only if an actual quotient reconstruction survives;
10. retain negative results and counterexamples;
11. terminate rather than fitting an unconstrained surrogate.

## Required artifacts

The substantive branch `research/vgse-eng-wp05` must retain at least:

- `README.md`
- `GRAPH_INCIDENCE.json`
- `GAUGE_ACTION.json`
- `INVARIANT_LATTICE.json`
- `CANCELLATION_DERIVATION.md`
- `BRANCH_REPLAY.json`
- `QUOTIENT_CHART.json`
- `RESULTS.json`
- `CLAIM_LEDGER.json`
- `NEXT_ACTION.md`
- deterministic analysis/replay code
- regression tests

Exact symbolic identities must be stored separately from floating-point checks.

## Terminal outcomes

Terminate at one evidence-supported disposition:

- `CYCLE_INVARIANT_QUOTIENT_RECONSTRUCTION_ESTABLISHED`
- `CYCLE_INVARIANT_QUOTIENT_RECONSTRUCTION_PARTIAL`
- `CYCLE_INVARIANTS_EXIST_BUT_DO_NOT_SPAN_QUOTIENT`
- `NUISANCE_FACTOR_CANCELLATION_FALSIFIED`
- `CYCLE_INVARIANT_ROUTE_NON_IDENTIFIABLE`

A negative result is a valid terminal outcome.

## Claim boundary

WP05 may establish mathematical facts about the admitted bipartite graph, gauge action, t-embedding increments, cycle/path invariants, and the protected mathematical weight quotient.

It does not establish:

- VGSE-C06 or Figure-16-to-pinned-C source correspondence;
- physical stiffness or mechanical advantage;
- rigid foldability or collision freedom;
- finite thickness;
- material, hinge, friction, tolerance, or fatigue behaviour;
- manufacturability;
- product performance;
- novelty, priority, patentability, or commercial value.

A mathematical graph weight remains a mathematical graph weight.

## Review and protection

Substantive completion requires:

1. exact-head deterministic replay;
2. a distinct read-only Adversary review;
3. a distinct Referee review;
4. required status checks;
5. continuity rebind to the exact reviewed head where required;
6. native merge-queue admission;
7. exact protected-main readback;
8. terminal checkpoint update and tracker closure.

Any substantive mutation after review invalidates the reviews.

Admission of this mandate does not itself establish any cycle-invariant theorem.
