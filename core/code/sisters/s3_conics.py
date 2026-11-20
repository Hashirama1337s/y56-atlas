# EXACT: which of the 188 irreducible conics of Y56 are real for each sister real structure sigma_g = g o conj,
# and whether each such conic has real points (definite vs indefinite real form), all in Q(sqrt2) with exact signs.
import sys, pickle, itertools, time
sys.path.insert(0, '.')
from q2 import *
import sympy as sp
t0 = time.time()
L = load_lines(); S = load_syms(); P2, P4 = load_planes(); CPP = load_cpp()
res = pickle.load(open('s1_group.pkl', 'rb'))['res']
# ---- tiny polynomial algebra over Q(sqrt2) in 3 variables ----
def padd(a, b):
    c = dict(a)
    for k, v in b.items():
        c[k] = c.get(k, Q2()) + v
    return {k: v for k, v in c.items() if not v.iszero()}
def pmul(a, b):
    c = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = tuple(x+y for x, y in zip(k1, k2)); c[k] = c.get(k, Q2()) + v1*v2
    return {k: v for k, v in c.items() if not v.iszero()}
def pscale(a, s): return {k: v*s for k, v in a.items() if not (v*s).iszero()}
def lin(coefs): return {tuple(1 if j == k else 0 for j in range(3)): c for k, c in enumerate(coefs) if not c.iszero()}
r2 = Q2(0, 1)
FMON = [(3*r2, (2, 1, 1, 0)), (3*r2, (0, 1, 1, 2)), (-r2, (0, 3, 1, 0)), (-r2, (0, 1, 3, 0)), (Q2(4), (3, 0, 0, 1)), (Q2(-4), (1, 0, 0, 3))]
def F_on_plane(P):
    zs = [lin([P[i][k] for k in range(3)]) for i in range(4)]
    out = {}
    for c, e in FMON:
        t = {(0, 0, 0): c}
        for i in range(4):
            for _ in range(e[i]): t = pmul(t, zs[i])
        out = padd(out, t)
    return out
def plane_param(nv):
    i = next(j for j in range(4) if not nv[j].iszero()); oth = [j for j in range(4) if j != i]
    P = [[Q2() for _ in range(3)] for _ in range(4)]
    for k, o in enumerate(oth): P[o][k] = Q2(1); P[i][k] = -nv[o]/nv[i]
    return P
def quad_from_sym(Qm):   # symmetric 3x3 -> poly
    out = {}
    for a in range(3):
        for b in range(3):
            k = tuple((a == j) + (b == j) for j in range(3)); out[k] = out.get(k, Q2()) + Qm[a][b]
    return {k: v for k, v in out.items() if not v.iszero()}
MONO2 = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
def solve_residual(Fp, l1, l2):
    """find symmetric Q with Fp = l1*l2*Q exactly"""
    base = pmul(l1, l2); cols = []
    for a, b in MONO2:
        Qm = [[Q2() for _ in range(3)] for _ in range(3)]; Qm[a][b] = Q2(1); Qm[b][a] = Q2(1) if a != b else Q2(1)
        if a != b: Qm[a][b] = Q2(Fr(1, 2)); Qm[b][a] = Q2(Fr(1, 2))
        cols.append(pmul(base, quad_from_sym(Qm)))
    keys = sorted(set(Fp) | set(k for c in cols for k in c))
    rows = [[c.get(k, Q2()) for c in cols] + [Fp.get(k, Q2())] for k in keys]
    R_, piv = rref(rows); assert 6 not in piv, 'inconsistent: residual not a conic'
    assert len(piv) == 6
    x = [R_[piv.index(j)][6] for j in range(6)]
    Qm = [[Q2() for _ in range(3)] for _ in range(3)]
    for (a, b), v in zip(MONO2, x):
        if a == b: Qm[a][a] = v
        else: Qm[a][b] = Qm[b][a] = v/2
    assert padd(pmul(base, quad_from_sym(Qm)), pscale(Fp, Q2(-1))) == {}
    return Qm
def line_form(li, P):
    for nv in nullspace([L[li][0], L[li][1]], 4):
        f = [dot(nv, [P[i][k] for i in range(4)]) for k in range(3)]
        if any(not x.iszero() for x in f): return f
# ---- build all 188 conics as (plane P, symmetric matrix Q, plane lines, tag) ----
conics = []
for nv, lines in P2:
    P = plane_param(nv); Fp = F_on_plane(P)
    l1, l2 = line_form(lines[0], P), line_form(lines[1], P)
    Qm = solve_residual(Fp, lin(l1), lin(l2))
    d = det(Qm); assert not d.iszero()
    conics.append(dict(kind='res', P=P, n=nv, Q=Qm, lines=lines))
x_, y_, w_ = sp.symbols('x y w')
def sym_to_Qm(expr):
    pol = sp.Poly(sp.expand(sp.sympify(expr)), x_, y_, w_); Qm = [[Q2() for _ in range(3)] for _ in range(3)]
    for mon, c in zip(pol.monoms(), pol.coeffs()):
        idx = [k for k in range(3) for _ in range(mon[k])]
        v = parse(c)
        if idx[0] == idx[1]: Qm[idx[0]][idx[0]] = v
        else: Qm[idx[0]][idx[1]] = Qm[idx[1]][idx[0]] = v/2
    return Qm
