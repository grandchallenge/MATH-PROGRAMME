# EC-BULK-007: #1173 mandatory independent mathematical review

**Disposition: PENDING.** Not a proof or protected admission.

- Original catalogue: https://www.erdosproblems.com/1173
- Authenticated original issue return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2444#issuecomment-6185315993
- Primary sources to adjudicate: Vardi (1999), Problem 7.88, and Komjáth (2025), Problem 35.
- External background: Hajnal (1960), free-set theorem; Soukup (2013), essentially disjoint families. Online working reports are not independently certified.

## Exact mathematical contract

Let $\mu=\aleph_\omega$ and $\kappa=\mu^+$. Assuming GCH, given $f:\kappa\to[\kappa]^{\le\mu}$ with $|f(\alpha)\cap f(\beta)|<\mu$ for distinct $\alpha,\beta$, determine whether some free $H\subseteq\kappa$ has size $\kappa$. Free means neither $x\in f(y)$ nor $y\in f(x)$ for distinct members. Review the optional requirement $x\notin f(x)$.

Critical boundary: $\operatorname{cf}(\mu)=\omega$. The pairwise strict $<\mu$ bound need not admit one uniform bound $<\nu$ for all pairs.

## Independently exact finite illustration

Phase20's eight-cycle map $f(i)=\{(i+1)\bmod 8\}$ has disjoint one-element images. Exhaustive enumeration of 256 subsets gives largest free set of size four, including the alternating set $\{0,2,4,6\}$. The empty mapping admits all eight elements. This proves nothing about existence of a $\kappa$-sized free set.

Evidence: ci/erdos_compendium_007_phase20_checks.py and EC-BULK-007_FINITE_CHECKS_PHASE20.json.

## Independent critic obligations

1. Read original primary Vardi and Komjáth pages and confirm exact GCH, cardinal, map and free-set hypotheses.
2. Audit all singular-cofinality/uniform intersection assumptions; do not apply regular-cardinal thinning without proof.
3. Independently verify the eight-cycle enumeration and normalize self-incidence.
4. Verify any cited Hajnal and Soukup theorem with exact assumptions before relying on an external working report.
5. Record non-author mathematical review APPROVE or REVISE, identity and source citation, before counting this mandatory sample.

**Mandatory sample #1173 remains PENDING. Cohort completed reviews: 0/20.**
