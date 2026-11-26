import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneTensorComparison
import Mathlib.Algebra.Homology.BifunctorHomotopy

/-! Iterated Eilenberg–Zilber comparison of genuine normalized bar columns
with tensor complexes, and the resulting homological connectivity. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneTensorComparison
open CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneNormalizedBar
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
namespace CMDG.CondensedCM5R0.BreenDeligneColumnConnectivity

abbrev tensor (K L : Ch) := HomologicalComplex.tensorObj K L

set_option backward.isDefEq.respectTransparency false in
def tensorEquiv (K : Ch) {L M : Ch} (e : HomotopyEquiv L M) :
    HomotopyEquiv (tensor K L) (tensor K M) where
  hom := HomologicalComplex.tensorHom (𝟙 K) e.hom
  inv := HomologicalComplex.tensorHom (𝟙 K) e.inv
  homotopyHomInvId := by
    have h := HomologicalComplex.mapBifunctorMapHomotopy₂ (𝟙 K) e.homotopyHomInvId
      (curriedTensor ZMod) c
    change Homotopy ((𝟙 K) ⊗ₘ (e.hom ≫ e.inv)) ((𝟙 K) ⊗ₘ (𝟙 L)) at h
    change Homotopy (((𝟙 K) ⊗ₘ e.hom) ≫ ((𝟙 K) ⊗ₘ e.inv)) (𝟙 _)
    rw [tensorHom_comp_tensorHom, Category.id_comp]
    simpa only [tensorHom_id, id_whiskerRight] using h
  homotopyInvHomId := by
    have h := HomologicalComplex.mapBifunctorMapHomotopy₂ (𝟙 K) e.homotopyInvHomId
      (curriedTensor ZMod) c
    change Homotopy ((𝟙 K) ⊗ₘ (e.inv ≫ e.hom)) ((𝟙 K) ⊗ₘ (𝟙 M)) at h
    change Homotopy (((𝟙 K) ⊗ₘ e.inv) ≫ ((𝟙 K) ⊗ₘ e.hom)) (𝟙 _)
    rw [tensorHom_comp_tensorHom, Category.id_comp]
    simpa only [tensorHom_id, id_whiskerRight] using h

def reducedSimp (X : SimplicialObject AGrp) : S := X ⋙ reducedFree ⋙ toZModule

def pointSimp (X : SimplicialObject AGrp) (p : ℕ) : S := X ⋙ pointTensorFunctor p

def pointSuccIso (X : SimplicialObject AGrp) (p : ℕ) :
    pointSimp X (p+1) ≅ diagonal (external (reducedSimp X) (pointSimp X p)) :=
  NatIso.ofComponents (fun _ => Iso.refl _) (by
    intro i j f
    rfl)

/-- Right-associated positive tensor powers, with degree-one base case. -/
def positivePower (K : Ch) : ℕ → Ch
  | 0 => K
  | p+1 => tensor K (positivePower K p)

def reducedChainsIso (A : AGrp) (n : ℕ) :
    C (reducedSimp ((EilenbergMacLaneModel.em n).obj A)) ≅ reducedChainsZ A n := by
  apply eqToIso
  let Y := (EilenbergMacLaneModel.em n).obj A ⋙ reducedFree
  have h := congrArg (fun F => F.obj Y)
    (AlgebraicTopology.map_alternatingFaceMapComplex toZModule)
  exact h.symm

def pointOneIso (X : SimplicialObject AGrp) :
    C (pointSimp X 1) ≅ C (reducedSimp X) :=
  (alternatingFaceMapComplex ZMod).mapIso (Functor.isoWhiskerLeft X pointTensorOneIso)

def pointComparison (X : SimplicialObject AGrp) :
    ∀ p : ℕ, HomotopyEquiv (C (pointSimp X (p+1))) (positivePower (C (reducedSimp X)) p)
  | 0 => HomotopyEquiv.ofIso (pointOneIso X)
  | p+1 =>
    (HomotopyEquiv.ofIso ((alternatingFaceMapComplex ZMod).mapIso (pointSuccIso X (p+1)))).trans
      ((externalComparison (reducedSimp X) (pointSimp X (p+1))).trans
        (tensorEquiv (C (reducedSimp X)) (pointComparison X p)))

def actualComparison (X : SimplicialObject AGrp) (p : ℕ) :
    HomotopyEquiv ((barDouble X).X (p+1)) (positivePower (C (reducedSimp X)) p) :=
  (HomotopyEquiv.ofIso (doubleColumnIso X (p+1) ≪≫ actualColumnIso X p ≪≫
    verticalSmashIso X (p+1))).trans (pointComparison X p)

theorem positivePower_supported (K : Ch) (n : ℕ) (hK : SupportedFrom K n) (p : ℕ) :
    SupportedFrom (positivePower K p) ((p+1)*n) := by
  induction p with
  | zero => simpa [positivePower] using hK
  | succ p ih =>
    have h := tensor_supported K (positivePower K p) n ((p+1)*n) hK ih
    change SupportedFrom (tensor K (positivePower K p)) ((p+1+1)*n)
    rw [Nat.add_mul,Nat.one_mul,Nat.add_comm ((p+1)*n) n]
    exact h

theorem reducedSimp_supported (A : AGrp) (n : ℕ) :
    SupportedFrom (C (reducedSimp ((EilenbergMacLaneModel.em n).obj A))) n := by
  intro m hm
  exact (reducedChains_supported A n m hm).of_iso ((HomologicalComplex.eval ZMod c m).mapIso (reducedChainsIso A n))

theorem column_homology_below (A : AGrp) (n p j : ℕ) (h : j < (p+1)*n) :
    IsZero (((barDouble ((EilenbergMacLaneModel.em n).obj A)).X (p+1)).homology j) :=
  (ShortComplex.isZero_homology_of_isZero_X₂ _
    (positivePower_supported _ n (reducedSimp_supported A n) p j h)).of_iso
      ((actualComparison ((EilenbergMacLaneModel.em n).obj A) p).toHomologyIso j)

theorem shifted_column_connectivity (A : AGrp) (n p q : ℕ)
    (hp : 1 ≤ p) (h : p+q < p*(n+1)) :
    IsZero (((barDouble ((EilenbergMacLaneModel.em n).obj A)).X p).homology q) := by
  obtain ⟨k,rfl⟩ : ∃ k, p=k+1 := ⟨p-1,by omega⟩
  apply column_homology_below
  rw [Nat.mul_add,Nat.mul_one] at h
  omega

#print axioms tensorEquiv
#print axioms pointComparison
#print axioms actualComparison
#print axioms column_homology_below
#print axioms shifted_column_connectivity
end CMDG.CondensedCM5R0.BreenDeligneColumnConnectivity
