import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntervalEndpoints

/-! Lift the interval chain filler to a simplicial morphism by
Dold–Kan, with exact endpoint identities. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneInterval
open CMDG.CondensedCM5R0.BreenDeligneIntervalFill
open CMDG.CondensedCM5R0.BreenDeligneIntervalEndpoints
namespace CMDG.CondensedCM5R0.BreenDeligneIntervalLift
abbrev DK := (CategoryTheory.Abelian.DoldKan.equivalence :
    SimplicialObject ZMod ≌ Ch)
abbrev N := normalizedMooreComplex ZMod
abbrev K := alternatingFaceMapComplex ZMod
abbrev incl (X : SimplicialObject ZMod) := inclusionOfMooreComplexMap X
abbrev proj (X : SimplicialObject ZMod) := AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex X
variable {X Y : SimplicialObject ZMod} {f g : X ⟶ Y}

def normFill (H : Homotopy (K.map f) (K.map g)) : N.obj (cyl X) ⟶ N.obj Y :=
  incl (cyl X) ≫ diagFill H ≫ proj Y

def cylinderMap (H : Homotopy (K.map f) (K.map g)) : cyl X ⟶ Y :=
  DK.functor.preimage (normFill H)

theorem cylinderMap_normalized (H : Homotopy (K.map f) (K.map g)) :
    N.map (cylinderMap H) = normFill H :=
  DK.functor.map_preimage _

set_option backward.isDefEq.respectTransparency false in
theorem cylinder_endpoint (H : Homotopy (K.map f) (K.map g)) (v : Fin 2) :
    endpoint X v ≫ cylinderMap H = if v=0 then f else g := by
  apply DK.functor.map_injective
  change N.map (endpoint X v ≫ cylinderMap H) = _
  rw [N.map_comp,cylinderMap_normalized,normFill,← Category.assoc,← Category.assoc]
  have hi := (inclusionOfMooreComplex ZMod).naturality (endpoint X v)
  change N.map (endpoint X v) ≫ incl (cyl X) = incl X ≫ K.map (endpoint X v) at hi
  rw [hi,Category.assoc (incl X),endpoint_fill]
  have he (k : X ⟶ Y) : incl X ≫ K.map k ≫ proj Y = N.map k := by
    have hn : K.map k ≫ proj Y = proj X ≫ N.map k :=
      AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex_naturality k
    rw [hn,← Category.assoc]
    have h := (AlgebraicTopology.DoldKan.splitMonoInclusionOfMooreComplexMap X).id
    change incl X ≫ proj X = 𝟙 _ at h
    rw [h,Category.id_comp]
  split_ifs with hv
  · exact he f
  · exact he g

#print axioms cylinderMap
#print axioms cylinder_endpoint
end CMDG.CondensedCM5R0.BreenDeligneIntervalLift
