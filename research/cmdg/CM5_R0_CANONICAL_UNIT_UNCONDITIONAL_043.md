# CM5 R0: unconditional canonical shifted comparison (043)

## Exact result

For any profinite spaces S and T, let F_T be the ordinary free condensed coefficient module and G_T the genuine free solid coefficient module, placed in degree zero in the existing standard derived category D. For every integer n, the canonical precomposition map induced by the underived solidification morphism is bijective:

$$
\mathrm{Hom}_{D}(G_T[n],G_S) \longrightarrow \mathrm{Hom}_{D}(F_T[n],G_S).
$$

Furthermore, for every positive integer q,

$$
\mathrm{Ext}^{q}(G_T,G_S)=0.
$$

The actual Lean endpoints are canonicalUnit_atShift, canonicalUnit_allShifts and genuineSolidSource_extPositive_zero_unconditional. No Breen–Deligne package parameter remains.

## Construction and proof

1. UniverseLift constructs the scalar transport of ordinary integer modules to lifted coefficient modules and a functor from the lifted finite-free lattice skeleton to the ordinary lattice skeleton, by conjugating maps with the actual finite free coordinate equivalences. The transported identity is naturally isomorphic to the lifted identity; the transport preserves exact sequences and epimorphisms by pointwise evaluation and explicit additive equivalences.
2. LiftRepresentable identifies the actual lattice hom sets with tuples in a finite free module using its basis. Free generators and coefficients are transported by additive equivalences of finitely supported functions; the resulting natural isomorphism identifies each transported free representable with a one-arity polynomial functor.
3. PolynomialSum establishes the coproduct universal property by specifying images on the two tagged sets of free generators. The finite arity lists are joined using the equivalence between a sum of finite index sets and the finite index set of their summed cardinalities. Naturality is explicit.
4. NormalizeResolution inducts over the finite polynomial class (zero, representable, binary biproduct) and conjugates every differential and the augmentation by the selected natural isomorphisms. Transported exactness gives an actual inhabitant actualLatticeBD of the precise lifted LatticeBD structure in every universe.
5. CanonicalUnitUnconditional applies the earlier all-module extension to obtain actualUniversalBD, then instantiates the already checked canonical comparison theorem. The positive Ext statement follows for the genuine source and target products.

The construction makes noncomputable choices of finite covers and finite arity presentations. No uniform bound on arities or effective computation of the chosen resolution is asserted.

## Local evidence

Pinned Lean 4.33.0-rc1 and Mathlib 79d0395a1825a6264ad5d269e35e60537518955e.

| Module | Successful CHAD execution capture |
|---|---|
| BreenDeligneUniverseLift | 6aa67363b2b642f8bb671d09da143a18 |
| BreenDeligneLiftRepresentable | 24f05f5e7edd480db4711f7855a868de |
| BreenDelignePolynomialSum | 862585bced424b8086fd86637a11ca86 |
| BreenDeligneNormalizeResolution | b6fcce0247f142869f558920777bad07 |
| CanonicalUnitUnconditional | cd1f0c8e52cc47fb9d84b2494932fa23 |

Final endpoint receipt SHA256: f609053cfed8d7b36adaa76db8f79de735979607699d516c17add16442d1b0cb. The printed axiom closures of the lattice package, universal package, Ext theorem and both comparison endpoints contain only propext, Classical.choice and Quot.sound. The 327-module transitive CMDG source closure and pinned toolchain/manifest match the candidate bytes, with compiled objects present (capture 5054bb6a58064ecfafadc35924003316). These are local execution records, not an independently authenticated replay.

## Scope and admission boundary

The mathematical hypothesis of the actual all-integer-shifts comparison is discharged. This does not assert that the solidification map itself is an isomorphism, nor does it establish a separate internal derived Hom or biduality equivalence beyond the stated comparison, the source-semantic identification of the candidate predicate with every formulation of derived solidity, or independent MATHCERT certification. The protected admission and independent source-semantic audit remain distinct obligations.

Parent PR #3859 is merged. Parent PR #3864 (head f3df8edf1e329777f17b50f81101834485752937) was retargeted to main and native auto-merge enabled; its protected admission remains pending. The present candidate preserves the exact dependency closure of that parent and is not a protection bypass.
