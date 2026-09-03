# GHOS estate membership sentinel — software contract

## Purpose

`classify_estate_membership(campaign, live_snapshot)` compares a caller-supplied live repository population with the stable repository identities frozen in a GHOS estate campaign. It is a detect-only classifier. It does not acquire the live snapshot and it does not mutate GitHub or governed records.

## Inputs

`campaign` must be a JSON-like object containing:

- non-empty `campaign_id`;
- `estate`, an array of objects with `repository` in `owner/name` form and positive integer `repository_id`.

`live_snapshot` must be a JSON-like object containing:

- `schema_version: "1.0.0"`;
- `repositories`, an array of objects with `repository`, positive integer `repository_id`, and boolean `archived`.

Repository ID is the stable identity key. Repository name remains a checked identity attribute so rename/replacement ambiguity fails closed rather than being silently accepted.

## Output contract

The function returns a dictionary with:

- `schema_version` and `detector_id`;
- the source `campaign_id`;
- one `result` status and its prescribed `route`;
- baseline and observed population counts;
- findings for new, missing, archived, or invalid identities;
- `historical_terminal_rewrite_permitted: false`;
- an explicit `authority_boundary` denying mutation/admission/claim authority.

Possible result statuses are:

- `UNCHANGED` — no material estate-membership change is detected;
- `NEW_ESTATE_MEMBER_SUCCESSOR_ADMISSION_REQUIRED` — at least one new stable repository ID is present and no conflicting removal/archive event is present;
- `ESTATE_MEMBER_REMOVED_OR_ARCHIVED` — a frozen member is missing or archived and no new-member conflict is present;
- `UNKNOWN_FAIL_CLOSED` — the snapshot is malformed, identity is ambiguous, duplicates exist, or simultaneous addition and removal/archive require an explicit disposition.

## Determinism and side effects

For equal Python input values under the supported interpreter, the returned value is deterministic. The module performs no network access, file writes, subprocess execution, GitHub mutation, secret access, scheduling, or autonomous wake action.

## Preconditions and completeness boundary

The caller is responsible for supplying a complete live snapshot for the estate being evaluated. An incomplete acquisition layer can cause the classifier to report a missing member or fail to reveal a private new member that was never supplied. The classifier therefore proves only the comparison of its inputs; it does not prove that acquisition was complete.

For the live GCL estate, this matters because private organization repositories cannot be safely inferred from a public-only listing. Cross-repository acquisition credentials are outside this component and require their own security/controller disposition if introduced.

## Failure semantics

Malformed populations, invalid repository IDs, duplicate names/IDs, repository identity replacement, and mixed addition/removal drift fail closed as `UNKNOWN_FAIL_CLOSED`. The caller must investigate before any governed transition.

A new repository result routes to a successor admission transaction. It does not itself admit the repository. A missing/archive result routes to a successor membership disposition. It does not rewrite historical terminal evidence.

## Compatibility

- language/runtime: Python 3.9 or newer; the protected source uses built-in generic type syntax such as `list[...]` and `tuple[...]`;
- external runtime dependencies: none;
- network/runtime credentials: none;
- serialized input schema version: `1.0.0`.

Changing the result vocabulary, identity key, fail-closed conditions, authority boundary, input schema, or route semantics is a material change requiring revalidation.

## Executable example

```python
from ci.ghos_material_state_sentinel import classify_estate_membership

report = classify_estate_membership(
    {
        "campaign_id": "EXAMPLE",
        "estate": [{"repository": "org/a", "repository_id": 1}],
    },
    {
        "schema_version": "1.0.0",
        "repositories": [
            {"repository": "org/a", "repository_id": 1, "archived": False},
            {"repository": "org/b", "repository_id": 2, "archived": False},
        ],
    },
)
assert report["result"] == "NEW_ESTATE_MEMBER_SUCCESSOR_ADMISSION_REQUIRED"
assert report["authority_boundary"]["may_admit_repository"] is False
```

## Tests linked to guarantees

From the repository root, replay the protected test module with:

```text
python3 tests/test_ghos_material_state_sentinel.py
```

`tests/test_ghos_material_state_sentinel.py` checks unchanged membership, new-member routing without auto-admission, archive/removal routing, identity replacement, duplicate identity, mixed drift fail-closed behavior, and parsing of the protected 14-member GHOS campaign. These tests establish implemented behavior for the protected source identity; they do not establish completeness of an external live-snapshot acquisition mechanism.
