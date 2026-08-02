# GCL Portfolio Pilot

## Purpose

The portfolio pilot is a protected decision-support ledger for comparing bounded GCL work without converting a score into institutional authority.

It addresses four recurring errors:

1. treating scientific importance as execution readiness;
2. allowing prestige or prospective product value to hide dependency gates;
3. replacing unknown cost or risk with fabricated precision;
4. treating an advisory calculation as authorization to allocate, suspend, terminate, publish, or promote.

Issue #190 governs the pilot. Its protected prerequisites are the truth spine, tooling Tranche 1, and negative-knowledge Tranche 1.

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

This is not an organization-wide portfolio inventory. It does not score mathematical campaigns, experimental programmes, repositories, people, or external opportunities.

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

The fixed pilot weights are schema-bound. Changing them requires a reviewed contract revision rather than editing a dashboard control.

## Reversibility and freshness

Every record must include pause, termination, and reopening conditions. Irreversible commitment is prohibited in this tranche.

Current evidence carries no refresh obligation. Stale or unknown evidence must name a concrete refresh obligation or validation fails.

## Fail-closed rules

The pilot rejects:

- missing or extra pilot members;
- duplicate record, work-package, or issue identities;
- mismatched issue mappings;
- hidden, negative, or malformed cost components;
- fabricated fractional precision;
- stale evidence without refresh work;
- scoring-weight changes outside the schema;
- blocked work with inflated or unknown readiness;
- active work retaining blocking dependencies;
- unknown, reversed, or cyclic dependencies;
- irreversible lock-in;
- generated-view drift;
- automated or machine-authored dispositions;
- every resource-allocation, execution, suspension, termination, claim, publication, novelty, patentability, product, and commercial authority flag.

## Activation boundary

The branch is non-authoritative. The declared `active_pilot` state becomes effective only after external exact-head review, explicit Human Steward release, and protected merge.

Validation demonstrates only conformance to the declared pilot contract. It does not determine what GCL should fund or execute, and it does not activate #191–#193.
