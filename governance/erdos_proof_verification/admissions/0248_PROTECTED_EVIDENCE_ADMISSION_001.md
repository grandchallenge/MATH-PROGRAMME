# Erdős #248 — final protected evidence-admission packet 001

**Proposed terminal disposition for this bounded work item:** VERIFIED_WITHOUT_CERTIFICATION, for the frozen **distinct-prime omega** Erdős #248 statement only. This packet is a *candidate* until this exact PR is admitted through the native protected merge queue and the resulting protected artifacts and issue/queue status are read back. It does not attest to its own future merge.

## Evidence-chain ledger

| Step | Protected authority | Exact mathematical/evidentiary identity |
| --- | --- | --- |
| Proof source | plby/lean-proofs commit 8822f7ddef30fadbd92e1c6ab4ed897af356af5e | Top-level Erdős248 source SHA-256 292041372e8f0e45a2ac06fb78dafc32d79cdc4638253139ea4f495a3334a267; 40 local modules, 16,369 lines |
| Compiler and axioms | PR #3432, merge a55255f01b18139ddf045d4c82fb566c3e77f36d | GREEN kernel receipt SHA-256 708fb9a104231e8d6a07f425226808a26c4a0227239a50ea139cb2777cd78f28; archive SHA-256 def278ff642df48c17787d4d5c0fdbfd671138b63728b66a9105f3ac7d450e08 |
| Non-author adversarial source review | PR #3435, merge bb91ff9e21679e201013de3ef9bc5fba8986748d | Source-critical review SHA-256 dc58e9dd9b2f069426ecfd3cfbb5c6a20094010bf4a0afa344e6aa7c1c323520; qualified distinct-prime-only PASS |
| Internal Referee decision | PR #3442, merge 3cd3e6951c9c34d970b1e0e8ca7ae7edcb6ba871 | Referee report SHA-256 0218423c75cb5712bdd3f9bc3031f003e398f5a966bfd82075cedcacfc753d6a; decision JSON SHA-256 ce859d609dcf89c7ae030234ea2aa3bae9e9d735fbb73a0e3f3cf7d9ee57f455; noncertifying acceptance |
| Final record | This PR, when protected-merged | Admission receipt governance/erdos_proof_verification/admissions/0248_PROTECTED_EVIDENCE_ADMISSION_001.json, with this narrative and the scoped manifest as the canonical bounded status |

**Actual compiler evidence:** 8,918 jobs successfully built, separately executed exact final theorem-type and axiom checks, and 60 authenticated archived stdout/stderr stage digests independently rehashed. Lean v4.33.0; Mathlib db584cd6d46c92f209a44c0f1c829460d327499d; nine documented compatibility patches applied to third-party dependencies. Observed axioms are exactly propext, Classical.choice and Quot.sound, with no sorryAx. The three preceding RED runs remain intact, non-promoting evidence.

**Adjudicated theorem:** one real positive constant controls the number of *distinct* prime factors of $n+k$ by a linear function of $k$ simultaneously for every positive integer shift $k$, for infinitely many positive integers $n$. The external formal proof discharges the original statement at the correct quantifier order.

## Claim and documentary consistency

The following are explicitly **not** claims of this completion:

- **Not the published stronger theorem:** Tao–Teräväinen arXiv:2512.01739v2 additionally controls the multiplicity-counting Omega function and the divisor-function consequence. The Lean theorem controls only distinct-prime omega. The elementary inequality omega at most Omega does not allow promoting the weaker formal result to the stronger paper claim. Full-paper verification stays under parent #3201.
- **Not the missing author map:** the frozen provider comments promise tex/248.tex as their mathematical proof and Leanization map, but it is absent. The GCL source-critical crosswalk is newly written, cannot be attributed to the provider and does not establish complete line-by-line correspondence with the published article. This remains a parent-programme documentary residual, nonblocking **only** for the exact kernel-checked statement.
- **Not unpatched source equivalence:** nine registered external compatibility patches form part of the exact admitted proof. No identity to upstream unpatched proof bytes is claimed.
- **Not independent external human certification:** the external formal proof and the GCL non-author source review have distinct authoring roles. The GCL adversarial reviewer and internal Referee are separate role-scoped passes under one authenticated operator; there is no falsely multiplied human identity. Only MATHCERT can certify publicly; the status is NOT_SUBMITTED.

**Cross-document check:** source audit #1517, verification issue #3204, programme parent #3201, protected #248 manifest, GREEN proof artifact, source-critical review and internal Referee decision all identify the same original distinct-prime theorem. The issue's completion is limited to this bounded verification. Parent #3201 remains open and owns programme-wide coverage and any stronger theorem or original-author documentation work.

**Amanuensis / continuity disposition:** Source author/provenance, artifact ledger references, role review provenance, issue/parent links, claim scope, external publication comparison and material non-certification limits are explicit in the present record and machine receipt. No blocking conflict remains for the **narrow #248 formal-proof verification lane**. The absent author map and unformalized multiplicity theorem remain visible unresolved outside this narrow closure. They must not be silently reclassified as solved in the parent programme.

## Two-step admission and tracker follow-through

This document is filed in the ordinary candidate branch and makes no claim of an already completed final protected merge. The machine receipt binds the previously admitted exact Referee merge and specifies the additional final protected readback requirement.

After the native merge queue admits the final packet, independently confirm the protected main commit, exact manifest/admission-receipt hashes, work_status VERIFIED_WITHOUT_CERTIFICATION, PROTECTED_EVIDENCE_ADMISSION PASS, and certification_status NOT_SUBMITTED. Only then reconcile issue #3204 to CLOSED/completed and its GCL Worker Queue Project #2 Mathematics status to Done, with a durable comment referencing all three protected predecessor merges and the final protected merge. The parent programme #3201 must remain open.

**Qualified outcome:** SOURCE_LOCKED_OMEGA248_PROOF_VERIFIED__NONCERTIFIED__PUBLICATION_OMEGA_SCOPE_EXCLUDED__AUTHOR_MAP_ABSENT.
