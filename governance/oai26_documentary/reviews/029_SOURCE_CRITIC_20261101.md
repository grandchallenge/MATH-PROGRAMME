# Family 029 — source-bound statement critic

Source lock: openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a.

The primary 92-page paper, *Primitive roots for every admissible integer base*, Git blob dc2342d776f280e81d73ffa5a8eaf7b8f51745df (891737 bytes), was downloaded. Its abstract and introductory Theorem 1.1 claim for each fixed integer a other than -1 or an integer square at least c_a x/(log x)^2 primes in (x,2x) with a primitive modulo p, for every sufficiently large x. The paper calls this an infinitude result, not the predicted full positive-density asymptotic.

The 21-page *Simultaneous primitive roots: a conditional lower bound for prime bases*, Git blob 5ec52e9d5a8b6c50490d3c28baef2dbe2e609b02 (450863 bytes), was downloaded. Its introductory Theorem 1.1 expressly ASSUMES Inputs 3.1, 4.1, 5.1 and 5.2: respectively a Hecke zero-free assertion, marked Type II estimate, block sieve and rough-number density estimate. It then claims the same shape of lower bound for simultaneous primitive roots of every fixed finite collection of distinct positive prime bases. Although the inputs are sourced to the companion, this manuscript's theorem must retain its conditional formulation.

Editorial disposition: ACCEPTED_EXPOSITION_WITH_LIMITS. The six-section article reflects these directly read theorem statements and scope, does not confuse a single arbitrary integer base with simultaneous prime bases, and explicitly declines to certify the mathematical proofs. Not checked: complete 113-page proof chains, analytic Hecke zero-free argument, cubic theta normalization, marked Type II estimates, field-splitting comparisons, sieve transfer, imported dependencies, Lean mapping or MATHCERT certificate. This bounded statement-level critic is not an independent mathematical certification. Exact-hash admission, generated HTML and regression checks are separate requirements.

Parent #2901 remains open.