# EC-BULK-007 critical sample #1188 — minimal distinct coverings

**Independent nonauthor mathematical review PENDING. Not a theorem proof, formal certificate or protected admission.**

Source: https://www.erdosproblems.com/1188
Original issue return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2459#issuecomment-6186945371
Primary references: Erdős 1980 p.95; Hough 2015, Ho15; Balister–Bollobás–Morris–Sahasrabudhe–Tiba 2024, BBMST24.

A *minimal distinct covering system* is an actual set of distinct moduli with assigned congruence residues, covering all integers, such that removal of any assigned class destroys the covering. An *irreducible covering set of moduli* is stronger: after removal of a modulus, **no alternative residue assignments** cover. The latter belongs to #1189, and unrestricted nonminimal covering systems must not inflate F(x).

The BBMST24 external lower bound is F(x) >= exp((log x)^(3-o(1))); the trivial upper is exp(O(x log x)). The exact theorem and parameter substitution must be independently verified.

**Finite evidence:** Phase22 restricts allowable moduli to {2,3,4,6,8,12}; exactly 49,140 options are checked over period 24. Exactly 216 choices cover and exactly 24 are minimal by original-residue deletion. Example: 0 mod2, 0 mod3, 1 mod4, 1 mod6, 11 mod12. This enumerates a **restricted six-modulus family**, NOT all F(12).

Evidence: ci/erdos_compendium_007_phase22_checks.py and EC-BULK-007_FINITE_CHECKS_PHASE22.json.

**Independent review must** inspect Er80, Ho15 and BBMST24 source definitions; re-enumerate using an independent method; check minimal original assignment versus irreducible moduli; verify all asymptotic exponent manipulations; submit authenticated nonauthor APPROVE/REVISE, reviewer identity and primary pages before critical completion.

**Critical review state PENDING; cohort approved 0/20.**
