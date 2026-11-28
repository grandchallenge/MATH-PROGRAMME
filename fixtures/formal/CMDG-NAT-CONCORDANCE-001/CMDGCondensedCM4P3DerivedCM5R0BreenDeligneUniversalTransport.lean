import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneProbeIndex

/-! Evaluation of a universal finite-type Breen--Deligne package.
The package existence theorem is separate; its natural exact
resolution data is transported by actual evaluation, probe indexing
and exact sheafification, not replaced by a hypothetical resolution. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
open scoped ZeroObject
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection AcyclicResolution

def tupleSet {k : ℕ} (arity : Fin k → ℕ) : Mod.{u} ⥤ Type (u+1) where
  obj M := Σ j : Fin k, (Fin (arity j) → M)
  map f := ↾fun z => ⟨z.1,fun a => f (z.2 a)⟩
  map_id M := by
    apply ConcreteCategory.hom_ext
    rintro ⟨j,x⟩
    rfl
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    rintro ⟨j,x⟩
    rfl

abbrev polynomial {k : ℕ} (arity : Fin k → ℕ) : Mod.{u} ⥤ Mod.{u} :=
  tupleSet arity ⋙ ModuleCat.free Coeff.{u}

structure UniversalBD where
  count : ℕ → ℕ
  arity : ∀ n, Fin (count n) → ℕ
  aug : polynomial (arity 0) ⟶ 𝟭 Mod.{u}
  d : ∀ n, polynomial (arity (n+1)) ⟶ polynomial (arity n)
  aug_zero : d 0 ≫ aug = 0
  sq_zero : ∀ n, d (n+1) ≫ d n = 0
  aug_epi : Epi aug
  aug_exact : (ShortComplex.mk (d 0) aug aug_zero).Exact
  exact : ∀ n, (ShortComplex.mk (d (n+1)) (d n) (sq_zero n)).Exact

abbrev transport (P : SetPsh.{u}) (A : Psh.{u}) :
    (Mod.{u} ⥤ Mod.{u}) ⥤ Ambient.{u} :=
  (Functor.whiskeringLeft _ _ _).obj A ⋙ indexedFunctor P ⋙ moduleSheafification

theorem transport_exact (P : SetPsh.{u}) (A : Psh.{u})
    (Q : ShortComplex (Mod.{u} ⥤ Mod.{u})) (h : Q.Exact) :
    (Q.map (transport P A)).Exact := by
  let W := (Functor.whiskeringLeft CompHaus.{u}ᵒᵖ Mod.{u} Mod.{u}).obj A
  have hw : (Q.map W).Exact := by
    apply functorShortComplex_exact_of_pointwise
    intro T
    exact h.map ((evaluation Mod.{u} Mod.{u}).obj (A.obj T))
  have hi := indexedFunctor_exact P _ hw
  have hs := moduleSheafification_preservesExact _ hi
  simpa only [transport,ShortComplex.map_comp] using hs

theorem transport_epi (P : SetPsh.{u}) (A : Psh.{u}) {X Y : Mod.{u} ⥤ Mod.{u}}
    (f : X ⟶ Y) [Epi f] : Epi ((transport P A).map f) := by
  let W := (Functor.whiskeringLeft CompHaus.{u}ᵒᵖ Mod.{u} Mod.{u}).obj A
  haveI : Epi (W.map f) := by
    apply (NatTrans.epi_iff_epi_app _).2
    intro T
    exact (NatTrans.epi_iff_epi_app f).1 inferInstance (A.obj T)
  haveI := indexedFunctor_epi P (W.map f)
  exact moduleSheafification.map_epi _

def transportedResolution (B : UniversalBD.{u}) (P : SetPsh.{u}) (A : Psh.{u}) :
    Resolution.{u} where
  target := (transport P A).obj (𝟭 Mod.{u})
  term n := (transport P A).obj (polynomial (B.arity n))
  aug := (transport P A).map B.aug
  d n := (transport P A).map (B.d n)
  aug_zero := by rw [← Functor.map_comp,B.aug_zero,Functor.map_zero]
  sq_zero n := by rw [← Functor.map_comp,B.sq_zero,Functor.map_zero]
  aug_epi := by
    letI := B.aug_epi
    exact transport_epi P A B.aug
  aug_exact := transport_exact P A _ B.aug_exact
  exact n := transport_exact P A _ (B.exact n)

