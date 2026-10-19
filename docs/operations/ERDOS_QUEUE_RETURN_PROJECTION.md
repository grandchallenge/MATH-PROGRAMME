# GCL Erdős catalogue — source-return queue projection

**Authoritative implementation:** `ci/erdos_catalogue_queue_projection.py` in
`grandchallenge/MATH-PROGRAMME`; protected controller:
`.github/workflows/erdos-catalogue-queue-projection.yml`.

This is a state-reconciliation service, **not** a mathematical review,
editorial acceptance, proof of global queue reduction, or work-completion
certificate. A merged source repair does not establish successful operation.

## Operating path

The existing GitHub Actions controller runs from protected `main` on
scheduled, qualifying source-comment, push, and manual triggers. It obtains a
short-lived Council Clerk installation token, rebuilds a live unadjudicated
catalogue snapshot, verifies Project #2's queue-class contract, and projects
each eligible **single structurally valid** `RESULT/1` return.

For an **open** source task, each successful projection confirms all three
authoritative surfaces: Project #2 Status `RETURNED`, exact organization
Issue Field `GCL State=RETURNED`, and absence of `gcl-state:available`.
A **closed**, genuinely Done task is source- and Project-readback-verified
without changing terminal custody. Source comment content is re-read and
checked against the snapshot's SHA-256 before either outcome.

The replay is idempotent. Its 55-minute job ceiling is deliberately below the
installation token's one-hour lifetime, unlike the former 15-minute ceiling
which cancelled the 769-return batch. If a run cannot complete, another
authorized controller run may safely retry; prior write attempts do not imply
successful completion.

## Inspect a run, not an assurance

1. Open the [queue projection workflow](https://github.com/grandchallenge/MATH-PROGRAMME/actions/workflows/erdos-catalogue-queue-projection.yml).
2. Select the specific run, check its **final** conclusion, and download
   `gcl-source-return-projection-<run-id>-<attempt>` from its Artifacts.
3. Inspect `projection.json`. The exact schema is
   `GCL-ERDOS-SOURCE-RETURN-PROJECTION/1`; the receipt includes the report
   SHA-256, protected source SHA, run URL, eligible count, processed count,
   current in-flight issue, per-issue result and authenticated readback,
   and any blocker.
4. Only `status=VERIFIED`, `verified=true`, `complete=true`,
   `applied=true`, and `processed_count=expected_issue_count`
   certify this *bounded source-return projection*. They do **not**
   certify that later workflow steps, the entire compendium, or the complete
   GCL queue succeeded. Check the full workflow's terminal conclusion and
   subsequent governing issue/Project state separately.

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
PYTHONPATH=. python3 tests/test_erdos_catalogue_queue_projection.py -q
PYTHONPATH=. python3 ci/test_gcl_queue_class_cutover.py -q
```

A full production completion claim requires terminal GitHub Actions success,
valid exact-scope receipt, and readback of any specific changed Project and
Issue Fields. Outstanding invalid or multiple returns remain separately
classified work; none are silently declared completed by this projector.
