import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberTotalHomotopy

/-! The actual Dold–Kan normalization homotopy is natural. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology AlgebraicTopology.DoldKan
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
namespace CMDG.CondensedCM5R0.BreenDeligneNormalizationNaturality

set_option backward.isDefEq.respectTransparency false in
theorem homotopyP_natural {U V : SimplicialObject AddCommGrpCat.{0}} (f : U ⟶ V)
    (r i j : ℕ) :
    f.app (op (SimplexCategory.mk i)) ≫ (homotopyPToId V r).hom i j =
      (homotopyPToId U r).hom i j ≫ f.app (op (SimplexCategory.mk j)) := by
  by_cases h : (ComplexShape.down ℕ).Rel j i
  · induction r with
    | zero => simp [homotopyPToId, Homotopy.refl]
    | succ r ih =>
      simp only [homotopyPToId, Homotopy.trans_hom, Homotopy.ofEq_hom,
        Pi.zero_apply, Homotopy.add_hom, Homotopy.compLeft_hom, zero_add, add_zero,
        homotopyHσToZero, Homotopy.nullHomotopy'_hom, dif_pos h]
      rw [Preadditive.comp_add, Preadditive.add_comp, ih,
        ← Category.assoc, P_f_naturality, Category.assoc, hσ'_naturality,
        ← Category.assoc]
  · rw [(homotopyPToId V r).zero i j h, (homotopyPToId U r).zero i j h,
      comp_zero, zero_comp]

theorem normalizationHomotopy_natural {U V : SimplicialObject AddCommGrpCat.{0}}
    (f : U ⟶ V) (i j : ℕ) :
    f.app (op (SimplexCategory.mk i)) ≫ (homotopyPInftyToId V).hom i j =
      (homotopyPInftyToId U).hom i j ≫ f.app (op (SimplexCategory.mk j)) :=
  homotopyP_natural f (j+1) i j

#print axioms normalizationHomotopy_natural
end CMDG.CondensedCM5R0.BreenDeligneNormalizationNaturality
