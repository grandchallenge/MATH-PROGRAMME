#!/usr/bin/env python3
"""Independent finite oracle for Erdős #561: source-locked Cor. 2.6 and Claim 3.10.

Source: Chunlin You, arXiv:2610.25958v1, 2026-10-19, §§2-3.
No claim that an empirical oracle proves the paper's full theorem.
Only Python standard library is required.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from typing import Iterator


@dataclass(frozen=True)
class Graph:
    n: int
    edges: tuple[tuple[int, int], ...]

    def __post_init__(self) -> None:
        if self.n < 0 or any(not (0 <= u < v < self.n) for u, v in self.edges):
            raise ValueError("expected finite simple graph with canonical edges")
        if tuple(sorted(set(self.edges))) != self.edges:
            raise ValueError("edges must be unique and sorted")

    @property
    def degrees(self) -> tuple[int, ...]:
        d = [0] * self.n
        for u, v in self.edges:
            d[u] += 1
            d[v] += 1
        return tuple(d)

    def components(self, vertices: set[int]) -> list[frozenset[int]]:
        """Connected components in the induced graph, including singleton vertices."""
        remaining = set(vertices)
        result = []
        while remaining:
            seed = min(remaining)
            remaining.remove(seed)
            comp = {seed}
            stack = [seed]
            while stack:
                v = stack.pop()
                for u, w in self.edges:
                    other = w if u == v else u if w == v else None
                    if other is not None and other in remaining:
                        remaining.remove(other)
                        comp.add(other)
                        stack.append(other)
            result.append(frozenset(comp))
        return result


def cuts(n: int) -> Iterator[tuple[frozenset[int], frozenset[int]]]:
    """All 3^n ordered disjoint S,T pairs."""
    for assignment in product((0, 1, 2), repeat=n):
        yield (frozenset(i for i, p in enumerate(assignment) if p == 1),
               frozenset(i for i, p in enumerate(assignment) if p == 2))


def cross(g: Graph, s: set[int] | frozenset[int],
          t: set[int] | frozenset[int]) -> int:
    return sum((u in s and v in t) or (v in s and u in t)
               for u, v in g.edges)


def cut_certificate(g: Graph, alpha: int, beta: int,
                    S: frozenset[int], T: frozenset[int]) -> dict:
    """Compute the two q definitions INDEPENDENTLY to catch parity/sign drift."""
    if alpha <= 0 or beta <= 0 or max(g.degrees, default=0) > alpha + beta:
        raise ValueError("requires positive alpha, beta and maximum degree <= D")
    if S & T or (S | T) - set(range(g.n)):
        raise ValueError("S and T must be disjoint vertex subsets")
    D = alpha + beta
    ds = g.degrees
    A = alpha * len(S) + sum(min(ds[v], beta) for v in T) - cross(g, S, T)
    Y = set(range(g.n)) - S - T
    counted = []
    original = []
    for C in g.components(Y):
        eCT = cross(g, C, T)
        if all(ds[v] == D for v in C) and (alpha * len(C) + eCT) % 2:
            counted.append(tuple(sorted(C)))
        # Lovasz q_{g,f} with g=max(0,d-beta), f=alpha (independent path).
        if (all(max(0, ds[v] - beta) == alpha for v in C)
                and (sum(alpha for _ in C) + eCT) % 2):
            original.append(tuple(sorted(C)))
    return {"A": A, "q_D": len(counted), "q_gf": len(original),
            "counted_components": tuple(counted),
            "original_components": tuple(original),
            "boundary": cross(g, S, Y) + cross(g, T, Y),
            "weighted": alpha * cross(g, S, Y) + beta * cross(g, T, Y)}


def cut_condition(g: Graph, alpha: int, beta: int) -> tuple[bool, tuple | None]:
    """Exact exhaustive Lovasz cut predicate; not a graph-factor algorithm."""
    for S, T in cuts(g.n):
        c = cut_certificate(g, alpha, beta, S, T)
        if c["q_D"] != c["q_gf"]:
            raise AssertionError("specialized and original parity definitions differ")
        if c["A"] < c["q_D"]:
            return False, (tuple(sorted(S)), tuple(sorted(T)), c)
    return True, None


def explicit_partition(g: Graph, alpha: int, beta: int) -> tuple[bool, tuple | None]:
    """Independent brute-force search, not based on cut predicates."""
    if alpha <= 0 or beta <= 0:
        raise ValueError("positive degree budgets needed")
    ds = g.degrees
    if max(ds, default=0) > alpha + beta:
        return False, None
    edges = sorted(g.edges, key=lambda e: -(ds[e[0]] + ds[e[1]]))
    left = [0] * g.n
    right = [0] * g.n
    choice = [0] * len(edges)

    def search(k: int) -> bool:
        if k == len(edges):
            return True
        u, v = edges[k]
        for color, degrees, limit in ((0, left, alpha), (1, right, beta)):
            if degrees[u] >= limit or degrees[v] >= limit:
                continue
            degrees[u] += 1
            degrees[v] += 1
            choice[k] = color
            if search(k + 1):
                return True
            degrees[u] -= 1
            degrees[v] -= 1
        return False

    ok = search(0)
    return ok, tuple(zip(edges, choice)) if ok else None


def all_graphs(n: int) -> Iterator[Graph]:
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
    for mask in range(1 << len(pairs)):
        yield Graph(n, tuple(e for k, e in enumerate(pairs) if mask >> k & 1))


def weighted_cut_inequality(g: Graph, alpha: int, beta: int) -> bool:
    """Claim 3.9 strengthened integer inequality D*A >= alpha eSY + beta eTY."""
    D = alpha + beta
    for S, T in cuts(g.n):
        c = cut_certificate(g, alpha, beta, S, T)
        if c["A"] < 0 or D * c["A"] < c["weighted"]:
            return False
    return True
