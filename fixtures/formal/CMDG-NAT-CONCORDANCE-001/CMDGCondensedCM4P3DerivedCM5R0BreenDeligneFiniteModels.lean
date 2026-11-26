import CMDGCondensedCM4P3DerivedCM5R0BarGroupMoore
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteBar
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneReducedBasis
import Mathlib.RingTheory.TensorProduct.Finite

/-! The genuine rank-one bar comparison and finite homology transfer
from a degreewise finite chain-homotopy replacement.
The existence of the replacement is a separate obligation. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CategoryTheory.MonoidalCategory HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BarGroupMoore
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneReducedNext
open CMDG.CondensedCM5R0.BreenDeligneMooreHomotopyTransport
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
open CMDG.CondensedCM5R0.BreenDeligneFiniteBar
open CMDG.CondensedCM5R0.BreenDeligneFiniteTotal
open CMDG.CondensedCM5R0.BreenDeligneTensorComparison
open CMDG.CondensedCM5R0.BreenDeligneColumnConnectivity
open CMDG.CondensedCM5R0.BreenDeligneColumnPower
open CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteModels

abbrev DK₁ := BreenDeligneAdditiveBarTotal.DK

def barOneIso (A : AGrp) : bar A ≅ (em 1).obj A :=
  DK₁.unitIso.app (bar A) ≪≫ DK₁.inverse.mapIso (groupMooreIso A)

def barOneReducedIso (A : AGrp) : RC (bar A) ≅ reducedChainsZ A 1 :=
  ZK.mapIso (reducedFunctor.mapIso (barOneIso A)) ≪≫ reducedEMChainIso A 1

theorem actualTermFree (A : AGrp) (n j : ℕ) :
    Module.Free ℤ ((reducedChainsZ A n).X j) := by
  change Module.Free ℤ (reducedFree.obj (((em n).obj A).obj (op (SimplexCategory.mk j))))
  exact Module.Free.of_basis (BreenDeligneReducedBasis.reducedBasis _)

theorem finiteHomologyOfTerm (K : Ch) (j : ℕ)
    [Module.Finite ℤ (K.X j)] : Module.Finite ℤ (K.homology j) := by
  letI : Module.Finite ℤ (K.cycles j) :=
    Module.Finite.of_injective (K.iCycles j).hom (iCycles_injective K j)
  exact Module.Finite.of_surjective (K.homologyπ j).hom (class_surj K j)

def totalSumAdd (K : BC) (n : ℕ) :
    (∀ i : Fin (n+1), (K.X i.val).X (n-i.val)) →+ (K.total c).X n where
  toFun x := ∑ i : Fin (n+1), K.ιTotal c i.val (n-i.val) n (by
    change i.val+(n-i.val)=n
    omega) (x i)
  map_zero' := by
    apply Finset.sum_eq_zero
    intro i _
    exact map_zero (K.ιTotal c i.val (n-i.val) n (by
      change i.val+(n-i.val)=n
      omega)).hom
  map_add' x y := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    exact map_add (K.ιTotal c i.val (n-i.val) n (by
      change i.val+(n-i.val)=n
      omega)).hom (x i) (y i)

theorem totalTermFinite (K : BC) (n : ℕ)
    (h : ∀ p q, p+q=n → Module.Finite ℤ ((K.X p).X q)) :
    Module.Finite ℤ ((K.total c).X n) := by
  letI (i : Fin (n+1)) : Module.Finite ℤ ((K.X i.val).X (n-i.val)) :=
    h i.val (n-i.val) (by omega)
  let f := intLinear (totalSumAdd K n)
  apply Module.Finite.of_surjective f
  intro x
  refine ⟨fun i => proj K n i.val (n-i.val) (by omega) x, ?_⟩
  exact sum_elements K n x

theorem tensorTermFinite (K L : Ch)
    (hK : ∀ j, Module.Finite ℤ (K.X j))
    (hL : ∀ j, Module.Finite ℤ (L.X j)) (j : ℕ) :
    Module.Finite ℤ ((tensor K L).X j) := by
  change Module.Finite ℤ (((tensorDouble K L).total c).X j)
  apply totalTermFinite
  intro p q _
  letI := hK p
  letI := hL q
  change Module.Finite ℤ (TensorProduct ℤ (K.X p) (L.X q))
  infer_instance

set_option backward.isDefEq.respectTransparency false in
def tensorEquivLeft {K L : Ch} (e : HomotopyEquiv K L) (M : Ch) :
    HomotopyEquiv (tensor K M) (tensor L M) where
  hom := HomologicalComplex.tensorHom e.hom (𝟙 M)
  inv := HomologicalComplex.tensorHom e.inv (𝟙 M)
  homotopyHomInvId := by
    have h := HomologicalComplex.mapBifunctorMapHomotopy₁ e.homotopyHomInvId (𝟙 M)
      (curriedTensor ZMod) c
    change Homotopy ((e.hom ≫ e.inv) ⊗ₘ (𝟙 M)) ((𝟙 K) ⊗ₘ (𝟙 M)) at h
    change Homotopy ((e.hom ⊗ₘ (𝟙 M)) ≫ (e.inv ⊗ₘ (𝟙 M))) (𝟙 _)
    rw [tensorHom_comp_tensorHom, Category.id_comp]
    simpa only [tensorHom_id, id_whiskerRight] using h
  homotopyInvHomId := by
    have h := HomologicalComplex.mapBifunctorMapHomotopy₁ e.homotopyInvHomId (𝟙 M)
      (curriedTensor ZMod) c
    change Homotopy ((e.inv ≫ e.hom) ⊗ₘ (𝟙 M)) ((𝟙 L) ⊗ₘ (𝟙 M)) at h
    change Homotopy ((e.inv ⊗ₘ (𝟙 M)) ≫ (e.hom ⊗ₘ (𝟙 M))) (𝟙 _)
    rw [tensorHom_comp_tensorHom, Category.id_comp]
    simpa only [tensorHom_id, id_whiskerRight] using h

def positivePowerEquiv {K L : Ch} (e : HomotopyEquiv K L) :
    ∀ p : ℕ, HomotopyEquiv (positivePower K p) (positivePower L p)
  | 0 => e
  | p+1 => (tensorEquivLeft e (positivePower K p)).trans
      (tensorEquiv L (positivePowerEquiv e p))

theorem finitePositivePowerTerms (K : Ch)
    (h : ∀ j, Module.Finite ℤ (K.X j)) (p : ℕ) :
    ∀ j, Module.Finite ℤ ((positivePower K p).X j) := by
  induction p with
  | zero => exact h
  | succ p ih =>
    intro j
    exact tensorTermFinite K (positivePower K p) h ih j

theorem finiteTensorPowerHomology_of_replacement {K L : Ch}
    (e : HomotopyEquiv K L) (h : ∀ j, Module.Finite ℤ (L.X j))
    (p j : ℕ) : Module.Finite ℤ ((tensorPower K (p+1)).homology j) := by
  letI := finitePositivePowerTerms L h p j
  letI := finiteHomologyOfTerm (positivePower L p) j
  exact finiteOfIso (((HomotopyEquiv.ofIso (originalPowerIso K p).symm).trans
    (positivePowerEquiv e p)).toHomologyIso j)

#print axioms barOneIso
#print axioms barOneReducedIso
#print axioms actualTermFree
#print axioms finiteHomologyOfTerm
#print axioms totalTermFinite
#print axioms tensorTermFinite
#print axioms finiteTensorPowerHomology_of_replacement
end CMDG.CondensedCM5R0.BreenDeligneFiniteModels
