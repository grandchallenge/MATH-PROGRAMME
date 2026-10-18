# Erdős Problem #14 — Exact Historical Source-Root Reconstruction and Lean Kernel Replay (`#2702`)

## 1. Attribution and Claim Boundary

- **Original External Solver**: `JenW1N` (September 2026 public submissions on Conjectures.io). GCL does **not** claim discovery or authorship of either proof.
- **Assignment Scope**: `ERDOS-014-EXACT-LEAN-REPLAY-001` (`#2702`, parent review `#2522`, catalogue `#1283`, programme `#2503`).
- **Governance Boundary**: This artifact records the deterministic reconstruction of historical source commit `8432eac998110a563e03df65a28c117e97c8c142`, compiler-verified canonical target type-hash parity (`01f4b21faa141073550ace4791e41bb283bad80fb700e8965387588dc9238029` and `92676249a3598e8a654641b6d8078ed91bb3b00db116143e5a586cd63e1e6b20` / negated `f70369d772ff7a4ffb6b04dd772d2765f578571e039e13c26ef25d6ba92bd708`), and independent trust-level-0 (`lean -t 0`) kernel replay of both unmodified `JenW1N` proof submissions (`i-Main.lean` and `ii-Main.lean`). It does **not** claim `MATHCERT`, does **not** alter owner status or frozen source locks, and does **not** directly clear `gcl-review:revise` on `#2522`.

---

## 2. Deterministic Reconstruction of Commit `8432eac998110a563e03df65a28c117e97c8c142`

Previously, `8432eac998110a563e03df65a28c117e97c8c142` was not directly fetchable as a raw ref from `google-deepmind/formal-conjectures` because the Conjectures pool builder constructs it deterministically by applying the audited tier-1 patch from `conjectures-io/conjectures-tasks@275ef4824c41d41f97ac4e9fff95ca471de9341d` (`scripts/pin_dependencies.sh` in `conjectures-validator@6a8f6c479eb7d9726b4e935f17dc012d1cc5224c`):

1. **Upstream Base Commit**: `google-deepmind/formal-conjectures@7d1a8c9912747679d0093f6d1216420c33ee5ffa`
2. **Audited Patch**: `tiers/tier-1/formal-conjectures-audit-fixes.patch` from `conjectures-io/conjectures-tasks@275ef4824c41d41f97ac4e9fff95ca471de9341d` (SHA256 `853372293b16a79ea495a28909e6077d41e2c6402165c3c6233ea0747c919814`)
3. **Deterministic Commit Tree**:
   - `GIT_AUTHOR_NAME="Conjectures Pool Builder"`, `GIT_AUTHOR_EMAIL="pool@conjectures.io"`, `GIT_AUTHOR_DATE="2026-08-03T00:00:00Z"`
   - `GIT_COMMITTER_NAME="Conjectures Pool Builder"`, `GIT_COMMITTER_EMAIL="pool@conjectures.io"`, `GIT_COMMITTER_DATE="2026-08-03T00:00:00Z"`
   - Message: `fix(ErdosProblems): correct audited candidate statements`
   - Resulting Git Commit SHA1: `8432eac998110a563e03df65a28c117e97c8c142` (exact match)
   - `FormalConjectures/ErdosProblems/14.lean` Git blob SHA1: `52016d0053f4656cca69c135f4e95ef1449d63f6` (file SHA256 `63e02a65ab619a881bcbec9319e71a61fc26bf8bdb9be069c85149bfcfc0cf4c`)
   - `lean/TaskSupport.lean` SHA256: `58a80a223dbd7383d92eb2a57b1ec207c0991131a1a1bf24585a4452777c257e`

---

## 3. Exact Canonical Target Type-Hash Parity and Kernel Replay

Using `TaskInspector.lean`'s exact `canonicalExpression` options (`pp.all = true`, `pp.universes = true`, `pp.explicit = true`, `pp.proofs = true`), the elaborated theorem types reproduce the exact historical SHA256 digests:

