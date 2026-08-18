# Classification and Discovery Standard

## Binding decision

The programme uses a layered classification and discovery architecture:

1. **MSC2020** is the normative external mathematics subject spine.
2. **Machine serializations** are separate governed artifacts; none is canonical or
   runtime-authoritative until its exact payload, completeness, digest, semantics,
   license, and fallback are qualified.
3. **The internal knowledge graph** owns programme concepts, relationships, and state.
4. **zbMATH Open** is the preferred mathematics-specific literature discovery source.
5. **OpenAlex and arXiv** supply non-authoritative discovery and current-awareness facets.
6. **OntoMathPRO, OpenMath, Wikidata, ACM CCS, and PhySH** may enter only through
   reviewed design references, domain facets, or concept crosswalks.

No external classification, topic assignment, citation metric, or search ranking
determines mathematical truth, certification status, research priority, or an
internal graph relationship.

This standard is the machinery behind the [Grand Challenge Pedagogy Standard](docs/GRAND_CHALLENGE_PEDAGOGY_STANDARD.md)'s external corpus quarantine rule: provider output may guide discovery, but it remains imported evidence until programme review reconstructs and promotes it.

## Canonical data

Programme-owned graph and mapping data are versioned JSON documents validated by
the schemas in `schemas/`. Stable programme identifiers remain meaningful when an
external provider changes its taxonomy or identifiers.

External mappings are separate assertions with:

- scheme and explicit scheme version;
- external identifier;
- a label snapshot, mapping relation, and explicit subject/facet/crosswalk role;
- source artifact identity, assignment method, provenance, confidence, review, and
  supersession state.

Every `ACTIVE` domain has exactly one non-rejected primary MSC2020 subject mapping
or one typed, owned, expiring waiver. A `CANDIDATE` mapping remains `PROPOSED`
until independent review records the reviewer, date, and review reference and the
mapping set is admitted as `QUALIFIED`. Provider-automated output cannot be
`AUDITED` directly.

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

## MSC2020 authority and serialization boundary

The normative subject reference is the official MSC2020 release published by
Mathematical Reviews and zbMATH. The programme records reviewed codes and label
snapshots rather than vendoring the complete taxonomy.

The programme separately pins this candidate serialization cache source:

```text
repository: https://github.com/TIBHannover/MSC2020_SKOS.git
commit: 33972ddb6a72c3660a6e499ee5f881b57fa92d41
license: CC-BY-NC-SA-4.0
```

The pinned tree contains multiple Turtle payloads, including one named
`incomplete`; no exact payload has been qualified as complete or canonical. It is
therefore `UNQUALIFIED_CANDIDATE`, has no runtime authority, and is not vendored.
Use `tools/cache_msc2020_skos.py` only to create and verify an ignored local cache.

The source registry records the reference-only MSC licensing boundary. Vendoring,
redistribution, derived serialization, or commercial/product reuse of third-party
taxonomy content requires a separately scoped human terms review.

## Reader display

Display one primary MSC code and label first, then secondary subjects and optional
discovery/domain facets. Link the programme concept/dependency graph separately.
Display scheme version, mapping role, review status, and waiver or staleness state
in text; do not rely on color or hierarchy alone.

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
