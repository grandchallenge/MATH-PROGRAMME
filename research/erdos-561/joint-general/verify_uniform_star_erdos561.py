#!/usr/bin/env python3
"""Exact deterministic uniform-star arithmetic, host colours and Euler split audit."""
from itertools import product
from collections import Counter,deque

def diag(n,m):
 return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==z)
              for z in range(len(n)+len(m)-1))
def includes(arms,tar):
 aa=sorted((x for x in arms if x),reverse=True);tt=sorted(tar,reverse=True)
 return len(aa)>=len(tt) and all(x>=y for x,y in zip(aa,tt))
counts=Counter()
for s in range(3,12):
 for t in range(3,12):
  for a in range(1,14):
   for b in range(1,14):
    n=(a,)*s;m=(b,)*t
    W=sum(diag(n,m));J=sum(diag(n,m)[1:])
    R=a+b-1
    assert W==(s+t-1)*R and J==(s+t-2)*R
    assert J==(t+1)*R+(s-3)*R
    assert W==J+R
    counts['exact_covered']+=1
    counts['all_uniform_profiles']+=1

sample=[
 (3,3,2,2),(4,3,2,2),(3,4,2,2),
 (4,4,2,2),(3,3,3,5),(4,3,3,5),
 (3,4,3,3),(3,3,4,4),(4,3,4,4),
 (3,3,2,4),(3,3,4,2),(4,3,2,4),(3,3,4,6),
 (3,3,2,3),(4,3,2,3),(3,3,3,4),(3,3,1,2),(3,3,2,1)
]
for s,t,a,b in sample:
 R=a+b-1;n=(a,)*s;m=(b,)*t
 for host,mode in [((R,)*(s+t-2),"joint"),((R,)*(s+t-1),"original")]:
  for red in product(*(range(v+1) for v in host)):
   blue=tuple(v-r for v,r in zip(host,red))
   if mode=="joint":
    assert includes(red,n[1:]) or includes(blue,m)
    assert includes(red,n) or includes(blue,m[1:])
   else:
    assert includes(red,n) or includes(blue,m)
   counts['complete_upper_arm_allocations']+=1
  counts['complete_host_instances']+=1

# Every connected odd-degree-free even-degree component with odd edge count
# that has max degree <= 2u-2 either has a vertex below maximum (safe Euler
# start) or is a full saturated regular exceptional component. Catalogue all
# simple graphs on <=6 vertices; inspect connected components and parity.
for vertices in range(1,7):
 pairs=[(i,j) for i in range(vertices) for j in range(i+1,vertices)]
 for mask in range(1<<len(pairs)):
  degree=[0]*vertices;adj=[[] for _ in range(vertices)];edges=0
  for k,(i,j) in enumerate(pairs):
   if mask>>k&1:
    degree[i]+=1;degree[j]+=1;edges+=1
    adj[i].append(j);adj[j].append(i)
  for u in (2,4):
   D=2*u-2
   if max(degree,default=0)>D:continue
   seen=set();bad=0;safe=0
   for v in range(vertices):
    if v in seen or degree[v]==0:continue
    pending=[v];seen.add(v);component=[]
    while pending:
     w=pending.pop();component.append(w)
     for z in adj[w]:
      if z not in seen:seen.add(z);pending.append(z)
    ecomp=sum(degree[w] for w in component)//2
    if all(degree[w]%2==0 for w in component) and ecomp%2:
     if all(degree[w]==D for w in component):
      assert len(component)>=D+1
      assert ecomp>= (u-1)*(2*u-1)
      bad+=1
     else:
      assert min(degree[w] for w in component)<=D-2
      safe+=1
   assert bad*(u-1)*(2*u-1)<=edges
   counts['bounded_euler_component_graph_checks']+=1
counts['source_profile_cases']=counts['all_uniform_profiles']
assert counts['all_uniform_profiles']==13689
assert counts['complete_host_instances']==2*len(sample)
print('ERDOS561_UNIFORM_PROFILE_GRID_13689_ALL_PARITIES_PASS')
print('ERDOS561_UNIFORM_ALL_PROFILES_EXACT',counts['exact_covered'])
print('ERDOS561_UNIFORM_CANONICAL_COMPLETE_HOSTS',counts['complete_host_instances'],'ARM_COLOURS',counts['complete_upper_arm_allocations'])
print('ERDOS561_UNIFORM_EULER_SMALL_SIMPLE_GRAPH_CHECKS',counts['bounded_euler_component_graph_checks'])
