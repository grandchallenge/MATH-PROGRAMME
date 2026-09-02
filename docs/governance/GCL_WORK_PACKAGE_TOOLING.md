# GCL work-package tooling

## Current status

`GCL-WP-TOOLING-WP00` Tranche 1 is `TRANCHE_1_PROTECTED_COMPLETE`.

It completed through PR #205 from reviewed candidate `ee1907499c248594ccc19383ee05076698d4d896` and protected merge `9150afcac705a4535b48fbf04fc089c65ea3bc6b`. The tooling consumes the institutional truth spine admitted through protected merge `50a2d20a21caa20570042a021842580d31d6d2d4`. It does not create a second authority registry and does not require AETHER or another live service.

The historical admission sequence included exact candidate validation, delegated review, Human Steward disposition, and protected merge. Those facts remain provenance; routine maintenance now follows `MP-STREAMLINED-EXECUTION-001` and does not reacquire those gates merely because implementation bytes receive an ordinary bounded update.

## Tranche 1 scope

Two commands are protected and executable for validating candidate artifacts:

- `validate-manifest` validates a JSON record against its repository-local schema and checks that the selected truth-spine record class permits the named repository and path class.
- `check-identities` verifies the byte length, SHA-256 digest, and Git blob SHA-1 of repository-local files against a closed identity manifest.

Three command names are registered but intentionally unavailable:

- `init-work-package`;
- `build-review-packet`;
- `verify-promotion`.

Calling a planned command returns a nonzero verdict. A placeholder cannot be mistaken for implemented institutional tooling.

## Validate a manifest

From the repository root:

```bash
python ci/gcl.py validate-manifest \
  --manifest governance/governed_campaign_registry.json \
  --schema schemas/governed_campaign_registry.schema.json \
  --record-class campaign_manifest \
  --repository grandchallenge/MATH-PROGRAMME \
  --relative-path governance/governed_campaign_registry.json
```

A valid result confirms only that the candidate record satisfies the supplied schema and the protected truth-spine repository/path rules. It does not promote or activate the candidate record.

## Check local identities

```bash
python ci/gcl.py check-identities \
  --identity-manifest fixtures/gcl_tooling/governed_campaign_registry.identity.json
```

The identity manifest is repository-local and closed-schema validated. Missing files, duplicate paths, unsafe paths, byte drift, SHA-256 drift, and Git blob drift fail closed.

## Output contract

Commands emit JSON containing:

- the command name;
- a Boolean validity verdict;
- explicit errors;
- an authority boundary.

Reports describe their **validated subject** as candidate output where appropriate. That wording refers to the artifact being inspected, not to the protected status of the tooling itself.

Every Tranche 1 report preserves these boundaries:

- validation does not modify protected records;
- validation cannot authorize promotion;
- AETHER is not required.

Exit status `0` means the requested validation passed. A nonzero status means the candidate subject failed validation or the command is not executable in the current tranche.

## Adoption fixture

The first end-to-end fixture is `governance/governed_campaign_registry.json`, classified as `campaign_manifest` by the protected truth spine. The fixture demonstrates equivalent local and hosted semantic validation without campaign-specific code in the CLI.

## Future tranches

Later bounded operations may implement work-package generation, exact-subject review packets, promotion verification, reusable Actions, stale-reference detection, orphan detection, and conformance matrices.

A future tranche receives the checks and review warranted by its material boundary. Ordinary implementation/documentation maintenance remains delegated. A new operation that changes promotion authority, certification semantics, security-sensitive execution, or another reserved boundary receives the specialist or Human Steward disposition required by that specific change. No future tranche inherits a generic fresh-review requirement solely from commit freshness.

No generated candidate, validation report, workflow run, issue, or explanatory document can create protected authority.
