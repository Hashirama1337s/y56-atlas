# Task A follow-up (EXACT): are the 32 unrealised graph automorphisms induced by the Galois twist
# tau = R o (sqrt2 -> -sqrt2), R(z0,z1,z2,z3) = (z0,-z2,z1,z3)?  (F^Gal(z) = F(R^-1 z) up to sign: check exactly.)
import sys, pickle
sys.path.insert(0, '../../core/code/sisters')
from q2 import *
import sympy as sp
L = load_lines(); n = 56
d = pickle.load(open('a_aut.pkl', 'rb')); grp = set(d['grp']); real = set(d['real'])
z = sp.symbols('z0:4'); r = sp.sqrt(2)
F = 3*r*z[0]**2*z[1]*z[2] + 3*r*z[1]*z[2]*z[3]**2 - r*z[1]**3*z[2] - r*z[1]*z[2]**3 + 4*z[0]**3*z[3] - 4*z[0]*z[3]**3
Fg = F.subs(r, -r)
R = [[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
Rz = [sum(R[i][j]*z[j] for j in range(4)) for i in range(4)]
# point x on Y56 -> Gal(x) on Y56^Gal -> R Gal(x): need F(R y) = c * Fg(y)
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
