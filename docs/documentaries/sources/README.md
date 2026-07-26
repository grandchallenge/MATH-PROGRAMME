# Documentary source records

The GCL–Chaidez documentary editions are maintained as coordinated artifact classes:

1. **Web records and web editions** in `docs/documentaries/`, suitable for MkDocs review, navigation, accessibility, and claim-boundary maintenance.
2. **Source records** in this directory. These small Git-tracked `.tex` pointers identify a complete source artifact by documentary title, page count, and checksum. They are not expected to compile.
3. **Authoritative source artifacts** consisting of the checksum-locked complete illustrated source bundles.
4. **Rendered editions** consisting of the checksum-locked PDFs.

The release-class files are intentionally not duplicated in ordinary Git history. Their exact byte lengths, SHA-256 digests, programme crosswalks, and release availability are fixed in [`../ARTIFACT_MANIFEST.json`](../ARTIFACT_MANIFEST.json).

A source record is not the authoritative complete source. A file presented as a source bundle or rendered edition is authentic only when its byte length and digest agree with the manifest. A checksum does not establish availability: entries marked `metadata_only` have governed identities but no asserted stable public release locator.

The Poincaré web edition is governed separately by [`../documentary_web.schema.json`](../documentary_web.schema.json) and [`../poincare.edition.json`](../poincare.edition.json). Its mathematics-rendering script is an enhancement rather than an archival authority; the source TeX remains readable without JavaScript.
