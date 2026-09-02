# GCL Portfolio Pilot

## Current status

`GCL-PORTFOLIO-WP00` Tranche 1 is `TRANCHE_1_PROTECTED_COMPLETE`.

It completed through PR #207 from reviewed candidate `038d2ba2597e0e4dde60679741d7c5f339343114` and protected merge `86a3f551f35aa67bdd0437d060ce786cb3d447fb`. The historical admission sequence included hosted checks, delegated review, Human Steward release, and protected merge. Those facts remain provenance; they do not impose a fresh approval ritual on current routine maintenance.

## Purpose

The portfolio pilot is a protected decision-support ledger for comparing bounded GCL work without converting a score into institutional authority.

It addresses four recurring errors:

1. treating scientific importance as execution readiness;
2. allowing prestige or prospective product value to hide dependency gates;
3. replacing unknown cost or risk with fabricated precision;
4. treating an advisory calculation as authorization to allocate, suspend, terminate, publish, or promote.

Issue #190 records the pilot admission. Its protected prerequisites are the truth spine, tooling Tranche 1, and negative-knowledge Tranche 1.

## Authority and files

The protected pilot registry is:

```text
portfolio/pilot_registry.json
```

Its closed schema is:

```text
schemas/gcl_portfolio_registry.schema.json
```

Validation and rendering run through:

```text
python3 ci/validate_portfolio.py
python3 ci/render_portfolio.py --check
```

The generated human-readable projection is:

```text
docs/governance/GCL_PORTFOLIO_VIEW.md
```

The projection is reconstructible and cannot override the registry.

## Pilot boundary

Tranche 1 contains exactly four umbrella records:

- `GCL-PORTFOLIO-WP00` under #190;
- `GCL-SYNTHESIS-WP00` under #191;
- `GCL-ASSURANCE-PRODUCT-WP00` under #192;
- `GCL-DISCLOSURE-WP00` under #193.

This is not an organization-wide portfolio inventory. It does not score mathematical campaigns, experimental programmes, repositories, people, or external opportunities unless separately admitted.

## Separate dimensions

Every record keeps these dimensions distinct:

- scientific or strategic importance;
- execution readiness;
- institutional leverage;
- expected information gain;
- compute, labour, review, and coordination cost;
- dependency and execution risk;
- probability and value of decisive falsification;
- transfer, publication, and product value.

Each metric is an integer on a documented 0–5 scale or the literal value `unknown`. Fractional pseudo-precision is rejected.

## Advisory interval

The pilot uses model `GCL-PORTFOLIO-ADVISORY-INTERVAL-001`:

```text
readiness / 5
× weighted benefit
÷ (1 + total cost + dependency risk + execution risk)
```

The falsification contribution is `probability / 5 × value`. Unknown inputs are evaluated over the declared 0–5 bounds, producing an interval rather than an imputed point estimate.

The model has three hard boundaries:

1. readiness zero forces the advisory interval to zero;
2. output is an interval only, not a rank or disposition;
3. records are displayed in issue order, never sorted into an automatic priority queue.

The fixed pilot weights are schema-bound. A material change to the decision model or authority boundary requires the review appropriate to that substantive change; routine projection or documentation maintenance uses standing delegated execution.

## Reversibility and freshness

Every record must include pause, termination, and reopening conditions. Irreversible commitment is prohibited in this tranche.

Evidence freshness is determined by material identity and the registry's declared refresh obligations. Unrelated repository-head movement does not make an unchanged evidence object stale. Stale or unknown material evidence must name a concrete refresh obligation or validation fails.

## Fail-closed rules

The pilot rejects:

- missing or extra pilot members;
- duplicate record, work-package, or issue identities;
- mismatched issue mappings;
- hidden, negative, or malformed cost components;
- fabricated fractional precision;
- stale material evidence without refresh work;
- scoring-weight changes outside the schema;
- blocked work with inflated or unknown readiness;
- active work retaining blocking dependencies;
- unknown, reversed, or cyclic dependencies;
- irreversible lock-in;
- generated-view drift;
- automated or machine-authored dispositions;
- every resource-allocation, execution, suspension, termination, claim, publication, novelty, patentability, product, and commercial authority flag.

## Ongoing operating boundary

The protected `active_pilot` state is already effective. Future routine maintenance follows `MP-STREAMLINED-EXECUTION-001`: classify the material closure, run affected checks, use delegated disposition, merge through protection, and read back protected state. A change that creates resource-allocation authority, alters constitutional decision semantics, or promotes an external claim crosses a reserved boundary and is not routine maintenance.

Validation demonstrates conformance to the protected pilot contract. It does not determine what GCL should fund or execute, and it does not automatically activate downstream work.
