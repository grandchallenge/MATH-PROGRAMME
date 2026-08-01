# ADR-0016: Adopt accelerated Core Clarity maintenance

## Status

Accepted by the Human Steward on 2026-07-31, subject to protected merge, exact-head validation, non-author Referee review, and INTELLECT adoption.

## Context

Seven umbrella reconciliation passes established a coherent authority split among MATH-PROGRAMME, MATHFORGE, MATHSOLVE, MATHCERT, and INTELLECT. The remaining administrative risk is not lack of governance structure. It is drift in current-state contracts, workflow evidence, canonical trackers, supersession records, and cross-repository consumer pins.

PR #184 introduced `MP-ADMIN-MAINT-001`, a candidate standing maintenance control, and Council issue #183 requested decisions D1–D8. The Council offices recommended event-triggered synchronization, measured periodic review, typed waivers, independent review for promotion-sensitive changes, explicit issue-mirror enforcement, narrow emergency authority, a maintenance-burden circuit breaker, and nonbinding use of GCL-TCS-00 during the pilot.

The Human Steward approved that substance and directed that every proposed time estimate and cadence interval be reduced by a factor of ten. Event-triggered obligations remain immediate.

## Decision

1. Adopt the Core Clarity invariants and five-repository authority split in `MP-ADMIN-MAINT-001`.
2. Record all Council decisions D1–D8 as resolved in `governance/administrative_maintenance_council_decision.json`.
3. Apply an exact maintenance acceleration factor of `0.1` to every proposed duration and cadence interval.
4. Run a nine-day pilot beginning at the protected merge timestamp of PR #184.
5. Use the following accelerated intervals:
   - structural sweep: every 16 hours 48 minutes;
   - administrative portfolio review: every 3 days;
   - deep conformance review: every 9 days;
   - constitutional review: every 36 days 12 hours;
   - canonical tracker refresh: within 7 hours 12 minutes;
   - ordinary Steward-approved administrative waiver: at most 3 days, with one renewal;
   - emergency override: at most 7 hours 12 minutes;
   - emergency Steward review: within 2 hours 24 minutes;
   - Council and Referee emergency retrospective: within 16 hours 48 minutes;
   - unresolved P1 circuit-breaker interval: 16 hours 48 minutes.
6. Keep material cross-repository synchronization in the same governed change sequence. This obligation is immediate and is not delayed by periodic cadence.
7. Require Council authority for cross-repository, provenance, certification, or required-check waivers. No waiver may authorize claim promotion.
8. Require a non-author Referee for authority, lifecycle, claim, role-boundary, waiver-class, emergency-power, branch-protection, required-check, or promotion-sensitive changes.
9. Adopt `MP-ADMIN-MIRROR-001`: issues are navigation and discussion mirrors only; contradiction or authority inflation is P1 fail-closed; ordinary noncontradictory staleness is P2; identified contradictions block reconciliation closure.
10. Limit emergency authority to availability, security, or CI restoration. Emergency authority cannot promote claims, admit campaigns, adjudicate certification, weaken branch protection, or delete required evidence.
11. Fail closed immediately for any campaign missing a critical workflow capability. Freeze new umbrella admissions when two active campaigns or more than 20 percent of the active portfolio are incomplete, whichever threshold is stricter, or when other D7 triggers apply.
12. Use GCL-TCS-00 principles during the accelerated pilot, but do not make GCL-TCS-00 binding until issue #108 completes G8 and G9. The canonical mathematical claim ledger remains controlling.
13. Require INTELLECT buy-in before final administrative closure. INTELLECT must consume the protected maintenance identity, reject stale or missing maintenance contracts, and preserve the same claim boundaries.
14. Activate the pilot only through protected merge. PR text, issue comments, draft branches, and review records cannot create operative authority.

## Council dispositions

| Decision | Disposition |
|---|---|
| D1 | `APPROVE_WITH_CORRECTION` — accelerated nine-day pilot and scaled cadence |
| D2 | `APPROVE_WITH_CORRECTION` — immediate material synchronization and 7h12m mirror clock |
| D3 | `APPROVE_WITH_CORRECTION` — 3-day ordinary waiver; Council-only critical waivers |
| D4 | `APPROVE` — independent review triggers retained |
| D5 | `APPROVE_WITH_CORRECTION` — binding issue-mirror policy and 7h12m refresh clock |
| D6 | `APPROVE_WITH_CORRECTION` — accelerated emergency limits |
| D7 | `APPROVE_WITH_CORRECTION` — campaign-level fail-close and accelerated circuit breaker |
| D8 | `APPROVE_WITH_CORRECTION` — GCL-TCS-00 principles remain nonbinding during pilot |

## Consequences

- Full umbrella reconciliations become periodic assurance events rather than the default response to every change.
- Material changes continue to trigger immediate synchronized repair.
- The nine-day pilot produces operating evidence quickly enough for the accelerated programme schedule.
- INTELLECT becomes an explicit consumer and enforcement partner for maintenance-state freshness.
- Administrative exceptions remain narrower than the controls they modify.
- Failed runs, stale evidence, and review defects remain preserved as audit evidence.

## Rejected alternatives

### Retain the 90-day pilot

Rejected by the Human Steward as incompatible with the accelerated programme schedule.

### Scale only the pilot duration

Rejected. The instruction applies to every timing estimate and cadence interval.

### Let issues carry current authority

Rejected. Issues remain mutable navigation surfaces.

### Permit ordinary Steward waivers for certification or required checks

Rejected. These exceptions can affect promotion and require Council authority.

### Treat INTELLECT adoption as optional

Rejected. The consumer layer must enforce stale-contract rejection and constitutional consistency.

## Affected artifacts

- `governance/administrative_maintenance_council_decision.json`
- `governance/administrative_maintenance_control.json`
- `governance/issue_mirror_enforcement_policy.json`
- `schemas/administrative_maintenance_council_decision.schema.json`
- `schemas/administrative_maintenance_control.schema.json`
- `schemas/issue_mirror_enforcement_policy.schema.json`
- `ci/validate_administrative_maintenance_control.py`
- administrative maintenance tests and review records
- `docs/governance/ADMINISTRATIVE_MAINTENANCE_PLAN.md`
- `docs/AGENT_COUNCIL_TERMINOLOGY_REGISTRY.md`
- `docs/AGENT_COUNCIL_DECISION_RECORDS.md`
- `docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md`
- INTELLECT adoption issue, contract, tests, PR, and protected merge evidence

## Claim boundary

This decision governs administrative maintenance only. It does not prove a mathematical target, promote interface qualification to theorem proof, admit a campaign, verify a source, issue a certificate, or authorize novelty, priority, patentability, mechanical, manufacturing, or commercial claims.
