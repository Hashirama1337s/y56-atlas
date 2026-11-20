# Round 2, task 2 (EXACT).  (a) explicit projective equivalence F0 ~ Fermat over K = Q(zeta8)(r), r^2 = 1 - i;
# (b) exhaustive twisted-conjugacy test of the 6 transported real structures under Aut(Fermat) (order 1536), exact in K;
# (c) exact sigma_g-real node counts of the wall quartic (nodes in Q(t), t^4 - 4t^2 + 2 = 0, t = 2cos(pi/8)).
import sys, pickle, itertools, cmath, math
from fractions import Fraction as Fr
import sympy as sp
sys.path.insert(0, '../../core/code/sisters')
from q2 import load_syms
SY = {nm: (c, M) for nm, c, M, _ in load_syms()}
res = pickle.load(open('../../core/code/sisters/s1_group.pkl', 'rb'))['res']
classes = {d['rep']: d['members'] for d in res}

# ---------------- (a) sympy: Fermat(A z) == 4 F0(z) ----------------
z0, z1, z2, z3, Z, r = sp.symbols('z0 z1 z2 z3 zeta r')
I_ = Z**2
F0 = 4*z0*z3*(z0**2 - z3**2) - 2*z1*z2*(z1**2 + z2**2)
Ay = [r*z0 + I_*r*z3, Z*r*z0 - I_*Z*r*z3, z1 - z2, Z*z1 + Z*z2]
expr = sp.expand(sum(y**4 for y in Ay) - 4*F0)
P = sp.Poly(expr, z0, z1, z2, z3)
ok = True
for mon, co in P.terms():
    c2 = sp.rem(sp.rem(sp.expand(co), r**2 - (1 - Z**2), r), Z**4 + 1, Z)
    if sp.expand(c2) != 0: ok = False
print('(a) y = A z with y0 = r(z0 + i z3), y1 = zeta8 r (z0 - i z3), y2 = z1 - z2, y3 = zeta8 (z1 + z2),  r^2 = 1 - i:')
print('    y0^4 + y1^4 + y2^4 + y3^4 - 4 F0(z) reduces to 0 in K[z]:', ok)
Amat = sp.Matrix([[sp.Poly(sp.expand(y), z0, z1, z2, z3).coeff_monomial(v) for v in (z0, z1, z2, z3)] for y in Ay])
detA = sp.expand(Amat.det()); detA = sp.rem(sp.rem(detA, r**2 - (1 - Z**2), r), Z**4 + 1, Z)
print('    det A (reduced) =', sp.factor(detA), ' (nonzero)')

# ---------------- exact field K = Q(zeta)[r]/(r^2 - 1 + zeta^2), zeta^4 = -1 ----------------
def kz(): return [Fr(0)]*8
def kred(acc):           # acc: dict (n, k) -> Fr with any n, k in {0,1,2}
    out = kz()
    for (n, k), v in acc.items():
        if v == 0: continue
        terms = [(n, k, v)]
        if k == 2: terms = [(n, 0, v), (n + 2, 0, -v)]       # r^2 = 1 - zeta^2
        for (nn, kk, vv) in terms:
            nn %= 8; s = 1
            if nn >= 4: nn -= 4; s = -1
            out[nn + 4*kk] += s*vv
    return tuple(out)
