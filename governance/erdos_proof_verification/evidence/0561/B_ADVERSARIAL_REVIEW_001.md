# Erdős #561 — Phase B hostile logical-role review

**Actor:** same authenticated GCL operator `fyremael`, acting in a separate **Adversary/Referee logical pass**; no claim of a distinct human mathematician, external independence or MATHCERT authority. **Reviewed bytes:** exact source-locked ordinary proof, source-to-semantics map and independent finite graph oracle. **Result:** bounded conditional factor-gate PASS, full paper proof **unverified**.

## Mandatory attacks

| Attack | Observation and disposition |
| --- | --- |
| Wrong graph target | The original statement is two-color, two-target, edge-minimal, with disjoint stars, not a one-color or induced subgraph problem. The source special case is one forest with exactly two components; the general `s,t>=3` question is still open |
| Corrupted factor theorem | Source `g=max(0,d-beta)`, `f=alpha>0`; `g=f` exactly when ambient `d=D`; parity is `alpha|C|+e(C,T)` odd, not just `alpha|C|` |
| Overlooked parity | `K3` with `(alpha,beta)=(1,1)` and `K5` with `(1,3)` expose odd regular obstruction; explicit edge assignment and the empty-cut test agree that no partition exists |
| Parity-edge sign | On `K3`, `S={2}, T={1}, Y={0}`, `alpha|C|` odd but `alpha|C|+e(C,T)` even, so the component must NOT contribute to `q_D` |
| Discarding structural hypotheses | `K13` at `(alpha,beta,D)=(3,9,12)` is an actual **counterexample** to bounded-degree-only partition, by odd 3-regular factor parity. It violates the required localization of degree-D vertices to disjoint star centers |
| Counting border of small components | For `1<=m<=D`, `m(D-m+1)-D=(m-1)(D-m)>=0`; all small counted components force boundary >=rD, which contradicts `A<=r-1` |
| Counting border of large components | At least one counted component has >=D+1 vertices; with r counted components the number of degree-D centers is >=D+r. Each center's own H0 leaves are outside Y or else become a degree-D noncenter, contradiction |
| Multiplicities or use of inducedness | H0 star edges are pairwise distinct by the *vertex-disjoint* star hypothesis; summing residual degrees <=2e(R) is valid even when residual edges connect two selected centers |
| Hidden use of strict gap | From alpha>=2, beta>=2(alpha+1)>=6: `D/alpha=1+beta/alpha<beta`. The large-component boundary lower bound exceeds `beta(r-1)` strictly even for `r=1` |
| False universal inference | The conditional proof does NOT derive Claims 3.2–3.8 from the original Ramsey hypotheses. Those earlier reductions and the independently unproved classical Lovász factor theorem are exactly the remaining substantive prerequisites |

## Disposition and limits

**PASS:** reconstructed exact conditional factor specialization and its final contradiction as an ordinary mathematical proof, with independently implemented exhaustive cut/edge-colouring agreement on small graphs, targeted parity counterexamples and reduced-case synthetic constructions. **NOT PROVED:** the paper's Claim 3.10 without its earlier hypotheses, the full two-star forest Theorem 1.2, the original all-star-forest conjecture, the 1978/2002 primary statements, Lean kernel completeness or priority/novelty.

Next gate must replay the earlier counterexample induction and structural Claims 3.2–3.8, including the $n_q=1$ and $k\geq1$ arguments. No claim of external human review is made.
