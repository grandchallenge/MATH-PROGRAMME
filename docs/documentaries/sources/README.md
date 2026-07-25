# Documentary source records

The GCL–Chaidez documentary editions are maintained as two coordinated artifact classes:

1. **Web documentation records** in `docs/documentaries/`, suitable for MkDocs review, navigation, and claim-boundary maintenance.
2. **Release-class editions** consisting of the rendered PDF and the complete illustrated LaTeX source bundle.

The release-class files are intentionally not duplicated in ordinary Git history. Their exact byte lengths and SHA-256 digests are fixed in [`../ARTIFACT_MANIFEST.json`](../ARTIFACT_MANIFEST.json). A file presented under one of these titles is authentic only when both its byte length and digest agree with the manifest.

The `.tex` records in this directory are archival pointers. They identify the authoritative source artifact, documentary title, page count, and checksum. They are not substitutes for the complete illustrated bundle and are not expected to compile independently.

This separation keeps documentation reviewable while preserving cryptographic identity for the full-resolution editions.
