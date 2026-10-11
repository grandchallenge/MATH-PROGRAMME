# Erdős-024 Colab logical-review adapter

**Status:** candidate implementation behind the protected AI runtime hold; an actual authenticated Colab session is not yet verified. The intended deliverable is Forge preparatory evidence only, not mathematical certification or formal publication.

This adapter reuses the GSD/QTR Colab control protocol: host allocates a runtime, uploads immutable research inputs, executes, downloads verified receipts, and stops the runtime. The GSD/QTR launchers are campaign-specific, so the bounded Erdős implementation comprises two standalone modules:

- ci/erdos_colab_host_runner.py: GitHub queue/source guards and Colab session lifecycle
- colab/erdos_024_remote_review.py: exact input verification, deterministic mathematical checks, optional model assessments and SHA-256 receipt

## Governance

The effective GI-STEWARD-0003 permits one model, session, and GitHub authentication to staff multiple non-reserved roles. Our work uses two separate logical passes, VERIFIER and ADVERSARY, both in non_authoring_read_only mode, with different logical_pass_id values and the same explicitly identified model. Source inputs are treated as untrusted research material rather than commands. Neither pass may change the candidate, announce an accepted theorem, or claim MATHCERT authority. More stringent domain-specific independence gates remain for certified or externally published mathematical results and expressly reserved changes.

The protected cohort is ERDOS-ROLLING-024-001 and this pilot is bound ONLY to Erdős #41 issue #2536, original RESULT/1 comment #6104193801 and its SHA-256, plus the immutable provider Lean source blob. Preparation reuses the existing protected Forge source builder.

## Use on a connected WSL/Linux Colab control host

Preflight: authenticate to GitHub on the host via the existing supported gh operator and to Google Colab via google-colab-cli OAuth. Do not place GitHub tokens or OAuth credentials in remote payloads. The host never uploads them to Colab. The QTR original CLI pin was 0.6.0 while GSD observed 0.7.4; verify version compatibility instead of assuming.

Offline preparation with no Colab allocation:

    python -m ci.erdos_colab_host_runner --backend witness_only --accelerator CPU

Live CPU mathematical witness test (does NOT execute an AI model):

    python -m ci.erdos_colab_host_runner --backend witness_only --accelerator CPU --execute

After protected runtime governance approval, run a local AI model with an explicitly selected accessible model repository and exact immutable 40-digit revision:

    python -m ci.erdos_colab_host_runner --backend local_transformers --accelerator L4 --model-id ORG/MODEL --model-revision EXACT_40_HEX_GIT_SHA --execute

The last line shows parameter syntax; ORG/MODEL and EXACT_40_HEX_GIT_SHA are placeholders, not validated model identities. Colab needs compatible installed PyTorch/transformers packages and GPU availability. A missing or unpinned model, unavailable accelerator, unauthorized service, malformed response or failed download must return an explicit blocked or RED state, never a generated approval.

## Research and evidence contract

A finite test verifies that the set {1,2,3} has exactly one 3-element subset, while the different multisets (1,1,3) and (1,2,2) both sum to 5. This establishes only non-equivalence of the two *finite predicates*. It neither settles the historical repetition convention nor the infinite Erdős problem.

- witness_only: deterministic mathematics and receipt; role_passes is empty, never represented as an AI review
- local_transformers: two genuine role-specific model calls, same model identity, different exact-subject logical-pass identifiers, substantive role findings and zero authority effects
- host readback: verifies all input hashes, model/reviewer fields, witness, result/receipt digest, role count and lack of certification/publication authority
- GCL research state: source candidacy only; no automatic Forge acceptance, Solve claim, Cert or external publication
- terminal report: RUN_STATUS.json history including RED on failure; raw Colab CLI output not retained, only its digest and byte count

The host defaults to **not posting anything**. After an actual two-pass local-model Colab execution and full receipt verification, an explicit --publish-provisional flag may post a GCL-FORGE-CRITIQUE-CANDIDATE/1 comment using the **same already authenticated host GitHub account**. This comment is an internal, unadjudicated research-evidence receipt, not formal publication of a proved mathematical result or an independent GitHub PR approval. The publisher rechecks live issue state, issue fields, original RESULT/1 custody, prior critical dispositions, model-output roles and receipt digests. Witness-only runs cannot post review evidence. Colab has no GitHub token. The host saves a local .attempted-<job SHA-256> ticket before allocating a session, suppressing duplicate spending for the same input on that host even after RED; this is a **host-local lock**, not a distributed lease. No unattended cross-host scheduler has been admitted.

An explicitly authorized model command with provisional evidence submission appends --publish-provisional. Do not use that flag to report test-only synthetic reviews as production findings. The protected Programme workflow for Copilot remains disabled by #2541. No protected changes to ordinary GitHub policy, source-semantic acceptance, Solve authority or MATHCERT result follow from an internal issue comment.

## Tests and status

The exact Colab contract test suite is tests/test_erdos_colab_review.py, wired into the existing Erdős source intake CI. Hostile checks include changed source digests, malformed model/reviewer output, impersonated certification, model revision drift, result-receipt forgery, missing queue fields and dry-run no-allocation.

A successful protected CI run verifies **code and offline custody**, not a live Colab allocation or model result. A live end-to-end verification still requires an authenticated connected host, an available pinned model and downloaded verified receipts. See INTELLECT #118 and PR #119 for control review, and Programme issue #2536 for the actual mathematical return.
