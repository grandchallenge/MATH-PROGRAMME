# Documentary source records

The GCL–Chaidez documentary programme distinguishes admitted public editions from pre-admission candidates.

## Admitted editions

For every volume in [`../ARTIFACT_MANIFEST.json`](../ARTIFACT_MANIFEST.json):

1. the browser page and edition record live in `docs/documentaries/`;
2. the small Git-tracked `.tex` **source record** lives in this directory;
3. the checksum-locked complete illustrated source bundle is the **authoritative source artifact**;
4. the checksum-locked PDF is the **rendered edition**.

Admitted source records are public static files because their corresponding page, edition record, assets, navigation, and manifest volume have entered atomically. They are pointers, not complete compilable projects.

The manifest fixes each admitted volume's title, topic, claim status, problem class, display status, page count, programme crosswalk, source record, edition record, claim authority, documentary tier, byte lengths, SHA-256 digests, and release availability.

## Pre-admission candidates

[`../DOCUMENTARY_CANDIDATES.json`](../DOCUMENTARY_CANDIDATES.json) is the public metadata authority for source-locked documentary candidates that have not yet entered the collection.

Candidate source pointers remain under their governing campaign and are **repository-only until manifest admission**. They are not copied into the Pages site. Public candidate metadata may identify the title, status, proposed tier, claim authority, source lock, review, release identities, and admission obligations without implying that a browser edition or public source record exists.

A candidate becomes an admitted edition only through one atomic change that adds its web page, edition record, native assets, source record in this directory, collection-index row, MkDocs navigation entry, and manifest volume. Candidate metadata alone confer no collection membership.

## Integrity and availability

A source record is not the authoritative complete source. A file presented as a source bundle or rendered edition is authentic only when its byte length and digest agree with its governing manifest or candidate source lock. A checksum establishes identity after acquisition; it does not establish availability. Entries marked `metadata_only` have governed identities but no asserted stable public release locator.

Every admitted browser edition is validated against [`../documentary_web.schema.json`](../documentary_web.schema.json) and the shared manifest-driven semantic, accessibility, asset, release, source, and rendering contracts. MathJax remains a version-pinned enhancement rather than an archival authority; source mathematics remains readable without JavaScript.
