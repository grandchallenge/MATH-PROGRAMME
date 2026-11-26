# CM5 R0: stable homology of the actual first-column inclusion

## Result

For the actual normalized reduced bar bicomplex of the Dold–Kan
object K(A,n), the already defined reducedSuspensionMap induces
an isomorphism on homology in every total degree j with j < 2n+1.
The proof works for every abelian group A. It uses the genuine column
connectivity in the preceding candidate, with no assumed spectral
sequence or convergence assertion.

## Proof spine

- TotalCoordinates: define projections out of the actual total complex
  using its coproduct universal property. Verify the diagonal and
  off-diagonal projection identities, prove that the sum of the
  projection-inclusion composites is identity, and establish the
  exact signed two-term formula for coordinates of the total differential.
- ColumnElimination: in total degree j a chain whose boundary is
  supported in horizontal degrees at most one can be modified by
  subtracting a boundary so that the chain itself is supported there.
  The top coordinate is a vertical cycle; vanishing of that column's
  homology gives a filling. Insert the signed filling and eliminate
  the top column. Descend by finite induction. This argument applies
  to chains, not merely cycles, and does not divide by any nonunit.
- FirstColumnRange: the actual suspension inclusion is degreewise
  injective, and every element of the total complex supported through
  horizontal degree one is in its range, since column zero vanishes.
- HomologyElements: connect cycle representatives and boundaries to
  Mathlib's actual homology object via its concrete module homology
  and the quotient by the range of the incoming differential.
- StableInclusion: apply elimination in degree j to get surjectivity,
  and in degree j+1 to obtain injectivity. Higher columns vanish in
  both degrees whenever j < 2n+1. Transport via the actual first-column
  isomorphism to the existing reducedSuspensionMap.

## Scope

The reduced suspended chains and the normalized reduced bar total
have now been compared in the stable range. The remaining step
toward the stable suspension theorem is to compare the actual
horizontally normalized bar total with its reduced diagonal chains,
and identify the diagonal bar group with K(A,n+1) up to a weak
equivalence which transports reduced homology. No CM5 closure,
independent certification, or external claim promotion is asserted.
