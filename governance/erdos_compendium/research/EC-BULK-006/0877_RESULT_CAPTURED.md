RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0877-S01
PROBLEM_ID: 877
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let f_m(n) be the count of INCLUSION-MAXIMAL sum-free A subset [n], and f(n) the count of ALL sum-free subsets. Sum-free means no Schur triple a+b=c with all terms in A; a=b is permitted and is prohibited when 2a is also in A. Maximal means no omitted x can be adjoined while remaining sum-free, NOT maximum cardinality. Cameron and Erdős ask whether f_m(n)=o(2^(n/2)), and f_m(n)=o(f(n)).

## Dated status and primary evidence
Cameron and Erdős, 'Notes on Sum-Free and Related Sets', Combinatorics Probability and Computing 8 (1999), 95-107, DOI 10.1017/S0963548398003435, original construction f_m(n)>=2^floor(n/4). Łuczak and Schoen, 'On the number of maximal sum-free sets', Proc Amer Math Soc 129 (2001), 2205-2207, DOI 10.1090/S0002-9939-01-05892-6, showed f_m(n)<=2^((1/2-epsilon)n) for absolute epsilon>0. Balogh, Liu, Sharifzadeh and Treglown, 'Sharp bound on the number of maximal sum-free subsets of integers', J Eur Math Soc 20 (2018), 1885-1911, DOI 10.4171/JEMS/802, author accepted manuscript https://web.mat.bham.ac.uk/A.Treglown/exactsumfree-ACCEPTEDFINAL.pdf. DIRECT PRIMARY examination on 2026-10-14 of Theorem 1.1 printed p.2 and introduction: for each residue i modulo 4, f_m(n)=(C_i+o(1))*2^(n/4) for a residue-class constant C_i. Authors' 2014 paper arXiv:1409.5661 had established weaker logarithmic-scale 2^((1/4+o(1))*n). Frozen teorth catalogue commit 536408716724a2402bdfa7c1d764bf83d64a8c89 reports PROVED, unformalized, statement metadata yes; maintained https://www.erdosproblems.com/877 same mathematical result. Primary article source is proof authority, not the status label.

## Strongest verified interface
The 2018 sharp formula implies f_m(n)=o(2^(n/2)); f(n)>=2^ceil(n/2) follows by taking subsets of odd integers, hence also f_m(n)=o(f(n)). Primary proof's dependency chain includes Green containers/removal, Deshouillers-Freiman-Sós-Temkin sum-free structure, Green-Morris small sumsets; not independently re-proved by GCL. An EXACT finite verifier governance/erdos_compendium/research/EC-BULK-006/finite_877.py/json counts all and maximal Schur-free sets for 1<=n<=16, including a+a=b prohibition. Sample n=4: f=9,f_m=4; n=8:61,13; n=12:369,37; n=16:1954,118. Direct extension and independent obstruction-based maximality agree for n<=11. These finite checks are not asymptotic proof.

## Proposed bounded successor task
Input finite [n], inclusive-diagonal Schur triple predicate, finite fixture. Target: formally prove A maximal sum-free iff A sum-free and for each x outside A, adding x causes 2x in A, x+a in A for some a in A, or a+b=x for some a,b in A (possibly equal). Acceptance: reviewed complete finite proof or pinned compiled no-sorry Lean theorem with actual axiom output plus exact n<=11 cross-check. Falsify via a finite maximal set violating an obstruction or an incorrect computed f_m count. STOP at finite obstruction lemma; the 2018 asymptotic is an imported published theorem requiring separate dependency audit.

## Prerequisites and blocker
Primary proof source and exact hypotheses verified; full 2018 container/structure proof and dependency closure not independently replayed or Lean certified. No GCL protected source-provider theorem for #877 was admitted. No novel result or independent proof of the sharp constants claimed.

## Reuse and claim boundary
Used Cameron–Erdős history, Łuczak–Schoen 2001 published bound, inspected Balogh–Liu–Sharifzadeh–Treglown 2018 Theorem 1.1, maintained catalogue and independent exact finite reproduction. This is evidence for source adjudication ONLY; no protected mathematical review, certification, protected merge or public-site admission.
