#!/usr/bin/env python3
"""Exact disjoint-star-host falsification for joint residual candidate.
NOT a proof for arbitrary graphs: star hosts are only one class.
Every red count on each star is explicitly tested by DFS and sorted
monochromatic degrees; no random colouring or graph subcase sampled.
"""
import itertools,sys,time,json
from functools import lru_cache

@lru_cache(None)
def partitions(total, maxpart=None):
 if maxpart is None:maxpart=total
 if total==0:return ((),)
 ret=[]
 for p in range(min(total,maxpart),1-1,-1):
  for tail in partitions(total-p,p):ret.append((p,)+tail)
 return tuple(ret)

def w(n,m):
 return [max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==k)
         for k in range(len(n)+len(m)-1)]

def has_target(degrees,need):
 ds=sorted(degrees,reverse=True)
 return len(ds)>=len(need) and all(ds[i]>=a for i,a in enumerate(need))

def avoids_any(host,redneed,blueneed):
 # Return first exact forbidden-free colouring (red arm counts), else None.
 # Detection is monotone: after a red or blue target occurs it cannot disappear.
 if len(host)<len(redneed):
  # All-red has too few nontrivial host components for the red forest.
  return tuple(host)
 if len(host)<len(blueneed):
  # All-blue has too few nontrivial host components for the blue forest.
  return tuple(0 for _ in host)
 @lru_cache(None)
 def recur(i,rc,bc):
  if has_target(rc,redneed) or has_target(bc,blueneed):return None
  if i==len(host):return ()
  for r in range(host[i]+1):
   b=host[i]-r
   z=recur(i+1,tuple(sorted(rc+(r,),reverse=True)[:len(redneed)]),
               tuple(sorted(bc+(b,),reverse=True)[:len(blueneed)]))
   if z is not None:return (r,)+z
  return None
 return recur(0,(),())

def arrows(host,n,m):return avoids_any(host,n,m) is None

def test(n,m,max_e=None,max_hosts=None):
 need=sum(w(n,m)[1:]);bound=need if max_e is None else min(need,max_e)
 if max_hosts is None:max_hosts=1000000
 count=0
 for e in range(0,bound):
  for host in partitions(e):
   if len(host)<max(len(n),len(m)):continue
   count+=1
   if count>max_hosts:return {'status':'BUDGET','count':count,'j':need}
   if arrows(host,n[1:],m) and arrows(host,n,m[1:]):
    return {'status':'REFUTED_STAR_HOST','n':n,'m':m,'host':host,'e':e,'j':need,'red_residual':n[1:],'blue_residual':m[1:],'count':count}
 return {'status':'STAR_HOST_NO_WITNESS','count':count,'j':need}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--level',type=int,default=2);p.add_argument('--max-e',type=int,default=17);p.add_argument('--max-hosts',type=int,default=20000);args=p.parse_args()
 suites=[(3,3),(3,4),(4,4),(3,5)]
 def trip(length,limit):
  return list(itertools.combinations_with_replacement(range(1,limit+1),length))
 for s,t in suites:
  if s+t>7+args.level:continue
  ns=trip(s,args.level);ms=trip(t,args.level)
  for aa in ns:
   n=tuple(aa[::-1]);
   for bb in ms:
    m=tuple(bb[::-1]);J=sum(w(n,m)[1:]);
    if J>args.max_e:continue
    res=test(n,m,max_e=args.max_e,max_hosts=args.max_hosts)
    print('RESULT',json.dumps(res,separators=(',',':')),flush=True)
    if res['status']=='REFUTED_STAR_HOST':sys.exit(2)
