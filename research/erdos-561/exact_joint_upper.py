"""Independent exhaustive 630 centre-degree partitions for F(6,5,4,2).
All red/blue colourings of disjoint stars are equivalent for the star-forest
arrowing relations to their red-edge counts in each connected component.
"""
from itertools import product,permutations
from math import prod

sizes=(6,5,4,2)

def contains_forest(colour_counts, target):
 for locations in permutations(range(len(colour_counts)),len(target)):
  if all(colour_counts[locations[i]]>=target[i] for i in range(len(target))):return True
 return False

n=0
for red in product(*(range(d+1) for d in sizes)):
 blue=tuple(sizes[i]-red[i] for i in range(4))
 assert contains_forest(red,(2,2)) or contains_forest(blue,(4,3,1)), ('R1',red)
 assert contains_forest(red,(4,2,2)) or contains_forest(blue,(3,1)), ('R2',red)
 n+=1
assert n==prod(d+1 for d in sizes)==630
print('PASS: 630 of 630 centre-degree red/blue allocations arrow both R1 and R2')
