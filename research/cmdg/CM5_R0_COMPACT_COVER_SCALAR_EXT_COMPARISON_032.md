# CM5 R0: actual compact-cover scalar Ext comparison

## Scope

Parent candidate: PR #3807, exact corrected head
`3b191ec2d5d0f6e9ab62e53b9a9d6c57ff9c53ee`.
Let p:P→T be an epimorphism from a profinite space onto a compact
Hausdorff space. Write R_n for the genuine closed equal-image
(n+1)-tuple space, C_n for its actual free condensed module,
M=F(T), and D for the discrete integer coefficient object.
The parent constructs the exact augmented Cech complex and proves
all positive Ext(C_n,D) vanish. No projectivity of arbitrary
relation terms is assumed.

## Construction

The new Lean modules construct K_0=M and K_(n+1) as the actual
kernel at C_n. Exactness gives short exact sequences
0→K_(n+1)→C_n→K_n→0. The Yoneda extension class of each sequence
induces the connecting maps. Relative acyclicity of the middle
term proves that each connecting map is surjective; in positive
source degree it is bijective.

A degree-(n+1) Hom cocycle on C_(n+1) factors uniquely through
the epic map onto K_(n+1). The first connecting map sends this
factor to Ext^1(K_n,D), and iteration of the positive-degree
connecting isomorphisms gives Ext^(n+1)(M,D).
This map is additive and surjective. Exactness identifies its
kernel with the restrictions of morphisms C_n→D, precisely the
coboundaries. The scalar Hom equivalence is additive and intertwines
the actual alternating face differential, so the same map induces
an additive equivalence from the quotient of scalar cocycles by
scalar coboundaries to actual positive Ext.

The declarations are:

- CompactCoverExtTransfer: actual syzygy short exact sequences;
  conditional transfer of scalar exactness to all positive Ext.
- CompactCoverExtClasses: genuine Yoneda connecting maps, positive
  dimension-shift isomorphisms, surjectivity and exact kernel of the
  syzygy-Hom class map, unique cocycle factorization.
- CompactCoverScalarCohomology: scalar differential agreement,
  square-zero, scalar cocycle/class map, exact kernel, quotient
  equivalence `scalarCohomologyExtEquiv` and its evaluation on
  quotient representatives `scalarCohomologyExtEquiv_mk`.

## Evidence and boundary

All three modules locally checked with the source-locked Lean
4.33.0-rc1 and Mathlib 79d0395a1825a6264ad5d269e35e60537518955e
in the restored NVMe environment; reported axioms are propext,
Classical.choice and Quot.sound only. Capture IDs: ExtTransfer
4d493a42ce6942489c0f536b22a59d1a; ExtClasses
d7a96960a7a149cd8e78684ff12988ed; ScalarCohomology
1aac8af9af774dff96ee6ae650553d28.
These are local checks, not independent certification or protected
admission. The positive-degree comparison is unconditional for
the stated genuine compact-cover epi; it does not assume scalar
acyclicity. Naturality across changes of cover and degree-zero
packaging are not asserted by this module.

The next geometric obligation remains to formalize the dyadic-cell
cover and the ordered-grid prism homotopy on its genuine finite
nerves. A source proof is recorded in PR #3807 comment 7212473796.
A local exact-integer regression (capture
13368899b7304c2ea4ad9642ca5753b0) checked 1300 cases on the 3x2 grid:
all admissible ordered tuples in degrees 0 through 3, for each of
the two coordinate reductions. This is a finite test, not the
general kernel proof. The actual compact-box calculation, coherent
box-colimit transfer, real/circle derived duality and final CM5
unit equivalence are not established here.
