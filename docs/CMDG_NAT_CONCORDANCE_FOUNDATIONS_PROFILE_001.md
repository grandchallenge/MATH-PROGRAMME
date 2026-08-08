# CMDG natural-number concordance foundational profiles

Operation: `CMDG-NAT-CONCORDANCE-FOUNDATIONS-PROFILE-001`  
Issue: `#304`  
Protected baseline: `0533e8b35c94b25f378af89063aaf840aecd4045`

## Purpose

This operation defines the foundational profiles that must exist before
`CMDG-NAT-CONCORDANCE-001` may compare the natural numbers in three settings:

- `N_DTT`: Lean's kernel-level `Nat`;
- `N_ZFC`: a natural-number object built in the declared ZFC object-theory lane;
- `N_NNO`: a categorical natural numbers object satisfying the declared universal property.

The machine authority is
`governance/cmdg_nat_concordance_foundations_profile_001.json`, validated by
`schemas/cmdg_nat_concordance_foundations_profile.schema.json` and
`ci/validate_cmdg_nat_foundations_profile.py`.

Protected admission of this profile may discharge only the profile-definition
prerequisite of `CMDG-C03`. It does not establish a concordance relation.

## 1. Proof substrate and pinned implementation environment

The retained comparison environment is pinned to:

- Lean `leanprover/lean4:v4.33.0-rc1`;
- Lean tag commit `62eed1db4d67327ec8120be05f1a1b0847d74561`;
- mathlib commit `79d0395a1825a6264ad5d269e35e60537518955e`.

The local evidence is the retained `lean-toolchain` and `lake-manifest.json`
under `fixtures/formal/LOG-GCD-001`. The validator checks their Git blob
identities and verifies that the manifest still binds the declared mathlib
commit.

Lean is the proof substrate. The ZF/ZFC theory described below is an object
theory represented within that substrate. The two roles must not be conflated.

## 2. Exact syntactic ZF/ZFC profile

CMDG fixes a one-sorted classical first-order language with built-in equality.
Its only primitive nonlogical symbol is the binary membership relation. Set
functions, ordered pairs, domains and related notions are definitions in that
membership language rather than additional primitive symbols.

For this profile, ZF has exactly these primitive postulates:

| Item | Kind |
| --- | --- |
| Extensionality | single axiom |
| Pairing | single axiom |
| Union | single axiom |
| Power Set | single axiom |
| Infinity | single axiom |
| Foundation | single axiom |
| Separation | axiom schema |
| Replacement | axiom schema |

Separation ranges over first-order formulas in the membership language with
parameters. Replacement ranges over first-order formulas defining functional
relations, again with parameters. The validator rejects either schema if it is
collapsed into a single axiom.

The Empty Set assertion is retained as a derived theorem in this exact
presentation, not as an additional primitive axiom.

ZFC is this ZF profile plus one Choice axiom in choice-function form:

> for every set `A` whose members are nonempty, there exists a function `f`
> with domain `A` such that `f(x) ∈ x` for every `x ∈ A`.

"Function" and "domain" in this statement are defined using membership; they do
not enlarge the primitive language.

The object logic is explicitly classical first-order logic with equality.
Nothing in this profile asserts consistency, categoricity, a standard model, or
equivalence with Lean's dependent type theory.

## 3. Retained set-theoretic implementation boundary

The pinned mathlib revision contains
`Mathlib/SetTheory/ZFC/Basic.lean`. Its module documentation describes the
construction as a model of Zermelo-Fraenkel set theory plus Choice. The retained
carrier is exactly:

`ZFSet : Type (u + 1)`

constructed as:

`Quotient PSet.setoid.{u}`.

The same module identifies `ZFSet.choice`, documenting it as proved from Lean's
axiom of choice. It also supplies `ZFSet.small_coe : Small.{u} x`, which is
recorded as part of the size boundary.

This upstream implementation evidence is not a Programme `REALIZES_AS`
admission. In particular, this operation does not claim that every formula in
the CMDG syntactic profile has already been independently cross-walked to a
specific mathlib declaration. The canonical machine profile therefore records:

