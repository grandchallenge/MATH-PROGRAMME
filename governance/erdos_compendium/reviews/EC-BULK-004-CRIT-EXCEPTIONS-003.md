# EC-BULK-004 — source-exception draft review 003

Date: 2026-10-13. Scope: Erdős #457 and #459. Role: accountable adversarial documentary QA, performed by the same coordinator and authenticated operator. **Not** an independent human mathematical review. Disposition: local pre-return manuscript QA **PASS WITH EXCEPTIONS**, not issue-return acceptance, protected editorial admission or mathematical certification.

## Evidence custody

| Problem | Original issue | Source evidence | Normalized manuscript SHA-256 |
| --- | --- | --- | --- |
| #457 | [#1727](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1727) | `EC-BULK-004_0457_UNPOSTED_RESULT.md`, SHA-256 `27c68b721d88bcfbbb9c5608aab05d3a0cb08264492ce03240de4dd1fbfefc25` | `67dc59da5c564e0e1709df75419d56a22cbf7896876ca9fb34e7e2090b3f2167` |
| #459 | [#1729](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1729) | `EC-BULK-004_0459_UNPOSTED_RESULT.md`, SHA-256 `69f994a574e26c9bb18774980ccfce06361dbce8a18bb7d3e17e6972dd472d84` | `0966fae1a4acf797f33e4f3b653640a9041e7124eeeaffee9535a1cac637fb30` |

Both issue comment lists were read back with **zero** `RESULT/1` comments. Posting via the authenticated CHAD shell was attempted but the execution transport returned `blocked by OpenAI's safety checks`; no comment was posted. The two staged results are **not** counted as the original 10 authenticated returns. Preserve the originals and never fabricate a return URL or worker identity.

## #457 mathematical and source-direction review

The 1979 Erdős question and 1980 Erdős–Graham question have **opposite** inequality directions. The manuscript explicitly identifies the 1980 infinitely-often lower-bound version as its subject. The 1979 eventual upper-bound formulation cannot be silently treated as the same claim. Both scanned primary texts were source-locked with their hashes in the staged return.

The elementary $2.1$ construction was checked for quantifier scope. For $m$ large, $A=\binom{2m}{m}$ is divisible by every prime $m<p\leq2m$. The number of primes in $(2m,3m]$ is $r\leq3m\log2/\log(2m)$, since each divides $\binom{3m}{m}\leq2^{3m}$. Simultaneous Dirichlet approximation supplies $1\leq k\leq6^r$ and $|kA-\ell_pp|\leq p/6$ for all such primes. With $c=\lfloor0.6m\rfloor$ and $n=kA-c$, Stirling's formula gives $\log n=2m\log2+O(m/\log m)$, hence $K=\lfloor\log n\rfloor>1.2m$ and $2.1\log n<3m$ eventually. All three prime ranges are covered by the positions $1\leq i\leq K$: $p\leq m$ by consecutive-block length, $m<p\leq2m$ by $i=c$, and $2m<p\leq3m$ by $i=c-(kA-\ell_pp)$, which lies between $0.1m+O(1)$ and $1.1m+O(1)$. Since $n\to\infty$, the construction proves infinitely many witnesses. The external Lean file remains **not compiled by GCL**, so this paper proof does not constitute formal certification.

Exact arithmetic fixture: $(n,K,q)=(32,3,13)$ and $(113729,11,59)$; prime-range and binomial divisibility checks passed. These are regression checks, not substitutes for the infinite proof.

## #459 typical-value and status review

The bounds $u+2\leq f(u)\leq u^2$ are exact, with equality at the upper bound for primes and at the lower bound for $u=2^k-2$. Thus a single pointwise asymptotic cannot describe all $u$. The maintained SOLVED status is editorial and does not claim pointwise regularity.

The density-one argument has two independent obligations. (1) For a uniformly random residue class modulo $\prod_{p\leq M}p$, let $X_M$ count distinct prime divisors at most $M$. The CRT makes the Bernoulli indicators independent, so $\mathbb EX_M=\sum_{p\leq M}1/p\to\infty$ and $\mathrm{Var}X_M\leq\mathbb EX_M$. Chebyshev yields $\Pr(X_M\leq1)\leq\mathbb EX_M/(\mathbb EX_M-1)^2\to0$. (2) For distinct primes $p,q$, the irrationality of $\log p/\log q$ gives a finite dense net of residues $a\log p$ modulo $\log q$. Once $\log t$ exceeds the maximum finite $a\log p$, a nonnegative $b$ puts $a\log p+b\log q$ in $(\log t,\log t+\log(1+\varepsilon))$. Since only finitely many pairs $p,q\leq M$ occur, their thresholds can be maximized. Together these prove the quantified density-one statement.

The primary 1980 source and pinned formal provider were read, but the live tracker returned HTTP 403 and the provider's statement-formalized metadata disagrees with the indexed tracker. The external Lean proof was text-inspected, **not** compiled, replayed or axiom-audited by GCL. No external formal claim is promoted to a GCL MathCert.

## QA and remaining gates

- `python3 -m pytest -q ci/test_ec_bulk_004_math_fixtures.py ci/test_erdos_compendium_*.py tests/test_erdos_compendium_0457_prime_block.py tests/test_erdos_compendium_0459_smooth_successor.py`: **63 passed, 5 subtests passed**.
- `mkdocs build --strict --quiet --site-dir /tmp/EC-BULK-004-QA-SITE`: exit code zero; the two generated local HTML pages include the six-heading draft content and Arithmatex markup. This is **not** a live browser check or public deployment.
- Both manuscripts have exactly the six required headings and balanced `$$` delimiters. Any byte change invalidates the manuscript hashes above.
- Required next custody step: authenticate and post one issue-bound `RESULT/1` per source issue, read back exact comment IDs/hashes, then re-review the exception status.
- The fixed deterministic 20-article sample remains incomplete. All 200-article protected production and V2 admission gates remain outstanding.
