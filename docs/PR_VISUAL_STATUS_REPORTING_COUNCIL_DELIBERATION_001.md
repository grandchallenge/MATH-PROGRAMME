# PR Visual Status Reporting Council Deliberation 001

## COUNCIL-PR-VISUAL-STATUS-REPORTING-001

**Docket:** MATH-PROGRAMME issue #415  
**Deliberation date:** 2026-08-10  
**Protected baseline reviewed:** `grandchallenge/MATH-PROGRAMME@cc0e7a3a87ab298645f1be5e1d6744b0d6cdd7e7`  
**Originating exemplar:** #407 / PR #414 closure audit visual  
**Authority state:** Council recommendation only; Human Steward approval and protected admission remain pending.

## 1. Purpose

Council reviewed the proposal to generate a standardized, richly informative visual status report for every significant pull request. The proposed report is a derived human-review interface exposing exact-head provenance, review/approval state, dispositions, checks, protected integration state, blockers, nonclaims, and residual obligations. It is not an authoritative governance source and cannot create merge, mathematical, source, certification, or programme authority.

## 2. Quorum and delegations

The current Agent Council schema requires fifteen offices. For this docket, quorum requires all fifteen offices to record reviewed findings, Referee synthesis, and no blocking dissent against presentation to the Human Steward. This is a procedural rule for this docket only.

Delegated scopes:

- Axiomatist — authority/status invariants.
- Prospector — strategic leverage and reviewer-value hypothesis.
- Experimentalist — pilot design, controls, measures, falsification.
- Cartographer — information architecture, significance classification, cross-repository applicability.
- Verifier — machine derivability, exact-head/freshness binding, source-to-render consistency.
- Adversary — misleading-green, stale-head, partial-evidence, identity and omission attacks.
- Formalist — schema/state-machine and provenance contracts.
- Steward — human-reader contract.
- Composer — segmentation, ordering, progressive disclosure.
- Grammarian — controlled status vocabulary.
- Amanuensis — continuity, supersession, provenance, final integration.
- Archivist — retention and historical integrity.
- Mechanist — deterministic rendering and GitHub transport.
- Typesetter — accessibility and legibility.
- Referee — synthesis and disposition.

## 3. Office deliberations

### Axiomatist
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

A visual state must remain strictly downstream of authoritative state. Distinct predicates for checks, review, authorization, merge, readback, blockers, and mathematical/source/certification status must not be collapsed into an ambiguous aggregate. A report may summarize authority; it cannot create or infer it.

### Prospector
**Disposition:** `APPROVE_FOR_BOUNDED_PILOT`

The proposal has high leverage because significant PRs increasingly carry enough exact-head, provenance, review, disposition, and readback data that human orientation cost is material. The likely benefit is faster orientation and anomaly detection rather than aesthetic improvement. A bounded cross-domain pilot is warranted.

### Experimentalist
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Utility must be measured. The pilot should track time-to-correctly-identify operative state, reviewer factual error rate, blocker-detection rate, stale-report detection, visual/source disagreement, generation latency, operational cost, and accessibility. Initial enforcement must be advisory.

### Cartographer
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Adopt a mandatory cross-repository core plus domain-specific modules rather than one flat universal schema. `Significant PR` requires a machine-readable significance profile with objective triggers and explicit Referee/Council/Human-Steward override.

### Verifier
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Every rendered fact must trace to a structured source snapshot. Bind report identity, repository/PR, exact head, observation time, source-snapshot digest, schema version, generator version, and freshness state. Head movement must automatically invalidate or regenerate the report. Text and graphic derivatives must come from the same structured input.

### Adversary
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Retained attacks must cover stale reports, wrong-head approvals/dispositions, partial check failures, missing fields, incomplete readback, hidden residual obligations, actor confusion, erased failure history, color-only status, ambiguous truncation, and renderer/content mismatch. Unknown or inconsistent state must never render as success. Unconstrained generative content must not be the canonical source of operative status text.

### Formalist
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Define a versioned `pr_visual_status_report` input schema and a rendering/state-machine contract. Canonical JSON is the authoritative derived report object; SVG/PNG/PDF and textual summaries are derivatives. Unknown/inconsistent inputs map fail-closed to `UNKNOWN`, `STALE`, or `BLOCKED`.

### Steward
**Disposition:** `APPROVE_FOR_BOUNDED_PILOT`

The reader contract is strong if a reviewer can answer within roughly one minute: what is this PR, what exact object is under review, who has approved it, what remains open, and is it safe to advance? Deep detail should remain reachable rather than overloading the primary visual.

### Composer
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Use the #407 exemplar as the starting grammar, not a frozen layout. Preferred order: `Identity/state -> authority/review -> provenance/exactness -> validation -> protected integration -> residual obligations -> conclusion`. Empty sections should be suppressible and domain modules composable.

### Grammarian
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Terms such as `approved`, `complete`, `clean`, and `verified` require named objects. Controlled statuses should include equivalents of `REVIEW_PENDING`, `CHANGES_REQUESTED`, `EXACT_HEAD_CHECKS_GREEN`, `AUTHORIZATION_PENDING`, `AUTHORIZED_FOR_PROTECTED_MERGE`, `MERGED_READBACK_PENDING`, `PROTECTED_COMPLETE`, `BLOCKED`, `STALE`, and `UNKNOWN`. Campaign dispositions remain separate.

