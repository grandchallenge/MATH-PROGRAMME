# NS-CI-WP04 — Initial triage decision

## Decision

Record `NS-CI-R014-A2` as the provisional leading restricted target. Retain `NS-CI-R014-E1` as the bridge-theorem fallback. Keep `NS-CI-R014-D1` on the shortlist only under explicit formulation debt.

No target is selected or Referee-promoted by this decision.

## Basis

### A2

A2 asks whether critical time integrability of the Cheskidov–Shvydkoy dissipation wavenumber,

```math
\Lambda\in L^2(0,T),
```

forces

```math
\int_0^T\|u(t)\|_6^4dt<\infty.
```

It is source-anchored, scaling-critical, independently stated, and lies between audited universal `L1_t` information and a known stronger `L5/2_t` sufficient criterion. Its main obstruction is explicit: elementary low-frequency estimates produce a product of two `L1_t` quantities, which does not close without a new equation-specific estimate.

### D1

D1 targets the exact cutoff and mollification losses exposed by WP01. It is not currently theorem-grade because its compensated enstrophy inequality already contains the desired closure. An independent observable hypothesis `H_D` must be supplied before D1 can compete for selection.

### E1

E1 cleanly resolves the compact-support-to-Schwartz and one-solution-to-every-solution bridges under a uniform critical bound. It is likely tractable through compactness, lower semicontinuity, LPS regularity, and weak–strong uniqueness, but the uniform approximation bound carries the substantive regularity content. Its leverage is therefore lower than A2's.

## Generic family dispositions

- generic geometric depletion: rejected as an established theorem family unless an exact distinct quantitative bridge is supplied;
- generic concentration/sparsity: rejected as an established theorem family with an audited unclosed scaling gap;
- generic symmetry classes: rejected as classical or low-leverage;
- recent 2026 arbitrary-swirl and broader global-regularity claims: diverted to MATHFORGE claimed-proof issue `#20` without acceptance.

## Required work before selection

1. confirm the exact prior-art boundary for A2;
2. replay WP01 against every attempted A2 estimate;
3. determine whether the product-of-`L1` obstruction admits a frequency-localized Navier–Stokes bypass;
4. supply an independent D1 hypothesis or terminate D1;
5. normalize E1's approximation topology and imported compactness interfaces;
6. complete MATHCERT scaling and quantifier fixtures;
7. obtain Referee selection or a no-selection disposition.

## Governance boundary

This decision does not establish novelty, prove A2, accept any recent claimed proof, authorize WP03, or change the open status of universal critical integrability.