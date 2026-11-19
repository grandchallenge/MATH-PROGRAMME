"""A constructive D-edge-colouring for an independent k-apex star forest.

If U is an independent set of k degree-D vertices in a finite simple graph G,
G-U is a star forest, and D >= 3k, this program constructs a proper edge
colouring with colours 0..D-1. Uses no third-party Python packages.

This is supporting executable evidence for the Hall/Konig proof, not a
substitute for the unbounded mathematical proof.
"""
from collections import defaultdict, deque
from itertools import combinations
import random
import json


def edge(u, v):
    assert u != v
    return tuple(sorted((u, v)))


def assign_distinct(objects, permitted):
    """Kuhn augmenting-path algorithm for a system of distinct representatives."""
    assigned = {}

    def visit(obj, seen):
        for color in sorted(permitted[obj]):
            if color in seen:
                continue
            seen.add(color)
            if color not in assigned or visit(assigned[color], seen):
                assigned[color] = obj
                return True
        return False

    for obj in objects:
        if not visit(obj, set()):
            raise AssertionError(('Hall failure', obj, permitted))
    return {obj: color for color, obj in assigned.items()}


def color_bipartite_edges(apices, edges, D):
    """Bipartite D-edge-colouring by Kempe-chain recolouring.

    Edges must have exactly one endpoint among apices. A partial edge colouring
    is extended a single edge at a time. When no common missing colour exists,
    the two-colour alternating component from the apex cannot reach the
    opposite-shore endpoint, by parity.
    """
    A = set(apices)
    E = sorted({edge(*e) for e in edges})
    inc = defaultdict(list)
    for a, b in E:
        assert (a in A) != (b in A)
        inc[a].append((a, b))
        inc[b].append((a, b))
    assert max((len(v) for v in inc.values()), default=0) <= D
    coloring = {}
    P = set(range(D))

    def missing(v):
        return P - {coloring[e] for e in inc[v] if e in coloring}

    for e in E:
        u, v = e
        if u not in A:
            u, v = v, u
        mu, mv = missing(u), missing(v)
        both = mu & mv
        if both:
            coloring[e] = min(both)
            continue
        a, b = min(mu), min(mv)
        # Follow the alternating (a,b) component of the left-shore vertex u.
        q = deque([u])
        seen = {u}
        component_edges = set()
        while q:
            w = q.popleft()
            for f in inc[w]:
                if coloring.get(f) not in (a, b):
                    continue
                component_edges.add(f)
                z = f[1] if f[0] == w else f[0]
                if z not in seen:
                    seen.add(z)
                    q.append(z)
        assert v not in seen, 'bipartite alternating path parity violated'
        for f in component_edges:
            coloring[f] = b if coloring[f] == a else a
        assert b in missing(u) and b in missing(v)
        coloring[e] = b
    assert len(coloring) == len(E)
    return coloring


def color_k_apex_graph(apices, stars, apex_edges, D):
    """Colour a graph with independent degree-D apices and residual star forest.

    Parameters
    ----------
    apices: distinct hashable vertex IDs
    stars: iterable of (center, tuple_of_leaves), pairwise vertex-disjoint
    apex_edges: list of edges with exactly one endpoint in apices
    D: desired palette size, at least 3 * len(apices)

    Isolated residual vertices may occur in apex_edges but not in stars.
    """
    apices = tuple(apices)
    k = len(apices)
    assert k >= 1 and D >= 3 * k
    assert len(set(apices)) == k
    A = set(apices)
    stars = [(c, tuple(leaves)) for c, leaves in stars]
    residual_nodes = []
    for c, leaves in stars:
        assert c not in leaves and c not in A and len(leaves) > 0
        residual_nodes.extend((c, *leaves))
    assert len(residual_nodes) == len(set(residual_nodes)), 'stars overlap'
    ae = {edge(*e) for e in apex_edges}
    for x, y in ae:
        assert (x in A) != (y in A)
    d = defaultdict(int)
    for x, y in ae:
        d[x] += 1
        d[y] += 1
    for c, leaves in stars:
        for x in leaves:
            d[c] += 1
            d[x] += 1
    assert max(d.values(), default=0) == D
    assert all(d[u] == D for u in apices)
    assert all(v <= D for v in d.values())
    out = color_bipartite_edges(A, ae, D)
    P = set(range(D))
    incident_apex_colors = defaultdict(set)
    for (x, y), color in out.items():
        if x not in A:
            incident_apex_colors[x].add(color)
        if y not in A:
            incident_apex_colors[y].add(color)
    for c, leaves in stars:
        Pc = P - incident_apex_colors[c]
        assert len(Pc) >= max(D-k, len(leaves))
        permitted = {x: Pc - incident_apex_colors[x] for x in leaves}
        assert all(len(v) >= D-2*k for v in permitted.values())
        choices = assign_distinct(leaves, permitted)
        for x in leaves:
            out[edge(c, x)] = choices[x]
    incidence = defaultdict(set)
    for (x, y), color in out.items():
        assert color not in incidence[x] and color not in incidence[y]
        incidence[x].add(color)
        incidence[y].add(color)
    assert len(out) == len(ae) + sum(len(ls) for _, ls in stars)
    assert all(len(incidence[a]) == D for a in apices)
    return out


def random_instance(rng, k, D):
    apices = tuple(range(k))
    nstars = rng.randint(1, k + 4)
    nxt = k
    stars = []
    deg = defaultdict(int)
    for _ in range(nstars):
        h = rng.randint(1, max(1, D-k))
        c = nxt
        leaves = tuple(range(nxt+1, nxt+h+1))
        nxt += h + 1
        stars.append((c, leaves))
        deg[c] += h
        for x in leaves:
            deg[x] += 1
    # Many neighbours are shared between apices, with fresh isolated leaves
    # added as needed. Residual degrees are kept <=D.
    ae = []
    residual = [x for c, leaves in stars for x in (c, *leaves)]
    for a in apices:
        available = [x for x in residual if deg[x] < D]
        number = rng.randint(0, min(D, len(available)))
        old = rng.sample(available, number)
        for x in old:
            ae.append((a, x))
            deg[x] += 1
        for _ in range(D-number):
            ae.append((a, nxt))
            deg[nxt] += 1
            nxt += 1
    return apices, stars, ae


def run_checks(seed=561, per_k=250):
    rng = random.Random(seed)
    results = []
    for k in range(1, 5):
        for D in (3*k, 3*k+1, 3*k+3):
            for i in range(per_k):
                apices, stars, ae = random_instance(rng, k, D)
                col = color_k_apex_graph(apices, stars, ae, D)
                assert len(col) == len(ae) + sum(len(x) for _, x in stars)
            results.append({'k':k, 'D':D, 'tested':per_k, 'passed':per_k})
    return {'seed':seed, 'total':sum(x['tested'] for x in results), 'failures':0, 'cases':results}


if __name__ == '__main__':
    out = run_checks()
    print(json.dumps(out, indent=2))
