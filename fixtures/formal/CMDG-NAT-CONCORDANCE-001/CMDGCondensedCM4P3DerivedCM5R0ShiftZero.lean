import CMDGCondensedCM4P3DerivedCM5R0ZeroHom

/-!
# CMDG CM5-R0: the zero-shift comparison

A zero shift is canonically isomorphic (rather than definitionally equal) to
the identity functor. We transfer the protected unshifted derived Hom theorem
through that natural isomorphism and obtain the actual n = 0 instance of the
existing shifted-comparison predicate.

Nonzero shifts, higher Ext, and source-semantic equivalence remain open.
No axioms, sorry, or unproved hypotheses are added.
-/

noncomputable section

universe u

open CategoryTheory Pretriangulated

namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

/-- Precomposition bijectivity is unchanged when the domain arrow is mapped
through a functor naturally isomorphic to the identity. -/
private theorem precomposition_bijective_of_natIso_id
    {C : Type*} [Category* C]
    (F : C ⥤ C) (i : F ≅ 𝟭 C)
    {X Y A : C} (f : X ⟶ Y)
    (hb : Function.Bijective (fun g : Y ⟶ A => f ≫ g)) :
    Function.Bijective (fun g : F.obj Y ⟶ A => F.map f ≫ g) := by
  have hn_inv : f ≫ i.inv.app Y = i.inv.app X ≫ F.map f := by
    simpa using i.inv.naturality f
  have hn_hom : F.map f ≫ i.hom.app Y = i.hom.app X ≫ f := by
    simpa using i.hom.naturality f
  constructor
  · intro g h eq
    have heq : f ≫ (i.inv.app Y ≫ g) = f ≫ (i.inv.app Y ≫ h) := by
      calc
        f ≫ (i.inv.app Y ≫ g) = (f ≫ i.inv.app Y) ≫ g := by simp [Category.assoc]
        _ = (i.inv.app X ≫ F.map f) ≫ g := by rw [hn_inv]
        _ = i.inv.app X ≫ (F.map f ≫ g) := by simp [Category.assoc]
        _ = i.inv.app X ≫ (F.map f ≫ h) :=
          congrArg (fun k => i.inv.app X ≫ k) eq
        _ = (i.inv.app X ≫ F.map f) ≫ h := by simp [Category.assoc]
        _ = (f ≫ i.inv.app Y) ≫ h := by rw [hn_inv]
        _ = f ≫ (i.inv.app Y ≫ h) := by simp [Category.assoc]
    have he := hb.1 heq
    have he' := congrArg (fun k => i.hom.app Y ≫ k) he
    simpa [Category.assoc] using he'
  · intro q
    obtain ⟨g, hg⟩ := hb.2 (i.inv.app X ≫ q)
    refine ⟨i.hom.app Y ≫ g, ?_⟩
    calc
      F.map f ≫ (i.hom.app Y ≫ g) = (F.map f ≫ i.hom.app Y) ≫ g := by simp [Category.assoc]
      _ = (i.hom.app X ≫ f) ≫ g := by rw [hn_hom]
      _ = i.hom.app X ≫ (f ≫ g) := by simp [Category.assoc]
      _ = i.hom.app X ≫ (i.inv.app X ≫ q) := by rw [hg]
      _ = q := by simp [Category.assoc]

/-- The actual zero-shift instance of the previously introduced
`comparisonAtShift` is bijective, by CM4 and full faithfulness. -/
theorem comparisonAtShift_zero_bijective (S T : Profinite.{u}) :
    Function.Bijective (comparisonAtShift S T 0) := by
  simpa only [comparisonAtShift] using
    (precomposition_bijective_of_natIso_id
      (shiftFunctor (DerivedCategory Ambient) (0 : ℤ))
      (shiftFunctorZero (DerivedCategory Ambient) ℤ)
      (solidificationAtZero T)
      (unshiftedDerivedPrecomposition_bijective S T))

#print axioms comparisonAtShift_zero_bijective

end CMDG.CondensedCM5R0