### Amanuensis
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Treat the report as a governed documentary derivative. Material retained states should bind report ID, exact head, schema/generator versions, source-snapshot digest, generation time, supersession relation, and archival location. Retain at least material state transitions, the final review/authorization state, and final protected-complete state. A textual/structured equivalent is mandatory.

### Archivist
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Retention must preserve why a PR was considered ready, blocked, authorized, or complete at material decision points. A later green report must not erase earlier failures, rejected reviews, lateness, or superseded dispositions. External source provenance remains governed by its own records.

### Mechanist
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

Recommended pipeline: `collectors -> normalized report JSON -> deterministic renderer -> text + visual derivatives -> PR surface + archival retention`. Report attachment must not mutate the candidate head. Regeneration should be event-driven and idempotent for head, review, check, disposition, merge, and readback changes. A short-lived Actions artifact alone is insufficient for long-term provenance.

### Typesetter
**Disposition:** `APPROVE_FOR_BOUNDED_PILOT`

The #407 exemplar is a strong baseline. Reports must be desktop-readable, printable, accessible, use text/icons in addition to color, render SHAs/run IDs clearly, and expose all operative information in an accessible text equivalent. Visual abbreviation of identities is permitted only when the full value is directly recoverable.

### Referee
**Disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`

All specialist offices support a bounded pilot. No office recommends return or rejection. The central risk is visually persuasive false readiness; therefore the pilot is approved only with deterministic, source-bound, fail-closed semantics and advisory enforcement.

## 4. Council correction register

- `PRVSR-C01` — Axiomatist + Formalist: canonical state/authority model; high; blocking before pilot implementation.
- `PRVSR-C02` — Cartographer + Grammarian: machine-readable significance profile; medium; blocking before automatic scope selection.
- `PRVSR-C03` — Formalist + Cartographer: canonical report-input schema and modular architecture; high; blocking before renderer implementation.
- `PRVSR-C04` — Verifier + Mechanist: deterministic provenance-bound rendering and automatic stale invalidation; critical; blocking before first live pilot report.
- `PRVSR-C05` — Adversary + Verifier: fail-closed adversarial suite; critical; blocking before first live pilot report.
- `PRVSR-C06` — Adversary + Mechanist: canonical operative content must come from deterministic structured data; high; blocking before first live pilot report.
- `PRVSR-C07` — Typesetter + Steward: accessible equivalent textual/structured surface; high; blocking before pilot acceptance.
- `PRVSR-C08` — Amanuensis + Archivist: continuity, retention, supersession, historical integrity; medium; blocking before pilot acceptance.
- `PRVSR-C09` — Mechanist + Amanuensis: non-mutating PR transport and stable archival channel; medium; blocking before live pilot integration.
- `PRVSR-C10` — Experimentalist + Prospector + Referee: advisory measured pilot; high; blocking before any mandatory policy gate.

## 5. Conditional successor delegations

If the Human Steward approves the bounded pilot, Council recommends:

- Axiomatist + Formalist — state/authority algebra and schema invariants.
- Cartographer + Grammarian — significance taxonomy, common information architecture, controlled vocabulary.
- Verifier + Adversary — derivation integrity, stale-state rules, mutation/adversarial tests.
- Mechanist + Typesetter — deterministic renderer, PR surfacing, archival transport, accessible presentation.
- Experimentalist + Prospector — pilot matrix, controls, quantitative utility assessment.
- Steward + Composer — one-minute reader contract, section grammar, progressive disclosure.
- Amanuensis + Archivist — identity, continuity, supersession, retention, decision/provenance references.
- Referee — independent pilot acceptance, correction discharge, and propagation recommendation.

These are conditional execution delegations only; they confer no current implementation authority.

## 6. Recommended pilot boundary

Approximately 8–12 significant PRs spanning governance/control-plane, administrative automation, source/claim classification, theorem/certification/formal replay, documentary migration, a blocked/changes-requested case, a moving-head stale-state adversarial case, and at least one low-complexity positive control.

The #407 / PR #414 closure is the originating design exemplar, not sufficient evidence for programme-wide rollout.

## 7. Quorum and Council decision

- offices reviewed: `15/15`;
- support bounded pilot: `15/15`;
- `RETURN_FOR_REVISION`: `0`;
- `REJECT`: `0`;
- blocking dissent: `0`.

**Council disposition:** `APPROVE_WITH_CORRECTIONS_FOR_BOUNDED_PILOT`.

Controlled state:

`PR_VISUAL_STATUS_REPORTING_APPROVED_WITH_CORRECTIONS_FOR_ADVISORY_BOUNDED_PILOT__HUMAN_STEWARD_AUTHORITY_PENDING`

## 8. Authority boundary

Council recommendation does not authorize implementation, require reports on current PRs, alter required checks/branch protection/review/merge authority, make a visual report a governance authority source, make a visualization mathematical evidence or certification, authorize programme-wide rollout, or authorize product/deployment/release/publication/novelty/priority/patentability/commercial claims.

The next legitimate step is Human Steward review of this Council disposition and correction register, followed—if approved—by a separately governed protected pilot implementation package.