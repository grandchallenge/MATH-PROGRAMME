"""Exact 24-edge disjoint-star upper witness for the original (4,2,2)/(4,3,1).
Every red/blue colouring is represented by its red edge-count per star centre.
"""
from itertools import product,permutations
from math import prod
host=(7,6,5,4,2)

def contains(values,target):
 return any(all(values[loc[i]]>=target[i] for i in range(len(target))) for loc in permutations(range(len(values)),len(target)))

count=0
for red in product(*(range(h+1) for h in host)):
 blue=tuple(host[i]-red[i] for i in range(len(host)))
 assert contains(red,(4,2,2)) or contains(blue,(4,3,1)),(red,blue)
 count+=1
assert count==prod(h+1 for h in host)==5040
print('PASS:',count,'of',count,'centre-degree colour allocations for F(7,6,5,4,2)')
