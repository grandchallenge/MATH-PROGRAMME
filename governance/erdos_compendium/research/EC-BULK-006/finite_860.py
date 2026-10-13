#!/usr/bin/env python3
"""Finite exact Hall/matching fixtures for Erdős #860; not asymptotic proof.

Conventions: h_closed(n) uses (m,m+H] = {m+1,...,m+H};
modern problem's literal open (m,m+h) has h_open(n)=h_closed(n)+1.
Only positive integer n, and prime moduli <= n.
"""
import json
from math import prod, isqrt


def primes_upto(n):
    return [p for p in range(2,n+1) if all(p%d for d in range(2,isqrt(p)+1))]


def matched(primes, m, H):
    # Kuhn augmenting paths on the bipartite divisibility graph.
    owner = [-1] * H
    def augment(i, seen):
        for j in range(H):
            if (m+j+1) % primes[i] == 0 and j not in seen:
                seen.add(j)
                if owner[j] == -1 or augment(owner[j],seen):
                    owner[j] = i
                    return True
        return False
    return all(augment(i,set()) for i in range(len(primes)))


def hall(primes,m,H):
    # Independent exhaustive Hall subset criterion, no matching search.
    for mask in range(1,1<<len(primes)):
        ps=[p for i,p in enumerate(primes) if (mask>>i)&1]
        union=sum(any((m+j)%p==0 for p in ps) for j in range(1,H+1))
        if union < len(ps):
            return False
    return True


def run(n):
    ps=primes_upto(n);period=prod(ps)
    records=[]
    for m in range(period):
        H=1
        while not matched(ps,m,H):
            H+=1
            assert H<=5*n+20,(n,m,H)
        assert hall(ps,m,H) and (H==1 or not hall(ps,m,H-1)),(n,m,H)
        records.append(H)
    worst=max(records)
    witnesses=[m for m,h in enumerate(records) if h==worst]
    assert all(matched(ps,m,worst) for m in range(period))
    assert not hall(ps,witnesses[0],worst-1)
    return {'n':n,'primes':ps,'primorial_period':period,'h_closed':worst,
            'h_literal_open':worst+1,'worst_residue_count':len(witnesses),
            'worst_residue_sample':witnesses[:10],
            'matching_and_hall_crosschecks':period}


def main():
    cases=[run(n) for n in (2,3,5,7,11)]
    print(json.dumps({'record_type':'EC_BULK_006_860_FINITE/1',
                      'authority':'FINITE_PERIODIC_HALL_CHECK_ONLY',
                      'conventions':'closed right endpoint versus literal open interval',
                      'cases':cases},indent=2))

if __name__=='__main__':main()
