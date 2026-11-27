# CM5 R0: dyadic compact-box acyclicity (033)

## Result

For any profinite probe S and any set-indexed product B of nonempty closed real intervals [a_i,b_i], including degenerate intervals, the genuine free condensed module on S × B is acyclic in every positive Ext degree against the discrete integer coefficient object.

The endpoint declaration is `probe_box_extPositive_zero` in
`CMDGCondensedCM4P3DerivedCM5R0CompactBoxProbeAcyclic.lean`.
The hypotheses are coordinatewise a_i ≤ b_i; no finite-dimensionality,
metrizability or countability of the box or probe is required.

## Proof architecture

1. Ordered lists, not sorted simplices, carry the alternating deletion differential. The signed prism satisfies the full chain homotopy identity, including repeated vertices. Coordinatewise clamps preserve the adjacency condition of the finite cell grid and contract it to zero.
2. A binary prefix of length m and index k has full closed image [k/2^m,(k+1)/2^m]. The tail expansion proves this including both endpoints.
3. Observations of actual equal-image tuples on finitely many axes have exactly the admissible ordered grid tuples as image. A common coordinatewise endpoint gives a lift; unobserved coordinates are fixed.
4. A locally constant integer cochain on the closed relation extends to the surrounding profinite product. Compactness gives finite coordinate dependence. Thus it descends to a finite-axis, finite-prefix observation, with face maps and differential preserved.
5. The grid primitive pulls back to a locally constant primitive on the genuine relation. The compact-cover Ext transfer of 032 proves positive Ext vanishing on the unit cube.
6. Affine maps with continuous sections exhibit general nonempty closed boxes, including singleton factors, as retracts of the unit cube. Positive Ext vanishing passes to these retracts.
7. The equal-image relation of the product cover with S is naturally S times the cube relation. The tube lemma shows that a jointly locally constant cochain on a compact fiber determines a locally constant family of whole fiber cochains. Choosing a primitive per cocycle and gluing the family proves probe-wise acyclicity. The affine retract then gives the asserted general box theorem over S.

## Evidence and scope

The eleven new modules passed local Lean 4.33.0-rc1 checking on the native SSD workspace, using the pinned Mathlib revision
`79d0395a1825a6264ad5d269e35e60537518955e`. In particular, the final probe theorem (local execution capture `72e65b3101d24bebb1eaebf8140e8cb5`) reports only propext, Classical.choice and Quot.sound. These are local kernel checks, not independent certification or protected admission. Native exact-head CI and protected integration are separate obligations.

The compact-cover resolution parent was admitted via PR #3807. The successor also contains the previously locally checked Ext comparison of 032.

This result concerns free condensed modules on compact boxes; it does not assert the vanishing for the condensed abelian group of real-valued functions itself. Passage from boxes to the real product, compatibility with the degree-zero projection, continuity and the final derived duality comparison are distinct obligations. No claim of the final CM5 unit equivalence is made.