| Task / Part | Task ID | Expected Type SHA256 | Recomputed Type SHA256 | Submission SHA256 | Kernel Replay (`lean -t 0`) | Printed Axioms |
|---|---|---|---|---|---|---|
| Part i (`formalized`) | `fc-8432eac9-parts-i-8313191e7a-formalized-v1` | `01f4b21faa141073550ace4791e41bb283bad80fb700e8965387588dc9238029` | `01f4b21faa141073550ace4791e41bb283bad80fb700e8965387588dc9238029` | `496840684dd5dc4f0747bf4732ee4fe246340353f8a11aae00bde325fa100ca5` | `PASS` (`exit_code = 0`) | `[propext, Classical.choice, Quot.sound]` |
| Part ii (`counterexample` source) | `fc-8432eac9-parts-ii-837c84619c-counterexample-v1` | `92676249a3598e8a654641b6d8078ed91bb3b00db116143e5a586cd63e1e6b20` | `92676249a3598e8a654641b6d8078ed91bb3b00db116143e5a586cd63e1e6b20` | `188ebf8bdf3a04694155ddf3e2d87c64f53d545781cfda7b63e21d6b1434cd74` | `PASS` (`exit_code = 0`) | `[propext, Classical.choice, Quot.sound]` |
| Part ii (`counterexample` negated target) | `fc-8432eac9-parts-ii-837c84619c-counterexample-v1` | `f70369d772ff7a4ffb6b04dd772d2765f578571e039e13c26ef25d6ba92bd708` | `f70369d772ff7a4ffb6b04dd772d2765f578571e039e13c26ef25d6ba92bd708` | `188ebf8bdf3a04694155ddf3e2d87c64f53d545781cfda7b63e21d6b1434cd74` | `PASS` (`exit_code = 0`) | `[propext, Classical.choice, Quot.sound]` |

### Verifier & Adversarial Checks

1. **Static Token Policy (`verifier.static_checks.check_submission`)**: Both `i-Main.lean` (49,184 bytes) and `ii-Main.lean` (46,599 bytes) pass with `valid = True`, `violations = ()`.
2. **Dependency Closure & No-Sorry Audit**:
   - Part i `Bounty.target` (`166` reachable local declarations) and Part ii `Bounty.target` (`155` reachable local declarations) have `depends_on_sorryAx = false`, `value_has_sorry = false`, `type_has_sorry = false`, and zero dependency on the forbidden source theorems `Erdos14.erdos_14.parts.i` or `Erdos14.erdos_14.parts.ii`.
3. **Hostile Altered-Target & Cross-Part Rejection**:
   - Kernel definitional equality check (`isDefEq`) confirms `defeq_hostile_altered = false` against an altered target statement (`∀ A : Set ℕ, nonUniqueSumCount A = nonUniqueSumCount A`) and `defeq_other_part_target = false` between Part i and Part ii.
4. **Natural-Number, Zero, Unordered-Pair, and Diagonal Semantics**:
   - `A : Set ℕ` allows $0 \in A$, while `nonUniqueSumCount A N = ((Set.Icc 1 N) \ allUniqueSums A).ncard` counts exceptions in $\{1, \dots, N\}$.
   - `allUniqueSums A` requires unordered pair uniqueness (`(a₁ = p.1 ∧ a₂ = p.2) ∨ (a₁ = p.2 ∧ a₂ = p.1)`), permitting diagonal summands $p_1 = p_2$ as a single representation (captured by `(pairs s n).card + (diagonal s n).card = 2`).
   - Both submissions establish the scale obstruction $T^2 < 1000 \cdot (\mathrm{nonUniqueSumCount}(A, 2T^4) + 1)$ for all $T \ge 10^6$, yielding the uniform $\Omega(N^{1/2})$ lower bound that simultaneously proves Part i (`∀ ε > 0`) and refutes Part ii (`¬ ∃ A, nonUniqueSumCount A = o(N^{1/2})`).
