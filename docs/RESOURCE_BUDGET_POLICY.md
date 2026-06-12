# Resource Budget Policy

## Purpose

Expensive symbolic methods must run with declared budgets. A timeout or blowup is not merely an engineering inconvenience; it is information about the tactic.

## Required budget fields

Every expensive symbolic lane should record:

```yaml
resource_budget:
  max_variables:
  max_total_degree:
  max_runtime_seconds:
  max_basis_elements:
  max_intermediate_terms:
  monomial_order:
  backend:
  backend_version:
  fallback_route:
```

## Failure statuses

A failed computation should be classified, not erased.

```yaml
failure_status:
  - timeout
  - degree_explosion
  - basis_size_explosion
  - memory_exhaustion
  - unstable_modular_reconstruction
  - unsuitable_monomial_order
  - side_conditions_missing
  - not_actually_algebraic
```

## Promotion rule

A symbolic computation may promote a claim only when the resulting artifact has a replay or proof route.

Raw output is evidence. A checked witness is support. A theorem or replayed certificate is the boundary.

## Operational maxim

> No expensive symbolic lane without a budget. No failed symbolic run without a ledger.
