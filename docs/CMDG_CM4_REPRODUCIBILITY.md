# CMDG-CM4 — Independent reproduction and provenance

**Status:** runnable, source-locked verification protocol. Repository CI previously proved the protected formal lanes; this page does **not** claim a fresh external machine has already executed the instructions. Anyone can run them without GCL credentials, special GitHub permissions, or accepting GCL's governance conclusions.

## What the replay establishes

The replay checks that the proof-bearing source has not drifted from the protected CM4 theorem, validates the registered formal lanes, verifies the *exact* mathlib commit and tree, and compiles the local transitive Lean import closure. It yields local JSON records for two formal lanes. It does **not**, by itself, establish independent mathematical peer review, originality of the proof, upstream compatibility with current mathlib master, or the derived/complex source theorem.

| Identity | Value |
| --- | --- |
| Public repository | [grandchallenge/MATH-PROGRAMME](https://github.com/grandchallenge/MATH-PROGRAMME) |
| Suggested stable checkout | `7a0f33588aa8d1add4d941c9b4681b6910644bf1` (contains #1208's protected proof repairs) |
| Terminal proposition | `CMDG.CondensedCM4.CM4Target` |
| Terminal theorem | `CMDG.CondensedCM4.cm4Target_via_pointFunctional` |
| Original protected CM4 closure | [#1218](https://github.com/grandchallenge/MATH-PROGRAMME/pull/1218) |
| Terminal source blob (Git SHA-1) | `8ab0051746507099f7321460fe091e56a84b57bb` |
| Point-functional source blob (Git SHA-1) | `d3ef22a2ad2d9c0af6982773d0a24b715e61f5a7` |
| Lean version | `leanprover/lean4:v4.33.0-rc1` |
| mathlib commit | `79d0395a1825a6264ad5d269e35e60537518955e` |
| mathlib tree | `d76f5e09b832a08949f6d8ad4fb80ce30527da64` |
| Formal registry | `governance/formal_validation_registry.json` |

All inputs above are **identity claims**: independently check the bytes, not merely the file names. The reference checkout is a snapshot with the repaired #1208 proof. A later tree with unchanged protected theorem/bridge blobs is also valid for the script, but any changed dependency requires a fresh provenance and replay audit.

## Prerequisites

A Linux environment or WSL2 with `git`, `python3`, a Python environment able to install `requirements/policy.txt`, and `elan` (which provides `lake`). Internet access is needed for first-time installation and obtaining mathlib caches. The pinned Lean toolchain comes from `fixtures/formal/CMDG-NAT-CONCORDANCE-001/lean-toolchain`; the matching Lake manifest is committed alongside it.

For a new researcher, avoid altering the dependency manifest or running `lake update`. That changes the question being reproduced.

## Formal replay against the exact protected proof snapshot

This sequence can be executed against the stated immutable commit **without** requiring the later external-release script:

```bash
git clone https://github.com/grandchallenge/MATH-PROGRAMME.git
cd MATH-PROGRAMME
git checkout --detach 7a0f33588aa8d1add4d941c9b4681b6910644bf1
python3 -m pip install --requirement requirements/policy.txt
python3 ci/formal_validation.py validate
(cd fixtures/formal/CMDG-NAT-CONCORDANCE-001 && lake exe cache get)
python3 ci/formal_validation.py run --lane cmdg-cm4 --mode promotion --changed-paths-json '[]'
python3 ci/formal_validation.py run --lane cmdg-cm4-p3 --mode promotion --changed-paths-json '[]'
```

A convenience script, `ci/replay_cmdg_cm4_external.sh`, is included in the newer external-release branch and will become available on `main` after its protected admission. Run it from that newer checkout as `bash ci/replay_cmdg_cm4_external.sh`. It checks the same **immutable protected theorem and bridge blobs** before invoking the two lanes. Do **not** expect that script to exist when checking out the earlier `7a0f335...` commit.

Both procedures are read-only with respect to protected GitHub state. They use the manifest-pinned mathlib dependency and existing governed compiler with the **promotion-mode** lane configuration. They do not push branches, open PRs, request reviews, or perform GitHub API mutations.

Two phases are compiled:

1. `cmdg-cm4` — terminal wrapper and full local theorem dependency closure.
2. `cmdg-cm4-p3` — the wider P3 family, including the independent global Point-recovery proof now protected via [#1208](https://github.com/grandchallenge/MATH-PROGRAMME/pull/1208).

The exact invocations inside the script are:

```bash
python3 ci/formal_validation.py validate
python3 ci/formal_validation.py run --lane cmdg-cm4 --mode promotion --changed-paths-json '[]'
python3 ci/formal_validation.py run --lane cmdg-cm4-p3 --mode promotion --changed-paths-json '[]'
```

The runner verifies `.lake/packages/mathlib` against both pinned commit and tree and refuses identity drift; its `promotion` mode compiles the closure, not merely recently changed files.

## Evidence and expected outcomes

A successful complete execution creates:

- `.formal-validation/cmdg-cm4/result.json`
- `.formal-validation/cmdg-cm4-p3/result.json`

For each file, check `status == "FORMAL_VALIDATION_SUCCEEDED"` and `mode == "promotion"`. The generated `compiled_local_lean_closure` lists the actual locally compiled proof files. The script prints the list sizes rather than supplying invented counts or timings.

Then independently inspect the theorem's dependencies and axiom readback:

```bash
cd fixtures/formal/CMDG-NAT-CONCORDANCE-001
lake env lean CMDGCondensedCM4Blocker.lean
git -C .lake/packages/mathlib rev-parse HEAD
git -C .lake/packages/mathlib rev-parse HEAD^{tree}
```

The terminal file contains the actual `#check` and `#print axioms` directives. Their recorded foundational output in the protected GCL proof is `[propext, Classical.choice, Quot.sound]`; any `sorryAx`, local axiom, changed proof blob, unexplained dependency, or mismatch between declared and checked theorem is a **stop condition**, not a permissible warning.

If cached dependencies are missing or the registry identities do not match, preserve the exact error and report `REPRODUCTION_BLOCKED`. Never claim successful reproduction from static source inspection alone.

## Negative controls and what not to conclude

A rigorous reviewer should try, in an isolated disposable copy:

- Corrupt a byte of the terminal Lean file. The script's protected source-lock check must fail.
- Point mathlib to a different commit. The formal runner's exact commit/tree check must fail.
- Remove a needed lemma, or inject `sorry` into a local proof. Closure replay or placeholder validation must fail.

These are suggested **adversarial checks**, not evidence that the controls have been exercised by an outside party. None should be performed on the shared protected checkout.

A successful `lake` replay demonstrates formal type checking under its environment. A specialist must additionally verify the correspondence of `CondensedMod.IsSolid` to the mathematical claim and check that the proof is not effectively importing an equivalent target.

## Independent review return format

Please add a substantive analysis to [CM4 external mathematical review #1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222) containing:

- platform, exact repository commit, Lean and mathlib identities;
- the two local replay results and any failures;
- which of the five proof interfaces were examined;
- a precise mathematical finding at a named Lean declaration, ideally a minimal counterexample or correction if there is a gap;
- one of `MATHEMATICALLY_SOUND__UPSTREAM_PORT_JUSTIFIED`, `SOUND_WITH_REQUIRED_CLARIFICATIONS`, `GAP_FOUND`, `TARGET_MISIDENTIFIED`, or `REVIEW_INCONCLUSIVE`.

Review identity must be genuinely independent of proof authorship. An automated replay is welcome as evidence but is **not** by itself independent mathematical adjudication.

## For prospective mathlib contributors

Begin with the [mathematical note](CMDG_CM4_MATHEMATICAL_NOTE.md) and [upstream-readiness assessment](CMDG-CM4-MATHLIB-UPSTREAM-ASSESSMENT.md), and coordinate via [#1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223). Mathlib's present master is **a different dependency target** from this pinned replay. Do not assert an upstream port works until separately rebuilding against master and satisfying contributor policy, reviewability, licensing and public discussion requirements.
