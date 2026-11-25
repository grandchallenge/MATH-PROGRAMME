# CM5 R0: Eilenberg–Zilber and stable suspension

## Evidence separation

The companion Lean modules verify Alexander–Whitney (AW) and its chain
law and naturality, the signed shuffle degree maps, the horizontal group-bar
Moore calculation, the free representable diagonal contraction and cycle
filling, universal evaluation and total-summand extension, and the natural
diagonal homotopy construction. The following source-level mathematical
argument supplies the remaining comparison. The shuffle chain law, total-model
contraction and second homotopy, and application to the normalized columns
and next Dold–Kan stage are not yet kernel-checked. No CM5 closure is asserted.

## Raw comparison

For a bisimplicial integer module B use total differential horizontal plus
(-1)^p times vertical in bidegree (p,q). Diagonal chains use alternating
simultaneous faces. AW in degree n sums over cuts p+q=n, restricting the first
ordinal to vertices 0 through p and the second to vertices p through n.
For source degree n+1 and target cut (p,q), simultaneous faces deleting a vertex
i at most p give the horizontal faces of (p+1,q) other than its last face.
The rest give the vertical faces of (p,q+1) other than its first face.
The omitted terms have identical ordinal maps and opposite signs
(-1)^(p+1) and (-1)^p. This proves the chain law, verified in Lean.

Shuffle sums over monotone paths from (0,0) to (p,q), with H and V unit
steps. Each path gives two ordinal maps alpha and beta; its pullback is
weighted by (-1)^inv, counting V-before-H pairs. The rank condition
alpha(k)+beta(k)=k forces these steps and endpoints. The Lean pathSign
sums the vertical coordinate preceding each H step, exactly this count.

To compute the shuffle differential delete vertex k of a path. Interior
deletions between HV or VH cancel in pairs: swapping those steps preserves
the maps after deletion and changes the inversion count by one.
Other interior deletions merge HH or VV; endpoint deletions remove the
adjacent step. Horizontal deletions correspond bijectively to a path of
type (p-1,q) and horizontal face index i in [0,p]. Relabel the remaining
horizontal coordinates in increasing order. Conversely split the unique H
step crossing the omitted coordinate, or prepend/append H for an endpoint.
The deleted vertex (i,j) has k=i+j. The removed H contributes j inversions,
so the coefficient is (-1)^(i+inv(shorter path)). Vertical deletion removes
a V contributing p-i inversions, hence coefficient (-1)^(p+j+inv(shorter
path)). This is precisely the signed total differential followed by
shuffle. If either degree is zero only the other axis contributes.
Naturality follows from naturality of each ordinal pullback.

## Both homotopies

The free bisimplicial representable R^(a,b) has in bidegree (p,q) the free
group on pairs of ordinal maps [p] -> [a], [q] -> [b]. Its identity-pair
generator e is universal: any x in B_(a,b) gives a unique linear natural
map R -> B taking each pair to its pullback of x. This map is additive in x.

On diagonal chains of R, prepend initial vertex (0,0). The face deleting
it is the identity; other faces commute with insertion with index reduced
by one. Thus dh+hd=id-P, with P augmentation followed by initial vertex
section (zero in positive degrees). This contraction is verified in Lean.

The total model is the tensor product of the two free unnormalized standard
simplex complexes. Let their contractions be h_a,h_b and projections
P_a,P_b. For x homogeneous of degree p set

    H(x tensor y) = h_a(x) tensor y + (-1)^p P_a(x) tensor h_b(y).

Expanding dH+Hd cancels the mixed differential terms by the Koszul sign.
The remaining sum is (id-P_a) tensor id + P_a tensor (id-P_b), which is
id-P_a tensor P_b. Hence both models have explicit positive-degree fillers.

For natural chain maps u,v from diagonal or total to either functor,
agreeing in degree zero, set K_0=0. In degree n>0, use the universal
generator e of the model corresponding to (n,n), or the generator of
each total summand (p,q) with p+q=n. Form

    z = (u_n-v_n)(e) - K_(n-1)(d e).

