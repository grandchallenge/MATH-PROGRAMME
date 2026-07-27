# Domain 02 · Navier–Stokes Critical Integrability

**Campaign ID:** `NS-CI-001`  
**Mathematical status:** open problem  
**Primary setting:** three-dimensional incompressible Navier–Stokes on `R^3`  
**Governance:** `ADR-0003`; `ADR-0013`

## Canonical challenge

For smooth rapidly decreasing divergence-free initial data and a Leray–Hopf weak solution, determine whether the critical quantity

```text
integral from 0 to T of ||u(t)||_L6^4 dt
```

is finite for every finite `T`.

This is the critical Ladyzhenskaya–Prodi–Serrin pair `(q,p)=(4,6)`. Any result for a narrower data class or a different spatial domain remains a restricted result until an explicit extension theorem is proved.

## Programme posture

WP00 normalized the problem and source boundary. WP01 and WP02 catalogued false routes and conditional regularity facts. Later work isolated restricted targets and tested equation-specific mechanisms. No route is promoted merely because it produces numerically plausible dissipation, excursion persistence, or generic decorrelation.

`NS-CI-WP06` is a separate non-blocking computability and reduction lane. It audits whether a genuine reduction from halting to a precisely represented event of the true viscous equation could exist. Current evidence concerns related Euler flows, modified equations, finite-dimensional ODEs, and a bounded software interface fixture. None of those artifacts supports Turing completeness, undecidable blow-up, singularity, noncomputability of the critical integral, or formal independence for the true equation.

## Canonical artifacts

- [Domain master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md)
- [Campaign directory](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/navier_stokes_critical_integrability)
- [WP06 undecidability lane](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/campaigns/navier_stokes_critical_integrability/WP06_UNDECIDABILITY_REDUCTION_LANE)
- [Review records](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/reviews/navier_stokes)
- [Governing decision ADR-0003](../decisions/ADR-0003_NAVIER_STOKES_CRITICAL_INTEGRABILITY.md)
- [WP06 decision ADR-0013](../decisions/ADR-0013_NS_WP06_UNDECIDABILITY_LANE.md)

## Claim boundary

The campaign has not proved regularity, global smoothness, the universal critical-integral estimate, a true-equation computational simulation, undecidability, or formal independence. Restricted estimates, negative results, route terminations, literature audits, and bounded interface fixtures are retained only as controlled changes in the search space.
