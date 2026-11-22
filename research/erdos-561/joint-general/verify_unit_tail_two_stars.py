#!/usr/bin/env python3
"""Proof-oriented finite audit of nonuniform 2-arm + trailing 1 families.

Completely enumerates small degree<=2 path/cycle component multisets; checks
the explicit lemma avoiding colourings using an INDEPENDENT exact vertex-disjoint
P3+K2 search oracle. Also checks canonical antidiagonal hosts exhaustively.
"""
from collections import Counter
from itertools import product
import functools

def diag0(n,m):
 return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==z)
              for z in range(len(n)+len(m)-1))
def diag1(n,m):
 return tuple(max(n[i-1]+m[z-i-1]-1 for i in range(1,len(n)+1) if 1<=z-i<=len(m))
              for z in range(2,len(n)+len(m)+1))
def arms_embed(red_arms, target):
 arms=sorted((a for a in red_arms if a),reverse=True)
 want=sorted(target,reverse=True)
 return len(arms)>=len(want) and all(a>=b for a,b in zip(arms,want))

ct=Counter()
for s in range(3,14):
 for t in range(3,14):
  n=(2,)*(s-1)+(1,)
  for type_ in (1,2):
   m=(2,)*t if type_==1 else (2,)*(t-1)+(1,)
   w=diag0(n,m);a=diag0(n[1:],m);b=diag0(n,m[1:])
   assert w==diag1(n,m) and a==diag1(n[1:],m) and b==diag1(n,m[1:])
   assert w[1:]==tuple(max(x,y) for x,y in zip(a,b))
   W=3*(s+t-2)+(2 if type_==1 else 0)
   J=W-3
   assert sum(w)==W and sum(w[1:])==J
   assert w==(3,)*(s+t-2)+(2,) if type_==1 else w==(3,)*(s+t-3)+(2,1)
   assert J==(3*(s+t-3)+(2 if type_==1 else 0))
   ct['algebra_profiles']+=1
   ct['type_'+str(type_)]+=1
for s,t in [(3,3),(3,4),(4,3),(4,4),(5,3),(3,5)]:
 n=(2,)*(s-1)+(1,)
 for case in (1,2):
  m=(2,)*t if case==1 else (2,)*(t-1)+(1,)
  original=diag0(n,m);joint=original[1:]
  for host,which in [(original,'original'),(joint,'joint')]:
   for red in product(*(range(v+1) for v in host)):
    blue=tuple(v-x for v,x in zip(host,red))
    if which=='original':
     assert arms_embed(red,n) or arms_embed(blue,m)
    else:
     assert arms_embed(red,n[1:]) or arms_embed(blue,m)
     assert arms_embed(red,n) or arms_embed(blue,m[1:])
    ct[which+'_colours']+=1
   ct[which+'_hosts']+=1

# A component has kind P (path with e edges) or C (cycle length e).
# A cycle of odd length may be alternating red- or blue-exception coloured;
# boundary cases may instead make entire triangles or the unique C5 one colour.
def construct(components,case,r,u):
 odd=[i for i,(kind,e) in enumerate(components) if kind=='C' and e%2]
 k=len(odd)
 edge_total=sum(e for _,e in components)
 threshold=3*(r+u-1)+2 if case==1 else 3*(r+u)
 assert edge_total<threshold
 choices={}
 if k<=r+u-2:
  for i,comp in enumerate(odd):
   choices[comp]='red-exc' if i<min(r-1,k) else 'blue-exc'
 else:
  assert k==r+u-1
  excess=edge_total-3*k
  assert excess<=(1 if case==1 else 2)
  big=[i for i in odd if components[i][1]>3]
  assert len(big)<=(0 if case==1 else 1)
  if big:
   assert case==2 and components[big[0]]==('C',5) and excess==2
   choices[big[0]]='all-blue'
   tri=[i for i in odd if i!=big[0]]
   assert len(tri)==r+u-2
   for j,i in enumerate(tri):
    choices[i]='all-red' if j<r else 'all-blue'
  else:
   assert all(components[i]==('C',3) for i in odd)
   for j,i in enumerate(odd):
    choices[i]='all-red' if j<r else 'all-blue'
 # Build graph and return RED/BLUE edge sets, no isolates needed.
 red=[];blue=[];position=0
 for i,(kind,e) in enumerate(components):
  verts=e+1 if kind=='P' else e
  edges=[(position+j,position+j+1) for j in range(e)] if kind=='P' else [(position+j,position+(j+1)%e) for j in range(e)]
  style=choices.get(i)
  if style=='all-red':
   red.extend(edges)
  elif style=='all-blue':
   blue.extend(edges)
  elif style=='red-exc':
   red.extend(edge for j,edge in enumerate(edges) if j%2==0)
   blue.extend(edge for j,edge in enumerate(edges) if j%2)
  elif style=='blue-exc':
   blue.extend(edge for j,edge in enumerate(edges) if j%2==0)
   red.extend(edge for j,edge in enumerate(edges) if j%2)
  else:
   if k==r+u-1:  # boundary: every spare exterior edge is BLUE
    blue.extend(edges)
   else:
    red.extend(edge for j,edge in enumerate(edges) if j%2==0)
    blue.extend(edge for j,edge in enumerate(edges) if j%2)
  position+=verts
 return tuple(red),tuple(blue)

