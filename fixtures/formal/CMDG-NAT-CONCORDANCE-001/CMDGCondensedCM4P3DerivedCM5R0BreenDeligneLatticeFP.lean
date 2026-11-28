import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFPApproximation
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteTermProjectives
import CMDGCondensedCM4P3DerivedCM5R0StoneanCechDegreeOneClosure

/-! Apply the abstract FP calculus to actual finite polynomial
representables on the lattice skeleton. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits Opposite
open scoped ZeroObject
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
open CMDG.CondensedCM5R0.BreenDeligneFiniteTermProjectives
open CMDG.CondensedCM5R0.BreenDeligneFP
open CMDG.CondensedCM5R0.BreenDeligneFPClosure
open CMDG.CondensedCM5R0.BreenDeligneCoefficientPresentation
open CMDG.CondensedCM5R0.BreenDeligneStableAdditive
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
namespace CMDG.CondensedCM5R0.BreenDeligneLatticeFP

abbrev LC := Latt ⥤ ZMod
abbrev V : LC := valueFunctor ⋙ toZModule
def poly (n : Latt) : LC := coyoneda.obj (op n) ⋙ ModuleCat.free ℤ

def polyEquiv (n : Latt) (F : LC) : (poly n ⟶ F) ≃ F.obj n :=
  (((ModuleCat.adj ℤ).whiskerRight Latt).homEquiv (coyoneda.obj (op n)) F).trans coyonedaEquiv

theorem polyEquiv_comp (n : Latt) {F G : LC} (f : poly n ⟶ F) (g : F ⟶ G) :
    polyEquiv n G (f ≫ g) = g.app n (polyEquiv n F f) := by
  let adj := (ModuleCat.adj ℤ).whiskerRight Latt
  change coyonedaEquiv (adj.homEquiv (coyoneda.obj (op n)) G (f ≫ g)) =
    g.app n (coyonedaEquiv (adj.homEquiv (coyoneda.obj (op n)) F f))
  have h := adj.homEquiv_naturality_right (X := coyoneda.obj (op n)) f g
  exact (congrArg coyonedaEquiv h).trans (coyonedaEquiv_comp _ _)

theorem polyProjective (n : Latt) : Projective (poly n) where
  factors f e he := by
    have hE : Epi (e.app n) := (NatTrans.epi_iff_epi_app e).mp he n
    obtain ⟨x,hx⟩ := (ModuleCat.epi_iff_surjective _).mp hE (polyEquiv n _ f)
    refine ⟨(polyEquiv n _).symm x,?_⟩
    apply (polyEquiv n _).injective
    rw [polyEquiv_comp,Equiv.apply_symm_apply,hx]

inductive FinitePoly : LC → Prop
  | zero : FinitePoly 0
  | rep (n : Latt) : FinitePoly (poly n)
  | sum {F G : LC} : FinitePoly F → FinitePoly G → FinitePoly (F ⊞ G)

theorem finitePoly_projective {F : LC} (h : FinitePoly F) : Projective F := by
  induction h with
  | zero => infer_instance
  | rep n => exact polyProjective n
  | sum hF hG iF iG =>
    letI := iF
    letI := iG
    constructor
    intro X Y f e he
    letI := he
    refine ⟨biprod.desc (Projective.factorThru (biprod.inl ≫ f) e)
      (Projective.factorThru (biprod.inr ≫ f) e),?_⟩
    apply biprod.hom_ext'
    · rw [biprod.inl_desc_assoc,Projective.factorThru_comp]
    · rw [biprod.inr_desc_assoc,Projective.factorThru_comp]

def latFinite : FiniteClass LC where
  finite := FinitePoly
  projective _ := finitePoly_projective
  zero := FinitePoly.zero
  sum _ _ := FinitePoly.sum

def freeTypeComponent (X : Type) :
    (AddCommGrpCat.free ⋙ toZModule).obj X ≅ (ModuleCat.free ℤ).obj X :=
  (FreeAbelianGroup.equivFinsupp X).toIntLinearEquiv.toModuleIso

theorem freeType_gen (X : Type) (x : X) :
    (freeTypeComponent X).hom (FreeAbelianGroup.of x) = ModuleCat.freeMk x :=
  FreeAbelianGroup.toFinsupp_of x

def freeTypeIso : AddCommGrpCat.free ⋙ toZModule ≅ ModuleCat.free ℤ :=
  NatIso.ofComponents freeTypeComponent (by
    intro X Y f
    apply ConcreteCategory.hom_ext
    intro x
    change (freeTypeComponent Y).hom (FreeAbelianGroup.map f x) =
      (ModuleCat.free ℤ).map f ((freeTypeComponent X).hom x)
    induction x using FreeAbelianGroup.induction_on with
    | zero => rw [map_zero,map_zero,map_zero,map_zero]
    | of x =>
      have he : FreeAbelianGroup.map f (FreeAbelianGroup.of x) = FreeAbelianGroup.of (f x) := by
        change FreeAbelianGroup.lift (fun a : X => FreeAbelianGroup.of (f a)) (FreeAbelianGroup.of x) = _
        exact FreeAbelianGroup.lift_apply_of _ _
      rw [he,freeType_gen,freeType_gen,ModuleCat.free_map_apply]
    | neg x hx => rw [map_neg,map_neg,map_neg,map_neg,hx]
    | add x y hx hy => rw [map_add,map_add,map_add,map_add,hx,hy])

