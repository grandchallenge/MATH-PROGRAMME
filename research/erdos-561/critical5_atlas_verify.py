#!/usr/bin/env python3
"""Exact small edge-5-critical obstruction certificate for Erdős #561.

Source: Brendan McKay, Combinatorial Data, `graph7.g6` and `graph8.g6`.
Use only standard Python 3 libraries; no network calls or third-party dependencies.
Complete fixed-vertex isomorphism-class census plus exact backtracking 5-edge colouring.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = {
    7: '5a878f1a46606da4733df250bf9a412d6ae0b3c73c2112e25d66ba00ae565b56',
    8: '546a249902101c97d3aa590f93e53366854bd0a6f405aa59bdb32d25c57f845a',
}
EXPECTED_COUNTS = {7: 1044, 8: 12346}


def parse_graph6(data: bytes):
    n = data[0] - 63
    if not (1 <= n <= 62):
        raise ValueError('unsupported graph6 vertex-order prefix')
    bits = []
    for ch in data[1:]:
        v = ch - 63
        if not (0 <= v <= 63):
            raise ValueError('bad graph6 character')
        bits.extend((v >> j) & 1 for j in (5, 4, 3, 2, 1, 0))
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    return n, edges


def connected(n: int, edges):
    nbr = [[] for _ in range(n)]
    for u, v in edges:
        nbr[u].append(v)
        nbr[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        for v in nbr[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def five_edge_colorable(n: int, edges):
    """Exact existential test; use global colour-symmetry breaking and MRV DFS."""
    degrees = [0] * n
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    ordered = sorted(edges, key=lambda e: degrees[e[0]] + degrees[e[1]], reverse=True)
    occupied = [0] * n

    def dfs(uncoloured: tuple[int, ...], introduced: int) -> bool:
        if not uncoloured:
            return True
        best_i, best_choices, best_size = -1, 0, 6
        for i in uncoloured:
            u, v = ordered[i]
            available = 31 & ~(occupied[u] | occupied[v])
            size = available.bit_count()
            if size < best_size:
                best_i, best_choices, best_size = i, available, size
                if size <= 1:
                    break
        if best_size == 0:
            return False
        u, v = ordered[best_i]
        tail = tuple(j for j in uncoloured if j != best_i)
        for c in range(min(introduced + 1, 5)):
            bit = 1 << c
            if best_choices & bit:
                occupied[u] |= bit
                occupied[v] |= bit
                success = dfs(tail, max(introduced, c + 1))
                occupied[u] ^= bit
                occupied[v] ^= bit
                if success:
                    return True
        return False

    return dfs(tuple(range(len(ordered))), 0)


def verify(n: int, filepath: Path):
    content = filepath.read_bytes()
    actual = hashlib.sha256(content).hexdigest()
    assert actual == SOURCE_SHA256[n], f'{filepath}: source hash mismatch {actual}'
    lines = content.splitlines()
    assert len(lines) == EXPECTED_COUNTS[n]
    candidate_count = 0
    connected_count = 0
    failures = []
    for data in lines:
        order, edges = parse_graph6(data)
        assert order == n
        limit = 15 if n == 7 else 17
        if len(edges) > limit:
            continue
        degrees = [0] * n
        for u, v in edges:
            degrees[u] += 1
            degrees[v] += 1
        if max(degrees) != 5:
            continue
        candidate_count += 1
        if not connected(n, edges):
            continue
        connected_count += 1
        if not five_edge_colorable(n, edges):
            failures.append({'graph6': data.decode('ascii'), 'edges': len(edges),
                             'degrees': sorted(degrees)})
    assert (candidate_count, connected_count) == ({7: (371, 337), 8: (4774, 4362)}[n])
    if n == 7:
        assert failures == [], failures
    else:
        assert len(failures) == 10, failures
        assert all(x['edges'] == 17 and x['degrees'][0] == 1 for x in failures)
    return {'order': n, 'total_graph_classes': len(lines), 'degree5_candidates': candidate_count,
            'connected_examined': connected_count, 'six_edge_chromatic': failures,
            'source_sha256': actual}


def main():
    base = Path(__file__).resolve().parent / 'fixtures'
    reports = [verify(n, base / f'graph{n}.g6') for n in (7, 8)]
    print(json.dumps({'status': 'PASS', 'theorem': '5-critical with <=17 edges has 7 vertices and >=16 edges',
                      'details': reports}, indent=2))


if __name__ == '__main__':
    main()
