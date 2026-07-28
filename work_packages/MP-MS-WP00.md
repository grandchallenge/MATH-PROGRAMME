# MP-MS-WP00 — Programme-Wide MATHSOLVE Routing Audit

## Result

All eight ACTIVE MATH-PROGRAMME campaigns now have a pinned MATHSOLVE provider route. The audit distinguishes native Solve work from retrospective registration and identifies every campaign whose Solve-owned work remains embedded in MATH-PROGRAMME.

## Inventory

| Campaign | Coverage | Placement | Solve record | Cert state | Future promotion |
| --- | --- | --- | --- | --- | --- |
| UC-001 | native | MATHSOLVE | MS-UC-WP04 | partial | blocked by open conjecture and legacy coverage debt |
| NS-CI-001 | native | MATHSOLVE | NS-CI-R014-A2 | partial | blocked by open A2/L5 obligations |
| HC-001 | native | MATHSOLVE | HC-WP00 | partial | blocked by open conjecture and no selected target |
| BSD-001 | retrospective | MATH-PROGRAMME | BSD-WP00-WP04-RETROSPECTIVE | pending | migration required |
| PNP-001 | retrospective | MATH-PROGRAMME | PNP-WP00-WP02-RETROSPECTIVE | pending | migration required |
| RH-001 | retrospective | MATH-PROGRAMME | RH-WP00-WP02-RETROSPECTIVE | pending | migration required |
| YM-001 | retrospective | MATH-PROGRAMME | YM-WP00-WP02-RETROSPECTIVE | pending | migration required |
| OZ-001 | retrospective | MATH-PROGRAMME | OZ-WP00-RETROSPECTIVE | pending | source intake and migration required |

## Exact lineage

`governance/mathsolve_routing_audit.json` pins:

- MATHSOLVE provider commit `ec84e40aff4d926c5962653fd313bfb4db1adb8a`;
- each `campaign_manifests/<CAMPAIGN>.json` path;
- each manifest Git blob SHA-1;
- the exact MATHFORGE provider commit, manifest path, and blob identity;
- Solve Work Package identifiers;
- MATHCERT state and issue where available;
- current blockers.

The registry does not guess absent Cert issues or call pending work certified.

## Misplaced work

The audit identifies BSD, PNP, RH, YM, and OZ as `programme_embedded`. Their historical bundles remain authoritative at their exact MATH-PROGRAMME commits. MATHSOLVE retrospective manifests preserve those identities and record migration debt.

Future theorem-spine, proof-attempt, route-selection, failed-route, restricted-target, or mechanism work for those campaigns is prohibited in MATH-PROGRAMME unless a reviewed waiver is recorded.

## Promotion gate

`ci/validate_mathsolve_routing.py` fails closed when:

- an ACTIVE campaign lacks a route or waiver;
- the pinned provider commit drifts;
- a route is incomplete;
- Programme-embedded work attempts to advance beyond retrospective WP00 registration;
- a mathematical claim reaches claim promotion or integration without a complete MATHCERT handoff state.

`pending` and `partial` Cert states preserve lineage but do not authorize claim promotion.

## Claim boundary

This audit promotes no mathematical claim. It changes governance and repository routing only. Every campaign retains the mathematical blockers recorded in its MATHSOLVE manifest.

## Next obligations

1. Merge and pin MS-GOV-WP00 after review.
2. Migrate the next active stages of BSD, PNP, RH, YM, and OZ into native MATHSOLVE Work Packages.
3. Open claim-specific MATHCERT handoffs as targets become exact enough for checking.
4. Add the routing gate to every future campaign promotion workflow.
5. Project GitHub lineage into AETHER only after GitHub-first conformance is stable.
