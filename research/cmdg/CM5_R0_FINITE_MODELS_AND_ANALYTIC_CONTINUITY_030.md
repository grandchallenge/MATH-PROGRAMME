# CM5 R0: finite models and analytic continuity

## Rank-one base in the actual model

The protected groupMooreIso identifies the Moore complex of the
additive bar with the single degree-one complex. Dold--Kan gives a
simplicial isomorphism of bar Z with em 1 at Z. Its simplices are
the successive integer edge differences of vertex tuples.

Put R=Z[t,t^{-1}]. The two-term free augmented resolution P is

$$
0\to R\xrightarrow{t-1}R\xrightarrow{\epsilon}\mathbb Z\to0.
$$

Multiplication by t-1 is injective in this domain. Every Laurent
polynomial of augmentation zero is a finite sum of a_m(t^m-1),
divisible by t-1 even for negative m.

Let Q_n be the free abelian group on integer vertex tuples, with
R-action simultaneous translation and alternating vertex deletion.
It is R-free on tuples anchored at first vertex zero. Prepending
vertex zero gives a nonequivariant augmented contraction s; Q is exact.
Define R-linear chain maps i:P->Q and p:Q->P by

$$
i_0(1)=(0),\qquad i_1(1)=(0,1),
$$

$$
p_0((a))=t^a,\qquad p_1((a,b))=\frac{t^b-t^a}{t-1},
\qquad p_n=0\ (n\ge2).
$$

The quotient is Laurent polynomial. Triangle edge differences
telescope, proving the degree-two chain identity; p i is identity.
Recursively define on anchored free generators b

$$
h_n(b)=s((1-ip)b-h_{n-1}db),\qquad h_{-1}=0.
$$

The argument of s is a cycle (at zero, of augmentation zero) by
the previous homotopy identity. Thus d h_n(b) is that argument.
Extend by R-linearity. This yields an equivariant homotopy without
asserting that s is equivariant.

Coinvariants preserve homotopy equivalence. A vertex tuple orbit is
specified by its edge differences, so the coinvariant Q is the actual
unreduced bar complex. The coinvariant differential of P is zero.
Removing the split constant basepoint chains gives reduced homology
Z in degree one and zero otherwise, with degree-one generator edge 1.

## Finite-free replacement

Let C be a nonnegative complex of free abelian groups with finitely
generated homology in every degree. Its cycles Z_i and boundaries B_i
are free by the subgroup theorem over Z, even at infinite rank.
Split each differential surjection onto B_(i-1), with B_(-1)=0:

$$
C_i\cong Z_i\oplus B_{i-1}.
$$

The differential includes the second summand into Z_(i-1) and kills
the first. Thus C is the degreewise locally finite sum of two-term free
resolutions B_i -> Z_i of H_i, placed in degrees i+1 and i.

For each i choose a finite free surjection F_i -> H_i with kernel E_i,
finite free by Noetherianity and the subgroup theorem. Lift F_i -> H_i
to Z_i and Z_i -> H_i to F_i by freeness; restrict lifts to the kernels.
Each composite minus identity in degree zero factors through the
corresponding kernel inclusion; this factor is a chain homotopy,
whose degree-one identity follows by cancellation of the injection.
Taking degreewise sums gives a homotopy equivalence to a complex
whose term i is F_i plus E_(i-1), finite free in every degree.

Tensoring preserves chain homotopy equivalences with the signed
total differential. Every degree of every finite tensor power of
the replacement has finitely many finite-free tensor summands.
Cycles are finite by Noetherianity and homology is their quotient.
Thus every tensor-power homology is finitely generated.

The protected reducedBasis gives freeness of the actual reduced
Eilenberg--MacLane terms. The rank-one base and finite_next in
029 prove finite generation of all reduced homology of K(Z,n)
for every positive n, without a Kunneth premise.

## Finite type on arbitrary groups

Use the approximate-resolution FP induction of 016, with these
finite rank-one coefficients and the natural matrix action of 028.
Tensoring a finite presentation of a coefficient M with the free
lattice functor U is exact on lattices. The induction produces a
resolution of U by finite sums of free representables.

Extend each representable as A -> Z[A^r] to all abelian groups.
Yoneda extends the differentials and augmentation uniquely, and
their identities are checked at the finite representing lattices.
Exactness on arbitrary free groups follows by filtered colimits
of finite free subgroups. For general A take the simplicial
free-forgetful cotriple resolution F_* -> A. Its underlying set
resolution has an augmented extra degeneracy, preserved by finite
powers and free abelian groups. In the other direction the extended
resolution is exact on each free F_q. The first-quadrant total
comparisons establish exactness at A. Pointwise evaluation on
presheaves followed by exact abelian sheafification gives the
condensed resolution.

## Compact analytic continuity

Write D for derived internal Hom into discrete integers.
Use compact cohomology comparison for free condensed groups,
homotopy invariance, and cohomology continuity under surjective
inverse systems of compact Hausdorff spaces. Apply these after
product with every Stonean probe S. These are explicit outstanding
formal inputs, not axioms.

For the real product E, use all coordinatewise closed symmetric boxes.
Every compact probe map lands in one. Boxes contract compatibly under
inclusions. Each finite power is a filtered colimit of box powers as
condensed sets. Derived Hom at S converts the corresponding free
groups to a derived inverse limit of compact cohomology complexes.
Projection to S identifies the coherent diagram with the constant
one; the directed indexing nerve is contractible. The zero-section
comparison on every finite-type resolution term is invertible.
First-quadrant Hom totalization gives D(E)=D(0)=0.

For the circle product K with finite-coordinate tori K_F, compact
cohomology continuity on every finite power gives the colimit of
cohomology from finite coordinates, tested against each S.
Exact filtered colimits commute with the finite sums and
first-quadrant Hom totalization. Hence

$$
D(K)\simeq\varinjlim_{F\subset I,\ F\ \mathrm{finite}}D(K_F).
$$

For one circle, the genuine real/circle sequence and D(R)=0
identify D(R/Z) with Z[-1] by the boundary class (R here denotes
the reals). Additivity gives finite direct sums for finite tori.
Coordinate projections induce coordinate inclusions on duals.
Therefore

$$
D((\mathbb R/\mathbb Z)^I)\simeq\mathbb Z^{(I)}[-1].
$$

This recovers the circle-product assertion from one circle and
continuity, not by assuming the circle-product theorem. The
integer-product sequence and coefficient compatibility in 027
identify D(Z^I) with the direct sum by evaluation itself.
The duality triangle and product-target argument of 027 give the
genuine canonical-unit comparison.

## Evidence boundary

This is source mathematics. The Lean candidate addresses the actual
circle-model bridge and finite homology transfer from degreewise
finite replacements. The homogeneous bar comparison, PID splitting,
finite-free replacement, FP induction, cotriple extension, and
compact cohomology comparison/continuity require kernel reconstruction.
No analytic vanishing is introduced as an axiom.

The previous SSD environment was unavailable after the CHAD storage
incident. No mechanical-disk Lean fallback or access to the failing
rescue source is used. The candidate requires existing native formal
validation; no MATHCERT certification or final CM5 promotion is claimed.
