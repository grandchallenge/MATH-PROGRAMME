# PC-WP02 — Source-normalized Hamilton–Perelman theorem ledger

## Status

- Campaign: `PC-001`
- Work Package: `PC-WP02`
- Tracker: `MATH-PROGRAMME#73`
- Input: Referee-reviewed `PC-WP00`
- State: `INTEGRATION_READY_AT_THEOREM_INTERFACE_LEVEL`
- Primary route: Poincaré-specific Ricci flow with surgery and finite extinction
- Claim boundary: literature reconstruction, not independent proof of the nonlinear analytic core

## Purpose

This ledger turns the phrase “by Perelman” into an explicit chain of theorem interfaces. Each interface records:

- the exact object and hypothesis profile;
- the conclusion actually consumed downstream;
- scale and parameter conventions;
- primary and reconstruction sources;
- known correction or version notes;
- adversarial guards from `PC-WP01`;
- formalization status.

The package is source-normalized when a specialist can trace every edge from a closed topological input to the terminal connected-sum classification without relying on an unnamed theorem or an ambiguous source version.

## Poincaré-specific chain

```text
PC02-T001  dimension-three Top/PL/Diff bridge
PC02-T002  smooth metric and short-time Ricci flow
PC02-T003  W-entropy monotonicity
PC02-T004  reduced distance and reduced-volume monotonicity
PC02-T005  pseudolocality
PC02-T006  no-local-collapsing
PC02-T007  ancient kappa-solutions and compactness
PC02-T008  canonical-neighbourhood theorem
PC02-T009  standard cap solution
PC02-T010  delta-neck surgery and pinching preservation
PC02-T011  noncollapsing through surgery
PC02-T012  strong canonical neighbourhoods for surgery flow
PC02-T013  all-time Ricci flow with surgery; locally finite surgery times
PC02-T014  topology of surgery and discarded components
PC02-T015  simply connected input satisfies the extinction hypothesis
PC02-T016  finite-time extinction
PC02-T017  finite surgery history and connected-sum reconstruction
PC02-T018  terminal fundamental-group elimination
PC02-T019  smooth and topological Poincaré conclusions
```

## Source tiers

### Primary

- `P-I`: Perelman, *The entropy formula for the Ricci flow and its geometric applications*, arXiv:`math/0211159`.
- `P-II`: Perelman, *Ricci flow with surgery on three-manifolds*, arXiv:`math/0303109`.
- `P-III`: Perelman, *Finite extinction time for the solutions to the Ricci flow on certain three-manifolds*, arXiv:`math/0307245`.

### Detailed reconstruction

- `MT`: Morgan–Tian, *Ricci Flow and the Poincaré Conjecture*, Clay Mathematics Monographs 3.
- `KL`: Kleiner–Lott, *Notes on Perelman's Papers*, versioned arXiv:`math/0605667` / Geometry & Topology 12.

### Foundational imports

- `MOISE`: dimension-three triangulation and Hauptvermutung;
- `SMOOTH`: compatible smoothing results;
- `HAM`: short-time Ricci-flow and precursor singularity theory;
- `KM`: Kneser–Milnor prime decomposition;
- `VK`: van Kampen/free-product calculations.

## Source correction policy

The ledger does not flatten the three Perelman preprints into one undifferentiated source. `P-II` explicitly corrects inaccuracies and withdraws or defers selected assertions from `P-I`. `KL` is used as an independent correction and detail audit for `P-I` and `P-II`. `KL` does not supply the finite-extinction proof; the finite-extinction lane is sourced to `P-III` and `MT`.

## Parameter discipline

The surgery construction uses an ordered hierarchy rather than a single “small surgery parameter.” The ledger distinguishes:

- `epsilon`: canonical-neighbourhood approximation accuracy;
- `r`: scale below which sufficiently high curvature has a canonical neighbourhood;
- `kappa`: quantitative noncollapsing constant;
- `delta`: neck quality allowed for surgery;
- `h`: surgery-neck radius selected from the preceding data;
- `D`: curvature cutoff multiplier associated with the surgery scale;
- stagewise sequences and time-dependent controls.

No consumer may reverse the dependency order or treat these constants as universal without their stage and source conventions.

## Principal theorem boundaries

### Analysis-to-surgery boundary

Entropy, reduced geometry, pseudolocality, and no-local-collapsing do not themselves perform surgery. They supply compactness and scale control for classifying high-curvature regions.

### Surgery-to-topology boundary

Surgery existence is not topology preservation. A separate theorem records cuts, caps, discarded components, and connected-sum reconstruction.

### Extinction-to-classification boundary

Finite extinction is not the Poincaré conclusion. It becomes topologically informative only when combined with the surgery history and the permitted terminal factors.

### Classification-to-Poincaré boundary

The final simply connected discharge computes fundamental groups of the permitted factors. It does not invoke “every simply connected prime is `S^3`.”

## Deliverables

- `01_SOURCE_LEDGER.yaml`: source identities, scope, and correction state;
- `02_THEOREM_CROSSWALK.md`: source and numbering map;
- `03_PARAMETER_REGISTRY.md`: scale and dependency conventions;
- `04_SOURCE_NORMALIZED_THEOREMS.md`: theorem interfaces and consumers;
- `05_FINITE_EXTINCTION_LEDGER.md`: extinction mechanism and topology discharge;
- `06_DEPENDENCY_DAG.json`: machine-readable chain and adversarial guards;
- `09_PROOF_DEBT.json`: remaining source and reconstruction debt;
- `10_CLAIM_LEDGER.yaml`: promoted and bounded claims;
- `11_CERT_HANDOFF.md`: delimited MATHCERT targets;
- `12_NEXT_EXECUTABLE_STEP.md`: joint WP01/WP02 gate.

## Result

WP02 reconstructs the proof architecture at theorem-interface level and exposes the remaining line-by-line analytic debt. It is suitable for joint Agent Council review with WP01. It is not a replacement for Perelman's proofs or their detailed reconstructions, and it does not authorize a claim that the Hamilton–Perelman analytic core has been independently verified or formalized.
