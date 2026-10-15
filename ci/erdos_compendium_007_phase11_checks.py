#!/usr/bin/env python3
"""Exact finite witnesses for #1103–#1108, not proofs of asymptotic claims."""
import itertools,json,math
from functools import lru_cache


def sqfree(n):
    if n<=0:return False
    p=2
    while p*p<=n:
        if n%(p*p)==0:return False
        p+=1
    return True


def a_plus_a():
    universe=range(1,45)
    for A in itertools.combinations(universe,4):
        sums={a+b for a in A for b in A}
        if all(sqfree(x) for x in sums):
            return {'example_A':list(A),'A_plus_A':sorted(sums),
                    'all_squarefree':True,'no_infinite_sequence_claim':True}
    raise AssertionError('no witness')


def chromatic(vertices, edges):
    adjacent=[set() for _ in range(vertices)]
    for i,j in edges:
        adjacent[i].add(j);adjacent[j].add(i)
    order=sorted(range(vertices),key=lambda x:-len(adjacent[x]))
    def possible(k):
        colors=[-1]*vertices
        def dfs(t):
            if t==vertices:return True
            v=order[t]
            forbidden={colors[u] for u in adjacent[v]}
            for c in range(k):
                if c not in forbidden:
                    colors[v]=c
                    if dfs(t+1):return True
                    colors[v]=-1
            return False
        return dfs(0)
    return next(k for k in range(1,vertices+1) if possible(k))


def mycielski():
    # Start with C5 and apply Mycielski construction.
    E={tuple(sorted((i,(i+1)%5))) for i in range(5)}
    H=set(E)
    for i,j in E:
        H.add(tuple(sorted((i,j+5))))
        H.add(tuple(sorted((j,i+5))))
    H|={(i+5,10) for i in range(5)}
    assert len(H)==20 and len({*H})==20
    triangles=sum(all(tuple(sorted(z)) in H for z in itertools.combinations(Q,2))
                  for Q in itertools.combinations(range(11),3))
    assert triangles==0
    assert chromatic(5,E)==3
    assert chromatic(11,H)==4
    return {'C5_vertices':5,'C5_chromatic':3,'Mycielskian_vertices':11,
            'Mycielskian_edges':20,'triangles':triangles,'chromatic':4}


def rainbow_triangle_colouring(n):
    # Color edge {i,j} by min(i,j). Any triangle has two equal-colored edges.
    c={(i,j):i for i,j in itertools.combinations(range(n),2)}
    assert len(set(c.values()))==n-1
    assert all(len({c[tuple(sorted(e))] for e in itertools.combinations(tri,2)})<3
               for tri in itertools.combinations(range(n),3))
    return {'vertices':n,'edge_colors':n-1,'rainbow_triangles':0,
            'bounded_lower_witness_only':True}


def prime_factors(n):
    ans=[];p=2
    while p*p<=n:
        if n%p==0:
            ans.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:ans.append(n)
    return ans


def partition_numbers(N):
    p=[0]*(N+1);p[0]=1
    for k in range(1,N+1):
        for n in range(k,N+1):p[n]+=p[n-k]
    union=set()
    rows=[]
    for n in range(1,N+1):
        union.update(prime_factors(p[n]))
        rows.append({'n':n,'p_n':p[n],'F_n':len(union)})
    assert [p[n] for n in range(1,11)]==[1,2,3,5,7,11,15,22,30,42]
    return {'rows':rows,'distinct_prime_divisors_up_to_N':sorted(union)}


def rpowerful(n,r):
    return all(e>=r for e in factor_exponents(n))


def factor_exponents(n):
    exps=[];p=2
    while p*p<=n:
        if n%p==0:
            a=0
            while n%p==0:n//=p;a+=1
            exps.append(a)
        p+=1
    if n>1:exps.append(1)
    return exps


def powerful_sums():
    vals=[n for n in range(1,201) if rpowerful(n,2)]
    rep={a+b for a in vals for b in vals if a+b<=120}
    rep.update(a for a in vals if a<=120)
    rep.update(a+b+c for a in vals for b in vals for c in vals if a+b+c<=120)
    missing=sorted(set(range(1,121))-rep)
    assert 7 in missing and 6 in rep
    return {'r':2,'positive_r_powerful_up_to_200':vals,
            'unrepresented_up_to_120_by_at_most_3_positive_terms':missing,
            'small_exceptions_do_not_disprove_eventually':True}


def factorial_sums():
    powers=[math.factorial(k) for k in range(1,8)]
    sums={sum(t) for n in range(8) for t in itertools.combinations(powers,n)}
    sq=sorted(x for x in sums if x>0 and math.isqrt(x)**2==x)
    powerful=sorted(x for x in sums if x>0 and rpowerful(x,2))
    assert len(sums)==128
    return {'factorials_1_to_7':powers,'distinct_subset_sums':len(sums),
            'positive_squares':sq,'positive_powerful':powerful,
            'finite_window_only':True}


def main():
    r={'record_type':'EC_BULK_007_FINITE_ARITHMETIC_PHASE_11/1',
       'cohort_id':'EC-BULK-007','mathematical_certification':False,
       'problem_1103':a_plus_a(),
       'problem_1104':mycielski(),
       'problem_1105':rainbow_triangle_colouring(6),
       'problem_1106':partition_numbers(25),
       'problem_1107':powerful_sums(),
       'problem_1108':factorial_sums(),
       'result':'FINITE_CHECKS_PASS'}
    print(json.dumps(r,indent=2))


if __name__=='__main__':main()
