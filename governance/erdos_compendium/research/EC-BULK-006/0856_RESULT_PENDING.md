RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0856-S01
PROBLEM_ID: 856
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For fixed k>=3 and N>=1, call A subset [N] LCM-k-free if no k distinct a_i in A have lcm(a_i,a_j) equal for every pair i<j. Let f_k(N)=max_A sum_{a in A}1/a. Estimate f_k(N) as N tends to infinity. The harmonic sum is distinct from the cardinality variant #536. Erdős originally asked this in 'Some Extremal Problems in Combinatorial Number Theory' (1970), printed pp.127-128, https://users.renyi.hu/~p_erdos/1970-21.pdf .

## Dated status and primary evidence
Pinned teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89: OPEN, 2025-08-31, no admitted Lean statement. Live https://www.erdosproblems.com/856 fetched 2026-10-13 (HTTP 200, last edit 2026-01-18): still open, notes an unadjudicated comment-level proof claim. Original Erdős 1970 printed pp.127-128 directly inspected. Tang and Zhang, 'Harmonic LCM patterns and sunflower-free capacity', arXiv:2512.20055v1, 2025-12-23, https://arxiv.org/abs/2512.20055 , provide improved exponents. The modern page revision is newer than the pinned packet, which remains unchanged.

## Strongest verified interface
For fixed t, suppose t=a_i p_i for k distinct primes p_i and a_i in A. Then lcm(a_i,a_j)=t for every i!=j, contradicting LCM-k-freeness. Thus at most k-1 such representations exist. Summing 1/(ap) gives (sum_{a in A}1/a)(sum_{p<=N}1/p) <= (k-1) sum_{t<=N^2}1/t, hence f_k(N)=O_k(log N/log log N) using classical prime reciprocal estimates. This is Erdős's 1970 argument, not a new theorem. Tang-Zhang's primary abstract states bounds (log N)^(log(mu_k)-o(1)) <= f_k(N) << (log N)^(mu_k-1+o(1)), where mu_k is the k-sunflower-free capacity; these published claims have not been proof-rederived. Exact exhaustive Fraction arithmetic for k=3 gives f_3(5)=137/60, f_3(6)=137/60 and f_3(7)=1019/420. The first forbidden triple is {2,3,6}, whose pairwise LCMs are all 6.

## Proposed bounded successor task
Inputs: Erdős 1970 pp.127-128, Tang-Zhang arXiv:2512.20055v1, the frozen registry and exhaustive k=3,N<=12 fixture. Prove the finite multiplicity lemma: LCM-k-free A implies at most k-1 representations t=ap with a in A and p prime. Derive the weighted double count, with correct endpoints. Accept a checked finite lemma plus independently reproduced exact rational maxima for N=5,6,7; falsify with an explicit t and k representations or an exact-value mismatch. Stop before asymptotic sharpness or any unregistered formal-provider change.

## Prerequisites and blocker
The 1970 primary source is accessible; the elementary lemma has no source blocker. The full Tang-Zhang proof and comment-level purported resolution require separate mathematical review. No protected Formal Conjectures statement is admitted for #856. Do not treat a source audit as a Solve campaign.

## Reuse and claim boundary
Used original Erdős 1970 scan pp.127-128, current #856 page, Tang-Zhang 2025 primary preprint abstract and original GCL issue #2127. Exhaustive rational examples recomputed directly, without Lean compilation. No claim of priority, general sharp asymptotics, mathematical certification or editorial acceptance.
