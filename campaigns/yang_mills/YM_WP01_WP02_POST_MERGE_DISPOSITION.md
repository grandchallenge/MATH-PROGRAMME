# YM-WP01 / YM-WP02 — Post-merge disposition and downstream gate reconciliation

**Campaign:** `YM-001`  
**Decision date:** 2026-09-16  
**Protected Programme predecessor:** `52e2e3df6ac54ab63a03c867b2b82a80d93ee577`  
**Mathematical status:** `OPEN PROBLEM`  
**Disposition:** `PROMOTED_AS_BOUNDED_INFRASTRUCTURE__RESTRICTED_TARGET_SELECTION_OPEN_IN_MATHSOLVE`

## Purpose

This record supersedes the pre-promotion status wording retained inside the frozen July 2026 WP01/WP02 candidate package. It changes documentary lifecycle and research routing only. It does not strengthen any Yang–Mills theorem claim.

The historical files under `WP01_FALSE_PROOF_ATLAS/` and `WP02_THEOREM_LEDGER/` remain immutable evidence of the package state at freeze. Their embedded closed gate remains a historical snapshot. The current routing authority after protected admission of this record is `campaigns/yang_mills/YM_CURRENT_ROUTING_GATE.json`.

## Repository integration and CI evidence

`YM-WP01` and `YM-WP02` were integrated through MATH-PROGRAMME PR #115.

- exact candidate head: `b55062d2d7de18ac6d0e5c1c943d530c53aae211`;
- protected merge: `54f233a2c3b0d91451f6900247e941d08eb0779f`;
- Programme policy workflow run: `30356885663`;
- workflow conclusion: `success`.

This discharges the repository-integration / CI substance retained as `YM-WP01-REV-001` and `YM-WP02-REV-001`. The frozen legacy review files remain unchanged and are superseded only for current routing by this exact disposition.

## Independent source-locator and theorem-body evidence

MATHFORGE now provides protected provider evidence:

1. `sources/YM-001/YM_D006_D009_EXTERNAL_SOURCE_AUDIT.md`, admitted at protected Forge merge `bfe09a5eff15de228a1855a1742bea68ef705a54`;
2. `sources/YM-001/YM_WP02_SOURCE_LOCATOR_SCOPE_REVIEW.md`, admitted at protected Forge merge `e4c6b668d28afa5f7557e6fddf31eb105a69a4a8`.

The source-locator review covers all 21 WP02 imported sources. The theorem-body audit resolves the source ambiguity that mattered for `YM-D006` through `YM-D009`.

This discharges the source-review substance retained as `YM-WP02-REV-002`.

## D003 theorem-interface supplement — 2026-09-18

A later protected Forge audit at `a609f40e809ebe74f35dc4ceb069c15e4d21f26e` adds the missing Balaban large-field/ultraviolet-stability spine and the qualified Magnen–Rivasseau–Sénéor fixed-infrared-cutoff construction.

Current theorem interfaces are recorded in:

`campaigns/yang_mills/YM_D003_UV_LARGE_FIELD_SUPPLEMENT.json`.

This refines, but does not discharge, `YM-D003`:

- Balaban large-field control and four-dimensional ultraviolet stability are materially available as bounded inputs;
- MRS supplies a qualified source-stated ultraviolet-cutoff-removal construction for pure `SU(2)` at fixed infrared cutoff;
- infrared-cutoff/infinite-volume removal remains open;
- uniqueness and full identification of the continuum theory remain open;
- the complete OS profile remains open and coupled to `YM-D002`;
- a finite nonzero non-circular physical reference scale remains open and coupled to `YM-D001`.

The current D003 frontier is therefore:

`BALABAN_4D_UV_STABILITY_AND_LARGE_FIELD_CONTROL_AVAILABLE__IR_REMOVAL_UNIQUENESS_OS_AND_PHYSICAL_IDENTIFICATION_OPEN`.

This supplement does not change the routing gate: `YM-D003` remains an admissible native Solve target and remains an open research debt.

## Referee debt disposition

