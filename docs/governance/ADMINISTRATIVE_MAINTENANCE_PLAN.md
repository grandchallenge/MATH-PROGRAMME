# MATH-PROGRAMME Administrative Maintenance Plan

**Control:** `MP-ADMIN-MAINT-001`  
**Decision:** `MP-ADMIN-DECISION-001`; `ADR-0016`  
**Status:** Human Steward approved accelerated pilot; activates only on protected merge  
**Programme tracker:** #182  
**Council authority tracker:** #183  
**INTELLECT adoption tracker:** grandchallenge/INTELLECT#21  
**Foundation:** seventh-pass closure merge `3cb6bfb9f132a4cfef279d0d3bf2309d99d0d6f1`

## 1. Purpose

This plan establishes a standing administrative system for:

- MATH-PROGRAMME;
- MATHFORGE;
- MATHSOLVE;
- MATHCERT;
- INTELLECT.

The system preserves **Core Clarity**. A reader, validator, or agent must be able to answer without inference:

1. What record is authoritative?
2. What exact object and revision does it identify?
3. What lifecycle, route, review, and claim state is current?
4. Which workflow validates that state?
5. What evidence proves that the workflow ran against the exact reviewed head?
6. What action is permitted next, and what remains prohibited?

This is administrative infrastructure. It cannot prove mathematics or authorize external claims.

## 2. Human Steward decision and time scale

The Human Steward approved Council decisions D1–D8 with one global correction: every proposed maintenance duration and cadence interval is multiplied by `0.1`.

Event-triggered obligations remain immediate. A periodic cadence never permits a material synchronization to wait.

The accelerated intervals are:

| Control | Binding interval |
|---|---:|
| Pilot | `P9D` |
| Structural sweep | `PT16H48M` |
| Administrative portfolio review | `P3D` |
| Deep conformance review | `P9D` |
| Constitutional review | `P36DT12H` |
| Canonical tracker refresh | `PT7H12M` |
| Ordinary local Steward waiver | `P3D` |
| Emergency override maximum | `PT7H12M` |
| Emergency Steward review | `PT2H24M` |
| Council and Referee retrospective | `PT16H48M` |
| Unresolved P1 circuit-breaker interval | `PT16H48M` |

The pilot starts at the protected merge timestamp of PR #184. The pilot review is due nine days later.

## 3. Authority model

Protected repository records are authoritative. Issues are mutable navigation and discussion mirrors.

| State dimension | Authority |
|---|---|
| Programme portfolio, lifecycle, routing, admission | MATH-PROGRAMME |
| Source identity, provenance, provider manifest, provider waiver | MATHFORGE |
| Mathematical work package, campaign manifest, producer handoff | MATHSOLVE |
| Certification route, adjudication, output, certified scope | MATHCERT |
| Consumer projection, stale-contract rejection, lifecycle semantics | INTELLECT |

INTELLECT is an explicit adoption and freshness-enforcement partner. Final administrative closure requires protected INTELLECT adoption of the exact protected Programme contract.

## 4. Identity and supersession

A repository head and a material artifact identity are different objects.

A downstream consumer repins when a consumed artifact changes. It does not repin merely because an unrelated commit moves the provider repository head. Every change review records whether the change is material or nonmaterial.

Historical audits, closures, and conformance records remain immutable. A later record may supersede them, but it does not rewrite their historical state.

## 5. Promotion boundary

Missing, stale, contradictory, unreviewed, or unverified evidence fails closed.

Presentation, documentation, issue wording, workflow-file presence, or a historical successful run cannot create current authority.

Interface qualification remains interface qualification. It is not theorem proof.

## 6. Event-triggered synchronization

Run this loop immediately after a material change to:

- a campaign registry or lifecycle record;
- a provider manifest or waiver;
- a Solve campaign manifest or handoff;
- a Cert route, adjudication, or certificate output;
- a Programme runtime, routing, admission, or claim contract;
- an INTELLECT provider pin or lifecycle rule;
- branch protection or a required workflow.

The change owner must:

