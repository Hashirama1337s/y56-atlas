"""Referee part 3: (i) own backtracking count of line-graph automorphisms (second algorithm, not networkx);
(ii) involutions, their conjugacy classes, fixed lines (= real lines of conj o g, since every line is defined over R);
(iii) Euler numbers 2 - tr(g | N) via the lattice action; (iv) nondegeneracy of the 148 conics (Hessian det != 0)."""
import os, sys, json, itertools
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'core')
sys.argv = [sys.argv[0], ROOT]
exec(open(os.path.dirname(os.path.abspath(__file__)) + '/ref_checks_core.py').read())
out2 = []
def rep2(s): print(s, flush=True); out2.append(s)
adj = [set() for _ in range(56)]
for i, j in E: adj[i].add(j); adj[j].add(i)
# (i) automorphisms by backtracking in BFS order, pruned by common-neighbour counts (exact, complete search)
A = [[1 if j in adj[i] else 0 for j in range(56)] for i in range(56)]
CN = [[len(adj[i] & adj[j]) for j in range(56)] for i in range(56)]
inv = [tuple(sorted(CN[i][j] for j in range(56) if j != i)) for i in range(56)]
order_ = [0]; seen = {0}; parent = {0: None}
for v in order_:
    for w in sorted(adj[v]):
        if w not in seen: seen.add(w); order_.append(w); parent[w] = v
cnt = 0; auts = []
def bt(k, img, used):
    global cnt
    if k == 56:
        cnt += 1; auts.append(tuple(img[i] for i in range(56))); return
    v = order_[k]
    cand = range(56) if parent[v] is None else sorted(adj[img[parent[v]]])
    for c in cand:
        if c in used or inv[c] != inv[v]: continue
        ok = True
        for u, iu in img.items():
            if A[u][v] != A[iu][c] or CN[u][v] != CN[iu][c]: ok = False; break
        if ok:
            img[v] = c; used.add(c); bt(k+1, img, used); del img[v]; used.discard(c)
bt(0, {}, set())
rep2('(i) line-graph automorphisms (own backtracking): %d' % cnt)
PS = set(perms)
rep2('(i) the 32 projective permutations are among them: %s' % PS.issubset(set(auts)))
# (ii) involutions and conjugacy classes
def comp(p, q): return tuple(p[q[i]] for i in range(56))
def invp(p):
    r = [0]*56
    for i, v in enumerate(p): r[v] = i
    return tuple(r)
ident = tuple(range(56))
invs = [p for p in perms if comp(p, p) == ident]
classes = []; done = set()
for p in invs:
    if p in done: continue
    cl = {comp(comp(g, p), invp(g)) for g in perms}; done |= cl; classes.append(cl)
info = []
# lattice action: coordinates of lines in a Z-basis (from ref_conics approach) -> trace via permutation of generators
import sympy as sp
n = 57
Gl = [[0]*n for _ in range(n)]
for i in range(56): Gl[i][i] = -2; Gl[i][56] = Gl[56][i] = 1
Gl[56][56] = 4
for i, j in E: Gl[i][j] = Gl[j][i] = 1
GM = sp.Matrix(Gl)
# choose 20 independent generators
idx = []
for k in range(n):
    if sp.Matrix([[Gl[a][b] for b in idx+[k]] for a in idx+[k]]).det() != 0: idx.append(k)
    if len(idx) == 20: break
G0 = sp.Matrix([[Gl[a][b] for b in idx] for a in idx]); G0i = G0.inv()
def coords(g): return G0i * sp.Matrix([Gl[a][g] for a in idx])
C = [coords(g) for g in range(n)]
for cl in classes:
    p = next(iter(cl)) ; fixed = sum(1 for i in range(56) if p[i] == i)
    pe = list(p) + [56]
    # matrix of g on N in basis idx: column k = coords of image of generator idx[k]
    Mg = sp.Matrix.hstack(*[C[pe[g]] for g in idx])
    tr = Mg.trace()
    info.append((len(cl), fixed, 2 - tr))
info.sort(key=lambda t: -t[1])
rep2('(ii)/(iii) involution classes incl. identity: %d; (class size, real lines, Euler 2 - tr(g|N)): %s' % (len(classes), info))
rep2('       total real structures (identity + involutions): %d' % len(invs))
# (iv) nondegeneracy of the 148 two-line-plane conics
x, y, w = sp.symbols('x y w'); Zs = sp.symbols('z0 z1 z2 z3'); r2 = sp.sqrt(2)
Fs = 3*r2*Zs[0]**2*Zs[1]*Zs[2] + 3*r2*Zs[1]*Zs[2]*Zs[3]**2 - r2*Zs[1]**3*Zs[2] - r2*Zs[1]*Zs[2]**3 + 4*Zs[0]**3*Zs[3] - 4*Zs[0]*Zs[3]**3
P2 = []
for ln in open(ROOT + '/data/planes_exact.txt'):
    if ln.startswith('P2 '):
        a = ln[3:ln.index(' lines')]; P2.append([sp.nsimplify(sp.sympify(t)) for t in eval(a)])
bad = []; dets = 0; signs_bad = []
for nvec in P2:
    i0 = next(j for j in range(4) if nvec[j] != 0); oth = [j for j in range(4) if j != i0]
    sub = {Zs[o]: v for o, v in zip(oth, (x, y, w))}; sub[Zs[i0]] = -sum(nvec[j]*sub[Zs[j]] for j in oth)/nvec[i0]
    S_ = sp.expand(sp.radsimp(sp.expand(Fs.subs(sub, simultaneous=True))))
    fl = sp.factor_list(S_, extension=r2)
    q = [f for f, e in fl[1] if sp.Poly(f, x, y, w).total_degree() == 2]
    if len(q) != 1: bad.append(nvec); continue
    H = sp.hessian(q[0], (x, y, w))
    d = sp.radsimp(sp.expand(H.det()))
    if d == 0: bad.append(nvec)
    else: dets += 1
rep2('(iv) 148 conics with nonzero Hessian det: %d; problems: %d' % (dets, len(bad)))
open(os.path.dirname(os.path.abspath(__file__)) + '/ref_extra.out', 'w').write('\n'.join(out2) + '\n')