def kmul(a, b):
    acc = {}
    for i, x in enumerate(a):
        if x == 0: continue
        for j, y in enumerate(b):
            if y == 0: continue
            key = (i % 4 + j % 4, i // 4 + j // 4); acc[key] = acc.get(key, 0) + x*y
    return kred(acc)
def kadd(a, b): return tuple(x + y for x, y in zip(a, b))
def kneg(a): return tuple(-x for x in a)
def kconst(q): o = list(kz()); o[0] = Fr(q); return tuple(o)
def kmono(n, k=0, c=1): return kred({(n, k): Fr(c)})
ZERO = tuple(kz()); ONE = kconst(1)
def kconj(a):             # zeta -> zeta^-1, r -> zeta r
    acc = {}
    for i, x in enumerate(a):
        if x: j, k = i % 4, i // 4; acc[(-j + k, k)] = acc.get((-j + k, k), 0) + x
    return kred(acc)
def kinv(a):
    # solve (mult-by-a) x = 1 over Q
    cols = [kmul(a, tuple(Fr(1 if t == s else 0) for t in range(8))) for s in range(8)]
    M = [[cols[s][t] for s in range(8)] + [Fr(1 if t == 0 else 0)] for t in range(8)]
    for c in range(8):
        p = next(i for i in range(c, 8) if M[i][c] != 0); M[c], M[p] = M[p], M[c]
        pv = M[c][c]; M[c] = [x/pv for x in M[c]]
        for i in range(8):
            if i != c and M[i][c] != 0:
                f = M[i][c]; M[i] = [x - f*y for x, y in zip(M[i], M[c])]
    return tuple(M[i][8] for i in range(8))
def knum(a):
    zt = cmath.exp(1j*math.pi/4); rr = 2**0.25*cmath.exp(-1j*math.pi/8)
    return sum(float(a[i])*zt**(i % 4)*rr**(i//4) for i in range(8))
# sanity of conj = complex conjugation in the embedding zeta = e^{i pi/4}, r = 2^{1/4} e^{-i pi/8}
import random; random.seed(1)
for _ in range(20):
    a = tuple(Fr(random.randint(-5, 5)) for _ in range(8)); b = tuple(Fr(random.randint(-5, 5)) for _ in range(8))
    assert abs(knum(kconj(a)) - knum(a).conjugate()) < 1e-9
    assert kconj(kmul(a, b)) == kmul(kconj(a), kconj(b))
    if any(a): assert kmul(a, kinv(a)) == ONE
print('    K arithmetic: conj is a field automorphism equal to complex conjugation (20 random checks); inverses exact')
SQ2 = kadd(kmono(1), kneg(kmono(3)))            # sqrt2 = zeta - zeta^3
assert kmul(SQ2, SQ2) == kconst(2)
def q2k(x): return kadd(kconst(x.a), kmul(kconst(x.b), SQ2))
def mmul(A, B): return [[ (lambda i, j: __import__('functools').reduce(kadd, [kmul(A[i][k], B[k][j]) for k in range(4)]))(i, j) for j in range(4)] for i in range(4)]
def mconj(A): return [[kconj(x) for x in row] for row in A]
iK = kmono(2); zK = kmono(1); rK = kmono(0, 1)
A = [[rK, ZERO, ZERO, kmul(iK, rK)], [kmul(zK, rK), ZERO, ZERO, kneg(kmul(iK, kmul(zK, rK)))],
     [ZERO, ONE, kneg(ONE), ZERO], [ZERO, zK, zK, ZERO]]
half = kconst(Fr(1, 2)); ri = kinv(rK); zi = kinv(zK); ii = kinv(iK)
Ainv = [[kmul(half, ri), kmul(half, kmul(zi, ri)), ZERO, ZERO],
        [ZERO, ZERO, half, kmul(half, zi)],
        [ZERO, ZERO, kneg(half), kmul(half, zi)],
        [kmul(kmul(half, ii), ri), kneg(kmul(kmul(half, ii), kmul(zi, ri))), ZERO, ZERO]]
Id = [[ONE if i == j else ZERO for j in range(4)] for i in range(4)]
assert mmul(A, Ainv) == Id and mmul(Ainv, A) == Id
print('    A^-1 exact (A A^-1 = I in K)')
cAinv = mconj(Ainv)
def Nmat(name):
    c, M = SY[name]; G = [[q2k(x) for x in row] for row in M]
    return mmul(mmul(A, G), cAinv)
def normalize(X):
    k = next((i, j) for i in range(4) for j in range(4) if any(X[i][j]))
    inv = kinv(X[k[0]][k[1]])
    return tuple(tuple(kmul(inv, x) for x in row) for row in X)
invols = sorted(set(m for v in classes.values() for m in v))
Nn = {m: Nmat(m) for m in invols}
# sanity: each N is a real structure on P^3 (N conj(N) proportional to I) preserving Fermat (checked via H-orbit below)
for m in invols:
    P_ = normalize(mmul(Nn[m], mconj(Nn[m])))
    assert P_ == normalize(Id), m
print('    every transported sigma_g satisfies N conj(N) ~ I exactly (15 involutions + identity)')
target = {normalize(Nn[m]): m for m in invols}
assert len(target) == len(invols)
# ---------------- (b) Aut(Fermat): monomial H = P D, D = diag(1, i^a, i^b, i^c) ----------------
def apply(H_perm, H_exp, N):
    # H = P D with (H y)_i = i^{e_pi(i)} y_{pi(i)} realised as matrix H[i][perm[i]] = zeta^{2 e}
    H = [[ZERO]*4 for _ in range(4)]
    for i in range(4): H[i][H_perm[i]] = kmono(2*H_exp[i])
    Hinv_c = [[ZERO]*4 for _ in range(4)]          # conj(H)^-1 = conj(H^-1); H^-1[perm[i]][i] = zeta^{-2e}
    for i in range(4): Hinv_c[H_perm[i]][i] = kconj(kmono(-2*H_exp[i]))
    return mmul(mmul(H, N), Hinv_c)
autos = [(p, (0,) + e) for p in itertools.permutations(range(4)) for e in itertools.product(range(4), repeat=3)]
print('(b) |Aut(Fermat)| projective =', len(autos))
reps = [d['rep'] for d in res]
hits = {}
for a in reps:
    for (p, e) in autos:
        X = normalize(apply(p, e, Nn[a]))
        if X in target:
            b = next(rr for rr in reps if target[X] in classes[rr])
            hits[(a, b)] = hits.get((a, b), 0) + 1
for a in reps:
    print('   ', a, '->', {b: hits[(a, b)] for b in reps if (a, b) in hits})
# classes
cls = []
for a in reps:
    for c_ in cls:
        if (a, c_[0]) in hits: c_.append(a); break
    else: cls.append([a])
print('    EXACT classes of the transported real structures on the Fermat member:', cls)

# ---------------- (c) wall nodes, exact in Q(t) ----------------
t = sp.symbols('t'); mp = t**4 - 4*t**2 + 2; s2 = t**2 - 2
def red(e): return sp.rem(sp.expand(e), mp, t)
assert red(s2**2 - 2) == 0
tinv = -(t**3 - 4*t)/2; assert red(t*tinv - 1) == 0
nodes = []
for e in (1, -1):
    u = t if e == 1 else s2*tinv
    v = s2*tinv if e == 1 else t
    for sg in (1, -1):
        nodes.append([1 + e*s2, -sg*u, sg*u, sp.Integer(1)])        # component z1 = -z2
        nodes.append([-1 + e*s2, sg*v, sg*v, sp.Integer(1)])         # component z1 = z2
def clear(vv):    # replace 1/t by -(t^3 - 4t)/2
    return [red(x) for x in vv]
nodes = [clear(n) for n in nodes]
W = 4*z0**3*z3 - 4*z0*z3**3 + 4*z1*z2*(z0**2 + z3**2) - 2*z1*z2*(z1**2 + z2**2)
grads = [sp.diff(W, v) for v in (z0, z1, z2, z3)]
for n in nodes:
    sub = dict(zip((z0, z1, z2, z3), n))
    assert all(red(g.subs(sub)) == 0 for g in grads), n
print('(c) 8 nodes, exact in Q(t), t = 2cos(pi/8): all gradients vanish exactly; numeric:')
tv = 2*math.cos(math.pi/8)
for n in nodes: print('    ', [round(float(sp.lambdify(t, x)(tv)), 6) for x in n], '   exact:', n)
assert len(set(tuple(round(float(sp.lambdify(t, x)(tv)), 9) for x in n) for n in nodes)) == 8
def q2t(x): return x.a + x.b*s2
for g in reps:
    c, M = SY[g]
    Mt = [[q2t(x) for x in row] for row in M]
    cnt = 0
    for n in nodes:
        gn = [sum(sp.nsimplify(Mt[i][j])*n[j] for j in range(4)) for i in range(4)]
        prop = all(red(gn[i]*n[j] - gn[j]*n[i]) == 0 for i in range(4) for j in range(4))
        cnt += prop
    print(f'    {g}: sigma_g-real wall nodes (g n ~ n, n real) = {cnt}')
