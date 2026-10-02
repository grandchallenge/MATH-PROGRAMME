# GCL-AGENT-CONTINUITY-PHASE-D0-001 — Shared adoption schema design and conformance audit

**State:** `CANDIDATE_CONFORMANCE_CONFIRMED__AWAITING_ROLE_SCOPED_REVIEW`  
**Council docket:** #1013  
**Canonical policy:** `GCL-AGENT-CONTINUITY-001@1.0.0`  
**INTELLECT authority head:** `7662e9b5eeecb065e75173176d535d57a5a42dee`  
**Migration authority:** none  
**Normative schema admission authority:** none in D0

## 1. Objective

Phase D0 tests whether the four protected continuity-policy adoptions can converge on one machine-readable envelope without changing repository authority semantics or replacing repository-local validators.

D0 is a design and conformance audit only. It does not mutate any adoption record and does not admit a normative schema to INTELLECT.

## 2. Exact protected reference corpus

| Repository | Protected head | Adoption blob | Local validator | Validator blob |
| --- | --- | --- | --- | --- |
| MATHSOLVE | `aca548821935600c36a03b70aca76a4a7f31e03b` | `4e540a4421bebd1cf6dbff09b5ec2c03f3d55371` | `scripts/validate_agent_continuity_adoption.py` | `1dde73ef018432e8f3ed29c8c686427c105f372b` |
| MATH-PROGRAMME | `2333f4804fe28e6e79847fdc1078a5c5ea276d75` | `5f1f301ecfba68168a801b0832adb9d7bc520c59` | `ci/validate_agent_continuity_adoption.py` | `d90c8c73caf959c294158b7ca280e44328261d4f` |
| MATHFORGE | `5f683563d7580eecb3bc5b2582d9a4577cbb4add` | `7ef3ed044da976e93624ec3bc1fa0e13cc100dca` | `ci/validate_agent_continuity_adoption.py` | `8971b142f7c77fecf9c8e7c40065501236a260cd` |
| MATHCERT | `ee58999acf43f8eed7952a06a2a9e15923d79179` | `7a502c59f864c659c3fa10e20c330adb521ab4b3` | `ci/validate_agent_continuity_adoption.py` | `097486f70ae5267cf1837c6af0b77c1f403364b5` |

The corpus is exact-head bound. Later changes to any source adoption record or validator do not silently alter this audit.

## 3. Observed common envelope

All four protected records already agree on these semantics:

- policy identifier `GCL-AGENT-CONTINUITY-001`;
- policy version `1.0.0`;
- canonical authority repository `grandchallenge/INTELLECT`;
- canonical authority path `governance/agent_execution/GCL-AGENT-CONTINUITY-001.md`;
- one adopting repository identity;
- `required=true`;
- root `AGENTS.md` as the binding instruction surface;
- continuity as operational state only, not authority.

Three records already carry an explicit repository specialization and `authority_preservation` object. MATHSOLVE is the earlier shape: its operational controls are under `controls`, and `certification_authority_changed=false` is top-level.

This is a representational difference, not an identified authority-semantic conflict.

## 4. Candidate common contract

D0 proposes the candidate schema in:

`docs/governance/GCL_AGENT_CONTINUITY_PHASE_D0_001.schema.candidate.json`

The universal envelope contains only:

- schema identity and schema version;
- adoption identity;
- canonical policy identity and version;
- canonical authority repository and path;
- adopting repository;
- binding surface;
- required-adoption flag;
- nullable repository specialization identity;
- explicit repository-local validator identity;
- `authority_preservation`;
- opaque `specialization_data` owned by the repository-local validator.

The common schema requires `authority_preservation.authority_changed=false` and an explicit `local_validator` path. This makes the split of responsibility machine-visible: common-schema conformance is necessary but never sufficient for repository admission. The common schema deliberately does not attempt to interpret every repository-specific authority assertion.

## 5. Repository mappings

### 5.1 MATHSOLVE

Unchanged common fields remain unchanged.

- `controls` moves under `specialization_data.controls`.
- top-level `certification_authority_changed=false` moves under `authority_preservation.certification_authority_changed`.
- `specialization` remains `null`; D0 does not invent a new semantic specialization merely for naming symmetry.
- the existing Solve validator remains responsible for all seven required operational controls.

No operational control is removed or weakened.

### 5.2 MATH-PROGRAMME

- current specialization identity is retained verbatim;
- `implementation` and `applicability` move under `specialization_data`;
- `authority_preservation` remains semantically unchanged;
- the bounded-operation checkpoint registry remains the single authoritative Programme continuity source of truth;
- the local validator retains the prohibition on a duplicate checkpoint registry and all applicability rules.

The common schema must not become a second checkpoint system.

