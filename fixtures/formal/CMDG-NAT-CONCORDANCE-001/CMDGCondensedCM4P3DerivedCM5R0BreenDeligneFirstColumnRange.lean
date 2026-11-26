import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneColumnElimination
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFirstColumnInclusion

/-! The actual first-column chain inclusion has precisely the supported
range in horizontal degree one, because horizontal degree zero vanishes. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneFirstColumnInclusion
open CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates
open CMDG.CondensedCM5R0.BreenDeligneColumnElimination
namespace CMDG.CondensedCM5R0.BreenDeligneFirstColumnRange

abbrev K (X : SimplicialObject AGrp) := barDouble X
abbrev L (X : SimplicialObject AGrp) := firstColumnOnly X

def oneIso (X : SimplicialObject AGrp) (q : ℕ) :
    ((L X).X 1).X q ≅ ((K X).X 1).X q :=
  (HomologicalComplex.eval ZMod c q).mapIso
    (HomologicalComplex.singleObjXSelf c 1 ((K X).X 1))

theorem off_zero (X : SimplicialObject AGrp) (p q : ℕ) (h : p≠1) :
    IsZero (((L X).X p).X q) :=
  (HomologicalComplex.eval ZMod c q).map_isZero
    (HomologicalComplex.isZero_single_obj_X c 1 ((K X).X 1) p h)

theorem zero_value {A : ZMod} (h : IsZero A) (x : A) : x=0 := by
  have he := CategoryTheory.congr_fun (h.eq_of_src (𝟙 A) 0) x
  exact he

set_option backward.isDefEq.respectTransparency false in
theorem first_proj (X : SimplicialObject AGrp) (n q : ℕ) (h : 1+q=n) :
    (suspensionInclusion X).f n ≫ proj (K X) n 1 q h =
      proj (L X) n 1 q h ≫ (oneIso X q).hom := by
  apply HomologicalComplex₂.total.hom_ext
  intro p t hpt
  change p+t=n at hpt
  by_cases hp : p=1
  · subst p
    have ht : t=q := by omega
    subst t
    rw [← Category.assoc, suspensionInclusion_on_summand,Category.assoc,
      incl_proj_same,Category.comp_id,incl_proj_same_assoc]
    rfl
  · exact (off_zero X p t hp).eq_of_src _ _

set_option backward.isDefEq.respectTransparency false in
theorem other_proj (X : SimplicialObject AGrp) (n p q : ℕ) (h : p+q=n) (hp : p≠1) :
    (suspensionInclusion X).f n ≫ proj (K X) n p q h = 0 := by
  apply HomologicalComplex₂.total.hom_ext
  intro a b hab
  change a+b=n at hab
  by_cases ha : a=1
  · subst a
    rw [← Category.assoc,suspensionInclusion_on_summand,Category.assoc,
      incl_proj_other (K X) n p q 1 b h hab (Ne.symm hp),comp_zero,comp_zero]
  · exact (off_zero X a b ha).eq_of_src _ _

theorem first_supported (X : SimplicialObject AGrp) (n : ℕ) (y : (suspendedFirst X).X n) :
    SupportedThrough (K X) n 1 ((suspensionInclusion X).f n y) := by
  intro p q h hp
  exact CategoryTheory.congr_fun (other_proj X n p q h (by omega)) y

theorem first_injective (X : SimplicialObject AGrp) (n : ℕ) :
    Function.Injective ((suspensionInclusion X).f n) := by
  intro y z he
  apply coord_ext (L X) n
  intro p q h
  by_cases hp : p=1
  · subst p
    have hf := congrArg (proj (K X) n 1 q h) he
    have h₁ := CategoryTheory.congr_fun (first_proj X n q h) y
    have h₂ := CategoryTheory.congr_fun (first_proj X n q h) z
    change proj (K X) n 1 q h ((suspensionInclusion X).f n y) = (oneIso X q).hom (proj (L X) n 1 q h y) at h₁
    change proj (K X) n 1 q h ((suspensionInclusion X).f n z) = (oneIso X q).hom (proj (L X) n 1 q h z) at h₂
    rw [h₁,h₂] at hf
    exact (ModuleCat.mono_iff_injective _).mp (show Mono (oneIso X q).hom by infer_instance) hf
  · exact (zero_value (off_zero X p q hp) _).trans (zero_value (off_zero X p q hp) _).symm

theorem first_range (X : SimplicialObject AGrp) (n : ℕ) (x : (barTotal X).X n)
    (hx : SupportedThrough (K X) n 1 x) :
    ∃ y : (suspendedFirst X).X n, (suspensionInclusion X).f n y=x := by
  cases n with
  | zero =>
    refine ⟨0,?_⟩
    apply coord_ext (K X) 0
    intro p q h
    have hp : p=0 := by omega
    subst p
    exact (zero_value (zeroColumn X q) _).trans (zero_value (zeroColumn X q) _).symm
  | succ n =>
    let y := (L X).ιTotal c 1 n (n+1) (by change 1+n=n+1; omega)
      ((oneIso X n).inv (proj (K X) (n+1) 1 n (by omega) x))
    refine ⟨y,?_⟩
    apply coord_ext (K X) (n+1)
    intro p q h
    by_cases hp : p=1
    · subst p
      have hq : q=n := by omega
      subst q
      have hf := CategoryTheory.congr_fun (first_proj X (n+1) n (by omega)) y
      change proj (K X) (n+1) 1 n _ ((suspensionInclusion X).f (n+1) y) =
        (oneIso X n).hom (proj (L X) (n+1) 1 n _ y) at hf
      rw [hf]
      have he : proj (L X) (n+1) 1 n (by omega) y =
          (oneIso X n).inv (proj (K X) (n+1) 1 n (by omega) x) :=
        incl_coord_same _ _ _ _ _ _
      rw [he]
      exact CategoryTheory.congr_fun (oneIso X n).inv_hom_id _
    · by_cases h₀ : p=0
      · subst p
        exact (zero_value (zeroColumn X q) _).trans (zero_value (zeroColumn X q) _).symm
      · rw [hx p q h (by omega)]
        exact first_supported X (n+1) y p q h (by omega)

#print axioms first_injective
#print axioms first_range
end CMDG.CondensedCM5R0.BreenDeligneFirstColumnRange
