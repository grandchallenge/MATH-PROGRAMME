import CMDGCondensedCM4P3DerivedCM5R0DiscreteProductSections
import CMDGCondensedCM4P3G

/-!
# CMDG CM5 — natural discrete-product Čech differential

The genuine categorical free-profinite Čech difference for the canonical Stonean
presentation is transported to the pointwise difference of locally constant
integer sections, coordinate by coordinate, including for infinite products.

All source and target morphisms are in the actual universe-lifted condensed
module category.  This does not identify G_S with an integer-coefficient
product or claim arbitrary kernel cochains are cocycles.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Genuine discrete coefficient evaluation commutes with
free-module precomposition by an arbitrary profinite morphism. -/
theorem freeProfiniteDiscreteIntegerHomScalarEquiv_precomp
    {X Y : Profinite.{u}} (q : X ⟶ Y)
    (g : ((Condensed.profiniteFree Coeff).obj Y) ⟶
      discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv X
      ((Condensed.profiniteFree Coeff).map q ≫ g) =
    (freeProfiniteDiscreteIntegerHomScalarEquiv Y g).comap q.hom.hom := by
  have h := CMDG.CondensedCM4P3G.lowerHomEquiv_precomp q g
  change freeProfiniteDiscreteIntegerHomEquiv X
      ((Condensed.profiniteFree Coeff).map q ≫ g) =
    (freeProfiniteDiscreteIntegerHomEquiv Y g).comap q.hom.hom at h
  change (freeProfiniteDiscreteIntegerHomEquiv X
      ((Condensed.profiniteFree Coeff).map q ≫ g)).map ULift.down =
    ((freeProfiniteDiscreteIntegerHomEquiv Y g).map ULift.down).comap q.hom.hom
  rw [h]
  rfl

/-- The true scalar coefficient Hom equivalence is additive and respects
subtraction of condensed-module morphisms. -/
theorem freeProfiniteDiscreteIntegerHomScalarEquiv_sub
    (X : Profinite.{u})
    (f g : ((Condensed.profiniteFree Coeff).obj X) ⟶
      discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv X (f - g) =
      freeProfiniteDiscreteIntegerHomScalarEquiv X f -
      freeProfiniteDiscreteIntegerHomScalarEquiv X g := by
  ext x
  rfl

/-- Natural in the actual profinite source, including when the
coefficient product is indexed by an infinite type. -/
theorem freeProfiniteDiscreteProductHomScalarEquiv_precomp
    {X Y : Profinite.{u}} (q : X ⟶ Y)
    {ι : Type (u + 1)}
    (g : ((Condensed.profiniteFree Coeff).obj Y) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    freeProfiniteDiscreteProductHomScalarEquiv X
      ((Condensed.profiniteFree Coeff).map q ≫ g) =
    fun i => (freeProfiniteDiscreteProductHomScalarEquiv Y g i).comap
      q.hom.hom := by
  funext i
  change freeProfiniteDiscreteIntegerHomScalarEquiv X
      (((Condensed.profiniteFree Coeff).map q ≫ g) ≫
        Pi.π (fun _ : ι => discreteIntegerCoeff) i) =
    (freeProfiniteDiscreteIntegerHomScalarEquiv Y
      (g ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)).comap
        q.hom.hom
  rw [Category.assoc]
  exact freeProfiniteDiscreteIntegerHomScalarEquiv_precomp q _

/-- The genuine product Hom-to-functions equivalence transports
categorical subtraction to coordinatewise subtraction. -/
theorem freeProfiniteDiscreteProductHomScalarEquiv_sub
    (X : Profinite.{u}) {ι : Type (u + 1)}
    (f g : ((Condensed.profiniteFree Coeff).obj X) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    freeProfiniteDiscreteProductHomScalarEquiv X (f - g) =
      fun i => freeProfiniteDiscreteProductHomScalarEquiv X f i -
        freeProfiniteDiscreteProductHomScalarEquiv X g i := by
  funext i
  change freeProfiniteDiscreteIntegerHomScalarEquiv X
      ((f - g) ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i) =
    freeProfiniteDiscreteIntegerHomScalarEquiv X
      (f ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i) -
    freeProfiniteDiscreteIntegerHomScalarEquiv X
      (g ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)
  rw [Preadditive.sub_comp]
  exact freeProfiniteDiscreteIntegerHomScalarEquiv_sub X _ _

/-- The concrete pointwise integral differential on the actual
categorical Stonean Čech pair, for arbitrary families of scalar sections. -/
noncomputable def stoneanDiscreteProductScalarCechDifference
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (b : ι → LocallyConstant
      (Stonean.toProfinite.obj T.presentation) ℤ) :
    ι → LocallyConstant (stoneanPresentationCechPairs T) ℤ :=
  fun i =>
    (b i).comap
      (pullback.fst (Profinite.presentation.π T)
        (Profinite.presentation.π T)).hom.hom -
    (b i).comap
      (pullback.snd (Profinite.presentation.π T)
        (Profinite.presentation.π T)).hom.hom

/-- **Exact categorical Čech differential comparison.**
For the actual free Stonean Čech difference, applied to an actual
morphism into a categorical product of discrete coefficient sheaves,
the resulting cochain is exactly pointwise subtraction of the source
scalar family evaluated on the two pullback endpoints. -/
theorem stoneanCechDifference_discreteProduct_scalar
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (g : ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanPresentationCechPairs T)
        (stoneanCechDifference T ≫ g) =
    stoneanDiscreteProductScalarCechDifference T
      (freeProfiniteDiscreteProductHomScalarEquiv
        (Stonean.toProfinite.obj T.presentation) g) := by
  unfold stoneanCechDifference stoneanDiscreteProductScalarCechDifference
  rw [Preadditive.sub_comp]
  rw [freeProfiniteDiscreteProductHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteProductHomScalarEquiv_precomp]
  rw [freeProfiniteDiscreteProductHomScalarEquiv_precomp]
  rfl

#print axioms freeProfiniteDiscreteIntegerHomScalarEquiv_precomp
#print axioms freeProfiniteDiscreteIntegerHomScalarEquiv_sub
#print axioms freeProfiniteDiscreteProductHomScalarEquiv_precomp
#print axioms freeProfiniteDiscreteProductHomScalarEquiv_sub
#print axioms stoneanCechDifference_discreteProduct_scalar

end CMDG.CondensedCM5R0
