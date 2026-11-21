#!/usr/bin/env python3
"""Exact bounded checks for 211 versus (b,c,c,c) joint-residual rigidity family.

All-host lower bound comes from the existing analytic single-matching rigidity
theorem, not from this star-host colour enumeration or finite parameter range.
"""
from itertools import product
from collections import Counter

def diagonal(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==k)
                 for k in range(len(n)+len(m)-1))

def diagonal_independent(n,m):
    return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1) if 1<=k-i<=len(m))
                 for k in range(2,len(n)+len(m)+1))

def contains(arms,target):
    arms=sorted((x for x in arms if x),reverse=True)
    target=sorted(target,reverse=True)
    return len(arms)>=len(target) and all(a>=b for a,b in zip(arms,target))

counts=Counter()
for c in range(1,16):
    for b in range(c+1,c+25):
        n=(2,1,1);m=(b,c,c,c)
        w=diagonal(n,m)
        assert w==diagonal_independent(n,m)==(b+1,b,b,c+1,c,c)
        A=diagonal(n[1:],m)
        B=diagonal(n,m[1:])
        assert A==diagonal_independent(n[1:],m)==(b,b,c,c,c)
        assert B==diagonal_independent(n,m[1:])==(c+1,c+1,c+1,c,c)
        assert (sum(w[1:]),sum(w),sum(A),sum(B))==(2*b+3*c+1,3*b+3*c+2,2*b+3*c,5*c+3)
        lower=(b,b,c,c,c)
        upper=(b,b,c+1,c,c)
        red=(0,0,1,1,1)
        blue=(b,b,c-1,c-1,c-1)
        assert not contains(red,n)
        assert not contains(blue,m[1:])
        counts['parameter_pairs']+=1
        if b>=c+2:
            assert sum(w[1:])-max(sum(A),sum(B))==1
            counts['strict_switch']+=1
        else:
            assert b==c+1 and sum(w[1:])==max(sum(A),sum(B))
            counts['zero_switch']+=1
        if b<=c+4 and c<=6:
            for r in product(*(range(x+1) for x in lower)):
                blue=tuple(h-x for x,h in zip(r,lower))
                assert contains(r,n[1:]) or contains(blue,m),('lower_A',b,c,r)
                counts['lower_A_colourings']+=1
            for r in product(*(range(x+1) for x in upper)):
                blue=tuple(h-x for x,h in zip(r,upper))
                assert contains(r,n[1:]) or contains(blue,m),('upper_A',b,c,r)
                assert contains(r,n) or contains(blue,m[1:]),('upper_B',b,c,r)
                counts['upper_both_colourings']+=1
        if b%2==1:
            W=sum(w)
            if b>=5:
                assert W<=b*(b+1)
            else:
                assert b==3 and c in (1,2)
            counts['odd_b']+=1
        else:
            E=sum(w)-1
            M=b+3*c
            if b==2:
                assert c==1 and W==11
                counts['even_b_d2']+=1
            else:
                R=M+4
                assert 2*E-R < (b-1)*(2*b+2), (b,c)
                if b>=6:
                    assert (b+1)*(b//2-1)>2*b
                    counts['even_b_regular_budget']+=1
                else:
                    assert b==4 and c in (1,2,3)
                    for u in (5,7):
                        assert u*(b//2-1)<=2*b
                        if u==5:
                            assert E-10==M-1
                        elif c==1:
                            assert E-14==2
                        else:
                            assert c in (2,3) and M-(E-14)==5
                    counts['even_b_4']+=1
            counts['even_b']+=1
assert counts==Counter({'parameter_pairs':360,'strict_switch':345,'zero_switch':15,
                        'lower_A_colourings':233018,'upper_both_colourings':271548,'odd_b':180,
                        'even_b':180,'even_b_d2':1,'even_b_4':3,'even_b_regular_budget':176}),counts
print('ERDOS561_FLAT_TAIL_360_PARAMETER_PAIRS_PASS')
print('ERDOS561_FLAT_TAIL_STRICT_SURPLUS_345_ZERO_15_PASS')
print('ERDOS561_FLAT_TAIL_FORCED_LOWER_A_233018_ARM_COLOURS_PASS')
print('ERDOS561_FLAT_TAIL_UPPER_BOTH_271548_ARM_COLOURS_PASS')
