#!/usr/bin/env python3
"""Exact nonstar candidate search with two independently coded arrow
certifiers: red matching-1 structural enumeration and general 2^E check.
"""
from exact_arbitrary_host import stars,identify,arrow
from fast_A import arrow_A
from star_host_falsifier import partitions,w
import sys,json,time,os
from collections import Counter
n=(2,1,1);m=(4,1,1,1,1);J=sum(w(n,m)[1:]);E=int(os.environ.get('ERDOS561_EDGE_BUDGET',J-1))
assert J==14 and E in (12,13)
bases=[p for p in partitions(E) if len(p)>=5 and max(p)>=4]
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
end=int(sys.argv[2]) if len(sys.argv)>2 else len(bases)
counts=Counter();now=time.monotonic()
for host in bases[start:end]:
  edges=stars(host);vertices=sorted({v for e in edges for v in e})
  for ix,u in enumerate(vertices):
    for v in vertices[ix+1:]:
      G=identify(edges,u,v)
      if G is None:continue
      counts['simple_candidates']+=1
      a,_=arrow_A(G,4,4)
      if not a:continue
      counts['arrow_red_deleted']+=1
      b,_=arrow(G,n,m[1:])
      if b:
        print('FOUND_REFUTATION',json.dumps({'n':n,'m':m,'e':E,'J':J,'base':host,'merge':[u,v],'edges':G}),flush=True)
        sys.exit(2)
      counts['fails_blue_deleted']+=1
  counts['bases']+=1
  print('BASE_DONE',host,dict(counts),'time',round(time.monotonic()-now,2),flush=True)
print('NO_REFUTATION_IN_CLASS',dict(counts),'time',round(time.monotonic()-now,2),flush=True)
