# EXT-015 REACH / UC-OP-002 — source-locked critical verification of the heat-normal conic rank gate

**Mathematical disposition: BOUNDED INTERNAL ACCEPT of the corrected exact primary UC-OP-001.** V-UC002 and A-UC002 are separate logical verification and hostile mathematical passes using the same ChatGPT/GitHub account and historical dependencies. This is not an independently authenticated nonauthor APPROVED review, an external referee report, or MATHCERT certification.

## 1. Exact immutable source, input contracts and verification evidence

The frozen primary under review is [UNIFORM_CONIC_GREEN_OPERATOR_AUDIT_UC001.md](UNIFORM_CONIC_GREEN_OPERATOR_AUDIT_UC001.md), Git blob 3ba80aa29c9a899ae9b5b02035aa6f4fdaec3713 on branch research/reach-uniform-conic-rank-gate-uc001-20261115, commit 9d0e884723174634dbc3ee5c5df5a9b8872c4320. Its prior draft Git blob ffa87226fc25a0034ab776dfd8050b78b6773b87 was superseded **before critical source freeze** to specify bounded parameter derivatives explicitly; there was no mathematical review and no admitted claim at that older source cut.

The frozen exact algebraic control fixture is [conic_heat_rank_gate_uc001.py](fixtures/conic_heat_rank_gate_uc001.py), Git blob 6e7b1ad23fe3d51c9274afe673d6b76e3ab49a72. CHAD's authenticated OS operator ran the actual GitHub branch file using Python 3.10 via a read-only repository API fetch, with execution receipt ID 1523f649dae5475098195c2d60f341e2 and downloaded bytes SHA256 42eb4e02b1e20c93b8301e9ecdd253c56f69d107fb26bd4f0bcb8d3682d1881d. All five exact rational rank cases PASS. The CHAD transport receipt explicitly says execution_origin LOCAL_OS_ONLY_NOT_INDEPENDENTLY_AUTHENTICATED; this is a live arithmetic test, **not** an independent mathematical proof attestation.

Original mathematical source contracts remain scalar105 Git blob a8ce66ff0edec33e2aff299550fca2089d671033, completed mixed108 blob 587c15fd6e24f6e6b14de574ff878221cdbd5cb6, parameter126 blob 5b05c6147d237ca1d22e4dcbce9262b0f038c163, and exact accepted conic first-core195 Git blob fc0fddb678f0cc0c1b9764bb449ab6d9150b33d0 with corrected source-locked review196 blob 6c9607eb3db55153e999587e6546931244ef2150 (protected PR3371 merge 1d741353367997f51d0789ad7049ded1c0712c9e). Proposed nonterminal checkpoint CP222 in PR3375 is a separate custody dependency, not a mathematical lemma.

## 2. V-UC002 — exact rank proof and source-stage moderation

On a fixed real vector space, the Gaussian directional convolution multiplier is the exponential of $-\epsilon^2 E(\zeta)/2$ with $E(\zeta)=|L\zeta|^2$. The zero set of this quadratic form is exactly $\ker L$. On a closed cone with compact unit cross-section, continuity yields a fixed strictly positive minimum on the unit section if and only if it misses the kernel. This proves UC1.1 without assuming that one positive value on one chosen basis vector controls the entire conormal subspace.

For each linear collision partition conormal $C_P$, ellipticity is therefore equivalent to injectivity of $L|_{C_P}$, i.e. the exact rank equality (UC1.3). Because only finitely many physical partitions are involved in an original finite history, a finite join of the positive constants is possible whenever every tested subspace has full rank. This is an algebraic necessary heat-normal gate, not an all-history source-inverse or a claim that every Gaussian factor is a directional convolution.

For a fixed compact $T\in H^{-s}_K$ and fixed high-frequency symbol $q$ supported in the elliptic cone, Fourier Cauchy–Schwarz gives a weighted integral with weight $\langle\zeta\rangle^{2s}|\zeta|^{2|\beta|}$. For the $k$th regulator derivative the Gaussian derivative is a finite sum of polynomial terms with at most $\epsilon^{-k}$ cost after scaling; a weaker Gaussian remains. The radial integral has scaling at most $\epsilon^{-2s-2|\beta|-m-2k}$. Taking the square root gives exactly (UC1.4), a continuous finite-seminorm bound independent of the chosen input within the fixed $H^{-s}$ stage. Smooth parameter differentiation requires uniformly bounded parameter derivative norms on compact parameter patches, as the corrected primary states. A moderate input curve is handled by finite Leibniz sums and its genuine original row orders.

**V-UC002 PASS UC1.1–UC1.4 as positive-regulator ambient smoothing and moderation for a factorized directional Gaussian heat family.** No all-corner PHG index set, completed108 coefficient output or original126.14 source-row lift follows solely from this bound.

