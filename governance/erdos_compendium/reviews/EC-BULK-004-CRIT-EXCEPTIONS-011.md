# EC-BULK-004 — Erdős #463 critical documentary review

Receipt: EC-BULK-004-CRIT-EXCEPTIONS-011  
Date: 2026-10-13  
Accountable editorial identity: fyremael  
Review scope: source normalization, mathematical falsification hooks, and six-section manuscript. Separate critical checking after drafting, not independent-person review, mathematical certification, or V2 admission.

## Source fidelity

- The scanned Erdős–Graham (1980), printed p. 92, PDF index 87, asks whether for **each fixed c**, sufficiently large n admit a **composite** m>n+c with m-p(m)<n. The composite condition is essential.
- The maintained modern #463 formulation asks for a single diverging f(n) with eventually valid composite witnesses. The source audit proves their equivalence through reach R(n), without exchanging infinitely-many and eventually-for-all quantifiers.
- Pinned Formal Conjectures file, blob a1620ab2df5014ea1bc8b1a62148ca1bbc9e400a, contains unproved placeholders and accurately preserves the composite domain; it has not been GCL-compiled.
- The different 1992 Erdős minimum problem has **not** been inspected. A minimum over unrestricted m>n is trivially zero, because primes have m-p(m)=0. The article preserves that semantic boundary and does not attribute an inferred restriction to the uninspected paper.

## Mathematical adversarial checks

Define R(n) as the maximal m-n for a qualifying composite m, or zero if there is no such m. For a composite, p(m)≤√m. With s=m-n, eligibility implies s²<n+s, giving the exact strict upper bound s<(1+√(1+4n))/2. This proves finite computability of R(n), not its asymptotic limit.

- The original constant-c question is ∀c ∃N ∀n≥N R(n)>c, exactly R(n)→∞. If true, f(n)=floor(R(n)/2) tends to infinity and preserves a strict witness. Conversely any valid diverging f gives R(n)>f(n), hence R(n)→∞.
- For prime q, put n=q²−q+1 and m=q². Then m−p(m)=q²−q<n and m−n=q−1. Thus R(n)≥q−1 on a special infinite subsequence. Unbounded limsup is **not** the conjectured limit to infinity.
- Independent exhaustive fixture tests/test_erdos_compendium_0463_reach.py reproduces R(10)=0, R(20)=1, R(23)=2, R(100)=0, R(200)=9; compares with a deliberately longer enumeration for every n≤300; and tests prime-square witnesses for nine primes.

## Identity, hashes and QA

- Authenticated source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1733#issuecomment-6156938593, author fyremael, normalized body SHA-256 b6cb7a710215c1d211a238882d9ca89b5c75265567fde02d50feb862c11973db, disposition BOUNDED_TASK_DESIGNED.
- Article: governance/erdos_compendium/editorial/0463.md; SHA-256 of stripped UTF-8 source 9206f12fe9b36d86cd1c88deefc712414d0da9503b857062ae9ba7994966dd4f; raw bytes SHA-256 b854a65d8abc29d6c6620682173b0376fbe15f3e8b033326d7312ba7b138c877.
- Six mandatory article headings each occur once, with balanced dollar-delimited mathematics.
- Source head 9932b233b205187a4986a6161b8b1d543121936b: 99 Python tests and 517 subtests passed; strict MkDocs build passed (76 editorial files, 23 pending and 50 reviewed **across the whole repository**, not within EC-BULK-004).

## Decision

CRITICAL_DRAFT_PASS_WITH_SOURCE_BOUNDARY. Valid documentary exposition as an **unaccepted** mathematical draft. The related 1992 minimum needs primary-source fidelity, the uniform-in-n conjecture remains OPEN, and no formal proof has been replayed. This review is not the mandated 20-article deterministic final sample. No protected production PR, deployed browser MathJax check, V2 admission, mathematical certificate, or novelty claim is asserted.
