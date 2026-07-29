# Resource Budget Policy

## Purpose

Expensive symbolic methods SHALL run with declared budgets. A timeout or blowup is not merely an engineering inconvenience; it is governed evidence about the tactic.

## Lane declaration

Every expensive symbolic lane SHALL declare:

```yaml
lane_class: expensive_symbolic
lane_id: APP-EXAMPLE-01
```

The lane SHALL appear in `governance/expensive_symbolic_lane_registry.json`. CI recursively discovers marked JSON and YAML lane records under the governed scan roots. It rejects unregistered lanes and registry entries that do not resolve to a marked lane.

## Required budget fields

Every expensive symbolic lane SHALL record:

```yaml
resource_budget:
  max_variables: 16
  max_total_degree: 12
  max_runtime_seconds: 600
  max_basis_elements: 10000
  max_intermediate_terms: 250000
  monomial_order: graded_reverse_lexicographic
  backend: SageMath/Singular
  backend_version: pinned-by-fixture
  fallback_route: alternate_exact_route
```

All numeric bounds must be positive integers. Backend, version, order, and fallback route must be explicit before execution.

## Run ledger

Every lane SHALL carry a `run_ledger` before it can execute.

An unstarted lane records `execution_status: not_started` and no result or failure evidence. A successful run records `execution_status: completed`, `termination_status: success`, an exact result artifact, and a timestamp. A failed run records `execution_status: failed`, one controlled failure status, a failure record, and a timestamp.

Controlled failure statuses are:

```text
timeout
degree_explosion
basis_size_explosion
memory_exhaustion
unstable_modular_reconstruction
unsuitable_monomial_order
side_conditions_missing
not_actually_algebraic
cancelled_by_budget
```

A failed run must not claim a result artifact. A completed run must not carry failure evidence.

## Enforcement

`ci/validate_symbolic_resource_budgets.py` validates registry coverage, discovery, budgets, and run-ledger state. `ci/validate_grobner_manifest.py` invokes this validator for the current symbolic application portfolio. Repository unit tests and adversarial manifest tests reject missing budgets, non-positive limits, hidden failures, orphan registrations, unregistered lanes, and completed runs without artifacts.

## Promotion rule

A symbolic computation may support promotion only when its bounded result has a replay or proof route. Raw output is evidence. A checked witness is support. A theorem or replayed certificate is the boundary.

## Operational maxim

> No expensive symbolic lane without a budget. No symbolic run without a ledger. No failed run without a preserved failure record.
