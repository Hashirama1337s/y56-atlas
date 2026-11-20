"""verify_all.py: one-command exact re-check of the Y56 data in ../data (nothing else is read).
Run from anywhere:  python code/verify_all.py        (a few minutes; needs sympy)
Checks are in exact arithmetic over Q(sqrt2); each prints PASS or FAIL.
Not re-run here (see the shipped transcripts): Singular Fano-scheme length 56 (data/logs/fano_rerun.out),
msolve degree 112 (data/logs/analyze.log), GAP group id (data/gap_out.txt), the line lattice
(data/lat.txt, data/lat_lines.txt, code/exact2/l2.py, l3.py)."""
import os, sys, json, itertools, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data') + os.sep
sys.path.insert(0, os.path.join(HERE, 'sisters'))
import sympy as sp
import q2
from q2 import Q2, rref, det, dot, matvec, load_lines, load_syms, load_planes, load_cpp

T0 = time.time(); RES = []
def check(name, ok, detail=''):
    RES.append((name, bool(ok))); print(('PASS ' if ok else 'FAIL ') + name + (' : ' + detail if detail else ''), flush=True)

r2 = sp.sqrt(2)
Z = sp.symbols('z0 z1 z2 z3'); x, y, w = sp.symbols('x y w')
F = 3*r2*Z[0]**2*Z[1]*Z[2] + 3*r2*Z[1]*Z[2]*Z[3]**2 - r2*Z[1]**3*Z[2] - r2*Z[1]*Z[2]**3 + 4*Z[0]**3*Z[3] - 4*Z[0]*Z[3]**3
# F as (coefficient in Q(sqrt2), exponents of z0..z3)
TERMS = [(Q2(0, 3), (2, 1, 1, 0)), (Q2(0, 3), (0, 1, 1, 2)), (Q2(0, -1), (0, 3, 1, 0)),
         (Q2(0, -1), (0, 1, 3, 0)), (Q2(4), (3, 0, 0, 1)), (Q2(-4), (1, 0, 0, 3))]

def pmul(p, q):
    out = [Q2() for _ in range(len(p)+len(q)-1)]
    for i, a in enumerate(p):
        for j, b in enumerate(q): out[i+j] = out[i+j] + a*b
    return out
def line_poly_F(A, B):
    pts = [[B[k], A[k]] for k in range(4)]            # z_k = A_k t + B_k
    tot = [Q2() for _ in range(5)]
    for c, e in TERMS:
        p = [Q2(1)]
        for k in range(4):
            for _ in range(e[k]): p = pmul(p, pts[k])
        for i, v in enumerate(p): tot[i] = tot[i] + c*v
    return tot
def canon_line(A, B):
    R, piv = rref([A, B]); assert len(R) == 2
    return tuple(tuple((t.a, t.b) for t in row) for row in R)
def canon_vec(n):
    i = max(j for j in range(len(n)) if not n[j].iszero()); iv = n[i].inv()
    return tuple((t*iv).a for t in n) + tuple((t*iv).b for t in n)
def normal_of_plane(rows):
    R, piv = rref(rows); assert len(R) == 3, 'not a plane'
    free = [c for c in range(4) if c not in piv][0]
    v = [Q2() for _ in range(4)]; v[free] = Q2(1)
    for i, p in enumerate(piv): v[p] = -R[i][free]
    return v

L = load_lines(); S = load_syms(); P2, P4 = load_planes(); CPP = load_cpp()
cnt = (len(L), len(S), len(P2), len(P4), len(CPP))
check('data loads: 56 lines, 32 symmetries, 148 + 50 line planes, 20 conic-pair planes', cnt == (56, 32, 148, 50, 20), str(cnt))

# 1. lines lie on F, pairwise distinct
bad = [i for i, (A, B) in enumerate(L) if not all(c.iszero() for c in line_poly_F(A, B))]
check('1a all 56 lines lie on F = 0 (F(tA+B) is identically 0 over Q(sqrt2))', not bad, 'failing: %s' % bad)
canon = [canon_line(A, B) for A, B in L]
check('1b the 56 lines are pairwise distinct', len(set(canon)) == 56)

# 2. intersection graph
edges = set()
for i, j in itertools.combinations(range(56), 2):
    if det([L[i][0], L[i][1], L[j][0], L[j][1]]).iszero(): edges.add((i, j))
deg = Counter(v for e in edges for v in e)
check('2a intersection graph has 448 edges and is 16-regular', len(edges) == 448 and all(deg[i] == 16 for i in range(56)),
      'edges %d, degrees %s' % (len(edges), sorted(set(deg.values()))))
