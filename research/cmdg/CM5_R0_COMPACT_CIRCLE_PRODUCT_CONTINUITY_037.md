# CM5-R0: compact-product continuity and genuine circle-group transfer (037)

## Disposition

Finite-coordinate continuity of scalar Ext is kernel-checked for pointed
compact products in every degree. Genuine circle-group continuity is
kernel-checked relative to the explicit UniversalBD package of 036.
The source-level calculation below uses its published existence theorem,
not the published circle-product duality calculation as a premise.
No independent certification or final CM5 admission is asserted.

## Compact-product continuity

Use the product of profinite presentations of the compact factors.
The genuine Cech equal-image tuple relations are products and their
homeomorphisms respect every face. Locally constant integer cochains
on compact products factor through finitely many coordinates.
Pointed extension gives sections, including at the relation level.
Thus cocycles descend and coboundaries are detected at finite stages.

The compact-cover resolution is exact after sheafification. Its
profinite relation terms are scalar-Ext-acyclic by the earlier
profinite calculation. Morphisms of syzygy short exact sequences
give actual Yoneda connecting-map naturality. Dimension shifting
transfers finite support from cochains to every positive Ext degree;
degree zero follows from locally constant functions. Pointed extension
proves injectivity of pullback in all degrees. The canonical comparison is

$$
\varinjlim_{F\subset I,\ F\text{ finite}}
\mathrm{Ext}^{q}(\mathbb Z[\prod_{i\in F}X_i],\mathbb Z)
\cong
\mathrm{Ext}^{q}(\mathbb Z[\prod_{i\in I}X_i],\mathbb Z).
$$

Lean proves the directed union, transition naturality, finite-stage
injectivity and common-stage detection explicitly.

## General resolution transfer

For an exact augmented resolution with compatible idempotent finite
truncations, suppose every scalar Ext class on each term has finite
support in all degrees. Neither projectivity nor Ext-acyclicity of
the terms is required. Write the successive syzygy tower as

$$
0\to K_{n+1}\to L_n\to K_n\to0.
$$

Choose a finite truncation F fixing the pullback of a class e on K_n
to L_n. Subtract the truncation pullback of e itself. The difference
lies in the kernel of the map to Ext of L_n. In degree zero that
kernel vanishes. In positive degree the difference lifts along the
actual Yoneda connecting map from Ext of K_(n+1) in one lower
degree. Induct simultaneously for all syzygies on Ext degree.
Naturality and absorption for larger truncations show that the union
of the two finite supports fixes the original class.

## Genuine circle group

Let K be the product of circles, S a nonempty profinite probe and
F(X) the free condensed group on X. Each finite power of K, with
S retained, satisfies the compact-product result: project a finite
set of power-coordinate pairs to a single finite subset of I.

Evaluate the natural UniversalBD resolution on the actual continuous
circle-valued group presheaf, index by maps to S, and sheafify,
as in 036. Its terms are finite coproducts of genuine free groups
on S times finite powers of K. The generator comparison intertwines
actual restriction and zero-extension maps. Finite coproduct Ext
detection gives a single finite truncation for each term class.
The general syzygy transfer proves finite support at the
augmentation. Zero-extension gives injectivity of coordinate pullback.

For the point probe the presheaf identifies with the existing
circleProductCondensed object of the protected real-circle sequence.
The isomorphism intertwines the protected circleReindex map.
Thus the theorem concerns the genuine circle group, not a surrogate.

## Source-level calculation and canonical boundary

Under the usual tensor identification of the indexed sheaf model,
the preceding result computes the relative groups as

$$
\mathrm{Ext}^{q}(F(S)\otimes K,\mathbb Z)
\cong\varinjlim_F
\mathrm{Ext}^{q}(F(S)\otimes K_F,\mathbb Z).
$$

Here K_F is the finite torus with coordinates F. Tensor its
integer-real-circle short exact sequence by F(S). This is exact
by exact probe-indexing and sheafification. The relative real term
has vanishing Ext in every degree by 036. The integer term is a
finite coproduct of F(S), whose positive scalar Ext vanishes
and whose Hom is C(S,Z) by the profinite calculation.
The finite torus therefore has Ext concentrated in degree one,
where the boundary identifies it with the finite direct sum
of C(S,Z). Naturality identifies coordinate pullback with inclusion
by zero extension. The directed union gives degree one equal to the
direct sum over I of C(S,Z), with all other degrees zero.
An empty probe has zero free source. Compactness of S identifies
this direct sum with C(S, direct sum of Z).

At source-proof level free Stonean probes are flat projective
generators. Evaluation and derived tensor-Hom adjunction detect
the canonical map built from individual circle extension classes:

$$
\bigoplus_{i\in I}\mathbb Z[-1]
\xrightarrow{\sim}
R\underline{\mathrm{Hom}}(K,\mathbb Z).
$$

For the genuine integer-real-circle sequence the connecting map
from the dual of the integer product to the shifted dual of K
is invertible, since the real dual vanishes. Coordinate naturality
identifies the composite with evaluation on each integer coordinate.
Hence evaluation of the direct sum of integers into the dual of
the integer product is invertible. This reconstructs the circle
calculation rather than citing it as an analytic hypothesis.
The tensor and internal derived-Hom detector, finite-torus boundary
calculation, and canonical-unit conclusion are source-level arguments,
not new Lean endpoints.

## Kernel-checked endpoints and receipts

All ten modules have prefix CMDGCondensedCM4P3DerivedCM5R0.
Local Lean v4.33.0-rc1, mathlib
79d0395a1825a6264ad5d269e35e60537518955e. SSD source closure
matches all 208 repository modules and pinned toolchain/manifest.

| Module suffix | Successful local capture |
| --- | --- |
| CompactProductContinuity | e31cef21d74a42abbf73506be413a188 |
| CompactCoverNaturality | 7b56ce1e39894cab9b31a0acbb11fac8 |
| CompactProductExtContinuity | f3099036df124631bca73f723c031a98 |
| CompactProductAllDegrees | 4505312ad134450c9affcb3002739519 |
| CirclePowerExtContinuity | 1890588687304a96936560408fa4f93b |
| ResolutionFiniteSupport | 11db362cee7645438d974e70b4030122 |
| BreenDeligneCircleCoordinates | c5e3a51ba15f470293a7745867e183be |
| BreenDeligneCircleRealization | 1e8556bbc508400e9ee3852fc4dc71b9 |
| BreenDeligneCircleTransfer | 1f5abfecb92b498c8c7050ebbf9290b9 |
| BreenDeligneCircleGroup | 39b41ab56f8b4b0585c24527f28ab6a0 |

Primary endpoints: compactProduct_ext_finiteSupport,
compactProduct_coordinatePull_injective, finiteClass_commonStage,
target_finiteSupport, relativeCircle_ext_finiteSupport,
relativeCircle_ext_pull_injective, circleGroup_ext_finiteSupport,
circleGroup_ext_pull_injective. Axiom reports contain only propext,
Classical.choice and Quot.sound. The circle existence input
UniversalBD is an explicit parameter, not a hidden axiom.
Local captures are not independent attestations. Native exact-head
replay is required for protected admission. Parent #3839 was
read back merged.

## Residual obligations

Construct UniversalBD internally (published Theorem 4.10,
arXiv:2605.03658v1); formalize the finite-torus boundary
identification and internal derived tensor-Hom detection; then
complete comparison with the genuine canonical solidification
unit using 027. No certification or promotion beyond the stated
endpoints.
