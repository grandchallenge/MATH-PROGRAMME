# Erdős #12: resolve the original 1970 Property P convention

Status: SOURCE_FIDELITY_ADJUDICATED; mathematical conjecture NOT solved.
Supersedes only the previously unresolved historical-terminology obligation
in GCL-ERDOS-CRITICAL-SOURCE-CORRECTIONS-005, not the frozen source lock.

## Primary evidence, page exact

P. Erdős and A. Sárközy, *On the Divisibility Properties of Sequences of
Integers*, Proceedings of the London Mathematical Society (3) 21 (1970),
97–101, DOI 10.1112/plms/s3-21.1.97, Rényi edition
https://users.renyi.hu/~p_erdos/1970-13.pdf

Full original five-page PDF retrieved and image-inspected, printed pp97–98,
2026-10-15. PDF SHA256:
4adba03f04de19ebb6ac9bddc6eaf43567619ca96c6cbe574e4c04be3595d0f3.
No source PDF is redistributed in this repo.

On printed p97 the authors define property P using “two larger terms”.
On printed p98 they explicitly state that the lower construction achieving
floor(x/3)+1 consists of the floor(x/3)+1 *largest* integers not exceeding x.
The same page attributes a statement about *three distinct terms* to
Szemerédi. This clarifies what “two larger terms” must mean for the original
exhibited construction: larger distinct terms, not two uses of one element.

## Decisive mathematical falsifier for the stronger reading

For each m >= 1, take x=3m and A_m={2m,2m+1,...,3m}. Then
|A_m|=m+1=floor(x/3)+1, the exact 1970 lower-example size.

This set obeys the weaker, distinct-larger-summands predicate:
for a<b<c with all in A_m, b+c>2a. If a>2m,
b+c<=6m<3a, so no positive multiple of a is possible.
If a=2m, then 2a<b+c<3a: the upper inequality is strict because
b and c cannot both equal 3m when b<c. Therefore a does not divide b+c.

But the stronger repeated-summands predicate is FALSE:
a=2m and b=c=3m satisfy a<b=c and
a divides b+c=6m=3a.

Thus for the very example the 1970 paper asserts to have property P, the
2017-style repeated-summand convention would make the assertion false.
The author's own theorem/example combination is therefore strong
evidence that the ORIGINAL 1970 convention and the frozen provider's
distinct-larger-summand IsGood agree on the repetition distinction.

The paper leaves “two larger terms” informal, so the conclusion is a
source-interpretation adjudication grounded in a logically decisive
author-provided example, rather than a quotation that explicitly states
b!=c in the original definition.

## Later literature has a different stronger convention

Elsholtz and Planitzer, *On Erdős and Sárközy’s sequences with Property P*,
Monatshefte für Mathematik 182 (2017), Section 1,
https://doi.org/10.1007/s00605-016-0995-9, use
i<j<=k, thereby FORBIDDING repeated larger summands b=c. This is a
strictly stronger condition, even for infinite sets as shown by the
counterexample already supplied in GCL critical review #2521.

It is incorrect to infer that the later repeated-summand definition is
identical to the original 1970 source. Maintain two separately named
predicates, ORIGINAL_1970_DISTINCT and STRONGER_REPEATED.

## Resulting source and proof boundary

- The frozen and refreshed provider IsGood predicates exclude only
  distinct b,c, matching the original paper's explicit extremal example.
- The upstream Schoen/Baier companion quantifier corrections remain
  accepted as source-fidelity fixes (bounds along infinitely many cutoffs).
- The existing 2026 external formal results for (i)/(ii) still require
  exact-type/axiom/source replay prior to GCL mathematical certification;
  their theorem types concern the provider's actual IsGood, NOT an
  unspecified 2017 stronger predicate.
- The still-OPEN reciprocal-summability conjecture (part iii) stays open.
- The original protected 2026 issue and provider Git SHA MUST NOT change.
  This audit is a new source-interpretation addendum only.
- No Solve campaign, certification, publication claim, or automated
  gcl-review:revise clearance is authorized by this source addendum.

## Executable evidence

Run python3 governance/source_erdos_critical_005/property_p_1970_primary_regression.py.

Exhaustively verifies each A_m for m=1..200 with distinct-vs-repeated
definitions; separately proves the entire family mathematically in the
inequalities above. Expected all 200 weak True, all 200 strong False.
The executable regression is a falsifier for equating 1970 and 2017
terminology, not a proof of the unresolved reciprocal conjecture.
