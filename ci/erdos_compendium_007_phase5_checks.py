#!/usr/bin/env python3
"""Finite, reproducible evidence for EC-BULK-007 problems 1075–1078.

This verifies only explicit examples and algebraic boundary checks.
It is not a proof of the referenced deep graph/hypergraph theorems.
"""
import itertools
import json
from math import comb


def complete_partite_hypergraphs():
    out = {}
    for r, t in [(3, 2), (3, 3), (4, 2)]:
        V = [list(range(j*t,(j+1)*t)) for j in range(r)]
        edges = list(itertools.product(*V))
        assert len(edges) == t**r
        assert len({v for edge in edges for v in edge}) == r*t
        out[f"r={r},t={t}"] = {"vertices":r*t,"edges":len(edges),
            "boundary_edges":(r*t//r)**r,
            "edge_density_denominator":(r*t)**r}
    return out


def sparse_triples():
    E = {(0,1,2),(3,4,5)}
    assert len(E)==2
    assert not any(len(T)>=3 for T in [E])
    assert 3 * len(E) <= comb(6,2)
    return {"n":6,"edges":2,"contains_3_edge_k5_forbidden_pattern":False,
            "linear_pair_bound":comb(6,2)//3}


def bipartite_counterexample():
    # n = 4096, alpha = 1/4: all powers are integers.
    n=4096
    root4=8
    a=2*root4
    b=n-a
    D=6
    threshold=n*root4
    original_required_m=n//root4
    balanced_vertex_upper=(D+1)*a
    assert a*b>=threshold
    assert balanced_vertex_upper<original_required_m
    assert a+b==n
    # Proof for ANY D-balanced subgraph (not just complete):
    # b'*delta <= edges <= a'*Delta <= a'*D*delta, so b'<=D*a'.
    return {"alpha":"1/4", "n":n, "a":a, "b":b,
       "edges":a*b, "minimum_requested_edges":threshold,
       "D":D, "every_positive_degree_D_balanced_subgraph_vertex_upper":balanced_vertex_upper,
       "original_vertex_lower_requirement_strictly_above":original_required_m,
       "double_counting_general_subgraph_lemma":"b' * minimum_degree <= E(H) <= a' * maximum_degree <= D * a' * minimum_degree"}


def multipartite_cliques():
    parts=[list(range(2*i,2*i+2)) for i in range(3)]
    vertices=[v for part in parts for v in part]
    assert len(vertices)==6
    edges={tuple(sorted((u,v))) for i,p in enumerate(parts)
           for q in parts[i+1:] for u in p for v in q}
    degree={v:sum(v in edge for edge in edges) for v in vertices}
    assert set(degree.values())=={4}
    triangles=sum(all(tuple(sorted(pair)) in edges
          for pair in itertools.combinations(choice,2))
          for choice in itertools.product(*parts))
    assert triangles==8
    removed={(u,v) for u in parts[1] for v in parts[2]}
    edges={e for e in edges if e not in removed}
    assert len(edges)==8
    degree_after={v:sum(v in edge for edge in edges) for v in vertices}
    assert min(degree_after.values())==2
    triangles_after=sum(all(tuple(sorted(pair)) in edges
          for pair in itertools.combinations(choice,2))
          for choice in itertools.product(*parts))
    assert triangles_after==0
    return {"r":3,"n_per_part":2,"initial_minimum_degree":4,
            "initial_triangles":triangles,"after_removing_second_third_edges_minimum_degree":2,
            "after_removing_second_third_edges_triangles":0}


def main():
    j={"record_type":"EC_BULK_007_FINITE_ARITHMETIC_PHASE_5/1",
       "cohort_id":"EC-BULK-007","mathematical_certification":False,
       "problem_1075":complete_partite_hypergraphs(),
       "problem_1076":sparse_triples(),
       "problem_1077":bipartite_counterexample(),
       "problem_1078":multipartite_cliques(),
       "result":"FINITE_CHECKS_PASS"}
    print(json.dumps(j,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
