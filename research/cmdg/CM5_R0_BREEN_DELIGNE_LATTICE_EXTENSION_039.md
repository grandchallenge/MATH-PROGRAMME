# CM5 R0: finite-lattice Breen–Deligne extension (039)

## Disposition

The extension from a degreewise finite polynomial resolution on finite
free integer lattices to all abelian groups is kernel-checked. This
is a reduction of the remaining existence problem, not a construction
of an inhabitant of the finite-lattice resolution type.

The input is the explicit LatticeBD structure in the required lifted
coefficient universe. The output LatticeBD.toUniversalBD supplies the
actual natural augmentation and differentials, their identities,
epimorphic augmentation and categorical exactness in every degree.

The canonical comparison is the existing protected endpoint of 038:
canonicalUnit_allShifts_of_LatticeBD is obtained by applying that
endpoint to the constructed UniversalBD package. Parent PR #3845
merged at 5dd36e28545e13e7b654454ad047911e21a824f3.

## Construction

For a polynomial functor

$$
P(A)=\bigoplus_{j=1}^{k}\mathbb Z[A^{r_j}],
$$

a natural map on finite free lattices extends uniquely to all
modules. Each tuple is the image of the generic tuple in the
appropriate finite free lattice. The formula applies the target
functor to this tuple map and the value on the generic tuple.
Naturality and the restriction identity are checked on free
generators. Injectivity of restriction implies that the augmentation
and differential identities on the lattices extend to the whole
module category.

Every polynomial element of an arbitrary free module involves a
finite union of finite supports of basis vectors. A finite-coordinate
retraction fixes the element. Exactness on finite free modules
therefore gives exactness on free modules of arbitrary rank.

For an arbitrary surjection of modules, form the actual equal-image
tuple relation modules, with alternating face maps. Their augmented
identity-functor complex is exact. For a cycle, prepend its first
coordinate if the number of alternating summands is even; otherwise
prepend zero, which has the required image because the cycle
condition forces that common image to vanish. The alternating
face identities prove that this produces a primitive. This argument
does not assume an additive section of the original surjection.

The finite polynomial functors carry the relation tuples to the
corresponding set-level relations: the coproduct tag is constant
and the remaining coordinates transpose. The resulting isomorphism
intertwines every face and augmentation. The previously proved split
free Cech contraction gives exactness of these rows.

The elementary commuting double-complex descent lemma uses
simultaneous cycle lifting by induction on vertical degree.
Horizontal exactness and exactness of positive vertical columns
imply exactness of the augmentation column. No spectral sequence
convergence assertion is needed.

For a finitely generated module take a finite free cover. Its
relation modules are submodules of finite products of finite free
modules over the lifted integers, a PID. They are finite free by
the finite torsion-free module theorem. Thus the actual Cech
descent proves exactness at every finitely generated module.

For a general module take the finitely generated submodule spanned
by all entries of tuples in a given polynomial element's finite
support. The polynomial element lifts to this submodule. Every
polynomial functor preserves injective module maps, as does the
identity functor. Consequently the cycle condition is detected on
the finitely generated submodule. Exactness there supplies a
primitive which maps to the original element. This proves
pointwise exactness in all degrees on every module, and hence
categorical exactness of the natural complex.

## Evidence

Lean v4.33.0-rc1, mathlib 79d0395a1825a6264ad5d269e35e60537518955e.
The complete 226-module source closure and pinned toolchain and
manifest match the candidate repository (capture
05f2715827bc4c98ad735e9f2df5b299).

| Module suffix | Local capture |
| --- | --- |
| BreenDeligneUniversalExtension | 080927ed30624421b07800a67b5c64b5 |
| BreenDeligneFreeExactness | f61aa0f2032e4a7da098ded7209b122f |
| BreenDeligneDoubleDescent | da0661ae5438429283e634daf297239c |
| BreenDeligneCechModules | 695a73c3c37f429fbfb22da2345d1734 |
| BreenDeligneCechPolynomial | f52fdcce8ab74c23bc38652675e4432c |
| BreenDeligneLatticeComplex | 4c1de9c64bb54a378b86d3d9e94a14f6 |
| BreenDeligneCechDescent | 240904ed948f4fb7a9bb19b7c61c303d |
| BreenDeligneFiniteModuleDescent | 0ae2657fb9704c0788f4afb53b202c6b |
| BreenDeligneAllModuleExtension | abfbbe769acf41f1bcf1e0feac70d713 |
| CanonicalUnitLatticeBD | 5535dfc562024c328dc3acf902853ef6 |

Final endpoints print only propext, Classical.choice and Quot.sound.
Lifted scalar-action instance mismatches were repaired by explicit
bundled submodule instances and integral scalar-action identities.
Twelve missing PID dependency modules were built on the NVMe
workspace; no HDD fallback or manual CI duplication used.
Local captures are not independent attestations.

## Residual mathematical obligation

Construct LatticeBD itself. In the source proof (Scholze, Lectures
on Condensed Mathematics, arXiv:2605.03658v1, Theorems 4.10 and
4.14, Lemma 4.15 and Theorem 4.16), the substantive finite-lattice
existence argument uses finite generation of the stable rank-one
Eilenberg–Mac Lane homology and a pseudocoherence induction.
The existing formal stable-range and matrix-action results provide
part of that argument. The rank-one finite generation, FP closure
and induction, and construction of a coherent infinite resolution
by finite polynomial terms remain to be checked, including the
bridge into the lifted lattice category used here.

No unconditional universal resolution, unconditional canonical
comparison, or independent certification is asserted.
