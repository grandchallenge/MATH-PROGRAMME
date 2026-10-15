# EC-BULK-007 critical sample #1186 — arithmetic progression density

**Independent nonauthor mathematical review PENDING. Not a certification, theorem proof, or protected admission.**

Original catalogue: https://www.erdosproblems.com/1186
Authenticated source research return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2457#issuecomment-6186944413
Primary source studies: Erdős 1980 p.93; Parrilo–Robertson–Saracino PRS08; Wolf 2010; Lu–Peng 2012.

The density parameter delta_k counts minimum monochromatic k-APs in binary colorings of [n], counting a positive step d and start a once, normalized by n^2. Check if the source means a limit or liminf before certifying any theorem. The reported PRS08 sharp interval is 1675/32768 <= delta_3 <= 117/2192. The conjectured upper value is NOT established. Do not confuse delta_k with the cyclic finite-field counterpart tilde-delta_k, whose counting convention differs.

**Finite evidence:** phase22 exact enumerator checks every binary coloring for n=8,10,12, obtaining minimum counts 0,1,2, respectively. Separate cyclic finite-field checks at p=5,7,11 enumerate unordered 3-APs. This is not an asymptotic density proof.

Evidence: ci/erdos_compendium_007_phase22_checks.py, EC-BULK-007_FINITE_CHECKS_PHASE22.json.

**Independent review must** (1) read Er80 and PRS08 originals and normalize the delta limit; (2) reproduce all exact finite minima by a separate implementation; (3) inspect PRS08 rigorous SDP bounds and source rational endpoints; (4) check Wolf and Lu–Peng field definitions, avoiding false equality with interval delta; (5) record nonauthor reviewer identity, source pages, APPROVE/REVISE and scope. Zero of these is considered completed merely by writing this dossier.

**Critical review state PENDING; cohort approved 0/20.**
