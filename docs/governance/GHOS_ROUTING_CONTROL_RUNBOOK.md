# GH-OS routing control runbook

## Purpose

This runbook governs maintenance of MATH-PROGRAMME's mandatory execution
routing control. The control is self-policing, not self-authorizing: it detects
coverage, capability, topology, controller, identity, and enforcement drift,
but a legitimate change still requires an exact reviewed pull request.

This runbook grants no merge, certification, promotion, publication,
mathematical-claim, or protected-bypass authority.

## Control surface

| Surface | Purpose |
| --- | --- |
| `.ghos-routing/workflows.json` | Complete workflow inventory, derived features, topology, controller, and fixed authority boundaries |
| `ci/ghos_execution_routing.py` | Repository-local deterministic validator |
| `schemas/ghos_execution_routing.schema.json` | Closed routing-record schema |
| `tests/test_ghos_execution_routing.py` | Hostile semantic tests |
| `.github/workflows/ghos-routing-enforcement.yml` | Protected-base candidate-independent enforcement |
| `grandchallenge/.github/scripts/ghos_execution_routing_gate.py` | External governed gate whose bytes are SHA-256 pinned by the enforcement workflow |
| Ruleset `21969152` | Dedicated protected-main requirement for `routing-enforcement` |
| Ruleset `17137629` | Separate Programme profile; not the GH-OS routing ruleset |

## Routine workflow maintenance

When adding, deleting, renaming, or changing a workflow:

1. Run `python ci/ghos_execution_routing.py`.
2. Update exactly one corresponding entry in
   `.ghos-routing/workflows.json`, or remove the stale entry when deleting a
   workflow.
3. Use the exact feature list and topology derived from workflow bytes. Do not
   weaken them manually and do not over-declare features: the shared gate
   requires exact equality with its byte-derived result.
4. For any non-`BOUNDED_ATOMIC` workflow, use the exact admitted controller and
   confirm that all derived features are supported. Otherwise decompose the
   operation into independently recoverable bounded workflows.
5. Run:

   ```text
   python ci/ghos_execution_routing.py
   python -m unittest tests.test_ghos_execution_routing
   python ci/validate_policy_reachability.py
   python ci/validate_workflow_coverage_v2.py
   python ci/validate_workflow_semantics.py
   ```

6. Require fresh exact-head policy, security, repository, campaign, and
   `routing-enforcement` results. Existing review and check evidence does not
   carry to changed bytes.

The expected maintenance burden is one routing-entry update per workflow
change. The gate supplies the authoritative diagnostic when the entry drifts.

## External gate and digest rotation

An external gate change is a control-plane upgrade, not routine workflow
maintenance.

1. Change and test the gate in `grandchallenge/.github` through its protected
   review path.
2. Record the reviewed and merged gate commit, exact script blob, SHA-256, test
   evidence, compatibility statement, and affected repositories.
3. Do not replace the active shared script path without a coordinated consumer
   plan. Prefer publishing a versioned successor path while the prior pinned
   path remains available.
4. Prepare a MATH-PROGRAMME control-upgrade PR containing only the justified
   enforcement pin/path change and any necessarily synchronized local
   validator, schema, tests, controller catalog, registry, or documentation.
5. Obtain fresh independent exact-head review. A prior routing approval cannot
   authorize the new control bytes.
6. Follow the protected self-modification procedure below.
7. After integration, run a hostile candidate that disables local validation,
   repins a reusable policy caller, and adds an unregistered unattended writer.
   `routing-enforcement` must fail while unrelated required checks may pass.

A digest mismatch is an expected fail-closed condition. Never bypass it by
removing the digest check, following an unpinned branch, or executing candidate
code.

## Protected self-modification procedure

The active enforcement workflow rejects any candidate change to itself. A
legitimate upgrade therefore requires a bounded Human Steward-authorized
bootstrap; it cannot be completed as an ordinary routing PR.

1. Freeze workflow-control changes and unattended campaign advancement for the
   bootstrap window. Bounded read-only evidence work may continue.
