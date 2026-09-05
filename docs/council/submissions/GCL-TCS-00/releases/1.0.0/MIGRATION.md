# GCL-TCS-00 migration: 0.1.0 to 1.0.0

The historical `GCL-TCS-00/0.1.0` candidate remains immutable evidence and remains the governing basis only for the previously admitted bounded-candidate pilot until a later G9 transaction changes authority.

The proposed `1.0.0` release uses the same field meanings, gate semantics, claim vocabulary, exception model, and conformance dimensions unless a versioned release file explicitly states otherwise. Consumers that validate machine declarations must update version locks from `0.1.0` to `1.0.0` and use the version-1 schemas and templates.

A declaration, review, gate, or release record bound to `0.1.0` MUST NOT be relabelled as `1.0.0`. Historical gate evidence MAY be cited as supporting evidence only when a new exact-revision gate independently determines that it remains applicable.

No authority transition occurs during migration preparation. The exact `1.0.0` candidate must be frozen, receive the required G0-G7 decisions, receive G8 PASS, and then be atomically admitted by G9 before version-1 authority is effective.