1. classify the change;
2. identify affected authoritative artifacts;
3. identify downstream consumers;
4. update all materially affected contracts in one governed sequence;
5. preserve unchanged content-addressed identities;
6. run exact-head validation;
7. merge only after required checks pass;
8. publish an external post-merge attestation when a protected artifact cannot identify its own future merge.

An incomplete material synchronization has disposition `FAIL_CLOSED_MATERIAL_SYNC_INCOMPLETE`.

## 7. Accelerated assurance loops

### 7.1 Structural sweep — every 16 hours 48 minutes

Check:

- protected heads;
- open pull-request interference;
- schema and current-state parseability;
- required workflow presence;
- canonical tracker links;
- issue text that appears to claim protected authority;
- expired review evidence;
- missing or duplicate canonical records.

### 7.2 Administrative portfolio review — every 3 days

Check:

- active, candidate, and dependency-bearing archived campaigns;
- provider manifest and waiver status;
- Solve handoff and Cert route concordance;
- consumer pins;
- workflow coverage;
- tracker freshness;
- P1 and P2 defects;
- maintenance burden and repeated manual work.

The output is a protected review record. A chat summary or issue comment is insufficient.

### 7.3 Deep conformance review — every 9 days

Perform:

- exact five-repository identity reconciliation;
- supersession and archival audit;
- adversarial mutation review;
- branch-protection and required-check verification;
- recurring-defect analysis;
- workflow evidence sampling;
- consolidation and retirement analysis.

A deep closure requires a versioned record, strict schema, adversarial tests, exact-head workflows, protected merge, and external post-merge attestation.

### 7.4 Constitutional review — every 36 days 12 hours

Review:

- authority hierarchy;
- role separation;
- lifecycle and promotion semantics;
- claim vocabulary;
- waiver authority;
- emergency powers;
- maintenance burden;
- communication standards;
- retention and archival policy.

This review belongs to the Council and Human Steward.

## 8. Workflow coverage

A workflow is **covered** only when all of the following are recorded:

1. repository;
2. capability;
3. workflow name or governed non-applicability record;
4. trigger;
5. required-check status;
6. exact-head execution evidence;
7. success evidence location;
8. failure evidence location;
9. owner;
10. repair route;
11. last verified identity.

The existence of a YAML file is not coverage.

The umbrella matrix must account for:

- schema and contract validation;
- unit tests;
- adversarial mutation tests;
- source or provider validation where applicable;
- campaign admission and routing validation where applicable;
- formal or certificate replay where applicable;
- documentation build where applicable;
- GCL conformance;
- branch-protection and release-trust evidence.

Non-applicability must be explicit, scoped, reviewed, and testable.

## 9. Tracker and issue hygiene

Every canonical tracker must state:

- authority boundary;
- protected authority identity;
- current lifecycle and route state;
- exact next controlled obligation;
- claim boundary;
- review trigger.

Refresh a canonical tracker within 7 hours 12 minutes after a protected material transition. A documented infrastructure or statutory-closure interruption may pause only this mirror clock. It cannot alter protected authority.

A stale but noncontradictory tracker is a P2 administrative defect. A contradictory tracker or authority-bearing issue statement is P1 fail-closed. An identified contradiction blocks reconciliation closure.

## 10. Defect classes

| Class | Meaning | Default response |
|---|---|---|
| P0 | Security, repository integrity, or evidence destruction risk | emergency containment; no promotion |
| P1 | Authority, identity, lifecycle, route, certificate, required-check, or claim-boundary mismatch | immediate fail-closed repair |
| P2 | Missing coverage, stale canonical tracker, incomplete supersession, or unresolved ownership | tracked correction before the next applicable accelerated review |
| P3 | Naming, navigation, or low-risk administrative debt | batch into routine maintenance |

A lower class cannot downgrade a defect that affects authority or promotion.

## 11. Waivers

A waiver is a typed temporary governance object. It records:

- identifier;
- scope;
- owner;
- reason;
- evidence;
- approver;
- issue and expiry times;
- prohibited uses;
- repair obligation;
- renewal count.

The Human Steward may approve an ordinary repository-local administrative waiver for at most three days and one renewal.

The Council must approve:

