# OZ-RT-BZ-T3-012-B

Issue #927 tests the first coupled correction-layer mechanism after the T3-011 multiplier family and T3-012-A recurrence-operator tangent gate closed negatively.

The protected T3-010-C degree-zero correction class is individually one-rank inconsistent in each symmetry-reduced channel. The protected T3-009 architecture nevertheless requires the channel construction split to be recombined according to the actual one-orientation Q-row functional before that local inconsistency can be used against the coupled class.

## Diagnostic projection tranche

The producer first reconstructs the complete protected T3-010-C systems and applies four increasingly permissive exact-Q projections. Every diagnostic quotient remains inconsistent by one rank:

- `erase_partition_only`: `311/312`;
- `erase_scalar_labels`: `303/304`;
- `retain_shell_erase_rational_labels`: `155/156`;
- `erase_rational_coefficient_labels`: `57/58`.

These projections remain discovery-only. None is used as the terminal negative witness.

## Source-functional negative witness

The decisive tranche binds `work/lb5/Qrow_rhosigma.m` at Git blob `61f12f412726887f506e1d423b7ee183a22116e5` and 44,980 bytes. It reconstructs the exact symmetric one-orientation scalar multipliers for `TN1`, `TN2`, `TN3`, `SK`, `AK`, `LKK`, and `LLK`, including the doubled spatial orientation, and replays the protected Q-row identity at two regular strict-interior points: `(8,1,2)` and `(9,2,1)`.

For the unchanged 506 shared support-locked degree-zero correction columns, the exact strict-interior necessary subsystem has coefficient rank `84` and augmented rank `85`, with 298 target coordinates and nullity 422. It is therefore inconsistent.

The producer and verifier establish this independently. The producer uses derivative-tuple jets and forward exact sparse elimination. The verifier uses a separate truncated bivariate Taylor algebra and reverse exact elimination. The verifier does not import producer source jets, projected matrices, or rank computations as authority.

This finite specialization is used only as an exact nonexistence witness. Any global correction in the declared shared-coefficient class would have to satisfy every valid regular strict-interior specialization of the protected source identity. Because this exact restriction is inconsistent, no such global correction exists in the declared class. Shell regularization cannot repair the contradiction because no shell point enters either witness.

This is not a finite-grid proof of a positive identity. The operation does not claim to have materialized every shell row of the global recombination map, and it does not prove the T3 residual sum vanishes.

## Terminal

`SUPPORT_LOCKED_DEGREE0_COUPLED_CORRECTION_RECOMBINATION_INCOMPATIBLE`

The terminal excludes only `SUPPORT_LOCKED_ORIENTED_ONE_BODY_DEGREE0_WEIGHT_CORRECTION_001`. It does not exclude broader rational coefficient families, support or harmonic widenings, higher-order operator deformations, or different certificate architectures.

Claim firewall:

- `residual_sum_zero_proved=false`
- `proof_effect=NONE`
- `promotion_effect=NONE`
- `t3_status=OPEN_WITH_CHARACTERIZED_BLOCKER`
