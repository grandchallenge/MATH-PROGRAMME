# Classification and Discovery Standard

## Binding decision

The programme uses a layered classification and discovery architecture:

1. **MSC2020-SKOS** is the canonical subject classification spine.
2. **The internal knowledge graph** owns programme concepts, relationships, and state.
3. **zbMATH Open** is the preferred mathematics-specific literature discovery source.
4. **OpenAlex** supplies semantic, citation, and cross-disciplinary discovery.
5. **arXiv** supplies rapid current-awareness intake.
6. **OntoMathPRO** is a non-binding ontology design reference.

No external classification, topic assignment, citation metric, or search ranking
determines mathematical truth, certification status, research priority, or an
internal graph relationship.

## Canonical data

Programme-owned graph and mapping data are versioned JSON documents validated by
the schemas in `schemas/`. Stable programme identifiers remain meaningful when an
external provider changes its taxonomy or identifiers.

External mappings are separate assertions with:

- scheme and explicit scheme version;
- external identifier;
- mapping relation and primary, secondary, or facet role;
- provenance, confidence, and review status.

An audited mapping may support navigation and query expansion. It does not imply
that two mathematical concepts are equivalent.

## Graph assertions

Every graph edge has a stable identifier, a typed relation, provenance, and an
assertion status. Only programme review changes an edge from `PROPOSED` to
`AUDITED`, `CHECKED`, or `CERTIFIED`.

`CHECKED` and `CERTIFIED` describe programme evidence recorded elsewhere. The
graph does not independently certify a claim and must point to the relevant claim
or artifact.

## Discovery evidence

MATHFORGE normalizes provider output into the discovery record contract. Raw
responses are cached outside version control. A normalized record may enter Git
only after review and must omit provider reviews and full abstracts unless their
redistribution is explicitly permitted.

Discovery records retain identifiers, bibliographic metadata, classifications,
metrics, query provenance, and a hash of the source response. Provider outages,
ranking changes, and automated topic assignments must not mutate canonical graph
data.

## MSC2020-SKOS pin

The programme pins:

```text
repository: https://github.com/TIBHannover/MSC2020_SKOS.git
commit: 33972ddb6a72c3660a6e499ee5f881b57fa92d41
license: CC-BY-NC-SA-4.0
```

The dataset is not vendored into these MIT-licensed repositories. Use
`tools/cache_msc2020_skos.py` to create and verify an ignored local cache.

## Promotion rule

Provider output follows this path:

```text
raw response
  -> normalized discovery record
  -> human review
  -> audited external mapping or proposed graph assertion
  -> independent programme review
  -> accepted graph assertion
```

Skipping a stage is a policy violation.
