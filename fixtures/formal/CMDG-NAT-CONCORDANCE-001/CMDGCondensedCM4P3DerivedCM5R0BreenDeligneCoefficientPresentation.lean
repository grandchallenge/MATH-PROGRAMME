import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRankOneFinite
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticeStabilization
import Mathlib.LinearAlgebra.FreeModule.PID

/-! Finite coefficient presentations over the integers, and natural
transport of coefficient maps to additive lattice functors. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
open CMDG.CondensedCM5R0.BreenDeligneStableLattice
open CMDG.CondensedCM5R0.BreenDeligneStableMatrix
open CMDG.CondensedCM5R0.BreenDeligneLatticeStabilization
open CMDG.CondensedCM5R0.BreenDeligneStableAdditive
open CMDG.CondensedCM5R0.BreenDeligneRankOneFinite
namespace CMDG.CondensedCM5R0.BreenDeligneCoefficientPresentation

abbrev Z := BreenDeligneStableLattice.Z
abbrev I := toZModule.obj Z
def power (b : ℕ) : AGrp ⥤ ZMod where
  obj A := coordModule (toZModule.obj A) b
  map f := coordinateMap (toZModule.map f) b
  map_id _ := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    rfl
  map_comp _ _ := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    rfl

instance (b : ℕ) : (power b).Additive where
  map_add := by
    intros
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    rfl

abbrev freeCoeff (b : ℕ) : ZMod := (power b).obj Z

structure Presentation (M : ZMod) where
  a : ℕ
  b : ℕ
  d : freeCoeff a ⟶ freeCoeff b
  p : freeCoeff b ⟶ M
  inj : Function.Injective d
  surj : Function.Surjective p
  zero : d ≫ p = 0
  exact : (ShortComplex.mk d p zero).Exact

theorem presentation_exists (M : ZMod) [Module.Finite ℤ M] : Nonempty (Presentation M) := by
  classical
  obtain ⟨b,x,hx⟩ := Module.Finite.exists_fin (R:=ℤ) (M:=M)
  let l : (Fin b →₀ ℤ) →ₗ[ℤ] M := Finsupp.linearCombination ℤ x
  have hl : Function.Surjective l := by
    apply LinearMap.range_eq_top.mp
    rw [Finsupp.range_linearCombination,hx]
  let p : freeCoeff b ⟶ M := ConcreteCategory.ofHom (C:=ZMod)
    (X:=freeCoeff b) (Y:=M) (BreenDeligneFiniteTotal.intLinear
      ((l.comp (Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin b)).symm.toLinearMap).toAddMonoidHom))
  have hp : Function.Surjective p := by
    intro y
    obtain ⟨v,hv⟩ := hl y
    exact ⟨(Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin b)) v, by
      change l ((Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin b)).symm
        ((Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin b)) v)) = y
      rw [LinearEquiv.symm_apply_apply,hv]⟩
  haveI : Module.Finite ℤ (freeCoeff b) := by
    change Module.Finite ℤ (Fin b → ℤ)
    infer_instance
  haveI : Module.IsTorsionFree ℤ (freeCoeff b) := by
    apply Module.IsTorsionFree.of_smul_eq_zero
    intro r v h
    by_cases hr : r=0
    · exact Or.inl hr
    · right
      funext i
      have he := congrFun h i
      let w : Fin b → ℤ := v
      change r * w i = 0 at he
      change w i = 0
      exact (mul_eq_zero.mp he).resolve_left hr
  haveI : Module.Finite ℤ (LinearMap.ker p.hom) := inferInstance
  haveI : Module.IsTorsionFree ℤ (LinearMap.ker p.hom) := inferInstance
  obtain ⟨a,e⟩ := Module.basisOfFiniteTypeTorsionFree' (R:=ℤ) (M:=LinearMap.ker p.hom)
  let g : (Fin a → ℤ) ≃ₗ[ℤ] LinearMap.ker p.hom :=
    (Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin a)).symm.trans e.repr.symm
  let d : freeCoeff a ⟶ freeCoeff b := ConcreteCategory.ofHom (C:=ZMod)
    (X:=freeCoeff a) (Y:=freeCoeff b) (BreenDeligneFiniteTotal.intLinear
      ((LinearMap.ker p.hom).subtype.comp g.toLinearMap).toAddMonoidHom)
  have hd : Function.Injective d := fun u v h => g.injective (Subtype.ext h)
  have hz : d ≫ p = 0 := by
    apply ConcreteCategory.hom_ext
    intro v
    exact (g v).property
  refine ⟨⟨a,b,d,p,hd,hp,hz,?_⟩⟩
  apply (ShortComplex.moduleCat_exact_iff _).mpr
  intro y hy
  obtain ⟨v,hv⟩ := g.surjective ⟨y,hy⟩
  exact ⟨v,congrArg Subtype.val hv⟩

