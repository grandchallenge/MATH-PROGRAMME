# Review and admission obligations

The old G8 disposition is DEFERRED for frozen revision `8833253f620c6c05930740bda983d6f43bee6612`. It is retained on PR #836. This correction does not inherit a PASS from it.

G0 through G7 each require an actual review record bound to this package's immutable manifest digest, with reviewer role, scope, method, evidence, findings and decision. All eight are currently **DEFERRED: review not yet performed on this candidate**. Source remeasurement is supporting evidence, not a substitute gate chain.

| Gate | Required review focus |
|---|---|
| G0 | Discoverable identity, owner and candidate registration |
| G1 | P07 governance scope, impact class, dependencies and version lock |
| G2 | Mandatory metadata, schemas, registries and navigation |
| G3 | Terminology, notation and meaning preservation across version edits |
| G4 | Claims, limitations and exact relevance of predecessor evidence |
| G5 | Schema, semantic, exception, revision-binding and authority-shape replay |
| G6 | Mutation tests, missing evidence, false promotion and boundary cases |
| G7 | Exact source hashes, reproducible assembly and complete inventory |

G8 remains DEFERRED. An actual authorized Referee must assess the completed earlier gate chain and state established properties, limitations, exceptions, residual risk and permitted downstream uses. The artifact owner cannot be the sole Referee for IC-2/IC-3. No fictional reviewer identity or independent session is supplied here.

G9 remains DEFERRED. Only after G8 PASS can a separate atomic admission bind the exact candidate, final release identities, manifest, changelog, migration and compatibility statement, all required review/promotion records, and rollback/supersession path. Neither an ordinary PR nor a Construction Gate freeze is that admission.

The manifest inventories payload files and their SHA-256 hashes. The manifest's own Git blob or SHA-256 identity is the reviewable package identity; it is intentionally not embedded in itself. Adding or altering payload files changes that identity. Review records must live outside the immutable payload and name it exactly.