2. Record the current protected-main SHA, dedicated routing ruleset `21969152`
   JSON, required contexts, bypass actors, active enforcement-workflow blob,
   external gate identity, and digest. Also read Programme profile `17137629`
   to prove it is not being modified as an incidental part of the routing
   bootstrap.
3. Obtain explicit authorization for the exact successor enforcement blob and
   for temporarily disabling or removing only the routing requirement supplied
   by ruleset `21969152`. Do not add a bypass actor or weaken any other rule.
4. Remove or disable only that routing requirement. Confirm that the
   control-upgrade PR remains subject to every other protected check,
   exact-head review, thread resolution, and merge restriction.
5. Merge only the pre-authorized exact head. A failing self-modification check
   is expected during this bounded bootstrap and supplies no authority.
6. Immediately restore ruleset `21969152` active with strict required status
   checks, zero bypass actors, and required context `routing-enforcement`,
   preserving all unrelated rulesets and actors. Verify the complete readback.
7. Verify the protected merge commit, parentage, enforcement blob, registry,
   local validator, external gate digest, and post-merge policy results.
8. Execute the hostile proof before unfreezing unattended campaign advancement.
9. Record the before/after routing-ruleset identity, unchanged Programme-profile
   identity, authorization, merge, restored protection, hostile PR, and
   terminal readback in the governing issue.

If the exact successor, authorization, ruleset snapshot, or restoration route
is unavailable, stop. Do not leave the routing requirement removed or disabled
while diagnosing an unrelated failure.

## Admitted-controller changes

The controller catalog is code-governed in both the local and external gates.
Adding or changing a controller requires evidence for its durable wake
mechanism, state store, supported feature classes, repository identity, and
failure/recovery behavior.

Update the external gate, local validator, schema if necessary, registry,
hostile tests, and every affected workflow entry together. Demonstrate agent
replacement, stale evidence rejection, interrupted execution recovery, and
unauthorized-transition failure before admission. Controller capability never
supplies authority.

## Ruleset care

After activation, periodically and after any ruleset administration:

1. Read dedicated routing ruleset `21969152` from GitHub.
2. Confirm it is active on `refs/heads/main`.
3. Confirm `routing-enforcement` is required with strict required-status policy.
4. Confirm its bypass actors remain empty.
5. Read Programme profile `17137629` separately and compare it with the last
   protected snapshot so a routing transaction cannot silently weaken legacy
   Programme protections.
6. Open a governed repair immediately on drift and pause unattended campaign
   advancement when enforcement is not mandatory.

Do not interpret a passing optional routing check as equivalent to a required
protected context.

## Emergency diagnosis

Use this order when `routing-enforcement` fails:

1. Bind the failure to repository, PR, head SHA, workflow run, job, and external
   gate digest.
2. Classify the first exact error: missing registry, coverage mismatch, feature
   drift, topology drift, controller mismatch, repository mismatch,
   self-modification, external digest failure, dependency failure, or platform
   outage.
3. For candidate drift, correct the candidate registry or workflow and require
   fresh exact-head results.
4. For an external digest mismatch, verify the shared protected script and
   change history; use the control-upgrade procedure rather than changing the
   pin ad hoc.
5. For a platform outage, leave the gate required and recover evidence through
   the execution-recovery guide. Do not infer success from absence of a result.
6. For unexpected ruleset drift or missing enforcement, pause unattended
   campaign advancement until protected enforcement is restored and proven.

Never solve an emergency by running untrusted candidate code from
`pull_request_target`, granting write credentials to candidate content,
removing authority boundaries, or carrying a stale approval to new bytes.

## Periodic evidence

At least after every control upgrade, and otherwise during the programme's
existing deep-conformance cadence, retain:

- current protected-main and enforcement-workflow identities;
- current workflow count and a successful full-coverage validation;
- external gate commit/path/digest;
- dedicated routing ruleset identity, required context, strictness, and bypass
  actors;
- unchanged/unrelated Programme-profile readback where routing administration
  occurred;
- focused hostile-test results; and
- one live hostile PR or equivalent protected fixture demonstrating fail-closed
  behavior outside candidate control.

Routine periods with no workflow, controller, gate, or ruleset change require
verification, not ceremonial regeneration of unchanged records.
