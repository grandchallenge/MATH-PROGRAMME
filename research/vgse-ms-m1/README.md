# VGSE-MS-M1 — rigid-panel kinematic semantics

**Governed work:** `VGSE-KINEMATIC-SEMANTICS-001`  
**Parent phase:** `VGSE-MECHANICAL-SEMANTICS-001`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#1163`  
**Protected predecessor:** M0 terminal merge/readback `c09d652f7a85b5b7277ce3c89a50d3bfc84d7d20`  
**State at activation admission:** `AUTHORIZED_READY`

## Objective

Attach one explicit infinitesimal rigid-panel semantics to the protected M0 TE3 realization family.

The first question is deliberately local and kinematic:

> At the flat TE3 realization, what infinitesimal body-hinge motions are permitted by the GCL-defined rigid-panel interpretation, and is that mobility stable across quotient samples and geometric branches?

No stiffness, material law, thickness, contact, friction, actuation, mountain/valley assignment, or finite folding is assumed.

## GCL-defined body-hinge interpretation

The embedded dual graph has eight bounded cells corresponding to the eight internal primal vertices `F01` through `F08`. M1 treats those bounded cells as rigid planar panels.

The ten internal primal edges are shared panel boundaries and are treated as ideal revolute hinges about their embedded dual segments. The six boundary primal edges `B1` through `B6` are free boundary edges.

One panel is fixed to quotient out global Euclidean rigid motion. The canonical fixed panel is `F04`; root-choice invariance must be replayed on at least the protected baseline.

The exact algebraic matrix convention is stored in `KINEMATIC_MODEL_CONTRACT.json`.

## Stages

### K0 — model audit

- verify panel and hinge incidence against the protected graph;
- verify every declared hinge corresponds to one nonzero M0 dual segment;
- construct the body-hinge Jacobian convention;
- verify matrix dimensions and fixed-body invariance;
- preserve the distinction between this GCL-defined semantics and any historical/source origami interpretation.

### K1 — infinitesimal mobility atlas

For every retained valid M0 realization:

- construct the flat-state body-hinge Jacobian;
- compute rank and infinitesimal mobility after rigid-motion removal;
- compute constraint-dependency/self-stress dimension;
- compare across quotient samples and across the multiple baseline geometric representatives;
- relate rank changes, if any, to M0 branch/sensitivity features;
- retain numerical singular-value margins.

### K2 — conditional local continuation

K2 is not authorized by activation alone. It may be proposed only if K1 identifies a nontrivial infinitesimal mechanism direction worth continuing.

Even then, K2 is a bounded local continuation experiment, not a claim of finite rigid foldability.

## Required falsification

K1 must test at least:

1. `all retained TE3 realizations have the same flat-state infinitesimal mobility`;
2. `the quotient point uniquely determines the flat-state infinitesimal kinematic state despite M0 geometric branch multiplicity`.

Either may fail. A counterexample is a valid result.

## Terminal dispositions

- `KINEMATIC_SEMANTICS_STABLE_MOBILITY_CLASS_ESTABLISHED`
- `KINEMATIC_SEMANTICS_BRANCH_DEPENDENT`
- `KINEMATIC_SEMANTICS_RIGID_AT_FLAT_STATE`
- `KINEMATIC_SEMANTICS_SINGULAR_OR_COMPONENT_RESTRICTED`
- `KINEMATIC_SEMANTICS_MODEL_BRIDGE_OBSTRUCTED`
- `KINEMATIC_SEMANTICS_UNRESOLVED`

## GCL-ID-00

K0/K1 are forward kinematic analysis from declared geometry and therefore do not trigger GCL-ID-00 merely because linear algebra is used.

If M1 introduces a claim that observed motion uniquely identifies quotient or geometry, that inverse subproblem must create an identifiability preflight before substantial inverse work.

M2 remains blocked.

## Claim boundary

M1 does not establish source correspondence or `VGSE-C06`, finite rigid foldability, mountain/valley assignment, collision-free motion, finite thickness, stiffness, force, energy, constitutive response, materials, actuation, manufacturing, product performance, novelty, patentability, or commercial value.
