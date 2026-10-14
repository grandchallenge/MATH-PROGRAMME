#!/usr/bin/env python3
"""Independent finite certificates for EC-BULK-006 Erdős 873 and 874.
No asymptotic theorem is certified by these finite tests.
"""
import itertools, math, functools, json, hashlib


def lcm_window_max_by_subsets(X,k):
    best=0; witness=()
    for mask in range(1<<(X-1)):
        A=[j+1 for j in range(X-1) if mask>>j&1]
        score=sum(math.lcm(*A[i:i+k])<X for i in range(len(A)-k+1))
        if score>best: best,witness=score,tuple(A)
    return best,list(witness)


def lcm_window_max_by_dp(X,k):
    @functools.lru_cache(None)
    def opt(tail):
        last=tail[-1] if tail else 0
        best=0
        for x in range(last+1,X):
            inc=int(len(tail)==k-1 and math.lcm(*(tail+(x,)))<X)
            best=max(best,inc+opt((tail+(x,))[-(k-1):]))
        return best
    return opt(())


def admissible_direct(A):
    by_sum={}
    for r in range(1,len(A)+1):
        for tup in itertools.combinations(A,r):
            s=sum(tup)
            if s in by_sum and by_sum[s]!=r: return False
            by_sum[s]=r
    return True


def admissible_max_by_direct(N):
    best=0; witness=[]; count=0
    for mask in range(1<<N):
        A=[i+1 for i in range(N) if mask>>i&1]
        if len(A)<best:continue
        if admissible_direct(A):
            count+=1
            if len(A)>best:best,witness=len(A),A
    return best,witness


def admissible_max_by_incremental(N):
    best=0; witness=[]; nodes=0
    def walk(x,subset,by_sum):
        nonlocal best,witness,nodes
        nodes+=1
        if len(subset)>best: best,witness=len(subset),subset
        if x>N: return
        walk(x+1,subset,by_sum)
        extra={}
        for s,r in by_sum.items():
            y=s+x
            if y in by_sum and by_sum[y]!=r+1:return
            if y in extra and extra[y]!=r+1:return
            extra[y]=r+1
        walk(x+1,subset+[x],by_sum|extra)
    walk(1,[],{0:0})
    return best,witness,nodes


def top_tail_k(N):
    k=0
    while (k+2)**2 <= 4*N+1:k+=1
    return k


def valuation_checks():
    count=0
    for k in range(2,9):
        for vals in itertools.combinations_with_replacement(range(5),k):
            pair=sum(min(vals[i],vals[j]) for i in range(k) for j in range(i+1,k))
            for t in range(k+1):
                assert t*sum(vals)-pair <= (t*(t+1)//2)*max(vals)
                count+=1
    return count


def run():
    lcm=[]
    for X in [8,10,12,14]:
        for k in [2,3,4,5]:
            a,w=lcm_window_max_by_subsets(X,k)
            b=lcm_window_max_by_dp(X,k)
            assert a==b,(X,k,a,b)
            lcm.append(dict(X=X,k=k,maximum=a,witness=w))
    admiss=[]
    for N in range(1,37):
        a,w,nodes=admissible_max_by_incremental(N)
        k=top_tail_k(N)
        assert admissible_direct(list(range(N-k+1,N+1)))
        if N<=14:
            b,_=admissible_max_by_direct(N)
            assert a==b,(N,a,b)
        admiss.append(dict(N=N,maximum=a,top_tail=k,witness=w,incremental_nodes=nodes,equals_tail=a==k))
    return {'scope':'offline exact finite checks only','873':lcm,'874':admiss,'valuation_cases':valuation_checks(), 'all_tests_passed':True}

if __name__=='__main__':
    receipt=run()
    p=__file__.replace('.py','.json')
    with open(p,'w') as f:json.dump(receipt,f,indent=2,sort_keys=True)
    print(json.dumps({'873':[(r['X'],r['k'],r['maximum']) for r in receipt['873']], '874':[(r['N'],r['maximum'],r['top_tail']) for r in receipt['874']], 'valuation_cases':receipt['valuation_cases']}))
