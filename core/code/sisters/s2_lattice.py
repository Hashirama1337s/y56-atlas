# EXACT integer lattice computation for the six real structures sigma_g = g o conj of Y56.
# (a) Lefschetz: chi(X_R) = 2 + tr(sigma*|H^2) = 2 - tr(g*|NS)  (conj* = -1 on NS; trace 0 on the period plane = T (x) R).
# (b) Nikulin invariants (r,a,delta) of L+ = {x in H^2(X,Z): sigma* x = x}, using H^2 = unimodular overlattice of NS (+) T,
#     NS = Z-span of the 56 lines (|disc| 64; T = [2,0,32] from DIS Table 2), glued along every anti-isometry of discriminant forms.
import sys, pickle, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '.')
from q2 import load_syms, det as qdet, Q2
import flint
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_decomp
S = load_syms(); d1 = pickle.load(open('s1_group.pkl', 'rb')); E = d1['E']; res = d1['res']
n = 56
G = [[-2 if i == j else 0 for j in range(n)] for i in range(n)]
for i, j in E: G[i][j] = G[j][i] = 1
Gq = flint.fmpq_mat(G)
print('rank of 56x56 intersection matrix:', Gq.rank())
# rational basis B of 20 lines (greedy)
B = []
for i in range(n):
    if flint.fmpq_mat([G[k] for k in B + [i]]).rank() > len(B): B.append(i)
assert len(B) == 20
GB = flint.fmpq_mat([[G[a][b] for b in B] for a in B]); GBi = GB.inv()
C = GBi * flint.fmpq_mat([[G[a][j] for j in range(n)] for a in B])      # 20 x 56: B-coordinates of each line
# check: Gram reproduced
assert all(( (C.transpose()*GB*C)[i, j] == G[i][j]) for i in range(n) for j in range(n))
# Z-basis of N = Z-span of lines
den = 1
for i in range(20):
    for j in range(n): den = int(den*int(C[i, j].q)) // __import__("math").gcd(den, int(C[i, j].q))
Cint = flint.fmpz_mat([[int(C[i, j]*den) for i in range(20)] for j in range(n)])   # 56 x 20
H = Cint.hnf(); Zb = [[Fr(int(H[i, j]), den) for j in range(20)] for i in range(20)]
assert all(H[i, j] == 0 for i in range(20, n) for j in range(20))
Zm = flint.fmpq_mat([[flint.fmpq(x.numerator, x.denominator) for x in row] for row in Zb])   # rows = Z-basis in B-coords
GZ = Zm*GB*Zm.transpose()
GZi = flint.fmpz_mat([[int(GZ[i, j]) for j in range(20)] for i in range(20)])
assert all(GZ[i, j].q == 1 for i in range(20) for j in range(20))
print('Z-basis of the line lattice N: det Gram =', GZi.det(), ' even:', all(int(GZ[i, i]) % 2 == 0 for i in range(20)))
Zinv = Zm.inv()
def gZ(sig):
    """matrix of g on N in the Z-basis, row convention: (row vector of Z-coords) -> row vector"""
    A = flint.fmpq_mat([[C[r, sig[B[k]]] for k in range(20)] for r in range(20)])   # columns = B-coords of g(B_k)
    # B-coord column v -> A v. Z-basis rows z_i: image column A z_i^T; Z-coords y with y Zm = (A z_i^T)^T
    M = (A*Zm.transpose()).transpose()*Zinv
    assert all(M[i, j].q == 1 for i in range(20) for j in range(20)), 'g not integral on N'
    return flint.fmpz_mat([[int(M[i, j]) for j in range(20)] for i in range(20)])
# discriminant group of N via Smith form: D = s GZ t
D_, s_, t_ = smith_normal_decomp(Matrix(GZi.tolist()), domain=ZZ)
dg = [abs(int(D_[i, i])) for i in range(20)]
print('Smith invariants of N:', [x for x in dg if x != 1])
tq = flint.fmpq_mat([[int(x) for x in row] for row in t_.tolist()]); assert s_*Matrix(GZi.tolist())*t_ == D_
gens = [(i, dg[i]) for i in range(20) if dg[i] != 1]
genvec = [[tq[k, i]/dg[i] for k in range(20)] for i, _ in gens]     # columns of t / d_i, as Z-coord vectors in N*
GZq = flint.fmpq_mat(GZ)
def bil(x, y): return sum(x[a]*GZq[a, b]*y[b] for a in range(20) for b in range(20))
for (i, d), v in zip(gens, genvec): print(f'  generator of order {d}: q = {bil(v, v)} (mod 2)')
# all elements of A_N as coefficient tuples
orders = [d for _, d in gens]
def combo(cs): return [sum(c*v[k] for c, v in zip(cs, genvec)) for k in range(20)]
def qmod2(x):
    v = bil(x, x); return Fr(int(v.p), int(v.q)) % 2
