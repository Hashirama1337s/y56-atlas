# Task C (NUMERICAL): at the wall member (1,2,-1), the sigma_g-real nodes: real Hessian signature in sister coordinates
# (definite = an isolated real point = a sphere component shrinks to it; indefinite = a handle/neck pinches), and, for g12,
# where those nodes sit relative to the msolve-certified separating levels of the three Y56 spheres.
import sys, pickle, numpy as np
sys.path.insert(0, '../../core/code/sisters')
src = open('c_family.py').read().split('# --- (2) mesh')[0]
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()): exec(src)
gen = {}
for k in ('g12_g13', 'g01_g02_g24_g00'):
    gen.update(pickle.load(open('b_gen_%s.pkl' % k, 'rb')))
sep = pickle.load(open('b_sep_g12_g13.pkl', 'rb'))
Fw = Ffam(1, 2, -1)
for d in res:
    g = d['rep']; M = np.array([[float(x) for x in row] for row in d['M']])
    A = np.array(gen[g]['A'].evalf(30).tolist(), dtype=complex)
    Xs = np.random.default_rng(0).normal(size=(4, 2000)); Fv = Fw(A @ Xs); ph = Fv[np.argmax(abs(Fv))]/abs(Fv[np.argmax(abs(Fv))])
    Gr = lambda xx: (Fw(A @ xx)/ph).real
    out = []
    for n in nodes:
        if np.linalg.matrix_rank(np.column_stack([M @ n, n]), tol=1e-8) != 1: continue
        xe = np.linalg.solve(A, n.astype(complex)); k = np.argmax(abs(xe)); xe = (xe/(xe[k]/abs(xe[k]))).real; xe /= np.linalg.norm(xe)
        H = np.empty((4, 4)); e = np.eye(4); hh = 1e-4
        for i in range(4):
            for j in range(4):
                H[i, j] = (Gr(xe+hh*e[i]+hh*e[j]) - Gr(xe+hh*e[i]-hh*e[j]) - Gr(xe-hh*e[i]+hh*e[j]) + Gr(xe-hh*e[i]-hh*e[j]))/(4*hh*hh)
        T = np.linalg.svd(xe[None, :])[2][1:].T; ev = np.linalg.eigvalsh(T.T @ H @ T)
        sig = 'definite (sphere shrinks to a point)' if (ev > 0).all() or (ev < 0).all() else 'indefinite (neck pinch)'
        extra = ''
        if g in sep:
            Q = sep[g]['Q']; t1, t2 = [float(t) for t in sep[g]['ts']]; qv = xe @ Q @ xe
            extra = f'; separating form q = {qv:.3f} (region {0 if qv < t1 else (1 if qv < t2 else 2)}; thresholds {t1:.3f}, {t2:.3f})'
        out.append(sig + extra)
    print(f'{g}: {len(out)} real nodes'); [print('    ', o) for o in out]
