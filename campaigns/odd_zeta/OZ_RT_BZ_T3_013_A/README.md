# OZ-RT-BZ-T3-013-A

Issue #949 admits and tests the first genuinely new T3 hypothesis class after structural closure of the T3-011 coordinate-zero Laurent response algebra and the negative T3-012-A/B bounded probes.

## New class

`SOURCE_QROW_CERTIFICATE_WEIGHTED_REDUCED_RESIDUAL_RESPONSE_001`

The protected reduced recurrence-residual target, support, harmonics, scalar namespace, and primitive correction columns are unchanged from T3-012-B. The only widening is the coefficient law on each protected correction column:

```text
span_Q { 1, rho(n,k,l), sigma(n,k,l) }
```

where `rho` and `sigma` are the two exact expressions in the currently admitted upstream source object

```text
rain-1/-odd-zeta-values-moremath
commit 6cc0bf07137815ceeef0d9f340559f85352391e5
work/lb5/Qrow_rhosigma.m
Git blob 61f12f412726887f506e1d423b7ee183a22116e5
```

No polynomial degree ladder, free denominator family, support widening, harmonic widening, scalar widening, recurrence refit, or recurrence-order change is admitted.

## Why this is not a recycled class

T3-011-R closed only the frozen coordinate-zero Laurent monomial response algebra. It explicitly excluded shifted poles and arbitrary rational functions. The pinned Q-row source functions are nonmonomial rational functions with non-coordinate denominator geometry, and the producer checks this source shape mechanically.

T3-008 searched a bounded polynomial-envelope two-flux ansatz on the original 198-dimensional raw-jet target. This operation acts after the T3-009 recurrence reduction, on the protected reduced-residual correction system, with fixed source functions rather than a free polynomial envelope.

T3-012-B excluded only the unchanged support-locked degree-zero correction class. Its contract explicitly leaves broader rational coefficient families outside scope. T3-013-A preserves that support but changes the coefficient law from constants to the exact source-defined Q-row basis.

## First exact gate

This operation deliberately reuses the exact two strict-interior sample points from T3-012-B:

```text
(8,1,2)
(9,2,1)
```

The sample set is not a cutoff defining the mathematical class. It is the exact inherited necessary subsystem that produced the T3-012-B obstruction, so it provides a controlled obstruction-escape test.

The producer first reconstructs the constant subspace and requires the protected predecessor rank pair `84/85`. If that control fails, the operation stops for semantic drift.

It then adds the exact `rho` and `sigma` weighted copies of every protected correction column and computes exact rational coefficient and augmented ranks in both pivot orders.

- If the enlarged system remains inconsistent, the exact declared source-weighted class is refuted because every global solution would have to satisfy this necessary subsystem.
- If the ranks become equal, only the known T3-012-B obstruction has been escaped. That is viability evidence; it is not a global certificate and does not prove the T3 identity.

The independent verifier reconstructs the protected target/support system, reparses the current admitted Q-row source through the predecessor's independent Taylor evaluator, rebuilds the weighted columns without importing the producer matrix, and replays the exact rank calculation.

## Claim boundary

Always retain for this gate:

```text
global_certificate_constructed = false
residual_sum_zero_proved = false
proof_effect = NONE
promotion_effect = NONE
t3_status = OPEN_WITH_CHARACTERIZED_BLOCKER
```

No T1-top, DEPTH, Sharp-12, primes `2,3`, formal, MATHCERT, companion/cuspidal, irrationality, infinitude, novelty, publication, patentability, deployment, product, or commercial claim is promoted by this operation.