shipped = {tuple(e) for e in json.load(open(DATA + 'edges.json'))}
check('2b edge list in data/edges.json equals the recomputed one', shipped == edges)

# 3. symmetries
ok3 = True; ok3b = True; ok3c = True
for name, c, M, sig in S:
    Ms = sp.Matrix([[t.sym() for t in row] for row in M])
    zz = Ms*sp.Matrix(Z)
    e = sp.expand(sp.radsimp(sp.expand(F.subs(dict(zip(Z, zz)), simultaneous=True) - c.sym()*F)))
    ok3 &= (e == 0 and c.sign() != 0)
    ok3c &= (not det(M).iszero())
    for i in range(56):
        if canon_line(matvec(M, L[i][0]), matvec(M, L[i][1])) != canon[sig[i]]: ok3b = False
check('3a all 32 matrices satisfy F(Mz) = c F(z) with c a nonzero real scalar in Q(sqrt2); matrices invertible', ok3 and ok3c)
check('3b each matrix maps line i to line sigma[i] as listed; sigma are permutations', ok3b and all(sorted(s[3]) == list(range(56)) for s in S))
perms = [tuple(s[3]) for s in S]; PS = set(perms)
closed = all(tuple(p[q[i]] for i in range(56)) in PS for p in perms for q in perms)
check('3c the 32 line permutations are distinct and closed under composition (a group of order 32)', len(PS) == 32 and closed)

def orbits_of(items, act):
    seen = set(); sizes = []
    for it in items:
        if it in seen: continue
        o = {act(p, it) for p in perms}; seen |= o; sizes.append(len(o))
    return sorted(sizes, reverse=True)
lo = orbits_of(range(56), lambda p, i: p[i])
check('3d orbits of the group on the 56 lines: 16 + 16 + 16 + 8', lo == [16, 16, 16, 8], str(lo))

# 4. planes containing lines, recomputed from scratch from the 448 meeting pairs
planes = {}
for i, j in edges:
    n = canon_vec(normal_of_plane([L[i][0], L[i][1], L[j][0], L[j][1]]))
    planes.setdefault(n, set()).update([i, j])
sets = Counter(len(v) for v in planes.values())
check('4a the 448 meeting pairs lie in 148 two-line planes and 50 four-line planes (148 + 6 x 50 = 448)',
      sets == Counter({2: 148, 4: 50}), str(dict(sets)))
shipped_pl = {canon_vec(n): set(ls) for n, ls in P2 + P4}
check('4b the shipped plane list equals the recomputed one (normals and line sets)', shipped_pl == planes)
okc = True
for n, ls in P2 + P4:
    okc &= ({k for k in range(56) if all(dot(n, row).iszero() for row in L[k])} == set(ls))
check('4c each listed plane contains exactly its listed lines (all 56 lines tested)', okc)

def section(n):
    i = [j for j in range(4) if not n[j].iszero()][0]
    ns = [t.sym() for t in n]; oth = [j for j in range(4) if j != i]
    sub = {Z[o]: v for o, v in zip(oth, (x, y, w))}
    sub[Z[i]] = -sum(ns[j]*sub[Z[j]] for j in oth)/ns[i]
    return sp.expand(sp.radsimp(sp.expand(F.subs(sub, simultaneous=True))))
def sdeg(f): return sp.Poly(f, x, y, w).total_degree()
def gram(f):
    H = sp.hessian(f, (x, y, w))/2
    return [[q2.parse(sp.radsimp(sp.expand(H[i, j]))) for j in range(3)] for i in range(3)]

t1 = time.time(); bad = []; conic_gram = []
for k, (n, ls) in enumerate(P2):
    fl = sp.factor_list(section(n), extension=r2)
    if sorted((sdeg(f), e) for f, e in fl[1]) == [(1, 1), (1, 1), (2, 1)]:
        conic_gram.append(gram([f for f, e in fl[1] if sdeg(f) == 2][0]))
    else: bad.append(k)
degenerate = [k for k, g in enumerate(conic_gram) if det(g).iszero()]
check('4d 148 two-line planes: section = line x line x irreducible nondegenerate conic over Q(sqrt2) (det of the 3x3 conic matrix != 0)', not bad and not degenerate and len(conic_gram) == 148,
      'bad %s, degenerate %s (%.0f s)' % (bad, degenerate, time.time()-t1))
t1 = time.time(); bad = []
for k, (n, ls) in enumerate(P4):
    fl = sp.factor_list(section(n), extension=r2)
    if sorted((sdeg(f), e) for f, e in fl[1]) != [(1, 1)]*4: bad.append(k)
