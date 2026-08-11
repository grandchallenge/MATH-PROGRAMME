# ADR-0019 — Significant-PR visual status reporting

**Date:** 2026-08-10  
**Status:** Council approved with corrections for advisory bounded pilot; Human Steward and protected admission pending  
**Docket:** `COUNCIL-PR-VISUAL-STATUS-REPORTING-001` / issue #415  
**Council disposition:** `PR_VISUAL_STATUS_REPORTING_APPROVED_WITH_CORRECTIONS_FOR_ADVISORY_BOUNDED_PILOT__HUMAN_STEWARD_AUTHORITY_PENDING`

## Context

The Programme's significant pull requests increasingly carry material review state distributed across issue bodies, PR descriptions, exact-head reviews, Human Steward dispositions, workflow/check runs, merge receipts, protected-main readback, synchronization state, blockers, nonclaims, and residual obligations. This is auditable but expensive for a human reviewer to reconstruct repeatedly.

The #407 / PR #414 namespace-hardening closure demonstrated a useful one-page visual grammar for summarizing these states. Council reviewed whether such reports should become a standardized programme capability.

## Council decision

Council supports an **advisory bounded pilot**, subject to corrections `PRVSR-C01` through `PRVSR-C10`.

The report is a **derived non-authoritative documentary interface**. It must never create review, merge, mathematical, source, certification, deployment, or programme authority. Authoritative state remains in protected repository/governance records and the live GitHub objects from which the report is derived.

## Required semantic contract

A pilot report shall, where applicable, expose:

1. repository/PR/docket identity and exact head;
2. governed lifecycle/integration state;
3. independent review and Referee state;
4. Human Steward disposition state where required;
5. required checks and exact run/check identities;
6. bounded purpose and nonclaims;
7. merge and protected-main readback state;
8. open blockers/residual obligations;
9. freshness/staleness state;
10. a concise reviewer-oriented conclusion.

Campaign-specific dispositions remain separate from lifecycle/integration state.

## Derived-state rule

Canonical operative content must be generated from a versioned structured report object. Graphical and textual representations are derivatives of that object.

Every retained report must bind sufficient provenance to identify at least:

- report ID;
- repository and PR;
- exact head;
- observation/generation time;
- source-snapshot digest;
- report-schema version;
- generator version;
- supersession/freshness state where applicable.

A changed head or material state change must regenerate or visibly invalidate the prior report. Missing, inconsistent, stale, or unknown evidence cannot be rendered as successful completion.

## Generative-tool boundary

Unconstrained generative text or image output must not be the canonical source of factual governance status. Generative tooling may assist non-operative design exploration only if all operative status text and values are deterministically produced from the structured report state and an accessible equivalent textual surface is retained.

## Pilot boundary

If authorized by the Human Steward, the pilot should cover approximately 8–12 materially different significant PRs, including governance/control-plane, administrative automation, source/claim classification, theorem/certification/formal replay, documentary migration, a blocked/changes-requested case, a moving-head stale-report adversarial case, and at least one low-complexity positive control.

The pilot is **advisory**. Absence or failure of the report generator is not a new merge blocker unless a later governed disposition makes it one.

## Pilot evaluation

At minimum evaluate:

- reviewer time to identify operative state;
- factual state-identification accuracy;
- blocker/residual-obligation detection;
- stale-report detection;
- source/render disagreement rate;
- regeneration latency and operational cost;
- accessibility and textual-equivalence fidelity.

Programme-wide mandatory reporting or any merge-gate requirement requires a separate post-pilot governed disposition.

## Correction register

- `PRVSR-C01` — canonical state/authority model.
- `PRVSR-C02` — machine-readable significant-PR profile.
- `PRVSR-C03` — versioned canonical report-input schema and modular architecture.
- `PRVSR-C04` — deterministic provenance-bound rendering and automatic stale invalidation.
- `PRVSR-C05` — fail-closed adversarial suite.
- `PRVSR-C06` — constrain canonical operative content to deterministic structured data.
- `PRVSR-C07` — accessible equivalent textual/structured surface.
- `PRVSR-C08` — continuity, retention, supersession, and historical integrity.
- `PRVSR-C09` — non-mutating PR transport and stable archival channel.
- `PRVSR-C10` — advisory measured pilot and separate propagation/gating adjudication.

Exact ownership and severity are recorded in `governance/pr_visual_status_reporting_council_review_candidate.json` and `docs/PR_VISUAL_STATUS_REPORTING_COUNCIL_DELIBERATION_001.md`.

## Authority boundary

This ADR candidate does not itself:

- authorize the pilot;
- create implementation authority;
- require reports on any current PR;
- modify required checks, review rules, branch protection, or merge authority;
- make a visual report a governance authority source;
- make visualization mathematical evidence or certification;
- authorize programme-wide rollout;
- authorize product, deployment, release, publication, novelty, priority, patentability, or commercial claims.

Protected authority remains pending explicit Human Steward exact-head disposition and protected admission.
