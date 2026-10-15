RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0899-S01
PROBLEM_ID: 899
DISPOSITION: SOURCE_LOCK_READY
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let A be an INFINITE set of positive integers with asymptotic density zero A(N)=|A∩[1,N]|=o(N). Let D(A)=(A−A)∩positive integers, using ordered difference a-b>0 of ANY two a,b∈A, including a,b>N when their positive difference <=N. Is limsup_{N->infinity}|D(A)∩[1,N]| / A(N)=+infinity? YES in literature Ruzsa [Ru78]. Do not conflate limsup with full limit to infinity, positive (A-A) with all signed differences or with finite A∩[1,N] minus itself, and do not replace zero density by positive density. Related sumset problem #245 is distinct.

## Dated status and primary evidence
Original Erdős source key [Er82e] via maintained https://www.erdosproblems.com/899, as of 2026-10-15 marks PROVED, credits Imre Z. Ruzsa [Ru78] for affirmative infinite theorem. Its external field reads 'Formalised statement? Yes', NOT independent Lean proof certificate. A period survey 'On difference sets of sets of integers', Séminaire Delange–Pisot–Poitou 1977–1978, https://archive.numdam.org/item/SDPP_1977-1978__19_1_A4_0/ discusses and attributes a related sparse-set difference theorem to Ruzsa. Bibliography of same 1977–1978 survey includes Ruzsa 'On difference sequences' Acta Arithmetica25 (1974)151–157 and another 'On difference sets' listed TO APPEAR. Exact bibliographic expansion and specific theorem of maintained [Ru78] have NOT been reliably established by primary-paper readback in this execution. Do NOT invent identification with unrelated Erdős–Sárközy 1978 difference-set papers, the 1974 paper, or a later positive-density theorem; source fidelity OPEN pending original full text. The maintained modern statement and proved attribution are established; exact primary Ruzsa proof not independently replayed.

## Strongest verified interface
An elementary complete special-case theorem: A={2^j:j>=0}; at N=2^m−1, A(N)=m. Any positive difference <=N of powers 2^j−2^i with j>i must have 0<=i<j<=m; all such pairs yield differences <=N, so exactly m(m+1)/2 candidates. The 2-adic valuation of 2^j−2^i=2^i(2^{j−i}−1) equals i and odd part determines j, so ALL pairs different. Hence |D(A)∩[1,N]|/A(N)=(m+1)/2->infinity; A(N)=O(log N)=o(N). IMPORTANT j=m contributes m differences even though 2^m>N: whole infinite A used. A positive-density CONTROL A=3positive integers has A(N)=floor(N/3), D(A)∩[1,N] exactly positive multiples of 3<=N, ratio1. CHAD finite_898_899.py/json exhaustively checks all m1..16, unique exponent-pair encodings and 3Z control N3..200; this does NOT establish the general arbitrary zero-density A theorem.

## Proposed bounded successor task
Prove exact powers-of-two positive-difference count for all m using 2-adic valuation uniqueness and correct role of terms larger than the cutoff, and demonstrate ratio diverges along N=2^m−1. Acceptance complete paper proof or pinned compiled no-sorry Lean with literal axiom readback, exact 16-case replay plus positive-density counter-control, including infinite-set semantics. A duplicate difference from distinct exponent pairs, missed j=m pair, or density calculation error falsifies. Next source task independently identify actual Ruzsa [Ru78] publication and source-proof of THE GENERAL limsup theorem, with exact zero-density and difference-set definitions; stop before GCL mathematical/Lean adjudication without full proof.

## Prerequisites and blocker
Full original Er82e text and precise bibliographic [Ru78] primary theorem unverified, zero-density general proof imported from maintained catalogue not independently reconstructed. Formalized statement metadata does not certify proof; no GCL Lean build or reviewer adjudication. Finite power-of-two witness cannot prove universal theorem.

## Reuse and claim boundary
Reused maintained Erdős catalogue and period survey with explicit unverified Ru78 bibliographic caveat, independently proved the powers-of-two example, exact CHAD finite tests and dense counter-control. No newly solved universal theorem, false source citation, protected main merge, live deployed MathJax check or V2 admission.
