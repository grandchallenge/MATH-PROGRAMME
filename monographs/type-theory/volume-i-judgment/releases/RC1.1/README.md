# Volume I — JUDGMENT RC1.1 durable release record

This directory binds the exact reconciled **Volume I — JUDGMENT: The Grammar of Computation** RC1.1 rebuild inputs to protected MATH-PROGRAMME state.

The rebuild core is transported as 12 bounded Base64 text parts because repository connector writes are text-oriented. Concatenate the parts in lexical order and Base64-decode them to obtain:

`GCL_Type_Theory_Volume_I_JUDGMENT_RC1_1_Rebuild_Core.zip`

Expected decoded identity:

- bytes: `134967`
- SHA-256: `013fd6b5f78a8bb45711bb9e167321f7ca58324b7a0ae3f0c7e594ba63a96e3b`

The archive contains the exact rebuild inputs: `main.tex`, `solutions_companion.tex`, `plates_folio.tex`, all 42 plate sources, and an internal source manifest. Generated PDFs are not duplicated in the archive; their identities remain pinned by `docs/monographs/type-theory-series/REFERENCE_BASELINE.json`. The manuscript, solutions, and folio source hashes in this transport match that baseline exactly.

`SOURCE_TRANSPORT_MANIFEST.json` records both SHA-256 and expected Git blob SHA-1 for every transport part so protected readback can verify the admitted bytes without trusting conversational transport.

The publication and exercise audits remain separately identified by the reference baseline and may be reviewed from the historical publication package. This release record is about exact rebuildability and institutional persistence.

Durable admission establishes persistence and provenance only. It does not establish independent mathematical review, mathematical certification, or publication authority.
