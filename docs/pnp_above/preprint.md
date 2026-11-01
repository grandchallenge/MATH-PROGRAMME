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

## Public preprint distribution

**Published working release:** [PNP-ABOVE preprint v0.1.0 — PDF, LaTeX and checksums](https://github.com/grandchallenge/MATH-PROGRAMME/releases/tag/pnp-above-preprint-v0.1.0-binary-2026-11-01)

- [Download the seven-page PDF](https://github.com/grandchallenge/MATH-PROGRAMME/releases/download/pnp-above-preprint-v0.1.0-binary-2026-11-01/PNP_ABOVE_Verification_Compression_Preprint_v0_1.pdf)
- [Download exact LaTeX source](https://github.com/grandchallenge/MATH-PROGRAMME/releases/download/pnp-above-preprint-v0.1.0-binary-2026-11-01/PNP_ABOVE_Verification_Compression_Preprint_v0_1.tex)
- [Download SHA-256 checksum record](https://github.com/grandchallenge/MATH-PROGRAMME/releases/download/pnp-above-preprint-v0.1.0-binary-2026-11-01/SHA256SUMS.txt)

The LaTeX source is also [admitted on protected main](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/preprints/PNP_ABOVE_Verification_Compression_Preprint_v0_1.tex). The released PDF is a fresh seven-page compilation of that exact source; its bytes differ from an earlier locally compiled edition, so the authoritative release hash is the one below.

| Released object | Bytes | SHA-256 |
| --- | ---: | --- |
| PDF | 347,551 | `c642a756a686cb9ea4c3e016e8c891b5be0bad8bfd26ef1c2574aee7d977410f` |
| LaTeX source | 23,711 | `ec20a5a881f87df7f86c7b9026db868186f7c1947c7350d315983bf43fa61141` |

All three assets were downloaded from the release and checked against the checksum file; the public PDF and TeX download URLs were also independently retrieved without authentication and matched these hashes. The [protected release manifest](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/research/preprints/PNP_ABOVE_v0_1_MANIFEST.json) captures the asset names and provenance.

The release is explicitly a **working preprint/prerelease**, not a submission to arXiv, a peer-reviewed article, or an independently certified mathematical result. An earlier immutable metadata-only prerelease with no binary assets remains an archival record; this newer tagged release is the binary distribution.

The source-checked MkDocs pages remain the online textual accompaniment: [reader's primer](primer.md), [technical spine](technical.md), and [evidence ledger](evidence.md). The earlier [lay manuscript](../research/pnp_above_lay_manuscript.md) is retained in the editorial archive.

## Suggested citation

Grand Challenge Labs. *P versus NP from Above: Verification Compression and the Classical Transfer Problem*. Working research preprint, version 0.1 (1 November 2026). Unsubmitted manuscript.

No DOI, journal acceptance, or arXiv record is claimed for this manuscript.

## Claim integrity and future editions

A source-normalization correction is not a new proof; a finite test is not an asymptotic theorem; a protected documentation merge is not mathematical certification. New mathematical claims require the distinct substantive verification and governed claim-admission route.

The parent [PNP-001](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162) remains an open programme. [PNP-ABOVE-WP00](https://github.com/grandchallenge/MATHSOLVE/issues/1136) remains responsible for the exact mathematical residual.
