import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneColumnConnectivity

/-! Identify the comparison target with the original tensorPower
implementation (left-associated, with a tensor unit). -/
noncomputable section
open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneTensorComparison
open CMDG.CondensedCM5R0.BreenDeligneColumnConnectivity
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneColumnPower

def rightAppend (K : Ch) : ∀ p : ℕ, positivePower K (p+1) ≅ tensor (positivePower K p) K
  | 0 => Iso.refl _
  | p+1 =>
    (Iso.refl K ⊗ᵢ rightAppend K p) ≪≫
      (α_ K (positivePower K p) K).symm

def originalPowerIso (K : Ch) : ∀ p : ℕ, positivePower K p ≅ tensorPower K (p+1)
  | 0 => (λ_ K).symm
  | p+1 =>
    rightAppend K p ≪≫ (originalPowerIso K p ⊗ᵢ Iso.refl K)

def tensorPowerIso {K L : Ch} (e : K ≅ L) : ∀ p : ℕ, tensorPower K p ≅ tensorPower L p
  | 0 => Iso.refl _
  | p+1 => tensorPowerIso e p ⊗ᵢ e

def columnPowerEquiv (A : AGrp) (n p : ℕ) :
    HomotopyEquiv ((barDouble ((EilenbergMacLaneModel.em n).obj A)).X (p+1))
      (tensorPower (reducedChainsZ A n) (p+1)) :=
  (actualComparison ((EilenbergMacLaneModel.em n).obj A) p).trans
    (HomotopyEquiv.ofIso (originalPowerIso _ p ≪≫ tensorPowerIso (reducedChainsIso A n) (p+1)))

theorem higherColumnStableVanish (A : AGrp) (n p q : ℕ)
    (hp : 2 ≤ p) (h : p+q < 2*n+2) :
    IsZero (((barDouble ((EilenbergMacLaneModel.em n).obj A)).X p).homology q) := by
  apply shifted_column_connectivity A n p q (by omega)
  have h' := Nat.mul_le_mul_right (n+1) hp
  omega

#print axioms columnPowerEquiv
#print axioms higherColumnStableVanish
end CMDG.CondensedCM5R0.BreenDeligneColumnPower
