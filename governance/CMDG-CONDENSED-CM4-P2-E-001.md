# CMDG-CONDENSED-CM4-P2-E-001 — comparison reconstruction audit

## Purpose

This operation is restricted to **CM4-P2-E**: construct a machine-replayable natural equivalence
between the protected P2-D canonical measure/dual functor and the pinned
`Condensed.profiniteSolid` functor.

The P2-D predecessor is now protected authority. This operation therefore begins from the exact
protected merge rather than from the pre-merge P2-D candidate.

## Programme semantic boundary — representation versus reconstruction

CM4-P2-D and CM4-P2-E are intentionally different claim kinds.

**P2-D — `REPRESENTATION`.** The protected predecessor constructs the canonical, basis-free,
functorial measure/dual condensed-module model associated to `C(S,ℤ)`, together with its
Hom/duality interface. Its admitted output is the protected `measureFunctor` representation. P2-D
does **not** assert that this representation is `profiniteSolid`, and the existence of the duality
interface does not itself carry reconstruction or equivalence authority.

**P2-E — `RECONSTRUCTION/EQUIVALENCE`.** Starting only from that protected representation, P2-E
must construct the comparison data and universal-property proof that recover the canonical
`profiniteSolid` functor naturally. The terminal P2-E mathematical object is the natural
isomorphism

```lean
measureFunctor ≅ Condensed.profiniteSolid R
```

not merely the existence of `measureFunctor`, an objectwise equivalence, or a duality pairing.

The governed construction hierarchy is therefore

```text
P2-D representation / duality
  → finite natural comparison
  → measure-side right-Kan reconstruction
  → canonical right-Kan uniqueness
  → P2-E natural equivalence
```

This is a proof architecture, not a universal implication chain in category theory. In particular,
**duality does not imply reconstruction**. P2-E becomes available only when the global natural
comparison is actually constructed and replayed. Identity is recovered only in the categorical
sense that the reconstruction loop is naturally isomorphic to the canonical target; no literal
object equality or chosen-basis identification is claimed.

This semantic boundary is fail-closed for the operation: no downstream record may promote P2-D
availability into P2-E availability without discharging E1, E2, and E3 below.

## Protected predecessor

- operation: `CMDG-CONDENSED-CM4-P2-D-001`
- issue: #369 — completed
- implementation PR: #371
- reviewed head: `358466932fde181c927cd428613f4578f38bfc1c`
- protected tree: `ac1e21d2746ad951a9aa3c747895b28f56092bf8`
- protected merge / P2-E baseline: `839e04e1b862ffddfe5ce1d4d733ba954cd45d96`
- protected P2-D replay: run `31342558880` — success
- Programme policy: run `31342558852` — success
- GCL conformance: run `31342559115` — success
- predecessor state: `AVAILABLE`

## Exact formal environment

- Lean image/toolchain: `leanprover/lean4:v4.33.0-rc1`
- Lean commit: `62eed1db4d67327ec8120be05f1a1b0847d74561`
- mathlib commit: `79d0395a1825a6264ad5d269e35e60537518955e`
- mathlib tree: `d76f5e09b832a08949f6d8ad4fb80ce30527da64`
- coefficient ring: `ULift.{u + 1} ℤ`

## Frozen theorem targets

The Stage-A fixture freezes, without proving, the two exact natural-isomorphism targets:

```lean
FintypeCat.toProfinite ⋙ measureFunctor ≅ Condensed.finFree R
```

and

```lean
measureFunctor ≅ Condensed.profiniteSolid R
```

The first is the finite comparison. The second is the P2-E theorem target.

Neither an objectwise equivalence nor a basis-selected product presentation is an admissible
substitute.

## Exact-tree comparison audit

### 1. `Mathlib/Condensed/Solid.lean`

Blob: `f5214433f91ee87fc8fbe7e2746e0bd227faed2a`.

Material declarations:

- `Condensed.finFree`
- `Condensed.profiniteSolid`
- `Condensed.profiniteSolidCounit`
- `Condensed.profiniteSolidIsPointwiseRightKanExtension`

The pinned `profiniteSolid` is exactly the right Kan extension of the finite-free functor along
`FintypeCat.toProfinite`. This supplies the target extension and its finite counit.

### 2. `Mathlib/CategoryTheory/Functor/KanExtension/Basic.lean`

Blob: `1d8ed3b224af14a8d909ada051de840ae3d5c59c`.

Material declarations:

- `Functor.IsRightKanExtension`
- `Functor.rightKanExtensionUniqueOfIso`
- `Functor.rightKanExtensionUnique`

This is the canonical uniqueness mechanism. Once the protected measure functor is proved to be a
right Kan extension of its finite restriction, and that finite restriction is naturally
isomorphic to `finFree R`, the global comparison follows without any arbitrary basis choice.

### 3. `Mathlib/CategoryTheory/Functor/KanExtension/Pointwise.lean`

Blob: `eca4f781a97fc9948e726bb4b89a9ab1bc255f96`.

Material declarations include the pointwise right-Kan-extension cone interface and
`IsPointwiseRightKanExtension.isRightKanExtension`.

This supplies the preferred route for the measure side: prove the finite-quotient limit statement
objectwise, then obtain the ordinary right-Kan-extension property.

### 4. `Mathlib/Condensed/Discrete/Colimit.lean`

Blob: `7579e7ecc282d20d4c61d4e5d0e3e37994069e11`.

Material declarations:

- `Condensed.isColimitLocallyConstantPresheafDiagram`
- `Condensed.lanPresheafNatIso`

This supplies the exact finite-quotient colimit statement for locally constant functions on a
profinite set. P2-E must combine this with the protected closed-Hom duality to reverse that
colimit into the limit required by the measure functor's right Kan extension.

### 5. Protected P2-D fixture

`fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P2D.lean`

Blob: `7515583c1b56308bbd48c2c690addd3b432eba09`.

Material declarations:

- `CMDG.CondensedCM4P2D.measureFunctor`
- `CMDG.CondensedCM4P2D.dualityHomEquiv`

These are now protected inputs. P2-E may use them directly; it may not replace them by a
chosen-basis product model.

## Mathematical decomposition

The natural equivalence is not a single opaque step. The exact-tree audit resolves it into two
constructive obligations followed by a formally available uniqueness step.

### E1 — canonical finite comparison

For finite `X`, construct naturally in `X` the evaluation/Kronecker identification between the
dual of `C(X,R)` and the finite free module on `X`, and transport that identification through the
protected condensed-module realization.

This must be canonical. No Nöbeling basis enters because a finite set already carries its
canonical delta generators.

State: `OPEN_CONSTRUCTION`.

### E2 — measure functor as right Kan extension

Use the finite-quotient presentation of locally constant functions

`C(S,R) = colim C(S_i,R)`

together with the protected internal-Hom duality to obtain the corresponding limit statement for
the measure object. Package those objectwise limits as a pointwise right Kan extension, then use
the pointwise-to-universal theorem.

State: `OPEN_CONSTRUCTION`.

### E3 — canonical uniqueness

Transport the finite source along E1 and apply `rightKanExtensionUniqueOfIso` (or the
identity-source specialization `rightKanExtensionUnique`) to E2 and the pinned
`profiniteSolid` extension.

State: `FORMALLY_AVAILABLE` once E1 and E2 are discharged.

## Audit result

`FORMAL_ROUTE_REACHABLE_WITH_TWO_CONSTRUCTION_OBLIGATIONS`

This is not a characterized blocker. The pinned tree contains the universal-property machinery
needed for the comparison. The remaining work is constructive proof work inside P2-E.

It is also not a theorem-completion claim. At this stage neither E1 nor E2 has been discharged.

## Fail-closed substitutions

The operation rejects:

- a chosen Nöbeling basis;
- an objectwise product identification without naturality;
- inference of reconstruction/equivalence merely from P2-D duality;
- reversed variance;
- an unexplained universe shift;
- `sorry`, local axioms, or opaque semantic placeholders;
- promotion of P2-E into parent-P2 closure before the parent acceptance conditions are separately
  revalidated.

## Current disposition

`P2_E_COMPARISON_AUDIT_COMPLETE_RECONSTRUCTION_ACTIVE`

## Explicit nonclaims

This stage does **not** establish:

- protected availability of CM4-P2-E;
- closure of parent P2 issue #363;
- CM4 theorem certification (#355);
- P3, P4, P5, or P6;
- the derived/complex form of Proposition 0.5.7;
- arbitrary-ring generalization;
- broader C04;
- C06;
- `GRAPH_CERTIFIED`;
- dependency minimality or uniqueness;
- CM5;
- global CMDG completeness.

The next implementation step inside this same operation is E1: construct and replay the canonical
finite-level natural comparison, then E2, then E3.