The chain law, prior homotopy identity and d squared zero give dz=0.
Set K_n(e)=h_model(z) and extend via universal evaluation and coproduct
extension. This is linear and natural and gives dK+Kd=u-v by evaluation
on generators. Both AW-shuffle composites agree with the respective
identity in degree zero (one cut and the empty path). Applying this
construction proves both chain homotopies mathematically. Lean now
verifies the universal extension and the diagonal-to-diagonal construction,
including the actual Homotopy object, not yet the total-side construction.

## Actual columns and stable range

Normalization has its natural inclusion and projection, a chain homotopy
equivalence with alternating chains. Apply it in one direction of a
bisimplicial module. Filtering the first-quadrant total by the other
degree gives shifted normalization equivalences on associated graded
complexes. The long exact sequence and finite filtration in each degree
give a total quasi-isomorphism. Repeat for the other direction if needed.

For the protected actual reduced bar, the positive horizontal column p
is the alternating chain complex of the pointwise p-fold tensor power
of the reduced free simplicial module. Apply the binary comparison to
the external tensor bisimplicial module and iterate. Tensoring a chain
homotopy equivalence preserves it: tensor its homotopies with identity,
using the Koszul sign for homotopies in the second factor. The resulting
tensor powers agree by associativity and unit with those in the protected
support theorem. Thus, for input Gamma(A[n]), the p-shifted actual column
has vanishing homology in total degree j<p(n+1). For p at least two,
this is vanishing below 2n+2.

Filter the horizontally normalized, vertically alternating bar total
by horizontal degree. The reduced zero column is zero; F_1 is the actual
first-column suspension, and F_p/F_(p-1) is the p-shifted vertical
column with signed differential. For p at least two the quotient homology
vanishes in degrees j and j+1 if j<2n+1. The long exact sequence shows
that the actual inclusion F_1 -> Tot is a homology isomorphism in that
range (surjective at j=2n+1). For fixed j only finitely many horizontal
degrees contribute to adjacent total chain degrees, so no infinite
filtration convergence assumption is required.

## Comparison with the next Dold–Kan object

Apply the reduced-free comparison to the actual bisimplicial group bar
after applying reduced free abelian groups degreewise. It identifies its
total homology with the reduced chain homology of its diagonal.

Separately apply the raw comparison to the bisimplicial abelian group
itself, before applying the reduced free functor. Its horizontal Moore
complex is naturally the input group in degree one. Degree zero is trivial;
degree one is evaluation at the single coordinate; every higher tuple is
a sum of single-coordinate tuples, all degenerate, killed by normalization.
This exact natural isomorphism is verified in BarGroupMoore.

The normalized chains of the diagonal group bar are therefore
quasi-isomorphic to the suspension of the normalized chains of the input:
use the normalized inclusion into alternating diagonal chains, AW, and
normalization projections in both directions. For X=Gamma(A[n]) the
Dold–Kan unit and counit identify the suspended complex with A[n+1]
(up to the chain suspension sign convention). Under Dold–Kan the
comparison corresponds to a natural simplicial abelian group map
from the diagonal bar of X to Gamma(A[n+1]). The identification of
simplicial abelian homotopy groups with Moore homology shows that the map
is a weak equivalence of underlying simplicial sets. Weak-equivalence
invariance of reduced integral homology identifies the reduced chain
homology of the diagonal with that of the next actual Dold–Kan object.
This is a weak-equivalence comparison, not a strict simplicial isomorphism.

The composite of the actual first-column inclusion with these comparisons
gives the suspension homology isomorphism in degree n+r+1 for 0<=r<n.
This source proof uses standard normalization, Dold–Kan, and weak-equivalence
invariance results; the corresponding Lean interfaces and application
remain to be verified.

## Exact remaining formal obligation

Prove the signed-shuffle differential and naturality for the constructed
degree maps; identify degree-zero composites; instantiate the verified
diagonal homotopy; construct the total-model contraction and total-side
homotopy; bind the resulting equivalence to the actual normalized bar
columns, filtration and Dold–Kan weak equivalence. Do not claim the final
suspension theorem, pseudocoherence or CM5 closure as kernel-checked.
