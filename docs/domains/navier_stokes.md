# Domain 02 · Navier–Stokes Critical Integrability

**Millennium status, 20 October 2026:** Clay lists the *parent* Navier–Stokes problem as **Active** after the [8 September announced finite-time breakdown proof](https://openai.com/index/navier-stokes-solution/). Its [11 September statement](https://www.claymath.org/news/navier-stokes-announcement/) says the problem had *apparently been settled*, but the evaluation process continues. GCL does not independently certify that proof. Importantly, the distinct **unforced NS-CI-001 critical-integrability question** below remains open. [See the seven-problem status](../MILLENNIUM_PRIZE_STATUS.md).

## The question in everyday language

The Navier–Stokes equations describe the movement of fluids, including water and air. A central open question asks whether smooth three-dimensional flows can develop a mathematical singularity, a point at which the usual smooth description fails.

GCL studies a narrower test involving the size of a solution over time. Even a successful estimate for that test would need further reasoning before it settled the general smoothness problem.

**What remains uncertain:** the central three-dimensional problem is unsolved. Results about related equations or computer simulations cannot automatically be transferred to the exact Navier–Stokes equations.

## Detailed research record

**Accessible research guide:** [NS-CI-001 Research Guide](NS_CI_001_RESEARCH_GUIDE.md)


!!! info "Research surface authority"
    **LIVE:** https://github.com/grandchallenge/MATH-PROGRAMME/issues/55  
    **AUTHORITY:** `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`.  
    **EXPOSITION:** this page is the human-facing projection; the issue governs mutable research state and protected records govern admitted claims.

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
