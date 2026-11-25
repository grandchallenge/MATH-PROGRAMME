# CM5 R0: explicit signed shuffle and both homotopies

## Result

The original signed shuffle path sum commutes with the differentials of the actual alternating diagonal and signed total complexes of every bisimplicial integer module. The natural chain map `signedShuffle` and unconditional `signedEquiv` use the original Alexander–Whitney and signed shuffle maps, not an abstract replacement inverse. Both composites are equipped with chain homotopies to the identity.

## Proof decomposition

- Corners: a mixed corner has a sign-reversing involution preserving the deleted ordinal pair. Its evaluated boundary contributions cancel.
- Straight and Insert: deleting a uniquely attained horizontal coordinate gives a lower-dimensional path and a face index. Inserting at the unique crossing gives the inverse, including endpoints.
- StraightSign: the change in the inversion exponent gives precisely the horizontal face sign.
- Transpose: exchanging axes complements the inversion count; the vertical sign consequently includes the total-complex factor.
- Partition and BoundarySum: all interior-bidegree deletions partition into horizontal, vertical, and mixed types. The resulting signed sum identity holds for arbitrary additive evaluations.
- Signed: evaluate the deleted ordinal pairs by the bisimplicial functor; include the previously established axis identities and use total-summand extensionality. This proves `signed_shuffle_comm` in all degrees. Naturality is inherited from the explicit shuffle family.
- Both homotopies: apply the diagonal and total acyclic-model homotopy constructors to the actual chain maps. Their degree-zero composites are identities. The total-model contraction is the explicit two-stage contraction established in the preceding candidate.

## Scope

The alternate acyclic-model inverse from the preceding candidate remains a separate construction; no equality with that inverse is claimed. The explicit signed shuffle now has its own unconditional equivalence. This does not yet establish the comparison of the actual normalized bar columns with tensor powers, nor the diagonal weak equivalence with the next Eilenberg–MacLane object. No independent certification is claimed.
