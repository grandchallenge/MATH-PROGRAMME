# ADR-0013: Authorize a non-probative Navier–Stokes undecidability lane

## Status

Accepted, 2026-07-26, for active non-blocking investigatory use.

## Context

Computational universality and undecidable dynamical properties are known in systems adjacent to the three-dimensional incompressible Navier–Stokes problem. Relevant examples include stationary Euler flows, smooth finite-dimensional ODEs with halting-equivalent blow-up, and an averaged Navier–Stokes model with finite-time blow-up.

These results do not transfer automatically to the true viscous equation. They also do not identify undecidability of an instance family with formal independence of the universal Clay statement. An investigatory lane is useful only if those separations are made explicit and the active critical-integrability work remains unaffected.

## Decision

1. Establish `NS-CI-WP06` as a non-blocking, non-probative investigatory lane under Domain 02.
2. Keep the active WP01/WP02 analytic mainline and all WP00–WP05 claim and promotion states unchanged.
3. Require every proposed reduction to discharge obligations `U001–U010`, including true-equation fidelity, admissible data, robust finite-precision simulation, both reduction directions, and an explicit transfer metatheorem.
4. Separate four layers without implicit arrows:
   - dynamics or simulation capacity;
   - an encoded instance-family decision problem;
   - the universal mathematical statement under investigation;
   - formal independence relative to a named formal system.
5. Classify the software fixture as bounded `EXPLORATORY_EVIDENCE`. It is an interface test, not a PDE simulation, reduction, non-halting oracle, or singularity witness.
6. Require experiment modules to remain library-only and reachable through the repository-wide unit-test gate.
7. Permit only literature audit, obligation mapping, risk analysis, and bounded interface fixtures at the current stage.
8. Require a new Council decision before any true-equation construction, mechanism campaign, or mathematical escalation begins.

## Alternatives considered

### Reject the lane as irrelevant

Rejected. The computability perspective can expose hidden representation, robustness, and quantifier obligations even when it does not solve the active problem.

### Treat related-system universality as evidence for the true equation

Rejected. Euler flow, averaged Navier–Stokes, finite-dimensional ODEs, and the true viscous equation have materially different structures and admissibility requirements.

### Equate undecidability with independence

Rejected. Undecidability of a represented instance family and independence of a fixed universal sentence are distinct claims requiring different metatheorems.

### Make the lane part of the active proof route

Rejected. No reduction obligation is currently discharged at theorem level, and the active critical-integrability programme does not depend on this lane.

## Consequences

- The programme gains a governed place to audit computability claims without distorting the main theorem spine.
- Related-system results remain literature evidence only.
- The bounded fixture can falsify software-interface assumptions but cannot support continuum or metamathematical claims.
- Any attempted escalation fails closed when one of `U001–U010` remains open.
- Mainline resource priority remains with WP01/WP02 and the equation-specific critical-integral routes.

## Affected artifacts

- `DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md`
- `DOMAIN_REGISTRY.yaml`
- `campaigns/navier_stokes_critical_integrability/WP06_UNDECIDABILITY_REDUCTION_LANE/`
- `experiments/ns_wp06_undec/`
- `tests/test_ns_wp06_halting_gate_fixture.py`
- `reviews/navier_stokes/NS-CI-WP06.agent_review.yaml`
- governance, inventory, terminology, and public-domain records

## Claim boundary

This decision does not claim Turing completeness, undecidable blow-up, singularity, noncomputability of the critical integral, or formal independence for the true three-dimensional incompressible Navier–Stokes equations. It authorizes only a governed investigatory lane.

## Supersession

This decision extends ADR-0003. It does not supersede ADR-0003’s analytic campaign authority, any WP00–WP05 review, or any mathematical claim ledger.
