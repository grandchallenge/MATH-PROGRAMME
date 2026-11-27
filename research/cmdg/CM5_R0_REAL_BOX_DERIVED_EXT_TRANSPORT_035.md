# CM5 R0: real box derived Ext transport

## Result and scope

For arbitrary profinite S and index type I, the actual canonical projection
from the free condensed relative real product to the free condensed object
on S induces a bijection against the discrete integer coefficient in every
nonnegative Ext degree. Positive Ext of the free relative real product
vanishes. These are not claims about the underlying condensed real abelian
group itself or about the final biduality unit.

Endpoint declarations: `RealProductProjection.freeProbeReal_extPositive_zero`
and `RealProductProjection.realProjection_ext_bijective`.

## Construction

Instead of a monotone-poset simplicial replacement, use the full ordered
Cech resolution of the cover by all compact centered boxes. Finite
nonempty intersections are actual boxes with coordinatewise minimum
radius. Each compact probe has a lift to some box, by compactness in each
coordinate. On a fixed compact test, the relation tuples are precisely
the ordered labels and sections of the common intersection. The
augmented free module complex is split exact on that test by a chosen
lift. Exact sheafification transports this to the actual augmented
condensed resolution; choices need not be natural in the test object.

Every degree is a coproduct of the compact-box free modules. Its relative
acyclicity follows from the actual Stonean projective generators, AB4,
and natural dimension shifting, not from an assumption that these box
modules are projective. The coefficient Hom complex identifies via the
canonical projection with functions on ordered tuples valued in Hom
from the free probe. All face restrictions become identities on these
coefficients. Prepending the zero-radius label contracts the positive
cochain complex. Actual syzygies and the long exact Ext sequence then
yield positive Ext vanishing, and degree zero is the previous canonical
projection bijection.

## Local evidence

Lean v4.33.0-rc1; mathlib 79d0395a1825a6264ad5d269e35e60537518955e.
The eight modules are checked on the CHAD NVMe workspace. Successful
local execution captures, in dependency order:

- AmbientProjectiveGenerators: 3906b938575d4a4cb597ee5745f5277a
- CoproductExt: 4aa5a17ec2de4ac4bb5cf18cf8da2c3c
- AcyclicResolutionTransfer: 830a8a2f5f5047c39bbefcc70ca0073b
- RealBoxCechGeometry: 701fdec5b10a49c382e13b84b1710777
- RealBoxCechPresheaf: 3b1c7721cadb4966a84007f16a6fbb07
- RealBoxCechExact: 5b4956274610427d8244e8c68c7bfe6b
- RealBoxCechCoproduct: 25482a52d5bf4a2f89beb3f78c3263dc
- RealBoxCechHom (final): ac0017cb981b459e88fe8eb5079b0c79

Endpoint axioms: propext, Classical.choice, Quot.sound only.
Local execution is not independent replay or mathematical certification.
Parent PR #3824 has successful formal validation on its exact head
86c8878e790ca0f5318c8373947f4756cd257ea9, but is not protected-admitted:
the specialist controller rejects its unmapped/mixed candidate paths.
This successor is retained without a redundant native CI dispatch while
that admission issue remains. No protected policy is weakened.

Next: the genuine finite-type Breen--Deligne resolution of the underlying
real abelian group, including compatibility of the canonical maps, then
circle continuity and the actual derived biduality unit.
