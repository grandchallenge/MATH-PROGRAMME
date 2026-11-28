# CM5-R0: genuine Breen–Deligne real-group transfer (036)

## Disposition

Source-theorem-backed mathematical transfer complete. Kernel-checked
transport for a supplied universal finite-type Breen–Deligne package.
The existence of the package itself is not yet kernel-proved. No
MATHCERT claim, protected admission claim, circle calculation, or
biduality claim follows from this receipt.

The input is Theorem 4.10 of Peter Scholze, *Lectures on Condensed
Mathematics*, arXiv:2605.03658v1 (5 May 2026), material jointly developed
with Dustin Clausen: https://arxiv.org/abs/2605.03658v1 .
Theorem 4.10 supplies a natural exact augmented resolution of the
identity on abelian groups by finite sums of free finite-power functors.
We use that existence theorem, not a newly postulated Ext vanishing.
In Lean, the explicit input UniversalBD consists of these natural maps,
finite arities, augmentation, and exactness in the functor category.
An inhabitant of UniversalBD has not been constructed internally.

## Mathematical reconstruction

Let $E=\mathbb R^I$ with its product topology and $F(X)=\mathbb Z[X]$.
For each profinite probe $S$, 035 proves the canonical projection
induces the all-degree Ext comparison between $F(S)$ and
$F(S\times E^r)$, for every finite power including power zero.
The zero-section split is canonical. The kernel of the projection has
vanishing Hom and positive Ext against the discrete integers: degree
zero follows from surjectivity of precomposition with projection;
positive degrees follow by retract from the free relative real product.

For a universal resolution term with finite arities $r_{nj}$, evaluate
the universal functor at the actual continuous-map abelian group
$C(T,E)$ for each compact Hausdorff test $T$. Take the direct sum
indexed by continuous maps $T\to S$. Both evaluation and indexed sum
are exact; the resulting presheaf complex is natural under pullback.
Sheafification is exact. This realizes the original augmentation onto
the sheafification of the indexed real-group presheaf, the usual
presheaf model for $F(S)\otimes E$.

The genuine coordinates of each transported term are

$$
L_n=\bigoplus_{j=1}^{k_n} F(S\times E^{r_{nj}}).
$$

Evaluation at the zero group gives a split chain projection onto the
corresponding zero-value complex, with base terms finite sums of
$F(S)$. Naturality of the universal differential gives the two chain
identities and compatibility with the augmentation. Its kernel
complex is an exact resolution of the same target, proved by retracts
on homology and the split augmentation. In each degree its terms are
retracts of the original terms and their Hom into the discrete
integers vanishes by surjectivity of the projection on Hom.
Consequently the entire reduced resolution is Ext-acyclic, including
degree zero. Actual categorical dimension shifting yields

$$
\mathrm{Ext}^{q}(F(S)\otimes E,\mathbb Z)=0
\qquad(q\geq0).
$$

The point probe specializes the indexed sum naturally to the original
real presheaf. The presheaf satisfies the compact Hausdorff sheaf
condition; dense Stonean comparison identifies it with the existing
realProductCondensed object used in the integer-real-circle sequence.
Thus ordinary Ext out of that genuine abelian group vanishes.

At source-proof level, free Stonean probes are flat projective
generators. Flatness follows from exact probe-indexing followed by
sheafification, the usual tensor model. Derived tensor-Hom adjunction
and evaluation on these generators imply the internal derived Hom
from the real product to the discrete integers is zero. The
tensor/derived-internal-Hom identification and detection step are not
claimed as a separate kernel-checked internal derived-category
endpoint in this tranche.

## Formal endpoints

All names below are in the CMDG.CondensedCM5R0 namespace.

- RealProductProjection.reducedRealPower_extZero: all-degree reduced
  free-power vanishing, with no universal resolution input.
- SplitResolution.reducedResolution: exact kernel resolution of the
  original augmentation.
- FiniteTypeRealResolution.target_extZero: transfer from an actual
  finite-type split resolution with canonical coordinates.
- BreenDeligneProbe.transportedResolution and transportedZeroSplit:
  transport the natural universal resolution through evaluation,
  exact indexed sums, and exact sheafification.
- BreenDeligneProbe.realBD: instantiate every coordinate and
  projection identity of the finite-type transfer.
- BreenDeligneProbe.relativeReal_extZero: all-degree Ext of the actual
  sheafified indexed real presheaf, with UniversalBD input.
- BreenDeligneProbe.realGroup_extZero: same all-degree conclusion
  for the existing RealCircleStoneanPresheaf.realProductCondensed,
  with UniversalBD input.

The final endpoints print only propext, Classical.choice and
Quot.sound. The explicit UniversalBD parameter remains visible;
absence of sorryAx does not establish existence of that parameter.

## Local evidence

Lean v4.33.0-rc1, mathlib 79d0395a1825a6264ad5d269e35e60537518955e,
NVMe workspace via the governed gcl-lean-work launcher. Successful
local compilation captures, in dependency order:

| Module suffix | Capture ID |
| --- | --- |
| ReducedRealPower | 363cd7408f2b48f194ff26592c8af912 |
| SplitReduction | 6f2d9cfafdc142898ebe4af27843e64b |
| RealTransfer | ebe1e4be3cb84a5ab9cafd61c049e9fb |
| ProbeIndex | 8e4c8f65ab6b4daf81656091e4af643e |
| UniversalTransport | bfadad1a1ee846629cb0723e9a83a8f3 |
| ProbeFree | ed52642bb0ca4441a78387cde9ba0115 |
| RealCoordinates | d7f2d6318525411aa02d7fbb8478e98c |
| RealCoproduct | 6dbc94c226c84c5db5999bcdf75ab864 |
| RealRealization | 7dd148881d7a4e8bbb21d4bdbd93f197 |
| RealGroup | be98424a9e7f4b48bcd1fab5ee1eaa41 |

Local captures are not independent execution attestations. Compilation
diagnostics were repaired before recording these endpoints. The
RealRealization capture has overall shell exit 1 from a subsequent
grep with no matches; the set-e command reached that grep only after
the successful Lean command. Exact-head native replay remains the
admission evidence requirement. The parent #3824 was read back merged;
035 and 036 are combined in one candidate to avoid redundant CI.

## Residual obligations

1. Construct the universal finite-type package in Lean, including the
   finite generation and stabilization argument behind Theorem 4.10.
2. Formalize the internal derived-Hom identification and detector
   argument as an explicit kernel-checked endpoint.
3. Continue the actual circle-product continuity calculation with the
   real-circle short exact sequence and canonical-unit compatibility.

These are separate from the now checked transfer of an actual
universal finite-type resolution onto the genuine real group.