for lab, nv, q1, q2 in CPP:
    P = plane_param(nv); Fp = F_on_plane(P)
    A1, A2 = sym_to_Qm(q1), sym_to_Qm(q2)
    prod = pmul(quad_from_sym(A1), quad_from_sym(A2))
    k0 = next(iter(prod)); cst = Fp[k0]/prod[k0]
    assert padd(Fp, pscale(prod, -cst)) == {}, 'conic-pair factorisation fails'
    assert not det(A1).iszero() and not det(A2).iszero()
    conics.append(dict(kind='cpp', P=P, n=nv, Q=A1, orbit=lab)); conics.append(dict(kind='cpp', P=P, n=nv, Q=A2, orbit=lab))
print('conics built and verified exactly:', len(conics), '(148 residual: F|plane = l1 l2 Q; 40 pair: F|plane = c Q1 Q2)')
# ---- per real structure ----
def sqrt_pos(lam):
    if lam == Q2(1): return Q2(1)
    if lam == Q2(2): return Q2(0, 1)
    if lam == Q2(4): return Q2(2)
    raise ValueError(lam)
def eig_basis(Gp, s):
    return nullspace([[Gp[i][j] - (s if i == j else Q2()) for j in range(3)] for i in range(3)], 3)
def nposroots(Rm):
    tr = Rm[0][0] + Rm[1][1] + Rm[2][2]
    m2 = sum((Rm[a][a]*Rm[b][b] - Rm[a][b]*Rm[b][a] for a, b in [(0, 1), (0, 2), (1, 2)]), Q2())
    dt = det(Rm)
    co = [1, (-tr).sign(), m2.sign(), (-dt).sign()]
    co = [c for c in co if c != 0]
    return sum(1 for a, b in zip(co, co[1:]) if a != b), dt
summary = {}
for d in res:
    name = d['rep']; M = d['M']; lam = matmul(M, M)[0][0]; sq = sqrt_pos(lam)
    Mp = [[x/sq for x in row] for row in M]
    inv_res = inv_cpp = 0; real_res = real_cpp = 0; empty = []; swapped_pairs = 0; details = []
    for ci, C in enumerate(conics):
        P, nv, Qm = C['P'], C['n'], C['Q']
        # plane invariant? n M proportional to n
        nM = [sum((nv[i]*Mp[i][j] for i in range(4)), Q2()) for j in range(4)]
        if rank([nv, nM]) > 1: continue
        # restriction G: Mp P = P G
        MP = matmul(Mp, P)
        G = []
        cols = []
        for k in range(3):
            # solve P g = MP[:,k]
            A = [[P[i][j] for j in range(3)] + [MP[i][k]] for i in range(4)]
            R_, piv = rref(A); assert 3 not in piv
            cols.append([R_[piv.index(j)][3] for j in range(3)])
        G = [[cols[k][i] for k in range(3)] for i in range(3)]
        GtQG = matmul(matmul([list(r) for r in zip(*G)], Qm), G)
        # conic invariant iff G^T Q G = kappa Q
        kappa = None
        a0, b0 = next((a, b) for a in range(3) for b in range(3) if not Qm[a][b].iszero())
        kap = GtQG[a0][b0]/Qm[a0][b0]
        if not all((GtQG[a][b] - kap*Qm[a][b]).iszero() for a in range(3) for b in range(3)):
            swapped_pairs += 1; continue        # plane fixed but the two conics are exchanged
        assert kap == Q2(1) or kap == Q2(-1)
        Ep, Em = eig_basis(G, Q2(1)), eig_basis(G, Q2(-1)); assert len(Ep) + len(Em) == 3
        Bv = Ep + Em; npl = len(Ep)
        Rm = [[None]*3 for _ in range(3)]
        for a in range(3):
            for b in range(3):
                v = dot(Bv[a], matvec(Qm, Bv[b]))
                ia, ib = a >= npl, b >= npl     # True = imaginary direction (i * E-)
                if kap == Q2(1):
                    Rm[a][b] = (-v if (ia and ib) else v) if ia == ib else Q2()
                    if ia != ib: assert v.iszero()
                else:
                    if ia == ib: assert v.iszero(); Rm[a][b] = Q2()
                    else: Rm[a][b] = v
        npos, dt = nposroots(Rm); assert not dt.iszero()
        has_real = 0 < npos < 3
        if C['kind'] == 'res': inv_res += 1; real_res += has_real
        else: inv_cpp += 1; real_cpp += has_real
        if not has_real: empty.append(ci)
        details.append((ci, C['kind'], has_real))
    summary[name] = dict(inv_res=inv_res, real_res=real_res, inv_cpp=inv_cpp, real_cpp=real_cpp, swapped_pair_halves=swapped_pairs, empty=empty, details=details)
    print(f"{name}: sigma-real conics: residual {inv_res} (with real points {real_res}), pair-plane {inv_cpp} (with real points {real_cpp}); "
          f"total {inv_res+inv_cpp} invariant, {real_res+real_cpp} with a real oval; conics in fixed pair-planes that are swapped: {swapped_pairs}")
pickle.dump(dict(summary=summary, conics=[(C['kind'], [[float(x) for x in r] for r in C['P']], [[float(x) for x in r] for r in C['Q']]) for C in conics]),
            open('s3_conics.pkl', 'wb'))
print('time %.1fs' % (time.time() - t0))
