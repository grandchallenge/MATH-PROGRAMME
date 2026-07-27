# NS-CI-WP06 Literature Capsule

## Scope

This capsule records primary sources relevant to computational universality, undecidable dynamical behaviour, and blow-up mechanisms adjacent to the Navier–Stokes problem. It does not infer corresponding results for the true three-dimensional incompressible Navier–Stokes equations.

The source identities and stated uses were checked against the cited arXiv records on 2026-07-26.

## Source ledger

### Cardona, Miranda, Peralta-Salas, and Presas — Turing-complete Euler flow

**Source:** Robert Cardona, Eva Miranda, Daniel Peralta-Salas, and Francisco Presas, *Constructing Turing complete Euler flows in dimension 3*, arXiv:2012.12828.

**Audited use:** The authors construct a Turing-complete stationary Euler flow on a Riemannian three-sphere. This supplies computational universality and undecidable particle-path phenomena for a related inviscid fluid system.

**Transfer barrier:** The construction concerns stationary Euler flow on a selected Riemannian manifold. It does not supply a viscous simulation, admissible Euclidean Navier–Stokes initial data, a critical-integral correspondence, or a singularity theorem.

### Cardona, Miranda, and Peralta-Salas — universality and undecidability

**Source:** Robert Cardona, Eva Miranda, and Daniel Peralta-Salas, *Looking at Euler flows through a contact mirror: Universality and undecidability*, arXiv:2107.09471.

**Audited use:** The article surveys the geometric universality programme and proves further undecidability statements for dynamical properties of suitable Turing-complete stationary Euler or Beltrami flows, including periodic-orbit questions.

**Transfer barrier:** Orbit-property undecidability is not blow-up undecidability, and Euler trajectory dynamics do not automatically persist under viscosity.

### Tao — averaged Navier–Stokes blow-up

**Source:** Terence Tao, *Finite time blowup for an averaged three-dimensional Navier-Stokes equation*, arXiv:1402.0290.

**Audited use:** Tao constructs finite-time blow-up after replacing the true bilinear term by an averaged bilinear operator that retains the energy-cancellation identity. The result shows that energy cancellation and generic harmonic-analysis bounds alone are insufficient for a positive regularity proof.

**Transfer barrier:** The averaged bilinear operator is not the true Navier–Stokes nonlinearity. The result is a structural warning and a mechanism programme, not a counterexample to the Millennium problem.

### Huynh — undecidable blow-up for a smooth ODE

**Source:** Manh Khang Huynh, *A simple geometric construction of an ODE with undecidable blow-ups*, arXiv:2410.01455.

**Audited use:** The paper constructs a smooth finite-dimensional ODE for which finite-time blow-up is equivalent to the halting problem for a universal Turing machine.

**Transfer barrier:** The construction does not obey the Navier–Stokes equation, its pressure constraint, divergence-free geometry, energy inequality, or parabolic smoothing.

## Synthesis

The sources establish three separate facts:

1. some Euler flows can carry universal computation;
2. some smooth ODEs can make blow-up equivalent to halting;
3. an averaged Navier–Stokes model can blow up while preserving energy cancellation.

The missing theorem is not a citation-level gap. It is the construction and proof that joins the required properties inside the true viscous Navier–Stokes equation while discharging `U001–U010`.

## Search posture

Future audits should prioritize primary papers that discharge a named reduction obligation. Mere use of the words “universal,” “fluid computer,” “cascade,” “blow-up,” or “undecidable” is insufficient for promotion.