def presentation (M : ZMod) [Module.Finite ℤ M] : Presentation M :=
  Classical.choice (presentation_exists M)

variable {F G : AGrp ⥤ ZMod} [F.Additive] [G.Additive]

def coeffComponent (f : F.obj Z ⟶ G.obj Z) (r : Latt) :
    F.obj (lattice r) ⟶ G.obj (lattice r) :=
  (coordinateIso F r).hom ≫ coordinateMap f r ≫ (coordinateIso G r).inv

theorem coeffComponent_apply (f : F.obj Z ⟶ G.obj Z) (r : Latt)
    (x : F.obj (lattice r)) (i : Fin r) :
    (coordinateIso G r).hom (coeffComponent f r x) i =
      f ((coordinateIso F r).hom x i) := by
  change (coordinateIso G r).hom ((coordinateIso G r).inv
    (coordinateMap f r ((coordinateIso F r).hom x))) i = _
  rw [show (coordinateIso G r).hom ((coordinateIso G r).inv
    (coordinateMap f r ((coordinateIso F r).hom x))) =
    coordinateMap f r ((coordinateIso F r).hom x) from
      CategoryTheory.congr_fun (coordinateIso G r).inv_hom_id _]
  rfl

def coeffNat (f : F.obj Z ⟶ G.obj Z) :
    valueFunctor ⋙ F ⟶ valueFunctor ⋙ G where
  app := coeffComponent f
  naturality {r s} g := by
    apply (cancel_mono (coordinateIso G s).hom).mp
    apply ConcreteCategory.hom_ext
    intro x
    funext j
    change (coordinateIso G s).hom (coeffComponent f s (F.map (valueFunctor.map g) x)) j =
      (coordinateIso G s).hom (G.map (valueFunctor.map g) (coeffComponent f r x)) j
    rw [coeffComponent_apply]
    have hF := matrix_action F (valueFunctor.map g) x j
    have hG := matrix_action G (valueFunctor.map g) (coeffComponent f r x) j
    change (coordinateIso F s).hom (F.map (valueFunctor.map g) x) j = _ at hF
    change (coordinateIso G s).hom (G.map (valueFunctor.map g) (coeffComponent f r x)) j = _ at hG
    rw [hF,hG]
    change f.hom (∑ i : Fin r, entry (valueFunctor.map g) j i • ((coordinateIso F r).hom x i)) = _
    rw [map_sum]
    apply Finset.sum_congr rfl
    intro i _
    rw [coeffComponent_apply]
    exact map_zsmul f.hom _ _

theorem coeffComponent_injective (f : F.obj Z ⟶ G.obj Z) (hf : Function.Injective f)
    (r : Latt) : Function.Injective (coeffComponent f r) := by
  intro x y h
  apply (ConcreteCategory.bijective_of_isIso (coordinateIso F r).hom).injective
  funext i
  apply hf
  rw [← coeffComponent_apply,← coeffComponent_apply,h]

theorem coeffComponent_surjective (f : F.obj Z ⟶ G.obj Z) (hf : Function.Surjective f)
    (r : Latt) : Function.Surjective (coeffComponent f r) := by
  intro y
  choose x hx using fun i : Fin r => hf ((coordinateIso G r).hom y i)
  refine ⟨(coordinateIso F r).inv x,?_⟩
  apply (ConcreteCategory.bijective_of_isIso (coordinateIso G r).hom).injective
  funext i
  rw [coeffComponent_apply]
  have he := CategoryTheory.congr_fun (coordinateIso F r).inv_hom_id x
  change (coordinateIso F r).hom ((coordinateIso F r).inv x) = x at he
  rw [he,hx]

