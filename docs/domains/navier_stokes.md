# Domain 02 · Navier–Stokes Critical Integrability

**Campaign ID:** `NS-CI-001`  
**Mathematical status:** open problem  
**Primary setting:** three-dimensional incompressible Navier–Stokes on `R^3`  
**Governance:** `ADR-0003`

## Canonical challenge

For smooth rapidly decreasing divergence-free initial data and a Leray–Hopf weak solution, determine whether the critical quantity

```text
integral from 0 to T of ||u(t)||_L6^4 dt
```

is finite for every finite `T`.

This is the critical Ladyzhenskaya–Prodi–Serrin pair `(q,p)=(4,6)`. Any result for a narrower data class or a different spatial domain remains a restricted result until an explicit extension theorem is proved.

## Programme posture

WP00 normalized the problem and source boundary. WP01 and WP02 catalogued false routes and conditional regularity facts. Later work isolated restricted targets and tested equation-specific mechanisms. No route is promoted merely because it produces numerically plausible dissipation, excursion persistence, or generic decorrelation.

## Canonical artifacts

- [Domain master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md)
- [Campaign directory](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/navier_stokes_critical_integrability)
- [Review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/navier_stokes)
- [Governing decision ADR-0003](../decisions/ADR-0003_NAVIER_STOKES_CRITICAL_INTEGRABILITY.md)

## Claim boundary

The campaign has not proved regularity, global smoothness, or the universal critical-integral estimate. Restricted estimates, negative results, and route terminations are retained as controlled changes in the search space.