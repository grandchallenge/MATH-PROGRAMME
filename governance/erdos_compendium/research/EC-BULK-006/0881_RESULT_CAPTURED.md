RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0881-S01
PROBLEM_ID: 881
DISPOSITION: STATUS_CONFLICT
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
Let A be an infinite asymptotic basis of order k, with every sufficiently large positive integer expressible as EXACTLY k summands from A, repetition permitted. Assume A is strongly minimal in the sense that removing ANY infinite subset B of A destroys its order-k basis property. Does SOME infinite deletion B leave A\B as an asymptotic basis of order k+1? The order k+1 quantifier is existential over infinite deletions, whereas strong minimality is universal; these cannot be exchanged. Exactly-k need not agree with at-most-k absent zero padding.

## Dated status and primary evidence
Erdős, 'Some of my new and almost new problems and results in combinatorial number theory', 1998 Eger proceedings pp169–180, DOI https://doi.org/10.1515/9783110809794.169; primary chapter full text not independently inspected. Maintained https://www.erdosproblems.com/881 OPEN as of October 14, 2026; frozen teorth catalogue @536408716724a2402bdfa7c1d764bf83d64a8c89 OPEN. May 3, 2026 submission by Svyable to https://www.erdosproblems.com/forum/thread/881 claims YES for k=1 and a NO counterexample for each k>=2 using thin strongly minimal bases. Independent discussion same day identifies major proof gaps (natso26) and requests explicit AI-work attribution (Thomas Bloom). No independent full construction, formal replay or adjudication; the claimed k>=2 negative resolution is NOT established by this return.

## Strongest verified interface
k=1 has an elementary independent positive solution. An order1 asymptotic basis A contains all sufficiently large integers. Choose B consisting of powers of two lying in A (infinitely many), and D=A\B. The complement of D has counting function O(log n)=o(n). To express a sufficiently large n as a sum x+(n-x) with x and n-x in D, choose x in [n/3,2n/3]; Omega(n) candidates are available, and at most 2o(n) excluded. Thus D is a basis of order2 after infinite deletion. An exact finite fixture separately verified this construction on targets n=30..2000; finite samples alone are not the proof. No statement about k>=2 is inferred.

## Proposed bounded successor task
Input original strong-minimal quantifiers and exact-k convention, Svyable 2026 submission and all referee objections. Target: independently prove or refute each claimed infinite k>=2 counterexample by checking (1) eventual order-k coverage, (2) destruction by EVERY infinite deletion and (3) NO infinite deletion preserving order k+1, including all stage inequalities. Acceptance source-locked complete proof or pinned no-sorry Lean build with literal axiom readback and explicit repair of every objection. Falsify via a missing k-sum target, an infinite deletion preserving order k, or a deletion yielding an order-(k+1) basis. Stop before solved-status promotion.

## Prerequisites and blocker
Original 1998 chapter full text and the critical claimed 2026 stage lemmas not independently source-locked. Public reviewer objections unresolved. No protected independent mathematical review or Lean kernel certificate. Strong minimality cannot be justified from finite prefixes.

## Reuse and claim boundary
Reused maintained problem statement and public forum discussion, independently established sparse-deletion k1 lemma and finite tests. No new result for the open k>=2 cases, protected merge, formal certification or editorial admission claimed.
