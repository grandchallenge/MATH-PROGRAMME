import CMDGCondensedCM4P3DerivedCM5R0EilenbergMacLaneModel
import Mathlib.Algebra.Homology.Monoidal
import Mathlib.Algebra.Category.ModuleCat.Monoidal.Closed
import Mathlib.CategoryTheory.Monoidal.Preadditive
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits

/-! Actual tensor-complex support for the reduced bar layers.
The comparison with the simplicial smash chains is a separate obligation. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneTensorSupport

abbrev ZMod := ModuleCat.{0} ℤ
abbrev Ch := ChainComplex ZMod ℕ
abbrev c := ComplexShape.down ℕ

def toZModule : AddCommGrpCat.{0} ⥤ ZMod where
  obj A := ModuleCat.of ℤ A
  map f := ModuleCat.ofHom f.hom.toIntLinearMap
  map_id _ := by ext x; rfl
  map_comp _ _ := by ext x; rfl

instance : toZModule.Additive where
  map_add := by intros; rfl

def reducedChainsZ (A : AddCommGrpCat.{0}) (n : ℕ) : Ch :=
  (toZModule.mapHomologicalComplex c).obj ((reducedEMChains n).obj A)

/-- Vanishing of actual chain terms, not merely homology. -/
def SupportedFrom (K : Ch) (n : ℕ) : Prop :=
  ∀ m, m < n → IsZero (K.X m)

theorem reducedChains_supported (A : AddCommGrpCat.{0}) (n : ℕ) :
    SupportedFrom (reducedChainsZ A n) n := by
  intro m hm
  exact toZModule.map_isZero (reducedEMChains_below A n m hm)

set_option backward.isDefEq.respectTransparency false in
theorem tensor_supported (K L : Ch) (a b : ℕ)
    (hK : SupportedFrom K a) (hL : SupportedFrom L b) :
    SupportedFrom (HomologicalComplex.tensorObj K L) (a+b) := by
  intro j hj
  apply (IsZero.iff_id_eq_zero _).mpr
  apply HomologicalComplex.mapBifunctor.hom_ext
  intro i₁ i₂ hi
  change i₁+i₂ = j at hi
  have hz : IsZero (K.X i₁ ⊗ L.X i₂) := by
    by_cases hk : i₁ < a
    · exact ((curriedTensor ZMod).flip.obj (L.X i₂)).map_isZero (hK i₁ hk)
    · exact ((curriedTensor ZMod).obj (K.X i₁)).map_isZero (hL i₂ (by omega))
  exact hz.eq_of_src _ _

def tensorPower (K : Ch) : ℕ → Ch
  | 0 => HomologicalComplex.tensorUnit ZMod c
  | p+1 => HomologicalComplex.tensorObj (tensorPower K p) K

theorem tensorPower_supported (K : Ch) (n : ℕ) (hK : SupportedFrom K n) (p : ℕ) :
    SupportedFrom (tensorPower K p) (p*n) := by
  induction p with
  | zero =>
    intro m hm
    omega
  | succ p hp =>
    rw [Nat.succ_mul]
    exact tensor_supported (tensorPower K p) K (p*n) n hp hK

/-- The algebraic tensor-chain model of the p-th suspended bar layer. -/
def shiftedTensorLayer (K : Ch) (p : ℕ) : Ch :=
  HomologicalComplex.tensorObj ((HomologicalComplex.single ZMod c p).obj (𝟙_ ZMod))
    (tensorPower K p)

theorem shiftedLayer_supported (K : Ch) (n p : ℕ) (hK : SupportedFrom K n) :
    SupportedFrom (shiftedTensorLayer K p) (p*(n+1)) := by
  have hs : SupportedFrom ((HomologicalComplex.single ZMod c p).obj (𝟙_ ZMod)) p :=
    fun m hm => HomologicalComplex.isZero_single_obj_X c p _ m (by omega)
  have h := tensor_supported _ _ p (p*n) hs (tensorPower_supported K n hK p)
  simpa only [shiftedTensorLayer, Nat.mul_add, Nat.mul_one, Nat.add_comm (p*n) p] using h

theorem actualLayer_homology_below (A : AddCommGrpCat.{0}) (n p j : ℕ)
    (h : j < p*(n+1)) :
    IsZero ((shiftedTensorLayer (reducedChainsZ A n) p).homology j) :=
  ShortComplex.isZero_homology_of_isZero_X₂ _
    (shiftedLayer_supported _ n p (reducedChains_supported A n) j h)

theorem higherLayer_stable_vanish (A : AddCommGrpCat.{0}) (n p j : ℕ)
    (hp : 2 ≤ p) (hj : j < 2*n+2) :
    IsZero ((shiftedTensorLayer (reducedChainsZ A n) p).homology j) := by
  apply actualLayer_homology_below
  have h := Nat.mul_le_mul_right (n+1) hp
  omega

#print axioms tensor_supported
#print axioms tensorPower_supported
#print axioms actualLayer_homology_below
#print axioms higherLayer_stable_vanish
end CMDG.CondensedCM5R0.BreenDeligneTensorSupport
