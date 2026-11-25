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
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary-host universal vertex-cover peeling and matching-side exact solution",
  "assumptions": [
    "s,t>=3; positive nonincreasing star lists n and m",
    "finite simple host graphs, ordinary non-induced vertex-disjoint star forest embeddings",
    "matching exact specialization: n=(1 repeated s), blue m completely arbitrary"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3618"
  ],
  "promotion_condition": "Paper theorem UNDER_REVIEW; numerical checker CHECKED only after exact-head replay. No full nonmatching/nonmatching theorem, no MATHCERT certification.",
  "claim_id": "ERDOS561-UNIVERSAL-MATCHING-PEELING-025",
  "short_name": "Universal vertex-cover deletion lower and exact matching-side joint and original Ramsey formulas",
  "claim_text": "For arbitrary positive nonincreasing original lists n,m of lengths s,t>=3, any joint residual host Q has e(Q)>=max((s-2)m1+sum(m),(t-2)n1+sum(n)); any original Ramsey host G has e(G)>=max((s-1)m1+sum(m),(t-1)n1+sum(n)). In particular, if n=(1^s) is a matching, the exact joint residual minimum for ANY m is J=(s-2)m1+sum(m) and the exact original size Ramsey value is W=(s-1)m1+sum(m) over arbitrary finite simple graphs, with no saturation or parity conditions. Colour all edges meeting up to s-2 (joint) or s-1 (original) deleted vertices red; matching number red<=|S| excludes red target. Surviving graph contains full blue m for all S, allowing sequential deletion of a new degree>=m1 centre and disjoint edge accounting before final surviving full forest. Canonical antidiagonal host matches. Same by symmetry if m is a matching. Full unrestricted nonmatching/nonnmatching conjecture OPEN.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "For any arrow G->(F(a),F(b)) with p=length(a), red every edge touching a vertex set S of <=p-1 vertices; red vertex cover S gives matching number <p, while F(a) has p vertex-disjoint positive stars. Thus G-S contains F(b). Sequentially select p-1 centres of b1-stars in successive remaining graphs, each removing >=b1 distinct edges, and leave at least B=sum(b) edges in final graph. Apply to each residual and original arrow; for n=1^s canonical antidiagonal exactly has s copies of m1 followed by m2..mt, hence matches peeled bounds. Does not require mathematical factor theorem or bounded full-graph search.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/MATCHING_DEGREE_PEELING_THEOREM.md",
    "research/erdos-561/joint-general/verify_matching_degree_peeling.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/MATCHING_PEELING_EVIDENCE.json",
    "research/erdos-561/joint-general/SATURATED_MATCHING_JOINT_THEOREM.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary-host universal vertex-cover peeling and matching-side exact solution",
  "assumptions": [
    "s,t>=3; positive nonincreasing star lists n and m",
    "finite simple host graphs, ordinary non-induced vertex-disjoint star forest embeddings",
    "matching exact specialization: n=(1 repeated s), blue m completely arbitrary"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3618"
  ],
  "promotion_condition": "Paper theorem UNDER_REVIEW; numerical checker CHECKED only after exact-head replay. No full nonmatching/nonmatching theorem, no MATHCERT certification.",
  "claim_id": "ERDOS561-UNIVERSAL-MATCHING-PEELING-CHECK-026",
  "short_name": "Independent antidiagonal verification of all matching-side profiles and complete canonical hosts",
  "claim_text": "Exact finite tests compare both antidiagonal indexing conventions for matching original lists versus every enumerated nonincreasing blue profile, check the universal two-sided peeling bounds on bounded arbitrary positive list pairs, and exhaust complete red-arm allocations on six joint and original matching-side canonical hosts. The finite checker is corroboration, not the analytic arbitrary-host proof.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Standard library enumeration and two indexing methods; original and both joint residual antidiagonal profiles, universal certificate lower-vs-upper inequalities, complete star-host red-arm colour allocations for six nonuniform examples, deterministic bounded results.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_matching_degree_peeling.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/MATCHING_PEELING_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / all positive three-star-versus-three-star joint residual",
  "assumptions": [
    "a>=b>=e>=1,c>=d>=f>=1, originals x=(a,b,e), y=(c,d,f)",
    "arbitrary finite simple host graphs, ordinary non-induced and vertex-disjoint positive star-forest copies",
    "imported pinned two-component 2026 theorem and ordinary Gallai, Vizing, Győri-Schelp classical results"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3502"
  ],
  "promotion_condition": "A prior October 2026 public three-component proposed proof is explicitly acknowledged; this is an internal paper reconstruction and algebraic review, not priority, independent referee certification, MATHCERT, or proof of all s,t.",
  "claim_id": "ERDOS561-THREE-BY-THREE-JOINT-027",
  "short_name": "Exact arbitrary-host 3x3 joint residual via matching deletion and two-component bridge",
  "claim_text": "For all ordered positive triples x=(a,b,e), y=(c,d,f), a>=b>=e>=1,c>=d>=f>=1, the exact unrestricted-host simultaneous residual minimum equals J=w3+w4+w5+w6 with antidiagonal maxima w_k=max_{i+j=k}(x_i+y_j-1). Proof reconstructs the Oct 2026 publicly proposed three-component argument, with a two-star residual bridge from a pinned exact two-component result, one-vertex deletion forcing copies of full x,y, a Gallai factor-critical matching-number>=4 lemma when e>=2 or f>=2, induction stripping a maximum matching and lowering all four w terms by one, and a complete e=f=1 boundary of individually forced two-star bounds, four-edge matching recursion, or sole matching-number-three core 3K3. Canonical four-star host attains J. This is not the unrestricted s,t conjecture.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Every Q-v contains full original x and y via red-/blue-star monochromatic deletion; ν(Q)=3 gives factor-critical components and at most nine nonisolated vertices, contradicting any min arm>=2. If min arm>=2, maximum matching of at least4 decreases every term of joint tail by exactly1 and preserves residuals. For both min1, b>=d, if b=d=1 two individual two-star bounds suffice; if c>max(a,b+d-1) first residual is sharp; else ν>=4 and two-star residual bridge yields L-4 after matching deletion; ν=3 forces 3K3 and c<=2. Imported two-star theorem pinned arXiv:2610.25958v1; public three-component antecedent https://botnet.com/posts/2ca6bbad-89fa-450c-91ea-ea82e142e0b1 .",
  "source_or_artifact": [
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_RECONSTRUCTION.md",
    "research/erdos-561/joint-general/verify_three_by_three_joint_induction.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / all positive three-star-versus-three-star joint residual",
  "assumptions": [
    "a>=b>=e>=1,c>=d>=f>=1, originals x=(a,b,e), y=(c,d,f)",
    "arbitrary finite simple host graphs, ordinary non-induced and vertex-disjoint positive star-forest copies",
    "imported pinned two-component 2026 theorem and ordinary Gallai, Vizing, Győri-Schelp classical results"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3502"
  ],
  "promotion_condition": "A prior October 2026 public three-component proposed proof is explicitly acknowledged; this is an internal paper reconstruction and algebraic review, not priority, independent referee certification, MATHCERT, or proof of all s,t.",
  "claim_id": "ERDOS561-THREE-BY-THREE-LARGE-LEADER-028",
  "short_name": "Original 3x3 size Ramsey exact when sum of leading star sizes at least 12",
  "claim_text": "For any positive ordered original triples x=(a,b,e),y=(c,d,f) with a,c>=2 and a+c>=12, the original unrestricted-host size Ramsey number equals the five-antidiagonal W=sum_{k=2}^6w_k. Via claim027 every original Ramsey graph G with E<W has every vertex deletion satisfying joint residual e>=J=W-(a+c-1), hence Delta(G)<=a+c-2=D. Vizing forces Delta=D, and Győri-Schelp saturation necessity forces at least D+1 saturated vertices, so D(D+1)<=2E<=2(W-1)<=10(D+1)-2, impossible for D>=10. Canonical host yields upper. Also for x=(3r,r,r), y=(4r,3r,r), exact joint J=17r-4 all r>=1 and original W=24r-5 for r>=2, with switching surplus r.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Exact 3x3 joint residual claim027 plus source-locked every-vertex deletion implication bounds max degree in hypothetical E<W graph by D=a+c-2. Vizing edge-colour partition shows Delta>=D; Győri-Schelp degree cap theorem forces at least D+1 vertices degree D to prevent avoiding cap colouring. Sum degrees at least D(D+1), yet five canonical antidiagonal entries all <=D+1 imply 2E<=10(D+1)-2, contradiction for D>=10. This leaves small leading a+c<=11 untouched by this theorem; public proposed proof has additional case-specific arguments under independent review.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_RECONSTRUCTION.md"
  ],
  "related_files": [
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_EVIDENCE.json",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / all positive three-star-versus-three-star joint residual",
  "assumptions": [
    "a>=b>=e>=1,c>=d>=f>=1, originals x=(a,b,e), y=(c,d,f)",
    "arbitrary finite simple host graphs, ordinary non-induced and vertex-disjoint positive star-forest copies",
    "imported pinned two-component 2026 theorem and ordinary Gallai, Vizing, Győri-Schelp classical results"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3502"
  ],
  "promotion_condition": "A prior October 2026 public three-component proposed proof is explicitly acknowledged; this is an internal paper reconstruction and algebraic review, not priority, independent referee certification, MATHCERT, or proof of all s,t.",
  "claim_id": "ERDOS561-THREE-BY-THREE-CHECK-029",
  "short_name": "All three-star antidiagonal/induction arithmetic and six exception profiles finite verification",
  "claim_text": "Exact finite script checks 27225 ordered 3x3 pair profiles and both antidiagonal indexing conventions, 19800 red and 19800 blue four-term matching decrement identities, 860 boundary residual bridge identities, 22330 large-leader degree saturation arithmetic cases, exact set of six published exceptional (a,b,c,d) boundary profiles, 100 scale-switch family identities, and all 1301 red-arm allocations of six canonical joint hosts. These checks support but do not replace the unbounded matching/Gallai proof.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Two independently coded index conventions for 3x3 antidiagonal lists, algebraic direct bridge identities and matching-decrement equations for bounded positive star size grid, boundary parameter exact comparisons, complete red-arm host allocations. Finite checks are not a graph-topology proof.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_three_by_three_joint_induction.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 complete ORIGINAL three-component versus three-component size Ramsey",
  "assumptions": [
    "Original lists x=(a,b,e),y=(c,d,f), a>=b>=e>=1,c>=d>=f>=1",
    "arbitrary finite simple host graphs, ordinary non-induced vertex-disjoint star forest copies",
    "prior public 2026-10-21 three-part original proposal with precedence and pinned 2026 two-component result; ordinary Tutte-Berge, Vizing and degree-split theorems"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3502",
    "MATH-PROGRAMME#3475"
  ],
  "promotion_condition": "All-positive 3x3 original theorem is paper-level reconstruction of publicly proposed result; source review required for Tutte-Berge matching criterion, 3K2 vs 2P3+K2 matching-number five lemma, six boundary core colourings and imported 2-component theorem. No independent MATHCERT/public priority or all s,t certification.",
  "claim_id": "ERDOS561-THREE-BY-THREE-ORIGINAL-ALL-030",
  "short_name": "Complete original arbitrary-host 3×3 formula including all low-degree boundary profiles",
  "claim_text": "For every two ordered positive original triples x=(a,b,e),y=(c,d,f), the exact asymmetric size Ramsey number over arbitrary finite simple graph hosts equals the sum of all five original antidiagonal maxima W=sum_{k=2}^6 max_{i+j=k}(x_i+y_j-1). The proof reconstructs the public 2026-10-21 complete three-part argument and independently closes the low-leader cases omitted by claim 028, under its named pinned/classical graph-theory imports. It first derives E=W-1 and Delta=D=a+c-2 for a hypothetical smaller Ramsey host using sharp joint 3x3 claim 027; Vizing degree cap and Gyori-Schelp saturation imply h>=D+1 degree-D vertices and D<=9, while both leaders odd exclude by even cap split. If either minimum original arm>=2, a Tutte-Berge matching-number-five obstruction for (3K2,2P3 disjoint K2) permits deletion of a >=5-edge matching and induction on all five antidiagonals. At the minimum-one boundary b=d=1, finite seven leader pairs are eliminated by degree/vertex budgets, prescribed-vertex matching saturation lemma and explicit max-degree-four core colourings. With b>=2, the pinned two-component theorem after removing a five-edge matching covers all but six quadruples; those are eliminated by saturated-vertex matching, Vizing missing-class absorption, or explicit induced core colourings. Canonical five-star host attains W. Not a proof for s>3 or t>3, nor an independent mathematical certificate.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Full detailed proof in THREE_BY_THREE_ORIGINAL_FULL_BOUNDARY.md; imported exact joint theorem in THREE_BY_THREE_JOINT_RECONSTRUCTION.md; Tutte-Berge matching-number-five lemma enumerates all witness partitions of matching number four, constructing avoiding two-colourings; induction on minimum arm uses 5-edge matching removal; b=d=1 h>=D+1 implies seven low leading pairs, eliminated using vertex budgets, odd-D matching-cover of saturated vertices, degree-4 core explicit colourings and max-degree-2 cycle case; b>=2 isolates six other parameter quadruples handled by Vizing class recolouring or induced saturated-core colourings. Explicit provenance 2026-10-21 publicly proposed proof, not claimed novel.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/THREE_BY_THREE_ORIGINAL_FULL_BOUNDARY.md",
    "research/erdos-561/joint-general/verify_three_by_three_original_boundary.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/THREE_BY_THREE_ORIGINAL_EVIDENCE.json",
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_RECONSTRUCTION.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 complete ORIGINAL three-component versus three-component size Ramsey",
  "assumptions": [
    "Original lists x=(a,b,e),y=(c,d,f), a>=b>=e>=1,c>=d>=f>=1",
    "arbitrary finite simple host graphs, ordinary non-induced vertex-disjoint star forest copies",
    "prior public 2026-10-21 three-part original proposal with precedence and pinned 2026 two-component result; ordinary Tutte-Berge, Vizing and degree-split theorems"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3502",
    "MATH-PROGRAMME#3475"
  ],
  "promotion_condition": "All-positive 3x3 original theorem is paper-level reconstruction of publicly proposed result; source review required for Tutte-Berge matching criterion, 3K2 vs 2P3+K2 matching-number five lemma, six boundary core colourings and imported 2-component theorem. No independent MATHCERT/public priority or all s,t certification.",
  "claim_id": "ERDOS561-THREE-BY-THREE-ORIGINAL-CHECK-031",
  "short_name": "Full original 3×3 boundary exact arithmetic and complete canonical star-host arm audits",
  "claim_text": "Exact bounded finite script checks 81225 original 3x3 ordered positive profile pairs; 62700 red and 62700 blue five-term matching decrement identities; 2255 two-component boundary subtraction identities; seven low-leader pairs, six last boundary quadruples, Vizing missing-class bound, and all full red-arm allocation classes of five small canonical original upper hosts (2552). These checks establish their declared finite arithmetic and upper bounds, not every arbitrary-host lower by computation.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Deterministic Python script computes original antidiagonal formula for every sorted positive 3x3 pair with leading sizes up to 11, independently validates each matching-decrement identity, boundary arithmetic, six exceptions and seven leader pairs, complete antidiagonal upper host arm-allocation enumeration. The unbounded all-host lower uses a separate paper matching/core proof; not certified from finite data.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_three_by_three_original_boundary.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/THREE_BY_THREE_ORIGINAL_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 uniform star forest original and joint results for arbitrary component counts",
  "assumptions": [
    "uniform original n=(a repeated s),m=(b repeated t), all s,t>=3 and positive a,b>=1",
    "NO parity, equality or star-size assumptions on a,b; arbitrary finite simple hosts",
    "Chunlin You 2026 pinned two-star size Ramsey formula, Vizing's classical edge colouring theorem",
    "The uniform-original exact result is PRIOR PUBLISHED: Fu, Luo, Ni, Size Ramsey minimal graphs for uniform star forests, arXiv:2606.04439v3 (2026), not claimed novel"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3624",
    "MATH-PROGRAMME#3622"
  ],
  "promotion_condition": "Known published uniform formula, do not claim GCL novelty. Paper-level independent proof reconstruction UNDER_REVIEW. General nonuniform all-profile Erdős #561 OPEN; no MATHCERT issued.",
  "claim_id": "ERDOS561-UNIFORM-ALL-LENGTHS-032",
  "short_name": "Known all-parity uniform star-forest Ramsey theorem, independently reconstructed via Vizing spare class",
  "claim_text": "KNOWN PUBLISHED uniform-family formula, independently proved by a shorter Vizing smallest-class method: for ALL s,t>=3 and a,b>=1, unrestricted simple-host joint J=(s+t-2)(a+b-1), original size Ramsey W=(s+t-1)(a+b-1). Fix A=a-1,B=b-1,D=A+B,R=D+1. If maxdeg G<=D and e(G)<(p+q-1)R, Vizing yields R matching classes; reserve the smallest M with |M|<=p+q-2 and give A base classes red/B blue. Each endpoint of a spare edge misses at least one base class, hence has a safe red or blue option. If endpoints lack a common safe colour, whichever colour assigned to that spare edge creates at most ONE red or blue overcap centre; spare edges form a matching, so each of <=p+q-2 conflicts permits independent red/blue exception assignment with <p red and<q blue centres. Therefore a graph arrowing uniform red F(a^p) and blue F(b^q) below canonical threshold must have degree >=R. Base sharp joint s=3,t arbitrary follows from pinned published two-component formula; delete a degree>=R vertex to induct joint in red count, then use every-deletion joint implication to prove original W. Previous Euler and twofactor proofs remain optional special-case explanations, not logical prerequisites. The uniform formula is known in previous literature and not GCL's first discovery. Full arbitrary nonuniform conjecture OPEN.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Complete independent Vizing colour-class proof at start of UNIFORM_ALL_COMPONENTS_EULER_DEFECT_THEOREM.md. Each G maximum degree D edge-decomposes into R=D+1 matchings; smallest spare class M <=e/R, each edge's endpoints miss at least one of D base class colours, allowing freely selectable single overcap defect if safe sets conflict. Assign at most p-1 red defects and q-1 blue defects, obtaining avoiding colouring for every G with maxdeg<=D and E<(p+q-1)R. Use published pinned two-component result for s=3 and joint vertex-deletion induction, then original deletion. Formula's novelty explicitly DISCLAIMED: Fu/Luo/Ni arxiv:2606.04439v3. Other longer Euler/Hall proofs remain restricted alternative cases.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/UNIFORM_ALL_COMPONENTS_EULER_DEFECT_THEOREM.md",
    "research/erdos-561/joint-general/verify_uniform_star_erdos561.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/UNIFORM_ALL_COMPONENTS_EVIDENCE.json",
    "research/erdos-561/joint-general/EVEN_CAP_DEGREE_SPLITTING_THEOREM.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 uniform star forest original and joint results for arbitrary component counts",
  "assumptions": [
    "uniform original n=(a repeated s),m=(b repeated t), all s,t>=3 and positive a,b>=1",
    "NO parity, equality or star-size assumptions on a,b; arbitrary finite simple hosts",
    "Chunlin You 2026 pinned two-star size Ramsey formula, Vizing's classical edge colouring theorem",
    "The uniform-original exact result is PRIOR PUBLISHED: Fu, Luo, Ni, Size Ramsey minimal graphs for uniform star forests, arXiv:2606.04439v3 (2026), not claimed novel"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3624",
    "MATH-PROGRAMME#3622"
  ],
  "promotion_condition": "Unbounded uniform theorem paper-level UNDER_REVIEW, deterministic finite arithmetic/graph checks CHECKED. General unequal-even or heterogeneous star-size conjecture remains OPEN/PARTIAL. No MATHCERT.",
  "claim_id": "ERDOS561-UNIFORM-ALL-LENGTHS-CHECK-033",
  "short_name": "All-uniform all-parity exact numeric and canonical host checks",
  "claim_text": "Deterministic arithmetic checks all 13689 uniform pairs with s,t=3..11,a,b=1..13, including ALL mixed-parity/unit edge cases, and complete red-arm allocations on 36 canonical original/joint hosts totalling 974916 colourings. An additional 36030 bounded simple-graph Euler component checks validate a narrower alternative proof. These exact finite checks corroborate but do not replace the unrestricted-host Vizing argument. Uniform exact formula is already established in published literature.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Standard-library checker computes original and joint uniform antidiagonal sums over all 13689 bounded pairs and complete original/joint canonical upper host colour allocations over 36 cases. Earlier Euler component mini-atlas remains regression, not requirement for general Vizing proof. Source and claim remain independently reviewed before any certification.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_uniform_star_erdos561.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/UNIFORM_ALL_COMPONENTS_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / nonuniform two-arm stars with exactly one single-edge tail, arbitrary component counts",
  "assumptions": [
    "original red n=(2 repeated s-1,1), s>=3, original blue m=(2 repeated t) OR (2 repeated t-1,1), t>=3",
    "finite simple arbitrary host graphs; ordinary non-induced vertex-disjoint star-forest embeddings",
    "published pinned Chunlin You 2026 two-component size Ramsey exact base for first residual at s=3"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3626"
  ],
  "promotion_condition": "New paper-level unbounded proof UNDER_REVIEW, finite complete path/cycle witnesses CHECKED. Source imports pinned two-component theorem. Full nonuniform Erdős #561 OPEN/PARTIAL; novelty not independently established and no MATHCERT.",
  "claim_id": "ERDOS561-NONUNIFORM-UNIT-TAIL-ALL-LENGTHS-034",
  "short_name": "Exact arbitrary-host nonuniform one-edge-tail two-edge-star families for all s,t",
  "claim_text": "For all s,t>=3, original n=(2^(s-1),1) and blue m=(2^t), sharp JOINT J=3(s+t-3)+2 and original W=3(s+t-2)+2. If both red n=(2^(s-1),1) and blue m=(2^(t-1),1) have one-edge tails, sharp JOINT J=3(s+t-3) and original W=3(s+t-2). All claims are for arbitrary finite simple host graphs, not just disjoint-star hosts. The exact proof gives a degree-two avoiding colouring below these canonical thresholds and then inducts on s using first-residual high-degree vertex and published two-component theorem for s=3. The full problem for other arbitrary nonuniform lists remains OPEN.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "For Δ<=2, components are paths/cycles. Proper alternating colours of paths/even cycles yield no monochromatic P3; odd cycles yield exactly one red OR blue P3 centre. Under edge thresholds, if number k odd cycles <=r+u-2, distribute defects to cap the number of monochromatic P3 centres below target counts. If k=r+u-1, edge budget forces ALL triangle components with <=1 extra edge in red-tail/blue-uniform case, or all triangles with <=2 extra edges OR one C5 with no extras in both-tail case. Choose r triangles wholly red and the others blue, extra edges blue, or colour the C5 blue, to prevent the required additional disjoint K2 or enough P3. Therefore any arrowing original or first residual subcanonical graph has degree >=3. First residual at s=3 is the pinned full two-component size Ramsey theorem, giving sharp J. Delete an appropriate degree>=3 vertex in both residuals to reduce red component count; canonical J attained. Original host E<W has degree>=3 and every deletion has the proven sharp J, giving E>=W. Explicit complete graph-class oracle supports but is not an unbounded proof.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/UNIT_TAIL_TWO_STAR_ALL_LENGTHS_THEOREM.md",
    "research/erdos-561/joint-general/verify_unit_tail_two_stars.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/UNIT_TAIL_TWO_STAR_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 / nonuniform two-arm stars with exactly one single-edge tail, arbitrary component counts",
  "assumptions": [
    "original red n=(2 repeated s-1,1), s>=3, original blue m=(2 repeated t) OR (2 repeated t-1,1), t>=3",
    "finite simple arbitrary host graphs; ordinary non-induced vertex-disjoint star-forest embeddings",
    "published pinned Chunlin You 2026 two-component size Ramsey exact base for first residual at s=3"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3626"
  ],
  "promotion_condition": "New paper-level unbounded proof UNDER_REVIEW, finite complete path/cycle witnesses CHECKED. Source imports pinned two-component theorem. Full nonuniform Erdős #561 OPEN/PARTIAL; novelty not independently established and no MATHCERT.",
  "claim_id": "ERDOS561-NONUNIFORM-UNIT-TAIL-CHECK-035",
  "short_name": "Two nonuniform all-length family algebra and actual degree-two graph avoiding colouring oracle",
  "claim_text": "Deterministic source checker independently validates original and both residual antidiagonal maxima for 242 bounded s,t/case pairs, verifies both residual and original Ramsey upper on 24 canonical star hosts across all 82080 red-arm allocation classes, and exhausts all 3460 declared path/cycle component multisets under Lemma 3/4 bounds using a true ordinary vertex-disjoint P3/K2 graph-embedding search to confirm explicit avoiding colourings. This finite validation corroborates the unbounded analytic proof.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Standard-library verifier exhaustively enumerates path/cycle component multiset isomorphism representatives under edge limits for six (lemma, r,u) instances, builds explicit avoiding edge-colouring witnesses including triangle and five-cycle boundary cases, then tests exact vertex-disjoint non-induced P3 and extra K2 embedding by DFS. Independent antidiagonal formulas and all red-arm canonical host allocations checked, no extrapolation to arbitrary topology from finite enumeration.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_unit_tail_two_stars.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/UNIT_TAIL_TWO_STAR_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 four-by-three heterogeneous joint residual and original size Ramsey, arbitrary finite simple hosts",
  "assumptions": [
    "original red n=(a,b,c,f), positive a>=b>=c>=f>=1, c>=f+1",
    "original blue m=(d,e,1), positive d>=e>=1",
    "derived A=a-f+1,B=b-f+1,C=c-f+1>=2; penalty P=(d-max(B,C+e-1))_+ +(e-C)_+",
    "ordinary vertex-disjoint, non-induced star-forest copies in finite simple host graphs",
    "paper-level imported exact 3x3 joint residual; classical Gallai factor critical; source-locked original degree-core transfer"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3624",
    "MATH-PROGRAMME#3627"
  ],
  "promotion_condition": "Mathematical proof source UNDER_REVIEW, nonindependent local exact finite checks CHECKED only; unbounded full all-profile Erdős #561 and full joint residual remain OPEN, no MATHCERT.",
  "claim_id": "ERDOS561-FOUR-BY-THREE-JOINT-MATCHING-BRIDGE-036",
  "short_name": "Exact four-by-three heterogeneous simultaneous residual under vanishing explicit matching deficit; unbounded switching surplus",
  "claim_text": "For n=(a,b,c,f) sorted positive c>=f+1, blue m=(d,e,1), write A=a-f+1,B=b-f+1,C=c-f+1>=2 and P=(d-max(B,C+e-1))_+ +(e-C)_+. Every finite simple joint-residual host Q satisfies e(Q)>=Jcan(n,m)-P; if e<=C and d<=max(B,C+e-1), P=0 and exact arbitrary-host joint residual equals the full five-nonleading-antidiagonal canonical tail Jcan. Proof: second residual alone Q→(F(a,b,c,f),F(e,1)) implies every Q-v contains red F(n) by colouring v edges BLUE. If ν(Q)<=4, then ν=4 and matching-stability Gallai factor-critical decomposition bounds nonisolated vertices<=12; the required red F(n) after arbitrary deletion needs>=11, forcing Q=4K3. Colour three triangles red, fourth blue, avoiding both residual targets. So ν(Q)>=5. Remove a maximum matching and colour it red to reduce red arm sizes by1, with last f=1 star dropped, resulting in known sharp 3x3 joint residual. The exact algebraic difference is 5+P, giving lower Jcan-P. For f>=2, induction uniformly decrements all 4 red arms and all five joint antidiagonal weights by1, preserving deficit P. An original equality also holds when d>=2 and W<=D(D+1)/2, D=a+d-2; automatically if a+d>=14, or if both leading sizes odd by even cap transfer, or via known matching-side result when d=1. Infinite genuinely heterogeneous scale family n_h=(6h,4h,4h,1), m_h=(4h,3h,1) has sharp joint J=28h-2, two separate residual sums 27h-2, switching surplus sigma=h for ALL h>=1 and sharp ORIGINAL W=38h-3 for ALL h>=1 by degree budget D(D+1)>2(W-1). This is not an all-profile theorem. Complementary exact regime: the individual first residual has full sharp 3x3 ORIGINAL size bound S1 by source reconstruction; second residual has full sharp 4x2 ORIGINAL bound S2 by pinned You two-component result. Their max equals Jcan-sigma, sigma:=Jcan-max(S1,S2). Thus any joint host has e(Q)>=Jcan-min(P,sigma), exact Jcan whenever either P=0 OR sigma=0, including P>0 cases not covered by matching deletion alone. The remaining nonsharp region requires BOTH P>0 AND sigma>0.\n New BLUE matching reduction for e>=2: remove at least five BLUE matching edges. This produces the JOINT residual for original red four-star n and the blue TWO-component list (d-1,e-1). The independently source-proved two-component residual bridge (3x3 reconstruction, Lemma1, after swapping colours) provides sharp canonical joint lower on that shortened pair. At last red arm f=1, exact algebraic deficit P_B=(a-max(b+e-1,c+d-1))_+ +(b-max(c+e-1,d))_+ +(c-e)_+. For general f>=1 uniformly decrement all four RED arms until the last becomes one, preserving reduced A,B,C and hence P_B=(A-max(B+e-1,C+d-1))_+ +(B-max(C+e-1,d))_+ +(C-e)_+. Combined unconditional lower becomes Jcan-min(P_R,P_B,sigma) when e>=2, and Jcan-min(P_R,sigma) when e=1. Hence exact canonical JOINT whenever ANY of the three legal deficits is zero. This BLUE bridge closes 838 additional base profiles in the finite grid, leaving 458 positive in all three. A distinct scale family n=(4h,2h,2h,1),m=(4h,3h,1) has P_R=sigma=h, P_B=0, exact JOINT J=21h-2 for all h>=1, separate residuals 20h-2, and exact ORIGINAL W=29h-3 for h>=2 by core transfer, with leading D=8h-2 and D(D+1)-2(W-1)=64h²-82h+10>0 at h>=2.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "See FOUR_BY_THREE_MATCHING_BRIDGE_THEOREM.md. Key new arbitrary-host matching lemma from a single two-component blue residual: after deleting ANY vertex red full 4-star n remains, forcing matching>=4. With ν=4 all components factor critical and <=12 nonisolated vertices; 11-vertex minimum red forest after each deletion forces Q=4K3, which explicit red3/blue1 triangle colouring avoids. Therefore a >=5 matching exists. Deleting it red turns 4x3 joint into full sharp 3x3 joint when last red arm=1; five-arm antidiagonal subtraction leaves only P=(d-max(b,c+e-1))_++(e-c)_+. Uniform red decrement inducts for f>1. Original from protected core-transfer. Scale family n_h=(6h,4h,4h,1),m_h=(4h,3h,1): w=(10h-1,9h-1,8h-1,7h-1,4h,1), J=28h-2, original W=38h-3, sigma=h, and D(D+1)-2(W-1)=(h-1)(100h-6)+4>0. Separately source-proved first residual exact 3x3 and second residual exact 4x2 yield Jcan-sigma lower; combine with matching bridge Jcan-P to get Jcan-min(P,sigma). BLUE matching-coloured removal reduces 4x3 JOINT to exact 4x2 JOINT (two-component residual Lemma1 with swapped colours). The corresponding three-positive-part algebraic deficit P_B is computed at red last-arm=1; red matching peeling transfers it to arbitrary f, giving exact Jcan-min(P_R,P_B,sigma) lower. Scale family (4h,2h,2h,1) vs (4h,3h,1) has exact J=21h-2, sigma=h, original W=29h-3 for h>=2.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_THEOREM.md",
    "research/erdos-561/joint-general/verify_four_by_three_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_EVIDENCE.json",
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_RECONSTRUCTION.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 four-by-three heterogeneous joint residual and original size Ramsey, arbitrary finite simple hosts",
  "assumptions": [
    "original red n=(a,b,c,f), positive a>=b>=c>=f>=1, c>=f+1",
    "original blue m=(d,e,1), positive d>=e>=1",
    "derived A=a-f+1,B=b-f+1,C=c-f+1>=2; penalty P=(d-max(B,C+e-1))_+ +(e-C)_+",
    "ordinary vertex-disjoint, non-induced star-forest copies in finite simple host graphs",
    "paper-level imported exact 3x3 joint residual; classical Gallai factor critical; source-locked original degree-core transfer"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3624",
    "MATH-PROGRAMME#3627"
  ],
  "promotion_condition": "Mathematical proof source UNDER_REVIEW, nonindependent local exact finite checks CHECKED only; unbounded full all-profile Erdős #561 and full joint residual remain OPEN, no MATHCERT.",
  "claim_id": "ERDOS561-FOUR-BY-THREE-MATCHING-CHECK-037",
  "short_name": "Four-by-three exact matching deficit, lifted profiles, switching and Gallai four-triangle witness arithmetic",
  "claim_text": "Deterministic standard-library tests calculate original and both separate residual antidiagonal maxima in independent indexing conventions across 14520 positive four-by-three base profiles; among them 5496 profiles have zero explicit matching deficit (375 with positive switching surplus), 9024 have positive deficit; 16488 all-positive-arm red uniform lifts checked; 4955 base parameter settings satisfy protected original core criterion; 150 scale-family tests verify sigma=h and full joint/original formulas. Independent structural enumeration checks all 8 factor-critical matching-number-four component-multiplicity shapes, proving only four triangles saturate the required nonisolated vertex budget. A concrete 4K3 red/blue avoiding colouring is checked against the minimal red four-star and blue two-star targets by exact ordinary vertex-disjoint star embedding DFS. Finite checks do not prove the general host lemma by enumeration. Checker additionally verifies the coupled residual inequality Jcan-min(P,sigma)=max(Jcan-P,S1,S2), counts the additional P>0,sigma=0 exact cases, and isolates the explicit P>0,sigma>0 frontier. Additional independent algebraic dual 4x2 JOINT matching-decrement checks verify P_B on all profiles with e>=2; red/blue/sigma three-way certificate closes 14062 of 14520 bounded base profiles, including 838 newly closed by the blue route, with exactly 458 three-way-positive cases remaining. Lifted sharp cases verified in 34314 parameter tuples; second 150-scale family checks blue P_B=0, sigma=h, exact J=21h-2 and original core-transfer arithmetic for h>=2.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Exact Python integer maxima and index conventions for base/lifted four-by-three profiles, exact two-positive-part deficit and switching identity, independent red/blue residual sums and sufficient original edge-budget check, 150 scale cases. Enumerates positive compositions of matching number four and validates nonisolated vertex budget using factor-critical order 2ν+1; graph DFS with actual edges of 4K3 validates explicit avoiding colouring against smallest four-red-star and two-blue-star targets. Unbounded reasoning relies on paper Gallai theorem and imported 3x3 result, NOT on finite computations. The 4x2 blue residual canonical arm array is independently compared with the 4x3 five-entry tail for all allowed blue e>=2, verifying the three-positive-part P_B. Two separate unbounded switching scale families checked, 150 h each.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_four_by_three_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 general blue terminal shifts and tied-bottom red four-versus-three joint residual theorem",
  "assumptions": [
    "red n=(a,b,c,f), a>=b>=c>=f>=1 with c>=f+1",
    "blue m=(d,e,g), positive d>=e>=g>=1",
    "blue-flat m0=(d-g+1,e-g+1,1); red reduced values A=a-f+1,B=b-f+1,C=c-f+1>=2",
    "all host graphs finite simple, stars embedded ordinarily non-induced and vertex-disjoint",
    "source-proved Gallai 5-matching lemma, exact 3x3 and 4x2 joint residual reductions"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3633"
  ],
  "promotion_condition": "Paper proof UNDER_REVIEW; arithmetic and actual graph witnesses CHECKED at exact committed source head. Full all-profile Erdős #561 OPEN/PARTIAL; no independent MATHCERT.",
  "claim_id": "ERDOS561-4X3-BLUE-TERMINAL-LIFT-038",
  "short_name": "Unrestricted-host four-versus-three joint lower bound under arbitrary blue minimum shifts",
  "claim_text": "For any blue terminal g>=1, n=(a,b,c,f) with c>=f+1 and m=(d,e,g) sorted positive, let mflat=(d-g+1,e-g+1,1). Form RED matching deficit P_R, BLUE matching deficit P_B (if second blue-flat arm>=2), and switching surplus sigma for pair (n,mflat) by source-locked Theorem B/C. Then every arbitrary finite simple joint host for (n,m) has e>=Jcan(n,m)-min(P_R,P_B,sigma), omitting P_B when not legal. Thus any zero deficit implies exact JOINT canonical value for ORIGINAL lists with all blue star sizes possibly >=2. Proof: the second residual blue (e,g) contains two positive stars. Blue-star incident-edge colouring around arbitrary vertex forces red full four-star forest after every deletion, giving a 5-edge matching by Gallai and the 4K3 avoiding-colour exception. Remove a BLUE matching, obtaining the two residual relations for the blue list (d-1,e-1,g-1) while keeping red unchanged. Repeat until blue terminal=1, preserving the flat parameters and dropping all five joint weights by one each step; then apply exact source-proved one-tail theorem. Independent original transfer when W<=D(D+1)/2 gives exact original; shifting both RED and BLUE profiles of red family (6h,4h,4h,1),blue(4h,3h,1) uniformly produces exact joint J=28h-2+5(r+k), W=38h-3+6(r+k) for every h>=1,r,k>=0, sigma=h, with ORIGINAL exact via protected degree-core. A second blue-family n=(4h+r,2h+r,2h+r,1+r), m=(4h+k,3h+k,1+k) has J=21h-2+5(r+k), sigma=h, original exact for h>=2 or h=1 and r+k>=3.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "BLUE-minimum induction Theorem D in FOUR_BY_THREE_MATCHING_BRIDGE_THEOREM.md. Every intermediate second residual has two blue positive stars, so a minimum-5 matching exists by the Gallai four-component obstruction. Colour removed matching blue; decrements blue stars and retains red. Five joint antidiagonal weights drop exactly one per uniform blue decrement, with reduced flat blue pair invariant. Base one-edge blue joint Theorems B/C/source independent individual residual lower. Exact three-parameter all-positive shift families and core-transfer inequalities are explicitly documented; no unrestricted all-profile theorem.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_THEOREM.md",
    "research/erdos-561/joint-general/verify_four_by_three_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 general blue terminal shifts and tied-bottom red four-versus-three joint residual theorem",
  "assumptions": [
    "red original n=(a,b,f,f), sorted positive a>=b>=f>=1",
    "blue original m=(d,e,g), sorted positive d>=e>=g>=1",
    "normalized A=a-f+1,B=b-f+1 with A+B>=5; D=d-g+1,E=e-g+1>=2",
    "all finite simple host graphs and ordinary non-induced vertex-disjoint star forests"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3633"
  ],
  "promotion_condition": "Paper proof UNDER_REVIEW; arithmetic and actual graph witnesses CHECKED at exact committed source head. Full all-profile Erdős #561 OPEN/PARTIAL; no independent MATHCERT.",
  "claim_id": "ERDOS561-4X3-TIED-RED-TAIL-BLUE-BRIDGE-039",
  "short_name": "Tied-bottom red four-star forests against heterogeneous three-star blue lists",
  "claim_text": "For every n=(a,b,f,f) and m=(d,e,g) satisfying A+B>=5,E>=2 as defined, any arbitrary finite simple JOINT residual host has e>=Jcan−P_tie, where P_tie=(A-max(B+E-1,D))_+ +(B-D)_+. Combined with separately known exact first/second residual size bounds, e>=Jcan−min(P_tie,sigma). Consequently P_tie=0 or sigma=0 implies exact full joint canonical value, despite red smallest TWO stars being equal. New Gallai support lemma: if red four-star forest uses >=11 nonisolated vertices, any graph arrowing it against two positive blue stars contains a matching of at least5. Colour v-edge blue forces red forest in every Q-v; ν(Q)=4 gives <=12 nonisolated vertices from Gallai factorcritical decomposition, forcing exactly 4K3 if red V=11 and impossible if larger; colour three triangles red, fourth blue to contradict. This applies to red-flat (A,B,1,1), A+B>=5, and all intermediate red shifts. Use red and blue matching deletions to reduce both minima to1; at red-flat and blue-flat base remove five BLUE matching edges and invoke source-proved 4x2 JOINT two-component residual lemma, with exact two-positive-part P_tie. A new scale family n=(4h+r,h+r,1+r,1+r),m=(4h+k,2h+k,1+k) for all h>=1,r,k>=0 has exact JOINT J=16h+5(r+k), unbounded sigma=h, Wcanonical=24h-1+6(r+k). Protected original degree-core transfer makes W exact for h>=2 or h=1 and r+k>=2; in particular all h>=1 with r,k>=1 and NO single-edge stars. Full unrestricted problem remains OPEN.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Section 9 Lemma E.1 and Theorem E.2: matching>=5 forced by red component vertex support V>=11 plus Gallai factorcritical nonisolated budget and explicit avoiding 4K3 red3/blue1 triangle colouring. No invalid red-to-zero-star reduction: only legal red decrement until tied red last=1 and blue decrement until blue last=1, then 4x2 blue matching residual bound. Direct antidiagonal algebra yields P_tie with no third positive part because C=1; separately proved residual lower gives sigma. Explicit 3param family and core formula 64h^2−72h+4+(16h−15)x+x^2 are checked and require x>=2 at h=1, or all x at h>=2.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_THEOREM.md",
    "research/erdos-561/joint-general/verify_four_by_three_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_EVIDENCE.json",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 general blue terminal shifts and tied-bottom red four-versus-three joint residual theorem",
  "assumptions": [
    "red original n=(a,b,f,f), sorted positive a>=b>=f>=1",
    "blue original m=(d,e,g), sorted positive d>=e>=g>=1",
    "normalized A=a-f+1,B=b-f+1 with A+B>=5; D=d-g+1,E=e-g+1>=2",
    "all finite simple host graphs and ordinary non-induced vertex-disjoint star forests"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3633"
  ],
  "promotion_condition": "Paper proof UNDER_REVIEW; arithmetic and actual graph witnesses CHECKED at exact committed source head. Full all-profile Erdős #561 OPEN/PARTIAL; no independent MATHCERT.",
  "claim_id": "ERDOS561-4X3-TIED-RED-AND-BLUE-LIFT-CHECK-040",
  "short_name": "Exact finite tied-red BLUE matching deficit, terminal shifts and third switching family checks",
  "claim_text": "Deterministic exact finite arithmetic checks cover 4884 base tied-red profiles (A,B,1,1) against (D,E,1) for A+B>=5,E>=2, checking exact P_tie and independent red/blue residual sums. Of these, 3160 have P_tie=0; 3212 sigma=0; union 4053 exact by proved lower bounds, including 841 positive-switching cases closed specifically by blue bridge. 43956 RED/BLUE terminal shifts verify five-edge change per matching deletion, switching invariance, legal positive profiles and core arithmetic; 35920 of the sharp shifted profiles satisfy the sufficient original core condition. Third infinite h,r,k family has 2400 exact profile checks and 2397 satisfies the protected original core criterion, with known three exceptions h=1,x=0 or1. The prior established blue-minimum lift checks cover 29040 parameter instances, and prior two three-parameter families each have 750 checked cases. A real 4K3 graph-colouring embedding oracle checks new tied-red n=(4,1,1,1), blue F(2,1) avoiding example; finite validation is distinct from unbounded all-host argument.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "verify_four_by_three_matching_bridge.py uses two indexing conventions, integer max antidiagonals, separate residual lower identities, P_tie formula, full three parameter scale identities and protected core criterion; it enumerates 4K3 explicit avoiding edge-colour graph witness by independent ordinary non-induced star-forest embedding DFS. All tests are finite and do not purport to establish unrestricted-host lemma by sampling.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_four_by_three_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 heterogeneous five-red versus three-blue unrestricted-host joint and original star forest Ramsey programme",
  "assumptions": [
    "red original five stars n=(a,b,c,d,f), a>=b>=c>=d>=f+1, positive",
    "blue original three stars m=(u,v,w), u>=v>=w>=1, positive",
    "arbitrary finite simple graph host, ordinary vertex-disjoint non-induced positive star-forest copies",
    "Gallai matching-stability theorem; source-proved 4x3 JOINT lower (including tied-last-two RED case); protected general ORIGINAL degree-core transfer"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3633"
  ],
  "promotion_condition": "Unbounded paper-level theorem UNDER_REVIEW, finite deterministic check CHECKED only upon fresh exact-head replay. Full unrestricted Erdős #561 OPEN/PARTIAL; do not self-certify mathematical independence, novelty or MATHCERT.",
  "claim_id": "ERDOS561-FIVE-BY-THREE-SIX-MATCHING-BRIDGE-041",
  "short_name": "Six-edge matching reduction from genuine 5x3 JOINT to proved 4x3 and fourth unbounded-switching family",
  "claim_text": "Every finite simple JOINT residual host Q for five-red n=(a,b,c,d,f) with first four red arms >=f+1 and blue m=(u,v,w) has a matching of size>=6. Specifically the second joint relation Q→(F(n),F(v,w)) forces red n inside every Q-t by colouring all t edges blue; red forest uses at least14 vertices. If ν(Q)=5, then all vertex deletions have ν=5, Gallai factorcritical decomposition bounds nonisolated vertices<=15. Red forest requires >=14 after deleting nonisolated vertex, forcing Q nontrivial part=5K3; colour four triangles red and one blue to avoid both targets, contradiction. For normalized f=w=1, RED matching deletion reduces joint to q=(a-1,b-1,c-1,d-1) vs m blue, and exact canonical tail identity Jcan5=6+Jcan4+P5 with P5=(u-max(c,d+v-1))_+ +(v-d)_+. General f,w obtained via RED and BLUE uniform matching decrements, each removing >=6 edges while preserving joint arrows and dropping each of six joint antidiagonal weights by1, giving e(Q)>=Jcan5-P5(flat)-Delta4 where Delta4 is source-proved 4x3 joint deficit. When P5=0 and reduced 4x3 JOINT is exact, original 5x3 joint is exact. Fourth heterogeneous family n=(6h+r,3h+r,3h+r,3h+r,1+r),m=(4h+k,2h+k,1+k) for all h>=1,r,k>=0 has exact JOINT J=30h-3+6(r+k), canonical switching sigma=h and exact ORIGINAL size Ramsey W=40h-4+7(r+k). Reduced q=(6h-1,3h-1,3h-1,3h-1) has tied bottom red sizes and is exact by 4x3 Theorem E.2: normalized A=3h+1,B=1,blue D=4h,E=2h, Ptie0; P5 zero. The original transfer holds since Dlead(Dlead+1)-2W=10(h-1)(10h-1)+(20h-17)(r+k)+(r+k)^2>=0 for all h,r,k. All star components >=2 when r,k>=1. This is a genuinely 5x3 all-host family and NOT all-profile closure.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "Complete all-host proof in FIVE_BY_THREE_SIX_MATCHING_BRIDGE_THEOREM.md. Matching stability and red support >=14 imply ν>=6, including explicit 5K3 red4/blue1 triangle contradiction. Remove RED six-edge matching to lower five-red joint to protected 4x3 source after dropping last red1 star; exact integer tail gap P5. Reduce positive red and blue terminal sizes by legal monochromatic matching deletions retaining JOINT. Source-proved tied-bottom 4x3 exact theorem closes fourth h,r,k scale family, protected degree-core ensures original W. Canonical switching h algebraic, and individual unrestricted-host minima exact for h>=2 where protected 4x3 original transfer applies; h1 only canonical gap asserted. All full conjecture claims remain OPEN.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/FIVE_BY_THREE_SIX_MATCHING_BRIDGE_THEOREM.md",
    "research/erdos-561/joint-general/verify_five_by_three_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FIVE_BY_THREE_SIX_MATCHING_BRIDGE_EVIDENCE.json",
    "research/erdos-561/joint-general/FOUR_BY_THREE_MATCHING_BRIDGE_THEOREM.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 heterogeneous five-red versus three-blue unrestricted-host joint and original star forest Ramsey programme",
  "assumptions": [
    "red original five stars n=(a,b,c,d,f), a>=b>=c>=d>=f+1, positive",
    "blue original three stars m=(u,v,w), u>=v>=w>=1, positive",
    "arbitrary finite simple graph host, ordinary vertex-disjoint non-induced positive star-forest copies",
    "Gallai matching-stability theorem; source-proved 4x3 JOINT lower (including tied-last-two RED case); protected general ORIGINAL degree-core transfer"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3633"
  ],
  "promotion_condition": "Unbounded paper-level theorem UNDER_REVIEW, finite deterministic check CHECKED only upon fresh exact-head replay. Full unrestricted Erdős #561 OPEN/PARTIAL; do not self-certify mathematical independence, novelty or MATHCERT.",
  "claim_id": "ERDOS561-FIVE-BY-THREE-SIX-MATCHING-CHECK-042",
  "short_name": "Exact 5x3 six-matching antidiagonal, complete canonical host and 5K3 graph witness audit",
  "claim_text": "Standard-library exhaustive integer checker verifies the exact five-versus-three six-weight difference J5−6−J4=P5 for 10584 bounded ordered positive star-profile parameter settings using independently indexed antidiagonal calculations. It verifies 7056 red terminal-lift identities, 172480 fully enumerated red/blue arm allocations across one original and one joint canonical 5x3 host, all 16 ordered positive factor-critical matching-number-five component partition types, and an explicit 5K3 red4/blue1 triangle avoiding-colouring witness against red F(2,2,2,2,1) and blue F(1,1), via independent actual vertex-disjoint ordinary star-forest graph embedding DFS. It also checks 2400 fourth unbounded-switching h,r,k profiles (including 1350 with red and blue minimum size>=2), with exact joint/original formulas, linked proven reduced 4x3 tied-tail deficit=0, 5x3 P5=0, and protected original degree-core arithmetic. Finite checks are complete in declared restricted classes and not a proof of all-host lemma by sampling.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Independent explicit Python checker verify_five_by_three_matching_bridge.py. Integer antidiagonal computations use two conventions and exact equality assertions; sample canonical star hosts exhaust all red-arm allocations; factorcritical compositions exact; actual 5K3 graph embedding DFS confirms red and blue absence under one concrete colouring. General all-host reasoning is separately proved in paper and pending mathematical review.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_five_by_three_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/FIVE_BY_THREE_SIX_MATCHING_BRIDGE_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary-length heterogeneous red staircase against three blue positive stars",
  "assumptions": [
    "s>=3 positive integer number red star components; h>=1 integer scale",
    "independent red shift r>=0 and blue shift k>=0",
    "red n_1=(2s-3)h+1+r,n_2=2(s-3)h+1+r,n_i=2(s-i)h+1+r for i=3,...,s",
    "blue m=(4h+1+k,2h+1+k,1+k)",
    "ordinary vertex-disjoint non-induced positive-star forest copies in arbitrary finite simple graph hosts",
    "source-proved 3x3 exact joint/original, published two-component original, protected general original-degree-core transfer, classical Gallai matching-stability theorem"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3650"
  ],
  "promotion_condition": "Paper all-host mathematical proof UNDER_REVIEW; bounded computational check CHECKED. Full all-profile Erdős #561 remains OPEN/PARTIAL; no MATHCERT or independent specialist attestation.",
  "claim_id": "ERDOS561-ALL-RED-LENGTHS-THREE-BLUE-STAIRCASE-043",
  "short_name": "Unrestricted-host exact joint and original size Ramsey for heterogeneous three-blue staircase with arbitrary red length and unbounded switching",
  "claim_text": "For all s>=3,h>=1,r,k>=0 with RED heterogeneous staircase n1=(2s-3)h+1+r,n2=2(s-3)h+1+r,ni=2(s-i)h+1+r for 3<=i<=s and BLUE m=(4h+1+k,2h+1+k,1+k): the minimum arbitrary-host simultaneous JOINT residual edge number is EXACT J=(s²+s−1)h+(s+1)(1+r+k); the ORIGINAL size Ramsey number is EXACT W=(s²+3s)h+(s+2)(1+r+k). The two SEPARATELY required original residual size Ramsey minima are each EXACT S=(s²+s−2)h+(s+1)(1+r+k), so ACTUAL switching surplus J−S=h, arbitrarily large for unbounded scale. General Gallai matching lemma: if a graph Q arrows a red forest of s positive stars with vertex support>=3s−1 against TWO positive blue stars, then ν(Q)>=s+1. Colour every edge at arbitrary vertex blue forces the red forest in all Q−v. Were ν(Q)=s, Gallai factorcritical matching stability bounds nonisolated order<=3s, and red support after deleting any nonisolated vertex>=3s−1 forces precisely s disjoint K3; colouring s−1 triangles red and one blue avoids both targets. General joint step: for red n=(n1,...,n_(s-1),1) with preceding all>=2 and blue (u,v,1), remove at least s+1 RED matching edges, reducing to red q=(n1−1,...,n_(s-1)−1), and canonical joint exact deficit P_s=(u−max(n_(s−2),n_(s−1)+v−1))_++(v−n_(s−1))_+. Thus J_s>=Jcan_s−P_s−Delta_(s−1) for source-proved shorter-list deficit. In staircase P_s=0 at every red length step. After removing the first s+1 edges, remove another 2h−1 matchings of size>=s to reduce red q to exactly staircase length s−1, yielding exact extra cost (s+1)+s(2h−1)=2sh+1, the canonical difference. Base s3 full 3x3 source-proved; induction proves all s. RED/BLUE uniform shifts carried by legal matching deletion at s+1 edges each. Protected ORIGINAL transfer applies because D=(2s+1)h+r+k and D(D+1)−2W is positive for all s,h,r,k. Separate first RED-deleted residual n_(2:) is equal-top red B_L with L=s−1; sharp JOINT by analogous zero-deficit induction from L3 3x3 and sharp ORIGINAL by protected core for L>=4 (correct h1 L4 margin4), with two-component L2 from published theorem. Second BLUE-deleted residual sharp by published two-component theorem. Therefore actual switching surplus h, not merely canonical upper-host difference. All star sizes >=2 for r,k>=1. No assertion about unrestricted arbitrary profiles.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "ALL_RED_LENGTHS_THREE_BLUE_STAIRCASE_THEOREM.md Section 1 general arbitrary-host matching obstruction by Gallai 3s−1 support and explicit sK3 avoiding red(s−1)/blue1 triangle colouring. Section 2 exact all-s matching deletion identity and nonnegative P_s; Section 3 staircase induction in red component count with P_s=0, matching cost 2sh+1, positive RED/BLUE terminal shifts and protected original transfer D(D+1)>=2W. Section 4 individually exact RED-deleted equal-top B_L residual original via its own matched recursion and core polynomial; BLUE-deleted exact two-component theorem. The matching proof is unbounded in red component count; code is only corroboration and manuscript UNDER_REVIEW. General all-profile #561 OPEN/PARTIAL.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/ALL_RED_LENGTHS_THREE_BLUE_STAIRCASE_THEOREM.md",
    "research/erdos-561/joint-general/verify_all_red_lengths_three_blue_staircase.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/ALL_RED_LENGTHS_THREE_BLUE_EVIDENCE.json",
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_RECONSTRUCTION.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary-length heterogeneous red staircase against three blue positive stars",
  "assumptions": [
    "s>=3 positive integer number red star components; h>=1 integer scale",
    "independent red shift r>=0 and blue shift k>=0",
    "red n_1=(2s-3)h+1+r,n_2=2(s-3)h+1+r,n_i=2(s-i)h+1+r for i=3,...,s",
    "blue m=(4h+1+k,2h+1+k,1+k)",
    "ordinary vertex-disjoint non-induced positive-star forest copies in arbitrary finite simple graph hosts",
    "source-proved 3x3 exact joint/original, published two-component original, protected general original-degree-core transfer, classical Gallai matching-stability theorem"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3650"
  ],
  "promotion_condition": "Paper all-host mathematical proof UNDER_REVIEW; bounded computational check CHECKED. Full all-profile Erdős #561 remains OPEN/PARTIAL; no MATHCERT or independent specialist attestation.",
  "claim_id": "ERDOS561-ALL-RED-LENGTHS-STAIRCASE-CHECK-044",
  "short_name": "Independent bounded all-s antidiagonal, equal-top residual, Gallai sK3 graph and canonical star host verification",
  "claim_text": "Standard-library independent checker of exact all-s three-blue heterogeneous staircase: 7200 s/h/r/k main family cases, 6480 general s+1-matching antidiagonal deficit identities on ordered nonstaircase 4<=s<=8 lists, 2772 equal-top B_L residual family cases, 420 main red-component induction steps, 286 equal-top induction steps, 4050 cases with all red and blue arm sizes>=2, complete 48624 arm-colour assignments for six canonical original and two joint classes (s=3/4,h=1), every nontrivial factor-critical matching number partition for s=3..9 (508 ordered component partitions), and explicit avoiding ordinary vertex-disjoint graph-embedding DFS on sK3 for s=3..9. Tests use zero-based and one-based independent antidiagonal conventions and assert exact formula, separate residual canonical values, shifted reductions, core inequalities and actual graph witness. This finite CHECKED computation is not a proof of all-host Gallai argument, or independently attested certification.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "verify_all_red_lengths_three_blue_staircase.py, deterministic standard-library code, no external network or stochastic data. Exact two-index arithmetic and full small canonical-host colouring exhaustive checks, seven explicit sK3 graph witnesses. The full formula uses a separate unbounded paper induction. Fresh exact-head SHA and test replay required before marking CHECKED; no MATHCERT.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_all_red_lengths_three_blue_staircase.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/ALL_RED_LENGTHS_THREE_BLUE_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 general s-red versus three-blue joint residual exactness under a single BLUE matching and normalized red vertex-support bound",
  "assumptions": [
    "s>=3 RED positive nonincreasing star edges n=(n1,...,ns) and blue THREE positive nonincreasing m=(u,v,g)",
    "normalized RED a_i=n_i-n_s+1 with a_s=1; BLUE U=u-g+1,V=v-g+1>=2",
    "normalized RED vertex support sum_i(a_i+1)>=3s−1",
    "arbitrary finite simple host graphs and ordinary vertex-disjoint non-induced positive star-forest copies",
    "source-proved two-component RED versus arbitrary-blue residual Lemma 1 in THREE_BY_THREE_JOINT_RECONSTRUCTION.md; apply with colours exchanged",
    "classical Gallai matching stability / factor critical components and protected ORIGINAL degree-core transfer"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3652"
  ],
  "promotion_condition": "Mathematical all-host theorem UNDER_REVIEW, finite checks CHECKED after exact-head execution. Unrestricted all-profile Erdős #561 remains OPEN/PARTIAL, no MATHCERT, no unsupported novelty assertion.",
  "claim_id": "ERDOS561-ALL-S-SINGLE-BLUE-MATCHING-045",
  "short_name": "General s×3 joint lower bound by ONE blue matching and arbitrary red profile interference penalty",
  "claim_text": "Let s>=3, arbitrary ordered positive RED n=(n1,...,ns), BLUE m=(u,v,g). Write a_i=n_i-n_s+1, U=u-g+1, V=v-g+1>=2 and require normalized red support sum_i(a_i+1)>=3s−1. For i=1,...,s−1 define T_i=max(a_(i+1)+V−1, a_(i+2)+U−1 when i+2<=s; omit second term otherwise). Then BLUE matching penalty P_BLUE=sum_i(a_i−T_i)_+ >=0. EVERY arbitrary finite simple JOINT residual host Q has e(Q)>=Jcan(n,m)−P_BLUE. Therefore if every a_i<=T_i, the arbitrary-host JOINT minimum is exactly Jcan(n,m), and if additionally protected Wcan<=D(D+1)/2 with D=n1+u−2, ORIGINAL size Ramsey is exactly Wcan. Proof: second residual arrows red full n vs two BLUE positive stars (v,g). Colour all edges incident to arbitrary t BLUE, forcing red F(n) in Q−t. If ν(Q)=s, Gallai factorcritical matching stability gives <=3s nonisolated vertices; normalized red needs >=3s−1 after any deletion, forces exactly s triangles; colour s−1 triangles red and one blue avoids both targets. So ν(Q)>=s+1 for all required intermediate hosts. Legitimately remove >=s+1 RED matchings to decrement red minimum to1, and >=s+1 BLUE matchings to decrement blue minimum to1; all s+1 canonical joint tail weights decrease by one per decrement and normalized profiles remain invariant. Then remove one BLUE matching from normalized joint Q; the remainder jointly arrows original RED a against blue TWO-component pair (U−1,V−1) as two residual relations. After exchanging colours, these are EXACTLY the source-proved two-component red-arbitrary-blue residual lemma hypotheses; therefore remainder has >=Jcan(a,(U−1,V−1)) edges. Exact canonical identity Jcan(a,(U,V,1))=(s+1)+Jcan(a,(U−1,V−1))+P_BLUE follows term-by-term: k3 contributes 1; k4..s+2 old maximum adds third blue arm a_(k−3) to A_k, giving 1+(a_(k−3)−A_k)_+; final k=s+3 contributes a_s=1. Combining with matching size yields quantified lower. All-lengths staircase n1=(2s−3)h+1+r,n2=2(s−3)h+1+r,ni=2(s−i)h+1+r for i>=3, blue (4h+1+k,2h+1+k,1+k) has P_BLUE=0 FOR ALL s,h,r,k, so its sharp JOINT is obtained by a SINGLE blue matching, not the older red length-induction or full 3x3 JOINT. Its first separately required equal-top residual B_L also has P_BLUE=0; actual switching surplus h follows with source-proved original core plus L3 original and L2 published two-component result. This theorem holds for arbitrary RED component count s and arbitrary ordered RED lists satisfying support and explicit zero penalty, not just staircase. Outside zero penalty only a quantitative lower, not all-profile sharpness.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md Sections 1-3 all-host Gallai sK3 obstruction and exact single BLUE matching reduction to existing TWO-component residual Lemma 1 after colour swap. Nonnegative interference penalty P_BLUE obtained from exact antidiagonal maxima (s+1 canonical tail weights versus s reduced two-blue weights). Normalization of positive RED and BLUE minimum sizes by same-size matching deletions uses fixed RED vertex support>=3s−1 and V>=2. Source Sections 4-5 reconstruct staircase JOINT in one BLUE step and independently equal-top JOINT; actual switching uses source-pinned original residual formulas. Claim strictly UNDER_REVIEW, unrestricted Erdős #561 OPEN/PARTIAL.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md",
    "research/erdos-561/joint-general/verify_all_s_blue_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/THREE_BY_THREE_JOINT_RECONSTRUCTION.md",
    "research/erdos-561/joint-general/ALL_RED_LENGTHS_THREE_BLUE_STAIRCASE_THEOREM.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 general s-red versus three-blue joint residual exactness under a single BLUE matching and normalized red vertex-support bound",
  "assumptions": [
    "s>=3 RED positive nonincreasing star edges n=(n1,...,ns) and blue THREE positive nonincreasing m=(u,v,g)",
    "normalized RED a_i=n_i-n_s+1 with a_s=1; BLUE U=u-g+1,V=v-g+1>=2",
    "normalized RED vertex support sum_i(a_i+1)>=3s−1",
    "arbitrary finite simple host graphs and ordinary vertex-disjoint non-induced positive star-forest copies",
    "source-proved two-component RED versus arbitrary-blue residual Lemma 1 in THREE_BY_THREE_JOINT_RECONSTRUCTION.md; apply with colours exchanged",
    "classical Gallai matching stability / factor critical components and protected ORIGINAL degree-core transfer"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3652"
  ],
  "promotion_condition": "Mathematical all-host theorem UNDER_REVIEW, finite checks CHECKED after exact-head execution. Unrestricted all-profile Erdős #561 remains OPEN/PARTIAL, no MATHCERT, no unsupported novelty assertion.",
  "claim_id": "ERDOS561-ALL-S-SINGLE-BLUE-MATCHING-CHECK-046",
  "short_name": "Exact arbitrary-red-list BLUE matching deficit in 179928 cells and 134447 sharp-criterion cases",
  "claim_text": "Deterministic standard-library checker verifies full exact all-s BLUE penalty identity Jcan(n,(U,V,1))−(s+1)−Jcan(n,(U−1,V−1))=sum_(i=1)^(s−1) (a_i−T_i)_+ in 179928 ordered positive RED profiles (lengths 3..8, largest s−1 arms from1..8, terminal=1) against positive BLUE (U,V,1) with 2<=V<=U<=8, using independent zero-based and one-based antidiagonal indexing. Among these exactly 177856 satisfy red support>=3s−1; 134447 also have P_BLUE=0 and hence paper theorem sharp JOINT; 11142 of those have positive canonical switching surplus and 7090 also satisfy protected sufficient ORIGINAL degree core criterion. Tests additionally cover 7266 normalized red/blue terminal lifts, 680 scale cases across red lengths3..19 with P_BLUE=0 in all-length staircase, 510 equal-top residual scale cases, seven actual sK3 avoiding-colour graph embedding oracles, and 5052 fully enumerated joint canonical-host star-arm allocations for three chosen nonuniform parameter pairs. These are FINITE exact algebra, enumeration, and graph witness checks, not an unrestricted-host proof by sampling nor MATHCERT.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "verify_all_s_blue_matching_bridge.py, two independent antidiagonal indexing conventions and exact Python integers, complete finite parameter domain, explicit sK3 graph DFS and canonical arm-colour allocations. The generic all-host lower is proved separately in mathematical manuscript, not inferred from bounded profile counts. No independent reviewer mathematical adjudication.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_all_s_blue_matching_bridge.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/ALL_S_BLUE_MATCHING_SINGLE_STEP_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 compositional exactness certification for arbitrary RED component count against three BLUE stars",
  "assumptions": [
    "red n sorted positive of arbitrary component count s>=3, blue m=(u,v,g) sorted positive length exactly3",
    "ordinary non-induced vertex-disjoint stars, arbitrary finite simple host graphs",
    "source-proved complete ORIGINAL/JOINT 3x3 theorem, pinned published two-component ORIGINAL theorem and source two-component residual bridge",
    "source-proved single BLUE matching theorem with normalized support/penalty and protected three ORIGINAL degree-core transfer clauses"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656"
  ],
  "promotion_condition": "Paper logical proof-tree composition UNDER_REVIEW; finite executable classification CHECKED; all all-profile conjecture OPEN/PARTIAL; no independent MATHCERT.",
  "claim_id": "ERDOS561-RECURSIVE-THREEBLUE-PROOF-CERTIFICATE-047",
  "short_name": "Well-founded source-derived JOINT and ORIGINAL exactness certificates from three residual mechanisms and protected degree core",
  "claim_text": "For arbitrary positive sorted RED lists of length s>=3 and three positive sorted BLUE sizes, define canonical original W and simultaneous JOINT J from antidiagonal maxima. A terminating source-derived proof procedure certifies exact JOINT when (B) normalized RED support>=3s-1, normalized BLUE second arm V>=2 and all-s single BLUE matching deficit P_B=0; OR (R2) exact pinned two-BLUE original second residual W(n,m[2:])=J; OR (R1) recursively certified exact ORIGINAL first residual red n[2:] versus same BLUE satisfies W(n[2:],m)=J. For red length s=3 source complete JOINT is unconditional; for red length2 two-component bridge handles auxiliary tails. The procedure certifies exact ORIGINAL if s<=3 by source complete ORIGINAL/two-component theorem, or for longer lists after certified JOINT using any one of the three protected transfer conditions: both leading RED/BLUE sizes odd; any parity W<=D(D+1)/2; or at least one leading odd with W<=D(D+1), D=n1+u−2. Recursion is well founded because first-residual proof uses one strictly shorter RED list. Every certified JOINT/ORIGINAL value holds for arbitrary finite simple graphs; returned UNKNOWN is not a counterexample and no full all-profile conjecture is assumed. In a declared 179928-profile finite grid s=3..8, other RED sizes1..8 terminal1 and blue (U,V,1), 2<=V<=U<=8, exact JOINT certificates are 162839; 17089 remain UNKNOWN by these methods; exact ORIGINAL certificates are 129885. The proof priorities yield 1008 baseline 3x3, 133949 BLUE zero-loss, 13924 second residual and 13958 recursively sharp first residual JOINT instances. A concrete JSON proof dependency trace and SHA256 classification fingerprint make provenance machine-inspectable but do not constitute independently formally checked mathematical certification.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md Sections 1-2 give precise well-founded inference rules and source dependencies; JOINT lower uses either all-s BLUE matching lemma, exact two-blue ORIGINAL second residual, or recursively exact first original residual with equal canonical edge number. ORIGINAL lower combines certified JOINT with exact protected degree-core transfer; base s<=3 full paper theorem. No inference from star-host upper alone. verify_recursive_three_blue_certificates.py emits named theorem source proof trees and a reproducible finite-grid fingerprint; mathematical source rules require substantive review. Full all-profile Erdős #561 OPEN.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md",
    "research/erdos-561/joint-general/verify_recursive_three_blue_certificates.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/THREE_BY_THREE_ORIGINAL_FULL_BOUNDARY.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 compositional exactness certification for arbitrary RED component count against three BLUE stars",
  "assumptions": [
    "red n sorted positive of arbitrary component count s>=3, blue m=(u,v,g) sorted positive length exactly3",
    "ordinary non-induced vertex-disjoint stars, arbitrary finite simple host graphs",
    "source-proved complete ORIGINAL/JOINT 3x3 theorem, pinned published two-component ORIGINAL theorem and source two-component residual bridge",
    "source-proved single BLUE matching theorem with normalized support/penalty and protected three ORIGINAL degree-core transfer clauses"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656"
  ],
  "promotion_condition": "Paper logical proof-tree composition UNDER_REVIEW; finite executable classification CHECKED; all all-profile conjecture OPEN/PARTIAL; no independent MATHCERT.",
  "claim_id": "ERDOS561-RECURSIVE-THREEBLUE-PROOF-TRACE-CHECK-048",
  "short_name": "Deterministic 179928-profile exact finite recursive proof trace census and classification fingerprint",
  "claim_text": "Executable standard-library verifier enumerates all 179928 sorted positive original RED profiles of lengths3..8 with final RED=1 and remaining red sizes in1..8, and BLUE (U,V,1) with2<=V<=U<=8. The proof tree classifier outputs 1008 source-complete 3x3 JOINT, 133949 zero BLUE matching, 13924 exact two-blue second residual, 13958 recursively certified exact first residual and 17089 UNKNOWN; thus 162839 sharp JOINT and 129885 sharp ORIGINAL under the stated sufficient transfer conditions. It checks canonical antidiagonal indexing by two independent conventions, all theorem branch guards, well-founded recursion and explicit inspectable JSON proof for RED (2,2,1,1,1) versus BLUE (8,2,1), and computes the deterministic complete-grid SHA256 classification digest adef49db40fed21300afe1bccc2ef85c6f06278be2856f7ff9a3c0c132c4906b. Its finite CHECKED status applies to arithmetic and trace generation only, not the mathematical truth of its imported paper-level theorems.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "verify_recursive_three_blue_certificates.py --grid; deterministic fully enumerated RED+BLUE grid, two independently indexed canonical arrays, source theorem branch verification and source-named nested JSON proof traces for specified profiles. Fingerprint pins decision+branch+original certificate on every case; replay on exact HEAD. Finite code does not prove Gallai or core transfer or certify full conjecture.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_recursive_three_blue_certificates.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 recursive source-derived joint/original exactness for arbitrary RED length versus three positive BLUE stars",
  "assumptions": [
    "nonincreasing positive original RED n length s>=4, BLUE m=(u,v,g) sorted positive",
    "normalized RED a_i=n_i−n_s+1, a_s=1 and a_(s-1)>=2; normalized BLUE b=(U,V,1)=(u-g+1,v-g+1,1) positive",
    "finite simple arbitrary hosts with ordinary non-induced vertex-disjoint copies",
    "all-s Gallai s+1 matching obstruction for normalized RED total support >=3s-1",
    "shorter joint q=(a_1−1,...,a_(s−1)−1) against b has independently source-backed exact JOINT proof when promoting sharp",
    "prior source-proved two-component/full three-by-three plus protected original degree-core transfer are unchanged"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656",
    "MATH-PROGRAMME#3671"
  ],
  "promotion_condition": "New paper RED-matching recursion UNDER_REVIEW; exact-grid trace computation CHECKED after source-locked replay. Source assumptions and protected core-transfer unchanged; full unrestricted all-profile #561 remains OPEN/PARTIAL and no MATHCERT.",
  "claim_id": "ERDOS561-RECURSIVE-RED-MATCHING-TRANSFER-049",
  "short_name": "Well-founded RED matching inference enhances all-s three-BLUE joint certificates, including normalized shorter tails",
  "claim_text": "For original sorted RED n length s>=4 and 3-blue m, normalize a_i=n_i−n_s+1 and b=(u-g+1,v-g+1,1), require a_(s−1)>=2. Define q=(a_1−1,...,a_(s−1)−1), and P_RED=(U−max(a_(s−2),a_(s−1)+V−1))_++(V−a_(s−1))_+. For EVERY arbitrary finite simple simultaneous residual host Q, e(Q)>=Jcan(n,m)−P_RED−(Jcan(q,b)−J_actual(q,b)). The protected Gallai s+1 matching lemma supplies RED and BLUE uniform terminal normalizations; the final RED-coloured matching removes >=s+1 edges, turning the TWO original joint residual arrows into precisely the joint residual arrows for shorter q and b. Exact canonical identity Jcan(a,b)=(s+1)+Jcan(q,b)+P_RED gives the bound. If P_RED=0 AND a source-proved sharp shorter joint certificate exists (including after its own lawful normalization), exact original JOINT follows. The terminating proof-tree procedure adds this inference after the admitted original BLUE matching, exact second residual and first-residual routes; it may itself provide a stronger source-proved first-residual ORIGINAL via protected degree-core transfer. Neither positive P_RED nor UNKNOWN is silently promoted to sharpness. In the declared 179928-cell integer profile grid, exact JOINT certificates increase from162839 to165677 (+2838), exact ORIGINAL from129885 to131052 (+1167), and JOINT UNKNOWN decreases from17089 to14251. Of 2838 new JOINT, 1871 trace directly to RED matching and 967 to subsequently newly sharp first-residual ORIGINAL. These are full bounded arithmetic classifications, not unrestricted all-host census or MATHCERT.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md proves arbitrary host Gallai matching support and legal monochromatic terminal reductions, final RED matching reduction from s-star original to source-proved (s-1)-star JOINT and exact P_RED antidiagonal difference. Well-founded recurrence on smaller red length, no unproved full conjecture. Old admitted 047-048 certificate unchanged, extend with explicit proof trace. Claims 049 paper UNDER_REVIEW and 050 finite CHECKED only; no independent mathematical cert.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md",
    "research/erdos-561/joint-general/verify_recursive_red_matching_certificates.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/RECURSIVE_RED_MATCHING_CERTIFICATE_EVIDENCE.json",
    "research/erdos-561/joint-general/RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md",
    "research/erdos-561/joint-general/ALL_RED_LENGTHS_THREE_BLUE_STAIRCASE_THEOREM.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 recursive source-derived joint/original exactness for arbitrary RED length versus three positive BLUE stars",
  "assumptions": [
    "nonincreasing positive original RED n length s>=4, BLUE m=(u,v,g) sorted positive",
    "normalized RED a_i=n_i−n_s+1, a_s=1 and a_(s-1)>=2; normalized BLUE b=(U,V,1)=(u-g+1,v-g+1,1) positive",
    "finite simple arbitrary hosts with ordinary non-induced vertex-disjoint copies",
    "all-s Gallai s+1 matching obstruction for normalized RED total support >=3s-1",
    "shorter joint q=(a_1−1,...,a_(s−1)−1) against b has independently source-backed exact JOINT proof when promoting sharp",
    "prior source-proved two-component/full three-by-three plus protected original degree-core transfer are unchanged"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656",
    "MATH-PROGRAMME#3671"
  ],
  "promotion_condition": "New paper RED-matching recursion UNDER_REVIEW; exact-grid trace computation CHECKED after source-locked replay. Source assumptions and protected core-transfer unchanged; full unrestricted all-profile #561 remains OPEN/PARTIAL and no MATHCERT.",
  "claim_id": "ERDOS561-RECURSIVE-RED-MATCHING-PROOF-TRACE-CHECK-050",
  "short_name": "Deterministic red/blue composed JOINT proof-tree trace and 2838 new exact source-certified profiles",
  "claim_text": "Executable deterministic checker verify_recursive_red_matching_certificates.py imports the original admitted proof-tree implementation without changes, adds a strictly-shorter RED matching rule and enhanced first residual ORIGINAL transfer, and exhausts all179928 sorted original RED lists length3..8, RED terminal1 and other arms in1..8, BLUE (U,V,1) with2<=V<=U<=8. Previous exact JOINT=162839 and ORIGINAL=129885 remain accepted profile-by-profile. The new classifier proves EXACT source-sufficient JOINT=165677, including2838 new, and ORIGINAL=131052, including1167 new; remaining joint UNKNOWN14251. Of newly accepted joint,1871 use RED matching directly and967 invoke first-residual ORIGINAL upgraded through the new rule. The classifier independently verifies 972 normalization identities for RED/BLUE terminal shifts in positive profiles, a concrete previously unknown example (7,5,2,1) vs (5,2,1) with trace to full sharp 3x3 JOINT, and complete classification SHA256 digest 5dd3bdc40bbed1ed951385a779a5bbd3137d2ff9ba6c4f2499dc1b7835365f97. This CHECKED finite trace certificate does not re-prove Gallai or prior paper-source theorems and does not imply MATHCERT or global #561 closure.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "verify_recursive_red_matching_certificates.py deterministic standard-library source imports verify_recursive_three_blue_certificates, preserves all existing old certificates and checks exact nested theorem guards. 179928 original/plus profile pairs, 972 terminal normalization assertions, two independent antidiagonal indexes through admitted source, reproducible classification digest, explicit new proof tree. No arbitrary host graph enumeration and no independent mathematical adjudication.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_recursive_red_matching_certificates.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/RECURSIVE_RED_MATCHING_CERTIFICATE_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary-host three-BLUE recursive JOINT/ORIGINAL proof certificates with omitted vertex-budget transfer",
  "assumptions": [
    "RED original list n has sorted positive length s>=3; BLUE m has sorted positive length exactly3",
    "any use of fourth transfer requires leading sizes n1,m1>=2, opposite parity, prior JOINT canonical sharpness proof for the exact profile",
    "D=n1+m1-2, W=canonical full original antidiagonal sum, R=max(sum(n)+s,sum(m)+3)",
    "fourth criterion strict inequality 2W<2D²+R, from already source-proved GENERAL_CORE_ORIGINAL_TRANSFER.md Theorem A condition4",
    "arbitrary finite simple graph hosts, ordinary non-induced vertex-disjoint star forests"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656",
    "MATH-PROGRAMME#3652"
  ],
  "promotion_condition": "Paper mathematical theorem source UNDER_REVIEW; bounded deterministic proof-dependency and arithmetic checks CHECKED only at fresh exact committed source head. The general Erdős #561 conjecture and joint residual remain OPEN/PARTIAL; no MATHCERT issued.",
  "claim_id": "ERDOS561-RECURSIVE-FOURTH-VERTEX-BUDGET-TRANSFER-051",
  "short_name": "Restore opposite-parity forest-vertex core transfer to the full existing 3-BLUE recursive theorem engine",
  "claim_text": "The existing source-proved general original degree-core transfer Theorem A has a fourth sufficient criterion not implemented in the prior recursive proof engine. If an unrestricted finite simple JOINT residual host is proved to require Jcan edges for original n,m, and n1,m1>=2 have opposite parity with 2Wcan<2D²+R, D=n1+m1−2, R=max(sum(n)+s,sum(m)+3), then the unrestricted original size-Ramsey number is exactly Wcan. Proof: hypothetical G arrowing original with e<=W-1 has all vertex-deletions jointly arrowing, hence degree Δ<=D. A red/blue split capped at n1−1,m1−1 would avoid both original forests; opposite parity caps and the protected 2D+1 saturated-core uniqueness theorem force at least 2D+2 degree-D vertices. Since G has >=R nonisolated vertices, handshake gives 2e>=R+(D−1)(2D+2)=R+2D²−2, contradicting 2e<=2W−2 and strict gate. The additional code is purely well-founded source-theorem composition: preserve the existing complete recursive 3BLUE and RED-matching rules, add fourth ORIGINAL transfer when previous ORIGINAL UNKNOWN and enhanced JOINT is independently certified; newly obtained JOINT traces may activate all THREE earlier original transfer gates. Reconsider an unknown JOINT only via a STRICTLY shorter RED first residual whose ORIGINAL is source-proved, or a certified zero-RED-matching deficit with a strictly shorter RED original. No unproved JOINT sharpness is assumed and UNKNOWN remains UNKNOWN. This exact theorem composition proves ORIGINAL formula W=31 for RED (3,3,1,1,1), BLUE (4,4,1) with J=25,D=5,R=14, because 62<64. General unrestricted Erdős #561 remains OPEN/PARTIAL.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "RECURSIVE_FOURTH_CORE_CERTIFICATE_THEOREM.md imports source-locked GENERAL_CORE_ORIGINAL_TRANSFER.md condition4 and prior `verify_recursive_three_blue_certificates.py` and `verify_recursive_red_matching_certificates.py` unmodified. Strict parity, support, leading>=2 and exact JOINT premise are enforced, with R and positive inequality margin retained. `verify_recursive_vertex_budget_certificates.py` propagates any new JOINT trace into all four ORIGINAL gates and only strictly shorter component lists recursively; never promotes UNKNOWN. The finite audit discovers 64 new source-conditional JOINT and 1341 new ORIGINAL within declared grid, contingent on correctness of imported paper theorems. No independent MATHCERT.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/RECURSIVE_FOURTH_CORE_CERTIFICATE_THEOREM.md",
    "research/erdos-561/joint-general/verify_recursive_vertex_budget_certificates.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RECURSIVE_RED_MATCHING_CERTIFICATE_THEOREM.md",
    "research/erdos-561/joint-general/RECURSIVE_FOURTH_CORE_CERTIFICATE_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 arbitrary-host three-BLUE recursive JOINT/ORIGINAL proof certificates with omitted vertex-budget transfer",
  "assumptions": [
    "RED original list n has sorted positive length s>=3; BLUE m has sorted positive length exactly3",
    "any use of fourth transfer requires leading sizes n1,m1>=2, opposite parity, prior JOINT canonical sharpness proof for the exact profile",
    "D=n1+m1-2, W=canonical full original antidiagonal sum, R=max(sum(n)+s,sum(m)+3)",
    "fourth criterion strict inequality 2W<2D²+R, from already source-proved GENERAL_CORE_ORIGINAL_TRANSFER.md Theorem A condition4",
    "arbitrary finite simple graph hosts, ordinary non-induced vertex-disjoint star forests"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656",
    "MATH-PROGRAMME#3652"
  ],
  "promotion_condition": "Paper mathematical theorem source UNDER_REVIEW; bounded deterministic proof-dependency and arithmetic checks CHECKED only at fresh exact committed source head. The general Erdős #561 conjecture and joint residual remain OPEN/PARTIAL; no MATHCERT issued.",
  "claim_id": "ERDOS561-RECURSIVE-FOURTH-VERTEX-BUDGET-CHECK-052",
  "short_name": "Complete 179928-profile fifth-source-gate proof trace and strict vertex-budget guard audit",
  "claim_text": "Deterministic exact arithmetic/proof-tree runner checks 179928 RED length3..8, sorted positive RED prefix1..8 terminal1, BLUE=(U,V,1) with 2<=V<=U<=8, against unmodified prior 50-claim proof engines. Baseline certificates exact JOINT=165677, ORIGINAL=131052; the new source-proved fourth transfer yields exact JOINT=165741 and ORIGINAL=132393, a monotone improvement +64 JOINT and +1341 ORIGINAL, JOINT UNKNOWN reduces 14251 to 14187. New JOINT routes consist of 45 FIRST_RESIDUAL_SHARP_VIA_FOURTH_CORE and 19 RED_MATCHING_VIA_FOURTH_CORE_RECURSION. Independent gate guard audit checks 107784 bounded parameter cells (including 605 with newly eligible fourth condition), exact strict inequality, opposite parity, both leaders>=2, and exclusions of previous gates and invalid heads. The exact classification fingerprint is 9de51f66f133867822961b38d2bf312a0f564fc28c75a72622249512ee4c2e6c. Concrete nested proof traces demonstrate new original n=(2,1,1,1,1),m=(5,4,1) and newly sharp joint n=(2,2,1,1,1,1),m=(5,4,1). The CHECKED finite trace certifies computation and source dependency consistency only, not mathematical independent referee approval or full all-profile conjecture.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "Standard-library deterministic `verify_recursive_vertex_budget_certificates.py`, exact integer canonical antidiagonals and source theorem guards, two-index canonical consistency from admitted `prior.canon/canon_alt`, monotonic old-certificate preservation and well-founded recursion. Full bounded grid fingerprint, an inspectable exact new proof tree and minimal guard examples. No arbitrary graph-host census; mathematical premises retain UNDER_REVIEW.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_recursive_vertex_budget_certificates.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/RECURSIVE_FOURTH_CORE_CERTIFICATE_THEOREM.md",
    "research/erdos-561/joint-general/RECURSIVE_FOURTH_CORE_CERTIFICATE_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 unrestricted-host exact ORIGINAL Ramsey from fifth nonisolated-vertex degree-core bound and recursive 3-BLUE inference",
  "assumptions": [
    "sorted positive original red n length s>=3 and blue m length t>=3 in finite simple graph",
    "both leading star sizes n1,m1>=2",
    "separately proved for the SAME original lists that every simultaneous JOINT residual host has at least Jcan=Wcan−(n1+m1−1) edges",
    "D=n1+m1−2, R=max(sum(n)+s,sum(m)+t), and 2Wcan<=D²+R",
    "ordinary non-induced vertex-disjoint positive-star forest embeddings",
    "source-proved ordinary Lovász factor theorem and maximum degree-D saturated core necessity (LOVASZ_CAP_PARTITION_BRIDGE.md)"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656"
  ],
  "promotion_condition": "Mathematical new sufficient all-parity ORIGINAL transfer UNDER_REVIEW; deterministic finite proof-tree replay CHECKED, not formally MATHCERT. Sharp JOINT must be individually source-proved for same red/blue lists, full Erdős #561 OPEN/PARTIAL.",
  "claim_id": "ERDOS561-FIFTH-CORE-VERTEX-SUPPORT-TRANSFER-053",
  "short_name": "Fifth all-parity original size-Ramsey transfer by saturated degree core plus minimum nonisolated support",
  "claim_text": "GENERAL ANY PARITY FIFTH SUFFICIENT ORIGINAL TRANSFER: if original red n and blue m sorted positive with leading sizes >=2, sharp JOINT residual lower Jcan individually already proved for these exact lists, D=n1+m1−2, R=max(required original red/blue forest nonisolated vertex counts), and 2Wcan<=D²+R, then exact unrestricted finite simple-host ORIGINAL size Ramsey is Wcan. Proof: hypothetically G arrowing original with e<=W−1, all G−v jointly arrow, hence delta(G)<=D. Capped edge red max n1−1 and blue max m1−1 partition must fail. Previously source-proved Lovász maximum-degree induced-core necessity therefore forces k>=D+1 degree-D vertices. All-red/all-blue targets imply Nnonisolated>=R. Handshake 2e>=kD+(N-k)>=R+(D−1)(D+1)=R+D²−1, but 2e<=2W−2<=R+D²−2, contradiction. The prior four sufficient transfer criteria remain valid and independent. New explicitly nontrivial even/even ORIGINAL n=(4,1,1,1),m=(4,2,1): original canonical weights (7,5,4,4,2,1), W=23,J=16,D=6,R=11; both leading even, half-core 2W=46>42, but fifth 46<=47. Source-proved JOINT for this exact pair gives unrestricted original value 23. Executable certified-premise composition checks same-source JOINT and fifth guard, and recurses only to strictly shorter red first residual or zero-loss RED matching. Full unrestricted JOINT remains OPEN/PARTIAL.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_THEOREM.md Theorem F is a new arithmetic/graph consequence of already sourced GENERAL_CORE_ORIGINAL_TRANSFER.md and LOVASZ_CAP_PARTITION_BRIDGE.md. Mathematically explicit core count k>=D+1 and nonisolated support R produce lower 2e>=R+D²−1, contradicted by hypothetical smaller host under inclusive 2W<=R+D². Requires an individually proven sharp JOINT for EXACT list. Recursive implementation preserves prior protected engines and evidence, with no theorem imported from finite census. Paper UNDER_REVIEW pending specialist scrutiny.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_THEOREM.md",
    "research/erdos-561/joint-general/verify_recursive_fifth_core_certificates.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_EVIDENCE.json",
    "research/erdos-561/formal-graph/LOVASZ_CAP_PARTITION_BRIDGE.md",
    "research/erdos-561/joint-general/GENERAL_CORE_ORIGINAL_TRANSFER.md",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561 unrestricted-host exact ORIGINAL Ramsey from fifth nonisolated-vertex degree-core bound and recursive 3-BLUE inference",
  "assumptions": [
    "earlier source-admitted recursive vertex-budget certificate engine claims 047–052 unchanged",
    "same full 179928 sorted 3-BLUE finite test grid from claims 047–052",
    "source-proved individually sharp JOINT required by each new ORIGINAL proof tree",
    "numerical fifth criterion guard 2W<=D²+R and both leading sizes >=2"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656"
  ],
  "promotion_condition": "Mathematical new sufficient all-parity ORIGINAL transfer UNDER_REVIEW; deterministic finite proof-tree replay CHECKED, not formally MATHCERT. Sharp JOINT must be individually source-proved for same red/blue lists, full Erdős #561 OPEN/PARTIAL.",
  "claim_id": "ERDOS561-FIFTH-CORE-RECURSIVE-TRACE-CHECK-054",
  "short_name": "Fifth-core full 179928-cell bounded proof-tree expansion adds 19492 original and 848 joint source-derived exact certificates",
  "claim_text": "Deterministic standard-library full bounded classification of 179928 sorted original red profiles of lengths s=3..8 with terminal red1 and other red entries in1..8, and original blue (U,V,1), 2<=V<=U<=8. Fifth all-parity nonisolated support gate combined with old FOUR rules and well-founded original/JOINT proof trees increases exact JOINT from165741 to166589 (+848) and exact ORIGINAL from132393 to151885 (+19492); 13339 JOINT and 28043 ORIGINAL remain UNKNOWN under existing sufficient rules. Of the 19492 new original, 18863 are directly newly unlocked by the fifth condition on profiles whose JOINT was already source-certified; other newly exact ORIGINAL values arise from additional recursively proven JOINT or older gate after new recursion. All 848 newly exact JOINT use strictly shorter first-residual original proof traces. Separate 107784 guard-grid cells include 83438 fifth criterion numerically legal, 1192 inclusive equality and 82246 positive strict margin; sample exact red (4,1,1,1),blue(4,2,1), W23,D6,R11 has fifth margin1. Full deterministic SHA256 fingerprint 47bfe81feacb0f0d1fd9686f248d85a4cc260afca9ea229c1cfe14b3060a0edf. This finite CHECKED claim verifies theorem application arithmetic and nested proof dependencies; it is not a census of host colourings or external mathematical certification.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "verify_recursive_fifth_core_certificates.py imports previous 52-claim proof engine unmodified, checks all fifth guards and inclusive margin, preserves every prior cert, recurses only to fewer RED components, retains nested exact-head theorem references and outputs fixed complete-grid digest. Entire 179928-cell classification and guards replay on exact current source; bounded computation independent of general all-host mathematical lemma, paper UNDER_REVIEW. No MATHCERT.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_recursive_fifth_core_certificates.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561; Gallai no-triangle sharpening of unrestricted-host all-s two-blue-star matching lower bound",
  "assumptions": [
    "finite simple unrestricted host, ordinary non-induced vertex-disjoint positive stars",
    "RED s-component forest F(a1,...,as) with s>=3 and required vertex support at least 2s+floor(s/2)",
    "BLUE forest F(v,g) has two positive disjoint stars",
    "for JOINT application original red sorted positive length s; original blue sorted positive (u,v,g); normalized a_i=n_i-n_s+1 and U=u-g+1,V=v-g+1 with V>=2"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656",
    "MATH-PROGRAMME#3652"
  ],
  "promotion_condition": "Paper mathematical theorem UNDER_REVIEW; bounded independent integer/proof trace checker CHECKED. Full unrestricted #561 OPEN/PARTIAL, no external MATHCERT or historical research priority claim.",
  "claim_id": "ERDOS561-GALLAI-NO-TRIANGLE-SUPPORT-SHARPENING-055",
  "short_name": "Improved s+1 matching lower by excluding factorcritical triangles; sharpen BLUE residual support threshold",
  "claim_text": "UNRESTRICTED-HOST MATCHING LEMMA: Q→(F(a1..as), F(v,g)) with s positive disjoint red stars, two positive disjoint blue stars and Vred=sum_i(ai+1)>=2s+floor(s/2), implies maximum matching nu(Q)>=s+1. Proof: all incident edges at arbitrary vertex blue force red F(a) in Q-x, so nu(Q-x)>=s for every x. If nu(Q)=s, Gallai matching-stability yields nonisolated components factor critical, with total matching s and nonisolated order N=2s+q. Any component with matching1 is exactly triangle K3; colouring it entirely BLUE and all other components RED avoids BLUE two positive stars (triangle has only 3 vertices) and RED s stars (remaining matching capacity s-1), contradiction. Hence all components have matching>=2, so q<=floor(s/2), N<=2s+floor(s/2)<=Vred. Deleting nonisolated vertex cannot retain Vred red target vertices, contradiction. Therefore nu>=s+1. GENERAL JOINT: for sorted original red length s and blue (u,v,g), normalize red a_i=n_i-n_s+1, blue U=u-g+1,V=v-g+1. If V>=2 and sum(ai+1)>=2s+floor(s/2), every arbitrary finite simple JOINT residual host has e>=Jcan-P_BLUE, with EXACT prior all-s positive-part deficit P_BLUE=sum_{i<s}(ai-max(ai+1+V-1, ai+2+U-1 when index exists))_+. Exact canonical JOINT if P_BLUE=0. Monochromatic red/blue matching deletions normalize terminal minima, each cost at least s+1, final BLUE deletion reduces to pinned two-component residual bridge after colour swap. Exact original W requires an independently sourced sufficient transfer, e.g. fifth saturated-core criterion 2W<=D^2+R. No sharp claim for P_BLUE>0 or support below threshold. Old 3s-1 threshold weakened, not a new complete unrestricted joint theorem.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "GALLAI_NO_TRIANGLE_SUPPORT_SHARPENING_THEOREM.md. Core constructive triangle-component avoiding colouring eliminates all ν(C)=1 factor-critical components in any hypothetical matching-stable ν(Q)=s graph; remaining number q of components<=floor(s/2) and nonisolated N=2s+q, incompatible with red vertex support after deleting arbitrary nonisolated vertex. Replaces solely the matching-size support threshold in source claim045 all-s BLUE matching theorem. All other canonical algebra and two-component lower imports unchanged. Sharpness of global all-profile joint and original problem remains OPEN.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/GALLAI_NO_TRIANGLE_SUPPORT_SHARPENING_THEOREM.md",
    "research/erdos-561/joint-general/verify_gallai_no_triangle_support.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md",
    "research/erdos-561/joint-general/RECURSIVE_FIFTH_CORE_VERTEX_SUPPORT_THEOREM.md",
    "research/erdos-561/joint-general/GALLAI_NO_TRIANGLE_SUPPORT_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561; Gallai no-triangle sharpening of unrestricted-host all-s two-blue-star matching lower bound",
  "assumptions": [
    "finite simple unrestricted host, ordinary non-induced vertex-disjoint positive stars",
    "RED s-component forest F(a1,...,as) with s>=3 and required vertex support at least 2s+floor(s/2)",
    "BLUE forest F(v,g) has two positive disjoint stars",
    "for JOINT application original red sorted positive length s; original blue sorted positive (u,v,g); normalized a_i=n_i-n_s+1 and U=u-g+1,V=v-g+1 with V>=2"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3656",
    "MATH-PROGRAMME#3652"
  ],
  "promotion_condition": "Paper mathematical theorem UNDER_REVIEW; bounded independent integer/proof trace checker CHECKED. Full unrestricted #561 OPEN/PARTIAL, no external MATHCERT or historical research priority claim.",
  "claim_id": "ERDOS561-GALLAI-NO-TRIANGLE-SUPPORT-RECURSIVE-CHECK-056",
  "short_name": "Exact bounded no-triangle support improvement and recursive proof-tree monotonic expansion",
  "claim_text": "Independent deterministic arithmetic and proof-trace checker exercises all179928 sorted RED profiles of lengths s3..8, preceding arms 1..8, terminal1 and normalized BLUE U,V in2..8. Old support 177856 vs new 179368 (+1512), old zero BLUE penalty 134447 vs new 135852 (+1405). A source-provenance-preserving monotone composition with the protected fifth-core recursive engine raises exact JOINT certificate count 166589→167485 (+896: 714 direct improved BLUE support, 163 RED matching recursions,19 first-residual original recursions) and ORIGINAL 151885→152446 (+561). Remaining UNKNOWN joint12443 and original27482, not counterexamples. Graph DFS verifies explicit avoiding colouring of s disjoint K3 for s=3..9 with one blue component and red remaining, using true ordinary disjoint positive star embeddings. All checks are finite arithmetic/proof rule execution, not formal proof of Gallai's theorem or mathematical independent certification. Exact-head replay and integrity manifest required.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "verify_gallai_no_triangle_support.py imports protected verify_recursive_fifth_core_certificates.py without modification; performs full 179928-grid monotone recursive classification, counts improved threshold P_BLUE=0 and new cases, checks exact star-host integer maxima from prior source, and tests 7 K3 avoiding colourings by independent vertex-disjoint forest DFS. Nested certificate trace recurses strictly to shorter red original profiles only, retains old provenance and no MATHCERT. Finite integrity and schema checks are distinguished from unbounded paper proof.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_gallai_no_triangle_support.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/GALLAI_NO_TRIANGLE_SUPPORT_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561; factor-critical component order adaptive matching obstruction for all-s RED versus two positive BLUE stars",
  "assumptions": [
    "s>=3, red positive s-component vertex-disjoint star forest A=F(a1,..,as), blue positive TWO-component B=F(v,g)",
    "all host graphs finite and simple; ordinary non-induced vertex-disjoint star-forest embeddings",
    "r=ceil((v+g+1)/2), red vertex support>=2s+floor(s/r)",
    "for JOINT original red n sorted positive length s, original blue (u,v,g) sorted positive; normalized red ai=ni−ns+1, BLUE U=u−g+1,V=v−g+1>=2"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3722"
  ],
  "promotion_condition": "Paper source theorem UNDER_REVIEW; finite arithmetic and recursive source-composition check CHECKED. Full Erdős #561 unrestricted arbitrary-profile OPEN/PARTIAL, no external MATHCERT or historical priority claim.",
  "claim_id": "ERDOS561-BLUE-TARGET-ORDER-ADAPTIVE-MATCHING-057",
  "short_name": "Factor-critical BLUE-target-order adaptive matching support and all-s exact JOINT sufficient criterion",
  "claim_text": "For ANY finite simple Q arrowing RED forest A with s positive disjoint star components against BLUE forest B=F(v,g) with two positive star components, let rho=ceil((v+g+1)/2)>=2 and red vertex support VA=sum(ai+1). If VA>=2s+floor(s/rho), then nu(Q)>=s+1. Proof: all edges incident to arbitrary vertex BLUE force full red A after deleting that vertex. Under hypothetical nu(Q)=s, classical Gallai matching-stability yields all nonisolated components factor-critical of order 2mu+1 with component matching μ>=1, sum μ=s, N=2s+q. If ANY component C had order <VB=v+g+2, colour ALL of C BLUE and other components RED: BLUE cannot contain B by vertex support; RED matching number s−mu(C)<s excludes the s RED star components. Therefore every component has 2mu+1>=VB and μ>=ceil((VB−1)/2)=rho. Hence q<=floor(s/rho), N<=2s+floor(s/rho)<=VA; deleting a nonisolated vertex leaves too few vertices for red A, contradiction. For original red n and BLUE (u,v,g), normalized second residual F(V,1) has rhoV=ceil((V+2)/2)=floor((V+3)/2). If V>=2 and normalized red sum(ai+1)>=2s+floor(s/rhoV), the SOURCE-LOCKED single BLUE matching theorem remains valid with identical nonnegative explicit interference penalty P_BLUE=sum_(i<s)(ai−max(ai+1+V−1,ai+2+U−1 if exists))_+. Thus any JOINT host e>=Jcan−P_BLUE and P_BLUE=0 proves exact unrestricted-host JOINT. ORIGINAL exactness still requires a separate protected core transfer; no claims for positive deficit or smaller support. This improves the parent no-triangle fixed support threshold 2s+floor(s/2), and full original #561 remains OPEN.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "UNDER_REVIEW",
  "certainty": "PROVED_NOT_FORMALIZED",
  "support_type": "HUMAN_PROOF",
  "support_summary": "BLUE_ORDER_ADAPTIVE_GALLAI_SUPPORT_THEOREM.md Theorem V: exclude *all* too-small factorcritical components by colouring one whole component blue and remaining components red, using target vertex order VB. For ν=s stable graph every nonisolated component matching>=rho, so N=2s+q<=2s+floor(s/rho), incompatible with red target support after any vertex deletion. Corollary W specializes to normalized BLUE second residual F(V,1), uniformly decrementing RED/BLUE minima and invoking earlier source two-component residual bridge and exact positive-part algebra. Mathematical proof is unbounded in s, but remains UNDER_REVIEW; finite checks not substitute.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/BLUE_ORDER_ADAPTIVE_GALLAI_SUPPORT_THEOREM.md",
    "research/erdos-561/joint-general/verify_blue_order_adaptive_gallai.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/GALLAI_NO_TRIANGLE_SUPPORT_SHARPENING_THEOREM.md",
    "research/erdos-561/joint-general/ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md",
    "research/erdos-561/joint-general/BLUE_ORDER_ADAPTIVE_GALLAI_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})
claims.append({
  "mathematical_domain": "Erdős #561; factor-critical component order adaptive matching obstruction for all-s RED versus two positive BLUE stars",
  "assumptions": [
    "s>=3, red positive s-component vertex-disjoint star forest A=F(a1,..,as), blue positive TWO-component B=F(v,g)",
    "all host graphs finite and simple; ordinary non-induced vertex-disjoint star-forest embeddings",
    "r=ceil((v+g+1)/2), red vertex support>=2s+floor(s/r)",
    "for JOINT original red n sorted positive length s, original blue (u,v,g) sorted positive; normalized red ai=ni−ns+1, BLUE U=u−g+1,V=v−g+1>=2"
  ],
  "knowledge_graph_refs": [
    "MATH-PROGRAMME#3490",
    "MATH-PROGRAMME#3722"
  ],
  "promotion_condition": "Paper source theorem UNDER_REVIEW; finite arithmetic and recursive source-composition check CHECKED. Full Erdős #561 unrestricted arbitrary-profile OPEN/PARTIAL, no external MATHCERT or historical priority claim.",
  "claim_id": "ERDOS561-BLUE-ORDER-ADAPTIVE-RECURSIVE-CHECK-058",
  "short_name": "Adaptive BLUE vertex-order support increases exact recursive three-BLUE proof certificates",
  "claim_text": "In deterministic full fixed179928-grid RED s3..8, prefix arm1..8 terminal1, BLUE U,V2..8, previous source-proved fixed no-triangle support qualifies179368 and its P_BLUE=0 region135852. BLUE-order adaptive support qualifies179635 (+267) and P_BLUE=0 region136118 (+266). A monotone source-premise-preserving recursive proof-tree extension built on protected fifth-core and fixed no-triangle engines raises exact JOINT certified by theorem composition 167485→167601 (+116, 97 direct adaptive matching zero deficit and19 red-matching recursion) and exact ORIGINAL 152446→152494 (+48). 12327 JOINT and27434 ORIGINAL remain UNKNOWN in this finite grid, not counterexamples. The deterministic program validates integer support orders, prior 179928-profile index identities and matching loss, monotone retention of every old proof, and new proof-trace dependency trees. No claim of MATHCERT or independent formalization; paper theorem remains UNDER_REVIEW.",
  "claim_class": "PROVED_IN_PACKAGE",
  "status": "CHECKED",
  "certainty": "CERTIFIED",
  "support_type": "EXACT_RATIONAL_COMPUTATION",
  "support_summary": "verify_blue_order_adaptive_gallai.py imports the exact source-locked verify_gallai_no_triangle_support.py parent; evaluates upgraded support threshold rhoV=floor((V+3)/2), all 179928 sorted profiles, old and new proof classes and their well-founded strictly shorter red matching/first residual dependents. Exact finite count 267 newly supported and 266 zero deficit; source-derived extra JOINT116 ORIGINAL48. Standard-library deterministic; source theorem is separate paper proof pending review.",
  "source_or_artifact": [
    "research/erdos-561/joint-general/verify_blue_order_adaptive_gallai.py"
  ],
  "related_files": [
    "research/erdos-561/joint-general/BLUE_ORDER_ADAPTIVE_GALLAI_EVIDENCE.json",
    "research/erdos-561/joint-general/RUN_MATRIX.md"
  ]
})

claims.append(dict(common,
  claim_id='ERDOS561-JOINT-4111-321-PAPER-059',
  short_name='Exact 15-edge arbitrary-host joint residual for original (4,1,1,1) against (3,2,1)',
  claim_text='If a finite simple Q simultaneously arrows (3K2,F(3,2,1)) and (F(4,1,1,1),F(2,1)), then e(Q)>=15; the disjoint-star host F(5,4,3,2,1) attains equality. Exact canonical JOINT=15 vs separate residual maxima 14 (switching surplus 1). The general unrestricted s,t conjecture and this ORIGINAL size Ramsey pair remain open under this claim.',
  claim_class='PROVED_IN_PACKAGE',
  status='UNDER_REVIEW',
  certainty='PROVED_NOT_FORMALIZED',
  support_type='HUMAN_PROOF',
  support_summary='Two-vertex RED-cover deletion of the first arrow and one-vertex BLUE-cover deletion of the second give e>=degree(u)+10, max degree<=4 under e<=14, and >=12 nonisolated vertices. Classical Tutte designated-vertex matching criterion forces >=5 degree-four vertices when no (3,1) cap partition exists. Handshake forces exactly five saturated core vertices and outside total degree eight. At most four core edges can be missing; if any is missing, an external core edge plus a K4 two-edge matching covers all five saturated vertices, avoiding the second arrow. Otherwise an isolated K5 plus four outside edges has an explicit avoiding colouring. The 15-edge host arrows both pairs by two elementary host-star case splits. Independent finite witnesses corroborate but do not replace the Tutte premise.',
  source_or_artifact=[root+'JOINT_4111_321_MATCHING_CORE_THEOREM.md'],
  related_files=[root+'verify_joint15_4111_321.py',root+'JOINT_4111_321_MATCHING_CORE_EVIDENCE.json',root+'RUN_MATRIX.md']
))
claims.append(dict(common,
  claim_id='ERDOS561-JOINT-4111-321-FINITE-060',
  short_name='Finite independent upper-host and missing-five-core matching checks',
  claim_text='The canonical five-star 15-edge host F(5,4,3,2,1) passes both exact residual arrow relations in each of 720 host-arm red count allocations and all 32768 individual edge-colouring masks. Every one of 385 missing-core configurations with one to four missing edges on the degree-four five-core has a constructive matching of the other four core vertices and at least one missing-incident core vertex eligible for an external matching edge. These finite checks do not claim global unrestricted arrow-host enumeration or proof of designated-vertex Tutte.',
  claim_class='PROVED_IN_PACKAGE',
  status='CHECKED',
  certainty='CERTIFIED',
  support_type='EXACT_RATIONAL_COMPUTATION',
  support_summary='Independent enumeration-by-permutation of 720 vectors, bitmask-state dynamic matching of 32768 concrete individual edge colourings, 385 complete missing-core subgraph cases with 3 K4 perfect matching options, and deterministic byte-identical JSON evidence. The verifier is standard-library only, retains full two-colour scope for the upper host, and labels this finite proof boundary.',
  source_or_artifact=[root+'verify_joint15_4111_321.py'],
  related_files=[root+'JOINT_4111_321_MATCHING_CORE_EVIDENCE.json',root+'JOINT_4111_321_MATCHING_CORE_THEOREM.md']
))

claims.append(dict(common,
  claim_id='ERDOS561-4111-321-INFINITE-ORIGINAL-061',
  short_name='Unbounded exact JOINT 2a+7 and ORIGINAL 3a+9 for (a,1,1,1) versus (3,2,1)',
  claim_text='For every integer a>=4 and arbitrary finite simple host, exact JOINT residual value for red (a,1,1,1) and blue (3,2,1) is 2a+7. For every integer a>=5, exact ORIGINAL asymmetric size Ramsey value is 3a+9. The a=4 ORIGINAL formula remains unproved by this argument; full Erdős #561 remains OPEN.',
  claim_class='PROVED_IN_PACKAGE',status='UNDER_REVIEW',certainty='PROVED_NOT_FORMALIZED',
  support_type='HUMAN_PROOF',
  support_summary='For hypothetical JOINT at 2a+6, two opposite vertex deletion colourings imply Δ<=a, nonisolated support N>=a+8, and lack of an avoiding colour (all BLUE edges a matching) implies no matching saturates degree-a vertices. The classical marked Tutte criterion with saturated-component boundary r(a-r+1)>=a forces >=a+1 such vertices; 2e>=N+(a-1)(a+1)=a²+a+7>4a+12 for a>=5. For a=4 use the preceding separate five-core proof. To transfer to ORIGINAL at a>=5: JOINT deletion bounds Δ<=a+1, Vizing plus cap splitting forces Δ=a+1 and the source-proved ordinary Lovasz saturated-core lemma forces >=a+2 vertices of degree a+1. All-red support N>=a+7 then yields 2e>=a²+3a+7>6a+16=2(W-1), with W=3a+9. Canonical original disjoint-star upper construction attains W. No use of unresolved general JOINT.',
  source_or_artifact=[root+'JOINT_4111_321_MATCHING_CORE_THEOREM.md', 'research/erdos-561/formal-graph/LOVASZ_CAP_PARTITION_BRIDGE.md'],
  related_files=[root+'verify_joint15_4111_321.py',root+'JOINT_4111_321_MATCHING_CORE_EVIDENCE.json']
))
claims.append(dict(common,
  claim_id='ERDOS561-4111-321-FAMILY-UPPER-AUDIT-062',
  short_name='Finite original-host and integer family regression',
  claim_text='Exact original canonical upper star-host arrowing verified for a=4,5,6,7 for the pair (a,1,1,1) versus (3,2,1), with all 42480 red allocation vectors and independent DP star matching; verifies antidiagonal weights (a+2,a+1,a,3,2,1), JOINT 2a+7, ORIGINAL 3a+9, and both threshold inequalities for integer a=5..100. Bounded checks do not prove the infinite theorem.',
  claim_class='PROVED_IN_PACKAGE',status='CHECKED',certainty='CERTIFIED',
  support_type='EXACT_RATIONAL_COMPUTATION',
  support_summary='Standard-library deterministic direct allocations and independent bitmask dynamic programming, source-locked and JSON persisted; 5040+8064+12096+17280=42480 original upper red-count vectors. Universal all-host lower is a separate paper proof via specified-vertex Tutte, Lovasz and Vizing.',
  source_or_artifact=[root+'verify_joint15_4111_321.py'],
  related_files=[root+'JOINT_4111_321_MATCHING_CORE_EVIDENCE.json',root+'JOINT_4111_321_MATCHING_CORE_THEOREM.md']
))
Path('CLAIM_LEDGER.json').write_text(json.dumps({'schema_version':'1.1.0','ledger_contract':'canonical_claim_ledger','ledger_id':'ERDOS561-JOINT-GENERAL-20261119','claims':claims},indent=2,ensure_ascii=False)+'\n')
print('CANONICAL_CLAIMS',len(claims))
