# GCL work-package tooling

`GCL-WP-TOOLING-001` is the repository-local command contract for reusable GCL work-package operations. It consumes the institutional truth spine admitted through protected merge `50a2d20a21caa20570042a021842580d31d6d2d4`. It does not create a second authority registry and does not require AETHER or another live service.

## Tranche 1 scope

Two commands are executable candidates:

- `validate-manifest` validates a JSON record against its repository-local schema and checks that the selected truth-spine record class permits the named repository and path class.
- `check-identities` verifies the byte length, SHA-256 digest, and Git blob SHA-1 of repository-local files against a closed identity manifest.

Three required command names are registered but intentionally unavailable:

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

A valid result confirms only that the candidate record satisfies the supplied schema and the protected truth-spine repository/path rules. It does not promote or activate the record.

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

Every Tranche 1 report states:

- candidate output only;
- protected records cannot be modified;
- promotion cannot be authorized;
- AETHER is not required.

Exit status `0` means the requested validation passed. A nonzero status means the candidate failed validation or the command is not executable in the current tranche.

## Adoption fixture

The first end-to-end fixture is `governance/governed_campaign_registry.json`, classified as `campaign_manifest` by the protected truth spine. The fixture demonstrates equivalent local and hosted semantic validation without campaign-specific code in the CLI.

## Future tranches

Later reviewed operations may implement work-package generation, exact-subject review packets, promotion verification, reusable Actions, stale-reference detection, orphan detection, and conformance matrices. Each operation requires its own closed schemas, adversarial tests, CI reachability, exact-subject review, and Human Steward disposition before programme-wide adoption.

No generated candidate, validation report, workflow run, issue, or explanatory document can create protected authority.