elems = list(itertools.product(*[range(d) for d in orders]))
qN = {e: qmod2(combo(e)) for e in elems}
# T = diag(2,32): A_T = <e/2> x <f/32>, q_T(a,b) = a^2/2 + b^2/32 mod 2
qT = lambda a, b: (Fr(a*a, 2) + Fr(b*b, 32)) % 2
Telems = [(a, b) for a in range(2) for b in range(32)]
# anti-isometries gamma: A_N -> A_T (A_N gens (order 2, order 32) expected)
assert sorted(orders) == [2, 32], orders
o2, o32 = orders.index(2), orders.index(32)
def addT(x, y): return ((x[0]+y[0]) % 2, (x[1]+y[1]) % 32)
def mulT(k, x): return ((k*x[0]) % 2, (k*x[1]) % 32)
gammas = []
for im2 in Telems:
    for im32 in Telems:
        img = {}
        for e in elems:
            y = addT(mulT(e[o2], im2), mulT(e[o32], im32)); img[e] = y
        if len(set(img.values())) != 64: continue
        if all(qT(*img[e]) == (-qN[e]) % 2 for e in elems): gammas.append(img)
print('anti-isometries A_N -> A_T:', len(gammas))
# check: every holomorphic g acts on A_N as eps = +-1 and eps = det(M)/c (action on the 2-form)
def act_AN(gm, e):
    x = combo(e); y = [sum(x[a]*gm[a, b] for a in range(20)) for b in range(20)]   # row convention
    for e2 in elems:
        z = combo(e2)
        if all(((y[k]-z[k]).q == 1) for k in range(20)): return e2
gmats = {name: gZ(sig) for name, c, M, sig in S}
for name, c, M, sig in S:
    gm = gmats[name]
    acts = {e: act_AN(gm, e) for e in [tuple(1 if k == j else 0 for k in range(2)) for j in range(2)]}
    neg = lambda e: tuple((-x) % d for x, d in zip(e, orders))
    eps = 1 if all(acts[e] == e for e in acts) else (-1 if all(acts[e] == neg(e) for e in acts) else None)
    om = qdet(M)/c
    print(f'  {name}: g on A_N = {eps};  det(M)/c = {om};  agree: {eps is not None and om == Q2(eps)}')
    assert eps is not None and om == Q2(eps)
# ---- per real structure ----
def kernel_Z(A):
    """Z-basis of {x row in Z^m : x A = 0} for integer m x k matrix A (flint)."""
    m, k = A.nrows(), A.ncols()
    Aug = flint.fmpz_mat([[int(A[i, j]) for j in range(k)] + [1 if i == jj else 0 for jj in range(m)] for i in range(m)])
    Hh = Aug.hnf()
    return [[int(Hh[i, k+j]) for j in range(m)] for i in range(m) if all(Hh[i, j] == 0 for j in range(k))]
