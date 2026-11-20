"""Referee part 2: signature of the line lattice N (56 lines + h) and enumeration of classes c in N with
c.h = 2, c^2 = -2 (conic classes), split into sums of two meeting lines vs others, and pairs {c, h-c}.
Input: data/edges.json (shown equal to the referee's own recomputed graph in ref_checks.out)."""
import os, sys, json, random, math, itertools
from fractions import Fraction as Fr
from collections import Counter
import sympy as sp

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'core')
E = {tuple(e) for e in json.load(open(ROOT + '/data/edges.json'))}
n = 57
G = [[0]*n for _ in range(n)]
for i in range(56): G[i][i] = -2; G[i][56] = G[56][i] = 1
G[56][56] = 4
for i, j in E: G[i][j] = G[j][i] = 1
out = []
def rep(s): print(s, flush=True); out.append(s)

def ldl(A):
    A = [[Fr(x) for x in r] for r in A]; m = len(A); pv = []
    for c in range(m):
        if A[c][c] == 0: return None
        pv.append(A[c][c])
        for r in range(c+1, m):
            f = A[r][c] / A[c][c]
            if f: A[r] = [A[r][k] - f*A[c][k] for k in range(m)]
    return pv

# find 20 generators forming a Z-basis of N: |det Gram| = 64 (the full |disc| from invariant factors)
random.seed(1)
basis = None
for trial in range(20000):
    idx = random.sample(range(n), 20)
    sub = [[G[a][b] for b in idx] for a in idx]
    pv = ldl(sub)
    if pv is None: continue
    d = 1
    for v in pv: d *= v
    if abs(d) == 64: basis = idx; break
rep('Z-basis of N found among generators: %s (trial %d)' % (basis is not None, trial))
idx = basis
B = [[G[a][b] for b in idx] for a in idx]
pv = ldl(B); rep('signature (exact LDL pivots): (%d, %d), det = %s' % (sum(v > 0 for v in pv), sum(v < 0 for v in pv), math.prod(pv)))
Bm = sp.Matrix(B)
# coordinates of every generator in this basis must be integral (confirms it is a Z-basis of the span)
Binv = Bm.inv()
coords = []
for g in range(n):
    col = sp.Matrix([G[a][g] for a in idx]); x = Binv * col; coords.append(x)
integral = all(all(v.is_integer for v in x) for x in coords)
rep('all 57 generators have integral coordinates in the basis: %s' % integral)
hx = coords[56]; Lx = coords[:56]
Bh = [sum(B[i][j]*hx[j] for j in range(20)) for i in range(20)]  # x.h = sum x_i Bh_i
# positive definite Q(x) = (x.h)^2/2 - x^2 ; Q = 4 for conic classes
Q = [[Fr(int(Bh[i]*Bh[j]), 2) - B[i][j] for j in range(20)] for i in range(20)]
# float Cholesky
import numpy as np
Qf = np.array([[float(v) for v in r] for r in Q])
ev = np.linalg.eigvalsh(Qf); rep('Q min eigenvalue %.4f (positive definite: %s)' % (ev.min(), ev.min() > 0))
# LLL-free Fincke-Pohst with Cholesky; small bound
Lc = np.linalg.cholesky(Qf)          # Qf = Lc Lc^T
R = Lc.T                              # Q(x) = |R x|^2, R upper triangular
m = 20; bound = 4.0 + 1e-6
qd = [R[i, i]**2 for i in range(m)]
mu = [[R[i, j]/R[i, i] for j in range(m)] for i in range(m)]
sols = []
x = [0]*m
def rec(k, rem):
    # centre for x_k
    c = -sum(mu[k][j]*x[j] for j in range(k+1, m))
    r = math.sqrt(max(rem, 0)/qd[k])
    lo, hi = math.ceil(c - r - 1e-9), math.floor(c + r + 1e-9)
    for v in range(lo, hi+1):
        x[k] = v; t = rem - qd[k]*(v - c)**2
        if t < -1e-9: continue
        if k == 0: sols.append(tuple(x))
        else: rec(k-1, t)
    x[k] = 0
rec(m-1, bound)
rep('vectors with Q <= 4 (incl. 0): %d' % len(sols))
def dotB(a, b): return sum(a[i]*B[i][j]*b[j] for i in range(20) for j in range(20) if a[i] and b[j])
hl = [int(v) for v in hx]
conics = []
for s in sols:
    if sum(s[i]*Bh[i] for i in range(20)) == 2 and dotB(s, s) == -2: conics.append(s)
rep('classes c with c.h = 2, c^2 = -2: %d' % len(conics))
Lt = [tuple(int(v) for v in x) for x in Lx]
pair = set()
for i, j in E: pair.add(tuple(a+b for a, b in zip(Lt[i], Lt[j])))
cs = set(conics)
red = cs & pair; irr = cs - pair
rep('sums of two meeting lines: %d (all in set: %s); others: %d' % (len(red), pair <= cs, len(irr)))
hpairs = {frozenset([c, tuple(h - a for h, a in zip(hl, c))]) for c in irr if tuple(h - a for h, a in zip(hl, c)) in irr}
rep('pairs {c, h-c} with both not line-pair sums: %d' % len(hpairs))
# also: are any 'other' classes of the form l1 + l2 with l1,l2 disjoint or 2l? (c^2 would differ; sanity)
open(os.path.dirname(os.path.abspath(__file__)) + '/ref_conics.out', 'w').write('\n'.join(out) + '\n')
