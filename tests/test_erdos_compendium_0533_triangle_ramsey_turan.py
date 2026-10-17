"""Exact small-graph Ramsey--Turan semantics for disproved Erdős #533.

K5-free dense complete multipartite examples do NOT themselves refute the
asymptotic statement because their alpha_3 remains linear.
"""
from fractions import Fraction as F
from itertools import combinations


def multipartite(sizes):
    parts=[]
    k=0
    for size in sizes:
        parts.append(tuple(range(k,k+size)))
        k+=size
    edges=set()
    for i,part in enumerate(parts):
        for other in parts[i+1:]:
            for u in part:
                for v in other:
                    edges.add((u,v) if u<v else (v,u))
    return k,edges,parts


def is_clique(vertices, edges):
    return all((min(u,v),max(u,v)) in edges
               for u,v in combinations(vertices,2))


def is_triangle_free(vertices,edges):
    return not any(is_clique(tri,edges)
                   for tri in combinations(vertices,3))


def max_clique_size(n,edges):
    return max((size for size in range(n+1)
                if any(is_clique(S,edges)
                       for S in combinations(range(n),size))))


def alpha3(n,edges):
    best=0
    for size in range(n+1):
        if any(is_triangle_free(S,edges)
               for S in combinations(range(n),size)):
            best=size
    return best


def alpha3_independent_bitmask(n,edges):
    def edge(u,v):
        return (min(u,v),max(u,v)) in edges
    triangles=[
        (1<<a)|(1<<b)|(1<<c)
        for a,b,c in combinations(range(n),3)
        if edge(a,b) and edge(a,c) and edge(b,c)
    ]
    return max(mask.bit_count() for mask in range(1<<n)
               if not any((mask&t)==t for t in triangles))


def test_533_explicit_eight_vertex_K5_free_graph():
    n,edges,parts=multipartite((2,2,2,2))
    assert n==8
    assert len(edges)==24
    assert max_clique_size(n,edges)==4
    assert not any(is_clique(x,edges) for x in combinations(range(n),5))
    assert alpha3(n,edges)==alpha3_independent_bitmask(n,edges)==4
    assert F(len(edges),n*n)==F(3,8)
    # alpha3=n/2 here, so NOT an asymptotic counterexample.


def test_533_complete_multipartite_alpha3_is_two_largest_parts():
    for sizes in ((1,1,1,1),(1,2,3,4),(2,1,2,2),(2,2,3)):
        n,edges,parts=multipartite(sizes)
        assert max_clique_size(n,edges)==len(parts)
        assert alpha3(n,edges)==sum(sorted(sizes)[-2:])
        assert alpha3_independent_bitmask(n,edges)==alpha3(n,edges)
        assert len(edges)==(n*n-sum(x*x for x in sizes))//2


def test_533_triangle_free_vs_independent_and_K5_free_distinct():
    n,edges,_=multipartite((2,2,2,2))
    # Largest independent set is one part of size 2, while largest
    # induced triangle-free set consists of two parts and has size 4.
    assert max(size for size in range(n+1)
               if any(all(not is_clique(pair,edges)
                          for pair in combinations(S,2))
                      for S in combinations(range(n),size))) == 2
    assert alpha3(n,edges)==4
    # The empty graph also satisfies the predicate but has no edge density.
    assert alpha3(5,set())==5
    assert max_clique_size(5,set())==1


def test_533_exact_density_denominator_factor_two():
    lower_balogh=F(1,64)
    sharp_in_n_squared=F(1,12)
    rho_in_n_choose_two=F(1,6)
    assert 2*sharp_in_n_squared==rho_in_n_choose_two
    assert 2*lower_balogh==F(1,32)
    assert F(1,128)<lower_balogh<sharp_in_n_squared
    # For n large, e/n^2 = (e/binom(n,2))*((n-1)/(2n)).
    for n in range(5,30):
        e=n*(n-1)//2
        assert F(e,n*n) == F(e,e)*F(n-1,2*n)
    # Actual asymptotic K5-free counterexamples require alpha3=o(n).