out = {}
for d in res:
    name = d['rep']; gm = gmats[name]; sig = d['sig']
    trNS = sum(int(gm[i, i]) for i in range(20))
    chi = 2 - trNS
    eps = 1 if all(act_AN(gm, e) == e for e in elems[:3]) else -1
    sT = [1, -1] if eps == 1 else [-1, 1]          # sigma on T must act on A_T as -eps (scalar), trace 0
    results = set()
    for gam in gammas:
        # overlattice H in Q^22 = (Z-coords of N) + (coords of e, f)
        lifts = []
        for e in [tuple(1 if k == j else 0 for k in range(2)) for j in range(2)]:
            a, b = gam[e]
            lifts.append(combo(e) + [flint.fmpq(a, 2), flint.fmpq(b, 32)])
        vecs = [[flint.fmpq(1 if i == j else 0) for j in range(22)] for i in range(22)] + lifts
        dd = 64
        Hint = flint.fmpz_mat([[int(v*dd) for v in row] for row in vecs]).hnf()
        Hb = flint.fmpq_mat([[flint.fmpq(int(Hint[i, j]), dd) for j in range(22)] for i in range(22)])
        Gfull = flint.fmpq_mat(22, 22)
        for i in range(20):
            for j in range(20): Gfull[i, j] = GZq[i, j]
        Gfull[20, 20] = 2; Gfull[21, 21] = 32
        GH = Hb*Gfull*Hb.transpose()
        assert all(GH[i, j].q == 1 for i in range(22) for j in range(22)), 'H not integral'
        GHi = flint.fmpz_mat([[int(GH[i, j]) for j in range(22)] for i in range(22)])
        assert abs(GHi.det()) == 1 and all(int(GHi[i, i]) % 2 == 0 for i in range(22)), 'H not even unimodular'
        Sig = flint.fmpq_mat(22, 22)
        for i in range(20):
            for j in range(20): Sig[i, j] = -gm[i, j]
        Sig[20, 20] = sT[0]; Sig[21, 21] = sT[1]
        SH = Hb*Sig*Hb.inv()
        assert all(SH[i, j].q == 1 for i in range(22) for j in range(22)), 'sigma not integral on H'
        SHi = flint.fmpz_mat([[int(SH[i, j]) for j in range(22)] for i in range(22)])
        assert SHi*SHi == flint.fmpz_mat([[1 if i == j else 0 for j in range(22)] for i in range(22)])
        tr = sum(int(SHi[i, i]) for i in range(22))
        I22 = flint.fmpz_mat([[1 if i == j else 0 for j in range(22)] for i in range(22)])
        K = kernel_Z(SHi - I22); r = len(K)
        Km = flint.fmpz_mat(K); GK = Km*GHi*Km.transpose()
        Dk, sk, tk = smith_normal_decomp(Matrix(GK.tolist()), domain=ZZ)
        dk = [abs(int(Dk[i, i])) for i in range(r)]
        nontriv = [x for x in dk if x != 1]
        two_el = all(x == 2 for x in nontriv); a = len(nontriv)
        # delta: 0 iff q(x) in Z for all x in discriminant group (2-elementary: suffices on generators)
        tkq = flint.fmpq_mat([[int(x) for x in row] for row in tk.tolist()]); assert sk*Matrix(GK.tolist())*tk == Dk; GKq = flint.fmpq_mat(GK)
        delta = 0
        for i in range(r):
            if dk[i] == 1: continue
            v = [tkq[k, i]/dk[i] for k in range(r)]
            qv = sum(v[x]*GKq[x, y]*v[y] for x in range(r) for y in range(r))
            if qv.q != 1: delta = 1
        # F2 cross-check of a: rank of (1 + sigma) mod 2
        Mm = SHi + I22
        a2 = flint.nmod_mat([[int(Mm[i, j]) % 2 for j in range(22)] for i in range(22)], 2).rank()
        results.add((tr, r, a, two_el, delta, a2))
    assert len(results) == 1, ('gluing-dependent!', results)
    tr, r, a, two_el, delta, a2 = results.pop()
    # Nikulin / Kharlamov: X_R = S_g + k S^2 with g = (22-r-a)/2, k = (r-a)/2, except (10,10,0) empty, (10,8,0) two tori
    if (r, a, delta) == (10, 10, 0): top = 'empty'
    elif (r, a, delta) == (10, 8, 0): top = '2 tori'
    else: top = f'S_{(22-r-a)//2} + {(r-a)//2} S^2'
    out[name] = dict(trNS=trNS, chi_lef=chi, eps=eps, sigmaT=sT, tr_sigma_H2=tr, r=r, a=a, delta=delta, two_elem=two_el, a_F2=a2, top=top,
                     chi_from_rad=2*r-20, betti_F2=24-2*a)
    print(f'{name}: tr(g|NS)={trNS}  chi(Lefschetz)={chi}  g on T: eps={eps}  sigma on T={sT}  tr(sigma*|H2)={tr} (2+tr={2+tr})'
          f'  L+: r={r} a={a} (F2 rank of 1+sigma: {a2}) 2-elementary={two_el} delta={delta}  => {top}; total F2-Betti of X_R = {24-2*a}')
pickle.dump(out, open('s2_lattice.pkl', 'wb'))
