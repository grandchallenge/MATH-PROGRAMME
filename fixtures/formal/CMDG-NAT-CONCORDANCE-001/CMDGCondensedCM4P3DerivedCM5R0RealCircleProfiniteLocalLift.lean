import CMDGCondensedCM4P3DerivedCM5R0RealCircleStoneanExact

/-!
# CMDG CM5: site-local real lifts on arbitrary profinite objects

Use the actual epimorphic Stonean presentation of every Profinite P
to lift continuous (ℝ/ℤ)^I-valued maps to ℝ^I after pulling back.
This is local surjectivity, not a false global real-lift claim.
-/

noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.RealCircleStonean

theorem profinite_torus_map_lifts_after_stonean_cover
    (P : Profinite.{u}) (I : Type v)
    (f : C(P, I → UnitAddCircle)) :
    ∃ g : C(P.presentation, I → ℝ),
      ∀ x : P.presentation, ∀ i : I,
        ((g x i : ℝ) : UnitAddCircle) =
          f ((Profinite.presentation.π P).hom.hom x) i := by
  let cover : C(P.presentation,P) :=
    ⟨(Profinite.presentation.π P).hom.hom,
      (Profinite.presentation.π P).hom.hom.continuous⟩
  let pulled : C(P.presentation,I → UnitAddCircle) := f.comp cover
  obtain ⟨g,hg⟩ :=
    torus_map_has_continuous_real_lift P.presentation I pulled
  exact ⟨g,fun x i => hg x i⟩

theorem profinite_stonean_cover_is_epi (P : Profinite.{u}) :
    CategoryTheory.Epi (Profinite.presentation.π P) := inferInstance

#print axioms profinite_torus_map_lifts_after_stonean_cover
#print axioms profinite_stonean_cover_is_epi
end CMDG.CondensedCM5R0.RealCircleStonean
