# NS-CI-WP06: Undecidability and Reduction Lane

## Metadata

- Domain: Domain 02 — Three-Dimensional Incompressible Navier–Stokes / Critical Integrability
- Campaign: `NS-CI-001`
- Artifact ID: `NS-CI-WP06`
- Primary type: non-blocking investigatory lane
- Lifecycle status: `active`
- Disposition: `speculative_non_probative`
- Incoming dependencies: promoted `NS-CI-WP00`; source-normalized interfaces from `NS-CI-WP01` and `NS-CI-WP02`
- Certification target: human audit only
- Priority: medium and subordinate to the active WP01/WP02 mainline
- Governing decision: `ADR-0013`
- Review record: `reviews/navier_stokes/NS-CI-WP06.agent_review.yaml`
- Mainline effect: none; WP00–WP05 claim, promotion, and certification boundaries remain unchanged

## Result-status box

| Field | Value |
|---|---|
| Result status | Investigatory lane authorized |
| Strongest supported claim | Primary sources establish computational universality or undecidable events in specified adjacent systems; no transfer to the true viscous equation is established |
| Not claimed | Turing completeness, undecidable blow-up, singularity, or formal independence for the true 3D incompressible Navier–Stokes equations |
| Support-route class | `EXPLORATORY_EVIDENCE` and source audit only |
| Certification state | Not eligible for mathematical promotion |
| First executable step | Maintain the source ledger, reduction-obligation map, and bounded interface fixture |

## Exact research question

Determine whether there exists a computable encoding

```math
(M,x)\longmapsto u_{M,x}
```

from a Turing machine and input to admissible smooth, divergence-free initial data for the true unforced three-dimensional incompressible Navier–Stokes equations such that, relative to an explicitly fixed domain, solution class, solution quantifier, representation, and fluid event, the event is equivalent to the machine halting.

Candidate fluid events must remain distinct:

1. finite-time loss of smoothness;
2. divergence of a scale-critical norm or integral;
3. reachability of an open set in an observable state space;
4. occurrence of a specified Lagrangian trajectory event;
5. failure of an effective modulus of regularity.

No implication or equivalence among these events may be assumed.

## Why the lane is non-blocking

The active campaign seeks a critical-integrability estimate and its exact conditional-regularity interfaces. A computability reduction is neither required by that route nor evidence against it. This lane therefore:

- does not alter the theorem spine;
- does not authorize mechanism generation for the true equation;
- does not reopen WP03;
- does not weaken any source, data-class, or solution-class requirement;
- cannot promote a numerical or software observation into a continuum claim;
- cannot change the status of WP00–WP05.

## Reduction-obligation map

A valid many-one reduction into a Navier–Stokes decision problem must discharge every obligation below.

| ID | Obligation | Completion condition |
|---|---|---|
| `U001` | Computable encoding | An explicit algorithm emits represented admissible initial data from `(M,x)` |
| `U002` | Equation fidelity | The construction uses the true Navier–Stokes nonlinearity, pressure projection, and viscosity |
| `U003` | Admissible data | Smoothness, divergence freedom, decay or periodicity, finite energy, and effective representation are proved |
| `U004` | Uniform simulation | One construction works for all encoded machines and inputs |
| `U005` | Robust clock | Computational steps are represented without an unproved infinite-precision oracle |
| `U006` | Viscous persistence | Dissipation does not erase the encoded transition before it is used |
| `U007` | Halting witness | Halting implies the chosen fluid event |
| `U008` | Non-halting safety | Non-halting excludes the chosen fluid event |
| `U009` | Event decision profile | The target event is stated with exact quantifiers, representations, tolerances, and observation horizon |
| `U010` | Solution semantics | Domain, solution class, existence assumptions, uniqueness or selection rule, and universal/existential quantification over solutions are explicit |
| `U011` | Undecidability transfer | A stated computability-theoretic theorem transfers the two-way reduction to the exact represented target decision problem |
| `U012` | Independence transfer | Any independence claim names a formal system, arithmetizes the target statement, and proves the separate metamathematical bridge |

Failure of any one obligation terminates the proposed reduction or the stronger conclusion that depends on it. `U012` is required only for formal-independence language, but no such language is permitted without it.

## Claim boundary

The existence of Turing-complete Euler flows does not transfer automatically to viscous Navier–Stokes. Blow-up in an averaged Navier–Stokes model does not establish blow-up in the true equation. Undecidable blow-up for a smooth finite-dimensional ODE does not establish undecidable blow-up for a PDE. Even undecidability of an instance family associated with individual initial data would not by itself settle the single universal Clay statement or prove independence from a named formal system.

The bounded software fixture under `experiments/ns_wp06_undec/` is an interface test only. It is not a PDE solver, reduction, non-halting oracle, or mathematical witness.

## Governed deliverables

1. `01_LITERATURE_CAPSULE.md`
2. `02_COMPUTABILITY_RISK_LEDGER.md`
3. `03_REVIEW_CHECKLIST.md`
4. `experiments/ns_wp06_undec/halting_gate_fixture.py`
5. `tests/test_ns_wp06_halting_gate_fixture.py`
6. `docs/decisions/ADR-0013_NS_WP06_UNDECIDABILITY_LANE.md`
7. `reviews/navier_stokes/NS-CI-WP06.agent_review.yaml`

## Escalation gate

Escalation beyond literature and bounded interface fixtures requires all of:

- [ ] a true-equation construction, not an averaged or altered nonlinearity;
- [ ] explicit effectively represented admissible initial data;
- [ ] an exact solution class and solution quantifier;
- [ ] a two-way halting/event proof;
- [ ] an adversarial precision and robustness audit;
- [ ] a computability-theoretic transfer theorem for the represented decision problem;
- [ ] a separate formal-system-relative theorem before any independence claim;
- [ ] a new Council decision authorizing the next stage.

Until then, the lane remains non-blocking and non-probative.