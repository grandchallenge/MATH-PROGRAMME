import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberModels

/-! The natural transformations and free-model evaluation machinery
for the acyclic-model construction. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberModels
open CMDG.CondensedCM5R0.EilenbergZilberAW
namespace CMDG.CondensedCM5R0.EilenbergZilberNatural

def D : Bi ⥤ Ch :=
  (Functor.whiskeringLeft Δ (Δ × Δ) ZMod).obj (Functor.diag Δ) ⋙ alternatingFaceMapComplex ZMod

def doubleF : Bi ⥤ HomologicalComplex₂ ZMod c c :=
  Functor.curry ⋙
    (Functor.whiskeringRight Δ (SimplicialObject ZMod) Ch).obj (alternatingFaceMapComplex ZMod) ⋙
    alternatingFaceMapComplex Ch

def Tot : Bi ⥤ Ch :=
  doubleF ⋙ HomologicalComplex₂.totalFunctor ZMod c c c

instance : D.Additive where
  map_add := by intros; rfl

instance : doubleF.Additive where
  map_add := by intros; rfl

set_option backward.isDefEq.respectTransparency false in
instance : Tot.Additive where
  map_add := by
    intro B C f g
    apply HomologicalComplex.Hom.ext
    funext n
    apply HomologicalComplex₂.total.hom_ext
    intro p q h
    change (double B).ιTotal c p q n h ≫
      (HomologicalComplex₂.total.map (doubleF.map (f+g)) c).f n =
      (double B).ιTotal c p q n h ≫
        ((HomologicalComplex₂.total.map (doubleF.map f) c).f n +
         (HomologicalComplex₂.total.map (doubleF.map g) c).f n)
    rw [Preadditive.comp_add,HomologicalComplex₂.ιTotal_map,
      HomologicalComplex₂.ιTotal_map,HomologicalComplex₂.ιTotal_map]
    change (f.app (pair p q) + g.app (pair p q)) ≫ _ = _
    rw [Preadditive.add_comp]
    rfl

abbrev degree (F : Bi ⥤ Ch) (n : ℕ) : Bi ⥤ ZMod := F ⋙ HomologicalComplex.eval ZMod c n

instance (F : Bi ⥤ Ch) [F.Additive] (n : ℕ) : (degree F n).Additive := by
  unfold degree
  infer_instance

set_option backward.isDefEq.respectTransparency false in
theorem awDegree_natural {B C : Bi} (f : B ⟶ C) (n : ℕ) :
    (D.map f).f n ≫ awDegree C n = awDegree B n ≫ (Tot.map f).f n := by
  rw [awDegree,awDegree,Preadditive.comp_sum,Preadditive.sum_comp]
  apply Finset.sum_congr rfl
  intro i _
  unfold awTerm
  change f.app (pair n n) ≫ C.map _ ≫ _ =
    (B.map _ ≫ (double B).ιTotal c i.val (n-i.val) n _) ≫
      (HomologicalComplex₂.total.map (doubleF.map f) c).f n
  rw [← Category.assoc,Category.assoc (B.map _),HomologicalComplex₂.ιTotal_map,← Category.assoc (B.map _)]
  change (f.app (pair n n) ≫ C.map _) ≫ _ = (B.map _ ≫ f.app (pair i.val (n-i.val))) ≫ _
  rw [f.naturality]
  rfl

def awNat : D ⟶ Tot where
  app B := aw B
  naturality {B C} f := by
    apply HomologicalComplex.Hom.ext
    funext n
    exact awDegree_natural f n

