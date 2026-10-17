# PAAR-C — Corroborated execution origin (GitHub-hosted replay)

## Gap and bounded remedy

The existing GCL-ARC-001 PROTECTION V2 receipt locks raw stdout/stderr to
Git blobs, hashes, reviewed source and native reviewer events. Those fields
alone cannot establish that a command actually ran. A reviewer can read a
faithful file without knowing whether the captured stdout was fabricated.

This work package adds a **distinct GitHub-hosted Actions rerun** of the
three permitted checks, using reviewed code from the protected MATH-PROGRAMME
`main` branch. The workflow never approves a pull request and never writes
to a protected repository. The workflow has read-only permissions, executes
only code from protected main with sanitized environment and no retained Git credentials,
and uploads a bounded JSON witness from the real runner.

The authenticated GitHub API supplies independent evidence of the run
event, protected workflow head, run attempt, completed job, GitHub-hosted
runner group, successful execution/upload steps and run-scoped artifact.
`verify-live` independently downloads that artifact from its original run
and checks exact source identity and every selected stdout/stderr hash.

**Trust limits:** This corroborates *a separately executed platform replay*
of the same assertions, not the provenance of the original CHAD process.
GitHub workflow records are platform assertions, not a hardware
cryptographic remote-attestation certificate. A passing test does not prove
the proposition tested. The original V2 receipt is not silently upgraded.
A GitHub Actions artifact expires after 90 days; promote a bounded receipt
and digest through governed protected source before relying on long-term
replay. Do not claim GCL-wide integrity certification.

## Execution protocol

1. Admit this workflow and verifier through ordinary MATH-PROGRAMME
   protected PR, CI and independent technical review as appropriate.
2. From protected `main`, dispatch
   `.github/workflows/paar-execution-origin.yml` with inputs:
   `pr_number=2710`,
   `candidate_sha=b380e583ca2c997c07a4b7f15cbf97728006a79e`,
   `material_sha256=b6b353decee67953b74c984a1c8856c3ea56debbae0599f759564f13bbe214b4`.
3. A bounded Ubuntu GitHub-hosted runner checks protected workflow SHA,
   protected main Git head, merged PR metadata, canonical changed-file hashes
   and exact per-file Git blob equivalence between the reviewed candidate and protected main,
   then exact allowlisted commands. It runs VERIFIER (14 tests),
   ADVERSARY (36 tests), and REFEREE (offline PAAR replay, bounded only).
   No arbitrary command is accepted from workflow inputs, and no user-selected
   revision is checked out or executed.
4. Record resulting GitHub run URL, ID, attempt, workflow SHA, artifact ID,
   exact candidate SHA, material digest, roles and result. Run
   `python3 ci/paar_execution_origin.py verify-live --run-id <RUN_ID>`.
   The verifier downloads the artifact using authenticated GitHub and
   rejects stale/missing/failed/expired/altered runs, source, artifacts
   or role output. When protected `main` advances, the historical run
   remains admissible only if the authenticated GitHub compare API proves
   the exact workflow commit is an ancestor of the current protected head
   with zero divergent ancestry; the source files remain pinned to the
   original workflow commit. Missing, divergent, rebased or nonprotected
   history fails closed. This preserves replay after a later evidence PR
   merges, without making the historical run attest later code.
5. Persist the independently reviewed platform witness and its digest
   through normal protected governance if it will serve as durable evidence.
   Do not retroactively assert that this workflow authenticated
   the previously captured CHAD stdout/stderr.

## Bounded test matrix

`python3 -m unittest -q tests.test_paar_execution_origin`

Mocked negative controls reject non-dispatch events, failed platform jobs,
private runner groups, missing runner steps, nonprotected/divergent main or fabricated ancestry,
expired or unrelated artifacts, wrong role, fabricated stdout digest,
incorrect/refuted referee assertions, material drift, unmerged/forked
sources and prohibited scope promotion. A mock positive is a unit test,
**not** evidence of an actual GitHub-hosted execution. The live run and
authenticated artifact download are mandatory for that claim.

## Future producer contract

Promote a new receipt/version requiring platform witness metadata only
after a real positive replay and source-side independent review. Do not
silently broaden existing V2 acceptance or fabricate historical execution
attestations. GCL-PAAR-001 and its estate-wide A/B/D/E audits remain open.

## V3 protected source and separately governed receipt — Pilot

INTELLECT #126 introduces source PR #127 with the original, real GitHub-hosted
run #38988609732 witness and a V3 source dossier. MATH-PROGRAMME's
`ci/paar_v3_origin_consumer.py` is a **new opt-in PROTECTION-origin verifier**.
It does not change older V1/V2 receipt acceptance. The V3 success claim is
restricted to the *later GitHub-hosted execution*; original October 15 CHAD
execution origin remains UNATTESTED.

A positive V3 claim requires **all** of the following: the independently
reviewed and merged INTELLECT source PR #127 exact head; real original
run-scoped witness/dossier bytes introduced by that source PR; a different,
separately merged and independently approved INTELLECT V3 receipt PR that
introduces its own exact receipt blob; current protected INTELLECT main and
stable Git blobs; independent download of the original GitHub Actions
artifact; and authenticated successful original run/job/step and source
manifest readback. Review and production platform evidence are independent
requirements. No local output hash alone is sufficient.

Production invocation, **only after** a genuine protected V3 receipt PR exists:
`python3 ci/paar_v3_origin_consumer.py --receipt-pr <actual-receipt-pr-number>`.
An absent source, missing native approval, unmerged receipt, expired artifact,
blob/content drift or failed hosted run aborts the check. Mock-positive unit
tests do **not** certify that a real V3 receipt exists. PR #127 and its
subsequent receipt must be protected-admitted before a real live end-to-end
V3 PASS can be asserted. Preserve the `original_chad_execution_attested=false`
limit permanently until genuine contemporaneous evidence is recovered.