## 3. A-UC002 — hostile three-coordinate partition and elliptic failure

Take real coordinates $(r,t,u)$ and one heat vector $v=(0,1,0)$. Its heat form is $E(\xi_r,\eta,\xi_u)=\eta^2$. The conormal to the partition $r=u$ consists of $(\tau,0,-\tau)$, which lies in $\ker L$. A proposed conic Fourier split removing this conormal from the “good” original R1 coefficient must have its bad selector $q=1$ on a high-frequency neighborhood of these rays.

The source $T(r,t,u)=\chi(r,u)\psi(t)\delta_0(r-u)$ is an actual **legal original108 nonidentity partition-inclusion history** with a smooth block coefficient and order-zero inclusion; it is not being smuggled in as an illegal original R1 coefficient on three independent vertices. Its t-direction heat convolution is exactly $\chi(r,u)\delta_0(r-u)(\kappa_\epsilon*\psi)(t)$. Choose $\psi$ nonnegative and nonzero. The smooth factor is then nonzero on a patch, so the $r=u$ conormal remains at each positive regulator.

The fixed conic multiplier $q(D)$ and the t-heat multiplier commute. Because $q$ is one microlocally on the entire nonzero conormal of this input, $(1-q(D))T$ is smooth there. Smoothing in t cannot manufacture the missing $r=u$ conormal from that smooth difference. Thus $q(D)\mathcal H_\epsilon^t T$ retains the delta conormal, and cannot be an interior-smooth scalar105 coefficient. Conversely the complementary piece cannot retain it while being an original R1 coefficient. This is a genuine no-go for the **one-edge R1-good plus scalar-bad transformation** on all partition inputs.

**A-UC002 PASS UC1.7–UC1.10 and Proposition UC1.3.** The hostile test is not a negative theorem about arbitrary original108 source membership: this $T$ is already legally sourced by its partition inclusion, and a different heat direction or different source presentation can evade the specific one-edge failure.

## 4. Additional adversarial scope checks

| Proposed inference | Critical disposition |
| --- | --- |
| A vector-wise nonzero heat pairing certifies an entire higher-dimensional conormal | FALSE. The two-generator full-diagonal example has nonzero pairing on each generator but rank deficient on their span. |
| A rank-passing convolutional Gaussian multiplier is smooth for positive regulator | PASS with fixed Sobolev estimates. |
| A rank-passing Gaussian multiplier is therefore an admitted fixed original105 scalar heat stage | NOT PROVED. Compatible all-corner indices, finite auxiliary weights and recursive differentiated remainders require their own construction. |
| Every original scalar105 **multiplication** edge is automatically a directional convolution | FALSE as a general inference. The primary expressly distinguishes them. |
| The conic multiplier $q(D)$ is an original108 universal source operation | NOT ASSERTED. It is an analytical splitting of a specified ambient distribution. |
| The 3-coordinate partition counterexample is an illegal source input | FALSE. A typed partition inclusion with smooth block coefficient is legal; it is illegal only as a free independent-vertex R1 coefficient. |
| Finite rank passing automatically supplies the 126 whole-source parameter rows | NOT PROVED. The result supplies only ambient estimates on bounded source input curves. |
| New result contradicts protected exact positive conic source of A and D | FALSE. The two-variable bad cone of conic195 is t-elliptic, whereas the 3-variable partition conormal is characteristic for t-heat. |
| Universal150.L, residual W acyclicity, originalR3, full126.14, higher weights, actual lifting and M5/R4 | OPEN. |

The five-case rational fixture explicitly checks a rank-deficient conormal **span** even though each displayed generator passes an individual nonzero-pairing test. Its run does not certify the Fourier estimates, source membership or any derived comparison.

## 5. Final bounded review decision

**ACCEPT corrected primary UC-OP-001 at exact Git blob 3ba80aa29c9a899ae9b5b02035aa6f4fdaec3713, with zero post-freeze mathematical corrections.** The new transferable mechanism is a finite heat-normal rank gate plus uniform positive-interior Sobolev estimates; the new negative result is one legal partition-inclusion source for which a fixed single heat direction cannot perform the scalar/R1 conic split.

The next genuine source obligation is to take a **rank-passing** set of actual factorized original108 histories and prove complete fixed105 scalar indices, full three-vertex or higher collision corners, real source-level completion, proper density maps and original126 whole-source rows. Failure of the rank gate rejects only the proposed heat-smoothing factorization, not every possible source history or the original Green comparison question.

Source-lock and scientific review are distinct from a downstream ledger UC-OP-003, exact-head native CI, protected merge and protected-main readback. No independent external mathematical certification, general Green inverse or programme completion is asserted.
