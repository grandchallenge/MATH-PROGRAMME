# MP-REL-TRUST-MATHCERT-EXACT-HEAD-LIVELOCK-001

Issue: #685

## Defect

MATHCERT remained subject to `strict_required_status_checks_policy: true` after MATH-PROGRAMME had already corrected the same exact-head/current-base livelock under #569/#570.

The failure mode is the same: a candidate may remain byte-identical and retain successful required checks, yet become unmergeable solely because unrelated protected `main` movement changes the merge base. Re-synchronizing that unrelated movement into the candidate changes the exact head and invalidates review/evidence. MATHCERT PR #169 demonstrated this directly when an exact-head independent approval was dismissed with GitHub reason `The merge-base changed after approval.`

## Bounded correction

The release-trust repository strictness map is changed to:

- `grandchallenge/MATHCERT`: `false`
- `grandchallenge/MATHSOLVE`: `true`
- `grandchallenge/MATH-PROGRAMME`: `false`
- `grandchallenge/INTELLECT`: `true`

This ports only the proven MATH-PROGRAMME anti-livelock behavior to MATHCERT. The shared default remains strict and MATHSOLVE/INTELLECT remain strict.

## Preserved controls

For MATHCERT this repair does not remove or rename any required status context. The exact required contexts remain:

- `certify`
- `policy / policy`
- `security / action-policy`

The repair also preserves stale-review dismissal on actual candidate pushes, required conversation resolution, zero bypass actors in the governed release-trust payload, force-push/deletion prohibitions, independent exact-head review requirements where governing procedures require them, expected-head protected merge semantics, and protected-main readback.

`strict=false` changes only GitHub's requirement that a candidate contain the latest protected-main commit before merge. It does not convert a missing, pending, cancelled, skipped, or failed required check into success.

## Scope boundary

No MATHCERT certificate, OTP result-family state, route, adjudication, output, mathematical claim, aggregate authority, or cross-family authority is changed by this control-plane repair.

No MATHSOLVE, MATH-PROGRAMME, or INTELLECT release-trust semantics are changed except that the exact strictness map now records the MATHCERT exception.

## Activation

Protected source admission does not itself modify the live MATHCERT ruleset. After protected merge, the governed `Release trust administration` workflow must apply the contract and a fresh live readback must show the MATHCERT `Cert profile - main` ruleset with:

- `strict_required_status_checks_policy: false`;
- all three required contexts intact;
- pull-request review controls intact;
- no bypass actors;
- deletion/non-fast-forward protections intact.

Only that readback closes the operational defect.