#print axioms presentation
#print axioms coeffNat
end CMDG.CondensedCM5R0.BreenDeligneCoefficientPresentation

namespace CMDG.CondensedCM5R0.BreenDeligneCoefficientPresentation
variable {F G H : AGrp ⥤ ZMod} [F.Additive] [G.Additive] [H.Additive]

theorem coeffNat_exact_pointwise (d : F.obj Z ⟶ G.obj Z)
    (p : G.obj Z ⟶ H.obj Z) (hz : d ≫ p = 0)
    (he : (ShortComplex.mk d p hz).Exact) (r : Latt)
    (x : G.obj (lattice r)) (hx : coeffComponent p r x = 0) :
    ∃ y : F.obj (lattice r), coeffComponent d r y = x := by
  have hk (i : Fin r) : p ((coordinateIso G r).hom x i) = 0 := by
    rw [← coeffComponent_apply,hx,map_zero]
    rfl
  choose y hy using fun i : Fin r => (ShortComplex.moduleCat_exact_iff _).mp he _ (hk i)
  refine ⟨(coordinateIso F r).inv y,?_⟩
  apply (ConcreteCategory.bijective_of_isIso (coordinateIso G r).hom).injective
  funext i
  rw [coeffComponent_apply]
  have hh := CategoryTheory.congr_fun (coordinateIso F r).inv_hom_id y
  change (coordinateIso F r).hom ((coordinateIso F r).inv y) = y at hh
  rw [hh,hy]

theorem coeffNat_zero (d : F.obj Z ⟶ G.obj Z)
    (p : G.obj Z ⟶ H.obj Z) (hz : d ≫ p = 0) :
    coeffNat d ≫ coeffNat p = 0 := by
  apply NatTrans.ext
  funext r
  apply ConcreteCategory.hom_ext
  intro x
  apply (ConcreteCategory.bijective_of_isIso (coordinateIso H r).hom).injective
  funext i
  change (coordinateIso H r).hom (coeffComponent p r (coeffComponent d r x)) i =
    (coordinateIso H r).hom 0 i
  rw [coeffComponent_apply,coeffComponent_apply,map_zero]
  exact CategoryTheory.congr_fun hz ((coordinateIso F r).hom x i)

structure LatticePresentation (F : AGrp ⥤ ZMod) where
  a : ℕ
  b : ℕ
  d : valueFunctor ⋙ power a ⟶ valueFunctor ⋙ power b
  p : valueFunctor ⋙ power b ⟶ valueFunctor ⋙ F
  mono : Mono d
  epi : Epi p
  zero : d ≫ p = 0
  exactAt : ∀ r, (ShortComplex.mk (d.app r) (p.app r) (NatTrans.congr_app zero r)).Exact

def latticePresentation (F : AGrp ⥤ ZMod) [F.Additive]
    [Module.Finite ℤ (F.obj Z)] : LatticePresentation F := by
  let P := presentation (F.obj Z)
  let d := coeffNat (F:=power P.a) (G:=power P.b) P.d
  let p := coeffNat (F:=power P.b) (G:=F) P.p
  have hz : d ≫ p = 0 := coeffNat_zero P.d P.p P.zero
  refine ⟨P.a,P.b,d,p,?_,?_,hz,?_⟩
  · apply (NatTrans.mono_iff_mono_app _).mpr
    intro r
    exact (ModuleCat.mono_iff_injective _).mpr (coeffComponent_injective P.d P.inj r)
  · apply (NatTrans.epi_iff_epi_app _).mpr
    intro r
    exact (ModuleCat.epi_iff_surjective _).mpr (coeffComponent_surjective P.p P.surj r)
  · intro r
    apply (ShortComplex.moduleCat_exact_iff _).mpr
    exact coeffNat_exact_pointwise P.d P.p P.zero P.exact r

def stablePresentation (n k : ℕ) (hk : k<n) :
    LatticePresentation (stableFunctor n k) := by
  letI := stableFunctor_additive n k hk
  letI := stable_rank_one_finite n k (by omega)
  exact latticePresentation _

#print axioms latticePresentation
#print axioms stablePresentation
end CMDG.CondensedCM5R0.BreenDeligneCoefficientPresentation