- the retained `ZFSet` carrier and exact source pin;
- the upstream module-level model claim;
- a direct declaration identity for `ZFSet.choice`;
- all other formula-to-declaration crosswalks as not yet admitted;
- `programme_realizes_as_status: NOT_ADMITTED`.

A later `REALIZES_AS` edge must supply the formula/declaration correspondence,
direction, exact environment, axiom/classicality footprint, limitations and
independent reviewed evidence required by the core CMDG edge contract.

## 4. DTT natural-number profile

`N_DTT` is grounded in Lean's core declaration `Nat` at the pinned Lean commit.
The profile binds:

- `Nat : Type`;
- constructors `Nat.zero` and `Nat.succ`;
- generated dependent recursor/induction interface `Nat.rec`;
- source file `src/Init/Prelude.lean`.

Lean's compiler and runtime may special-case natural-number representation for
efficiency. That implementation detail does not change the logical identity of
the kernel inductive declaration.

No definitional identity or foundational equivalence with `N_ZFC` or `N_NNO`
is inferred from the existence of zero, successor, recursion or induction.

## 5. Categorical natural numbers object

`N_NNO` is an abstract specification in an ambient category `C`. No concrete
mathlib declaration is bound by this operation.

The chosen presentation requires a terminal object `1`, an object `N`, and
morphisms

`zero : 1 ⟶ N`

and

`succ : N ⟶ N`.

For every object `X`, point `x0 : 1 ⟶ X`, and endomorphism `s : X ⟶ X`, there
must exist a unique morphism `h : N ⟶ X` satisfying

`zero ≫ h = x0`

and

`succ ≫ h = h ≫ s`.

This direct recursor universal property does not require binary coproducts.
Consequently the profile does not silently assume them. A reformulation as an
initial algebra for `1 + (-)` may be established later under the additional
categorical structure needed for that formulation; it is not part of the
defining requirement here.

Any two NNO structures satisfying the profile are expected to be unique up to
unique isomorphism only as a derived categorical theorem. This is never
definitional identity, and this operation does not record that derived theorem
as already machine-checked.

The profile names separate object and hom universe variables, `u` and `v`, and
makes no additional smallness claim beyond the declared ambient-category
profile.

## 6. Cross-foundational relation discipline

The reserved comparison identities are exactly `N_DTT`, `N_ZFC` and `N_NNO`.
This operation promotes no edge among them.

Future `REALIZES_AS`, `INTERPRETS`, `EQUIVALENT_TO` or `TRANSPORTS_ALONG`
claims must identify source, target and direction; bind exact profile versions;
cite evidence; record limitations; bind a proof environment when formal
evidence is used; and receive independent review. Implementation imports alone
have no semantic authority.

A future foundational-concordance record is separate from those edge types and
must likewise carry admitted evidence. Similar interfaces or recursively
defined operations do not establish definitional identity or equivalence.

## 7. Fail-closed tests

The test suite mutates the canonical profile and requires rejection for at
least:

- missing theory or language identity;
- incomplete ZF inventory;
- Separation/Replacement schema confusion;
- hidden classicality;
- Lean-substrate/object-theory conflation;
- semantic-model or `REALIZES_AS` overclaim;
- missing universe/size profiles;
- malformed NNO universal property;
- definitional-identity overclaim;
- premature foundational concordance;
- premature `GRAPH_CERTIFIED`;
- attempts to treat the artifact alone as protected discharge of C03.

## Claim boundary

This operation defines a prerequisite profile only. It does not establish
`CMDG-NAT-CONCORDANCE-001`; it does not prove DTT/ZFC foundational equivalence;
it does not assert the consistency or standardness of a ZFC model; it does not
bind a concrete categorical NNO implementation; it does not confer
`REALIZES_AS`, `GRAPH_CERTIFIED`, or global dependency completeness.

`CMDG-C04`, `CMDG-C05`, and `CMDG-C06` remain unchanged. The successor
`CMDG-NAT-CONCORDANCE-001` remains gated until this profile receives independent
exact-head review and protected admission.
