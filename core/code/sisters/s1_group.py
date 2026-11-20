# EXACT (Q(sqrt2) arithmetic, Fractions): Aut(Y56) in PGL(4,C), its involution classes, and real lines of each sister.
import sys, pickle, itertools, time
sys.path.insert(0, '.')
from q2 import *
import sympy as sp, networkx as nx
t0 = time.time()
L = load_lines(); S = load_syms(); n = 56
# --- F and its check under each M (sympy, exact) ---
z = sp.symbols('z0:4'); r = sp.sqrt(2)
F = 3*r*z[0]**2*z[1]*z[2] + 3*r*z[1]*z[2]*z[3]**2 - r*z[1]**3*z[2] - r*z[1]*z[2]**3 + 4*z[0]**3*z[3] - 4*z[0]*z[3]**3
def F_after(M):
    Mz = [sum(M[i][j].sym()*z[j] for j in range(4)) for i in range(4)]
    return sp.expand(F.subs(dict(zip(z, Mz)), simultaneous=True))
okF = all(sp.expand(F_after(M) - c.sym()*F) == 0 for _, c, M, _ in S)
print('F(Mz) = c F(z) exactly for all 32 listed maps:', okF)
# --- lines lie on F (exact) ---
tt = sp.symbols('t')
okL = all(sp.expand(F.subs({z[i]: tt*l[0][i].sym() + l[1][i].sym() for i in range(4)}, simultaneous=True)) == 0 for l in L)
print('all 56 lines on F:', okL)
# --- normals of each line (2 covectors) ---
NRM = [nullspace([l[0], l[1]], 4) for l in L]
assert all(len(x) == 2 for x in NRM)
def meets(i, j): return det([L[i][0], L[i][1], L[j][0], L[j][1]]).iszero()
E = [(i, j) for i, j in itertools.combinations(range(n), 2) if meets(i, j)]
print('intersecting pairs (exact):', len(E), ' degrees:', sorted(set(sum(1 for e in E if k in e) for k in range(n))))
G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(E)
# --- listed permutations are correct (exact: M maps both spanning points of line i into line sigma(i)) ---
def maps_line(M, i, j):
    return all(dot(nv, matvec(M, p)).iszero() for nv in NRM[j] for p in L[i])
okP = all(maps_line(M, i, sig[i]) for _, _, M, sig in S for i in range(n))
print('listed line permutations verified exactly:', okP)
# --- full projective automorphism group: every automorphism of Y56 permutes lines -> a graph automorphism ---
GM = nx.algorithms.isomorphism.GraphMatcher(G, G)
autos = [tuple(m[i] for i in range(n)) for m in GM.isomorphisms_iter()]
print('graph automorphisms of the 56-line intersection graph:', len(autos))
def solve_M(perm):
    rows = []
    for i in range(n):
        for nv in NRM[perm[i]]:
            for p in L[i]:
                rows.append([nv[a]*p[b] for a in range(4) for b in range(4)])
    ns = nullspace(rows, 16)
    return ns
realised = []
for perm in autos:
    ns = solve_M(perm)
    if len(ns) == 0: continue
    assert len(ns) == 1, ('solution space dim', len(ns))
    M = [ns[0][4*i:4*i+4] for i in range(4)]
    realised.append((perm, M))
print('graph automorphisms realised by a projective map (solution space dim 1):', len(realised), '; the rest: dim 0')
# identity perm solution space dim 1 => faithful action on lines
assert any(perm == tuple(range(n)) for perm, _ in realised)
listed = {tuple(sig) for _, _, _, sig in S}
print('realised set == listed 32 permutations:', {p for p, _ in realised} == listed)
# realised maps preserve F (they must, being the listed ones; check directly anyway)
def prop(M, c):
    # is M proportional to some listed matrix?
    pass
