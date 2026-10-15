RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0916-S01
PROBLEM_ID: 916
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For finite simple undirected graph G with n vertices and >=2n−2 edges, there exists a SIMPLE cycle C and vertex v NOT on C which is adjacent to at least THREE DISTINCT vertices of C. This is a special K4 subdivision with THREE UNSUBDIVIDED spokes, not merely existence of an arbitrary homeomorph of K4. Non-induced cycles allowed. Exact equality 2n−2 is enough; monotonicity in added edges extends to >=. Meaningful graph order n>=4.

## Dated status and primary evidence
Original Erdős [Er67b] and Dirac [Di60]: G.A. Dirac 'In abstrakten Graphen vorhandene vollständige 4-Graphen und ihre Unterteilungen', Math. Nachr. (1960)61–85 proves weaker K4 topological subdivision. FULL PROVED result C. Thomassen, 'A minimal condition implying a special K4-subdivision in a graph', Archiv der Mathematik (Basel) 25 (1974)210–215 DOI10.1007/BF01238666. Exact bibliographic https://www.erdosproblems.com/latex/916 and external indexing https://openurl.ebsco.com/results?bquery=AU+Thomassen%2C+Carsten&page=1&sid=ebsco%3Aocu_results%3Acache verifies citation. Maintained https://www.erdosproblems.com/916 PROVED as of source audit 2026-10-15, original frozen 2025-08-31 also PROVED; formalised statement metadata No, no protected GCL Lean theorem. Original full six-page Thomassen proof NOT independently replayed. Later C Thomassen and B Toft, 'Non-separating induced cycles in graphs', JCT B31(1981)199–224 DOI10.1016/S0095-8956(81)80025-1 explicitly cites earlier result and develops stronger related statements. 2023 graph-decomposition literature reports Thomassen also characterized 2n−3-edge obstruction families by K3/K3,3 cockades; that stronger characterization requires a direct original theorem/source audit.

## Strongest verified interface
Witness checker: enumerate simple cycles C with distinct vertices and edges, then outside v with |N(v)∩V(C)|>=3. Independent exact CHAD finite_916_917.py/json exhausts all 33866 labelled simple graphs orders n2..6, filters 5001 graphs with m>=2n−2, finds valid cycle/outside vertex witness in every one; no finite counterexamples. SHARP family for every n>=4: two central adjacent vertices u,w plus n−2 independent peripheral vertices each joined to both centers has precisely 1+2(n−2)=2n−3 edges and no special witness; all cycles are 3- or 4-cycles, outside neighbors at most two cycle vertices. Fixture explicitly verifies n4..7. This finite result and elementary sharpness are independent GCL proofs; they do NOT establish Thomassen1974 all n or structural cockade theorem.

## Proposed bounded successor task
Formalize source-normalized cycle+outside-vertex predicate and lemma that its witness yields special K4 subdivision with three undivided spokes, graph may have extra edges. Acceptance complete paper proof or pinned no-sorry Lean compilation plus literal axiom report, exact 5001 graph witness replay and sharp obstruction family n4..7; reject invalid witness with repeated cycle vertices, outside vertex on cycle or fewer than 3 spokes. Substantive independent task: inspect full Thomassen 1974 six-page proof and exact 2n−3 obstruction classification, prove/generalize structural lemma without confusing Dirac's weaker topological subdivision. Stop before attributing independent GCL proof of universal theorem without actual full source proof/Lean.

## Prerequisites and blocker
Thomassen full 1974 theorem and proof page images not independently checked in this run; original Erdős [Er67b] full historical page not independently page-reviewed. No accepted protected mathematical reviewer, GCL Lean kernel or live public rendering.

## Reuse and claim boundary
Reused published Dirac1960/Thomassen1974 and 1981 primary evidence and current catalogue; independently finite-verified exact witness and sharpness construction, source-grounded complete six-section article. This comment is editorial research evidence, NOT proof novelty, independently certified full 1974 theorem, protected main merge, formal validation or V2 admission.
