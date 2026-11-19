#!/usr/bin/env python3
"""Second arithmetic enumerator, distinct antidiagonal expansion and loops."""
from itertools import combinations_with_replacement as CW
import hashlib,json
tt=sorted((tuple(reversed(q)) for q in CW(range(1,10),3) if q[-1]>=2))
selected=[];seen=0;old=0
for n in tt:
 for m in tt:
  d=n[0]+m[0]-2
  if d>=10:continue
  seen+=1
  w=(n[0]+m[0]-1,max(n[0]+m[1],n[1]+m[0])-1,
     max(n[0]+m[2],n[1]+m[1],n[2]+m[0])-1,
     max(n[1]+m[2],n[2]+m[1])-1,n[2]+m[2]-1)
  e=sum(w)-1;t=d*(d+1)//2
  if e<t:continue
  nr=sum(n)+3;nm=sum(m)+3;r=max(nr,nm)
  b=2*e-d*d+1
  if r>b:continue
  if r==b and min(nr,nm)>d+1 and e-t<max(n[0],m[0]):continue
  old+=1
  delta=b-r
  if delta<=d-2 and e-t>delta:selected.append([list(n),list(m)])
h=hashlib.sha256(json.dumps(sorted(selected),separators=(',',':')).encode()).hexdigest()
assert (seen,old,len(selected))==(4566,851,316)
assert h=="d2d741b5432bacce00fc5fc2a7394b54f966c66c9478dcbcb0e4e6b5e33df91b"
print(json.dumps({'scanned':seen,'previous':old,'eliminated':len(selected),'remaining':old-len(selected),'digest':h},indent=2))
