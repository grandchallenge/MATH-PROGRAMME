# Volume I — JUDGMENT RC1.1 durable release record

This directory binds the exact reconciled **Volume I — JUDGMENT: The Grammar of Computation** RC1.1 rebuild inputs to MATH-PROGRAMME protected state.

The rebuild core is transported as 23 bounded Base64 text parts. Concatenate the parts in lexical order and Base64-decode them to obtain:

`GCL_Type_Theory_Volume_I_JUDGMENT_RC1_1_Rebuild_Core.zip`

Expected decoded identity:

- bytes: `134967`
- SHA-256: `013fd6b5f78a8bb45711bb9e167321f7ca58324b7a0ae3f0c7e594ba63a96e3b`

The archive contains the exact rebuild inputs: `main.tex`, `solutions_companion.tex`, `plates_folio.tex`, all 42 plate sources, and an internal source manifest. Generated PDFs are not duplicated; their identities remain pinned by `docs/monographs/type-theory-series/REFERENCE_BASELINE.json`.

`SOURCE_TRANSPORT_MANIFEST.json` records SHA-256 and expected Git blob SHA-1 for every transport part. Protected readback can therefore verify admitted bytes without trusting conversational transport.

The publication, exercise, cosmetic, and executable-audit identities remain pinned by the reference baseline and historical RC package. This durable admission is specifically the exact rebuild core plus its institutional state record.

Durable admission establishes persistence and provenance only. It does not establish independent mathematical review, mathematical certification, or publication authority.
