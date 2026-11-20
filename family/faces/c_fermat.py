# Task C (NUMERICAL, finite exhaustive check): at the Fermat-type member F0 = Im(w^4) - Im(p^2)|p|^2 of the symmetric pencil
# (b = 0, kappa = 0; complex form 4 z0 z3 (z0^2 - z3^2) - 2 z1 z2 (z1^2 + z2^2), projectively the Fermat quartic), the 32 maps
# of Y56 are still automorphisms and every sigma_g = g o conj is still a real structure.  Aut(F0) = T Aut(Fermat) T^-1 has
# order 1536.  Which of the six Y56 real-structure classes become isomorphic on F0?  sigma_g ~ sigma_g'  iff  h g conj(h)^-1 ~ g'
# for some h in Aut(F0) (projectively).
import sys, pickle, itertools, numpy as np
sys.path.insert(0, '../../core/code/sisters')
res = pickle.load(open('../../core/code/sisters/s1_group.pkl', 'rb'))['res']
def F0(z):
    z0, z1, z2, z3 = z
    return 4*z0*z3*(z0**2 - z3**2) - 2*z1*z2*(z1**2 + z2**2)
def binary_to_fermat(fb):
    """2x2 S with fb(S (u,v)) = alpha (u^4 + v^4); fb(t,1) roots by numpy"""
    tgt = [np.exp(1j*np.pi*(2*k+1)/4) for k in range(4)]   # roots of u^4 + v^4 in u/v
    # roots of fb in projective coords: brute force via polynomial in t = x/y and check infinity
    rng = np.random.default_rng(0)
    for perm in itertools.permutations(range(4)):
        pass
    return None
def mobius_from(src, dst):
    """2x2 matrix sending three points src (complex or np.inf) to dst."""
    def to01inf(p):   # matrix sending p0,p1,p2 -> 0, inf, 1
        a, b, c = p
        def col(x): return np.array([x, 1.0]) if x != np.inf else np.array([1.0, 0.0])
        A = np.column_stack([col(a), col(b)]); k = np.linalg.solve(A, col(c))
        return np.linalg.inv(A @ np.diag(k))   # inverse sends a->[1,0]?? handled below
    # build generic: matrix M_s with M_s * src_i ~ e_i pattern
    def std(p):
        def col(x): return np.array([x, 1.0], dtype=complex) if x != np.inf else np.array([1.0, 0.0], dtype=complex)
        A = np.column_stack([col(p[0]), col(p[1])]); k = np.linalg.solve(A, col(p[2]))
        return A @ np.diag(k)          # sends [1,0]->p0, [0,1]->p1, [1,1]->p2
    return std(dst) @ np.linalg.inv(std(src))
def act(Mb, t):
    v = Mb @ (np.array([t, 1.0], dtype=complex) if t != np.inf else np.array([1.0, 0.0], dtype=complex))
    return np.inf if abs(v[1]) < 1e-12*abs(v[0]) else v[0]/v[1]
# blocks: w-block coords (z0,z3) with f = 4 z0 z3 (z0^2 - z3^2), roots z0/z3 in {0, inf, 1, -1}
# p-block coords (z1,z2) with g = -2 z1 z2 (z1^2 + z2^2), roots z1/z2 in {0, inf, i, -i}
tgt = [np.exp(1j*np.pi*(2*k+1)/4) for k in range(4)]
def block_map(roots, fb):
    for perm in itertools.permutations(range(4)):
        S = mobius_from([tgt[perm[0]], tgt[perm[1]], tgt[perm[2]]], roots[:3])   # u/v -> block ratio
        if np.isclose(act(S, tgt[perm[3]]), roots[3]) if roots[3] != np.inf else act(S, tgt[perm[3]]) == np.inf:
            # check fb(S(u,v)) proportional to u^4 + v^4
            P = np.random.default_rng(1).normal(size=(2, 30)) + 1j*np.random.default_rng(2).normal(size=(2, 30))
            vals = np.array([fb(*(S @ P[:, k])) for k in range(30)]); ref = P[0]**4 + P[1]**4
            al = vals[0]/ref[0]
            if np.allclose(vals, al*ref, rtol=1e-9): return S, al
    raise RuntimeError('no harmonic match')
Sw, aw = block_map([0, np.inf, 1, -1], lambda z0, z3: 4*z0*z3*(z0**2 - z3**2))
Sp, ap = block_map([0, np.inf, 1j, -1j], lambda z1, z2: -2*z1*z2*(z1**2 + z2**2))
Sw = Sw/aw**0.25; Sp = Sp/ap**0.25
T = np.zeros((4, 4), dtype=complex)        # z = T y,  y Fermat coords (y0,y1 <- w block; y2,y3 <- p block)
T[np.ix_([0, 3], [0, 1])] = Sw; T[np.ix_([1, 2], [2, 3])] = Sp
P = np.random.default_rng(3).normal(size=(4, 50)) + 1j*np.random.default_rng(4).normal(size=(4, 50))
print('F0(T y) == sum y^4 :', np.allclose(F0(T @ P), np.sum(P**4, axis=0), rtol=1e-9))
Ti = np.linalg.inv(T)
aut = []
for perm in itertools.permutations(range(4)):
    Pm = np.eye(4)[list(perm)]
    for ks in itertools.product(range(4), repeat=3):
        D = np.diag([1] + [1j**k for k in ks])
        aut.append(T @ Pm @ D @ Ti)
print('Aut(F0) elements built:', len(aut))
ok = all(np.allclose(F0(h @ P[:, :8]) / F0(P[:, :8]), (F0(h @ P[:, :8]) / F0(P[:, :8]))[0]) for h in aut)
print('all preserve F0 up to scalar:', ok)
G = {d['rep']: np.array([[float(x) for x in row] for row in d['M']]) for d in res}
for nm, M in G.items():
    r = F0(M @ P[:, :8])/F0(P[:, :8]); assert np.allclose(r, r[0]), nm
print('the 32-group reps act on F0 with constant character: True')
def proj_eq(A, B):
    k = np.unravel_index(np.argmax(abs(B)), B.shape); lam = A[k]/B[k]
    return abs(lam) > 1e-9 and np.allclose(A, lam*B, atol=1e-8*np.abs(A).max())
# all 15 involutions + identity, by class
S_all = {}
sys.path.insert(0, '../../core/code/sisters')
from q2 import load_syms
for nm, c, M, _ in load_syms(): S_all[nm] = np.array([[float(x) for x in row] for row in M])
reps = [d['rep'] for d in res]; members = {d['rep']: d['members'] for d in res}
iso = {}
for a in reps:
    for b in reps:
        if a >= b: continue
        found = any(proj_eq(h @ G[a] @ np.linalg.inv(h.conj()), S_all[m]) for h in aut for m in members[b])
        iso[(a, b)] = found
        print(f'on F0: sigma_{a} isomorphic to sigma_{b}: {found}')
# classes on F0
cls = []
for a in reps:
    for c_ in cls:
        if iso.get(tuple(sorted((a, c_[0]))), False): c_.append(a); break
    else: cls.append([a])
print('Y56 real-structure classes merged on the Fermat-type member:', cls)
