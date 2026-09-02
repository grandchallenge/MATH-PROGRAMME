# MATH-PROGRAMME Administrative Maintenance Plan

**Control:** `MP-ADMIN-MAINT-001`  
**Decision lineage:** `MP-ADMIN-DECISION-001`; `ADR-0016`  
**Current operating interpretation:** amended by `MP-STREAMLINED-EXECUTION-001` and `AGENT_CADENCE_OPERATING_DESIGN.md`  
**Programme tracker:** #182  
**Foundation:** seventh-pass closure merge `3cb6bfb9f132a4cfef279d0d3bf2309d99d0d6f1`

## 1. Purpose

This plan maintains administrative Core Clarity across MATH-PROGRAMME, MATHFORGE, MATHSOLVE, MATHCERT, and INTELLECT.

A reader, validator, or agent should be able to answer without inference:

1. What record is authoritative?
2. What material object and revision does it identify?
3. What lifecycle, route, review, and claim state is current?
4. Which workflow or validator establishes the relevant state?
5. What material evidence supports the conclusion?
6. What action is permitted next, and what remains prohibited?

This is administrative infrastructure. It cannot prove mathematics or authorize external claims.

## 2. Current execution model

The original accelerated pilot and its fixed countdowns are historical operating evidence. They are not the current routine cadence.

Current maintenance is event-driven and material-closure based:

- routine bounded work uses standing delegated authority;
- protected branches may advance concurrently;
- evidence binds to material closure rather than whole-repository freshness;
- affected checks are selected by impact routing;
- expensive formal, external, and computational replay runs only when its material inputs change, on explicit dispatch, or on scheduled assurance;
- protected readback completes the routine transaction without a second approval cycle;
- specialist non-author review is reserved for substantive mathematical certification, source-semantic adjudication, constitutional authority expansion, security-sensitive protection weakening, and external claim promotion.

There is no programme-wide countdown whose expiry itself creates work or authority. Campaigns and controls keep their own bounded terminal conditions where materially justified.

### Historical pilot parameters

ADR-0016 originally recorded a 0.1 acceleration factor and intervals including a nine-day pilot, 16h48m structural sweep, three-day portfolio review, nine-day deep conformance review, and 36d12h constitutional review. Those values remain historical evidence of the admitted pilot; they do not require recurring administrative transactions now. `docs/governance/AGENT_CADENCE_OPERATING_DESIGN.md` records the superseding cadence interpretation.

## 3. Authority model

Protected repository records are authoritative. Issues are mutable navigation and discussion mirrors.

| State dimension | Authority |
|---|---|
| Programme portfolio, lifecycle, routing, admission | MATH-PROGRAMME |
| Source identity, provenance, provider manifest, provider waiver | MATHFORGE |
| Mathematical work package, campaign manifest, producer handoff | MATHSOLVE |
| Certification route, adjudication, output, certified scope | MATHCERT |
| Consumer projection, stale-contract rejection, lifecycle semantics | INTELLECT |

INTELLECT is an adoption and freshness-enforcement partner. Its routing and release-trust controls do not transfer mathematical or source authority to INTELLECT.

## 4. Identity, concurrency, and supersession

A repository head and a material artifact identity are different objects.

A downstream consumer repins when a consumed artifact changes. It does not repin merely because an unrelated commit moves the provider repository head. Historical audits, closures, and conformance records remain historical; a later record may supersede their current operational interpretation without rewriting the historical event.

A candidate does not require branch synchronization merely because protected `main` advanced. It remains valid when it is mergeable, its relevant protected dependencies and material closure are unchanged, its affected checks pass, and its scope or authority has not widened.

## 5. Promotion boundary

Missing, stale, contradictory, unreviewed, or unverified **required** evidence fails closed. “Required” is determined by the material claim, authority boundary, current machine contract, and applicable specialist-review rule; it is not a synonym for every review or every workflow in the estate.

Presentation, documentation, issue wording, workflow-file presence, or a historical successful run cannot create current mathematical or certification authority. Interface qualification remains interface qualification. It is not theorem proof.

## 6. Event-triggered material propagation

After a material change to a campaign lifecycle, provider manifest, Solve handoff, Cert route, Programme runtime/routing/claim contract, INTELLECT provider pin, required workflow, or repository protection:

1. classify the material change;
2. identify affected authoritative artifacts and consumers;
3. update only materially affected contracts;
4. preserve unchanged content-addressed identities;
5. run the affected checks selected by current policy;
6. obtain specialist review only if the material boundary requires it;
7. merge through protection under the applicable delegated or reserved authority;
8. perform protected readback and update navigation mirrors that materially depend on the transition.

“Synchronization” here means propagation of changed governed contracts. It does not mean rebasing a branch or making every consumer repository numerically current.

## 7. Assurance

Assurance is layered rather than timer-driven.

### Event-driven assurance

Run immediately when a material transition changes authority, lifecycle, route, certification, claim scope, workflow semantics, required-check policy, or consumed evidence identity.

### Scheduled assurance

Low-frequency scheduled workflows may exercise full sentinels, expensive replay paths, policy dependency maps, publication reconstruction, and repository administration. Scheduled assurance exists to test paths that transition-local impact routing intentionally avoids running on every pull request.

### Explicit deep review

A Human Steward, Council office, or authorized operator may explicitly dispatch a deeper review where recurring defects, control-plane changes, cross-repository ambiguity, or material risk justify it. The review should reuse existing evidence and controls rather than manufacture a new governance layer.

