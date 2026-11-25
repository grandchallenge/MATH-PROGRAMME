import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberHomotopy

/-! The natural signed shuffle family, and reduction of its differential
law to a single universal-model equality in each bidegree. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberNatural
open CMDG.CondensedCM5R0.EilenbergZilberHomotopy
namespace CMDG.CondensedCM5R0.EilenbergZilberShuffle

set_option backward.isDefEq.respectTransparency false in
theorem shufflePart_natural {B C : Bi} (f : B ⟶ C) (p q : ℕ) :
    f.app (pair p q) ≫ shufflePart C p q =
      shufflePart B p q ≫ (D.map f).f (p+q) := by
  unfold shufflePart
  rw [Preadditive.comp_sum,Preadditive.sum_comp]
  apply Finset.sum_congr rfl
  intro u _
  rw [Preadditive.comp_zsmul,Preadditive.zsmul_comp]
  congr 1
  exact (f.naturality _).symm

set_option backward.isDefEq.respectTransparency false in
theorem shuffleDegree_natural {B C : Bi} (f : B ⟶ C) (n : ℕ) :
    (Tot.map f).f n ≫ shuffleDegree C n =
      shuffleDegree B n ≫ (D.map f).f n := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=n at h
  subst n
  change (double B).ιTotal c p q (p+q) rfl ≫
      (HomologicalComplex₂.total.map (doubleF.map f) c).f (p+q) ≫ shuffleDegree C (p+q) =
    (double B).ιTotal c p q (p+q) rfl ≫ shuffleDegree B (p+q) ≫ (D.map f).f (p+q)
  rw [← Category.assoc,HomologicalComplex₂.ιTotal_map,Category.assoc,← Category.assoc ( (double B).ιTotal c p q (p+q) rfl)]
  change f.app (pair p q) ≫ (double C).ιTotal c p q (p+q) rfl ≫ shuffleDegree C (p+q) =
    ((double B).ιTotal c p q (p+q) rfl ≫ shuffleDegree B (p+q)) ≫ (D.map f).f (p+q)
  rw [shuffleDegree_summand,shuffleDegree_summand]
  exact shufflePart_natural f p q

def shuffleNatDegree (n : ℕ) : degree Tot n ⟶ degree D n where
  app B := shuffleDegree B n
  naturality {_B _C} f := shuffleDegree_natural f n

def shuffleResidual (n : ℕ) : degree Tot (n+1) ⟶ degree D n :=
  shuffleNatDegree (n+1) ≫ dNat D n - dNat Tot n ≫ shuffleNatDegree n

theorem shuffleResidual_zero_iff (n : ℕ) :
    shuffleResidual n = 0 ↔
      ∀ i : Split (n+1),
        (shuffleResidual n).app _ (splitGenerator (n+1) i) = 0 := by
  constructor
  · intro h i
    rw [h]
    rfl
  · intro h
    apply total_ext (degree D n) (n+1)
    intro i
    exact h i

set_option backward.isDefEq.respectTransparency false in
def shuffleNat (h : ∀ n (i : Split (n+1)),
    (shuffleResidual n).app _ (splitGenerator (n+1) i) = 0) : Tot ⟶ D where
  app B := ChainComplex.ofHom (shuffleDegree B) (fun n => by
    have he := congrArg (fun k => k.app B) ((shuffleResidual_zero_iff n).mpr (h n))
    exact sub_eq_zero.mp he)
  naturality {_B _C} f := by
    apply HomologicalComplex.Hom.ext
    funext n
    exact shuffleDegree_natural f n

#print axioms shuffleDegree_natural
#print axioms shuffleResidual_zero_iff
#print axioms shuffleNat
end CMDG.CondensedCM5R0.EilenbergZilberShuffle
