# MATH-PROGRAMME Administrative Maintenance Plan

**Control:** `MP-ADMIN-MAINT-001`  
**Status:** Candidate pending Council decision  
**Programme tracker:** #182  
**Council authority tracker:** #183  
**Foundation:** seventh-pass closure merge `3cb6bfb9f132a4cfef279d0d3bf2309d99d0d6f1`

## 1. Purpose

This plan establishes a standing administrative system for the five-repository MATH-PROGRAMME umbrella:

- MATH-PROGRAMME;
- MATHFORGE;
- MATHSOLVE;
- MATHCERT;
- INTELLECT.

The system preserves **Core Clarity**. Core Clarity means that a reader, validator, or agent can answer six questions without inference:

1. What record is authoritative?
2. What exact object and revision does it identify?
3. What lifecycle, route, review, and claim state is current?
4. Which workflow validates that state?
5. What evidence proves that the workflow ran against the exact reviewed head?
6. What action is permitted next, and what remains prohibited?

The plan is administrative infrastructure. It cannot prove mathematics or authorize external claims.

## 2. Operating principles

### 2.1 One authority per state dimension

Protected repository records are authoritative. Mutable issues are navigation and discussion mirrors. A tracker may explain authority, but it cannot create authority.

The authority split is:

| State dimension | Authority |
|---|---|
| Programme portfolio, lifecycle, routing, admission | MATH-PROGRAMME |
| Source identity, provenance, provider manifest, provider waiver | MATHFORGE |
| Mathematical work package, campaign manifest, producer handoff | MATHSOLVE |
| Certification route, adjudication, output, certified scope | MATHCERT |
| Consumer projection and constitutional lifecycle semantics | INTELLECT |

### 2.2 Identity is content-sensitive

A repository head and a material artifact identity are different objects.

A downstream consumer must repin when a consumed artifact changes. It must not repin merely because an unrelated commit moves the provider repository head. Ceremonial repins increase noise and hide material changes.

Every change review must therefore classify the change as material or nonmaterial and record the evidence for that classification.

### 2.3 Historical evidence stays historical

A completed audit, closure, or conformance record is immutable. It may be superseded, but it is not rewritten into the present. Current-state records must identify their predecessor and state whether the predecessor is historical, superseded, or still independently authoritative for a bounded purpose.

### 2.4 Promotion fails closed

Missing, stale, contradictory, unreviewed, or unverified evidence cannot support promotion. Presentation, documentation, issue wording, or workflow existence cannot substitute for exact reviewed evidence.

Interface qualification remains interface qualification. It is not theorem proof.

## 3. Control architecture

The maintenance system has four control loops.

### 3.1 Event-triggered synchronization

Run this loop after any material change to:

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
8. publish an external post-merge attestation when the protected artifact cannot identify its own future merge.

An incomplete material synchronization has disposition `FAIL_CLOSED_MATERIAL_SYNC_INCOMPLETE`.

### 3.2 Weekly structural sweep

The proposed weekly sweep checks:

- protected heads;
- open pull-request interference;
- parseability of schemas and current-state records;
- required workflow presence;
- canonical tracker links;
- issue text that appears to claim protected authority;
- expired candidate review evidence;
- unexpected missing or duplicate canonical records.

This cadence is provisional until Council decision D1.

### 3.3 Monthly administrative portfolio review

The proposed monthly review checks:

- every active campaign;
- every candidate campaign;
- every archived campaign that still has live dependencies;
- provider manifest and waiver status;
- Solve handoff and Cert route concordance;
- consumer pins;
- workflow coverage;
- tracker freshness;
- open administrative P1 and P2 defects;
- maintenance burden and repeated manual work.

The output is a protected review record. A chat summary or issue comment is not sufficient evidence.

### 3.4 Quarterly deep conformance review

The proposed quarterly review performs:

- exact five-repository identity reconciliation;
- supersession and archival audit;
- adversarial mutation review;
- branch-protection and required-check verification;
- recurring-defect analysis;
- workflow evidence sampling;
- burden, consolidation, and retirement analysis.

A quarterly closure requires a versioned record, strict schema, adversarial tests, exact-head workflows, protected merge, and external post-merge attestation.

### 3.5 Annual constitutional review

The proposed annual review examines:

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

## 4. Workflow coverage model

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

The existence of a workflow file is not coverage.

### 4.1 Required capabilities

The umbrella coverage matrix must account for:

- schema and contract validation;
- unit tests;
- adversarial mutation tests;
- source or provider validation where applicable;
- campaign admission and routing validation where applicable;
- formal or certificate replay where applicable;
- documentation build where applicable;
- GCL conformance;
- branch-protection and release-trust evidence.

A capability may be non-applicable, but non-applicability must be explicit, scoped, reviewed, and testable.

### 4.2 Failure preservation

