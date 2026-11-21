#!/usr/bin/env python3
"""Canonical narrow GCL claims; explicit PARTIAL for unrestricted issue."""
from pathlib import Path
import json
root='research/erdos-561/joint-general/'
common={'mathematical_domain':'Erdős #561 / exact star host Ramsey order / multistar residual Ramsey lower bounds','assumptions':['all target stars have positive integer edge sizes','all host graphs finite and simple','ordinary non-induced and vertex-disjoint forest subgraphs','s,t>=3 unless a more general star-host theorem states otherwise'],'knowledge_graph_refs':['MATH-PROGRAMME#3490','MATH-PROGRAMME#3573','MATH-PROGRAMME#3523'],'promotion_condition':'Do not change full unrestricted joint-residual hypothesis from OPEN/PARTIAL; the constructive full-graph peeling theorem and exact infinite families are paper proofs UNDER_REVIEW, not Lean full graph formalizations. Source-only admission may proceed through ordinary protected CI/queue under delegated GCL policy; public MATHCERT must not follow by inference.'}
claims=[
 dict(common,claim_id='ERDOS561-JOINT-STAR-IFF-001',short_name='Complete coordinatewise characterisation of star-host Ramsey arrowing',claim_text='A disjoint union of stars with sorted component sizes h_i arrows (F(n),F(m)) iff at least s+t-1 nontrivial stars exist and h_i dominates the corresponding antidiagonal max for every i. Consequently the minimum star-host simultaneous joint-residual edge count is exactly J=Σ_{k>=3}w_k for all lengths s,t.',claim_class='PROVED_IN_PACKAGE',status='UNDER_REVIEW',certainty='PROVED_NOT_FORMALIZED',support_type='HUMAN_PROOF',support_summary='Necessity by explicit adversarial split of the first i-1 red and j-1 blue star-components and constrained tail; sufficiency by monotone greedy lattice-path allocation. Complete independent exhaustive check of 7,954 single-pair and 5,917 simultaneous star-host/target tests with all red arm-count colourings.',source_or_artifact=[root+'JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md',root+'verify_star_host_iff.py'],related_files=[root+'README.md',root+'RUN_MATRIX.md']),
 dict(common,claim_id='ERDOS561-JOINT-GENERAL-PEELING-002',short_name='Unconditional two-hub iterative peeling bound for arbitrary simple graph hosts',claim_text='For all s>=3,t>=4, if G simultaneously arrows both joint residual pairs then e(G)>=2*m1+sum(n_i)+(t-4)*n1. If s>=4 also e(G)>=2*n1+sum(m_j)+(s-4)*m1. No star-host assumption. Below the threshold a constructive red/blue colouring defeats one residual relation.',claim_class='PROVED_IN_PACKAGE',status='UNDER_REVIEW',certainty='PROVED_NOT_FORMALIZED',support_type='HUMAN_PROOF',support_summary='Complete direct paper proof: blue edge classes covered by at most t-2 vertices cannot contain t-1 disjoint blue stars; all such deletions force a red full forest and degree≥n1. If a non-v vertex has post-v degree≥m1, peel t-4 fresh red leading-star centres, requiring 2m1+(t-4)n1+sum n edges. Else all blue-dangerous vertices touch v, yielding a one-centre red avoiding-colouring. Test 1,162 explicit arbitrary graph/target cases with independently enumerated star embeddings.',source_or_artifact=[root+'JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md',root+'verify_iterated_peeling.py'],related_files=[root+'exact_arbitrary_host.py',root+'README.md']),
 dict(common,claim_id='ERDOS561-JOINT-EXACT-INF-FAMILY-003',short_name='Exact general-host 3-versus-t family with unbounded switching surplus',claim_text='For t>=4, red n=(a,1,1), blue m=(b,c,1,...,1), a>=c>=1,b>=a+c-1, the exact minimum edge count of a graph simultaneously arrowing the two residual pairs is J=2b+(t-3)a+2. The algebraic switching surplus can be arbitrarily large: t=4,a=2r,b=3r,c=r gives sigma=r.',claim_class='PROVED_IN_PACKAGE',status='UNDER_REVIEW',certainty='PROVED_NOT_FORMALIZED',support_type='HUMAN_PROOF',support_summary='Exact antidiagonal weights b,b,a repeated t-3,1,1; their sum equals the unbounded peeling theorem lower bound. The canonical disjoint-star host attains equality. The surplus identity is independent of any unproved size-Ramsey formula. Recomputed for 6,072 exact finite family examples and 199 growing-r cases.',source_or_artifact=[root+'JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md',root+'verify_unbounded_families.py'],related_files=[root+'UNBOUNDED_FAMILY_PARAMETER_CERTIFICATE.json']),
 dict(common,claim_id='ERDOS561-JOINT-OTHER-FAMILIES-004',short_name='Exact all-spike and all-matching arbitrary-host joint residual families',claim_text='For all s,t>=3, n=(a,1,...,1) and m=(a,1,...,1) with same leading size a>=1, the simultaneous joint residual minimum is (max(s,t)-1)*a+min(s,t)-1. The all-matching family follows as a special case. In addition, every simultaneous host satisfies elementary vertex-cover centre-selection bounds N+Σ first(t-2)m_j and M+Σ first(s-2)n_i.',claim_class='PROVED_IN_PACKAGE',status='UNDER_REVIEW',certainty='PROVED_NOT_FORMALIZED',support_type='HUMAN_PROOF',support_summary='Direct full-graph peeling for max(s,t)>=4; s=t=3 from direct centre-deletion lower bound; canonical star host upper. Independent exact arithmetic tests of 1,944 family instances.',source_or_artifact=[root+'JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md'],related_files=[root+'verify_unbounded_families.py']),
 dict(common,claim_id='ERDOS561-JOINT-RIGID-3X4-006',short_name='Two exact positive-switching 3-versus-4 original joint residual minima',claim_text='For arbitrary finite simple graph hosts, the minimum edge count simultaneously arrowing the two residual relations for (n,m)=((3,2,1),(3,1,1,1)) is 13, and for ((3,1,1),(4,3,1,1)) is 14. In each case the separate residual antidiagonal sums are one smaller than the joint minimum.',claim_class='PROVED_IN_PACKAGE',status='UNDER_REVIEW',certainty='PROVED_NOT_FORMALIZED',support_type='EXACT_RATIONAL_COMPUTATION',support_summary='Universal peeling theorem forces equality-edge hypothetical counterexample into a fixed residual star forest plus two nonadjacent saturated hubs. Two separately implemented COMPLETE finite attachment enumerators agree for the 12-edge instance (9,194 configs, 130 pass necessary constraints, one arrows B and fails A) and the 13-edge instance (31,667 configs, 9,225 with enough vertices, only one arrows A and fails B). Both exhaustive colouring verifiers use ordinary vertex-disjoint star embeddings. This is a complete bounded proof conditional only on the independently demonstrated unbounded peeling lower bound; no full general joint theorem claim.',source_or_artifact=[root+'RIGID_12EDGE_FINITE_THEOREM.md',root+'RIGID_13EDGE_FINITE_THEOREM.md',root+'RIGID_12EDGE_CERTIFICATE.json',root+'RIGID_13EDGE_CERTIFICATE.json'],related_files=[root+'search_rigid_12edge.py',root+'verify_rigid12_independent.py',root+'search_rigid_13edge.py',root+'verify_rigid13_independent.py']),
 dict(common,claim_id='ERDOS561-JOINT-FINITE-CHECKS-005',short_name='Complete bounded exact falsification and constructive verification',claim_text='The package contains exactly 155,737 disjoint-star host/parameter comparisons over 420 parameter pairs, 9,250 simple one-vertex-identification nonstar host tests in a declared 12/13-edge benchmark, 7,954 plus 5,917 full-colouring iff tests, 1,162 verified constructive colourings, and independent finite parameter family checks; no counterexample found in the exact declared domains.',claim_class='PROVED_IN_PACKAGE',status='CHECKED',certainty='CERTIFIED',support_type='EXACT_RATIONAL_COMPUTATION',support_summary='Two independent host-class verification algorithms, full exact 2^E colouring check crossverified against a structural fast matcher on 160 graph instances, explicit vertex-disjoint target embeddings, exact source logs and SHA256 evidence. NO global falsification/proof is asserted by finite testing.',source_or_artifact=[root+'FALSIFICATION_SEARCH_EVIDENCE.json',root+'verify_star_host_iff.py',root+'verify_iterated_peeling.py',root+'verify_fast_vs_full.py'],related_files=[root+'RUN_MATRIX.md',root+'UNBOUNDED_FAMILY_PARAMETER_CERTIFICATE.json']),
 dict(common,**{'knowledge_graph_refs': ['MATH-PROGRAMME#3490',
                            'MATH-PROGRAMME#3573',
                            'MATH-PROGRAMME#3523',
                            'MATH-PROGRAMME#3578'],
   'claim_id': 'ERDOS561-JOINT-RIGID-3X4-007',
   'short_name': 'Exact 15-edge nonuniform joint residual case with general-host finite '
                 'classification',
   'claim_text': 'For all finite simple graphs G, simultaneous arrowing of (red F(2,1), blue '
                 'F(4,1,1,1)) and (red F(3,2,1), blue F(1,1,1)) requires at least 15 edges; the '
                 'canonical star host F(5,4,3,2,1) with 15 edges attains it. This establishes '
                 'J((3,2,1),(4,1,1,1))=15, not the general conjecture.',
   'claim_class': 'PROVED_IN_PACKAGE',
   'status': 'UNDER_REVIEW',
   'certainty': 'PROVED_NOT_FORMALIZED',
   'support_type': 'EXACT_RATIONAL_COMPUTATION',
   'support_summary': 'Self-contained two-centre argument forces any 14-edge hypothetical host to be '
                      'F(3,2,1) plus two nonadjacent degree-four hubs. All 74,553 remaining simple '
                      'attachments independently enumerated by full C++ and Python implementations; '
                      '72,512 fail B via two-vertex deletion; 1,914 fail A by red star; 127 fail A '
                      'by explicit red matching. C++ also independently exhausts all 2^14 '
                      'two-colourings for residual hard cases. Canonical 15-edge upper host verified '
                      'by antidiagonal greedy Ramsey proof. Mathematical source review pending; full '
                      's,t>=3 question remains OPEN/PARTIAL.',
   'source_or_artifact': ['research/erdos-561/joint-general/RIGID_14EDGE_FINITE_THEOREM.md',
                          'research/erdos-561/joint-general/verify_rigid14_exact.cpp',
                          'research/erdos-561/joint-general/verify_rigid14_independent.py',
                          'research/erdos-561/joint-general/RIGID_14EDGE_CERTIFICATE.json'],
   'related_files': ['research/erdos-561/joint-general/RIGID_14EDGE_EVIDENCE.json',
                     'research/erdos-561/joint-general/RUN_MATRIX.md']}),
 dict(common,**{'knowledge_graph_refs': ['MATH-PROGRAMME#3490',
                            'MATH-PROGRAMME#3573',
                            'MATH-PROGRAMME#3523',
                            'MATH-PROGRAMME#3578'],
   'claim_id': 'ERDOS561-JOINT-EQUAL-LEAD-INFINITE-008',
   'short_name': 'Exact infinite 3×4 equal-leading joint residual values and strengthened lower '
                 'bound',
   'claim_text': 'For every a>=4, every finite simple graph simultaneously arrowing residuals for '
                 'red n=(a,2,1) and blue m=(a,1,1,1) has at least 3a+4 edges, and canonical host '
                 'F(a+1,a,a,2,1) attains that bound. For every a>=4 and 2<=b<a, corresponding '
                 'residuals for n=(a,b,1) and m=(a,1,1,1) require at least 3a+b+2 edges. General '
                 'joint residual hypothesis remains OPEN/PARTIAL.',
   'claim_class': 'PROVED_IN_PACKAGE',
   'status': 'UNDER_REVIEW',
   'certainty': 'PROVED_NOT_FORMALIZED',
   'support_type': 'HUMAN_PROOF',
   'support_summary': 'Direct all-host proof: A forces a high-degree vertex; unless another '
                      'high-degree vertex survives deletion of the first, a one-centre red star '
                      'avoids A. B forces F(a,b,1) after every 2-vertex deletion. At equality '
                      '3a+b+1, two nonadjacent degree-a hubs and the exact residual forest are '
                      'forced; deletion of the third saturated centre and one hub shows both hubs '
                      'avoid the small F(b,1); a>=4 ensures only three saturated centres; two-vertex '
                      'deletion forbids any shared neighbour, leaving only three disjoint a-stars '
                      'and F(b,1), which fails A via explicit red matching. Sharp antidiagonal host '
                      'when b=2. Separate C++/Python full finite enumeration of all 84653 a4b2 '
                      'attachments; no full Lean formalization claimed.',
   'source_or_artifact': ['research/erdos-561/joint-general/RIGID_15EDGE_THEOREM.md',
                          'research/erdos-561/joint-general/verify_rigid15_exact.cpp',
                          'research/erdos-561/joint-general/verify_rigid15_structural.py',
                          'research/erdos-561/joint-general/RIGID_15EDGE_STRUCTURAL_CERTIFICATE.json'],
   'related_files': ['research/erdos-561/joint-general/RIGID_15EDGE_EVIDENCE.json',
                     'research/erdos-561/joint-general/RUN_MATRIX.md']}),
 dict(common,**{'knowledge_graph_refs': ['MATH-PROGRAMME#3490',
                            'MATH-PROGRAMME#3573',
                            'MATH-PROGRAMME#3523',
                            'MATH-PROGRAMME#3578'],
   'claim_id': 'ERDOS561-JOINT-RIGID-3X4-009',
   'short_name': 'Exact arbitrary-host 16-edge joint residual for 311 versus 5221',
   'claim_text': 'Every finite simple graph simultaneously arrowing red F(1,1) versus blue '
                 'F(5,2,2,1), and red F(3,1,1) versus blue F(2,2,1), has at least 16 edges. '
                 'Canonical disjoint-star host F(5,5,3,2,1) arrows both. This proves '
                 'J((3,1,1),(5,2,2,1))=16; the unrestricted joint residual hypothesis remains OPEN.',
   'claim_class': 'PROVED_IN_PACKAGE',
   'status': 'UNDER_REVIEW',
   'certainty': 'PROVED_NOT_FORMALIZED',
   'support_type': 'HUMAN_PROOF',
   'support_summary': 'A self-contained rigidity lemma shows any (2K2,H)-arrowing G at '
                      'h+maxdegree(H) edges, for unique maximal star centre degree >=3, is precisely '
                      'H disjoint union K1,d. In the candidate 15-edge case H=F(5,2,2,1), that '
                      'forced graph fails the second residual via explicit colouring; a 16-edge '
                      'disjoint-star host satisfies both by an elementary two-case argument. Full '
                      'finite upper corroboration: 864 arm allocations per residual; lower forced '
                      'host has 648 allocations and nine avoiding the second relation. No '
                      'unrestricted-host enumeration replaces the lower proof.',
   'source_or_artifact': ['research/erdos-561/joint-general/RIGID_15EDGE_311_5221_THEOREM.md',
                          'research/erdos-561/joint-general/verify_rigid15_311_5221.py'],
   'related_files': ['research/erdos-561/joint-general/RIGID_16EDGE_311_5221_EVIDENCE.json',
                     'research/erdos-561/joint-general/RUN_MATRIX.md']}),
 dict(common,**{'knowledge_graph_refs': ['MATH-PROGRAMME#3490',
                            'MATH-PROGRAMME#3573',
                            'MATH-PROGRAMME#3523',
                            'MATH-PROGRAMME#3578'],
   'claim_id': 'ERDOS561-JOINT-PROFILE-MISMATCH-INFINITE-010',
   'short_name': 'Unrestricted graph-host residual-profile mismatch and sharp two-parameter family',
   'claim_text': 'For all s>=3,t>=4 and positive nonincreasing n,m with b=m1 and N=sum(n)=sum(m2,...,mt), '
                 'if F(n) and F(m2,...,mt) are nonisomorphic positive-edge star forests, then every '
                 'finite simple graph simultaneously arrowing both residual pairs has at least 2b+N+1 '
                 'edges. Sharp family: n=(a,1,1), m=(b,a-1,2,1), a>=3,b>=2a-2, has exact joint minimum '
                 'J=2b+a+3 over arbitrary simple hosts. The single n311,m5221 instance was already '
                 'independently established in earlier claim 009 and is not counted as a new discovery.',
   'claim_class': 'PROVED_IN_PACKAGE',
   'status': 'UNDER_REVIEW',
   'certainty': 'PROVED_NOT_FORMALIZED',
   'support_type': 'HUMAN_PROOF',
   'support_summary': 'Self-contained unbounded proof: first Ramsey property forces a maximum degree >=b '
                      'vertex v plus a vertex u of degree >=b after removing v, otherwise explicit '
                      'red-star colouring defeats it. Second Ramsey condition forces G-{u,v} to contain '
                      'full F(n) with N edges, yielding e>=2b+N. At equality both hubs have degree b, are '
                      'nonadjacent, and the residual is exactly F(n). Colouring every edge at u red '
                      'forces all b+N remaining edges of G-u to form precisely F(m) because its edge '
                      'count equals M=b+N. Deleting its other degree-b hub v yields F(m_tail), '
                      'contradicting profile mismatch. Sharp canonical antidiagonal host has weights '
                      '(b,b,a,2,1). Complete 84630 candidate 15-edge profiles independently checked in '
                      'Python and C++ by explicit red-hub colouring, plus independent exact integer '
                      'profile checks. No Lean kernel proof, no global conjecture proof.',
   'source_or_artifact': ['research/erdos-561/joint-general/JOINT_PROFILE_MISMATCH_THEOREM.md',
                          'research/erdos-561/joint-general/verify_profile_mismatch.py',
                          'research/erdos-561/joint-general/PROFILE_MISMATCH_PARAMETER_CERTIFICATE.json'],
   'related_files': ['research/erdos-561/joint-general/verify_profile_mismatch_15edge.py',
                     'research/erdos-561/joint-general/verify_profile_mismatch_cpp.cpp',
                     'research/erdos-561/joint-general/RIGID_15EDGE_MISMATCH_CERTIFICATE.json',
                     'research/erdos-561/joint-general/PROFILE_MISMATCH_EVIDENCE.json',
                     'research/erdos-561/joint-general/RUN_MATRIX.md']}),
]
# Monotone-plateau derivation, dependent on earlier admitted base proofs.
claims.append({
  "mathematical_domain": "Erdős #561 / exact star host Ramsey order / multistar residual Ramsey lower bounds",
  "assumptions": [
    "all target stars have positive integer edge sizes",
    "all host graphs finite and simple",
    "ordinary non-induced and vertex-disjoint forest subgraphs",
    "s,t>=3 unless a more general star-host theorem states otherwise"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3573",
    "MATH-PROGRAMME#3523",
    "MATH-PROGRAMME#3578"
  ],
  "promotion_condition": "Do not change full unrestricted joint-residual hypothesis from OPEN/PARTIAL; the constructive full-graph peeling theorem and exact infinite families are paper proofs UNDER_REVIEW, not Lean full graph formalizations. Source-only admission may proceed through ordinary protected CI/queue under delegated GCL policy; public MATHCERT must not follow by inference.",
  "claim_id": "ERDOS561-JOINT-MONOTONE-PLATEAU-011",
  "short_name": "Monotone antidiagonal plateau closure and inherited exact multistar residual cases",
  "claim_text": "For arbitrary finite simple host graphs, coordinatewise larger red/blue star targets inherit a proved exact joint-residual value H=J whenever their antidiagonal sum J is unchanged. This closes n=(3,2,1),m=(4,c,d,1) for 1<=d<=min(c,2),1<=c<=3 at J=15; n=(3,2,1),m=(3,2,1,1) at J=13; and infinite families n=(a,2,1),m=(a,2,1,1),a>=4, at J=3a+4 and n=(3,1,1),m=(b,3,2,1),b>=5, at J=2b+6. The parent mathematical proofs remain UNDER_REVIEW and the unrestricted joint residual hypothesis remains OPEN/PARTIAL.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Unconditional monotonicity transfer lemma: every larger star forest contains its coordinatewise smaller version, so simultaneous Ramsey arrowing of stronger residual pairs implies arrowing of weaker pairs. As J is coordinatewise nondecreasing and the canonical star-host construction gives H<=J, equality of J along a dominance plateau lifts any established parent H=J. Parent results are the admitted 13-edge, 15-edge rigid cases and two sharp infinite families. Direct explicit antidiagonal algebra proves the listed tail weights; independent source script crosschecks W using two indexings and enumerates nine inherited cases in a declared bounded grid. No new graph enumeration or unrestricted-conjecture proof claimed.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/MONOTONE_PLATEAU_CLOSURE_THEOREM.md",
    "research/erdos-561/joint-general/verify_joint_monotone_plateaus.py",
    "research/erdos-561/joint-general/MONOTONE_PLATEAU_CERTIFICATE.json"
  ],
  "related_files": [
    "research/erdos-561/joint-general/RIGID_12EDGE_FINITE_THEOREM.md",
    "research/erdos-561/joint-general/RIGID_14EDGE_FINITE_THEOREM.md",
    "research/erdos-561/joint-general/RIGID_15EDGE_THEOREM.md",
    "research/erdos-561/joint-general/JOINT_PROFILE_MISMATCH_THEOREM.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / exact star host Ramsey order / multistar residual Ramsey lower bounds",
  "assumptions": [
    "all target stars have positive integer edge sizes",
    "all host graphs finite and simple",
    "ordinary non-induced and vertex-disjoint forest subgraphs",
    "n=(3,2,2),m=(3,1,1,1)"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3578",
    "MATH-PROGRAMME#3591"
  ],
  "promotion_condition": "Full Erdős #561 and unrestricted joint residual issue #3490 stay OPEN/PARTIAL. This is a paper theorem depending on the published ordinary Lovasz (g,f) factor theorem. Protected source-only admission is not mathematical certification. Retain UNDER_REVIEW until substantive independent mathematical adjudication.",
  "claim_id": "ERDOS561-JOINT-322-3111-012",
  "short_name": "Exact 15-edge arbitrary-host 322/3111 joint residual by Lovasz factor and deletion",
  "claim_text": "Every finite simple G satisfying both G->(F(2,2),F(3,1,1,1)) and G->(F(3,2,2),F(1,1,1)) has at least 15 edges, and F(4,4,3,2,2) attains it. Thus J((3,2,2),(3,1,1,1))=15. This solves one strict-switch 3x4 residual case, not the unrestricted conjecture.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Two-vertex deletion forces a ten-vertex full F(3,2,2). A single-vertex deletion forces arrowing (K1,2,F(3,1,1,1)), requiring at least ten edges. The degree-4 case then leaves a ten-edge subcubic residual with <=5 cubic vertices, which the specialized ordinary Lovasz (g,f)-factor matching lemma makes colourable to avoid the residual arrowing. The degree-3 case needs >=8 cubic vertices; handshake plus >=12 nonisolated vertices at 14 edges forces four leaves and a contradiction from deleting a leaf-neighbour and one other vertex. Canonical 15-edge upper forest checked under all 900 arm-colouring classes; no brute-force arbitrary host extrapolation.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/RIGID_14EDGE_322_3111_THEOREM.md",
    "research/erdos-561/joint-general/verify_rigid14_322_3111.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/RIGID_14EDGE_322_3111_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / original two-colour size Ramsey equality, fixed 3-by-4 positive star-forest cases",
  "assumptions": [
    "all host graphs finite and simple",
    "ordinary vertex-disjoint, non-induced positive-edge stars",
    "red F(3,2,2)",
    "blue either F(3,1,1,1) or F(3,2,1,1)"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3569",
    "MATH-PROGRAMME#3591"
  ],
  "promotion_condition": "The new original 20-edge results depend on upstream paper-level claim 012 and elementary even-cap splitting, with no independent mathematical certification. Keep this claim UNDER_REVIEW, and global Erdős #561 OPEN. Protected source-only admission is not MATHCERT.",
  "claim_id": "ERDOS561-ORIGINAL-322-3111-3211-013",
  "short_name": "Two exact original 20-edge size Ramsey values for 322 versus 3111/3211",
  "claim_text": "For c=1,2, rhat(F(3,2,2),F(3,c,1,1))=20 over arbitrary finite simple host graphs. Canonical host F(5,4,4,3,2,2) attains each bound. Any original host with <=19 edges would, by vertex deletion and upstream sharp 15-edge joint residual (claim 012), have maximum degree <=4. The elementary universal (2,2)-capped edge partition then avoids both original forests. No full Erdős #561 conjecture is claimed.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Sharp joint 15-edge residual for blue (3,1,1,1) proved analytically (claim 012), transferred by monotone plateau to blue (3,2,1,1). Original arrowing yields both residual relations after any vertex deletion, bounding degree at most 4 for a 19-edge host. Complete constructive proof that every subquartic graph splits into two degree<=2 colours via two-copy 4-regular multigraph completion, Euler orientation and bipartite cycle alternating. Direct complete 5400 arm allocations for each of the two exact 20-edge canonical hosts corroborate the upper; no arbitrary-host finite extrapolation.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/ORIGINAL_20EDGE_322_3111_3211_THEOREM.md",
    "research/erdos-561/joint-general/verify_original20_322_3111_3211.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/ORIGINAL_20EDGE_322_3111_3211_EVIDENCE.json",
    "research/erdos-561/joint-general/RIGID_14EDGE_322_3111_THEOREM.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / original asymmetric size Ramsey for star forests / sharp-residual transfer",
  "assumptions": [
    "all host graphs finite and simple",
    "ordinary non-induced vertex-disjoint star forest embeddings",
    "source-proved sharp joint residual J for stated target pairs",
    "ordinary Lovasz (g,f) factor theorem classical input"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3564",
    "MATH-PROGRAMME#3578",
    "MATH-PROGRAMME#3587",
    "MATH-PROGRAMME#3591",
    "MATH-PROGRAMME#3600"
  ],
  "promotion_condition": "Unrestricted Erdős #561 and unrestricted joint-residual hypothesis remain OPEN/PARTIAL; paper-level new theorem and infinite-family applications UNDER_REVIEW pending substantive mathematical adjudication. Bounded exact finite certificates may be CHECKED without making independent MATHCERT claims.",
  "claim_id": "ERDOS561-GENERAL-CORE-ORIGINAL-014",
  "short_name": "General core transfer and three parity-free infinite original star-forest families",
  "claim_text": "Given a source-proved sharp joint residual J=W-(n1+m1-1), the original size Ramsey value equals W when both n1,m1 odd, or W<=D(D+1)/2 for any parity, or W<=D(D+1) if at least one n1,m1 odd, or for opposite-parity leading sizes with 2W<2D^2+R. Combined with source-proved joint residuals, exact original all-host parity-free results are: (a,1,1)/(b,c,1,1) for a>=2,1<=c<=a,b>=a+c-1 at 3b+2a+1; (a,2,1)/(a,1,1,1) for a>=4 at 5a+3; (a,1,1)/(b,a-1,2,1) for a>=3,b>=2a-2 at 3b+2a+2; and five (3,2,1)/(4,c,d,1) original cases at 21.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Original vertex deletion forces every G-v to satisfy the two sharp residual relations, hence Delta<=D in any E<=W-1 host. Classical Lovasz degree-core necessity gives >=D+1 saturated vertices for failed cap splits; uniqueness up to 2D+1 saturated vertices forces both caps odd; therefore if at least one cap even failure requires >=2D+2 saturated vertices and E>=D(D+1). Vertex-budget refinement gives 2E>=R+2D^2-2. A (1,2) subcubic matching lemma improves the cubic threshold to nine saturated vertices; isolated odd regular core/exterior avoiding colourings handle b=4,6 and a=4 exceptions; a complete exact 106-class finite degree-two proof handles (211)/(2111). Residual parent results are admitted but still paper-level; full conjecture remains open.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/verify_core_original_transfer.py",
    "research/erdos-561/joint-general/verify_d2_original_211_2111.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md",
    "research/erdos-561/joint-general/CLAIM_LEDGER.json"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / original asymmetric size Ramsey for star forests / sharp-residual transfer",
  "assumptions": [
    "all host graphs finite and simple",
    "ordinary non-induced vertex-disjoint star forest embeddings",
    "source-proved sharp joint residual J for stated target pairs",
    "ordinary Lovasz (g,f) factor theorem classical input"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3564",
    "MATH-PROGRAMME#3578",
    "MATH-PROGRAMME#3587",
    "MATH-PROGRAMME#3591",
    "MATH-PROGRAMME#3600"
  ],
  "promotion_condition": "Unrestricted Erdős #561 and unrestricted joint-residual hypothesis remain OPEN/PARTIAL; paper-level new theorem and infinite-family applications UNDER_REVIEW pending substantive mathematical adjudication. Bounded exact finite certificates may be CHECKED without making independent MATHCERT claims.",
  "claim_id": "ERDOS561-D2-211-2111-015",
  "short_name": "Complete 106-class ten-edge max-degree-two original Ramsey avoidance certificate",
  "claim_text": "Every finite simple maximum-degree-two graph with exactly ten edges admits a red/blue edge-colouring avoiding red F(2,1,1) and blue F(2,1,1,1). Up to isolates, exactly 106 canonical path/cycle component multisets exist. All 108544 colourings were compared between two independent exact ordinary vertex-disjoint subgraph oracles, with at least one avoiding colouring for each class. The complete finite result, combined with upstream sharp residual J=8 and degree bound Delta<=2, proves the single original 11-edge size Ramsey lower bound, without classifying arbitrary general-degree hosts by sampling.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Source generator enumerates partitions of ten into positive edge-size path components and cycle components of length >=3, canonicalized to 106 isomorphism-type multisets; both an explicit red two-edge-star plus disjoint matching search and a fully separate generic noninduced star-forest edge-mask embedding enumeration/upward DP agree for all 106*1024 colourings. Every type has a constructed avoiding red bitmask, with 106-witness JSON digest SHA256 2840d4d0a16690272b3052a33e21d8b487ce717e982879899735af3577680aaf; no external mathematical attestation. The universal degree reduction is separately paper-level UNDER_REVIEW.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_d2_original_211_2111.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / sharp unrestricted-host joint residual and original size Ramsey for nonuniform star forests",
  "assumptions": [
    "finite simple arbitrary host graphs; ordinary non-induced and vertex-disjoint positive star forests",
    "c>=1, b>=c+1, original n=(2,1,1),m=(b,c,c,c)",
    "published ordinary graph-factor results only through source-locked prior GCL structural lemmas"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3585",
    "MATH-PROGRAMME#3578",
    "MATH-PROGRAMME#3606"
  ],
  "promotion_condition": "Do not promote full joint residual or unrestricted Erdős #561. Paper theorem inherits under-review source lemma; only deterministic bounded arithmetic and star-host scans CHECKED. Source admission is not mathematical certification.",
  "claim_id": "ERDOS561-JOINT-FLAT-TAIL-RIGIDITY-016",
  "short_name": "Exact all-host 211 versus (b,c,c,c) joint residual and unbounded +1 switching surplus",
  "claim_text": "For every c>=1 and b>=c+1 the exact minimum edges for simultaneous arrowing (F(1,1),F(b,c,c,c)) and (F(2,1,1),F(c,c,c)) equals J=2b+3c+1 over arbitrary finite simple graphs. For b>=3, sharp single-matching Ramsey equality rigidity forces every hypothetical J-1 host to be F(b,b,c,c,c), defeated in the second relation by colouring one arm of each c-star red; b=2,c=1 is already covered by the peeling theorem. Canonical host F(b,b,c+1,c,c) attains J. Switching surplus is exactly one for b>=c+2. Moreover the ORIGINAL size Ramsey number rhat(F(2,1,1),F(b,c,c,c)) equals W=3b+3c+2 for ALL c>=1,b>=c+1 regardless of parity. The odd b result follows from core transfer or the nine-cubic matching lemma; even b>=6 from isolated regular core versus blue forest edge budget, b=4 from explicit u=5/7 core exclusions, b=2 from the prior 106-class exact certificate. General conjecture OPEN.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Unrestricted host first residual (2K2,H) with H unique maximal b-star implies e>=h+b; equality forces H disjoint union K1,b by a source-proved rigidity theorem. A red matching on the c-star components defeats the second residual relation, yielding exact J=h+b+1. Original vertex deletion forces Delta<=b at E<W. Odd b handled by source-proved core transfer or nine-cubic matching lemma. Even b cap obstruction must have isolated odd-order b-regular C, u>=b+1; all-blue forest H with M=b+3c edges uses at most u-1 internal forest edges, so E>=M+u(b/2-1)+1 >W-1 for b>=6. At b=4 only u=5/7 and explicit avoiding colourings or impossibility of all-blue H eliminate them. At b=2,c=1 the complete 106-class earlier certificate applies. Finite 360-pair verifier is corroborating arithmetic, not unbounded proof.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/FLAT_TAIL_SINGLE_MATCHING_RIGIDITY_THEOREM.md",
    "research/erdos-561/joint-general/verify_flat_tail_rigidity_family.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FLAT_TAIL_RIGIDITY_EVIDENCE.json",
    "research/erdos-561/joint-general/RIGID_15EDGE_311_5221_THEOREM.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / sharp unrestricted-host joint residual and original size Ramsey for nonuniform star forests",
  "assumptions": [
    "finite simple arbitrary host graphs; ordinary non-induced and vertex-disjoint positive star forests",
    "c>=1, b>=c+1, original n=(2,1,1),m=(b,c,c,c)",
    "published ordinary graph-factor results only through source-locked prior GCL structural lemmas"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3585",
    "MATH-PROGRAMME#3578",
    "MATH-PROGRAMME#3606"
  ],
  "promotion_condition": "Do not promote full joint residual or unrestricted Erdős #561. Paper theorem inherits under-review source lemma; only deterministic bounded arithmetic and star-host scans CHECKED. Source admission is not mathematical certification.",
  "claim_id": "ERDOS561-JOINT-FLAT-TAIL-CHECK-017",
  "short_name": "Exact flat-tail antidiagonal and complete star-arm corroboration",
  "claim_text": "The deterministic parameter verifier proves exact finite arithmetic for 360 admissible flat-tail pairs (345 with +1 switching surplus and 15 without) and exhausts 233018 red-arm allocation classes on forced lower R1 star hosts plus 271548 red-arm allocation classes on canonical upper joint hosts, all matching the proved claims in their declared classes. It is not an unrestricted-host finite enumeration or certification of the analytic rigidity lemma.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Two distinct index conventions for antidiagonal maxima; exact arm allocation conditions are necessary and sufficient for disjoint-star hosts. Source script checks entire declared finite rectangle and records zero mismatches, with no random seeds or network access.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_flat_tail_rigidity_family.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FLAT_TAIL_RIGIDITY_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary finite simple host joint residual and flat-tail star-forest Ramsey",
  "assumptions": [
    "t>=4,a>=2,b>=c>=1, original n=(a,1,1),m=(b,c repeated t-1)",
    "ordinary non-induced, vertex-disjoint positive star-forest embeddings",
    "first residual arrowing relation G->(F(1,1),F(b,c^{t-1})), second G->(F(a,1,1),F(c^{t-1}))"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3609",
    "MATH-PROGRAMME#3606"
  ],
  "promotion_condition": "New all-host theorem paper-level UNDER_REVIEW. Finite complete star-arm-colouring checks and bounded arithmetic CHECKED only; no MATHCERT or unrestricted Erdős #561 closure.",
  "claim_id": "ERDOS561-MULTIARM-FLAT-TAIL-JOINT-018",
  "short_name": "Sharp multi-arm recolouring budget gives exact flat-tail joint residual for all t",
  "claim_text": "For t>=4,a>=2,b>=c>=1, every arbitrary finite simple joint residual host for n=(a,1,1),m=(b,c^{t-1}) has at least 2b+(t-1)c+(t-3)min(a-1,c) edges. When c>=a-1 and b>=a+c-1 this exactly equals the canonical antidiagonal host J=2b+(t-3)(a+c-1)+2c. In particular the formerly one-edge-open t=5,a=2 family has J=2b+4c+2 for all c>=1,b>=c+1. The general conjecture remains unresolved.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "R1 all-blue forces degree>=b vertex v, and red v-star forces H=F(b,c^{t-1}) in G-v, with q=e(G-v)-h extra edges. Colour r=min(a-1,c) arms in each secondary c-star red and all other edges blue. Red maximum degree r<a avoids original red n. A blue F(c^{t-1}) can use v in at most one star and primary b-star edges in at most one more. At least t-3 remaining vertex-disjoint c-stars each need r distinct extra edges since residual secondary base degree<=c-r. Thus q>=r(t-3), proving lower. The exact antidiagonal lists A=(b,b,c^{t-1}),B=((a+c-1)^{t-1},c,c) and b>=a+c-1 give canonical upper equality. Does not rely on universal joint conjecture or finite-host enumeration.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/FLAT_TAIL_MULTIARM_RECOLOURING_THEOREM.md",
    "research/erdos-561/joint-general/verify_flat_tail_multiarm.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FLAT_TAIL_MULTIARM_EVIDENCE.json",
    "research/erdos-561/joint-general/JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary finite simple host joint residual and flat-tail star-forest Ramsey",
  "assumptions": [
    "t>=4,a>=2,b>=c>=1, original n=(a,1,1),m=(b,c repeated t-1)",
    "ordinary non-induced, vertex-disjoint positive star-forest embeddings",
    "first residual arrowing relation G->(F(1,1),F(b,c^{t-1})), second G->(F(a,1,1),F(c^{t-1}))"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3609",
    "MATH-PROGRAMME#3606"
  ],
  "promotion_condition": "New all-host theorem paper-level UNDER_REVIEW. Finite complete star-arm-colouring checks and bounded arithmetic CHECKED only; no MATHCERT or unrestricted Erdős #561 closure.",
  "claim_id": "ERDOS561-MULTIARM-FLAT-TAIL-CHECK-019",
  "short_name": "Multi-arm antidiagonal arithmetic and complete small upper-host colouring audit",
  "claim_text": "Independent zero/one-based index conventions confirm 2772 exact flat-tail family parameter cases and 1890 general lower-only pairs. Seven declared canonical star hosts have been checked across every one of their 177482 red-arm colour allocation classes, each arrowing both residual pairs. These finite checks corroborate the analytic theorem but do not establish the universal arbitrary-host result by sampling.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Standard-library deterministic verifier independently recomputes original and two residual antidiagonal arrays, exact lower and upper formulas and full colour allocation classes of seven finite star-forest hosts. All finite tests are complete within their explicitly enumerated classes; unrestricted host lower is proven separately by the combinatorial recolouring argument.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_flat_tail_multiarm.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FLAT_TAIL_MULTIARM_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary-host joint residual / nonuniform blue star tails",
  "assumptions": [
    "a>=2,k>=3,b>=c1>=...>=ck>=1; original n=(a,1,1),m=(b,c1,...,ck)",
    "ordinary non-induced vertex-disjoint star-forest embeddings in arbitrary finite simple graphs",
    "exact regime b>=a+c1-1, c_(k-2)>=a-1"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3615"
  ],
  "promotion_condition": "New unbounded theorem UNDER_REVIEW; deterministic finite nonuniform star-host checks CHECKED only. Full joint-residual conjecture OPEN/PARTIAL and no MATHCERT certification.",
  "claim_id": "ERDOS561-VARIABLE-TAIL-ORDERED-DEFICIT-020",
  "short_name": "Exact unrestricted-host joint residual for unequal blue tails via ordered deficits",
  "claim_text": "For every a>=2,k>=3,b>=c1>=...>=ck>=1, let d_i=max(0,c_i-a+1). Every arbitrary finite simple graph jointly arrowing the two residuals of n=(a,1,1),m=(b,c1,...,ck) has at least 2b+sum_i c_i+sum_{i=1}^{k-2}max(0,c_{i+2}-d_i) edges. If b>=a+c1-1 and c_{k-2}>=a-1, this lower equals the canonical joint antidiagonal host edge sum; the star-size host is (b,b,max(c1,a+c3-1),...,max(c_{k-2},a+ck-1),c_{k-1},ck). In particular J((4,1,1),(8,5,4,3,2,1))=34. This is an all-finite-simple-host exact theorem in the stated family, not unrestricted #561.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "All-blue first residual supplies vertex v degree>=b, red star at v forces H=F(b,c1,...,ck) inside G-v. Colour min(a-1,c_i) arms in each secondary H star red, avoiding F(a,1,1). Any blue F(c1,...,ck) has k-2 stars avoiding v and edges of primary b-star. Each uses H secondary base edges in at most one component; distinct selected target stars using H secondary edges belong to distinct secondary components since all host-star edges meet at the same centre. Injectively assign no-base stars to unused components, and count distinct extra edges at least (p-d_j)_+. Monge rearrangement sorted demand-capacity injection plus order statistics p_i>=c_{i+2} gives exact deficit lower L. Under c_(k-2)>=a-1, d_i=c_i-a+1 for i<=k-2 and matches the independently derived residual antidiagonal max when b>=a+c1-1. No reliance on full conjecture or finite graph enumeration.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/VARIABLE_TAIL_ORDERED_DEFICIT_THEOREM.md",
    "research/erdos-561/joint-general/verify_variable_tail_deficit.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/VARIABLE_TAIL_DEFICIT_EVIDENCE.json",
    "research/erdos-561/joint-general/FLAT_TAIL_MULTIARM_RECOLOURING_THEOREM.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary-host joint residual / nonuniform blue star tails",
  "assumptions": [
    "a>=2,k>=3,b>=c1>=...>=ck>=1; original n=(a,1,1),m=(b,c1,...,ck)",
    "ordinary non-induced vertex-disjoint star-forest embeddings in arbitrary finite simple graphs",
    "exact regime b>=a+c1-1, c_(k-2)>=a-1"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3615"
  ],
  "promotion_condition": "New unbounded theorem UNDER_REVIEW; deterministic finite nonuniform star-host checks CHECKED only. Full joint-residual conjecture OPEN/PARTIAL and no MATHCERT certification.",
  "claim_id": "ERDOS561-VARIABLE-TAIL-CHECK-021",
  "short_name": "Exact nonuniform antidiagonal grid and complete six-host red-arm colour audit",
  "claim_text": "Two distinct antidiagonal index conventions agree over 24500 exact variable-tail and 19305 lower-only parameter cases, and six concrete nonuniform canonical joint star hosts satisfy both residual arrowing properties for all 147188 individual red-arm allocations. These declared finite checks are complete in their classes but do not certify the unbounded all-host paper theorem by extrapolation.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Standard-library deterministic bounded parameter generator; independent zero- and one-index antidiagonal routines; exact complete red-arm allocation enumeration on six grounded nonuniform star forests. Source script and retained evidence record pass.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_variable_tail_deficit.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/VARIABLE_TAIL_DEFICIT_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / matching versus arbitrary star forests joint residual",
  "assumptions": [
    "s,t>=3,s-1<=t",
    "red original n=(1 repeated s), blue original m1>=...>=mt positive",
    "ordinary non-induced, vertex-disjoint star-forest embeddings; arbitrary finite simple graph hosts"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3617"
  ],
  "promotion_condition": "New unrestricted-host restricted theorem UNDER_REVIEW. Finite standard-library verifier CHECKED. Full all-profiles joint-residual conjecture and original Erdős #561 remain OPEN/PARTIAL; not MATHCERT.",
  "claim_id": "ERDOS561-SATURATED-MATCHING-022",
  "short_name": "Exact all-host matching versus arbitrary-tail star forest with saturated largest tier",
  "claim_text": "For s,t>=3,s-1<=t, original red matching n=(1^s) and arbitrary sorted positive blue m=(m1,...,mt) satisfy universal joint residual lower J>=m1+sum(m)+sum_{j=3}^{s-1}m_j. If the first s-1 blue star sizes are equal b=m1, the exact arbitrary-host minimum is J=(2s-3)b+sum_{j=s}^t m_j, attained by canonical U=F(b^(2s-3),m_s,...,m_t), with completely nonuniform remaining blue tail. The unrestricted conjecture remains open.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "All-blue R1 gives vertex v degree>=m1. Red colour on v-star forces full H=F(m) in G-v. Colour the s-1 largest H components entirely red and all other edges blue. Red matching number<=s-1 avoids red original F(1^s), so R2 forces blue F(m2..mt) with M-m1 edges. At most one blue target star uses v and it has <=m2 edges; >=M-m1-m2 target edges therefore outside v. Available blue edges outside v are exactly q extra edges plus M-sum_{j=1}^{s-1}m_j edges from untouched H tail. This yields q>=sum_{j=3}^{s-1}m_j and e>=m1+M+q. When m1..m_{s-1}=b the bound matches the exact canonical antidiagonal list (b repeated s-1, m2..mt), proving all-host sharpness. No bounded graph search or unproved general hypothesis in proof.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/SATURATED_MATCHING_JOINT_THEOREM.md",
    "research/erdos-561/joint-general/verify_saturated_matching_joint.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/SATURATED_MATCHING_JOINT_EVIDENCE.json",
    "research/erdos-561/joint-general/JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / matching versus arbitrary star forests joint residual",
  "assumptions": [
    "s,t>=3,s-1<=t",
    "red original n=(1 repeated s), blue original m1>=...>=mt positive",
    "ordinary non-induced, vertex-disjoint star-forest embeddings; arbitrary finite simple graph hosts"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3617"
  ],
  "promotion_condition": "New unrestricted-host restricted theorem UNDER_REVIEW. Finite standard-library verifier CHECKED. Full all-profiles joint-residual conjecture and original Erdős #561 remain OPEN/PARTIAL; not MATHCERT.",
  "claim_id": "ERDOS561-SATURATED-MATCHING-CHECK-023",
  "short_name": "Matching-star saturated-prefix exact parameter and complete upper-host arm colouring tests",
  "claim_text": "Two independent antidiagonal indexing conventions and exact matching lower calculations agree across 14203 general parameter profiles, with 3385 satisfying the saturated-maximal-prefix exact family and 4651 general lower-bound equalities. Seven fixed canonical star hosts satisfy both residual arrowing properties for every one of 116386 complete red-arm allocations. Finite checks do not establish all-host theorem by extrapolation. The same finite checker also exhaustively verifies the original upper host for three saturated matching examples across 14742 full red-arm allocations, without extrapolating finite cases to unbounded arbitrary hosts.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Standard-library deterministic parameter enumeration over 3<=s<=7, max(3,s-1)<=t<=8 and positive stars<=6; independent zero-/one-index original and residual antidiagonal arrays plus exact lower arithmetic; seven canonical star forests exhaust every full-arm red/blue allocation. Exact source and evidence JSON under joint-general. Three explicit original canonical star hosts are also exhaustively checked for all 14742 arm allocations.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_saturated_matching_joint.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/SATURATED_MATCHING_JOINT_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / matching versus arbitrary star forests joint residual",
  "assumptions": [
    "s,t>=3,s-1<=t",
    "red original n=(1 repeated s), blue original m1>=...>=mt positive",
    "ordinary non-induced, vertex-disjoint star-forest embeddings; arbitrary finite simple graph hosts"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3617"
  ],
  "promotion_condition": "General matching-leading transfer is valid under individually proved sharp residual. Claim 024 and its saturated matching original corollary remain paper-level UNDER_REVIEW; not independent MATHCERT certification. Original unrestricted Erdős #561 stays OPEN/PARTIAL.",
  "claim_id": "ERDOS561-MATCHING-ORIGINAL-TRANSFER-024",
  "short_name": "General matching-leading sharp-residual-to-original transfer and exact saturated matching original family",
  "claim_text": "For any nonincreasing positive star lists n,m with lengths s,t>=3, if the individual sharp joint residual J=W-(n1+m1-1) has been proved and either n1=1 or m1=1, then the unrestricted-host ORIGINAL size Ramsey value equals W. Any hypothetically smaller original-arrowing G would have every vertex deletion satisfying both residuals, hence degree Delta(G)<=n1+m1-2; if n1=1 all-blue forces Delta(G)>=m1, contradiction, and if m1=1 all-red forces Delta(G)>=n1, contradiction. Applying to claim 022 yields exact original rhat(F(1^s),F(b^(s-1),c1,...,cL))=(2s-2)b+sum ci for all s>=3, t=s-1+L>=3 and arbitrary b>=c1>=...>=cL>=1. This is a theorem conditional on individually proved residual bounds, not on the unresolved general residual conjecture.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Any original host G gives both vertex-deletion residual arrows in G-v, since extending any avoiding residual colouring with red or blue v-star yields an original avoiding colouring; if an original target copy used v, discarding its one v-containing component leaves all other s-1 or t-1 components coordinatewise dominating the respective deleted-largest profile. Sharp J therefore forces d(v)<=W-1-J=n1+m1-2 in a hypothetical E<W host. For a matching on either side, all-monochromatic colouring forces a larger leading star than that degree bound, impossible. Combining with claim 022 exact J from elementary matching edge-charge yields the stated original formula. Finite original canonical hosts are checked as corroboration, not the unrestricted-host lower proof.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/SATURATED_MATCHING_JOINT_THEOREM.md",
    "research/erdos-561/joint-general/verify_saturated_matching_joint.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/SATURATED_MATCHING_JOINT_EVIDENCE.json",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
Path('CLAIM_LEDGER.json').write_text(json.dumps({'schema_version':'1.1.0','ledger_contract':'canonical_claim_ledger','ledger_id':'ERDOS561-JOINT-GENERAL-20261119','claims':claims},indent=2,ensure_ascii=False)+'\n')
print('CANONICAL_CLAIMS',len(claims))
