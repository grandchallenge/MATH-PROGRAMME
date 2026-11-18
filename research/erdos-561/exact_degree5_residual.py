"""Complete structural enumeration of 11-edge Q arrow (K1,2, F(4,3,1)),
using equality in the one-star size Ramsey theorem.

No assumptions about a general Ramsey conjecture. Base F has 11 vertices, 8 edges.
All Q of 11 edges must have a maximum matching M of size 3 with Q-M=F.
Hence every Q is F plus three pairwise disjoint edges, each incident to a vertex of F.
"""
from itertools import combinations
from collections import Counter
import time,json

# Three disjoint stars on vertex ranges 0..4, 5..8, 9..10.
base={(0,i) for i in range(1,5)} | {(5,i) for i in range(6,9)} | {(9,10)}
assert len(base)==8
old=tuple(range(11))

def pairings(vertices):
 if not vertices:
  yield ();return
 x,*tail=vertices
 for y in tail:
  other=tuple(z for z in tail if z!=y)
  for p in pairings(other):yield ((x,y),)+p

def addmatchings():
 for k in range(4):  # k fresh endpoints, matched to old vertices
  oldneeded=6-k
  for selection in combinations(old,oldneeded):
   for freshold in combinations(selection,k):
    inold=tuple(x for x in selection if x not in freshold)
    for p in pairings(inold):
     added=tuple(sorted(tuple(sorted(e)) for e in p+(tuple((f,11+i) for i,f in enumerate(freshold)))))
     if any(e in base for e in added):continue
     yield added

def is_H_edge_list(edges):
 if len(edges)!=8:return False
 adj={}
 for a,b in edges:
  adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
 seen=set();size=[]
 for v in adj:
  if v in seen:continue
  stack=[v];seen.add(v);vertices=[];ec=0
  while stack:
   x=stack.pop();vertices.append(x);ec+=len(adj[x])
   for u in adj[x]:
    if u not in seen:seen.add(u);stack.append(u)
  e=ec//2
  if len(vertices)!=e+1 or max(len(adj[x]) for x in vertices)!=e:return False
  size.append(e)
 return sorted(size,reverse=True)==[4,3,1]

def Q_arrows_single_star(edges):
 n=len(edges)
 assert n==11
 # All 3-edge subsets whose removal leaves exactly H.
 good=[]
 for c in combinations(range(11),3):
  skip=set(c)
  if is_H_edge_list([e for i,e in enumerate(edges) if i not in skip]):
   good.append(sum(1<<i for i in c))
 if not good:return False,0
 # Every red matching S must be contained in at least one H-complement set.
 supported=bytearray(1<<11)
 for M in good:
  sub=M
  while True:
   supported[sub]=1
   if sub==0:break
   sub=(sub-1)&M
 # Identify all red matching subsets and check they have blue H.
 # A matching has at most 3 edges, since red 4-matching would witness failure.
 for size in range(1,5):
  for inds in combinations(range(11),size):
   used=set()
   for i in inds:
    a,b=edges[i]
    if a in used or b in used:break
    used.update((a,b))
   else:
    bits=sum(1<<i for i in inds)
    if not supported[bits]:return False,len(good)
 return True,len(good)

start=time.monotonic();cnt=0;passed=[];kind=Counter()
for M in addmatchings():
 cnt+=1
 edges=tuple(sorted(base|set(M)))
 yes,k=Q_arrows_single_star(edges)
 if yes:
  vertices=max(max(e) for e in edges)+1
  degrees=Counter(v for edge in edges for v in edge)
  passed.append({'base_matching':M,'edge_list':edges,'q_max_degree':max(degrees.values()),'good_H_complements':k})
  kind[vertices]+=1
print(json.dumps({'candidate_M':cnt,'passed':len(passed),'by_vertices':dict(kind),'seconds':round(time.monotonic()-start,2),'first':passed[:30]},indent=2))
# For portability, CI prints the result; it does not mutate an absolute path.
# The original archive contains the historical JSON output and its SHA256.

