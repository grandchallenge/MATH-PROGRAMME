# OAI26 Family 082 — three pinned primary-source theorem statement reviews

**Scope:** Documentary source fidelity only; not proof validation, formal correspondence, or MATHCERT certification.

Pinned source: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`. All three files were retrieved independently and the computed Git blob hashes matched their pinned source identities.

- `preprints/Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026/annular-variation.pdf`: 523,253 bytes, 37 pages, Git blob `b84bc5405b3714f613563e0bb1b5e7f8d1618a77`, SHA-256 `f5857c58037fa5289f2f9fe1fe4421af11df8d9fa9b2914ba041469f1195ea31`.
- `preprints/An-L3-bound-for-the-dyadic-triangular-Hilbert-form-October-5-2026/dyadic-triangular-hilbert.pdf`: 361,519 bytes, 11 pages, Git blob `61895200ebee8b0899ab731973841a6a6c1091f5`, SHA-256 `8e92ed5c9a2964956f01ed38b0dc88a849d6baaaf9cc593618e4f1103f2240a6`.
- `preprints/The-maximal-triangular-Hilbert-transform-at-the-symmetric-point-September-24-2026/paper.pdf`: 487,898 bytes, 27 pages, Git blob `c00c217df7e19ddcff8c1fb9e33853312ee953ff`, SHA-256 `9dbcf9cb984bcf7b0809cc4221d119794ebca0e40027833ce9fe95b1e72c4247`.

## Theorem readback, with distinctions preserved

Annular paper, page 2, Theorem 1.1: for every real r > 2, the **complex-input** triangular Hilbert annular r-variation operator maps L^3(R^2) x L^3(R^2) into L^(3/2)(R^2) boundedly. The underlying truncation is the integral for epsilon < |t| < R of F(x+t,y)G(x,y+t) dt/t. Partitions may depend on each output point, include **all positive radii**, and have **unrestricted numbers of endpoints in each dyadic scale**. Restriction to rational partition endpoints is for measurability, and endpoint continuity recovers the full supremum. One-increment variation gives the **two-hard-endpoint maximal bound**. The paper also claims a **joint** principal value as epsilon tends to zero and R tends to infinity, both almost everywhere and in L^(3/2), with a tail-uniform norm statement.

Dyadic paper, page 1, Theorem 1.1: for **real** L^3 inputs on the nonnegative quadrant, an exact **dyadic model with XOR-admissible interval triples** satisfies the sum of absolute local contributions over any finite set of scales <= **40** times the product of three input L^3 norms. This permits independently selected coefficients of magnitude <=1 at the local triple level, beyond a single coefficient per scale. It does not by itself prove the continuous complex-input theorem; the mathematical settings differ.

Maximal paper, page 2, Theorem 1.1: for arbitrary **complex** L^3 inputs the pointwise supremum over **both** hard finite truncation endpoints is bounded in L^(3/2) by a constant times the input norms. The truncation choices can depend on the output point. The paper also states joint almost-everywhere and L^(3/2) convergence, and a symmetric scalar trilinear bound on three L^3 inputs by pairing. These are not claims at the variation endpoint r=2.

**Verdict: ACCEPTED_EXPOSITION_WITH_LIMITS.** The article reflects the three source statements and correctly separates a discrete real dyadic model from two continuous complex-input assertions. Not independently verified: matrix trace/energy inequalities, Gaussian heat dissipation, endpoint errors, count-to-variation argument, dyadic telescoping proof, a.e. convergence proof, exact formal mapping, or mathematical correctness.

**Claim boundary:** Source-grounded editorial correspondence only; NO_CERTIFICATION. The exact article SHA-256, Markdown/compendium tests, rendered HTML, and protected merge/readback remain required.
