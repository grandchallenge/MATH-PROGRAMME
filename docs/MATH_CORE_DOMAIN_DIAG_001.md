# MCORE-DOMAIN-DIAG-001

`MCORE-DOMAIN-DIAG-001` is the first deterministic query surface over the protected Condensed Mathematics MATH-CORE shadow. It is an observation-only diagnostic. It does not create a live coordinator, allocate work, prune search, certify mathematics, promote claims, or alter source state.

## Authority and source identity

The diagnostic is bound to protected `MATH-PROGRAMME` checkpoint:

`03ca91bf486d38007799bee0b0552afbfb61245c`

Its sole domain-state input is:

`governance/math_core_domain_shadow_condensed_001.json`

with Git blob SHA-1:

`c95e5dc79f1138b1066db42fefe4c56b0cc81c84`

The validator recomputes that blob identity and revalidates the underlying `MCORE-DOMAIN-SHADOW-001` semantics before accepting the diagnostic artifact. The diagnostic is therefore a deterministic projection of already protected state, not a second source of authority.

## What it exposes

The diagnostic exposes six read-only query forms:

```text
summary
frontier
node <node_id>
ancestry <node_id>
blockers [--class BLOCKER_CLASS]
evidence <node_id>
```

Run them from the repository root, for example:

```bash
python3 tools/math_core_domain_diag.py summary
python3 tools/math_core_domain_diag.py frontier
python3 tools/math_core_domain_diag.py blockers --class MATHEMATICAL
python3 tools/math_core_domain_diag.py node MCORE:CONDENSED:CM4:P3
python3 tools/math_core_domain_diag.py ancestry MCORE:CONDENSED:CM4:P6
python3 tools/math_core_domain_diag.py evidence MCORE:CONDENSED:CM4:P3
```

Every invocation validates the diagnostic artifact against the protected shadow before emitting output.

## Protected lineage view

The diagnostic preserves the current protected dependency lineage without rewriting historical source records:

| Ordinal | Node | Current protected status |
|---:|---|---|
| 1 | `MCORE:CONDENSED:CM1` | `PROTECTED_CLOSED` |
| 2 | `MCORE:CONDENSED:CM2` | `PROTECTED_CLOSED` |
| 3 | `MCORE:CONDENSED:CM3` | `PROTECTED_CLOSED` |
| 4 | `MCORE:CONDENSED:C05` | `PROTECTED_CLOSED_DEFINITION_BOUNDARY` |
| 5 | `MCORE:CONDENSED:CM4` | `OPEN_UNCERTIFIED` |

The C05 status remains a definition-boundary authority. It is not interpreted as unrestricted general-ring semantic authority or as a nontrivial solid-object theorem.

## Current CM4 frontier

| Item | Diagnostic role | Current status | Dependencies | Blocker classes |
|---|---|---|---|---|
| `CM4-P1` | `AVAILABLE` | `AVAILABLE` | none | none |
| `CM4-P2` | `DISCHARGED` | `PROTECTED_CLOSED` | none | none |
| `CM4-P3` | `BLOCKING` | `OPEN_WITH_CHARACTERIZED_BLOCKER` | none recorded | `MATHEMATICAL`, `FORMALIZATION` |
| `CM4-P4` | `BLOCKING` | `BLOCKING` | `CM4-P5` | `MATHEMATICAL`, `FORMALIZATION` |
| `CM4-P5` | `BLOCKING` | `BLOCKING` | none recorded | `MATHEMATICAL`, `FORMALIZATION` |
| `CM4-P6` | `PARTIAL_BLOCKING` | `PARTIAL_BLOCKING` | `CM4-P3`, `CM4-P4` | `MATHEMATICAL`, `FORMALIZATION` |

`CM4-P2` is discharged and is rejected if reintroduced as a blocker. `CM4-P3` remains narrowed to the missing profinite/discrete acyclicity specialization or a certified underived reduction; generic Ext and sheaf-cohomology infrastructure are not represented as missing execution infrastructure.

The dependency structure is descriptive, not an optimization result. It does not establish that any dependency is minimal, unique, globally complete, or the preferred research priority.

## Blocker taxonomy

The diagnostic carries the controlled four-way blocker taxonomy:

- `MATHEMATICAL` — unresolved mathematical content;
- `FORMALIZATION` — unresolved formal interface or proof realization;
- `GOVERNANCE_EVIDENCE` — missing or insufficient governed evidence;
- `EXECUTION_INFRASTRUCTURE` — missing runtime or execution machinery.

The present protected CM4 frontier records mathematical and formalization blockers. It does not currently justify an `EXECUTION_INFRASTRUCTURE` blocker.

## Evidence and ancestry semantics

`ancestry` reports the protected lineage leading to the requested lineage/frontier node. It is not a proof of dependency minimality or necessity beyond the represented governed edges.

`evidence` reports a node's source operation, source reference, authority class, and incident shadow edges with their evidence references. Every returned edge retains `authority_effect: NONE_DIRECT`; graph connectivity itself does not promote a claim or transfer authority.

## Architecture gates remain active

This operation does not discharge the stage-bounded architecture controls:

- `MCORE-ARCH-C03`: no cross-domain authority is inferred; a typed, evidence-bearing bridge remains required before such use.
- `MCORE-ARCH-C04`: no live INTELLECT coordinator, concurrency protocol, or invalidation mechanism is introduced.
- `MCORE-ARCH-C05`: no replayable/checked production pruning or operational witness use is introduced.
- `MCORE-ARCH-C06`: provenance-bound migration and the blocker taxonomy are preserved; no retroactive live-event history is invented.
- `MCORE-ARCH-C07`: no persistent unattended execution is introduced.

## Claim boundary

`MCORE-DOMAIN-DIAG-001` proves no new mathematics, certifies no theorem or dependency edge, promotes no claim, upgrades no Condensed frontier status, and makes no graph-completeness, dependency-minimality, or dependency-uniqueness claim. It authorizes no live allocation, live pruning, persistent coordinator, publication, or external mathematical claim.
