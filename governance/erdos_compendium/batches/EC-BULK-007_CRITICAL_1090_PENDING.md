# EC-BULK-007 critical sample #1090 — pending proof replay

**Status:** REVIEW_PENDING_PRIMARY_AND_LEAN_REPLAY. This is NOT a completed critical review.

- Source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2361#issuecomment-6162323194
- Source: https://www.erdosproblems.com/1090 and https://www.erdosproblems.com/forum/thread/1090
- Formal snapshot: google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020, ErdosProblems/1090.lean with unresolved sorry and an external plby/lean-proofs v4.29.1 link.

## Exact external Lean proof source lock (metadata review; kernel replay STILL pending)

- External theorem source: [plby/lean-proofs, Erdos1090.lean](https://github.com/plby/lean-proofs/blob/8822f7ddef30fadbd92e1c6ab4ed897af356af5e/src/v4.29.1/ErdosProblems/Erdos1090.lean); commit `8822f7ddef30fadbd92e1c6ab4ed897af356af5e`, Git blob `e7116b25fc1677d3e517c49efa2c306481e33415`. This is source identity, not an authenticated kernel check.
- External toolchain source: `src/v4.29.1/lean-toolchain`, blob `33e0c088939ad08c9f2b1befa3118a423b06ad7d`, declares `leanprover/lean4:v4.29.1`.
- External mathlib dependency: `src/v4.29.1/lakefile.toml`, blob `b489dc7a13b9a0146a3eb99d41bb7a9cb48cf995`, requires mathlib tag `v4.29.1`. The exact `lake-manifest.json`, blob `9c9e0d75c31725cfca7e29bf9d61f2e53b7e0c95`, pins mathlib commit `5e932f97dd25535344f80f9dd8da3aab83df0fe6` and transitive package commits. Do not substitute an updated mathlib build.
- Static proof-body inspection: the 524-line external file contains a theorem named `Erdos1090.exists_set_with_strict_monochromatic_line_property`. Its quantified conclusion includes `∀ y ∈ A, y ∈ affineSpan ℝ (S : Set (Fin 2 → ℝ)) → y ∈ S`, the **strong** no-extra-points-on-the-line interface. No file-level `sorry`, `admit` or `axiom` commands appear in this pinned file; its commented `#print axioms` output is **not** new execution evidence. The frozen formal-conjectures theorem still contains `sorry` and is a separate artifact.
- An actual pinned `lake env lean` / module build and `#print axioms` readback with retained return code, reproducible dependency cache and source-check is **still not complete**. CHAD has Lean v4.29.1 installed, but workspace interrogation and an attempted isolated source checkout encountered intermittent internal tool failures; no compilation receipt, Lean theorem check, transitive axiom audit, or independent proof certification is claimed.
- After source-version binding, replay exactly this external proof with the committed manifest; inspect build output, theorem type, actual kernel-reported axioms, and precise dependency closure. Only then decide if the per-problem independent critic disposition can advance. The current state remains `EXCEPTION / REVIEW_PENDING_PRIMARY_AND_LEAN_REPLAY`.

- Unaccepted draft: governance/erdos_compendium/editorial/1090.md

## Exact theorem boundary

The statement requires a finite planar set A such that, under any 2-colouring, one Euclidean line contains at least k points and ALL points of A on that line are monochromatic. This is stronger than merely finding k collinear points of one colour. A Feb 27 2026 forum report explicitly distinguishes an original weaker formal statement from a purported corrected Lean proof.

## Standard Hales–Jewett geometric reduction

Two-colour Hales–Jewett on the finite alphabet grid {0,...,k-1}^N supplies a monochromatic combinatorial line. Choose a generic linear projection from R^N to R^2 injective on the finite grid and introducing no new collinear triple. Such a map exists because finitely many point collisions and unwanted collinearities each define a proper algebraic zero set of matrix coefficients. A combinatorial line contains exactly k points of the grid; preserving absence of extra collinearity guarantees its projected geometric line contains exactly those k points. This is an established standard reduction, not a novel theorem or Lean certificate.

Independent finite fixture in ci/erdos_compendium_007_phase8_checks.py checks the map L(x,y,z)=(x+7y+49z,x+13y+169z) on 27 grid points: all images distinct, 2925 triples tested, 49 original collinear triples and zero new collinear triples. This does not establish that dimension 3 is enough for Hales–Jewett.

## Required before critical approval

Inspect Erdős 1975 p.106, Hales–Jewett source and Graham–Selfridge historical proof. Pin external Lean proof commit and its transitive dependencies; verify kernel check, full strong quantifier, no sorry/admit and no unsupported axioms. Complete an independent second-pass review. Until then 0/20 deterministic reviews completed, no protected source-fidelity approval.
