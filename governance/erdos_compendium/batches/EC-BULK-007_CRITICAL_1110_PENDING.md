# EC-BULK-007 — Erdős #1110 predetermined critical sample

**Disposition: PRIMARY-SOURCE-AND-INDEPENDENT-CRITICAL-REVIEW-PENDING.** Not a completed review, source-fidelity certification or protected admission.

Source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2381#issuecomment-6168841804
Maintained catalogue: https://www.erdosproblems.com/1110 (parent OPEN, April 2026).
Unaccepted manuscript: governance/erdos_compendium/editorial/1110.md

## Exact theorem/quantifier separation

Fix coprime p>q>=2. Representation means a sum of distinct p^k q^l with selected summands a DIVISIBILITY ANTICHAIN. Original density and coprime-nonrepresentability questions are about all p,q EXCEPT {3,2}. The elementary (3,2) induction solves existence for all positive integers, whereas a separate problem optimizes the smallest summand for (3,2).

Reported published boundaries:
- Erdős–Lewin 1996: finitely many nonrepresentable positive integers iff {p,q}={3,2}.
- Yu–Chen 2022: representables have density zero when q>3, or q=3,p>6, or q=2,p>10; infinitely many coprime nonrepresentables if q>3, or q=3,p!=5, or q=2,p outside {3,5,9}.
- Blecksmith–McCallum–Selfridge (1998) and Yang–Zhao (2025) are attributed minimum-summand asymptotics; full original theorem statements and dates must be verified before certification.

## Reproduced construction

Phase-12 script ci/erdos_compendium_007_phase12_checks.py recursively represents every n<=1024 for p=3,q=2, verifies each term 2^a3^b, exact sum, uniqueness, and that neither of two terms divides the other. Induction: even n double an antichain for n/2; odd n subtract greatest 3^k<=n and double antichain for (n-3^k)/2; each old term is <3^k, so its factor of 3 has exponent <k, while each new term is even. This preserves antichain with 3^k. The induction is standard and attributed to prior work, not a novel GCL theorem. Bounded enumeration is an independent replay, not a substitute for the external density proofs.

## Mandatory critical-review obligations

1. Obtain and hash original Erdős–Lewin 1996, Yu–Chen 2022 and the 1998/2025 minimum-summand papers; record theorem pages and exact remaining exceptional (p,q).
2. Independently inspect the induction proof, especially no-divisibility condition, k,l=0, zero/empty-sum base and uniqueness.
3. Verify reported sharp constant and whether it applies to the *fastest growing minimal-summand threshold* or a different optimization.
4. Reconcile current formalized statement with older frozen formal-conjectures snapshot; no kernel proof implied by source label.
5. Perform independent mathematical critical review and record APPROVE/REVISE with proof citations, not merely self-audit.

Critical sample completion remains 0/20 in this stage; source fidelity, protected production and V2 admission pending.
