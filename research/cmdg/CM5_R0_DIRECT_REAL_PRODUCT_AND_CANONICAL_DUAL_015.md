# CM5-R0: direct real-product calculation and canonical duality (015)

Status: source-relative mathematical reconstruction; compact-exhaustion Lean
module checked locally; full analytic/derived realization in pinned Lean
remains open. No MATHCERT certification. Source: Peter Scholze, Lectures on
Condensed Mathematics, May 2026, https://arxiv.org/abs/2605.03658
(Theorems 3.2, 3.3, 4.5; Corollary 4.8; Proposition 4.17; Theorem 4.3 as
cross-check). Fix the cardinal/universe regime in which the relevant boxes
belong to the site.

## Direct real-product calculation

Write E=R^I, K=(R/Z)^I, B=Z^I, A=direct_sum_I Z, all condensed.
D denotes derived INTERNAL Hom into the discrete coefficient Z.
For b:I->R_{>=0}, set Q_b=product_i[-b_i,b_i]. The boxes are compact
Hausdorff and directed by coordinatewise maximum. On any compact probe P,
every continuous f:P->E lands in Q_b for b_i=sup_{p in P}|f_i(p)|.
Use zero radii for empty P. Inclusions are injective; two factorizations
agree in a common larger box. This proves a filtered-colimit identity of
condensed sets on probes, not a countable exhaustion or uniform bound over I.
The same holds for E^r using I times Fin r.
For a Stonean probe S, Q_b x S is compact, and the homotopy
(t,x,s)->(tx,s) fixes S and commutes with all box inclusions.

Free condensed abelian groups preserve this colimit, and AB5 identifies
ordinary filtered colimits with derived colimits of degree-zero objects.
Derived mapping-out into Z takes the colimit to the derived inverse limit.
On Q_b x S, zero-section pullback identifies condensed cohomology with that
of S by the compact Hausdorff comparison (Theorem 3.2) and homotopy invariance
of Cech cohomology with constant coefficients. These natural maps are
quasi-isomorphisms of RΓ, not abstract group isomorphisms. The resulting
diagram is equivalent to the constant diagram RΓ(S,Z). The nonempty directed
index has contractible nerve, so its derived limit is RΓ(S,Z), even for
uncountable I. No general vanishing of higher derived limits is presumed.
Thus zero-section pullback RΓ(E^r x S,Z)->RΓ(S,Z) is invertible.

Apply the functorial finite-type Breen–Deligne resolution (Theorem 4.5)
and first-quadrant mapping-out spectral sequence (Corollary 4.8) to
0->E. Every E1 term is the zero-section isomorphism just proved for
each finite arity and Stonean probe. Comparison in every total degree
yields D(E)->D(0)=0 an equivalence. This avoids the derived real
scalar adjunction.

## Circle calculation and actual connecting morphisms

For one circle the real/integer/circle exact sequence and D(R)=0
make its canonical boundary D(Z)[-1]->D(T) invertible. For finite J,
the direct sum of these boundaries is invertible. For general I,
the inverse system K_J of finite products has surjective projections.
For finite r and compact S, K_I^r x S=lim_J K_J^r x S. Cech continuity
and compact comparison give the filtered-colimit isomorphism on every
cohomology group, via the actual pullbacks. Finite-type BD and exactness
of filtered colimits give first-quadrant spectral sequence comparison
in every total degree. The canonical sum of pullbacks of single-circle
boundaries A[-1]->D(K) is therefore an equivalence.

The genuine exact sequence 0->B->E->K->0 (PR #3643) and coordinate
naturality (#3647) give the actual map c:D(B)->D(K)[1], invertible
since D(E)=0. Naturality sends each coordinate pi_i:B->Z in degree
zero under c to the pullback of the corresponding single-circle
boundary, with the same triangle convention. Consequently the
canonical evaluation kappa:A->D(B) satisfies c kappa = the sum of
those boundaries shifted by one. Both c and that sum are invertible,
so kappa is invertible. This proves D(B)=A[0] and positive Ext
vanishing into Z. No unnamed isomorphism is substituted for kappa.

For real coefficients on K, separately use Theorem 3.3 to identify the
BD mapping-out complex with finite sums of compact-continuous real cochains.
On finite free integer modules BD terms are finite sums of representables.
The natural chain homotopy between two lifts of doubling (Proposition 4.17)
has components given by finite integer combinations of matrix maps by Yoneda.
Their dual maps are bounded by sums of absolute coefficients, using the
compact pullback norm lemma. The geometric-series contraction of
reconstruction 014 applies on each Stonean probe. This gives RHom(K,R)=0,
source-relative to BD and cohomology comparison; it is distinct from D(E)=0.

## Canonical unit and solid-source comparison

Let F_X=Z[X], G_X=Z[X]^solid for profinite X. For every Stonean S,
D(F_X)(S)=RΓ(X x S,Z), concentrated in zero by compact cohomology
comparison. Compactness and finite clopen rectangles identify locally
constant functions on X x S with locally constant S-families of
locally constant X-functions. Thus D(F_X) is the discrete module
C(X,Z), free by Nöbeling. Its dual is the product of Z, using exact
products. The protected gsFreeSolidToCoefficientProductIso realizes
the genuine G_X as this product with the original enriched coordinates.

In the source model G_X is the measure dual of C(X,Z).
The canonical unit on a generator x is the evaluation f->f(x).
Double-dual evaluation eta_{F_X} has exactly those same components.
Apply the free-object adjunction and compare the sections over X
in every coefficient coordinate: both are the corresponding locally
constant basis function on X. This identifies theta_X u_X=eta_{F_X}
in the source category, where theta_X is the measure-dual identification
with D^2(F_X). The duality triangle identity
D(eta_Y) eta_{D(Y)}=id and kappa imply that D(u_X) is invertible.
Since G_Y is a genuine product of discrete coefficients, derived
internal Hom into G_Y is the product of derived internal Homs into Z
(the derived right adjoint preserves products, and AB4* identifies the
degree-zero target product). Thus RHom(G_X,G_Y)->RHom(F_X,G_Y) induced
by the actual unit is invertible, and Ext^q(G_X,G_Y)=0 for q>0.
Point-probe evaluation is exact. Equivalently, the already-proved
degree-zero and positive-source-shift comparison and the positive
Ext vanishing close the shiftedComparisonCandidate_iff_genuineSolidSourceExtZero
criterion. This is the source-category mathematical argument, not a
Lean verification of those analytic comparisons.

## Evidence and remaining formal work

The compact-exhaustion Lean module proves compactness, factorization,
injectivity, directedness, lifted factorization, contraction naturality,
and probe-relative contraction. Lean v4.33.0-rc1; Mathlib
79d0395a1825a6264ad5d269e35e60537518955e. Source SHA256
b5e7b1ae5ce38b48e0321ac4efe28863d8debcb3af0cd95eb12afda61560f94d.
Local check is not independent attestation. The actual lifted basis index
is small by injection through basis.injective and the inverse integral
locally constant semilinear equivalence; this lemma elaborated, but
the categorical product-cone transport has not passed a complete replay.
Remaining Lean obligations: the small-index product transport and
identification of the exact Stonean topological-product construction
with the coefficient sheaves; actual condensed filtered colimit and
derived RΓ compact comparison, Cech continuity and BD spectral sequence;
actual derived internal Hom/evaluation or the all-shifts Ext criterion;
affected formal replay and protected admission. No new Lean axioms,
assumed analytic equivalences, or MATHCERT promotion.
