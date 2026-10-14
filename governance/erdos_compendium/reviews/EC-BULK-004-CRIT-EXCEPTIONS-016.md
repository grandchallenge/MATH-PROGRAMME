# EC-BULK-004 — Erdős #474 special-status critical review

Receipt: EC-BULK-004-CRIT-EXCEPTIONS-016  
Observed: 2026-10-14  
Accountable GitHub identity: fyremael  
Decision: **CRITICAL_DRAFT_PASS_WITH_PRIMARY_SOURCE_BLOCKER**. This is an editorial mathematical source review by the same authenticated identity, not independent external referee review, forcing-proof certification, protected publication or mathematical adjudication. The deterministic cohort sample selects #474, but a full sample PASS **must await original Erdős/Vaught source readback and independent status adjudication**.

## Exact original question and interpretation

The plane $\mathbb R^2$ has continuum cardinality $\mathfrak c$. The problem is coloring **two-element unordered subsets** of that vertex set, *not* individual points or geometric distances. The property P is:

$$
\exists c:[\mathbb R^2]^2\to 3\ \forall A\subseteq\mathbb R^2,\
(|A|\geq\aleph_1\implies c[[A]^2]=3).
$$

Correct partition notation: P is $\mathfrak c\not\to[\aleph_1]^2_3$. The **positive** square-bracket arrow $\mathfrak c\to[\aleph_1]^2_3$ means that every three-coloring of unordered pairs has an uncountable set *omitting at least one color*, not necessarily a monochromatic set. Arrow negation, ZFC provability, logical independence, and truth inside a named model are different assertions. The special status NOT PROVABLE is not an ordinary unsolved number-theory inequality.

## Historical source limits

- The maintained https://www.erdosproblems.com/474 (page last edited 2026-02-01) reports that Erdős proved the required coloring under CH, and that Shelah's 1988 forcing produced a model with the *opposite* positive partition arrow. The stated residual question for continuum $\aleph_2$ remains open.
- The exact 1995 Erdős primary paper is *On some problems in combinatorial set theory*, Publ. Inst. Math. (Beograd) 57(71), 61–65, specifically p. 64; bibliographic entry https://geodesic.mathdoc.fr/item/PIM_1995_N_S_57_71_a5/ . Its original PDF could not be inspected: institutional archive returned 502/timeout and the anticipated Rényi PDF path returned HTTP 403. Vaught 1999 Problem 7.81 was also not inspected. **Source audit disposition remains PARTIAL**; bibliography is not page-level source readback.
- Direct primary Shelah 1988: https://shelah.logic.at/files/95955/276.pdf, printed p.356 (PDF second page), explicitly states the consistency result $2^{\aleph_0}\to[\aleph_1]^2_3$, with large-cardinal ground assumptions. The result is relative model consistency, not a bare ZFC proof of the positive arrow.

## Material post-catalogue 2026 theorem

Saharon Shelah's arXiv:2601.02923v1 (Jan. 6, 2026), https://arxiv.org/html/2601.02923v1 , Theorem 0.1 asserts a ccc forcing extension of GCH with

$$
2^{\aleph_0}=\aleph_6,\qquad
\forall n\ge3:\quad \aleph_5\to[\aleph_2]^2_{n,2}.
$$

Theorem 0.2 gives more general cardinal assumptions; Definition 0.3 defines this $(n,2)$ notation as an $\aleph_2$-subset using at most **two** colors in every n-coloring of unordered pairs.

**Independent logical implication CHECKED:** Given a three-coloring of $[\aleph_6]^2$, choose an $\aleph_5$-subset and restrict. Theorem 0.1 at $n=3$ yields an $\aleph_2$-subset using no more than two colors. Choose any $\aleph_1$-subset. Thus

$$
\aleph_6\to[\aleph_1]^2_3.
$$

With continuum $\aleph_6$ in the extension, **P fails**. The 2026 preprint says no large-cardinal hypothesis is required for this example, materially superseding the old strength-of-assumption narrative in the maintained #474 entry. **The 14-page forcing proof itself was not independently referee-checked or Lean replayed.** This is an author-stated theorem and a checked logical reduction, not independent GCL certification. Also, continuum $\aleph_6$ does *not* resolve the separate $\aleph_2$ case.

## Independent finite falsification hooks

The finite $K_4$ coloring by three perfect matchings gives every 3-vertex induced triangle exactly the three edge colors. For $K_5$, the same property is impossible, since at any vertex four incident edges would need four different colors, contradicting the use of only three. Separately, a triangle using precisely two colors demonstrates that square-bracket color *omission* does not imply monochromaticity.

The committed tests/test_erdos_compendium_0474_partition_semantics.py reproduced these three finite semantics checks exactly: **3 tests passed** on source head 3805ccbaea0207e0303e49452b4c322f7fdf682e. These tests do not decide any infinite-cardinal or forcing model statement.

## Evidence hashes and outstanding gates

- Original issue: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1744#issuecomment-6167424347, exact authenticated author fyremael, six substantive RESULT/1 sections, disposition PARTIAL. CRLF-to-LF body SHA256 `de1c87366962984bb07398428c0a7ad0e7793d2d3ed167df369725640442c523`.
- Six-section manuscript: governance/erdos_compendium/editorial/0474.md; SHA256(UTF8(article_text.strip())) `4516e6159d42b7eebb79281986fe8b85cfac195079c3ab30cd35e6a5f5c2bc57`; raw UTF-8 bytes SHA256 `3b4723d0f73477b929df611063376f7e470912983474aa250de2d28dfbcc7c3b`. Six mandatory headings occur once each, and dollar-delimited mathematics is balanced.
- At the exact source-head above the three new finite tests PASS. Full Compendium pytest and strict MkDocs **must be separately run on the final register-bearing branch head**; the present review does not claim their success.
- Pending: direct Erdős Er95d printed p.64 and Vaught [Va99] §7.81 reading; independent specialist read of full Shelah 2026 forcing proof and comparison with Shelah 1988; a correctly delimited assertion about continuum $\aleph_2$.

**No protected publication, live browser mathematical rendering, V2 batch admission, new forcing theorem, external reviewer certification, MathCert or monetary award is claimed.**
