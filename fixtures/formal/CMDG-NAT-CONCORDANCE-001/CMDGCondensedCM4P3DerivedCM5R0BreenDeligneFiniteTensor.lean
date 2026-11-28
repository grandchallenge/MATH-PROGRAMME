import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteSubcomplexComparison
import Mathlib.Algebra.Homology.DerivedCategory.KProjective
import Mathlib.Algebra.Category.ModuleCat.Projective
import Mathlib.Algebra.Category.ModuleCat.Biproducts
import Mathlib.RingTheory.Finiteness.Bilinear
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneReducedBasis

/-! Finite replacement is homotopy equivalent for degreewise free
integral complexes. Finite tensor powers preserve the equivalence. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneFiniteSubcomplex
open CMDG.CondensedCM5R0.BreenDeligneFiniteBar
open CMDG.CondensedCM5R0.BreenDeligneColumnConnectivity
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteTensor

theorem finiteTensor (M N : ZMod) [Module.Finite ℤ M] [Module.Finite ℤ N] :
    Module.Finite ℤ (M ⊗ N : ZMod) := by
  exact ⟨(TensorProduct.map₂_mk_top_top_eq_top ℤ M N).subst
    ((Module.Finite.fg_top (R:=ℤ) (M:=M)).map₂ _
      (Module.Finite.fg_top (R:=ℤ) (M:=N)))⟩

theorem finiteCoproduct {J : Type} [Finite J] (f : J → ZMod)
    (hf : ∀ j, Module.Finite ℤ (f j)) : Module.Finite ℤ (∐ f : ZMod) := by
  classical
  letI := Fintype.ofFinite J
  letI (j : J) : Module.Finite ℤ (f j) := hf j
  let B : ZMod := ⨁ f
  let W (j : J) : Submodule ℤ B := LinearMap.range (biproduct.ι f j).hom
  have hW : (⨆ j, W j).FG := Submodule.fg_iSup W (fun j => Submodule.fg_range _)
  have htop : (⨆ j, W j) = ⊤ := by
    apply eq_top_iff.mpr
    intro x _
    have hh := CategoryTheory.congr_fun (biproduct.total (f := f)) x
    change (∑ j, biproduct.π f j ≫ biproduct.ι f j).hom x = x at hh
    rw [ModuleCat.hom_sum,LinearMap.sum_apply] at hh
    rw [← hh]
    apply Submodule.sum_mem
    intro j _
    exact (le_iSup W j) ⟨biproduct.π f j x,rfl⟩
  haveI : Module.Finite ℤ B := ⟨htop ▸ hW⟩
  exact finiteOfIso (biproduct.isoCoproduct f).symm