abbrev zeroPsh : Psh.{u} := (Functor.const CompHaus.{u}ᵒᵖ).obj (0 : Mod.{u})

def pZero (A : Psh.{u}) : A ⟶ zeroPsh := 0
def sZero (A : Psh.{u}) : zeroPsh ⟶ A := 0

theorem zeroPsh_id : 𝟙 (zeroPsh.{u}) = 0 := by
  apply NatTrans.ext
  funext T
  change 𝟙 (0 : Mod.{u}) = 0
  exact (isZero_zero Mod.{u}).eq_of_src _ _

theorem sZero_pZero (A : Psh.{u}) : sZero A ≫ pZero A = 𝟙 _ := by
  rw [sZero,zero_comp,zeroPsh_id]

abbrev relativeSheafify (P : SetPsh.{u}) : Psh.{u} ⥤ Ambient.{u} :=
  indexedFunctor P ⋙ moduleSheafification

def changeInput (P : SetPsh.{u}) {A Z : Psh.{u}} (f : A ⟶ Z)
    (F : Mod.{u} ⥤ Mod.{u}) :
    (transport P A).obj F ⟶ (transport P Z).obj F :=
  (relativeSheafify P).map (Functor.whiskerRight f F)

theorem changeInput_comp (P : SetPsh.{u}) {A Z K : Psh.{u}}
    (f : A ⟶ Z) (g : Z ⟶ K) (F : Mod.{u} ⥤ Mod.{u}) :
    changeInput P f F ≫ changeInput P g F = changeInput P (f ≫ g) F := by
  unfold changeInput
  rw [← Functor.map_comp]
  congr 1
  apply NatTrans.ext
  funext T
  exact (F.map_comp (f.app T) (g.app T)).symm

theorem changeInput_id (P : SetPsh.{u}) (A : Psh.{u}) (F : Mod.{u} ⥤ Mod.{u}) :
    changeInput P (𝟙 A) F = 𝟙 _ := by
  unfold changeInput
  have h : Functor.whiskerRight (𝟙 A) F = 𝟙 _ := by
    apply NatTrans.ext
    funext T
    exact F.map_id _
  rw [h]
  exact (relativeSheafify P).map_id _

theorem changeInput_natural (P : SetPsh.{u}) {A Z : Psh.{u}} (f : A ⟶ Z)
    {F G : Mod.{u} ⥤ Mod.{u}} (g : F ⟶ G) :
    (transport P A).map g ≫ changeInput P f G =
      changeInput P f F ≫ (transport P Z).map g := by
  change (relativeSheafify P).map (Functor.whiskerLeft A g) ≫
    (relativeSheafify P).map (Functor.whiskerRight f G) =
      (relativeSheafify P).map (Functor.whiskerRight f F) ≫
        (relativeSheafify P).map (Functor.whiskerLeft Z g)
  rw [← Functor.map_comp,← Functor.map_comp]
  congr 1
  apply NatTrans.ext
  funext T
  exact (g.naturality (f.app T)).symm

theorem changeInput_zero_identity (P : SetPsh.{u}) (A : Psh.{u}) :
    changeInput P (sZero A) (𝟭 Mod.{u}) = 0 := by
  unfold changeInput
  have h : Functor.whiskerRight (sZero A) (𝟭 Mod.{u}) = 0 := by
    apply NatTrans.ext
    funext T
    rfl
  rw [h,Functor.map_zero]

def transportedZeroSplit (B : UniversalBD.{u}) (P : SetPsh.{u}) (A : Psh.{u}) :
    SplitResolution (transportedResolution B P A) where
  base n := (transport P zeroPsh).obj (polynomial (B.arity n))
  p n := changeInput P (pZero A) _
  s n := changeInput P (sZero A) _
  split n := by rw [changeInput_comp,sZero_pZero,changeInput_id]
  d n := (transport P zeroPsh).map (B.d n)
  p_chain n := changeInput_natural P (pZero A) (B.d n)
  s_chain n := changeInput_natural P (sZero A) (B.d n)
  s_aug := by
    change changeInput P (sZero A) _ ≫ (transport P A).map B.aug = 0
    rw [← changeInput_natural,changeInput_zero_identity,comp_zero]

#print axioms transportedResolution
#print axioms transportedZeroSplit
end CMDG.CondensedCM5R0.BreenDeligneProbe
