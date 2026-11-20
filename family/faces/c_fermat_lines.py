# Task C extra (NUMERICAL): the 48 lines of the Fermat-type member F0 (b = 0) and how many are real for each sister sigma_g;
# plus the lines that persist along the whole pencil (planes z1 = 0 and z2 = 0: F = 4 z0 z3 (z0^2 - z3^2) there).
import sys, itertools, numpy as np, contextlib, io
sys.path.insert(0, '../../core/code/sisters')
src = open('c_fermat.py').read().split("reps = [d['rep']")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
z = np.exp(1j*np.pi*np.array([1, 3, 5, 7])/4)          # zeta^4 = -1
lines = []                                              # each line: 2 spanning vectors in y coords
for (i, j), (k, l) in [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]:
    for a in z:
        for b in z:
            u = np.zeros(4, complex); v = np.zeros(4, complex)
            u[j] = 1; u[i] = a; v[l] = 1; v[k] = b       # y_i = a y_j, y_k = b y_l
            lines.append(np.column_stack([T @ u, T @ v]))
P = np.random.default_rng(5).normal(size=(2, 6))
print('lines on F0:', len(lines), ' all on F0:', all(np.allclose(F0(Lm @ P), 0, atol=1e-9) for Lm in lines))
def same(L1, L2): return np.linalg.matrix_rank(np.hstack([L1, L2]), tol=1e-8) == 2
for d in res:
    M = G[d['rep']]
    nreal = sum(1 for Lm in lines if same(M @ Lm.conj(), Lm))
    print(f"{d['rep']}: sigma_g-real lines on the Fermat-type member: {nreal}   (on Y56: {len(d['fixed'])})")
# persistent lines: z2 = 0, z0 z3 (z0^2 - z3^2) = 0 and z1 = 0 likewise (8 lines through (0:1:0:0), (0:0:1:0))
pers = []
for zero in (1, 2):
    for r in [(1, 0), (0, 1), (1, 1), (1, -1)]:        # (z0, z3) direction with z0 z3 (z0^2 - z3^2) = 0
        u = np.zeros(4, complex); u[0], u[3] = r; v = np.zeros(4, complex); v[3 - zero] = 1
        pers.append(np.column_stack([u, v]))
def fam(a, b, c):
    return lambda zz: a*(4*zz[0]**3*zz[3] - 4*zz[0]*zz[3]**3) + 2*zz[1]*zz[2]*(b*(zz[0]**2 + zz[3]**2) + c*(zz[1]**2 + zz[2]**2))
print('8 persistent lines lie on members (1,b,c) for random b,c:', all(np.allclose(fam(1, bb, cc)(Lm @ P), 0) for Lm in pers for bb, cc in [(0.3, -1.7), (2.2, 0.4)]))
for d in res:
    M = G[d['rep']]
    print(f"{d['rep']}: sigma_g-real persistent lines: {sum(1 for Lm in pers if same(M @ Lm.conj(), Lm))}")
