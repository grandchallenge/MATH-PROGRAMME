import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCechModules

/-! Polynomial functors preserve the genuine set-valued Čech
relations, including the finite-coproduct tag. Transport the
already-proved split free Čech contraction through this equivalence. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
open BreenDeligneProbe
variable {M N : Mod.{u}} (p : M ⟶ N) {k : ℕ} (a : Fin k → ℕ)

abbrev Tup (A : Mod.{u}) := (tupleSet a).obj A
abbrev tp : Tup a M → Tup a N := (tupleSet a).map p
abbrev tupleRel (n : ℕ) := splitCechTuple (Tup a M) (Tup a N) (tp p a) n

def packTuple (n : ℕ) (x : Tup a (rel p n)) : tupleRel p a n :=
  ⟨fun i => ⟨x.1,fun j => (x.2 j).val i⟩,by
    intro i
    apply Sigma.ext
    · rfl
    · apply heq_of_eq
      funext j
      exact (x.2 j).property i⟩

theorem packTuple_injective (n : ℕ) : Function.Injective (packTuple p a n) := by
  rintro ⟨j,x⟩ ⟨l,y⟩ h
  have he := congrArg (fun t : tupleRel p a n => (t.val 0).1) h
  change j=l at he
  subst l
  apply Sigma.ext
  · rfl
  · apply heq_of_eq
    funext i
    apply Subtype.ext
    funext t
    have ht := congrArg (fun z : tupleRel p a n => z.val t) h
    change (⟨j,fun i => (x i).val t⟩ : Tup a M) = ⟨j,fun i => (y i).val t⟩ at ht
    exact congrFun (Sigma.mk.inj ht).2.eq i

def tagEq (n : ℕ) (x : tupleRel p a n) (i : Fin (n+1)) :
    (x.val i).1 = (x.val 0).1 :=
  congrArg (fun t : Tup a N => t.1) (x.property i)

def tagTuple (n : ℕ) (x : tupleRel p a n) (i : Fin (n+1)) :
    Fin (a (x.val 0).1) → M :=
  cast (congrArg (fun j => Fin (a j) → M) (tagEq p a n x i)) (x.val i).2

theorem tagTuple_spec (n : ℕ) (x : tupleRel p a n) (i : Fin (n+1)) :
    (⟨(x.val 0).1,tagTuple p a n x i⟩ : Tup a M) = x.val i := by
  have helper (t : Tup a M) (j : Fin k) (h : t.1 = j) :
      (⟨j,cast (congrArg (fun j => Fin (a j) → M) h) t.2⟩ : Tup a M) = t := by
    rcases t with ⟨l,z⟩
    change l=j at h
    subst j
    rfl
  exact helper (x.val i) (x.val 0).1 (tagEq p a n x i)

theorem tagTuple_image (n : ℕ) (x : tupleRel p a n)
    (i : Fin (n+1)) (j : Fin (a (x.val 0).1)) :
    p (tagTuple p a n x i j) = p (tagTuple p a n x 0 j) := by
  have h := (congrArg (tp p a) (tagTuple_spec p a n x i)).trans
    ((x.property i).trans (congrArg (tp p a) (tagTuple_spec p a n x 0)).symm)
  change (⟨(x.val 0).1,fun j => p (tagTuple p a n x i j)⟩ : Tup a N) =
    ⟨(x.val 0).1,fun j => p (tagTuple p a n x 0 j)⟩ at h
  exact congrFun (Sigma.mk.inj h).2.eq j

theorem packTuple_surjective (n : ℕ) : Function.Surjective (packTuple p a n) := by
  intro x
  refine ⟨⟨(x.val 0).1,fun j => ⟨fun i => tagTuple p a n x i j,
    fun i => tagTuple_image p a n x i j⟩⟩,?_⟩
  apply Subtype.ext
  funext i
  exact tagTuple_spec p a n x i

def packEquiv (n : ℕ) : Tup a (rel p n) ≃ tupleRel p a n :=
  Equiv.ofBijective (packTuple p a n) ⟨packTuple_injective p a n,packTuple_surjective p a n⟩

theorem pack_face (n : ℕ) (i : Fin (n+2)) :
    ((tupleSet a).map (relFace p n i)) ≫ (↾packTuple p a n) =
      (↾packTuple p a (n+1)) ≫ (↾splitCechFace (Tup a M) (Tup a N) (tp p a) n i) := by
  apply ConcreteCategory.hom_ext
  intro x
  apply Subtype.ext
  rfl

theorem pack_aug :
    (↾packTuple p a 0) ≫ (↾splitCechBaseProjection (Tup a M) (Tup a N) (tp p a)) =
      (tupleSet a).map (relAug p) := by
  apply ConcreteCategory.hom_ext
  intro x
  rfl

def packIso (n : ℕ) :
    (polynomial a).obj (rel p n) ≅ (ModuleCat.free Coeff).obj (tupleRel p a n) :=
  (ModuleCat.free Coeff).mapIso (Equiv.toIso (packEquiv p a n))

