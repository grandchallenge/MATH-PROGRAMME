# VGSE-MS-M2 — identifiability-aware infinitesimal inverse design

**Governed work:** `VGSE-KINEMATIC-INVERSE-DESIGN-001`  
**Parent phase:** `VGSE-MECHANICAL-SEMANTICS-001`  
**Tracker:** `grandchallenge/MATH-PROGRAMME#1179`  
**Protected predecessor:** M1 terminal merge/readback `8b9e442220b7cd3d3dd4e926f10d10847e4349e2`  
**State at activation admission:** `AUTHORIZED_READY`

## Objective

Synthesize at least one admissible TE3-native design whose declared flat-state kinematic observable matches a target, without pretending the target uniquely identifies quotient coordinates or geometry.

M2 is the first VGSE tranche directly governed by the adopted GCL-ID-00 identifiability preflight.

## Observable

For an admissible realization `g`, M1 computes the four-dimensional labeled hinge-rate mechanism subspace

`H(g) subset R^10`

and its orthogonal projector `P_H(g)`.

M2 defines the basis-invariant hinge-participation profile

`d(g) = diag(P_H(g))`.

Properties inherited from the projector:

- `0 <= d_i <= 1`;
- `sum_i d_i = rank(P_H) = 4` on the retained M1 mobility-four class;
- the profile is invariant to a change of basis inside the mechanism subspace;
- it remains a compressed observable and does not uniquely encode the full projector.

The exact observable contract is stored in `TARGET_CONTRACT.json`.

## Identifiability preflight

The required GCL-ID-00 record is:

`governance/identifiability_preflights/VGSE-MS-M2-ID-001.json`.

The preflight disposition is deliberately `UNRESOLVED` for representative recovery.

M1 already proves that one quotient point can admit several distinct geometric representatives with distinct mechanism subspaces. M2 therefore does not authorize a claim that a target participation profile determines one quotient or one geometry.

The allowed inverse target is set-valued:

> construct one or more admissible design witnesses whose participation profile matches the target within the declared tolerance.

If several witnesses are found, preserve them.

## Authorized stages

### D0 — target and pipeline audit

- reuse the exact M0 realization and M1 projector code;
- generate the positive-control target from the retained `BASELINE-B1` realization;
- replay the target profile and invariant checks;
- verify that mechanism-basis choice does not change the target profile;
- bind all side information and unavailable fixture information explicitly.

### D1 — bounded witness synthesis

Attempt to synthesize at least one admissible design witness for the positive-control target.

The implementation may use:

- retained-atlas retrieval as a deterministic replay baseline;
- local log-quotient perturbations;
- an explicitly declared branch-conditioned M0 representative selector.

The output is a witness or a named search/selector/conditioning boundary.

It is not a unique inverse.

### D2 — conditional falsification target

D2 is not authorized by activation alone.

If D1 closes cleanly, a later transition may test one off-grid or interpolated profile target. Any infeasibility claim must distinguish structural evidence from optimizer or selector failure.

## Required falsification

M2 must challenge, not assume, at least one stronger claim:

- `the target participation profile uniquely determines the quotient coordinates`;
- `the target participation profile uniquely determines the geometric representative`.

A multi-solution witness is a positive identifiability result even if inverse uniqueness fails.

## GCL-ID-00 stopping rule

If M2 constructs two distinct admissible designs with the same target profile within the declared observational relation, representative-level uniqueness is structurally refuted on that domain.

At that point, do not respond by merely trying a stronger optimizer.

Retain the equivalence class or add explicitly justified information.

## Claim boundary

M2 remains flat-state infinitesimal kinematic design under the GCL-defined M1 semantics.

It does not establish:

- unique recovery of quotient coordinates or geometry;
- finite rigid foldability;
- mountain/valley assignment;
- collision-free motion;
- finite thickness;
- stiffness, force, energy, material, constitutive, or actuation behaviour;
- manufacturing;
- product performance;
- `VGSE-C06` or source correspondence;
- novelty, patentability, or commercial value.