### 5.3 MATHFORGE

- current specialization identity is retained verbatim;
- `applicability` and `checkpoint_requirements` move under `specialization_data`;
- current `authority_preservation` values remain unchanged;
- the local validator remains authoritative for provenance preservation, generated-witness status, non-promotion, and independence non-inheritance.

Common-schema validity cannot turn discovery evidence into proof or verification.

### 5.4 MATHCERT

- current specialization identity is retained verbatim;
- `interruption_rebind`, `provenance`, `succession`, and `fail_closed` move under `specialization_data`;
- current `authority_preservation` values remain unchanged;
- the Cert validator continues to enforce anti-authority-inheritance, anti-independence-inheritance, exact subject/evidence rebinding, and certification fail-closed behavior.

Common-schema validity is never a certification disposition.

## 6. Losslessness result

The machine-readable mapping is recorded in:

`docs/governance/GCL_AGENT_CONTINUITY_PHASE_D0_001.conformance.json`

For the exact protected corpus above, every existing adoption field has one of three treatments:

1. preserved verbatim in the common envelope;
2. preserved verbatim inside `authority_preservation`;
3. preserved verbatim inside `specialization_data`.

No protected source field needs to be discarded, weakened, reinterpreted, or converted into a cross-repository authority rule.

**Candidate D0 result:** `LOSSLESS_REPRESENTATION_CONFIRMED_FOR_BOUND_CORPUS`.

This is an engineering/conformance result. It is not yet a Council disposition authorizing migration.

## 7. Shared-schema authority location

If D1 is later authorized, the normative JSON Schema should be admitted in `grandchallenge/INTELLECT`, alongside the authority policy it describes, proposed path:

`schemas/agent_continuity_adoption.schema.json`

`gcl-standards` may publish or mirror an admitted schema under its normal subordinate publication machinery, but it should not become the canonical authority source for this policy.

## 8. Runtime architecture

No central continuity runtime, controller, write service, or cross-pillar mutation path is proposed.

The intended architecture is:

```text
INTELLECT policy + normative common schema
              |
              v
repository-local adoption record
              |
      +-------+--------+
      |                |
common schema      local validator
validation         specialization semantics
```

Each repository validates locally in its own protected CI surface. D1 must not introduce a mutable network fetch of the schema at CI/runtime. A repository may carry a non-authoritative local schema snapshot only when that snapshot is bound to the exact admitted INTELLECT schema commit/blob identity and its validator fails on drift. A shared schema is a representation contract, not a remote runtime dependency.

## 9. Required adversarial properties

A D1 implementation must demonstrate at least:

1. policy-ID drift fails;
2. policy-version drift fails;
3. authority-repository/path drift fails;
4. `required=false` fails;
5. `authority_preservation.authority_changed=true` fails;
6. missing or malformed `specialization_data` fails common validation;
7. Programme's duplicate-checkpoint prohibition remains locally enforced;
8. Forge's provenance/non-promotion invariants remain locally enforced;
9. Cert's anti-authority-inheritance and anti-independence-inheritance invariants remain locally enforced;
10. missing local-validator identity fails common validation;
11. a mutable or unpinned remote schema dependency is forbidden;
12. a repository-local schema snapshot must be exact-digest bound to the admitted INTELLECT schema identity;
13. common-schema validity cannot satisfy proof, certification, publication, promotion, protected-bypass, or independent-review requirements.

## 10. Proposed D1 ordering

If separately authorized after D0 review:

1. MATHSOLVE;
2. MATH-PROGRAMME;
3. MATHFORGE;
4. MATHCERT.

The ordering moves from the smallest/oldest record shape toward the repository with the most consequential authority boundary.

Each repository is an independent protected transaction. A later migration must:

- rebind the current live protected head;
- migrate only the adoption representation and its local validator interface;
- keep local specialization semantics intact;
- run affected checks;
- satisfy repository protection;
- read back exact protected state before the next repository begins.

## 11. D1 acceptance gate

D1 should not be authorized unless D0 review finds all of the following:

- the bound four-record corpus is losslessly representable;
- the common schema remains thinner than every repository specialization;
- all local validators remain necessary, explicitly identified, and retained;
- no central runtime/controller is introduced;
- INTELLECT remains the canonical policy/schema authority, with any local schema snapshot exact-digest bound and non-authoritative;
- no mathematical, certification, publication, promotion, protected-bypass, or independent-review authority changes.

## 12. Current boundary

`PHASE_D1_BLOCKED_PENDING_D0_ROLE_SCOPED_REVIEW_AND_DISPOSITION`

The D0 artifact may be protected-admitted as an audit/design record under existing Programme controls. Its admission does not authorize any repository migration or normative INTELLECT schema mutation.