theorem finiteTensorTerm (K L : Ch) (hK : ∀ i, Module.Finite ℤ (K.X i))
    (hL : ∀ i, Module.Finite ℤ (L.X i)) (n : ℕ) :
    Module.Finite ℤ ((HomologicalComplex.tensorObj K L).X n) := by
  let I := {p : ℕ × ℕ // p.1+p.2=n}
  haveI : Finite I := Finite.of_injective
    (fun x : I => (⟨x.val.1,by have h := x.property; omega⟩ : Fin (n+1)))
    (by
      intro a b hab
      have he := congrArg Fin.val hab
      apply Subtype.ext
      apply Prod.ext
      · exact he
      · have ha := a.property
        have hb := b.property
        change a.val.1 = b.val.1 at he
        omega)
  change Module.Finite ℤ (∐ (fun p : I => K.X p.val.1 ⊗ L.X p.val.2) : ZMod)
  apply finiteCoproduct
  intro p
  letI := hK p.val.1
  letI := hL p.val.2
  exact finiteTensor _ _

theorem finiteHomology (K : Ch) (n : ℕ) [Module.Finite ℤ (K.X n)] :
    Module.Finite ℤ (K.homology n) := by
  letI : Module.Finite ℤ (K.cycles n) :=
    Module.Finite.of_injective (K.iCycles n).hom (iCycles_injective K n)
  exact Module.Finite.of_surjective (K.homologyπ n).hom (class_surj K n)

def finiteReplacement (K : Ch) (h : ∀ n, Module.Finite ℤ (K.homology n))
    (hK : ∀ n, Module.Free ℤ (K.X n)) :
    HomotopyEquiv (finiteComplex K h) K := by
  letI (n : ℕ) : Module.Free ℤ (K.X n) := hK n
  letI (n : ℕ) : CategoryTheory.Projective (K.X n) := inferInstance
  letI (n : ℕ) : Module.Finite ℤ ((finiteComplex K h).X n) := finite_obj K h n
  letI (n : ℕ) : Module.IsTorsionFree ℤ ((finiteComplex K h).X n) :=
    Function.Injective.moduleIsTorsionFree ((inclusion K h).f n)
      (inclusion_inj K h n) (fun r x => ((inclusion K h).f n).hom.map_smul r x)
  letI (n : ℕ) : Module.Free ℤ ((finiteComplex K h).X n) := inferInstance
  letI (n : ℕ) : CategoryTheory.Projective ((finiteComplex K h).X n) := inferInstance
  exact Classical.choose ((ChainComplex.quasiIso_iff_of_projective (inclusion K h)).1
    (inclusion_quasiIso K h))

def tensorEquivLeft {K L : Ch} (e : HomotopyEquiv K L) (M : Ch) :
    HomotopyEquiv (HomologicalComplex.tensorObj K M) (HomologicalComplex.tensorObj L M) where
  hom := HomologicalComplex.tensorHom e.hom (𝟙 M)
  inv := HomologicalComplex.tensorHom e.inv (𝟙 M)
  homotopyHomInvId := by
    have h := mapBifunctorMapHomotopy₁ e.homotopyHomInvId (𝟙 M) (curriedTensor ZMod) c
    change Homotopy ((e.hom ≫ e.inv) ⊗ₘ (𝟙 M)) ((𝟙 K) ⊗ₘ (𝟙 M)) at h
    change Homotopy ((e.hom ⊗ₘ (𝟙 M)) ≫ (e.inv ⊗ₘ (𝟙 M))) (𝟙 _)
    rw [tensorHom_comp_tensorHom, Category.id_comp]
    simpa only [tensorHom_id, id_whiskerRight] using h
  homotopyInvHomId := by
    have h := mapBifunctorMapHomotopy₁ e.homotopyInvHomId (𝟙 M) (curriedTensor ZMod) c
    change Homotopy ((e.inv ≫ e.hom) ⊗ₘ (𝟙 M)) ((𝟙 L) ⊗ₘ (𝟙 M)) at h
    change Homotopy ((e.inv ⊗ₘ (𝟙 M)) ≫ (e.hom ⊗ₘ (𝟙 M))) (𝟙 _)
    rw [tensorHom_comp_tensorHom, Category.id_comp]
    simpa only [tensorHom_id, id_whiskerRight] using h

def powerEquiv {K L : Ch} (e : HomotopyEquiv K L) : ∀ p, HomotopyEquiv (tensorPower K p) (tensorPower L p)
  | 0 => HomotopyEquiv.refl _
  | p+1 => (tensorEquivLeft (powerEquiv e p) K).trans (tensorEquiv (tensorPower L p) e)

theorem finiteUnitTerm (n : ℕ) : Module.Finite ℤ ((tensorUnit ZMod c).X n) := by
  by_cases hn : n = 0
  · subst n
    apply finiteOfIso (HomologicalComplex.singleObjXSelf c 0 (𝟙_ ZMod))
  · exact finiteOfZero _ (HomologicalComplex.isZero_single_obj_X c 0 (𝟙_ ZMod) n hn)

theorem finitePowerTerm (K : Ch) (h : ∀ n, Module.Finite ℤ (K.X n)) (p n : ℕ) :
    Module.Finite ℤ ((tensorPower K p).X n) := by
  induction p generalizing n with
  | zero => exact finiteUnitTerm n
  | succ p ih => exact finiteTensorTerm _ _ ih h n

theorem finitePowerHomology (K : Ch) (h : ∀ n, Module.Finite ℤ (K.homology n))
    (hK : ∀ n, Module.Free ℤ (K.X n)) (p n : ℕ) :
    Module.Finite ℤ ((tensorPower K p).homology n) := by
  let L := finiteComplex K h
  letI := finitePowerTerm L (finite_obj K h) p n
  letI := finiteHomology (tensorPower L p) n
  exact finiteOfIso ((powerEquiv (finiteReplacement K h hK) p).toHomologyIso n).symm

#print axioms finiteReplacement
#print axioms finitePowerHomology
end CMDG.CondensedCM5R0.BreenDeligneFiniteTensor
