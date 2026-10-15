# EC-BULK-007 — #1193 literal convolution-density counterexample

**Original-source intention PENDING; mathematical literal counterexample established.**

Original: https://www.erdosproblems.com/1193
Authenticated return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2464#issuecomment-6187244091
Primary historical source Erdős (1980), p.100.

With A={0,1,2,...}, each n>=0 has exactly n+1 ordered decompositions n=a+b, hence (1_A*1_A)(n)=n+1. Take positive nondecreasing g(n)=n+1. The agreement set contains all n; upper and lower densities equal 1, refuting both printed assertions. With positive-only integers, take A={1,2,...} and g(n)=max(1,n-1), agreeing for all n>=2. Phase23 validates the first 21 coefficients, while the formula itself is proved for every n by enumeration of the pairs (a,n-a).

This is NOT a new counterexample to a possible **corrected** problem imposing restrictions on A or g. Independently inspect Er80 and current formal-conjectures code for any omitted density/sparseness/growth hypotheses and preserve the original issue source hash.

**Source-fidelity status: pending; protected V2 review not complete.**
