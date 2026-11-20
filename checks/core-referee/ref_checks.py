"""Referee's own independent checks of Y56 headline facts (a)-(d).
Own Q(sqrt2) arithmetic (pairs of Fractions), own parser, own polynomial code.
Does not import anything from the release's code/ folder. Reads only data/*.txt and data/edges.json."""
import os, sys, re, json, itertools
from fractions import Fraction as Fr
from collections import Counter

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'core')
D = ROOT + '/data/'

class K:
    __slots__ = ('a', 'b')  # a + b*sqrt2
    def __init__(s, a=0, b=0): s.a = Fr(a); s.b = Fr(b)
    def _c(o): return o if isinstance(o, K) else K(o)
    def __add__(s, o): o = K._c(o); return K(s.a+o.a, s.b+o.b)
    __radd__ = __add__
    def __neg__(s): return K(-s.a, -s.b)
    def __sub__(s, o): return s + (-K._c(o))
    def __rsub__(s, o): return K._c(o) - s
    def __mul__(s, o): o = K._c(o); return K(s.a*o.a + 2*s.b*o.b, s.a*o.b + s.b*o.a)
    __rmul__ = __mul__
    def norm(s): return s.a*s.a - 2*s.b*s.b
    def inv(s):
        n = s.norm(); assert n != 0; return K(s.a/n, -s.b/n)
    def __truediv__(s, o): return s * K._c(o).inv()
    def __rtruediv__(s, o): return K._c(o) * s.inv()
    def __pos__(s): return s
    def z(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): o = K._c(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def key(s): return (s.a, s.b)
    def __repr__(s): return '(%s+%s*r2)' % (s.a, s.b)
    def sign(s):  # exact sign of a + b sqrt2
        a, b = s.a, s.b
        if b == 0: return (a > 0) - (a < 0)
        if a == 0: return (b > 0) - (b < 0)
        if a > 0 and b > 0: return 1
        if a < 0 and b < 0: return -1
        # opposite signs: compare a^2 vs 2b^2
        if a > 0: return 1 if a*a > 2*b*b else -1
        return -1 if a*a > 2*b*b else 1

R2 = K(0, 1)
def sqrt(x):
    assert K._c(x) == K(2); return R2

def P(expr):
    e = expr.replace('**', '^^')
    e = re.sub(r'(?<![\w.])(\d+)(?![\w.])', r'K(\1)', e)
    e = e.replace('^^', '**')
    return eval(e, {'K': K, 'sqrt': sqrt})

def load_lines():
    out = []
    for ln in open(D + 'lines_exact.txt'):
        if not ln.startswith('L'): continue
        name, rest = ln.split(':', 1)
        a, b = rest.split('|')
        out.append(([P(t) for t in eval(a)], [P(t) for t in eval(b)]))
    return out

def load_syms():
    out = []
    for ln in open(D + 'symmetry_exact.txt'):
        if not ln.startswith('g'): continue
        m = re.match(r'(g\d+) c=(\S+) M=(.*) sigma=(.*)$', ln.strip())
        c = P(m.group(2))
        Ms = m.group(3)
        rows = re.findall(r'\[([^\[\]]*)\]', Ms)
        M = [[P(t.strip()) for t in r.split(',')] for r in rows]
        out.append((m.group(1), c, M, json.loads(m.group(4))))
    return out

# ---- F as polynomial dict: exps -> K
def padd(p, q):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, K()) + v
        if r[k].z(): del r[k]
    return r
def pmul(p, q):
    r = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = tuple(x+y for x, y in zip(k1, k2)); r[k] = r.get(k, K()) + v1*v2
    return {k: v for k, v in r.items() if not v.z()}
def pscale(p, c): return {k: v*c for k, v in p.items() if not (v*c).z()}
def var(i):
    e = [0, 0, 0, 0]; e[i] = 1; return {tuple(e): K(1)}
# F = 3e z0^2 z1 z2 + 3e z1 z2 z3^2 - e z1^3 z2 - e z1 z2^3 + 4 z0^3 z3 - 4 z0 z3^3  (from README)
FT = {(2, 1, 1, 0): 3*R2, (0, 1, 1, 2): 3*R2, (0, 3, 1, 0): -R2, (0, 1, 3, 0): -R2, (3, 0, 0, 1): K(4), (1, 0, 0, 3): K(-4)}
def Fval(z):
    tot = K()
    for e, c in FT.items():
        t = c
        for i in range(4):
            for _ in range(e[i]): t = t * z[i]
        tot = tot + t
    return tot
def F_of_linear(forms):  # forms[i] = polynomial dict for z_i
    tot = {}
    for e, c in FT.items():
        t = {(0, 0, 0, 0): c}
        for i in range(4):
            for _ in range(e[i]): t = pmul(t, forms[i])
        tot = padd(tot, t)
    return tot

def det(M):
    M = [list(r) for r in M]; n = len(M); d = K(1)
    for c in range(n):
        p = next((r for r in range(c, n) if not M[r][c].z()), None)
        if p is None: return K()
        if p != c: M[c], M[p] = M[p], M[c]; d = -d
        d = d * M[c][c]; iv = M[c][c].inv()
        for r in range(c+1, n):
            f = M[r][c] * iv
            if not f.z(): M[r] = [M[r][k] - f*M[c][k] for k in range(n)]
    return d

def plucker(A, B):
    p = [A[i]*B[j] - A[j]*B[i] for i, j in itertools.combinations(range(4), 2)]
    k = next(i for i in range(6) if not p[i].z()); iv = p[k].inv()
    return tuple((x*iv).key() for x in p)

