# GCL Erdős catalogue — source-return queue projection

**Authoritative implementation:** `ci/erdos_catalogue_queue_projection.py` in
`grandchallenge/MATH-PROGRAMME`; protected controller:
`.github/workflows/erdos-catalogue-queue-projection.yml`.

This is a state-reconciliation service, **not** a mathematical review,
editorial acceptance, proof of global queue reduction, or work-completion
certificate. A merged source repair does not establish successful operation.

## Operating path

Two **separate protected GitHub Actions paths** now operate:

- **One-issue fast path:** `.github/workflows/erdos-catalogue-return-fastpath.yml`
  handles new or edited `RESULT/1` comments. It reads only the target
  issue and its current comment census, validates the exact pinned source and
  GitHub actor, mints a bounded Clerk token, reconciles that one issue, and
  archives authenticated Project/Issue Field/label readback. Concurrency is
  scoped per issue rather than the complete catalogue.
- **Full catalogue sweep:** `.github/workflows/erdos-catalogue-queue-projection.yml`
  runs on protected push, schedule or manual dispatch, not individual worker
  comments. It retains the complete source/exception batch aggregates.

Invalid or competing returns fail closed. Edited/deleted return history remains
in the event-custody ledger and scheduled full snapshot; no result is promoted
to mathematical acceptance merely because its status becomes RETURNED.

For an **open** source task, each successful projection confirms all three
authoritative surfaces: Project #2 Status `RETURNED`, exact organization
Issue Field `GCL State=RETURNED`, and absence of `gcl-state:available`.
A **closed**, genuinely Done task is source- and Project-readback-verified
without changing terminal custody. Source comment content is re-read and
checked against the snapshot's SHA-256 before either outcome.

The one-issue projector is idempotent. Its fast-path artifact is named
`gcl-return-fastpath-<issue>-<run>-<attempt>`. The terminal
`PROJECTION.json` must show `VERIFIED`, the exact
comment binding and complete three-surface readback. A BLOCKED or missing
artifact does not count as success. The separate fast path is
[viewable here](https://github.com/grandchallenge/MATH-PROGRAMME/actions/workflows/erdos-catalogue-return-fastpath.yml).

The scheduled replay remains idempotent. A protected controller captures one source snapshot
and immutable batch manifest. It runs at most **64 source issues per job** and
**two jobs concurrently**, each with a 25-minute limit and its own short-lived
Council Clerk credential. Monolithic bulk runs are forbidden.

The read-only whole-snapshot verifier rejects missing, duplicate, incomplete
or contradictory batch receipts, changed snapshot identity and changed
protected source head. Only the verifier can emit a manifest-wide VERIFIED
result; an isolated green batch cannot prove that the queue is reconciled.

## Inspect a run, not an assurance

1. Open the [queue projection workflow](https://github.com/grandchallenge/MATH-PROGRAMME/actions/workflows/erdos-catalogue-queue-projection.yml).
2. Check the **terminal conclusion** of the entire workflow, including
   source_return_batches and source_return_verify.
3. Download gcl-source-return-input-<run-id>-<attempt>, containing REPORT.json
   and BATCH_MANIFEST.json from the same captured intake.
4. For every batch, examine gcl-source-return-batch-<index>-<run-id>-<attempt>
   and projection.json. Each verified shard must have VERIFIED_BATCH,
   verified=true, complete=true, processed_count=expected_issue_count.
5. Check gcl-source-return-aggregate-<run-id>-<attempt> / receipt.json.
   Only manifest-wide VERIFIED, verified=true, complete=true, applied=true,
   and verified_issue_count=eligible_issue_count demonstrate full projection
   of single-valid-return tasks. They do not certify mathematics, editorial
   acceptance, or total GCL queue closure.

`RUNNING` is an **interrupted or still-in-progress checkpoint**, never a
completion claim. `BLOCKED` records failure and, where known, the precise
in-flight issue. `DRY_RUN_ONLY` is an observation, never applied success.
The on-disk receipt is atomically rewritten after each confirmed issue
readback. The existing Actions controller attempts to archive it even if a
step fails. If the runner terminates before archival, the missing artifact
is itself **unverified**, not success.

To manually rerun the authorized persistent controller after an incident:

```sh
gh workflow run erdos-catalogue-queue-projection.yml \
  --repo grandchallenge/MATH-PROGRAMME --ref main
```

Do not run the bulk `--all` mutator under an ordinary agent shell or declare
completion from a PR merge, a job start, a green preflight, a progress counter,
or a missing/partial artifact. To reproduce the local contract tests:

```sh
PYTHONPATH=. python3 tests/test_erdos_return_fastpath.py -q
PYTHONPATH=. python3 tests/test_erdos_catalogue_queue_projection.py -q
PYTHONPATH=. python3 tests/test_erdos_source_return_batches.py -q
PYTHONPATH=. python3 ci/test_gcl_queue_class_cutover.py -q
```

A full production completion claim requires terminal GitHub Actions success,
valid exact-scope receipt, and readback of any specific changed Project and
Issue Fields. Outstanding invalid or multiple returns remain separately
classified work; none are silently declared completed by this projector.
