# CM5 R0: genuine solid integer product and analytic Ext bridge

## Verified result

The genuine free-solid source, not a replacement object, is identified
with the integer term of the protected real/circle short exact sequence.
The theorem solidIntegerIso_projection identifies the forward map on
every protected Nöbeling coefficient coordinate.

IntegerProductBridge proves the product universal property directly on
Stonean probes. Coordinates of a continuous map into a product of discrete
integers are locally constant; conversely any family of locally constant
coordinates assembles into a continuous product map. These are linear
natural transformations. The limiting fan transports along the Stonean
sheaf equivalence and the discrete-coefficient comparison.

SolidIntegerProduct proves the protected lifted basis index is small by
injection into the integral locally constant functions. Reindexing the
actual protected coefficient fan by Shrink and comparing limiting fans
gives solidIntegerIso and its coordinate identity.

SolidAnalyticExtReduction transports the established dimension shift
along this actual source isomorphism. In every positive degree, vanishing
of Ext from the real product in all degrees and from the circle product
in the next degree, into the genuine solid target, implies vanishing of
Ext between the genuine solid source and target. Composing with the
protected all-shifts criterion reduces the derived comparison of the
canonical unit to precisely those analytic inputs. The theorem takes
the analytic assertions as explicit hypotheses, not axioms.

## Mathematical closure relative to the published inputs

The stable suspension isomorphism on actual reduced chains was admitted
in PR #3784. The source-relative finite-type argument in reconstruction
016 and the real-product argument in reconstruction 015 describe the
remaining resolution and derived cohomology formalization.

For an index set I let B be the integer product, E the real product,
K the circle product, and A the direct sum of I copies of Z. Write D
for derived internal Hom into the discrete integers.

For E, use all coordinatewise compact boxes, rather than a countable
exhaustion. On any compact probe the image lands in such a box.
The zero sections and contractions commute with inclusions. Compact
cohomology comparison and the derived limit of a coherent constant
diagram over the directed box index give the zero-section comparison
for every finite power and Stonean probe. The finite-type Breen–Deligne
resolution and its functorial first-quadrant spectral sequence then
give D(E)=0. This uses Theorem 3.2, Theorem 4.5 and Corollary 4.8 of
Scholze, Lectures on Condensed Mathematics, arXiv:2605.03658v1.
It is independent of the derived scalar-adjunction shortcut.

For K, Theorem 4.3(i) of the same source computes D(K) as A[-1],
via the sum of the pullbacks of the individual circle boundaries.
The genuine short exact sequence and coordinate naturality give an
invertible connecting map D(B) -> D(K)[1]. Under this map the
coordinate evaluation A -> D(B) becomes precisely the sum of those
boundaries shifted by one. Thus the actual evaluation is invertible.
No assertion of derived solidness from Proposition 5.7 is used as a
premise.

For a profinite X, compact cohomology comparison gives the derived
dual of the free condensed group as the discrete group C(X,Z).
Its dual is the genuine solid product by the free basis comparison.
The double-dual map on generators is evaluation of locally constant
functions, which is exactly the protected canonical unit in its
coefficient coordinates. The duality triangle identity and the
evaluation equivalence show that precomposition by this unit is
invertible on the derived dual. Derived internal Hom into a product
of discrete coefficients is the product of the scalar mapping
complexes; products are exact. Thus comparison into every genuine
solid target is invertible in every shift. In particular all positive
Ext groups between these genuine objects vanish.

## Evidence and boundary

The three new Lean modules prove the limiting-fan identification,
the genuine-source isomorphism and coordinate compatibility, and
the conditional positive-Ext reduction. They do not formalize the
external analytic cohomology theorems. The source-category proof is
complete relative to the stated published inputs; an independent
kernel-checked derivation of the real and circle analytic inputs,
the functorial finite-type resolution and derived cohomology
comparison remains open. No independent certification or final
CM5 promotion is asserted.