def matvec(M, v): return [sum((M[i][j]*v[j] for j in range(4)), K()) for i in range(4)]
def matmul(A, B): return [[sum((A[i][k]*B[k][j] for k in range(4)), K()) for j in range(4)] for i in range(4)]
def projkey(M):
    flat = [x for r in M for x in r]; k = next(x for x in flat if not x.z()); iv = k.inv()
    return tuple((x*iv).key() for x in flat)

out = []
def rep(s): print(s, flush=True); out.append(s)

L = load_lines(); rep('lines loaded: %d' % len(L))
# (a) on F: F(B + tA) is a quartic in t; vanishing at t = 0..4 and leading coefficient F(A)=0 -> identically 0
bad = []
for i, (A, B) in enumerate(L):
    vals = [Fval([B[k] + t*A[k] for k in range(4)]) for t in range(5)] + [Fval(A)]
    if not all(v.z() for v in vals): bad.append(i)
rep('(a) lines on F (5 points + point at infinity, quartic in t): failing %s' % bad)
# rank-2 check and distinctness by normalised Plucker vector
PL = [plucker(A, B) for A, B in L]
rep('(a) distinct Plucker classes: %d of %d' % (len(set(PL)), len(L)))
# Plucker relation sanity: p01 p23 - p02 p13 + p03 p12 = 0 is automatic; check reality: all coords in Q(sqrt2) by construction
# (b) intersection graph
E = set()
for i, j in itertools.combinations(range(56), 2):
    if det([L[i][0], L[i][1], L[j][0], L[j][1]]).z(): E.add((i, j))
deg = Counter(v for e in E for v in e)
rep('(b) meeting pairs %d; degree set %s' % (len(E), sorted(set(deg[i] for i in range(56)))))
sh = {tuple(e) for e in json.load(open(D + 'edges.json'))}
rep('(b) edges.json equal to own graph: %s' % (sh == E))
# (c) symmetries
S = load_syms(); rep('symmetries loaded: %d' % len(S))
Fp = dict(FT); okF = []; cs = []
plidx = {p: i for i, p in enumerate(PL)}
perms = []; sig_ok = True
for name, c, M, sig in S:
    forms = [{(1 if j == 0 else 0, 1 if j == 1 else 0, 1 if j == 2 else 0, 1 if j == 3 else 0): M[i][j] for j in range(4) if not M[i][j].z()} for i in range(4)]
    G = F_of_linear(forms)
    # find scalar
    lam = G[(3, 0, 0, 1)] / FT[(3, 0, 0, 1)] if (3, 0, 0, 1) in G else None
    ok = lam is not None and not lam.z() and padd(G, pscale(FT, -lam)) == {}
    okF.append(ok); cs.append(lam)
    perm = []
    for A, B in L:
        perm.append(plidx.get(plucker(matvec(M, A), matvec(M, B)), -1))
    perms.append(tuple(perm)); sig_ok &= (perm == list(sig))
rep('(c) F(Mz) = lam F(z) for all 32: %s; lam values %s' % (all(okF), sorted(set(str(x) for x in cs))))
rep('(c) own induced permutations map lines to lines: %s; equal shipped sigma: %s' % (all(-1 not in p for p in perms), sig_ok))
keys = [projkey(M) for _, _, M, _ in S]
rep('(c) distinct projective classes: %d' % len(set(keys)))
kset = set(keys); closed = all(projkey(matmul(A[2], B[2])) in kset for A in S for B in S)
rep('(c) matrix products closed projectively (group): %s' % closed)
rep('(c) permutation images distinct: %d' % len(set(perms)))
# element orders (projective)
def order(M):
    I = projkey([[K(1) if i == j else K() for j in range(4)] for i in range(4)]); X = M; n = 1
    while projkey(X) != I: X = matmul(X, M); n += 1
    return n
rep('(c) element orders %s' % sorted(Counter(order(s[2]) for s in S).items()))
seen = set(); orb = []
for i in range(56):
    if i in seen: continue
    o = {p[i] for p in perms}; seen |= o; orb.append(len(o))
rep('(c) line orbits %s' % sorted(orb))
# real matrices? all entries in Q(sqrt2) subset R: yes by construction
# (d) lattice of 56 lines + h
import sympy as sp
from sympy.matrices.normalforms import invariant_factors
from sympy.polys.domains import ZZ
n = 57
G = [[0]*n for _ in range(n)]
for i in range(56):
    G[i][i] = -2; G[i][56] = G[56][i] = 1
G[56][56] = 4
for i, j in E: G[i][j] = G[j][i] = 1
Gm = sp.Matrix(G)
rk = Gm.rank(); rep('(d) rank of Gram(56 lines + h) = %d' % rk)
inv = invariant_factors(Gm, domain=ZZ)
nz = [int(x) for x in inv if x != 0]
prod = 1
for x in nz: prod *= x
rep('(d) nonzero invariant factors (%d): %s ; product = |disc| = %d' % (len(nz), Counter(nz), prod))
ev = Gm.evalf(30).eigenvals(multiple=True) if False else None
# signature via LDL on an independent subset: greedy pick of 20 independent generators
idx = []
for k in range(n):
    if sp.Matrix([[G[a][b] for b in idx + [k]] for a in idx + [k]]).rank() == len(idx) + 1: idx.append(k)
    if len(idx) == rk: break
G0 = sp.Matrix([[G[a][b] for b in idx] for a in idx])
pos = sum(1 for v in G0.evalf(40).eigenvals(multiple=True) if sp.re(v) > 0)
rep('(d) signature of the line lattice: (%d, %d)' % (pos, rk - pos))
open(os.path.dirname(os.path.abspath(__file__)) + '/ref_checks.out', 'w').write('\n'.join(out) + '\n')