## 8. Workflow coverage

A workflow or governed non-applicability record is covered when its capability, trigger, required-context role, affected-input rule, evidence location, owner, repair route, and last verified material identity are known.

Programme policy is a routed DAG. `validate-json` is the stable aggregate required context over selected shards; it is not proof that every policy shard ran. The current executable detail is maintained in `docs/WORKFLOW_COVERAGE.md` and `governance/policy_shard_registry.json`.

Formal and computational evidence may complete through protected material-identity reuse when unchanged. Repository regression is complementary residual coverage and must not serially rerun suites already owned by dedicated shards.

## 9. Tracker and issue hygiene

Every canonical tracker should state the authority boundary, protected authority identity, current lifecycle/route state, next controlled obligation, claim boundary, and review trigger.

Refresh a tracker after a protected **material** transition when the existing mirror would otherwise become stale or contradictory. There is no standing hourly refresh clock. A stale but noncontradictory mirror is administrative debt; a contradictory authority-bearing mirror is repaired promptly because it can misdirect operators.

Issues and comments remain navigation. They cannot create protected authority.

## 10. Defect classes

| Class | Meaning | Default response |
|---|---|---|
| P0 | Security, repository integrity, or evidence-destruction risk | emergency containment; no promotion |
| P1 | Authority, identity, lifecycle, route, certificate, required-check, or claim-boundary mismatch | immediate bounded fail-closed repair |
| P2 | Missing coverage, stale canonical tracker, incomplete supersession, or unresolved ownership | tracked correction before affected promotion or the next relevant maintenance pass |
| P3 | Naming, navigation, or low-risk administrative debt | batch into routine maintenance |

A lower class cannot downgrade a defect that affects authority or promotion.

## 11. Waivers and emergency recovery

A waiver is a typed, scoped, expiring governance object. It cannot authorize mathematical or external claim promotion.

Security-sensitive weakening, required-check removal, cross-repository authority expansion, certification waiver, or comparable constitutional exception remains outside routine delegation and requires the authority specified by the governing instrument. Routine implementation inconvenience is not a waiver case.

Emergency action is limited to restoring availability, responding to a security incident, or restoring CI operability. It may not promote a claim, admit a mathematical campaign without authority, issue certification, delete required evidence, or leave repository protection weakened after recovery.

Historical ADR-0016 emergency durations remain historical pilot parameters; current recovery is bounded by the incident and current superior controls rather than a standing countdown inherited from that pilot.

## 12. Review proportionality

A non-author specialist Referee is appropriate for changes to:

- substantive mathematical certification or theorem-level claim promotion;
- source-semantic adjudication or provenance exceptions;
- authority hierarchy, lifecycle, or promotion semantics;
- provider, producer, or adjudicator jurisdiction;
- constitutional waiver classes or emergency powers;
- security-sensitive branch-protection or required-check weakening;
- control changes whose failure could materially authorize promotion or bypass a substantive boundary.

Routine semantic-preserving repins, issue mirrors, documentation, bounded engineering, ordinary workflow maintenance, and similar authorized administration use standing delegated disposition plus affected checks. They do not require a fresh independent approval.

Review evidence binds to the material object under review. Unrelated `main` movement does not make it stale.

## 13. Maintenance-burden circuit breaker

Administrative machinery must not consume more recurring computational, human, or cognitive cost than the material risk it reduces.

Open a bounded repair or freeze only the affected promotion path when:

- a critical required capability is absent or materially broken;
- required repository protection is missing;
- current authoritative records contradict each other;
- a material dependency cannot be resolved safely;
- the same material defect recurs and indicates that the existing control is inadequate.

Do not freeze unrelated campaigns because a timer expired, a repository head advanced, or a routine mirror is late. Prefer consolidation, automation, retirement, or narrower impact routing over adding more review and CI stages.

## 14. Release trust and INTELLECT

The original INTELLECT Phase A/Phase B adoption sequence is historical admission evidence. Current repository administration is governed by `governance/release_trust_admin_contract.json`, `ci/release_trust_admin.py`, and `docs/RELEASE_TRUST_ADMINISTRATION.md`.

The current Release Trust contract uses repository-specific `strict_status_checks: false` so mergeable concurrent development does not require an update-branch synchronization solely for freshness. GitHub approval count is zero. Required checks remain exact per repository, and INTELLECT includes `routing-enforcement`.

Changing those protections is a control-plane change. Applying the already-admitted contract is routine administration.

## 15. Routine release gate

For bounded work already within authorized scope:

1. classify the material closure;
2. run affected protected checks;
3. satisfy any route-specific machine contract that genuinely applies;
4. exercise standing delegated disposition;
5. protected merge;
6. protected readback.

Add specialist review or Human Steward action only when the governing boundary expressly reserves it. Do not add such gates because a commit is new, a branch is behind, or an unrelated protected commit appeared.

## 16. Historical decision record

ADR-0016 and its D1–D8 Council dispositions remain part of the programme's history. Their pilot timing and admission mechanics are not silently rewritten; this current plan states how they are interpreted after `MP-STREAMLINED-EXECUTION-001` and the later concurrency/impact-routing controls.

## 17. Claim boundary

This plan does not:

- prove a mathematical target;
- promote interface qualification to theorem proof;
- verify a source;
- issue a certificate;
- authorize novelty, priority, patentability, mechanical, manufacturing, or commercial claims.
