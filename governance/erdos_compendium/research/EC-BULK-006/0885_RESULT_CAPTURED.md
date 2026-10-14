RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0885-S01
PROBLEM_ID: 885
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For N>=1 define factor-difference set D(N)={|a-b|:a,b positive integers, ab=N}; 0 belongs exactly when N is square. Original Erdős–Rosenfeld assertion: for EVERY k>=1 exist k DISTINCT positive integers N_1<...<N_k with at least k DISTINCT elements in intersection D(N_i). Distinguish number of integers from number of shared differences: three N with four common differences does NOT settle k=4 or k=5. Equivalent exact integer square/parity certificate: d in D(N) iff s²=d²+4N for some integer s>0 with s≡d mod2 and (s-d)/2>0, yielding factors (s±d)/2.

## Dated status and primary evidence
Paul Erdős & Moshe Rosenfeld, 'The factor-difference set of integers', Acta Arithmetica 79(4) (1997) pp353–359, original journal https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/79/4/109554/the-factor-difference-set-of-integers DOI 10.4064/aa-79-4-353-359, proved k=2. Jorge Jiménez-Urroz, 'A Note on a Conjecture of Erdős and Rosenfeld', J Number Theory 78 (1999) pp140–143 DOI 10.1006/jnth.1999.2407, proved k=3. Andrew Bremner, 'On a problem of Erdős related to common factor differences', Int J Number Theory 15 (2019) pp1059–1068 DOI 10.1142/S1793042119500581, proved k=4, using elliptic curves. Maintained https://www.erdosproblems.com/885 OPEN, no k>=5 solution admitted. April 19 2026 forum https://www.erdosproblems.com/forum/thread/885 contains computational partial claims; full externally reported Lean source NOT independently built. Original ErRo97 printed introduction source content checked via journal and primary extract, primary full pdf not accessible to screenshot; no independent full proof replay.

## Strongest verified interface
On CHAD exact integer fixture finite_885_886.py/json independently computes D(79200)∩D(227205)∩D(1258560)={36,468,692,1028}; prints and checks an actual positive factor pair for every one of the 12 memberships; confirms NOT 1029. A public catalogue reply accidentally transcribed 1029 rather than 1028. Separately verifies z in {330,870,2445,4155,10482} all give squares z²+a for each of offsets a={756000,15971200,45130176}; this is a 5-point, THREE-offset square construction, not 5 factor-difference sets sharing 5 values. Full D(N) enumeration agrees with exact square/parity factor certificate for N=1..2000. None of these finite checks proves the general all-k conjecture.

## Proposed bounded successor task
First prove the square-and-parity certificate ↔ D(N) membership for all positive N and nonnegative d, with exact >0 factor condition, paper proof or pinned Lean no-sorry theorem and literal axiom output, full finite regression. Second reconstruct Bremner's actual k=4 elliptic-curve witness via source-grounded exact 4-row/4-column factor table and investigate k=5 independently. Acceptance of k=5 requires 5 distinct increasing N with 5 exact shared differences, every square/parity certificate verified. Stop at reported k<=4 literature if no new witness; finite saturation and failed searches are not impossibility theorems.

## Prerequisites and blocker
1997/1999/2019 historical proofs not independently reconstructed or Lean-replayed; public April 2026 partial formalization not GCL-audited, and one public transcription contains wrong last value. No review or priority claim for k>=5.

## Reuse and claim boundary
Used original 1997 journal source, primary published result metadata, maintained problem status and independently reproduced exact finite arithmetic including transcription correction. No novel mathematical solution, independent elliptic curve proof, protected review/merge, live browser MathJax or V2 admission claimed.