# --- group structure on permutations ---
perms = [tuple(sig) for _, _, _, sig in S]; idx = {p: k for k, p in enumerate(perms)}
comp = lambda p, q: tuple(p[q[i]] for i in range(n))     # (p o q)(i) = p(q(i))
inv = lambda p: tuple(sorted(range(n), key=lambda i: p[i]))
assert all(comp(p, q) in idx for p in perms for q in perms)
def order(p):
    k, q = 1, p
    while q != tuple(range(n)): q = comp(p, q); k += 1
    return k
orders = [order(p) for p in perms]
print('element orders:', {o: orders.count(o) for o in sorted(set(orders))})
# --- conjugacy classes of elements with g^2 = 1 ---
seen = set(); classes = []
for k, p in enumerate(perms):
    if orders[k] > 2 or k in seen: continue
    cl = sorted({idx[comp(comp(h, p), inv(h))] for h in perms}); seen |= set(cl); classes.append(cl)
print('classes of {1} + involutions:', len(classes), [len(c) for c in classes])
# --- matrix side: M^2 = lambda I with lambda > 0 (so g o conj has real points in P^3) ---
res = []
for cl in classes:
    k = cl[0]; name, c, M, sig = S[k]
    M2 = matmul(M, M)
    lam = M2[0][0]; scal = all((M2[i][j] == (lam if i == j else Q2())) for i in range(4) for j in range(4))
    allsc = []
    for kk in cl:
        N2 = matmul(S[kk][2], S[kk][2]); l2 = N2[0][0]
        allsc.append(all((N2[i][j] == (l2 if i == j else Q2())) for i in range(4) for j in range(4)) and l2.sign() > 0)
    fixed = [i for i in range(n) if sig[i] == i]
    # centraliser order (= 32 / class size)
    res.append(dict(rep=name, members=[S[kk][0] for kk in cl], size=len(cl), c=c, lam=lam, scalar=scal, all_pos=all(allsc),
                    fixed=fixed, nfixed=len(fixed), M=M, sig=sig))
    print(f'{name} class size {len(cl)} members {[S[kk][0] for kk in cl]}  c={c}  M^2 = {lam} * I: {scal}, lambda>0 for all members: {all(allsc)}  fixed lines {len(fixed)}')
# twisted-conjugacy == conjugacy because every automorphism matrix is real (all in Q(sqrt2)); check reality is trivially true here.
# A sigma-invariant line in a real structure with lambda>0 is a real line of a real P^3 => has a real circle.
# Still, verify directly per fixed line: 2x2 matrix A of M on the line; A^2 = lambda I with lambda>0 -> real eigenvector exists.
for d in res:
    M = d['M']; ok = True
    for i in d['fixed']:
        p, q = L[i]
        # solve M p = a p + b q, M q = c p + e q via 2 coordinates where (p,q) is invertible
        cols = next((a, b) for a, b in itertools.combinations(range(4), 2) if not (p[a]*q[b] - p[b]*q[a]).iszero())
        B2 = [[p[cols[0]], q[cols[0]]], [p[cols[1]], q[cols[1]]]]
        dd = B2[0][0]*B2[1][1] - B2[0][1]*B2[1][0]
        Bi = [[B2[1][1]/dd, -B2[0][1]/dd], [-B2[1][0]/dd, B2[0][0]/dd]]
        Mp, Mq = matvec(M, p), matvec(M, q)
        A = [[None, None], [None, None]]
        for col, v in enumerate((Mp, Mq)):
            co = matvec(Bi, [v[cols[0]], v[cols[1]]])
            assert all((co[0]*p[k] + co[1]*q[k] - v[k]).iszero() for k in range(4))
            A[0][col], A[1][col] = co
        A2 = matmul(A, A)
        ok &= A2[0][1].iszero() and A2[1][0].iszero() and A2[0][0] == A2[1][1] and A2[0][0].sign() > 0
    d['fixed_lines_have_real_circle'] = ok
    print(d['rep'], 'every fixed line carries a real circle (A^2 = lambda I, lambda>0):', ok)
pickle.dump(dict(res=res, E=E, autos_realised=len(realised), n_autos=len(autos)), open('s1_group.pkl', 'wb'))
print('time %.1fs' % (time.time() - t0))