- longer or repeated waivers;
- cross-repository waivers;
- provenance waivers;
- certification waivers;
- required-check waivers.

No waiver can authorize mathematical or external claim promotion.

## 12. Independent review

A non-author Referee is required for changes to:

- authority hierarchy;
- lifecycle or promotion semantics;
- claim vocabulary or scope;
- provider, producer, or adjudicator boundaries;
- waiver classes;
- emergency powers;
- branch-protection or required-check weakening;
- maintenance controls whose failure could permit promotion.

Routine semantic-preserving identity repins and mirror refreshes use ordinary administrative review.

## 13. Emergency override

Emergency authority exists only to restore availability, respond to a security incident, or restore CI operability.

It may not:

- promote a claim;
- admit a campaign;
- issue a certification disposition;
- weaken branch protection;
- delete required evidence.

It expires after 7 hours 12 minutes. Human Steward review is due within 2 hours 24 minutes. Council and Referee retrospective is due within 16 hours 48 minutes. Expiry reverts fail closed automatically.

## 14. Maintenance-burden circuit breaker

A campaign missing a critical required capability fails closed immediately.

Freeze new umbrella admissions when:

- two consecutive three-day administrative reviews fail;
- a P1 mismatch remains unresolved for 16 hours 48 minutes;
- two active campaigns lack complete critical workflow coverage;
- more than 20 percent of active campaigns lack complete workflow coverage;
- required-check or branch-protection evidence is missing;
- the same defect recurs in two consecutive nine-day deep reviews.

For portfolio coverage, use the stricter threshold of two active campaigns or more than 20 percent of the active portfolio.

The Council may consolidate controls, increase automation, archive obsolete records, change ownership, suspend campaigns, or restore normal operation.

## 15. Council dispositions

| Decision | Binding disposition |
|---|---|
| D1 | `APPROVE_WITH_CORRECTION` |
| D2 | `APPROVE_WITH_CORRECTION` |
| D3 | `APPROVE_WITH_CORRECTION` |
| D4 | `APPROVE` |
| D5 | `APPROVE_WITH_CORRECTION` |
| D6 | `APPROVE_WITH_CORRECTION` |
| D7 | `APPROVE_WITH_CORRECTION` |
| D8 | `APPROVE_WITH_CORRECTION` |

The exact rules are in `governance/administrative_maintenance_council_decision.json` and ADR-0016.

## 16. Communication profile

GCL-TCS-00 clarity principles apply during the pilot as guidance. GCL-TCS-00 does not become binding maintenance authority until issue #108 completes G8 non-author Referee review and G9 Human Steward release.

Where communication vocabulary overlaps mathematical claim governance, the canonical mathematical claim ledger controls.

## 17. INTELLECT adoption

INTELLECT adoption has two phases.

### Phase A

Before Programme merge, INTELLECT records constitutional buy-in to:

- the authority split;
- the 0.1 acceleration factor;
- immediate material synchronization;
- stale-contract rejection;
- claim boundaries;
- the requirement for an exact protected pin after Programme merge.

### Phase B

After Programme merge, INTELLECT must:

- pin the exact protected Programme merge;
- pin the exact Git blob identities of the maintenance control, mirror policy, and decision record;
- reject missing, stale, branch-floating, or inflated contracts;
- pass exact-head INTELLECT CI and GCL conformance;
- merge through protected review.

Final cross-repository closure is prohibited before Phase B completes.

## 18. Release gate

Programme control merge requires:

1. schema and semantic validation;
2. adversarial tests;
3. Programme policy checks;
4. GCL conformance;
5. resolved D1–D8 decisions;
6. registered terminology;
7. non-author Referee approval;
8. Human Steward approval;
9. INTELLECT Phase A buy-in;
10. protected merge.

Final cross-repository closure additionally requires protected INTELLECT Phase B adoption and external attestation.

## 19. Claim boundary

This plan does not:

- prove a mathematical target;
- promote interface qualification to theorem proof;
- admit a campaign;
- verify a source;
- issue a certificate;
- authorize novelty, priority, patentability, mechanical, manufacturing, or commercial claims.
