#!/usr/bin/env python3
"""Small exact #865 sharpness and #866 positive/unrestricted sum forcing."""
from itertools import combinations
import json
def triple_free(A):
    S=set(A)
    for a,b,c in combinations(A,3):
        if a+b in S and a+c in S and b+c in S:
            return False,(a,b,c)
    return True,None
def witness_masks(n,k,positive):
    # For distinct b_i, all pair sums must be in [1,2n].
    # At most one b_i <=0; two other b_i are positive and their sum <=2n,
    # so all b_i fall within [-2n,2n].
    bvalues=range(1,2*n+1) if positive else range(-2*n,2*n+1)
    masks=set()
    for B in combinations(bvalues,k):
        ps={a+b for a,b in combinations(B,2)}
        if min(ps)>=1 and max(ps)<=2*n:
            masks.add(sum(1<<(s-1) for s in ps))
    return masks
def maximal_bad(n,k,positive):
    # Witness-set zeta closure: Boolean status for any superset of a
    # valid pair-sum mask. Exhausts ALL subsets A of [2n].
    size=1<<(2*n)
    contained=bytearray(size)
    masks=witness_masks(n,k,positive)
    for m in masks:contained[m]=1
    for bit in range(2*n):
        step=1<<bit
        for m in range(size):
            if m&step and contained[m^step]:
                contained[m]=1
    maxbad=max(m.bit_count() for m,yes in enumerate(contained) if not yes)
    threshold=maxbad+1
    bad_at_threshold_minus_1=sum(not yes and m.bit_count()==maxbad for m,yes in enumerate(contained))
    return {'n':n,'k':k,'positive':positive,
            'threshold_absolute_size':threshold,
            'offset_from_n':threshold-n,
            'counterexamples_at_previous_size':bad_at_threshold_minus_1,
            'witness_masks':len(masks)}
def main():
    sharp=[]
    for M in (1,2,3,4,5,8,12,20,40):
        A=sorted(set(range(M,2*M+1))|set(range(4*M,8*M+1)))
        ok,collision=triple_free(A)
        assert ok,(M,collision)
        assert len(A)==5*M+2
        sharp.append({'M':M,'N':8*M,'size':len(A),'triple_free':ok})
    thresholds=[]
    for n in range(2,8):
        for k in (3,4):
            for positive in (True,False):
                thresholds.append(maximal_bad(n,k,positive))
    def get(n,k,pos):return next(v for v in thresholds if v['n']==n and v['k']==k and v['positive']==pos)
    for n in range(2,8):
        assert get(n,4,False)['offset_from_n']==3,(n,get(n,4,False))
    for n in (3,4,6,7):
        assert get(n,4,True)['offset_from_n']==4,(n,get(n,4,True))
    assert get(5,4,True)['offset_from_n']==5
    for n in range(3,8):assert get(n,3,False)['offset_from_n']==1
    for n in range(4,8):assert get(n,3,True)['offset_from_n']==2
    print(json.dumps({'record_type':'EC_BULK_006_865_866_FINITE/1',
     'authority':'EXACT_FINITE_COMPUTATION_ONLY',
     'triples':'three distinct a,b,c with all pairwise sums in A',
     'forcing':'exist k distinct integers b_i with ALL pair sums in A; positive variant restricts b_i>=1',
     'sharpness':sharp,'thresholds':thresholds},indent=2))
if __name__=='__main__':main()
