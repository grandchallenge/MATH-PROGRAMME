# EC-BULK-004 — Erdős #478 independent-stage documentary critical review

Receipt: EC-BULK-004-CRIT-EXCEPTIONS-017  
Observed: 2026-10-14  
Accountable authenticated GitHub identity: fyremael  
Type: separate adversarial editorial checking after article drafting, not independent-person review, independent analysis of the complete published proof, mathematical certification, or V2 admission.

## Source, status and quantifier comparison

- Original Erdős–Graham (1980), printed p. 96, visually inspected at https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=92 . It defines the **SET** of distinct factorial residues $A_p=\{k!\bmod p:1\leq k<p\}$ and asks whether $|A_p|/p\to1-1/e$ through primes. This remains OPEN. Confusing multiset size $p-1$ with set cardinality would trivialize it.
- Primary 2024 published theorem: A. Grebennikov, A. Sagdeev, A. Semchankau and A. Vasilevskii, *Rev. Mat. Iberoam.* 40 (2024) pp. 637–648, https://ems.press/content/serial-article-files/47109 , printed p.638 Theorem 1.1/Corollary 1.2, checked by visual PDF readback: $|A_pA_p|=p-O(p^{13/14}(\log p)^{4/7})$ in the appropriate lower-bound asymptotic interpretation and $|A_p|\ge(\sqrt2-o(1))\sqrt p$. The product-set theorem does NOT prove $|A_p|$ has positive density.
- July 2026 author source https://github.com/hxypqr/factorial-residues-mod-prime : Xiyu Hu claims $|A_p|\gg p^{8/15}$, README blob 922b544d446a9c3558e1e817cf30257e9bd1d579, LaTeX blob b34143edde31eaa1416587e30709e79eac0becb5. The exact proof outline was inspected, including Stevens–de Zeeuw point-line bound, transition count, affine-line multiplicity, and $m^{15/4}$ implication. The author's README explicitly calls the internal Lean work a **partial formalization** with the published external incidence theorem assumed as an input. **No independent complete GCL incidence-theorem proof check, peer review, or Lean kernel replay occurred.** Therefore the $p^{8/15}$ statement remains a claim requiring adjudication, not adopted as established latest bound.
- The maintained #478 page updated 2026-04-12 predates the Hu preprint and retains OPEN status. Regardless of the latter's eventual validity, $p^{8/15}=o(p)$ cannot resolve the proposed $(1-1/e)p$ asymptotic.

## Adversarial arithmetic and logical checks

For any prime p, $A_p/A_p=\mathbb F_p^\times$ because $k!/(k-1)!\equiv k$ for $2\le k<p$ and 1 is included. Hence $|A_p|^2\ge p-1$. Wilson's theorem gives $(p-2)!\equiv1\equiv1!$; this is a collision between **distinct** factorial indices only for $p\ge5$. Thus the commonly repeated inequality $|A_p|\le p-2$ needs that cutoff: it is **false** at $p=2,3$. The manuscript explicitly documents the exceptions.

An exact finite test enumerated all modular factorials, all nonzero quotient classes and the lower/upper boundaries for every prime $p<102$. Particular residue sets for $p=3,5,7,11,13$ were reproduced. The preliminary 2026 transition identity $(n+2)!=(n+1)!+((n+1)!)^2/n!$ and distinct-pair count $p-2$ were independently checked modulo nine small primes. This does **not** check the advanced external incidence-theorem hypothesis; GCL must not mistake a verified elementary lemma for confirmation of the claimed exponent.

Published product-set estimate plus the number of unordered products $\binom{|A|+1}2$ correctly implies the $\sqrt2$ coefficient. The stronger bound $p^{8/15}$ would imply super-square-root growth but not positive density.

## Immutable evidence and QA boundary

- Original issue authenticated return https://github.com/grandchallenge/MATH-PROGRAMME/issues/1748#issuecomment-6167582562 , author fyremael, LF-normalized SHA-256 `7e3050815a5fc9d778968935b9a050a5d05ebbefea75c187e11ccce3bef074a6`, disposition SOURCE_LOCK_READY **for documentary 1980/2024 evidence only**.
- Six-section article `governance/erdos_compendium/editorial/0478.md` stripped UTF-8 SHA-256 `4cf890e2998e6884f900e17afef24218181a6290ed80c71093875965b731cbb4`, raw SHA-256 `d30b7ea45a0841d589cbe170f4a80c4fce046f544614c3c8a746b04ce21a61f7`. All six mandatory H2 headings occur exactly once and mathematical dollar delimiters are balanced.
- Three exact new finite tests in `tests/test_erdos_compendium_0478_factorials.py` PASSED at commit ceca6bdbd7cac199feca4753a2478e8652155083. Full test suite and strict MkDocs MUST be run at register-bearing reviewed head before final declaration.
- No independent human identity, no MathCert, no approved 2026 preprint theorem, no protected production merge, no live-browser rendering, and no V2 editorial admission are represented.

## Editorial outcome

**CRITICAL_DRAFT_PASS_WITH_UNREVIEWED_2026_ASYMPTOTIC_EXCEPTION.** The article is source-faithful for established mathematics and explicitly labels the 2026 proposed exponent as unaudited. The cohort's deterministic 20-item sample and all proof/status/source exceptions remain separate gates. Do not use this editorial review as a formal mathematical certificate or claim that the factorial asymptotic has been settled.
