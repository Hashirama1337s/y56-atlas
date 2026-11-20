# Exact check that the 32 line-graph automorphisms not induced by projective maps come from a Galois twist.
# tau = R o (sqrt2 -> -sqrt2), R(z0,z1,z2,z3) = (z0,-z2,z1,z3).
# Self-contained: reads data/edges.json, data/symmetry_exact.txt, data/lines_exact.txt (via code/sisters/q2.py).
# Run from code/exact:  python galois_twist.py
import sys, os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sisters'))
DATA = os.path.join(HERE, '..', '..', 'data') + '/'
from q2 import *
import sympy as sp
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

n = 56
# (a) all automorphisms of the line intersection graph
G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(json.load(open(DATA + 'edges.json')))
grp = {tuple(m[i] for i in range(n)) for m in GraphMatcher(G, G).isomorphisms_iter()}
print('graph automorphisms:', len(grp))
# (b) the 32 permutations realised by projective symmetries
real = set()
for ln in open(DATA + 'symmetry_exact.txt'):
    if ln.startswith('g'):
        real.add(tuple(eval(re.search(r'sigma=(\[.*\])', ln).group(1))))
print('realised projective permutations:', len(real), ' all are graph automorphisms:', real <= grp)
# (c) exact checks
L = load_lines()
z = sp.symbols('z0:4'); r = sp.sqrt(2)
F = 3*r*z[0]**2*z[1]*z[2] + 3*r*z[1]*z[2]*z[3]**2 - r*z[1]**3*z[2] - r*z[1]*z[2]**3 + 4*z[0]**3*z[3] - 4*z[0]*z[3]**3
Fg = F.subs(r, -r)
R = [[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
Rz = [sum(R[i][j]*z[j] for j in range(4)) for i in range(4)]
chk = sp.expand(F.subs(dict(zip(z, Rz)), simultaneous=True))
print('F(R y) == Fg(y):', sp.expand(chk - Fg) == 0, '  F(R y) == -Fg(y):', sp.expand(chk + Fg) == 0)
RQ = [[Q2(x) for x in row] for row in R]
NRM = [nullspace([l[0], l[1]], 4) for l in L]
def img(i):
    pts = [matvec(RQ, [x.conj() for x in p]) for p in L[i]]
    js = [j for j in range(n) if all(dot(nv, q).iszero() for nv in NRM[j] for q in pts)]
    assert len(js) == 1, js
    return js[0]
tau = tuple(img(i) for i in range(n))
print('tau permutes the 56 lines:', sorted(tau) == list(range(n)))
print('tau is a graph automorphism:', tau in grp, ' tau realised projectively:', tau in real)
comp = lambda p, q: tuple(p[q[i]] for i in range(n))
coset = {comp(tau, h) for h in real}
print('tau * (32 realised) == the 32 unrealised:', coset == grp - real)
