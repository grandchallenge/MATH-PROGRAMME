import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberAW
import Mathlib.AlgebraicTopology.ExtraDegeneracy
import Mathlib.CategoryTheory.Limits.Types.Products

/-! Explicit free bisimplicial representables and contractions of their
diagonal chains. The universal models are indexed by two simplex degrees. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
namespace CMDG.CondensedCM5R0.EilenbergZilberModels

abbrev pair (p q : ℕ) : Δ × Δ := (d p,d q)

def freeZ : Type ⥤ ZMod := AddCommGrpCat.free ⋙ toZModule

def model (p q : ℕ) : Bi := coyoneda.obj (op (pair p q)) ⋙ freeZ

def modelSet (p q : ℕ) : SimplicialObject (Type) :=
  Functor.diag Δ ⋙ coyoneda.obj (op (pair p q))

def aug (p q : ℕ) : SimplicialObject.Augmented (Type) :=
  (modelSet p q).augmentOfIsTerminal Types.isTerminalPUnit

abbrev shift := @SSet.Augmented.StandardSimplex.shift

theorem shift_face {n : ℕ} {z : SimplexCategory}
    (f : SimplexCategory.mk (n+1) ⟶ z) (i : Fin (n+2)) :
    SimplexCategory.δ i.succ ≫ shift f = shift (SimplexCategory.δ i ≫ f) := by
  apply SimplexCategory.Hom.ext
  apply OrderHom.ext
  funext j
  change SSet.Augmented.StandardSimplex.shiftFun f.toOrderHom (i.succ.succAbove j) =
    SSet.Augmented.StandardSimplex.shiftFun ((SimplexCategory.δ i ≫ f).toOrderHom) j
  cases j using Fin.cases
  · rfl
  · rw [Fin.succ_succAbove_succ]
    rfl

theorem shift_degeneracy {n : ℕ} {z : SimplexCategory}
    (f : SimplexCategory.mk n ⟶ z) (i : Fin (n+1)) :
    SimplexCategory.σ i.succ ≫ shift f = shift (SimplexCategory.σ i ≫ f) := by
  apply SimplexCategory.Hom.ext
  apply OrderHom.ext
  funext j
  change SSet.Augmented.StandardSimplex.shiftFun f.toOrderHom (i.succ.predAbove j) =
    SSet.Augmented.StandardSimplex.shiftFun ((SimplexCategory.σ i ≫ f).toOrderHom) j
  cases j using Fin.cases
  · rfl
  · rw [Fin.succ_predAbove_succ]
    rfl

/-- Insert the initial vertex in both coordinates simultaneously. -/
def modelExtra (p q : ℕ) : SimplicialObject.Augmented.ExtraDegeneracy (aug p q) where
  s' := ↾fun _ => ((SimplexCategory.const (SimplexCategory.mk 0) (SimplexCategory.mk p) 0).op,
    (SimplexCategory.const (SimplexCategory.mk 0) (SimplexCategory.mk q) 0).op)
  s n := ↾fun x => ((shift x.1.unop).op,(shift x.2.unop).op)
  s'_comp_ε := by
    apply ConcreteCategory.hom_ext
    intro x
    change (PUnit.unit : PUnit) = _
    rfl
  s₀_comp_δ₁ := by
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    all_goals
      apply congrArg Quiver.Hom.op
      apply SimplexCategory.Hom.ext
      apply OrderHom.ext
      funext i
      fin_cases i
      rfl
  s_comp_δ₀ n := by
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    all_goals
      apply congrArg Quiver.Hom.op
      apply SimplexCategory.Hom.ext
      apply OrderHom.ext
      funext i
      rfl
  s_comp_δ n i := by
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    · exact congrArg Quiver.Hom.op (shift_face x.1.unop i)
    · exact congrArg Quiver.Hom.op (shift_face x.2.unop i)
  s_comp_σ n i := by
    apply ConcreteCategory.hom_ext
    intro x
    apply Prod.ext
    · exact congrArg Quiver.Hom.op (shift_degeneracy x.1.unop i)
    · exact congrArg Quiver.Hom.op (shift_degeneracy x.2.unop i)

/-- Actual diagonal model chain contraction onto the free group on one point. -/
def diagonalModelHomotopy (p q : ℕ) :
    HomotopyEquiv (diagChains (model p q)) ((ChainComplex.single₀ ZMod).obj (freeZ.obj PUnit)) :=
  ((modelExtra p q).map freeZ).homotopyEquiv

def modelGenerator (p q : ℕ) : (model p q).obj (pair p q) :=
  FreeAbelianGroup.of (𝟙 (pair p q))

