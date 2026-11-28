import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteSubcomplex
import Mathlib.Algebra.Homology.QuasiIso

noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteSubcomplex

variable (K : Ch) (h : ∀ n, Module.Finite ℤ (K.homology n))

abbrev obj (n : ℕ) : ZMod := ModuleCat.of ℤ (F K h n)

def dAdd (n : ℕ) : F K h (n+1) →+ F K h n where
  toFun x := ⟨K.d (n+1) n x.val,term_closed K h n x⟩
  map_zero' := by apply Subtype.ext; exact map_zero (K.d (n+1) n).hom
  map_add' x y := by apply Subtype.ext; exact map_add (K.d (n+1) n).hom x.val y.val

def d (n : ℕ) : obj K h (n+1) ⟶ obj K h n :=
  ModuleCat.ofHom (dAdd K h n).toIntLinearMap

theorem d_sq (n : ℕ) : d K h (n+1) ≫ d K h n = 0 := by
  apply ConcreteCategory.hom_ext
  intro x
  apply Subtype.ext
  change K.d (n+1) n (K.d (n+2) (n+1) x.val) = 0
  exact CategoryTheory.congr_fun (K.d_comp_d (n+2) (n+1) n) x.val

abbrev finiteComplex : Ch := ChainComplex.of (obj K h) (d K h) (d_sq K h)

def inclAt (n : ℕ) : obj K h n ⟶ K.X n :=
  ModuleCat.ofHom (CMDG.CondensedCM5R0.BreenDeligneFiniteTotal.intLinear
    ((F K h n).subtype.toAddMonoidHom))

def inclusion : finiteComplex K h ⟶ K :=
  ChainComplex.ofHom (inclAt K h) (by
    intro n
    change inclAt K h (n+1) ≫ K.d (n+1) n =
      ChainComplex.of.d (obj K h) (d K h) (n+1) n ≫ inclAt K h n
    rw [ChainComplex.of_d]
    rfl)

theorem inclusion_apply (n : ℕ) (x : (finiteComplex K h).X n) :
    (inclusion K h).f n x = x.val := rfl

theorem inclusion_inj (n : ℕ) : Function.Injective ((inclusion K h).f n) :=
  Subtype.coe_injective

theorem finite_obj (n : ℕ) : Module.Finite ℤ ((finiteComplex K h).X n) :=
  by
    have hf := @Module.Finite.iff_fg ℤ (K.X n) _ _ _ (F K h n) |>.mpr (finiteTerm K h n).property
    change Module.Finite ℤ (F K h n)
    convert hf using 1 <;> exact Subsingleton.elim _ _

theorem homology_surj (n : ℕ) : Function.Surjective (homologyMap (inclusion K h) n) := by
  intro x
  have hx : x ∈ (cycleLift K h n).map (K.homologyπ n).hom := by
    rw [(cycleLift_spec K h n).2]
    trivial
  obtain ⟨z,hz,hx⟩ := hx
  let y : (finiteComplex K h).X n := ⟨K.iCycles n z,cyclePart_le K h n ⟨z,hz,rfl⟩⟩
  have hy : (finiteComplex K h).d n (n-1) y = 0 := by
    apply inclusion_inj K h (n-1)
    rw [map_zero]
    have hc := CategoryTheory.congr_fun ((inclusion K h).comm n (n-1)).symm y
    change (inclusion K h).f (n-1) ((finiteComplex K h).d n (n-1) y) =
      K.d n (n-1) ((inclusion K h).f n y) at hc
    rw [hc,inclusion_apply]
    exact cycle_closed K n z
  let w := cycleOf (finiteComplex K h) n y hy
  refine ⟨(finiteComplex K h).homologyπ n w,?_⟩
  rw [map_class]
  have hw : cyclesMap (inclusion K h) n w = z := by
    apply iCycles_injective K n
    rw [map_cycle_i,cycleOf_i,inclusion_apply]
  rw [hw]
  exact hx

theorem homology_inj (n : ℕ) : Function.Injective (homologyMap (inclusion K h) n) := by
  apply (injective_iff_map_eq_zero _).2
  intro x hx
  obtain ⟨z,rfl⟩ := class_surj (finiteComplex K h) n x
  rw [map_class] at hx
  obtain ⟨y,hy⟩ := (class_zero_iff K n _).mp hx
  rw [map_cycle_i,inclusion_apply] at hy
  obtain ⟨w,hw⟩ := term_fills K h n ((finiteComplex K h).iCycles n z) y hy
  apply (class_zero_iff (finiteComplex K h) n z).mpr
  refine ⟨w,?_⟩
  apply inclusion_inj K h n
  rw [inclusion_apply,inclusion_apply]
  change ((ChainComplex.of.d (obj K h) (d K h) (n+1) n) w).val = _
  rw [ChainComplex.of_d]
  exact hw

theorem inclusion_quasiIso : QuasiIso (inclusion K h) := by
  apply (quasiIso_iff _).2
  intro n
  apply (quasiIsoAt_iff_isIso_homologyMap _ _).2
  exact (ConcreteCategory.isIso_iff_bijective _).2 ⟨homology_inj K h n,homology_surj K h n⟩

#print axioms inclusion_quasiIso
#print axioms finite_obj
end CMDG.CondensedCM5R0.BreenDeligneFiniteSubcomplex
