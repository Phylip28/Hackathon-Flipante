#!/usr/bin/env python3
"""Reto I - La Chocita: circulo de 5-10 figuras con seguimiento mutuo que
maximiza los fans distintos. Fuente: follows.csv (follower_id,followed_id)."""
import csv, sys, collections, itertools

CSV = "follows.csv"
FIG_LO, FIG_HI = 80001, 80600      # IDs de las figuras publicas (aparecen como followed)
KMIN, KMAX = 5, 10

def load(path):
    follows = collections.defaultdict(set)     # x -> {y}: x sigue a y
    fanbit  = collections.defaultdict(int)      # figura -> bitmask de sus followers
    figures = set()
    with open(path, newline="") as f:
        r = csv.reader(f); next(r)
        for row in r:
            if len(row) != 2 or not row[0] or not row[1]: continue
            a, b = int(row[0]), int(row[1])
            follows[a].add(b); fanbit[b] |= (1 << a)
            if FIG_LO <= b <= FIG_HI: figures.add(b)
    return follows, fanbit, figures

def mutual_graph(follows, figures):
    """Grafo no dirigido: arista a-b si a y b se siguen mutuamente."""
    adj = collections.defaultdict(set); fset = set(figures)
    for a in figures:
        for b in follows[a]:
            if b in fset and b > a and a in follows[b]:
                adj[a].add(b); adj[b].add(a)
    return adj

def maximal_cliques(adj, nodes):
    """Bron-Kerbosch con pivote: todos los grupos que se siguen entre si al 100%."""
    cliques = []
    def bk(R, P, X):
        if not P and not X: cliques.append(R); return
        pivot = max(P | X, key=lambda u: len(adj[u] & P))
        for v in list(P - adj[pivot]):
            bk(R | {v}, P & adj[v], X & adj[v]); P -= {v}; X |= {v}
    sys.setrecursionlimit(10000)
    bk(set(), set(nodes), set())
    return cliques

def coverage(members, fanbit):
    """Fans distintos del conjunto, excluyendo a los propios miembros."""
    u = 0
    for m in members: u |= fanbit[m]
    for m in members: u &= ~(1 << m)
    return u.bit_count()

def best_k_subset(clique, k, fanbit, lower):
    """Mejor k-subconjunto por cobertura. Poda: la cobertura del clique completo
    acota por arriba la de cualquier subconjunto (monotonia)."""
    if coverage(clique, fanbit) <= lower: return -1, None
    if len(clique) == k: return coverage(clique, fanbit), tuple(clique)
    best, bestset = -1, None
    for sub in itertools.combinations(clique, k):
        c = coverage(sub, fanbit)
        if c > best: best, bestset = c, sub
    return best, bestset

def solve():
    follows, fanbit, figures = load(CSV)
    adj = mutual_graph(follows, figures)
    cliques = [tuple(c) for c in maximal_cliques(adj, figures)]
    best, members = -1, None
    for k in range(KMIN, KMAX + 1):               # el optimo esta en k=10 (cobertura monotona)
        cands = sorted((c for c in cliques if len(c) >= k),
                       key=lambda c: coverage(c, fanbit), reverse=True)
        for c in cands:
            cov, sub = best_k_subset(c, k, fanbit, best)
            if cov > best: best, members = cov, tuple(sorted(sub))
    return members, best

if __name__ == "__main__":
    members, fans = solve()
    print(f"Circulo optimo {list(members)}  ->  {fans:,} fans distintos")