A clean workflow does not erase failed evidence. The maintenance record must identify where failed runs, replay logs, or rejected artifacts are preserved. A repair must distinguish a corrected defect from an ignored defect.

## 5. Tracker and issue hygiene

Every canonical tracker must contain:

- authority boundary;
- protected authority identity;
- current lifecycle and route state;
- exact next controlled obligation;
- claim boundary;
- review trigger.

A tracker refresh is required after a material state transition. The proposed target is two business days after protected merge, subject to Council decision D2.

A stale tracker does not override protected state. A contradictory canonical tracker blocks closure of the reconciliation that identified it.

Completed implementation issues should close. Long-lived campaign trackers may remain open when they clearly distinguish completed stages from the next obligation.

## 6. Defect classes and response

| Class | Meaning | Default response |
|---|---|---|
| P0 | Security, repository integrity, or evidence destruction risk | emergency containment; no promotion |
| P1 | Authority, identity, lifecycle, route, certificate, required-check, or claim-boundary mismatch | immediate fail-closed repair sequence |
| P2 | Missing coverage, stale canonical tracker, incomplete supersession, or unresolved ownership | tracked correction before next deep review; earlier when it affects interpretation |
| P3 | Documentation, naming, navigation, or low-risk administrative debt | batch into routine maintenance |

A lower class cannot be used to downgrade a defect that can affect authority or promotion.

## 7. Waivers

A waiver is an explicit temporary governance object, not an informal exception.

A waiver must record:

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

The proposed model allows Human Steward approval for at most 30 days and one renewal. Longer, repeated, cross-repository, provenance, certification, or required-check waivers require Council decision. These limits remain nonbinding pending D3.

No waiver can authorize mathematical or external claim promotion.

## 8. Independent review

The proposed policy requires a non-author Referee for changes to:

- authority hierarchy;
- lifecycle or promotion semantics;
- claim vocabulary or scope;
- provider, producer, or adjudicator boundaries;
- waiver classes;
- emergency powers;
- branch-protection or required-check weakening;
- a maintenance control whose failure could permit promotion.

Routine exact-identity repins and mirror refreshes do not require an independent Referee when semantics remain unchanged. This boundary remains subject to D4.

## 9. Emergency override

The proposed override exists only to restore availability, respond to a security incident, or restore CI operability.

It may not:

- promote a claim;
- admit a campaign;
- issue a certification disposition;
- weaken branch protection;
- delete required evidence.

The proposed maximum duration is 72 hours. Human Steward review is due within 24 hours. Council and Referee retrospective is due within seven days. The override expires automatically and reverts fail-closed. These rules remain subject to D6.

## 10. Maintenance-burden circuit breaker

The proposed circuit breaker freezes new campaign admission and refers the matter to the Council when:

- two consecutive monthly reviews fail;
- a P1 authority or identity mismatch remains unresolved for seven days;
- more than 20 percent of active campaigns lack complete workflow coverage;
- required-check or branch-protection evidence is missing;
- the same control defect recurs in two consecutive quarterly reviews.

The Council may consolidate controls, increase automation, archive obsolete records, change ownership, suspend campaigns, or restore normal operation. This remains subject to D7.

## 11. Council decisions

Issue #183 requests decisions D1–D8:

| Decision | Question |
|---|---|
| D1 | Mandatory maintenance cadence |
| D2 | Freshness clocks and fail-closed thresholds |
| D3 | Waiver authority, duration, and renewal |
| D4 | Independent Referee triggers |
| D5 | Issue-mirror enforcement level |
| D6 | Emergency override powers and retrospective |
| D7 | Maintenance-burden circuit breaker |
| D8 | GCL-TCS-00 maintenance profile |

Until these decisions are resolved, the candidate control records proposed values but sets `effective: false` and `may_promote_now: false`.

## 12. Communication profile

GCL-TCS-00 clarity principles may guide the pilot. GCL-TCS-00 is not binding maintenance authority until issue #108 completes G8 non-author Referee review and G9 Human Steward release.

Where communication vocabulary overlaps mathematical claim governance, the canonical mathematical claim ledger controls.

## 13. Promotion and release gate

The maintenance control may become binding only after:

1. schema validation;
2. semantic validation;
3. adversarial mutation tests;
4. Programme policy checks;
5. GCL conformance;
6. Council decisions D1–D8;
7. non-author Referee review;
8. Human Steward release;
9. protected merge;
10. external post-merge attestation.

Until then, existing protected Programme, Forge, Solve, Cert, and INTELLECT contracts remain authoritative.

## 14. Claim boundary

This plan does not:

- prove a mathematical target;
- promote interface qualification to theorem proof;
- admit a campaign;
- verify a source;
- issue a certificate;
- authorize novelty, priority, patentability, mechanical, manufacturing, or commercial claims.