def contains_2stars_and_edge(edges,number,need_edge):
 """True iff ordinary F(2^number,1^need_edge) embeds vertex-disjointly."""
 verts=set(v for e in edges for v in e)
 adj={v:set() for v in verts}
 for x,y in edges:
  adj[x].add(y);adj[y].add(x)
 triples=set()
 for v,near in adj.items():
  seq=sorted(near)
  for i in range(len(seq)):
   for j in range(i+1,len(seq)):
    triples.add(frozenset((v,seq[i],seq[j])))
 triples=tuple(sorted(triples,key=lambda x:tuple(sorted(x))))
 def dfs(pos,used,count):
  if count==number:
   return not need_edge or any(x not in used and y not in used for x,y in edges)
  for i in range(pos,len(triples)):
   triple=triples[i]
   if triple.isdisjoint(used) and dfs(i+1,used|triple,count+1):return True
  return False
 return dfs(0,frozenset(),0)

# All multisets of path/cycle components with positive edge count <= E limit.
def multisets(edge_limit):
 labels=[(kind,e) for e in range(1,edge_limit+1) for kind in ('P','C') if kind=='P' or e>=3]
 # sorted labels allow unique multisets; zero graph included.
 yield ()
 def grow(start,remaining,out):
  for i in range(start,len(labels)):
   kind,e=labels[i]
   if e>remaining:continue
   new=out+(labels[i],)
   yield new
   yield from grow(i,remaining-e,new)
 yield from grow(0,edge_limit,())

cases=[(1,1,2),(1,2,2),(1,2,3),(2,1,2),(2,2,2),(2,2,3)]
for case,r,u in cases:
 E=3*(r+u-1)+1 if case==1 else 3*(r+u)-1
 for comps in multisets(E):
  red,blue=construct(comps,case,r,u)
  assert not contains_2stars_and_edge(red,r,True),('red',case,r,u,comps,red)
  assert not contains_2stars_and_edge(blue,u,case==2),('blue',case,r,u,comps,blue)
  ct['degree2_full_graph_classes']+=1
 ct['degree2_case_parameter_sets']+=1

assert ct['algebra_profiles']==242
assert ct['original_hosts']==12 and ct['joint_hosts']==12
assert ct['degree2_case_parameter_sets']==6
print('ERDOS561_UNIT_TAIL_ALGEBRA_242_PROFILES_PASS')
print('ERDOS561_UNIT_TAIL_CANONICAL_HOST_CLASSES',ct['original_hosts']+ct['joint_hosts'])
print('ERDOS561_UNIT_TAIL_CANONICAL_ARM_COLOURS',ct['original_colours']+ct['joint_colours'])
print('ERDOS561_UNIT_TAIL_DEGREE2_EXACT_AVOIDING_COLOURINGS',ct['degree2_full_graph_classes'])