The nine protected debts are dispositioned as follows for the purpose of downstream routing.

| Debt | Current disposition | Routing effect |
|---|---|---|
| `YM-D001` | `OPEN_RESEARCH_DEBT` — regulator-survival spectral bridge remains unproved | admissible native Solve target surface |
| `YM-D002` | `OPEN_RESEARCH_DEBT` — full limiting OS hierarchy remains unproved | admissible native Solve target surface |
| `YM-D003` | `OPEN_RESEARCH_DEBT` — Balaban 4d large-field/UV stability now admitted as bounded input; IR/infinite-volume removal, uniqueness/full identification, OS, and physical scaling remain open | admissible native Solve target surface |
| `YM-D004` | `OPEN_RESEARCH_DEBT` — local gauge-invariant observable renormalization remains unproved | admissible native Solve target surface |
| `YM-D005` | `OPEN_RESEARCH_DEBT` — converse Euclidean-decay / physical-spectrum bridge remains unproved | admissible native Solve target surface |
| `YM-D006` | `SOURCE_AMBIGUITY_CLOSED` — audited near-vacuum/truncated partition-function result supplies no composable continuum/gap bridge | no target bypass |
| `YM-D007` | `SOURCE_ROUTE_NONCOMPOSABLE_AS_WRITTEN` — complete-solution route fails at its displayed weak-coupling convergence step | no target bypass; reopen only on material source revision |
| `YM-D008` | `SOURCE_ROUTE_NONCOMPOSABLE_AS_WRITTEN` — continuum spectral-gap proof contains an unclosed operator-inequality step | no target bypass; reopen only on material source revision |
| `YM-D009` | `FIXED_REGULATOR_BOUNDARY_ESTABLISHED` — current lattice manuscript explicitly leaves continuum gap survival open | no target bypass |

An open research debt is not a failed promotion condition when the downstream lane being opened exists specifically to attack that debt. It remains a hard claim boundary. A restricted target must state exactly which debt it narrows and which hypotheses it imports.

## Referee disposition

The repository/CI, source-locator, source-body, composition-state, debt-coverage, and claim-boundary obligations needed for **restricted-target selection** are now discharged.

`YM-WP01` is promoted as eliminative false-proof infrastructure.

`YM-WP02` is promoted as a source-normalized theorem/dependency interface ledger.

The following lane is opened:

- native MATHSOLVE restricted-target selection against `YM-D001` through `YM-D005`.

The following lanes remain closed:

- unrestricted mechanism generation;
- numerical experimentation not subordinate to an admitted exact target;
- novelty or priority claims;
- any assertion that `YM-D001` through `YM-D005` has already been solved;
- any terminal Yang–Mills existence or physical-mass-gap claim.

The first native Solve target must satisfy the 18-field restricted-target contract and must begin proof/falsification work immediately after selection. Historical Programme scorecard machinery is not to be restarted or copied into Solve.

## Exact next package

The authorized next package is a native MATHSOLVE target-selection/theorem-development tranche for `YM-001`.

- target repository: `grandchallenge/MATHSOLVE`;
- predecessor Solve protected head at this reconciliation's preflight: `b0854bb7770296b610b655753bc62b27365b27bb`;
- predecessor source authority: MATHFORGE protected head `e4c6b668d28afa5f7557e6fddf31eb105a69a4a8`;
- admissible theorem frontier: `YM-D001` through `YM-D005`;
- preferred first action: generate a small mathematically distinct candidate set, falsify against WP01/WP02, select the smallest exact target that materially narrows one protected debt, freeze its contract, and begin the proof attempt.

The exact Solve head must be re-fetched before mutation; the SHA above is a routing predecessor, not an authorization to ignore later drift.

## Claim boundary

This disposition does not construct four-dimensional quantum Yang–Mills theory, prove a physical mass gap, confinement, an area law, regulator-independent continuum control, a complete OS hierarchy, or novelty. It changes only the research-routing state needed to attack the remaining mathematical debts in the repository that owns new theorem work.
