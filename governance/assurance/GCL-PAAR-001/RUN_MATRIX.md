# GCL-PAAR-001 — Reproducibility and independent audit matrix

The baseline is a sampled observation, not global certification. No live status changes are made by the commands below.

| Obligation | Command or evidence | Expected result | Important limitation |
|---|---|---|---|
| PAAR-00 | python3 governance/assurance/GCL-PAAR-001/replay_baseline.py --offline | Six pinned repositories, fourteen pinned files, internal receipt consistency and hostile-data negative controls PASS | Saved data are not live-source authentication |
| PAAR-01 | python3 governance/assurance/GCL-PAAR-001/replay_baseline.py --live | Re-fetch 14 blobs at exact pinned commits; report current branch drift/protection, no writes | Only 14 known controls, not assertion coverage |
| PAAR-02 | python3 -m unittest -v ci.test_erdos_compendium_publication_gate ci.test_erdos_compendium_editorial_replay | Initial run 40/40 PASS, including duplicate, stale and forged source checks | Selected publication subsystem only |
| PAAR-03 | python3 ci/validate_policy_reachability.py | Existing policy command registry reachability PASS | Reachability is not semantic truth |
| PAAR-04 | Independently source-check EC-BULK-007 manifest, Project RETURNED receipt, live public rendering receipt and admissions ledger at exact source SHA | 168 returns, 168 Project RETURNED, 168 public UNACCEPTED, 173 real browser pages, 2807 MathJax expressions, no EC007 V2 admission at baseline | One bounded specimen, not all published GCL claims |
| PAAR-05 | Run current protected MATHCERT certificate/assumption-source checks and adversarial theorem-promotion negatives with exact toolchain | Certification level cannot exceed reproduced proof/evidence level | PENDING specialist execution |
| PAAR-06 | Independently replay INTELLECT logical-role provenance and CONTROL transport/security return boundaries | No unsupported self-review or false shared-login identity claims | PENDING specialist execution |
| PAAR-07 | Independently replay MATHSOLVE source return and MATHFORGE evidence intake, including unavailable/unclaimed items | Accurate AVAILABLE/CLAIMED/RETURNED and source evidence fingerprints | PENDING specialist execution |
| PAAR-08 | Reconcile actual operator console, public docs and dashboards to protected authority at a sampled exact head | No fabricated status, unsupported mathematically certified/public claim | PENDING specialist execution |
| PAAR-09 | In-memory/sandbox hostile receipts: tampered blob, forged authority, stale head, duplicate, changed theorem, invalid independent role, missing source | Fail closed, no corrupted protected writes | PENDING cross-system specialist execution |

## Authoritative capture

The AUDIT_BASELINE.json file contains commit and Git blob SHA values for all fourteen selected controls and labels each claim VERIFIED_BOUNDED or UNVERIFIED. To obtain an independent live readback, run PAAR-01 with an authenticated GitHub CLI and explicitly compare each source SHA. A changed branch head is DRIFT, not automatic failure or an excuse to silently overwrite the historical receipt.

For each independently executed new test, capture: UTC time, protected main SHA, path and blob SHA, user/agent logical role and real transport identity, command input/digest, code dependency/toolchain, expected output, raw stdout/stderr or proof certificate, output digest, negative control, claim limitations and exact admission authority.

No credentials, private keys or sensitive authentication values may be persisted in public artifacts.

## Closure and failure policy

Do not claim full conformance from these sampled PASS results. Every UNKNOWN remains UNKNOWN until evidence is produced. If the original system rejects a tampered receipt, link the exact test and scope. If it accepts a forged promotion, mark NONCONFORMANT, identify owner and reproduce using the existing governed remediation path. Closure requires independent specialist audit of the full conformance matrix and protected final evidence at exact SHA, with explicitly bounded exclusions if any.

The prior GCL contracts remain authoritative; this workstream neither modifies nor supersedes them.
