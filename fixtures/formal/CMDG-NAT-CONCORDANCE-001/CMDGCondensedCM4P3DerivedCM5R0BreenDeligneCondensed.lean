import Mathlib.Condensed.Module
import Mathlib.Condensed.Functors
import Mathlib.Condensed.AB
import Mathlib.Topology.Category.CompHaus.Basic
import Mathlib.CategoryTheory.Preadditive.Biproducts
import Mathlib.Topology.Instances.AddCircle.Real

/-!
# Genuine condensed free abelian Breen–Deligne low-degree source maps

Using the real functor CompHaus.toCondensed then Condensed.freeAb,
construct F₀,F₁,F₂ for any compact Hausdorff abelian group, with
actual categorical additive differentials d₁,d₂, doubling maps,
and degree-zero/degree-one doubling homotopies. Specialize to genuine
compact torus (ℝ/ℤ)^I. All maps are morphisms in the true CondensedAb.
This module only constructs typed maps. Their categorical identities,
all-degree resolution exactness, and derived-Hom comparison remain open.
-/

noncomputable section
universe u
open CategoryTheory
open CategoryTheory.Limits
namespace CMDG.CondensedCM5R0.BreenDeligneCondensed

variable (A : Type u) [TopologicalSpace A] [CompactSpace A] [T2Space A]
variable [AddCommGroup A] [ContinuousAdd A]

noncomputable abbrev src0 : CondensedAb.{u} :=
    (Condensed.freeAb).obj ((CompHaus.of A).toCondensed)
noncomputable abbrev src1 : CondensedAb.{u} :=
    (Condensed.freeAb).obj ((CompHaus.of (A × A)).toCondensed)

noncomputable def polyMap {X Y : Type u}
    [TopologicalSpace X] [CompactSpace X] [T2Space X]
    [TopologicalSpace Y] [CompactSpace Y] [T2Space Y]
    (f : C(X, Y)) :
    (Condensed.freeAb).obj ((CompHaus.of X).toCondensed) ⟶
    (Condensed.freeAb).obj ((CompHaus.of Y).toCondensed) :=
  (Condensed.freeAb).map
    (compHausToCondensed.map
      (CompHausLike.ofHom _ f))

noncomputable def d1 : src1 A ⟶ src0 A :=
    polyMap (X := A × A) (Y := A) (⟨fun p : A × A => p.1 + p.2,
        continuous_fst.add continuous_snd⟩) -
    polyMap (X := A × A) (Y := A) (⟨fun p : A × A => p.1, continuous_fst⟩) -
    polyMap (X := A × A) (Y := A) (⟨fun p : A × A => p.2, continuous_snd⟩)

noncomputable abbrev src2assoc : CondensedAb.{u} :=
  (Condensed.freeAb).obj ((CompHaus.of (A × (A × A))).toCondensed)

noncomputable abbrev src2 : CondensedAb.{u} :=
  src2assoc A ⊞ src1 A

noncomputable def assocBC : C(A × (A × A), A × A) :=
  ⟨fun p => (p.2.1, p.2.2),
    (continuous_fst.comp continuous_snd).prodMk
      (continuous_snd.comp continuous_snd)⟩

noncomputable def assocAB_C : C(A × (A × A), A × A) :=
  ⟨fun p => (p.1 + p.2.1, p.2.2),
    (continuous_fst.add (continuous_fst.comp continuous_snd)).prodMk
      (continuous_snd.comp continuous_snd)⟩

noncomputable def assocA_BC : C(A × (A × A), A × A) :=
  ⟨fun p => (p.1, p.2.1 + p.2.2),
    continuous_fst.prodMk
      ((continuous_fst.comp continuous_snd).add
        (continuous_snd.comp continuous_snd))⟩

noncomputable def assocAB : C(A × (A × A), A × A) :=
  ⟨fun p => (p.1, p.2.1),
    continuous_fst.prodMk (continuous_fst.comp continuous_snd)⟩

