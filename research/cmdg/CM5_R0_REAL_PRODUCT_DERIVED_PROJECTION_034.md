# CM5 R0: canonical projection and the directed real-box system (034)

## Target and status

For a profinite S and an arbitrary index set I, let E be the topological
product of I copies of the reals, considered as a condensed set, and F
the actual free condensed module functor with the pinned lifted integer
coefficient ring. Write Z for the discrete integer module. The projection
induces a quasi-isomorphism

$$
R\mathrm{Hom}(F(S),Z)\longrightarrow
R\mathrm{Hom}(F(S\times E),Z).
$$

The proof below reconstructs this claim in source mathematics. The Lean
candidate handles the canonical degree-zero comparison and the actual
relative colimit; these declarations require exact-head native replay.
The all-degree categorical simplicial-replacement transport below is
not yet a kernel-checked theorem. No final CM5 unit or certification
claim is made.

## Degree zero and actual colimit

Let J be the coordinatewise partially ordered set of nonnegative
radius families, including the zero family. It is directed by
coordinatewise maximum and has a least object 0. Write B_r for the
product of the closed intervals from -r_i to r_i, X_r = S × B_r, and
A_r = F(X_r). Write A = F(S).

Every coordinate interval is nonempty and connected, hence so is the
product, even in arbitrary dimension. Under the actual free/Yoneda
adjunction Hom(A_r,Z) is the group of locally constant integer functions
on X_r. Restriction to each fiber over S is constant. Precomposition
with projection is therefore an additive isomorphism whose inverse is
restriction to the zero section. These isomorphisms commute with every
inclusion of boxes and with pullback along every map of probes.

The compact-test factorization of the protected
RealProductCompactExhaustion module bounds each coordinate of a map
from a compact Hausdorff T to E by its continuous-map sup norm. For a
map to S × E retain its S component and apply this factorization to the
second component. Two lifts with the same image coincide after
enlarging to their common coordinatewise maximum. Thus on every
compact test the relative box cocone is a filtered colimit of sets.
The inclusion of sheaves reflects this colimit; the actual free functor
is left adjoint and preserves it. The colimit of A_r is precisely
F(S × E), not the free group on the underlying points.

## All-degree transport: explicit simplicial replacement

Use the unnormalized ordered simplicial replacement of A_r:

$$
L_p=\bigoplus_{r_0\leq\cdots\leq r_p} A_{r_0}.
$$

The zeroth face applies the inclusion A_(r_0) → A_(r_1) and deletes
r_0; each other face deletes its radius and is the identity on the
coefficient. The alternating face sum is the boundary. At degree zero
the augmentation is the colimit cocone. The simplicial identities
follow from functoriality, including the identity arrows.

For any t in J restrict the strings to radii at most t. The analogous
augmentation is to A_t, and the augmented complex contracts by
appending t, with sign (-1)^(p+1) in degree p, and by the summand
inclusion A_t → L_0 in degree -1. For each summand all faces other
than the final deletion cancel against the homotopy of its boundary;
the final deletion is the identity. At degree zero the zeroth face
uses the inclusion into A_t, giving precisely the augmented identity.
Repeated indices are retained. Taking the filtered colimit over t
recovers L_p in each degree: each finite string already lies in its
last-radius subdiagram, with canonical coproduct inclusions.
The augmentations give colim A_t = F(S × E). The condensed module
category satisfies AB5 (pinned Mathlib Condensed/AB.lean); therefore
filtered colimits preserve this augmented exactness. This proves
that L resolves the genuine relative real product. No countability
or ordinary-limit exactness is assumed.

By protected PR 3819 every A_r is Ext-acyclic into Z in positive
degree, including the zero-radius stage, which is canonically A.
For an injective resolution J^q of Z, the Hom complex of each
coproduct L_p is the product over strings of Hom(A_(r_0),J^q).
Products of abelian groups are exact, so each L_p is Ext-acyclic,
with H^0 the product of the degree-zero Hom groups. This establishes
acyclicity of the resolution terms without claiming that they
are projective or that products of general condensed objects
are exact.

Now form the first-quadrant double complex Hom(L_p,J^q).
The horizontal-first comparison uses augmented exactness of L
and injectivity of every J^q; its total cohomology is the actual
RHom of the colimit. The vertical-first comparison uses the just
proved term acyclicity; it identifies the total cohomology with
the scalar cochain complex Hom(L_p,Z). In every total degree there
are finitely many bidegrees, so no unbounded totalization or
convergence assumption enters.

By the canonical degree-zero identifications, Hom(L_p,Z) is the
ordinary product of a single abelian group M = Hom(A,Z) over all
ordered strings of length p+1. Every face acts as identity on M;
the differential is the alternating deletion differential.
Prepending the least radius 0 contracts the augmented cochains:
for p ≥ 1 set

$$
(hc)(r_0,\ldots,r_{p-1})=c(0,r_0,\ldots,r_{p-1}).
$$

In degree zero use evaluation at 0. The first face of (0,r_0,...)
gives c itself and all subsequent terms cancel against d h. Thus
d h + h d = 1 in the augmented complex; it has H^0 = M and no
positive cohomology. The augmentation from M sends g to its
projection pullbacks at every box; hence the induced quasi-isomorphism
is exactly the projection, not just an abstract group isomorphism.

Equivalently the derived inverse limit of this coherent diagram of
derived Hom complexes is the constant complex M in degree zero.
We have established this by an explicit resolution rather than
assuming inverse limits commute with homology. It works for arbitrary
set-sized I and every profinite S, including empty S.

## Boundary

The next kernel obligation is the general categorical simplicial
replacement exactness, coproduct Ext calculation and acyclic-resolution
comparison (or an equivalent exact-colimit derived adjunction).
The source proof does not claim their formal implementation.
The comparison is on free modules F(S × E), not the abelian group
object E; transfer to a finite-type Breen--Deligne resolution and its
canonical unit remains separate. Circle-product continuity is not
established by this argument.
