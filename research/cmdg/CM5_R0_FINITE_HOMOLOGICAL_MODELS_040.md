# CM5 R0: finite homological models and the rank-one bar reduction (040)

## Disposition

The finite-free replacement and tensor-power finite-generation
mechanisms are now kernel-checked, as is induction over all positive
Eilenberg–Mac Lane stages from the actual additive bar base. This
does not assert the remaining rank-one bar homology computation.

Parent PR #3850 is protected at merge
60afab132850f9c6f09dcd3d522d9f2f88db1780.

## Finite subcomplex

Let C be any nonnegative integral chain complex with finitely
generated homology. For a finite submodule V contained in the range
of a linear map, choose finitely many generators of V and lift them.
The span of the lifts is finite and maps onto V.

In each degree choose a finite submodule of the cycles mapping
onto homology. Write L_n for its image in C_n. Define F_0=L_0.
Given F_n, the intersection of F_n with the range of the next
differential is finite by Noetherianity of finite integer modules.
Choose a finite lift U of this intersection into C_(n+1).
Put F_(n+1)=L_(n+1)+U. The exact equality is

$$
d(F_{n+1})=F_n\cap\mathrm{im}(d:C_{n+1}\to C_n).
$$

Thus these actual submodules form a complex. Its inclusion into C
is surjective on homology by the selected cycle representatives
and injective by the boundary-lifting equality. All degrees are
handled by one recursion, not by independent incompatible truncations.

If the original chain terms are free, the finite subcomplex terms
are finite and torsion-free, hence finite free over the integers.
Both complexes are bounded below and degreewise projective.
The Mathlib projective-complex quasi-isomorphism criterion supplies
a chain homotopy equivalence. This bypasses the infinite-rank
subgroup freeness/splitting step in the source reconstruction 030.

## Tensor powers and the bar induction

A finite tensor product of finite modules is finite: the bilinear
image of two finitely generated top submodules is finitely generated,
and the pure tensors span. A finite coproduct is finite by the
biproduct identity, since the ranges of its finitely many inclusions
are finite and their sum is the entire module. In each total degree
there are only finitely many bidegrees. Consequently tensor powers
of the finite replacement have finite terms, and their homology
is finite by Noetherianity of the cycle submodule and the quotient
map onto homology.

The actual signed tensor complexes preserve chain homotopy
equivalences separately in both variables. Induction gives an
equivalence of every finite tensor power. Transfer finite homology
across that equivalence.

The existing reducedBasis gives freeness of every actual reduced
Eilenberg–Mac Lane chain term. The protected finite_next theorem now
applies with the checked tensor-power finite-generation theorem.
This gives finite_positive in all positive stages, conditional
only on finite homology of the degree-one model.

The existing groupMooreIso computes the normalized Moore complex
of the additive simplicial bar. Apply the Dold–Kan unit and inverse
functor to obtain barEMIso, an actual simplicial isomorphism with
em 1. Apply the reduced free chain functor and the existing comparison
to obtain barReducedIso. The theorem finite_from_bar now transfers
finite generation from the actual reduced additive bar of a group
to every positive Eilenberg–Mac Lane stage of that group.

## Residual proof target

For the integer group the missing base is the integral reduced
homology of the genuine additive bar in all degrees. The source
proof in 030 uses the homogeneous vertex-tuple resolution and the
two-term integral Laurent-polynomial resolution. The equivariant
comparison and passage to coinvariants remain to be checked.
After the rank-one base, the pseudocoherence/FP induction, the
finite-lattice construction, and the lifted-universe bridge remain.
No inhabitant of LatticeBD or unconditional canonical comparison
is claimed.

## Local execution evidence

Lean v4.33.0-rc1; mathlib
79d0395a1825a6264ad5d269e35e60537518955e.
Exact 70-module source closure and pinned manifest/toolchain match
capture 133cc43a3f9e40c4877d63b889c091ed.

| Module suffix | Final local capture |
| --- | --- |
| BreenDeligneFiniteSubcomplex | 17831cb25a8044d28a3b5112b91dd21f |
| BreenDeligneFiniteSubcomplexComparison | 0555ba0a3a0e413293f4f4b9e5f62120 |
| BreenDeligneFiniteTensor | d1006d05e6bc456294f4d017f8d4bc67 |
| BreenDeligneFiniteInduction | ad9295571d3a4555a43d63b2d4b06ab5 |
| BreenDeligneRankOneBar | 5f3dfd9b938046d39d1c8349672c32cc |

All final endpoints print only propext, Classical.choice and
Quot.sound. The K-projective imports required eleven additional
Mathlib modules in the NVMe overlay. A nonessential Mathlib
TensorProduct.Maps overlay compilation returned a simp diagnostic;
the candidate instead proves the required finite-generation fact
directly using the successfully compiled Finiteness.Bilinear API.
No upstream source patch or HDD fallback was used. No failed
candidate was copied to the repository. Local captures are not
independent attestations.