def termRetract (n m : ℕ) :
    Retract (latticeChainDegree n m ⋙ toZModule) (poly (EilenbergMacLaneModel.activeRank n m)) := by
  let t : Latt := EilenbergMacLaneModel.activeRank n m
  let X : Latt ⥤ Type := coyoneda.obj (op t)
  let e : polynomial t ⋙ toZModule ≅ poly t :=
    Functor.associator X AddCommGrpCat.free toZModule ≪≫ Functor.isoWhiskerLeft X freeTypeIso
  let r : Retract (latticeChainDegree n m ⋙ toZModule) (polynomial t ⋙ toZModule) :=
    (latticeTermRetract n m).map ((Functor.whiskeringRight Latt AGrp ZMod).obj toZModule)
  exact r.trans (Retract.ofIso e)

theorem term_fp (n m k : ℕ) : FP latFinite k (latticeChainDegree n m ⋙ toZModule) :=
  fp_retract latFinite (termRetract n m) (fp_of_finite latFinite k (FinitePoly.rep _))

abbrev Pow (b : ℕ) : LC := valueFunctor ⋙ power b

def powerIn (b : ℕ) : Pow b ⟶ Pow (b+1) where
  app r := ConcreteCategory.ofHom (C:=ZMod) (X:=(Pow b).obj r) (Y:=(Pow (b+1)).obj r)
    (BreenDeligneFiniteTotal.intLinear {
      toFun := fun x => Fin.cons (α:=fun _ => toZModule.obj (lattice r)) 0 x
      map_zero' := by funext i; refine Fin.cases ?_ (fun j => ?_) i <;> rfl
      map_add' := by intro x y; funext i; refine Fin.cases ?_ (fun j => ?_) i
                     · change (0 : lattice r) = 0+0; simp
                     · rfl })
  naturality {r s} f := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    refine Fin.cases ?_ (fun j => ?_) i
    · change (0 : lattice s) = valueFunctor.map f 0; rw [map_zero]
    · rfl

def powerOut (b : ℕ) : Pow (b+1) ⟶ V where
  app r := ConcreteCategory.ofHom (C:=ZMod) (X:=(Pow (b+1)).obj r) (Y:=V.obj r)
    (BreenDeligneFiniteTotal.intLinear {
      toFun := fun x => x 0
      map_zero' := rfl
      map_add' := fun _ _ => rfl })
  naturality {r s} f := by apply ConcreteCategory.hom_ext; intro x; rfl

theorem powerZero (b : ℕ) : powerIn b ≫ powerOut b = 0 := by
  apply NatTrans.ext
  funext r
  apply ConcreteCategory.hom_ext
  intro x
  rfl

def powerSC (b : ℕ) : ShortComplex LC := ShortComplex.mk (powerIn b) (powerOut b) (powerZero b)

theorem powerSC_exact (b : ℕ) : (powerSC b).ShortExact := by
  refine { exact := ?_, mono_f := ?_, epi_g := ?_ }
  · apply functorShortComplex_exact_of_pointwise
    intro r
    apply (ShortComplex.moduleCat_exact_iff _).mpr
    intro x hx
    change x 0 = 0 at hx
    refine ⟨fun i => x i.succ,?_⟩
    funext i
    refine Fin.cases ?_ (fun j => ?_) i
    · exact hx.symm
    · rfl
  · apply (NatTrans.mono_iff_mono_app _).mpr
    intro r
    apply (ModuleCat.mono_iff_injective _).mpr
    intro x y h
    funext i
    exact congrFun h i.succ
  · apply (NatTrans.epi_iff_epi_app _).mpr
    intro r
    apply (ModuleCat.epi_iff_surjective _).mpr
    intro x
    exact ⟨Fin.cons (α:=fun _ => toZModule.obj (lattice r)) x (fun _ => 0),rfl⟩

theorem power_fp (k b : ℕ) (h : FP latFinite k V) : FP latFinite k (Pow b) := by
  induction b with
  | zero =>
    have hZ : IsZero (Pow 0) := by
      apply (IsZero.iff_id_eq_zero _).mpr
      apply NatTrans.ext
      funext r
      apply ConcreteCategory.hom_ext
      intro x
      funext i
      exact Fin.elim0 i
    exact fp_iso latFinite hZ.isoZero.symm (fp_of_finite latFinite k FinitePoly.zero)
  | succ b ih => exact fp_extension latFinite k (powerSC b) (powerSC_exact b) ih h

def coefficientSC (n k : ℕ) (hk : k<n) : ShortComplex LC :=
  let P := stablePresentation n k hk
  ShortComplex.mk P.d P.p P.zero

theorem coefficientSC_exact (n k : ℕ) (hk : k<n) : (coefficientSC n k hk).ShortExact := by
  let P := stablePresentation n k hk
  refine { exact := ?_, mono_f := P.mono, epi_g := P.epi }
  apply functorShortComplex_exact_of_pointwise
  exact P.exactAt

theorem stable_fp (r n k : ℕ) (hk : k<n) (h : FP latFinite (r+1) V) :
    FP latFinite (r+1) (valueFunctor ⋙ stableFunctor n k) := by
  let P := stablePresentation n k hk
  exact fp_cokernel latFinite r (coefficientSC n k hk) (coefficientSC_exact n k hk)
    (power_fp r P.a (fp_mono_degree latFinite r h)) (power_fp (r+1) P.b h)

theorem stable_fp_zero (n k : ℕ) (hk : k<n) (h : FP latFinite 0 V) :
    FP latFinite 0 (valueFunctor ⋙ stableFunctor n k) := by
  let P := stablePresentation n k hk
  letI := P.epi
  exact fp0_epi latFinite P.p (power_fp 0 P.b h)

#print axioms term_fp
#print axioms power_fp
#print axioms stable_fp
end CMDG.CondensedCM5R0.BreenDeligneLatticeFP
