# PAAR-C — Protected reviewer execution evidence V2 (staged)

**Scope:** GCL-ARC-001 PROTECTION-domain evidence. It does not create a new
certification office, independent mathematical proof, GitHub login, or
general-purpose review mechanism. Existing INTELLECT constitutional main
requires one native nonauthor GitHub approval.

## Producer and consumer sequence

1. Start from a known candidate MATH-PROGRAMME PR head SHA and material SHA-256.
   Run actual VERIFIER, ADVERSARY and REFEREE checks read-only at that source.
2. Capture the real stdout/stderr streams, exact command, environment, UTC time,
   exit code, logical pass ID, reviewer system ID and authenticated transport
   identity. Preserve binary-identical UTF-8 output. Mark one nonempty stream
   as \`selected_stream\` and hash precisely its UTF-8 bytes (SHA-256).
3. For every specialist pass and check index, create a source artifact at
   \`governance/agent_execution/executions/MATH-PROGRAMME-<head>/<role>-<index>.json\`
   in INTELLECT. Its record_type is
   \`GCL_PROTECTED_ROLE_EXECUTION_OUTPUT_V1\`. Include:
   \`subject\`, \`role\`, \`logical_pass_id\`, \`reviewer_system_id\`,
   \`transport_login\`, \`mode=non_authoring_read_only\`, \`command\`,
   \`exit_code=0\`, \`finding=PASS\`, \`observed_utc\`,
   \`environment={python,os,toolchain}\`, and
   \`output={stdout,stderr,selected_stream}\`.
4. Include an \`execution_evidence={path,blob_sha}\` pointer in each dossier
   \`checks[]\`, with the raw-output digest in \`receipt_sha256\`. Use
   \`GCL_AGENT_REVIEW_DOSSIER_V2\` as the dossier record type.
   Exact path and Git blob SHA must resolve to the protected object.
5. Submit the dossier **and every referenced raw-output artifact** in one
   protected INTELLECT PR. The GitHub source PR itself must introduce exactly
   those same blob identities. Require actual nonauthor **native GitHub
   APPROVED** review on the exact source PR head. A role pass recorded under
   the same institutional transport login is not a native approval. Preserve
   INTELLECT's status checks and merge protection.
6. After source PR protected admission, issue the separate
   \`GCL_PROTECTED_AGENT_ROLE_ADMISSION_EVIDENCE_V2\` receipt,
   \`schema_version=3.0.0\`, referencing the immutable dossier and the
   now-known source PR number, head and blob. The receipt itself must be
   protected under the existing INTELLECT receipt path.
7. MATH-PROGRAMME's existing specialist receipt adapter reads only
   the INTELLECT protected main and verifies all protected output bytes,
   digests, subject binding, logical role identity, source PR changed-file
   manifest, exact-head native nonauthor approval, native CI checks and
   stable protected branch. Reject missing or contradictory evidence.
   This checks **artifact authenticity and review provenance**, not the
   metaphysical fact that a command ran: the real independent reviewer
   remains responsible for replaying commands and examining the capture.

## Historical migration policy

The single already protected V1 PROTECTION receipt for PR #2624 remains
readable only when the subject head, material SHA-256, receipt Git blob,
dossier Git blob, original INTELLECT source PR #121 and source head all
match exact pinned historical identities in \`ci/agent_role_receipt.py\`.

This legacy result is classified
\`HISTORICAL_LOCKED_V1_NO_CONSUMER_OUTPUT_CHECK\`. It is **not** silently
upgraded to V2 or retroactively claimed to have a native GitHub approval.
No other newly fabricated or unbound V1 receipts may pass this route.

## Reproduce

\`python3 -m unittest -q tests.test_paar_role_evidence_v2 tests.test_specialist_receipt_adapter\`

The tests use a synthetic protected GitHub API and test genuine consumer
code. The positive mock has three protected raw-output artifact blobs and
a nonauthor exact-head native reviewer. Negatives include unbound V1
receipts, invented output hashes, changed output, blob drift, role drift,
output absent from native-reviewed PR, review absent/self/stale/dismissed,
failed CI and branch drift.

**Scope limit:** The positive V2 execution is a fixture, not a live
INTELLECT V2 admission. Follow-up requires an actual governed INTELLECT
producer transaction with independent replay. PAAR-wide certification
remains OPEN.
