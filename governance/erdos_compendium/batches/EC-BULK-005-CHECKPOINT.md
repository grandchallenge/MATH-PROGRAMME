# EC-BULK-005 — authenticated production checkpoint (2026-10-13)

**Authority:** source/comment audit and unaccepted manuscript preparation ONLY. Nothing in this checkpoint authorizes a protected merge, mathematical claim certification, or V2 editorial admission.

## Exact scope and provenance

- Problems: 652–851 inclusive; 200 unique canonical registry entries.
- Registry Git blob: `90f6499cfbaca8c8a9e1ac4c6beb468ca09127a5`.
- Original issue mappings read individually from the registry; 1923–2122 in this cohort.
- Production branch: `editorial/ec-bulk-005-200`.
- Baseline protected main head: `10fd41c8ab7af25a4d498da8649faa8b2ffa210d`.
- No overlap with previously accepted editorial admission rows at baseline.
- Separate [preflight JSON](EC-BULK-005-PREFLIGHT.json): all 200 issues open, with expected source-audit/available labels, no assignees, and exact registry issue body SHA-256 matches; zero exceptions. Project saved Editorial, Mathematics, Available views independently verified; global queue class audit indicated zero changes necessary. Individual Project State on every item was **not** separately read back.

## Exact progress counts at checkpoint

| Distinct metric | Verified count |
| --- | ---: |
| Registry intake IDs | 200 |
| Original issue comment threads reconciled | 200 |
| Authenticated RESULT/1 returns | 2 |
| Source return without GCL source-lock completion | 2 |
| Source returns still absent | 198 |
| Substantive manuscript drafts | 2 |
| Fully source-qualified manuscripts | 0 |
| Accountable batch critical-review sample completed | 0 of 20 selected |
| Protected production merges | 0 |
| Cohort public mathematical-rendering checks | 0 |
| Cohort V2 editorial admissions | 0 |

- [#652 source return](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1923#issuecomment-6141669045): PARTIAL. Mathialagan's published 2021 Theorem 14 and Elekes' construction provide the known sharp order `alpha_k = Theta(sqrt(k))` in the maintained formulation. The correct Er97e bibliography is P. Erdős, *Some of my favourite unsolved problems*, *Math. Japon.* (1997), 527–537; exact historical primary paragraph uninspected. [Unaccepted manuscript](../editorial/0652.md).
- [#653 source return](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1924#issuecomment-6141940643): STATUS_CONFLICT. Maintained catalogue OPEN versus external Conjectures.io proof certified 17 September 2026. GCL did **not** replay the external Lean file or verify its task-bundle dependencies. [Unaccepted manuscript](../editorial/0653.md).

## Local validation

- Both manuscript files pass `ci/math_markdown_gate.py --file` after corrections for supported mathematical delimiters and prose adjacency.
- `python3 -m pytest -q ci/test_erdos_compendium_publication_gate.py ci/test_erdos_compendium_editorial_replay.py`: 22 tests passed.
- `mkdocs build --strict`: success (documentation built in approximately 27 s). This is a **local static build**, not a public browser-based mathematical-rendering readback.
- The site generator reports existing global catalogue coverage of 1,221 references; it must not count this cohort's 2 unaccepted manuscripts as reviewed editorial admissions.

## Verified execution capacity and blockers

- CHAD operator authenticated to GitHub as `fyremael`.
- CLI `codex 0.146.1` authenticated, but a single bounded read-only canary for assignment #653 was rejected by the Codex quota check *before work began*. It produced **no** research return. **No 12–16-way external worker execution capacity is currently verified.**
- The two source returns listed above were directly produced and posted by the authenticated coordinator, **not** by a successful Codex worker.
- #652: original Er97e survey primary-source question/page uninspected.
- #653: external certified proof conflicts with maintained OPEN status; exact Lean task/environment replay, axioms and source semantics await independent mathematical review. GCL must not treat the external certificate as its own proof.
- 198 additional source audits and their manuscript/review work remain undone; absence is not an implicit acceptance.

## Resume rule and admission boundary

On resumption first revalidate main, the branch and registry, then re-run the live 200-thread authenticated reconciler into a **new** proposed JSON and preserve existing source-comment links. Resume no more than verified worker capacity permits; do not invent concurrent jobs. Complete sources and manuscripts before the minimum 20-item critical sample plus all exception audits. Only after all 200 are source-qualified and pass editorial QA may **one consolidated protected production PR** be prepared. After exact-head protected merge, verify public MkDocs and real-browser MathJax, then make **one separate protected V2 batch admission PR** with all normalized manuscript SHA-256 values. Never infer mathematical certification from either editorial merge.