/-- Every natural map out of a bidegree is explicitly determined
by its value at the identity generator of the free representable. -/
def evalLift (G : Bi ⥤ ZMod) [G.Additive] (p q : ℕ) (z : G.obj (model p q)) :
    (CategoryTheory.evaluation (Δ × Δ) ZMod).obj (pair p q) ⟶ G where
  app B := ModuleCat.ofHom {
    toFun x := G.map (modelEval B p q x) z
    map_add' x y := by
      rw [modelEval_add,Functor.map_add]
      rfl
    map_smul' n x := by
      -- Additive maps of abelian groups preserve integer multiples.
      let f : B.obj (pair p q) →+ G.obj B :=
        { toFun x := G.map (modelEval B p q x) z
          map_zero' := by rw [modelEval_zero,Functor.map_zero]; rfl
          map_add' x y := by rw [modelEval_add,Functor.map_add]; rfl }
      convert! AddMonoidHom.map_zsmul f n x <;>
        try rfl
      · congr 1; congr 1; congr 1
        exact congrArg (modelEval B p q) (int_smul_eq_zsmul (B.obj (pair p q)).isModule n x)
      · ext
        apply int_smul_eq_zsmul }
  naturality {B C} f := by
    apply ConcreteCategory.hom_ext
    intro x
    change G.map (modelEval C p q (f.app (pair p q) x)) z =
      G.map f (G.map (modelEval B p q x) z)
    rw [← modelEval_comp,Functor.map_comp]
    rfl

theorem evalLift_generator (G : Bi ⥤ ZMod) [G.Additive] (p q : ℕ)
    (z : G.obj (model p q)) :
    (evalLift G p q z).app (model p q) (modelGenerator p q) = z := by
  change G.map (modelEval (model p q) p q (modelGenerator p q)) z = z
  rw [modelEval_identity,G.map_id]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem eval_ext (G : Bi ⥤ ZMod) (p q : ℕ)
    (f g : (CategoryTheory.evaluation (Δ × Δ) ZMod).obj (pair p q) ⟶ G)
    (h : f.app (model p q) (modelGenerator p q) = g.app (model p q) (modelGenerator p q)) :
    f = g := by
  apply NatTrans.ext
  funext B
  apply ConcreteCategory.hom_ext
  intro x
  have hf := CategoryTheory.congr_fun (f.naturality (modelEval B p q x)) (modelGenerator p q)
  have hg := CategoryTheory.congr_fun (g.naturality (modelEval B p q x)) (modelGenerator p q)
  change f.app B ((modelEval B p q x).app (pair p q) (modelGenerator p q)) =
    G.map (modelEval B p q x) (f.app (model p q) (modelGenerator p q)) at hf
  change g.app B ((modelEval B p q x).app (pair p q) (modelGenerator p q)) =
    G.map (modelEval B p q x) (g.app (model p q) (modelGenerator p q)) at hg
  rw [modelEval_generator] at hf hg
  rw [hf,hg,h]

abbrev Split (n : ℕ) := {i : ℕ × ℕ // i.1+i.2=n}

def splitGenerator (n : ℕ) (i : Split n) : (degree Tot n).obj (model i.val.1 i.val.2) :=
  (double (model i.val.1 i.val.2)).ιTotal c i.val.1 i.val.2 n i.property
    (modelGenerator i.val.1 i.val.2)

set_option backward.isDefEq.respectTransparency false in
def summandNat (n p q : ℕ) (h : p+q=n) :
    (evaluation (Δ × Δ) ZMod).obj (pair p q) ⟶ degree Tot n where
  app B := (double B).ιTotal c p q n h
  naturality {B C} f := by
    change f.app (pair p q) ≫ (double C).ιTotal c p q n h =
      (double B).ιTotal c p q n h ≫ (HomologicalComplex₂.total.map (doubleF.map f) c).f n
    rw [HomologicalComplex₂.ιTotal_map]
    rfl

set_option backward.isDefEq.respectTransparency false in
def totalLift (G : Bi ⥤ ZMod) [G.Additive] (n : ℕ)
    (z : ∀ i : Split n, G.obj (model i.val.1 i.val.2)) : degree Tot n ⟶ G where
  app B := (double B).totalDesc (c₁₂ := c)
    (fun p q h => (evalLift G p q (z ⟨(p,q),h⟩)).app B)
  naturality {B C} f := by
    apply HomologicalComplex₂.total.hom_ext
    intro p q h
    change (double B).ιTotal c p q n h ≫
        (HomologicalComplex₂.total.map (doubleF.map f) c).f n ≫
        (double C).totalDesc _ =
      (double B).ιTotal c p q n h ≫ (double B).totalDesc _ ≫ G.map f
    rw [← Category.assoc,HomologicalComplex₂.ιTotal_map,Category.assoc]
    change f.app (pair p q) ≫ (double C).ιTotal c p q n h ≫
        (double C).totalDesc (fun a b hab => (evalLift G a b (z ⟨(a,b),hab⟩)).app C) =
      (double B).ιTotal c p q n h ≫
        (double B).totalDesc (fun a b hab => (evalLift G a b (z ⟨(a,b),hab⟩)).app B) ≫ G.map f
    rw [HomologicalComplex₂.ι_totalDesc,← Category.assoc,HomologicalComplex₂.ι_totalDesc]
    exact (evalLift G p q (z ⟨(p,q),h⟩)).naturality f

set_option backward.isDefEq.respectTransparency false in
theorem totalLift_generator (G : Bi ⥤ ZMod) [G.Additive] (n : ℕ)
    (z : ∀ i : Split n, G.obj (model i.val.1 i.val.2)) (i : Split n) :
    (totalLift G n z).app _ (splitGenerator n i) = z i := by
  obtain ⟨⟨p,q⟩,h⟩ := i
  have he := HomologicalComplex₂.ι_totalDesc (K := double (model p q)) (c₁₂ := c)
    (f := fun a b hab => (evalLift G a b (z ⟨(a,b),hab⟩)).app (model p q)) p q h
  exact (CategoryTheory.congr_fun he (modelGenerator p q)).trans (evalLift_generator G p q _)

set_option backward.isDefEq.respectTransparency false in
theorem total_ext (G : Bi ⥤ ZMod) (n : ℕ)
    (f g : degree Tot n ⟶ G)
    (h : ∀ i : Split n, f.app _ (splitGenerator n i) = g.app _ (splitGenerator n i)) : f = g := by
  apply NatTrans.ext
  funext B
  apply HomologicalComplex₂.total.hom_ext
  intro p q hpq
  have he := eval_ext G p q (summandNat n p q hpq ≫ f) (summandNat n p q hpq ≫ g)
    (h ⟨(p,q),hpq⟩)
  exact congrArg (fun k => k.app B) he

#print axioms awNat
#print axioms evalLift_generator
#print axioms eval_ext
#print axioms totalLift_generator
#print axioms total_ext
end CMDG.CondensedCM5R0.EilenbergZilberNatural