def polyD (n : ℕ) : (polynomial a).obj (rel p (n+1)) ⟶ (polynomial a).obj (rel p n) :=
  ∑ i : Fin (n+2), (-1 : ℤ)^i.val • (polynomial a).map (relFace p n i)

theorem polyD_pack (n : ℕ) :
    polyD p a n ≫ (packIso p a n).hom =
      (packIso p a (n+1)).hom ≫ splitBarD (Tup a M) (Tup a N) (tp p a) n := by
  unfold polyD splitBarD
  rw [Preadditive.sum_comp,Preadditive.comp_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [Preadditive.zsmul_comp,Preadditive.comp_zsmul]
  congr 1
  change (ModuleCat.free Coeff).map ((tupleSet a).map (relFace p n i)) ≫
    (ModuleCat.free Coeff).map (↾packTuple p a n) =
    (ModuleCat.free Coeff).map (↾packTuple p a (n+1)) ≫
      (ModuleCat.free Coeff).map (↾splitCechFace (Tup a M) (Tup a N) (tp p a) n i)
  rw [← Functor.map_comp,← Functor.map_comp,pack_face]

theorem polyAug_pack :
    (packIso p a 0).hom ≫ splitBarBaseMap (Tup a M) (Tup a N) (tp p a) =
      (polynomial a).map (relAug p) := by
  change (ModuleCat.free Coeff).map (↾packTuple p a 0) ≫
    (ModuleCat.free Coeff).map (↾splitCechBaseProjection (Tup a M) (Tup a N) (tp p a)) = _
  rw [← Functor.map_comp,pack_aug]
  rfl

theorem polyD_sq (n : ℕ) : polyD p a (n+1) ≫ polyD p a n = 0 := by
  apply (cancel_mono (packIso p a n).hom).1
  rw [Category.assoc,polyD_pack,← Category.assoc,polyD_pack,Category.assoc,
    splitBarD_comp_D_zero,comp_zero,zero_comp]

theorem polyD_aug : polyD p a 0 ≫ (polynomial a).map (relAug p) = 0 := by
  rw [← polyAug_pack,← Category.assoc,polyD_pack,Category.assoc,
    splitBarZeroBoundary_comp_augmentation,comp_zero]

theorem tuple_surj (hp : Function.Surjective p) : Function.Surjective (tp p a) := by
  rintro ⟨j,x⟩
  choose y hy using fun i => hp (x i)
  refine ⟨⟨j,y⟩,?_⟩
  apply Sigma.ext
  · rfl
  · exact heq_of_eq (funext hy)

theorem polyAug_surj (hp : Function.Surjective p) :
    Function.Surjective ((polynomial a).map (relAug p)) := by
  have h := tuple_surj (relAug p) a (relAug_surj p hp)
  obtain ⟨s,hs⟩ := h.hasRightInverse
  have hsplit : (ModuleCat.free Coeff).map (↾s) ≫ (polynomial a).map (relAug p) = 𝟙 _ := by
    change (ModuleCat.free Coeff).map (↾s) ≫ (ModuleCat.free Coeff).map ((tupleSet a).map (relAug p)) = _
    rw [← Functor.map_comp]
    have hh : (↾s) ≫ (tupleSet a).map (relAug p) = 𝟙 _ := by
      apply ConcreteCategory.hom_ext
      exact hs
    rw [hh]
    exact (ModuleCat.free Coeff).map_id _
  intro x
  exact ⟨(ModuleCat.free Coeff).map (↾s) x,CategoryTheory.congr_fun hsplit x⟩

theorem poly_exact (hp : Function.Surjective p) (n : ℕ) :
    (ShortComplex.mk (polyD p a (n+1)) (polyD p a n) (polyD_sq p a n)).Exact := by
  obtain ⟨s,hs⟩ := (tuple_surj p a hp).hasRightInverse
  let Q := splitBarShortComplex (Tup a M) (Tup a N) (tp p a) n
  have iso : (ShortComplex.mk (polyD p a (n+1)) (polyD p a n) (polyD_sq p a n)) ≅ Q :=
    ShortComplex.isoMk (packIso p a (n+2)) (packIso p a (n+1)) (packIso p a n)
      (polyD_pack p a (n+1)).symm (polyD_pack p a n).symm
  exact ShortComplex.exact_of_iso iso.symm (splitBarShortComplex_exact _ _ _ s hs n)

theorem poly_zero_exact (hp : Function.Surjective p) :
    (ShortComplex.mk (polyD p a 0) ((polynomial a).map (relAug p)) (polyD_aug p a)).Exact := by
  obtain ⟨s,hs⟩ := (tuple_surj p a hp).hasRightInverse
  let Q := splitBarZeroShortComplex (Tup a M) (Tup a N) (tp p a)
  have iso : (ShortComplex.mk (polyD p a 0) ((polynomial a).map (relAug p)) (polyD_aug p a)) ≅ Q :=
    ShortComplex.isoMk (packIso p a 1) (packIso p a 0) (Iso.refl _)
      (polyD_pack p a 0).symm (polyAug_pack p a)
  exact ShortComplex.exact_of_iso iso.symm (splitBarZeroShortExact _ _ _ s hs)

#print axioms poly_exact
#print axioms poly_zero_exact
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
