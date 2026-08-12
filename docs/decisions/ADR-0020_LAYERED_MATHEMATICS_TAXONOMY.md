# ADR-0020 — Layered mathematics taxonomy

## Status

**Council disposition:** `COUNCIL_RECOMMENDS_LAYERED_MSC2020_CORE_WITH_CONTROLLED_FACETS_AND_SERIALIZATION_CORRECTION`.  
**Human Steward disposition:** `HUMAN_STEWARD_RATIFIED__LAYERED_MSC2020_CORE_WITH_CONTROLLED_FACETS__MATH_TAX_C01_THROUGH_C10_BINDING__BOUNDED_IMPLEMENTATION_AUTHORIZED`.  
**Authority evidence:** issue #468, Council comment `5266563332` (SHA-256 `b4c750e0bfa9407fde92eaebc0590757fd60e86651a4f602880ed44870da76b7`) and Human Steward comment `5266922480` (SHA-256 `973a6eaad02a3c7caa2626c375e72b88e0899111a9f3dd021855aa95028f1a83`).  
**Implementation docket:** issue #469.  
**Protected authority:** pending independent qualification, protected merge, and protected-main readback.

## Decision

Adopt MSC2020 as the normative external mathematics subject spine within a layered
architecture. Keep machine serializations, discovery/domain facets, the
programme-owned concept/dependency graph, and proof/claim/certification/lifecycle
records as separate governed layers.

Every active domain shall have exactly one primary MSC2020 mapping or a typed,
owned, expiring waiver. Candidate mappings remain proposed until independent
review and protected admission. Automated provider output never self-promotes.

The official MSC2020 release and every machine serialization are distinct governed
objects. The current TIB SKOS pin is an unqualified cache candidate because no one
payload has yet been admitted with completeness, semantic, digest, license, and
fallback evidence.

## Binding corrections

`MATH-TAX-C01` through `MATH-TAX-C10` govern layered authority, serialization
qualification, licensing, active-domain completeness, registry discovery, mapping
provenance, provider non-authority, portfolio qualification, ordered downstream
synchronization, and evidence/nonclaims respectively.

## Admission sequence

1. prepare programme policy, contracts, seven-domain mapping packet, and tests;
2. obtain independent mapping/artifact review at one exact revision;
3. record Human Steward protected-merge authorization where required;
4. merge through protected controls and verify protected `main`;
5. synchronize MATHFORGE, MATHSOLVE, then MATHCERT by exact-revision PRs.

This ADR does not certify a mapping, a serialization, or mathematics. A green test
run proves contract execution only. The architecture is not active until protected
admission and readback complete.