/-- The universal free representable map induced by an element of a bidegree. -/
def modelEval (B : Bi) (p q : ℕ) (x : B.obj (pair p q)) : model p q ⟶ B where
  app t := ModuleCat.ofHom {
    toFun := FreeAbelianGroup.lift (fun f : pair p q ⟶ t => B.map f x)
    map_add' := map_add _
    map_smul' n y := by
      convert! AddMonoidHom.map_zsmul
        (FreeAbelianGroup.lift (fun f : pair p q ⟶ t => B.map f x)) n y <;>
        ext <;> apply int_smul_eq_zsmul }
  naturality {t u} f := by
    apply ModuleCat.hom_ext
    apply LinearMap.toAddMonoidHom_injective
    apply FreeAbelianGroup.lift_ext
    intro g
    change (FreeAbelianGroup.lift (fun h : pair p q ⟶ u => B.map h x))
        (FreeAbelianGroup.map (fun h => h ≫ f) (FreeAbelianGroup.of g)) =
      B.map f (FreeAbelianGroup.lift (fun h : pair p q ⟶ t => B.map h x) (FreeAbelianGroup.of g))
    rw [FreeAbelianGroup.map_of_apply,FreeAbelianGroup.lift_apply_of,
      FreeAbelianGroup.lift_apply_of,B.map_comp]
    rfl

theorem modelEval_generator (B : Bi) (p q : ℕ) (x : B.obj (pair p q)) :
    (modelEval B p q x).app (pair p q) (modelGenerator p q) = x := by
  change FreeAbelianGroup.lift (fun f : pair p q ⟶ pair p q => B.map f x)
    (FreeAbelianGroup.of (𝟙 _)) = _
  rw [FreeAbelianGroup.lift_apply_of,B.map_id]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem modelEval_comp {B C : Bi} (f : B ⟶ C) (p q : ℕ) (x : B.obj (pair p q)) :
    modelEval B p q x ≫ f = modelEval C p q (f.app (pair p q) x) := by
  apply NatTrans.ext
  funext t
  apply ModuleCat.hom_ext
  apply LinearMap.toAddMonoidHom_injective
  apply FreeAbelianGroup.lift_ext
  intro g
  change f.app t (FreeAbelianGroup.lift (fun h : pair p q ⟶ t => B.map h x)
    (FreeAbelianGroup.of g)) =
    FreeAbelianGroup.lift (fun h : pair p q ⟶ t => C.map h (f.app (pair p q) x))
      (FreeAbelianGroup.of g)
  rw [FreeAbelianGroup.lift_apply_of,FreeAbelianGroup.lift_apply_of]
  exact CategoryTheory.congr_fun (f.naturality g) x

set_option backward.isDefEq.respectTransparency false in
theorem modelEval_zero (B : Bi) (p q : ℕ) : modelEval B p q 0 = 0 := by
  apply NatTrans.ext
  funext t
  apply ModuleCat.hom_ext
  apply LinearMap.toAddMonoidHom_injective
  apply FreeAbelianGroup.lift_ext
  intro g
  change FreeAbelianGroup.lift (fun h : pair p q ⟶ t => B.map h 0) (FreeAbelianGroup.of g) = 0
  rw [FreeAbelianGroup.lift_apply_of]
  exact map_zero (B.map g).hom

set_option backward.isDefEq.respectTransparency false in
theorem modelEval_add (B : Bi) (p q : ℕ) (x y : B.obj (pair p q)) :
    modelEval B p q (x+y) = modelEval B p q x + modelEval B p q y := by
  apply NatTrans.ext
  funext t
  apply ModuleCat.hom_ext
  apply LinearMap.toAddMonoidHom_injective
  apply FreeAbelianGroup.lift_ext
  intro g
  change FreeAbelianGroup.lift (fun h : pair p q ⟶ t => B.map h (x+y)) (FreeAbelianGroup.of g) =
    FreeAbelianGroup.lift (fun h : pair p q ⟶ t => B.map h x) (FreeAbelianGroup.of g) +
    FreeAbelianGroup.lift (fun h : pair p q ⟶ t => B.map h y) (FreeAbelianGroup.of g)
  rw [FreeAbelianGroup.lift_apply_of,FreeAbelianGroup.lift_apply_of,FreeAbelianGroup.lift_apply_of]
  exact map_add (B.map g).hom x y

set_option backward.isDefEq.respectTransparency false in
theorem modelEval_identity (p q : ℕ) :
    modelEval (model p q) p q (modelGenerator p q) = 𝟙 _ := by
  apply NatTrans.ext
  funext t
  apply ModuleCat.hom_ext
  apply LinearMap.toAddMonoidHom_injective
  apply FreeAbelianGroup.lift_ext
  intro g
  change FreeAbelianGroup.lift (fun h : pair p q ⟶ t =>
    (model p q).map h (modelGenerator p q)) (FreeAbelianGroup.of g) = FreeAbelianGroup.of g
  rw [FreeAbelianGroup.lift_apply_of]
  change FreeAbelianGroup.map (fun h => h ≫ g) (FreeAbelianGroup.of (𝟙 _)) = _
  rw [FreeAbelianGroup.map_of_apply,Category.id_comp]

#print axioms modelExtra
#print axioms diagonalModelHomotopy
#print axioms modelEval_comp
#print axioms modelEval_identity
end CMDG.CondensedCM5R0.EilenbergZilberModels