noncomputable def d2assoc : src2assoc A ⟶ src1 A :=
  polyMap (X := A × (A × A)) (Y := A × A) (assocBC A) -
  polyMap (X := A × (A × A)) (Y := A × A) (assocAB_C A) +
  polyMap (X := A × (A × A)) (Y := A × A) (assocA_BC A) -
  polyMap (X := A × (A × A)) (Y := A × A) (assocAB A)

noncomputable def d2comm : src1 A ⟶ src1 A :=
  𝟙 _ - polyMap (X := A × A) (Y := A × A)
     (⟨fun p => (p.2,p.1), continuous_snd.prodMk continuous_fst⟩)

noncomputable def d2 : src2 A ⟶ src1 A :=
  biprod.desc (d2assoc A) (d2comm A)

noncomputable def h0 : src0 A ⟶ src1 A :=
  -polyMap (X := A) (Y := A × A)
    (⟨fun a => (a,a), continuous_id.prodMk continuous_id⟩)

noncomputable def h1 : src1 A ⟶ src2 A :=
  (polyMap (X := A × A) (Y := A × (A × A))
    (⟨fun p => (p.1,(p.1,p.2+p.2)),
      continuous_fst.prodMk (continuous_fst.prodMk
        (continuous_snd.add continuous_snd))⟩)
       ≫ biprod.inl) -
  (polyMap (X := A × A) (Y := A × (A × A))
    (⟨fun p => (p.1,(p.2,p.2)),
      continuous_fst.prodMk (continuous_snd.prodMk continuous_snd)⟩)
       ≫ biprod.inl) -
  (polyMap (X := A × A) (Y := A × (A × A))
    (⟨fun p => (p.1,(p.2,p.1+p.2)),
      continuous_fst.prodMk
        (continuous_snd.prodMk (continuous_fst.add continuous_snd))⟩)
       ≫ biprod.inl) -
  (polyMap (X := A × A) (Y := A × A)
    (⟨fun p => (p.1+p.2,p.2),
      (continuous_fst.add continuous_snd).prodMk continuous_snd⟩)
       ≫ biprod.inr)

noncomputable def double0 : src0 A ⟶ src0 A :=
  polyMap (X := A) (Y := A)
    (⟨fun a => a+a, continuous_id.add continuous_id⟩)

noncomputable def double1 : src1 A ⟶ src1 A :=
  polyMap (X := A × A) (Y := A × A)
    (⟨fun p => (p.1+p.1,p.2+p.2),
      (continuous_fst.add continuous_fst).prodMk
        (continuous_snd.add continuous_snd)⟩)

#check src2
#check d2
#check h0
#check h1
#check double0
#check double1

#check src0
#check polyMap
#check d1

/-- The actual infinite-coordinate circle torus is compact Hausdorff,
so the preceding categorical functor applies without finite-index
restrictions. -/
noncomputable def torusF0 (I : Type u) : CondensedAb.{u} :=
  src0 (I → UnitAddCircle)

noncomputable def torusF1 (I : Type u) : CondensedAb.{u} :=
  src1 (I → UnitAddCircle)

noncomputable def torusF2 (I : Type u) : CondensedAb.{u} :=
  src2 (I → UnitAddCircle)

noncomputable def torusD1 (I : Type u) : torusF1 I ⟶ torusF0 I :=
  d1 (I → UnitAddCircle)

noncomputable def torusD2 (I : Type u) : torusF2 I ⟶ torusF1 I :=
  d2 (I → UnitAddCircle)

noncomputable def torusH0 (I : Type u) : torusF0 I ⟶ torusF1 I :=
  h0 (I → UnitAddCircle)

noncomputable def torusH1 (I : Type u) : torusF1 I ⟶ torusF2 I :=
  h1 (I → UnitAddCircle)

#check torusF0
#check torusF1
#check torusF2
#check torusD1
#check torusD2
#check torusH0
#check torusH1

end CMDG.CondensedCM5R0.BreenDeligneCondensed
