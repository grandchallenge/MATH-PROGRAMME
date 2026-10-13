from itertools import combinations
from math import lcm
from fractions import Fraction

def test_856(N,k=3):
 forbidden=[]
 for tri in combinations(range(1,N+1),k):
  vals={lcm(a,b) for a,b in combinations(tri,2)}
  if len(vals)==1: forbidden.append(sum(1<<(a-1) for a in tri))
 best=Fraction(-1);best_mask=0;ok=0
 for mask in range(1<<N):
  if any(mask&tri==tri for tri in forbidden):continue
  ok+=1
  val=sum((Fraction(1,a) for a in range(1,N+1) if mask&(1<<(a-1))),Fraction(0))
  if val>best:best,best_mask=val,mask
 return {'N':N,'k':k,'forbidden_triples':len(forbidden),'valid_families':ok,'max_harmonic':str(best),'witness':[a for a in range(1,N+1) if best_mask&(1<<(a-1))]}

def test_857(n,k=3):
 sets=range(1<<n)
 forbidden=[]
 for tri in combinations(sets,k):
  inter=[a&b for a,b in combinations(tri,2)]
  if len(set(inter))==1:forbidden.append(sum(1<<a for a in tri))
 best=-1;best_mask=0
 for mask in range(1<<(1<<n)):
  size=mask.bit_count()
  if size<=best:continue
  if any(mask&tri==tri for tri in forbidden):continue
  best=size;best_mask=mask
 return {'n':n,'k':k,'forbidden_sunflower_triples':len(forbidden),'max_free_family_size':best,'m_n_k':best+1,'witness_masks':[a for a in sets if best_mask&(1<<a)]}
if __name__=='__main__':
 import json
 print(json.dumps({'856':[test_856(n) for n in range(3,13)],'857':[test_857(n) for n in range(1,5)]},indent=2))