check('4e 50 four-line planes: section = four distinct lines over Q(sqrt2)', not bad, 'bad %s (%.0f s)' % (bad, time.time()-t1))

# 5. the 20 conic-pair planes
t1 = time.time(); bad = []; pair_gram = []; nolines = True
for k, (lab, n, qa, qb) in enumerate(CPP):
    nolines &= not any(all(dot(n, row).iszero() for row in L[i]) for i in range(56))
    G = section(n)
    f1 = sp.sympify(qa, locals={'x': x, 'y': y, 'w': w}); f2 = sp.sympify(qb, locals={'x': x, 'y': y, 'w': w})
    prod = sp.expand(sp.radsimp(sp.expand(f1*f2)))
    const = False
    if prod != 0:
        pp = sp.Poly(prod, x, y, w); gg = sp.Poly(G, x, y, w)
        mon = pp.monoms()[0]
        cc = sp.radsimp(gg.coeff_monomial(mon)/pp.coeff_monomial(mon))     # candidate constant
        const = cc != 0 and sp.expand(sp.radsimp(sp.expand(G - cc*prod))) == 0
    fl = sp.factor_list(G, extension=r2)
    irr = sorted((sdeg(f), e) for f, e in fl[1]) == [(2, 1), (2, 1)]
    gs = [gram(f1), gram(f2)]
    if not (const and irr and all(not det(g).iszero() for g in gs)): bad.append(k)
    pair_gram += gs
check('5a 20 conic-pair planes: section = nonzero constant x Q1 x Q2, Q1 and Q2 irreducible over Q(sqrt2) and nondegenerate',
      not bad and len(pair_gram) == 40, 'bad %s (%.0f s)' % (bad, time.time()-t1))
check('5b none of the 56 lines lies in any of the 20 conic-pair planes', nolines)

# 6. real points: a nondegenerate conic has real points iff its Gram matrix is not definite (exact signs)
def definite(g):
    s = (g[0][0].sign(), det([g[0][:2], g[1][:2]]).sign(), det(g).sign())
    return s == (1, 1, 1) or s == (-1, 1, -1)
nd = [i for i, g in enumerate(pair_gram) if definite(g)]
check('6a all 40 conics of the conic-pair planes have real points (Gram matrix indefinite)', not nd and len(pair_gram) == 40, 'definite: %s' % nd)
nd = [i for i, g in enumerate(conic_gram) if definite(g)]
check('6b all 148 conics of the two-line planes have real points (Gram matrix indefinite)', not nd and len(conic_gram) == 148, 'definite: %s' % nd)

# 7. orbits of planes
def act_plane(p, fs): return frozenset(p[i] for i in fs)
o2 = orbits_of([frozenset(ls) for n, ls in P2], act_plane); o4 = orbits_of([frozenset(ls) for n, ls in P4], act_plane)
check('7a orbits on the 148 two-line planes: 32, 16 x 6, 8, 8, 4', o2 == [32, 16, 16, 16, 16, 16, 16, 8, 8, 4], str(o2))
check('7b orbits on the 50 four-line planes: 16, 16, 16, 2', o4 == [16, 16, 16, 2], str(o4))
MiT = []
for name, c, M, sig in S:
    Mm = sp.Matrix([[t.sym() for t in row] for row in M]).inv().T
    MiT.append([[q2.parse(sp.radsimp(sp.expand(Mm[i, j]))) for j in range(4)] for i in range(4)])
cset = {canon_vec(n) for lab, n, a, b in CPP}; seen = set(); osz = []; closed = True
for lab, n, a, b in CPP:
    if canon_vec(n) in seen: continue
    o = {canon_vec(matvec(Mi, n)) for Mi in MiT}
    closed &= o <= cset; seen |= o; osz.append(len(o))
check('7c orbits on the 20 conic-pair planes: 8, 8, 4 (list closed under the group)',
      closed and len(cset) == 20 and sorted(osz, reverse=True) == [8, 8, 4], str(sorted(osz, reverse=True)))

bad = [n for n, ok in RES if not ok]
print('\nSUMMARY: %d checks, %d PASS, %d FAIL, %.0f s' % (len(RES), len(RES)-len(bad), len(bad), time.time()-T0))
print('Recorded elsewhere, not re-run here: Singular Fano scheme length 56 -> data/logs/fano_rerun.out; '
      'msolve degree 112 -> data/logs/analyze.log; group id -> data/gap_out.txt')
sys.exit(1 if bad else 0)
