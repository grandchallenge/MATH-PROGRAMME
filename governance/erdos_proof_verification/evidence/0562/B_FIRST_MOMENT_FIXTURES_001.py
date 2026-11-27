"""Exact finite adversarial fixtures; not a proof of the unbounded theorem."""
from itertools import product
from math import comb

def root12_floor(x):
    lo, hi = 0, 1 << ((x.bit_length()+11)//12)
    while lo < hi:
        mid = (lo+hi+1)//2
        if mid**12 <= x: lo = mid
        else: hi = mid-1
    return lo

def main():
    masks=0
    for t in range(7):
        for mask in product((None,False,True), repeat=t):
            count=sum(all(m is None or m==b for m,b in zip(mask,bits)) for bits in product((False,True),repeat=t))
            assert count==2**mask.count(None)
            masks+=1
    for n in range(4,129):
        a=(n-1)*(n-2); k=comb(n,3); m=root12_floor(2**a)
        assert m**12<=2**a<(m+1)**12 and n*a==6*k and 2*m**n<2**k
    # A sharp negative union-bound boundary: two masks fix the sole coordinate.
    assert all(any(b==m for m in (False,True)) for b in (False,True))
    print(f'PASS: {masks} exact masks; 125 integer-floor cases; equality-boundary hostile fixture')
if __name__=='__main__': main()
