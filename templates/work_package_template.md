# WP##_TITLE

## Metadata

- Domain:
- Work Package number:
- Primary type:
- Global theorem-spine node:
- Incoming dependencies:
- Claim status:
- Certification target:
- Knowledge graph refs:
- Classification mapping refs:
- Discovery record refs:
- Foundational profile: present | inherited | deferred

## 1. Result-status box

| Field | Value |
|---|---|
| Result status | |
| Conditional on | |
| Strongest supported claim | |
| Not claimed | |
| Support-route class | `NONE` |
| Foundational profile | |
| Certification state | |
| First executable step | |

## 2. Foundational profile

Use `schemas/foundational_profile.schema.json` for machine-readable artifacts.
Historical packages may inherit or defer this profile, but new Work Packages
should make the carrier, ambient structure, axiom profile, witness policy, and
pathology risk explicit.

```yaml
foundational_profile:
  carrier_type: unknown
  ambient_structure: []
  regularity: []
  axiom_profile:
    base: unknown
    choice_usage: unknown
    excluded_middle: unknown
    large_cardinal_usage: unknown
    determinacy_usage: unknown
  witness_policy:
    existence_claim: unknown
    witness_location: absent
  certification_target:
    - human_audit
  pathology_risk:
    level: unknown
    notes: ""
```

## 3. Lay executive companion

### The object

### The obstruction

### The restricted target

### What this package achieved

### What this package did not achieve

## 4. Formal problem statement

### Definitions and notation

### Exact target statement

### Model or encoding correspondence

## 5. Object and obstruction

Give the smallest exact example, calculation, counterexample, or failed
mechanism that exposes the principal obstruction.

## 6. Known terrain and source audit

| Source or result | Claim used here | Audit state | Spine dependency |
|---|---|---|---|
| | | | |

## 7. Claim ledger summary and trust quartet

### Claim ledger summary

| Claim ID | Statement | Status | Evidence | Certification state |
|---|---|---|---|---|
| | | | | |

### What is proved?

### What is checked?

### What remains open?

### What requires external verification?

## 8. Theorem-spine slice and dependency DAG

| Node ID | Role | Statement | Status | Dependencies | Discharge criterion |
|---|---|---|---|---|---|
| | | | | | |

Explain how this local slice advances the global theorem spine.

## 9. Proofs and classified computations

For each support route record:

- pedagogical class:
  `EXPLORATORY_EVIDENCE`, `REGRESSION_AUDIT`,
  `EXACT_FINITE_VERIFICATION`, `CERTIFICATE_REPLAY`,
  `FORMAL_PROOF`, `CONTINUUM_PROOF`, or `NEGATIVE_RESULT`;
- arithmetic or proof mode;
- input and output;
- reproducibility command;
- claim IDs supported;
- limitations.

## 10. Failure and negative-result analysis

### Attempted route

### Why it was plausible

### Smallest exact obstruction

### What the obstruction rules out

### What remains viable

## 11. Proof-debt register

| Debt ID | Category | Blocked node | Current evidence | Discharge condition | Route or owner |
|---|---|---|---|---|---|
| | | | | | |

Allowed categories:

```text
MISSING_LEMMA
UNPROVED_BRIDGE
EXTERNAL_SOURCE
COMPUTATIONAL_REPLAY
SEMANTIC_CORRESPONDENCE
FOUNDATIONAL_PROFILE_GAP
ANALYTIC_ESTIMATE
FORMALIZATION_BLOCKER
```

## 12. Certification boundary and MATHCERT handoff

### Pencil-and-paper claims

### Machine-checked or replayed claims

### Exact certificate candidates

### Formalization blockers

### First item for MATHCERT

## 13. First executable step

- Input:
- Operation:
- Output artifact:
- Completion test:
- Spine node advanced or debt item discharged:

## 14. Escalation gate

- [ ] The theorem-spine slice has been audited.
- [ ] All dependencies are named.
- [ ] The proof-debt register is current.
- [ ] The trust quartet is complete.
- [ ] The foundational profile is present, inherited, or explicitly deferred.
- [ ] The first executable step is explicit.
- [ ] Any proposed next package names the spine node it advances.
