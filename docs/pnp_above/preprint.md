# PNP-ABOVE research preprint

<p class="page-deck">Scholarly accompaniment to the public documentary and source-pinned PNP-ABOVE-WP00 investigation.</p>

## Citation record

**Title:** *P versus NP from Above: Verification Compression and the Classical Transfer Problem*  
**Author:** Grand Challenge Labs, Mathematics Programme  
**Edition:** Version 0.1, 1 November 2026  
**Format:** LaTeX typeset, seven-page working research preprint  
**Status:** Not submitted to arXiv; not peer reviewed; not mathematically certified.

!!! info "Distinguish the two papers"
    The source identifier [arXiv:2001.04383](https://arxiv.org/abs/2001.04383) belongs to the established external theorem *MIP*=RE* by Ji, Natarajan, Vidick, Wright and Yuen. **GCL's PNP-ABOVE manuscript has no arXiv identifier.** Do not quote the source identifier as the GCL preprint's identifier.

## Abstract

We examine a possible “from above” approach to the P versus NP problem motivated by the equality MIP* = RE. Recursive compression of quantum multiprover verification might expose a structural invariant with a classical lower-bound interpretation. The principal obstacle is an invalid identification of verifier computation, entanglement resources, strategy synthesis, and deterministic decision time.

The manuscript formalizes the missing classical-transfer obligation; summarizes the established gap-preserving compression theorem; gives the magic-square finite calibration; and documents GCL's nine-level finite input-verifier construction with its theorem-derived cofinite indexed-language observation. These results expose a methodological obstruction to a naive transfer, not a new lower bound for unrestricted classical computation.

## Paper structure

| Section | Content |
| --- | --- |
| 1 | P versus NP, SAT, and the rationale for approaching from a richer model |
| 2 | Distinct computational and entanglement resource measures |
| 3 | The source's three-stage compression theorem and symbolic constants |
| 4 | Magic-square classical value and entangled advantage |
| 5 | Nine-level identity sampler, finite emulator and conditional corollary |
| 6 | The precise uniform classical transfer implication |
| 7–8 | Complexity barriers, falsification policy, reproducibility and next obligations |
| Appendices | Claim matrix, interdisciplinary glossary and bibliography |

## Distribution record

Version 0.1 has a protected [LaTeX source file](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/preprints/PNP_ABOVE_Verification_Compression_Preprint_v0_1.tex). The source's verified SHA-256 is `ec20a5a881f87df7f86c7b9026db868186f7c1947c7350d315983bf43fa61141`.

A seven-page PDF has been built on the GCL publication host directly from those source bytes, with SHA-256 `c642a756a686cb9ea4c3e016e8c891b5be0bad8bfd26ef1c2574aee7d977410f`. A **draft distribution release** was created under tag `pnp-above-preprint-v0.1.0-binary-2026-11-01` containing the PDF, TeX source and `SHA256SUMS.txt`; all three assets were downloaded back from GitHub and the checksums passed. **Public release publication is not yet confirmed**, so this page does not assert a working public release asset URL.

An earlier local seven-page PDF was supplied in the conversation (SHA-256 `0b6805dc7109abdadc64eac7a455ebdf086e95f7d6cd9f4d2e2a0c4bd8850d61`). It differs in binary identity from the reproducibly rebuilt release candidate. The [machine-readable preprint manifest](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/preprints/PNP_ABOVE_v0_1_MANIFEST.json) distinguishes them and records the remaining publication readback obligation. Neither PDF is an arXiv deposit.

The source-checked MkDocs pages are already usable as a public textual companion:
[reader's primer](primer.md), [technical spine](technical.md), and [evidence ledger](evidence.md). The earlier [lay manuscript](../research/pnp_above_lay_manuscript.md) is retained in the editorial archive.

## Suggested citation

Grand Challenge Labs. *P versus NP from Above: Verification Compression and the Classical Transfer Problem*. Working research preprint, version 0.1 (1 November 2026). Unsubmitted manuscript.

No DOI, journal acceptance, or arXiv record is claimed for this manuscript.

## Claim integrity and future editions

A source-normalization correction is not a new proof; a finite test is not an asymptotic theorem; a protected documentation merge is not mathematical certification. New mathematical claims require the distinct substantive verification and governed claim-admission route.

The parent [PNP-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162) remains an open programme. [PNP-ABOVE-WP00](https://github.com/grandchallenge/MATHSOLVE/issues/1136) remains responsible for the exact mathematical residual.
