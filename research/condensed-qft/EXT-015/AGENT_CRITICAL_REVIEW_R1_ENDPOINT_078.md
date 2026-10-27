# EXT-015 REACH / 078 — critical audit of the uniform normal regulator endpoint

**Provenance:** distinct logical mathematical critic pass after the author source was frozen, within the same Codex session/account. No external independent certification is claimed.

**Exact source:** commit `907df5ecc330d49d92f28553d800fc7fd251580a`; [077](R1_UNIFORM_NORMAL_REGULATOR_ENDPOINT_077.md) blob `f2c2460a9d13efc2604a061f171538aeb22aba4f`; [fixture](fixtures/check_uniform_normal_endpoint_077.py) blob `accd24bc6030ad142e12492b195302216c89ea20`.

## 1. Normal-topology smoothness is checked at zero

The regulator is the actual even compact mollifier of 028. Its extension to negative parameter values is defined distributionally by scaled tests, so zero lies in an open parameter interval. Differentiation under the compact integral is uniform on bounded test families and gives the stated even moment/delta derivatives.

Strong distributional smoothness alone would not suffice. The source separately checks every extra normal Fourier seminorm: localizations away from the collision have identically vanishing mollifier or identically unchanged primitive near zero; localizations meeting zero admit no nonempty Fourier cone separated from the full relative conormal there. At nonzero scale, ordinary joint smoothness supplies the remaining neighborhoods. This is a valid proof in the fixed normal topology.

**Assessment:** support Lemma 77.1, including the exact primitive and its regulator derivatives. Compact support and evenness of the mollifier are used explicitly.

## 2. The uniform operator quantifier follows from hypocontinuity

The pair-variable pullback is a submersion and the cutoff is a fixed smooth compact localization. Their normal-topology continuity gives one kernel sector for all nearby regulator values. The cutoff is only an estimate device; it is one near the fixed input support and does not change the intrinsic contraction.

The product cone contains the input term, pair-conormal term and their sums. The output calculation rules out all three possible forbidden output contributions, using the full simultaneous-partition exclusion. Thus one admissible output sector works for the family and every regulator derivative.

Hypocontinuity with respect to a bounded input set is exactly the continuity needed for the kernel-to-operator map into the bounded-input operator topology. Composing with the smooth kernel curve therefore gives smooth operator curves, not merely convergence on one input. Taylor's estimate for each operator seminorm yields the stated order-two estimates because the first regulator derivative vanishes.

**Assessment:** support Theorem 77.2 with its stated bounded-input quantifiers. No estimate uniform across every support/cone sector or excluded collision kernel is inferred.

## 3. Completed transport and the connection are correctly typed

At finite total weight, the contractions, exponentials and inverses are finite and pass through finitely many compatible sectors. The fixed-sector uniform theorem therefore applies to each composition. Product plots and split truncations from 069 justify the formal completed statement without interchanging support colimits or requiring analytic convergence in the quantum parameter.

The transport is the actual Wick-conjugation cochain isomorphism. Its inverse, cocycle identity, interval naturality and compatibility with disjoint structure maps follow at each finite weight and hence in the completion.

The quantum differential varies with the regulator. The source does not identify bare regulator differentiation with a cochain connection. The transported connection in (77.10) is conjugate to the constant classical connection, so it commutes with the differential and has the asserted horizontal transport. This is a connection on the regulator family; the fixed-regulator DVS connections retain their original parameter meaning. The distinction is essential.

The Weiss argument uses the already-proved refined classical comparison, natural Wick trivialization and the same split finite-weight tower. It proves the result on this restricted microlocal family, not an unproved equivalence with the positive-scale domain containing all compact distributions.

**Assessment:** support Theorem 77.3 and the stated completed-family/Weiss consequence.

## 4. Hostile controls and disposition

The fixture checks formal independent even moments and spatial delta-jet differentiation, exact finite cochain conjugation, 49 transports and 343 cocycle identities. Its independent explicit differential derivative verifies the transported connection and gives a nonzero failure for the bare derivative away from zero. These controls do not stand in for the infinite normal-topology estimates.

The global LCS identity remains obstructed by 075; the refined sector endpoint theorem does not undo that result. Excluded collision delta kernels, global renormalized BV/QME and original-source higher liquid Ext are outside this theorem.

**Verdict:** accept the uniform endpoint, completed Wick transport and correctly typed connection within the precise D21/069 domain. Together with 069/070 and 075/076 these address the distinct R1 analytic obligations. Any R1 tracker closeout still requires protected source/fixture/audit readback, an exact acceptance ledger and editorial reconciliation; no full REACH completion or external certification follows.
