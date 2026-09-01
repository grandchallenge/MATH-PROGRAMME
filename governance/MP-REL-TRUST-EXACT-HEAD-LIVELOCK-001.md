# MP-REL-TRUST-EXACT-HEAD-LIVELOCK-001

Issue: #569

## Defect

MATH-PROGRAMME release-trust protection currently combines exact-head certification/review with strict required-status-check freshness against a high-churn protected `main`. A reviewed candidate that has already passed all required checks becomes unmergeable when unrelated work advances `main`; synchronizing `main` back into the candidate then changes the reviewed head and invalidates exact-head evidence. PR #519 demonstrated this loop repeatedly.

## Bounded correction

The release-trust contract now declares required-status-check strictness per governed repository while retaining the shared strict default.

The exact effective map is:

- `grandchallenge/MATHCERT`: `true`
- `grandchallenge/MATHSOLVE`: `true`
- `grandchallenge/MATH-PROGRAMME`: `false`
- `grandchallenge/INTELLECT`: `true`

The administration runtime derives an effective repository policy before both ruleset application and ruleset readback. Contract validation fails closed if this map or any required-check context drifts.

## Preserved controls

This repair does not remove or rename any required status check. It preserves stale-review invalidation on candidate pushes, required conversation resolution, zero bypass actors, force-push/deletion prohibitions, expected-head merge semantics, independent exact-head review requirements, and protected-main readback.

For MATH-PROGRAMME, `strict=false` changes only GitHub's requirement that the candidate branch contain the latest protected-main commit before merge. It does not convert a missing, pending, cancelled, skipped, or failed required check into success.

## Future integration testing

Ephemeral current-base integration testing through a separately governed merge queue / merge-group design may be added later. It is not part of this bounded correction and must not mutate a reviewed candidate head.

## Activation

Merging this source change does not itself alter the live repository ruleset. After protected admission, the governed release-trust administration workflow must apply the contract and the resulting live ruleset must be read back before the repair is treated as operative.
